---
layout: Reference
title: Role Based Access Control - Search Environment Role Assignments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/authorization/role-based-access-control/search-environment-role-assignments
uid: api.powerplatform.com.power-platform.authorization.rolebasedaccesscontrol.searchenvironmentroleassignments
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
description: Search environment role assignments. Searches role assignments for the specified environment, with optional transitive lookup up to parent scopes or down into n
locale: en-us
document_id: 30d39575-a2ae-cefc-63db-74e42aefbe4e
document_version_independent_id: 61031991-c639-7d79-1c50-5118cef6fd17
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Search-Environment-Role-Assignments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/authorization/role-based-access-control/search-environment-role-assignments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/authorization/Role-Based-Access-Control/Search-Environment-Role-Assignments.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/12ed19f9-ebdf-4c8a-8bcd-7a681836774d
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/3a764584-4f97-452b-8f1d-36f19b12f6ae
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 49d6f558-5f4d-653e-e1ad-de0496721e19
---

# Role Based Access Control - Search Environment Role Assignments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Search environment role assignments. Searches role assignments for the specified environment, with optional transitive lookup up to parent scopes or down into nested scopes. Preview.

```http
POST https://api.powerplatform.com/authorization/environments/{environmentId}/listRoleAssignments?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/authorization/environments/{environmentId}/listRoleAssignments?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The unique identifier of the environment. |
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
| 200 OK | SearchRoleAssignmentsResponse | A page of role assignments for the environment matching the search filters. |
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