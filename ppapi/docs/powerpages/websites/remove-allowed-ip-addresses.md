---
layout: Reference
title: Websites - Remove Allowed Ip Addresses - REST API (Power Platform API) | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/rest/api/power-platform/powerpages/websites/remove-allowed-ip-addresses
uid: api.powerplatform.com.power-platform.powerpages.websites.removeallowedipaddresses
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
description: "Remove allowed IP addresses from a Power Pages website. Removes the specified IP addresses from the website's IP restriction allow list. "
locale: en-us
document_id: aec2c600-112d-40d5-4ea9-75c6365f5215
document_version_independent_id: bccd0290-2c5f-a66f-7a18-dd0a90a7abfb
original_content_git_url: https://github.com/MicrosoftDocs/powerplatform-rest/blob/live/docs-ref-autogen/power-platform/powerpages/Websites/Remove-Allowed-Ip-Addresses.yml
site_name: Docs
depot_name: MSDN.powerplatform-rest
page_type: rest
page_kind: operation
toc_rel: ../../../toc.json
feedback_product_url: ''
feedback_help_link_type: ''
feedback_help_link_url: ''
asset_id: api/power-platform/powerpages/websites/remove-allowed-ip-addresses
moniker_range_name: 
monikers: []
item_type: Content
source_path: docs-ref-autogen/power-platform/powerpages/Websites/Remove-Allowed-Ip-Addresses.yml
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/e6f942e8-55a7-4c86-b8e3-7456508ea850
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c2975bf6-bf61-46d5-8621-bc6aec151623
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f1834696-48d6-470d-966b-6ee418881596
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/93eba64c-cee2-4c90-a45b-c5546aae2cb8
platformId: b21fafed-e2e2-7a14-2cda-cbd562dbd034
---

# Websites - Remove Allowed Ip Addresses

- Service:
    - Power Platform API

- API Version:
    - 2024-10-01

Remove allowed IP addresses from a Power Pages website. Removes the specified IP addresses from the website's IP restriction allow list.

```http
POST https://api.powerplatform.com/powerpages/environments/{environmentId}/websites/{id}/removeAllowedIpAddresses?api-version=2024-10-01
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
| IpAddresses | IpAddressEntity[] | Represents an IP address entry in the allow list. |

## Responses

| Name | Type | Description |
| --- | --- | --- |
| 204 No Content |  | Success |
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
| Details |  |
| Error |  |
| ErrorMessage |  |
| IpAddressConfiguration |  |
| IpAddressEntity | Represents an IP address entry in the allow list. |
| IpAddressType | The type of the IP address. |

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

### IpAddressConfiguration

Object

| Name | Type | Description |
| --- | --- | --- |
| IpAddresses | IpAddressEntity[] | Represents an IP address entry in the allow list. |

### IpAddressEntity

Object

Represents an IP address entry in the allow list.

| Name | Type | Description |
| --- | --- | --- |
| IpAddress | string | The IP address or CIDR range (e.g., "208.130.0.0/16") |
| IpAddressType | IpAddressType | The type of the IP address. |

### IpAddressType

Enumeration

The type of the IP address.

| Value | Description |
| --- | --- |
| IPv4 |  |
| IPv6 |  |