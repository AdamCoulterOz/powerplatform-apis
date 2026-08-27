---
layout: Reference
title: Recommendations - Get Scenario Actions - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/get-scenario-actions
uid: api.powerplatform.com.power-platform.analytics.recommendations.getscenarioactions
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
description: 'Learn more about Power Platform API service - Get recommendation actions. Gets allowed actions for a recommendation. '
locale: en-us
document_id: a596bb9b-e961-a320-a965-feff5ffc7cee
document_version_independent_id: 0d2a77d4-21a5-a3e6-fe64-dce56f1aad27
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Get-Scenario-Actions.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/get-scenario-actions
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Get-Scenario-Actions.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 94f09369-117f-5180-feab-d2ca6cd1214c
---

# Recommendations - Get Scenario Actions

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get recommendation actions. Gets allowed actions for a recommendation.

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations/{scenario}/actions?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| scenario | path | True | string | The recommendation name. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorAction[] | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |
| 429 Too Many Requests |  | Too Many Requests |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### AdvisorAction

Object

The allowed action.

| Name | Type | Description |
| --- | --- | --- |
| actionName | string | Action display name |
| actionType | string | The action identifier |