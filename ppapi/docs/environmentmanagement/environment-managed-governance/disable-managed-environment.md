---
layout: Reference
title: Environment Managed Governance - Disable Managed Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-managed-governance/disable-managed-environment
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentmanagedgovernance.disablemanagedenvironment
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
description: 'Learn more about Power Platform API service - Disables managed governance for the specified environment. '
locale: en-us
document_id: 1296b9db-cbe3-4936-7fe7-3a5c06f7c1aa
document_version_independent_id: 62bf5eb1-5e58-b53e-5ba9-6adc659b6a41
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Managed-Governance/Disable-Managed-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-managed-governance/disable-managed-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Managed-Governance/Disable-Managed-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 05d9459c-23c7-104e-fcc2-85d13cb7798e
---

# Environment Managed Governance - Disable Managed Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Disables managed governance for the specified environment.

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/governanceSetting/disableManaged?api-version=2024-10-01
```

 With optional parameters: 

```http
POST https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/governanceSetting/disableManaged?ValidateOnly={ValidateOnly}&ValidateProperties={ValidateProperties}&api-version=2024-10-01
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