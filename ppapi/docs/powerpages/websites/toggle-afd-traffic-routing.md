---
layout: Reference
title: Websites - Toggle AFD Traffic Routing - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/toggle-afd-traffic-routing
uid: api.powerplatform.com.power-platform.powerpages.websites.toggleafdtrafficrouting
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
description: Toggle AFD traffic routing for a Power Pages website. Toggles traffic routing between Azure Front Door and web apps for a portal.
locale: en-us
document_id: 28f34222-5a5e-95e1-202f-5279fd89634a
document_version_independent_id: ab80e7fd-a890-e765-f6fc-79635cc30295
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Toggle-AFD-Traffic-Routing.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/toggle-afd-traffic-routing
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Toggle-AFD-Traffic-Routing.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/b5e53e15-0a76-4936-b270-8b2badca62ac
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/7ebba99b-05c3-4387-8883-f7bbf6632cb8
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/6908a4c7-0b59-4f8b-a00e-59c83ae0a04a
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/006ab567-b18c-4cf1-9a25-c24daa46ede1
platformId: 1c5d380e-dd0e-27db-c7c1-95804f161062
---

# Websites - Toggle AFD Traffic Routing

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Toggle AFD traffic routing for a Power Pages website. Toggles traffic routing between Azure Front Door and web apps for a portal. When enableAFD is true, enables the AFD endpoint and adds service tag restrictions to web apps. When false, removes service tags and disables the AFD endpoint.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/toggleAFDTrafficRouting?enableAFD={enableAFD}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| enableAFD | query | True | boolean | True to enable AFD routing, false to disable. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ToggleAFDTrafficRoutingResponse | Success |
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
| ToggleAFDTrafficRoutingResponse |  |

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

### ToggleAFDTrafficRoutingResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| message | string | Result message describing the outcome of the toggle operation. |