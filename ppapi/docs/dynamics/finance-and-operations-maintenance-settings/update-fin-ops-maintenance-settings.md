---
layout: Reference
title: Finance And Operations Maintenance Settings - Update Fin Ops Maintenance Settings - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/dynamics/finance-and-operations-maintenance-settings/update-fin-ops-maintenance-settings
uid: api.powerplatform.com.power-platform.dynamics.financeandoperationsmaintenancesettings.updatefinopsmaintenancesettings
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
description: 'Update Finance and Operations Maintenance Settings. Updates the F&O maintenance settings for an environment managed by Power Platform admin center. '
locale: en-us
document_id: 72e90887-48de-428f-2854-b6cf6eed921f
document_version_independent_id: 7a68d15c-18e6-adac-86f5-da00bb51c852
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Maintenance-Settings/Update-Fin-Ops-Maintenance-Settings.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/dynamics/finance-and-operations-maintenance-settings/update-fin-ops-maintenance-settings
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/dynamics/Finance-And-Operations-Maintenance-Settings/Update-Fin-Ops-Maintenance-Settings.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/410e33a0-5420-48ba-a8e2-7fb3dc6a9163
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/437f62ae-23a5-4ffc-9ff2-ac42acc41d76
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 88c82eb8-d3e5-58b4-4679-d7661e20f91e
---

# Finance And Operations Maintenance Settings - Update Fin Ops Maintenance Settings

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update Finance and Operations Maintenance Settings. Updates the F&O maintenance settings for an environment managed by Power Platform admin center.

```http
PUT https://api.powerplatform.com/dynamics/environments/{environmentId}/finopsadminsettings?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string (uuid) | The unique identifier of the environment. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| updatedMaintenanceWindowCadence | FinOpsUpdateCadence | Cadence for major version application updates. |
| updatedMaintenanceWindowDaysOfWeek | FinOpsDayOfWeek[] | The updated maintenance window days of the week. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | FinOpsAdminSettingsResponse | Successfully updated Finance and Operations Maintenance. |
| 400 Bad Request | FinOpsErrorResponse | Bad Request. |
| 401 Unauthorized | FinOpsErrorResponse | Unauthorized. |
| 403 Forbidden | FinOpsErrorResponse | Forbidden. |
| 404 Not Found | FinOpsErrorResponse | Not Found. |
| 500 Internal Server Error | FinOpsErrorResponse | Internal Server Error. |

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
| Error |  |
| FinOpsAdminSettingsResponse | Finance and Operations Maintenance response. |
| FinOpsDayOfWeek | Day of the week (aligned with .NET System.DayOfWeek enum). |
| FinOpsErrorResponse | Standard error response. |
| FinOpsUpdateCadence | Cadence for major version application updates. |
| UpdateFinOpsAdminSettingsRequestBody | Request body for updating Finance and Operations Maintenance. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### FinOpsAdminSettingsResponse

Object

Finance and Operations Maintenance response.

| Name | Type | Description |
| --- | --- | --- |
| maintenanceWindowCadence | FinOpsUpdateCadence | Cadence for major version application updates. |
| maintenanceWindowDaysOfWeek | FinOpsDayOfWeek[] | The preferred days of week for RunOne Updates. |

### FinOpsDayOfWeek

Enumeration

Day of the week (aligned with .NET System.DayOfWeek enum).

| Value | Description |
| --- | --- |
| Sunday |  |
| Monday |  |
| Tuesday |  |
| Wednesday |  |
| Thursday |  |
| Friday |  |
| Saturday |  |

### FinOpsErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### FinOpsUpdateCadence

Enumeration

Cadence for major version application updates.

| Value | Description |
| --- | --- |
| EveryUpdate |  |
| EveryOtherUpdate |  |
| Regulated |  |

### UpdateFinOpsAdminSettingsRequestBody

Object

Request body for updating Finance and Operations Maintenance.

| Name | Type | Description |
| --- | --- | --- |
| updatedMaintenanceWindowCadence | FinOpsUpdateCadence | Cadence for major version application updates. |
| updatedMaintenanceWindowDaysOfWeek | FinOpsDayOfWeek[] | The updated maintenance window days of the week. |