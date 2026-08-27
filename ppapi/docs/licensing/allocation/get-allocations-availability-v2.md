---
layout: Reference
title: Allocation - Get Allocations Availability V2 - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/allocation/get-allocations-availability-v2
uid: api.powerplatform.com.power-platform.licensing.allocation.getallocationsavailabilityv2
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
description: 'Learn more about Power Platform API service - Get the entitlements available to be allocated for the scope. '
locale: en-us
document_id: 1b84daab-08ff-9c84-5563-e929cd773eda
document_version_independent_id: 9cdd4fe0-25cd-eb20-1c79-57a70ab23773
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Allocation/Get-Allocations-Availability-V2.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/allocation/get-allocations-availability-v2
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Allocation/Get-Allocations-Availability-V2.yml
platformId: 956942d9-ce14-01d5-9469-3f315508b035
---

# Allocation - Get Allocations Availability V2

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the entitlements available to be allocated for the scope.

```http
GET https://api.powerplatform.com/licensing/allocationsV2/availability?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/allocationsV2/availability?$filter={$filter}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $filter | query |  | string | OData filter expression. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AllocationAvailabilityResponseModel | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |

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
| AllocationAvailabilityResponseModel | Allocation availability response model. |
| EntitlementAllocationAvailabilityModel |  |
| EntitlementUnit | The unit of measure for an entitlement. |
| ScopeModel |  |

### AllocationAvailabilityResponseModel

Object

Allocation availability response model.

| Name | Type | Description |
| --- | --- | --- |
| entitlementAllocationsAvailable | EntitlementAllocationAvailabilityModel[] | Availability of the entitlements for the scope. |
| scope | ScopeModel |  |

### EntitlementAllocationAvailabilityModel

Object

| Name | Type | Description |
| --- | --- | --- |
| availableQuantity | number (double) |  |
| entitlementId | string |  |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### ScopeModel

Object

| Name | Type | Description |
| --- | --- | --- |
| environmentGroupId | string |  |
| environmentId | string |  |
| resourceId | string |  |
| tenantId | string |  |
| userGroupId | string |  |
| userId | string |  |