# analytics

The Power Platform admin analytics API — "CS Analytics", served from regional hosts such as `na.csanalytics.powerplatform.microsoft.com` — which backs **Data export** in the Power Platform admin center: the tenant-wide list of analytics data-export connections, each pointing a set of environments at an Application Insights sink.

It is a tiny API. One resource, one useful operation. What makes it worth a folder of its own is everything *around* that operation.

## Why this one is different

**There is no server.** Every other spec in this repo names a host. This API is deployed once per geography, publishes no discovery endpoint for those hosts, and answers on all of them — so *choosing the host is part of the contract*, and getting it wrong is not an error. A valid token is accepted on every regional host; the wrong one returns `200` with that geography's list, which for most tenants is empty. A caller that guesses gets a plausible, silently wrong answer.

The host table therefore lives in the spec three times over, generated from one source: as the `region` server-variable `enum`, as the `enum` on `GatewayCluster.geoName`, and in full — with per-entry provenance — as `info.x-region-hosts`.

**Finding your region takes a second API.** `GET /gateway/cluster` on the tenant-scoped Power Platform API host returns the caller's `geoName`, which indexes that table. It belongs to [ppapi](../ppapi), not here, but the analytics operation is unusable without it, so it is reproduced under the *Region Discovery* tag with its own `servers` and `security` overrides.

## Layout

```
analytics/
  scripts/probe.py     the live probe harness — read-only, re-runnable
  scripts/build.py     emits oas/openapi.json deterministically
  oas/openapi.json     the spec (hand-owned)
  README.md
```

The spec is **owned directly**, like [bapi](../bapi)'s: there is no upstream reference to regenerate from. `build.py` is not a generator in the ppapi sense — it is a formatter, so that `indent=1` output stays byte-stable and the region table cannot drift between the three places it appears. Edit the structures in `build.py`, re-run it, commit the JSON.

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

## What could not be probed

**The item schema.** The probe tenant has no data-export connections configured, so `value` came back empty on all twenty hosts. Everything below `ConnectionListResponse.value` — `Connection`, `Sink`, `ConnectionStatus`, `ConnectionEnvironment` — is derived from the Terraform provider's DTOs and its one recorded admin-center fixture. Those schemas carry **no** `x-probe-verified` flag, and their `enum`s each carry an `x-enum-evidence` note saying what the values were observed in and that the set may be larger. No field is marked `required`, and no field was invented: in particular the API exposes **no schedule, frequency or retention configuration**, so none is documented — `status[].lastRunOn` is the only timing signal a connection carries.

The sovereign hosts (`gcc`, `high`, `dod`) were confirmed reachable but reject a commercial-cloud token, so their paths are unverified.

A note on the sink: `Sink.key` is an Application Insights instrumentation key, returned in plain text by the listing. Treat the whole response body as a credential.

## Conventions

- 3 operations over 3 paths, 6 schemas, OpenAPI 3.0.3.
- Two security schemes: the analytics scope for the connections operations, the Power Platform API scope for region discovery, applied per operation.
- `x-probe-verified: true` marks the three operations and the two envelope schemas confirmed live. Its absence on the connection item schemas is deliberate.

## Status

Spec written and validated; operations and host table live-verified against a tenant in the `oce` geography. The item schema awaits a tenant with a data-export connection configured.
