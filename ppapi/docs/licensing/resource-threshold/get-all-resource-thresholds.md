---
layout: Reference
title: Resource Threshold - Get All Resource Thresholds - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/resource-threshold/get-all-resource-thresholds
uid: api.powerplatform.com.power-platform.licensing.resourcethreshold.getallresourcethresholds
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
description: 'Learn more about Power Platform API service - Get all resource thresholds for the specified entitlement. '
locale: en-us
document_id: 5aee106e-5f49-698f-6ae2-33e76604ee90
document_version_independent_id: ecd408ec-c401-293b-6826-00778b2c2004
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Resource-Threshold/Get-All-Resource-Thresholds.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/resource-threshold/get-all-resource-thresholds
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Resource-Threshold/Get-All-Resource-Thresholds.yml
platformId: 6d93e097-b274-c4d8-f2a0-967df719dcf5
---

# Resource Threshold - Get All Resource Thresholds

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get all resource thresholds for the specified entitlement.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/resourceThresholds?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ResourceThresholdModel[] | Success |
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