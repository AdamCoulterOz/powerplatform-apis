# athena

The orchestration service behind Dataverse **Link to Microsoft Fabric** and Azure Synapse Link — known internally as *athena*, and formally as the Microsoft first-party application **"Azure Synapse Link for Dataverse"**. It is what the maker portal's Link to Fabric wizard actually drives: it creates the mirror lakehouse inside a target Fabric workspace, writes the `synapselinkprofile` and `datalakefolder` rows into Dataverse server-side, and tears the link down again.

**This is not the Power Platform admin centre API.** That is a different service, on a different host, with a different scope, and it is specified in [`admin/`](../admin). The two have nothing to do with each other beyond both being unofficial. This repository previously conflated them; it no longer does.

## Read this first

This spec is derived from an **unmerged feature branch** of a fork of the [Terraform provider](https://github.com/microsoft/terraform-provider-power-platform) — `internal/services/fabric_link`, which itself reverse-engineered the surface from a maker-portal HAR capture. That feature has not shipped. The API may change before it does, and the provider's own reading of it may be wrong in ways nothing here would catch.

**It is the least-verified spec in this repository, and by some distance.** Every operation carries `x-probe-verified: false`. That is not an oversight; it is the honest result, and the reason is structural rather than circumstantial.

## Why nothing here could be verified

Three properties of this boundary compound.

**There are no read operations.** The entire surface is one POST that provisions a real Fabric integration, one POST that mutates an organization's registration, and one DELETE that destroys the integration. There is no list, no read, no status, no dry-run. Nothing on it can be exercised without changing something, and provisioning a link additionally requires a Fabric workspace id and a Fabric-to-Dataverse connection id that this exercise did not have. The shared probe environment used elsewhere in this repository has been deleted. There was no safe place to do it and nothing was done anywhere.

**The service does not distinguish a wrong method from a wrong path.** Elsewhere in this repo, route existence is established for free: a GET against a POST-only route answers `405` with an `Allow` header, or a wrong `api-version` answers `400 UnsupportedApiVersion` — either proves the route is there without invoking it. That technique does not work here. Every `GET`, `HEAD` and `OPTIONS`, against the three documented paths and against invented ones alike, answers an identical bare `404`: no body, no `Allow` header, no `Content-Type`, no `api-version` parameter to get wrong. The three paths in `oas/openapi.json` are there because the provider and the HAR capture say so, not because the service confirmed them.

**Authentication is unobservable too.** Routing fails before authentication runs, so a valid token, no token, a wrong-audience token and the literal string `not-a-token` all produce the same `404`. Nothing on this host ever issues a `WWW-Authenticate` challenge, so unlike every other boundary here, the audience cannot be discovered by asking. It is knowable only from the token itself or from captured traffic.

What *was* established live is set out below. It is mostly about the outside of the service rather than its inside.

## Layout

```
athena/
  scripts/probe.py     the live probe harness (read-only by construction, generic, re-runnable)
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py --environment-id ENVID          # everything below
scripts/probe.py --dns-only                      # host construction; needs no credentials
scripts/probe.py --cluster-uri-suffix us-il101.gateway.prod.island --azure-region eastus
scripts/probe.py --environment-id ENVID --skip-dataverse
```

It takes an Entra token for `7f15f9d9-cad0-44f1-bbba-d36650e07765/.default` from the logged-in az CLI session (or `ATHENA_TOKEN`), and separate tokens for the two prerequisite reads. Ids come from the command line or the environment, never from source. It prints statuses, header presence and shapes — no tenant id, environment id, organization id, Dataverse hostname or token.

**It is read-only by construction, not by convention.** `ReadOnly.request()` raises on any method other than `GET`, `HEAD` and `OPTIONS`, in the transport, before a request object exists. There is no code path in it — or addable to it without deleting that guard — that can provision a lakehouse, register an organization or unlink anything.

## The host, which is the interesting part

There is no global host and no endpoint that publishes one. The hostname is composed per environment, from two fields of a BAPI environment read that have to be joined by hand:

```
athenawebservice.{azureRegionPrefix}{cluster.uriSuffix}.powerapps.com
```

`clusterUriSuffix` is `properties.cluster.uriSuffix` verbatim. `azureRegionPrefix` is the **compass-direction component of `properties.azureRegion`**, with the geography dropped — the geography is already in the cluster suffix. The two concatenate with no separator, which is why the result reads as though a stray letter had been prepended:

| `azureRegion` | `cluster.uriSuffix` | host |
|---|---|---|
| `eastus` | `us-il101.gateway.prod.island` | `athenawebservice.e` + `us-il101…` |
| `westeurope` | `eu-il101.gateway.prod.island` | `athenawebservice.w` + `eu-il101…` |
| `northeurope` | `eu-il101.gateway.prod.island` | `athenawebservice.n` + `eu-il101…` |

A region with a two-word direction contributes both letters: an `australiasoutheast` environment gives `se`, not `e`.

The Terraform provider hardcodes `e` and carries a TODO admitting it. That is correct only for east-something regions and silently wrong elsewhere — a wrong prefix does not produce a helpful error, it produces `NXDOMAIN`.

Two things about verifying this are worth knowing, because the first one nearly produced a false positive.

**DNS proves the scale unit exists, not the service.** Everything under a live island resolves: `*.eus-il101.gateway.prod.island.powerapps.com` is a wildcard CNAME onto that island's ingress gateway, so an invented hostname on a real island resolves exactly like the real one. Only a *dropped* prefix (`athenawebservice.us-il101…`) and a *nonexistent scale unit* fail to resolve. "The derived hostname resolves" is therefore almost no evidence at all.

**The gateway's own headers are the evidence.** The island gateway routes on the `Host` header. A hostname it knows is forwarded to a registered Service Fabric application, and the response carries `x-ms-webservice`, `x-servicefabric` and an upstream `server-timing` entry. A hostname it does not know is refused by the gateway itself: the same `404` status, but none of those headers. That difference is clean, costs one request, and confirms the derived host is a real service on every island tested. It is why the `servers` entry in the spec is the one thing marked `x-probe-verified: true`.

The CORS preflight is a second, weaker confirmation: `OPTIONS` with an `Origin` and `Access-Control-Request-Method` is answered `204` by the application rather than 404'd by it. But it is a blanket reflector — the same fixed `GET,POST,OPTIONS,PUT,DELETE,PATCH` for every path including invented ones, any `Origin` echoed back, any requested header allowed, with `Access-Control-Allow-Credentials: true`. It confirms the host and says nothing whatever about the routes. (By contrast the `powervamg` service on the same islands answers a preflight with `Access-Control-Allow-Methods: POST` and `Origin: *` — so the policy is per-service, not a gateway default.)

## What live probing established

Nothing that could be probed was in the spec's request or response bodies, so the findings are about identity, the host, and the caller's surrounding workflow. Several of them correct the source the spec is derived from.

- **The service's identity, from the directory.** Application `7f15f9d9-cad0-44f1-bbba-d36650e07765` is **"Azure Synapse Link for Dataverse"**, owned by the Microsoft first-party tenant, with the identifier URI **`https://exporttodatalake.com/`**. Its single delegated permission `user_impersonation` carries the admin-consent text *"Have access to Dynamics 365 Athena - CDS to Azure data lake API"* — which independently confirms both the internal name and the design doc's claim that athena is the old Export to Data Lake service. Both `7f15f9d9-…/.default` and `https://exporttodatalake.com/.default` are issuable and produce different `aud` claims; which the service accepts is untested, because testing it means provisioning something.

- **App-only tokens cannot work here, and now there is a reason rather than an observation.** The application publishes **zero application roles**. A client-credentials token therefore arrives with no `roles` claim and there is nothing for the service to authorize it as. The design doc inferred "the provisioning path requires a delegated token" from a failed attempt; the directory says it categorically. This is why the provider's `fabric_link` resource is driven through a username/password alias while every other resource in that provider uses the default app-only identity.

- **The provider's BAPI api-version is unnecessary.** `internal/services/fabric_link` pins `api-version=2020-10-01-alpha` on the environment read, an oddity worth explaining. There is nothing to explain: `2020-10-01`, `2021-04-01`, `2022-05-01`, `2023-06-01` and `2024-05-01` all return `properties.cluster.uriSuffix`, `properties.azureRegion` and the full `linkedEnvironmentMetadata` identically. Nothing requires the alpha version. See [`bapi/`](../bapi) for that operation.

- **`cds2_workspace` and `cds3_workspace` are stock system rows, not artefacts of a link.** The design doc states "Link to Fabric creates both a `cds2_workspace` and a `cds3_workspace` folder". It does not. An environment with **zero** `synapselinkprofiles` rows already carries **ten** `datalakefolders` rows, `cds2_workspace` and `cds3_workspace` among them, alongside `msdyn_analytics`, `msdyn_processadvisor` and others. The consequence is a live bug in the provider's `getDatalakeFolderId`: its final fallback returns `value[0]` when neither `cds3_workspace` nor `cds2_workspace` is found, and on any never-linked organization that selects an unrelated system folder — which `DELETE .../lakehouseArtifacts/{id}` would then be asked to remove. The fallback is unreachable in practice only because the two named folders always exist. The delete operation's description says which folder to name and warns against the positional fallback. The read itself belongs to [`dataverse/`](../dataverse).

- **The `x-ms-webservice` header is not a route identity.** It looked like one. It varies per request against the same URL (`ZA0000001`, `zb0000018`, `zb0000026`, `ZB0000000` were all observed for the same path within a minute), so it identifies the serving node, not the service or the route. Only its *presence* means anything.

- **There is no error envelope to document.** Every observable failure on this host is a `404` with `Content-Length: 0`. The `403` and `404` semantics in the spec — the empty-bodied `403` meaning "organization not registered with this island", the `DatalakefolderNotFoundException` meaning "no organization context" — come from the HAR capture and the provider's comments, not from anything reproduced here.

## The caller's workflow, and what belongs to other specs

Two of the calls in the provider's `fabric_link` client are **not athena operations** and are not in this spec. They are prerequisites, and both are plain reads:

1. **The BAPI environment read** — `GET /providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{environmentId}`, specified in [`bapi/`](../bapi). It supplies `cluster.uriSuffix` and `azureRegion` (the host), and `linkedEnvironmentMetadata`'s `resourceId`, `instanceUrl`, `uniqueName` and `friendlyName` (the `x-ms-organization-id` header and most of the create body). Nothing on this surface can be addressed without it.
2. **The Dataverse `datalakefolders` read** — `GET /api/data/v9.1/datalakefolders`, specified in [`dataverse/`](../dataverse). The create response does not contain the `datalakefolderid` that the unlink needs, so a caller intending to tear the link down must resolve it separately and persist it. A link whose folder id was lost cannot be removed through this API.

The full sequence, then:

```
BAPI environment read            -> host, organization id, organization url, unique/friendly name
  POST .../lakehouseArtifacts    -> 403 if the organization is new to the island
  POST .../updateorganizationdetails
  POST .../lakehouseArtifacts    -> base64( { WorkspaceId, LakehouseId, ConnectionId } )
Dataverse datalakefolders read   -> the datalakefolderid to persist for later
  DELETE .../lakehouseArtifacts/{datalakeFolderId}
```

The `403`-then-register-then-retry shape is the maker portal's, not an invention: the wizard does not register speculatively. Note also that the Fabric workspace and the Fabric-to-Dataverse connection are composed from other providers entirely — the connection lets **Fabric read Dataverse**, not the reverse, and in the captured flow authenticates as the target workspace's system-assigned identity, which must already be a Dataverse application user holding the *Synapse Link Service Access* role.

## Two things that will mislead you

**The response is not JSON.** `POST .../lakehouseArtifacts` returns a JSON *string* containing base64-encoded JSON. Decode, then parse. The spec models this as `type: string, format: byte` with the decoded shape hung off it as `x-decoded-schema`, because that is what is on the wire.

**PascalCase.** Every property in the request and response bodies is PascalCase — `OrganizationId`, `WorkspaceId`, `EntityDescriptions`. No other Power Platform API in this repository does this. Go's case-insensitive unmarshalling means the provider's DTOs would work either way and cannot be used as evidence of the casing; the HAR capture is the source.

## Conventions

- 3 operations over 3 paths, 4 schemas, 2 tags (Lakehouse Artifacts, Organization Registration), OpenAPI 3.0.3.
- **No `api-version` parameter anywhere.** This surface has none — which is also why the usual wrong-version route-existence probe is unavailable.
- `x-probe-verified: false` on all three operations and all four schemas. The only `x-probe-verified: true` in the file is on the `servers` entry, whose host construction was confirmed live on two islands.
- **Nothing is marked `required` in the request bodies.** No request was ever sent, so no field's necessity was tested. `required` appears only on parameters that are structurally required — path segments, and the `x-ms-organization-id` header, whose absence the provider documents a concrete failure for.
- Closed sets carry `enum` only where a value is genuinely all that is known (`EntitySource: Dataverse`). The host's direction prefix is plainly a larger set than the four confirmed, so it sits in `x-observed-values` on the server variable rather than in a false `enum` — the same treatment `admin/` gives `organizationType`.
- Status-code meanings live under their own response entries, never in operation descriptions.

## Status

Spec written from an unmerged provider feature branch and a maker-portal capture, with the host construction, the identity model, the routing and auth behaviour, and the two prerequisite reads confirmed against a live tenant (2026-08). Validates against `openapi-spec-validator`.

**Nothing was created, modified or deleted anywhere.** No Fabric link, lakehouse artifact, datalake folder or organization registration was touched, on any environment. The three operations in this spec remain unexercised and are documented as such.
