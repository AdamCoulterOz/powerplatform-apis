---
layout: Reference
title: Role Based Access Control - Search Role Assignments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/search-role-assignments
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.searchroleassignments
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
description: 'Search role assignments. Searches role assignments by scope, principal, and permission, with optional transitive lookup up to parent scopes or down into nested '
locale: en-us
document_id: f9151eea-4988-0c75-d26d-9d51b81f68ae
document_version_independent_id: 35fe5084-cc26-e442-101f-41f0013fc49b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Search-Role-Assignments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/search-role-assignments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Search-Role-Assignments.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/12ed19f9-ebdf-4c8a-8bcd-7a681836774d
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/3a764584-4f97-452b-8f1d-36f19b12f6ae
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 90fd99e0-f6f8-40ec-cd96-41902ca04d0f
---

# Role Based Access Control - Search Role Assignments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Search role assignments. Searches role assignments by scope, principal, and permission, with optional transitive lookup up to parent scopes or down into nested scopes. Preview.

```http
POST https://api.powerplatform.com/authorization/listRoleAssignments?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/authorization/listRoleAssignments?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | The continuation token from a previous response, used to retrieve the next page of results. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| scope | True | string | The scope to filter role assignments by |
| expandEnvironmentClusters |  | boolean | Whether to include role assignments inherited from the environment cluster an environment belongs to |
| expandEnvironmentGroups |  | boolean | Whether to include role assignments inherited from the environment groups an environment belongs to |
| expandSecurityGroups |  | boolean | Whether to include role assignments inherited from the security groups the principal belongs to |
| includeNestedScopes |  | boolean | Whether to include role assignments from scopes nested under the provided scope |
| includeParentScopes |  | boolean | Whether to include role assignments from parent scopes up to the tenant |
| includeVirtualEntraRoleAssignments |  | boolean | Whether to include virtual role assignments granted through an Entra directory role |
| permission |  | string | The permission to filter by |
| principalObjectId |  | string | The ID of the principal to filter by |
| principalType |  | string | The type of the principal to filter by |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | SearchRoleAssignmentsResponse | A page of role assignments matching the search filters. |
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
| SearchRoleAssignmentsRequest | Request to search role assignments using scope, principal, and permission filters. |
| SearchRoleAssignmentsResponse | A page of role assignments matching the search filters. |
| Value |  |

### SearchRoleAssignmentsRequest

Object

Request to search role assignments using scope, principal, and permission filters.

| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| expandEnvironmentClusters | boolean | False | Whether to include role assignments inherited from the environment cluster an environment belongs to |
| expandEnvironmentGroups | boolean | False | Whether to include role assignments inherited from the environment groups an environment belongs to |
| expandSecurityGroups | boolean | False | Whether to include role assignments inherited from the security groups the principal belongs to |
| includeNestedScopes | boolean | False | Whether to include role assignments from scopes nested under the provided scope |
| includeParentScopes | boolean | False | Whether to include role assignments from parent scopes up to the tenant |
| includeVirtualEntraRoleAssignments | boolean | False | Whether to include virtual role assignments granted through an Entra directory role |
| permission | string |  | The permission to filter by |
| principalObjectId | string |  | The ID of the principal to filter by |
| principalType | string |  | The type of the principal to filter by |
| scope | string |  | The scope to filter role assignments by |

### SearchRoleAssignmentsResponse

Object

A page of role assignments matching the search filters.

| Name | Type | Description |
| --- | --- | --- |
| nextLink | string | The URL to retrieve the next page of results, or null if there are no more pages |
| value | Value[] |  |

### Value

Object

| Name | Type | Description |
| --- | --- | --- |
| permissions | string[] |  |
| roleDefinitionId | string | Role definition ID |
| roleDefinitionName | string | Role definition name |