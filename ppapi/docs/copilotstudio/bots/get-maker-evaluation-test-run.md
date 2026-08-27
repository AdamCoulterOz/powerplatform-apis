---
layout: Reference
title: Bots - Get Maker Evaluation Test Run - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots/get-maker-evaluation-test-run
uid: api.powerplatform.com.power-platform.copilotstudio.bots.getmakerevaluationtestrun
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
description: 'Get maker evaluation test run by ID. Get the status and results of a specific maker evaluation test run. '
locale: en-us
document_id: 9218fb0c-00fc-f3ee-1327-6e825d8b799e
document_version_independent_id: aa878208-1984-d473-b108-10df8f7ce547
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Maker-Evaluation-Test-Run.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/copilotstudio/bots/get-maker-evaluation-test-run
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/copilotstudio/Bots/Get-Maker-Evaluation-Test-Run.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: e4cf9701-6ea1-deac-5417-033170f8d120
---

# Bots - Get Maker Evaluation Test Run

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get maker evaluation test run by ID. Get the status and results of a specific maker evaluation test run.

```http
GET https://api.powerplatform.com/copilotstudio/environments/{EnvironmentId}/bots/{BotId}/api/makerevaluation/testruns/{TestRunId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| BotId | path | True | string | The bot ID. |
| EnvironmentId | path | True | string | The environment ID. |
| TestRunId | path | True | string (uuid) | The test run ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | TestRun | Successful response. |

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
| Metric | A grader metric associated with a test case in a maker evaluation run. |
| MetricErrorReason | The error reason providing additional information about a metric evaluation result. |
| MetricResult | The result of a grader metric in a maker evaluation run. |
| MetricStatus | The status of a grader metric result in a maker evaluation run. |
| MetricType | The type of a grader metric in a maker evaluation run. |
| TestCaseResult | The result of a test case in a maker evaluation run. |
| TestCaseState | The state of a test case in a maker evaluation run. |
| TestRun | The response payload for a get evaluation run details request. |

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

### Metric

Object

A grader metric associated with a test case in a maker evaluation run.

| Name | Type | Description |
| --- | --- | --- |
| result | MetricResult | The result of a grader metric in a maker evaluation run. |
| type | MetricType | The type of a grader metric in a maker evaluation run. |

### MetricErrorReason

Enumeration

The error reason providing additional information about a metric evaluation result.

| Value | Description |
| --- | --- |
| AgentResponseIsNullOrEmpty |  |
| EmptyOrInvalidModelResponse |  |
| ExpectedInvocationStepsAreNullOrEmpty |  |
| ExpectedKeywordsAreNullOrEmpty |  |
| ExpectedOutputIsNullOrEmpty |  |
| GraderCreationFailed |  |
| InputOutputCountMismatch |  |
| IntentMatchInvalidMatchType |  |
| ModelLabelGraderInvalidLabel |  |
| QueryIsNullOrEmpty |  |
| RequestTokenLimitExceeded |  |
| RetrievedKnowledgeSourcesTextsAreEmpty |  |
| RetrievedKnowledgeTokenLimitExceeded |  |
| UnexpectedInternalError |  |

### MetricResult

Object

The result of a grader metric in a maker evaluation run.

| Name | Type | Description |
| --- | --- | --- |
| aiResultReason | string | The reason generated by LLM, providing additional context to the evaluation result. |
| data | object | The set of key-value pairs that defines this metric. Keys are normalized to lowercase. |
| errorReason | MetricErrorReason | The error reason providing additional information about a metric evaluation result. |
| status | MetricStatus | The status of a grader metric result in a maker evaluation run. |

### MetricStatus

Enumeration

The status of a grader metric result in a maker evaluation run.

| Value | Description |
| --- | --- |
| Error |  |
| Fail |  |
| Pass |  |
| Unknown |  |

### MetricType

Enumeration

The type of a grader metric in a maker evaluation run.

| Value | Description |
| --- | --- |
| AllKeywordMatch |  |
| AnyKeywordMatch |  |
| CapabilityUse |  |
| CompareMeaning |  |
| CustomLabels |  |
| ExactMatch |  |
| GeneralQuality |  |
| TextSimilarity |  |
| Unknown |  |

### TestCaseResult

Object

The result of a test case in a maker evaluation run.

| Name | Type | Description |
| --- | --- | --- |
| metricsResults | Metric[] | The list of grader metrics associated with the test case. |
| state | TestCaseState | The state of a test case in a maker evaluation run. |
| testCaseId | string (uuid) | The ID of the object model entity that the test case is sourced from. |

### TestCaseState

Enumeration

The state of a test case in a maker evaluation run.

| Value | Description |
| --- | --- |
| Cancelled |  |
| Completed |  |
| Error |  |
| Running |  |
| Unknown |  |

### TestRun

Object

The response payload for a get evaluation run details request.

| Name | Type | Description |
| --- | --- | --- |
| cdsBotId | string (uuid) | The CDS bot ID where the evaluation run is executed. |
| endTime | string (date-time) | The timestamp when the evaluation run ended. |
| environmentId | string | The environment ID where the evaluation run is executed. |
| id | string (uuid) | The unique identifier for this evaluation run. |
| mcsConnectionId | string | The MCS connection ID used in the evaluation run. |
| name | string | The name of the evaluation run. |
| ownerId | string | The ID of the owner who initiated the evaluation run. |
| startTime | string (date-time) | The timestamp when the evaluation run started. |
| state | EvaluationRunState | The state of an evaluation run describing the currently active stage. |
| testCasesResults | TestCaseResult[] | The test cases and their results in the evaluation run. |
| testSetId | string (uuid) | The ID of the object model test set entity record that the run is associated with. |
| totalTestCases | integer | Number of test cases included in the evaluation run. |