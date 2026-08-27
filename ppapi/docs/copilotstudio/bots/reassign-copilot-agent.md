---
layout: Reference
title: Bots - Reassign Copilot Agent - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/reassign-copilot-agent
uid: api.powerplatform.com.power-platform.copilotstudio.bots.reassigncopilotagent
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
description: 'Learn more about Power Platform API service - Reassign the owner of the bot. '
locale: en-us
document_id: 738847ac-5477-d12a-aca0-821428e6b8fb
document_version_independent_id: ab9b9b72-51ca-35e0-b2a6-c93b5e1a937b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Reassign-Copilot-Agent.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/reassign-copilot-agent
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Reassign-Copilot-Agent.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/46e3c7c4-fe77-4a6e-b40a-44c569819fa5
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d0c6fab8-2d7d-4bb0-bf40-589e08d7c132
platformId: 85648774-7157-5eb8-d3ca-e716a3dd3993
---

# Bots - Reassign Copilot Agent

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Reassign the owner of the bot.

```http
POST https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/botAdminOperations/reassign?api-version=2024-10-01
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
| NewOwnerAadUserId | True | string | The new owner Entra ID. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | Successful response |
| 400 Bad Request |  | Bad Request. |
| 500 Internal Server Error |  | Internal Server Error. |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |

## Definitions

### ReassignBotRequestBody

Object

Request body for reassigning bot's owner.

| Name | Type | Description |
| --- | --- | --- |
| NewOwnerAadUserId | string | The new owner Entra ID. |