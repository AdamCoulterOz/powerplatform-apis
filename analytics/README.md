# analytics

The Power Platform admin analytics surface: **two separate services** that the admin center's analytics pages call, both geo-prefixed and both undocumented.

- **CS Analytics** (`{geo}.csanalytics.powerplatform.microsoft.com`) backs **Data export** — the tenant-wide list of analytics data-export connections, each pointing a set of environments at an Application Insights sink — plus tenant analytics consent, inventory tags and out-of-box settings.
- **Admin Analytics** (`{geo}.adminanalytics.powerplatform.microsoft.com`) serves the reporting and monitoring surface: the `/api/v1/cds/*` reports, the resource-metric routes behind Monitoring Hub, and the environment-group compliance routes.

They are different deployments with different aliases in the admin center's own service table (`ConfigService` and `AnalyticsForOrg`/`AnalyticsForTenant`/`AnalyticsInsightsApi`), so operations carry a per-operation `servers` override rather than being merged into one host.

What makes the data-export operation worth a folder of its own is everything *around* it.

## Why this one is different

**There is no server.** Every other spec in this repo names a host. This API is deployed once per geography, publishes no discovery endpoint for those hosts, and answers on all of them — so *choosing the host is part of the contract*, and getting it wrong is not an error. A valid token is accepted on every regional host; the wrong one returns `200` with that geography's list, which for most tenants is empty. A caller that guesses gets a plausible, silently wrong answer.

The host table therefore lives in the spec three times over, generated from one source: as the `region` server-variable `enum`, as the `enum` on `GatewayCluster.geoName`, and in full — with per-entry provenance — as `info.x-region-hosts`.

**Finding your region takes a second API.** `GET /gateway/cluster` on the tenant-scoped Power Platform API host returns the caller's `geoName`, which indexes that table. It belongs to [ppapi](../ppapi), not here, but the analytics operation is unusable without it, so it is reproduced under the *Region Discovery* tag with its own `servers` and `security` overrides.

## Two services, one spec

Every operation says which host serves it: the document-level `servers` block is CS Analytics, and each Admin Analytics operation overrides it. Resolving the region is identical for both — one geo short code, one lookup — which is why they share a folder rather than being split.

The correction that produced this split is worth stating, because the obvious guess is wrong: `/api/v1/cds/*` is **not** on `csanalytics`. Those routes are built against the `AnalyticsForOrg` / `AnalyticsForTenant` aliases, which resolve to `adminanalytics`. `csanalytics` is the `ConfigService` alias and serves sinks, connections, consent, inventory tags and `oobsettings`.

Three further Admin Analytics hosts appear in the ring table and are **not** in the spec, because nothing observed a route on them: `adminanalytics.powerplatform.microsoft.com` without a geo prefix (the insights alias, which does serve `/api/echo` and the environment-group routes), `{geo}.dfanalytics.powerplatform.microsoft.com`, and the `-test`/`-preprod` rings.

## Layout

```
analytics/
  scripts/probe.py     the live probe harness — read-only, re-runnable
  scripts/build.py     emits oas/openapi.json deterministically
  oas/openapi.json     the spec (hand-owned)
  README.md
```

The spec is **owned directly**, like [bapi](../bapi)'s: there is no upstream reference to regenerate from. `build.py` is not a generator in the ppapi sense — it is a formatter, so that `indent=1` output stays byte-stable and the region table cannot drift between the three places it appears.

**`build.py` is behind the spec, and it now refuses to run rather than catch up by deleting.** It emits only the three originally probed operations; the other 26 were added directly to `oas/openapi.json` from the admin centre's bundles. Running it prints the 26 it would drop and exits non-zero.

That guard replaced a real hazard rather than a theoretical one. The script used to `open(out, "w")` and dump into the handle, which truncated the published spec *before* the replacement existed — so a raise inside `spec()` left a half-written file, and a clean run silently deleted 26 operations and reported success. It now builds in memory, compares against what is published, refuses on any loss, and only then writes through a temp file and `os.replace`.

Treat the JSON as the source of truth. To make `build.py` whole again, either teach it the 26 operations or move the hand-authored surface into an enrichment file it merges, the way [ppapi](../ppapi) does with `enrichment.json` — do not delete operations to make a run pass.

```
python3 scripts/build.py                 # rewrite oas/openapi.json

python3 scripts/probe.py                 # region discovery -> host sweep -> operations -> edges
python3 scripts/probe.py --hosts         # host reachability sweep only
python3 scripts/probe.py --region oce    # skip discovery, probe one host
python3 scripts/probe.py --edges         # contract-edge probes only
```

`probe.py` takes tokens from the logged-in Azure CLI session, takes ids from arguments or environment variables, and prints shapes and status codes rather than tenant data. Every request it makes is a read.

## What live probing changed

Probed on 2026-08-27 against a real tenant. Against the provider-only view, this is what moved:

- **The provider's region map is broken for the tenant that was probed.** `gateway/cluster` returns `geoName: "au"`. The provider upper-cases that and looks up `AU`, which its map does not contain, so its analytics data source fails with `invalid region: au` *before issuing a request*. There is no `au` host — `oce` serves Australia.
- **`dod.csanalytics.csanalytics.appsplatform.us` does not exist.** The provider's map doubles the `csanalytics` label for the DoD region. That name is NXDOMAIN; `dod.csanalytics.appsplatform.us` resolves and answers. The spec carries the corrected host, and `info.x-region-hosts.x-provider-defects` records the defect.
- **Two live hosts the provider has never heard of:** `pol` (Poland) and `ita` (Italy), both `200`. Twenty commercial hosts answer in total, each fronting a distinct physical cluster — the `x-ms-islandgateway` response header names it, which is how each prefix was confirmed to be a separate deployment rather than an alias.
- **`sg.csanalytics.powerplatform.microsoft.com` resolves but is not this service** — it `404`s the path. DNS resolution alone is not evidence of a deployment, which is why the sweep issues a request.
- **The path is read-only.** `OPTIONS`, `POST`, `PUT`, `PATCH`, `DELETE` and `HEAD` all return `405` with `Allow: GET`. The provider carries a `DataCreateDto` shaped like a create body; no such operation exists on this path.
- **There is no per-connection read.** `/api/v2/connections/{id}` `404`s, as does every other `/api/v2/...` sibling guessed at (`environments`, `sinks`, `scenarios`, `packages`, `sources`, `settings`, `status`, `exports`, `tenants`). The surface really is one path.
- **`/api/v1/connections` still answers**, on every host, identically to v2 against an empty tenant.
- **Query parameters are ignored, not rejected.** `$top`, `$filter`, `source`, `environmentId`, `api-version` — all accepted, all `200`, no filtering. There is no paging, no `nextLink` and no `@odata` metadata.
- **The tenant GUID in the PPAPI gateway host is decorative.** A bogus tenant label, and even `api.powerplatform.com` with no tenant label at all, return the caller's own cluster: the answer comes from the token. `api-version` on that operation is likewise optional and ignored.
- **Three distinct `401` bodies**, all `text/plain` rather than JSON, emitted by the gateway before the service sees the request: empty with `WWW-Authenticate: Bearer error="invalid_token"` when the header is absent, `MISE unauthorized.` for a malformed bearer, and `An error occurred processing your authentication.` for a well-formed token with the wrong audience. That last one is the trap — the analytics hosts reject Power Platform API tokens.

## What the admin centre's bundles added

The probe found one useful operation. Reading the admin center's own JavaScript bundles found 26 more, and this is the only client that touches either host — no Microsoft SDK or PowerShell module calls them at all. Every one of those operations is marked `x-source: ppac-spa` and **none** carries `x-probe-verified`: a shipped client proves a route exists in the client, not that it answers.

What the bundles gave beyond paths:

- **Request bodies with real fields**, for the five write routes that previously carried a bare `{"type": "object"}`: both sink-connection creates, both inventory-tag writes and the tenant-setting update. The v2 create's `resourceProvider` enum is four *space-containing* strings (`cloud flow`, `customer service`, `dataverse`, `power apps`), and two sink fields are attached by a later `Object.assign`, so they are present only on the VNet path.
- **Response envelopes for nine reports**, read at the *consumer* — the code that walks the parsed response — rather than from a schema. The CDS reports return `Data` with a capital D; `CopilotUsageV2` breaks that convention and returns `copilotHubData`; the metrics routes return `metricGroups`/`lastRefreshed`/`totalCount`; the tenant-settings read returns a `value` array even for a single key. Only fields the client touches are listed, and every one of those schemas says so.
- **A construction rule, not a path.** The three resource-metric routes are assembled as `/api/v1` + (`` | `/admin`) + `/metrics/...`, with the segment chosen from the caller's role at request time. Both forms are live. Only the non-admin form is written out under `paths`; the rule is recorded in each operation's `x-notes` so a caller can build the other.
- **Two DELETEs that are not shaped like DELETEs**: the inventory-tag remove carries a JSON body, and the v1/v2 sink deletes order their path segments differently from each other.

What they did **not** give: a response shape for `CategorySeries` or for the resource-metric time series. Both are called and neither response is read field-by-field anywhere in the bundles, so both keep an untyped 200 rather than borrowing their siblings' envelope.

## What could not be probed

**The item schema.** The probe tenant has no data-export connections configured, so `value` came back empty on all twenty hosts. Everything below `ConnectionListResponse.value` — `Connection`, `Sink`, `ConnectionStatus`, `ConnectionEnvironment` — is derived from the Terraform provider's DTOs and its one recorded admin-center fixture. Those schemas carry **no** `x-probe-verified` flag, and their `enum`s each carry an `x-enum-evidence` note saying what the values were observed in and that the set may be larger. No field is marked `required`, and no field was invented: in particular the API exposes **no schedule, frequency or retention configuration**, so none is documented — `status[].lastRunOn` is the only timing signal a connection carries.

The sovereign hosts (`gcc`, `high`, `dod`) were confirmed reachable but reject a commercial-cloud token, so their paths are unverified.

A note on the sink: `Sink.key` is an Application Insights instrumentation key, returned in plain text by the listing. Treat the whole response body as a credential.

## Conventions

- 29 operations over 27 paths, 23 schemas, nine tags, OpenAPI 3.0.3.
- Two security schemes: the analytics scope for the connections operations, the Power Platform API scope for region discovery, applied per operation.
- `x-probe-verified: true` marks the four operations and the two envelope schemas confirmed live. Its absence everywhere else — on the connection item schemas and on all 25 bundle-derived operations — is deliberate: nothing else here has been executed against a tenant.
- `x-source` carries the evidence grade: 25 operations are `ppac-spa` and four are `live`. Three of the four also carry `x-corroborated-by: ["ppac-spa"]` — the two data-export lists and the tenant-consent read, which the probe and the shipped client reached independently.

## Status

Spec written and validated. Four operations and the host table are live-verified against a tenant in the `oce` geography; the other 25 come from the admin centre's bundles and have never been executed. The data-export item schema awaits a tenant with a connection configured, and the Admin Analytics report rows await either a probe or a bundle that reads them field-by-field.
