---
layout: Reference
title: Copilot Settings - Update Copilot Setting - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotgovernance/copilot-settings/update-copilot-setting
uid: api.powerplatform.com.power-platform.copilotgovernance.copilotsettings.updatecopilotsetting
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
description: Update a Copilot governance setting. Updates the value of a setting for an environment in the tenant.
locale: en-us
document_id: f0e4caf4-57ba-e5c3-639d-492d08f71649
document_version_independent_id: 60ba314c-5bac-ddb3-87db-e948e9dffac2
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/Update-Copilot-Setting.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotgovernance/copilot-settings/update-copilot-setting
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/Update-Copilot-Setting.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/46e3c7c4-fe77-4a6e-b40a-44c569819fa5
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d0c6fab8-2d7d-4bb0-bf40-589e08d7c132
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 3c63c81f-3e84-c765-3843-20ff394370f6
---

# Copilot Settings - Update Copilot Setting

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update a Copilot governance setting. Updates the value of a setting for an environment in the tenant. Requires the Copilot Governance settings write permission and a user API context. Service API contexts aren't supported. Legacy setting names are accepted. Null values are accepted only for NullableBooleanValue settings. For EnumValue settings with defined options, the value must match an option returned by the setting.

```http
PUT https://api.powerplatform.com/copilotgovernance/environments/{environmentId}/settings/{settingName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment that contains the settings. |
| settingName | path | True | string <br>minLength: 1 | The non-empty name of the setting, as returned by the settings collection. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| value | CopilotGovernanceSettingValue | A setting value whose JSON type is determined by valueType. Values can be strings, integers, numbers, booleans, arrays, or numeric enum options. Null values are preserved when returned by the service. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | The setting was updated. No response body is returned. |
| 400 Bad Request |  | The request body, environment ID, setting name, or setting value is invalid. |
| 401 Unauthorized |  | A valid access token is required. |
| 403 Forbidden |  | The caller doesn't have write permission or isn't using a user API context. |
| 404 Not Found |  | The setting wasn't found or isn't available to the caller. |
| 500 Internal Server Error |  | An unexpected error occurred while updating the setting. |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### CopilotGovernanceSettingUpdate

Object

A setting value to update. The value's JSON type must match the setting. A missing value is treated as null. Null is accepted only for NullableBooleanValue settings. For EnumValue settings with defined options, supply a numeric option value from options.

| Name | Type | Description |
| --- | --- | --- |
| value | CopilotGovernanceSettingValue | A setting value whose JSON type is determined by valueType. Values can be strings, integers, numbers, booleans, arrays, or numeric enum options. Null values are preserved when returned by the service. |