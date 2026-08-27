---
layout: Reference
title: User Per Flow Capacity Source - Get User Per Flow Capacity Source User Context Summary For User Id - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-user-context-summary-for-user-id
uid: api.powerplatform.com.power-platform.licensing.userperflowcapacitysource.getuserperflowcapacitysourceusercontextsummaryforuserid
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
description: "Learn more about Power Platform API service - Get user context summary for a specific user's per flow capacity source. "
locale: en-us
document_id: 0529dfae-37fa-7892-fd0d-890dd72dd99b
document_version_independent_id: f6e25fe3-df9c-fc27-e9a3-9017ed431992
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-User-Context-Summary-For-User-Id.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-user-context-summary-for-user-id
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-User-Context-Summary-For-User-Id.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0fd47fb9-88df-b54e-69f1-4b0767b2c230
---

# User Per Flow Capacity Source - Get User Per Flow Capacity Source User Context Summary For User Id

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get user context summary for a specific user's per flow capacity source.

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/UserContextSummary/{userId}?startDate={startDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/UserContextSummary/{userId}?startDate={startDate}&endDate={endDate}&pageNumber={pageNumber}&pageSize={pageSize}&environmentId={environmentId}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| userId | path | True | string (uuid) | The user identifier. |
| api-version | query | True | string | The API version. |
| startDate | query | True | string (date-time) | The start date for the query range. |
| endDate | query |  | string (date-time) | The end date for the query range. Defaults to current UTC time if not provided. |
| environmentId | query |  | string (uuid) | Filter by environment identifier. |
| pageNumber | query |  | integer (int32) | The page number for pagination. |
| pageSize | query |  | integer (int32) | The page size for pagination. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceUserContextRecord | Success |
| 204 No Content |  | No Content |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |
| 500 Internal Server Error |  | Internal Server Error |

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
| PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceUserContextRecord | Paginated result container for user context summary records. |
| UserPerFlowCapacitySourceUserContextRecord | User context summary for per flow capacity source. |

### PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceUserContextRecord

Object

Paginated result container for user context summary records.

| Name | Type | Description |
| --- | --- | --- |
| currentPage | integer (int32) | The current page number. |
| records | UserPerFlowCapacitySourceUserContextRecord[] | Collection of user context summary records. |

### UserPerFlowCapacitySourceUserContextRecord

Object

User context summary for per flow capacity source.

| Name | Type | Description |
| --- | --- | --- |
| consumptionDate | string (date-time) | The date of consumption. |
| flowContext | string | The context in which flows were executed. |
| flowLicenseCategorization | string | The license categorization of the flows. |
| tenantId | string (uuid) | The tenant identifier. |
| totalCapacity | integer (int64) | The total capacity available for the user. |
| totalConsumption | integer (int64) | The total consumption units for the user. |
| totalFlows | integer (int64) | The total number of flows executed by the user. |
| userId | string | The user identifier. |