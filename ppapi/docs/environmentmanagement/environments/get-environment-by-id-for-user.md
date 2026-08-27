---
layout: Reference
title: Environments - Get Environment By Id For User - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environments/get-environment-by-id-for-user
uid: api.powerplatform.com.power-platform.environmentmanagement.environments.getenvironmentbyidforuser
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
description: 'Learn more about Power Platform API service - Retrieves a single environment by ID (preview). '
locale: en-us
document_id: fe524721-20fa-764f-848c-01e6ecaa5154
document_version_independent_id: e53c0f94-b391-f96c-2f72-89a56bfe0c94
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environments/Get-Environment-By-Id-For-User.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environments/get-environment-by-id-for-user
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environments/Get-Environment-By-Id-For-User.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/68ec7f3a-2bc6-459f-b959-19beb729907d
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/90370425-aca4-4a39-9533-d52e5e002a5d
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 5c302bb5-40a6-72aa-cdf2-85053e664a07
---

# Environments - Get Environment By Id For User

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Retrieves a single environment by ID (preview).

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}?$select={$select}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| api-version | query | True | string | The API version. |
| $select | query |  | string | Comma-separated list of properties to include in the response. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentResponse | Success |

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
| EnterprisePolicies | The set of enterprise policies linked to the environment. |
| EnterprisePolicyLink | A link between the environment and an Azure enterprise policy resource. |
| EnterprisePolicyLinkStatus | The status of the link between an environment and an enterprise policy. |
| EnvironmentPrincipal | Represents a principal (user or application). |
| EnvironmentResponse |  |
| FinOpsMetadata | Metadata describing a linked FinOps environment. |
| RetentionDetails | The retention details of the environment. |

### EnterprisePolicies

Object

The set of enterprise policies linked to the environment.

| Name | Type | Description |
| --- | --- | --- |
| encryption | EnterprisePolicyLink | A link between the environment and an Azure enterprise policy resource. |
| identity | EnterprisePolicyLink | A link between the environment and an Azure enterprise policy resource. |
| networkInjection | EnterprisePolicyLink | A link between the environment and an Azure enterprise policy resource. |
| privateEndpoint | EnterprisePolicyLink | A link between the environment and an Azure enterprise policy resource. |

### EnterprisePolicyLink

Object

A link between the environment and an Azure enterprise policy resource.

| Name | Type | Description |
| --- | --- | --- |
| error | string | Error details when the link status is Failed. |
| id | string | The ID of the enterprise policy. |
| resourceId | string | The fully-qualified Azure resource ID of the enterprise policy. |
| status | EnterprisePolicyLinkStatus | The status of the link between an environment and an enterprise policy. |

### EnterprisePolicyLinkStatus

Enumeration

The status of the link between an environment and an enterprise policy.

| Value | Description |
| --- | --- |
| Linking |  |
| Unlinking |  |
| Linked |  |
| Failed |  |
| LinkingOnline |  |
| UnlinkingOnline |  |

### EnvironmentPrincipal

Object

Represents a principal (user or application).

| Name | Type | Description |
| --- | --- | --- |
| id | string | The principal ID. |
| type | string | The principal type. |

### EnvironmentResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| adminMode | string | Indicates whether admin-only mode is enabled or disabled for the environment. |
| azureRegion | string | The Azure region of the environment. |
| backgroundOperationsState | string | Indicates whether background operations are enabled or disabled for the environment. |
| clusterCategory | string | The cluster category the environment is in. |
| connectedGroupId | string | The ID of the AAD group connected to the environment. |
| createdBy | EnvironmentPrincipal | Represents a principal (user or application). |
| createdDateTime | string (date-time) | The creation date and time of the environment. |
| createdFor | EnvironmentPrincipal | Represents a principal (user or application). |
| dataverseId | string | The ID of the Dataverse database (organization) associated with the environment. |
| deletedDateTime | string (date-time) | The deletion date and time of the environment. |
| displayName | string | The display name of the environment. |
| domainName | string | The domain name of the Dataverse database associated with the environment. |
| enterprisePolicies | EnterprisePolicies | The set of enterprise policies linked to the environment. |
| environmentGroupId | string | The ID of the environment group to which this environment belongs. |
| finOpsMetadata | FinOpsMetadata | Metadata describing a linked FinOps environment. |
| geo | string | The geographical region of the environment. |
| id | string | The ID of the environment. |
| protectionLevel | string | The protection level applied to the environment. |
| retentionDetails | RetentionDetails | The retention details of the environment. |
| scenarioName | string | The scenario name associated with the environment (for example, singleton scenario type). |
| securityGroupId | string | The security group that controls access to the environment. |
| state | string | The current state of the environment. |
| tenantId | string | The ID of the tenant that the environment belongs to. |
| type | string | The type (SKU) of the environment. |
| url | string | The URL of the Dataverse database associated with the environment. |
| version | string | The version of the Dataverse database associated with the environment. |

### FinOpsMetadata

Object

Metadata describing a linked FinOps environment.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The linked FinOps environment ID. |
| type | string | The linked FinOps environment type. |
| url | string | The linked FinOps environment URL. |

### RetentionDetails

Object

The retention details of the environment.

| Name | Type | Description |
| --- | --- | --- |
| availableFromDateTime | string (date-time) | The date and time from which the environment is available for recovery. |
| retentionPeriod | string | The retention period of the environment. |