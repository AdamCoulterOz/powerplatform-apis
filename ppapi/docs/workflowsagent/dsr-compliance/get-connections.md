---
layout: Reference
title: Dsr Compliance - Get Connections - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-connections
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getconnections
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
description: 'Learn more about Power Platform API service - Get connections for DSR export. Returns user connections for DSR compliance export. '
locale: en-us
document_id: 80657afc-6761-23f7-5d71-ed15e0c0821b
document_version_independent_id: 764f0be4-2071-9ea5-967f-72ea201a38d7
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Connections.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-connections
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Connections.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5e3dbb3b-f7d2-c5c5-40a9-ded81fd90fc8
---

# Dsr Compliance - Get Connections

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get connections for DSR export. Returns user connections for DSR compliance export.

```http
GET https://api.powerplatform.com/workflowsagent/connections?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/connections?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | Continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrPagedResponse | Successful request. Connections returned. |
| 400 Bad Request |  | Bad request. |
| 401 Unauthorized |  | Unauthorized. |
| 404 Not Found |  | Not found. M365 Copilot workflows environment could not be resolved. |
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