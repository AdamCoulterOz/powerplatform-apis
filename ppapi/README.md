# ppapi

An unofficial markdown mirror of the [Microsoft Power Platform API reference](https://learn.microsoft.com/en-us/rest/api/power-platform/) (`api.powerplatform.com`), plus a reverse-engineered OpenAPI spec, refreshed daily by the `ppapi-mirror` workflow. Diffing a mirror commit shows exactly what Microsoft changed that day.

This is the `ppapi` folder of the [powerplatform-apis](..) monorepo; the spec browser at the repo root renders `oas/openapi.json`.

## Layout

- `docs/` is the mirror itself, laid out to match the site: `{namespace}/{group}.md` for each operation group overview and `{namespace}/{group}/{operation}.md` for each operation, plus `index.md` and `whats-new-changed.md`. Links between pages are rewritten to work locally; links out of the corpus point back at learn.microsoft.com.
- `catalogue/` is a machine-readable index of every documented operation (JSON and CSV): namespace, group, operation, method, path, api-version, preview flag, introduction date where the changelog announced it, and a logical-resource grouping that maps Microsoft's namespaces onto the resources they actually manage. It indexes the mirror, so the 25 operations that exist only in the spec are absent from it by design.
- `oas/openapi.json` is a single OpenAPI 3.0.3 spec: 240 operations over 205 paths and 434 schemas, reverse-engineered from the docs and then corrected and extended against two further sources (see [Sources and how they are graded](#sources-and-how-they-are-graded)). One spec, not one per namespace: the namespaces are transport and org-chart artifacts, and the resources people actually manage span them. Tags group operations by logical resource (the same taxonomy as the catalogue, plus seven resources the docs never describe) and each operation carries `x-ms-namespace` recording where Microsoft filed it. The Learn pages are generated from an internal OpenAPI, so the tables invert cleanly. Treat the unverified majority as a map, not a contract.
- `enrichment.json` is the hand-maintained layer over the generated spec, and the only place to edit: `oas.py` rebuilds `oas/openapi.json` from `docs/` on every run, so a change made in the spec itself is lost on the next mirror commit. Its sections:
  - `info` overrides the spec description; `servers` declares the host forms (see [Hosts](#hosts)); `securityScheme` merges into the OAuth2 scheme.
  - `operations`, keyed `namespace/group/slug`, curates a docs-derived operation: a clean `summary`, optional `tags`, `description` and `x-probe-verified`; `parameters` patches a parameter by name (deep-merging into its `schema`, so a wrong default or a missing enum is corrected without restating the type) or appends one the docs never listed; `responses` adds or corrects response bodies, headers and status codes; `requestBody` supplies one the docs omit; and `notes` records a doc-vs-reality discrepancy, which comes out as `x-notes` (see [Notes](#notes)). A note is a plain string, graded by the entry's own `x-source`, or `{"note": ..., "source": ...}` when it is graded differently — a live-verified operation can still carry a finding only the CLI attests to.
  - `addOperations`, keyed `METHOD /path`, contributes a whole operation the docs do not describe at all. The value is an OAS operation object; `{"$ref": "Name"}` is shorthand for a component schema, `notes` behaves as above, and `servers` names which host serves it (the prose is stripped on the way out, since it already sits in the top-level `servers` list).
  - `schemas` curates an existing model: `rename` (the docs auto-name the OData envelope item type `Value`), `description`, `notes`, `enum`, `required`, `x-probe-verified`, `x-source`, `renameProperties` for names the docs spell wrongly, and `properties` to add or replace individual properties (`null` deletes one).
  - `addSchemas` defines shapes the docs omit or model wrongly, including the two the docs left as `x-stub` placeholders that are really discriminated unions.
  - `x-source` on any of the above records where non-docs content came from. `pac-cli` means the Power Platform CLI's own client and nothing stronger; it is what keeps client-derived findings out of the "verified against the live API" group.

  `oas.py` applies all of it at generate time and warns about keys that no longer match, so docs renames surface in the daily run. New operations that have no entry get a mechanical cleanup of Microsoft's title.
- `scripts/` regenerates everything: `fetch.py` (stdlib only), then `catalogue.py`, then `oas.py`. `pac_extract.py` is separate: it mines the Power Platform CLI's own client and diffs it against the spec, and never writes the spec itself.

## Notes

A doc-vs-reality finding lives in exactly one place: `x-notes` on the operation
or schema it belongs to. Descriptions stay clean prose and never restate a note.

```json
"x-notes": [
  { "note": "… markdown, one finding …", "source": "live" },
  { "note": "…", "source": "pac-cli" }
]
```

`source` is the evidence grade behind that one finding, and the grades are not
interchangeable. `live` means someone saw the service do this. `pac-cli` means
Microsoft's own decompiled client says so, which is strong structural evidence
and not an observation — the build can be older than the service. Entries come
out grouped by grade, `live` first, so a consumer groups on `source` without
parsing prose and a renderer shows the grades in a stable order under separate
headings.

An earlier revision also folded each note into the owning `description` as a
`> **Heading**` blockquote, because the site was then Stoplight Elements, which
renders `description` and ignores extensions. The site is now the Blazor browser
in [app/](../app), which reads `x-notes` directly and renders it as its own
element, so the duplication is gone.

## Hosts

The API answers on three host forms, and which one an operation is served from is part of its contract. All three are in `servers`, and every operation added from recorded traffic names the one it was observed on.

- `https://api.powerplatform.com` — the global endpoint. Everything the docs describe is reachable here; the gateway routes to the tenant's own cluster.
- `https://{head}.{tail}.tenant.api.powerplatform.com` — tenant-scoped.
- `https://{head}.{tail}.environment.api.powerplatform.com` — environment-scoped.

The tenant and environment hosts are derived from an id alone; there is no region or scale unit in them. Remove the hyphens from the tenant or environment id to get 32 hex characters, then split: the first 30 are the first DNS label, the last 2 are the second. Environment `00000000-0000-0000-0000-0000000000ab` is therefore `https://000000000000000000000000000000.ab.environment.api.powerplatform.com`. Because the host already identifies the scope, these paths carry no id segment — `/connectivity/connections` on the environment host is the same resource as `/connectivity/environments/{environmentId}/connections` on the global host, and `/powerapps/environment` is singular with no id at all.

`POST /powerapps/apps/{appName}/locate` on the global host is the bootstrap: given only an app id it returns the tenant, environment and geography needed to build the right host for everything after. `GET /gateway/cluster` confirms which stamp a host resolved to.

## Sources and how they are graded

Three sources, in descending order of authority. Where they disagree the higher one wins, and the disagreement is recorded rather than smoothed over — there are 36 operations carrying `x-notes` for exactly this reason.

**1. Recorded first-party traffic** — HAR captures of the Power Platform admin centre and the Power Apps maker portal driving this API on a real tenant. This is an observation of the running service, which beats any description of it. **34 of 240 operations** and **30 of 434 schemas** carry `x-probe-verified: true`; 25 of those operations appear in no other source at all, across seven resources Microsoft does not document (user settings, feature gates, notifications, service plans, gateway clusters, Copilot governance settings, governance configurations).

The tokens the recorded clients presented also settle authentication: the audience is `https://api.powerplatform.com` on all three hosts, and the 87 granular delegated permissions seen in real tokens are listed under `x-delegated-scopes` on the security scheme. Which scope each operation requires is *not* recorded there — a token shows what was granted, not what was needed.

**2. `Microsoft.PowerPlatform.Management`**, the Kiota-generated client shipped inside the Power Platform CLI (2.11.2), mined by `scripts/pac_extract.py`. Kiota generates from OpenAPI, so this assembly and the Learn pages are two machine projections of the same internal document — and the client is much the less lossy one, because it carries RFC 6570 URL templates, request and response types, discriminated unions and enum members rather than prose tables. It carries no descriptions at all, though: decompilation strips XML doc comments, so it can say what the shape is and never what it means. Content sourced only from it carries `x-source: pac-cli` and never `x-probe-verified`: a shipped client is strong structural evidence, but the build can be older than the service. **6 operations** and **59 schemas** are marked this way.

**3. The docs mirror** in `docs/`, parsed by `oas.py`. Everything not marked otherwise comes from here, and that is still most of the file. Treat the unmarked majority as a map, not a contract.

### Why the docs are still the base, and the client is not

The client is the better description of the surface it covers. It does not cover enough of it. Measured operation for operation, it has 174 operations over 148 paths against the spec's 240 over 205: **4 operations it knew and the docs did not** (environment enable, disable, SKU change, and an alternate create route), against **66 the docs describe and it omits** — whole documented areas including most of `powerapps`, the `licensing` entitlement tree and `gateway`. Inverting the generator to build from the client would therefore lose two thirds of the surface and every description in the file, to gain four operations and better modelling of the ones it does cover.

A note on a figure that has been quoted the other way: the assembly holds 244 distinct URL templates, which looks like far more than 148 paths. It is not. There are 237 request-builder classes, and only 148 of them ever issue an HTTP verb — the other 89 are fluent-API navigation nodes such as `{+baseurl}/analytics`, which exist so `client.Analytics.AdvisorRecommendations` can be written and address nothing on their own. (Each builder also declares its template twice, once per constructor, so counting raw template literals gives 475.) Any per-namespace count taken from template literals rather than from `RequestInformation(Method.…)` call sites overstates the surface by roughly a factor of two.

So the client is applied as enrichment rather than as the base: `pac_extract.py --check` diffs it against the generated spec after every mirror run, and what it finds is written into `enrichment.json` by hand. As of the last run that diff is down to the deliberate disagreements listed below.

### Where the sources contradict each other

- **`EnvironmentManagementSetting` property casing.** The docs and the client independently agree on camelCase (`powerApps_AllowCodeApps`); the wire returns PascalCase (`PowerApps_AllowCodeApps`), and `$select` matches case-sensitively, so the documented spelling silently returns nothing. Since Kiota preserves wire casing elsewhere in the same assembly, this is not a docs-generation bug: Microsoft's internal OpenAPI really does declare these camelCase and the running service really does not honour it. The wire spelling is what the spec carries.
- **api-version.** The docs claim `2024-10-01` everywhere; the admin centre sends `1`, `2021-10-01-preview`, `2022-03-01-preview` or `3` depending on the namespace; and the CLI forces `2024-10-01` onto every request it makes, overwriting whatever a caller set — including on nine routes where the recorded traffic used an older value. All three are true at once, because the service accepts several versions per route. The `default` on each `api-version` parameter records what was observed, and one recorded 400-free call with `api-version=1` alongside `2024-10-01` on the same route confirms the tolerance directly. Read these defaults as observations of one client, not as a contract.
- **`IpAddressEntity`** names the address kind `IpAddressType` in the docs and `IpType` in the client; neither has been seen on the wire, so the documented name is kept and the other is recorded in a note.
- **`ErrorResponse`** is an envelope (`{error: {...}}`) in the docs and flat (`{code, message, details}`) in the client, on the Power Automate operations that return it. Same treatment: documented shape kept, client shape noted.
- **`includeRuleSetCounts`** is required in the client on all four rule-assignment list routes; the recorded traffic omits it on one of them and succeeds, so that one is documented optional.

### What the client added

Beyond the four operations, the two schemas the docs had left as `x-stub` placeholders turned out to be discriminated unions, and filling them in pulled in 53 further models: `Clause` (nine resource-query clause kinds behind a `$type` discriminator, which is the request body of `POST /resourcequery/resources/query`) and `ActionEvent` (seven AI-flow-run trace event kinds behind a `type` discriminator). It also supplied the `WebApplicationFirewallStatus` enum, `NotSpecified` on two others, three undocumented 409/412 conflict responses on optimistic writes, and several fields the docs omit.

Two further operations come from the CLI's `advisor` module rather than the generated client — a tenant-scoped advisor chat. They are marked preview: the module is behind a feature flag, absent from the CLI's published command manifest, and absent from the generated client, which means the released internal OpenAPI does not describe them yet.

Nothing was inferred: a recorded request/response, or a route the CLI actually builds, is the bar for an addition. Where only an empty collection or a 204 was observed the schema says so rather than inventing an item shape.

## How the mirror works

learn.microsoft.com serves the clean markdown source of any page when asked with an `Accept: text/markdown` header. `fetch.py` discovers every Power Platform page from the site TOC, fetches each as markdown, strips volatile build metadata (so commits only happen on real content changes), and replaces `docs/` atomically only when every page fetched successfully.

The `ppapi-mirror` workflow (`.github/workflows/ppapi-mirror.yml`, run from this folder) fetches daily and commits whatever changed. The commit history is the change log: diff any commit to see exactly what Microsoft changed that day.

## Attribution and licence

The content under `docs/` is Microsoft's documentation, mirrored from learn.microsoft.com and owned by Microsoft. Microsoft documentation is generally published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); this mirror exists for change tracking and offline reference, with attribution to Microsoft Learn as the source. The scripts in this repository are MIT licensed. If Microsoft objects to this mirror it will be taken down.
