---
layout: Reference
title: Bots - Download Maker Evaluation Snapshot - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/download-maker-evaluation-snapshot
uid: api.powerplatform.com.power-platform.copilotstudio.bots.downloadmakerevaluationsnapshot
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
description: 'Download maker evaluation snapshot. Download the bot content snapshot associated with a specific maker evaluation test run as a ZIP file. '
locale: en-us
document_id: 504aae26-9cec-6273-e2e3-cb3f9017883a
document_version_independent_id: c3a9976c-485b-f097-8493-f965ecf6263c
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Download-Maker-Evaluation-Snapshot.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/download-maker-evaluation-snapshot
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Download-Maker-Evaluation-Snapshot.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0ed3fdcf-539e-0531-b139-538a63a703db
---

# Bots - Download Maker Evaluation Snapshot

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Download maker evaluation snapshot. Download the bot content snapshot associated with a specific maker evaluation test run as a ZIP file.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/makerevaluation/testruns/{TestRunId}/snapshot?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| TestRunId | path | True | string (uuid) | The test run ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | string | The bot content snapshot ZIP file.<br><br>Media Types: "application/zip"<br><br>Headers<br><br>Content-Disposition: string |
| 404 Not Found |  | Test run not found.<br><br>Media Types: "application/zip" |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |