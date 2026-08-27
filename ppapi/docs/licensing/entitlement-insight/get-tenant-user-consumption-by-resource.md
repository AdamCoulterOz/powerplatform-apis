---
layout: Reference
title: Entitlement Insight - Get Tenant User Consumption By Resource - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement-insight/get-tenant-user-consumption-by-resource
uid: api.powerplatform.com.power-platform.licensing.entitlementinsight.gettenantuserconsumptionbyresource
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
description: 'Learn more about Power Platform API service - Get tenant user consumption by entitlement and resource ID. '
locale: en-us
document_id: 69eefb15-0966-2758-67e0-b5a9a0f1f7fb
document_version_independent_id: 197cefd7-dc99-b0b8-1334-4f6a31cfafd5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-User-Consumption-By-Resource.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement-insight/get-tenant-user-consumption-by-resource
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-User-Consumption-By-Resource.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: adca38c1-239d-f22f-2951-0a81cec9e832
---

# Entitlement Insight - Get Tenant User Consumption By Resource

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get tenant user consumption by entitlement and resource ID.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/resources/{resourceId}/users?fromDate={fromDate}&toDate={toDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/resources/{resourceId}/users?fromDate={fromDate}&toDate={toDate}&pageSize={pageSize}&searchRequest={searchRequest}&continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| resourceId | path | True | string | The resource ID. |
| api-version | query | True | string | The API version. |
| fromDate | query | True | string | The start date (inclusive) of the query range. |
| toDate | query | True | string | The end date (inclusive) of the query range. |
| continuationToken | query |  | string | Continuation token for pagination. |
| pageSize | query |  | integer (int32) | The page size for pagination. |
| searchRequest | query |  | string | Search request for filtering. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantUserResponseModelPagedResponse | Success |
| 204 No Content |  | No Content |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |

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
| TenantCapacityConsumptionUserSnapshotResponseModel |  |
| TenantUserResponseModel |  |
| TenantUserResponseModelPagedResponse | A paged response with a continuation token. |

### TenantCapacityConsumptionUserSnapshotResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| asOfDate | string (date-time) |  |
| consumed | number (double) |  |
| environmentId | string |  |
| metadata | object |  |
| tenantId | string |  |
| unit | string |  |
| userId | string |  |

### TenantUserResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| users | TenantCapacityConsumptionUserSnapshotResponseModel[] | The list of users associated with the tenant. |

### TenantUserResponseModelPagedResponse

Object

A paged response with a continuation token.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) |  |
| @odata.nextLink | string |  |
| continuationtoken | string |  |
| value | TenantUserResponseModel[] |  |