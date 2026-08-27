---
layout: Reference
title: Entitlement - Get Many Environment Entitlements - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement/get-many-environment-entitlements
uid: api.powerplatform.com.power-platform.licensing.entitlement.getmanyenvironmententitlements
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
description: 'Learn more about Power Platform API service - Get the entitlements for the tenant by environment. '
locale: en-us
document_id: 229ef8ac-4955-9283-24da-abfa8738309f
document_version_independent_id: d75c4705-2cee-9e54-9f66-9e9eb24e59b2
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement/Get-Many-Environment-Entitlements.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement/get-many-environment-entitlements
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement/Get-Many-Environment-Entitlements.yml
platformId: 76e78492-8ed4-6e2d-fd0f-f522485258b4
---

# Entitlement - Get Many Environment Entitlements

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the entitlements for the tenant by environment.

```http
GET https://api.powerplatform.com/licensing/environments/{environmentId}/entitlements?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/environments/{environmentId}/entitlements?$filter={$filter}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| $filter | query |  | string | OData filter expression. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentEntitlementResponseModel[] | Success |
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
| AllocationEnforcementRule |  |
| AllocationEnforcementRuleTypes | The type of an allocation enforcement rule. |
| CatalogPayGoEntitlementModel |  |
| CurrencyType | The currency (capacity) type for an addon. |
| EntitlementAllocationModelV2 |  |
| EntitlementConsumedModel |  |
| EntitlementConsumptionType | The consumption type for an entitlement. |
| EntitlementEntitledModel |  |
| EntitlementUnit | The unit of measure for an entitlement. |
| EnvironmentAddonResponseModel | A BAP addon attached to an environment. |
| EnvironmentCapacityEntitlementModel | The capacity entitlement for an environment scope. |
| EnvironmentDisasterRecoveryLocation | The disaster recovery location of the environment. |
| EnvironmentDisasterRecoveryState | The disaster recovery state of the environment. |
| EnvironmentEntitlementDetailServiceModel | The entitlement capacity and pay-as-you-go details for an environment-scoped entitlement. |
| EnvironmentEntitlementResponseModel | An entitlement and its capacity/pay-as-you-go details scoped to a single environment, including environment metadata. |
| EnvironmentPermissionResponseModel | A BAP permission on an environment. |
| EnvironmentScenario | The scenario of the environment. |
| EnvironmentType | The type of the environment. |
| OverageStatus | The overage status of an entitled capacity. |
| ProductCategory | The product category associated with an entitlement. |

### AllocationEnforcementRule

Object

| Name | Type | Description |
| --- | --- | --- |
| enabled | boolean |  |
| ruleType | AllocationEnforcementRuleTypes | The type of an allocation enforcement rule. |

### AllocationEnforcementRuleTypes

Enumeration

The type of an allocation enforcement rule.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Alert |  |
| PayGo |  |
| TenantPool |  |
| Deny |  |
| Throttle |  |

### CatalogPayGoEntitlementModel

Object

| Name | Type | Description |
| --- | --- | --- |
| consumed | EntitlementConsumedModel |  |
| entitled | EntitlementEntitledModel |  |

### CurrencyType

Enumeration

The currency (capacity) type for an addon.

| Value | Description |
| --- | --- |
| None |  |
| AppPass |  |
| AI |  |
| PortalLogins |  |
| PortalViews |  |
| PerFlowPlan |  |
| ApiCalls |  |
| VAConversations |  |
| AppPassForTeams |  |
| PAUnattendedRPA |  |
| PowerPagesAuthenticated |  |
| PowerPagesAnonymous |  |
| PAHostedRPA |  |
| Invoice |  |
| PortalAddOns |  |
| PowerAutomatePerProcess |  |
| MCSSessions |  |
| MCSMessages |  |
| SCMessages |  |
| ProcessMiningDataStorage |  |
| W365APAYGO |  |
| Internal\_AI\_BC |  |
| Internal\_ISV\_DataverseUserSync |  |
| Internal\_AI\_TemporaryCapacity |  |
| Internal\_OmniChannelRecordRouting |  |
| Internal\_OmniChannelVoice |  |
| Internal\_OmniChannelLiveChat |  |
| Internal\_OmniChannelDigitalMessaging |  |
| PowerPagesMigration\_PortalAddOns\_Authenticated |  |
| PowerPagesMigration\_PortalAddOns\_Anonymous |  |
| PowerPagesMigration\_PortalLogins |  |
| PowerPagesMigration\_PortalViews |  |
| MCSMessagesStandard |  |
| MCSMessagesGenAI |  |
| MCSMessagesUnbillable |  |
| TenantM365Copilot |  |

### EntitlementAllocationModelV2

Object

| Name | Type | Description |
| --- | --- | --- |
| autoAllocated | number (double) |  |
| value | number (double) |  |

### EntitlementConsumedModel

Object

| Name | Type | Description |
| --- | --- | --- |
| consumptionType | EntitlementConsumptionType | The consumption type for an entitlement. |
| lastUpdatedOn | string (date-time) |  |
| value | number (double) |  |
| writeOff | number (double) |  |

### EntitlementConsumptionType

Enumeration

The consumption type for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Snapshot |  |
| MonthToDate |  |

### EntitlementEntitledModel

Object

| Name | Type | Description |
| --- | --- | --- |
| value | number (double) |  |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### EnvironmentAddonResponseModel

Object

A BAP addon attached to an environment.

| Name | Type | Description |
| --- | --- | --- |
| addonType | CurrencyType | The currency (capacity) type for an addon. |
| addonUnit | string |  |
| allocated | number (double) |  |

### EnvironmentCapacityEntitlementModel

Object

The capacity entitlement for an environment scope.

| Name | Type | Description |
| --- | --- | --- |
| allocated | EntitlementAllocationModelV2 |  |
| availableQuantity | number (double) |  |
| consumed | EntitlementConsumedModel |  |
| enforcementRules | AllocationEnforcementRule[] |  |
| status | OverageStatus | The overage status of an entitled capacity. |

### EnvironmentDisasterRecoveryLocation

Enumeration

The disaster recovery location of the environment.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| NearCopy |  |
| FarCopy |  |

### EnvironmentDisasterRecoveryState

Enumeration

The disaster recovery state of the environment.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Enabled |  |
| Ready |  |
| Disabled |  |
| Unavailable |  |

### EnvironmentEntitlementDetailServiceModel

Object

The entitlement capacity and pay-as-you-go details for an environment-scoped entitlement.

| Name | Type | Description |
| --- | --- | --- |
| capacity | EnvironmentCapacityEntitlementModel | The capacity entitlement for an environment scope. |
| payGo | CatalogPayGoEntitlementModel |  |
| unit | EntitlementUnit | The unit of measure for an entitlement. |

### EnvironmentEntitlementResponseModel

Object

An entitlement and its capacity/pay-as-you-go details scoped to a single environment, including environment metadata.

| Name | Type | Description |
| --- | --- | --- |
| addons | EnvironmentAddonResponseModel[] | The BAP addons attached to the environment. |
| cleanupOpportunitySize | integer (int64) | The total storage in bytes that could be reclaimed. |
| disasterRecoveryLocation | EnvironmentDisasterRecoveryLocation | The disaster recovery location of the environment. |
| disasterRecoveryState | EnvironmentDisasterRecoveryState | The disaster recovery state of the environment. |
| entitlement | EnvironmentEntitlementDetailServiceModel | The entitlement capacity and pay-as-you-go details for an environment-scoped entitlement. |
| entitlementId | string | The entitlement ID. |
| environmentId | string | The environment ID. |
| environmentName | string | The environment name. |
| environmentType | EnvironmentType | The type of the environment. |
| isManagedEnvironment | boolean | Indicates whether the environment is a managed environment. |
| location | string | The geographic location of the environment. |
| permissions | EnvironmentPermissionResponseModel[] | The BAP permissions on the environment. |
| productCategories | ProductCategory[] | The entitlement product categories (e.g., D365Apps, Dataverse, Power Apps, Power Automate). |
| recommendationCount | integer (int32) | The number of active cleanup recommendations. |
| scenario | EnvironmentScenario | The scenario of the environment. |

### EnvironmentPermissionResponseModel

Object

A BAP permission on an environment.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string |  |
| name | string |  |

### EnvironmentScenario

Enumeration

The scenario of the environment.

| Value | Description |
| --- | --- |
| None |  |
| OfficeAi |  |
| M365CopilotChat |  |
| M365CompliantContainer |  |

### EnvironmentType

Enumeration

The type of the environment.

| Value | Description |
| --- | --- |
| None |  |
| Production |  |
| Sandbox |  |
| Support |  |
| Preview |  |
| Trial |  |
| Default |  |
| Developer |  |
| SubscriptionBasedTrial |  |
| Teams |  |
| NotSpecified |  |
| Platform |  |

### OverageStatus

Enumeration

The overage status of an entitled capacity.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| WithinCapacity |  |
| Overage |  |
| CoveredOverage |  |

### ProductCategory

Enumeration

The product category associated with an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| D365Apps |  |
| Dataverse |  |
| Fno |  |
| PowerApps |  |
| PowerAutomate |  |
| PowerPages |  |
| PowerVirtualAgent |  |
| CopilotStudio |  |
| PowerPlatform |  |
| Project |  |
| W365 |  |
| D365CustomerInsights |  |
| D365ContactCenter |  |
| Teams |  |
| CloudForSustainability |  |
| CoWork |  |
| M365 |  |
| ManagedApps |  |