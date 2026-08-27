---
layout: Reference
title: User Per Flow Capacity Source - Get User Per Flow Capacity Source Tenant Context Summary - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-tenant-context-summary
uid: api.powerplatform.com.power-platform.licensing.userperflowcapacitysource.getuserperflowcapacitysourcetenantcontextsummary
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
description: 'Learn more about Power Platform API service - Get tenant context summary for user per flow capacity source. '
locale: en-us
document_id: a0a915e3-3147-964a-b71a-8998ca615fb9
document_version_independent_id: f6122109-52f9-974d-d621-4966d09a71c5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-Tenant-Context-Summary.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/user-per-flow-capacity-source/get-user-per-flow-capacity-source-tenant-context-summary
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/User-Per-Flow-Capacity-Source/Get-User-Per-Flow-Capacity-Source-Tenant-Context-Summary.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 854e2f3c-e242-ae43-964d-4b473ddee7ab
---

# User Per Flow Capacity Source - Get User Per Flow Capacity Source Tenant Context Summary

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get tenant context summary for user per flow capacity source.

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/TenantContextSummary?startDate={startDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/UserPerFlowCapacitySource/TenantContextSummary?startDate={startDate}&endDate={endDate}&environmentId={environmentId}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| startDate | query | True | string (date-time) | The start date for the query range. |
| endDate | query |  | string (date-time) | The end date for the query range. Defaults to current UTC time if not provided. |
| environmentId | query |  | string (uuid) | Filter by environment identifier. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | UserPerFlowCapacitySourceTenantContextSummaryRecord[] | Success |
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

### UserPerFlowCapacitySourceTenantContextSummaryRecord

Object

Tenant-level context summary for per flow capacity source.

| Name | Type | Description |
| --- | --- | --- |
| countOfUsersExceedingCapacity | integer (int64) | Number of users who have exceeded their capacity limits. |
| countOfUsersInCompliance | integer (int64) | Number of users who are within their capacity limits. |
| countOfUsersWithoutALicense | integer (int64) | Number of users without any license. |
| countOfUsersWithoutPremiumLicenseUsingPremiumFeatures | integer (int64) | Number of users using premium features without a premium license. |
| flowContext | string | The context in which flows were executed. |
| tenantId | string (uuid) | The tenant identifier. |