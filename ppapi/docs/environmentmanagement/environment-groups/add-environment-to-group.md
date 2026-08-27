---
layout: Reference
title: Environment Groups - Add Environment To Group - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-groups/add-environment-to-group
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.addenvironmenttogroup
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
description: 'Learn more about Power Platform API service - Add the environment to the environment group. '
locale: en-us
document_id: aa0f6ada-d84e-7261-6bfc-455caa306d6f
document_version_independent_id: a1d3a1ff-eeb1-6322-4462-f7c9b892a4ec
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Add-Environment-To-Group.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-groups/add-environment-to-group
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Add-Environment-To-Group.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 64237b95-e7b0-c9ca-37eb-a5d2a18f0bf8
---

# Environment Groups - Add Environment To Group

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Add the environment to the environment group.

```http
POST https://api.powerplatform.com/environmentmanagement/environmentGroups/{groupId}/addEnvironment/{environmentId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| groupId | path | True | string (uuid) | The group ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted |
| 204 No Content |  | No Content |
| 400 Bad Request | ProblemDetails | Bad Request |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### ProblemDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| detail | string |  |
| extensions | api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.addenvironmenttogroup |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |