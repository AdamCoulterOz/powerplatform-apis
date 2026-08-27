---
layout: Reference
title: Rule Sets - Create Rule Set - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-sets/create-rule-set
uid: api.powerplatform.com.power-platform.governance.rulesets.createruleset
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
description: 'Learn more about Power Platform API service - Create Rule Set. Creates the Rule Set for the environment group. '
locale: en-us
document_id: 55a7ee73-c32f-562a-2888-44d2b884c98c
document_version_independent_id: 696dcd77-90a3-149f-5182-28cb8d38513f
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Sets/Create-Rule-Set.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-sets/create-rule-set
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Sets/Create-Rule-Set.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: e9e0a84a-d76a-f61b-c3d1-35e5f1e855e2
---

# Rule Sets - Create Rule Set

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Create Rule Set. Creates the Rule Set for the environment group.

```http
POST https://api.powerplatform.com/governance/environmentGroups/{groupId}/ruleSets?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| groupId | path | True | string (uuid) | The unique identifier of the environment group. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| environmentFilter | MgGovPolicyEnvironmentFilter | Defines the environment filters. |
| id | string | The ID of the Rule Set. |
| lastModified | string (date-time) | The last modified timestamp. |
| parameters | RuleSetParameters[] | The Rule Set parameters. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 201 Created | RuleSetDto | Successfully created Rule Set. |
| 204 No Content |  | No Content. |
| 400 Bad Request | MgGovErrorResponse | Bad Request. |
| 401 Unauthorized | MgGovErrorResponse | Unauthorized. |
| 403 Forbidden | MgGovErrorResponse | Forbidden. |
| 500 Internal Server Error | MgGovErrorResponse | Internal Server Error. |

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
| Error |  |
| MgGovEnvironmentValues | Environment information. |
| MgGovErrorResponse | Standard error response. |
| MgGovFilterType | The type of environment filter. |
| MgGovPolicyEnvironmentFilter | Defines the environment filters. |
| MgGovResourceType | The type of resource. |
| MgGovRule | A rule definition. |
| MgGovRuleSetType | The type of the Rule Set. |
| RuleSetDto | Rule Set data transfer object. |
| RuleSetParameters | Parameters for a Rule Set. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### MgGovEnvironmentValues

Object

Environment information.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The ID of the environment. |
| name | string | The name of the environment. |
| type | string | The type of the environment. |

### MgGovErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |

### MgGovFilterType

Enumeration

The type of environment filter.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Include |  |
| Exclude |  |

### MgGovPolicyEnvironmentFilter

Object

Defines the environment filters.

| Name | Type | Description |
| --- | --- | --- |
| type | MgGovFilterType | The type of environment filter. |
| values | MgGovEnvironmentValues[] | The environment information. |

### MgGovResourceType

Enumeration

The type of resource.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Flow |  |
| App |  |
| AuthoringBot |  |
| UsersBot |  |

### MgGovRule

Object

A rule definition.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The rule ID. |
| value | string | The rule value. |

### MgGovRuleSetType

Enumeration

The type of the Rule Set.

| Value | Description |
| --- | --- |
| NotSpecified |  |
| Sharing |  |
| AdminDigest |  |
| SolutionChecker |  |
| MakerOnboarding |  |
| Lifecycle |  |
| Copilot |  |
| CrossGeoCopilotDataMovement |  |
| GenerativeAISettings |  |
| CopilotAuth |  |
| FlowAutomationRestrictions |  |

### RuleSetDto

Object

Rule Set data transfer object.

| Name | Type | Description |
| --- | --- | --- |
| environmentFilter | MgGovPolicyEnvironmentFilter | Defines the environment filters. |
| id | string | The ID of the Rule Set. |
| lastModified | string (date-time) | The last modified timestamp. |
| parameters | RuleSetParameters[] | The Rule Set parameters. |

### RuleSetParameters

Object

Parameters for a Rule Set.

| Name | Type | Description |
| --- | --- | --- |
| resourceType | MgGovResourceType | The type of resource. |
| type | MgGovRuleSetType | The type of the Rule Set. |
| value | MgGovRule[] | The rule values. |