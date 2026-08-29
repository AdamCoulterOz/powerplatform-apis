# athena

The orchestration service behind Dataverse **Link to Microsoft Fabric** and Azure Synapse Link — known internally as *athena*, and formally as the Microsoft first-party application **"Azure Synapse Link for Dataverse"**. It is what the maker portal's Link to Fabric wizard and the Fabric portal's Dataverse connection wizard both drive: it lists the tables an environment may mirror, creates the mirror lakehouse inside a target Fabric workspace, writes the `synapselinkprofile` and `datalakefolder` rows into Dataverse server-side, reports sync progress table by table, and tears the link down again.

**This is not the Power Platform admin centre API.** That is a different service, on a different host, with a different scope, and it is specified in [`admin/`](../admin). The two have nothing to do with each other beyond both being unofficial.

## Read this first: where the spec comes from

This spec is derived from **recorded traffic**, not from probing. 291 real calls to this service were captured across 18 browser HAR sessions of `make.powerapps.com` and `app.fabric.microsoft.com` driving genuine link, table-modification and unlink workflows on a live tenant. Every operation, request body, response body, status code and query parameter documented here was observed on the wire.

That is not a weaker substitute for probing — for this boundary it is stronger. A probe shows you what the service tolerates from a synthetic client; a capture shows you what the service actually does under its own client, including the shapes of bodies you could never have guessed and the order the calls have to go in. It is also the only evidence available here, because probing this surface safely is impossible: see below.

The honest limits of it are two.

**It is evidence of the happy path.** The captures contain exactly one non-2xx response in 291 calls — a `403` on the premium-licence check — so the error surface is almost entirely undocumented. There is no observed 400, no 404 on a real route, no 409, no 429, no timeout, and no error envelope. Nothing here tells you what a malformed request does.

**It is evidence from one tenant's configuration.** No environment in the capture had a Finance & Operations link, so `/fnoTables` returned an empty array every time and its row shape is unknown. No environment used a bring-your-own Azure Data Lake Storage account, so roughly half the fields of the lake payload were empty strings throughout. No environment had an encryption enterprise policy, so the enterprise-policy credential read returned nulls every time. Those three are marked `x-probe-verified: false` at schema level or called out in prose; everything else is `true`.

The previous revision of this spec covered **3 operations**, all `x-probe-verified: false`, derived from an unmerged Terraform provider feature branch. This one covers **15**, every one of them observed on the wire, with a single schema left unverified — the row shape of the Finance & Operations table list, which was never populated. The "least-verified spec in this repository" framing no longer holds; the surface is now among the better-evidenced ones here, with the caveat above about errors.

## Why it could not be probed instead

Three properties of this boundary compound, and they are the reason recorded traffic was the only route.

**Everything that matters mutates.** The read operations discovered in the capture — the table catalogue, the workspace list, the lake list, the lake profile — are safe and would have been probeable *if their existence had been known*. The three operations the provider knew about were not: one POST that provisions a real Fabric integration, one POST that mutates an organization's registration, and one DELETE that destroys the integration. Provisioning additionally needs a Fabric workspace id and a Fabric-to-Dataverse connection id that the probing exercise did not have. So the surface as it was then understood had no safe entry point at all, and the reads that would have been the way in could not be found without already knowing they were there.

**The service does not distinguish a wrong method from a wrong path.** Elsewhere in this repo, route existence is established for free: a GET against a POST-only route answers `405` with an `Allow` header, or a wrong `api-version` answers `400 UnsupportedApiVersion`. That does not work here. Every `GET`, `HEAD` and `OPTIONS` against an unknown path answers an identical bare `404`: no body, no `Allow` header, no `Content-Type`, and there is no `api-version` parameter to get wrong. Route discovery by probing was therefore not merely unsafe, it was impossible.

**Authentication is unobservable too.** Routing fails before authentication runs, so a valid token, no token, a wrong-audience token and the literal string `not-a-token` all produce the same `404`. Nothing on this host ever issues a `WWW-Authenticate` challenge, so unlike every other boundary here the audience cannot be discovered by asking. It is knowable only from a token or from captured traffic — and the capture settles it: every recorded request carries a delegated token whose `aud` is `7f15f9d9-cad0-44f1-bbba-d36650e07765`, whose `scp` is `user_impersonation`, and whose `idtyp` is `user`.

## What the recording changed

Against the 3-operation, provider-derived view, the capture corrected four things and added twelve.

**The base64 response was never real.** The old spec modelled `POST .../lakehouseArtifacts` as returning `type: string, format: byte` — a JSON string containing base64-encoded JSON — with the decoded shape hung off it as `x-decoded-schema`, and the README warned readers to "decode, then parse". That was wrong, and it was wrong for an instructive reason: the earlier HAR read had taken the HAR file's own `response.content.encoding: "base64"` field for the API's content type. It is the capture format, not the service's. Recorded responses carry `Content-Type: application/json` and a plain JSON object. `scripts/har_extract.py` decodes the transport encoding and says so loudly, precisely so this does not happen again.

**The `403`-then-register-then-retry dance is real, but it is on a different operation.** The old spec put it on lakehouse artifact creation, inferring the sequence. In the recorded traffic, an unregistered organization does not fail at creation — it fails much earlier and far more obscurely, on `GET .../lakehouseArtifacts/hasPowerBIPremiumLicense`, with a bodiless `403` that is indistinguishable at the transport level from a genuine authorization failure. Both portals recover identically: within 200 milliseconds they call `updateorganizationdetails`, then repeat the licence check, which then returns `200`. A client that treats that `403` as fatal will report a licensing problem to a user who has no licensing problem.

**`updateorganizationdetails` takes no body at all.** Its inputs are query parameters — `organizationUrl` and `organizationId` — and every recorded request sends `Content-Length: 0`. One capture did send a body, and it was a client bug: the portal had serialised its own HTTP header bag into the request. The service ignored it and answered `200`.

**The datalakefolder id does not have to come from Dataverse.** The old spec's most awkward claim was that a caller who wants to unlink must resolve the `datalakefolderid` from a separate Dataverse `datalakefolders` read and persist it, because the create response does not return it — and that a link whose folder id was lost cannot be removed. That is no longer true. `GET .../lakedetails` returns it as `Id`, and the recorded unlink flows use exactly that value as the path id for `DELETE .../lakehouseArtifacts/{datalakeFolderId}` and for the lake profile. The `Id` -> `DELETE` correspondence is directly observable within a single capture.

That correction matters beyond convenience. The Dataverse route is not just indirect, it is unreliable: `cds2_workspace` and `cds3_workspace` rows exist on *every* organization whether or not it has ever been linked, alongside about eight other system folders, so the Dataverse read cannot tell a linked environment from an unlinked one. `lakedetails` can — it returns an empty array when there is no link, and it goes empty roughly thirty seconds after a successful unlink. The provider's own `getDatalakeFolderId` had a fallback that returned `value[0]` when neither named row was found, which on any organization would select an unrelated system folder for deletion; it was unreachable only because the two named rows always exist. That fallback is gone as of `@eb90b78d`: the provider now keeps only the folders a `synapselinkprofile` actually references and errors rather than guessing. That is a safer Dataverse read, not a substitute for `lakedetails` — it still cannot distinguish a Fabric link from a Synapse one except by the `cds3_workspace` name, and it was written before this capture existed.

**The provider drives three operations; the portals drive fifteen.** `internal/services/fabric_link` calls `POST .../lakehouseArtifacts`, `DELETE .../lakehouseArtifacts/{id}` and `POST .../updateorganizationdetails`, and nothing else — enough to create and destroy a link, and nothing to inspect or amend one. The other twelve operations were entirely unknown to it, and the gap is not incidental: it is the whole read side, plus the only mechanism for changing a link's table list after creation. A provider limited to those three can implement a `fabric_link` resource that creates and deletes, but it cannot implement a data source, cannot detect drift, cannot report whether a link is actually syncing, and cannot update the table list in place — every table change becomes a destroy-and-recreate. The interesting additions:

- **`GET /entities`** is the table catalogue the wizard is built from, and it is *organization*-scoped, not environment-scoped — it takes only `organizationUrl`, no path id. It returns every table including the ones that cannot be linked, each flagged with `IsDisabled` and a display-text `ReasonIfDisabled`. Across 13,690 recorded rows the only reason ever given was `Change Tracking is Disabled`, which is the single most common thing a caller will hit and the only remedy is in Dataverse, not here.
- **`GET /relationships`** returns only many-to-many relationships (`IsIntersect` was true on all 684 recorded rows) with their intersect table names. Linking both ends of an N:N does not bring the join across; the intersect table has to be linked in its own right, and this is how you find its name.
- **`GET .../lakeprofile/{id}`** is the progress endpoint, and there was no way to know it existed. It carries per-table sync state — `CurrentState` walking `InitialSyncNotStarted` -> `InitialSyncInProgress` -> `InitialSyncPostProcessing` -> `InProgress`, where `InProgress` confusingly means *done and on delta sync*. It is the only place a Link to Fabric's progress is observable at all.
- **`PUT .../lakeprofile/{id}` plus `POST .../lakeprofile/{id}/activate`** are how tables are added to and removed from an existing link. Nothing in the provider's three operations can do that; re-posting lakehouse artifacts does not change the table list.
- **`GET .../fabric/workspaces`** means a caller does not need a Fabric token to enumerate workspaces — athena proxies it. It also supplies the `capacityId` you need to filter on, since a workspace with no Fabric capacity cannot host a mirror lakehouse.

## The Fabric-link workflow, as recorded

This is the part a reader would otherwise have to guess, and guessing it wrong is expensive. The sequences below are the portals' own, observed end to end.

**Establishing a link.** The three catalogue reads fire in parallel, and the licence check with them:

```
GET  /entities?organizationUrl=…            ─┐
GET  /relationships?organizationUrl=…        ├─ in parallel
GET  /fnoTables?organizationUrl=…            │
GET  .../lakehouseArtifacts/hasPowerBIPremiumLicense  ─┘
      └─ 403 → POST .../updateorganizationdetails → repeat the check → 200
GET  .../fabric/workspaces
POST .../lakehouseArtifacts          → { WorkspaceId, LakehouseId, ConnectionId }
```

The create call is synchronous and slow — roughly forty seconds in the captures — and returns once the artifacts exist. Initial sync is *not* included in that; poll the lake profile for it.

**Changing which tables are mirrored.** Three calls, and all three are needed:

```
GET  .../lakedetails?isManagedLake&isCDS3&fetchLakehouseInfo   → Id (the datalakefolder id)
GET  .../lakeprofile/{Id}?status&publishErrorMessageToUI       → the current profile
PUT  .../lakeprofile/{Id}                                      → whole-document replace
POST .../lakeprofile/{Id}/activate                             → restart the sync jobs
POST .../updateorganizationdetails
POST .../lakehouseArtifacts?removeShortcutsFirst=true&adlsShortcuts=false
      └─ body identifies the existing lake by LakeId/FolderId; rebuilds Fabric shortcuts
```

The `PUT` is a whole-document replace, not a merge: omitting a table removes it from the link. The client reads the profile, reduces each entry from the fifty-odd fields the read returns to the six the update accepts (`Type`, `EntitySource`, `AppendOnlyMode`, `PartitionStrategy`, `RecordCountPerBlock`, `Settings`), and sends everything else back untouched. An update that is never activated leaves the stored profile changed and the running sync unchanged; an activate without the shortcut resynchronise leaves Fabric showing tables that are no longer in the link.

**Unlinking.**

```
GET    .../isIslandEnabled?organizationId&organizationUrl
GET    /entities, /relationships, /fnoTables, /isComoEnabledForOrg
GET    .../lakedetails?fetchLakehouseInfo                     → Id
GET    .../tenant/{tenantId}/getclientidfromep
POST   .../updateorganizationdetails
GET    .../lakeprofile/{Id}?…
DELETE .../lakehouseArtifacts/{Id}?dxt=false
GET    .../lakedetails?fetchLakehouseInfo                     → []
```

The delete returns `200` after about ten seconds, and `lakedetails` goes empty about thirty seconds later — so confirm the unlink by re-reading the list, not by trusting the status.

Two calls the provider makes are **not athena operations** and are not in this spec. Both are prerequisites and both are plain reads:

1. **The BAPI environment read** — `GET /providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{environmentId}`, specified in [`bapi/`](../bapi). It supplies `cluster.uriSuffix` and `azureRegion` (the host), and `linkedEnvironmentMetadata`'s `resourceId`, `instanceUrl`, `uniqueName` and `friendlyName` (the `x-ms-organization-id` header and most of the create body). Nothing on this surface can be addressed without it.
2. **The Dataverse `datalakefolders` read** — `GET /api/data/v9.1/datalakefolders`, specified in [`dataverse/`](../dataverse). Now superseded for this purpose by `lakedetails`, as above.

Note also that the Fabric workspace and the Fabric-to-Dataverse connection are composed from other providers entirely — the connection lets **Fabric read Dataverse**, not the reverse, and in the captured flow authenticates as the target workspace's system-assigned identity, which must already be a Dataverse application user holding the *Synapse Link Service Access* role.

## The host, which is still the interesting part

There is no global host and no endpoint that publishes one. The hostname is composed per environment, from two fields of a BAPI environment read that have to be joined by hand:

```
athenawebservice.{azureRegionPrefix}{clusterUriSuffix}.powerapps.com
```

`clusterUriSuffix` is `properties.cluster.uriSuffix` verbatim. `azureRegionPrefix` is the **compass-direction component of `properties.azureRegion`**, with the geography dropped — the geography is already in the cluster suffix. The two concatenate with no separator, which is why the result reads as though a stray letter had been prepended:

| `azureRegion` | `cluster.uriSuffix` | host |
|---|---|---|
| `eastus` | `us-il102.gateway.prod.island` | `athenawebservice.e` + `us-il102…` |
| `westeurope` | `eu-il102.gateway.prod.island` | `athenawebservice.w` + `eu-il102…` |
| `northeurope` | `eu-il102.gateway.prod.island` | `athenawebservice.n` + `eu-il102…` |

**The prefix is not a constant, and the recorded traffic now proves it independently of the DNS work.** The 18 captures address two hostnames. Both end in the *same* island scale unit; they differ only in the prefix — `e{island}` for environments in `australiaeast` and `se{island}` for environments in `australiasoutheast`. Same island, same cluster suffix, two different hostnames, both live, in the same tenant, in the same captures. A region with a two-word direction contributes both letters, and the prefix tracks the environment's Azure region while the cluster suffix does not move.

The Terraform provider hardcoded `e` and carried a TODO admitting it. That was correct only for east-something regions and silently wrong elsewhere — and the capture contains real traffic to exactly the hostname it would have failed to construct. It now derives the prefix from `properties.azureRegion`, and errors rather than guessing when a region carries no identifiable direction, because a wrong prefix does not produce a helpful error; it produces `NXDOMAIN`. (`terraform-provider-power-platform@eb90b78d`, on the unmerged `feature/fabric-link-ropc`.)

Two things about verifying this by probe are worth keeping, because the first nearly produced a false positive.

**DNS proves the scale unit exists, not the service.** Everything under a live island resolves: `*.eus-il102.gateway.prod.island.powerapps.com` is a wildcard CNAME onto that island's ingress gateway, so an invented hostname on a real island resolves exactly like the real one. Only a *dropped* prefix (`athenawebservice.us-il102…`) and a *nonexistent scale unit* fail to resolve. "The derived hostname resolves" is therefore almost no evidence at all.

**The gateway's own headers are the evidence.** The island gateway routes on the `Host` header. A hostname it knows is forwarded to a registered Service Fabric application, and the response carries `x-ms-webservice`, `x-servicefabric` and an upstream `server-timing` entry. A hostname it does not know is refused by the gateway itself: the same `404` status, but none of those headers. That difference is clean, costs one request, and confirms the derived host is a real service on every island tested.

The `x-ms-webservice` header, incidentally, is not a route identity, though it looks like one. It varies per request against the same URL — `ZA0000001`, `zb0000018`, `zb0000026`, `ZB0000000` were all observed for the same path within a minute — so it identifies the serving node. Only its *presence* means anything.

## CORS

Both portals are browser clients, so every non-simple request in the captures is preceded by an `OPTIONS` preflight — 124 of the 291 recorded calls. They are not operations and are not in the spec, but the behaviour is worth stating: every preflight is answered `204` by the application (not by the gateway), with `Access-Control-Allow-Methods: GET,POST,OPTIONS,PUT,DELETE,PATCH` on every path regardless of what that path actually supports, the requesting `Origin` echoed back, `Access-Control-Allow-Credentials: true`, and `Access-Control-Allow-Headers` reflecting whatever the client asked for. There is no `Access-Control-Max-Age`, so nothing is cached and every call pays for its preflight.

The blanket allow-methods list is a reflector, not a description of the route: it is identical on invented paths. It confirms the host and says nothing whatever about the routes. (By contrast the `powervamg` service on the same islands answers a preflight with `Access-Control-Allow-Methods: POST` — so the policy is per-service, not a gateway default.)

## Two things that will still mislead you

**Casing is not uniform.** Nearly every payload on this surface is PascalCase — `OrganizationId`, `WorkspaceId`, `EntityDescriptions` — which no other Power Platform API in this repository does. But `GET .../fabric/workspaces` is camelCase (`id`, `name`, `capacityId`), because athena passes Fabric's own representation straight through. And the create body's `DatalakefolderUniqueName` does not match the lake payload's `DatalakeFolderUniqueName`; the capital F moves. Go's case-insensitive unmarshalling means the provider's DTOs would work either way and cannot be used as evidence; the captures are the source.

**Two of the boolean fields lie.** `IsCDS3` on a lake row is `false` on every recorded row *including rows whose `DatalakeFolderUniqueName` is exactly `cds3_workspace`* — read the unique name instead. And `Status.InitialSyncState` on a profile reads `Completed` on profiles whose individual tables are still mid-sync; poll the per-table `CurrentState`, not the aggregate.

## Layout

```
athena/
  scripts/probe.py         the live probe harness (read-only by construction, generic, re-runnable)
  scripts/har_extract.py   the HAR inventory extractor this revision was written from (generic)
  oas/openapi.json         the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py --environment-id ENVID          # everything below
scripts/probe.py --dns-only                      # host construction; needs no credentials
scripts/probe.py --cluster-uri-suffix us-il102.gateway.prod.island --azure-region eastus
```

`probe.py` is kept because it is still the tool for the host, identity and routing questions, and because it is **read-only by construction, not by convention**: `ReadOnly.request()` raises on any method other than `GET`, `HEAD` and `OPTIONS`, in the transport, before a request object exists. There is no code path in it — or addable to it without deleting that guard — that can provision a lakehouse, register an organization or unlink anything.

```
scripts/har_extract.py ~/Desktop --match athenawebservice
scripts/har_extract.py ~/Desktop --match athenawebservice --bodies --timeline
```

`har_extract.py` reproduces the inventory this spec was written from, from any directory of HAR files and any host substring. It prints routes, statuses, query-parameter sets, body *shapes* (keys and types, never values) and per-capture timelines. It decodes HAR's base64 transport encoding and says so, which is the mistake it exists to prevent. Its `--json` mode writes raw bodies for local analysis; that output contains real tenant data and must never be committed.

## Conventions

- 15 operations over 14 paths, 19 schemas, 6 tags, OpenAPI 3.0.3.
- **No `api-version` parameter anywhere.** This surface has none.
- `x-probe-verified: true` on all 15 operations and on all schemas derived from observed bodies. The single `false` in the file is on `/fnoTables`' row schema, whose shape was never observed because every recorded call returned an empty array. The `servers` entry is `true` — its host construction is confirmed both by the two hostnames in the captures and by gateway-header probing on further islands.
- **Nothing is marked `required` in the request bodies.** Every recorded request sent every field of its shape, so no field's necessity was tested. `required` appears only on parameters that are structurally required — path segments, the query parameters the route is meaningless without, and `x-ms-organization-id` where every recorded call carried it.
- `required` *is* used on response schemas, where it records fields present on every observed row.
- Closed sets carry `enum` only where every observed value is listed and the set is plausibly complete (`PartitionStrategy`, `CurrentState`, `InitialSyncState`). Where a single value was observed but the set is obviously larger — `ReasonIfDisabled`, `AccessType`, `DestinationType` — the description states the value the service returns and no enum is asserted. The host's direction prefix sits in `x-observed-values` on the server variable for the same reason.
- Status-code meanings live under their own response entries, never in operation descriptions.

## Status

Spec rewritten from 18 HAR captures (291 recorded calls) of two Microsoft portals driving real Link to Fabric workflows, 2026-08, with the host construction, identity model and routing behaviour additionally confirmed by live directory and DNS probing. Validates against `openapi-spec-validator`.

**Nothing was created, modified or deleted by this exercise.** The captures are recordings of work the tenant's owner did through Microsoft's own portals; no request was issued to this service by any script here. The HAR files themselves are not committed and never should be — they contain organization ids, tenant ids, Fabric workspace names, storage account names and bearer tokens. Every id, hostname and name in this spec is a neutral placeholder.
