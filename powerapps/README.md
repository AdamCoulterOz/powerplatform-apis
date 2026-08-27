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

Two sources, in order.

1. **The Terraform provider's client library** ([`internal/clients/powerapps`](https://github.com/microsoft/terraform-provider-power-platform/tree/main/internal/clients/powerapps)) — the starting inventory. It contains exactly two operations: the per-environment app list and the connector catalogue with its `~Default` fallback. Its unit tests pin the exact URLs.
2. **Live probes** — everything else. Two operations is not a useful spec, so [`scripts/probe.py`](scripts/probe.py) was pointed at a real production tenant to verify those two properly and to find the adjacent read-only surface around them.

**Every operation in [`oas/openapi.json`](oas/openapi.json) was confirmed with a real 200.** Nothing is in the document because a URL looked plausible. Routes that clearly exist but could never be exercised are listed [below](#probed-but-not-in-the-spec) rather than guessed at.

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

- 10 operations over 10 paths, 32 schemas, tagged by logical resource (Canvas App, Connector, Connection, Environment, Gateway), OpenAPI 3.0.3.
- `api-version` defaults are per operation: `2023-06-01` for the admin app list, `2019-05-01` for connectors, `2016-11-01` for everything else. The service enumerates all 25 versions it accepts in its own `InvalidApiVersion` 400, and that list is `info.x-api-versions` and the `enum` on every `api-version` parameter. Versions appear to be routing labels rather than contracts here — the app list answers identically on `2016-11-01`, `2023-06-01` and `2025-04-01`.
- `required` is empty everywhere. There is no write operation on this surface to test optionality against, so field-presence counts from the live catalogue are stated in schema descriptions instead of guessed at as `required`.
- `x-probe-verified: true` marks what was confirmed against the live service. The app schemas carry `x-probe-verified: false` — see below.

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

**Everything mutating.** No write operation exists on this boundary in the provider, and none was attempted. This is a read-only spec.

### Probed but not in the spec

These routes demonstrably exist — they answer with a typed JSON error rather than the empty-body 404 an unrouted path gives — but no 200 was ever obtained from them, so they are excluded rather than guessed:

| route | observed |
|---|---|
| `GET /providers/Microsoft.PowerApps/apps/{appName}` | 404 `ApplicationNotFound` |
| `GET /providers/Microsoft.PowerApps/apps/{appName}/connections` | 404 `ApplicationNotFound` |
| `GET /providers/Microsoft.PowerApps/apps/{appName}/permissions` | 403 `Forbidden` |

Confirmed *not* to exist (empty-body 404): `scopes/admin/apps`, `scopes/admin/apps/{app}`, `scopes/admin/environments/{env}/apps/{app}`, `scopes/admin/environments`, `scopes/admin/user`, `scopes/admin/environments/{env}/permissions`, `environments/{env}/permissions`, `environments/{env}/apis`, `apis/{api}/apiOperations`, `connectionReferences`, `connectorPermissions`.

## Status

Spec written and validated; every operation live-verified against a production tenant on 2026-08-27. App and gateway item schemas await a tenant that actually has apps and gateways.
