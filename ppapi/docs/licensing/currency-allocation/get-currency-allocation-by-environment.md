---
layout: Reference
title: Currency Allocation - Get Currency Allocation By Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/currency-allocation/get-currency-allocation-by-environment
uid: api.powerplatform.com.power-platform.licensing.currencyallocation.getcurrencyallocationbyenvironment
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
description: 'Learn more about Power Platform API service - Get currency allocations for the environment. '
locale: en-us
document_id: 64e923d8-0f6f-12c6-4236-ca75132f7983
document_version_independent_id: 8d088d1e-dda7-43ec-a4c5-e6357122ee79
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Currency-Allocation/Get-Currency-Allocation-By-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/currency-allocation/get-currency-allocation-by-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Currency-Allocation/Get-Currency-Allocation-By-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 608b3feb-b070-8b0e-f3da-ad626c67ac88
---

# Currency Allocation - Get Currency Allocation By Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get currency allocations for the environment.

```http
GET https://api.powerplatform.com/licensing/environments/{environmentId}/allocations?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AllocationsByEnvironmentResponseModelV1 | Success |
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
| AllocationsByEnvironmentResponseModelV1 | The response body includes environment ID and allocated currencies. |
| CurrencyAllocationResponseModelV1 |  |
| ExternalCurrencyType | Available currency type which can be allocated to environment. |

### AllocationsByEnvironmentResponseModelV1

Object

The response body includes environment ID and allocated currencies.

| Name | Type | Description |
| --- | --- | --- |
| currencyAllocations | CurrencyAllocationResponseModelV1[] | The collection of currencies with allocation count. |
| environmentId | string | The environment ID for which the currency has been allocated. |

### CurrencyAllocationResponseModelV1

Object

| Name | Type | Description |
| --- | --- | --- |
| allocated | integer (int32) | The allocated count of currency type |
| currencyType | ExternalCurrencyType | Available currency type which can be allocated to environment. |

### ExternalCurrencyType

Enumeration

Available currency type which can be allocated to environment.

| Value | Description |
| --- | --- |
| AI |  |
| AppPass |  |
| AppPassForTeams |  |
| Invoice |  |
| MCSSessions |  |
| MCSMessages |  |
| PAHostedRPA |  |
| PAUnattendedRPA |  |
| PerFlowPlan |  |
| PortalAddOns |  |
| PortalLogins |  |
| PortalViews |  |
| PowerPagesAuthenticated |  |
| PowerPagesAnonymous |  |
| PowerAutomatePerProcess |  |
| ProcessMiningDataStorage |  |
| SCMessages |  |
| VAConversations |  |