---
layout: Reference
title: Finance And Operations Versions - Apply Fin Ops Version - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/dynamics/finance-and-operations-versions/apply-fin-ops-version
uid: api.powerplatform.com.power-platform.dynamics.financeandoperationsversions.applyfinopsversion
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
description: 'Apply a Finance and Operations version. Applies the specified Finance and Operations application version to an environment as a long-running operation. '
locale: en-us
document_id: b9d4c617-cf16-8c05-2819-154e25551fc6
document_version_independent_id: 5c480a9c-c1bc-743c-6544-4fe89c7e4327
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Versions/Apply-Fin-Ops-Version.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/dynamics/finance-and-operations-versions/apply-fin-ops-version
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Versions/Apply-Fin-Ops-Version.yml
platformId: 67e09e5e-525f-25f3-67a0-7c559f21f9af
---

# Finance And Operations Versions - Apply Fin Ops Version

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Apply a Finance and Operations version. Applies the specified Finance and Operations application version to an environment as a long-running operation.

```http
POST https://api.powerplatform.com/dynamics/environments/{environmentId}/finopsversions/{version}/apply?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string (uuid) | The unique identifier of the environment. |
| version | path | True | string | The Finance and Operations application version to apply (for example, 10.0.47.5). |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted | ApplyFinOpsVersionAcceptedResponse | The apply version operation was accepted and is being processed.<br><br>Headers<br><br>- Location: string<br>- Retry-After: integer |
| 204 No Content |  | No update was required because the environment is already at or above the requested version. |
| 400 Bad Request | FinOpsErrorResponse | Bad Request. |
| 401 Unauthorized | FinOpsErrorResponse | Unauthorized. |
| 403 Forbidden | FinOpsErrorResponse | Forbidden. |
| 404 Not Found | FinOpsErrorResponse | Not Found. |
| 500 Internal Server Error | FinOpsErrorResponse | Internal Server Error. |

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
| ApplyFinOpsVersionAcceptedResponse | Accepted response for a long-running apply version operation. |
| Error |  |
| FinOpsErrorResponse | Standard error response. |

### ApplyFinOpsVersionAcceptedResponse

Object

Accepted response for a long-running apply version operation.

| Name | Type | Description |
| --- | --- | --- |
| operationId | string | The identifier of the long-running operation to poll for status. |
| resourceId | string | The identifier of the environment resource the operation applies to. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### FinOpsErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |