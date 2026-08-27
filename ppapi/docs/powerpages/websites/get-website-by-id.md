---
layout: Reference
title: Websites - Get Website By Id - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-website-by-id
uid: api.powerplatform.com.power-platform.powerpages.websites.getwebsitebyid
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
description: 'Get the Power Pages website details by specifying its unique identifier (ID). Get website details using a specified website ID. '
locale: en-us
document_id: 39f36f01-0378-9c83-8863-100e6ed1bcca
document_version_independent_id: e45d9456-beb2-73e5-3736-009b2ed320ca
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-Website-By-Id.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-website-by-id
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-Website-By-Id.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/1433a524-c01f-4b87-beab-670c040dea4f
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/312f1f05-a431-4193-8a4d-e6245d5966de
platformId: cd5dbb66-ce41-c65f-52cc-ddbd5fad80ec
---

# Websites - Get Website By Id

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the Power Pages website details by specifying its unique identifier (ID). Get website details using a specified website ID.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | WebsiteDto | Success |
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
| WebsiteDto |  |

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

### WebsiteDto

Object

| Name | Type | Description |
| --- | --- | --- |
| applicationUserAadAppId | string | Entra ID (formerly Azure Active Directory) object unique identifier (ID) |
| createdOn | string | Website creation time in the ISO 8601 UTC format |
| customHostNames | string[] | Custom hostnames added for the website |
| dataverseInstanceUrl | string | Organization URL of the website |
| dataverseOrganizationId | string | Organization unique identifier (ID) of the website |
| environmentId | string | Environment unique identifier (ID) of the website |
| environmentName | string | Environment name of the website |
| id | string | Website unique identifier (ID) |
| isCustomErrorEnabled | boolean | Custom error enablement for Website |
| isEarlyUpgradeEnabled | boolean | Website eligibility for early upgrade |
| name | string | Website name |
| ownerId | string | User unique identifier (ID) of the website owner |
| packageInstallStatus | enum:<br>- InstallFailed<br>- InstallRequested<br>- InstallRetrying<br>- InstallScheduled<br>- Installed<br>- Installing<br>- None<br>- TemplateInstalled<br>- UninstallFailed<br>- UninstallRequested<br>- Uninstalled<br>- Uninstalling | Package installation status of the website |
| packageVersion | string | Package version of the website |
| selectedBaseLanguage | integer (int32) | Language ID - https://go.microsoft.com/fwlink/?linkid=2208135 |
| siteVisibility | enum:<br>- private<br>- public | Website visibility status |
| status | enum:<br>- OperationComplete<br>- OperationFailed<br>- OperationInProgress<br>- OperationNotStarted | Website status |
| subdomain | string | Subdomain of website |
| suspendedWebsiteDeletingInDays | integer (int32) | Time (in days) to website deletion, if suspended |
| templateName | enum:<br>- DefaultPortalTemplate<br>- PowerPortals\_BookMeeting<br>- PowerPortals\_ProgramRegistration | Website template name |
| tenantId | string | Tenant unique identifier (ID) of the website |
| trialExpiringInDays | integer (int32) | Time (in days) to expiration of the website |
| type | enum:<br>- Production<br>- Trial | Application type of the website |
| websiteRecordId | string | Dataverse record unique identifier (ID) of the website |
| websiteUrl | string | Website URL |