---
layout: Reference
title: Bots - Get Connector Consent Bypass - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/get-connector-consent-bypass
uid: api.powerplatform.com.power-platform.copilotstudio.bots.getconnectorconsentbypass
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
description: 'Learn more about Power Platform API service - Get connector consent bypass. Get the admin connector consent bypass setting for a bot. '
locale: en-us
document_id: 13d98243-fea8-b424-0017-363b1277fd09
document_version_independent_id: fa30cfd6-b130-c700-ec5b-7213806c28db
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Connector-Consent-Bypass.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/get-connector-consent-bypass
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Connector-Consent-Bypass.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0e8a27cf-3358-2004-9a8c-362aa6e67709
---

# Bots - Get Connector Consent Bypass

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get connector consent bypass. Get the admin connector consent bypass setting for a bot.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/connectorConsentBypass?api-version=2024-10-01
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
| 200 OK | ConnectorConsentBypassResponse | Successful response |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### ConnectorConsentBypassResponse

Object

The admin connector consent bypass setting for a bot.

| Name | Type | Description |
| --- | --- | --- |
| adminConsentBypass | boolean | Indicates whether admin connector consent bypass is enabled for the bot. |