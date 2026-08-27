---
layout: Reference
title: Websites - Create Waf Rules - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/create-waf-rules
uid: api.powerplatform.com.power-platform.powerpages.websites.createwafrules
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
description: 'Create web application Firewall rules on a Power Pages website. Create web application Firewall rules on the given website. '
locale: en-us
document_id: c910e717-f030-2ef6-9c1a-bd9793eb61a8
document_version_independent_id: 4418ff65-8bb5-7b9e-f233-15ad843583be
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Create-Waf-Rules.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/create-waf-rules
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Create-Waf-Rules.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e8fdebed-2921-4997-a75a-fa863723a535
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/cf1e63a8-325f-42be-b60c-d84a95a42b1f
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
platformId: 8884edb4-1d1d-ff4a-8ef4-0bb95a3177a0
---

# Websites - Create Waf Rules

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create web application Firewall rules on a Power Pages website. Create web application Firewall rules on the given website.

```http
PUT https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/createWafRules?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| customRules | CustomRule[] |  |
| managedRules | ManagedRules[] |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |
| 404 Not Found | ErrorMessage | Not Found |

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
| CustomRule |  |
| Details |  |
| Error |  |
| ErrorMessage |  |
| ManagedRules |  |
| MatchConditions |  |
| RuleGroupOverrides |  |
| Rules |  |
| WafRuleAction | Action to take for the rule. |
| WafRuleType | WAF rule type. |
| WebApplicationFirewallRules |  |

### CustomRule

Object

| Name | Type | Description |
| --- | --- | --- |
| action | enum:<br>- Allow<br>- Block<br>- Log | Action to take when the rule matches |
| enabledState | enum:<br>- Disabled<br>- Enabled | State of the rule |
| matchConditions | MatchConditions[] |  |
| name | string | Name of the custom rule |
| priority | integer (int32) | Priority of the rule |
| rateLimitDurationInMinutes | integer (int32) | Duration in minutes for rate limiting |
| rateLimitThreshold | integer (int32) | Threshold for rate limiting |
| ruleType | WafRuleType | WAF rule type. |

### Details

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| message | string | Error message |
| target | string | Target parameter |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| details | Details[] |  |
| message | string | Error message |
| target | string | Target parameter |

### ErrorMessage

Object

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### ManagedRules

Object

| Name | Type | Description |
| --- | --- | --- |
| Exclusions | string[] | List of exclusions for the rule set |
| RuleGroupOverrides | RuleGroupOverrides[] |  |
| RuleSetAction | enum:<br>- Allow<br>- Block<br>- Log | Action to take for the rule set |
| RuleSetType | string | Type of the managed rule set |
| RuleSetVersion | string | Version of the managed rule set |

### MatchConditions

Object

| Name | Type | Description |
| --- | --- | --- |
| matchValue | string[] | Values to match |
| matchVariable | string | Variable to match |
| negateCondition | boolean | Whether to negate the condition |
| operator | enum:<br>- Contains<br>- EndsWith<br>- Equals<br>- GeoMatch<br>- StartsWith | Operator for the match condition |
| selector | string | Selector for the match variable |
| transforms | string[] | Transformations to apply |

### RuleGroupOverrides

Object

| Name | Type | Description |
| --- | --- | --- |
| Exclusions | string[] | List of exclusions for the rule group |
| RuleGroupName | string | Name of the rule group |
| Rules | Rules[] |  |

### Rules

Object

| Name | Type | Description |
| --- | --- | --- |
| Action | WafRuleAction | Action to take for the rule. |
| EnabledState | enum:<br>- Disabled<br>- Enabled | State of the rule |
| Exclusions | string[] | List of exclusions for the rule |
| RuleId | string | ID of the rule |

### WafRuleAction

Enumeration

Action to take for the rule.

| Value | Description |
| --- | --- |
| Allow |  |
| Block |  |
| Log |  |
| AnomalyScoring |  |

### WafRuleType

Enumeration

WAF rule type.

| Value | Description |
| --- | --- |
| MatchRule |  |
| RateLimitRule |  |

### WebApplicationFirewallRules

Object

| Name | Type | Description |
| --- | --- | --- |
| customRules | CustomRule[] |  |
| managedRules | ManagedRules[] |  |