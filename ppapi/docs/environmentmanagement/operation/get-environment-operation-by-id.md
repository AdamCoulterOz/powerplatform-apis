---
layout: Reference
title: Operation - Get Environment Operation By ID - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/operation/get-environment-operation-by-id
uid: api.powerplatform.com.power-platform.environmentmanagement.operation.getenvironmentoperationbyid
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
description: Gets the status of a lifecycle operation scoped to a specific environment. Gets the status of an environment lifecycle operation scoped under a specific environ
locale: en-us
document_id: 0a04ca25-2f81-184b-ce64-3486d480b1ff
document_version_independent_id: 3b2d30db-74f1-92ad-7709-e2e1b92c2045
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Operation/Get-Environment-Operation-By-ID.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/operation/get-environment-operation-by-id
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Operation/Get-Environment-Operation-By-ID.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 4dcfff09-bd13-30cb-1193-1463203dce83
---

# Operation - Get Environment Operation By ID

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the status of a lifecycle operation scoped to a specific environment. Gets the status of an environment lifecycle operation scoped under a specific environment, enabling environment-level authorization on the operation lookup.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{targetEnvironmentId}/operations/{operationId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| operationId | path | True | string | The ID of the operation. |
| targetEnvironmentId | path | True | string | The ID of the target environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | OperationExecutionResult | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| OperationExecutionResult | The result of an environment lifecycle operation. |
| OperationStatus | The status of operation. |
| StageStatus | The status of a single stage of an operation. |
| StepExecutionStatus | The execution status of an operation stage. |
| UserIdentity | Represents the identity of a user. |
| ValidationResponse | Represents the response for validation of an operation. |

### Environment

Object

Power Platform environment.

| Name | Type | Description |
| --- | --- | --- |
| dataverseOrganizationUrl | string | Dataverse organization URL of the environment. |
| displayName | string | Display name of the environment. |
| environmentId | string | The environment ID. |

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

### OperationExecutionResult

Object

The result of an environment lifecycle operation.

| Name | Type | Description |
| --- | --- | --- |
| endTime | string (date-time) | The end time of the operation. |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |
| name | string | The name of the operation. |
| operationId | string | The ID of the operation. |
| requestedBy | UserIdentity | Represents the identity of a user. |
| stageStatuses | StageStatus[] | Per-stage progress of the operation. |
| startTime | string (date-time) | The start time of the operation. |
| status | OperationStatus | The status of operation. |
| updatedEnvironment | Environment | Power Platform environment. |

### OperationStatus

Enumeration

The status of operation.

| Value | Description |
| --- | --- |
| Queued |  |
| InProgress |  |
| Succeeded |  |
| ValidationFailed |  |
| Failed |  |
| NoOperation |  |
| ValidationPassed |  |

### StageStatus

Object

The status of a single stage of an operation.

| Name | Type | Description |
| --- | --- | --- |
| endTime | string (date-time) | The end time of the stage. |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |
| name | string | The name of the stage. |
| startTime | string (date-time) | The start time of the stage. |
| status | StepExecutionStatus | The execution status of an operation stage. |

### StepExecutionStatus

Enumeration

The execution status of an operation stage.

| Value | Description |
| --- | --- |
| Succeeded |  |
| Failed |  |
| Skipped |  |
| Postponed |  |
| InProgress |  |
| NotStarted |  |

### UserIdentity

Object

Represents the identity of a user.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | The display name of the user. |
| tenantId | string | The tenant ID of the user. |
| type | string | The type of the user identity (for example, User). |
| userId | string | The ID of the user. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |