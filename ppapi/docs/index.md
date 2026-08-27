---
layout: Conceptual
title: Microsoft Power Platform API reference - Power Platform API | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/
uhfHeaderId: MSDocsHeader-PowerPlatform
enable_rest_try_it: false
rest_product: powerplatform-rest
breadcrumb_path: ~/breadcrumb/toc.yml
author: laneswenka
ms.author: laswenka
ms.topic: reference
ms.devlang: http
ms.date: 2026-07-10T00:00:00.0000000Z
ms.service: power-platform
ms.subservice: developer
feedback_system: None
description: Unified REST API for all administrative capabilities in Microsoft Power Platform.
ms.reviewer: phecke
locale: en-us
document_id: a2ea6fc6-9284-85b0-1fd8-b87bec2af957
document_version_independent_id: 826319d8-49ae-b1a6-0ba2-42ea935fd34a
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/index.md
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: conceptual
toc_rel: ../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
word_count: 546
asset_id: api/power-platform/index
moniker_range_name: 
monikers: []
item_type: Content
source_path: index.md
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
platformId: 77b33148-01c3-b9b5-fdf1-e53103ff1300
---

# Microsoft Power Platform API reference - Power Platform API | Microsoft Learn

The Power Platform API enables you to access Power Platform services and resources. You access these services and resources using a RESTful web API that is described in this reference.

To use the Power Platform API:

1. [Register](https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2) your app.
2. Get authentication tokens for [a user](https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2) or [service](https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2).

Note

A .NET implementation of the Power Platform API is now available.

More info: [Power Platform management API reference](https://learn.microsoft.com/en-us/dotnet/api/), [Microsoft.PowerPlatform.Management](https://www.nuget.org/packages/Microsoft.PowerPlatform.Management) NuGet package

## Call a REST API method

To read from or write to a resource such as a user or an email message, you construct a request that looks like the following:

```http
{HTTP method} https://api.powerplatform.com/{namespace}/{resource}?api-version={version}
```

The components of a request include:

- {HTTP method} - The HTTP method used on the request to Power Platform API.
- {namespace} - The logical grouping of capabilities you're referencing.
- {resource} - The resource in Power Platform API that you're referencing.
- {version} - The version of the Power Platform API you're using.

## HTTP methods

Power Platform API uses the HTTP method on your request to determine what your request is doing. The API supports the following methods.

| **Method** | **Description** |
| --- | --- |
| GET | Read data from a resource. |
| POST | Create a new resource, or perform an action. |
| PATCH | Update a resource with new values. |
| PUT | Replace a resource with a new one. |
| DELETE | Remove a resource. |

- For the CRUD methods `GET` and `DELETE`, no request body is required.
- The `POST`, `PATCH`, and `PUT` methods require a request body, usually specified in JSON format, that contains additional information, such as the values for properties of the resource.

## Namespace

The Power Platform API defines most of its resources, methods, and enumerations in namespaces. Each namespace is a logical grouping of capabilities such as **Licensing** for Billing Policy administration, and **AppManagement** for managing installation for Microsoft-provided application packages in Dataverse. More namespaces will be added over time, until full parity is reached in Power Platform API for what an administrator can perform in Power Platform admin center. From that point onward, new features will always be made available API-first.

## Resource

A resource can either be tenant level or environment level:

When a resource is at the tenant level, the tenantID is inferred using the OAuth bearer token and the call is routed to the Azure region that matches your tenant's physical address. An example tenant level resource call would be:

```http
GET https://api.powerplatform.com/licensing/billingPolicies/{billingPolicyId}?api-version=2022-03-01-preview
```

When a resource is at the environment level, the tenantID is still inferred as mentioned above but an environmentID must also be specified in the path before you can interact with the resource. An example environment level resource call would be:

```http
GET https://api.powerplatform.com/appmanagement/environments/{environmentId}/operations/{operationId}?api-version=2022-03-01-preview
```

For details about permissions, go to [Permissions reference](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference).

## Version

For information about available API versions, see [Versioning and support](https://learn.microsoft.com/en-us/power-platform/admin/programmability-versioning-support).

For information on what's changed in the monthly releases, see [Programmability and extensibility - what's new or changed](whats-new-changed.md).

## Tutorials for using Power Platform API

You might be wondering how do I make use of these REST endpoints in an end to end, real world scenario? We're so glad you asked! Use the following tutorials:

- [Tutorial: Create a daily capacity report](https://learn.microsoft.com/en-us/power-platform/admin/programmability-tutorial-create-daily-capacity-report)
- [Tutorial: Install an application to a target environment](https://learn.microsoft.com/en-us/power-platform/admin/programmability-tutorial-install-application-environment)
- [Tutorial: Create, update, and list Environment Management Settings](https://learn.microsoft.com/en-us/power-platform/admin/programmability-tutorial-environmentmanagement-settings)