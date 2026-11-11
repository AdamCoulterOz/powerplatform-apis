---
layout: Reference
title: Known Issues - Search Known Issues - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/support/known-issues/search-known-issues
uid: api.powerplatform.com.power-platform.support.knownissues.searchknownissues
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
description: Search known issues. Searches known issues for the supplied product IDs and search text. Requires a valid Power Platform API access token.
locale: en-us
document_id: 8c9fdf17-6dc7-aef6-ff54-8332a6fa8fdf
document_version_independent_id: 6f45b091-ca14-31bf-d241-8c81c8ade5f6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/support/Known-Issues/Search-Known-Issues.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/support/known-issues/search-known-issues
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/support/Known-Issues/Search-Known-Issues.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/12ed19f9-ebdf-4c8a-8bcd-7a681836774d
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/3a764584-4f97-452b-8f1d-36f19b12f6ae
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 06de44ec-48c3-22b0-6469-8846e9088210
---

# Known Issues - Search Known Issues

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Search known issues. Searches known issues for the supplied product IDs and search text. Requires a valid Power Platform API access token. Returns a JSON array of issues, without a collection wrapper or continuation token. Use skip and maxIssueCount in the request body to control the result window. An empty productIds array returns 204 with no body. A valid search with no matches returns an empty array.

```http
POST https://api.powerplatform.com/support/KnownIssue/search?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| productIds | True | string[] (uuid) | Product IDs to search. Each ID must be a GUID. An empty array returns 204. |
| searchText | True | string <br>minLength: 1 | The search text. Use an asterisk to search without a text filter. |
| issueStatus |  | SupportKnownIssueStatus(int32) | The numeric status selector: 0 Unknown, 1 New, 2 Active, 3 Resolved, or 4 Closed. |
| locale |  | string | The preferred locale for translated search content, when available. |
| maxIssueCount |  | integer (int32) | The requested result count. Values from 1 to 200 are used; otherwise the service uses 25. |
| minMatchingScore |  | number (double) | The minimum matching score. A value of zero lets the service select a threshold for the search mode. |
| skip |  | integer (int32) | The number of results to skip in the search. |
| source |  | string | An optional caller context label used by the search service. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | SupportKnownIssue[] | The matching known issues as a JSON array. |
| 204 No Content |  | The productIds array was empty. No response body is returned. |
| 400 Bad Request |  | The request or a product ID is invalid, the search text is empty, or the search failed. |
| 401 Unauthorized |  | A valid Power Platform API access token is required. |
| 403 Forbidden |  | Access to the known-issue endpoint is forbidden. |
| 500 Internal Server Error |  | An unexpected error occurred before the search could complete. |

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
| SupportKnownIssue | A known issue and its product, status, content, and search metadata. |
| SupportKnownIssueSearchRequest | The public request fields for searching known issues. |
| SupportKnownIssueStatus | The numeric status selector: 0 Unknown, 1 New, 2 Active, 3 Resolved, or 4 Closed. |

### SupportKnownIssue

Object

A known issue and its product, status, content, and search metadata.

| Name | Type | Description |
| --- | --- | --- |
| @search.rerankerScore | number (double) | The semantic reranker score returned by the service. |
| @search.score | number (double) | The search relevance score returned by the service. |
| changedDate | string | The latest change timestamp as returned by the service. |
| createdDate | string | The creation timestamp as returned by the service. |
| description | string | The issue description, which can contain HTML. |
| impactedProducts | string[] | The IDs of products impacted by the issue. |
| isSearchable | boolean | Whether the issue is eligible for search results. Retired issues can remain retrievable by ID. |
| parentUrl | string | The parent work item URL provided by the service. |
| product | string | The primary product's display name. |
| productFamilyTags | string[] | The product family tags associated with the issue. |
| productId | string | The primary product ID. |
| solution | string | The resolution or workaround guidance, which can contain HTML. |
| state | string | The issue state returned by the service. |
| title | string | The known issue title. |
| version | string | Version information associated with the issue. |
| workItemId | string | The known issue work item ID. |

### SupportKnownIssueSearchRequest

Object

The public request fields for searching known issues.

| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| issueStatus | SupportKnownIssueStatus(int32) | 0 | The numeric status selector: 0 Unknown, 1 New, 2 Active, 3 Resolved, or 4 Closed. |
| locale | string |  | The preferred locale for translated search content, when available. |
| maxIssueCount | integer (int32) | 25 | The requested result count. Values from 1 to 200 are used; otherwise the service uses 25. |
| minMatchingScore | number (double) | 0 | The minimum matching score. A value of zero lets the service select a threshold for the search mode. |
| productIds | string[] (uuid) |  | Product IDs to search. Each ID must be a GUID. An empty array returns 204. |
| searchText | string <br>minLength: 1 |  | The search text. Use an asterisk to search without a text filter. |
| skip | integer (int32) | 0 | The number of results to skip in the search. |
| source | string |  | An optional caller context label used by the search service. |

### SupportKnownIssueStatus

Enumeration

The numeric status selector: 0 Unknown, 1 New, 2 Active, 3 Resolved, or 4 Closed.

| Value | Description |
| --- | --- |
| 0 |  |
| 1 |  |
| 2 |  |
| 3 |  |
| 4 |  |