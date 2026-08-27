---
layout: Reference
title: Allocation - Put Allocations V2 - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/allocation/put-allocations-v2
uid: api.powerplatform.com.power-platform.licensing.allocation.putallocationsv2
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
description: 'Learn more about Power Platform API service - Set the allocations for the scope. '
locale: en-us
document_id: bb27e7a0-8d20-d036-b50a-4e722e2ea8a4
document_version_independent_id: 91eef067-8ffa-75dd-2647-f27088eb4082
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Allocation/Put-Allocations-V2.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/allocation/put-allocations-v2
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Allocation/Put-Allocations-V2.yml
platformId: fc29988b-3f15-949d-076a-ea6533a2eee7
---

# Allocation - Put Allocations V2

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Set the allocations for the scope.

```http
PUT https://api.powerplatform.com/licensing/allocationsV2?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| allocatedEntitlements | EntitlementAllocationModel[] | Allocated entitlements. |
| scope | ScopeModel |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | NeptuneOperationResult | Success |
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
| AllocationEnforcementRule |  |
| AllocationEnforcementRuleTypes | The type of an allocation enforcement rule. |
| AllocationModel |  |
| AllocationPutRequestModel | Allocation put request model. |
| EntitlementAllocationModel |  |
| EntitlementUnit | The unit of measure for an entitlement. |
| NeptuneOperationResult | The result of a Neptune operation. |
| ScopeModel |  |

### AllocationEnforcementRule

Object

| Name | Type | Description |
| --- | --- | --- |
| enabled | boolean |  |
| ruleType | AllocationEnforcementRuleTypes | The type of an allocation enforcement rule. |

### AllocationEnforcementRuleTypes

Enumeration

The type of an allocation enforcement rule.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Alert |  |
| PayGo |  |
| TenantPool |  |
| Deny |  |
| Throttle |  |

### AllocationModel

Object

| Name | Type | Description |
| --- | --- | --- |
| autoAllocated | number (double) |  |
| quantity | number (double) |  |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### AllocationPutRequestModel

Object

Allocation put request model.

| Name | Type | Description |
| --- | --- | --- |
| allocatedEntitlements | EntitlementAllocationModel[] | Allocated entitlements. |
| scope | ScopeModel |  |

### EntitlementAllocationModel

Object

| Name | Type | Description |
| --- | --- | --- |
| allocation | AllocationModel |  |
| enforcementRules | AllocationEnforcementRule[] |  |
| entitlementId | string |  |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### NeptuneOperationResult

Object

The result of a Neptune operation.

| Name | Type | Description |
| --- | --- | --- |
| isErrorResult | boolean | Indicates whether the operation result represents an error. |
| statusCode | integer (int32) | The HTTP status code of the operation result. |

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