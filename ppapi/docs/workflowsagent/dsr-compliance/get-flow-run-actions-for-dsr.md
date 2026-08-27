---
layout: Reference
title: Dsr Compliance - Get Flow Run Actions For Dsr - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-flow-run-actions-for-dsr
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getflowrunactionsfordsr
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
description: 'Learn more about Power Platform API service - Get flow run actions for DSR export. Returns the action history for a specific flow run. '
locale: en-us
document_id: e3e49cde-982b-d16f-1509-f19c945ab5a7
document_version_independent_id: 9ca39c4b-8893-1592-0079-3a178774faf2
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Run-Actions-For-Dsr.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-flow-run-actions-for-dsr
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Flow-Run-Actions-For-Dsr.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 8081f637-f968-e3bd-d951-c1ab8ce1d0ae
---

# Dsr Compliance - Get Flow Run Actions For Dsr

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get flow run actions for DSR export. Returns the action history for a specific flow run.

```http
GET https://api.powerplatform.com/workflowsagent/aiFlows/{aiFlowId}/runs/{runId}/actions?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/aiFlows/{aiFlowId}/runs/{runId}/actions?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| aiFlowId | path | True | string | The workflow ID. |
| runId | path | True | string | The run ID. |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | integer (int64) | Byte offset continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrFlowRunsResponse | Successful request. Flow run action history returned.<br><br>Headers<br><br>Retry-After: string |
| 401 Unauthorized |  | Unauthorized. |
| 403 Forbidden |  | Forbidden. |
| 404 Not Found |  | Not found. Workflows environment not resolved or not enabled. |
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
| DsrFlowRunData | Action event data for a single flow run. |
| DsrFlowRunsResponse | Response containing flow run action history for DSR export. |

### DsrFlowRunData

Object

Action event data for a single flow run.

| Name | Type | Description |
| --- | --- | --- |
| actionEvents | ActionEvent[] | List of action events in the run. |
| runId | string | The run ID. |

### DsrFlowRunsResponse

Object

Response containing flow run action history for DSR export.

| Name | Type | Description |
| --- | --- | --- |
| flowId | string | The workflow ID. |
| nextLink | string | URL to retrieve the next page of results, if available. |
| value | DsrFlowRunData[] | List of flow run data entries. |