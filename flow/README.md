# flow

The Power Automate service API (`api.flow.microsoft.com`), which addresses flows under the `Microsoft.ProcessSimple` resource provider — the internal name Power Automate still carries on the wire, and the reason searching Microsoft's documentation for "Power Automate REST API" finds so little.

## Why this one is the weakest spec here

**Nothing in it has been observed on the wire.** Every route was read from the call sites of working third-party clients — `pnp/cli-microsoft365`, `d365collaborative/d365bap.tools` and the Power Platform admin centre's own bundles — and cross-checked between them. That establishes what exists and is called. It establishes nothing about what comes back.

So, deliberately:

- no operation carries `x-probe-verified`
- no response body is modelled, rather than guessed at from a client's parser
- the `api-version` is what shipped clients send, not one the service was seen to accept
- everything carries `x-source: provider`

It is a map of the surface, not a contract. That is worth having because the alternative was silence: every other Power Platform boundary in this corpus had a spec and this one did not, so a reader comparing a working client against the corpus would have concluded Power Automate had no API rather than that nobody had documented it.

## Shape

It is a sibling of [powerapps](../powerapps) rather than part of [ppapi](../ppapi): the same `/providers/{resourceProvider}/environments/{environmentId}/...` convention, the same `scopes/admin` elevation for tenant-wide reach, and its own host. Anyone who has read the Power Apps spec will recognise the layout immediately.

Two details worth knowing before you build against it:

- **The admin flow list is not the user route with a prefix.** It inserts `scopes/admin` *and* a `/v2/` path segment: `scopes/admin/environments/{env}/v2/flows`. Every other admin form in this family is a straight prefix, so this one will catch you out.
- **Restore exists only on the admin scope.** An owner cannot undo their own delete; an administrator must. That asymmetry is a real operational constraint rather than an oversight in the client.

## Relationship to the rest of the corpus

The Power Platform API is absorbing this surface, as it is absorbing BAPI's — see the PPEM note in [ppapi](../ppapi). Flows already appear under PPAPI's `powerautomate` namespace, and the admin centre carries a rewrite table mapping legacy resource-provider paths onto their PPAPI successors. Expect this spec to describe the older of two live surfaces for some time.

## What would improve it most

One capture. A single authenticated session against a tenant with flows in it would settle response shapes, real status codes, the paging behaviour on `runs`, and whether the regional host prefixes some clients use are real. Until then this spec can tell you where to knock and not what answers.
