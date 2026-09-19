---
layout: Reference
title: Websites - Get Affected Sites - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-affected-sites
uid: api.powerplatform.com.power-platform.powerpages.websites.getaffectedsites
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
description: Lists the websites affected by an exception scenario for a tenant. Lists the websites in the tenant affected by an exception scenario, with each site's existing
locale: en-us
document_id: cf527c6c-d899-ff1a-7ac4-a9c1d9aa13b1
document_version_independent_id: aecfe78d-27db-5148-60e3-81b425ebfa00
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-Affected-Sites.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-affected-sites
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-Affected-Sites.yml
platformId: 77d2f1b6-1ece-8bc9-5833-8905474e6f2a
---

# Websites - Get Affected Sites

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Lists the websites affected by an exception scenario for a tenant. Lists the websites in the tenant affected by an exception scenario, with each site's existing grant state, so an admin can review and select sites before granting.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/exceptions/affectedSites?exceptionType=WebApiStarRetirement&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| exceptionType | query | True | string | The exception scenario discriminator, e.g. "WebApiStarRetirement". |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AffectedSitesResult | OK |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |
| 403 Forbidden | ErrorMessage | Forbidden |
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
| AffectedSite |  |
| AffectedSitesResult |  |
| Details |  |
| Error |  |
| ErrorMessage |  |
| ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |

### AffectedSite

Object

| Name | Type | Description |
| --- | --- | --- |
| detail | string | Scenario-specific detail of why the website is affected. |
| expirationDate | string (date-time) | Expiry of the existing grant, when one exists (null otherwise). |
| grantStatus | string | Existing grant state for this website and exception type ("None" when no grant exists, otherwise the derived lifecycle status). |
| portalId | string | Website unique identifier (ID). |
| portalName | string | Friendly website name (may be null when not resolvable). |
| portalUrl | string | Website URL (may be null when not resolvable). |
| ppacUrl | string | Deep link to this website's settings page in the Power Platform admin center (may be null when the base URL is not configured). |
| siteType | string | Site type ("Production" or "Trial"). |

### AffectedSitesResult

Object

| Name | Type | Description |
| --- | --- | --- |
| exceptionType | ExceptionType | Exception scenario discriminator identifying which admin exception ("break-glass") scenario a grant, revoke, or query targets. |
| sites | AffectedSite[] | The affected websites. |
| totalCount | integer (int32) | Number of affected sites. |

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