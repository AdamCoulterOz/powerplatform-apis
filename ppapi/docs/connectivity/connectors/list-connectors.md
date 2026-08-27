---
layout: Reference
title: Connectors - List Connectors - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/connectivity/connectors/list-connectors
uid: api.powerplatform.com.power-platform.connectivity.connectors.listconnectors
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
description: 'Learn more about Power Platform API service - List connectors in environment. Retrieves a list of connectors in the specified environment. '
locale: en-us
document_id: 59c245ec-5ff6-6407-5572-9d41c41917e0
document_version_independent_id: 319d2011-b731-5259-5c1b-6e6a0bdf1395
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/connectivity/Connectors/List-Connectors.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/connectivity/connectors/list-connectors
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/connectivity/Connectors/List-Connectors.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 988fd237-a243-382b-a78f-f3ce4c2cd0cd
---

# Connectors - List Connectors

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List connectors in environment. Retrieves a list of connectors in the specified environment.

```http
GET https://api.powerplatform.com/connectivity/environments/{environmentId}/connectors?$filter={$filter}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | ID of the environment. |
| $filter | query | True | string | Filter query to specify the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ListConnectorsResponse | A list of connectors in the specified environment. |

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
| GetConnectorByIdResponse |  |
| Interfaces |  |
| ListConnectorsResponse |  |
| Metadata |  |
| Properties |  |
| Version |  |

### GetConnectorByIdResponse

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

### ListConnectorsResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| value | GetConnectorByIdResponse[] |  |

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