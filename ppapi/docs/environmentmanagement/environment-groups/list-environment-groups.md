---
layout: Reference
title: Environment Groups - List Environment Groups - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-groups/list-environment-groups
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.listenvironmentgroups
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
description: 'Learn more about Power Platform API service - List the environment groups. '
locale: en-us
document_id: d625c759-0a77-9071-a2d2-f0218c009a12
document_version_independent_id: 8dd0b140-c541-a433-f818-ddaf5eae7c35
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/List-Environment-Groups.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-groups/list-environment-groups
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/List-Environment-Groups.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 710ec088-45ab-8573-9a43-754fc19d059d
---

# Environment Groups - List Environment Groups

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List the environment groups.

```http
GET https://api.powerplatform.com/environmentmanagement/environmentGroups?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentGroupResponseWithOdataContinuation | Success |
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

| Name | Description |
| --- | --- |
| EnvironmentGroup |  |
| EnvironmentGroupResponseWithOdataContinuation |  |
| Principal |  |
| ProblemDetails |  |

### EnvironmentGroup

Object

| Name | Type | Description |
| --- | --- | --- |
| childrenGroupIds | string[] (uuid) |  |
| createdBy | Principal |  |
| createdTime | string (date-time) |  |
| description | string |  |
| displayName | string |  |
| id | string (uuid) |  |
| lastModifiedBy | Principal |  |
| lastModifiedTime | string (date-time) |  |
| parentGroupId | string (uuid) |  |

### EnvironmentGroupResponseWithOdataContinuation

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | EnvironmentGroup[] |  |

### Principal

Object

| Name | Type | Description |
| --- | --- | --- |
| displayName | string |  |
| email | string |  |
| id | string |  |
| tenantId | string |  |
| type | string |  |
| userPrincipalName | string |  |

### ProblemDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| detail | string |  |
| extensions | api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.listenvironmentgroups |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |