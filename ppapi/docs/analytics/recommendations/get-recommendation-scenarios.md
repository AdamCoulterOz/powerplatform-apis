---
layout: Reference
title: Recommendations - Get Recommendation Scenarios - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/get-recommendation-scenarios
uid: api.powerplatform.com.power-platform.analytics.recommendations.getrecommendationscenarios
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
description: 'Learn more about Power Platform API service - Get recommendation names. Gets the list of recommendation scenario names for the tenant. '
locale: en-us
document_id: e42fb11e-1b04-7dd2-33b4-fff4a01e05ec
document_version_independent_id: 84a1abaf-fd88-6e67-f188-1bd5e1903841
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendation-Scenarios.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/get-recommendation-scenarios
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendation-Scenarios.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 2106b471-7fd7-40fe-581d-9b79274ef70a
---

# Recommendations - Get Recommendation Scenarios

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get recommendation names. Gets the list of recommendation scenario names for the tenant.

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations/scenarios?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorScenario[] | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### AdvisorScenario

Object

The recommendation scenario.

| Name | Type | Description |
| --- | --- | --- |
| scenario | string | The scenario identifier |
| scenarioName | string | Scenario display name |