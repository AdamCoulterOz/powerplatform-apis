---
layout: Reference
title: Recommendations - Execute Recommendation Action - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/execute-recommendation-action
uid: api.powerplatform.com.power-platform.analytics.recommendations.executerecommendationaction
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
description: 'Learn more about Power Platform API service - Execute recommendation action. Execute a recommended action on a set of recommendation resource(s). '
locale: en-us
document_id: 4b3df111-6108-9f07-79e3-c65ac51f2791
document_version_independent_id: 70a4aeb5-079d-f850-d0c5-b23b46f7f912
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Execute-Recommendation-Action.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/execute-recommendation-action
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Execute-Recommendation-Action.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 802da273-486b-9998-44b7-0558fae22907
---

# Recommendations - Execute Recommendation Action

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Execute recommendation action. Execute a recommended action on a set of recommendation resource(s).

```http
POST https://api.powerplatform.com/analytics/actions/{actionName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| actionName | path | True | string | The name of the action to execute. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| actionParameters | True | object | The collection of parameters to carry out the action for a resource |
| scenario | True | string | The name of the recommendation for which the action is triggered |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorActionResponse | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Too Many Requests |

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
| AdvisorActionRequest | The request with details to carry out an action on resource(s). |
| AdvisorActionResponse | The response for action performed on resources. |
| AdvisorActionResult | The result of an action performed on a resource. |

### AdvisorActionRequest

Object

The request with details to carry out an action on resource(s).

| Name | Type | Description |
| --- | --- | --- |
| actionParameters | object | The collection of parameters to carry out the action for a resource |
| scenario | string | The name of the recommendation for which the action is triggered |

### AdvisorActionResponse

Object

The response for action performed on resources.

| Name | Type | Description |
| --- | --- | --- |
| results | AdvisorActionResult[] | The result of an action performed on a resource. |

### AdvisorActionResult

Object

The result of an action performed on a resource.

| Name | Type | Description |
| --- | --- | --- |
| actionFinalResult | string | Final status of the action request |
| error | string | The error message associated with any error encountered during the action execution |
| errorCode | string | The error code associated with any error encountered during the action execution |
| resourceId | string | The unique ID of the resource for which the action was performed |
| statusCode | integer (int32) | The status code of the action request for the given resource |