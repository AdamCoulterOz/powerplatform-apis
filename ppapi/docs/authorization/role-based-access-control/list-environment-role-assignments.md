---
layout: Reference
title: Role Based Access Control - List Environment Role Assignments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/list-environment-role-assignments
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.listenvironmentroleassignments
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
description: 'List environment role assignments. Retrieves a list of role assignments for the specified environment. Preview. '
locale: en-us
document_id: ba6b752e-0384-0e67-4528-dfc88748aea8
document_version_independent_id: 5de11c76-b5a3-a35e-3886-5b55e77f6fd2
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/List-Environment-Role-Assignments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/list-environment-role-assignments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/List-Environment-Role-Assignments.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: b7b2bef3-d5fb-df05-c4ab-978b281900ad
---

# Role Based Access Control - List Environment Role Assignments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List environment role assignments. Retrieves a list of role assignments for the specified environment. Preview.

```http
GET https://api.powerplatform.com/authorization/environments/{environmentId}/roleAssignments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RoleAssignmentResponse | A list of role assignments for the environment. |
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