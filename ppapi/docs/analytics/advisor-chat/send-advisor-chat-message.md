---
layout: Reference
title: Advisor Chat - Send Advisor Chat Message - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/analytics/advisor-chat/send-advisor-chat-message
uid: api.powerplatform.com.power-platform.analytics.advisorchat.sendadvisorchatmessage
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
description: Send an advisor chat message. Sends a message to the advisor chat agent and returns the agent response.
locale: en-us
document_id: a7b905aa-f0e8-93d2-26de-d7c31afbe66d
document_version_independent_id: 46524c4b-ef4e-6733-3bb8-97173c2329f5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/analytics/Advisor-Chat/Send-Advisor-Chat-Message.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/analytics/advisor-chat/send-advisor-chat-message
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/analytics/Advisor-Chat/Send-Advisor-Chat-Message.yml
platformId: 2e2bfe18-004a-90ca-6ba0-8e6d608fa810
---

# Advisor Chat - Send Advisor Chat Message

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Send an advisor chat message. Sends a message to the advisor chat agent and returns the agent response. Supply the conversation ID returned by a previous turn to continue a multi-turn conversation.

```http
POST https://api.powerplatform.com/analytics/advisor/chat/messages?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| message | True | string | The user message to send to the advisor chat agent |
| conversationId |  | string | The conversation ID for multi-turn chat. Omit to start a new conversation |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AdvisorChatMessageResponse | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |
| 429 Too Many Requests |  | Too Many Requests |

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
| AdvisorChatMessageRequest | The request to send a message to the advisor chat agent |
| AdvisorChatMessageResponse | The response from the advisor chat agent |

### AdvisorChatMessageRequest

Object

The request to send a message to the advisor chat agent

| Name | Type | Description |
| --- | --- | --- |
| conversationId | string | The conversation ID for multi-turn chat. Omit to start a new conversation |
| message | string | The user message to send to the advisor chat agent |

### AdvisorChatMessageResponse

Object

The response from the advisor chat agent

| Name | Type | Description |
| --- | --- | --- |
| conversationId | string | The conversation ID to supply on the next turn to continue the conversation |
| executionTimeMs | integer (int64) | The time taken to produce the response, in milliseconds |
| message | string | The agent response message |
| role | string | The role of the message author, always 'assistant' |