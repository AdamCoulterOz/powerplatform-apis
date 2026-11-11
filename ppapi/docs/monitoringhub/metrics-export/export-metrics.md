---
layout: Reference
title: Metrics Export - Export Metrics - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/monitoringhub/metrics-export/export-metrics
uid: api.powerplatform.com.power-platform.monitoringhub.metricsexport.exportmetrics
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
description: 'Export completed daily resource metrics (preview) Returns one OTLP JSON ExportMetricsServiceRequest page for 1 to 10 resources of one resource type and subtype '
locale: en-us
document_id: 416a117d-d868-b235-4122-56f3645da3b6
document_version_independent_id: 4cd6c007-87a5-e68b-3a34-aae61b3b10fe
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/monitoringhub/Metrics-Export/Export-Metrics.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/monitoringhub/metrics-export/export-metrics
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/monitoringhub/Metrics-Export/Export-Metrics.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 25926c86-7a60-f7a2-4bb6-818b8777353d
---

# Metrics Export - Export Metrics

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Export completed daily resource metrics (preview) Returns one OTLP JSON ExportMetricsServiceRequest page for 1 to 10 resources of one resource type and subtype in an environment. Each page contains at most 2,000 data points and 4 MiB of uncompressed JSON. To get the next page, repeat the same method, route, API version, and body with the x-ms-continuation response value in the x-ms-continuation request header. The last page has no continuation header. Only elapsed UTC days are eligible. The effective end date is capped at today's UTC midnight; a range with no eligible days returns an empty resourceMetrics array. Missing source data is omitted, not synthesized. Requires a user token with the PowerApps.Apps.Read delegated permission, a Global, Power Platform, Dynamics 365, AI, or Teams administrator role, and tenant preview admission. Application-only tokens and environment RBAC assignments alone don't grant access.

```http
POST https://api.powerplatform.com/monitoringhub/environments/{environmentId}/resourceType/{resourceType}/resourceSubType/{resourceSubType}/exports/metrics?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string <br>minLength: 1maxLength: 100pattern: ^[A-Za-z0-9](../metrics-export.md)?$ | The ID of the environment containing the resources. Use 1 to 100 ASCII letters, digits, or hyphens, starting and ending with a letter or digit. |
| resourceSubType | path | True | string | The resource subtype for the selected resource type, matched without regard to case. MicrosoftApp requires App and uses the Managed App export action. |
| resourceType | path | True | string | The resource type, matched without regard to case. Supported pairs are PowerApp with CanvasApp, CodeApp, or ModelApp (also accepted as ModelDrivenApp); PowerAutomate with CloudFlow or DesktopFlow; CopilotStudio with Agent; and MicrosoftApp with App. |
| api-version | query | True | string | The API version. |

## Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| x-ms-continuation |  | string <br>maxLength: 16384 | The opaque continuation token from the previous page. Omit it for the first page and keep the original route, API version, and request body unchanged. |
| x-ms-client-request-id |  | string (uuid) | A caller-generated correlation GUID, echoed when valid. |

## Request Body

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| resourceIds | True | string[] (uuid) | The IDs of 1 to 10 resources of the route's resource type and subtype in the environment. Each ID must be a non-empty, non-zero GUID in hyphenated format. Duplicate GUIDs are rejected, including case variants. |
| timeRange | True | MonitoringHubMetricsExportTimeRange | A UTC date range of at most 30 days, with an inclusive start and exclusive end. |
| metricNames |  | string[] | Up to 20 distinct supported metric names for the selected route pair. Omit this property or supply null to export all mapped metrics for that pair. An empty array or unsupported name is rejected. Names are trimmed and matched without regard to case; duplicates are consolidated and output names are canonical. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 200 OK | MonitoringHubMetricsExportPage | One OTLP JSON page, including an empty resourceMetrics array when no eligible data matches.<br><br>Headers<br><br>- x-ms-continuation: string<br>- x-ms-available-through: string<br>- x-ms-record-count: integer<br>- x-ms-request-id: string<br>- x-ms-client-request-id: string |
| 400 Bad Request | MonitoringHubErrorResponse | BadRequest indicates an unsupported route pair or metric, invalid resource ID, invalid date range, or invalid or expired continuation token. InvalidRequestContent indicates an invalid JSON body, missing required property, or unknown property. |
| 401 Unauthorized |  | A valid authenticated user token is required. |
| 403 Forbidden | MonitoringHubErrorResponse | Required authorization is missing, or the routing tenant doesn't match the authenticated tenant. |
| 404 Not Found | MonitoringHubErrorResponse | ApiResourceNotFound indicates that the authenticated tenant isn't admitted to the preview. |
| 429 Too Many Requests |  | The gateway throttled the request. Retry after the indicated delay, if supplied.<br><br>Headers<br><br>Retry-After: string |
| 500 Internal Server Error | MonitoringHubErrorResponse | InternalServerError indicates that the export couldn't produce a valid page. |
| Other Status Codes | MonitoringHubErrorResponse | RequestEntityTooLarge indicates that one metric record exceeds the 4 MiB response limit. |
| Other Status Codes | MonitoringHubErrorResponse | ServiceUnavailable indicates a temporary dependency failure or timeout. |

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
| MonitoringHubError | The error code and message. |
| MonitoringHubErrorResponse | The error response returned when an export fails. |
| MonitoringHubMetricsExportPage | An OTLP JSON ExportMetricsServiceRequest with no proprietary wrapper. |
| MonitoringHubMetricsExportRequest | The export selection. Unknown properties, including scope, lookbackDays, and maxRecords, are rejected. |
| MonitoringHubMetricsExportTimeRange | A UTC date range of at most 30 days, with an inclusive start and exclusive end. |
| MonitoringHubOtlpGauge | The data points of a gauge metric. |
| MonitoringHubOtlpInstrumentationScope | The instrumentation scope producing the metrics. |
| MonitoringHubOtlpKeyValue | An attribute key and string value. |
| MonitoringHubOtlpMetric | A metric and its daily values. Counts use delta monotonic sums. Ratios and timings use gauges. Non-Managed App timings are P75; Managed App timings are daily averages. Only gauge or sum is emitted for a metric. |
| MonitoringHubOtlpNumberDataPoint | A daily metric value, with either asInt or asDouble. |
| MonitoringHubOtlpResource | Resource attributes identifying the service, tenant, environment, resource type, subtype, and resource ID. Resource display names aren't emitted. |
| MonitoringHubOtlpResourceMetrics | The metrics for one Power Platform resource. |
| MonitoringHubOtlpScopeMetrics | The metrics from one instrumentation scope. |
| MonitoringHubOtlpStringValue | An OTLP string attribute value. |
| MonitoringHubOtlpSum | The data points of a delta monotonic sum metric. |

### MonitoringHubError

Object

The error code and message.

| Name | Type | Description |
| --- | --- | --- |
| code | string | A stable error code, such as BadRequest, InvalidRequestContent, or ServiceUnavailable. |
| message | string | A message describing the failure. |

### MonitoringHubErrorResponse

Object

The error response returned when an export fails.

| Name | Type | Description |
| --- | --- | --- |
| error | MonitoringHubError | The error code and message. |

### MonitoringHubMetricsExportPage

Object

An OTLP JSON ExportMetricsServiceRequest with no proprietary wrapper.

| Name | Type | Description |
| --- | --- | --- |
| resourceMetrics | MonitoringHubOtlpResourceMetrics[] | The metrics grouped by Power Platform resource, or an empty array. |

### MonitoringHubMetricsExportRequest

Object

The export selection. Unknown properties, including scope, lookbackDays, and maxRecords, are rejected.

| Name | Type | Description |
| --- | --- | --- |
| metricNames | string[] | Up to 20 distinct supported metric names for the selected route pair. Omit this property or supply null to export all mapped metrics for that pair. An empty array or unsupported name is rejected. Names are trimmed and matched without regard to case; duplicates are consolidated and output names are canonical. |
| resourceIds | string[] (uuid) | The IDs of 1 to 10 resources of the route's resource type and subtype in the environment. Each ID must be a non-empty, non-zero GUID in hyphenated format. Duplicate GUIDs are rejected, including case variants. |
| timeRange | MonitoringHubMetricsExportTimeRange | A UTC date range of at most 30 days, with an inclusive start and exclusive end. |

### MonitoringHubMetricsExportTimeRange

Object

A UTC date range of at most 30 days, with an inclusive start and exclusive end.

| Name | Type | Description |
| --- | --- | --- |
| endDate | string (date) | The UTC day after the last requested day, in YYYY-MM-DD format. It must be later than startDate. The effective end is capped at today's UTC midnight. |
| startDate | string (date) | The first UTC day to export, in YYYY-MM-DD format. |

### MonitoringHubOtlpGauge

Object

The data points of a gauge metric.

| Name | Type | Description |
| --- | --- | --- |
| dataPoints | MonitoringHubOtlpNumberDataPoint[] | The data points. |

### MonitoringHubOtlpInstrumentationScope

Object

The instrumentation scope producing the metrics.

| Name | Type | Description |
| --- | --- | --- |
| name | string | The instrumentation scope name. |
| version | string | The instrumentation scope version. |

### MonitoringHubOtlpKeyValue

Object

An attribute key and string value.

| Name | Type | Description |
| --- | --- | --- |
| key | string | The attribute key. |
| value | MonitoringHubOtlpStringValue | An OTLP string attribute value. |

### MonitoringHubOtlpMetric

Object

A metric and its daily values. Counts use delta monotonic sums. Ratios and timings use gauges. Non-Managed App timings are P75; Managed App timings are daily averages. Only gauge or sum is emitted for a metric.

| Name | Type | Description |
| --- | --- | --- |
| gauge | MonitoringHubOtlpGauge | The data points of a gauge metric. |
| name | string | The canonical metric name. |
| sum | MonitoringHubOtlpSum | The data points of a delta monotonic sum metric. |
| unit | string | The unit, using 1 for ratios, {count} for counts, and s for seconds. |

### MonitoringHubOtlpNumberDataPoint

Object

A daily metric value, with either asInt or asDouble.

| Name | Type | Description |
| --- | --- | --- |
| asDouble | number (double) | The floating-point value, when present. |
| asInt | string | The integer count, encoded as a decimal string, when present. |
| attributes | MonitoringHubOtlpKeyValue[] | The public data-point dimensions, when present. |
| timeUnixNano | string | The value's time in nanoseconds since the Unix epoch, encoded as a decimal string. |

### MonitoringHubOtlpResource

Object

Resource attributes identifying the service, tenant, environment, resource type, subtype, and resource ID. Resource display names aren't emitted.

| Name | Type | Description |
| --- | --- | --- |
| attributes | MonitoringHubOtlpKeyValue[] | The resource attributes. |

### MonitoringHubOtlpResourceMetrics

Object

The metrics for one Power Platform resource.

| Name | Type | Description |
| --- | --- | --- |
| resource | MonitoringHubOtlpResource | Resource attributes identifying the service, tenant, environment, resource type, subtype, and resource ID. Resource display names aren't emitted. |
| scopeMetrics | MonitoringHubOtlpScopeMetrics[] | The metrics grouped by instrumentation scope. |

### MonitoringHubOtlpScopeMetrics

Object

The metrics from one instrumentation scope.

| Name | Type | Description |
| --- | --- | --- |
| metrics | MonitoringHubOtlpMetric[] | The metrics. |
| scope | MonitoringHubOtlpInstrumentationScope | The instrumentation scope producing the metrics. |

### MonitoringHubOtlpStringValue

Object

An OTLP string attribute value.

| Name | Type | Description |
| --- | --- | --- |
| stringValue | string | The attribute value. |

### MonitoringHubOtlpSum

Object

The data points of a delta monotonic sum metric.

| Name | Type | Description |
| --- | --- | --- |
| aggregationTemporality | enum:<br> 1 (int32) | The aggregation temporality. The service emits 1 for delta. |
| dataPoints | MonitoringHubOtlpNumberDataPoint[] | The data points. |
| isMonotonic | boolean | Whether the sum only increases. |