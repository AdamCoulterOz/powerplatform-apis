# dataverse

The Dataverse Web API (`{organization}.crm{n}.dynamics.com/api/data/v9.2`), the per-environment OData v4 endpoint through which every table in an environment is addressable — and, for an infrastructure client, the place solutions are imported, environment variables are set, application users are created and environment settings are changed.

## Why this one is a *subset*

Unlike [bapi](../bapi) and [ppapi](../ppapi), Dataverse **has** an official contract: each environment publishes its own CSDL at `GET /api/data/v9.2/$metadata`, and Microsoft Learn documents the surface in prose. That contract is also per environment, includes every custom table anyone ever made, and runs to megabytes. Reproducing it here would be neither possible nor useful.

So [`oas/openapi.json`](oas/openapi.json) is deliberately **a curated admin/ALM subset** — the operation surface an infrastructure client actually uses:

| Tag | What it covers |
|---|---|
| Identity | `WhoAmI` |
| Discovery | `globaldisco.*` — the Global Discovery Service: which organizations a token can reach, and each one's Web API URL |
| Table Definitions | `EntityDefinitions`, columns, relationship metadata |
| Records | generic CRUD and OData query against any table |
| Relationships | `@odata.bind`, the `$ref` collection, associate/disassociate |
| Batch | `$batch` — several requests in one `multipart/mixed` round trip |
| Solutions | the installed inventory, exporting one, and deleting one |
| Solution Import | `StageSolution`, `ImportSolutionAsync`, `StageAndUpgradeAsync`, `asyncoperations`, `RetrieveSolutionImportResult`, `PublishAllXml` |
| Environment Variables | definitions and their per-environment values |
| Publishers | publishers and their customization prefix |
| Users and Roles | system and application users, security roles, teams, memberships, effective privileges, business units |
| Organization Settings | the three unrelated settings surfaces — the `organizations` row, the OrgDB bag, `settingdefinitions` — and the functions by which an environment describes itself |
| Feature Control | `GetFeatureEnabledState`, `RetrieveFeatureControlSetting` |
| Dataverse Search | whether the environment's index has been provisioned |
| Fabric and Synapse Link | `datalakefolders`, `synapsedatabases`, `synapselinkexternaltablestates`, `entityanalyticsconfigs` |

Every tag but one lives on the per-environment host. **Discovery does not** — it is a separate service on `globaldisco.*` with its own audience, and those paths carry their own `servers` block. That block, and the paragraph explaining it, is repeated verbatim on each of the three discovery paths, because OpenAPI 3.0 has no `$ref` for Server objects — a shared component is not available here, so the duplication is the format's, not an oversight. It is in this document anyway because it answers the question every other operation here takes for granted: which host?

## Finding an environment's Web API URL

Every other operation here needs a host, and a Dataverse host is not derivable from an environment id — `contoso.crm11.dynamics.com` cannot be computed from a GUID. There are two ways to learn it.

The usual one is the admin APIs: [bapi](../bapi)'s environment record, or the `instanceApiUrl` on [ppapi](../ppapi)'s environment resource. Both require environment-admin reach.

The other is **discovery**, and it needs no admin permission and no environment id at all — just a token. `GET https://globaldisco.crm.dynamics.com/api/discovery/v2.0/Instances` returns every organization the caller can reach across every region at once, each with its organization id, its Power Platform environment id, its platform version and both of its URLs. That makes it the natural first call for a client that has an identity and nothing else, and the natural join between the Power Platform view of an environment and the Dataverse view of an organization.

Two caveats decide whether you can use it:

- **Service principals are not admitted.** App-only identities get nothing from global discovery; `pac` short-circuits and returns an empty set for them without calling, and treats a 401 from a directory-credential profile as evidence the identity is really an SPN — falling back to BAPI's environment list. An app-only client must go through BAPI.
- **It is per cloud, not global.** `globaldisco.crm.dynamics.com` serves worldwide commercial. China, US Gov High, US Gov DoD and the North America 2 scale group each have their own, and a token for one is not accepted by another.

Build the Web API base from an instance as `{ApiUrl}/api/data/v{major}.{minor}/`, taking major.minor from that instance's own `Version`. Note `ApiUrl` is not `Url`: it carries an extra `api` label (`contoso.api.crm.dynamics.com` against `contoso.crm.dynamics.com`).

### CRM region numbers

The regional discovery endpoints are SOAP and out of scope, but the region-to-host mapping the SDK carries is not recorded anywhere else in this repo, and the same region number appears in every organization's own hostname — so `contoso.crm11.dynamics.com` is a United Kingdom environment. The full table is in the Discovery tag's description in the spec. In brief:

| # | Region | # | Region | # | Region |
|---|---|---|---|---|---|
| `crm` | North America | `crm7` | Japan | `crm15` | United Arab Emirates |
| `crm2` | South America (`LATAM`) | `crm8` | India | `crm16` | Germany (Go Local) |
| `crm3` | Canada | `crm9` | North America 2 | `crm17` | Switzerland |
| `crm4` | Europe, Middle East, Africa | `crm11` | United Kingdom | `crm19` | Norway |
| `crm5` | Asia Pacific | `crm12` | France | `crm20` | Singapore |
| `crm6` | Oceania (`OCE`) | `crm14` | South Africa | `crm21` | Korea |

Sovereign clouds do not use a number: `crm.dynamics.cn` is China, `crm.microsoftdynamics.us` US Gov High, `crm.appsplatform.us` US Gov DoD, `crm.microsoftdynamics.de` the sovereign German cloud. `crm10` and `crmtest` are Microsoft's own pre-production and test rings. `crm13`, `crm18` and `crm22` upwards are absent from this build — whether unused or merely unshipped is not something the CLI can tell us.

**For anything outside that, go to the environment's own `$metadata`.** It is authoritative, machine-readable, and always current for that environment; this spec never can be.

## How it was derived

The inventory came from the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform), whose client-library refactor put every Dataverse call in one package (`internal/clients/dataverse`) encoding per operation the method, path, api-version, request/response DTOs and accepted status codes.

The **behaviour** came from two kinds of evidence against the real service.

First, probing a live tenant. That is where the value is: the provider models only the fields it consumes, and its accepted-status lists are a superset of what the service actually does. Live probing produced the annotation and envelope conventions, real option-set values read out of the metadata endpoint, the 5000-row count ceiling, api-version routing, and thirteen distinct Dataverse error codes with the conditions that produce them.

Second, **recorded first-party UI traffic** — HAR captures of the Power Platform admin centre, the maker portal and the Link to Fabric wizard driving nine real Dataverse organizations — 20 captures holding 613 Dataverse entries, of which 322 are requests and the rest CORS preflights. Recorded production traffic is stronger evidence than synthetic probing: it shows the request and response bodies the real first-party client sends and receives, including endpoints and fields no external caller would think to guess. A recorded 200 is treated as confirmation, so `x-probe-verified: true` now means "confirmed against the real service" by either route.

Operations confirmed against the live service carry `x-probe-verified: true` — 64 of 76. The six that do not are `ImportSolutionAsync` and `StageAndUpgradeAsync` (only their rejection paths were exercised; no solution was actually imported), `PublishAllXml`, and application-user create/update/delete, which needs a service principal to register.

Third, the **decompiled Power Platform CLI** (`pac` 2.11.2), which ships Microsoft's own `Microsoft.PowerPlatform.Dataverse.Client` SDK. A first-party client's source is strong *structural* evidence — real route templates, wire names from `[JsonProperty]` and `[DataMember]` attributes, enumerations, headers, retry rules and geography maps — but it is not an observation, and the build can be older than the service. So anything sourced only from it carries **`x-source: pac-cli`** and is deliberately **not** `x-probe-verified`. The entire Discovery tag is in that category: nobody has called those endpoints from here.

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

## The 2026-09-05 live sweep

A later read-only capture, driven through the admin centre's environment pages on a commercial tenant in the Australia geo, with request and response both recorded. It confirmed a stretch of this spec on the wire rather than adding much to it: fourteen operations carry `x-source: "live"` from it and nothing else had its grade touched.

- **Two entity sets the admin centre addresses by name were missing here**: `applicationusers` and `savedqueries`. Both are added with their routes and the usual query options, and **no response schema** — the routes were observed, the bodies were not, and this spec does not guess column sets.
- **`RetrieveUsersPrivilegesThroughTeams` carries its arguments inline in the URL**, captured verbatim as `(ExcludeOrgDisabledPrivileges=true,IncludeSetupUserFiltering=true)` — inside the parentheses, not as query options beside them. A bundle yields the function's name and nothing about how its arguments are carried; only a call does.
- **`issytemgenerated` is confirmed on the wire**, read as attribute metadata on `role`. It is recorded as an `x-observed-value` on `attributeLogicalName` precisely so a later reader treats it as data rather than as a typo to correct.
- **The service accepts a doubled slash after the host.** The admin centre concatenates an organization host that already ends in `/` with a path that starts with one, producing `//api/data/v9.0/...`, and both forms were seen answering against the same organization in one session.
- **The Dataverse side is keyed by the organization id, not the environment id.** The admin centre's own sub-pages show it: `/environments/{organizationId}/securityroles` uses the organization id alone, and the users page carries both, in the order `/environments/{organizationId}/{environmentId}/users`. A caller holding only an environment id cannot address this API.
- **`/api/nosql/` is a separate root on the same host**, not a branch of the Web API. It is kept in this spec because it shares the host, the token and the audience — and its description now says outright that it does not share the protocol.
- Several entity-set reads were seen on the **`v9.0`** segment where this spec pins `v9.2` in the path. Those operations carry the mark with a note saying so: the evidence is for the operation, not for the segment it is written under.

## What the CLI added

Structural facts no amount of probing this tenant would have produced, because they are about services and messages the provider never calls:

- **The Global Discovery Service, which the spec did not cover at all.** `GET https://globaldisco.{cloud}/api/discovery/v2.0/Instances`, with the `Instances({id})` single-read template beside it — declared by the SDK and, tellingly, never actually issued by this build. The `Instance` model's seventeen fields come from its `[JsonProperty]` names, including the two that make it useful to an infrastructure client: `EnvironmentId`, the join to BAPI and PPAPI, and `ApiUrl`, the host the Web API hangs off.
- **The sovereign and regional host map**, in full — twenty-two regions with their geo codes, their SOAP discovery hosts and, for the four that need one, their own global discovery host. Nothing else in this repo maps a CRM region number to a geography.
- **`GET /api/aad/challenge`**, and the rule behind it. An unauthenticated request returns `WWW-Authenticate: Bearer authorization_uri=…, resource_id=…`, and the SDK builds its scope from `resource_id` — `/user_impersonation` appended for a delegated sign-in, `.default` for a certificate or secret. It also rewrites the advertised authority, stripping `oauth2/authorize` and turning `common` into `organizations`, and it treats a 404 or 400 as a dead end rather than reading the header from it.
- **`RetrieveCurrentOrganization`**, which is discovery's answer read from inside a single environment — the cheapest way to get from a Dataverse hostname back to a Power Platform environment id.
- **`RetrieveOrganizationInfo`**, which names the instance type (production, trial, developer, Teams) and lists installed solutions. The instance type is the check worth making before writing to an environment, and this is the only call that returns it.
- **`ExportSolution`** — the missing half of the ALM story, and notably *synchronous*: the whole `.zip` comes back base64 in one response, with no job to poll and no download URL.
- **Six request headers** the SDK sends that the spec did not carry: `MSCRM.SolutionUniqueName` (which solution a created component lands in — the usual reason automation-created components cannot later be exported), `MSCRM.BypassCustomPluginExecution`, `MSCRM.SuppressDuplicateDetection`, `Consistency: Strong` (see current metadata rather than a cached copy, which matters on the read right after a schema change), and the two impersonation headers `MSCRMCallerID` and `CallerObjectId`.
- **Three named throttling codes** behind the single 429: `0x80072321` time, `0x80072322` burst, `0x80072326` concurrency. Only the concurrency one warrants exponential backoff; the others are windowed, so `Retry-After` is the real answer.

### What it corroborated

- **The `WWW-Authenticate` challenge** as the reliable way to discover authority and audience — already in the spec from live 401s, and independently how both the SDK and `pac` itself bootstrap.
- **The api-version scatter has a cause.** The spec had already recorded that clients disagree about the segment. The SDK explains it: it does not pin one. It takes the environment's own build, truncates to major.minor, and composes `/api/data/v{major}.{minor}/` — falling back to `9.0` with no version and refusing the Web API below major 8. The segment tracks the environment, not the client.
- **`If-Match: *` on update and delete**, which the SDK sends unconditionally — matching what probing found about PATCH upserting without it.
- **The global discovery host list**, twice over: the SDK's `DiscoveryServers` table and `pac`'s own `AudienceResolver` agree on all five production hosts independently.

### Where it disagreed

One place, and it is unresolved rather than resolved. The SDK matches throttling error codes as **decimal signed integers** (`-2147015902`); every error body observed live on this API spells `code` in hexadecimal. Nobody has captured a live 429 against this tenant, so live evidence cannot win — there is none. Both forms are recorded under the 429 response and a client should match on both.

### What the CLI offered and was left out

- **The SOAP organization service.** `System.ServiceModel.*` assemblies ship inside `pac`, and the SDK translates only ten message types to HTTP — `Create`, `Update`, `Delete`, `WhoAmI`, `RetrieveVersion`, `RetrieveCurrentOrganization`, `RetrieveOrganizationInfo`, `ExportSolution`, `ImportSolution`, `StageSolution` — falling back to SOAP at `/XRMServices/2011/Organization.svc` for everything else. That is worth one honest sentence: the CLI still speaks SOAP, and this spec covers the OData Web API only. Documenting the SOAP surface would mean documenting a different protocol.
- **The regional discovery endpoints** at `disco.crm{n}.dynamics.com/XRMServices/2011/Discovery.svc`, for the same reason. Their host map is kept; their operations are not.
- **`ImportSolutionProperties`** — the ten parameter names (`DesiredLayerOrder`, `AsyncRibbonProcessing`, `IsTemplateMode`, `SchemaUpdatesOnly` and the rest) the SDK puts in a SOAP `ImportSolutionRequest`'s parameter bag. They plainly *relate* to `ImportSolutionAsync`'s body, but the SDK never sends them over HTTP, so mapping them onto the Web API action would be inference dressed as evidence.
- **The synchronous `ImportSolution`**, which the SDK does translate. The spec already documents `ImportSolutionAsync`, which is what any current client should use, and adding the synchronous form would suggest it is a real choice.
- **`RetrieveUserLicenseInfo`**, which appears in the SDK's verb table but not in its list of messages it will actually send over HTTP — and which belongs to [licensing](../licensing)'s boundary regardless.
- **The ModelBuilder and codegen surface**, and the SDK's metadata-caching, batching and connection-string machinery. All client-side, none of it a wire contract.

## What was deliberately left out

The capture also contains Dataverse calls that are **not** in this spec's scope, and they stay out:

- Business data — `account`, `contact` and the captured tenant's own publisher-prefixed custom tables. The whole point of the subset is that per-environment business tables belong in that environment's `$metadata`, not here.
- Maker and studio surface: `customcontrols`, `workflows`, `appmodules/RetrieveUnpublishedMultiple`, `sdkmessages`.
- Copilot and AI surface: `bots`, `msdyn_aimodels`, `IsPaiEnabled`, `msdyn_analysisoverrides`. That boundary is [copilot](../copilot)'s.
- `usersettingscollection` — per-user UI personalisation (timezone, density, email preferences), not environment administration.
- `recyclebinconfigs` — observed once, answering an empty array to a malformed filter, which is not enough to document a shape from.
- `OPTIONS` preflights. The browser sends one before every cross-origin Dataverse call; the service answers with `Access-Control-Allow-Headers: authorization, client-activity-id, client-session-id, consistency, content-type, request-id, x-ms-client-request-id, x-ms-client-session-id`. That is CORS, not an operation.

## Status

Spec validates as OpenAPI 3.0.3; 91 operations over 73 paths, 98 schemas. 66 operations carry `x-probe-verified: true`; the six SDK-derived additions carry `x-source: pac-cli` and claim nothing. Rendered by the browser at the repo root.
