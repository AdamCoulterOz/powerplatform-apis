---
layout: Reference
title: User Per Flow Capacity Source - Get User Per Flow Capacity Source - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source
uid: api.powerplatform.com.power-platform.licensing.userperflowcapacitysource.getuserperflowcapacitysource
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
description: 'Learn more about Power Platform API service - Get user per flow capacity source data with pagination and filtering options. '
locale: en-us
document_id: ea602d77-673e-9242-9379-4c4b79e00b73
document_version_independent_id: beecfb31-02b7-f761-a68b-21a8c2fccb3a
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 78c25442-a129-b8c2-7edb-abee2cfe3877
---

# User Per Flow Capacity Source - Get User Per Flow Capacity Source

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get user per flow capacity source data with pagination and filtering options.

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource?startDate={startDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource?startDate={startDate}&endDate={endDate}&pageNumber={pageNumber}&pageSize={pageSize}&userId={userId}&flowContext={flowContext}&flowLicenseCategorization={flowLicenseCategorization}&resourceId={resourceId}&environmentId={environmentId}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| startDate | query | True | string (date-time) | The start date for the query range. |
| endDate | query |  | string (date-time) | The end date for the query range. Defaults to current UTC time if not provided. |
| environmentId | query |  | string (uuid) | Filter by environment identifier. |
| flowContext | query |  | string | Filter by flow context. |
| flowLicenseCategorization | query |  | string | Filter by flow license categorization. |
| pageNumber | query |  | integer (int32) | The page number for pagination. |
| pageSize | query |  | integer (int32) | The page size for pagination. |
| resourceId | query |  | string | Filter by resource identifier. |
| userId | query |  | string | Filter by user identifier. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceRecord | Success |
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
| PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceRecord | Paginated result container for user per flow capacity source records. |
| UserPerFlowCapacitySourceRecord | Detailed capacity source record for a specific flow execution. |

### PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceRecord

Object

Paginated result container for user per flow capacity source records.

| Name | Type | Description |
| --- | --- | --- |
| currentPage | integer (int32) | The current page number. |
| records | UserPerFlowCapacitySourceRecord[] | Collection of user per flow capacity source records. |

### UserPerFlowCapacitySourceRecord

Object

Detailed capacity source record for a specific flow execution.

| Name | Type | Description |
| --- | --- | --- |
| consumptionDate | string (date-time) | The date when the consumption occurred. |
| consumptionUnits | integer (int64) | The number of consumption units used. |
| environmentId | string (uuid) | The environment identifier. |
| flowContext | string | The context in which the flow was executed. |
| flowLicenseCategorization | string | The license categorization of the flow. |
| resourceId | string | The resource identifier. |
| tenantId | string (uuid) | The tenant identifier. |
| userId | string | The user identifier. |