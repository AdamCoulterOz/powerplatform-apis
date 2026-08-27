---
layout: Reference
title: Websites - List Ssl Bindings By Thumbprints - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/list-ssl-bindings-by-thumbprints
uid: api.powerplatform.com.power-platform.powerpages.websites.listsslbindingsbythumbprints
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
description: 'List SSL bindings for a website by hostname. Returns the SSL bindings (certificate thumbprints) associated with the specified hostname on the website. '
locale: en-us
document_id: d405333b-bf88-c9e4-2d76-9a4a9155692e
document_version_independent_id: 7cd1505b-8bc7-240e-95e1-58ab4945d36f
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/List-Ssl-Bindings-By-Thumbprints.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/list-ssl-bindings-by-thumbprints
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/List-Ssl-Bindings-By-Thumbprints.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c9645752-fc3b-47c1-4524-3b88dda8d22b
---

# Websites - List Ssl Bindings By Thumbprints

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List SSL bindings for a website by hostname. Returns the SSL bindings (certificate thumbprints) associated with the specified hostname on the website.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/sslBindings?hostName={hostName}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| hostName | query | True | string | The custom domain hostname to filter SSL bindings by. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | SslBindingThumbprintDTO[] | Success |
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
| SslBindingThumbprintDTO |  |

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

### SslBindingThumbprintDTO

Object

| Name | Type | Description |
| --- | --- | --- |
| Name | string | The custom hostname the SSL binding is associated with. |
| Thumbprint | string | The certificate thumbprint bound to the hostname. |