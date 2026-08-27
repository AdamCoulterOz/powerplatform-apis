---
layout: Reference
title: Websites - Convert Trial To Production - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/convert-trial-to-production
uid: api.powerplatform.com.power-platform.powerpages.websites.converttrialtoproduction
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
description: 'Learn more about Power Platform API service - Convert a trial Power Pages website to production. Convert a trial website to a production website. '
locale: en-us
document_id: b69b14d5-3d2b-ce1d-c997-7b02ff65a694
document_version_independent_id: 4840ae56-c9ca-bc4f-ff07-b795e7c2add6
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Convert-Trial-To-Production.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/convert-trial-to-production
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Convert-Trial-To-Production.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
- https://authoring-docs-microsoft.poolparty.biz/devrel/befac1c4-b371-401f-bb32-b2c555258404
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
- https://authoring-docs-microsoft.poolparty.biz/devrel/a3a42e80-4ec5-48ab-90ee-478df3614861
platformId: 5c2fcae9-c59d-561a-437b-afa747c30524
---

# Websites - Convert Trial To Production

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Convert a trial Power Pages website to production. Convert a trial website to a production website.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/convertToProduction?api-version=2024-10-01
```

## URI Parameters

| Name | In | Required | Type | Description |
| --- | --- | --- | --- | --- |
| environmentId | path | True | string | The environment ID. |
| id | path | True | string | Website unique identifier (ID). |
| api-version | query | True | string | The API version. |

## Request Body

| Name | Type | Description |
| --- | --- | --- |
| EnableCDN | boolean | Enable Content Delivery Network (CDN) for the website |
| EnableWAF | boolean | Enable Web Application Firewall (WAF) for the website |
| UseDynamics365PortalAddOnLicense | boolean | Use Dynamics 365 Portal Add-On License for the website |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 202 Accepted |  | Accepted<br><br>Headers<br><br>Operation-Location: string |
| 400 Bad Request | ErrorMessage | Bad Request |
| 401 Unauthorized | ErrorMessage | Unauthorized |
| 404 Not Found | ErrorMessage | Not Found |

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
| ConvertTrialToProductionRequest |  |
| Details |  |
| Error |  |
| ErrorMessage |  |

### ConvertTrialToProductionRequest

Object

| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| EnableCDN | boolean | False | Enable Content Delivery Network (CDN) for the website |
| EnableWAF | boolean | False | Enable Web Application Firewall (WAF) for the website |
| UseDynamics365PortalAddOnLicense | boolean | False | Use Dynamics 365 Portal Add-On License for the website |

### Details

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| message | string | Error message |
| target | string | Target parameter |

### Error

Object

| Name | Type | Description |
| --- | --- | --- |
| code | string | Error code |
| details | Details[] |  |
| message | string | Error message |
| target | string | Target parameter |

### ErrorMessage

Object

| Name | Type | Description |
| --- | --- | --- |
| error | Error |  |