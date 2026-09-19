---
layout: Reference
title: Websites - Grant Exception - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/grant-exception
uid: api.powerplatform.com.power-platform.powerpages.websites.grantexception
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
description: Grants an admin exception for one or more Power Pages websites in a tenant. Grants a break-glass admin exception (one-time per website and exception type) acros
locale: en-us
document_id: 3ff4778e-42dc-67a1-2af5-0977608cd006
document_version_independent_id: 940e73e4-054c-6ada-d47c-efeb41b6de02
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Grant-Exception.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/grant-exception
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Grant-Exception.yml
platformId: 42bfaecc-dbbd-148b-d0c8-6776d42b7bac
---

# Websites - Grant Exception

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Grants an admin exception for one or more Power Pages websites in a tenant. Grants a break-glass admin exception (one-time per website and exception type) across one or more websites in the tenant. Gating, validation, and audit/state writes are synchronous; application-setting propagation is queued asynchronously.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/exceptions/grant?api-version=2024-10-01
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
| portalIds | string[] | Websites the exception should be applied to (deduplicated server-side). |
| riskAcknowledged | boolean | Whether the admin explicitly acknowledged the risk. Must be true to proceed. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | GrantExceptionResult | OK |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |
| 403 Forbidden | ErrorMessage | Forbidden |
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
| GrantExceptionRequest |  |
| GrantExceptionResult |  |
| PortalExceptionResult |  |

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

### GrantExceptionRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| portalIds | string[] | Websites the exception should be applied to (deduplicated server-side). |
| riskAcknowledged | boolean | Whether the admin explicitly acknowledged the risk. Must be true to proceed. |

### GrantExceptionResult

Object

| Name | Type | Description |
| --- | --- | --- |
| exceptionId | string | Id of the audit record created for this grant request. |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| expirationDate | string (date-time) | Effective UTC expiry applied to every accepted website in this request. |
| portals | PortalExceptionResult[] | Per-website outcomes. |
| propagationOrchestrationId | string | Optional orchestration instance id for queued application-setting propagation. |

### PortalExceptionResult

Object

| Name | Type | Description |
| --- | --- | --- |
| message | string | Optional human-readable detail (populated for non-granted outcomes). |
| portalId | string | Website unique identifier (ID). |
| status | string | Per-website outcome status, e.g. "Granted", "Accepted", "AlreadyGranted", "NotApplicable", "Failed", "Revoked", "AlreadyRevoked". |