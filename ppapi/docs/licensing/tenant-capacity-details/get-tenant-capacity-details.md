---
layout: Reference
title: Tenant Capacity Details - Get Tenant Capacity Details - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/tenant-capacity-details/get-tenant-capacity-details
uid: api.powerplatform.com.power-platform.licensing.tenantcapacitydetails.gettenantcapacitydetails
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
description: 'Learn more about Power Platform API service - Get the tenant capacity details for the tenant. '
locale: en-us
document_id: 57807dc6-2e47-c851-b4e3-32358d7a5477
document_version_independent_id: e9eee46f-9bf5-89ab-ea55-36d091d3e247
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Tenant-Capacity-Details/Get-Tenant-Capacity-Details.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/tenant-capacity-details/get-tenant-capacity-details
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Tenant-Capacity-Details/Get-Tenant-Capacity-Details.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 30c04bd7-6dfe-5712-68c9-f33fbf6beacc
---

# Tenant Capacity Details - Get Tenant Capacity Details

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the tenant capacity details for the tenant.

```http
GET https://api.powerplatform.com/licensing/tenantCapacity?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantCapacityDetailsModel | Success |
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
| CapacityAvailabilityStatus |  |
| CapacityEntitlementType |  |
| CapacityStatusMessageCode |  |
| CapacitySummary |  |
| CapacityType |  |
| CapacityUnits |  |
| ConsumptionModel |  |
| LegacyCapacityModel |  |
| LicenseDetailsModel |  |
| LicenseModel |  |
| LicenseQuantity |  |
| OverflowCapacityModel |  |
| TemporaryLicenseInfo |  |
| TenantCapacityAndConsumptionModel |  |
| TenantCapacityDetailsModel |  |
| TenantCapacityEntitlementModel |  |

### CapacityAvailabilityStatus

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Available |  |
| AvailableByOverflow |  |
| NotAvailable |  |

### CapacityEntitlementType

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| DatabaseBase |  |
| DatabaseIncremental |  |
| DatabaseAddOn |  |
| FileBase |  |
| FileIncremental |  |
| FileAddOn |  |
| LogBase |  |
| LogAddOn |  |
| SubscriptionTrialDatabaseBase |  |
| SubscriptionTrialFileBase |  |
| SubscriptionTrialLogBase |  |
| SubscriptionTrialEnvironmentCountBase |  |
| SubscriptionTrialEnvironmentCountIncremental |  |
| TrialDatabaseBase |  |
| TrialFileBase |  |
| TrialLogBase |  |
| M365DatabaseBase |  |
| M365DatabaseIncremental |  |
| M365EnvironmentCountBase |  |
| M365EnvironmentCountIncremental |  |
| ApiCallCountIncremental |  |
| ApiCallCountBase |  |
| CapacityPassBase |  |
| FinOpsDatabaseBase |  |
| FinOpsDatabaseIncremental |  |
| FinOpsFileBase |  |
| FinOpsFileIncremental |  |

### CapacityStatusMessageCode

Enumeration

| Value | Description |
| --- | --- |
| AllCapacityAvailable |  |
| DBCapacityOver |  |
| LogOverDBCover |  |
| LogCapacityOver |  |
| FileOverDBCover |  |
| FileOverLogCover |  |
| FileOverDBAndLogCover |  |
| FileCapacityOver |  |
| DBAndLogOver |  |
| DBAndFileOver |  |
| LogAndFileOverDBCover |  |
| LogAndFileOver |  |
| AllCapacityOver |  |
| LegacyCapacityAvailable |  |
| LegacyCapacityOver |  |
| FinOpsAllCapacityAvailable |  |
| FinOpsNotAvailable |  |
| FinOpsAllCapacityOver |  |
| FinOpsDBCapacityOver |  |
| FinOpsFileCapacityOver |  |
| LegacyCapacityMoreThanEightyFive |  |
| DBCapacityMoreThanEightyFive |  |
| LogCapacityMoreThanEightyFive |  |
| FileCapacityMoreThanEightyFive |  |
| DBAndFileCapacityMoreThanEightyFive |  |
| DBAndLogCapacityMoreThanEightyFive |  |
| LogAndFileCapacityMoreThanEightyFive |  |
| AllCapacityMoreThanEightyFive |  |

### CapacitySummary

Object

| Name | Type | Description |
| --- | --- | --- |
| finOpsStatus | CapacityAvailabilityStatus |  |
| finOpsStatusMessage | string |  |
| finOpsStatusMessageCode | CapacityStatusMessageCode |  |
| status | CapacityAvailabilityStatus |  |
| statusMessage | string |  |
| statusMessageCode | CapacityStatusMessageCode |  |

### CapacityType

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Database |  |
| File |  |
| Log |  |
| TrialDatabase |  |
| TrialFile |  |
| TrialLog |  |
| SubscriptionTrialDatabase |  |
| SubscriptionTrialFile |  |
| SubscriptionTrialLog |  |
| M365Database |  |
| M365EnvironmentCount |  |
| SubscriptionTrialEnvironmentCount |  |
| CapacityPass |  |
| ApiCallCount |  |
| FinOpsDatabase |  |
| FinOpsFile |  |
| PIProcess |  |

### CapacityUnits

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Unit |  |
| MB |  |

### ConsumptionModel

Object

| Name | Type | Description |
| --- | --- | --- |
| actual | number (double) |  |
| actualUpdatedOn | string (date-time) |  |
| rated | number (double) |  |
| ratedUpdatedOn | string (date-time) |  |

### LegacyCapacityModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacityUnits | CapacityUnits |  |
| totalCapacity | number (double) |  |
| totalConsumption | number (double) |  |

### LicenseDetailsModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capabilityStatus | string |  |
| displayName | string |  |
| entitlementCode | string |  |
| isTemporaryLicense | boolean |  |
| nextLifecycleDate | string (date-time) |  |
| paid | LicenseQuantity |  |
| servicePlanId | string (uuid) |  |
| skuId | string (uuid) |  |
| temporaryLicenseExpiryDate | string (date-time) |  |
| totalCapacity | number (double) |  |
| trial | LicenseQuantity |  |

### LicenseModel

Enumeration

| Value | Description |
| --- | --- |
| None |  |
| Legacy |  |
| StorageDriven |  |

### LicenseQuantity

Object

| Name | Type | Description |
| --- | --- | --- |
| enabled | integer (int32) |  |
| suspended | integer (int32) |  |
| warning | integer (int32) |  |

### OverflowCapacityModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacityType | CapacityType |  |
| value | number (double) |  |

### TemporaryLicenseInfo

Object

| Name | Type | Description |
| --- | --- | --- |
| hasTemporaryLicense | boolean |  |
| temporaryLicenseExpiryDate | string (date-time) |  |

### TenantCapacityAndConsumptionModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacityEntitlements | TenantCapacityEntitlementModel[] |  |
| capacityType | CapacityType |  |
| capacityUnits | CapacityUnits |  |
| consumption | ConsumptionModel |  |
| maxCapacity | number (double) |  |
| overflowCapacity | OverflowCapacityModel[] |  |
| status | CapacityAvailabilityStatus |  |
| totalCapacity | number (double) |  |

### TenantCapacityDetailsModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacitySummary | CapacitySummary |  |
| legacyModelCapacity | LegacyCapacityModel |  |
| licenseModelType | LicenseModel |  |
| temporaryLicenseInfo | TemporaryLicenseInfo |  |
| tenantCapacities | TenantCapacityAndConsumptionModel[] |  |
| tenantId | string (uuid) |  |

### TenantCapacityEntitlementModel

Object

| Name | Type | Description |
| --- | --- | --- |
| capacitySubType | CapacityEntitlementType |  |
| capacityType | CapacityType |  |
| licenses | LicenseDetailsModel[] |  |
| maxNextLifecycleDate | string (date-time) |  |
| totalCapacity | number (double) |  |