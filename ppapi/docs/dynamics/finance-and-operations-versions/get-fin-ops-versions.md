---
layout: Reference
title: Finance And Operations Versions - Get Fin Ops Versions - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/dynamics/finance-and-operations-versions/get-fin-ops-versions
uid: api.powerplatform.com.power-platform.dynamics.financeandoperationsversions.getfinopsversions
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
description: 'Get available Finance and Operations versions. Retrieves the list of Finance and Operations application versions available for an environment. '
locale: en-us
document_id: 7eaae03e-3dc2-5870-45ef-732cb73ec523
document_version_independent_id: fc89e546-9185-6e14-ec7b-a57eda4807be
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Versions/Get-Fin-Ops-Versions.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/dynamics/finance-and-operations-versions/get-fin-ops-versions
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Versions/Get-Fin-Ops-Versions.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/410e33a0-5420-48ba-a8e2-7fb3dc6a9163
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/437f62ae-23a5-4ffc-9ff2-ac42acc41d76
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 4a5aff7e-29a8-848b-fbbb-14faca54c3cb
---

# Finance And Operations Versions - Get Fin Ops Versions

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get available Finance and Operations versions. Retrieves the list of Finance and Operations application versions available for an environment.

```http
GET https://api.powerplatform.com/dynamics/environments/{environmentId}/finopsversions?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string (uuid) | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | FinOpsVersionsResponse | Successfully retrieved available Finance and Operations versions. |
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
| FinOpsAppVersion | A Finance and Operations application version. |
| FinOpsErrorResponse | Standard error response. |
| FinOpsVersionsResponse | Finance and Operations available versions response. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### FinOpsAppVersion

Object

A Finance and Operations application version.

| Name | Type | Description |
| --- | --- | --- |
| releaseStage | string | The release stage of the version. |
| version | string | The application version. |

### FinOpsErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### FinOpsVersionsResponse

Object

Finance and Operations available versions response.

| Name | Type | Description |
| --- | --- | --- |
| availableVersions | FinOpsAppVersion[] | The list of available Finance and Operations application versions. |