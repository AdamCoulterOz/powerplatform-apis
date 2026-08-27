---
layout: Reference
title: Applications - Get Environment Application Package - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/appmanagement/applications/get-environment-application-package
uid: api.powerplatform.com.power-platform.appmanagement.applications.getenvironmentapplicationpackage
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
description: 'Get the list of application packages that are available for install. Lists available app packages for a target environment with OData filtering. '
locale: en-us
document_id: a26a0d31-3a85-a0db-7e3a-323e6d9a9551
document_version_independent_id: e15c5be9-5a0a-8291-cad5-255c0c26a112
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/appmanagement/Applications/Get-Environment-Application-Package.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/appmanagement/applications/get-environment-application-package
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/appmanagement/Applications/Get-Environment-Application-Package.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 959235d6-47ef-19e7-299a-c64a2a7efb36
---

# Applications - Get Environment Application Package

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the list of application packages that are available for install. Lists available app packages for a target environment with OData filtering.

```http
GET https://api.powerplatform.com/appmanagement/environments/{environmentId}/applicationPackages?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/appmanagement/environments/{environmentId}/applicationPackages?appInstallState={appInstallState}&lcid={lcid}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | Environment ID (not to be confused with Org ID). |
| api-version | query | True | string | The API version. |
| appInstallState | query |  | string | Application package install state. |
| lcid | query |  | string | Application package supported language ID. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ApplicationPackageContinuationResponse | Success |
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
| ApplicationPackage |  |
| ApplicationPackageContinuationResponse |  |
| ApplicationVisibility | Application visibility. |
| CatalogVisibility | Catalog visibility for the application. |
| ErrorDetails |  |
| InstancePackageState | State of the instance package. |

### ApplicationPackage

Object

| Name | Type | Description |
| --- | --- | --- |
| applicationDescription | string | Application description |
| applicationId | string (uuid) | Application ID |
| applicationName | string | Application name |
| applicationVisibility | ApplicationVisibility | Application visibility. |
| catalogVisibility | CatalogVisibility | Catalog visibility for the application. |
| customHandleUpgrade | boolean | Available package custom upgrade |
| endDateUtc | string (date-time) | End date for application package |
| id | string (uuid) | Package or instance package ID that maps to the app package ID |
| instancePackageId | string (uuid) | Instance package ID used only for install retry (e.g., reinstall). |
| lastError | ErrorDetails |  |
| learnMoreUrl | string | Learn more URL for the application |
| localizedDescription | string <br>maxLength: 1000 | Localized description for the application package |
| localizedName | string | Localized name of application package |
| platformMaxVersion | string | Available package platform maximum version |
| platformMinVersion | string | Available package platform minimum version |
| publisherId | string (uuid) | Publisher ID |
| publisherName | string | Publisher name |
| singlePageApplicationUrl | string | Single Page Application (SPA) URL associated with the application |
| startDateUtc | string (date-time) | Start date for application package |
| state | InstancePackageState | State of the instance package. |
| supportedCountries | string[] | List of supported countries/regions for the application |
| uniqueName | string | Available package unique name or instance package unique name |
| version | string | Available package version or instance package version |

### ApplicationPackageContinuationResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | ApplicationPackage[] |  |

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

### InstancePackageState

Enumeration

State of the instance package.

| Value | Description |
| --- | --- |
| None |  |
| Installed |  |
| Uninstalled |  |
| InstallRequested |  |
| UninstallRequested |  |
| InstallFailed |  |
| UninstallFailed |  |
| Installing |  |
| Uninstalling |  |
| InstallScheduled |  |
| InstallRetrying |  |
| TemplateInstalled |  |