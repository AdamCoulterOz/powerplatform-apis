---
layout: Reference
title: Rule Based Policies - Update Rule Based Policy By ID - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/update-rule-based-policy-by-id
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.updaterulebasedpolicybyid
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
description: 'Learn more about Power Platform API service - Update rule-based policy by ID. Updates a policy by ID including rule sets and metadata. '
locale: en-us
document_id: 5b851566-51cf-0d5c-92cb-455b02a8a68f
document_version_independent_id: f786e5e5-49a4-7950-a71b-5b32b0b6fcd5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Update-Rule-Based-Policy-By-ID.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/update-rule-based-policy-by-id
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Update-Rule-Based-Policy-By-ID.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: c9a5aa30-ec8a-28c0-8aa7-997d8cd51584
---

# Rule Based Policies - Update Rule Based Policy By ID

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update rule-based policy by ID. Updates a policy by ID including rule sets and metadata.

```http
PUT https://api.powerplatform.com/governance/ruleBasedPolicies/{policyId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| policyId | path | True | string | The unique identifier of the policy. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the policy. |
| ruleSets | RuleSet[] |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | RuleAssignment | The details of the policy. |
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
| PolicyRequest |  |
| RuleAssignment |  |
| RuleSet |  |

### PolicyRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the policy. |
| ruleSets | RuleSet[] |  |

### RuleAssignment

Object

| Name | Type | Description |
| --- | --- | --- |
| policyId | string | The unique identifier of the policy. |
| resourceId | string | The unique identifier of the resource. |
| resourceType | enum:<br>- Environment<br>- EnvironmentGroup<br>- NotSpecified | The type of resource assigned to the rule. |
| ruleSetCount | integer | The count of rule sets assigned. |
| tenantId | string | The unique identifier of the tenant. |

### RuleSet

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier of the rule set. |
| inputs | object | The inputs for the rule set, which may vary based on the rule. |
| version | string | The version of the rule set. |