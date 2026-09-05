# flow

The Power Automate service API (`api.flow.microsoft.com`), which addresses flows under the `Microsoft.ProcessSimple` resource provider — the internal name Power Automate still carries on the wire, and the reason searching Microsoft's documentation for "Power Automate REST API" finds so little.

## Why this one is the weakest spec here

**Nothing in it has been observed on the wire.** Every route was read from the call sites of shipped clients — Microsoft's own `Microsoft.PowerApps.Administration.PowerShell` module, the Power Platform admin centre's JavaScript bundles, and third-party clients including `pnp/cli-microsoft365` and `d365collaborative/d365bap.tools` — and cross-checked between them. That establishes what exists and is called. It establishes nothing about what comes back.

So, deliberately:

- no operation carries `x-probe-verified`
- the response shapes here are what a client *expects*: read from its own test fixtures and from the fields its code reaches for, never from a reply anyone here has seen
- each `api-version` is the one a shipped client sends, not one the service was seen to accept — and in the PowerShell-derived routes it is a cmdlet default the caller can override, which makes it weaker still
- every operation is graded by the strongest client that witnesses it, and `x-corroborated-by` lists the weaker ones that witness the same route independently

Two clients agreeing is the only kind of confirmation available here, and it is agreement about the *request*. Treat the spec as a map of what exists and is called, not as a contract.

## Shape

It is a sibling of [powerapps](../powerapps) rather than part of [ppapi](../ppapi): the same `/providers/{resourceProvider}/environments/{environmentId}/...` convention, the same `scopes/admin` elevation for tenant-wide reach, and its own host. Anyone who has read the Power Apps spec will recognise the layout immediately.

Details worth knowing before you build against it:

- **`scopes/admin/` is an optional path segment, so several operations appear twice.** In `cli-microsoft365` it is a `--asAdmin` switch that concatenates either `scopes/admin/` or an empty string. OpenAPI cannot describe an optional segment, so each concrete route is written out — `flows_get` and `flows_getAdmin`, `flows_start` and `flows_startAdmin`, and so on.
- **The axis is not uniform.** `restore` and `modifyowners` exist *only* on the admin scope; the admin flow list inserts `scopes/admin` **and** a `/v2/` path segment; and the same PowerShell module grants owners on the admin scope while revoking them on the user scope. Do not assume a route has an admin twin because its neighbour does.
- **One route is under a different resource provider.** `migrateFlows` is `Microsoft.Flow`, not `Microsoft.ProcessSimple`, on the same host. A client that templates the provider segment once will send it to the wrong place.
- **The api-version is not one value.** Most routes are called on `2016-11-01`, `owners` on `2017-06-01`, and the admin centre pins `2016-11-01-beta` on the environment operations list and on one flow-list call.
- **Two routes hang off no environment at all**: `POST /batch`, which carries its own sub-requests and no `api-version`, and the tenant-wide `getPowerPlatformRequestReport`, which returns a pre-signed download URL rather than the report and is then fetched with no `Authorization` header.
- **`~default` is a value, not a route.** It is a literal alias for the tenant default environment, documented here as a value of `environmentName`.

## Relationship to the rest of the corpus

The Power Platform API is absorbing this surface, as it is absorbing BAPI's — see the PPEM note in [ppapi](../ppapi). Flows already appear under PPAPI's `powerautomate` namespace, and the admin centre carries a rewrite table mapping legacy resource-provider paths onto their PPAPI successors. Expect this spec to describe the older of two live surfaces for some time.

## What would improve it most

One capture. A single authenticated session against a tenant with flows in it would settle response shapes, real status codes, the paging behaviour on `runs`, whether the regional host prefixes some clients use are real, and whether the two oddities the clients themselves carry — the stray apostrophe the PowerShell module appends to the `owners` URL, and the capital-P `/Providers/` the admin centre sends on one admin delete — are tolerated or were always broken. Until then this spec can tell you where to knock and not what answers.
