---
layout: Reference
title: Billing Policy Environment - List Billing Policy Environments - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy-environment/list-billing-policy-environments
uid: api.powerplatform.com.power-platform.licensing.billingpolicyenvironment.listbillingpolicyenvironments
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
description: 'Learn more about Power Platform API service - Get the list of environments linked to the billing policy. '
locale: en-us
document_id: 67a17003-f199-2e0b-5ba0-16abe3e39bf9
document_version_independent_id: 9f9b619f-75ea-adc0-21d3-b70f2dc4ddb0
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/List-Billing-Policy-Environments.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy-environment/list-billing-policy-environments
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/List-Billing-Policy-Environments.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 885c81b8-8349-b4e5-55b5-fa5184aaeda0
---

# Billing Policy Environment - List Billing Policy Environments

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get the list of environments linked to the billing policy.

```http
GET https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}/environments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| billingPolicyId | path | True | string | The billing policy ID. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BillingPolicyEnvironmentResponseModelV1ResponseWithOdataContinuation | Success |
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
| BillingPolicyEnvironmentResponseModelV1 |  |
| BillingPolicyEnvironmentResponseModelV1ResponseWithOdataContinuation |  |

### BillingPolicyEnvironmentResponseModelV1

Object

| Name | Type | Description |
| --- | --- | --- |
| billingPolicyId | string |  |
| environmentId | string |  |

### BillingPolicyEnvironmentResponseModelV1ResponseWithOdataContinuation

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextLink | string |  |
| value | BillingPolicyEnvironmentResponseModelV1[] |  |