#!/usr/bin/env python3
"""Live probe for the Power Platform admin analytics (CS Analytics) API.

Read-only. Every request this script makes is a GET, an OPTIONS or a
deliberately-unsupported method against a path that only serves GET; nothing
is created, changed or deleted. The output is a *shape* summary — field names,
types, cardinalities, status codes — never tenant data.

What it establishes, in order:

  1. region discovery   GET {tenantHost}/gateway/cluster  (PPAPI, tenant-scoped)
     -> the caller's `geoName`, which is what the Terraform provider feeds into
        its geoName -> analytics-host map.
  2. host reachability  a DNS + GET sweep over every candidate regional host,
     so the spec's `servers` enum lists hosts that actually answer.
  3. the one operation  GET {analyticsHost}/api/v2/connections
     -> the response envelope, and the item shape when the tenant has any
        data-export connections configured.
  4. contract edges     allowed methods, unknown paths, unknown query params,
     api-version handling, and the three authentication failure modes.

Usage:

    python3 probe.py                          # everything, tenant id from az
    python3 probe.py --tenant-id <guid>       # explicit tenant id
    python3 probe.py --region oce             # skip discovery, probe one host
    python3 probe.py --hosts                  # host reachability sweep only
    python3 probe.py --edges                  # contract-edge probes only

Tokens come from the logged-in Azure CLI session; no secret is ever printed.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

ANALYTICS_SCOPE = "https://adminanalytics.powerplatform.microsoft.com/.default"
PPAPI_SCOPE = "https://api.powerplatform.com/.default"

PPAPI_HOST_SUFFIX = "tenant.api.powerplatform.com"

# Candidate regional analytics hosts. The commercial cloud names a host by a
# short geo prefix; the sweep in --hosts decides which of these are real, so
# extra guesses here are free.
COMMERCIAL_PREFIXES = [
    "na", "can", "sam", "emea", "oce", "apac", "jpn", "che", "fra", "uae",
    "ger", "gbr", "ind", "kor", "nor", "zaf", "sgp", "swe", "pol", "ita",
    # guesses, kept so the sweep can disprove them
    "au", "aus", "eur", "asia", "us", "sg", "chn", "isr", "esp", "nld",
]
COMMERCIAL_SUFFIX = "csanalytics.powerplatform.microsoft.com"
SOVEREIGN_HOSTS = [
    "gcc.csanalytics.powerplatform.microsoft.us",
    "high.csanalytics.powerplatform.microsoft.us",
    "dod.csanalytics.appsplatform.us",
    # the hostname the Terraform provider actually ships for DOD; it does not
    # resolve, which is the point of probing it.
    "dod.csanalytics.csanalytics.appsplatform.us",
]

# geoName (from gateway/cluster, lower-cased) -> regional host prefix. The
# service publishes no discovery endpoint for this, so it is a table either
# way; this one corrects the Terraform provider's, which has no entry for the
# 'au' geoName a live Australian tenant returns.
GEO_TO_PREFIX = {
    "us": "na", "can": "can", "sam": "sam", "emea": "emea", "oce": "oce",
    "au": "oce", "pac": "apac", "jpn": "jpn", "che": "che", "ch": "che",
    "fra": "fra", "uae": "uae", "ger": "ger", "gbr": "gbr", "ind": "ind",
    "kor": "kor", "nor": "nor", "zaf": "zaf", "sgp": "sgp", "swe": "swe",
    "pol": "pol", "ita": "ita",
}

PAUSE = 0.4  # seconds between calls; the service is shared, do not hammer it


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------

def token(scope: str) -> str:
    """Fetch an access token for `scope` from the logged-in az CLI session."""
    out = subprocess.run(
        ["az", "account", "get-access-token", "--scope", scope,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def az_tenant_id() -> str:
    out = subprocess.run(
        ["az", "account", "show", "--query", "tenantId", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def tenant_host(tenant_id: str, suffix: str = PPAPI_HOST_SUFFIX) -> str:
    """The tenant-scoped PPAPI host: {guid-no-dashes minus last 2}.{last 2}."""
    flat = tenant_id.replace("-", "")
    return f"{flat[:-2]}.{flat[-2:]}.{suffix}"


def call(url: str, bearer: str | None = None, method: str = "GET",
         timeout: int = 30) -> tuple[int, dict[str, str], str]:
    """Issue one request. Returns (status, headers, body). Never raises on 4xx/5xx.

    Header names are lower-cased: HTTP/2 sends them lower-case and HTTP/1.1
    does not, and the probe reads `allow` and `www-authenticate` by name.
    """
    def lower(headers) -> dict[str, str]:
        return {k.lower(): v for k, v in (headers or {}).items()}

    req = urllib.request.Request(url, method=method)
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, lower(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, lower(err.headers), err.read().decode("utf-8", "replace")
    except (urllib.error.URLError, socket.gaierror, ssl.SSLError, TimeoutError) as err:
        return 0, {}, f"{type(err).__name__}: {err}"
    finally:
        time.sleep(PAUSE)


def resolves(host: str) -> bool:
    try:
        socket.getaddrinfo(host, 443)
        return True
    except socket.gaierror:
        return False


def shape(value, path: str = "", out: dict | None = None) -> dict:
    """Flatten a JSON value into {dotted.path: type-name}. Arrays collapse to [0]."""
    out = {} if out is None else out
    if isinstance(value, dict):
        for key, item in value.items():
            shape(item, f"{path}.{key}" if path else key, out)
    elif isinstance(value, list):
        out[f"{path}[]"] = f"array({len(value)})"
        for item in value[:1]:
            shape(item, f"{path}[0]", out)
    else:
        out[path] = "null" if value is None else type(value).__name__
    return out


def print_shape(label: str, body: str) -> dict | None:
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        print(f"  {label}: non-JSON body ({len(body)} bytes)")
        return None
    print(f"  {label}:")
    for key, kind in sorted(shape(parsed).items()):
        print(f"    {key}: {kind}")
    return parsed


# --------------------------------------------------------------------------
# probes
# --------------------------------------------------------------------------

def probe_region(tenant_id: str) -> str | None:
    """Region discovery: the PPAPI gateway/cluster lookup."""
    print("\n== 1. region discovery (PPAPI gateway/cluster) ==")
    bearer = token(PPAPI_SCOPE)
    host = tenant_host(tenant_id)
    status, _, body = call(f"https://{host}/gateway/cluster?api-version=1", bearer)
    print(f"  GET {{tenantHost}}/gateway/cluster?api-version=1 -> {status}")
    parsed = print_shape("shape", body)
    if status != 200 or not isinstance(parsed, dict):
        return None

    geo = parsed.get("geoName")
    print(f"  geoName -> {geo!r}  geoLongName -> {parsed.get('geoLongName')!r}")
    if geo and geo.lower() not in GEO_TO_PREFIX:
        print(f"  the Terraform provider upper-cases this and looks up"
              f" {geo.upper()!r} in its host map; a missing key makes its"
              f" analytics data source fail with 'invalid region: {geo}'.")

    # Is the tenant id in the host actually load-bearing, or is the answer
    # derived from the token alone?
    for label, alt in [
        ("bogus tenant label", tenant_host("0" * 32)),
        ("no tenant label", "api.powerplatform.com"),
    ]:
        alt_status, _, alt_body = call(f"https://{alt}/gateway/cluster?api-version=1", bearer)
        same = alt_status == 200 and json.loads(alt_body or "{}").get("geoName") == geo
        print(f"  {label}: {alt_status}" + ("  (same cluster -> host label ignored)" if same else ""))

    no_version, _, _ = call(f"https://{host}/gateway/cluster", bearer)
    print(f"  api-version omitted -> {no_version}")
    return geo


def probe_hosts() -> list[str]:
    """Host reachability: which regional analytics hosts actually serve the API."""
    print("\n== 2. regional host sweep ==")
    bearer = token(ANALYTICS_SCOPE)
    live: list[str] = []
    candidates = [f"{p}.{COMMERCIAL_SUFFIX}" for p in COMMERCIAL_PREFIXES] + SOVEREIGN_HOSTS
    for host in candidates:
        if not resolves(host):
            print(f"  {host:<58} DNS: no such host")
            continue
        status, headers, _ = call(f"https://{host}/api/v2/connections", bearer)
        # x-ms-islandgateway names the physical cluster behind the host; it is
        # the evidence that each prefix is a distinct regional deployment.
        cluster = headers.get("x-ms-islandgateway", "")
        note = {200: "serves the API", 401: "reachable, rejects a commercial token"}.get(
            status, "resolves but does not serve this path")
        print(f"  {host:<58} {status}  {note}  {cluster}")
        if status == 200:
            live.append(host)
    return live


def probe_connections(host: str) -> None:
    """The one operation the Terraform provider calls."""
    print(f"\n== 3. connections listing on {host} ==")
    bearer = token(ANALYTICS_SCOPE)
    for version in ("v2", "v1"):
        status, headers, body = call(f"https://{host}/api/{version}/connections", bearer)
        print(f"  GET /api/{version}/connections -> {status}"
              f"  content-type={headers.get('content-type', '-')}")
        parsed = print_shape("envelope", body)
        if version == "v2" and isinstance(parsed, dict):
            items = parsed.get("value") or []
            print(f"  connections configured: {len(items)}")
            if not items:
                print("  NOTE: no connections configured on this tenant — the item"
                      " schema stays provider-derived and unverified.")
            for index, item in enumerate(items):
                print(f"  item[{index}] shape:")
                for key, kind in sorted(shape(item).items()):
                    print(f"    {key}: {kind}")
                # enum-ish fields are safe to echo: they are service vocabulary,
                # not tenant identifiers.
                for field in ("source", "aiType", "resourceProvider"):
                    if field in item:
                        print(f"    literal {field} = {item[field]!r}")
                for entry in item.get("status") or []:
                    print(f"    literal status.state = {entry.get('state')!r}")
                for field in ("type",):
                    if field in (item.get("sink") or {}):
                        print(f"    literal sink.{field} = {item['sink'][field]!r}")


def probe_edges(host: str) -> None:
    """Contract edges: methods, unknown paths, query handling, auth failures."""
    print(f"\n== 4. contract edges on {host} ==")
    bearer = token(ANALYTICS_SCOPE)
    base = f"https://{host}/api/v2/connections"

    print("  methods:")
    for method in ("OPTIONS", "POST", "PUT", "PATCH", "DELETE", "HEAD"):
        status, headers, _ = call(base, bearer, method=method)
        allow = headers.get("allow")
        print(f"    {method:<8} -> {status}" + (f"  Allow: {allow}" if allow else ""))

    print("  unknown paths (siblings the service might expose):")
    for path in ("api/v3/connections", "api/connections",
                 "api/v2/connections/00000000-0000-0000-0000-000000000000",
                 "api/v2/environments", "api/v2/sinks", "api/v2/scenarios",
                 "api/v2/packages", "api/v2/sources", "api/v2/settings",
                 "api/v2/status", "api/v2/exports", "api/v2/tenants", "health"):
        status, _, body = call(f"https://{host}/{path}", bearer)
        print(f"    /{path:<52} -> {status} ({len(body)}-byte body)")

    print("  query parameters (are unknown ones rejected or ignored?):")
    for query in ("?api-version=2", "?%24top=1", "?source=app",
                  "?environmentId=00000000-0000-0000-0000-000000000000"):
        status, _, body = call(base + query, bearer)
        print(f"    {query:<52} -> {status} {body[:40]}")

    print("  authentication failures:")
    status, headers, body = call(base)
    print(f"    no Authorization header  -> {status}"
          f"  WWW-Authenticate: {headers.get('www-authenticate', '-')}  body={body[:60]!r}")
    status, _, body = call(base, "not.a.real.token")
    print(f"    malformed bearer         -> {status}  body={body[:60]!r}")
    status, _, body = call(base, token(PPAPI_SCOPE))
    print(f"    valid token, wrong audience -> {status}  body={body[:60]!r}")


# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tenant-id", default=os.environ.get("PP_TENANT_ID"),
                        help="tenant GUID (default: the az CLI session's tenant)")
    parser.add_argument("--region", default=os.environ.get("PP_ANALYTICS_REGION"),
                        help="analytics host prefix to probe, e.g. 'oce'; "
                             "skips region discovery")
    parser.add_argument("--hosts", action="store_true", help="host sweep only")
    parser.add_argument("--edges", action="store_true", help="edge probes only")
    args = parser.parse_args()

    if args.hosts:
        probe_hosts()
        return 0

    host = None
    if args.region:
        host = f"{args.region}.{COMMERCIAL_SUFFIX}"
    else:
        tenant_id = args.tenant_id or az_tenant_id()
        geo = probe_region(tenant_id)
        prefix = GEO_TO_PREFIX.get((geo or "").lower())
        if geo and not prefix:
            print(f"\n  geoName {geo!r} maps to no known analytics host — add it"
                  " to GEO_TO_PREFIX once the sweep below shows which host serves it.")
        live = probe_hosts()
        if not live:
            print("no reachable analytics host; stopping", file=sys.stderr)
            return 1
        host = f"{prefix}.{COMMERCIAL_SUFFIX}" if prefix else live[0]
        print(f"\n  probing operations against {host}"
              " (pass --region to pick a different one)")

    if args.edges:
        probe_edges(host)
        return 0

    probe_connections(host)
    probe_edges(host)
    return 0


if __name__ == "__main__":
    sys.exit(main())
