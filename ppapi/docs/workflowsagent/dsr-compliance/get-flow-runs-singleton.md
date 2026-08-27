---
layout: Reference
title: Dsr Compliance - Get Flow Runs Singleton - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-flow-runs-singleton
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getflowrunssingleton
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
description: 'Learn more about Power Platform API service - Get flow runs for DSR export. Returns flow run records for a flow for DSR export. '
locale: en-us
document_id: ea531e6c-ea1e-3140-19f4-f3a5515391be
document_version_independent_id: 68b35c4e-244b-37dd-c4dd-9c185173960b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Runs-Singleton.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-flow-runs-singleton
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Runs-Singleton.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 03386b73-82c0-82fd-70e4-46b3f6d01925
---

# Dsr Compliance - Get Flow Runs Singleton

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get flow runs for DSR export. Returns flow run records for a flow for DSR export.

```http
GET https://api.powerplatform.com/workflowsagent/flows/{flowId}/flowRuns?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/flows/{flowId}/flowRuns?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| flowId | path | True | string (uuid) | The flow ID. |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | Continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrPagedResponse | Successful request. Flow runs returned. |
| 400 Bad Request |  | Bad request. Flow ID is not a valid GUID. |
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