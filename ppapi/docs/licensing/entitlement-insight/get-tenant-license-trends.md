---
layout: Reference
title: Entitlement Insight - Get Tenant License Trends - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement-insight/get-tenant-license-trends
uid: api.powerplatform.com.power-platform.licensing.entitlementinsight.gettenantlicensetrends
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
description: 'Learn more about Power Platform API service - Get the license trends for the tenant for the specified entitlement. '
locale: en-us
document_id: e2b01396-45d3-4dd7-3373-a6dc650abdee
document_version_independent_id: 50da1cf7-9dc8-7481-81ec-b2a759abed45
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-License-Trends.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement-insight/get-tenant-license-trends
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Tenant-License-Trends.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: efa9381a-e581-7f5e-2629-4ae4230e1dbf
---

# Entitlement Insight - Get Tenant License Trends

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the license trends for the tenant for the specified entitlement.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/licenses?fromDate={fromDate}&toDate={toDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/licenses?fromDate={fromDate}&toDate={toDate}&$top={$top}&$filter={$filter}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| api-version | query | True | string | The API version. |
| fromDate | query | True | string | The start date (inclusive) of the query range. |
| toDate | query | True | string | The end date (inclusive) of the query range. |
| $filter | query |  | string | OData filter expression. |
| $top | query |  | integer (int32) | The maximum number of records to return. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantEntitlementLicenseTrendResponseModelPagedResponse | Success |
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
| LicenseModelType | The license model type. |
| LicenseTier | The tier of a license. |
| TenantEntitlementLicenseModel |  |
| TenantEntitlementLicenseTrendResponseModel |  |
| TenantEntitlementLicenseTrendResponseModelPagedResponse | A paged response with a continuation token. |

### LicenseModelType

Enumeration

The license model type.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Usl |  |
| Capacity |  |
| PayGo |  |
| TenantLicense |  |

### LicenseTier

Enumeration

The tier of a license.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Paid |  |
| Trial |  |
| Internal |  |

### TenantEntitlementLicenseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| entitled | number (double) |  |
| licenseId | string |  |
| licenseQuantity | integer (int32) |  |
| licenseStatus | string |  |
| licenseTier | LicenseTier | The tier of a license. |
| productName | string |  |
| skuId | string |  |

### TenantEntitlementLicenseTrendResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| date | string (date-time) |  |
| licenseModelType | LicenseModelType | The license model type. |
| licenses | TenantEntitlementLicenseModel[] |  |

### TenantEntitlementLicenseTrendResponseModelPagedResponse

Object

A paged response with a continuation token.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) |  |
| @odata.nextLink | string |  |
| continuationtoken | string |  |
| value | TenantEntitlementLicenseTrendResponseModel[] |  |