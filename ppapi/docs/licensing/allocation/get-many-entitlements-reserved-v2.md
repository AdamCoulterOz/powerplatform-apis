---
layout: Reference
title: Allocation - Get Many Entitlements Reserved V2 - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/allocation/get-many-entitlements-reserved-v2
uid: api.powerplatform.com.power-platform.licensing.allocation.getmanyentitlementsreservedv2
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
description: 'Learn more about Power Platform API service - Get the reserved entitlements for the scope. '
locale: en-us
document_id: 9de948be-0209-93d5-e33c-06a543b7eb05
document_version_independent_id: 6995b6ff-d121-b205-503d-a18129c78314
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Allocation/Get-Many-Entitlements-Reserved-V2.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/allocation/get-many-entitlements-reserved-v2
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Allocation/Get-Many-Entitlements-Reserved-V2.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 52e88fe2-704b-0953-4410-5cb8d28e75ab
---

# Allocation - Get Many Entitlements Reserved V2

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the reserved entitlements for the scope.

```http
GET https://api.powerplatform.com/licensing/allocationsV2/entitlements/reserved?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/allocationsV2/entitlements/reserved?$filter={$filter}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $filter | query |  | string | OData filter expression. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EntitlementReservedResponseModel[] | Success |
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
| EntitlementReservedResponseModel | The reserved allocation for an entitlement within a scope. |
| EntitlementUnit | The unit of measure for an entitlement. |
| ReservedModel | The reserved quantity and unit for an entitlement. |

### EntitlementReservedResponseModel

Object

The reserved allocation for an entitlement within a scope.

| Name | Type | Description |
| --- | --- | --- |
| entitlementId | string |  |
| reserved | ReservedModel | The reserved quantity and unit for an entitlement. |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### ReservedModel

Object

The reserved quantity and unit for an entitlement.

| Name | Type | Description |
| --- | --- | --- |
| quantity | number (double) |  |
| unit | EntitlementUnit | The unit of measure for an entitlement. |