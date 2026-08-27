---
layout: Reference
title: Storage Warnings - Get Storage Warning By Category And Entity - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/storage-warnings/get-storage-warning-by-category-and-entity
uid: api.powerplatform.com.power-platform.licensing.storagewarnings.getstoragewarningbycategoryandentity
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
description: 'Learn more about Power Platform API service - Storage warning thresholds filtered by category and storage entity name. '
locale: en-us
document_id: 9ede8a8c-cda7-4b81-c0b1-97c63a23949c
document_version_independent_id: ba6bf45e-b440-9b01-f4c1-c0b5d6b1b7ea
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Storage-Warnings/Get-Storage-Warning-By-Category-And-Entity.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/storage-warnings/get-storage-warning-by-category-and-entity
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Storage-Warnings/Get-Storage-Warning-By-Category-And-Entity.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: e94fdc15-ba13-b03e-4765-5f23fd896a5d
---

# Storage Warnings - Get Storage Warning By Category And Entity

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Storage warning thresholds filtered by category and storage entity name.

```http
GET https://api.powerplatform.com/licensing/storageWarning/{storageCategory}/{entityName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entityName | path | True | string | The name of the entity. |
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