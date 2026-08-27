---
layout: Reference
title: Bots - Run Maker Evaluation Test Set - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/run-maker-evaluation-test-set
uid: api.powerplatform.com.power-platform.copilotstudio.bots.runmakerevaluationtestset
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
description: 'Learn more about Power Platform API service - Run maker evaluation test set. Trigger a maker evaluation test run for a specific test set. '
locale: en-us
document_id: cb1b240b-6836-c295-0a40-f075a6594dab
document_version_independent_id: a11d24ae-98c1-4068-86ae-5eea5627e394
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Run-Maker-Evaluation-Test-Set.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/run-maker-evaluation-test-set
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Run-Maker-Evaluation-Test-Set.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 009e6d45-1f03-9f6c-2a3c-1dc9e867af0d
---

# Bots - Run Maker Evaluation Test Set

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Run maker evaluation test set. Trigger a maker evaluation test run for a specific test set.

```http
POST https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/makerevaluation/testsets/{TestSetId}/run?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| TestSetId | path | True | string | The test set ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| evaluationRunName | string | The name of the evaluation run. |
| mcsConnectionId | string | The connection ID for the MCS connector that is used to execute the evaluation run, or leave empty for an anonymous run. |
| runOnPublishedBot | boolean | Indicates whether the operation should run on a published bot instance. If set to false, the operation will run on a draft bot instance. |
| toolsConnections | ToolsConnections[] | The tools connections that will be used to execute the evaluation run. This is a list of tools along with the corresponding user connections that should be used for each tool. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RunStatusResponse | Successful response. |
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

| Name | Description |
| --- | --- |
| EvaluationRunState | The state of an evaluation run describing the currently active stage. |
| ExecutionState | The current execution state indicating the progress status of a maker evaluation run. |
| MakerEvaluationConnection | A connector and its associated user connection for a maker evaluation run. |
| RunStatusResponse | The response payload from triggering an evaluation run request. |
| RunTestSetRequestBody | Request body for triggering a maker evaluation test run. |
| ToolsConnections | A tool along with the corresponding user connections to use for a maker evaluation run. |

### EvaluationRunState

Enumeration

The state of an evaluation run describing the currently active stage.

| Value | Description |
| --- | --- |
| Abandoned |  |
| Cancelled |  |
| Completed |  |
| Deleted |  |
| Failed |  |
| InProgress |  |
| Queued |  |
| Unknown |  |

### ExecutionState

Enumeration

The current execution state indicating the progress status of a maker evaluation run.

| Value | Description |
| --- | --- |
| Abandoned |  |
| Cancelled |  |
| Completed |  |
| CreatingRunContent |  |
| Deleted |  |
| EvaluatingRun |  |
| Failed |  |
| Initializing |  |
| ProcessingRunContent |  |
| Queued |  |
| Unknown |  |

### MakerEvaluationConnection

Object

A connector and its associated user connection for a maker evaluation run.

| Name | Type | Description |
| --- | --- | --- |
| connectionId | string | User connection ID. |
| connectionReferenceName | string | Connection reference name in the bot definition. |
| connectorId | string | The tool (connector) ID. |

### RunStatusResponse

Object

The response payload from triggering an evaluation run request.

| Name | Type | Description |
| --- | --- | --- |
| callbackUri | string (uri) | The URI to poll for the evaluation run results. |
| executionState | ExecutionState | The current execution state indicating the progress status of a maker evaluation run. |
| lastUpdatedAt | string (date-time) | The timestamp when the last status update occurred. |
| runId | string (uuid) | The unique identifier for this evaluation run. |
| state | EvaluationRunState | The state of an evaluation run describing the currently active stage. |
| testCasesProcessed | integer | The number of test cases processed so far in the evaluation run. |
| totalTestCases | integer | Total number of test cases to be processed in the evaluation run. |

### RunTestSetRequestBody

Object

Request body for triggering a maker evaluation test run.

| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| evaluationRunName | string |  | The name of the evaluation run. |
| mcsConnectionId | string |  | The connection ID for the MCS connector that is used to execute the evaluation run, or leave empty for an anonymous run. |
| runOnPublishedBot | boolean | False | Indicates whether the operation should run on a published bot instance. If set to false, the operation will run on a draft bot instance. |
| toolsConnections | ToolsConnections[] |  | The tools connections that will be used to execute the evaluation run. This is a list of tools along with the corresponding user connections that should be used for each tool. |

### ToolsConnections

Object

A tool along with the corresponding user connections to use for a maker evaluation run.

| Name | Type | Description |
| --- | --- | --- |
| botId | string | The Dataverse bot ID. |
| botSchemaName | string | Bot schema name. |
| connections | MakerEvaluationConnection[] | A list of connections. |