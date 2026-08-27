---
layout: Reference
title: Resource Threshold - Upsert Resource Threshold - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/resource-threshold/upsert-resource-threshold
uid: api.powerplatform.com.power-platform.licensing.resourcethreshold.upsertresourcethreshold
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
description: 'Learn more about Power Platform API service - Create or update the resource threshold for an environment resource. '
locale: en-us
document_id: 69c4a675-79cf-1a54-9386-7dedfdbfa356
document_version_independent_id: ba575a38-7be2-995d-1e00-5bc63f5ee7f6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Resource-Threshold/Upsert-Resource-Threshold.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/resource-threshold/upsert-resource-threshold
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Resource-Threshold/Upsert-Resource-Threshold.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 17d18807-d2a2-c433-1635-3846fda888eb
---

# Resource Threshold - Upsert Resource Threshold

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create or update the resource threshold for an environment resource.

```http
PUT https://api.powerplatform.com/licensing/environments/{environmentId}/entitlements/{entitlementId}/resources/{resourceId}/threshold?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| environmentId | path | True | string | The environment ID. |
| resourceId | path | True | string | The resource ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| limit | integer (int32) |  |
| notificationThreshold | integer (int32) |  |
| notifyIfOverCapacity | boolean |  |
| resourceConsumption | number (double) |  |
| stopIfOverCapacity | boolean |  |
| stopResource | boolean |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ResourceThresholdModel | Success |
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
| ResourceThresholdModel |  |
| ResourceThresholdRequestModel |  |

### ResourceThresholdModel

Object

| Name | Type | Description |
| --- | --- | --- |
| createdOn | string (date-time) | The UTC date and time when the resource threshold configuration was first created. |
| entitlementId | string | Entitlement ID associated with the resource. |
| environmentId | string | Unique identifier for the environment associated with the resource. |
| limit | number (double) | The limit set for the resource consumption. |
| notificationThreshold | integer (int32) | The threshold percentage for sending notifications about resource consumption. |
| notifyIfOverCapacity | boolean | Indicates whether to notify when the resource consumption reaches its notification threshold. |
| resourceConsumption | number (double) | Current consumption of the resource. |
| resourceId | string | Unique identifier for the resource. |
| stopIfOverCapacity | boolean | Indicates whether to stop consuming the capacity if the resource exceeds its limit. |
| stopResource | boolean | Indicates whether the user has selected to stop the resource explicitly or not. If 'true' the resource is in a disabled state. |

### ResourceThresholdRequestModel

Object

| Name | Type | Description |
| --- | --- | --- |
| limit | integer (int32) |  |
| notificationThreshold | integer (int32) |  |
| notifyIfOverCapacity | boolean |  |
| resourceConsumption | number (double) |  |
| stopIfOverCapacity | boolean |  |
| stopResource | boolean |  |