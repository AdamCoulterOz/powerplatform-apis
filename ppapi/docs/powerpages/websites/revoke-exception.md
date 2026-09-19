---
layout: Reference
title: Websites - Revoke Exception - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/revoke-exception
uid: api.powerplatform.com.power-platform.powerpages.websites.revokeexception
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
description: Revokes an admin exception for one or more Power Pages websites in a tenant. Revokes a previously granted admin exception across one or more websites in the ten
locale: en-us
document_id: 4d41e4b0-ce8b-1373-650a-766b120bb29a
document_version_independent_id: 35dd62cd-1397-42f8-5bbb-8c645c5c16cc
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Revoke-Exception.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/revoke-exception
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Revoke-Exception.yml
platformId: 40a497c6-5e2e-8cb5-128d-8893c459569a
---

# Websites - Revoke Exception

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Revokes an admin exception for one or more Power Pages websites in a tenant. Revokes a previously granted admin exception across one or more websites in the tenant. Each exception state row is force-expired and asynchronous application-setting revert is queued.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/exceptions/revoke?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| portalIds | string[] | Websites whose exception should be revoked (deduplicated server-side). |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RevokeExceptionResult | OK |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |
| 404 Not Found | ErrorMessage | Not Found |

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
| Details |  |
| Error |  |
| ErrorMessage |  |
| ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| PortalExceptionResult |  |
| RevokeExceptionRequest |  |
| RevokeExceptionResult |  |

### Details

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| message | string | Error message |
| target | string | Target parameter |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| details | Details[] |  |
| message | string | Error message |
| target | string | Target parameter |

### ErrorMessage

Object

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### ExceptionType

Enumeration

Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets.

| Value | Description |
| --- | --- |
| WebApiStarRetirement |  |

### PortalExceptionResult

Object

| Name | Type | Description |
| --- | --- | --- |
| message | string | Optional human-readable detail (populated for non-granted outcomes). |
| portalId | string | Website unique identifier (ID). |
| status | string | Per-website outcome status, e.g. "Granted", "Accepted", "AlreadyGranted", "NotApplicable", "Failed", "Revoked", "AlreadyRevoked". |

### RevokeExceptionRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| portalIds | string[] | Websites whose exception should be revoked (deduplicated server-side). |

### RevokeExceptionResult

Object

| Name | Type | Description |
| --- | --- | --- |
| auditId | string | Id of the audit record created for this revoke request. |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| portals | PortalExceptionResult[] | Per-website outcomes. |
| propagationOrchestrationId | string | Optional orchestration instance id for the queued application-setting revert propagation. |