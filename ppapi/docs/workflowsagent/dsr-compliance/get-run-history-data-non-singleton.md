---
layout: Reference
title: Dsr Compliance - Get Run History Data Non Singleton - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-run-history-data-non-singleton
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getrunhistorydatanonsingleton
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
description: 'Get run history customer data for DSR export (environment-scoped). Returns run history data for a flow run in an environment. '
locale: en-us
document_id: ec119b71-79c7-edb9-67a9-f1219884c7d5
document_version_independent_id: 328dbdf1-3a10-9acc-1b03-03fe2755adeb
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Run-History-Data-Non-Singleton.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-run-history-data-non-singleton
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Run-History-Data-Non-Singleton.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
platformId: f7103137-022b-6958-a000-9532157fe559
---

# Dsr Compliance - Get Run History Data Non Singleton

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get run history customer data for DSR export (environment-scoped). Returns run history data for a flow run in an environment.

```http
GET https://api.powerplatform.com/workflowsagent/environments/{environmentId}/flows/{flowId}/runs/{runId}/runHistoryData?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/environments/{environmentId}/flows/{flowId}/runs/{runId}/runHistoryData?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| flowId | path | True | string (uuid) | The flow ID. |
| runId | path | True | string | The run ID. |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | Base64-encoded continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrPagedResponse | Successful request. Run history data returned. |
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