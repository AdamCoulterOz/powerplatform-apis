---
layout: Reference
title: Entitlement Insight - Get Tenant Resources Across Environments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement-insight/get-tenant-resources-across-environments
uid: api.powerplatform.com.power-platform.licensing.entitlementinsight.gettenantresourcesacrossenvironments
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
description: 'Learn more about Power Platform API service - Get tenant resources for an entitlement across all environments. '
locale: en-us
document_id: 4a10ebb1-9362-e71c-a0f5-01ed8c57ac76
document_version_independent_id: 589394c5-0a92-23e0-2862-ab4f9600da8a
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-Resources-Across-Environments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement-insight/get-tenant-resources-across-environments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-Resources-Across-Environments.yml
platformId: e1a492dd-28fd-b05e-58fd-c40d1c5a5803
---

# Entitlement Insight - Get Tenant Resources Across Environments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get tenant resources for an entitlement across all environments.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/resources?fromDate={fromDate}&toDate={toDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/resources?fromDate={fromDate}&toDate={toDate}&pageSize={pageSize}&continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| api-version | query | True | string | The API version. |
| fromDate | query | True | string | The start date (inclusive) of the query range. |
| toDate | query | True | string | The end date (inclusive) of the query range. |
| continuationToken | query |  | string | Opaque continuation token returned by the previous page, or null for the first page. |
| pageSize | query |  | integer (int32) | Maximum number of environments to fan out to per page. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantEnvironmentResourceSnapshotResponseModelPagedResponse | Success |
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
| EntitlementUnit | The unit of measure for an entitlement. |
| TenantEnvironmentResourceSnapshotResponseModel | Per-resource snapshot for a tenant-scoped, all-environments listing. |
| TenantEnvironmentResourceSnapshotResponseModelPagedResponse | A paged response with a continuation token. |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### TenantEnvironmentResourceSnapshotResponseModel

Object

Per-resource snapshot for a tenant-scoped, all-environments listing.

| Name | Type | Description |
| --- | --- | --- |
| consumed | number (double) | The consumed value. |
| environmentId | string | The environment this resource belongs to. |
| lastRefreshedDate | string (date-time) | The last refreshed date. |
| metadata | object | Additional metadata such as Feature, ProductName and nonBillableConsumed for MCSMessages. |
| resourceId | string | The resource ID. |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### TenantEnvironmentResourceSnapshotResponseModelPagedResponse

Object

A paged response with a continuation token.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) |  |
| @odata.nextLink | string |  |
| continuationtoken | string |  |
| value | TenantEnvironmentResourceSnapshotResponseModel[] | Per-resource snapshot for a tenant-scoped, all-environments listing. |