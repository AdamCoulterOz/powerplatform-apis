---
layout: Reference
title: Applications - Get Application Package Install Status - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/appmanagement/applications/get-application-package-install-status
uid: api.powerplatform.com.power-platform.appmanagement.applications.getapplicationpackageinstallstatus
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
description: 'Get the polling status for a previously triggered installation. Gets install progress for an operation by its operation ID. '
locale: en-us
document_id: f48a8b34-e046-8bb5-d545-1c76df4f4afa
document_version_independent_id: 0089cc56-387e-3311-ff76-029d50c88b66
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/appmanagement/Applications/Get-Application-Package-Install-Status.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/appmanagement/applications/get-application-package-install-status
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/appmanagement/Applications/Get-Application-Package-Install-Status.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 8867a102-3279-69c6-ea7a-033d2c699f6e
---

# Applications - Get Application Package Install Status

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the polling status for a previously triggered installation. Gets install progress for an operation by its operation ID.

```http
GET https://api.powerplatform.com/appmanagement/environments/{environmentId}/operations/{operationId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | Environment ID (not to be confused with organization ID). |
| operationId | path | True | string (uuid) | Operation ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | InstancePackageOperationPollingResponse | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |

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
| ErrorDetails |  |
| InstancePackageOperationPollingResponse |  |
| InstancePackageOperationStatus |  |

### ErrorDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| errorCode | integer (int32) | Error code from Dataverse |
| errorName | string | Error name |
| message | string | Error message |
| source | string | Source of the error |
| statusCode | integer (int32) | Status code for error |
| type | string | Error type |

### InstancePackageOperationPollingResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| createdDateTime | string (date-time) |  |
| error | ErrorDetails |  |
| lastActionDateTime | string (date-time) |  |
| operationId | string (uuid) |  |
| status | InstancePackageOperationStatus |  |
| statusMessage | string |  |

### InstancePackageOperationStatus

Enumeration

| Value | Description |
| --- | --- |
| NotStarted |  |
| Running |  |
| Succeeded |  |
| Failed |  |
| Canceled |  |