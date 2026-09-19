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
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
- https://authoring-docs-microsoft.poolparty.biz/devrel/c1641ec8-45f4-44f8-96be-791a543c4e4e
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2433524-1328-496f-9385-a27d967008a9
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
| templateName | True | WebsiteTemplateName | Website template name. Supported templates, their display names, and template type:<br><br><br>| Template | Display Name | Template Type |<br>| --- | --- | --- |<br>| `StarterLayout1` | Starter Layout 1 | Power Pages |<br>| `StarterLayout2` | Starter Layout 2 | Power Pages |<br>| `StarterLayout3` | Starter Layout 3 | Power Pages |<br>| `StarterLayout4` | Starter Layout 4 | Power Pages |<br>| `StarterLayout5` | Starter Layout 5 | Power Pages |<br>| `BlankPage` | Blank Page | Power Pages |<br>| `BookMeetings` | Schedule and Manage Meetings | Power Pages |<br>| `DefaultPortalTemplate` | Starter Layout 1 | Power Pages |<br>| `PowerPortals_ProgramRegistration` | Program Registration | Power Pages |<br>| `PowerPortals_BookMeeting` | Schedule and Manage Meetings | Power Pages |<br>| `FAQ` | Frequently Asked Questions | Power Pages |<br>| `ProgramRegistration` | Program Registration | Power Pages |<br>| `BuildingPermit` | Application Processing | Power Pages |<br>| `Community` | Community | Dynamics 365 |<br>| `EventPortal` | Event Portal | Dynamics 365 |<br>| `CustomerSelfServicePortal` | Customer Self Service Portal | Dynamics 365 |<br>| `EmployeeSelfServicePortal` | Employee Self Service Portal | Dynamics 365 |<br>| `PartnerPortal` | Partner Portal | Dynamics 365 |<br>| `CustomerPortal` | Customer Portal | Dynamics 365 |<br>| `FieldService` | Field Service | Dynamics 365 | |
| --- | --- | --- | --- |
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

### NewWebsiteRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| dataverseOrganizationId | string (uuid) | Dataverse organization's unique identifier (ID) |
| name | string | Name of the website |
| selectedBaseLanguage | integer (int32) | Language ID - https://go.microsoft.com/fwlink/?linkid=2208135 |
| subdomain | string | Subdomain for the website URL |
| templateName | WebsiteTemplateName | Website template name. Supported templates, their display names, and template type:<br><br><br>| Template | Display Name | Template Type |<br>| --- | --- | --- |<br>| `StarterLayout1` | Starter Layout 1 | Power Pages |<br>| `StarterLayout2` | Starter Layout 2 | Power Pages |<br>| `StarterLayout3` | Starter Layout 3 | Power Pages |<br>| `StarterLayout4` | Starter Layout 4 | Power Pages |<br>| `StarterLayout5` | Starter Layout 5 | Power Pages |<br>| `BlankPage` | Blank Page | Power Pages |<br>| `BookMeetings` | Schedule and Manage Meetings | Power Pages |<br>| `DefaultPortalTemplate` | Starter Layout 1 | Power Pages |<br>| `PowerPortals_ProgramRegistration` | Program Registration | Power Pages |<br>| `PowerPortals_BookMeeting` | Schedule and Manage Meetings | Power Pages |<br>| `FAQ` | Frequently Asked Questions | Power Pages |<br>| `ProgramRegistration` | Program Registration | Power Pages |<br>| `BuildingPermit` | Application Processing | Power Pages |<br>| `Community` | Community | Dynamics 365 |<br>| `EventPortal` | Event Portal | Dynamics 365 |<br>| `CustomerSelfServicePortal` | Customer Self Service Portal | Dynamics 365 |<br>| `EmployeeSelfServicePortal` | Employee Self Service Portal | Dynamics 365 |<br>| `PartnerPortal` | Partner Portal | Dynamics 365 |<br>| `CustomerPortal` | Customer Portal | Dynamics 365 |<br>| `FieldService` | Field Service | Dynamics 365 | |
| --- | --- | --- |
| websiteRecordId | string | Dataverse record unique identifier (ID) of the website |

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