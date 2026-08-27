---
layout: Reference
title: Websites - Get WAF Rules - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/get-waf-rules
uid: api.powerplatform.com.power-platform.powerpages.websites.getwafrules
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
description: 'Learn more about Power Platform API service - Get the web application firewall rules associated with the given website. '
locale: en-us
document_id: f583db58-3619-cc8d-b97f-8b908a04c129
document_version_independent_id: aff21c7a-05de-ce4d-231a-60f990a5597d
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Get-WAF-Rules.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/get-waf-rules
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Get-WAF-Rules.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e8fdebed-2921-4997-a75a-fa863723a535
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/cf1e63a8-325f-42be-b60c-d84a95a42b1f
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 6ba5358f-2060-5584-77fc-9cef48378429
---

# Websites - Get WAF Rules

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the web application firewall rules associated with the given website.

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/getWafRules?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/getWafRules?ruleType={ruleType}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |
| ruleType | query |  | string | Type of web application firewall rules to retrieve. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | WebApplicationFirewallConfiguration | Success |
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
| WebApplicationFirewallConfiguration |  |

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

### WebApplicationFirewallConfiguration

Object

| Name | Type | Description |
| --- | --- | --- |
| CustomRules | CustomRule[] |  |
| ManagedRules | ManagedRules[] |  |