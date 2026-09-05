# copilot

The management and authoring surface of **Copilot Studio** (formerly Power Virtual Agents): an agent's Application Insights configuration on the environment's own PowerVirtualAgents runtime endpoint, plus the dialogs, intents, variable types, fallback, provisioning, content, connectors and extensions the Copilot Studio maker portal drives.

**Two of the 44 operations here were executed against a live service. The other 42 were not.** That split is the most important thing on this page, and the spec marks it per operation.

The probed pair reads and writes a bot's Application Insights configuration. There is no published reference for it, no discovery document, and unrecognised routes answer with a bare 404 and no body, so nothing beyond what a real client is observed doing can be found by poking. Its source of truth is the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform) (`internal/clients/copilot`), itself derived from Copilot Studio UI traffic recordings, probed here against a live tenant.

Everything else was read out of the Copilot Studio maker portal's own JavaScript — `main.cb28c5f0.js`, build `0.0.20260903.1-26.08.30-prod`, downloaded 2026-09-05 — and carries `x-source: ppac-spa`. A bundle contains every route the client *can* call, including branches no session exercised, so its coverage is wider than a capture and its confirmation weaker. Nothing sourced that way was sent. **No response body is described anywhere in it**, because the extract records not one response field on any Copilot Studio route.

## Three things that will trip you up on the probed surface

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

## Three hosts, not one

The spec has three `servers`, and no operation is assigned to a host the evidence did not put it on. Collapsing them would be the single easiest way to make this spec confidently wrong.

| Server | What it is | How well known |
|---|---|---|
| `pvaRuntimeHost` | The environment's own PVA gateway, `powervamg.<scale-unit>.gateway.prod.island.powerapps.com` | **Probed.** Looked up from BAPI; see section 1 above. Serves the two Application Insights operations. |
| `botApiHost` | The `baseUrl` the generated Copilot Studio API clients are constructed with. 38 of the 42 bundle routes. | **Unknown.** Injected at client construction from runtime region discovery; never a literal anywhere in 1,027 chunks. Not one concrete value was observed, which is why its server default is a reserved `.invalid` name rather than a plausible-looking host. |
| `copilotStudioRegionalHost` | The `regionUrl` a second client is constructed with. 4 routes. | **Family known, route mapping not.** Candidate hosts exist — `powerva.microsoft.com`, `web.powerva.microsoft.com`, `powerva.appsplatform.us`, `powerva.powervirtualagents.cn`, `copilotstudio.microsoft.com` and the US government pair — but no route was confirmed against any of them. |

The two injected hosts are separate variables in the *same chunk file*, on clients sitting side by side, and the same `/api/botmanagement/v1/environments/{environmentId}/...` prefix appears on both. That is the sharpest reason not to merge them.

### Is `botApiHost` the same machine as `pvaRuntimeHost`?

Unresolved, and left that way in `info.x-host-families`. The evidence pulls both ways:

- **For same:** both serve `/api/botmanagement/...` with the same segment names, one segment different (a date on the gateway, `v1`/`v2` in the bundle). Both carry `CCI`-prefixed headers unique to this boundary — the gateway requires `x-cci-tenantid`, and every `botauthoring` call sets `_X-CCI-Routing-BotId`.
- **For different:** the bundle's clients read as regionally hosted, which describes the `powerva.microsoft.com` family rather than a per-environment gateway.

One request would settle it — a `botauthoring` call against a resolved `pvaRuntimeHost`. It was not made, because nothing added in this pass was executed.

### There is a migration in flight, which is probably why the families coexist

The bundle reads a feature gate named **`BotManagementEndpointMigration2026`** into a field called `convergedAgentEndpointEnabled`, and uses it to select a `convergedEndpointApiClient`. So the client can already choose between the endpoint it has been using and a converged one.

That is a good reason not to read this layout as settled architecture: a date-versioned gateway route, `v1` and `v2` families on an injected host, and an unversioned `chatbotmanagement` family are what a half-finished consolidation looks like. Which family is the converged one, and what its base URL is, are not in the evidence — the flag name and those two field names are the whole of it.

## What the bundle added, and what it could not say

42 operations over 38 paths, in four route families:

| Family | Ops | Host | What it covers |
|---|---|---|---|
| `botauthoring/v1` | 27 | `botApiHost` | Dialogs (topics), intents, variable types, fallback, connection dependencies |
| `botmanagement/v1` | 3 | `botApiHost` | Connector definitions, feedback, the route the client calls `openAIApi` |
| `botmanagement/v1` | 4 | `copilotStudioRegionalHost` | AI Builder models, Copilot plugins, bot components read/write |
| `botmanagement/v2` | 6 | `botApiHost` | Bot create and provisioning status, default template, viral-signup job |
| `chatbotmanagement` | 2 | `botApiHost` | Connector intellisense, Direct Line token |

Things worth knowing before writing against any of it:

- **`etag` is a query parameter, not `If-Match`.** Five routes take concurrency tokens that way. A client written to the HTTP convention will send `If-Match` and be silently ignored.
- **Two headers are written with a leading underscore** — `_X-CCI-Routing-BotId` and `_x-ms-solution-unique-name` — and the options literal then passes through a `transformOptions()` the extract does not contain. Whether the underscore reaches the wire cannot be read from this evidence, so the spec declares the bundle's spelling and says so.
- **`botauthoring` routes carry no bot id in the path.** Dialogs, intents, variable types and fallback are all addressed as if there were one agent; `_X-CCI-Routing-BotId` is what selects it.
- **Two POSTs carry no body**, `provisioningStatus` and `fallback`/add — reads wearing a write's verb. Anything treating POST as unsafe will get them wrong.
- **`content/botcomponents` speaks YAML**, `application/json+yaml` on both `Accept` and `Content-Type`, alongside a header that asks the service to compute component properties. Reproduced exactly as written; that media type is not registered and is not `application/yaml`.
- **`connectorintellisense` swallows every failure.** `if (status >= 300) return null` — an error is indistinguishable from "no completions".

### Verbs: three upgraded, one corrected

The extract binds a verb only when it sits at the same call site as the URL, and four records here go through `transformOptions({method: ...})` first, which its binder does not follow.

- Bound from the evidence string, having been emitted as `method: null`: `GET /api/botmanagement/v2/content/defaultTemplate`, `DELETE .../viral-signup/clear`, `GET .../api/directline/token`.
- **Corrected:** `.../viral-signup/create/status` is recorded as `POST` with confidence `method-bound`, but its own quoted evidence reads `transformOptions({method:"GET", ...})` in the same statement chain as the URL. The spec uses `GET` and records the disagreement on the operation, so anyone reconciling against the extract expects the mismatch.

Records whose evidence carries no method literal at all were **not** guessed. They are out of `paths` entirely and listed in `info.x-adjacent-routes` — which is also where the Copilot Studio bundle's calls to PowerApps, BAPI, PPAPI, Dataverse, `mss.office.com` and `slack.botframework.com` went, since those belong to other boundaries. One of them is worth naming here: **`GET-ish /powervirtualagent/listBots` on `api.powerapps.com`** is a bot *list*, on a fourth host. It does not contradict the probed finding that `.../bots` 404s on `pvaRuntimeHost` — different service — but it is a third answer to "how do I enumerate agents", next to the Dataverse table in section 3.

### What it could not say

- **No response bodies at all.** The extract records `responseFieldsRead: []` for all 57 Copilot Studio records without exception. Every added `200` says the shape is unestablished rather than carrying an invented schema.
- **No auth.** The bundle acquires its token inside `transformOptions()`, which is not in the extract, so the audience for the two injected hosts is unknown. The document-level `security` is confirmed for two operations and assumed for the other 42; the spec says so.
- **Most request bodies.** Fields are modelled only where the bundle serialises them inline — `connectorIds`/`skipCache`, `aiModelIds`, `pluginLookupId`, and the `category` the feedback client validates. (The extract lists `Accept` among `requestBodyFields` on a dozen records; that is the header key picked up from the same options literal, and it is not modelled as a body field.)
- **Live PPAC shows Copilot Studio agents as resource-query rows** carrying `componentsCounts.knowledgeByType`, `channels[]`, `orchestration`, `authentication`, `isWebSearchEnabledForKnowledge`, `sharedWithViewers` and `sharedWithEditors`. No route in this spec manages any of those fields, and no bundle route reads or writes them. They are recorded in `info.x-notes` only so a reader knows they were checked against this surface and do not belong to it.

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

- 44 operations over 39 paths, 3 schemas, thirteen tags, OpenAPI 3.0.3. Two of those operations are the probed pair; the other 42 come from the maker bundle and carry `x-source: ppac-spa`.
- Summaries are bare verbs (`Read`, `Update`) — the tag names the resource. Status-code meanings live in the response entries, never in the operation description.
- No operation anywhere takes an `api-version` query parameter. Versioning is a path segment throughout, but not one scheme: a date on the gateway family, `v1`/`v2` in the bundle families, and none at all on `chatbotmanagement`. `info.x-versioning` lays the four out side by side.
- Contracts are in the schema where they could be established: `uuid` format and a GUID `pattern` on all three ids, a `key=value` `pattern` and a neutral placeholder `example` on the connection string, `nullable: true` on the three envelope fields observed as explicit nulls.
- **Two deliberate non-enums.** `ErrorCode` and `Error.Code` carry `x-observed-values` rather than `enum`: the licence gate answered first and hid every other code, so the sets are demonstrably open. `networkIsolation` does carry `enum: ["PublicNetwork"]` — the only value ever evidenced, since the provider hardcodes it on write and every recorded response returns it — but it is marked `x-probe-verified: false` and its description says outright that the real set is probably larger. Treat it as a record of evidence, not a closed contract.
- Nothing is marked `required` in the schemas, and the flags carry no `default` — the service's optionality was never observable. (The Terraform resource defaults all three flags to `true`; that is the provider's choice, not the service's, so it is not in the spec.) The three *parameters* are required: two are path segments, and `x-cci-tenantid` is required on the provider's behaviour.
- `x-probe-verified: true` marks what was confirmed live (the error envelope, the 401/403/404 responses). Its absence, or `false`, means provider-derived; `x-probe-notes` on each operation says exactly which is which. **Nothing added from the maker bundle carries `x-probe-verified` in any form** — none of it was executed, and marking it `false` would have implied it was tried.

## Status

Spec written and validated. The Application Insights read path is partially verified against the live service; its `200` bodies and the update operation are blocked on a per-user Copilot Studio licence the probing account does not hold. Nothing was created and nothing was modified — every request ever made against this API was a GET.

The other 42 operations are structural evidence from a shipped client and nothing more: routes, verbs, parameters and a few body fields. They have never been sent. Two of the three hosts in this spec are variables nobody has resolved to a value, and a feature gate in the same bundle says the endpoint layout is mid-migration — so treat this surface as a map of what the client can do, not as a contract.
