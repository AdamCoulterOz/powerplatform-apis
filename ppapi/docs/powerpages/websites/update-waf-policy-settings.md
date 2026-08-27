---
layout: Reference
title: Websites - Update Waf Policy Settings - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/update-waf-policy-settings
uid: api.powerplatform.com.power-platform.powerpages.websites.updatewafpolicysettings
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
description: Update web application firewall policy settings on a Power Pages website. Updates policy-level web application firewall settings (enforcement mode and JavaScrip
locale: en-us
document_id: f2d651cb-58ca-1e2f-8dd6-96dd88f322f4
document_version_independent_id: bfe9caf8-c3d1-cd3a-88aa-a6aba7c0b5c5
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Update-Waf-Policy-Settings.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/update-waf-policy-settings
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Update-Waf-Policy-Settings.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e8fdebed-2921-4997-a75a-fa863723a535
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/cf1e63a8-325f-42be-b60c-d84a95a42b1f
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
platformId: 3a0918e2-e143-0a9c-a9f7-b78f771f9550
---

# Websites - Update Waf Policy Settings

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Update web application firewall policy settings on a Power Pages website. Updates policy-level web application firewall settings (enforcement mode and JavaScript/CAPTCHA challenge cookie lifetimes) on the given website. Only the fields provided in the request body are applied; omitted fields are left unchanged.

```http
PUT https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/updateWafPolicySettings?api-version=2024-10-01
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
| captchaExpirationInMinutes | integer (int32) | CAPTCHA challenge cookie validity lifetime in minutes. The accepted range is validated by Azure Front Door. |
| javascriptChallengeExpirationInMinutes | integer (int32) | JavaScript challenge cookie validity lifetime in minutes. The accepted range is validated by Azure Front Door. |
| mode | enum:<br>- Prevention<br>- Detection | Web application firewall enforcement mode. Prevention blocks matching requests; Detection only logs them. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | WebApplicationFirewallPolicySettings | OK |
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
| Details |  |
| Error |  |
| ErrorMessage |  |
| WebApplicationFirewallPolicySettings | Policy-level web application firewall settings. All properties are optional; only the properties provided are applied, and any omitted property is left unchanged. |

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

### WebApplicationFirewallPolicySettings

Object

Policy-level web application firewall settings. All properties are optional; only the properties provided are applied, and any omitted property is left unchanged.

| Name | Type | Description |
| --- | --- | --- |
| captchaExpirationInMinutes | integer (int32) | CAPTCHA challenge cookie validity lifetime in minutes. The accepted range is validated by Azure Front Door. |
| javascriptChallengeExpirationInMinutes | integer (int32) | JavaScript challenge cookie validity lifetime in minutes. The accepted range is validated by Azure Front Door. |
| mode | enum:<br>- Detection<br>- Prevention | Web application firewall enforcement mode. Prevention blocks matching requests; Detection only logs them. |