---
layout: Reference
title: Dsr Compliance - Get Flow Runs Non Singleton - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-flow-runs-non-singleton
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getflowrunsnonsingleton
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
description: 'Get flow runs for DSR export (environment-scoped). Returns flow run records for a flow in an environment. '
locale: en-us
document_id: beff7fb2-98d9-5371-5620-09f968114956
document_version_independent_id: 1e68a2d2-a821-de79-1a16-dd7370fee7e1
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Runs-Non-Singleton.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-flow-runs-non-singleton
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Runs-Non-Singleton.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: b6bcc141-f662-d8ea-9e55-faa53a9a85fc
---

# Dsr Compliance - Get Flow Runs Non Singleton

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get flow runs for DSR export (environment-scoped). Returns flow run records for a flow in an environment.

```http
GET https://api.powerplatform.com/workflowsagent/environments/{environmentId}/flows/{flowId}/flowRuns?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/environments/{environmentId}/flows/{flowId}/flowRuns?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| flowId | path | True | string (uuid) | The flow ID. |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | Continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrPagedResponse | Successful request. Flow runs returned. |
| 400 Bad Request |  | Bad request. |
| 401 Unauthorized |  | Unauthorized. |
| 404 Not Found |  | Not found. Specified environment could not be found. |
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

### DsrPagedResponse

Object

Generic paged response for DSR compliance APIs.

| Name | Type | Description |
| --- | --- | --- |
| nextLink | string | URL to retrieve the next page of results, if available. |
| value | object[] | Collection of records. Structure varies by resource type. |