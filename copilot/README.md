# copilot

The bot-management surface of **Copilot Studio** (formerly Power Virtual Agents): reading and writing a bot's Application Insights configuration, reached through each environment's own PowerVirtualAgents runtime endpoint.

Two operations, one path. That is not a summary of the API — it is the whole of what is *knowable*. There is no published reference, no discovery document, and unrecognised routes answer with a bare 404 and no body, so nothing beyond what a real client is observed doing can be found by poking. The source of truth is the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform) (`internal/clients/copilot`), itself derived from Copilot Studio UI traffic recordings, probed here against a live tenant.

## Three things that will trip you up

### 1. The host is per environment, and you cannot compose it

Every other Power Platform boundary has a fixed host (`api.bap.microsoft.com`) or a regional one you can build from a location name. This one has neither. The host is an **opaque per-environment gateway hostname** assigned by whichever scale unit the environment landed on — `powervamg.<something>.gateway.prod.island.powerapps.com` — and the `<something>` is a scale-unit identifier, not a region code. You look it up:

```
GET https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/scopes/admin
    /environments/{environmentId}?api-version=2023-06-01&$expand=properties

-> properties.runtimeEndpoints["microsoft.PowerVirtualAgents"]
```

See [bapi](../bapi) for that read. `runtimeEndpoints` carries a sibling endpoint for each service that has a per-environment presence (`microsoft.PowerApps`, `microsoft.Flow`, `microsoft.CommonDataModel`, `microsoft.PowerAppsAdvisor`, …); Copilot Studio's is the `microsoft.PowerVirtualAgents` entry, under its pre-rename name.

Guessing is not merely unreliable, it fails at the network layer: a plausible-looking hostname with a scale-unit number that does not exist has no DNS record at all. Environments sharing a scale unit share a host, and one tenant's environments routinely span several — in the probe tenant, thirteen environments resolved to two distinct hosts. The spec models this as a `pvaRuntimeHost` server variable.

The environment id in the path and the host must agree. A gateway serves the environments on its own scale unit.

### 2. `x-cci-tenantid` is mandatory

Every call carries the environment's Entra tenant id in an `x-cci-tenantid` header. It is *not* inferred from the bearer token, it is spelled lower-case, and it is the single easiest thing to leave out — nothing about the URL suggests it exists.

(A Go footnote, since the reference client is Go: the provider sets the header via a literal lower-case `http.Header` key. On the wire that is fine, but reading it back with `Header.Get` canonicalises to `X-Cci-Tenantid` and misses it. Its own tests read the raw map.)

### 3. Bots are Dataverse rows, and this API will not list them for you

There is no `GET .../bots`. That path 404s. A `botId` is the primary key of a row in the **`bot` table of the environment's Dataverse organization**, so enumeration goes through the Dataverse Web API instead:

```
GET https://{dataverseHost}/api/data/v9.2/bots?$select=botid,name
```

See [dataverse](../dataverse). Confirmed against a live organization: `bot` is a solution-provisioned custom table — entity set `bots`, primary id `botid`, primary name `name` — carrying roughly thirty columns including `schemaname`, `statecode`/`statuscode`, `componentstate`, `language`, `supportedlanguages`, `authenticationmode`, `template`, `publishedon` and `runtimeprovider`. The table only exists where Copilot Studio has provisioned it; elsewhere the query returns an empty `value` array rather than an error, and an environment with no Dataverse at all cannot host bots.

## Auth, and the licence gate

The scope is the fixed first-party application id of the Copilot Studio service, `96ff4394-9197-43aa-b393-6a41652e21f8/.default`. Unlike its siblings there is no `https://` resource-URI form and no per-cloud variation — the provider hardcodes it as a constant rather than reading it from cloud configuration.

**A valid token is necessary but not sufficient.** This is a *maker* surface gated on a **per-user Copilot Studio licence**, and Power Platform tenant-administrator rights do not substitute for it. Without the licence every request is refused:

```
403  {"ErrorCode":4030, "ErrorMessage":"User license not found",
      "Error":{"Code":"UserHasNoLicense", ...}}
```

That check runs *first* — before the tenant header, the environment id and the bot id are examined. An unlicensed caller gets an identical 403 for a valid request, a missing `x-cci-tenantid`, a nonexistent bot and a nonexistent environment alike, which makes the API almost undebuggable until the licence is in place.

## What live probing established, and what it did not

Probed against a real tenant: a real environment, its real PVA host, and a real bot id discovered through Dataverse.

**Verified:**

- the route exists and answers on the resolved per-environment host;
- the auth model — `401` `UnauthenticatedUser` (`ErrorCode` 1000) with no token, `403` `UserHasNoLicense` (`ErrorCode` 4030) with one;
- the **error envelope**, which the provider models not at all: a flat `ErrorCode`/`ErrorMessage`/`ErrorInfo` triple beside a nested `Error` object of `Code`, `Message`, `RetryIn`, `InnerErrors`, `Properties`, `Diagnostics`;
- **`2022-01-15` is a path segment, not an `api-version` query parameter.** An `?api-version=` query string is ignored entirely; a different date in the path 404s. The segment is part of the route;
- unrecognised routes — the `.../bots` collection, `.../bots/{botId}` alone, the host root — return `404` with an **empty body**, not the error envelope;
- the 403 is cluster-independent: identical across both scale units in the tenant.

**Not verified:** both `200` bodies. The probing account was a tenant administrator, but held no Copilot Studio licence — confirmed against its Graph `licenseDetails` — so every request stopped at the gate. The response schema is provider-derived and carries `x-probe-verified: false`.

**Not attempted:** the update. It is a mutation, the probe tenant's only bot is a real user-owned bot, and creating a throwaway one to write against was impossible for the same reason the read failed — bot creation is behind the same licence. `appInsightsConfiguration_update` is documented entirely from the provider client and its unit tests.

## The update's failure modes

Worth stating plainly even though it is unverified, because a naive client gets it wrong twice:

- **`200` does not mean success.** The service reports validation failures *in band*, in an `errors` string on an otherwise normal `200` body. Check that field.
- **`500` is terminal, not transient.** The provider lists 500 among the update's *accepted* statuses precisely to keep its retry layer away from it, then turns it into an error carrying the raw body. A 500 here means the update was rejected. Retrying it does nothing.

The whole object is sent on the way in — `environmentId`, `botId` and an empty `errors` included — not a patch. Both operations echo `environmentId` and `botId` in the response, and the provider overwrites both with the values it asked for rather than trusting what comes back.

## Layout

```
copilot/
  scripts/probe.py     live probe harness (read-only, no code path writes)
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py --discover                        # find bots across the tenant
scripts/probe.py --environment-id <guid>           # resolve host, discover a bot, read + negative probes
scripts/probe.py --environment-id <guid> --bot-id <guid>
```

Ids come from arguments or `PROBE_ENVIRONMENT_ID`/`PROBE_TENANT_ID`/`PROBE_BOT_ID`; auth is the logged-in Azure CLI session. Output is deliberately shape-only — key names and JSON types, environments numbered rather than named — so a run can be pasted somewhere public.

## What the three flags actually control

Worth stating outside the spec, because the names are close enough to be confused:

| Flag | What it logs |
|---|---|
| `includeActivities` | Incoming and outgoing **messages and events** — the conversational transcript's shape and timing. Highest volume. |
| `includeActions` | An event each time a **node within a topic** executes — which topic triggered, which branch was taken, where it stopped. What makes a broken conversation debuggable. |
| `includeSensitiveInformation` | The **content** inside the above rather than only their structure: user id, user name, message text. Off, those properties are stripped; on, end-user text and any Dataverse values the bot has echoed into messages leave the environment's compliance boundary for an Application Insights resource with its own retention, geography and access control. |

The connection string is the master switch — empty stops export regardless of the flags. It is also a write credential for the target resource, so reading this configuration is reading a secret.

## Conventions

- 2 operations over 1 path, 3 schemas, one tag, OpenAPI 3.0.3.
- Summaries are bare verbs (`Read`, `Update`) — the tag names the resource. Status-code meanings live in the response entries, never in the operation description.
- The api-version is baked into the path; there is no version parameter.
- Contracts are in the schema where they could be established: `uuid` format and a GUID `pattern` on all three ids, a `key=value` `pattern` and a neutral placeholder `example` on the connection string, `nullable: true` on the three envelope fields observed as explicit nulls.
- **Two deliberate non-enums.** `ErrorCode` and `Error.Code` carry `x-observed-values` rather than `enum`: the licence gate answered first and hid every other code, so the sets are demonstrably open. `networkIsolation` does carry `enum: ["PublicNetwork"]` — the only value ever evidenced, since the provider hardcodes it on write and every recorded response returns it — but it is marked `x-probe-verified: false` and its description says outright that the real set is probably larger. Treat it as a record of evidence, not a closed contract.
- Nothing is marked `required` in the schemas, and the flags carry no `default` — the service's optionality was never observable. (The Terraform resource defaults all three flags to `true`; that is the provider's choice, not the service's, so it is not in the spec.) The three *parameters* are required: two are path segments, and `x-cci-tenantid` is required on the provider's behaviour.
- `x-probe-verified: true` marks what was confirmed live (the error envelope, the 401/403/404 responses). Its absence, or `false`, means provider-derived; `x-probe-notes` on each operation says exactly which is which.

## Status

Spec written and validated. Read path partially verified against the live service; `200` bodies and the update operation blocked on a per-user Copilot Studio licence the probing account does not hold. Nothing was created and nothing was modified — every request made against this API was a GET.
