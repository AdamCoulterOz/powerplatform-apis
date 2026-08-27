---
layout: Reference
title: Websites - Delete Ssl Binding By Thumbprint - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/delete-ssl-binding-by-thumbprint
uid: api.powerplatform.com.power-platform.powerpages.websites.deletesslbindingbythumbprint
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
description: 'Delete SSL binding for a website by certificate thumbprint. Removes the SSL binding for the specified hostname and certificate thumbprint from the website. '
locale: en-us
document_id: 3bae6810-c1ff-77c6-6f92-14abbc5ac969
document_version_independent_id: 5bb93b78-f493-50bc-713a-e2f25c2d19d6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Delete-Ssl-Binding-By-Thumbprint.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/delete-ssl-binding-by-thumbprint
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Delete-Ssl-Binding-By-Thumbprint.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 7d9e3e86-e322-5c0f-5a38-450c3684ce47
---

# Websites - Delete Ssl Binding By Thumbprint

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete SSL binding for a website by certificate thumbprint. Removes the SSL binding for the specified hostname and certificate thumbprint from the website.

```http
DELETE https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/sslBindings?hostName={hostName}&thumbprint={thumbprint}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| hostName | query | True | string | The custom domain hostname whose SSL binding will be removed. |
| thumbprint | query | True | string | The thumbprint of the certificate to unbind. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | Success |
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