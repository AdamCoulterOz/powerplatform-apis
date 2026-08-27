---
layout: Reference
title: Billing Policy - List Billing Policies - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy/list-billing-policies
uid: api.powerplatform.com.power-platform.licensing.billingpolicy.listbillingpolicies
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
description: 'Learn more about Power Platform API service - Get the list of billing policies for the tenant. '
locale: en-us
document_id: cf7180f7-ea09-5e4f-0a2f-7a18d1cdfe8d
document_version_independent_id: 1494149d-6613-1ba5-f7ec-fa2da1de92aa
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy/List-Billing-Policies.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy/list-billing-policies
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy/List-Billing-Policies.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 970063cf-205c-7a83-da01-c9cdfc6733bd
---

# Billing Policy - List Billing Policies

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the list of billing policies for the tenant.

```http
GET https://api.powerplatform.com/licensing/billingPolicies?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/billingPolicies?$top={$top}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $top | query |  | string | The ISV contract ID. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BillingPolicyResponseModelResponseWithOdataContinuation | Success |
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
| BillingInstrumentModel | The ISV billing instrument information. |
| BillingPolicyResponseModel |  |
| BillingPolicyResponseModelResponseWithOdataContinuation |  |
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

### BillingPolicyResponseModelResponseWithOdataContinuation

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | BillingPolicyResponseModel[] |  |

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