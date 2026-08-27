---
layout: Reference
title: Environment Groups - Get Environment Group Operation - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-groups/get-environment-group-operation
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.getenvironmentgroupoperation
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
description: 'Learn more about Power Platform API service - Get operation status. '
locale: en-us
document_id: 00a50284-5a17-99e2-f011-461bf9a84192
document_version_independent_id: 9991e2d6-b1ac-ee00-a1e3-69f7eb375f49
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Get-Environment-Group-Operation.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-groups/get-environment-group-operation
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Groups/Get-Environment-Group-Operation.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: ed54efef-95dc-416e-99ad-81c8c3a61d6a
---

# Environment Groups - Get Environment Group Operation

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get operation status.

```http
GET https://api.powerplatform.com/environmentmanagement/environmentGroupOperations/{operationId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| operationId | path | True | string (uuid) | The operation ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | Success |
| 204 No Content |  | No Content |
| 400 Bad Request | ProblemDetails | Bad Request |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### ProblemDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| detail | string |  |
| extensions | api.powerplatform.com.power-platform.environmentmanagement.environmentgroups.getenvironmentgroupoperation |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |