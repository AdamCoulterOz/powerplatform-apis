---
layout: Reference
title: Billing Policy Environment - Get Billing Policy Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy-environment/get-billing-policy-environment
uid: api.powerplatform.com.power-platform.licensing.billingpolicyenvironment.getbillingpolicyenvironment
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
description: 'Learn more about Power Platform API service - Get the environment linked to the billing policy. '
locale: en-us
document_id: 3d63a164-a334-4e0e-1510-cad28a341257
document_version_independent_id: 5b4a6ad0-8a50-7942-b271-6eb99d346ded
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/Get-Billing-Policy-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy-environment/get-billing-policy-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/Get-Billing-Policy-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 109ec183-1117-9371-9b0f-d11cb631980c
---

# Billing Policy Environment - Get Billing Policy Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the environment linked to the billing policy.

```http
GET https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}/environments/{environmentId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| billingPolicyId | path | True | string | The billing policy ID. |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BillingPolicyEnvironmentResponseModelV1 | Success |
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

### BillingPolicyEnvironmentResponseModelV1

Object

| Name | Type | Description |
| --- | --- | --- |
| billingPolicyId | string |  |
| environmentId | string |  |