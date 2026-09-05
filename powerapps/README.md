# powerapps

The PowerApps API (`api.powerapps.com`): the undocumented service behind the Power Apps maker portal and the app, connector and connection pages of the Power Platform admin centre.

## Its relationship to bapi

This API and [bapi](../bapi) share one OAuth audience — `https://service.powerapps.com/.default` — and one URL grammar, `/providers/<namespace>/...` with an `api-version` query parameter. They are nonetheless different hosts with different surfaces, and the same concept can be spelled differently on each:

| | [bapi](../bapi) (`api.bap.microsoft.com`) | powerapps (`api.powerapps.com`) |
|---|---|---|
| namespace | `Microsoft.BusinessAppPlatform` | `Microsoft.PowerApps` |
| owns | environment provisioning, DLP, tenant settings, enterprise policies, billing | apps, connectors, connections, gateways |
| environments | the authoritative admin projection | its own read-only projection: cluster, per-service runtime endpoints, caller capability map |
| "environment not found" | — | `EnvironmentNotFound` on app paths, `ServiceToServiceEnvironmentNotFound` on connector paths |

The two also compose. The Terraform provider's `powerplatform_connectors` data source calls this API's connector list and then merges BAPI's `unblockableConnectorsMetadata` and `virtualConnectorsMetadata` on top, which is why the provider's connector DTO carries an `Unblockable` field that **this API never returns** — see [Corrections](#what-live-probing-corrected).

## How the spec was derived

Four sources, weakest to strongest, and every operation says which one it rests on in its `x-source`.

1. **The Terraform provider's client library** ([`internal/clients/powerapps`](https://github.com/microsoft/terraform-provider-power-platform/tree/main/internal/clients/powerapps)) — the starting inventory. It contains exactly two operations: the per-environment app list and the connector catalogue with its `~Default` fallback. Its unit tests pin the exact URLs.
2. **Live probes** — [`scripts/probe.py`](scripts/probe.py) against a real production tenant. Two operations is not a useful spec, so the probe verified those two properly and mapped the adjacent read-only surface around them.
3. **Microsoft's PowerShell modules** — `Microsoft.PowerApps.PowerShell` ships as readable script, so its routes, methods, default `api-version` values *and its response readers* are quoted rather than inferred. It is the source of the write surface, which the probe deliberately never touched, and of most of the operations added since.
4. **The admin centre's own bundles and third-party clients** — the Power Platform admin centre's JavaScript, the `cli-microsoft365` command set and a recorded HTTP cassette. These contribute routes the vendor script does not reach, response samples for objects the probe tenant did not contain, and the migration table described [below](#the-parp--power-platform-api-migration-table).

**10 of the 36 operations were confirmed with a real 200**; they carry `x-probe-verified: true`. The rest are client-derived: a shipped client proves a route exists in the client, and that is a weaker claim, so nothing else carries that flag. Nothing is in the document because a URL looked plausible — a route with no witness stays out, and a witnessed route with no witnessed method stays in the migration table rather than becoming an operation.

Like `bapi`, and unlike [`ppapi`](../ppapi), there is no upstream reference to regenerate from: `oas/openapi.json` is **owned directly**. There is no enrichment file.

## Layout

```
powerapps/
  scripts/probe.py     live probe harness (read-only; ids from argv/env)
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py --environment <environmentId>
scripts/probe.py --discover-environment            # use the first visible environment
scripts/probe.py --environment <id> --all-environments
```

It authenticates from the logged-in `az` session, issues only GETs, sleeps between calls and backs off on 429. It prints *shapes* — key names and value types — never leaf values, so its output is safe to paste.

## Conventions

- 36 operations over 31 paths, 45 schemas, tagged by logical resource (Canvas App, Connector, Connection, Environment, Gateway, Notification), OpenAPI 3.0.3.
- `api-version` defaults are per operation: `2023-06-01` for the admin app list, `2019-05-01` for connectors, `2016-11-01` for everything else. The service enumerates all 25 versions it accepts in its own `InvalidApiVersion` 400, and that list is `info.x-api-versions` and the `enum` on every `api-version` parameter. Versions appear to be routing labels rather than contracts here — the app list answers identically on `2016-11-01`, `2023-06-01` and `2025-04-01`.
- `required` is empty everywhere. There is no write operation on this surface to test optionality against, so field-presence counts from the live catalogue are stated in schema descriptions instead of guessed at as `required`.
- `x-probe-verified: true` marks what was confirmed against the live service, and appears on 10 operations. The app schemas carry `x-probe-verified: false` — see below.
- `x-source` carries the evidence grade: 10 `live`, 18 `ps-admin`, 4 `ppac-spa`, 4 `provider`. Where more than one source witnesses the same path *and method*, the strongest is `x-source` and the rest are listed in `x-corroborated-by` — 13 operations carry one. A source that witnesses only the path, or only a different method on it, is recorded in `x-notes` instead, because it is not evidence for the operation.
- One route is often addressable three ways, and clients build the path rather than hard-coding it: `/providers/Microsoft.PowerApps` + optionally `/scopes/admin` + optionally `/environments/{environmentId}` + the resource path. Only the forms actually witnessed are written out; the rule is stated in `info.description`.
- Path parameters were normalised: `{appName}` for the app segment and `{environmentId}` for the environment segment throughout. The document previously used `{appId}` and `{environmentName}` in some places, which made templated siblings disagree at the same position — not a legal path set, and every operation added since would have had to pick a side.
- `required` is now non-empty on the write bodies, because the PowerShell module shows which fields it always sends. On read responses it is still empty, for the reason above.

## What live probing corrected

This is the part the provider could not have told you.

**The connector list returns 19 properties; the provider models 4.** `displayName`, `description`, `tier` and `publisher` are a small slice. The service also returns `capabilities`, `interfaces`, `connectionParameters`, `connectionParameterSets`, `scopes`, `metadata` (source, version, stack owner, hide key, connection limits), `termsOfUseUrl`, `iconUri`, `iconBrandColor`, `isCustomApi`, `apiEnvironment`, `releaseTag`, `rateLimit`, `apiVersion`, `blobUrisAreProxied` and timestamps.

**The provider's `Unblockable` field is not part of this API.** `ConnectorPropertiesDto.Unblockable` has no `json` tag and is never populated by a PowerApps response; `internal/services/connectors` fills it from BAPI. A reader of the provider DTO alone would document a field that does not exist here.

**The three connector flags each do something measurable.** On a production tenant with 1710 connectors:

| flag | effect |
|---|---|
| `showApisWithToS=true` | +319 connectors — exactly the set carrying `termsOfUseUrl` |
| `hideDlpExemptApis=true` | −5 connectors: `shared_logicflows`, `shared_powerflows`, `shared_powervirtualagents`, `shared_conversionservice`, `shared_contentconversionservice` |
| `showAllDlpEnforceableApis=true` | +110 connectors, **and** strips `runtimeUrls`, `primaryRuntimeUrl` and `doNotUseApiHubNetRuntimeUrl` from every item |

That last one is the surprise: the larger list is the *smaller* payload per connector. Sending all four provider parameters yields 1710 connectors; sending `$filter` alone yields 1286.

**`$filter` is mandatory on the connector paths.** Omitting it is a 400 `MissingEnvironmentFilter`, not an unfiltered list. On the app paths it is optional — and obeys a narrow, non-OData grammar the service states in its own error text: only a `tagname`/`tagvalue` pair or `Visibility` alone, with `$expand=permissions($filter=maxAssignedTo('<objectId>'))` as the sole expansion, and the two are mutually exclusive (`InvalidAppFilterCombination`). An *unrecognised* `$filter` key on the admin app path is silently ignored rather than rejected, so a typo returns the unfiltered list.

**Real enum values, from the tenant rather than from imagination.** Connector `tier` is `Standard`/`Premium` and is overwhelmingly Premium (1487 of 1710). `capabilities` has twelve distinct values including singular/plural duplicates (`action` and `actions`). `releaseTag` includes a lower-case `preview` on one catalogue entry, so match case-insensitively. `metadata.source` is `marketplace`/`independentpublisher`/`manual` and is the reliable first-party-vs-community signal — `publisher` is free text and appears as both `Microsoft` and `Microsoft Corporation`.

**Error bodies are structured and worth reading.** `InvalidApiVersion` enumerates every accepted version. `InvalidAppFilterCombination` states the whole supported filter grammar. A 404 on the apps path is a `BusinessAppPlatformRequestFailed` wrapper with `EnvironmentNotFound` nested two levels down in `details`, one of which re-serialises the unlocalised error as a JSON *string*. Distinguishing an empty-body 404 (no such route) from a JSON-body 404 (route exists, resource does not) is what made the endpoint discovery below tractable.

**The environment projection differs from BAPI's, and from itself.** The list reports `azureRegionHint`; the single read reports `azureRegion` and adds `clientUris`, `databaseType` and the expanded `governanceConfiguration.settings`. The list's `linkedEnvironmentMetadata` carries six fields the read omits. `~Default` is a server-side alias for the tenant default environment on both the environment read and the connector `$filter`. `$expand=permissions` returns a capability *map* — `CreatePowerApp`, `SetDLPPolicy`, `DeleteAnyFlow` and twenty more — where an ungranted capability is absent rather than false.

## What could not be probed

**The app object.** The probe tenant contained **zero canvas apps across all 14 of its environments**, so no live app was ever returned. `App`, `AppProperties` and `AppEnvironmentRef` remain provider-derived and are marked `x-probe-verified: false`. The *operations* are verified — path, api-version, 200 with an empty `value`, and the full `$filter`/`$expand`/404 behaviour — but the item shape is not. Fields the admin centre is known to show (app version, connection references, embedded app metadata) are deliberately **not** in the spec, because nothing here observed them.

**The gateway object.** Same story, smaller: `gateways_list` returns 200 with an empty `value` on a tenant with no gateways installed, so `GatewayList.value` is left open.

**Everything mutating.** No write was ever attempted here. The 12 write bodies now in the document come entirely from reading Microsoft's PowerShell module and two third-party clients — what a client *sends*, not what the service accepts. A field a client never sets is not documented as optional; it is simply absent.

### What the probe said about routes now documented from clients

The probe could not obtain a 200 from these, but each answered with a **typed JSON error** rather than the empty-body 404 an unrouted path gives — which on this host is itself evidence the route exists. They are now in the spec on client evidence, with the probe result as corroboration:

| route | probe observed |
|---|---|
| `GET /providers/Microsoft.PowerApps/apps/{appName}` | 404 `ApplicationNotFound` |
| `GET /providers/Microsoft.PowerApps/apps/{appName}/permissions` | 403 `Forbidden` |

`GET /providers/Microsoft.PowerApps/apps/{appName}/connections` answered 404 `ApplicationNotFound` too, but no client here calls it, so it stays out — the probe proves the route, and nothing proves the method is useful or what it returns.

### An unresolved disagreement

The probe recorded `scopes/admin/environments/{env}/apps/{app}` as **confirmed absent** — an empty-body 404, which on this host means no such route. Two third-party clients call exactly that path, one of them pinning the full URL in its tests. The route is in the spec on the clients' evidence, and both observations are recorded in the operation's `x-notes` rather than one being quietly dropped. A caller who gets an empty-body 404 from it should read that as the probe's result reproducing, not as a bad app id.

Also confirmed *not* to exist by the probe (empty-body 404), and still absent from the spec: `scopes/admin/apps`, `scopes/admin/apps/{app}`, `scopes/admin/environments`, `scopes/admin/user`, `scopes/admin/environments/{env}/permissions`, `environments/{env}/permissions`, `environments/{env}/apis`, `apis/{api}/apiOperations`, `connectionReferences`, `connectorPermissions`.

### The PARP → Power Platform API migration table

The admin centre ships a route table that rewrites legacy `api.powerapps.com` paths onto the Power Platform API, gated by a `deprecateLegacyPARP` flag. It is the service's own statement of which of these routes are being retired and what replaces each one, so it is recorded verbatim in `info.x-ppapi-migration` — 72 routes, each with its replacement path and which of the two Power Platform API hosts (tenant-scoped or environment-scoped) serves it.

It is deliberately **not** turned into operations. The table names paths and targets; for all but three entries it does not name an HTTP method, and inventing one would turn a strong fact — this route exists and is being replaced by that one — into a guess. The three that do name a method (`displayName`, `publishedSettings`, `unpublishedSettings`, all POST) are in `paths`.

The table is also the evidence behind two claims elsewhere in the document: that the maker and admin-scope connector lists are one handler (both rewrite to the same `/connectivity/connectors`), and that a legacy path still answering today is a migration state rather than an accident.

## Status

Spec written and validated. 10 operations are live-verified against a production tenant (2026-08-27); the other 26 rest on Microsoft's PowerShell module, the admin centre's bundles and third-party clients, and have not been executed. The app item schema is now populated from a recorded third-party sample and still carries `x-probe-verified: false`; the gateway item schema awaits a tenant with a gateway installed. Nothing on the write surface has been executed by anyone here.
