---
layout: Reference
title: Allocations By Environment - Get Allocations By Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/allocations-by-environment/get-allocations-by-environment
uid: api.powerplatform.com.power-platform.licensing.allocationsbyenvironment.getallocationsbyenvironment
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
description: 'Learn more about Power Platform API service - Get currency allocations and enforcement rules for an environment. '
locale: en-us
document_id: 94ac5bd0-7545-cf22-777d-7ff137fe71de
document_version_independent_id: cc398ecd-9c80-27a3-3acf-db74860cfc56
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Allocations-By-Environment/Get-Allocations-By-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/allocations-by-environment/get-allocations-by-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Allocations-By-Environment/Get-Allocations-By-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 1e1b2521-4e64-e862-9278-c525da194d0d
---

# Allocations By Environment - Get Allocations By Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get currency allocations and enforcement rules for an environment.

```http
GET https://api.powerplatform.com/licensing/allocationsByEnvironment/{environmentId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | AllocationByEnvironmentModel | Success |
| 400 Bad Request |  | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 404 Not Found |  | Not Found |

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
| AllocationByEnvironmentModel | The currency allocations and enforcement rules for an environment. |
| CurrencyAllocationModel |  |
| EnforcementRule |  |
| EnforcementRuleTypes |  |
| ExternalCurrencyType | Available currency type which can be allocated to environment. |

### AllocationByEnvironmentModel

Object

The currency allocations and enforcement rules for an environment.

| Name | Type | Description |
| --- | --- | --- |
| currencyAllocations | CurrencyAllocationModel[] | The per-currency allocations, including enforcement rules such as TenantPool that can be enabled or disabled. |
| environmentId | string | The environment ID. |

### CurrencyAllocationModel

Object

| Name | Type | Description |
| --- | --- | --- |
| allocated | integer (int32) |  |
| autoAllocated | integer (int32) |  |
| currencyType | ExternalCurrencyType | Available currency type which can be allocated to environment. |
| enforcementRules | EnforcementRule[] |  |

### EnforcementRule

Object

| Name | Type | Description |
| --- | --- | --- |
| enabled | boolean |  |
| ruleType | EnforcementRuleTypes |  |

### EnforcementRuleTypes

Enumeration

| Value | Description |
| --- | --- |
| Alert |  |
| PayGo |  |
| TenantPool |  |
| Deny |  |

### ExternalCurrencyType

Enumeration

Available currency type which can be allocated to environment.

| Value | Description |
| --- | --- |
| AI |  |
| AppPass |  |
| AppPassForTeams |  |
| Invoice |  |
| MCSSessions |  |
| MCSMessages |  |
| PAHostedRPA |  |
| PAUnattendedRPA |  |
| PerFlowPlan |  |
| PortalAddOns |  |
| PortalLogins |  |
| PortalViews |  |
| PowerPagesAuthenticated |  |
| PowerPagesAnonymous |  |
| PowerAutomatePerProcess |  |
| ProcessMiningDataStorage |  |
| SCMessages |  |
| VAConversations |  |