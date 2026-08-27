---
layout: Reference
title: Bots - Get Bot Quarantine Status - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/get-bot-quarantine-status
uid: api.powerplatform.com.power-platform.copilotstudio.bots.getbotquarantinestatus
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
description: 'Learn more about Power Platform API service - Get bot quarantine status. Retrieve the quarantine status of a bot. '
locale: en-us
document_id: 93cb820b-cf7a-34fa-4e56-ececa9c5198d
document_version_independent_id: 7dbe90ba-0683-625b-5efa-e1b5490b28a9
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Bot-Quarantine-Status.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/get-bot-quarantine-status
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Bot-Quarantine-Status.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 8fa602b7-e0b8-604a-63b1-1103c39b7901
---

# Bots - Get Bot Quarantine Status

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get bot quarantine status. Retrieve the quarantine status of a bot.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/botQuarantine?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BotQuarantineStatus | Successful response |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### BotQuarantineStatus

Object

| Name | Type | Description |
| --- | --- | --- |
| isBotQuarantined | boolean | Indicates whether the bot is quarantined. |
| lastUpdateTimeUtc | string (date-time) | The last update time in UTC. |