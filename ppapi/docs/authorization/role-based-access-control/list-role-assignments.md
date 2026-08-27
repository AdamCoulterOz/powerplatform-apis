---
layout: Reference
title: Role Based Access Control - List Role Assignments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/list-role-assignments
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.listroleassignments
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
description: 'Learn more about Power Platform API service - List role assignments. Retrieves a list of role assignments. Preview. '
locale: en-us
document_id: 6fd7cd34-3df1-2f7b-b2eb-8d2b6b6780f9
document_version_independent_id: 5f898c08-e835-c813-2f41-86d1027e245f
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/List-Role-Assignments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/list-role-assignments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/List-Role-Assignments.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 33c1303f-a2ce-a8aa-3475-16072f24af63
---

# Role Based Access Control - List Role Assignments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List role assignments. Retrieves a list of role assignments. Preview.

```http
GET https://api.powerplatform.com/authorization/roleAssignments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RoleAssignmentResponse | A list of role assignments. |
| 400 Bad Request |  | Bad Request - The query parameters are invalid. |
| 401 Unauthorized |  | Unauthorized - Invalid credentials or missing authentication. |
| 404 Not Found |  | Not Found - The specified resource does not exist. |
| 500 Internal Server Error |  | Internal Server Error - Unexpected server error. |

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
| RoleAssignmentResponse | The role assignments. |
| Value |  |

### RoleAssignmentResponse

Object

The role assignments.

| Name | Type | Description |
| --- | --- | --- |
| value | Value[] |  |

### Value

Object

| Name | Type | Description |
| --- | --- | --- |
| permissions | string[] |  |
| roleDefinitionId | string | Role definition Id |
| roleDefinitionName | string | Role definition name |