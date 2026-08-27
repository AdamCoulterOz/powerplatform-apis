---
layout: Reference
title: Recommendations - Get Recommendations - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/get-recommendations
uid: api.powerplatform.com.power-platform.analytics.recommendations.getrecommendations
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
description: 'Learn more about Power Platform API service - Get recommendations. Gets the list of recommendations for the tenant. '
locale: en-us
document_id: ad706b12-6ee9-22ce-3594-fe7d7fec390f
document_version_independent_id: 27e87089-00d7-ef42-a340-7915f95653be
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendations.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/get-recommendations
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendations.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0b182b46-95cd-c732-877b-ec290ebdfff4
---

# Recommendations - Get Recommendations

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get recommendations. Gets the list of recommendations for the tenant.

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations?$skipToken={$skipToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $skipToken | query |  | string | Skip token for the next page of recommendations. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorRecommendationIEnumerableResponseWithContinuation | Success |
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

| Name | Description |
| --- | --- |
| AdvisorRecommendation | Information for a recommendation. |
| AdvisorRecommendationDetails | Details for a recommendation. |
| AdvisorRecommendationIEnumerableResponseWithContinuation | Paged list of recommendations. |

### AdvisorRecommendation

Object

Information for a recommendation.

| Name | Type | Description |
| --- | --- | --- |
| details | AdvisorRecommendationDetails | Details for a recommendation. |
| scenario | string | The recommendation name. |

### AdvisorRecommendationDetails

Object

Details for a recommendation.

| Name | Type | Description |
| --- | --- | --- |
| expectedNextRefreshTimestamp | string (date-time) | Time when the recommendation will be refreshed again |
| lastRefreshedTimestamp | string (date-time) | Time when the recommendation was refreshed |
| resourceCount | integer (int32) | The number of resources |

### AdvisorRecommendationIEnumerableResponseWithContinuation

Object

Paged list of recommendations.

| Name | Type | Description |
| --- | --- | --- |
| nextLink | string | Link to get the next page of recommendations |
| value | AdvisorRecommendation[] | List of recommendations |