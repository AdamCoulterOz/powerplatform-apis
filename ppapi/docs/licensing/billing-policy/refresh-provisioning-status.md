---
layout: Reference
title: Billing Policy - Refresh Provisioning Status - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy/refresh-provisioning-status
uid: api.powerplatform.com.power-platform.licensing.billingpolicy.refreshprovisioningstatus
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
description: 'Learn more about Power Platform API service - Refresh the billing policy provisioning status. '
locale: en-us
document_id: 0dcd5929-b26d-5cf3-f28d-6f64277480dc
document_version_independent_id: 922dff9d-2d09-4f92-70b6-d4bb31821545
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy/Refresh-Provisioning-Status.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy/refresh-provisioning-status
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy/Refresh-Provisioning-Status.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0c1eac64-ce1d-48d4-5f11-90309a8e02e3
---

# Billing Policy - Refresh Provisioning Status

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Refresh the billing policy provisioning status.

```http
POST https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}/refreshProvisioningStatus?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| billingPolicyId | path | True | string | The billing policy ID. |
| api-version | query | True | string | The API version. |

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