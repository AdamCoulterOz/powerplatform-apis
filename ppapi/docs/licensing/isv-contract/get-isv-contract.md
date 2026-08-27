---
layout: Reference
title: ISV Contract - Get ISV Contract - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/isv-contract/get-isv-contract
uid: api.powerplatform.com.power-platform.licensing.isvcontract.getisvcontract
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
description: 'Learn more about Power Platform API service - Get an ISV contract by its identifier (ID). '
locale: en-us
document_id: 2826547f-3aab-2cee-c532-32ce59128e71
document_version_independent_id: d628a6df-d5f9-70bc-9fd6-3d66007063a5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Isv-Contract/Get-ISV-Contract.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/isv-contract/get-isv-contract
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Isv-Contract/Get-ISV-Contract.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 9f6a2371-5a0f-fc0e-68ed-2df66fe19302
---

# ISV Contract - Get ISV Contract

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get an ISV contract by its identifier (ID).

```http
GET https://api.powerplatform.com/licensing/isvContracts/{isvContractId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| isvContractId | path | True | string | The ISV contract ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | IsvContractResponseModel | Success |
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
| BillingPolicyConditionsApiFilterModel | The Power Platform connector filter. |
| BillingPolicyConditionsApiModel |  |
| BillingPolicyConditionsModel | The ISV Contract API filter conditions. |
| BillingPolicyStatus | The desired ISV contract status. |
| ConsumerIdentityModel | The consumer identity for ISV contract. |
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