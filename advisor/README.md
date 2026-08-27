# advisor

The PowerApps Advisor API (`{region}.api.advisor.powerapps.com`), the service behind Power Platform **solution checker**: it publishes the rule catalogue — what each check looks for, how severe a violation is, where the guidance lives — and runs static analysis over uploaded solution files, returning a [SARIF](https://sarifweb.azurewebsites.net) v2 report.

## Why this one is different

There is no per-region global host. Every environment advertises its own advisor endpoint in its runtime endpoints (`PowerAppsAdvisor`), so the host is per-geography and must be **read from the environment**, not composed from its location — the mapping is not a string transform. That is why the spec's `servers` entry is templated `https://{region}.api.advisor.powerapps.com`.

The decompiled pac CLI later supplied the lookup table behind that mapping (`info.x-dataverse-host-geography-map`), so the composition *is* possible from a Dataverse hostname — `crm4.dynamics.com` → `europe`, `crm22.dynamics.com` → `sweden` — but only as a lookup, and an incomplete one. Reading the environment remains the correct approach; the table is the fallback when there is no environment to ask.

It is also the boundary where the [Terraform provider](https://github.com/microsoft/terraform-provider-power-platform) sees least of the service. `internal/clients/advisor` performs exactly **one** call — `GET /api/rule?api-version=2.0&ruleset=<solution checker>` — and models nine fields of it. The service has a second catalogue read, a three-step analysis job flow, a second submission that writes results into a Dataverse environment, and a tenant-wide cache purge behind the same host.

Unlike [bapi](../bapi), the provider client was the *starting* inventory, not the source of truth. Three sources fed the spec, in descending order of authority: live probing of a real tenant, the decompiled first-party SDK inside the Power Platform CLI, and Microsoft's published documentation. Everything marked `x-probe-verified: true` is what the live service actually returned; everything marked `x-source: pac-cli` is what Microsoft's own client sends and expects, which is not the same thing.

## Layout

```
advisor/
  scripts/probe.py     the live probe harness (read-only, generic, re-runnable)
  oas/openapi.json     the spec (hand-owned, OpenAPI 3.0.3)
  README.md
```

```
scripts/probe.py                                   # survey every known geography
scripts/probe.py --region unitedstates --region europe
scripts/probe.py --host <env's PowerAppsAdvisor host>
scripts/probe.py --ruleset "AppSource Certification"
```

It takes an Entra token for `https://advisor.powerapps.com/.default` from the logged-in az CLI session (or `ADVISOR_TOKEN`), prints shapes, counts and enum distributions rather than tenant data, sleeps between calls and backs off on 429.

**It is read-only by construction**: `request()` refuses any method other than GET/HEAD/OPTIONS, so there is no code path that uploads a solution, starts an analysis job or purges a cache. Route existence for the write endpoints is established *without invoking them* — a GET against a POST-only route answers `405` with `Allow: POST`, and the wrong `api-version` answers `400 UnsupportedApiVersion` instead of a bare `404`. Both prove the route is there; neither submits work. The same trick covers the cache purge: it is probed with GET alone, so a `405` naming `DELETE` confirms it exists without purging anything.

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

## The third source: the first-party SDK inside pac CLI

The Power Platform CLI ships a complete solution-checker SDK, `Microsoft.PowerApps.Checker.Client`, which is what `pac solution check` and the older `Invoke-PowerAppsChecker` PowerShell cmdlet talk to this service with. Decompiling pac 2.11.2 exposed its 32 source files: the `ICheckerClient` interface, the request and response models, the geography map, the retry handler chain and the polling loop.

It is Microsoft's own client for this API, so it is strong structural evidence — real routes, real models, real headers. It is **not** an observation: it is a build artefact that may lag the service. Nothing here was promoted to `x-probe-verified` on its strength. Operations and fields whose only evidence is the SDK carry `x-source: pac-cli`.

### What it added that nothing else had

- **`POST /api/cds/analysisrequest`** — a second analysis submission, undocumented anywhere. The name is misleading and the initial guess about it was wrong: it does **not** analyse a live Dataverse instance. The files still come from storage URIs exactly as with `/api/analyze`; what the Dataverse context buys you is that the run is *written back* into an environment, where it appears in the Solution Health Hub app as `msdyn_analysisjobs` records. It is what `pac solution check --saveResults` does. Three things distinguish it: it answers `200` rather than `202`; it returns a body instead of a `Location` header, so the caller composes the status URL itself as `/api/status/{runcorrelationid}?api-version=1.0`; and it adds a caller-populated `Solutions` list so results are labelled per solution rather than by opaque file URI. The environment is identified entirely by headers — `x-ms-orgurl`, `x-ms-organization-id`, `x-ms-requestorid`, `x-ms-tenant-id` — never by the body.
- **`DELETE /api/QueryValidationResults`** — the cache purge, and the route name is nothing like the `api/cache` one might guess. It clears the **Managed Environments solution checker enforcement cache for the whole tenant**: every stored past verdict, not one solution's. That is the fix for a solution that enforcement keeps blocking on a result you have already remediated, and the cost is that the next import of every other solution pays for a fresh analysis. It is the only route on this host with no `api-version` at all, takes no path, query or body input, and identifies the tenant purely from the token.
- **`tenantId`** as a query parameter on both catalogue reads. The SDK appends it whenever it holds a non-empty tenant id, which implies the catalogue can be tenant-scoped — a tenant with a private ruleset would presumably only see it when this is sent. Live probing never sent it and never needed it, so the effect is unobserved.
- **`x-ms-client-tenant-id`**, sent on *every* request including the catalogue reads, and defaulted to a random GUID when there is no tenant context — which means the service cannot be relying on it for authorization. Distinct from `x-ms-tenant-id`, which names the tenant owning the solution.
- **`ruleLevelOverrides`** on the analysis submission, a member Microsoft's documentation of that body omits. It re-levels named rules for one run without touching the catalogue — how a team accepts a finding without disabling the check. Downgrading below `Critical` is what takes a rule out of the way of Managed Environments enforcement.
- **The `Opened` job state** and the **`additionalMessage`** response field, neither of which appears in Microsoft's documentation. `additionalMessage` is free service text, typically explaining which rules failed to evaluate under `FinishedWithErrors`; pac strips control characters from it before printing, so treat it as untrusted.
- **A transport-level retry contract** (`info.x-retry-contract`) that applies to the whole boundary: `429` carrying `Retry-After` is honoured literally and retried *without limit*, and the header is parsed as an integer count of seconds only — an HTTP-date `Retry-After` aborts the retry rather than being converted. Separately, `408`, `429` and any `5xx` other than `501`/`505` are retried up to three times with exponential backoff between one and ten seconds.
- **Five more geographies and the four sovereign hosts.** `ApiGeographyMap` lists 22 public-cloud geographies to the 17 that answered live, adding `italy`, `newzealand`, `poland`, `sweden` and `unitedstatesfirstrelease` — the last being a first-release *ring* rather than a geography, and the obvious endpoint to diff against when a catalogue difference between regions needs explaining. The sovereign hosts do not follow the `{region}.api.advisor.powerapps.com` pattern at all: `china.api.advisor.powerapps.cn`, `gov.` and `high.api.advisor.powerapps.us`, and `mil.api.advisor.appsplatform.us`.

### What it corrected

- **`POST /api/upload` returns a body.** Microsoft's documentation implies an empty `200`; the SDK deserialises a bare JSON array of storage URIs and takes the first as the URI to analyse. A client that believes the documentation has nothing to put in `sasUriList`. This is the single most consequential correction in this pass.
- **The upload accepts more than zips**, and the part's `Content-Type` is chosen from the extension: `.zip` → `application/x-zip-compressed`, `.cab` → `application/octet-stream`, `.gz` → `application/x-gzip`, `.z` → `application/x-compress`.
- **`resultFileUris` is not "SAS download URIs".** The SDK classifies six URI kinds before downloading and downloads only some: Azure blob SAS (`sig=`), Power Platform blob proxy (`*.powerplatformusercontent.com`, `esig=`), and Dataverse `/api/filedownload` are fetchable; a Dataverse `msdyn_analysisjobs(...)` record URI and a maker-portal deep link (`make.powerapps.com/environments/{id}/solutions/{id}/overview/checkerResults`) are pointers for a human and are *skipped*. Expect the latter kinds back from a Dataverse-context run. Only the blob forms carry a usable file name.
- **The polling contract is a plain fixed-interval loop** with no `Retry-After` handling on the status route and no adaptive backoff: pac waits 30 s between polls for up to 120 polls (an hour's ceiling), the PowerShell cmdlet 15 s for 20 polls (five minutes). `progress` is for a progress bar; nothing reads it to decide when to poll. Terminal states are `Failed`, `Finished` and `FinishedWithErrors`; `Opened` and `InProgress` mean keep going. The client accepts `200` and `202` interchangeably and branches purely on `status`, which is the safer reading — a finished job and a failed one are both `200`.
- **The size limit is unresolved, not 30 MB.** Microsoft documents 30 MB with a `413` above it; the SDK's own guard refuses locally at 100 MB. Both are recorded; neither is verified.
- **`x-ms-tenant-id` is no longer asserted as required.** The SDK never sends it routinely — it sends `x-ms-client-tenant-id` instead, and adds `x-ms-tenant-id` only with the Dataverse-context headers. Microsoft's "required" is kept in the description, but the parameter is now `required: false` because two sources disagree and neither is a live observation.
- **The OAuth audience is per-cloud and chosen from the *Dataverse* host**, not the advisor host: `crm9.dynamics.com` → `https://gov.api.advisor.powerapps.us/`, `crm.dynamics.cn` → `https://china.api.advisor.powerapps.cn/`, and so on. The public-cloud value `https://api.advisor.powerapps.com/` matches the `WWW-Authenticate` challenge probing saw, and is added to the spec's scopes alongside the `https://advisor.powerapps.com/.default` that probing actually used — both app ID URIs resolve.

### What it corroborated

- **`Rules List` and `Rulesets List` stay verified from live probing**, and the SDK agrees with the probe on every point it touches: `api-version=2.0`, `includeMessageFormats` always sent explicitly, and several ruleset GUIDs **joined with a comma into the one `ruleset` parameter** — which is exactly the union behaviour probing found and the provider client never exercised. The SDK also mirrors this API's fail-open behaviour in its own resolver: an unmatched ruleset *name* is a hard client error, an unmatched *GUID* is passed straight through.
- **`IssueSummary`** matches field for field, and **`MessageTemplate`**'s three fields match under the same names.
- **Severity vocabulary agrees.** The SDK's `RuleLevel` enum is `Critical, High, Medium, Low, Informational` — the same five names probing pinned to `severity` 5 down to 1, and the same five buckets as `IssueSummary`. Its C# ordinals run 0–4 in the opposite direction, which looks like a contradiction and is not: the enum is only ever used as a *string* (`OverrideLevel`), never serialised as a number. Live evidence needed no correction.
- **The all-zeros GUID quirk.** Probing found `GET /api/status/00000000-...` faults with a bare `500`. Independently, the SDK treats an all-zeros `runcorrelationid` in a Dataverse-context response as a protocol failure rather than an id, and treats an all-zeros `tenantId` as absent. The service and its own client agree that the zero GUID means "unset", which is why it faults.

### What it did not settle

**The three analysis operations are still `x-probe-verified: false`, and stay that way.** Nobody has run them. The SDK tells us what the product's client sends and expects; it cannot tell us what the service replies, and a decompiled client can be ahead of or behind the deployment. `Rules List` and `Rulesets List` keep their verified markers because they were probed live, not because the SDK agrees with them.

Also unsettled: whether `/api/cds/analysisrequest` and `/api/QueryValidationResults` exist on the live service at all — unlike `/api/analyze`, `/api/upload` and `/api/status`, whose existence *was* confirmed non-destructively, these two were found only in the SDK and have never been touched. `scripts/probe.py` now checks both (with `GET` only for the cache purge, so a `405` naming `DELETE` confirms it without purging anything), so the next live run can close that gap. What `Solution.Status` can contain, whether the catalogue reads behave differently under `tenantId`, and which of 30 MB or 100 MB the upload actually enforces all remain open.

### The other "advisor" in pac 2.11.2 — a different service entirely

`bolt.module.advisor` is new in 2.11.2 and has **nothing to do with this API**. It is a preview, feature-flagged (`ModuleAdvisor`) chat client — `pac advisor ask` and `pac advisor list` — and it talks to the *tenant* endpoint of the Power Platform API, `https://{tenant-hex}.tenant.api.powerplatform.com`, at:

- `POST analytics/advisor/chat/messages?api-version=2024-10-01` — body `{message, conversationId?}`, response `{message, role, executionTimeMs, conversationId}`
- `GET  analytics/advisor/chat/conversations?api-version=2024-10-01` — response `{value: [{conversationId, title, timestamp}]}`

Different host, different audience, different api-version, different concept: a conversational assistant over tenant analytics, not solution checker. It belongs to whoever owns the Power Platform API / analytics boundary and was deliberately **not** added here. It does not appear in `pac.doc.json`, consistent with it being unreleased.

### One dead end

`ErrorCodes`/`ErrorCodesMap` are not service error codes, despite the name. They are the PowerShell cmdlet's own client-side failure identifiers (`PACHECKER_PS_NO_SAS_URI`, `PACHECKER_PS_STATUS_TIMEOUT`, `PACHECKER_PS_INVALID_PARAM`, `PACHECKER_PS_FILE_NOT_FOUND`, `PACHECKER_PS_DIRECTORY_NOT_FOUND`, `PACHECKER_PS_FILE_TOO_LARGE`), used to build an `fwlink` help URL. Nothing about them reaches the wire, so none of them was documented as an API error.

## What was not probed, and why

The analysis-job operations — `POST /api/upload`, `POST /api/analyze`, `GET /api/status/{analysisId}` on a real job, `POST /api/cds/analysisrequest` and `DELETE /api/QueryValidationResults` — carry `x-probe-verified: false`. Exercising them means uploading solution files, submitting real analysis jobs, or purging a production tenant's enforcement cache, which this exercise does not do. Their request and response bodies come from Microsoft's documentation and from the first-party SDK, not from observation.

What *was* established live for the first three, non-destructively: all three routes exist, are served at api-version `1.0` only, `analyze` and `upload` accept `POST` alone, `status` accepts GET, all three require a bearer token, and `status` returns problem+json for an unknown job. Their `x-probe-verified: false` stands regardless, because the payloads are the part that matters and the payloads are unverified. The last two routes have not even had their existence confirmed.

## Conventions

- 7 operations over 7 paths, tagged by logical resource (Rules, Rulesets, Analysis, Enforcement Cache), OpenAPI 3.0.3.
- **Three evidence grades, kept distinct.** `x-probe-verified: true` means observed against the live service — the two catalogue reads and the schemas confirmed with them. `x-source: pac-cli` means the decompiled first-party SDK is the evidence, and never implies verification. Anything with neither is from Microsoft's published documentation. Where sources disagree, the live evidence wins and the description says so.
- `required` is listed only where probing proved presence across all 1531 observed rule objects — on responses, not on the unprobed request bodies (the one exception, `AnalysisRequest.sasUriList`, is Microsoft's documented requirement, corroborated by the SDK refusing to submit without it, and is marked unverified alongside its schema).
- Closed value sets are carried as `enum` rather than described in prose: severities, categories, `componentType`, ruleset ids and names, api-versions, job statuses, rule override levels, the server region variable.
- Status-code meanings live under their own response entries, never in operation descriptions.
- **Doc-vs-reality findings live in `x-notes`, not in prose.** Each entry is `{"note", "source"}`, `source` being the evidence grade behind that one finding — `live` for what probing saw, `pac-cli` for what only the SDK attests to. Descriptions describe the API; the notes are where the published reference is contradicted, and the spec browser renders each grade as its own callout so the two are never read as equally solid. The shape is the one `ppapi/scripts/oas.py` emits.
- Property-name casing is asserted only where a source proves it. The analysis submission is documented in Microsoft's camelCase with a note that the SDK sends PascalCase and the service accepts both; the Dataverse-context submission, whose only source is the SDK, is documented in the PascalCase the SDK provably sends.

## Status

Spec complete and validating. The catalogue surface is fully probed against a live tenant across all 17 public-cloud geographies. The analysis job flow, the Dataverse-context submission and the enforcement-cache purge are documented from Microsoft's documentation and the decompiled first-party SDK, and are marked unverified. Sovereign clouds (US Government, China, DoD) are now listed as servers on the SDK's authority but were not probed.
