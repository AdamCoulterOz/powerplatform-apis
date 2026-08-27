---
layout: Reference
title: Rule Based Policies - Patch Rule Based Policy - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/patch-rule-based-policy
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.patchrulebasedpolicy
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
description: 'Learn more about Power Platform API service - Patch rule-based policy. Allows adding or updating one or more rule sets to an existing policy. '
locale: en-us
document_id: 42d9b053-ba17-1c3e-ea89-139cffebeb97
document_version_independent_id: ca9f815e-8b24-8515-5d48-f8dff7a2f468
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Patch-Rule-Based-Policy.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/patch-rule-based-policy
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Patch-Rule-Based-Policy.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 22da61a3-4464-ea05-d7ba-25a26dbe7615
---

# Rule Based Policies - Patch Rule Based Policy

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Patch rule-based policy. Allows adding or updating one or more rule sets to an existing policy.

```http
PATCH https://api.powerplatform.com/governance/ruleBasedPolicies/{policyId}?api-version=2024-10-01
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
| 200 OK | Policy | The updated policy. |
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
| Policy |  |
| PolicyRequest |  |
| RuleSet |  |

### Policy

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier of the policy assignment. |
| lastModified | string (date-time) | The date and time when the policy was last modified. |
| name | string | The name of the policy. |
| ruleSetCount | integer | The number of rule sets associated with this policy. |
| ruleSets | RuleSet[] |  |
| tenantId | string | The unique identifier of the tenant. |

### PolicyRequest

Object

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the policy. |
| ruleSets | RuleSet[] |  |

### RuleSet

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier of the rule set. |
| inputs | object | The inputs for the rule set, which may vary based on the rule. |
| version | string | The version of the rule set. |