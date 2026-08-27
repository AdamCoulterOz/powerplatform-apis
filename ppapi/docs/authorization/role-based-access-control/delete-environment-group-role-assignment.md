---
layout: Reference
title: Role Based Access Control - Delete Environment Group Role Assignment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/delete-environment-group-role-assignment
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.deleteenvironmentgrouproleassignment
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
description: 'Delete environment group role assignment. Deletes a role assignment by ID for the specified environment group. Preview. '
locale: en-us
document_id: 5615b0f7-8b81-ed91-2ba7-ba913d6b6c83
document_version_independent_id: 9775d750-88d8-3cc6-4f7d-b3c9a026ed05
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Delete-Environment-Group-Role-Assignment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/delete-environment-group-role-assignment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Delete-Environment-Group-Role-Assignment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: abd428fc-290c-3234-491d-9e9665317dbc
---

# Role Based Access Control - Delete Environment Group Role Assignment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete environment group role assignment. Deletes a role assignment by ID for the specified environment group. Preview.

```http
DELETE https://api.powerplatform.com/authorization/environmentGroups/{environmentGroupId}/roleAssignments/{roleAssignmentId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentGroupId | path | True | string | The unique identifier of the environment group. |
| roleAssignmentId | path | True | string | The unique identifier of the role assignment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | Role assignment deleted successfully. |
| 400 Bad Request |  | Bad Request - The parameters are invalid. |
| 401 Unauthorized |  | Unauthorized - Invalid credentials or missing authentication. |
| 404 Not Found |  | Not Found - The role assignment does not exist. |
| 500 Internal Server Error |  | Internal Server Error - Unexpected server error. |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |