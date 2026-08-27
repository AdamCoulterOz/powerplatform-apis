---
layout: Reference
title: Storage Warnings - Get Storage Warning By Category - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/storage-warnings/get-storage-warning-by-category
uid: api.powerplatform.com.power-platform.licensing.storagewarnings.getstoragewarningbycategory
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
description: 'Learn more about Power Platform API service - Storage warning thresholds filtered by category. '
locale: en-us
document_id: 65cf2f3c-752c-f0a6-4201-27dd10c7f7ef
document_version_independent_id: 84b3cb0c-8d32-b308-cac4-2f7ca7ffe7e9
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Storage-Warnings/Get-Storage-Warning-By-Category.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/storage-warnings/get-storage-warning-by-category
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Storage-Warnings/Get-Storage-Warning-By-Category.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 71289372-8a11-d8cd-d6ba-3871d95c8316
---

# Storage Warnings - Get Storage Warning By Category

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Storage warning thresholds filtered by category.

```http
GET https://api.powerplatform.com/licensing/storageWarning/{storageCategory}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| storageCategory | path | True | string | The storage category value. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | StorageWarningThresholdsDocument[] | Success |
| 404 Not Found | LicensingProblemDetails | Not Found |

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
| LicensingProblemDetails |  |
| StorageWarningThresholds |  |
| StorageWarningThresholdsDocument |  |

### LicensingProblemDetails

Object

| Name | Type | Description |
| --- | --- | --- |
| detail | string |  |
| instance | string |  |
| status | integer (int32) |  |
| title | string |  |
| type | string |  |

### StorageWarningThresholds

Object

| Name | Type | Description |
| --- | --- | --- |
| storageCategory | string |  |
| storageEntity | string |  |
| thresholdInMB | integer (int32) |  |
| warningMessageConstKey | string |  |

### StorageWarningThresholdsDocument

Object

| Name | Type | Description |
| --- | --- | --- |
| isActive | boolean |  |
| storageCategory | string |  |
| storageEntity | string |  |
| thresholds | StorageWarningThresholds[] |  |