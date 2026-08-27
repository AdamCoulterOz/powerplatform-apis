---
layout: Reference
title: Entitlement Insight - Get Environment Resources - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/entitlement-insight/get-environment-resources
uid: api.powerplatform.com.power-platform.licensing.entitlementinsight.getenvironmentresources
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
description: 'Learn more about Power Platform API service - Get environment resource entitlement snapshots for an entitlement. '
locale: en-us
document_id: 9a0d4c58-0957-d900-7301-d8ec53afbc56
document_version_independent_id: 08ac8e7b-4b66-93c1-47e7-4afcfc74aa7b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Environment-Resources.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/entitlement-insight/get-environment-resources
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Entitlement-Insight/Get-Environment-Resources.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: f3973f58-416c-ceac-6485-ff8b7f74f47b
---

# Entitlement Insight - Get Environment Resources

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get environment resource entitlement snapshots for an entitlement.

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/environments/{environmentId}/resources?fromDate={fromDate}&toDate={toDate}&api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/licensing/entitlements/{entitlementId}/environments/{environmentId}/resources?fromDate={fromDate}&toDate={toDate}&searchRequest={searchRequest}&includeFields={includeFields}&orderbyConsumed={orderbyConsumed}&continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| entitlementId | path | True | string | The entitlement ID. |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| fromDate | query | True | string | The start date (inclusive) of the query range. |
| toDate | query | True | string | The end date (inclusive) of the query range. |
| continuationToken | query |  | string | Continuation token for pagination. |
| includeFields | query |  | string | Comma separated additional fields to include in the response. |
| orderbyConsumed | query |  | string | Order by consumed date time if specified. |
| searchRequest | query |  | string | Search request for filtering the resources. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentEntitlementSnapshotResponseModelPagedResponse | Success |
| 204 No Content |  | No Content |
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
| EntitlementUnit | The unit of measure for an entitlement. |
| EnvironmentEntitlementSnapshotResponseModel |  |
| EnvironmentEntitlementSnapshotResponseModelPagedResponse | A paged response with a continuation token. |
| EnvironmentResourceEntitlementSnapshotResponseModel |  |

### EntitlementUnit

Enumeration

The unit of measure for an entitlement.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| MB |  |
| Count |  |
| Hour |  |

### EnvironmentEntitlementSnapshotResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| resources | EnvironmentResourceEntitlementSnapshotResponseModel[] |  |

### EnvironmentEntitlementSnapshotResponseModelPagedResponse

Object

A paged response with a continuation token.

| Name | Type | Description |
| --- | --- | --- |
| @odata.count | integer (int32) |  |
| @odata.nextLink | string |  |
| continuationtoken | string |  |
| value | EnvironmentEntitlementSnapshotResponseModel[] |  |

### EnvironmentResourceEntitlementSnapshotResponseModel

Object

| Name | Type | Description |
| --- | --- | --- |
| consumed | number (double) | The consumed value. |
| lastRefreshedDate | string (date-time) | The last refreshed date. |
| metadata | object | Additional metadata such as Feature, ProductName and nonBillableConsumed for MCSMessages. |
| resourceId | string | The resource ID. |
| unit | EntitlementUnit | The unit of measure for an entitlement. |