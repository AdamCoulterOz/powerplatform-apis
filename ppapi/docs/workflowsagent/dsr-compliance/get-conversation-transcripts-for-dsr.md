---
layout: Reference
title: Dsr Compliance - Get Conversation Transcripts For Dsr - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/workflowsagent/dsr-compliance/get-conversation-transcripts-for-dsr
uid: api.powerplatform.com.power-platform.workflowsagent.dsrcompliance.getconversationtranscriptsfordsr
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
description: 'Get conversation transcripts for DSR export. Returns conversation transcripts for DSR compliance export. '
locale: en-us
document_id: 22241b46-1640-8bb0-81c7-10d400b4ceb5
document_version_independent_id: b812874f-004b-1dca-142c-3567ec50e011
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Conversation-Transcripts-For-Dsr.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/workflowsagent/dsr-compliance/get-conversation-transcripts-for-dsr
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/workflowsagent/Dsr-Compliance/Get-Conversation-Transcripts-For-Dsr.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/540ac133-a371-4dbb-8f94-28d6cc77a70b
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/60bfc045-f127-4841-9d00-ea35495a5800
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0bd609f2-3610-ee84-cddc-0aef83155bbb
---

# Dsr Compliance - Get Conversation Transcripts For Dsr

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get conversation transcripts for DSR export. Returns conversation transcripts for DSR compliance export.

```http
GET https://api.powerplatform.com/workflowsagent/conversationTranscripts?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/workflowsagent/conversationTranscripts?continuationToken={continuationToken}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| continuationToken | query |  | string | Continuation token for paging. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | DsrConversationTranscriptsResponse | Successful request. Conversation transcripts returned.<br><br>Headers<br><br>Retry-After: string |
| 401 Unauthorized |  | Unauthorized. |
| 403 Forbidden |  | Forbidden. |
| 404 Not Found |  | Not found. Workflows environment not resolved or not enabled. |
| 500 Internal Server Error |  | Internal server error. |

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
| ConversationTranscript | A single conversation transcript record. |
| ConversationTranscriptCompletion | A completion generated in the conversation response. |
| ConversationTranscriptFunction | Function details of a tool call. |
| ConversationTranscriptMessage | A message in the conversation. |
| ConversationTranscriptRequest | The request portion of a conversation transcript. |
| ConversationTranscriptResponse | The response portion of a conversation transcript. |
| ConversationTranscriptScenario | The scenario under which the conversation occurred. |
| ConversationTranscriptSystemMetadata | System metadata for a conversation transcript. |
| ConversationTranscriptTool | A tool available during the conversation. |
| ConversationTranscriptToolCall | A tool call within a conversation. |
| ConversationTranscriptToolFunction | Function definition of a tool. |
| DsrConversationTranscriptsResponse | Response containing conversation transcripts for DSR export. |

### ConversationTranscript

Object

A single conversation transcript record.

| Name | Type | Description |
| --- | --- | --- |
| objectId | string | The user object ID. |
| request | ConversationTranscriptRequest | The request portion of a conversation transcript. |
| requestCorrelationId | string | Request correlation ID for tracing. |
| response | ConversationTranscriptResponse | The response portion of a conversation transcript. |
| serviceRequestCorrelationId | string | Service request correlation ID for tracing. |
| systemMetadata | ConversationTranscriptSystemMetadata | System metadata for a conversation transcript. |
| tenantId | string | The tenant ID. |
| timestamp | string (date-time) | Timestamp of the conversation. |

### ConversationTranscriptCompletion

Object

A completion generated in the conversation response.

| Name | Type | Description |
| --- | --- | --- |
| finishReason | string | Reason the completion finished (e.g., stop, tool\_calls). |
| text | string | Generated text content. |
| toolCalls | ConversationTranscriptToolCall[] | Tool calls requested by the completion. |

### ConversationTranscriptFunction

Object

Function details of a tool call.

| Name | Type | Description |
| --- | --- | --- |
| arguments | string | JSON-encoded arguments passed to the function. |
| name | string | Name of the function called. |

### ConversationTranscriptMessage

Object

A message in the conversation.

| Name | Type | Description |
| --- | --- | --- |
| content | string | Text content of the message. |
| isCustomerContent | boolean | Whether this message contains customer content. |
| name | string | Name of the message sender, if applicable. |
| role | string | Role of the message sender (e.g., user, assistant, system, tool). |
| toolCallId | string | ID of the tool call this message is responding to. |
| toolCalls | ConversationTranscriptToolCall[] | Tool calls made in this message. |

### ConversationTranscriptRequest

Object

The request portion of a conversation transcript.

| Name | Type | Description |
| --- | --- | --- |
| messages | ConversationTranscriptMessage[] | Messages in the conversation request. |
| toolChoice | string | The tool choice strategy. |
| tools | ConversationTranscriptTool[] | Tools available during the conversation. |

### ConversationTranscriptResponse

Object

The response portion of a conversation transcript.

| Name | Type | Description |
| --- | --- | --- |
| completions | ConversationTranscriptCompletion[] | Completions generated by the model. |
| succeeded | boolean | Whether the response was successful. |

### ConversationTranscriptScenario

Enumeration

The scenario under which the conversation occurred.

| Value | Description |
| --- | --- |
| WorkflowsAgentRuntime |  |
| WorkflowsAgentAuthoring |  |

### ConversationTranscriptSystemMetadata

Object

System metadata for a conversation transcript.

| Name | Type | Description |
| --- | --- | --- |
| scenario | ConversationTranscriptScenario | The scenario under which the conversation occurred. |

### ConversationTranscriptTool

Object

A tool available during the conversation.

| Name | Type | Description |
| --- | --- | --- |
| function | ConversationTranscriptToolFunction | Function definition of a tool. |
| type | string | Type of the tool. |

### ConversationTranscriptToolCall

Object

A tool call within a conversation.

| Name | Type | Description |
| --- | --- | --- |
| function | ConversationTranscriptFunction | Function details of a tool call. |
| id | string | Unique identifier of the tool call. |
| type | string | Type of the tool call. |

### ConversationTranscriptToolFunction

Object

Function definition of a tool.

| Name | Type | Description |
| --- | --- | --- |
| description | string | Description of what the function does. |
| name | string | Name of the function. |
| parameters | object | JSON Schema defining the function parameters. |

### DsrConversationTranscriptsResponse

Object

Response containing conversation transcripts for DSR export.

| Name | Type | Description |
| --- | --- | --- |
| nextLink | string | URL to retrieve the next page of results, if available. |
| value | ConversationTranscript[] | List of conversation transcripts. |