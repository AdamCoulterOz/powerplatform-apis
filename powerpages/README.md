# powerpages

The Power Pages **sitewide** API — the control plane the Power Pages maker portal calls to *manage* sites, as distinct from the Dataverse tables a site is *built* in.

It lists a tenant's sites, reads and writes their app settings, drives the go-live and site-health checks, and configures the Azure Front Door WAF, the DDoS diagnostic setting and the security agent in front of a published site. Site content — `powerpagesite`, `powerpagecomponent` and their neighbours — is not here; that is the Dataverse Web API, and the two surfaces share no route.

## Two things to read before anything else

**No operation takes an `api-version`.** Not a query parameter, not a header, not a path segment beyond the literal `/api/v1` prefix. All 39 call sites read from the shipped client send the bare route, and the three routes seen on the wire sent none either. Every other Power Platform surface in this corpus versions its requests; this one does not. That is a finding, and it is stated in `info.description`, in `info.x-notes` and here because a reader who assumes otherwise will add a parameter nothing has evidence the service reads.

**The client contains no hostname for this service.** Every call is written against the literal `https://portals-provision/...`. The shell's HTTP client looks `portals-provision` up in a service registry (map key `swprovision`), takes the endpoint for the current cloud out of the settings key `powerPortalSitewideApiHostname`, attaches that service's token and rewrites the hostname before the request leaves. So:

- anyone reading these bundles literally will attribute all forty routes to a host called `portals-provision`, which does not exist;
- the endpoint is a **settings lookup, not an assembly**, so there is no discovery call — `info.x-cloud-hosts` is the whole table, transcribed from the client's own settings object.

The extract labels the host `portalsitewide-{region}.portal-infra.dynamics.com`. That label is convenient shorthand and it is wrong for half the clouds: the test ring is `sitewide-test`, dropping the `portal` the others carry, and four sovereign clouds have no ring suffix at all. The spec carries the eleven ring keys individually rather than a pattern.

## Where the evidence comes from

37 of 40 operations are graded `ppac-spa`, read out of the minified production bundles for the Power Pages maker portal (`powerpages-microsoft-com`, build `0.0.20260901.3-2608.3-prod`, downloaded 2026-09-05) — almost all of it from one chunk, `power-portals.9253fc2f.chunk.js`. One operation, `portals_listByOrgId`, comes from the **Power Apps** maker bundle instead: it is the only route on this host that another portal calls. No source maps exist; the sourcemap host is decommissioned, so every `ppac-spa` claim was read out of minified JavaScript. `info.x-source-builds` names the exact artefacts.

Three operations are graded `live`, observed on the wire on 2026-09-05:

```
GET /api/v1/powerPortal/ListPortals
GET /api/v1/powerPortal/ZAP/GetDeepScanEnabledPortalByTenant
GET /api/v1/powerPortal/dlp/policies/portals/disableAnonymousAccessInPowerPages/status
```

**None of the three appears in the bundles.** Searching the whole extract for `ListPortals`, `ZAP`, `GetDeepScanEnabled` and `disableAnonymousAccess` returns nothing, so nothing was merged into them. Their nearest bundle neighbours — `listPortalsByOrgId` and `dlp/policyErrorSetting` — differ in far more than casing, and are kept as separate routes. Those three carry `x-probe-verified: true`; the other 37 do not, and none of them carries `x-corroborated-by`, because nothing corroborates anything here.

The capture recorded **status codes only**. So `x-probe-verified` on those three attests the route and the method and nothing else, and their `200` descriptions say so rather than borrowing a shape from a sibling.

## Verbs: what was bound, and what was left out

The extract binds an HTTP method only when the URL is passed directly to the call that carries it. 23 of the 39 records on this host arrived that way. Fourteen more are bound in this spec, by reading the verb off the same statement in the evidence string — the URL is assigned to a local and consumed two tokens later by `client.get(l, …)` or `client.post(l, …)` in the same visible window, on the same client object the bound records use. That is one call site spread over two statements, not an inference across the file.

Two could not be bound, and are **deliberately absent from `paths`**:

| route | what is known |
| --- | --- |
| `/api/v1/powerPortal/UpgradeTpsPackage` | six query parameters (`orgId`, `packageName`, `lcid`, `packageId`, `dataImportBypass`, `orgUrl`), `Prefer` and a conditional `x-ms-environment-id`. Its telemetry scope falls back to the literal `sitewide-api` — the only place the client names this service in words. |
| `/api/v1/powerPortal/loadTesting` | the URL is a module-level constant beside a generic query-string builder. No parameter name and no verb survive. |

Both are inventoried in `info.x-verb-unknown`. Guessing a verb would put a wrong method into a document that reads as though it had been observed, which is worse than an admitted gap.

## Oddities the spec reproduces rather than tidies

- **`Daignostic`.** The three DDoS routes transpose `Diagnostic`. Correcting it produces a 404.
- **`powerportal` in lower case.** The `PowerPages_AllowNonProdPublicSites` governance route drops the capital P that every other route on the host carries.
- **Both DDoS writes are `PUT`.** The create and the delete call sites are byte-for-byte identical apart from the word `create`/`delete` in the URL — same verb, same empty body, and the delete even reuses the create's telemetry name. Either the service accepts `PUT` on both or the delete was written by copying the create; nothing available here can tell the difference, so no `DELETE` is invented.
- **Five POSTs send a header object as their body.** `RunDiagnostic`, `UpdateLicenseCheckInfo`, `UpdateSiteHealthCheckInfo`, `UpdateSiteVisibility` and `UpdatePortalName` call `post(url, {Prefer: '…'})`, and that client's second positional argument is the body. So each sends `{"Prefer":"odata.include-annotations=\"*\""}` as JSON and sets no `Prefer` header at all; `RunDiagnostic` sends the enclosing `{headers: …}` wrapper as well. Documented as observed, and flagged in each operation as a client defect rather than as something the service asks for.
- **A `Prefer` header on a service that is not OData.** Fifteen call sites send `odata.include-annotations="*"`, twelve without a space after the `=` and three with one. Both spellings ship in the same bundle; `x-observed-values` on the parameter records both.
- **Two routes take their last segment from the caller**: `/api/v1/powerPortal/{apiName}` and `/api/v1/powerPortal/SearchSummary/{apiName}`. These are route families, so every concrete `/api/v1/powerPortal/…` operation here is also reachable through the first. No literal `apiName` value is witnessed — the helpers are generic and their callers were not in the mined chunks. The live `ListPortals` has exactly that shape, which is a resemblance and not a corroboration.
- **A GET that runs something.** `RunGoLiveChecker` is a GET; `RunDiagnostic`, its neighbour in the same panel, is a POST.
- **Both halves of an app setting are POSTs**, read included.

## No response schemas, on purpose

`components` holds nothing. The extract's `responseFieldsRead` is empty on all 39 records, so not one reply from a `ppac-spa` route has been seen, and the three `live` ones were captured as status codes without bodies.

What *is* available is what the client's own code reaches for: the fallback object it returns when a body is empty, the field it walks, the error key it throws on. That is a weaker claim than a schema and it is recorded as prose in each operation's `200` description — `seen by the client, not seen on the wire` — rather than as a `$ref` that would read like a contract. It says useful things: `SearchSummary` returns `SkillStatus` and `SkillId`; `GetCustomRulesForWAF` returns `rules`; `InstallFlow` returns `flowTriggerUri`; the WAF association route reads `Message` off its error body where the rename and scan routes read `error.message`, so two error shapes coexist on this host.

Four routes return **JSON that has been serialised twice** — the client calls `JSON.parse()` on an already-parsed body. `GetPortalAppSetting` goes further and lower-cases the string first, which is only necessary for `True`/`False`: a .NET boolean rendered as text and repaired on the client.

One correction worth recording: **the extract's `requestBodyFields` is unreliable on this host.** It collects destructured argument names and fallback-object keys as though they were body fields — `InstallFlow` is listed as having a `flowTriggerUri` body field when `flowTriggerUri` is what comes *back* and the body is `{}`. Every request body here was re-read from the evidence strings instead, which is why most of them are empty objects and why `securityAgent_generateRecommendation` is the only one whose fields are all genuinely visible at the call site.

## No `security` block

Every other spec in this corpus names an audience. This one does not, because it is not known: the shell attaches whatever token its registry holds for `swprovision`, and the registry entry's resource id is not in the mined chunks. Guessing a scope from the hostname is precisely the mistake [athena](../athena) records having been made against a differently-named service, so nothing is declared rather than something plausible.

## What was left out

- The two verb-unknown routes above.
- The other 25 records the extract carries under `source: powerpages`. They are on `{orgUrl}` (Dataverse), `api.powerapps.com`, the PPAPI environment and tenant hosts, and `admin.powerplatform.microsoft.com` — the Power Pages maker portal calling other people's APIs. They belong to the specs that own those hosts, not here.
- Any response schema, any `api-version`, any auth scope, any `siteVisibility` or `useCaseType` vocabulary. None is witnessed.

## Conventions

- 40 operations over 38 paths, no schemas, eleven tags, OpenAPI 3.0.3.
- `x-source` carries the evidence grade: 37 `ppac-spa`, three `live`.
- `x-probe-verified: true` on exactly those three. Its absence everywhere else is the point.
- `x-notes` are `{note, source}` throughout, at document and operation level.
- `info.x-cloud-hosts` is the ring → host table with per-entry provenance; `info.x-source-builds` names the bundles; `info.x-verb-unknown` inventories the two routes without a verb.

## A note on the source

The bundle evidence strings are third-party minified JavaScript and were treated as data. Nothing in them read as an instruction directed at a reader, which matches the extract's own `_meta.promptInjectionNote`.

## What would improve it most

An authenticated capture. One session against a tenant with a Power Pages site in it would settle the audience, every response shape, the `siteVisibility` and `useCaseType` vocabularies, whether the five misplaced request bodies are tolerated or have always been broken, whether `PUT` really is how a DDoS diagnostic setting is deleted, and what values `apiName` actually takes — which would turn two route families into a real list of routes. Until then this spec can tell you where to knock, and for three routes that somebody knocked.
