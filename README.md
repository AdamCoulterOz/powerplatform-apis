# powerplatform-apis

A browsable reference for the Power Platform admin APIs, published at [adamcoulteroz.github.io/powerplatform-apis](https://adamcoulteroz.github.io/powerplatform-apis/).

The site renders OpenAPI specs that are reverse-engineered daily from the public Microsoft Learn documentation by the `pp-{ApiName}` mirror repos. It always shows the latest committed spec, with operations grouped by logical resource rather than by Microsoft's transport namespaces.

Current APIs:

- **PPAPI** (api.powerplatform.com) from [pp-PPAPI](https://github.com/AdamCoulterOz/pp-PPAPI)

To add another API, add an entry to `specs.json` with an `id`, a `title`, the raw URL of its OpenAPI file, and its mirror repo. The dropdown picks it up automatically.

The specs are unofficial reconstructions and are not verified against the service. Treat them as a map, not a contract.
