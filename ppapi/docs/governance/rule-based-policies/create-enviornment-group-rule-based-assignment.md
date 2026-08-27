---
layout: Reference
title: Rule Based Policies - Create Enviornment Group Rule Based Assignment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/create-enviornment-group-rule-based-assignment
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.createenviornmentgrouprulebasedassignment
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
description: 'Create environment group rule-based assignment. Creates a rule-based policy assignment for an environment group. '
locale: en-us
document_id: f50ff98d-43be-3293-e045-6d94f4dacd05
document_version_independent_id: ee5d9c71-9dff-3a18-da07-9db011d46acf
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Create-Enviornment-Group-Rule-Based-Assignment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/create-enviornment-group-rule-based-assignment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Create-Enviornment-Group-Rule-Based-Assignment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: a7c73c7c-3c5b-0b0c-fbf0-fa781924dd93
---

# Rule Based Policies - Create Enviornment Group Rule Based Assignment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create environment group rule-based assignment. Creates a rule-based policy assignment for an environment group.

```http
POST https://api.powerplatform.com/governance/ruleBasedPolicies/{policyId}/environmentGroups/{groupId}/assignments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| groupId | path | True | string | The unique identifier of the environment group. |
| policyId | path | True | string | The unique identifier of the policy. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| assignmentOverrides | PolicyAssignmentOverride[] | List of policy assignment overrides. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RuleAssignment | The details of the policy. |
| 201 Created | RuleAssignment | Record created. |
| 400 Bad Request |  | Bad Request - The query parameters are invalid. |
| 401 Unauthorized |  | Unauthorized - Invalid credentials or missing authentication. |
| 404 Not Found |  | Not Found - The specified resource does not exist. |
| 500 Internal Server Error |  | Internal Server Error - Unexpected server error. |

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
| PolicyAssignmentOverride |  |
| PolicyAssignmentRequest |  |
| RuleAssignment |  |

### PolicyAssignmentOverride

Object

| Name | Type | Description |
| --- | --- | --- |
| behaviorType | enum:<br>- Exclude<br>- Include<br>- NotSpecified | The Behavior type. |
| resourceId | string | Resource ID; for example, the environment group ID. |
| resourceType | enum:<br>- Environment<br>- EnvironmentGroup<br>- NotSpecified<br>- Tenant | The Resource type. |

### PolicyAssignmentRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| assignmentOverrides | PolicyAssignmentOverride[] | List of policy assignment overrides. |

### RuleAssignment

Object

| Name | Type | Description |
| --- | --- | --- |
| policyId | string | The unique identifier of the policy. |
| resourceId | string | The unique identifier of the resource. |
| resourceType | enum:<br>- Environment<br>- EnvironmentGroup<br>- NotSpecified | The type of resource assigned to the rule. |
| ruleSetCount | integer | The count of rule sets assigned. |
| tenantId | string | The unique identifier of the tenant. |