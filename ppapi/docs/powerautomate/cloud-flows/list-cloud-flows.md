---
layout: Reference
title: Cloud Flows - List Cloud Flows - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerautomate/cloud-flows/list-cloud-flows
uid: api.powerplatform.com.power-platform.powerautomate.cloudflows.listcloudflows
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
description: 'Learn more about Power Platform API service - Retrieve cloud flows with filters. Returns a list of cloud flows. '
locale: en-us
document_id: 21130cde-1fd6-c6ae-3c88-c8a1251b352e
document_version_independent_id: 48b73139-60af-f647-2358-ca1eb29f5e54
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerautomate/Cloud-Flows/List-Cloud-Flows.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerautomate/cloud-flows/list-cloud-flows
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerautomate/Cloud-Flows/List-Cloud-Flows.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 3a4c112a-b808-68f5-9e46-2da65537fa98
---

# Cloud Flows - List Cloud Flows

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Retrieve cloud flows with filters. Returns a list of cloud flows.

```http
GET https://api.powerplatform.com/powerautomate/environments/{environmentId}/cloudFlows?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/powerautomate/environments/{environmentId}/cloudFlows?workflowId={workflowId}&resourceId={resourceId}&createdBy={createdBy}&ownerId={ownerId}&createdOnStartDate={createdOnStartDate}&createdOnEndDate={createdOnEndDate}&modifiedOnStartDate={modifiedOnStartDate}&modifiedOnEndDate={modifiedOnEndDate}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| createdBy | query |  | string (uuid) | The creator Dataverse ID. |
| createdOnEndDate | query |  | string (date) | Filter for created on or before this date. |
| createdOnStartDate | query |  | string (date) | Filter for created on or after this date. |
| modifiedOnEndDate | query |  | string (date) | Filter for modified on or before this date. |
| modifiedOnStartDate | query |  | string (date) | Filter for modified on or after this date. |
| ownerId | query |  | string (uuid) | The owner Dataverse ID. |
| resourceId | query |  | string (uuid) | The resource ID. |
| workflowId | query |  | string (uuid) | The workflow ID. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | Successful request. One or more cloud flows were returned. |
| 204 No Content |  | No content. No matching cloud flows found. |
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