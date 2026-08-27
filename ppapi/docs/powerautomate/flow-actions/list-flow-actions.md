---
layout: Reference
title: Flow Actions - List Flow Actions - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerautomate/flow-actions/list-flow-actions
uid: api.powerplatform.com.power-platform.powerautomate.flowactions.listflowactions
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
description: 'Learn more about Power Platform API service - Retrieve flow actions with filters. Returns a list of flow actions. '
locale: en-us
document_id: 6a8e508e-5dff-2947-7ac3-fd61dd46732c
document_version_independent_id: 255e3be1-5457-f144-b996-d0bebe0211ad
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerautomate/Flow-Actions/List-Flow-Actions.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerautomate/flow-actions/list-flow-actions
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerautomate/Flow-Actions/List-Flow-Actions.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 487a5028-4872-b4ec-009b-039f281ab06d
---

# Flow Actions - List Flow Actions

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Retrieve flow actions with filters. Returns a list of flow actions.

```http
GET https://api.powerplatform.com/powerautomate/environments/{environmentId}/flowActions?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/powerautomate/environments/{environmentId}/flowActions?workflowId={workflowId}&parentProcessStageId={parentProcessStageId}&connector={connector}&isTrigger={isTrigger}&parameterName={parameterName}&parameterValue={parameterValue}&exact={exact}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| connector | query |  | string | The connector name. |
| exact | query |  | boolean | Use exact matching for parameterName and parameterValue. |
| isTrigger | query |  | boolean | Indicates if the action is a trigger. No filter if unset. |
| parameterName | query |  | string | A keyword to search within the parameter name field. |
| parameterValue | query |  | string | A keyword to search within the parameter value field. |
| parentProcessStageId | query |  | string (uuid) | The parent process stage ID. |
| workflowId | query |  | string (uuid) | The workflow ID. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | A list of flow actions matching the filters. |
| 204 No Content |  | No content. No matching flow actions found. |
| 400 Bad Request | ErrorResponse | Bad request. |
| 401 Unauthorized |  | Unauthorized. |
| 403 Forbidden |  | Forbidden. |
| 404 Not Found | ErrorResponse | Not found. Environment does not have a Microsoft Dataverse database. |
| 500 Internal Server Error |  | Internal server error. |

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
| Error |  |
| ErrorResponse | The error response object. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code for the failure type (e.g., BadRequest). |
| message | string | Description of the error. |

### ErrorResponse

Object

The error response object.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |