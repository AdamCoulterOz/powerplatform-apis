---
layout: Reference
title: Operation - Get Operations For Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/operation/get-operations-for-environment
uid: api.powerplatform.com.power-platform.environmentmanagement.operation.getoperationsforenvironment
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
description: 'Gets the list of environment lifecycle operations for a specific environment. Lists the environment lifecycle operations for a specific environment. '
locale: en-us
document_id: f5ebe5ae-e72e-68ed-699a-6ca17492bc64
document_version_independent_id: 8a001f71-84a0-d809-5109-b72d98a1940f
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Operation/Get-Operations-For-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/operation/get-operations-for-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Operation/Get-Operations-For-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5914aebd-c36c-7419-4d92-dd07845803da
---

# Operation - Get Operations For Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of environment lifecycle operations for a specific environment. Lists the environment lifecycle operations for a specific environment.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/operations?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/operations?limit={limit}&continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment. |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | An opaque token returned by a previous response, used to fetch the next page of results. Omit to retrieve the first page. |
| limit | query |  | string | The maximum number of records to return per request. Must be a positive integer; a server default applies if omitted. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | OperationExecutionResultPagedCollection | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| OperationExecutionResultPagedCollection |  |
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

### OperationExecutionResultPagedCollection

Object

| Name | Type | Description |
| --- | --- | --- |
| collection | OperationExecutionResult[] | The result of an environment lifecycle operation. |
| continuationToken | string |  |

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