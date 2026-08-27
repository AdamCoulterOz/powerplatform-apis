---
layout: Reference
title: Fin Ops Licensing - Get Fin Ops License Summary V2 - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/fin-ops-licensing/get-fin-ops-license-summary-v2
uid: api.powerplatform.com.power-platform.licensing.finopslicensing.getfinopslicensesummaryv2
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
description: 'Learn more about Power Platform API service - Get FinOps license summary (V2) for the tenant. '
locale: en-us
document_id: ec31700e-f2ff-f5c8-3507-4e96ed0a31cd
document_version_independent_id: 30f34ba5-4ee7-dfd1-9548-3d8655482bbc
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Fin-Ops-Licensing/Get-Fin-Ops-License-Summary-V2.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/fin-ops-licensing/get-fin-ops-license-summary-v2
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Fin-Ops-Licensing/Get-Fin-Ops-License-Summary-V2.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 6327a799-3ff9-bef7-9c55-cb4b6365e159
---

# Fin Ops Licensing - Get Fin Ops License Summary V2

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get FinOps license summary (V2) for the tenant.

```http
GET https://api.powerplatform.com/licensing/FinOpsLicensing/GetLicenseSummaryV2?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | FinOpsLicenseSummaryV2Response | Success |
| 204 No Content |  | No Content |
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
| FinOpsAttachLicenseConsumption |  |
| FinOpsBaseLicenseConsumption |  |
| FinOpsLicenseRequirements |  |
| FinOpsLicensesConsumption |  |
| FinOpsLicenseSummaryV2Response |  |
| FinOpsOperationsLicenseConsumption |  |
| FinOpsProductLicenseConsumption |  |
| FinOpsProjectOperationsOrHumanResourcesLicenseConsumption |  |
| FinOpsSimpleLicenseConsumption |  |
| FinOpsSupplyChainManagementOrFinanceOrCommerceLicenseConsumption |  |

### FinOpsAttachLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| purchasedAttachAssignedCount | integer (int32) |  |
| purchasedAttachUnassignedCount | integer (int32) |  |

### FinOpsBaseLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| purchasedBaseAssignedCount | integer (int32) |  |
| purchasedBaseUnassignedCount | integer (int32) |  |

### FinOpsLicenseRequirements

Object

| Name | Type | Description |
| --- | --- | --- |
| usersNeedingLicenseCount | integer (int32) |  |

### FinOpsLicensesConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| activity | FinOpsSimpleLicenseConsumption |  |
| commerce | FinOpsProductLicenseConsumption |  |
| finance | FinOpsProductLicenseConsumption |  |
| humanResources | FinOpsProductLicenseConsumption |  |
| operations | FinOpsOperationsLicenseConsumption |  |
| projectOperations | FinOpsProductLicenseConsumption |  |
| projectOperationsOrHumanResources | FinOpsProjectOperationsOrHumanResourcesLicenseConsumption |  |
| selfService | FinOpsSimpleLicenseConsumption |  |
| supplyChainManagement | FinOpsProductLicenseConsumption |  |
| supplyChainManagementOrFinanceOrCommerce | FinOpsSupplyChainManagementOrFinanceOrCommerceLicenseConsumption |  |
| teamMember | FinOpsSimpleLicenseConsumption |  |

### FinOpsLicenseSummaryV2Response

Object

| Name | Type | Description |
| --- | --- | --- |
| allUsersCount | integer (int32) |  |
| lastReportRefreshTime | string (date-time) |  |
| licensesConsumption | FinOpsLicensesConsumption |  |
| overLicensedUsersCount | integer (int32) |  |
| tenantId | string |  |
| underLicensedUsersCount | integer (int32) |  |
| usersWithoutLicensesCount | integer (int32) |  |

### FinOpsOperationsLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| baseConsumption | FinOpsBaseLicenseConsumption |  |
| licenseRequirements | FinOpsLicenseRequirements |  |

### FinOpsProductLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| attachConsumption | FinOpsAttachLicenseConsumption |  |
| baseConsumption | FinOpsBaseLicenseConsumption |  |
| licenseRequirements | FinOpsLicenseRequirements |  |

### FinOpsProjectOperationsOrHumanResourcesLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| humanResourcesConsumption | FinOpsBaseLicenseConsumption |  |
| licenseRequirements | FinOpsLicenseRequirements |  |
| projectOperationsConsumption | FinOpsBaseLicenseConsumption |  |

### FinOpsSimpleLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| baseConsumption | FinOpsBaseLicenseConsumption |  |
| licenseRequirements | FinOpsLicenseRequirements |  |

### FinOpsSupplyChainManagementOrFinanceOrCommerceLicenseConsumption

Object

| Name | Type | Description |
| --- | --- | --- |
| commerceConsumption | FinOpsBaseLicenseConsumption |  |
| financeConsumption | FinOpsBaseLicenseConsumption |  |
| licenseRequirements | FinOpsLicenseRequirements |  |
| supplyChainManagementConsumption | FinOpsBaseLicenseConsumption |  |