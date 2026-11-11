---
layout: Reference
title: Copilot Settings - List Copilot Settings - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotgovernance/copilot-settings/list-copilot-settings
uid: api.powerplatform.com.power-platform.copilotgovernance.copilotsettings.listcopilotsettings
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
description: List Copilot governance settings. Lists the settings available for an environment in the tenant. Requires the Copilot Governance settings read permission and su
locale: en-us
document_id: 25510af9-d2e8-5136-43e5-b7b23a295321
document_version_independent_id: 963faba6-a06c-b213-2e45-f8673182d97c
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/List-Copilot-Settings.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotgovernance/copilot-settings/list-copilot-settings
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/List-Copilot-Settings.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/46e3c7c4-fe77-4a6e-b40a-44c569819fa5
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d0c6fab8-2d7d-4bb0-bf40-589e08d7c132
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c770123d-372d-bff2-bba6-eca021804828
---

# Copilot Settings - List Copilot Settings

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List Copilot governance settings. Lists the settings available for an environment in the tenant. Requires the Copilot Governance settings read permission and supports user and service API contexts. The collection is returned in results. The current implementation returns the collection without a continuation token.

```http
GET https://api.powerplatform.com/copilotgovernance/environments/{environmentId}/settings?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment that contains the settings. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | CopilotGovernanceSettingsResponse | The settings available for the environment. |
| 400 Bad Request |  | The environment ID is invalid. |
| 401 Unauthorized |  | A valid access token is required. |
| 403 Forbidden |  | The caller doesn't have permission to read settings. |
| 500 Internal Server Error |  | An unexpected error occurred while retrieving settings. |

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
| CopilotGovernanceAudienceType | The audience that can use the setting. |
| CopilotGovernanceCategoryType | The category of the setting. |
| CopilotGovernanceEnabledStatus | Whether the setting is enabled for no users, all users, or a restricted set of users. |
| CopilotGovernanceEnumOption | A numeric option and its display name for an EnumValue setting. |
| CopilotGovernancePlatformProductType | The Power Platform product associated with the setting. |
| CopilotGovernanceRuleInput | The input and setting names that associate a setting with a rule. |
| CopilotGovernanceSetting | A Copilot governance setting, its value, and its metadata. |
| CopilotGovernanceSettingRule | The environment-group rule associated with a setting. |
| CopilotGovernanceSettingsResponse | A collection of environment settings in the service's OData response shape. |
| CopilotGovernanceSettingState | The release state of the setting. |
| CopilotGovernanceSettingValueType | The JSON value type of the setting. |
| CopilotGovernanceStatusMessage | The localized badge and tooltip messages for a setting. |
| CopilotGovernanceStoreResourceType | The backing resource used to store the setting. |

### CopilotGovernanceAudienceType

Enumeration

The audience that can use the setting.

| Value | Description |
| --- | --- |
| Admins |  |
| Makers |  |
| EndUsers |  |

### CopilotGovernanceCategoryType

Enumeration

The category of the setting.

| Value | Description |
| --- | --- |
| None |  |
| DataEntryAgent |  |
| DataExplorationAgent |  |
| SummaryAgent |  |
| ChatAgent |  |
| ExternalModels |  |

### CopilotGovernanceEnabledStatus

Enumeration

Whether the setting is enabled for no users, all users, or a restricted set of users.

| Value | Description |
| --- | --- |
| EnabledForNone |  |
| EnabledForAll |  |
| EnabledForSome |  |

### CopilotGovernanceEnumOption

Object

A numeric option and its display name for an EnumValue setting.

| Name | Type | Description |
| --- | --- | --- |
| name | string | The display name of the option. |
| value | integer (int32) | The numeric option value. |

### CopilotGovernancePlatformProductType

Enumeration

The Power Platform product associated with the setting.

| Value | Description |
| --- | --- |
| PowerPlatform |  |
| PowerApps |  |
| PowerAutomate |  |
| PowerPages |  |
| CopilotStudio |  |
| Agent365 |  |
| D365Marketing |  |
| D365Sales |  |
| D365CustomerService |  |
| D365ProjectOperations |  |
| MicrosoftDataverse |  |
| ManagedApps |  |

### CopilotGovernanceRuleInput

Object

The input and setting names that associate a setting with a rule.

| Name | Type | Description |
| --- | --- | --- |
| inputName | string | The name of the rule input. |
| settingName | string | The setting name associated with the rule input. |

### CopilotGovernanceSetting

Object

A Copilot governance setting, its value, and its metadata.

| Name | Type | Description |
| --- | --- | --- |
| audiences | CopilotGovernanceAudienceType[] | The audiences for the setting. |
| category | CopilotGovernanceCategoryType | The category of the setting. |
| checkboxLabel | string | The checkbox label shown instead of On in the setting update panel. |
| defaultValue | CopilotGovernanceSettingValue | A setting value whose JSON type is determined by valueType. Values can be strings, integers, numbers, booleans, arrays, or numeric enum options. Null values are preserved when returned by the service. |
| description | string | The setting description. |
| displayName | string | The display name of the setting. |
| enabledStatus | CopilotGovernanceEnabledStatus | Whether the setting is enabled for no users, all users, or a restricted set of users. |
| environmentId | string | The ID of the environment that owns the setting. |
| hideWhenNull | boolean | Whether a NullableBooleanValue setting should be hidden when its value is null. |
| invertValue | boolean | Whether the displayed setting value should be inverted. |
| isDisabled | boolean | Whether the setting is disabled for editing. |
| isManagedEnvironmentProperty | boolean | Whether the setting is a Managed Environment property. |
| learnDocLink | string | The documentation link for the setting. |
| options | CopilotGovernanceEnumOption[] | The allowed numeric options for an EnumValue setting, when available. |
| platformProduct | CopilotGovernancePlatformProductType | The Power Platform product associated with the setting. |
| resourceId | string | The setting resource ID. |
| rule | CopilotGovernanceSettingRule | The environment-group rule associated with a setting. |
| settingName | string | The setting name. |
| settingState | CopilotGovernanceSettingState | The release state of the setting. |
| statusMessage | CopilotGovernanceStatusMessage | The localized badge and tooltip messages for a setting. |
| storeResource | CopilotGovernanceStoreResourceType | The backing resource used to store the setting. |
| tenantId | string | The ID of the tenant that owns the setting. |
| value | CopilotGovernanceSettingValue | A setting value whose JSON type is determined by valueType. Values can be strings, integers, numbers, booleans, arrays, or numeric enum options. Null values are preserved when returned by the service. |
| valueType | CopilotGovernanceSettingValueType | The JSON value type of the setting. |

### CopilotGovernanceSettingRule

Object

The environment-group rule associated with a setting.

| Name | Type | Description |
| --- | --- | --- |
| isLegacyRule | boolean | Whether the rule uses the legacy rule definition. |
| resourceType | string | The resource type, when applicable to a legacy rule. |
| ruleId | string | The rule ID registered for the setting. |
| ruleInput | CopilotGovernanceRuleInput[] | The rule inputs associated with settings. |

### CopilotGovernanceSettingsResponse

Object

A collection of environment settings in the service's OData response shape.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) | The optional collection count. The current implementation doesn't populate it. |
| @odata.nextLink | string | The next-page URL. The current implementation doesn't issue continuation tokens. |
| results | CopilotGovernanceSetting[] | The settings returned for the environment. |

### CopilotGovernanceSettingState

Enumeration

The release state of the setting.

| Value | Description |
| --- | --- |
| PrivatePreview |  |
| PublicPreview |  |
| GenerallyAvailable |  |
| Beta |  |

### CopilotGovernanceSettingValueType

Enumeration

The JSON value type of the setting.

| Value | Description |
| --- | --- |
| StringValue |  |
| IntegerValue |  |
| NumberValue |  |
| BooleanValue |  |
| ArrayValue |  |
| EnumValue |  |
| NullableBooleanValue |  |

### CopilotGovernanceStatusMessage

Object

The localized badge and tooltip messages for a setting.

| Name | Type | Description |
| --- | --- | --- |
| disabledLearnMoreLink | string | The documentation link in the disabled badge tooltip. |
| disabledText | string | The badge text when the setting is disabled. |
| disabledTooltip | string | The badge tooltip when the setting is disabled. |
| enabledText | string | The badge text when the setting is enabled. |
| someText | string | The badge text when the setting is enabled for some users. |

### CopilotGovernanceStoreResourceType

Enumeration

The backing resource used to store the setting.

| Value | Description |
| --- | --- |
| BAPRPTenant |  |
| BAPRPEnvironment |  |
| DataverseOrganization |  |
| OMSEnvironment |  |
| OMSEnvironmentV2 |  |