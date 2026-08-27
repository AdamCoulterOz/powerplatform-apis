---
layout: Reference
title: Entitlement - Get Entitlement - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement/get-entitlement
uid: api.powerplatform.com.power-platform.licensing.entitlement.getentitlement
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
description: 'Learn more about Power Platform API service - Get the entitlement details for the tenant. '
locale: en-us
document_id: f387dcd6-c459-1a98-aea7-f9e4d5d2c16f
document_version_independent_id: 89d354bc-aef4-adff-b56f-9b622cdf46a8
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement/Get-Entitlement.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement/get-entitlement
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement/Get-Entitlement.yml
platformId: 0bf561c3-a1a3-e44d-8e50-ac9cf8419d81
---

# Entitlement - Get Entitlement

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the entitlement details for the tenant.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantEntitlementResponseModel | Success |
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
| CapacityEntitlementModel |  |
| CapacityLicenseModel |  |
| CatalogPayGoEntitlementModel |  |
| EntitlementAllocationModelV2 |  |
| EntitlementConsumedModel |  |
| EntitlementConsumptionType | The consumption type for an entitlement. |
| EntitlementEntitledModel |  |
| EntitlementUnit | The unit of measure for an entitlement. |
| LicensedPolicyModel |  |
| LicenseSource | The source of a license. |
| LicenseTier | The tier of a license. |
| OverageStatus | The overage status of an entitled capacity. |
| ProductCategory | The product category associated with an entitlement. |
| TenantEntitlementDetailServiceModel |  |
| TenantEntitlementResponseModel | Represents an entitlement and its capacity, pay-as-you-go and licensed policy details for a tenant. |

### CapacityEntitlementModel

Object

| Name | Type | Description |
| --- | --- | --- |
| allocated | EntitlementAllocationModelV2 |  |
| availableQuantity | number (double) |  |
| consumed | EntitlementConsumedModel |  |
| entitled | EntitlementEntitledModel |  |
| licenses | CapacityLicenseModel[] |  |
| status | OverageStatus | The overage status of an entitled capacity. |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### CapacityLicenseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| entitled | EntitlementEntitledModel |  |
| isUnlimited | boolean |  |
| licenseId | string |  |
| licenseQuantity | integer (int32) |  |
| licenseSource | LicenseSource | The source of a license. |
| licenseStatus | string |  |
| licenseTier | LicenseTier | The tier of a license. |
| nextLifecycleDate | string (date-time) |  |
| nextLifecycleStatus | string |  |
| productName | string |  |
| skuId | string |  |

### CatalogPayGoEntitlementModel

Object

| Name | Type | Description |
| --- | --- | --- |
| consumed | EntitlementConsumedModel |  |
| entitled | EntitlementEntitledModel |  |

### EntitlementAllocationModelV2

Object

| Name | Type | Description |
| --- | --- | --- |
| autoAllocated | number (double) |  |
| value | number (double) |  |

### EntitlementConsumedModel

Object

| Name | Type | Description |
| --- | --- | --- |
| consumptionType | EntitlementConsumptionType | The consumption type for an entitlement. |
| lastUpdatedOn | string (date-time) |  |
| value | number (double) |  |
| writeOff | number (double) |  |

### EntitlementConsumptionType

Enumeration

The consumption type for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Snapshot |  |
| MonthToDate |  |

### EntitlementEntitledModel

Object

| Name | Type | Description |
| --- | --- | --- |
| value | number (double) |  |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### LicensedPolicyModel

Object

| Name | Type | Description |
| --- | --- | --- |
| entitled | boolean |  |

### LicenseSource

Enumeration

The source of a license.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| CommerceService |  |
| AppSource |  |
| Internal |  |
| PayAsYouGo |  |

### LicenseTier

Enumeration

The tier of a license.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Paid |  |
| Trial |  |
| Internal |  |

### OverageStatus

Enumeration

The overage status of an entitled capacity.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| WithinCapacity |  |
| Overage |  |
| CoveredOverage |  |

### ProductCategory

Enumeration

The product category associated with an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| D365Apps |  |
| Dataverse |  |
| Fno |  |
| PowerApps |  |
| PowerAutomate |  |
| PowerPages |  |
| PowerVirtualAgent |  |
| CopilotStudio |  |
| PowerPlatform |  |
| Project |  |
| W365 |  |
| D365CustomerInsights |  |
| D365ContactCenter |  |
| Teams |  |
| CloudForSustainability |  |
| CoWork |  |
| M365 |  |
| ManagedApps |  |

### TenantEntitlementDetailServiceModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacity | CapacityEntitlementModel |  |
| licensedPolicy | LicensedPolicyModel |  |
| payGo | CatalogPayGoEntitlementModel |  |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### TenantEntitlementResponseModel

Object

Represents an entitlement and its capacity, pay-as-you-go and licensed policy details for a tenant.

| Name | Type | Description |
| --- | --- | --- |
| entitlement | TenantEntitlementDetailServiceModel |  |
| entitlementId | string | The entitlement ID. |
| productCategories | ProductCategory[] | The entitlement product categories (e.g., D365Apps, Dataverse, Power Apps, Power Automate). |