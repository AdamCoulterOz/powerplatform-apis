---
layout: Reference
title: Environment Copy - Get Environment Copy Candidates - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-copy/get-environment-copy-candidates
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentcopy.getenvironmentcopycandidates
uhfHeaderId: MSDocsHeader-PowerPlatform
enable_rest_try_it: false
rest_product: powerplatform-rest
breadcrumb_path: ~/breadcrumb/toc.yml
author: laneswenka
ms.author: laswenka
ms.topic: generated-reference
ms.devlang: rest-api
ms.date: 2023-06-13T00:00:00.0000000Z
ms.service: power-platform
ms.subservice: developer
feedback_system: None
description: 'Learn more about Power Platform API service - Gets the list of environments that can be copied as the target environment. '
locale: en-us
document_id: 9a58ae60-0c8c-a9c0-22f6-1da9982dd4cb
document_version_independent_id: 11d6ea95-e9cc-d6b3-07b2-96f2c1ac2f3b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Copy/Get-Environment-Copy-Candidates.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-copy/get-environment-copy-candidates
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Copy/Get-Environment-Copy-Candidates.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 4801c53d-35d7-fcab-8bab-b584745d62d4
---

# Environment Copy - Get Environment Copy Candidates

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of environments that can be copied as the target environment.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{sourceEnvironmentId}/copyCandidates?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{sourceEnvironmentId}/copyCandidates?ValidateOnly={ValidateOnly}&ValidateProperties={ValidateProperties}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| sourceEnvironmentId | path | True | string | The ID of the source environment to copy from. |
| api-version | query | True | string | The API version. |
| ValidateOnly | query |  | boolean | When true, validates the request without executing it. Use with validateProperties to validate only specific fields. If validateProperties is empty, the entire request is validated. Defaults to false (validate and execute). |
| ValidateProperties | query |  | string | A comma-separated list of property names to validate (for example, "property1,property2"). Applies only when validateOnly is true. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentPagedCollection | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 400 Bad Request | ValidationResponse | Bad Request<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 401 Unauthorized |  | Unauthorized<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 403 Forbidden |  | Forbidden<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 404 Not Found |  | Not Found<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 429 Too Many Requests |  | Too Many Requests<br><br>Media Types: "text/plain", "application/json", "text/json" |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

| Name | Description |
| --- | --- |
| Environment | Power Platform environment. |
| EnvironmentPagedCollection |  |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| ValidationResponse | Represents the response for validation of an operation. |

### Environment

Object

Power Platform environment.

| Name | Type | Description |
| --- | --- | --- |
| dataverseOrganizationUrl | string | Dataverse organization URL of the environment. |
| displayName | string | Display name of the environment. |
| environmentId | string | The environment ID. |

### EnvironmentPagedCollection

Object

| Name | Type | Description |
| --- | --- | --- |
| collection | Environment[] | Power Platform environment. |
| continuationToken | string |  |

### FieldError

Object

The error detail for a single field.

| Name | Type | Description |
| --- | --- | --- |
| errorMessages | string[] | The error messages describing what is wrong with the field. |
| suggestedValue | string | A suggested or accepted value that would resolve the error. |

### OperationErrorDetail

Object

Structured error detail for a failed request.

| Name | Type | Description |
| --- | --- | --- |
| code | string | The error code. |
| fieldErrors | &lt;string, FieldError&gt; | Per-field error detail, keyed by field name. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |