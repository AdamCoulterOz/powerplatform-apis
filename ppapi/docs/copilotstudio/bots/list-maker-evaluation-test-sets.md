---
layout: Reference
title: Bots - List Maker Evaluation Test Sets - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/list-maker-evaluation-test-sets
uid: api.powerplatform.com.power-platform.copilotstudio.bots.listmakerevaluationtestsets
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
description: 'List maker evaluation test sets. Retrieves the list of test sets for a bot in a specified environment. '
locale: en-us
document_id: 66305d50-c0c6-7bc6-ea65-2939defd9794
document_version_independent_id: 1c120c2a-b986-7261-29e9-7ff9cef89444
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/List-Maker-Evaluation-Test-Sets.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/list-maker-evaluation-test-sets
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/List-Maker-Evaluation-Test-Sets.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 0a269742-9954-d41d-f7b6-913c45494320
---

# Bots - List Maker Evaluation Test Sets

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List maker evaluation test sets. Retrieves the list of test sets for a bot in a specified environment.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/makerevaluation/testsets?api-version=2024-10-01
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
| 200 OK | TestSetCollection | Successful response. |

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
| TestSetCollection | A collection of maker evaluation test sets. |

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

### TestSetCollection

Object

A collection of maker evaluation test sets.

| Name | Type | Description |
| --- | --- | --- |
| value | TestSet[] | The list of test sets. |