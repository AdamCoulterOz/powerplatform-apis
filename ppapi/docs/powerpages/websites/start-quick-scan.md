---
layout: Reference
title: Websites - Start Quick Scan - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/start-quick-scan
uid: api.powerplatform.com.power-platform.powerpages.websites.startquickscan
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
description: 'Learn more about Power Platform API service - Execute quick scan for a Power Pages website. Execute a quick scan for a Power Pages website. '
locale: en-us
document_id: 23a47d3a-3396-8222-5fd8-f7ab7051141a
document_version_independent_id: 04c807b7-0750-95a1-a782-4f0ac575a804
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Start-Quick-Scan.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/start-quick-scan
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Start-Quick-Scan.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
platformId: 5a4df591-5e96-53fa-7282-3f4741f07711
---

# Websites - Start Quick Scan

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Execute quick scan for a Power Pages website. Execute a quick scan for a Power Pages website.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/scan/quick/execute?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/scan/quick/execute?lcid={lcid}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| lcid | query |  | string | Language code identifier (LCID) for the website. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | PortalScanIssues[] | Success |
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
| PortalScanIssues |  |

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

### PortalScanIssues

Object

| Name | Type | Description |
| --- | --- | --- |
| category | enum:<br>- Configuration Issues<br>- Performance<br>- Portal Startup Issue<br>- Provisioning issues<br>- Security | The category of the issue |
| description | string | Detailed description of the issue |
| issue | string | The specific issue identified |
| learnMoreUrl | string (uri) | URL for more information about the issue |
| result | enum:<br>- Error<br>- Pass<br>- Warning | The result of the issue check |