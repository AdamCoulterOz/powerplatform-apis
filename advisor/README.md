# advisor

The PowerApps Advisor API (`{region}.api.advisor.powerapps.com`), the service behind Power Platform **solution checker**: it publishes the rule catalogue — what each check looks for, how severe a violation is, where the guidance lives — and runs static analysis over uploaded solution files, returning a [SARIF](https://sarifweb.azurewebsites.net) v2 report.

## Why this one is different

There is no per-region global host. Every environment advertises its own advisor endpoint in its runtime endpoints (`PowerAppsAdvisor`), so the host is per-geography and must be **read from the environment**, not composed from its location — the mapping is not a string transform. That is why the spec's `servers` entry is templated `https://{region}.api.advisor.powerapps.com` with the 17 public-cloud geographies that answered live.

It is also the boundary where the [Terraform provider](https://github.com/microsoft/terraform-provider-power-platform) sees least of the service. `internal/clients/advisor` performs exactly **one** call — `GET /api/rule?api-version=2.0&ruleset=<solution checker>` — and models nine fields of it. The service has a second catalogue read and a three-step analysis job flow behind the same host.

Unlike [bapi](../bapi), the provider client was the *starting* inventory, not the source of truth. Everything in `oas/openapi.json` marked `x-probe-verified: true` is what the live service actually returned.

## Layout

```
advisor/
  scripts/probe.py     the live probe harness (read-only, generic, re-runnable)
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py                                   # survey all 17 geographies
scripts/probe.py --region australia --region europe
scripts/probe.py --host <env's PowerAppsAdvisor host>
scripts/probe.py --ruleset "AppSource Certification"
```

It takes an Entra token for `https://advisor.powerapps.com/.default` from the logged-in az CLI session (or `ADVISOR_TOKEN`), prints shapes, counts and enum distributions rather than tenant data, sleeps between calls and backs off on 429.

**It is read-only by construction**: `request()` refuses any method other than GET/HEAD/OPTIONS, so there is no code path that uploads a solution or starts an analysis job. Route existence for the three analysis endpoints is established *without invoking them* — a GET against a POST-only route answers `405` with `Allow: POST`, and the wrong `api-version` answers `400 UnsupportedApiVersion` instead of a bare `404`. Both prove the route is there; neither submits work.

## What live probing changed

Probing the two catalogue reads against 17 geographies (1531 rule objects) corrected or added things the provider client alone could not show:

- **The catalogue is not uniform across geographies.** The provider client's comment says "the ruleset is always the same for all regions". It is not: the Solution Checker ruleset returned **98 rules in `unitedstates` and `australia`, 89 in the other 15** — the nine `web-sdl-*` security rules had reached only two deployment rings. Anything that diffs, caches or pins the catalogue must key by region.
- **Real enum semantics.** `severity` and `primaryCategory` are bare integers in the provider DTO. Cross-referencing 38 rule codes against their documented severities and categories on Microsoft Learn pins them with no collisions: severity `1 Informational, 2 Low, 3 Medium, 4 High, 5 Critical` (2–5 observed); category `1 Performance, 2 Upgrade Readiness, 3 Usage, 4 Security, 5 Design, 7 Maintainability, 8 Supportability, 9 Accessibility, 10 licensing`. The numbering is **not** the order of the published category list. `6` never appeared anywhere and is presumed Online Migration, the one documented category with no live rule. `componentType` is `0` on every rule in every geography — no mapping is derivable, and the component family is instead readable from the code prefix (`app-`, `connector-`, `desktopflow-`, `flow-`, `meta-`, `web-`).
- **Real optionality.** `code`, `guidanceUrl`, `include`, `componentType`, `primaryCategory` and `severity` are present on all 1531 rule objects; `description`, `summary` and `howToFix` are **absent entirely** on rules with no authored text (`web-unsupported-syntax`), and `howToFix` is an empty string on about half the rest. No property was ever explicitly `null`. `include` is `true` on every rule this endpoint returns, so it is not a usable filter.
- **Two undocumented-by-the-provider query parameters.** `includeMessageFormats=true` adds per-rule SARIF message templates (135 over 98 rules), and `Accept-Language` localises `summary`, `description` and `howToFix` while leaving `code`, `guidanceUrl`, `severity` and `primaryCategory` invariant. Ruleset *names* are not localised.
- **`ruleset` fails open.** An unrecognised id or name is not rejected — it returns the single rule that belongs to no ruleset, so a typo silently yields a near-empty catalogue. An empty, whitespace or bare-comma value behaves like omitting the parameter and returns everything. It also accepts **display names** case-insensitively and **comma- or semicolon-separated lists**, whose result is the union (103 for both public rulesets, which overlap heavily). Microsoft's documented `204` for "no results" was not reproducible by any input.
- **A second ruleset exists.** `GET /api/ruleset` — a route the provider never calls — returns `Solution Checker` (`0ad12346-…`) and `AppSource Certification` (`083a2ef5-…`), identically in all 17 geographies. They overlap rather than nest: AppSource has 5 rules Solution Checker lacks, Solution Checker has 39 AppSource lacks. Note that Microsoft's own rule documentation labels `083a2ef5-…` "Solution Checker" in its examples; the service disagrees.
- **Two unrelated error envelopes, and a contradicted doc.** An unsupported `api-version` returns `{"error":{"code","message"}}` — whose `message` leaks the internal service-fabric node address of the instance that served the request, so log it but never surface it. A query parameter that fails model binding returns an RFC 9110 `ValidationProblemDetails` instead. The analysis status route uses a third shape, `application/problem+json`. Separately, Microsoft documents the rule and ruleset reads as needing no OAuth token; live they answer `401` with a `WWW-Authenticate` challenge naming `resource_id="https://api.advisor.powerapps.com/"`.
- **`howToFix` is a string, not an object.** Microsoft's documentation shows it as `{"summary": ""}`. At api-version 2.0 the service returns a plain string — the provider's DTO is right and the docs are stale.
- **Two api-versions coexist.** `2.0` serves the catalogue reads (`1.0` works too, identically; omitting it also works); the analysis routes are `1.0` only. Sending the wrong one is rejected as an unsupported version rather than as a missing route.
- **A sentinel that faults.** `GET /api/status/{id}` answers a clean `404 problem+json` for any unknown GUID, but the **all-zeros GUID** produces a bare `500` with an empty body — it is evidently treated as an unset value rather than an unknown id. Do not use it as a placeholder.

## What was not probed, and why

The three analysis-job operations — `POST /api/upload`, `POST /api/analyze`, `GET /api/status/{analysisId}` on a real job — are transcribed from [Microsoft's public documentation](https://learn.microsoft.com/power-platform/alm/checker-api/overview) and carry `x-probe-verified: false`. Exercising them means uploading solution files and submitting real analysis jobs against a production tenant, which this exercise does not do. Their request and response bodies are therefore documentation, not observation.

What *was* established live for them, non-destructively: all three routes exist, are served at api-version `1.0` only, `analyze` and `upload` accept `POST` alone, `status` accepts GET, all three require a bearer token, and `status` returns problem+json for an unknown job. Their `x-probe-verified: false` stands regardless, because the payloads are the part that matters and the payloads are unverified.

## Conventions

- 5 operations over 5 paths, tagged by logical resource (Rules, Rulesets, Analysis), OpenAPI 3.0.3.
- `x-probe-verified: true` on the two catalogue reads and the seven schemas confirmed live; `false` on the three analysis operations and their five schemas.
- `required` is listed only where probing proved presence across all 1531 observed rule objects — on responses, not on the unprobed request bodies (the one exception, `AnalysisRequest.sasUriList`, is Microsoft's documented requirement and is marked unverified alongside its schema).
- Closed value sets are carried as `enum` rather than described in prose: severities, categories, `componentType`, ruleset ids and names, api-versions, job statuses, the server's region variable.
- Status-code meanings live under their own response entries, never in operation descriptions.

## Status

Spec complete and validating. The catalogue surface is fully probed against a live tenant across all 17 public-cloud geographies; the analysis job flow is documented but unverified and marked as such. Sovereign clouds (US Government, China, DoD) use different hostnames and were not probed.
