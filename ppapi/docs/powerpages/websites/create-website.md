---
layout: Reference
title: Websites - Create Website - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/create-website
uid: api.powerplatform.com.power-platform.powerpages.websites.createwebsite
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
description: 'Learn more about Power Platform API service - Create a Power Pages website. Trigger the creation of a new website. '
locale: en-us
document_id: 86e77224-118b-92f0-b0a8-915adf9e8740
document_version_independent_id: 8523cd3f-8246-6e37-d685-a5577706c0fc
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Create-Website.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/create-website
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Create-Website.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/0ceb3227-2ff7-4d97-8e75-3d7b9ccc937a
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/4d680e1a-c470-4772-a236-5c714bd09be0
platformId: 99375bbd-e243-567f-6fea-509cd48e20e3
---

# Websites - Create Website

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create a Power Pages website. Trigger the creation of a new website.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| dataverseOrganizationId | True | string (uuid) | Dataverse organization's unique identifier (ID) |
| name | True | string | Name of the website |
| selectedBaseLanguage | True | integer (int32) | Language ID - https://go.microsoft.com/fwlink/?linkid=2208135 |
| subdomain | True | string | Subdomain for the website URL |
| templateName | True | enum:<br>- DefaultPortalTemplate<br>- PowerPortals\_ProgramRegistration<br>- PowerPortals\_BookMeeting | Website template name |
| websiteRecordId |  | string | Dataverse record unique identifier (ID) of the website |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted<br><br>Headers<br><br>Operation-Location: string |
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
| NewWebsiteRequest |  |

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

### NewWebsiteRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| dataverseOrganizationId | string (uuid) | Dataverse organization's unique identifier (ID) |
| name | string | Name of the website |
| selectedBaseLanguage | integer (int32) | Language ID - https://go.microsoft.com/fwlink/?linkid=2208135 |
| subdomain | string | Subdomain for the website URL |
| templateName | enum:<br>- DefaultPortalTemplate<br>- PowerPortals\_BookMeeting<br>- PowerPortals\_ProgramRegistration | Website template name |
| websiteRecordId | string | Dataverse record unique identifier (ID) of the website |