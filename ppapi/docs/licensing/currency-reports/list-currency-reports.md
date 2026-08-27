---
layout: Reference
title: Currency Reports - List Currency Reports - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/currency-reports/list-currency-reports
uid: api.powerplatform.com.power-platform.licensing.currencyreports.listcurrencyreports
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
description: 'Learn more about Power Platform API service - Get the currency report for the tenant. '
locale: en-us
document_id: 9008efa1-ef5f-d9dd-e784-e6142e83c93f
document_version_independent_id: 6bda5c6d-1868-5751-2d69-6cfd8ef6a7ab
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Currency-Reports/List-Currency-Reports.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/currency-reports/list-currency-reports
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Currency-Reports/List-Currency-Reports.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 59e722c6-8233-3478-37fa-8a51bba9f04e
---

# Currency Reports - List Currency Reports

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the currency report for the tenant.

```http
GET https://api.powerplatform.com/licensing/tenantCapacity/currencyReports?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/tenantCapacity/currencyReports?includeAllocations={includeAllocations}&includeConsumptions={includeConsumptions}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| includeAllocations | query |  | boolean | Flag indicating to include allocations. |
| includeConsumptions | query |  | boolean | Flag indicating to include consumptions. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | CurrencyReportV2[] | Success |

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
| CurrencyConsumption |  |
| CurrencyReportV2 |  |
| ExternalCurrencyType | Available currency type which can be allocated to environment. |

### CurrencyConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| lastUpdatedDay | string (date-time) |  |
| unitsConsumed | integer (int64) |  |

### CurrencyReportV2

Object

| Name | Type | Description |
| --- | --- | --- |
| allocated | integer (int64) |  |
| consumed | CurrencyConsumption |  |
| currencyType | ExternalCurrencyType | Available currency type which can be allocated to environment. |
| purchased | integer (int64) |  |

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