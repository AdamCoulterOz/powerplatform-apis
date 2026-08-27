---
layout: Reference
title: Connections - List Connections - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/connectivity/connections/list-connections
uid: api.powerplatform.com.power-platform.connectivity.connections.listconnections
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
description: 'Learn more about Power Platform API service - List connections in environment. Retrieves a list of connections in the specified environment. '
locale: en-us
document_id: 7fab0b84-3699-7606-31f3-e7de030dd5e2
document_version_independent_id: dcb04d3c-f30a-5f15-779d-e8f980158140
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/connectivity/Connections/List-Connections.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/connectivity/connections/list-connections
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/connectivity/Connections/List-Connections.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: a17cb9bf-a066-a4b1-0d16-408e2973f174
---

# Connections - List Connections

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List connections in environment. Retrieves a list of connections in the specified environment.

```http
GET https://api.powerplatform.com/connectivity/environments/{environmentId}/connections?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | ID of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ListConnectionsResponse | A list of connections in the specified environment. |

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
| Connection |  |
| Interfaces |  |
| ListConnectionsResponse |  |
| Metadata |  |
| Properties |  |
| Version |  |

### Connection

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string |  |
| name | string |  |
| properties | Properties |  |
| type | string |  |

### Interfaces

Object

| Name | Type | Description |
| --- | --- | --- |
|  |  |  |

### ListConnectionsResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| value | Connection[] |  |

### Metadata

Object

| Name | Type | Description |
| --- | --- | --- |
| allowSharing | boolean |  |
| brandColor | string |  |
| source | string |  |
| useNewApimVersion | string |  |
| version | Version |  |

### Properties

Object

| Name | Type | Description |
| --- | --- | --- |
| apiEnvironment | string |  |
| apiVersion | string |  |
| blobUrisAreProxied | boolean |  |
| capabilities | string[] |  |
| changedTime | string (date-time) |  |
| createdTime | string (date-time) |  |
| description | string |  |
| displayName | string |  |
| doNotUseApiHubNetRuntimeUrl | string (uri) |  |
| iconBrandColor | string |  |
| iconUri | string (uri) |  |
| interfaces | Interfaces |  |
| isCustomApi | boolean |  |
| metadata | Metadata |  |
| primaryRuntimeUrl | string (uri) |  |
| publisher | string |  |
| rateLimit | integer |  |
| releaseTag | string |  |
| runtimeUrls | string[] (uri) |  |
| tier | string |  |

### Version

Object

| Name | Type | Description |
| --- | --- | --- |
| current | string |  |
| previous | string |  |