# ppapi

An unofficial markdown mirror of the [Microsoft Power Platform API reference](https://learn.microsoft.com/en-us/rest/api/power-platform/) (`api.powerplatform.com`), plus a reverse-engineered OpenAPI spec, refreshed daily by the `ppapi-mirror` workflow. Diffing a mirror commit shows exactly what Microsoft changed that day.

This is the `ppapi` folder of the [powerplatform-apis](..) monorepo; the spec browser at the repo root renders `oas/openapi.json`.

## Layout

- `docs/` is the mirror itself, laid out to match the site: `{namespace}/{group}.md` for each operation group overview and `{namespace}/{group}/{operation}.md` for each operation, plus `index.md` and `whats-new-changed.md`. Links between pages are rewritten to work locally; links out of the corpus point back at learn.microsoft.com.
- `catalogue/` is a machine-readable index of every documented operation (JSON and CSV): namespace, group, operation, method, path, api-version, preview flag, introduction date where the changelog announced it, and a logical-resource grouping that maps Microsoft's namespaces onto the resources they actually manage. It indexes the mirror, so the 25 operations that exist only in the spec are absent from it by design.
- `oas/openapi.json` is a single OpenAPI 3.0.3 spec: 234 operations over 199 paths and 381 schemas, reverse-engineered from the docs and then corrected and extended against recorded traffic (see [Verification](#verification)). One spec, not one per namespace: the namespaces are transport and org-chart artifacts, and the resources people actually manage span them. Tags group operations by logical resource (the same taxonomy as the catalogue, plus seven resources the docs never describe) and each operation carries `x-ms-namespace` recording where Microsoft filed it. The Learn pages are generated from an internal OpenAPI, so the tables invert cleanly. Treat the unverified majority as a map, not a contract.
- `enrichment.json` is the hand-maintained layer over the generated spec, and the only place to edit: `oas.py` rebuilds `oas/openapi.json` from `docs/` on every run, so a change made in the spec itself is lost on the next mirror commit. Its sections:
  - `info` overrides the spec description; `servers` declares the host forms (see [Hosts](#hosts)); `securityScheme` merges into the OAuth2 scheme.
  - `operations`, keyed `namespace/group/slug`, curates a docs-derived operation: a clean `summary`, optional `tags`, `description` and `x-probe-verified`; `parameters` patches a parameter by name (deep-merging into its `schema`, so a wrong default or a missing enum is corrected without restating the type) or appends one the docs never listed; `responses` adds or corrects response bodies, headers and status codes; `requestBody` supplies one the docs omit; and `notes` records a verified doc-vs-reality discrepancy, which renders as a single blockquote callout on the operation and as `x-notes`.
  - `addOperations`, keyed `METHOD /path`, contributes a whole operation the docs do not describe at all. The value is an OAS operation object; `{"$ref": "Name"}` is shorthand for a component schema, `notes` behaves as above, and `servers` names which host serves it (the prose is stripped on the way out, since it already sits in the top-level `servers` list).
  - `schemas` curates an existing model: `rename` (the docs auto-name the OData envelope item type `Value`), `description`, `notes`, `x-probe-verified`, `renameProperties` for names the docs spell wrongly, and `properties` to add or replace individual properties (`null` deletes one).
  - `addSchemas` defines shapes the docs omit or model wrongly.

  `oas.py` applies all of it at generate time and warns about keys that no longer match, so docs renames surface in the daily run. New operations that have no entry get a mechanical cleanup of Microsoft's title.
- `scripts/` regenerates everything: `fetch.py` (stdlib only), then `catalogue.py`, then `oas.py`.

## Hosts

The API answers on three host forms, and which one an operation is served from is part of its contract. All three are in `servers`, and every operation added from recorded traffic names the one it was observed on.

- `https://api.powerplatform.com` — the global endpoint. Everything the docs describe is reachable here; the gateway routes to the tenant's own cluster.
- `https://{head}.{tail}.tenant.api.powerplatform.com` — tenant-scoped.
- `https://{head}.{tail}.environment.api.powerplatform.com` — environment-scoped.

The tenant and environment hosts are derived from an id alone; there is no region or scale unit in them. Remove the hyphens from the tenant or environment id to get 32 hex characters, then split: the first 30 are the first DNS label, the last 2 are the second. Environment `00000000-0000-0000-0000-0000000000ab` is therefore `https://000000000000000000000000000000.ab.environment.api.powerplatform.com`. Because the host already identifies the scope, these paths carry no id segment — `/connectivity/connections` on the environment host is the same resource as `/connectivity/environments/{environmentId}/connections` on the global host, and `/powerapps/environment` is singular with no id at all.

`POST /powerapps/apps/{appName}/locate` on the global host is the bootstrap: given only an app id it returns the tenant, environment and geography needed to build the right host for everything after. `GET /gateway/cluster` confirms which stamp a host resolved to.

## Verification

The spec started life docs-derived and unverified. A subset has since been checked against recorded first-party traffic — HAR captures of the Power Platform admin centre and the Power Apps maker portal driving this API on a real tenant — which is stronger evidence than probing: it shows the request and response bodies the real client sends and receives, including endpoints, parameters and fields no external caller would guess.

- **34 of 234 operations** and **30 of 381 schemas** carry `x-probe-verified: true`. Its absence means docs-derived only, and that is still the majority of the file.
- **25 of those 34 operations do not appear in the docs at all** and exist only here, across seven resources Microsoft does not document: user settings, feature gates, notifications, service plans, gateway clusters, Copilot governance settings and governance configurations — plus undocumented operations on documented resources (app DLP pre-evaluation, app co-authoring sessions, app location, effective rule-based policies, rule set UI configurations).
- **27 operations carry `x-notes`**, each a specific place the docs and the service disagree. The biggest: the docs claim `api-version=2024-10-01` everywhere, and the wire uses `1`, `2021-10-01-preview`, `2022-03-01-preview` or `3` depending on the namespace; and every property of `EnvironmentManagementSetting` is PascalCase on the wire (`PowerApps_AllowCodeApps`) while the docs lowercase the leading letter, which matters because `$select` matches case-sensitively.

The tokens the recorded clients presented also settle authentication: the audience is `https://api.powerplatform.com` on all three hosts, and the 87 granular delegated permissions seen in real tokens are listed under `x-delegated-scopes` on the security scheme. Which scope each operation requires is *not* recorded there — a token shows what was granted, not what was needed.

Nothing was inferred: a recorded request/response is the bar for an addition, and where only an empty collection or a 204 was observed the schema says so rather than inventing an item shape.



## How the mirror works

learn.microsoft.com serves the clean markdown source of any page when asked with an `Accept: text/markdown` header. `fetch.py` discovers every Power Platform page from the site TOC, fetches each as markdown, strips volatile build metadata (so commits only happen on real content changes), and replaces `docs/` atomically only when every page fetched successfully.

The `ppapi-mirror` workflow (`.github/workflows/ppapi-mirror.yml`, run from this folder) fetches daily and commits whatever changed. The commit history is the change log: diff any commit to see exactly what Microsoft changed that day.

## Attribution and licence

The content under `docs/` is Microsoft's documentation, mirrored from learn.microsoft.com and owned by Microsoft. Microsoft documentation is generally published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); this mirror exists for change tracking and offline reference, with attribution to Microsoft Learn as the source. The scripts in this repository are MIT licensed. If Microsoft objects to this mirror it will be taken down.
