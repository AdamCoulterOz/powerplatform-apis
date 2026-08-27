---
layout: Reference
title: Rule Sets - Delete Rule Set - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/governance/rule-sets/delete-rule-set
uid: api.powerplatform.com.power-platform.governance.rulesets.deleteruleset
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
description: 'Learn more about Power Platform API service - Delete Rule Set. Deletes the Rule Set. Only tenant admins can delete. '
locale: en-us
document_id: a9362cad-c731-516e-0142-269ee5e0063c
document_version_independent_id: b4c8556c-15f0-eca9-808d-6889f1d4999b
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/governance/Rule-Sets/Delete-Rule-Set.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/governance/rule-sets/delete-rule-set
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/governance/Rule-Sets/Delete-Rule-Set.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 8519b35e-210b-ff86-67b7-b734aec04588
---

# Rule Sets - Delete Rule Set

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Delete Rule Set. Deletes the Rule Set. Only tenant admins can delete.

```http
DELETE https://api.powerplatform.com/governance/ruleSets/{ruleSetId}?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| ruleSetId | path | True | string (uuid) | The unique identifier of the Rule Set. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK |  | Successfully deleted Rule Set. |
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
| MgGovErrorResponse | Standard error response. |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code. |
| message | string | Error message. |

### MgGovErrorResponse

Object

Standard error response.

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |