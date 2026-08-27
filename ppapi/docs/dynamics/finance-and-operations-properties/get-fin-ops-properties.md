---
layout: Reference
title: Finance And Operations Properties - Get Fin Ops Properties - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/dynamics/finance-and-operations-properties/get-fin-ops-properties
uid: api.powerplatform.com.power-platform.dynamics.financeandoperationsproperties.getfinopsproperties
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
description: Get Finance and Operations environment properties. Retrieves Finance and Operations environment properties such as AOS counts, deployment type, and demo dataset
locale: en-us
document_id: 02bc4d0a-78b8-5122-2867-177d85f61c33
document_version_independent_id: 3cdfe914-8608-597c-2000-4dd37c96c8d6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Properties/Get-Fin-Ops-Properties.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/dynamics/finance-and-operations-properties/get-fin-ops-properties
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Properties/Get-Fin-Ops-Properties.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/410e33a0-5420-48ba-a8e2-7fb3dc6a9163
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/437f62ae-23a5-4ffc-9ff2-ac42acc41d76
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: cccc0bd4-a7df-ab28-925c-689372743316
---

# Finance And Operations Properties - Get Fin Ops Properties

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get Finance and Operations environment properties. Retrieves Finance and Operations environment properties such as AOS counts, deployment type, and demo dataset.

```http
GET https://api.powerplatform.com/dynamics/environments/{environmentId}/finopsproperties?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string (uuid) | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | FinOpsPropertiesResponse | Successfully retrieved Finance and Operations properties. |
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
| FinOpsDeploymentCategory | The deployment category of a Finance and Operations environment. |
| FinOpsErrorResponse | Standard error response. |
| FinOpsPropertiesResponse | Finance and Operations environment properties response. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### FinOpsDeploymentCategory

Enumeration

The deployment category of a Finance and Operations environment.

| Value | Description |
| --- | --- |
| UnifiedDeveloper |  |
| UnifiedSandbox |  |
| UnifiedProduction |  |
| LCSSandbox |  |
| LCSProduction |  |
| Trial |  |
| Unknown |  |

### FinOpsErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### FinOpsPropertiesResponse

Object

Finance and Operations environment properties response.

| Name | Type | Description |
| --- | --- | --- |
| appId | string | The Finance and Operations environment ID (AppId). |
| demoDataset | string | The demo dataset name for the environment. |
| deploymentType | FinOpsDeploymentCategory | The deployment category of a Finance and Operations environment. |
| lastObservedAOSCount | integer (int32) | The last observed interactive AOS instance count. |
| lastObservedBatchAOSCount | integer (int32) | The last observed batch (non-interactive) AOS instance count. |
| maxAOSCount | string | The maximum number of interactive AOS instances configured for the environment. |
| maxBatchAOSCount | string | The maximum number of batch (non-interactive) AOS instances configured for the environment. |