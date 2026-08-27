---
layout: Reference
title: Environment Restore - Restore Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-restore/restore-environment
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentrestore.restoreenvironment
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
description: 'Learn more about Power Platform API service - Restores the specified environment to a previous backup. '
locale: en-us
document_id: 36aa87d4-c1e5-b83a-d1af-8fca438a8204
document_version_independent_id: 1a87aeca-1829-b081-574d-82064c1666ee
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Restore/Restore-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-restore/restore-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Restore/Restore-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/aebdc4a3-c54b-4eea-94e3-663d5e166f57
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/1baec8e6-ab38-4b56-bb59-f6282d94f311
platformId: ac505976-81b2-fa8e-7c27-3982791307d9
---

# Environment Restore - Restore Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Restores the specified environment to a previous backup.

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{targetEnvironmentId}/restore?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{targetEnvironmentId}/restore?ValidateOnly={ValidateOnly}&ValidateProperties={ValidateProperties}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| targetEnvironmentId | path | True | string | The ID of the target environment that will be overwritten. |
| api-version | query | True | string | The API version. |
| ValidateOnly | query |  | boolean | When true, validates the request without executing it. Use with validateProperties to validate only specific fields. If validateProperties is empty, the entire request is validated. Defaults to false (validate and execute). |
| ValidateProperties | query |  | string | A comma-separated list of property names to validate (for example, "property1,property2"). Applies only when validateOnly is true. |

## Request Body

Media Types: "application/json", "text/json", "application/\*+json"

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| restorePointDateTime | True | string (date-time) | The point in time to restore the environment to. Must include a timezone offset per RFC 3339 (for example, 2025-04-30T12:34:56+02:00). |
| sourceEnvironmentId | True | string | The ID of the source environment from which the backup will be restored. |
| restoreOptions |  | RestoreRequestOptions | Optional inputs for restore request. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted |
| 400 Bad Request | ValidationResponse | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 429 Too Many Requests |  | Too Many Requests |
| Other Status Codes | ValidationResponse | Conflict |

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
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| RestoreRequest | Request model for restoring an environment to a previous backup. |
| RestoreRequestOptions | Optional inputs for restore request. |
| ValidationResponse | Represents the response for validation of an operation. |

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

### RestoreRequest

Object

Request model for restoring an environment to a previous backup.

| Name | Type | Description |
| --- | --- | --- |
| restoreOptions | RestoreRequestOptions | Optional inputs for restore request. |
| restorePointDateTime | string (date-time) | The point in time to restore the environment to. Must include a timezone offset per RFC 3339 (for example, 2025-04-30T12:34:56+02:00). |
| sourceEnvironmentId | string | The ID of the source environment from which the backup will be restored. |

### RestoreRequestOptions

Object

Optional inputs for restore request.

| Name | Type | Description |
| --- | --- | --- |
| environmentNameToOverride | string | Environment name to override on target environment. |
| securityGroupIdToOverride | string | Security group ID to override on target environment. |
| skipAuditData | boolean | Boolean flag to skip audit data during restore. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |