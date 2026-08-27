---
layout: Reference
title: Role Based Access Control - Create Environment Role Assignment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/create-environment-role-assignment
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.createenvironmentroleassignment
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
description: 'Create environment role assignment. Creates a new role assignment for the specified environment. Preview. '
locale: en-us
document_id: 6566223f-acf2-8fcd-4adc-5e4b143f8d69
document_version_independent_id: 925954bd-889b-30d3-0217-3c753570f57e
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Create-Environment-Role-Assignment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/create-environment-role-assignment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Create-Environment-Role-Assignment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 10057839-ae1b-46e6-efb6-2b80757f42de
---

# Role Based Access Control - Create Environment Role Assignment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create environment role assignment. Creates a new role assignment for the specified environment. Preview.

```http
POST https://api.powerplatform.com/authorization/environments/{environmentId}/roleAssignments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| principalObjectId | string | The ID of the principal to assign |
| principalType | string | The type of the principal |
| roleDefinitionId | string | The ID of the role definition |
| scope | string | The assignment scope |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 201 Created | RoleAssignmentResponse | Role assignment created. |
| 400 Bad Request |  | Bad Request - The body is invalid. |
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
| RoleAssignmentRequest | Request to assign a role to a principal. |
| RoleAssignmentResponse | The role assignments. |
| Value |  |

### RoleAssignmentRequest

Object

Request to assign a role to a principal.

| Name | Type | Description |
| --- | --- | --- |
| principalObjectId | string | The ID of the principal to assign |
| principalType | string | The type of the principal |
| roleDefinitionId | string | The ID of the role definition |
| scope | string | The assignment scope |

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