# licensing

The Power Platform licensing service (`licensing.powerplatform.microsoft.com`): the tenant-wide store of record for entitlements — storage and API capacity, pay-as-you-go billing policies and the Azure subscriptions behind them, per-currency purchase and allocation reports, and per-user product trials.

## Why this one is different

**Nothing calls it.** Every other spec in this repo documents an API the Terraform provider uses. This one documents an API the provider *declares and then forgets*. `PUBLIC_LICENSING_API_DOMAIN` sits at `internal/constants/constants.go:33`, with `USDOD`/`USGOV`/`USGOVHIGH`/`CHINA`/`EX`/`RX` siblings at lines 47, 61, 75, 89, 104 and 119. All seven are pinned by `constants_test.go` and threaded into `config.ProviderConfigUrls.LicensingUrl` for every cloud in `provider.go`. That field is never read. There is no call site, no client package, no request. The provider's own `internal/services/licensing` package — billing policies and their environment links — talks to `api.powerplatform.com/licensing` instead.

So the seven hostnames are dead configuration, and they are also the only published record that this host exists at all: it has no Microsoft Learn reference, no `swagger.json`, no service document, no health endpoint. Recording those seven names, and what is behind the one that could be probed, is most of what this folder is for.

**Three version segments coexist on one host, and none of them is an api-version.** Routes are `/{segment}/tenants/{tenantId}/...` where `{segment}` is `v0.1-alpha`, `v1.0` or `v2.0` — a literal part of the route template, not a version negotiated with the service. See *[The versioning is not versioning](#the-versioning-is-not-versioning)*.

## Layout

```
licensing/
  scripts/probe.py     the live probe harness — read-only by construction, re-runnable
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

There is no `extract.py`: there is no provider client to extract from.

```
scripts/probe.py --tenant TENANT_ID
scripts/probe.py --tenant T --environment E --user U       # widen the coverage
scripts/probe.py --tenant T --sections recorded,versioning
scripts/probe.py --hosts                                   # sovereign DNS sweep, no token
```

Ids come from arguments or `LICENSING_TENANT_ID` / `LICENSING_ENVIRONMENT_ID` / `LICENSING_USER_ID`; nothing is hardcoded. Output is shapes, status codes, key names and enum vocabulary — never a tenant id, environment id, user object id, billing policy id or name, Azure subscription id or resource group, and never a token.

`probe.py` is **read-only by construction**, following `advisor/scripts/probe.py` and `athena/scripts/probe.py`: its transport raises on any method other than `GET`, `HEAD` and `OPTIONS`, and never sends a request body. This is not politeness — the probed tenant has two live billing policies covering eight real environments, and a `PUT` here is a change to production billing configuration.

The scope is the host's own name:

```
az account get-access-token --scope https://licensing.powerplatform.microsoft.com/.default
```

## How it relates to the Power Platform API

`api.powerplatform.com` serves the same resources under `/licensing/` — billing policies, their environment links, currency reports, `allocationsByEnvironment`, tenant capacity, entitlements, ISV contracts — with the same route nouns, in the same order, under the same `/licensing/` prefix. The two hosts front the same service; [ppapi](../ppapi) is the tenant-scoped façade and this is the thing behind it.

| | this host | [ppapi](../ppapi) `/licensing/…` |
|---|---|---|
| Tenant | named in the path, `/tenants/{tenantId}/…` | taken from the token; no tenant segment exists |
| Version | a literal path segment, three of them | one `?api-version=2022-03-01-preview` query parameter |
| `?api-version` | only `1.0`; anything else is `400` | required, and the segment form does not exist |
| Audience | `https://licensing.powerplatform.microsoft.com` | `https://api.powerplatform.com` — **not interchangeable**, each rejects the other's token with `401` |
| Billing policy record | adds `type`, `payGoEntitlements[]`, `billingInstrument.provisioningStatus` | `BillingPolicyResponseModel` has none of the three |
| Alternate representation | `v0.1-alpha` models pay-as-you-go per product family | one model only |
| Documentation | none at all | [Microsoft Learn](https://learn.microsoft.com/rest/api/power-platform/licensing/billing-policy/get-billing-policy) |
| Writes | routes exist; bodies never observed | documented, and exercised by the Terraform provider |

**Prefer ppapi.** It is documented, coherently versioned, tenant-scoped by token, and it is what the provider actually calls. Reach for this host only for what ppapi does not expose — the `v0.1-alpha` per-product policy representation, `payGoEntitlements`, `billingInstrument.provisioningStatus`, per-user trials — or to read a tenant other than the token's own.

## The versioning is not versioning

Three segments coexist. They are route prefixes, and the evidence is unambiguous:

- Every route on this host, whatever its segment, answers `api-supported-versions: 1.0`.
- `GET /v2.0/tenants/{id}/BillingPolicies?api-version=1.0` returns `200`. The same path with `?api-version=2.0` returns `400`. The segment and the parameter are independent, and `1.0` is the only valid api-version anywhere on the host.
- `Users/{id}/Trials` advertises `api-supported-versions: 1.0, 2`, and rejects `?api-version=2` with `400`. The advertised set is not honoured either.
- An `api-version` request header, `x-ms-api-version`, and `Accept: application/json;v=2.0` are all ignored.
- Route matching is case-insensitive down to the segment: `/V2.0/tenants/{id}/billingpolicies` is the same route.

Which segments a route registers is per-route and arbitrary:

| route | v0.1-alpha | v1.0 | v2.0 |
|---|---|---|---|
| `BillingPolicies`, `BillingPolicies/{id}` | ✅ different model | — | ✅ |
| `BillingPolicies/{id}/Environments[/{envId}]` | ✅ | — | — |
| `Environments/{envId}/BillingPolicy` | ✅ | ✅ | ✅ — all three identical |
| `Entitlements` | ✅ | — | — |
| `Entitlements/{id}` | ✅ different model | — | ✅ |
| `TenantCapacity` | ✅ | — | — |
| `CurrencyReports` | ✅ | ✅ identical | — |
| `allocationsByEnvironment[/{envId}]` | ✅ | — | — |
| `Users/{id}/Trials[/{type}]` | ✅ narrower model | ✅ | — |
| `IsvContracts` | — | ✅ (`403` on a tenant with none) | — |

And where a route serves more than one segment, the representations sometimes differ profoundly:

- **Billing policy.** `v0.1-alpha` models pay-as-you-go as five per-product objects carrying `Enabled`/`Disabled` strings (`powerAutomatePolicy` with three sub-switches, `powerAppsPolicy`, `storagePolicy`, `powerPagesPolicy`, `powerVirtualAgentPolicy`). `v2.0` models the same record as a flat `payGoEntitlements` array of eleven `{entitlementId, productCategory, payAsYouGoState, value}` booleans. Neither contains the other: `v0.1-alpha` collapses the three Dataverse storage meters into one switch and has no representation of `W365APAYGO` at all; `v2.0` lists all eleven meters but loses the grouping.
- **Entitlement.** `v0.1-alpha` returns `capacity.entitled` and `capacity.consumed` as bare numbers; `v2.0` boxes them and adds `allocated`, `availableQuantity` and `status`. The unit vocabulary differs too — the Windows 365 meter is `Hour` under `v0.1-alpha` and `Count` under `v2.0`.
- **Trial.** `v0.1-alpha` returns dates only; `v1.0` adds `trialCurrencyUnits` and `trialCount`, so `v0.1-alpha` cannot answer how much allowance is left.

…and sometimes not at all: `Environments/{envId}/BillingPolicy` returns the **v2.0** representation on all three segments, `v0.1-alpha` included.

Because of all that, each observed `(route, segment)` pair is written out as its own path rather than collapsed behind a server variable that would imply a uniformity the service does not have. Operations carry `x-version-segments` (every segment observed to serve that route) and `x-representation` (which model this path returns).

## Three things that will mislead you

**A 404 does not mean what you think.** An unmatched route answers `404` with an *empty body*; a route that exists whose bound id has no record answers `404` with a JSON problem-details body. The discriminator is the `api-supported-versions` response header: **present if and only if a route matched**. `x-servicefabric: ResourceNotFound` accompanies both and is not a discriminator. `probe.py` has a `route_exists()` predicate for exactly this, and it is what proved `BillingPolicies/{id}/Environments/add` and `/remove` — which ppapi does expose — are *not* routes here: they bind as `{environmentId}` on the GET route instead.

**`GET /` answers 200.** The host mounts a vestigial, empty OData surface at its root: `/` returns a service document with an empty `value` and an `@odata.context` pointing at an internal cluster address on a private IP, and `/$metadata` returns an EDMX with an empty entity container. Neither is part of this API, and both will fool route discovery that treats `200` as evidence. Documented under the *Service Root* tag so nobody rediscovers it.

**Five unrelated error envelopes.** One host, five shapes, and a client must branch on the status code *and* the JSON's top-level type before it can read any of them:

| shape | when |
|---|---|
| `{type, title, status, traceId}` (RFC 9110) | `404` on a route that exists, id has no record |
| `{error: {code, message, details: [{code, message, target}]}}` | `400` when a path segment fails enum binding |
| `[{key, message}]` — a bare **array** | `404` on `Entitlements/{id}` for an unrecognised id |
| `{error: {namespace, code}}` (Service Fabric) | `500` when a route parameter cannot be bound at all |
| *(no body)* | every `401`, `403`, `405`; `400` on `api-version`; `404` on an unmatched route |

`Entitlements/{entitlementId}` returns *two* of these for the same status code depending on the id, which is how the entitlement-id vocabulary split below was found.

## What probing established

Probed 2026-08-27/28 against a live tenant. Four operations came from recorded first-party UI traffic — the admin center calling `/v2.0/…/BillingPolicies`, and the maker portal calling `/v0.1-alpha/…/CurrencyReports`, `/v0.1-alpha/…/allocationsByEnvironment/{env}` and `/v1.0/…/Users/{user}/Trials/AI` directly from the browser. All four still answer identically. Everything else was found by probing outward from them.

- **Fifteen more read operations** than the recordings showed, across five resources the recordings never touched: `TenantCapacity` (a sixteen-meter rollup with layered entitlements and licence attribution), `Entitlements` and `Entitlements/{id}`, `BillingPolicies/{id}` and its `Environments` collection and items, `Environments/{id}/BillingPolicy`, the `allocationsByEnvironment` collection, and `Users/{id}/Trials` as a list.
- **The recorded `allocationsByEnvironment/{env}` call was a 404 in the recording, and has never returned anything else.** The maker portal issues it speculatively and treats the 404 as "nothing allocated". The tenant allocates no currency to any environment, so the collection is `[]` and the item 404s; the success body is undocumented and the operation is marked unverified. Note the two failure modes differ: all thirteen long-lived environments in the tenant answered problem-details `404`, while an id the service cannot resolve answers `403` with an empty body — and that included a *newly provisioned* environment as well as ids from outside the tenant, so `403` here means "not visible to this service, yet or at all" rather than a clean permission verdict.
- **The whole write surface, mapped without writing.** `HEAD` is refused with `405` on every route, and the `Allow` header enumerates what that route does accept: `BillingPolicies` is `GET, POST`; `BillingPolicies/{id}` is `DELETE, GET, PUT`; `allocationsByEnvironment` is `GET, PATCH`; `Users/{id}/Trials` is `GET, POST`; `refreshProvisioningStatus` is `POST` alone; everything else is `GET`. Those match the ppapi operations one for one, which is further evidence the two hosts front the same service. **None was invoked**, no body was ever observed, and none is written up as an operation — `info.x-write-surface` records the map and stops there.
- **`entitlementId` is two vocabularies wearing one name.** A billing policy enumerates eleven of them. Asked of `Entitlements/{id}`, four resolve (`Database`, `File`, `Log`, `W365APAYGO`), five 404 with problem details, and two — `CloudFlowRuns` and `PAAttendedRPA` — 404 with the `[{key, message}]` array, i.e. the entitlement subsystem does not recognise them at all. A client cannot carry ids across the two subsystems.
- **`trialType` is a validated .NET enum with `AI` as its only member.** Fifteen other plausible product names each return `400 InvalidValue` with `target: "trialType"`. The binder is generous — `ai`, `Ai`, `AI ` and the ordinal `1` all resolve and normalise to `AI` — and brittle: ordinal `0` and the literal `None` bind to a value the handler has no case for and produce a `500`.
- **`Double.MaxValue` is a sentinel.** `payGoEntitlements[].value` came back as `1.7976931348623157e308` on every meter of every policy: not a number, but the service's way of saying *no ceiling*.
- **Query parameters are ignored, not rejected** — `$top`, `environmentId`, anything invented — with the single exception of `api-version`, which is validated and is a trap.
- **Both audiences confirmed, and confirmed distinct.** `https://licensing.powerplatform.microsoft.com/.default` is obtainable from the az CLI and mints a token with `aud: https://licensing.powerplatform.microsoft.com` and one legacy scope, `user_impersonation` — there is no granular scope to request, so any token that works here works for the whole surface. A `https://api.powerplatform.com/.default` token is rejected with `401 Bearer error="invalid_token"`, even though that host serves the same resources under `/licensing/`.
- **Status codes actually observed:** `200`, `400` (enum binding; `api-version`), `401`, `403` (foreign or malformed tenant, unknown billing policy id, unresolvable environment id), `404` (both flavours), `405` (every non-GET method), `500` (unbindable route parameter). No `429` was provoked.
- **`403`, not `404`, for an unknown billing policy id** — the one id on this host that does not 404 when it is wrong, which makes a typo indistinguishable from a permission failure on that route alone.

### The sovereign hostnames

The seven names the provider declares, and what each resolves to (2026-08-28, DNS only — no token was ever sent to a sovereign host):

| cloud | hostname | resolves to |
|---|---|---|
| `PUBLIC` | `licensing.powerplatform.microsoft.com` | `nptn-prod-tm.trafficmanager.net` → Azure Front Door |
| `USGOV` | `gov.licensing.powerplatform.microsoft.us` | `nptn-gcc-tm.usgovtrafficmanager.net` |
| `USGOVHIGH` | `high.licensing.powerplatform.microsoft.us` | `nptn-usg-tm.usgovtrafficmanager.net` |
| `USDOD` | `licensing.appsplatform.us` | `nptn-dod-tm.usgovtrafficmanager.net` |
| `CHINA` | `licensing.partner.microsoftonline.cn` | `nptn-chn-tm.trafficmanager.cn` → `neptune.<cluster>.gateway.mooncake.cm.powerapps.cn` |
| `EX` | `licensing.eaglex.ic.gov` | not publicly resolvable — expected for an air-gapped cloud |
| `RX` | `licensing.microsoft.scloud` | not publicly resolvable |

**The naming is not uniform**, which is why these are worth recording rather than deriving. The two US Government clouds keep the commercial domain and prefix the geo (`gov.`, `high.`); DoD, China and both air-gapped clouds replace the domain outright. No string transform gets you from one to another.

Every resolvable host fronts a Traffic Manager profile named `nptn-<cloud>-tm`, and the China chain spells it out: the service's internal codename is **Neptune**. That is the only self-identification this host offers.

## Conventions

- 20 paths, 20 operations, 36 schemas, OpenAPI 3.0.3. Nineteen operations are `GET`; the twentieth is a `POST` that was never issued.
- Tagged by logical resource: Billing Policy, Billing Policy to Environment link, Entitlement, Tenant Capacity, Currency Allocation, User Trial, Service Root.
- **No `api-version` parameter anywhere.** The version is a path segment, and the query parameter is documented as a `400`.
- Path-level `x-allowed-methods` carries the observed `Allow` header; operation-level `x-version-segments` and `x-representation` carry the versioning facts; `info.x-versioning`, `info.x-error-envelopes`, `info.x-route-existence-oracle`, `info.x-write-surface`, `info.x-sovereign-hosts` and `info.x-relationship-to-power-platform-api` carry the rest.
- **Nothing is marked `required`.** Every documented field was present on every object observed, but the service's own optionality was never proven — no request was ever made that the service could reject for a missing field.
- `x-probe-verified: true` marks the eighteen operations that returned a real `200` with a JSON body, and the schemas built from those bodies. It is `false` on `refreshProvisioningStatus` (route located by `405`/`Allow`, never invoked) and on `allocationsByEnvironment/{environmentId}` (never observed to succeed).
- Enums carry only what was proven. Where a set is plainly larger than what was seen — `billingPolicy.type`, `provisioningStatus`, `licenseTier`, `currencyType` — the observed values sit in `x-observed-values` rather than in a false `enum`. Where a set was fully enumerated by the service itself in one response (`capacityType`, `capacitySubType`, `payGoEntitlements[].entitlementId`, `productCategory`) it is an `enum` with an `x-enum-evidence` note saying so.
- Two fields are documented as *not* meaning what they say: `TenantCapacityMeter.maxCapacity` was `0` on every meter including entitled ones, and `CapacityLicense.displayName` was empty on every licence.
- `allocationsByEnvironment` items and `TenantCapacityMeter.overflowCapacity` items are typed as bare objects, because neither was ever non-empty and guessing from the ppapi models would be an invention.

## Status

Written from recorded first-party traffic and live probing of one tenant in the `australia` geography (2026-08); validates against `openapi-spec-validator`; rendered by the browser at the repo root. **Nothing was created, modified or deleted** — the harness cannot issue a write, and the write routes it found were left alone. The item schema for environment currency allocations awaits a tenant that allocates one, and the sovereign hosts await a caller in those clouds.
