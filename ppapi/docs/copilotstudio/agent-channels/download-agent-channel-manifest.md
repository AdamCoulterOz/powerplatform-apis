---
layout: Reference
title: Agent Channels - Download Agent Channel Manifest - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/agent-channels/download-agent-channel-manifest
uid: api.powerplatform.com.power-platform.copilotstudio.agentchannels.downloadagentchannelmanifest
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
description: 'Download agent channel manifest. Downloads the channel manifest package for the specified agent and channel as a zip file. Currently only the "M365" channel is '
locale: en-us
document_id: 45e06bec-03c9-3f26-9456-dd61951920f4
document_version_independent_id: 5e2020f6-2b88-54d0-843b-fa05c038e7e6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Agent-Channels/Download-Agent-Channel-Manifest.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/agent-channels/download-agent-channel-manifest
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Agent-Channels/Download-Agent-Channel-Manifest.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/1dd701e0-441f-4b0a-9806-aa47decc4e35
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/0a2fc935-5977-4aa6-9f55-0be03bd2acb8
platformId: a044637b-fe05-0847-c4e7-0224f2656741
---

# Agent Channels - Download Agent Channel Manifest

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Download agent channel manifest. Downloads the channel manifest package for the specified agent and channel as a zip file. Currently only the "M365" channel is supported.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/agents/{AgentId}/channels/{ChannelName}/download?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/agents/{AgentId}/channels/{ChannelName}/download?includeAgentSchema={includeAgentSchema}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| AgentId | path | True | string (uuid) | The bot ID. |
| ChannelName | path | True | string | The channel name. Currently only "M365" is supported. |
| EnvironmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| includeAgentSchema | query |  | boolean | Whether to include the agent schema in the downloaded manifest package. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | string | The channel manifest package as a downloadable zip file.<br><br>Media Types: "application/zip" |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |