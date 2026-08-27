---
layout: Reference
title: Temporary Currency Entitlement - Retrieve Temporary Currency Entitlement Count - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/temporary-currency-entitlement/retrieve-temporary-currency-entitlement-count
uid: api.powerplatform.com.power-platform.licensing.temporarycurrencyentitlement.retrievetemporarycurrencyentitlementcount
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
description: 'Learn more about Power Platform API service - Get the temporary currency count and limit for the month by type. '
locale: en-us
document_id: 21987174-75bb-925a-f332-eb7bfa94bc04
document_version_independent_id: 576a3876-ef1a-5607-9e10-1fd542d8f777
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Temporary-Currency-Entitlement/Retrieve-Temporary-Currency-Entitlement-Count.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/temporary-currency-entitlement/retrieve-temporary-currency-entitlement-count
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Temporary-Currency-Entitlement/Retrieve-Temporary-Currency-Entitlement-Count.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 2ce25515-c688-ffb3-ad4d-99d3da164885
---

# Temporary Currency Entitlement - Retrieve Temporary Currency Entitlement Count

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the temporary currency count and limit for the month by type.

```http
POST https://api.powerplatform.com/licensing/TemporaryCurrencyEntitlement/{currencyType}/Count?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| currencyType | path | True | string | The currency type. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | GetTemporaryCurrencyEntitlementCountResponseModel | Success |
| 400 Bad Request | NeptuneValidationError[] | Bad Request |
| 500 Internal Server Error |  | Internal Server Error |

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
| GetTemporaryCurrencyEntitlementCountResponseModel |  |
| IErrorDetail |  |
| NeptuneValidationError |  |
| NeptuneValidationErrorMessage |  |

### GetTemporaryCurrencyEntitlementCountResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| entitledQuantity | integer (int64) |  |
| temporaryCurrencyEntitlementCount | integer (int32) |  |
| temporaryCurrencyEntitlementsAllowedPerMonth | integer (int32) |  |

### IErrorDetail

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| message | string |  |
| target | string |  |

### NeptuneValidationError

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| details | IErrorDetail[] |  |
| errorMessage | NeptuneValidationErrorMessage |  |
| key | string |  |
| message | string |  |
| target | string |  |

### NeptuneValidationErrorMessage

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| helpLink | string |  |
| message | string |  |
| operationCode | string |  |
| target | string |  |