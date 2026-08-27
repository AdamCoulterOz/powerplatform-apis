---
layout: Reference
title: Environment Billing Policy - Get Environment Billing Policy - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/environment-billing-policy/get-environment-billing-policy
uid: api.powerplatform.com.power-platform.licensing.environmentbillingpolicy.getenvironmentbillingpolicy
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
description: 'Learn more about Power Platform API service - Get the linked billing policy details for an environment. '
locale: en-us
document_id: 44f90323-6c89-f535-c904-48fa95f34e1f
document_version_independent_id: 6b5e864e-d2ee-6582-4c26-d563570fd0fd
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Environment-Billing-Policy/Get-Environment-Billing-Policy.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/environment-billing-policy/get-environment-billing-policy
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Environment-Billing-Policy/Get-Environment-Billing-Policy.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c2d5fc27-cb15-d97c-9e86-3ea9a3496dc9
---

# Environment Billing Policy - Get Environment Billing Policy

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the linked billing policy details for an environment.

```http
GET https://api.powerplatform.com/licensing/environments/{environmentId}/billingPolicy?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BillingPolicyResponseModel | Success |
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