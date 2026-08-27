# bapi

The Business Application Platform API (`api.bap.microsoft.com`, the legacy Power Platform admin API): environment provisioning and lifecycle, managed environments, enterprise policies, DLP, tenant settings, and the rest of the admin surface that predates [ppapi](../ppapi).

## Why this one is different

`ppapi` is reverse-engineered from Microsoft's own OpenAPI-generated Learn documentation, so its docs invert mechanically into a spec and hand edits ride in an `enrichment.json` that survives regeneration. **BAPI has no such published reference.** Its shape was recovered from a real, working client — and because there is no upstream to re-fetch, [`oas/openapi.json`](oas/openapi.json) is **owned directly**: names, descriptions, tags and schema polish are edited in place. There is no enrichment file.

The source of truth is the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform). Since its client-library refactor, every BAPI call lives in one package (`internal/clients/bapi`) behind one uniform harness, which encodes per operation: the method and path, the request/response DTOs (`json:` tags), the accepted status codes, and the 202 + `Location` lifecycle-operation pattern. The provider itself derives from admin-center traffic recordings.

## Layout

```
bapi/
  scripts/extract.py   parse the provider's bapi client -> operation/DTO inventory
  oas/openapi.json     the spec (hand-owned; seeded once from the inventory)
  README.md
```

`extract.py` seeded the spec and now serves as a **drift audit**:

```
scripts/extract.py <provider-checkout>            # print the extracted inventory
scripts/extract.py <provider-checkout> --check    # diff provider vs oas/openapi.json
```

`--check` fails when the provider gains BAPI operations the spec lacks, or the spec claims provider-sourced operations the provider no longer performs. Operations documented from live behavior without a provider call site (the lifecycle-operation poll) carry `x-provider-unsourced: true` and are excluded from the audit.

## Conventions

- 38 operations over 28 paths, tagged by logical resource (Environments, DLP Policies, Tenant, …), OpenAPI 3.0.3.
- `api-version` defaults are per operation (2019-10-01 → 2023-06-01); the `PowerPlatform.Governance` paths take no api-version at all.
- Nothing is marked `required` and only fields the provider consumes are listed — the service's own optionality is unverified. Property descriptions exist only where they say something a name doesn't.
- Async mutations respond 202 with a `Location` URL rendering `LifecycleOperation`; terminal states are `Succeeded`/`Failed`.

## Status

Spec generated and in sync with the provider client (`--check` clean); rendered by the browser at the repo root.
