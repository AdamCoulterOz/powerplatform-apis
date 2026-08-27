---
layout: Reference
title: ISV Contract - Create ISV Contract - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/isv-contract/create-isv-contract
uid: api.powerplatform.com.power-platform.licensing.isvcontract.createisvcontract
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
description: 'Learn more about Power Platform API service - Create an ISV contract. '
locale: en-us
document_id: e595203b-f76f-2baf-17dc-6e5a82fa7c48
document_version_independent_id: d188721d-7547-1e12-2595-164405931ae1
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Isv-Contract/Create-ISV-Contract.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/isv-contract/create-isv-contract
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Isv-Contract/Create-ISV-Contract.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/54918a83-0404-4863-9c91-715186c1f582
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/b26f5f7a-0913-4a95-8337-ed7543902f2d
platformId: 4d2155bb-83e6-1329-9dfd-a3287fe18953
---

# ISV Contract - Create ISV Contract

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create an ISV contract.

```http
POST https://api.powerplatform.com/licensing/isvContracts?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| billingInstrument | True | BillingInstrumentModel | The ISV billing instrument information. |
| conditions | True | BillingPolicyConditionsModel | The ISV Contract API filter conditions. |
| consumer | True | ConsumerIdentityModel | The consumer identity for ISV contract. |
| geo | True | Geo[] | Resource location for billing account creation. Immutable. |
| name | True | string <br>minLength: 10maxLength: 64pattern: /^[a-zA-Z\d]+$/ |  |
| powerAutomatePolicy | True | PowerAutomatePolicyModel | The Power Platform requests policies. |
| status | True | BillingPolicyStatus | The desired ISV contract status. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 201 Created | IsvContractResponseModel | Success |
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
| BillingPolicyConditionsApiFilterModel | The Power Platform connector filter. |
| BillingPolicyConditionsApiModel |  |
| BillingPolicyConditionsModel | The ISV Contract API filter conditions. |
| BillingPolicyStatus | The desired ISV contract status. |
| ConsumerIdentityModel | The consumer identity for ISV contract. |
| IsvContractPostRequestModel | The ISV contract model for update operations. |
| IsvContractResponseModel |  |
| LicensingPrincipal |  |
| PayAsYouGoState |  |
| PowerAutomatePolicyModel | The Power Platform requests policies. |
| PrincipalType |  |

### BillingInstrumentModel

Object

The ISV billing instrument information.

| Name | Type | Description |
| --- | --- | --- |
| id | string |  |
| resourceGroup | string | The resource group within the tenant subscription. |
| subscriptionId | string (uuid) | The tenant subscription ID. |

### BillingPolicyConditionsApiFilterModel

Object

The Power Platform connector filter.

| Name | Type | Description |
| --- | --- | --- |
| allowOtherPremiumConnectors | boolean | Whether metered usage with premium connectors may be attributed. |
| requiredApis | BillingPolicyConditionsApiModel[] | Connectors where at least one must be in the metered usage. |

### BillingPolicyConditionsApiModel

Object

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of an API connector. |

### BillingPolicyConditionsModel

Object

The ISV Contract API filter conditions.

| Name | Type | Description |
| --- | --- | --- |
| apiFilter | BillingPolicyConditionsApiFilterModel | The Power Platform connector filter. |

### BillingPolicyStatus

Enumeration

The desired ISV contract status.

| Value | Description |
| --- | --- |
| Enabled |  |
| Disabled |  |

### ConsumerIdentityModel

Object

The consumer identity for ISV contract.

| Name | Type | Description |
| --- | --- | --- |
| tenantId | string (uuid) | The ID of the customer tenant. |

### IsvContractPostRequestModel

Object

The ISV contract model for update operations.

| Name | Type | Description |
| --- | --- | --- |
| billingInstrument | BillingInstrumentModel | The ISV billing instrument information. |
| conditions | BillingPolicyConditionsModel | The ISV Contract API filter conditions. |
| consumer | ConsumerIdentityModel | The consumer identity for ISV contract. |
| geo | Geo[] | Resource location for billing account creation. Immutable. |
| name | string <br>minLength: 10maxLength: 64pattern: /^[a-zA-Z\d]+$/ |  |
| powerAutomatePolicy | PowerAutomatePolicyModel | The Power Platform requests policies. |
| status | BillingPolicyStatus | The desired ISV contract status. |

### IsvContractResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| billingInstrument | BillingInstrumentModel | The ISV billing instrument information. |
| conditions | BillingPolicyConditionsModel | The ISV Contract API filter conditions. |
| consumer | ConsumerIdentityModel | The consumer identity for ISV contract. |
| createdBy | LicensingPrincipal |  |
| createdOn | string (date-time) |  |
| geo | string |  |
| id | string |  |
| lastModifiedBy | LicensingPrincipal |  |
| lastModifiedOn | string (date-time) |  |
| name | string |  |
| powerAutomatePolicy | PowerAutomatePolicyModel | The Power Platform requests policies. |
| status | BillingPolicyStatus | The desired ISV contract status. |

### LicensingPrincipal

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string |  |
| type | PrincipalType |  |

### PayAsYouGoState

Enumeration

| Value | Description |
| --- | --- |
| Enabled |  |
| Disabled |  |

### PowerAutomatePolicyModel

Object

The Power Platform requests policies.

| Name | Type | Description |
| --- | --- | --- |
| cloudFlowRunsPayAsYouGoState | PayAsYouGoState |  |
| desktopFlowAttendedRunsPayAsYouGoState | PayAsYouGoState |  |
| desktopFlowUnattendedRunsPayAsYouGoState | PayAsYouGoState |  |

### PrincipalType

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Application |  |
| User |  |
| DelegatedAdmin |  |