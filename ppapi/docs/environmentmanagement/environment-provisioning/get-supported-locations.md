---
layout: Reference
title: Environment Provisioning - Get Supported Locations - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-provisioning/get-supported-locations
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentprovisioning.getsupportedlocations
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
description: 'Learn more about Power Platform API service - Gets the list of supported locations for environment provisioning. '
locale: en-us
document_id: f516b5c5-8c91-ea36-8d1f-7128f7739ca5
document_version_independent_id: 73c2e555-2596-15bb-6597-7de8cb33daab
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Supported-Locations.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-provisioning/get-supported-locations
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Get-Supported-Locations.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: aa464a9f-4ccc-b293-680e-e6dbe6c194f4
---

# Environment Provisioning - Get Supported Locations

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Gets the list of supported locations for environment provisioning.

```http
GET https://api.powerplatform.com/environmentmanagement/provisioning/locations?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | ProvisioningLocations | OK<br><br>Media Types: "text/plain", "application/json", "text/json" |
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
| FieldError | The error detail for a single field. |
| Location | Represents a location/geo for environment provisioning. |
| LocationSelectionMode | Describes how a tenant selects a provisioning location. Returned alongside the supported locations to tell callers whether to pick a specific location or a macro region. |
| MacroRegion | Represents a macro region that groups one or more provisioning locations. |
| OperationErrorDetail | Structured error detail for a failed request. |
| ProvisioningLocations | Response envelope for the list-provisioning-locations endpoint. Surfaces the list of locations at the top level alongside tenant-scoped provisioning metadata. |
| ValidationResponse | Represents the response for validation of an operation. |

### FieldError

Object

The error detail for a single field.

| Name | Type | Description |
| --- | --- | --- |
| errorMessages | string[] | The error messages describing what is wrong with the field. |
| suggestedValue | string | A suggested or accepted value that would resolve the error. |

### Location

Object

Represents a location/geo for environment provisioning.

| Name | Type | Description |
| --- | --- | --- |
| canProvisionDatabase | boolean | Whether database provisioning is allowed. |
| code | string | The location code. |
| displayName | string | The display name. |
| hasFirstReleaseIslandAvailableForProvisioning | boolean | Whether a first-release island is available for provisioning in this location. |
| isDefault | boolean | Whether this is the default location. |
| isDisabled | boolean | Whether this location is disabled. |
| name | string | The location name. |

### LocationSelectionMode

Enumeration

Describes how a tenant selects a provisioning location. Returned alongside the supported locations to tell callers whether to pick a specific location or a macro region.

| Value | Description |
| --- | --- |
| Region |  |
| MacroRegion |  |

### MacroRegion

Object

Represents a macro region that groups one or more provisioning locations.

| Name | Type | Description |
| --- | --- | --- |
| dataResidencyNote | string | The data residency note shown to customers for this macro region. |
| displayName | string | The display name of the macro region. |
| macroRegionId | string | The macro region identifier. |

### OperationErrorDetail

Object

Structured error detail for a failed request.

| Name | Type | Description |
| --- | --- | --- |
| code | string | The error code. |
| fieldErrors | &lt;string, FieldError&gt; | Per-field error detail, keyed by field name. |

### ProvisioningLocations

Object

Response envelope for the list-provisioning-locations endpoint. Surfaces the list of locations at the top level alongside tenant-scoped provisioning metadata.

| Name | Type | Description |
| --- | --- | --- |
| collection | Location[] | The list of provisioning locations available to the tenant. |
| locationSelectionMode | LocationSelectionMode | Describes how a tenant selects a provisioning location. Returned alongside the supported locations to tell callers whether to pick a specific location or a macro region. |
| macroRegions | MacroRegion[] | The list of macro regions available to the tenant. |

### ValidationResponse

Object

Represents the response for validation of an operation.

| Name | Type | Description |
| --- | --- | --- |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |