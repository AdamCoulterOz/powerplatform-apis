---
layout: Reference
title: Apps - Get AdminApp - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerapps/apps/get-admin-app
uid: api.powerplatform.com.power-platform.powerapps.apps.get-adminapp
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
description: 'Learn more about Power Platform API service - Get app as administrator. Returns a PowerApp. '
locale: en-us
document_id: 45afc077-a65f-ad60-572d-bfbfabb8ffce
document_version_independent_id: 93a6f575-400d-c0ab-d8db-57600e72b360
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerapps/Apps/Get-Admin-App.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerapps/apps/get-admin-app
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerapps/Apps/Get-Admin-App.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0b6f3a15-20c4-c5e8-4fb8-1cabcee4b4e6
---

# Apps - Get AdminApp

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get app as administrator. Returns a PowerApp.

```http
GET https://api.powerplatform.com/powerapps/environments/{environmentId}/apps/{app}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| app | path | True | string | Name field of the PowerApp. |
| environmentId | path | True | string | Name field of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | PowerApp | 200 |

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
| AppUris | PowerApp appUri object. |
| ConnectionReference |  |
| CreatedBy | PowerApp created by principal object. |
| CreatedByClientVersion | PowerApp property createdByClientVersion object. |
| DocumentUri | PowerApp appUri document URI object. |
| Environment | PowerApp environment property object. |
| LastModifiedBy | PowerApp last modified by object. |
| MinClientVersion | PowerApp property minClientVersion object. |
| Owner | PowerApp owner principal object. |
| PowerApp |  |
| Properties | PowerApp properties object. |
| Tags | tags |
| UserAppMetadata | PowerApp property user app metadata object. |

### AppUris

Object

PowerApp appUri object.

| Name | Type | Description |
| --- | --- | --- |
| documentUri | DocumentUri | PowerApp appUri document URI object. |
| imageUris | string[] | PowerApp appUri image URI array. |

### ConnectionReference

Object

| Name | Type | Description |
| --- | --- | --- |
| apiTier | string | API tier is standard or premium |
| bypassConsent | boolean | Flag indicates bypassed API consent |
| dataSources | string[] | List of data sources for the connection |
| dependencies | string[] | List of dependencies for the connection |
| dependents | string[] | List of dependent connectors for the connector |
| displayName | string |  |
| executionRestrictions | object | Execution restrictions for the runtime policy |
| iconUri | string |  |
| id | string |  |
| isCustomApiConnection | boolean | Flag indicates custom connector |
| isOnPremiseConnection | boolean | Flag indicates on-premises data gateway |
| runtimePolicyName | string | String indicating the name of the runtime policy |
| sharedConnectionId | string | String indicating the ID of the shared connection |

### CreatedBy

Object

PowerApp created by principal object.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | PowerApp creator principal display name. |
| email | string | PowerApp creator principal email. |
| id | string | PowerApp creator principal object ID. |
| tenantId | string | PowerApp creator principal tenant ID. |
| type | string | PowerApp creator principal type. |
| userPrincipalName | string | PowerApp creator principal user principal name. |

### CreatedByClientVersion

Object

PowerApp property createdByClientVersion object.

| Name | Type | Description |
| --- | --- | --- |
| build | integer (int32) | PowerApp property createdByClientVersion build. |
| major | integer (int32) | PowerApp property createdByClientVersion major. |
| majorRevision | integer (int32) | PowerApp property createdByClientVersion majorRevision. |
| minor | integer (int32) | PowerApp property createdByClientVersion minor. |
| minorRevision | integer (int32) | PowerApp property createdByClientVersion minorRevision. |
| revision | integer (int32) | PowerApp property createdByClientVersion revision. |

### DocumentUri

Object

PowerApp appUri document URI object.

| Name | Type | Description |
| --- | --- | --- |
| readonlyValue | string | PowerApp appUri document URI read only value. |
| value | string | PowerApp appUri document URI value. |

### Environment

Object

PowerApp environment property object.

| Name | Type | Description |
| --- | --- | --- |
| id | string | PowerApp environment ID. |
| name | string | PowerApp environment name. |

### LastModifiedBy

Object

PowerApp last modified by object.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | PowerApp last modified by principal display name. |
| email | string | PowerApp last modified by principal email. |
| id | string | PowerApp last modified by principal object ID. |
| tenantId | string | PowerApp last modified by principal tenant ID. |
| type | string | PowerApp last modified by principal type. |
| userPrincipalName | string | PowerApp last modified by principal userPrincipalName. |

### MinClientVersion

Object

PowerApp property minClientVersion object.

| Name | Type | Description |
| --- | --- | --- |
| build | integer (int32) | PowerApp property minClientVersion build. |
| major | integer (int32) | PowerApp property minClientVersion major. |
| majorRevision | integer (int32) | PowerApp property minClientVersion majorRevision. |
| minor | integer (int32) | PowerApp property minClientVersion minor. |
| minorRevision | integer (int32) | PowerApp property minClientVersion minorRevision. |
| revision | integer (int32) | PowerApp property minClientVersion revision. |

### Owner

Object

PowerApp owner principal object.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | PowerApp owner principal display name. |
| email | string | PowerApp owner principal email. |
| id | string | PowerApp owner principal user ID. |
| tenantId | string | PowerApp owner principal tenant ID. |
| type | string | PowerApp owner principal type. |
| userPrincipalName | string | PowerApp owner principal user principal name. |

### PowerApp

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string | PowerApp ID field. |
| name | string | PowerApp name field. |
| properties | Properties | PowerApp properties object. |
| tags | Tags | tags |
| type | string | PowerApp type field. |

### Properties

Object

PowerApp properties object.

| Name | Type | Description |
| --- | --- | --- |
| appOpenProtocolUri | string | PowerApp property app open protocol URI. |
| appOpenUri | string | PowerApp property app open URI. |
| appUris | AppUris | PowerApp appUri object. |
| appVersion | string (date-time) | PowerApp property appVersion. |
| backgroundColor | string | PowerApp background color. |
| backgroundImageUri | string | PowerApp background image URI. |
| bypassConsent | boolean | PowerApp property bypass consent. |
| connectionReferences | ConnectionReference[] |  |
| createdBy | CreatedBy | PowerApp created by principal object. |
| createdByClientVersion | CreatedByClientVersion | PowerApp property createdByClientVersion object. |
| createdTime | string (date-time) | PowerApp property created time. |
| description | string | PowerApp description. |
| displayName | string | PowerApp display name. |
| environment | Environment | PowerApp environment property object. |
| isFeaturedApp | boolean | PowerApp property is featured app. |
| isHeroApp | boolean | PowerApp property indicating hero application. |
| lastModifiedBy | LastModifiedBy | PowerApp last modified by object. |
| lastModifiedTime | string (date-time) | PowerApp property last modified time. |
| minClientVersion | MinClientVersion | PowerApp property minClientVersion object. |
| owner | Owner | PowerApp owner principal object. |
| sharedGroupsCount | integer (int32) | PowerApp property shared groups count. |
| sharedUsersCount | integer (int32) | PowerApp property shared users count. |
| userAppMetadata | UserAppMetadata | PowerApp property user app metadata object. |

### Tags

Object

tags

| Name | Type | Description |
| --- | --- | --- |
| deviceCapabilities | string | PowerApp tag device capabilities. |
| minimumRequiredApiVersion | string (date-time) | PowerApp tag minimum required API version. |
| primaryDeviceHeight | string | PowerApp tag primary device height. |
| primaryDeviceWidth | string | PowerApp tag primary device width. |
| primaryFormFactor | string | PowerApp tag primary form factor. |
| publisherVersion | string | PowerApp tag publisher version. |
| sienaVersion | string | PowerApp tag siena version. |
| supportsLandscape | string | PowerApp tag supports landscape. |
| supportsPortrait | string | PowerApp tag supports portrait. |

### UserAppMetadata

Object

PowerApp property user app metadata object.

| Name | Type | Description |
| --- | --- | --- |
| favorite | string | PowerApp property user app metadata favorite. |
| includeInAppsList | boolean | PowerApp property user app metadata include in apps list. |