---
layout: Reference
title: Entitlement Insight - Get Tenant Resource Consumption By User - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement-insight/get-tenant-resource-consumption-by-user
uid: api.powerplatform.com.power-platform.licensing.entitlementinsight.gettenantresourceconsumptionbyuser
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
description: 'Learn more about Power Platform API service - Get resource consumption by entitlement and user ID. '
locale: en-us
document_id: d77ac489-0ef0-085a-a504-6b1098afc83b
document_version_independent_id: 194cdc7f-2d44-6d1d-dfef-acd4d93cabca
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-Resource-Consumption-By-User.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement-insight/get-tenant-resource-consumption-by-user
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-Resource-Consumption-By-User.yml
platformId: 6f4fe493-f861-ae9c-febf-8809b0a77281
---

# Entitlement Insight - Get Tenant Resource Consumption By User

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get resource consumption by entitlement and user ID.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/users/{userId}/resources?fromDate={fromDate}&toDate={toDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/users/{userId}/resources?fromDate={fromDate}&toDate={toDate}&pageSize={pageSize}&searchRequest={searchRequest}&continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| userId | path | True | string | The user ID. |
| api-version | query | True | string | The API version. |
| fromDate | query | True | string | The start date (inclusive) of the query range. |
| toDate | query | True | string | The end date (inclusive) of the query range. |
| continuationToken | query |  | string | Continuation token for pagination. |
| pageSize | query |  | integer (int32) | The page size for pagination. |
| searchRequest | query |  | string | Search request for filtering. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantResourceResponseModelPagedResponse | Success |
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
| TenantCapacityConsumptionSnapshotResponseModel |  |
| TenantResourceResponseModel |  |
| TenantResourceResponseModelPagedResponse | A paged response with a continuation token. |

### TenantCapacityConsumptionSnapshotResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| asOfDate | string (date-time) |  |
| consumed | number (double) |  |
| environmentId | string |  |
| metadata | object |  |
| resourceId | string |  |
| tenantId | string |  |
| unit | string |  |

### TenantResourceResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| resources | TenantCapacityConsumptionSnapshotResponseModel[] | The list of resources associated with the tenant. |

### TenantResourceResponseModelPagedResponse

Object

A paged response with a continuation token.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) |  |
| @odata.nextLink | string |  |
| continuationtoken | string |  |
| value | TenantResourceResponseModel[] |  |