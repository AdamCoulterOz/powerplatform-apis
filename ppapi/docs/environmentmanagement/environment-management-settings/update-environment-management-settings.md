---
layout: Reference
title: Environment Management Settings - Update Environment Management Settings - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-management-settings/update-environment-management-settings
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentmanagementsettings.updateenvironmentmanagementsettings
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
description: 'Learn more about Power Platform API service - Update fields on the environment management setting. '
locale: en-us
document_id: c1cd7d41-e632-4e70-98fe-646c6c762ebf
document_version_independent_id: ed679d58-05f2-c864-a842-3fdd5bb753f2
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Management-Settings/Update-Environment-Management-Settings.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-management-settings/update-environment-management-settings
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Management-Settings/Update-Environment-Management-Settings.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 3140100a-b9e9-916c-cec7-f05c95d0b94d
---

# Environment Management Settings - Update Environment Management Settings

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update fields on the environment management setting.

```http
PATCH https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/settings?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID for the environment management setting being updated. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | OperationResponse | OK<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| 404 Not Found | OperationResponse | Not Found<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| Other Status Codes | OperationResponse | Conflict<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| Other Status Codes | OperationResponse | Precondition Failed<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |

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
| EnvironmentServiceErrorResponse |  |
| ErrorDetail |  |
| OperationResponse | Represents the response object for APIs in this service. |

### EnvironmentServiceErrorResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| details | ErrorDetail[] |  |
| message | string |  |

### ErrorDetail

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| message | string |  |
| target | string |  |
| value | string |  |

### OperationResponse

Object

Represents the response object for APIs in this service.

| Name | Type | Description |
| --- | --- | --- |
| debugErrors | string | Gets or sets debug errors, that are only shown for private/local testing |
| errors | EnvironmentServiceErrorResponse |  |
| nextLink | string (uri) | Gets or sets the next link if there are more records to be returned |
| objectResult | api.powerplatform.com.power-platform.environmentmanagement.environmentmanagementsettings.updateenvironmentmanagementsettings | Gets or sets the response's object |
| responseMessage | string | Gets or sets the error message. |