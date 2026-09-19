---
layout: Reference
title: Websites - Get Websites - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-websites
uid: api.powerplatform.com.power-platform.powerpages.websites.getwebsites
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
description: 'Learn more about Power Platform API service - List Power Pages websites. Get a list of all the websites in your environment. '
locale: en-us
document_id: 37c8ca2f-c8a7-48e2-3255-d2324fa72a95
document_version_independent_id: 9e3375b3-084c-c340-f41a-41de193f2ad8
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-Websites.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-websites
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-Websites.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
- https://authoring-docs-microsoft.poolparty.biz/devrel/c1641ec8-45f4-44f8-96be-791a543c4e4e
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2433524-1328-496f-9385-a27d967008a9
platformId: c80d36de-ca5a-b7d5-aef6-97264679c214
---

# Websites - Get Websites

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List Power Pages websites. Get a list of all the websites in your environment.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites?skip={skip}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| skip | query |  | string | The number of items to skip before returning the remaining items. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ODataListWebsitesDto | Success |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |

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
| ODataListWebsitesDto |  |
| WebsiteDto |  |
| WebsiteTemplateName | Website template name. Supported templates, their display names, and template type:<br><br><br>| Template | Display Name | Template Type |<br>| --- | --- | --- |<br>| `StarterLayout1` | Starter Layout 1 | Power Pages |<br>| `StarterLayout2` | Starter Layout 2 | Power Pages |<br>| `StarterLayout3` | Starter Layout 3 | Power Pages |<br>| `StarterLayout4` | Starter Layout 4 | Power Pages |<br>| `StarterLayout5` | Starter Layout 5 | Power Pages |<br>| `BlankPage` | Blank Page | Power Pages |<br>| `BookMeetings` | Schedule and Manage Meetings | Power Pages |<br>| `DefaultPortalTemplate` | Starter Layout 1 | Power Pages |<br>| `PowerPortals_ProgramRegistration` | Program Registration | Power Pages |<br>| `PowerPortals_BookMeeting` | Schedule and Manage Meetings | Power Pages |<br>| `FAQ` | Frequently Asked Questions | Power Pages |<br>| `ProgramRegistration` | Program Registration | Power Pages |<br>| `BuildingPermit` | Application Processing | Power Pages |<br>| `Community` | Community | Dynamics 365 |<br>| `EventPortal` | Event Portal | Dynamics 365 |<br>| `CustomerSelfServicePortal` | Customer Self Service Portal | Dynamics 365 |<br>| `EmployeeSelfServicePortal` | Employee Self Service Portal | Dynamics 365 |<br>| `PartnerPortal` | Partner Portal | Dynamics 365 |<br>| `CustomerPortal` | Customer Portal | Dynamics 365 |<br>| `FieldService` | Field Service | Dynamics 365 | |
| --- | --- |

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

### ODataListWebsitesDto

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.metadata | string |  |
| @odata.nextLink | string |  |
| value | WebsiteDto[] |  |

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
| templateName | WebsiteTemplateName | Website template name. Supported templates, their display names, and template type:<br><br><br>| Template | Display Name | Template Type |<br>| --- | --- | --- |<br>| `StarterLayout1` | Starter Layout 1 | Power Pages |<br>| `StarterLayout2` | Starter Layout 2 | Power Pages |<br>| `StarterLayout3` | Starter Layout 3 | Power Pages |<br>| `StarterLayout4` | Starter Layout 4 | Power Pages |<br>| `StarterLayout5` | Starter Layout 5 | Power Pages |<br>| `BlankPage` | Blank Page | Power Pages |<br>| `BookMeetings` | Schedule and Manage Meetings | Power Pages |<br>| `DefaultPortalTemplate` | Starter Layout 1 | Power Pages |<br>| `PowerPortals_ProgramRegistration` | Program Registration | Power Pages |<br>| `PowerPortals_BookMeeting` | Schedule and Manage Meetings | Power Pages |<br>| `FAQ` | Frequently Asked Questions | Power Pages |<br>| `ProgramRegistration` | Program Registration | Power Pages |<br>| `BuildingPermit` | Application Processing | Power Pages |<br>| `Community` | Community | Dynamics 365 |<br>| `EventPortal` | Event Portal | Dynamics 365 |<br>| `CustomerSelfServicePortal` | Customer Self Service Portal | Dynamics 365 |<br>| `EmployeeSelfServicePortal` | Employee Self Service Portal | Dynamics 365 |<br>| `PartnerPortal` | Partner Portal | Dynamics 365 |<br>| `CustomerPortal` | Customer Portal | Dynamics 365 |<br>| `FieldService` | Field Service | Dynamics 365 | |
| --- | --- | --- |
| tenantId | string | Tenant unique identifier (ID) of the website |
| trialExpiringInDays | integer (int32) | Time (in days) to expiration of the website |
| type | enum:<br>- Production<br>- Trial | Application type of the website |
| websiteRecordId | string | Dataverse record unique identifier (ID) of the website |
| websiteUrl | string | Website URL |

### WebsiteTemplateName

Enumeration

Website template name. Supported templates, their display names, and template type:

| Template | Display Name | Template Type |
| --- | --- | --- |
| `StarterLayout1` | Starter Layout 1 | Power Pages |
| `StarterLayout2` | Starter Layout 2 | Power Pages |
| `StarterLayout3` | Starter Layout 3 | Power Pages |
| `StarterLayout4` | Starter Layout 4 | Power Pages |
| `StarterLayout5` | Starter Layout 5 | Power Pages |
| `BlankPage` | Blank Page | Power Pages |
| `BookMeetings` | Schedule and Manage Meetings | Power Pages |
| `DefaultPortalTemplate` | Starter Layout 1 | Power Pages |
| `PowerPortals_ProgramRegistration` | Program Registration | Power Pages |
| `PowerPortals_BookMeeting` | Schedule and Manage Meetings | Power Pages |
| `FAQ` | Frequently Asked Questions | Power Pages |
| `ProgramRegistration` | Program Registration | Power Pages |
| `BuildingPermit` | Application Processing | Power Pages |
| `Community` | Community | Dynamics 365 |
| `EventPortal` | Event Portal | Dynamics 365 |
| `CustomerSelfServicePortal` | Customer Self Service Portal | Dynamics 365 |
| `EmployeeSelfServicePortal` | Employee Self Service Portal | Dynamics 365 |
| `PartnerPortal` | Partner Portal | Dynamics 365 |
| `CustomerPortal` | Customer Portal | Dynamics 365 |
| `FieldService` | Field Service | Dynamics 365 |

| Value | Description |
| --- | --- |
| StarterLayout1 |  |
| StarterLayout2 |  |
| StarterLayout3 |  |
| StarterLayout4 |  |
| StarterLayout5 |  |
| BlankPage |  |
| BookMeetings |  |
| FAQ |  |
| ProgramRegistration |  |
| BuildingPermit |  |
| Community |  |
| EventPortal |  |
| CustomerSelfServicePortal |  |
| EmployeeSelfServicePortal |  |
| PartnerPortal |  |
| CustomerPortal |  |
| FieldService |  |
| DefaultPortalTemplate |  |
| PowerPortals\_ProgramRegistration |  |
| PowerPortals\_BookMeeting |  |