# bapi

The Business Application Platform API (`api.bap.microsoft.com`, the legacy Power Platform admin API): environment provisioning and lifecycle, managed environments, enterprise policies, DLP, tenant settings, and the rest of the admin surface that predates [ppapi](../ppapi).

## Why this one is different

`ppapi` is reverse-engineered from Microsoft's own OpenAPI-generated Learn documentation, so its docs invert mechanically into a spec. **BAPI has no such published reference.** Its shape has to be recovered from a real, working client instead.

The source of truth here is the Terraform provider [`microsoft/terraform-provider-power-platform`](https://github.com/microsoft/terraform-provider-power-platform), which calls BAPI extensively. The provider's Go code encodes, for each operation:

- the HTTP method and path (`internal/api/*.go`, `internal/services/*/api_*.go`),
- the request and response bodies as typed DTOs (`internal/services/*/dto.go`, with `json:` tags),
- the expected status codes, the lifecycle-operation polling shape, and error handling.

That is enough to reconstruct an OpenAPI spec.

## Target layout (match ppapi)

```
bapi/
  scripts/        extract endpoints + DTOs from the provider source, emit oas/openapi.json
  oas/openapi.json
  enrichment.json optional: clean operation names, notes, live-verified shapes
  README.md
```

The generated spec should be the same shape as `ppapi/oas/openapi.json` so the browser at the repo root can render it: add an entry to the root `specs.json` once a spec exists.

## Status

Scaffold only. No extraction written yet.
