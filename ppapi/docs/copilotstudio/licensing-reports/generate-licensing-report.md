---
layout: Reference
title: Licensing Reports - Generate Licensing Report - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/licensing-reports/generate-licensing-report
uid: api.powerplatform.com.power-platform.copilotstudio.licensingreports.generatelicensingreport
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
description: Generate Licensing Report. Starts generating a Copilot Studio licensing report for your tenant over the requested date range.
locale: en-us
document_id: b2bb7178-47aa-4b5d-44f3-078906a0ff24
document_version_independent_id: 2bfdae01-ffe8-d4c9-e611-0ce3decef146
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Generate-Licensing-Report.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/licensing-reports/generate-licensing-report
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Generate-Licensing-Report.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c389ea6b-b6a0-46df-93a1-1e21f25e19e7
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/19ada1b6-705b-4ed7-aad0-bffd1bd03dfa
platformId: cffaf219-2e57-dabe-9abb-d018dc19f44b
---

# Licensing Reports - Generate Licensing Report

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Generate Licensing Report. Starts generating a Copilot Studio licensing report for your tenant over the requested date range. Generation runs asynchronously; poll the URL in the Location header for status. Requires the Global, Dynamics 365, or Power Platform administrator role.

```http
POST https://api.powerplatform.com/copilotstudio/licensing/reports/{ReportName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| ReportName | path | True | string | The name of the report to generate. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| endDate | True | string (date) | The inclusive UTC end date of the report range. Must be on or after the start date. |
| startDate | True | string (date) | The inclusive UTC start date of the report range. |
| granularity |  | CopilotStudioLicensingReportGranularity | The granularity of a licensing report. Daily returns one row per day in the date range, and Summary returns a single summarized row for the whole range. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted. Report generation started.<br><br>Headers<br><br>- Location: string<br>- Retry-After: string |
| 400 Bad Request |  | Bad request. The request body or a date is missing or invalid, or the end date is before the start date. |
| 401 Unauthorized |  | Unauthorized. A valid access token is required. |
| 403 Forbidden |  | Forbidden. The caller must be a Global, Dynamics 365, or Power Platform administrator of the tenant. |
| 404 Not Found |  | Not found. The report isn't supported or licensing reports aren't available for the tenant. |

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
| CopilotStudioLicensingReportGranularity | The granularity of a licensing report. Daily returns one row per day in the date range, and Summary returns a single summarized row for the whole range. |
| CopilotStudioLicensingReportRequest | The request body for generating a licensing report. |

### CopilotStudioLicensingReportGranularity

Enumeration

The granularity of a licensing report. Daily returns one row per day in the date range, and Summary returns a single summarized row for the whole range.

| Value | Description |
| --- | --- |
| Daily |  |
| Summary |  |

### CopilotStudioLicensingReportRequest

Object

The request body for generating a licensing report.

| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| endDate | string (date) |  | The inclusive UTC end date of the report range. Must be on or after the start date. |
| granularity | CopilotStudioLicensingReportGranularity | Daily | The granularity of a licensing report. Daily returns one row per day in the date range, and Summary returns a single summarized row for the whole range. |
| startDate | string (date) |  | The inclusive UTC start date of the report range. |