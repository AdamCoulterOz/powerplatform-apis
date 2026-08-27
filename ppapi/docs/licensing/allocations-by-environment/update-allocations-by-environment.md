---
layout: Reference
title: Allocations By Environment - Update Allocations By Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/allocations-by-environment/update-allocations-by-environment
uid: api.powerplatform.com.power-platform.licensing.allocationsbyenvironment.updateallocationsbyenvironment
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
description: 'Learn more about Power Platform API service - Update currency allocations and enforcement rules for an environment. '
locale: en-us
document_id: 337d3a74-913a-bbfc-6f0d-3db6960f307e
document_version_independent_id: 02ff52c9-04bc-b9aa-7761-4da480e4e807
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Allocations-By-Environment/Update-Allocations-By-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/allocations-by-environment/update-allocations-by-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Allocations-By-Environment/Update-Allocations-By-Environment.yml
platformId: a7c0520b-8129-e844-bec5-7f3729a91946
---

# Allocations By Environment - Update Allocations By Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update currency allocations and enforcement rules for an environment.

```http
PATCH https://api.powerplatform.com/licensing/allocationsByEnvironment?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| currencyAllocations | CurrencyAllocationModel[] | The per-currency allocations, including enforcement rules such as TenantPool that can be enabled or disabled. |
| environmentId | string | The environment ID. |

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