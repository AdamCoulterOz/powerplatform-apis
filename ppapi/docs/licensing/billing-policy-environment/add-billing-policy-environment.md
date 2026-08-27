---
layout: Reference
title: Billing Policy Environment - Add Billing Policy Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/licensing/billing-policy-environment/add-billing-policy-environment
uid: api.powerplatform.com.power-platform.licensing.billingpolicyenvironment.addbillingpolicyenvironment
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
description: 'Learn more about Power Platform API service - Link billing policy ID with environments. '
locale: en-us
document_id: aa4de92e-fce4-dfda-41c9-e5cfdbd9b7ca
document_version_independent_id: f7f5074e-ade4-a0f9-57a5-391ec1c59bec
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/Add-Billing-Policy-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/licensing/billing-policy-environment/add-billing-policy-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/licensing/Billing-Policy-Environment/Add-Billing-Policy-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 3002334a-5bec-f1e2-34b2-fe2996bff867
---

# Billing Policy Environment - Add Billing Policy Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Link billing policy ID with environments.

```http
POST https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}/environments/add?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| billingPolicyId | path | True | string | The billing policy ID. |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| environmentIds | string[] |  |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | Success |
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

### BillingPolicyEnvironmentAddRequestModel

Object

| Name | Type | Description |
| --- | --- | --- |
| environmentIds | string[] |  |