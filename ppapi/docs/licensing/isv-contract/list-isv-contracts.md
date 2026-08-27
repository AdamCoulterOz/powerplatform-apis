---
layout: Reference
title: ISV Contract - List ISV Contracts - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/isv-contract/list-isv-contracts
uid: api.powerplatform.com.power-platform.licensing.isvcontract.listisvcontracts
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
description: 'Learn more about Power Platform API service - Get the list of ISV contracts for the tenant. '
locale: en-us
document_id: cdd0a7ab-cea8-7f0f-b1a3-3852c3009e89
document_version_independent_id: b7c47dbc-7542-e393-bc61-bfc58248301e
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Isv-Contract/List-ISV-Contracts.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/isv-contract/list-isv-contracts
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Isv-Contract/List-ISV-Contracts.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: ee4ea370-0080-5048-c034-1ef4887ca270
---

# ISV Contract - List ISV Contracts

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the list of ISV contracts for the tenant.

```http
GET https://api.powerplatform.com/licensing/isvContracts?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/isvContracts?$top={$top}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $top | query |  | string | Top limit of results. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | IsvContractResponseModelResponseWithOdataContinuation | Success |
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
| IsvContractResponseModel |  |
| IsvContractResponseModelResponseWithOdataContinuation |  |
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

### IsvContractResponseModelResponseWithOdataContinuation

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | IsvContractResponseModel[] |  |

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