---
layout: Reference
title: Recommendations - Get Recommendation Resources - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/get-recommendation-resources
uid: api.powerplatform.com.power-platform.analytics.recommendations.getrecommendationresources
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
description: 'Learn more about Power Platform API service - Get recommendation resources. Gets the list of resources for a recommendation for the tenant. '
locale: en-us
document_id: 4d0a4f4f-9b0c-74f9-c319-f2e517e23dd6
document_version_independent_id: d4e51bbb-3704-e711-1432-b65433826253
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendation-Resources.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/get-recommendation-resources
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Get-Recommendation-Resources.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 52939933-15d8-c67f-844e-9776ce234f01
---

# Recommendations - Get Recommendation Resources

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get recommendation resources. Gets the list of resources for a recommendation for the tenant.

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations/{scenario}/resources?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations/{scenario}/resources?$skipToken={$skipToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| scenario | path | True | string | The recommendation name. |
| api-version | query | True | string | The API version. |
| $skipToken | query |  | string | Skip token for the next page of resources. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorRecommendationResourceIEnumerableResponseWithContinuation | Success |
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

| Name | Description |
| --- | --- |
| AdvisorRecommendationResource | Details of a resource included in a recommendation. |
| AdvisorRecommendationResourceIEnumerableResponseWithContinuation | Paged list of recommendation resources. |

### AdvisorRecommendationResource

Object

Details of a resource included in a recommendation.

| Name | Type | Description |
| --- | --- | --- |
| environmentId | string | The environment unique ID |
| environmentName | string | The environment display name |
| lastAccessedDate | string (date-time) | Time when the resource was last used |
| lastModifiedDate | string (date-time) | Time when the resource was last modified |
| resourceActionStatus | string | Current status of any action taken since the last refresh time |
| resourceDescription | string | The resource description |
| resourceId | string | The resource unique ID |
| resourceName | string | The resource display name |
| resourceOwner | string | The resource owner display name |
| resourceOwnerId | string | The resource owner object ID |
| resourceSubType | string | The sub type of the resource |
| resourceType | string | The type of resource |
| resourceUsage | number (double) | Number of unique users who used the resource in the last thirty (30) days |

### AdvisorRecommendationResourceIEnumerableResponseWithContinuation

Object

Paged list of recommendation resources.

| Name | Type | Description |
| --- | --- | --- |
| nextLink | string | Link to get the next page of resources |
| value | AdvisorRecommendationResource[] | List of recommendation resources |