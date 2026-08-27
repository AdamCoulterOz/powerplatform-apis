---
layout: Reference
title: Environment Provisioning - Get Provisioning Languages - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-provisioning/get-provisioning-languages
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentprovisioning.getprovisioninglanguages
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
description: 'Gets the list of available languages for provisioning in a location. Retrieves available languages for environment provisioning in a location. '
locale: en-us
document_id: b249a5fa-9e21-edd2-0f54-f9d54269b85a
document_version_independent_id: bb480ab5-8654-243d-1e78-38e0c34bd1e8
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Provisioning-Languages.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-provisioning/get-provisioning-languages
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Provisioning-Languages.yml
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c6f99e62-1cf6-4b71-af9b-649b05f80cce
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/3f56b378-07a9-4fa1-afe8-9889fdc77628
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: a51b98a7-2ed0-d4a2-fb66-6656f33133c7
---

# Environment Provisioning - Get Provisioning Languages

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of available languages for provisioning in a location. Retrieves available languages for environment provisioning in a location.

```http
GET https://api.powerplatform.com/environmentmanagement/provisioning/locations/{location}/languages?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| location | path | True | string | The location name. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentLanguageResourceCollection | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| EnvironmentLanguage | Represents a language available for environment provisioning. |
| EnvironmentLanguageResourceCollection | A non-paginated collection of resources returned in full (no continuation token). Used for finite reference lists where partial results would be incorrect. |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| ValidationResponse | Represents the response for validation of an operation. |

### EnvironmentLanguage

Object

Represents a language available for environment provisioning.

| Name | Type | Description |
| --- | --- | --- |
| isTenantDefault | boolean | Whether this is the tenant's default language. |
| localeId | integer (int32) | The locale identifier (LCID, for example, 1033 for English). |
| localizedName | string | The language name, localized for display. |

### EnvironmentLanguageResourceCollection

Object

A non-paginated collection of resources returned in full (no continuation token). Used for finite reference lists where partial results would be incorrect.

| Name | Type | Description |
| --- | --- | --- |
| collection | EnvironmentLanguage[] | Represents a language available for environment provisioning. |

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