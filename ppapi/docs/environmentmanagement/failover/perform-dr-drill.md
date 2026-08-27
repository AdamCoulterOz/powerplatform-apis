---
layout: Reference
title: Failover - Perform DR Drill - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/failover/perform-dr-drill
uid: api.powerplatform.com.power-platform.environmentmanagement.failover.performdrdrill
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
description: 'Learn more about Power Platform API service - Performs DR Drill for the specified environment. '
locale: en-us
document_id: cf49bb15-f160-0b6a-c3d8-4136cd1d86cc
document_version_independent_id: 369cf9a3-309d-6a0d-a595-1886ac9e1c9a
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Failover/Perform-DR-Drill.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/failover/perform-dr-drill
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Failover/Perform-DR-Drill.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 1c7cf8af-2da3-3d2e-25aa-430c5810dd45
---

# Failover - Perform DR Drill

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Performs DR Drill for the specified environment.

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/disasterRecoveryDrill?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/disasterRecoveryDrill?ValidateOnly={ValidateOnly}&ValidateProperties={ValidateProperties}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The ID of the environment. |
| api-version | query | True | string | The API version. |
| ValidateOnly | query |  | boolean | When true, validates the request without executing it. Use with validateProperties to validate only specific fields. If validateProperties is empty, the entire request is validated. Defaults to false (validate and execute). |
| ValidateProperties | query |  | string | A comma-separated list of property names to validate (for example, "property1,property2"). Applies only when validateOnly is true. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted |
| 400 Bad Request | ValidationResponse | Bad Request |
| 401 Unauthorized |  | Unauthorized |
| 403 Forbidden |  | Forbidden |
| 429 Too Many Requests |  | Too Many Requests |
| Other Status Codes | ValidationResponse | Conflict |

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
| OperationErrorDetail | Structured error detail for a failed request. |
| ValidationResponse | Represents the response for validation of an operation. |

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