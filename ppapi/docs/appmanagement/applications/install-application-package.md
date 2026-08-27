---
layout: Reference
title: Applications - Install Application Package - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/appmanagement/applications/install-application-package
uid: api.powerplatform.com.power-platform.appmanagement.applications.installapplicationpackage
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
description: 'Start the install of application package in target environment. Installs an app package by unique name into a target environment. '
locale: en-us
document_id: 56eadfc0-4b42-fbf8-b16b-74ba1e9bd3e9
document_version_independent_id: acf35d02-85f6-80f6-5ac2-0c7510368cb8
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/appmanagement/Applications/Install-Application-Package.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/appmanagement/applications/install-application-package
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/appmanagement/Applications/Install-Application-Package.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 21993001-cff0-7b68-e732-921d7eb3b34e
---

# Applications - Install Application Package

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Start the install of application package in target environment. Installs an app package by unique name into a target environment.

```http
POST https://api.powerplatform.com/appmanagement/environments/{environmentId}/applicationPackages/{uniqueName}/install?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | Environment ID (not to be confused with the organization ID). |
| uniqueName | path | True | string | Package unique name. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| payloadValue | string |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | InstancePackage | Success |
| 202 Accepted |  | Success |
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
| ErrorDetails |  |
| InstancePackage |  |
| InstancePackageOperation |  |
| InstancePackageState | State of the instance package. |
| TpsInstallRequestPayload | Payload to be sent during installation of the package. |

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

### InstancePackage

Object

| Name | Type | Description |
| --- | --- | --- |
| applicationDescription | string | Application description associated with the instance package |
| applicationId | string (uuid) | Application ID associated with the instance package |
| applicationName | string | Application name associated with the instance package |
| applicationVisibility | ApplicationVisibility | Application visibility. |
| customHandleUpgrade | boolean | Custom handle upgrade flag for the application |
| id | string (uuid) | Instance package ID |
| lastOperation | InstancePackageOperation |  |
| learnMoreUrl | string | Learn more URL for the application |
| localizedDescription | string | Localized description of application |
| localizedName | string | Localized name of application |
| packageId | string (uuid) | Package ID |
| packageUniqueName | string | Package unique name. |
| packageVersion | string | Package version |
| publisherId | string (uuid) | Publisher ID |
| publisherName | string | Publisher name for the application |
| singlePageApplicationUrl | string | Single Page Application (SPA) URL |
| termsOfServiceBlobUris | string[] | Terms of service for the application |

### InstancePackageOperation

Object

| Name | Type | Description |
| --- | --- | --- |
| createdOn | string (date-time) | Date and time for creation of the instance package operation |
| errorDetails | ErrorDetails |  |
| instancePackageId | string (uuid) | Instance package ID |
| modifiedOn | string (date-time) | Date and time for modification of the instance package operation |
| operationId | string (uuid) | Operation ID for the operation triggered on the instance package |
| state | InstancePackageState | State of the instance package. |
| statusMessage | string | Status message |

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

### TpsInstallRequestPayload

Object

Payload to be sent during installation of the package.

| Name | Type | Description |
| --- | --- | --- |
| payloadValue | string |  |