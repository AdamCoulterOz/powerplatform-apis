---
layout: Reference
title: Bots - Set Connector Consent Bypass - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/set-connector-consent-bypass
uid: api.powerplatform.com.power-platform.copilotstudio.bots.setconnectorconsentbypass
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
description: 'Learn more about Power Platform API service - Set connector consent bypass. Set the admin connector consent bypass setting for a bot. '
locale: en-us
document_id: c47c292e-2e52-54f8-a2c7-a974f11dcf50
document_version_independent_id: 32cb01c2-7ed7-35c8-dc85-11bc1a944c25
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Set-Connector-Consent-Bypass.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/set-connector-consent-bypass
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Set-Connector-Consent-Bypass.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5de95d4c-b01d-6106-f75c-784a603c6def
---

# Bots - Set Connector Consent Bypass

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Set connector consent bypass. Set the admin connector consent bypass setting for a bot.

```http
PUT https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/connectorConsentBypass?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| adminConsentBypass | True | boolean | Indicates whether to enable admin connector consent bypass for the bot. |

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

| Name | Description |
| --- | --- |
| ConnectorConsentBypassResponse | The admin connector consent bypass setting for a bot. |
| SetAdminConsentBypassRequest | Request body for setting the admin connector consent bypass setting for a bot. |

### ConnectorConsentBypassResponse

Object

The admin connector consent bypass setting for a bot.

| Name | Type | Description |
| --- | --- | --- |
| adminConsentBypass | boolean | Indicates whether admin connector consent bypass is enabled for the bot. |

### SetAdminConsentBypassRequest

Object

Request body for setting the admin connector consent bypass setting for a bot.

| Name | Type | Description |
| --- | --- | --- |
| adminConsentBypass | boolean | Indicates whether to enable admin connector consent bypass for the bot. |