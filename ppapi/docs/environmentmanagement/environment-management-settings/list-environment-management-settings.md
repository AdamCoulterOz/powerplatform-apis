---
layout: Reference
title: Environment Management Settings - List Environment Management Settings - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/environmentmanagement/environment-management-settings/list-environment-management-settings
uid: api.powerplatform.com.power-platform.environmentmanagement.environmentmanagementsettings.listenvironmentmanagementsettings
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
description: 'Learn more about Power Platform API service - Get environment management setting by ID. '
locale: en-us
document_id: b7c60ec0-d1af-817a-6302-cb40c28446f8
document_version_independent_id: 39be693e-d0a1-a651-d8fc-e3f2e35e1ff0
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/environmentmanagement/Environment-Management-Settings/List-Environment-Management-Settings.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/environmentmanagement/environment-management-settings/list-environment-management-settings
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/environmentmanagement/Environment-Management-Settings/List-Environment-Management-Settings.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 28b16a23-7bff-79ed-6755-736a0da4ef6d
---

# Environment Management Settings - List Environment Management Settings

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Get environment management setting by ID.

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/settings?api-version=2024-10-01
```

 With optional parameters: 

```http
GET https://api.powerplatform.com/environmentmanagement/environments/{environmentId}/settings?$top={$top}&$select={$select}&api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | ID for the environment management setting. |
| api-version | query | True | string | The API version. |
| $select | query |  | string | List of properties to select for this entity. |
| $top | query |  | integer | Number of records to retrieve. Defaults to 500 if not set. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | GetEnvironmentManagementSettingResponse | OK<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| 400 Bad Request | GetEnvironmentManagementSettingResponse | Bad Request<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| 404 Not Found | GetEnvironmentManagementSettingResponse | Not Found<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |
| 429 Too Many Requests | GetEnvironmentManagementSettingResponse | Too Many Requests<br><br>Media Types: "application/json;odata.metadata=minimal;odata.streaming=true", "application/json;odata.metadata=minimal;odata.streaming=false", "application/json;odata.metadata=minimal", "application/json;odata.metadata=full;odata.streaming=true", "application/json;odata.metadata=full;odata.streaming=false", "application/json;odata.metadata=full", "application/json;odata.metadata=none;odata.streaming=true", "application/json;odata.metadata=none;odata.streaming=false", "application/json;odata.metadata=none", "application/json;odata.streaming=true", "application/json;odata.streaming=false", "application/json", "application/xml", "application/prs.odatatestxx-odata", "text/plain", "text/json" |

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
| EnvironmentManagementSetting |  |
| EnvironmentServiceErrorResponse |  |
| ErrorDetail |  |
| GetEnvironmentManagementSettingResponse | Represents the response object for APIs in this service. |

### EnvironmentManagementSetting

Object

| Name | Type | Description |
| --- | --- | --- |
| allowedIpRangeForStorageAccessSignatures | string |  |
| copilotStudio\_CodeInterpreter | boolean |  |
| copilotStudio\_ComputerUseAppAllowlist | string |  |
| copilotStudio\_ComputerUseCredentialsAllowed | boolean |  |
| copilotStudio\_ComputerUseSharedMachines | boolean |  |
| copilotStudio\_ComputerUseWebAllowlist | string |  |
| copilotStudio\_ConnectedAgents | boolean |  |
| copilotStudio\_ConversationAuditLoggingEnabled | boolean |  |
| d365CustomerService\_AIAgents | boolean |  |
| d365CustomerService\_Copilot | boolean |  |
| enableIpBasedStorageAccessSignatureRule | boolean |  |
| id | string |  |
| ipBasedStorageAccessSignatureMode | integer (int32) |  |
| loggingEnabledForIpBasedStorageAccessSignature | boolean |  |
| powerApps\_AllowCodeApps | boolean |  |
| powerApps\_ChartVisualization | boolean |  |
| powerApps\_CopilotChat | boolean |  |
| powerApps\_EnableFormInsights | boolean |  |
| powerApps\_FormPredictAutomatic | boolean |  |
| powerApps\_FormPredictSmartPaste | boolean |  |
| powerApps\_NLSearch | boolean |  |
| powerPages\_AllowIntelligentFormsCopilotForSites | string |  |
| powerPages\_AllowListSummaryCopilotForSites | string |  |
| powerPages\_AllowMakerCopilotsForExistingSites | string |  |
| powerPages\_AllowMakerCopilotsForNewSites | string |  |
| powerPages\_AllowNonProdPublicSites | string |  |
| powerPages\_AllowNonProdPublicSites\_Exemptions | string |  |
| powerPages\_AllowProDevCopilotsForEnvironment | string |  |
| powerPages\_AllowProDevCopilotsForSites | string |  |
| powerPages\_AllowSearchSummaryCopilotForSites | string |  |
| powerPages\_AllowSiteCopilotForSites | string |  |
| powerPages\_AllowSummarizationAPICopilotForSites | string |  |
| tenantId | string (uuid) |  |

### EnvironmentServiceErrorResponse

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| details | ErrorDetail[] |  |
| message | string |  |

### ErrorDetail

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string |  |
| message | string |  |
| target | string |  |
| value | string |  |

### GetEnvironmentManagementSettingResponse

Object

Represents the response object for APIs in this service.

| Name | Type | Description |
| --- | --- | --- |
| errors | EnvironmentServiceErrorResponse |  |
| nextLink | string (uri) | Gets or sets the next link if there are more records to be returned |
| objectResult | EnvironmentManagementSetting[] | Gets or sets the fields for the entities being queried. |
| responseMessage | string | Gets or sets the error message. |