---
layout: Reference
title: Dsr Compliance - Delete Approval - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/delete-approval
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.deleteapproval
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
description: 'Delete an approval for DSR compliance. Deletes an approval and associated records for DSR compliance. '
locale: en-us
document_id: 38863b53-2faa-f5a0-2c36-1f593a4258a2
document_version_independent_id: d4e8415c-7fea-b7d8-1fd7-e1c6b36a52e4
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Delete-Approval.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/delete-approval
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Delete-Approval.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 7624c204-2292-e29b-6a5c-4f451de96c52
---

# Dsr Compliance - Delete Approval

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete an approval for DSR compliance. Deletes an approval and associated records for DSR compliance.

```http
DELETE https://api.powerplatform.com/workflowsagent/approvals/{approvalId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| approvalId | path | True | string (uuid) | The approval ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | Successfully deleted. |
| 400 Bad Request |  | Bad request. Approval ID is not a valid GUID. |
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