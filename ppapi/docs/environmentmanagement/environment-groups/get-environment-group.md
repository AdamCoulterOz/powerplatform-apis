---
layout: Reference
title: Environment Groups - Get Environment Group - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-groups/get-environment-group
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.getenvironmentgroup
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
description: 'Learn more about Power Platform API service - Get the environment group. '
locale: en-us
document_id: b8c0e76c-e7b4-f3db-50c7-a31e9205255e
document_version_independent_id: d684aa42-a0ab-70f4-8d32-59971236b062
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Get-Environment-Group.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-groups/get-environment-group
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Get-Environment-Group.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 325ad407-2af8-dcad-cf6f-8ce0f2b35642
---

# Environment Groups - Get Environment Group

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the environment group.

```http
GET https://api.powerplatform.com/environmentmanagement/environmentGroups/{groupId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| groupId | path | True | string | The group ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentGroup | Success |
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
| extensions | api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.getenvironmentgroup |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |