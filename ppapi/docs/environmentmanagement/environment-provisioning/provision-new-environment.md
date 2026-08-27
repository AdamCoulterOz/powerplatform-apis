---
layout: Reference
title: Environment Provisioning - Provision New Environment - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-provisioning/provision-new-environment
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentprovisioning.provisionnewenvironment
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
description: 'Learn more about Power Platform API service - Provisions a new environment. '
locale: en-us
document_id: 5d91c500-31eb-9ae6-101b-fc9cec804946
document_version_independent_id: 7059ff5c-3a3f-f7ce-1ba0-7a7d9ab050e4
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Provision-New-Environment.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-provisioning/provision-new-environment
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Provisioning/Provision-New-Environment.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/0ceb3227-2ff7-4d97-8e75-3d7b9ccc937a
- https://authoring-docs-microsoft.poolparty.biz/devrel/63959238-cb90-4871-a33d-4a5519097e47
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/4d680e1a-c470-4772-a236-5c714bd09be0
- https://authoring-docs-microsoft.poolparty.biz/devrel/78d87f42-5582-4a6b-90be-7db2f12b34e6
platformId: 6017abb7-4705-f436-6b2e-7b6d844cd923
---

# Environment Provisioning - Provision New Environment

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Provisions a new environment.

```http
POST https://api.powerplatform.com/environmentmanagement/provisioning/environments?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| api-version | query | True | string | The API version. |

## Request Body

Media Types: "application/json", "text/json", "application/\*+json"

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| displayName | True | string <br>minLength: 1 | The display name of the environment. |
| environmentSku | True | EnvironmentSku | The environment SKU. |
| billingPolicy |  | CreateEnvironmentRequestBillingPolicy | Billing policy for the environment. |
| cluster |  | CreateEnvironmentRequestCluster | Cluster configuration. |
| connectedGroupIdForTeamsEnvironment |  | string | Microsoft 365 Group ID to be linked to the Teams environment during provisioning. This property is not applicable for non-Teams environments. |
| databaseType |  | string | The type of database to create (for example, CommonDataService). |
| description |  | string | An optional description for the environment. |
| finOpsMetadata |  | CreateEnvironmentRequestFinOpsMetadata | FinOps metadata for environment provisioning. |
| governanceConfiguration |  | CreateEnvironmentRequestGovernance | Governance configuration. |
| linkedEnvironmentMetadata |  | CreateEnvironmentRequestLinkedMetadata | Metadata for the linked Dataverse environment. |
| location |  | string | The location where the environment will be provisioned. Mutually exclusive with MacroRegion. |
| macroRegion |  | string | The macro region where the environment will be provisioned. |
| parentEnvironmentGroup |  | CreateEnvironmentRequestParentGroup | Parent environment group. |
| usedBy |  | UserIdentity | Represents the identity of a user. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 201 Created | OperationExecutionResult | Created<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 202 Accepted |  | Accepted<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 400 Bad Request | ValidationResponse | Bad Request<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 401 Unauthorized |  | Unauthorized<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 403 Forbidden |  | Forbidden<br><br>Media Types: "text/plain", "application/json", "text/json" |
| 429 Too Many Requests |  | Too Many Requests<br><br>Media Types: "text/plain", "application/json", "text/json" |
| Other Status Codes | ValidationResponse | Conflict<br><br>Media Types: "text/plain", "application/json", "text/json" |

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
| CreateEnvironmentRequest | Request model for provisioning a new environment. |
| CreateEnvironmentRequestBillingPolicy | Billing policy for the environment. |
| CreateEnvironmentRequestCluster | Cluster configuration. |
| CreateEnvironmentRequestFinOpsMetadata | FinOps metadata for environment provisioning. |
| CreateEnvironmentRequestGovernance | Governance configuration. |
| CreateEnvironmentRequestLinkedMetadata | Metadata for the linked Dataverse environment. |
| CreateEnvironmentRequestParentGroup | Parent environment group. |
| Environment | Power Platform environment. |
| EnvironmentRequestCurrency | Currency settings for an environment. |
| EnvironmentSku | The environment SKU. |
| FieldError | The error detail for a single field. |
| OperationErrorDetail | Structured error detail for a failed request. |
| OperationExecutionResult | The result of an environment lifecycle operation. |
| OperationStatus | The status of operation. |
| ProtectionLevel | The environment governance protection level. |
| StageStatus | The status of a single stage of an operation. |
| StepExecutionStatus | The execution status of an operation stage. |
| UserIdentity | Represents the identity of a user. |
| ValidationResponse | Represents the response for validation of an operation. |

### CreateEnvironmentRequest

Object

Request model for provisioning a new environment.

| Name | Type | Description |
| --- | --- | --- |
| billingPolicy | CreateEnvironmentRequestBillingPolicy | Billing policy for the environment. |
| cluster | CreateEnvironmentRequestCluster | Cluster configuration. |
| connectedGroupIdForTeamsEnvironment | string | Microsoft 365 Group ID to be linked to the Teams environment during provisioning. This property is not applicable for non-Teams environments. |
| databaseType | string | The type of database to create (for example, CommonDataService). |
| description | string | An optional description for the environment. |
| displayName | string <br>minLength: 1 | The display name of the environment. |
| environmentSku | EnvironmentSku | The environment SKU. |
| finOpsMetadata | CreateEnvironmentRequestFinOpsMetadata | FinOps metadata for environment provisioning. |
| governanceConfiguration | CreateEnvironmentRequestGovernance | Governance configuration. |
| linkedEnvironmentMetadata | CreateEnvironmentRequestLinkedMetadata | Metadata for the linked Dataverse environment. |
| location | string | The location where the environment will be provisioned. Mutually exclusive with MacroRegion. |
| macroRegion | string | The macro region where the environment will be provisioned. |
| parentEnvironmentGroup | CreateEnvironmentRequestParentGroup | Parent environment group. |
| usedBy | UserIdentity | Represents the identity of a user. |

### CreateEnvironmentRequestBillingPolicy

Object

Billing policy for the environment.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The billing policy ID. |

### CreateEnvironmentRequestCluster

Object

Cluster configuration.

| Name | Type | Description |
| --- | --- | --- |
| category | string | The cluster category. Eg: FirstRelease. |

### CreateEnvironmentRequestFinOpsMetadata

Object

FinOps metadata for environment provisioning.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The FinOps environment ID. |
| type | string | The FinOps environment link type. |
| url | string | The FinOps environment URL. |

### CreateEnvironmentRequestGovernance

Object

Governance configuration.

| Name | Type | Description |
| --- | --- | --- |
| protectionLevel | ProtectionLevel | The environment governance protection level. |

### CreateEnvironmentRequestLinkedMetadata

Object

Metadata for the linked Dataverse environment.

| Name | Type | Description |
| --- | --- | --- |
| baseLanguageCode | integer (int32) | The base language code (for example, 1033 for English). |
| currency | EnvironmentRequestCurrency | Currency settings for an environment. |
| domainName | string | The domain name. |
| securityGroupId | string | The security group ID. |
| templateMetadata | object | A JSON object payload customized for the selected templates. |
| templates | string[] | The templates to apply. |

### CreateEnvironmentRequestParentGroup

Object

Parent environment group.

| Name | Type | Description |
| --- | --- | --- |
| id | string | The environment group ID. |

### Environment

Object

Power Platform environment.

| Name | Type | Description |
| --- | --- | --- |
| dataverseOrganizationUrl | string | Dataverse organization URL of the environment. |
| displayName | string | Display name of the environment. |
| environmentId | string | The environment ID. |

### EnvironmentRequestCurrency

Object

Currency settings for an environment.

| Name | Type | Description |
| --- | --- | --- |
| code | string | The currency code (for example, USD). |
| name | string | The currency name. |
| precision | integer (int32) | The currency precision. |
| symbol | string | The currency symbol. |

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

### OperationExecutionResult

Object

The result of an environment lifecycle operation.

| Name | Type | Description |
| --- | --- | --- |
| endTime | string (date-time) | The end time of the operation. |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |
| name | string | The name of the operation. |
| operationId | string | The ID of the operation. |
| requestedBy | UserIdentity | Represents the identity of a user. |
| stageStatuses | StageStatus[] | Per-stage progress of the operation. |
| startTime | string (date-time) | The start time of the operation. |
| status | OperationStatus | The status of operation. |
| updatedEnvironment | Environment | Power Platform environment. |

### OperationStatus

Enumeration

The status of operation.

| Value | Description |
| --- | --- |
| Queued |  |
| InProgress |  |
| Succeeded |  |
| ValidationFailed |  |
| Failed |  |
| NoOperation |  |
| ValidationPassed |  |

### ProtectionLevel

Enumeration

The environment governance protection level.

| Value | Description |
| --- | --- |
| Basic |  |
| Standard |  |

### StageStatus

Object

The status of a single stage of an operation.

| Name | Type | Description |
| --- | --- | --- |
| endTime | string (date-time) | The end time of the stage. |
| errorDetail | OperationErrorDetail | Structured error detail for a failed request. |
| name | string | The name of the stage. |
| startTime | string (date-time) | The start time of the stage. |
| status | StepExecutionStatus | The execution status of an operation stage. |

### StepExecutionStatus

Enumeration

The execution status of an operation stage.

| Value | Description |
| --- | --- |
| Succeeded |  |
| Failed |  |
| Skipped |  |
| Postponed |  |
| InProgress |  |
| NotStarted |  |

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