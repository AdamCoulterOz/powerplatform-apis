---
layout: Reference
title: Rule Based Policies - List Rule Based Policies - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/list-rule-based-policies
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.listrulebasedpolicies
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
description: 'Learn more about Power Platform API service - List rule-based policies available in the tenant. '
locale: en-us
document_id: 2d6d88d3-62c3-a132-2829-4e43453a2034
document_version_independent_id: ce4889f0-bf9d-0613-6882-25366c52cb66
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/List-Rule-Based-Policies.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/list-rule-based-policies
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/List-Rule-Based-Policies.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: d7cb93e5-3463-074f-798f-0b4f179ff6ab
---

# Rule Based Policies - List Rule Based Policies

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

List rule-based policies available in the tenant.

```http
GET https://api.powerplatform.com/governance/ruleBasedPolicies?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ListPolicyResponse | The list of policies. |
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
| ListPolicyResponse |  |
| Policy |  |
| RuleSet |  |

### ListPolicyResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| value | Policy[] |  |

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

### RuleSet

Object

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier of the rule set. |
| inputs | object | The inputs for the rule set, which may vary based on the rule. |
| version | string | The version of the rule set. |