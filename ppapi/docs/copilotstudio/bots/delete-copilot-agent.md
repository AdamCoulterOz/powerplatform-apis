---
layout: Reference
title: Bots - Delete Copilot Agent - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/delete-copilot-agent
uid: api.powerplatform.com.power-platform.copilotstudio.bots.deletecopilotagent
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
description: 'Learn more about Power Platform API service - Delete a bot in Copilot Studio. '
locale: en-us
document_id: e0b542d7-1341-1a4a-038b-07fb1de79dcb
document_version_independent_id: 1dc1314a-14b8-b981-e781-c06659d582a7
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Delete-Copilot-Agent.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/delete-copilot-agent
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Delete-Copilot-Agent.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/46e3c7c4-fe77-4a6e-b40a-44c569819fa5
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d0c6fab8-2d7d-4bb0-bf40-589e08d7c132
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 49f150a8-ff8d-199a-1202-9305bd9ceafe
---

# Bots - Delete Copilot Agent

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete a bot in Copilot Studio.

```http
DELETE https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/botAdminOperations?api-version=2024-10-01
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
| 200 OK |  | Successful response |

## Security

### oauth2

Microsoft Entra ID OAuth2

Type:  oauth2Flow:  implicitAuthorization URL:  https://login.microsoftonline.com/common/oauth2/authorize?resource=https://api.powerplatform.com

#### Scopes

| Name | Description |
| --- | --- |
| .default | .default |