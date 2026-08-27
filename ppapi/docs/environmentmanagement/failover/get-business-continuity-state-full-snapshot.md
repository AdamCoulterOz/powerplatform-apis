---
layout: Reference
title: Failover - Get Business Continuity State Full Snapshot - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/failover/get-business-continuity-state-full-snapshot
uid: api.powerplatform.com.power-platform.environmentmanagement.failover.getbusinesscontinuitystatefullsnapshot
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
description: 'Gets the full business continuity state snapshot for the specified environment. Gets business continuity snapshot including LastSyncTime. '
locale: en-us
document_id: 375d5ab6-10a4-0532-b7ac-92a788269e78
document_version_independent_id: f916341a-709b-2f42-c4b9-e8b92ed9f1cc
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Failover/Get-Business-Continuity-State-Full-Snapshot.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/failover/get-business-continuity-state-full-snapshot
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Failover/Get-Business-Continuity-State-Full-Snapshot.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: a463beb6-2730-0915-6f33-4789fd45487f
---

# Failover - Get Business Continuity State Full Snapshot

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the full business continuity state snapshot for the specified environment. Gets business continuity snapshot including LastSyncTime.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/businessContinuityStateFullSnapshot?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | BusinessContinuityStateFullSnapshot | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 400 Bad Request | ValidationResponse | Bad Request<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 401 Unauthorized |  | Unauthorized<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 403 Forbidden |  | Forbidden<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 404 Not Found |  | Not Found<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 429 Too Many Requests |  | Too Many Requests<br><br>Media Types: "text/plain", "application/json", "text/json" |

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
| BusinessContinuityStateFullSnapshot | Business-continuity (disaster-recovery) state snapshot for an environment. |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| ValidationResponse | Represents the response for validation of an operation. |

### BusinessContinuityStateFullSnapshot

Object

Business-continuity (disaster-recovery) state snapshot for an environment.

| Name | Type | Description |
| --- | --- | --- |
| lastSyncTime | string (date-time) | The last time the environment's business-continuity state was synced. |

### FieldError

Object

The error detail for a single field.

| Name | Type | Description |
| --- | --- | --- |
| errorMessages | string[] | The error messages describing what is wrong with the field. |
| suggestedValue | string | A suggested or accepted value that would resolve the error. |

### OperationErrorDetail

Object

Structured error detail for a failed request.

| Name | Type | Description |
| --- | --- | --- |
| code | string | The error code. |
| fieldErrors | &lt;string, FieldError&gt; | Per-field error detail, keyed by field name. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |