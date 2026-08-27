---
layout: Reference
title: Environment Groups - Remove Environment From Group - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-groups/remove-environment-from-group
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.removeenvironmentfromgroup
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
description: 'Learn more about Power Platform API service - Remove the environment from the environment group. '
locale: en-us
document_id: 1cf13f69-7e20-a757-ce47-827e26fda610
document_version_independent_id: d47a82fd-b580-51df-f873-184614c3ea8b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Remove-Environment-From-Group.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-groups/remove-environment-from-group
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Remove-Environment-From-Group.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 580ddadb-26e0-6a6f-405e-f9ec5af4c180
---

# Environment Groups - Remove Environment From Group

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Remove the environment from the environment group.

```http
POST https://api.powerplatform.com/environmentmanagement/environmentGroups/{groupId}/removeEnvironment/{environmentId}?api-version=2024-10-01
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
| extensions | api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.removeenvironmentfromgroup |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |