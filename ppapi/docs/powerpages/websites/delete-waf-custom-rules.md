---
layout: Reference
title: Websites - Delete Waf Custom Rules - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/delete-waf-custom-rules
uid: api.powerplatform.com.power-platform.powerpages.websites.deletewafcustomrules
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
description: 'Deletes web application firewall custom rules on a Power Pages website. Deletes web application firewall custom rules on the given website. '
locale: en-us
document_id: eea88a4a-b758-7fe6-c1b5-3f6cf8ce47dd
document_version_independent_id: dbcd6d7a-7760-1a9b-3c2d-703f8da6e283
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Delete-Waf-Custom-Rules.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/delete-waf-custom-rules
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Delete-Waf-Custom-Rules.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e8fdebed-2921-4997-a75a-fa863723a535
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/cf1e63a8-325f-42be-b60c-d84a95a42b1f
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
platformId: 073098fd-1fa9-9f33-1ff6-8b5a0a36568b
---

# Websites - Delete Waf Custom Rules

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Deletes web application firewall custom rules on a Power Pages website. Deletes web application firewall custom rules on the given website.

```http
PUT https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/deleteWafCustomRules?api-version=2024-10-01
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
| body | string[] |  |

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
| Details |  |
| Error |  |
| ErrorMessage |  |

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