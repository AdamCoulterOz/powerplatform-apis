---
layout: Reference
title: Environments - List Environments For User - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environments/list-environments-for-user
uid: api.powerplatform.com.power-platform.environmentmanagement.environments.listenvironmentsforuser
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
description: 'Retrieve a list of environments (preview). Returns a list of environments available for the authenticated user. '
locale: en-us
document_id: e120efc4-8f65-f0d8-b225-61b67b1789d2
document_version_independent_id: 33cd25be-6c11-f4a7-dcf7-463e7c71a39a
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environments/List-Environments-For-User.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environments/list-environments-for-user
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environments/List-Environments-For-User.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/68ec7f3a-2bc6-459f-b959-19beb729907d
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/8b896464-3b7d-4e1f-84b0-9bb45aeb5f64
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/90370425-aca4-4a39-9533-d52e5e002a5d
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/b1d2d671-9549-46e8-918c-24349120dbf5
platformId: 54a7fad1-c47d-6fb6-343b-fc4d263681b9
---

# Environments - List Environments For User

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Retrieve a list of environments (preview). Returns a list of environments available for the authenticated user.

```http
GET https://api.powerplatform.com/environmentmanagement/environments?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/environmentmanagement/environments?ids={ids}&$filter={$filter}&$select={$select}&$top={$top}&$skip={$skip}&$orderby={$orderby}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |
| $filter | query |  | string | OData filter expression to restrict the set of environments returned. Supported filter properties include `dataverseId`, `type`, `geo`, `state`, `environmentGroupId`, and `domainName`. |
| $orderby | query |  | string | OData order-by expression for sorting the results. |
| $select | query |  | string | Comma-separated list of properties to include in the response. |
| $skip | query |  | integer <br>minimum: 0 | Number of environments to skip before returning results. |
| $top | query |  | integer <br>minimum: 0 | Maximum number of environments to return. |
| ids | query |  | string[] | Comma-separated list of environment IDs to retrieve. When specified, only environments matching these IDs are returned. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | EnvironmentList | A list of environments. |

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
| EnvironmentList |  |
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

### EnvironmentList

Object

| Name | Type | Description |
| --- | --- | --- |
| @odata.nextlink | string (uri) | Opaque URL to retrieve the next page of results. Present only when additional pages are available. |
| value | EnvironmentResponse[] |  |

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