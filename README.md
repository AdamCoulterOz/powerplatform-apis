# powerplatform-apis

Browsable, machine-readable references for the family of APIs behind Microsoft Power Platform, each reverse-engineered from the best available source and kept current. Published at [adamcoulteroz.github.io/powerplatform-apis](https://adamcoulteroz.github.io/powerplatform-apis/).

## Layout

One folder per API. Each folder is self-contained: its own extraction scripts, its source material where relevant, and a generated `oas/openapi.json` in the same shape, so any OpenAPI reader can render it.

```
powerplatform-apis/
  index.html               redirect to the browser, with this catalogue selected
  specs.json               the APIs the browser offers, each pointing at its own oas/openapi.json
  ppapi/                   Power Platform API — reverse-engineered from Microsoft Learn's OpenAPI-generated docs
  bapi/                    Business Application Platform API — reverse-engineered from the Terraform provider's code
  .github/workflows/       per-API refresh jobs (e.g. ppapi-mirror runs daily)
```

The site is published by the `pages` workflow, which serves the specs, the catalogue, the deep-link index and the documentation mirrors, plus a redirect at the root.

**The viewer lives elsewhere.** It is a general OpenAPI browser at [AdamCoulterOz/oas-browser](https://github.com/AdamCoulterOz/oas-browser), which knows nothing about Power Platform and loads this corpus by URL. The root redirect sends a reader there with this catalogue selected, preserving any fragment so an existing deep link survives the hop. The specs themselves stay addressable here and are readable without the viewer at all.

That the browser fetches this corpus from another origin makes one header load-bearing: GitHub Pages serves `access-control-allow-origin: *`, and if that ever stops the browser fails to load this corpus silently rather than loudly.

To surface a new API, add an entry to `specs.json` pointing at its `oas/openapi.json`: the deploy checks that every spec named there is actually present, and fails rather than shipping a picker with a dead entry.

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
