---
layout: Reference
title: Licensing Reports - Download Licensing Report File - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/licensing-reports/download-licensing-report-file
uid: api.powerplatform.com.power-platform.copilotstudio.licensingreports.downloadlicensingreportfile
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
description: Download Licensing Report File. Downloads a generated licensing report as a gzip-compressed CSV file. Use the file name returned by a report operation with a Su
locale: en-us
document_id: ede3b6fc-c272-0031-0c02-020ff4b68421
document_version_independent_id: e3acb8ed-13d5-bbcb-6d8f-023fcdb13822
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Download-Licensing-Report-File.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/licensing-reports/download-licensing-report-file
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Licensing-Reports/Download-Licensing-Report-File.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 6a6486b6-b35c-748b-99c3-552efc41a304
---

# Licensing Reports - Download Licensing Report File

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Download Licensing Report File. Downloads a generated licensing report as a gzip-compressed CSV file. Use the file name returned by a report operation with a Succeeded status.

```http
GET https://api.powerplatform.com/copilotstudio/licensing/reports/{ReportName}/files/{FileName}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| FileName | path | True | string | The report file name, returned by a report operation with a Succeeded status. |
| ReportName | path | True | string | The name of the generated report. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | string | The report file as a gzip-compressed CSV.<br><br>Media Types: "application/gzip"<br><br>Headers<br><br>Content-Disposition: string |
| 401 Unauthorized |  | Unauthorized. A valid access token is required.<br><br>Media Types: "application/gzip" |
| 403 Forbidden |  | Forbidden. The caller must be a Global, Dynamics 365, or Power Platform administrator of the tenant.<br><br>Media Types: "application/gzip" |
| 404 Not Found |  | Not found. The file doesn't exist, doesn't belong to your tenant, or licensing reports aren't available for the tenant.<br><br>Media Types: "application/gzip" |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |