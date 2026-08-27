---
layout: Reference
title: Bots - Get Maker Evaluation Test Set - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/get-maker-evaluation-test-set
uid: api.powerplatform.com.power-platform.copilotstudio.bots.getmakerevaluationtestset
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
description: 'Learn more about Power Platform API service - Get maker evaluation test set by ID. Get a specific test set for maker evaluation of a bot. '
locale: en-us
document_id: bb0a94ee-ce4a-6def-3097-5b06c8011774
document_version_independent_id: d90437ea-6166-4d16-337d-94f4f63beabc
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Maker-Evaluation-Test-Set.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/get-maker-evaluation-test-set
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Maker-Evaluation-Test-Set.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c8f84df2-1adc-a539-fda9-e5e954dca7fb
---

# Bots - Get Maker Evaluation Test Set

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get maker evaluation test set by ID. Get a specific test set for maker evaluation of a bot.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/makerevaluation/testsets/{TestSetId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| TestSetId | path | True | string | The test set ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TestSet | Successful response. |

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
| AuditInfo | Audit information for a resource. |
| StateCode | The state of an evaluation run describing the currently active stage. |
| TestSet | The response payload for a get test set request. |

### AuditInfo

Object

Audit information for a resource.

| Name | Type | Description |
| --- | --- | --- |
| createdBy | string (uuid) | The ID of the user who created the record. |
| createdTimeUtc | string (date-time) | The UTC time when the record was created. |
| modifiedBy | string (uuid) | The ID of the user who last modified the record. |
| modifiedTimeUtc | string (date-time) | The UTC time when the record was last modified. |

### StateCode

Enumeration

The state of an evaluation run describing the currently active stage.

| Value | Description |
| --- | --- |
| Active |  |
| Inactive |  |
| Unknown |  |

### TestSet

Object

The response payload for a get test set request.

| Name | Type | Description |
| --- | --- | --- |
| auditInfo | AuditInfo | Audit information for a resource. |
| description | string | Description of the test set. |
| displayName | string | Display name of the test set. |
| id | string | The unique identifier for the test set component. |
| state | StateCode | The state of an evaluation run describing the currently active stage. |
| totalTestCases | integer | The number of test cases in the test set. |