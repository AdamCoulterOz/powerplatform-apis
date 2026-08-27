---
layout: Reference
title: Websites - Get Certificates By Portal - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-certificates-by-portal
uid: api.powerplatform.com.power-platform.powerpages.websites.getcertificatesbyportal
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
description: 'Get certificates associated with a website. Returns the list of certificates associated with the specified website, filtered by certificate type. '
locale: en-us
document_id: 42b5f7f4-d338-e4da-55ab-815104c5ead2
document_version_independent_id: b932ad58-53f2-a360-0255-f26dffa849e1
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-Certificates-By-Portal.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-certificates-by-portal
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-Certificates-By-Portal.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 80f133c6-c17b-5c63-f833-35105f7b2fe5
---

# Websites - Get Certificates By Portal

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get certificates associated with a website. Returns the list of certificates associated with the specified website, filtered by certificate type.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/certificates?certType={certType}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| certType | query | True | string | The type of certificate to retrieve. Allowed values: SSL, MANAGED. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | CertificateDTO[] | Success |
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
| CertificateDTO |  |
| Details |  |
| Error |  |
| ErrorMessage |  |

### CertificateDTO

Object

| Name | Type | Description |
| --- | --- | --- |
| ExpirationDate | string (date-time) | The expiration date of the certificate. |
| Location | string | The Azure region where the certificate is stored. |
| SubjectName | string | The subject name of the certificate. |
| Thumbprint | string | The thumbprint of the certificate. |
| Type | string | The type of the certificate (e.g., SSL, MANAGED, AZURE\_MANAGED). |

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