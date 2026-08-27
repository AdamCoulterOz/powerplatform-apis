---
layout: Reference
title: Bots - Set Bot As Quarantined - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/set-bot-as-quarantined
uid: api.powerplatform.com.power-platform.copilotstudio.bots.setbotasquarantined
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
description: 'Learn more about Power Platform API service - Set bot as quarantined. Set the quarantine status of a bot to true. '
locale: en-us
document_id: f3c3769f-73ab-82bf-fc79-6f8de5e981fa
document_version_independent_id: 6c405b1c-f45e-a9ea-9d9e-2458a6b15666
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Set-Bot-As-Quarantined.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/set-bot-as-quarantined
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Set-Bot-As-Quarantined.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: dd84829c-7d00-d1e5-5d7f-22c749aa1bb2
---

# Bots - Set Bot As Quarantined

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Set bot as quarantined. Set the quarantine status of a bot to true.

```http
POST https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/botQuarantine/SetAsQuarantined?api-version=2024-10-01
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