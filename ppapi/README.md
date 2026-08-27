# ppapi

An unofficial markdown mirror of the [Microsoft Power Platform API reference](https://learn.microsoft.com/en-us/rest/api/power-platform/) (`api.powerplatform.com`), plus a reverse-engineered OpenAPI spec, refreshed daily by the `ppapi-mirror` workflow. Diffing a mirror commit shows exactly what Microsoft changed that day.

This is the `ppapi` folder of the [powerplatform-apis](..) monorepo; the spec browser at the repo root renders `oas/openapi.json`.

## Layout

- `docs/` is the mirror itself, laid out to match the site: `{namespace}/{group}.md` for each operation group overview and `{namespace}/{group}/{operation}.md` for each operation, plus `index.md` and `whats-new-changed.md`. Links between pages are rewritten to work locally; links out of the corpus point back at learn.microsoft.com.
- `catalogue/` is a machine-readable index of every operation (JSON and CSV): namespace, group, operation, method, path, api-version, preview flag, introduction date where the changelog announced it, and a logical-resource grouping that maps Microsoft's namespaces onto the resources they actually manage.
- `oas/openapi.json` is a single OpenAPI 3.0.3 spec reverse-engineered from the docs. One spec, not one per namespace: the namespaces are transport and org-chart artifacts, and the resources people actually manage span them. Tags group operations by logical resource (the same taxonomy as the catalogue) and each operation carries `x-ms-namespace` recording where Microsoft filed it. The Learn pages are generated from an internal OpenAPI, so the tables invert cleanly, but this spec is unofficial and not verified against the service. Treat it as a map, not a contract.
- `enrichment.json` is the hand-maintained layer over the generated spec: per operation (keyed `namespace/group/slug`) a clean `summary`, and optionally `tags` and `description` overrides; a `tags` section can override tag descriptions; a `schemas` section renames generically-named models (the docs auto-name the OData envelope item type `Value`, for instance). Where the live API differs from the docs, per-operation `notes` record the discrepancy, per-operation `responses` add or correct response bodies, headers and status codes, and an `addSchemas` section defines the real shapes (verified against a live tenant) that the docs omit or model wrongly. `oas.py` applies it at generate time and warns about keys that no longer match an operation, so docs renames surface in the daily run. New operations that have no entry get a mechanical cleanup of Microsoft's title.
- `scripts/` regenerates everything: `fetch.py` (stdlib only), then `catalogue.py`, then `oas.py`.

## How the mirror works

learn.microsoft.com serves the clean markdown source of any page when asked with an `Accept: text/markdown` header. `fetch.py` discovers every Power Platform page from the site TOC, fetches each as markdown, strips volatile build metadata (so commits only happen on real content changes), and replaces `docs/` atomically only when every page fetched successfully.

The `ppapi-mirror` workflow (`.github/workflows/ppapi-mirror.yml`, run from this folder) fetches daily and commits whatever changed. The commit history is the change log: diff any commit to see exactly what Microsoft changed that day.

## Attribution and licence

The content under `docs/` is Microsoft's documentation, mirrored from learn.microsoft.com and owned by Microsoft. Microsoft documentation is generally published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); this mirror exists for change tracking and offline reference, with attribution to Microsoft Learn as the source. The scripts in this repository are MIT licensed. If Microsoft objects to this mirror it will be taken down.
