#!/usr/bin/env python3
"""Emit analytics/oas/openapi.json deterministically.

The spec is hand-owned; this script exists only so the JSON is byte-stable
(`indent=1`, key order as written) across edits, and so the region tables that
appear in three places (server variable enum, geoName enum, x-region-hosts) are
generated from one source of truth. Edit the structures below, re-run, commit.
"""

from __future__ import annotations

import json
import os

ANALYTICS_SCOPE = "https://adminanalytics.powerplatform.microsoft.com/.default"
PPAPI_SCOPE = "https://api.powerplatform.com/.default"

COMMERCIAL_SUFFIX = "csanalytics.powerplatform.microsoft.com"

# ---------------------------------------------------------------------------
# Region table — the single source of truth for the server variable enum, the
# geoName enum and info.x-region-hosts.
#
# geoName: the value GET /gateway/cluster returns, lower-case.
# host:    the analytics host that serves it. Commercial entries give the
#          `region` server-variable value; sovereign entries give a full host,
#          because those sit on different domains.
# probed:  "host" = the host answered GET /api/v2/connections with 200 on
#                   2026-08-27
#          "geo"  = the geoName itself was observed from a live tenant
#          "reachable" = the host answered, but not with a commercial token
#          "provider" = taken from the Terraform provider's map, unprobed
# ---------------------------------------------------------------------------
REGIONS = [
    ("us", "na", "United States.", ["host"]),
    ("can", "can", "Canada.", ["host"]),
    ("sam", "sam", "South America.", ["host"]),
    ("emea", "emea", "Europe, Middle East and Africa — the catch-all European geography, distinct from the single-country European hosts below.", ["host"]),
    ("oce", "oce", "Oceania.", ["host"]),
    ("au", "oce", "Australia. Live-observed geoName, and **absent from the Terraform provider's map**, which is why its analytics data source fails on Australian tenants. There is no `au` host; `oce` serves it.", ["host", "geo"]),
    ("pac", "apac", "Asia Pacific. Note the geoName and the host prefix differ.", ["host"]),
    ("jpn", "jpn", "Japan.", ["host"]),
    ("che", "che", "Switzerland.", ["host"]),
    ("ch", "che", "Switzerland. Alternate geoName spelling carried by the Terraform provider; unattested in a live response.", ["host"]),
    ("fra", "fra", "France.", ["host"]),
    ("uae", "uae", "United Arab Emirates.", ["host"]),
    ("ger", "ger", "Germany.", ["host"]),
    ("gbr", "gbr", "United Kingdom.", ["host"]),
    ("ind", "ind", "India.", ["host"]),
    ("kor", "kor", "Korea.", ["host"]),
    ("nor", "nor", "Norway.", ["host"]),
    ("zaf", "zaf", "South Africa.", ["host"]),
    ("sgp", "sgp", "Singapore. Shares a physical cluster with `apac` but is a separate deployment.", ["host"]),
    ("swe", "swe", "Sweden.", ["host"]),
    ("pol", "pol", "Poland. Host live-verified; **absent from the Terraform provider's map**.", ["host"]),
    ("ita", "ita", "Italy. Host live-verified; **absent from the Terraform provider's map**.", ["host"]),
    ("gov", "gcc.csanalytics.powerplatform.microsoft.us", "US Government Community Cloud.", ["reachable"]),
    ("high", "high.csanalytics.powerplatform.microsoft.us", "US Government GCC High.", ["reachable"]),
    ("dod", "dod.csanalytics.appsplatform.us", "US Department of Defense. Note the different domain — and see `x-provider-defects` for the malformed hostname the Terraform provider ships.", ["reachable"]),
]

# Host prefixes confirmed to answer GET /api/v2/connections with 200.
COMMERCIAL_PREFIXES = sorted({
    host for _, host, _, probed in REGIONS
    if "host" in probed and "." not in host
})

PROVIDER_DEFECTS = [
    "`internal/clients/analytics/data_exports.go` maps DOD to `dod.csanalytics.csanalytics.appsplatform.us`, doubling the `csanalytics` label. That name does not resolve (NXDOMAIN); the real host is `dod.csanalytics.appsplatform.us`, which answers. Corrected here.",
    "The provider's map has no key for geoName `au`, which is what a live Australian tenant returns, so its analytics data source fails with `invalid region: au` before issuing a request. `oce` serves that tenant. Added here.",
    "The provider's map lacks the live `pol` (Poland) and `ita` (Italy) hosts. Added here.",
    "The provider upper-cases the geoName before lookup while the service returns it lower-case. Its map keys are upper-case so this works, but it means an unmapped geography fails hard rather than degrading.",
]

DESCRIPTION = (
    "Unofficial. The Power Platform admin analytics API (\"CS Analytics\") backs the "
    "*Data export* / Application Insights integration in the Power Platform admin "
    "center: the tenant-wide list of analytics data-export connections, each pointing "
    "a set of environments at an Azure sink. The service is undocumented and this spec "
    "is reverse-engineered — from the wire behaviour encoded in "
    "microsoft/terraform-provider-power-platform's client (`internal/clients/analytics`), "
    "itself derived from admin-center traffic recordings, and from live probing of a "
    "real tenant on 2026-08-27 (see `scripts/probe.py`). It is a map, not a contract.\n\n"
    "**Host selection is part of the contract.** There is no single server. The API is "
    "deployed once per geography and a caller must reach *its own* geography's host. "
    "The service publishes no discovery endpoint for these hosts, so the mapping is a "
    "table either way: it is carried here as `info.x-region-hosts`, as the `region` "
    "server-variable `enum`, and as the `enum` on `GatewayCluster.geoName`. All twenty "
    "commercial hosts accept a valid token and answer, so reaching the wrong one is not "
    "an error — a caller that guesses wrong gets a silently incomplete answer.\n\n"
    "**Finding your region** takes a second API. `GET /gateway/cluster` on the "
    "tenant-scoped Power Platform API host returns the caller's `geoName`, which "
    "indexes the host table. That operation belongs to PPAPI, not to this service; it "
    "is reproduced here (tag *Region Discovery*, with its own server and scope) because "
    "the analytics operations cannot be addressed without it. See "
    "[ppapi](../../ppapi) for the rest of that API.\n\n"
    "**What live probing established:** the request and response envelope; the complete "
    "set of reachable hosts and the physical cluster behind each; that "
    "`/api/v2/connections` and its `/api/v1/` twin are read-only; that unknown query "
    "parameters are accepted and ignored; that unknown paths return a bodiless 404; and "
    "three distinct plain-text 401 bodies. **What it did not:** the probe tenant had no "
    "data-export connections configured, so `value` came back empty on every host and "
    "the `Connection` item schema remains provider-derived — it and its children carry "
    "no `x-probe-verified` flag, and their `enum`s record observed vocabulary rather "
    "than a set the service confirmed is closed (each carries `x-enum-evidence`). "
    "Nothing is marked `required`."
)


def region_server() -> dict:
    return {
        "url": "https://{region}.csanalytics.powerplatform.microsoft.com",
        "description": (
            "Commercial cloud. Pick `region` by resolving the caller's `geoName` "
            "through `info.x-region-hosts`; every value in the enum was confirmed to "
            "serve `GET /api/v2/connections`."
        ),
        "variables": {
            "region": {
                "default": "na",
                "enum": COMMERCIAL_PREFIXES,
                "description": (
                    "Regional host prefix. **Not always the geoName**: an Australian "
                    "tenant reports geoName `au` and is served by `oce`, and a `pac` "
                    "tenant by `apac`. Sovereign clouds are separate `servers` entries "
                    "because they use different domains."
                ),
            }
        },
    }


def spec() -> dict:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Power Platform Admin Analytics API (CS Analytics)",
            "version": "v2",
            "description": DESCRIPTION,
            "x-region-hosts": {
                "description": (
                    "geoName (from `GET /gateway/cluster`, compared case-insensitively) "
                    "-> analytics host. Commercial entries give the `region` "
                    "server-variable value; sovereign entries give a full host, because "
                    "those sit on different domains."
                ),
                "map": {geo: host for geo, host, _, _ in REGIONS},
                "notes": {geo: note for geo, _, note, _ in REGIONS},
                "verification": {geo: probed for geo, _, _, probed in REGIONS},
                "x-verification-legend": {
                    "host": "the host answered GET /api/v2/connections with 200 on 2026-08-27",
                    "geo": "this geoName was observed in a live gateway/cluster response",
                    "reachable": "the host answered, but rejects a commercial-cloud token, so its paths were not probed",
                },
                "x-provider-defects": PROVIDER_DEFECTS,
            },
        },
        "servers": [
            region_server(),
            {
                "url": "https://gcc.csanalytics.powerplatform.microsoft.us",
                "description": "US Government Community Cloud. Reachable; not probed with a matching token.",
            },
            {
                "url": "https://high.csanalytics.powerplatform.microsoft.us",
                "description": "US Government GCC High. Reachable; not probed with a matching token.",
            },
            {
                "url": "https://dod.csanalytics.appsplatform.us",
                "description": "US Department of Defense. Reachable; not probed with a matching token. See `info.x-region-hosts.x-provider-defects` for the malformed name the Terraform provider ships for this cloud.",
            },
        ],
        "security": [{"analytics_auth": [ANALYTICS_SCOPE]}],
        "tags": [
            {
                "name": "Data Export Connections",
                "description": (
                    "A data-export connection is the tenant-level object behind *Data "
                    "export* in the Power Platform admin center: it binds a set of "
                    "environments to one Azure sink (an Application Insights component) "
                    "and streams a chosen set of telemetry scenarios into it, reporting "
                    "ingestion health per scenario. Connections are created and edited "
                    "in the admin center UI; this API only reads them back."
                ),
            },
            {
                "name": "Region Discovery",
                "description": (
                    "Which geography, and therefore which analytics host, serves the "
                    "caller's tenant. This resource belongs to the Power Platform API "
                    "(ppapi) rather than to analytics; it is reproduced here because no "
                    "analytics operation can be addressed without it."
                ),
            },
        ],
        "paths": {
            "/api/v2/connections": {
                "get": {
                    "operationId": "connections_list",
                    "summary": "List",
                    "tags": ["Data Export Connections"],
                    "x-probe-verified": True,
                    "description": (
                        "Returns every data-export connection the caller's geography holds "
                        "for the tenant, wrapped in a `{ \"value\": [...] }` envelope. There "
                        "is no `@odata` metadata, no `nextLink` and no observed paging; "
                        "`$top`, `$filter` and every other query parameter are accepted and "
                        "ignored, so the response is always the full set.\n\n"
                        "**Resolve the host before calling this.** Results are scoped to the "
                        "geography the host serves, and a valid token is accepted on *every* "
                        "regional host, so an unresolved guess succeeds and returns the wrong "
                        "geography's (usually empty) list. Call *Region Discovery* first, take "
                        "`geoName` from its response and index `info.x-region-hosts`.\n\n"
                        "The path is read-only. The Terraform provider carries a "
                        "`DataCreateDto` shaped like a create body, but no create operation "
                        "exists here — connections are configured in the admin center under "
                        "*Data export*.\n\n"
                        "Each connection's sink carries its Application Insights "
                        "instrumentation key in plain text, so treat the whole response body "
                        "as a credential.\n\n"
                        "Service principals do not work against this API in practice; the "
                        "Terraform provider documents its analytics data source as user-auth "
                        "only."
                    ),
                    "responses": {
                        "200": {
                            "description": (
                                "The tenant's data-export connections in this geography. An "
                                "empty `value` is normal and ambiguous — it means either that "
                                "nothing is configured or that this host serves a geography "
                                "the tenant does not use, so confirm the region before "
                                "reading it as \"none configured\"."
                            ),
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ConnectionListResponse"},
                                    "examples": {
                                        "empty": {
                                            "summary": "No connections configured — the live-probed result",
                                            "value": {"value": []},
                                        },
                                        "appInsights": {
                                            "summary": "One Application Insights connection — provider-derived, not live-verified",
                                            "value": {
                                                "value": [
                                                    {
                                                        "id": "00000000-0000-0000-0000-000000000000",
                                                        "source": "AppInsight",
                                                        "environments": [
                                                            {
                                                                "environmentId": "00000000-0000-0000-0000-000000000000",
                                                                "organizationId": "00000000-0000-0000-0000-000000000000",
                                                            }
                                                        ],
                                                        "sink": {
                                                            "id": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso-analytics/providers/microsoft.insights/components/contoso-insights",
                                                            "type": "AppInsights",
                                                            "resourceName": "contoso-insights",
                                                            "key": "00000000-0000-0000-0000-000000000000",
                                                        },
                                                        "status": [
                                                            {
                                                                "name": "Plugin executions excep",
                                                                "state": "Connected",
                                                                "lastRunOn": "2025-03-08T06:55:56.0481713+00:00",
                                                                "message": None,
                                                            }
                                                        ],
                                                        "scenarios": ["Plugin executions excep"],
                                                        "packageName": "contoso",
                                                        "resourceProvider": "dataverse",
                                                        "aiType": "Local",
                                                    }
                                                ]
                                            },
                                        },
                                    },
                                }
                            },
                        },
                        "401": {"$ref": "#/components/responses/Unauthorized"},
                        "403": {"$ref": "#/components/responses/Forbidden"},
                        "404": {"$ref": "#/components/responses/NotFound"},
                        "405": {"$ref": "#/components/responses/MethodNotAllowed"},
                    },
                }
            },
            "/api/v1/connections": {
                "get": {
                    "operationId": "connections_list_v1",
                    "summary": "List (v1)",
                    "tags": ["Data Export Connections"],
                    "x-probe-verified": True,
                    "description": (
                        "The predecessor of the v2 listing, still served on every regional "
                        "host. Against an empty tenant it is indistinguishable from v2: same "
                        "envelope, same read-only behaviour. Whether the item shape differs "
                        "could not be established, because the probe tenant had no "
                        "connections. Prefer v2; this is documented only because it answers."
                    ),
                    "responses": {
                        "200": {
                            "description": "The tenant's data-export connections in this geography.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ConnectionListResponse"}
                                }
                            },
                        },
                        "401": {"$ref": "#/components/responses/Unauthorized"},
                        "405": {"$ref": "#/components/responses/MethodNotAllowed"},
                    },
                }
            },
            "/gateway/cluster": {
                "servers": [
                    {
                        "url": "https://{tenantPrefix}.{tenantSuffix}.tenant.api.powerplatform.com",
                        "description": (
                            "The tenant-scoped Power Platform API host. The label is the "
                            "tenant GUID with hyphens stripped, split so the final two "
                            "characters form their own label."
                        ),
                        "variables": {
                            "tenantPrefix": {
                                "default": "00000000000000000000000000000",
                                "description": "The tenant GUID without hyphens, less its final two characters — 30 characters.",
                            },
                            "tenantSuffix": {
                                "default": "00",
                                "description": "The final two characters of the tenant GUID without hyphens.",
                            },
                        },
                    }
                ],
                "get": {
                    "operationId": "gatewayCluster_read",
                    "summary": "Gateway Cluster Read",
                    "tags": ["Region Discovery"],
                    "x-probe-verified": True,
                    "x-source-api": "ppapi",
                    "description": (
                        "Returns the Power Platform cluster serving the caller, whose "
                        "`geoName` selects the analytics host through "
                        "`info.x-region-hosts`. This is a PPAPI operation: it lives on the "
                        "tenant-scoped `api.powerplatform.com` host and takes the Power "
                        "Platform API scope, not the analytics one — note the per-operation "
                        "`servers` and `security` overrides.\n\n"
                        "Two things about it are surprising, and both were confirmed live. "
                        "The tenant GUID in the host is **decorative**: a bogus tenant label, "
                        "and even the bare `api.powerplatform.com` host with no tenant label "
                        "at all, return the caller's own cluster, because the answer is "
                        "derived from the bearer token. And `api-version` is optional and "
                        "ignored — omitting it, or passing `2`, returns the same body as "
                        "`api-version=1`, which is what the Terraform provider sends."
                    ),
                    "security": [{"ppapi_auth": [PPAPI_SCOPE]}],
                    "parameters": [
                        {
                            "name": "api-version",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "default": "1", "example": "1"},
                            "description": "Ignored by the service — omitting it or passing any value returns the same body. The Terraform provider sends `1`.",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "The cluster serving the caller's tenant.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/GatewayCluster"},
                                    "example": {
                                        "clusterNumber": "001",
                                        "geoName": "au",
                                        "environment": "Prod",
                                        "clusterType": "CustomerManagement",
                                        "clusterCategory": "Prod",
                                        "clusterName": "prdcm001eau",
                                        "geoLongName": "australia",
                                    },
                                }
                            },
                        },
                        "401": {"$ref": "#/components/responses/Unauthorized"},
                    },
                },
            },
        },
        "components": {
            "securitySchemes": {
                "analytics_auth": {
                    "type": "oauth2",
                    "description": "Microsoft Entra ID OAuth2. The analytics hosts accept tokens for the admin-analytics audience only; a valid Power Platform API token is rejected.",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                            "tokenUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                            "scopes": {ANALYTICS_SCOPE: "Power Platform admin analytics"},
                        }
                    },
                },
                "ppapi_auth": {
                    "type": "oauth2",
                    "description": "Microsoft Entra ID OAuth2 for the Power Platform API, used only by the region-discovery operation.",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                            "tokenUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                            "scopes": {PPAPI_SCOPE: "Power Platform API"},
                        }
                    },
                },
            },
            "responses": {
                "Unauthorized": {
                    "description": (
                        "The token was rejected at the gateway, before the service saw the "
                        "request. The body is `text/plain`, not JSON, and takes one of three "
                        "observed forms: empty, with `WWW-Authenticate: Bearer "
                        "error=\"invalid_token\"`, when no `Authorization` header was sent; "
                        "`MISE unauthorized.` for a malformed bearer; and `An error occurred "
                        "processing your authentication.` for a well-formed token issued for "
                        "the wrong audience — the last is the one to check first, since the "
                        "analytics hosts reject Power Platform API tokens."
                    ),
                    "content": {
                        "text/plain": {
                            "schema": {
                                "type": "string",
                                "enum": ["", "MISE unauthorized.", "An error occurred processing your authentication."],
                                "x-enum-evidence": "The three bodies observed on 2026-08-27; the gateway may emit others.",
                            }
                        }
                    },
                    "headers": {
                        "WWW-Authenticate": {
                            "description": "Sent only when the request carried no `Authorization` header.",
                            "schema": {"type": "string", "example": "Bearer error=\"invalid_token\""},
                        }
                    },
                },
                "Forbidden": {
                    "description": "The token is valid for this audience but the caller is not a tenant administrator. Not reproduced live — the probe account is an admin — but it is the rejection the Terraform provider's tests pin for this operation.",
                },
                "NotFound": {
                    "description": "No such route. The body is empty: the service returns no error document for unknown paths. `/api/v2/connections/{id}` answers this way, so there is no per-connection read — fetch the list and filter it.",
                },
                "MethodNotAllowed": {
                    "description": "The connections paths are read-only. Every method other than `GET` — including `OPTIONS` and `HEAD` — is refused this way, with an `Allow` header naming `GET` alone.",
                    "headers": {
                        "Allow": {
                            "description": "Always `GET`.",
                            "schema": {"type": "string", "enum": ["GET"], "example": "GET"},
                        }
                    },
                },
            },
            "schemas": {
                "ConnectionListResponse": {
                    "type": "object",
                    "x-probe-verified": True,
                    "description": "The listing envelope. Live-verified: `value` is its only member, with no paging cursor and no `@odata` metadata alongside it.",
                    "properties": {
                        "value": {
                            "type": "array",
                            "description": "Every data-export connection in this geography, unordered and unpaged.",
                            "items": {"$ref": "#/components/schemas/Connection"},
                        }
                    },
                },
                "Connection": {
                    "type": "object",
                    "description": (
                        "One data-export connection: a set of environments streaming a set of "
                        "telemetry scenarios into one Azure sink. Note what is *not* here — "
                        "there is no schedule, frequency or retention field. Export cadence is "
                        "fixed by the service and is not caller-configurable; the only "
                        "timing signal a connection exposes is each scenario's `lastRunOn`. "
                        "**Provider-derived and not live-verified**: the probe tenant had no "
                        "connections, so every member below comes from the Terraform "
                        "provider's DTO and its recorded admin-center fixture, and the service "
                        "may return more."
                    ),
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "00000000-0000-0000-0000-000000000000",
                        },
                        "source": {
                            "type": "string",
                            "description": "The integration that produced this connection — which admin-center feature created it. Distinct from `resourceProvider`, which names the Power Platform service whose telemetry is being exported.",
                            "enum": ["AppInsight"],
                            "x-enum-evidence": "Single value observed in the provider's recorded admin-center fixture; the set may be larger.",
                            "example": "AppInsight",
                        },
                        "environments": {
                            "type": "array",
                            "description": "The environments whose telemetry this connection exports. One connection covers many environments, and an environment may appear in more than one connection, so this is not a partition.",
                            "items": {"$ref": "#/components/schemas/ConnectionEnvironment"},
                        },
                        "status": {
                            "type": "array",
                            "description": "Ingestion health, one entry per exported scenario — each entry's `name` matches a member of `scenarios`. Health is reported per scenario, not per connection, so a connection can be healthy for some streams and stalled for others.",
                            "items": {"$ref": "#/components/schemas/ConnectionStatus"},
                        },
                        "sink": {"$ref": "#/components/schemas/Sink"},
                        "packageName": {
                            "type": "string",
                            "description": "The analytics package — the named bundle of scenarios — the connection was created from. Set by the admin center at configuration time and not otherwise meaningful to a caller.",
                        },
                        "scenarios": {
                            "type": "array",
                            "description": "The telemetry streams this connection exports. Carried as UI display strings rather than stable codes (`Plugin executions excep` is a truncated label, not an identifier), so match them to `status[].name` rather than treating them as an API vocabulary.",
                            "items": {"type": "string"},
                            "example": ["Plugin executions excep", "SDK executions excep"],
                        },
                        "resourceProvider": {
                            "type": "string",
                            "description": "The Power Platform service emitting the telemetry. Despite the name this is not an Azure resource-provider namespace — the observed value is the lower-case service name `dataverse`.",
                            "enum": ["dataverse"],
                            "x-enum-evidence": "Single value observed in the provider's recorded admin-center fixture; the set may be larger.",
                            "example": "dataverse",
                        },
                        "aiType": {
                            "type": "string",
                            "description": "How the Application Insights resource is attached. `Local` means the customer supplied their own component in their own subscription — the only arrangement the admin center's data-export UI offers.",
                            "enum": ["Local"],
                            "x-enum-evidence": "Single value observed in the provider's recorded admin-center fixture; the set may be larger.",
                            "example": "Local",
                        },
                    },
                },
                "ConnectionEnvironment": {
                    "type": "object",
                    "description": "One environment in a connection's scope, identified twice over: telemetry is emitted against the Dataverse organization, while everything else in Power Platform addresses the environment, so both ids are carried.",
                    "properties": {
                        "environmentId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "00000000-0000-0000-0000-000000000000",
                        },
                        "organizationId": {
                            "type": "string",
                            "format": "uuid",
                            "description": "The Dataverse organization id of the environment, which is what appears in the exported telemetry. Environments without Dataverse have none and cannot be exported from.",
                            "example": "00000000-0000-0000-0000-000000000000",
                        },
                    },
                },
                "ConnectionStatus": {
                    "type": "object",
                    "description": "Ingestion health for a single exported scenario within a connection.",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The scenario this entry reports on; matches an entry in the connection's `scenarios`.",
                            "example": "Plugin executions excep",
                        },
                        "state": {
                            "type": "string",
                            "description": "Whether the exporter is attached and delivering for this scenario. `Connected` is the healthy state.",
                            "enum": ["Connected"],
                            "x-enum-evidence": "Single value observed in the provider's recorded admin-center fixture; failure states exist but were not captured.",
                            "example": "Connected",
                        },
                        "lastRunOn": {
                            "type": "string",
                            "format": "date-time",
                            "description": "When this scenario last exported. With no schedule field on a connection, this is the only freshness signal a caller gets: a `lastRunOn` far in the past is how a stalled export shows up. Serialised in the .NET round-trip form — a numeric UTC offset and seven fractional-second digits — not the `Z`-suffixed form other Power Platform APIs use.",
                            "example": "2025-03-08T06:55:56.0481713+00:00",
                        },
                        "message": {
                            "type": "string",
                            "nullable": True,
                            "description": "Explanatory text for a non-healthy `state`. Sent as an explicit `null`, not omitted, when there is nothing to report.",
                        },
                    },
                },
                "Sink": {
                    "type": "object",
                    "description": "The Azure destination a connection writes telemetry into — in practice a customer-owned Application Insights component, which is then queried like any other Application Insights data.",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "The sink's full ARM resource id, and the authoritative locator: `subscriptionId` and `resourceGroupName` merely restate parts of it and are not always sent, so parse this when you need them reliably.",
                            "example": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/contoso-analytics/providers/microsoft.insights/components/contoso-insights",
                        },
                        "type": {
                            "type": "string",
                            "description": "The kind of destination, which determines how the remaining sink fields are read. `AppInsights` is an Application Insights component addressed by instrumentation key.",
                            "enum": ["AppInsights"],
                            "x-enum-evidence": "Single value observed in the provider's recorded admin-center fixture and its DTO; the data-export feature offers no other destination today.",
                            "example": "AppInsights",
                        },
                        "subscriptionId": {
                            "type": "string",
                            "format": "uuid",
                            "description": "Azure subscription holding the sink. Omitted from the recorded response even though `id` contains it — treat it as optional.",
                            "example": "00000000-0000-0000-0000-000000000000",
                        },
                        "resourceGroupName": {
                            "type": "string",
                            "description": "Resource group holding the sink. Omitted from the recorded response even though `id` contains it — treat it as optional.",
                            "example": "contoso-analytics",
                        },
                        "resourceName": {
                            "type": "string",
                            "description": "Name of the Application Insights component; the last segment of `id`.",
                            "example": "contoso-insights",
                        },
                        "key": {
                            "type": "string",
                            "description": "The Application Insights instrumentation key the exporter writes with. This is a live credential returned in plain text by an unprivileged-looking list call — do not log the response, and rotate the key if it leaks.",
                            "example": "00000000-0000-0000-0000-000000000000",
                        },
                    },
                },
                "GatewayCluster": {
                    "type": "object",
                    "x-probe-verified": True,
                    "description": "The Power Platform cluster serving a tenant. Its `geoName` is the key that selects an analytics host. Live-verified: all seven members were present.",
                    "properties": {
                        "clusterNumber": {
                            "type": "string",
                            "description": "Zero-padded ordinal of the cluster within its geography — a string, not a number.",
                            "example": "001",
                        },
                        "geoName": {
                            "type": "string",
                            "description": "Short geography code, lower-case, and **not** an Azure region name. This is the key into `info.x-region-hosts`; several codes do not match their host prefix (`au` -> `oce`, `pac` -> `apac`).",
                            "enum": [geo for geo, _, _, _ in REGIONS],
                            "x-enum-evidence": "`au` was observed live; `us` appears in the Terraform provider's recorded fixture; the remainder are the keys of the provider's host map, which the provider documents as gateway-cluster geo names. The set may be incomplete — treat an unknown code as a missing host-table entry, not as an error.",
                            "example": "au",
                        },
                        "environment": {
                            "type": "string",
                            "description": "Service ring the cluster belongs to. Unrelated to a Power Platform environment.",
                            "example": "Prod",
                        },
                        "clusterType": {
                            "type": "string",
                            "description": "Role of the cluster within the ring.",
                            "example": "CustomerManagement",
                        },
                        "clusterCategory": {
                            "type": "string",
                            "description": "Broad classification of the cluster; in the observed response it repeats `environment`.",
                            "example": "Prod",
                        },
                        "clusterName": {
                            "type": "string",
                            "description": "Internal cluster identifier, encoding ring, type, number and Azure region — `prdcm001eau` is production customer-management cluster 001 in East Australia. Useful for correlating with the `x-ms-islandgateway` response header.",
                            "example": "prdcm001eau",
                        },
                        "geoLongName": {
                            "type": "string",
                            "description": "Lower-case long geography name, matching the `location` an environment reports.",
                            "example": "australia",
                        },
                    },
                },
            },
        },
    }


def _operations(doc: dict) -> set:
    """Every (path, method) the document declares."""
    verbs = {"get", "put", "post", "delete", "patch", "head", "options"}
    return {(p, m) for p, item in doc.get("paths", {}).items()
            for m in item if m in verbs}


def main() -> None:
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "oas", "openapi.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fresh = spec()

    # Refuse to regress the published spec.
    #
    # This script used to open the output "w" and dump into it, which truncated
    # the file BEFORE the new content existed: a raise inside spec() left a
    # half-written spec, and a successful run silently deleted anything the file
    # had gained since. That is not hypothetical -- the spec had been enriched
    # from mined evidence to 29 operations while this emitter still knew about
    # three, so the next run would have dropped 26 of them and reported success.
    #
    # An emitter that only ever adds is safe to run. One that would remove is
    # out of date with the file it owns, and it must say so rather than win.
    if os.path.exists(out):
        try:
            with open(out, encoding="utf-8") as handle:
                published = json.load(handle)
        except (OSError, ValueError) as exc:
            raise SystemExit(f"{out} exists but could not be read ({exc}); "
                             f"refusing to overwrite a file this script cannot compare against")
        lost = _operations(published) - _operations(fresh)
        if lost:
            listed = "\n".join(f"  {m.upper():7}{p}" for p, m in sorted(lost))
            raise SystemExit(
                f"refusing to write {out}: it would drop "
                f"{len(lost)} operation(s) the published spec already carries:\n"
                f"{listed}\n"
                f"Those came from mined evidence this emitter does not know about. "
                f"Teach it those operations, or move the hand-authored surface into "
                f"an enrichment file this script merges, as ppapi/enrichment.json does. "
                f"Do not delete them to make this run pass.")

    # Write via a temp file and rename, so a failure mid-write cannot leave a
    # truncated spec where a valid one was.
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(fresh, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    os.replace(tmp, out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
