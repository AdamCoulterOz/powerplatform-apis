---
layout: Reference
title: Rule Based Policies - List Rule Assignments By Environment Id - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/list-rule-assignments-by-environment-id
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.listruleassignmentsbyenvironmentid
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
description: 'List rule-based policy assignments for a specific environment. Lists rule assignments for a specific environment. '
locale: en-us
document_id: 5041477f-eaad-41f5-14a7-aef75ce6cffe
document_version_independent_id: d982e35e-1ebd-ac80-ba7d-465d4b11594d
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/List-Rule-Assignments-By-Environment-Id.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/list-rule-assignments-by-environment-id
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/List-Rule-Assignments-By-Environment-Id.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 695f4699-a959-d52a-e1d1-4eccb99b563f
---

# Rule Based Policies - List Rule Assignments By Environment Id

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List rule-based policy assignments for a specific environment. Lists rule assignments for a specific environment.

```http
GET https://api.powerplatform.com/governance/ruleBasedPolicies/environments/{environmentId}/assignments?includeRuleSetCounts={includeRuleSetCounts}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The unique identifier of the environment group. |
| api-version | query | True | string | The API version. |
| includeRuleSetCounts | query | True | boolean | Flag to include rule set counts in the response. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RuleAssignmentsResponse | A list of policy assignments for the specified policy. |
| 400 Bad Request |  | Bad Request - The query parameters are invalid. |
| 401 Unauthorized |  | Unauthorized - Invalid credentials or missing authentication. |
| 404 Not Found |  | Not Found - The specified policy does not exist. |
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
| RuleAssignment |  |
| RuleAssignmentsResponse |  |

### RuleAssignment

Object

| Name | Type | Description |
| --- | --- | --- |
| policyId | string | The unique identifier of the policy. |
| resourceId | string | The unique identifier of the resource. |
| resourceType | enum:<br>- Environment<br>- EnvironmentGroup<br>- NotSpecified | The type of resource assigned to the rule. |
| ruleSetCount | integer | The count of rule sets assigned. |
| tenantId | string | The unique identifier of the tenant. |

### RuleAssignmentsResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| value | RuleAssignment[] |  |