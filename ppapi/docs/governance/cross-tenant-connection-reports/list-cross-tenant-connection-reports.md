---
layout: Reference
title: Cross Tenant Connection Reports - List Cross Tenant Connection Reports - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/cross-tenant-connection-reports/list-cross-tenant-connection-reports
uid: api.powerplatform.com.power-platform.governance.crosstenantconnectionreports.listcrosstenantconnectionreports
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
description: 'Learn more about Power Platform API service - List cross-tenant connection reports for a tenant. '
locale: en-us
document_id: e299f329-ef95-b186-88bb-c083fe9338a3
document_version_independent_id: 315477a6-58f5-d7ea-26c4-ec1bc70ab920
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Cross-Tenant-Connection-Reports/List-Cross-Tenant-Connection-Reports.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/cross-tenant-connection-reports/list-cross-tenant-connection-reports
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Cross-Tenant-Connection-Reports/List-Cross-Tenant-Connection-Reports.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 1835cb88-bc7e-816a-bcf8-4e9a36a247bb
---

# Cross Tenant Connection Reports - List Cross Tenant Connection Reports

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List cross-tenant connection reports for a tenant.

```http
GET https://api.powerplatform.com/governance/crossTenantConnectionReports?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | CrossTenantConnectionReportsResponseWithOdataContinuation | Success. |
| 400 Bad Request |  | Bad Request. |
| 401 Unauthorized |  | Unauthorized. |
| 403 Forbidden |  | Forbidden. |

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
| CrossTenantConnection |  |
| CrossTenantConnectionReport |  |
| CrossTenantConnectionReportsResponseWithOdataContinuation |  |

### CrossTenantConnection

Object

| Name | Type | Description |
| --- | --- | --- |
| connectionType | enum:<br>- Inbound<br>- Outbound | The direction of the cross-tenant connection. |
| tenantId | string (uuid) | The Azure AD tenant ID to or from which the cross-tenant connection occurred. |

### CrossTenantConnectionReport

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string | Next page URI for additional cross-tenant connections. |
| connections | CrossTenantConnection[] | The page of cross-tenant connections occurring within the report date window. |
| endDate | string (date-time) | The end of the report date window. |
| reportId | string (uuid) | The report ID. |
| requestDate | string (date-time) | The date when the cross-tenant connection report was requested. |
| startDate | string (date-time) | The start of the report date window. |
| status | enum:<br>- Completed<br>- Failed<br>- InProgress<br>- Received |  |
| tenantId | string (uuid) | The Azure AD tenant ID for which the report was generated. |

### CrossTenantConnectionReportsResponseWithOdataContinuation

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string | The URI of the next page of the list response. |
| value | CrossTenantConnectionReport[] | The cross-tenant connection reports for the tenant. |