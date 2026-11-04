---
layout: Reference
title: Licensing Reports - Get Licensing Report Operation - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/licensing-reports/get-licensing-report-operation
uid: api.powerplatform.com.power-platform.copilotstudio.licensingreports.getlicensingreportoperation
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
description: Get Licensing Report Operation Status. Gets the status of a licensing report generation operation. When the status is Succeeded, the response includes the repor
locale: en-us
document_id: f66a4b4f-6f0f-54e7-4484-bc36c19e9103
document_version_independent_id: 26ad1a68-56e2-c2ce-280f-654348c43692
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Get-Licensing-Report-Operation.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/licensing-reports/get-licensing-report-operation
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Get-Licensing-Report-Operation.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 2fcb2505-27d0-390c-aa4b-c4cb1210e015
---

# Licensing Reports - Get Licensing Report Operation

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get Licensing Report Operation Status. Gets the status of a licensing report generation operation. When the status is Succeeded, the response includes the report file name and the Location header contains the download URL.

```http
GET https://api.powerplatform.com/copilotstudio/licensing/reports/{ReportName}/operations/{OperationId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| OperationId | path | True | string | The report operation ID, returned in the Location header when report generation starts. |
| ReportName | path | True | string | The name of the report being generated. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | CopilotStudioLicensingReportOperation | Successful response. The body contains the current status of the operation.<br><br>Headers<br><br>- Location: string<br>- Retry-After: string |
| 401 Unauthorized |  | Unauthorized. A valid access token is required. |
| 403 Forbidden |  | Forbidden. The caller must be a Global, Dynamics 365, or Power Platform administrator of the tenant. |
| 404 Not Found |  | Not found. The operation doesn't exist or licensing reports aren't available for the tenant. |

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
| CopilotStudioLicensingReportOperation | The status of a licensing report generation operation. |
| CopilotStudioLicensingReportOperationStatus | The status of a licensing report generation operation. |

### CopilotStudioLicensingReportOperation

Object

The status of a licensing report generation operation.

| Name | Type | Description |
| --- | --- | --- |
| error | string | A message describing why report generation failed. Returned only when the status is Failed. |
| fileName | string | The generated report file name to use when downloading the report. Returned only when the status is Succeeded. |
| status | CopilotStudioLicensingReportOperationStatus | The status of a licensing report generation operation. |

### CopilotStudioLicensingReportOperationStatus

Enumeration

The status of a licensing report generation operation.

| Value | Description |
| --- | --- |
| Running |  |
| Succeeded |  |
| Failed |  |