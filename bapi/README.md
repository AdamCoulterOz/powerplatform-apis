# bapi

The Business Application Platform API (`api.bap.microsoft.com`, the legacy Power Platform admin API): environment provisioning and lifecycle, managed environments, enterprise policies, DLP, tenant settings, and the rest of the admin surface that predates [ppapi](../ppapi).

## Why this one is different

`ppapi` is reverse-engineered from Microsoft's own OpenAPI-generated Learn documentation, so its docs invert mechanically into a spec and hand edits ride in an `enrichment.json` that survives regeneration. **BAPI has no such published reference.** Its shape was recovered from a real, working client — and because there is no upstream to re-fetch, [`oas/openapi.json`](oas/openapi.json) is **owned directly**: names, descriptions, tags and schema polish are edited in place. There is no enrichment file.

The source of truth is the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform). Since its client-library refactor, every BAPI call lives in one package (`internal/clients/bapi`) behind one uniform harness, which encodes per operation: the method and path, the request/response DTOs (`json:` tags), the accepted status codes, and the 202 + `Location` lifecycle-operation pattern. The provider itself derives from admin-center traffic recordings.

## Layout

```
bapi/
  scripts/extract.py   parse the provider's bapi client -> operation/DTO inventory
  scripts/probe.py     call the live service -> real shapes, optionality, enums
  oas/openapi.json     the spec (hand-owned; seeded from the inventory, corrected by probing)
  README.md
```

`extract.py` seeded the spec and now serves as a **drift audit**:

```
scripts/extract.py <provider-checkout>            # print the extracted inventory
scripts/extract.py <provider-checkout> --check    # diff provider vs oas/openapi.json
```

`--check` fails when the provider gains BAPI operations the spec lacks, or the spec claims provider-sourced operations the provider no longer performs. Operations documented from live behavior without a provider call site (the lifecycle-operation poll, the admin-applications list) carry `x-provider-unsourced: true` and are excluded from the audit.

## Probing

`probe.py` is the other half. A client only models what it needs, so the seeded spec listed a fraction of each response, marked nothing `required`, and guessed at optionality. The harness calls the real service to settle those questions:

```
scripts/probe.py read --tenant-file facts.json    # GET every read surface, print shapes
scripts/probe.py errors                            # provoke 4xx, capture the error envelope
scripts/probe.py lifecycle --location <loc> --billing-policy <id>
scripts/probe.py dlp --environment <id>
scripts/probe.py cleanup                           # sweep anything a crashed run left behind
```

It authenticates through the logged-in `az` CLI. No tenant id is hardcoded: ids come from arguments or a facts file. `read` and `errors` are non-destructive. `lifecycle` and `dlp` create resources, name every one of them with `--prefix`, and tear them down in a `finally` block; `cleanup` re-runs the sweep and reports what remains. Raw captures land in a git-ignored directory because they are full of tenant data — stdout carries only shapes, and the spec quotes neutral placeholders.

## Conventions

- 39 operations over 29 paths, tagged by logical resource (Environments, DLP Policies, Tenant, …), OpenAPI 3.0.3.
- `api-version` defaults are per operation (2019-10-01 → 2023-06-01); the `PowerPlatform.Governance` paths take no api-version at all. The version is not always cosmetic: `locations/{location}/templates` returns a *different response shape* either side of 2021-04-01, and the environment PATCH is pinned to 2021-04-01 because newer versions turn Managed Environments on as a side effect.
- Contracts live in the schema, not the prose: `enum` for every closed set observed, `format`/`pattern` for real constraints, `example` for id and hostname shapes, `default` on api-version.
- `required` appears only where a request was actually rejected without the field. On responses it means nothing: BAPI omits members rather than nulling them, and which members appear varies with SKU, Dataverse linkage and `$expand`.
- `x-probe-verified: true` marks what was confirmed live. Its absence means provider-derived only.
- Async mutations respond 202 with an absolute poll URL in `Location` (or, for `modifySku`, `Operation-Location`) rendering a `LifecycleOperation`; states run `NotStarted` → `Running` → `Succeeded`/`Failed`.

## Status

In sync with the provider client (`--check` clean) and **probed against a live tenant**: 26 of 39 operations and 100 of 125 schemas carry `x-probe-verified: true`.

Probing corrected the provider-only view in ways worth knowing about. A synchronous create returns the entire environment, not the reduced shape the client parses. Environment reads carry roughly twice the properties the client models — `lifecycleOperationsEnforcement` lists exactly which operations the environment will currently accept and why the rest are blocked, and `ongoingOperation` names the operation behind a 409. `properties.databaseType` turns out to be the switch that makes `linkedEnvironmentMetadata` meaningful; omit it and Dataverse is silently skipped. Delete answers a 409 with an empty body, and 204 rather than 404 once the environment is gone. The whole `Environment Role Assignments` tag is refused outright on Dataverse-linked environments. Every failure shares one error envelope, and its `message` is frequently the only place the service enumerates a closed value set.

What was not probed: the tenant-wide write surfaces (tenant settings, tenant isolation, admin application registration, enterprise policies) were deliberately left read-only, so their write semantics stay unverified; and sovereign clouds were not touched at all.
