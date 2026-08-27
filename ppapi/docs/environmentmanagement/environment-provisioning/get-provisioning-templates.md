---
layout: Reference
title: Environment Provisioning - Get Provisioning Templates - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-provisioning/get-provisioning-templates
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentprovisioning.getprovisioningtemplates
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
description: 'Gets the list of available templates for provisioning in a location. Retrieves available templates for environment provisioning in a location. '
locale: en-us
document_id: 8c2f7e0a-1648-9dc9-ece1-729c59dbc64c
document_version_independent_id: d620d39a-8c90-a21d-f4be-cf3f446e1b66
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Provisioning-Templates.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-provisioning/get-provisioning-templates
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Provisioning-Templates.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 1a85a515-c63e-5701-f2e8-78a0b9039e15
---

# Environment Provisioning - Get Provisioning Templates

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of available templates for provisioning in a location. Retrieves available templates for environment provisioning in a location.

```http
GET https://api.powerplatform.com/environmentmanagement/provisioning/locations/{location}/templates?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| location | path | True | string | The location name. |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentTemplateResourceCollection | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| DisabledReason | Explains why a template is unavailable for a given SKU. |
| EnvironmentSku | The environment SKU. |
| EnvironmentTemplate | Represents a template available for environment provisioning. |
| EnvironmentTemplateResourceCollection | A non-paginated collection of resources returned in full (no continuation token). Used for finite reference lists where partial results would be incorrect. |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| TemplateAvailability | Availability of a template for a specific environment SKU. |
| ValidationResponse | Represents the response for validation of an operation. |

### DisabledReason

Object

Explains why a template is unavailable for a given SKU.

| Name | Type | Description |
| --- | --- | --- |
| code | string | The reason code. |
| message | string | The reason message. |

### EnvironmentSku

Enumeration

The environment SKU.

| Value | Description |
| --- | --- |
| Standard |  |
| Premium |  |
| Developer |  |
| Basic |  |
| Production |  |
| Sandbox |  |
| Trial |  |
| Default |  |
| Support |  |
| SubscriptionBasedTrial |  |
| Teams |  |
| Platform |  |

### EnvironmentTemplate

Object

Represents a template available for environment provisioning.

| Name | Type | Description |
| --- | --- | --- |
| availability | TemplateAvailability[] | The per-SKU availability of this template. |
| displayName | string | The template name, localized for display. |
| isCustomerEngagement | boolean | Whether the template is a Customer Engagement template. |
| isSupportedForResetOperation | boolean | Whether this template is supported for the reset operation. |
| name | string | The template name (identifier). |

### EnvironmentTemplateResourceCollection

Object

A non-paginated collection of resources returned in full (no continuation token). Used for finite reference lists where partial results would be incorrect.

| Name | Type | Description |
| --- | --- | --- |
| collection | EnvironmentTemplate[] | Represents a template available for environment provisioning. |

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

### TemplateAvailability

Object

Availability of a template for a specific environment SKU.

| Name | Type | Description |
| --- | --- | --- |
| disabledReason | DisabledReason | Explains why a template is unavailable for a given SKU. |
| environmentSku | EnvironmentSku | The environment SKU. |
| isDisabled | boolean | Whether the template is disabled for this SKU. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |