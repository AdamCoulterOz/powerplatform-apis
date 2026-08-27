---
layout: Reference
title: Rule Based Policies - Create Rule Based Policy - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-based-policies/create-rule-based-policy
uid: api.powerplatform.com.power-platform.governance.rulebasedpolicies.createrulebasedpolicy
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
description: 'Learn more about Power Platform API service - Create rule-based policy. Creates a rule-based policy with rule sets and metadata. '
locale: en-us
document_id: 8d9ed413-f17f-340f-d110-22bb1143ef53
document_version_independent_id: 5adab4ed-17c0-70b0-5f48-165aac3ff567
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Create-Rule-Based-Policy.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-based-policies/create-rule-based-policy
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Based-Policies/Create-Rule-Based-Policy.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5a847e3f-5bba-c384-8a7d-4686d761432b
---

# Rule Based Policies - Create Rule Based Policy

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create rule-based policy. Creates a rule-based policy with rule sets and metadata.

```http
POST https://api.powerplatform.com/governance/ruleBasedPolicies?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of the policy. |
| ruleSets | RuleSet[] |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | Policy | The details of the policy. |
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