# admin

The Power Platform admin centre API (`api.admin.powerplatform.microsoft.com`): the service the admin centre itself calls. This spec covers its release-wave surface — the per-environment opt-in to a Dataverse release wave.

## Why this one is different

Every other API in this repo addresses an **environment** by its Power Platform environment id. This one does not. It addresses a **Dataverse organization** by organization id, together with a **geo** — and it will never accept the environment id. Passing one gets a `403`, indistinguishable from a permission failure, because this API has no `404`.

So a caller starting from an environment id has two mandatory hops before it can call anything here:

```
environmentId
  -> BAPI: GET .../environments/{environmentId}
     take properties.linkedEnvironmentMetadata.resourceId   = organizationId
  -> this API: GET /api/tenants/mytenant/organizations
     find that id, take its crmGeo                          = geo
  -> GET /api/environments/{organizationId}/features?geo={geo}
```

The organization listing is the only place the geo is published, which makes it less a resource than a lookup table. And `crmGeo` is a CRM geo, not a Power Platform location: an environment BAPI reports in `australia` is `Oce` here. The two vocabularies never meet.

## Layout

```
admin/
  scripts/probe.py     the live probe harness: re-derives everything the spec claims
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

Two sources, in order. The Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform) supplied the inventory: `internal/clients/admin` holds all three calls, and its unit tests pin the exact URLs. Live probing supplied everything else — and corrected the provider in several places, which is the point of the exercise.

`probe.py` is that probing, made repeatable. It takes no ids from source; organizations come from the tenant listing, and the one mutation runs only against ids passed on the command line. Its output is a *shape* summary — no organization ids, no Dataverse hostnames, no tenant id — so it is safe to paste into an issue.

```
scripts/probe.py                            # organizations, features, paging, geos, errors
scripts/probe.py --geos                     # re-enumerate the geo enum only
scripts/probe.py --enable ORG:GEO:FEATURE   # the one mutation, opt-in and explicit
```

The scope is a bare first-party application id rather than a URL:

```
az account get-access-token --scope 065d9450-1e87-434e-ac2f-69af271549ed/.default
```

## Two things that will mislead you

**Unmatched routes do not 404.** Every path this host does not recognise — `/`, `/api/anything`, and *every* method including `POST` and `DELETE` — answers `200` with the `text/html` body `This action is to redirect legacy routes`. A `200` proves nothing here; only a JSON content type does. This is why `probe.py` has an `is_real()` predicate and why `GET /api/environments/{organizationId}/features/{featureName}` is not in the spec: it looks like it works, and it is the fallback. Reading one feature means listing all of them and filtering client-side.

**Error bodies come in three unrelated shapes.** Parameter validation returns a bare JSON *array of strings* (`["The value 'ZZ' is not valid."]`). An upstream fault returns a `{code, message, requestId}` object. An organization the caller cannot administer returns an empty body. A client must branch on the JSON's top-level type before it can read either shape.

## What probing changed

| | Provider's view | What the service does |
|---|---|---|
| Feature property casing | camelCase `json` tags | **PascalCase** on the wire. Go's case-insensitive unmarshalling hides it. |
| Feature fields | 11 | **14** — `IsOrgGeoOptedIn`, `GeneralAvailabilityDate`, `AppInstallationStatus`. |
| Feature envelope | `{values}` | `{values, count, totalCount, nextPageToken}` — all three extras inert. |
| Organization fields | 7 | 7. Nothing hidden; there is no friendly name, version, state or cluster here at all. |
| `geo` | opaque string | A validated **20-value enum**, matched case-insensitively. |
| `geo` semantics | the org's location | The **release calendar**, not the organization. Same org under `NA`/`EMEA`/`Oce` returns identical opt-in state and three GA dates three weeks apart. |
| Missing `geo` | — | `500`, not `400`, on the listing — bound before validated. On `enable`, `403`. |
| Unknown organization | — | `403` with an empty body. Never `404`. |
| Paging | — | `pageSize`, `$top`, `pageToken` all accepted, all ignored. |

`crmGeo` returned `Oce` for every organization in the probed tenant, so the provider's `NA` test fixture is representative of nothing. Enumerating the geo parameter against the live service — valid codes `200`, invalid `400` — recovered the full set of twenty; four more (`CHN`, `USG`, `DOD`, `TIP`) are recognised but belong to sovereign clouds and fault on the public host.

## Conventions

- 3 operations over 3 paths, 5 schemas, tagged by logical resource (Organization, Release Wave Feature), OpenAPI 3.0.3.
- **No `api-version` parameter anywhere.** This surface has none.
- Nothing is marked `required` on response schemas; every field documented was present on every object observed, but the service's own optionality is unverified.
- `x-probe-verified: true` marks what was confirmed live. The enable mutation carries `false`: it is irreversible — `CanBeReset` is `false` on every wave feature, and there is no disable operation — so only its failure paths were exercised. Its request shape comes from the provider client and its unit tests.
- Enums carry what was proven. Where a set is plainly larger than what was seen (`organizationType`, `relationType`), the observed values sit in `x-observed-values` rather than in a false `enum`. `FeatureName` is enumerated but is a dated snapshot: the service lists exactly the waves in their opt-in window, so the `pattern` outlives the `enum`.

## Status

Spec written from the provider client and corrected against a live tenant (2026-08); validates against `openapi-spec-validator`; rendered by the browser at the repo root. Nothing was created or modified in the probed tenant — the surface is two reads plus one mutation that was deliberately not run.
