---
layout: Reference
title: Resource Query - Query Resources - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/resourcequery/resource-query/query-resources
uid: api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources
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
description: 'Learn more about Power Platform API service - Query Power Platform resources. Executes a KQL query against Azure Resource Graph with ARG paging. '
locale: en-us
document_id: 8ea7c70e-4871-952d-1913-05d3cbb8a661
document_version_independent_id: 5c772671-d70b-ad16-1fd7-39197a391ddf
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/resourcequery/Resource-Query/Query-Resources.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/resourcequery/resource-query/query-resources
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/resourcequery/Resource-Query/Query-Resources.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/d3928677-9b71-43a6-875f-004dc4f98b65
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/6bbc70ca-58b2-4c69-8249-28ec92c08029
platformId: cf20b408-0dc3-6313-13c1-82337b610cc7
---

# Resource Query - Query Resources

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Query Power Platform resources. Executes a KQL query against Azure Resource Graph with ARG paging.

```http
POST https://api.powerplatform.com/resourcequery/resources/query?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Clauses | True | Clause[] | Ordered list of query clauses; evaluated in order |
| TableName | True | string | Target table/resource set (e.g., "PowerPlatformResources") |
| Options |  | ResourceQueryRequestOptions |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ResourceQueryResponse | Successful query execution |
| 400 Bad Request |  | Bad Request – invalid query specification |
| 401 Unauthorized |  | Unauthorized – missing/invalid credentials |
| 429 Too Many Requests |  | Too Many Requests – ARG throttling |
| 500 Internal Server Error |  | Internal Server Error |

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
| ResourceItem | ARG row with Power Platform-specific fields. Arbitrary properties may exist under `properties`. |
| ResourceQueryRequest |  |
| ResourceQueryRequestOptions |  |
| ResourceQueryResponse |  |

### ResourceItem

Object

ARG row with Power Platform-specific fields. Arbitrary properties may exist under `properties`.

| Name | Type | Description |
| --- | --- | --- |
| environmentId | string |  |
| environmentId1 | string |  |
| environmentName | string |  |
| environmentRegion | string |  |
| environmentType | string |  |
| extendedLocation | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |
| id | string |  |
| identity | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |
| isManagedEnvironment | boolean |  |
| kind | string |  |
| location | string |  |
| managedBy | string |  |
| name | string |  |
| plan | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |
| properties | object | Free-form ARG properties bag |
| resourceGroup | string |  |
| sku | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |
| subscriptionId | string |  |
| tags | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |
| tenantId | string |  |
| type | string |  |
| zones | api.powerplatform.com.power-platform.resourcequery.resourcequery.queryresources |  |

### ResourceQueryRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| Clauses | Clause[] | Ordered list of query clauses; evaluated in order |
| Options | ResourceQueryRequestOptions |  |
| TableName | string | Target table/resource set (e.g., "PowerPlatformResources") |

### ResourceQueryRequestOptions

Object

| Name | Type | Description |
| --- | --- | --- |
| Skip | integer <br>minimum: 0 | Offset; don't include when using SkipToken |
| SkipToken | string | Continuation token from previous page |
| Top | integer <br>minimum: 1 | Max rows per page |

### ResourceQueryResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| count | integer (int64) | Rows in this page |
| data | ResourceItem[] | ARG row with Power Platform-specific fields. Arbitrary properties may exist under `properties`. |
| resultTruncated | enum:<br>- 0<br>- 1 | 0 = truncated, 1 = not truncated |
| skipToken | string | Continuation token for next page |
| totalRecords | integer (int64) | Total rows matching the query |