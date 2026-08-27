#!/usr/bin/env python3
"""Live probe of the Copilot Studio bot-management API.

Read-only by design. Every request this script makes is a GET; there is no code
path that writes. The only mutating operation in the spec
(`appInsightsConfiguration_update`) is a PUT against a real, user-owned bot, and
a probe harness has no business performing it.

What it does, in order:

  1. resolves the environment's PowerVirtualAgents runtime endpoint from BAPI
     (`properties.runtimeEndpoints["microsoft.PowerVirtualAgents"]`) - the host
     is opaque and per-environment, so it must be looked up, not composed;
  2. enumerates bots through the environment's Dataverse Web API, because the
     bot-management API has no list endpoint and a `botId` is just the primary
     key of a row in Dataverse's `bot` table;
  3. reads each bot's Application Insights configuration and prints the *shape*
     of the response - key names and JSON types, never values;
  4. runs a set of negative reads (no token, wrong tenant header, unknown bot,
     unknown environment, wrong api-version segment, parent collection paths) to
     pin the real status codes and the error envelope.

Nothing tenant-specific is hardcoded. Ids come from arguments or the
environment, and output is deliberately shape-only so a transcript can be pasted
into a public issue.

Usage:

    probe.py --environment-id <guid> [--tenant-id <guid>] [--bot-id <guid>]
    probe.py --discover                # sweep every environment for bots

    PROBE_ENVIRONMENT_ID / PROBE_TENANT_ID / PROBE_BOT_ID are read as defaults.

Auth is the logged-in Azure CLI session:

    az login
    az account get-access-token --scope 96ff4394-9197-43aa-b393-6a41652e21f8/.default

Note that a token is not enough. This is a maker surface gated on a per-user
Copilot Studio licence: an account without one is refused 403 `UserHasNoLicense`
no matter how much Power Platform admin rights it holds, and the licence check
runs before the tenant header, the environment id or the bot id are looked at.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

COPILOT_SCOPE = "96ff4394-9197-43aa-b393-6a41652e21f8/.default"
BAPI = "https://api.bap.microsoft.com"
BAPI_SCOPE = "https://service.powerapps.com/.default"
BAPI_API_VERSION = "2023-06-01"
BOTMANAGEMENT_PREFIX = "/api/botmanagement/2022-01-15"
NIL_GUID = "00000000-0000-0000-0000-000000000000"
PAUSE = 0.7  # be a polite neighbour on a shared service

_token_cache: dict[str, str] = {}


def token(scope: str) -> str:
    if scope not in _token_cache:
        result = subprocess.run(
            ["az", "account", "get-access-token", "--scope", scope,
             "--query", "accessToken", "-o", "tsv"],
            capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"could not get a token for {scope}: {result.stderr.strip()}")
        _token_cache[scope] = result.stdout.strip()
    return _token_cache[scope]


def get(url: str, bearer: str | None = None, headers: dict | None = None):
    """GET. Returns (status, parsed-body-or-text). Never raises on HTTP errors."""
    h = {"Accept": "application/json"}
    if bearer:
        h["Authorization"] = "Bearer " + bearer
    if headers:
        h.update(headers)
    request = urllib.request.Request(url, headers=h, method="GET")
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode()
            status = response.status
    except urllib.error.HTTPError as error:
        raw = error.read().decode()
        status = error.code
    except urllib.error.URLError as error:
        return 0, f"<transport error: {error.reason}>"
    try:
        return status, json.loads(raw) if raw.strip() else None
    except json.JSONDecodeError:
        return status, raw


def shape(value, depth: int = 0):
    """Describe a JSON value structurally. Never returns any value the service sent."""
    if isinstance(value, dict):
        if depth > 3:
            return "{...}"
        return {k: shape(v, depth + 1) for k, v in sorted(value.items())}
    if isinstance(value, list):
        if not value:
            return ["<empty>"]
        return [shape(value[0], depth + 1), f"<+{len(value) - 1} more>"] if len(value) > 1 \
            else [shape(value[0], depth + 1)]
    if value is None:
        return "null"
    return type(value).__name__


def safe_error(body):
    """Error envelopes carry no tenant data, so codes and messages can be shown."""
    if isinstance(body, dict) and "ErrorCode" in body:
        detail = body.get("Error") or {}
        return f"ErrorCode={body.get('ErrorCode')} Code={detail.get('Code')!r} " \
               f"Message={detail.get('Message')!r}"
    if body is None:
        return "<empty body>"
    return f"<{type(body).__name__} body, {len(json.dumps(body)) if not isinstance(body, str) else len(body)} bytes>"


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #

def environments():
    status, body = get(
        f"{BAPI}/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments"
        f"?api-version={BAPI_API_VERSION}&$expand=properties",
        token(BAPI_SCOPE))
    if status != 200:
        sys.exit(f"BAPI environment list failed: {status}")
    return body.get("value", [])


def environment(environment_id: str):
    status, body = get(
        f"{BAPI}/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/"
        f"{environment_id}?api-version={BAPI_API_VERSION}&$expand=properties",
        token(BAPI_SCOPE))
    if status != 200:
        sys.exit(f"BAPI environment read failed: {status}")
    return body


def endpoints(env: dict):
    """(pva host, dataverse host) for an environment, either possibly None."""
    props = env.get("properties", {})
    pva = (props.get("runtimeEndpoints") or {}).get("microsoft.PowerVirtualAgents")
    dataverse = ((props.get("linkedEnvironmentMetadata") or {}).get("instanceUrl"))
    return (urllib.parse.urlparse(pva).netloc if pva else None,
            urllib.parse.urlparse(dataverse).netloc if dataverse else None)


def bots(dataverse_host: str):
    """Bot ids in an environment. The bot-management API has no list endpoint;
    bots are rows in the Dataverse `bot` table (entity set `bots`)."""
    status, body = get(
        f"https://{dataverse_host}/api/data/v9.2/bots?$select=botid,name&$top=50",
        token(f"https://{dataverse_host}/.default"))
    if status != 200:
        return status, []
    return status, [row["botid"] for row in body.get("value", [])]


# --------------------------------------------------------------------------- #
# probes
# --------------------------------------------------------------------------- #

def config_url(host: str, environment_id: str, bot_id: str) -> str:
    return (f"https://{host}{BOTMANAGEMENT_PREFIX}/environments/{environment_id}"
            f"/bots/{bot_id}/applicationinsightsconfiguration")


def read_configuration(host: str, tenant_id: str, environment_id: str, bot_id: str):
    print("\n== appInsightsConfiguration_get ==")
    status, body = get(config_url(host, environment_id, bot_id),
                       token(COPILOT_SCOPE), {"x-cci-tenantid": tenant_id})
    print(f"  status {status}")
    if status == 200:
        print("  response shape:")
        print("   " + json.dumps(shape(body), indent=1).replace("\n", "\n   "))
    else:
        print(f"  {safe_error(body)}")
        if status == 403:
            print("  -> the account holds no Copilot Studio licence; the 200 body cannot be "
                  "captured from this session")
    time.sleep(PAUSE)
    return status


def negative_probes(host: str, tenant_id: str, environment_id: str, bot_id: str):
    """Read-only probes that pin status codes and the error envelope."""
    print("\n== negative probes (all GET) ==")
    url = config_url(host, environment_id, bot_id)
    cases = [
        ("no bearer token", url, {"x-cci-tenantid": tenant_id}, None),
        ("no x-cci-tenantid header", url, {}, COPILOT_SCOPE),
        ("wrong x-cci-tenantid", url, {"x-cci-tenantid": NIL_GUID}, COPILOT_SCOPE),
        ("unknown botId", config_url(host, environment_id, NIL_GUID),
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("malformed botId", config_url(host, environment_id, "not-a-guid"),
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("unknown environmentId", config_url(host, NIL_GUID, bot_id),
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("api-version as query parameter", url + "?api-version=2022-01-15",
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("different api-version path segment",
         config_url(host, environment_id, bot_id).replace("2022-01-15", "2021-01-15"),
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("parent bots collection",
         f"https://{host}{BOTMANAGEMENT_PREFIX}/environments/{environment_id}/bots",
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
        ("single bot resource",
         f"https://{host}{BOTMANAGEMENT_PREFIX}/environments/{environment_id}/bots/{bot_id}",
         {"x-cci-tenantid": tenant_id}, COPILOT_SCOPE),
    ]
    for label, target, headers, scope in cases:
        status, body = get(target, token(scope) if scope else None, headers)
        print(f"  {label:38} {status}  {safe_error(body)}")
        time.sleep(PAUSE)


def discover():
    """Sweep every environment for bots, so a probe run can find something to read."""
    print("== discovery ==")
    print("  environments are numbered, not named: ids and display names are tenant data")
    found = []
    for index, env in enumerate(environments()):
        pva, dataverse = endpoints(env)
        if not dataverse:
            print(f"  env #{index:<3} no Dataverse - bots cannot exist here")
            continue
        status, ids = bots(dataverse)
        print(f"  env #{index:<3} dataverse={status}  pva_host={'yes' if pva else 'no'}  "
              f"bots={len(ids)}")
        for bot_id in ids:
            found.append((env["name"], pva, bot_id))
        time.sleep(PAUSE)
    print(f"\n  {len(found)} bot(s) across the tenant")
    if found:
        print("  re-run with --environment-id/--bot-id for one of them "
              "(ids withheld from this output on purpose)")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--environment-id", default=os.environ.get("PROBE_ENVIRONMENT_ID"))
    parser.add_argument("--tenant-id", default=os.environ.get("PROBE_TENANT_ID"))
    parser.add_argument("--bot-id", default=os.environ.get("PROBE_BOT_ID"))
    parser.add_argument("--discover", action="store_true",
                        help="list bots in every environment and exit")
    args = parser.parse_args()

    if args.discover:
        discover()
        return

    if not args.environment_id:
        parser.error("--environment-id is required (or run --discover first)")

    env = environment(args.environment_id)
    pva_host, dataverse_host = endpoints(env)
    print("== host resolution ==")
    print(f"  runtimeEndpoints['microsoft.PowerVirtualAgents'] -> "
          f"{'resolved' if pva_host else 'ABSENT'}")
    if not pva_host:
        sys.exit("environment exposes no PowerVirtualAgents runtime endpoint")
    # The scale-unit segment is the only non-constant part and is not tenant data.
    print(f"  host pattern: {pva_host.split('.')[0]}.<scale-unit>."
          f"{'.'.join(pva_host.split('.')[2:])}")

    tenant_id = args.tenant_id or env.get("properties", {}).get("tenantId")
    if not tenant_id:
        sys.exit("--tenant-id not given and BAPI did not report one")

    bot_id = args.bot_id
    if not bot_id:
        if not dataverse_host:
            sys.exit("environment has no Dataverse, so it has no bots; pass --bot-id or "
                     "pick another environment")
        status, ids = bots(dataverse_host)
        print(f"\n== bot discovery via Dataverse ==\n  GET /api/data/v9.2/bots -> {status}, "
              f"{len(ids)} bot(s)")
        if not ids:
            sys.exit("no bots in this environment; nothing to read")
        bot_id = ids[0]

    read_configuration(pva_host, tenant_id, args.environment_id, bot_id)
    negative_probes(pva_host, tenant_id, args.environment_id, bot_id)


if __name__ == "__main__":
    main()
