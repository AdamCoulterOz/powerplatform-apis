---
layout: Reference
title: Applications - Get Tenant Application Package - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/appmanagement/applications/get-tenant-application-package
uid: api.powerplatform.com.power-platform.appmanagement.applications.gettenantapplicationpackage
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
description: 'List the installable application packages for a tenant. Get the list of available application packages for a tenant. '
locale: en-us
document_id: 0d4d923c-cdaa-4c16-3a53-ec5c7e5b6249
document_version_independent_id: c0cc50d8-5528-d5f8-ffee-b53a2ca0ab62
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/appmanagement/Applications/Get-Tenant-Application-Package.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/appmanagement/applications/get-tenant-application-package
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/appmanagement/Applications/Get-Tenant-Application-Package.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 162cfa02-e2a4-ecb7-b11e-269ca815b412
---

# Applications - Get Tenant Application Package

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List the installable application packages for a tenant. Get the list of available application packages for a tenant.

```http
GET https://api.powerplatform.com/appmanagement/applicationPackages?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TenantApplicationPackageContinuationResponse | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |

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
| ApplicationVisibility | Application visibility. |
| CatalogVisibility | Catalog visibility for the application. |
| ErrorDetails |  |
| TenantApplicationPackage |  |
| TenantApplicationPackageContinuationResponse |  |

### ApplicationVisibility

Enumeration

Application visibility.

| Value | Description |
| --- | --- |
| None |  |
| CrmAdminCenter |  |
| BapAdminCenter |  |
| OneAdminCenter |  |
| All |  |

### CatalogVisibility

Enumeration

Catalog visibility for the application.

| Value | Description |
| --- | --- |
| None |  |
| AdminCenter |  |
| Teams |  |
| All |  |

### ErrorDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| errorCode | integer (int32) | Error code from Dataverse |
| errorName | string | Error name |
| message | string | Error message |
| source | string | Source of the error |
| statusCode | integer (int32) | Status code for error |
| type | string | Error type |

### TenantApplicationPackage

Object

| Name | Type | Description |
| --- | --- | --- |
| applicationDescription | string | Application description |
| applicationId | string (uuid) | Application ID |
| applicationName | string | Application name |
| applicationVisibility | ApplicationVisibility | Application visibility. |
| catalogVisibility | CatalogVisibility | Catalog visibility for the application. |
| lastError | ErrorDetails |  |
| learnMoreUrl | string | Learn more URL |
| localizedDescription | string | Localized description of the tenant application package |
| localizedName | string | Localized name |
| publisherId | string (uuid) | Publisher ID |
| publisherName | string | Publisher name |
| uniqueName | string | Unique name of the tenant application package |

### TenantApplicationPackageContinuationResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | TenantApplicationPackage[] |  |