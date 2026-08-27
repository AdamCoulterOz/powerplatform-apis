# dataverse

The Dataverse Web API (`{organization}.crm{n}.dynamics.com/api/data/v9.2`), the per-environment OData v4 endpoint through which every table in an environment is addressable — and, for an infrastructure client, the place solutions are imported, environment variables are set, application users are created and environment settings are changed.

## Why this one is a *subset*

Unlike [bapi](../bapi) and [ppapi](../ppapi), Dataverse **has** an official contract: each environment publishes its own CSDL at `GET /api/data/v9.2/$metadata`, and Microsoft Learn documents the surface in prose. That contract is also per environment, includes every custom table anyone ever made, and runs to megabytes. Reproducing it here would be neither possible nor useful.

So [`oas/openapi.json`](oas/openapi.json) is deliberately **a curated admin/ALM subset** — the operation surface an infrastructure client actually uses:

| Tag | What it covers |
|---|---|
| Identity | `WhoAmI` |
| Table Definitions | `EntityDefinitions`, columns, relationship metadata |
| Records | generic CRUD and OData query against any table |
| Relationships | `@odata.bind`, the `$ref` collection, associate/disassociate |
| Solutions | the installed inventory, and deleting one |
| Solution Import | `StageSolution`, `ImportSolutionAsync`, `StageAndUpgradeAsync`, `asyncoperations`, `RetrieveSolutionImportResult`, `PublishAllXml` |
| Environment Variables | definitions and their per-environment values |
| Publishers | publishers and their customization prefix |
| Users and Roles | system and application users, security roles, business units |
| Organization Settings | the `organizations` row, `RetrieveSettingList()`, `SaveSettingValue()` |

**For anything outside that, go to the environment's own `$metadata`.** It is authoritative, machine-readable, and always current for that environment; this spec never can be.

## How it was derived

The inventory came from the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform), whose client-library refactor put every Dataverse call in one package (`internal/clients/dataverse`) encoding per operation the method, path, api-version, request/response DTOs and accepted status codes.

The **behaviour** came from probing a live tenant. That is where the value is: the provider models only the fields it consumes, and its accepted-status lists are a superset of what the service actually does. Live probing produced the annotation and envelope conventions, real option-set values read out of the metadata endpoint, the 5000-row count ceiling, api-version routing, and thirteen distinct Dataverse error codes with the conditions that produce them.

Operations confirmed against the live service carry `x-probe-verified: true` — 42 of 48. The five that do not are `ImportSolutionAsync` and `StageAndUpgradeAsync` (only their rejection paths were exercised; no solution was actually imported), `PublishAllXml`, and application-user create/update/delete, which needs a service principal to register.

## Layout

```
dataverse/
  scripts/probe.py     the live probe harness
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

`probe.py` is generic — the host comes from `argv` or `DATAVERSE_HOST`, tokens from the logged-in `az` session — and prints shapes, not tenant data:

```
scripts/probe.py read  <host>     # envelope, paging, collections, error shapes
scripts/probe.py enums <host>     # the option sets the spec pins, read from metadata
scripts/probe.py write <host>     # create/update/associate/delete, cleaned up in `finally`
```

Point `write` only at a throwaway environment. Everything it creates is prefixed and removed, and it verifies the removal before exiting.

## What probing changed

The corrections worth knowing, because a provider-only reading of this API gets them wrong:

- **`@odata.bind` takes the navigation property, not the lookup column.** They are frequently spelled differently — `environmentvariablevalue`'s column is `environmentvariabledefinitionid`, its navigation property is `EnvironmentVariableDefinitionId` — and binding to the column name is refused outright as an undeclared property. Read `ReferencingEntityNavigationPropertyName` from relationship metadata.
- **Counts saturate at 5000.** Both `@odata.count` and `@Microsoft.Dynamics.CRM.totalrecordcount` cap there; `totalrecordcountlimitexceeded` is the only way to tell a table of exactly 5000 rows from one of half a million.
- **Metadata endpoints are not entity sets.** `EntityDefinitions` and its children accept `$top` and ignore it, and never page.
- **PATCH upserts.** Without `If-Match: *`, a PATCH at a wrong id silently creates a record.
- **Read-only columns on `organizations` are accepted and discarded**, not refused — patching `name` returns success and changes nothing.
- **`StageSolution` reports failure inside a success response**, with an all-zeros upload id and a fully-null `SolutionDetails`. Its real response also carries far more than the provider models: the *installed* solution's name, version, publisher and pending-upgrade state alongside the package's, which is what makes an install-versus-upgrade decision possible before importing.
- **A bad role id is `0x80040217`**, a missing `role` record — not the generic unresolvable-reference code a client might special-case.
- **`SaveSettingValue()` refuses with 400**, not 500: `0x81000067` for an unknown setting name, `0x81000068` for a value that will not convert.
- **401 has an empty body.** The reason is in `WWW-Authenticate` (which also advertises the exact audience to request) and a non-standard `401_error_reason` header. A request with no api-version segment answers `{"Message": ...}` from below the OData layer, escaping the error envelope entirely. And some transport-level failures return the envelope with `code` set to the empty string.

## Status

Spec validates as OpenAPI 3.0.3; 48 operations over 31 paths, 58 schemas. Rendered by the browser at the repo root.
