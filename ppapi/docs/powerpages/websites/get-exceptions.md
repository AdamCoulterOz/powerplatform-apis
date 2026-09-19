---
layout: Reference
title: Websites - Get Exceptions - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-exceptions
uid: api.powerplatform.com.power-platform.powerpages.websites.getexceptions
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
description: "Lists the admin exceptions for a tenant. Lists the tenant's exception state rows (optionally filtered by exception type) with the derived lifecycle status. "
locale: en-us
document_id: 1e7314f9-649c-af82-0e12-ec49fa7a26c8
document_version_independent_id: ed75da75-2d63-c7aa-477f-0febfc6d9ad5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-Exceptions.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-exceptions
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-Exceptions.yml
platformId: 0ec08f57-b886-c3c2-c05b-6472637d385d
---

# Websites - Get Exceptions

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Lists the admin exceptions for a tenant. Lists the tenant's exception state rows (optionally filtered by exception type) with the derived lifecycle status.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/exceptions/list?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/exceptions/list?exceptionType=WebApiStarRetirement&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| exceptionType | query |  | string | Optional exception scenario discriminator to filter by, e.g. "WebApiStarRetirement". |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ExceptionView[] | OK |
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
| ExceptionView |  |

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

### ExceptionView

Object

| Name | Type | Description |
| --- | --- | --- |
| created | string (date-time) | UTC time the exception was created. |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| expirationDate | string (date-time) | UTC expiry of the exception. |
| portalId | string | Website unique identifier (ID). |
| status | string | Derived lifecycle status of the exception. |