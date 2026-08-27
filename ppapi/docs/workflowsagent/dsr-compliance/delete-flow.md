---
layout: Reference
title: Dsr Compliance - Delete Flow - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/delete-flow
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.deleteflow
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
description: 'Delete a flow for DSR compliance. Deletes a flow in the M365 Copilot workflows environment for DSR compliance. '
locale: en-us
document_id: 5aad7b22-afb0-3bc0-7b78-36138b338943
document_version_independent_id: 237c38f0-0c32-c35e-cb27-bd534fd0f336
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Delete-Flow.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/delete-flow
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Delete-Flow.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: e3e2315d-c109-b3f4-66b5-dfdb7f94ba78
---

# Dsr Compliance - Delete Flow

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete a flow for DSR compliance. Deletes a flow in the M365 Copilot workflows environment for DSR compliance.

```http
DELETE https://api.powerplatform.com/workflowsagent/flows/{flowId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| flowId | path | True | string (uuid) | The flow ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | Successfully deleted. |
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