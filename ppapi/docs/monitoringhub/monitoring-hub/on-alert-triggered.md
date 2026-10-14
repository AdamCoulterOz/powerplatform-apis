---
layout: Reference
title: Monitoring Hub - On Alert Triggered - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/monitoringhub/monitoring-hub/on-alert-triggered
uid: api.powerplatform.com.power-platform.monitoringhub.monitoringhub.onalerttriggered
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
description: When an alert triggers (preview) Triggers when a daily Power Platform Monitor alert rule fires in your tenant and its notification type is set to "Connector" or
locale: en-us
document_id: 348682f5-52b0-07a5-0dfa-bc8033482804
document_version_independent_id: 2c00e432-52aa-bbd1-79a7-a15609254eea
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/monitoringhub/Monitoring-Hub/On-Alert-Triggered.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/monitoringhub/monitoring-hub/on-alert-triggered
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/monitoringhub/Monitoring-Hub/On-Alert-Triggered.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://authoring-docs-microsoft.poolparty.biz/devrel/07bb3e10-d135-43ff-bc8b-360497cb39fa
- https://authoring-docs-microsoft.poolparty.biz/devrel/1ae5c491-970a-4062-8301-6336e69f9026
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://authoring-docs-microsoft.poolparty.biz/devrel/12e559b9-eaf6-4aee-9af7-62334e15f863
- https://authoring-docs-microsoft.poolparty.biz/devrel/f2c3e52e-3667-4e8a-bf11-20b9eaccdc8c
platformId: 3e7761a3-0b80-be44-b653-0df7260363e5
---

# Monitoring Hub - On Alert Triggered

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

When an alert triggers (preview) Triggers when a daily Power Platform Monitor alert rule fires in your tenant and its notification type is set to "Connector" or "Email and connector". This preview supports daily alert rules and returns alert IDs, metadata, affected resources, and a link to the Power Platform admin center. Each alert is returned as one item in the value array. To start a separate flow run for each alert, enable Split On for value.

```http
GET https://api.powerplatform.com/monitoringhub/powerplatform/triggeredAlerts/poll
```

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | MonitoringHubTriggeredAlertsPollResponse | Successful request. The response contains one or more alert events.<br><br>Headers<br><br>- Location: string<br>- Retry-After: string |
| 202 Accepted |  | Accepted. No alert events are returned; there is no body and no flow run.<br><br>Headers<br><br>- Location: string<br>- Retry-After: string |
| 400 Bad Request |  | Bad request. One or more request parameters are invalid. |
| 401 Unauthorized |  | Unauthorized. A valid access token is required. |
| 403 Forbidden |  | Forbidden. You don't have permission to read alerts in this tenant. |
| 429 Too Many Requests |  | Too many requests. Retry after the indicated delay.<br><br>Headers<br><br>Retry-After: string |
| 500 Internal Server Error |  | Internal server error. |

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
| MonitoringHubAffectedResource | The IDs of an affected resource and its environment, with the observed metric value when available. |
| MonitoringHubTriggeredAlert | A Power Platform Monitor alert with its rule, metric, and affected-resource details. Unknown indicates an unrecognized value. Optional details are omitted when unavailable. |
| MonitoringHubTriggeredAlertsPollResponse | A batch of Power Platform Monitor alerts. Use the value array as the Split On target to start a separate flow run for each alert. |

### MonitoringHubAffectedResource

Object

The IDs of an affected resource and its environment, with the observed metric value when available.

| Name | Type | Description |
| --- | --- | --- |
| environmentId | string | The environment ID: a GUID, or Default-{tenant GUID} for the default environment. |
| metricValue | number (double) | The observed value for this resource, expressed in the alert's Metric Unit. Omitted when unavailable. |
| resourceId | string (uuid) | The ID of the affected resource. |

### MonitoringHubTriggeredAlert

Object

A Power Platform Monitor alert with its rule, metric, and affected-resource details. Unknown indicates an unrecognized value. Optional details are omitted when unavailable.

| Name | Type | Description |
| --- | --- | --- |
| affectedResourceCount | integer (int32)<br>minimum: 0 | The total number of affected resources, including any resources omitted from the Affected Resources list. |
| affectedResources | MonitoringHubAffectedResource[] | A list of affected resource and environment IDs, with observed metric values when available. The list can be limited. Check Affected Resource Count and Affected Resources Truncated to determine whether more resources were affected. |
| affectedResourcesTruncated | boolean | True when the Affected Resources list omits one or more resources included in Affected Resource Count. |
| alertId | string (uuid) | The ID of the alert instance. |
| alertLink | string (uri) | A link to view the alert in Power Platform admin center. Sign in with an account that has access to the alert. |
| alertRuleId | string (uuid) | The ID of the alert rule in the Power Platform admin center. |
| dataReviewPeriod | string | The time period evaluated by the rule, as an ISO-8601 duration, such as PT1H for one hour or P1D for one day. |
| firedDateTime | string (date-time) | The time the alert fired, in UTC ISO-8601 format. |
| metric | enum:<br>- AgentSuccessRate<br>- CanvasAppAvailability<br>- CanvasAppDataRequest<br>- CanvasAppDataRequestLatency<br>- CanvasAppRecentAppLaunches<br>- CanvasAppTimeToFullLoad<br>- CanvasAppTimeToInteract<br>- CloudFlowDuration<br>- CloudFlowRunCount<br>- CloudFlowSuccessRate<br>- CodeAppAvailability<br>- CodeAppDataRequest<br>- CodeAppDataRequestLatency<br>- CodeAppRecentAppLaunches<br>- CodeAppTimeToInteract<br>- DesktopFlowDuration<br>- DesktopFlowRunCount<br>- DesktopFlowSuccessRate<br>- DesktopFlowTimeInQueue<br>- ModelAppAvailability<br>- ModelDrivenAppRecentAppLaunches<br>- PowerPagesAvailability<br>- PowerPagesErrorRate<br>- PowerPagesPageLoadTime<br>- PowerPagesSessionTime<br>- PowerPagesSessions<br>- Unknown<br>- WorkQueueBusinessException<br>- WorkQueueGenericException<br>- WorkQueueItException<br>- WorkQueueOutOfSla | The metric monitored by the alert rule, or Unknown when the metric isn't recognized. |
| metricUnit | enum:<br>- Count<br>- Percent<br>- Seconds<br>- Unknown | The unit for the threshold and observed metric values. Percent uses percentage points (95 means 95 percent), Seconds uses seconds, and Count uses item or event counts. Unknown indicates an unrecognized unit. |
| monitorCondition | enum:<br>- Fired<br>- Resolved<br>- Unknown | Whether the alert has fired or resolved. Daily alert rules currently report Fired only. Unknown indicates an unrecognized condition. |
| operator | enum:<br>- Equals<br>- IsOver<br>- IsOverOrEqual<br>- IsUnder<br>- IsUnderOrEqual<br>- Unknown | How the metric is compared with the threshold. IsUnder and IsOver exclude equality; IsUnderOrEqual and IsOverOrEqual include equality. Unknown indicates an unrecognized comparison. |
| productType | enum:<br>- CopilotStudio<br>- PowerApps<br>- PowerAutomate<br>- PowerPages<br>- Unknown | The Power Platform product associated with the alert, or Unknown when unrecognized. |
| resolvedDateTime | string (date-time) | The time the alert resolved, in UTC ISO-8601 format. Omitted when no resolution time is available. |
| scope | enum:<br>- Environment<br>- Resource<br>- Tenant<br>- Unknown | Whether the rule monitors a tenant, environment, or resource, or Unknown when unrecognized. |
| severity | enum:<br>- High<br>- Low<br>- Medium<br>- Unknown | The alert severity, or Unknown when the severity isn't recognized. |
| subProductType | enum:<br>- Agent<br>- CanvasApp<br>- CloudFlow<br>- CodeApp<br>- DesktopFlow<br>- ModelDrivenApp<br>- PowerPages<br>- Unknown<br>- WorkQueue | The type of app, flow, or other resource associated with the alert, or Unknown when unrecognized. |
| tenantId | string (uuid) | The ID of your Power Platform tenant. |
| threshold | number (double) | The threshold configured for the rule, expressed in Metric Unit. For example, 95 with Percent means 95 percent. |

### MonitoringHubTriggeredAlertsPollResponse

Object

A batch of Power Platform Monitor alerts. Use the value array as the Split On target to start a separate flow run for each alert.

| Name | Type | Description |
| --- | --- | --- |
| totalCount | integer (int32)<br>minimum: 0 | The number of alerts in this response. |
| value | MonitoringHubTriggeredAlert[] | The alerts returned by this poll. |