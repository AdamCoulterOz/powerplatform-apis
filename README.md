# powerplatform-apis

Browsable, machine-readable references for the family of APIs behind Microsoft Power Platform, each reverse-engineered from the best available source and kept current. Published at [adamcoulteroz.github.io/powerplatform-apis](https://adamcoulteroz.github.io/powerplatform-apis/).

## Layout

One folder per API. Each folder is self-contained: its own extraction scripts, its source material where relevant, and a generated `oas/openapi.json` in the same shape, so the browser at the repo root can render any of them.

```
powerplatform-apis/
  index.html, specs.json   the spec browser (Stoplight Elements); reads each spec from its folder
  ppapi/                   Power Platform API — reverse-engineered from Microsoft Learn's OpenAPI-generated docs
  bapi/                    Business Application Platform API — reverse-engineered from the Terraform provider's code
  .github/workflows/       per-API refresh jobs (e.g. ppapi-mirror runs daily)
```

The site loads each spec from its folder over the same origin (no external fetch), so a spec change is live as soon as Pages redeploys. To surface a new API in the browser, add an entry to `specs.json` pointing at its `oas/openapi.json`.

## APIs

| Folder | API | Host | Source of the spec |
|---|---|---|---|
| [ppapi](ppapi) | Power Platform API | `api.powerplatform.com` | Microsoft Learn (OpenAPI-generated docs) |
| [bapi](bapi) | Business Application Platform API | `api.bap.microsoft.com` | Terraform provider client, corrected by live probing |
| [dataverse](dataverse) | Dataverse Web API (admin/ALM subset) | `{org}.crm*.dynamics.com` | Terraform provider client, corrected by live probing |
| [powerapps](powerapps) | PowerApps API | `api.powerapps.com` | Terraform provider client, extended by live probing |
| [admin](admin) | Power Platform Admin Centre API | `api.admin.powerplatform.microsoft.com` | Terraform provider client, corrected by live probing |
| [analytics](analytics) | Admin analytics (CS Analytics) | `{geo}.csanalytics.powerplatform.microsoft.com` | Terraform provider client, corrected by live probing |
| [advisor](advisor) | PowerApps Advisor (solution checker) | `{region}.api.advisor.powerapps.com` | Terraform provider client, extended by live probing |
| [copilot](copilot) | Copilot Studio | per-environment PVA gateway, e.g. `powervamg.wus-il102.gateway.prod.island.powerapps.com` | Terraform provider client (responses licence-gated, unverified) |
| [athena](athena) | Synapse Link / Link to Fabric orchestration | `athenawebservice.{regionPrefix}{clusterSuffix}.powerapps.com`, e.g. `athenawebservice.wus-il102.gateway.prod.island.powerapps.com` | Recorded UI traffic (the provider's `feature/fabric-link-ropc` branch covers only 3 of its 15 operations) |
| [licensing](licensing) | Power Platform Licensing | `licensing.powerplatform.microsoft.com` | Recorded UI traffic + live probing |

Note that `admin` and `athena` are entirely different services: `admin` is the
Power Platform admin centre API, `athena` is the Synapse Link / Link to Fabric
orchestration service reached at each environment's own gateway cluster.

## Nature of these specs

Every spec here is an unofficial reconstruction, not verified end to end against the live service. Treat them as maps, not contracts. Each folder's README records where its spec comes from and how faithful it is.
