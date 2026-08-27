#!/usr/bin/env python3
"""Live probe harness for the PowerApps API (api.powerapps.com).

Every request is a read-only GET. Nothing here mutates the tenant.

The point of the harness is to check the spec against the service: it walks the
operations in ``oas/openapi.json``, records the status code the service really
returns, and prints a *shape* of each response (key names and value types) so
you can diff the schemas without ever staring at tenant data.

Usage
-----
    scripts/probe.py --environment <environmentId>
    scripts/probe.py --environment <environmentId> --connector shared_sharepointonline
    scripts/probe.py --environment <environmentId> --all-environments
    scripts/probe.py --discover-environment          # pick the first env the token can see

Ids come from the command line or from ``PA_ENVIRONMENT_ID`` / ``PA_CONNECTOR``.
Nothing tenant-specific is hardcoded, and the output prints no ids, no
hostnames, no display names and no user identities — only shapes, counts and
status codes.

Authentication uses the logged-in Azure CLI session:

    az account get-access-token --scope https://service.powerapps.com/.default

The same token audience serves BAPI (``api.bap.microsoft.com``); see ../bapi.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCOPE = "https://service.powerapps.com/.default"
DEFAULT_HOST = "https://api.powerapps.com"

# api-version defaults, matching oas/openapi.json.
APPS_API_VERSION = "2023-06-01"
CONNECTORS_API_VERSION = "2019-05-01"
CORE_API_VERSION = "2016-11-01"

# Fields worth calling out when they show up (or fail to): the ones the
# Terraform provider's client models, plus the ones only the live service
# returns.
PROVIDER_APP_FIELDS = [
    "displayName", "owner", "createdBy", "lastModifiedBy", "lastPublishedBy",
    "createdTime", "lastModifiedTime", "lastPublishTime", "environment",
]
PROVIDER_CONNECTOR_FIELDS = ["displayName", "description", "tier", "publisher"]


def token(scope: str = SCOPE) -> str:
    out = subprocess.run(
        ["az", "account", "get-access-token", "--scope", scope,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def shape(value, depth: int = 0, maxdepth: int = 5):
    """Reduce a JSON value to key names and value types.

    Lists of objects collapse to a single merged object so a 1700-element
    connector list prints as one schema. No leaf value is ever echoed.
    """
    if depth > maxdepth:
        return "..."
    if isinstance(value, dict):
        return {k: shape(v, depth + 1, maxdepth) for k, v in value.items()}
    if isinstance(value, list):
        if not value:
            return []
        if all(isinstance(x, dict) for x in value):
            merged: dict = {}
            for item in value:
                for k, v in item.items():
                    if k not in merged or merged[k] in (None, [], {}):
                        merged[k] = shape(v, depth + 1, maxdepth)
            return [merged]
        return [shape(value[0], depth + 1, maxdepth)]
    if value is None:
        return None
    return type(value).__name__


class Probe:
    def __init__(self, host: str, bearer: str, pause: float = 1.0):
        self.host = host.rstrip("/")
        self.bearer = bearer
        self.pause = pause
        self.results: list[tuple[str, int]] = []

    def get(self, label: str, path: str, query: dict | None = None,
            show: bool = True, maxdepth: int = 4):
        url = self.host + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", "Bearer " + self.bearer)
        req.add_header("Accept", "application/json")

        for attempt in range(4):
            try:
                with urllib.request.urlopen(req) as resp:
                    status, raw = resp.status, resp.read()
                    retry_after = None
                break
            except urllib.error.HTTPError as exc:
                status, raw = exc.code, exc.read()
                retry_after = exc.headers.get("Retry-After")
            except Exception as exc:  # network-level
                print(f"  {label}: request failed ({type(exc).__name__})")
                self.results.append((label, -1))
                return None, None
            if status != 429:
                break
            wait = float(retry_after or 5) * (attempt + 1)
            print(f"  {label}: 429, backing off {wait:.0f}s")
            time.sleep(wait)

        try:
            body = json.loads(raw)
        except Exception:
            body = None

        self.results.append((label, status))
        print(f"\n--- {label}  [{status}]  {len(raw)} bytes")
        if body is None:
            # An empty body on a 404 means the route does not exist at all; a
            # JSON error body means the route exists and the resource does not.
            print("    (no JSON body)")
        elif status >= 400:
            err = body.get("error", {}) if isinstance(body, dict) else {}
            print(f"    error.code = {err.get('code')}")
            if err.get("code") == "InvalidApiVersion":
                # The message enumerates every api-version the provider accepts.
                msg = err.get("message", "")
                print(f"    {msg[:400]}")
        elif show:
            print("    " + json.dumps(shape(body, maxdepth=maxdepth),
                                      indent=1).replace("\n", "\n    ")[:4000])
        if self.pause:
            time.sleep(self.pause)
        return status, body

    def env_filter(self, environment_id: str) -> str:
        return f"environment eq '{environment_id}'"


def report_fields(label: str, items: list, provider_fields: list[str]) -> None:
    """Print provider-modelled vs service-returned field sets."""
    if not items:
        print(f"    {label}: 0 items - field comparison not possible")
        return
    seen: dict[str, int] = {}
    for item in items:
        for key in item.get("properties", {}):
            seen[key] = seen.get(key, 0) + 1
    n = len(items)
    print(f"    {label}: {n} items")
    extra = sorted(k for k in seen if k not in provider_fields)
    missing = sorted(k for k in provider_fields if k not in seen)
    print(f"    fields the service returns that the provider does not model: {extra}")
    print(f"    provider-modelled fields absent from the response: {missing}")
    partial = sorted(k for k, c in seen.items() if c < n)
    print(f"    fields present on only some items (genuinely optional): {partial}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--environment", default=os.environ.get("PA_ENVIRONMENT_ID"),
                    help="environment id (GUID) to probe; also PA_ENVIRONMENT_ID")
    ap.add_argument("--connector", default=os.environ.get("PA_CONNECTOR",
                                                          "shared_sharepointonline"),
                    help="connector name for the single-connector read")
    ap.add_argument("--host", default=os.environ.get("PA_HOST", DEFAULT_HOST))
    ap.add_argument("--discover-environment", action="store_true",
                    help="use the first environment the token can list")
    ap.add_argument("--all-environments", action="store_true",
                    help="list apps for every visible environment (counts only)")
    ap.add_argument("--pause", type=float, default=1.0,
                    help="seconds between calls (be kind to the service)")
    args = ap.parse_args()

    probe = Probe(args.host, token(), pause=args.pause)

    print("=" * 72)
    print("Environments")
    print("=" * 72)
    status, envs = probe.get("environments_list", "/providers/Microsoft.PowerApps/environments",
                             {"api-version": CORE_API_VERSION})
    visible = [e["name"] for e in (envs or {}).get("value", [])]

    env_id = args.environment
    if args.discover_environment and visible:
        env_id = visible[0]
    if not env_id:
        print("\nNo environment id. Pass --environment or --discover-environment.")
        return 2

    probe.get("environments_list$expand=permissions",
              "/providers/Microsoft.PowerApps/environments",
              {"api-version": CORE_API_VERSION, "$expand": "permissions"},
              maxdepth=2)
    probe.get("environments_get", f"/providers/Microsoft.PowerApps/environments/{env_id}",
              {"api-version": CORE_API_VERSION})
    # '~Default' is a server-side alias for the tenant default environment.
    probe.get("environments_get(~Default)",
              "/providers/Microsoft.PowerApps/environments/~Default",
              {"api-version": CORE_API_VERSION}, show=False)

    print()
    print("=" * 72)
    print("Apps")
    print("=" * 72)
    apps_path = f"/providers/Microsoft.PowerApps/scopes/admin/environments/{env_id}/apps"
    status, apps = probe.get("apps_listByEnvironment", apps_path,
                             {"api-version": APPS_API_VERSION})
    if apps is not None:
        report_fields("apps (admin scope)", apps.get("value", []), PROVIDER_APP_FIELDS)

    status, mine = probe.get("apps_list", "/providers/Microsoft.PowerApps/apps",
                             {"api-version": CORE_API_VERSION})
    if mine is not None:
        report_fields("apps (caller scope)", mine.get("value", []), PROVIDER_APP_FIELDS)

    # The service documents its own $filter/$expand grammar in this 400.
    probe.get("apps_list(illegal $filter)", "/providers/Microsoft.PowerApps/apps",
              {"api-version": CORE_API_VERSION, "$filter": "classification eq 'SharedWithMe'"})
    # An omitted api-version enumerates every version the provider accepts.
    probe.get("apps_listByEnvironment(no api-version)", apps_path)

    if args.all_environments:
        print("\n    app counts per environment (ids not printed):")
        for i, name in enumerate(visible):
            s, body = probe.get(f"apps[{i}]",
                                f"/providers/Microsoft.PowerApps/scopes/admin/environments/{name}/apps",
                                {"api-version": APPS_API_VERSION}, show=False)
            count = len(body.get("value", [])) if isinstance(body, dict) else "?"
            print(f"      env[{i}]: {s} {count} apps")

    print()
    print("=" * 72)
    print("Connectors")
    print("=" * 72)
    apis_path = "/providers/Microsoft.PowerApps/apis"
    base = {"api-version": CONNECTORS_API_VERSION, "$filter": probe.env_filter(env_id)}
    flags = {"showApisWithToS": "true", "hideDlpExemptApis": "true",
             "showAllDlpEnforceableApis": "true"}

    status, full = probe.get("connectors_list", apis_path, {**base, **flags}, maxdepth=3)
    if full is not None:
        report_fields("connectors", full.get("value", []), PROVIDER_CONNECTOR_FIELDS)

    # Each flag changes the result set; measure by how much.
    baseline = set()
    if full:
        baseline = {c["name"] for c in full["value"]}
    for drop in ("showApisWithToS", "hideDlpExemptApis", "showAllDlpEnforceableApis"):
        q = {**base, **{k: v for k, v in flags.items() if k != drop}}
        s, body = probe.get(f"connectors_list(no {drop})", apis_path, q, show=False)
        if isinstance(body, dict) and baseline:
            names = {c["name"] for c in body["value"]}
            print(f"    dropping {drop}: {len(names)} connectors "
                  f"({len(baseline - names)} only with it, {len(names - baseline)} only without)")

    probe.get("connectors_list(no $filter)", apis_path, {"api-version": CONNECTORS_API_VERSION})
    probe.get("connectors_list(~Default)", apis_path,
              {**flags, "api-version": CONNECTORS_API_VERSION,
               "$filter": "environment eq '~Default'"}, show=False)

    status, one = probe.get("connectors_get", f"{apis_path}/{args.connector}",
                            base, maxdepth=1)
    if isinstance(one, dict) and "properties" in one:
        props = set(one["properties"])
        listed = set()
        for c in (full or {}).get("value", []):
            if c["name"] == args.connector:
                listed = set(c["properties"])
        print(f"    single-read adds over the list item: {sorted(props - listed)}")
        sw = one["properties"].get("swagger")
        if isinstance(sw, dict):
            print(f"    swagger: OpenAPI {sw.get('swagger')} document, "
                  f"{len(sw.get('paths', {}))} paths, "
                  f"{len(sw.get('definitions', {}))} definitions")

    probe.get("connectors_get(unknown)", f"{apis_path}/shared_thisdoesnotexist", base)
    probe.get("connectors_listConnections", f"{apis_path}/{args.connector}/connections",
              {"api-version": CORE_API_VERSION, "$filter": probe.env_filter(env_id)})

    print()
    print("=" * 72)
    print("Connections and gateways")
    print("=" * 72)
    probe.get("connections_listByEnvironment",
              f"/providers/Microsoft.PowerApps/scopes/admin/environments/{env_id}/connections",
              {"api-version": CORE_API_VERSION})
    probe.get("connections_list", "/providers/Microsoft.PowerApps/connections",
              {"api-version": CORE_API_VERSION, "$filter": probe.env_filter(env_id)})
    probe.get("gateways_list", "/providers/Microsoft.PowerApps/gateways",
              {"api-version": CORE_API_VERSION})

    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    for label, status in probe.results:
        print(f"  {status:>4}  {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
