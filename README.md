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
| [bapi](bapi) | Business Application Platform API | `api.bap.microsoft.com` | Terraform provider source (scaffold) |

Not yet built, but part of the intended set (host patterns for reference):

| API | Host |
|---|---|
| dataverse | `{org}.crm*.dynamics.com` |
| powerapps | `api.powerapps.com` |
| admin | `api.admin.powerplatform.microsoft.com` |
| analytics | `{geo}.csanalytics.powerplatform.microsoft.com` |
| advisor | `{region}.api.advisor.powerapps.com` |
| copilot | per-environment PVA gateway, e.g. `powervamg.eu-il107.gateway.prod.island.powerapps.com` |
| athena | `athenawebservice.e{clusterSuffix}.powerapps.com` (Fabric link) |

## Nature of these specs

Every spec here is an unofficial reconstruction, not verified end to end against the live service. Treat them as maps, not contracts. Each folder's README records where its spec comes from and how faithful it is.
