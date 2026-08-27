---
layout: Reference
title: Billing Policy - Update Billing Policy - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy/update-billing-policy
uid: api.powerplatform.com.power-platform.licensing.billingpolicy.updatebillingpolicy
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
description: 'Learn more about Power Platform API service - Updates the billing policy at tenant level. '
locale: en-us
document_id: d804991e-3e12-b4db-aa61-a7863099065a
document_version_independent_id: d9f5f354-6116-5866-b3ee-bc9c64a03d58
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy/Update-Billing-Policy.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy/update-billing-policy
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy/Update-Billing-Policy.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c50ad430-a3ac-9b98-9c11-d67e6c0bffda
---

# Billing Policy - Update Billing Policy

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Updates the billing policy at tenant level.

```http
PUT https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| billingPolicyId | path | True | string | The billing policy ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| name | string |  |
| status | BillingPolicyStatus | The desired ISV contract status. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BillingPolicyResponseModel | Success |
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
| BillingInstrumentModel | The ISV billing instrument information. |
| BillingPolicyPutRequestModel |  |
| BillingPolicyResponseModel |  |
| BillingPolicyStatus | The desired ISV contract status. |
| LicensingPrincipal |  |
| PrincipalType |  |

### BillingInstrumentModel

Object

The ISV billing instrument information.

| Name | Type | Description |
| --- | --- | --- |
| id | string |  |
| resourceGroup | string | The resource group within the tenant subscription. |
| subscriptionId | string (uuid) | The tenant subscription ID. |

### BillingPolicyPutRequestModel

Object

| Name | Type | Description |
| --- | --- | --- |
| name | string |  |
| status | BillingPolicyStatus | The desired ISV contract status. |

### BillingPolicyResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| billingInstrument | BillingInstrumentModel | The ISV billing instrument information. |
| createdBy | LicensingPrincipal |  |
| createdOn | string (date-time) |  |
| id | string |  |
| lastModifiedBy | LicensingPrincipal |  |
| lastModifiedOn | string (date-time) |  |
| location | string |  |
| name | string |  |
| status | BillingPolicyStatus | The desired ISV contract status. |

### BillingPolicyStatus

Enumeration

The desired ISV contract status.

| Value | Description |
| --- | --- |
| Enabled |  |
| Disabled |  |

### LicensingPrincipal

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string |  |
| type | PrincipalType |  |

### PrincipalType

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Application |  |
| User |  |
| DelegatedAdmin |  |