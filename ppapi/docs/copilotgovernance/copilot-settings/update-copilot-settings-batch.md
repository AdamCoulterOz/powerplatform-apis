---
layout: Reference
title: Copilot Settings - Update Copilot Settings Batch - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotgovernance/copilot-settings/update-copilot-settings-batch
uid: api.powerplatform.com.power-platform.copilotgovernance.copilotsettings.updatecopilotsettingsbatch
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
description: Update a batch of Copilot governance settings. Updates one or more setting values for an environment in the tenant.
locale: en-us
document_id: b96472d3-64e1-e416-1db4-85e87ff7959d
document_version_independent_id: b14bcdab-9b2c-c847-4dec-342a4c840606
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/Update-Copilot-Settings-Batch.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotgovernance/copilot-settings/update-copilot-settings-batch
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotgovernance/Copilot-Settings/Update-Copilot-Settings-Batch.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/46e3c7c4-fe77-4a6e-b40a-44c569819fa5
- https://authoring-docs-microsoft.poolparty.biz/devrel/86a4b315-a9f1-4577-b985-6fb0e0e67420
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d0c6fab8-2d7d-4bb0-bf40-589e08d7c132
- https://authoring-docs-microsoft.poolparty.biz/devrel/96ac410d-d052-4707-8007-df31dd0fe041
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 55255028-68c6-63f8-82b1-63a4a8143a68
---

# Copilot Settings - Update Copilot Settings Batch

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update a batch of Copilot governance settings. Updates one or more setting values for an environment in the tenant. Requires the Copilot Governance settings write permission and a user API context. Service API contexts aren't supported. Supply a non-empty dictionary keyed by setting name. Legacy setting names are accepted. Null update objects aren't allowed. A null value is accepted only for a NullableBooleanValue setting. For EnumValue settings with defined options, each value must match an option returned by the setting.

```http
PUT https://api.powerplatform.com/copilotgovernance/environments/{environmentId}/settings?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment that contains the settings. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| settings | True | &lt;string, CopilotGovernanceSettingUpdate&gt; | Setting updates keyed by setting name. Each update object must be non-null. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | The settings were updated. No response body is returned. |
| 400 Bad Request |  | The environment ID, request body, settings dictionary, or a setting value is invalid. |
| 401 Unauthorized |  | A valid access token is required. |
| 403 Forbidden |  | The caller doesn't have write permission or isn't using a user API context. |
| 404 Not Found |  | A setting wasn't found or isn't available to the caller. |
| 500 Internal Server Error |  | An unexpected error occurred while updating settings. |

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
| CopilotGovernanceSettingsBatchUpdate | A non-empty dictionary of setting names and their update objects. |
| CopilotGovernanceSettingUpdate | A setting value to update. The value's JSON type must match the setting. A missing value is treated as null. Null is accepted only for NullableBooleanValue settings. For EnumValue settings with defined options, supply a numeric option value from options. |

### CopilotGovernanceSettingsBatchUpdate

Object

A non-empty dictionary of setting names and their update objects.

| Name | Type | Description |
| --- | --- | --- |
| settings | &lt;string, CopilotGovernanceSettingUpdate&gt; | Setting updates keyed by setting name. Each update object must be non-null. |

### CopilotGovernanceSettingUpdate

Object

A setting value to update. The value's JSON type must match the setting. A missing value is treated as null. Null is accepted only for NullableBooleanValue settings. For EnumValue settings with defined options, supply a numeric option value from options.

| Name | Type | Description |
| --- | --- | --- |
| value | CopilotGovernanceSettingValue | A setting value whose JSON type is determined by valueType. Values can be strings, integers, numbers, booleans, arrays, or numeric enum options. Null values are preserved when returned by the service. |