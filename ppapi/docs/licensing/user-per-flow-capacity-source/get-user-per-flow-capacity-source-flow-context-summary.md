---
layout: Reference
title: User Per Flow Capacity Source - Get User Per Flow Capacity Source Flow Context Summary - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-flow-context-summary
uid: api.powerplatform.com.power-platform.licensing.userperflowcapacitysource.getuserperflowcapacitysourceflowcontextsummary
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
description: 'Learn more about Power Platform API service - Get flow context summary for user per flow capacity source. '
locale: en-us
document_id: 8701000d-04d1-5e69-5379-c4f8a3478823
document_version_independent_id: 011ce958-2026-5f0e-d31b-63f42e91e4cb
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-Flow-Context-Summary.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-flow-context-summary
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-Flow-Context-Summary.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
platformId: b08318cf-d0be-2ab8-491d-e68f4d3eb013
---

# User Per Flow Capacity Source - Get User Per Flow Capacity Source Flow Context Summary

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get flow context summary for user per flow capacity source.

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/FlowContextSummary?startDate={startDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/FlowContextSummary?startDate={startDate}&endDate={endDate}&pageNumber={pageNumber}&pageSize={pageSize}&environmentId={environmentId}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| startDate | query | True | string (date-time) | The start date for the query range. |
| endDate | query |  | string (date-time) | The end date for the query range. Defaults to current UTC time if not provided. |
| environmentId | query |  | string (uuid) | Filter by environment identifier. |
| pageNumber | query |  | integer (int32) | The page number for pagination. |
| pageSize | query |  | integer (int32) | The page size for pagination. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceFlowContextRecord | Success |
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
| PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceFlowContextRecord | Paginated result container for flow context summary records. |
| UserPerFlowCapacitySourceFlowContextRecord | Flow context summary for per flow capacity source. |

### PowerPlatformRequestSnapshotResultWithoutPagesUserPerFlowCapacitySourceFlowContextRecord

Object

Paginated result container for flow context summary records.

| Name | Type | Description |
| --- | --- | --- |
| currentPage | integer (int32) | The current page number. |
| records | UserPerFlowCapacitySourceFlowContextRecord[] | Collection of flow context summary records. |

### UserPerFlowCapacitySourceFlowContextRecord

Object

Flow context summary for per flow capacity source.

| Name | Type | Description |
| --- | --- | --- |
| consumptionDate | string (date-time) | The date of consumption. |
| environmentId | string (uuid) | The environment identifier. |
| flowContext | string | The context in which the flow was executed. |
| flowId | string | The flow identifier. |
| flowLicenseCategorization | string | The license categorization of the flow. |
| tenantId | string (uuid) | The tenant identifier. |
| totalConsumption | integer (int64) | The total consumption units for the flow. |
| userId | string | The user identifier. |