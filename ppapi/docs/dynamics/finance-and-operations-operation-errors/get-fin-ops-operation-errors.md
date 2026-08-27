---
layout: Reference
title: Finance And Operations Operation Errors - Get Fin Ops Operation Errors - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/dynamics/finance-and-operations-operation-errors/get-fin-ops-operation-errors
uid: api.powerplatform.com.power-platform.dynamics.financeandoperationsoperationerrors.getfinopsoperationerrors
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
description: 'Get Finance and Operations operation errors. Retrieves recent operation errors for a Finance and Operations environment. '
locale: en-us
document_id: b78a5dae-d571-d810-20b7-44f99b72b2c4
document_version_independent_id: 411391b8-6681-124c-c4b4-085942ecb760
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Operation-Errors/Get-Fin-Ops-Operation-Errors.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/dynamics/finance-and-operations-operation-errors/get-fin-ops-operation-errors
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Operation-Errors/Get-Fin-Ops-Operation-Errors.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/410e33a0-5420-48ba-a8e2-7fb3dc6a9163
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/437f62ae-23a5-4ffc-9ff2-ac42acc41d76
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5a9559d0-6b78-e763-84e1-7013572dfab0
---

# Finance And Operations Operation Errors - Get Fin Ops Operation Errors

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get Finance and Operations operation errors. Retrieves recent operation errors for a Finance and Operations environment.

```http
GET https://api.powerplatform.com/dynamics/environments/{environmentId}/operationerrors?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/dynamics/environments/{environmentId}/operationerrors?maxResults={maxResults}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string (uuid) | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |
| maxResults | query |  | integer (int32) | The maximum number of operation errors to return. Defaults to twenty (20) and is capped at one thousand (1000). |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | OperationErrorsResponse | Successfully retrieved Finance and Operations operation errors. |
| 400 Bad Request | FinOpsErrorResponse | Bad Request. |
| 401 Unauthorized | FinOpsErrorResponse | Unauthorized. |
| 403 Forbidden | FinOpsErrorResponse | Forbidden. |
| 404 Not Found | FinOpsErrorResponse | Not Found. |
| 500 Internal Server Error | FinOpsErrorResponse | Internal Server Error. |

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
| Error |  |
| FinOpsErrorResponse | Standard error response. |
| OperationErrorItem | A single Finance and Operations operation error. |
| OperationErrorsResponse | Response containing operation errors for an environment. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### FinOpsErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### OperationErrorItem

Object

A single Finance and Operations operation error.

| Name | Type | Description |
| --- | --- | --- |
| correlationId | string | The correlation ID. |
| errorCode | string | The error code. |
| errorMessage | string | The customer-friendly error message. |
| failedActionName | string | The name of the failed action. |
| failedAt | string (date-time) | The timestamp when the operation failed. |
| operationType | string | The operation type. |

### OperationErrorsResponse

Object

Response containing operation errors for an environment.

| Name | Type | Description |
| --- | --- | --- |
| environmentId | string | The environment ID. |
| errors | OperationErrorItem[] | The list of operation errors. |