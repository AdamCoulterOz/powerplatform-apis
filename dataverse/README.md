# dataverse

The Dataverse Web API (`{organization}.crm{n}.dynamics.com/api/data/v9.2`), the per-environment OData v4 endpoint through which every table in an environment is addressable — and, for an infrastructure client, the place solutions are imported, environment variables are set, application users are created and environment settings are changed.

## Why this one is a *subset*

Unlike [bapi](../bapi) and [ppapi](../ppapi), Dataverse **has** an official contract: each environment publishes its own CSDL at `GET /api/data/v9.2/$metadata`, and Microsoft Learn documents the surface in prose. That contract is also per environment, includes every custom table anyone ever made, and runs to megabytes. Reproducing it here would be neither possible nor useful.

So [`oas/openapi.json`](oas/openapi.json) is deliberately **a curated admin/ALM subset** — the operation surface an infrastructure client actually uses:

| Tag | What it covers |
|---|---|
| Identity | `WhoAmI` |
| Table Definitions | `EntityDefinitions`, columns, relationship metadata |
| Records | generic CRUD and OData query against any table |
| Relationships | `@odata.bind`, the `$ref` collection, associate/disassociate |
| Batch | `$batch` — several requests in one `multipart/mixed` round trip |
| Solutions | the installed inventory, and deleting one |
| Solution Import | `StageSolution`, `ImportSolutionAsync`, `StageAndUpgradeAsync`, `asyncoperations`, `RetrieveSolutionImportResult`, `PublishAllXml` |
| Environment Variables | definitions and their per-environment values |
| Publishers | publishers and their customization prefix |
| Users and Roles | system and application users, security roles, teams, memberships, effective privileges, business units |
| Organization Settings | the `organizations` row, and the three unrelated settings surfaces beside it |
| Feature Control | `GetFeatureEnabledState`, `RetrieveFeatureControlSetting` |
| Dataverse Search | whether the environment's index has been provisioned |
| Fabric and Synapse Link | `datalakefolders`, `synapsedatabases`, `synapselinkexternaltablestates`, `entityanalyticsconfigs` |

**For anything outside that, go to the environment's own `$metadata`.** It is authoritative, machine-readable, and always current for that environment; this spec never can be.

## How it was derived

The inventory came from the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform), whose client-library refactor put every Dataverse call in one package (`internal/clients/dataverse`) encoding per operation the method, path, api-version, request/response DTOs and accepted status codes.

The **behaviour** came from two kinds of evidence against the real service.

First, probing a live tenant. That is where the value is: the provider models only the fields it consumes, and its accepted-status lists are a superset of what the service actually does. Live probing produced the annotation and envelope conventions, real option-set values read out of the metadata endpoint, the 5000-row count ceiling, api-version routing, and thirteen distinct Dataverse error codes with the conditions that produce them.

Second, **recorded first-party UI traffic** — HAR captures of the Power Platform admin centre, the maker portal and the Link to Fabric wizard driving nine real Dataverse organizations — 20 captures holding 613 Dataverse entries, of which 322 are requests and the rest CORS preflights. Recorded production traffic is stronger evidence than synthetic probing: it shows the request and response bodies the real first-party client sends and receives, including endpoints and fields no external caller would think to guess. A recorded 200 is treated as confirmation, so `x-probe-verified: true` now means "confirmed against the real service" by either route.

Operations confirmed against the live service carry `x-probe-verified: true` — 64 of 70. The six that do not are `ImportSolutionAsync` and `StageAndUpgradeAsync` (only their rejection paths were exercised; no solution was actually imported), `PublishAllXml`, and application-user create/update/delete, which needs a service principal to register.

Operations that came from the recordings carry `x-observed-api-versions`, listing the `v9.x` segments actually seen on the wire — because the first-party clients are not consistent about the version they call, and neither is the provider.

## Layout

```
dataverse/
  scripts/probe.py     the live probe harness
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

`probe.py` is generic — the host comes from `argv` or `DATAVERSE_HOST`, tokens from the logged-in `az` session — and prints shapes, not tenant data:

```
scripts/probe.py read  <host>     # envelope, paging, collections, error shapes
scripts/probe.py enums <host>     # the option sets the spec pins, read from metadata
scripts/probe.py write <host>     # create/update/associate/delete, cleaned up in `finally`
```

Point `write` only at a throwaway environment. Everything it creates is prefixed and removed, and it verifies the removal before exiting.

## What probing changed

The corrections worth knowing, because a provider-only reading of this API gets them wrong:

- **`@odata.bind` takes the navigation property, not the lookup column.** They are frequently spelled differently — `environmentvariablevalue`'s column is `environmentvariabledefinitionid`, its navigation property is `EnvironmentVariableDefinitionId` — and binding to the column name is refused outright as an undeclared property. Read `ReferencingEntityNavigationPropertyName` from relationship metadata.
- **Counts saturate at 5000.** Both `@odata.count` and `@Microsoft.Dynamics.CRM.totalrecordcount` cap there; `totalrecordcountlimitexceeded` is the only way to tell a table of exactly 5000 rows from one of half a million.
- **Metadata endpoints are not entity sets.** `EntityDefinitions` and its children accept `$top` and ignore it, and never page.
- **PATCH upserts.** Without `If-Match: *`, a PATCH at a wrong id silently creates a record.
- **Read-only columns on `organizations` are accepted and discarded**, not refused — patching `name` returns success and changes nothing.
- **`StageSolution` reports failure inside a success response**, with an all-zeros upload id and a fully-null `SolutionDetails`. Its real response also carries far more than the provider models: the *installed* solution's name, version, publisher and pending-upgrade state alongside the package's, which is what makes an install-versus-upgrade decision possible before importing.
- **A bad role id is `0x80040217`**, a missing `role` record — not the generic unresolvable-reference code a client might special-case.
- **`SaveSettingValue()` refuses with 400**, not 500: `0x81000067` for an unknown setting name, `0x81000068` for a value that will not convert.
- **401 has an empty body.** The reason is in `WWW-Authenticate` (which also advertises the exact audience to request) and a non-standard `401_error_reason` header. A request with no api-version segment answers `{"Message": ...}` from below the OData layer, escaping the error envelope entirely. And some transport-level failures return the envelope with `code` set to the empty string.

## What the recordings changed

The corrections and additions the HAR capture produced, over and above what probing had already established:

- **`GetFeatureEnabledState` exists and is the busiest Dataverse call the admin centre makes** — 98 times in one session to paint one settings page, because it takes exactly one feature name per call and has no bulk form. It is an unbound *action*, so a POST that only reads. Forty-nine distinct feature names were observed and are recorded as `x-observed-values`; the namespace is open, and two naming conventions (`FCB.`-prefixed and bare) coexist. There is no error path: an unknown name answers `false` exactly like a switched-off feature.
- **`datalakefolders` has ten or eleven rows before anything is ever linked.** An organization with no Link to Fabric already carries `cds_workspace`, `cds2_workspace`, `cds3_workspace`, `msdyn_analytics`, `msdyn_processadvisor`, `msdyn_skillmining_workspace`, `msdyn_iap_federated`, `msdyn_nl2sq`, `pai_capi_batch_datalake`, `smartdataimport_workspace` and a per-installation `cds_<guid>` — the timestamps prove it, since the three `cds*_workspace` rows were created within two seconds of each other at provisioning, two months before the link that later used `cds3_workspace`. This is a live provider bug: the unmerged `fabric_link` client's `getDatalakeFolderId` falls back to `list.Value[0]` when neither `cds3_workspace` nor `cds2_workspace` matches, and [athena](../athena)'s unlink deletes whatever folder that id names. In the capture, row zero was `cds2_workspace` while the linked folder was `cds3_workspace`. Two positive signals distinguish the real one, and both were observed only on it: `extendedproperties` parsing to `{"IsActiveFabricProfile":true}`, and a non-empty `synapsedatabases` under `$expand`.
- **The Fabric link's artifact ids live in `synapsedatabases`** — lakehouse, lakehouse workspace and the Fabric-to-Dataverse connection — which is what makes them recoverable after a create call that does not return them.
- **`systemusers` is 133 columns**, and the recordings pinned a dozen the spec was missing: `islicensed`, `setupuser`, `azurestate`/`azuredeletedon`, `internalemailaddress` (which was observed *differing* from `domainname`, so neither substitutes for the other), `organizationid` as a plain column rather than a `_..._value` lookup, and the `teammembership_association` expand.
- **`azureactivedirectoryobjectid` is an alternate key**, not just a filterable column: `systemusers(azureactivedirectoryobjectid=<guid>)` reads the row directly, and answers 404 where the filtered form answers 200 with an empty page.
- **Roles carry a misspelled column.** `role.issytemgenerated` is missing an `s`, and the misspelling is the real name — the portal filters on it, and reading the attribute metadata for it succeeds. Also new: `roleidunique` (the identity that survives across business units and environments, where `roleid` does not) and `_roletemplateid_value` (stable across every environment, which is how the portal finds administrator roles without matching a localized name).
- **Team-inherited privileges are a separate call.** `RetrieveUserPrivileges` returns only directly-held privileges — thousands on an administrator — while `RetrieveUsersPrivilegesThroughTeams` returned an empty array for the same user. Neither is a superset; the effective set is the union.
- **`systemuserrolescollection` wants its guids quoted** (`$filter=systemuserid eq '<guid>'`), which is the opposite of the unquoted form ordinary tables require on their `_..._value` shadows. `teammemberships` beside it takes them unquoted.
- **There are three unrelated settings surfaces, not two.** Beside the `organization` row and the OrgDB bag reachable through `RetrieveSettingList()`, there is a `settingdefinitions` catalogue with typed defaults and an `isoverridable` flag, read one at a time through `RetrieveSetting(SettingName=…,AppUniqueName=…)`. `GetOrgDbOrgSetting` is the by-name read of the OrgDB bag — the only way to ask about a setting the list operation omits because it has never been set.
- **Empty string is the OrgDB bag's "not set", and it is indistinguishable from "no such name".** Neither is an error, so that surface cannot validate a name. And in `RetrieveSettingList()`, a string-typed empty value arrives as the two-character JSON literal `""` while a non-empty one arrives bare — strip quotes before use.
- **`organizations` PATCH returns a `Location` header** alongside its 204, with `Content-Type: text/html` on an empty body. Three settings the admin centre reads were missing from the row: `suppressvalidationemails`, `validationmode` and `releasechannel`. `powerappsmakerbotenabled` is **null, not false**, on a stock environment.
- **`EntityDefinitions` filters on metadata properties** — `$filter=SyncToExternalSearchIndex eq true and ChangeTrackingEnabled eq true` is how the portal finds link-eligible tables — and its `totalrecordcount` annotation carries a **real count** there, unlike the `-1` entity sets return. It also takes a PascalCase, non-OData `RetrieveAllSettings=True`.
- **A single attribute is addressable and comes back cast** to its concrete metadata subtype, with the cast in both the context path and `@odata.type`. One request carried an `api-version=9.1` *query* parameter disagreeing with the `v9.0` in its path and succeeded anyway; the query parameter appears to be ignored.
- **`$batch` chooses its own response boundary**, unrelated to the request's, and returns 200 whether the parts succeeded or not.
- **`/api/nosql/audit/isreadenabled` and `/api/search/v1.0/status` are not OData.** They sit on the same host under the same token with no version segment and no envelope; the first answers a bare `true`/`false` literal.
- **The api-version segments disagree between clients.** The portal calls `datalakefolders` on `v9.2` while the provider pins `v9.1`; `GetOrgDbOrgSetting` was seen on both `v9.0` and `v9.2`. Where the recordings saw only one segment, the path pins it and `x-observed-api-versions` says so.

## What was deliberately left out

The capture also contains Dataverse calls that are **not** in this spec's scope, and they stay out:

- Business data — `account`, `contact` and the captured tenant's own publisher-prefixed custom tables. The whole point of the subset is that per-environment business tables belong in that environment's `$metadata`, not here.
- Maker and studio surface: `customcontrols`, `workflows`, `appmodules/RetrieveUnpublishedMultiple`, `sdkmessages`.
- Copilot and AI surface: `bots`, `msdyn_aimodels`, `IsPaiEnabled`, `msdyn_analysisoverrides`. That boundary is [copilot](../copilot)'s.
- `usersettingscollection` — per-user UI personalisation (timezone, density, email preferences), not environment administration.
- `recyclebinconfigs` — observed once, answering an empty array to a malformed filter, which is not enough to document a shape from.
- `OPTIONS` preflights. The browser sends one before every cross-origin Dataverse call; the service answers with `Access-Control-Allow-Headers: authorization, client-activity-id, client-session-id, consistency, content-type, request-id, x-ms-client-request-id, x-ms-client-session-id`. That is CORS, not an operation.

## Status

Spec validates as OpenAPI 3.0.3; 70 operations over 53 paths, 86 schemas. Rendered by the browser at the repo root.
