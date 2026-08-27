---
layout: Reference
title: Environment Backup - Get Environment Backups - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-backup/get-environment-backups
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentbackup.getenvironmentbackups
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
description: 'Gets the list of backups for the specified environment. Gets the backups for the specified environment. '
locale: en-us
document_id: d24ebf1f-eb90-72d6-de06-59cf83328dff
document_version_independent_id: 52f9b7ef-8e82-0942-0e5f-84e66b70dfcd
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Backup/Get-Environment-Backups.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-backup/get-environment-backups
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Backup/Get-Environment-Backups.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/aebdc4a3-c54b-4eea-94e3-663d5e166f57
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/1baec8e6-ab38-4b56-bb59-f6282d94f311
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: eb53706b-45f1-0cd2-9fd6-35d1d2ed2c8d
---

# Environment Backup - Get Environment Backups

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of backups for the specified environment. Gets the backups for the specified environment.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/backups?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentBackupPagedCollection | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| EnvironmentBackup | Represents an environment backup. |
| EnvironmentBackupPagedCollection |  |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| UserIdentity | Represents the identity of a user. |
| ValidationResponse | Represents the response for validation of an operation. |

### EnvironmentBackup

Object

Represents an environment backup.

| Name | Type | Description |
| --- | --- | --- |
| backupExpiryDateTime | string (date-time) | The backup expiry date time. |
| backupPointDateTime | string (date-time) | The backup point date time. |
| createdBy | UserIdentity | Represents the identity of a user. |
| id | string | The identifier of the environment backup. |
| label | string | The label for the manually created backup. |

### EnvironmentBackupPagedCollection

Object

| Name | Type | Description |
| --- | --- | --- |
| collection | EnvironmentBackup[] | Represents an environment backup. |
| continuationToken | string |  |

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

### UserIdentity

Object

Represents the identity of a user.

| Name | Type | Description |
| --- | --- | --- |
| displayName | string | The display name of the user. |
| tenantId | string | The tenant ID of the user. |
| type | string | The type of the user identity (for example, User). |
| userId | string | The ID of the user. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |