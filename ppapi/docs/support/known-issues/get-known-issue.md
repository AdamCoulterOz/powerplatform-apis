---
layout: Reference
title: Known Issues - Get Known Issue - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/support/known-issues/get-known-issue
uid: api.powerplatform.com.power-platform.support.knownissues.getknownissue
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
description: Get a known issue by ID. Retrieves a known issue by its numeric work item ID. Requires a valid Power Platform API access token.
locale: en-us
document_id: 4929774b-0db9-70d8-667d-fc186e1e6eb1
document_version_independent_id: f9299a18-160f-d8eb-6c12-df4264a001dd
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/support/Known-Issues/Get-Known-Issue.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/support/known-issues/get-known-issue
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/support/Known-Issues/Get-Known-Issue.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/fcc3cd4a-59ea-47a2-9cc1-784142a5a25d
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/d7a55faf-a992-4e27-aa3a-eadc9830e778
platformId: 11adabeb-0fa7-f6db-fea1-6dedaf028350
---

# Known Issues - Get Known Issue

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get a known issue by ID. Retrieves a known issue by its numeric work item ID. Requires a valid Power Platform API access token. A preferred locale can be supplied for translated content when translation is available. An issue can remain retrievable by ID after it is excluded from search results. The implementation returns 400, not 404, when an issue doesn't exist.

```http
GET https://api.powerplatform.com/support/KnownIssue/{issueId}?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/support/KnownIssue/{issueId}?locale={locale}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| issueId | path | True | string <br>minLength: 1 | The numeric work item ID of the known issue. |
| api-version | query | True | string | The API version. |
| locale | query |  | string | The preferred locale for translated issue content, when available. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | SupportKnownIssue | The known issue, including its state and resolution guidance. |
| 400 Bad Request |  | The issue ID isn't a valid signed 64-bit integer, the issue doesn't exist, or the lookup failed. |
| 401 Unauthorized |  | A valid Power Platform API access token is required. |
| 403 Forbidden |  | Access to the known-issue endpoint is forbidden. |
| 500 Internal Server Error |  | An unexpected error occurred before the lookup could complete. |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

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