---
layout: Reference
title: Recommendations - Get Action Schema - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/recommendations/get-action-schema
uid: api.powerplatform.com.power-platform.analytics.recommendations.getactionschema
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
description: 'Learn more about Power Platform API service - Get action schema. Gets the schema for an action. '
locale: en-us
document_id: e8ce0a09-8359-b6b1-5c85-438d4f1bb9d9
document_version_independent_id: dac60daa-5d1e-27d8-4d86-da33299081c6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Recommendations/Get-Action-Schema.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/recommendations/get-action-schema
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Recommendations/Get-Action-Schema.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 40630f30-0bab-91a5-2eca-f796f1ed198b
---

# Recommendations - Get Action Schema

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get action schema. Gets the schema for an action.

```http
GET https://api.powerplatform.com/analytics/advisorRecommendations/{scenario}/actionmetadata/{actionName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| actionName | path | True | string | The name of the action. |
| scenario | path | True | string | The recommendation name. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | object | Success |
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