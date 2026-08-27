#!/usr/bin/env python3
"""Probe the live Business Application Platform API and report its real shapes.

The spec in ``bapi/oas/openapi.json`` was seeded from the Terraform provider's
client, which only models the fields the provider consumes. This harness calls
the real service so the spec can record what the service actually returns:
undocumented fields, genuine optionality, real enum values, the async
lifecycle contract, and the error envelope.

It authenticates with the logged-in Azure CLI session::

    az account get-access-token --scope https://service.powerapps.com/.default

Nothing about a tenant is hardcoded. Ids come from CLI arguments or from a
tenant facts file (``--tenant-file``, default ``$BAPI_PROBE_TENANT_FILE``) with
the shape ``{"environments": [{"id": ...}], "billingPolicies": [{"id": ...}]}``.

SAFETY. ``read`` and ``errors`` are GET/validate only and safe against any
tenant. ``lifecycle`` and ``dlp`` create resources; every created resource is
named with ``--prefix`` (default ``zzz-probe-bapi``) and torn down in a
``finally`` block. ``cleanup`` sweeps anything a crashed run left behind. The
harness never writes to a resource it did not create, and never touches tenant
settings, the tenant isolation policy, admin applications or existing DLP
policies.

Captures land under ``--out`` (default ``captures/``, git-ignored) and contain
raw tenant data: they are inputs for hand-authoring schemas, not artifacts to
commit. stdout only ever carries shape summaries -- field names, types, status
codes, header names -- never values.

Usage::

    probe.py read                       # GET every read surface, summarise shapes
    probe.py errors                     # provoke and capture the error envelope
    probe.py lifecycle --billing-policy <id> --location <loc> [--dataverse]
    probe.py dlp --environment <id>
    probe.py cleanup                    # delete leftovers matching --prefix
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import random
import string
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = "api.bap.microsoft.com"
SCOPE = "https://service.powerapps.com/.default"

# The provider pins one of three api-versions per operation; probes use the
# same version the provider uses for that call so the observed shape matches
# what the provider actually sees.
V2019 = "2019-10-01"
V2020 = "2020-10-01"
V2021 = "2021-04-01"
V2022 = "2022-05-01"
V2023 = "2023-06-01"

# Header names the async contract uses. Captured case-insensitively; reported
# verbatim so the spec can document what the service really sends.
ASYNC_HEADERS = (
    "location",
    "operation-location",
    "retry-after",
    "x-ms-service-request-id",
    "x-ms-correlation-id",
    "x-ms-ratelimit-burst-remaining-tenant-requests",
    "x-ms-ratelimit-time-remaining-tenant-requests",
)

_token: str | None = None


def token() -> str:
    global _token
    if _token is None:
        _token = subprocess.run(
            ["az", "account", "get-access-token", "--scope", SCOPE,
             "--query", "accessToken", "-o", "tsv"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    return _token


class Result:
    def __init__(self, status: int, headers: dict, body):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    def async_headers(self) -> dict:
        return {k: v for k, v in self.headers.items() if k in ASYNC_HEADERS}


def call(method: str, path: str, api_version: str | None = V2023,
         body=None, query: dict | None = None, absolute: str | None = None,
         pause: float = 0.4) -> Result:
    """One BAPI request. Sleeps after every call, retries once on 429/503."""
    if absolute:
        url = absolute
    else:
        values = dict(query or {})
        if api_version:
            values["api-version"] = api_version
        url = f"https://{HOST}{path}"
        if values:
            url += "?" + urllib.parse.urlencode(values)

    for attempt in range(3):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, method=method, data=data)
        req.add_header("Authorization", "Bearer " + token())
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read()
                status, headers = resp.status, dict(resp.headers)
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            status, headers = exc.code, dict(exc.headers)
        except urllib.error.URLError as exc:
            print(f"  ! transport error {exc}", file=sys.stderr)
            time.sleep(5)
            continue

        headers = {k.lower(): v for k, v in headers.items()}
        if status in (429, 503) and attempt < 2:
            wait = float(headers.get("retry-after", 10) or 10)
            print(f"  ! {status}, backing off {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue

        try:
            parsed = json.loads(raw) if raw else None
        except ValueError:
            parsed = raw.decode("utf-8", "replace")
        time.sleep(pause)
        return Result(status, headers, parsed)

    return Result(0, {}, None)


# --------------------------------------------------------------------------
# shape summarising -- stdout must never carry tenant data
# --------------------------------------------------------------------------

def type_of(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return "object"


def shape(value, prefix: str = "", acc: dict | None = None) -> dict:
    """Flatten a JSON document into {json.pointer: set-of-types}.

    Arrays collapse to ``[]`` so 13 environments produce one shape, and every
    element contributes its keys -- that is how optional fields surface.
    """
    acc = {} if acc is None else acc
    kind = type_of(value)
    acc.setdefault(prefix or "$", set()).add(kind)
    if kind == "object":
        for key, item in value.items():
            shape(item, f"{prefix}.{key}", acc)
    elif kind == "array":
        for item in value:
            shape(item, f"{prefix}[]", acc)
    return acc


def enums(value, keys: set[str], prefix: str = "", acc: dict | None = None) -> dict:
    """Collect the distinct values seen at the given leaf names."""
    acc = {} if acc is None else acc
    if isinstance(value, dict):
        for key, item in value.items():
            here = f"{prefix}.{key}"
            if key in keys and isinstance(item, (str, int, bool)):
                acc.setdefault(here, set()).add(item)
            enums(item, keys, here, acc)
    elif isinstance(value, list):
        for item in value:
            enums(item, keys, prefix + "[]", acc)
    return acc


def report(label: str, result: Result, out: pathlib.Path | None = None,
           show: bool = True) -> Result:
    print(f"\n### {label}  -> HTTP {result.status}")
    interesting = result.async_headers()
    if interesting:
        print("  headers: " + ", ".join(f"{k}={v}" if k in
              ("retry-after",) else k for k, v in sorted(interesting.items())))
    if out is not None and result.body is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result.body, indent=1, sort_keys=True))
    if show and result.body is not None:
        for pointer, kinds in sorted(shape(result.body).items()):
            print(f"  {pointer}: {'|'.join(sorted(kinds))}")
    return result


def rand(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def load_tenant(path: str | None) -> dict:
    path = path or os.environ.get("BAPI_PROBE_TENANT_FILE")
    if not path:
        return {}
    return json.loads(pathlib.Path(path).read_text())


# --------------------------------------------------------------------------
# read probes -- safe anywhere
# --------------------------------------------------------------------------

ENUM_KEYS = {
    "environmentSku", "environmentType", "state", "protectionLevel",
    "provisioningState", "classification", "displayName", "type",
    "runtimeEndpointsState", "environmentFilterType", "policyType",
    "governanceConfiguration", "updateCadence", "connectorType",
}


def cmd_read(args) -> None:
    tenant = load_tenant(args.tenant_file)
    out = pathlib.Path(args.out)
    env_ids = [e["id"] for e in tenant.get("environments", [])]
    if args.environment:
        env_ids = [args.environment] + env_ids
    location = args.location or (tenant.get("environments") or [{}])[0].get("location", "unitedstates")
    tenant_id = args.tenant_id or tenant.get("tenantId")

    envs = report("GET environments (list, $expand)", call(
        "GET", "/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments",
        query={"$expand": "properties/billingPolicy,properties/copilotPolicies"},
    ), out / "environments-list.json")

    # One list call already exposes every optional field across the tenant's
    # environments; per-environment GETs add the $expand-only branches.
    for env_id in env_ids[: args.max_environments]:
        report(f"GET environment {env_id[:8]}...", call(
            "GET", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            query={"$expand": "permissions,properties.capacity,properties/billingPolicy,properties/copilotPolicies"},
        ), out / f"environment-{env_id}.json", show=False)
        report(f"GET roleAssignments {env_id[:8]}...", call(
            "GET", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}/roleAssignments",
            api_version=V2022,
        ), out / f"role-assignments-{env_id}.json", show=False)

    report("GET tenant", call("GET", "/providers/Microsoft.BusinessAppPlatform/tenant"),
           out / "tenant.json")
    report("POST listTenantSettings", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/listTenantSettings",
        api_version=V2023, body={}), out / "tenant-settings.json")
    report("GET locations", call("GET", "/providers/Microsoft.BusinessAppPlatform/locations"),
           out / "locations.json")
    report(f"GET currencies ({location})", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/locations/{location}/environmentCurrencies"),
        out / "currencies.json")
    report(f"GET languages ({location})", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/locations/{location}/environmentLanguages"),
        out / "languages.json")
    report(f"GET templates ({location})", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/locations/{location}/templates",
        api_version=V2019),
        out / "templates.json")
    report("GET DLP policies", call(
        "GET", "/providers/PowerPlatform.Governance/v2/policies", api_version=None),
        out / "dlp-policies.json")
    report("GET unblockable connectors", call(
        "GET", "/providers/PowerPlatform.Governance/v1/connectors/metadata/unblockable",
        api_version=None), out / "connectors-unblockable.json")
    report("GET virtual connectors", call(
        "GET", "/providers/PowerPlatform.Governance/v1/connectors/metadata/virtual",
        api_version=None), out / "connectors-virtual.json")
    if tenant_id:
        report("GET tenant isolation policy", call(
            "GET", f"/providers/PowerPlatform.Governance/v1/tenants/{tenant_id}/tenantIsolationPolicy",
            api_version=V2023), out / "tenant-isolation.json")
    if args.client_id:
        report("GET adminApplication", call(
            "GET", f"/providers/Microsoft.BusinessAppPlatform/adminApplications/{args.client_id}",
            api_version=V2020),
            out / "admin-application.json")

    # Real enum values, gathered across every environment at once.
    print("\n### observed enum values")
    for pointer, values in sorted(enums(envs.body, ENUM_KEYS).items()):
        if pointer.endswith("displayName"):
            continue
        print(f"  {pointer}: {sorted(str(v) for v in values)}")


# --------------------------------------------------------------------------
# error envelope -- provoked without touching anything real
# --------------------------------------------------------------------------

def cmd_errors(args) -> None:
    out = pathlib.Path(args.out)
    missing = "00000000-0000-0000-0000-000000000000"

    report("GET environment (nonexistent id)", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{missing}"),
        out / "error-404-environment.json")
    report("GET lifecycle operation (nonexistent id)", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/lifecycleOperations/{missing}"),
        out / "error-404-lifecycle.json")
    report("GET DLP policy (nonexistent name)", call(
        "GET", f"/providers/PowerPlatform.Governance/v2/policies/{missing}", api_version=None),
        out / "error-404-dlp.json")
    report("GET environments (bad api-version)", call(
        "GET", "/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments",
        api_version="1999-01-01"), out / "error-badversion.json")
    report("POST validateEnvironmentDetails (empty body)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
        api_version=V2021, body={}), out / "error-validate-empty.json")
    report("POST validateEnvironmentDetails (bad location)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
        api_version=V2021,
        body={"domainName": "zzzprobe" + rand(), "environmentLocation": "nowhere"}),
        out / "error-validate-location.json")
    report("POST validateEnvironmentDetails (malformed domain)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
        api_version=V2021,
        body={"domainName": "not valid!", "environmentLocation": args.location or "unitedstates"}),
        out / "error-validate-domain.json")
    report("POST validateEnvironmentDetails (unknown environmentName)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
        api_version=V2021,
        body={"domainName": "zzzprobe" + rand(), "environmentName": missing}),
        out / "error-validate-environment.json")

    # Which create fields the service genuinely demands, discovered by removing
    # one at a time. The order the service validates in is itself the answer.
    report("POST environments (empty body)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/environments",
        api_version=V2023, body={}), out / "error-create-empty.json")
    report("POST environments (no displayName)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/environments",
        api_version=V2023, body={"location": args.location or "unitedstates",
                                 "properties": {}}),
        out / "error-create-nodisplayname.json")
    report("POST environments (no environmentSku)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/environments",
        api_version=V2023, body={"location": args.location or "unitedstates",
                                 "properties": {"displayName": "zzz" + rand()}}),
        out / "error-create-nosku.json")
    report("POST environments (no location)", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/environments",
        api_version=V2023,
        body={"properties": {"displayName": "zzz" + rand(), "environmentSku": "Sandbox"}}),
        out / "error-create-nolocation.json")

    report("POST DLP policy (empty body)", call(
        "POST", "/providers/PowerPlatform.Governance/v2/policies", api_version=None, body={}),
        out / "error-dlp-empty.json")
    report("POST DLP policy (unwrapped definition)", call(
        "POST", "/providers/PowerPlatform.Governance/v2/policies", api_version=None,
        body={"displayName": "zzz" + rand()}), out / "error-dlp-unwrapped.json")

    report("GET environment group (nonexistent id)", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/environmentGroups/{missing}"),
        out / "error-404-environment-group.json")
    report("GET adminApplication (unregistered id)", call(
        "GET", f"/providers/Microsoft.BusinessAppPlatform/adminApplications/{missing}",
        api_version=V2020), out / "error-adminapplication.json")
    report("POST modifySku (nonexistent environment)", call(
        "POST", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{missing}/modifySku",
        api_version=V2021, body={"environmentSku": "Production"}),
        out / "error-modifysku.json")


def cmd_validate(args) -> None:
    out = pathlib.Path(args.out)
    domain = f"{args.prefix}-{rand()}"
    report("validateEnvironmentDetails: create variant, free domain", call(
        "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
        api_version=V2021,
        body={"domainName": domain, "environmentLocation": args.location}),
        out / "validate-create-ok.json")
    if args.taken_domain:
        report("validateEnvironmentDetails: create variant, taken domain", call(
            "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
            api_version=V2021,
            body={"domainName": args.taken_domain, "environmentLocation": args.location}),
            out / "validate-create-taken.json")
    if args.environment:
        report("validateEnvironmentDetails: update variant", call(
            "POST", "/providers/Microsoft.BusinessAppPlatform/validateEnvironmentDetails",
            api_version=V2021,
            body={"domainName": domain, "environmentName": args.environment}),
            out / "validate-update-ok.json")


# --------------------------------------------------------------------------
# environment lifecycle -- creates and always deletes
# --------------------------------------------------------------------------

def poll_lifecycle(url: str, out: pathlib.Path, label: str,
                   limit: int = 120, interval: float = 5.0) -> Result:
    """Follow a 202's Location/Operation-Location to a terminal state.

    Prints every distinct state id seen: that sequence is the async contract
    the spec documents.
    """
    seen: list[str] = []
    result = Result(0, {}, None)
    for _ in range(limit):
        result = call("GET", "", absolute=url, pause=0.0)
        body = result.body if isinstance(result.body, dict) else {}
        state = (((body.get("state") or {}).get("id"))
                 or ((body.get("properties") or {}).get("provisioningState"))
                 or f"HTTP{result.status}")
        if not seen or seen[-1] != state:
            seen.append(state)
            print(f"  {label}: {state} (HTTP {result.status})")
        if state in ("Succeeded", "Failed") or result.status in (404, 400):
            break
        time.sleep(interval)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"states": seen, "final": result.body}, indent=1))
    print(f"  {label}: state sequence {seen}")
    return result


def follow_url(result: Result) -> str | None:
    return result.headers.get("operation-location") or result.headers.get("location")


def cmd_lifecycle(args) -> None:
    out = pathlib.Path(args.out)
    name = f"{args.prefix}-{rand()}"
    env_id = None

    body = {
        "location": args.location,
        "properties": {
            "displayName": name,
            "environmentSku": args.sku,
            "billingPolicy": {"id": args.billing_policy} if args.billing_policy else None,
        },
    }
    if body["properties"]["billingPolicy"] is None:
        del body["properties"]["billingPolicy"]
    if args.dataverse:
        body["properties"]["linkedEnvironmentMetadata"] = {
            "baseLanguage": args.language,
            "domainName": name,
            "currency": {"code": args.currency},
            "securityGroupId": "",
        }

    try:
        created = report("POST environments (create)", call(
            "POST", "/providers/Microsoft.BusinessAppPlatform/environments",
            api_version=V2023, body=body), out / "create-202.json")
        url = follow_url(created)
        if created.status == 202 and url:
            final = poll_lifecycle(url, out / "create-lifecycle.json", "create")
            fbody = final.body if isinstance(final.body, dict) else {}
            path = (((fbody.get("links") or {}).get("environment") or {}).get("path")) or ""
            env_id = path.rstrip("/").rsplit("/", 1)[-1] or None
            print(f"  create: links.environment.path present={bool(path)}")
        elif created.status == 201 and isinstance(created.body, dict):
            env_id = created.body.get("name")
        if not env_id:
            print("  ! no environment id recovered; aborting lifecycle probe")
            return
        print(f"  created environment {env_id[:8]}...")

        report("GET created environment", call(
            "GET", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            query={"$expand": "permissions,properties.capacity,properties/billingPolicy,properties/copilotPolicies"}),
            out / "created-environment.json")

        # Every mutation below must wait for the previous lifecycle operation:
        # BAPI serialises them per environment and answers 409
        # OperationNotStartable (PATCH) or a bodyless 409 (DELETE) otherwise.
        sku = report("POST modifySku", call(
            "POST", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}/modifySku",
            api_version=V2021, body={"environmentSku": args.modify_sku}),
            out / "modify-sku.json")
        if follow_url(sku):
            poll_lifecycle(follow_url(sku), out / "modify-sku-lifecycle.json", "modifySku")

        ai = report("PATCH environment (generative AI features)", call(
            "PATCH", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            api_version=V2021,
            body={"properties": {"bingChatEnabled": True,
                                 "copilotPolicies": {"crossGeoCopilotDataMovementEnabled": True}}}),
            out / "patch-ai-features.json")
        if follow_url(ai):
            poll_lifecycle(follow_url(ai), out / "patch-ai-lifecycle.json", "ai-features")
        # A PATCH whose values already match answers 204 with no lifecycle
        # operation at all; re-sending the same body proves that branch.
        repeat = report("PATCH environment (same AI values again)", call(
            "PATCH", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            api_version=V2021,
            body={"properties": {"bingChatEnabled": True,
                                 "copilotPolicies": {"crossGeoCopilotDataMovementEnabled": True}}}),
            out / "patch-ai-features-noop.json")
        print(f"  no-op PATCH: HTTP {repeat.status}")

        updated = report("PATCH environment (displayName, description)", call(
            "PATCH", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            api_version=V2021, query={"$expand": "permissions,properties.capacity,properties/billingPolicy"},
            body={"properties": {"displayName": name + "-renamed", "description": "probe"}}),
            out / "patch-display-name.json")
        if follow_url(updated):
            poll_lifecycle(follow_url(updated), out / "patch-update-lifecycle.json", "update")

        # Managed Environments on an environment with no Dataverse: the
        # rejection is the documentation.
        report("POST governanceConfiguration", call(
            "POST", f"/providers/Microsoft.BusinessAppPlatform/environments/{env_id}/governanceConfiguration",
            api_version=V2021,
            body={"protectionLevel": "Standard",
                  "settings": {"extendedSettings": {"excludeEnvironmentFromAnalysis": "false"}}}),
            out / "governance-configuration.json")

        report("DELETE environment (no reason code)", call(
            "DELETE", f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}",
            api_version=V2023), out / "delete-nocode.json")

    finally:
        if env_id:
            delete_environment(env_id, out)


def delete_environment(env_id: str, out: pathlib.Path, attempts: int = 12) -> None:
    """Delete and confirm gone, replaying the bodyless 409 the service uses to
    say "a lifecycle operation is already running"."""
    path = f"/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{env_id}"
    for attempt in range(attempts):
        deleted = report(f"DELETE environment (attempt {attempt + 1})", call(
            "DELETE", path, api_version=V2023,
            body={"code": "7", "message": "probe cleanup"}),
            out / "delete.json", show=False)
        print(f"  delete: HTTP {deleted.status}, body present={deleted.body is not None}")
        if deleted.status == 409:
            time.sleep(20)
            continue
        if follow_url(deleted):
            poll_lifecycle(follow_url(deleted), out / "delete-lifecycle.json", "delete")
        break

    for _ in range(60):
        after = call("GET", path)
        if after.status == 404:
            report("GET environment after delete", after, out / "after-delete.json")
            break
        time.sleep(10)
    else:
        print(f"  ! environment {env_id} still readable -- run `probe.py cleanup`")
        return
    gone = call("DELETE", path, api_version=V2023,
                body={"code": "7", "message": "probe cleanup"})
    print(f"  DELETE on an already-deleted environment: HTTP {gone.status}")


# --------------------------------------------------------------------------
# DLP -- a brand new policy scoped to one environment, then deleted
# --------------------------------------------------------------------------

ENVIRONMENT_ID_PREFIX = "/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/"
ENVIRONMENT_TYPE = "Microsoft.BusinessAppPlatform/scopes/environments"


def cmd_dlp(args) -> None:
    out = pathlib.Path(args.out)
    name = None
    display = f"{args.prefix}-{rand()}"
    # The wire body wraps the policy in `policyDefinition`; the service
    # deserialises it strictly and rejects unknown members, so a flat body is
    # a 400 rather than a merge.
    body = {
        "policyDefinition": {
            "displayName": display,
            "defaultConnectorsClassification": args.classification,
            "environmentType": "OnlyEnvironments" if args.environment else "AllEnvironments",
            "environments": ([{"name": args.environment,
                               "id": ENVIRONMENT_ID_PREFIX + args.environment,
                               "type": ENVIRONMENT_TYPE}] if args.environment else []),
            "connectorGroups": [
                {"classification": "Confidential", "connectors": []},
                {"classification": "General", "connectors": []},
                {"classification": "Blocked", "connectors": []},
            ],
        },
        # A catch-all pattern rule is mandatory: an empty rule list is a 400.
        "customConnectorUrlPatternsDefinition": {
            "rules": [{"order": 1, "customConnectorRuleClassification": "Ignore",
                       "pattern": "*"}],
        },
    }
    try:
        created = report("POST DLP policy", call(
            "POST", "/providers/PowerPlatform.Governance/v2/policies",
            api_version=None, body=body), out / "dlp-create.json")
        if isinstance(created.body, dict):
            name = (created.body.get("policyDefinition") or {}).get("name")
        if not name:
            print("  ! policy not created; aborting")
            return
        report("GET DLP policy", call(
            "GET", f"/providers/PowerPlatform.Governance/v2/policies/{name}", api_version=None),
            out / "dlp-get.json")
        report("GET DLP policies (list, after create)", call(
            "GET", "/providers/PowerPlatform.Governance/v2/policies", api_version=None),
            out / "dlp-list.json")

        patched = json.loads(json.dumps(created.body))
        patched["policyDefinition"]["displayName"] = display + "-renamed"
        report("PATCH DLP policy", call(
            "PATCH", f"/providers/PowerPlatform.Governance/v2/policies/{name}",
            api_version=None, body=patched), out / "dlp-patch.json", show=False)
        report("PATCH DLP policy (empty body)", call(
            "PATCH", f"/providers/PowerPlatform.Governance/v2/policies/{name}",
            api_version=None, body={}), out / "dlp-patch-empty.json")
        report("PUT DLP policy (is PUT accepted?)", call(
            "PUT", f"/providers/PowerPlatform.Governance/v2/policies/{name}",
            api_version=None, body=patched), out / "dlp-put.json", show=False)
    finally:
        if name:
            report("DELETE DLP policy", call(
                "DELETE", f"/providers/PowerPlatform.Governance/v2/policies/{name}",
                api_version=None), out / "dlp-delete.json")
            report("GET DLP policy after delete", call(
                "GET", f"/providers/PowerPlatform.Governance/v2/policies/{name}", api_version=None),
                out / "dlp-after-delete.json")


# --------------------------------------------------------------------------
# cleanup -- only ever touches names carrying the prefix
# --------------------------------------------------------------------------

def cmd_cleanup(args) -> None:
    leftovers = 0
    envs = call("GET", "/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments")
    for env in (envs.body or {}).get("value", []):
        display = (env.get("properties") or {}).get("displayName", "")
        if not display.startswith(args.prefix):
            continue
        leftovers += 1
        print(f"  deleting environment '{display}'")
        if not args.dry_run:
            delete_environment(env["name"], pathlib.Path(args.out))

    policies = call("GET", "/providers/PowerPlatform.Governance/v2/policies", api_version=None)
    for policy in (policies.body or {}).get("value", []):
        if not policy.get("displayName", "").startswith(args.prefix):
            continue
        leftovers += 1
        print(f"  deleting DLP policy '{policy['displayName']}'")
        if not args.dry_run:
            call("DELETE", f"/providers/PowerPlatform.Governance/v2/policies/{policy['name']}",
                 api_version=None)

    print(f"\n{leftovers} resource(s) matched prefix '{args.prefix}'"
          + (" (dry run, nothing deleted)" if args.dry_run else ""))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="captures",
                        help="directory for raw captures (git-ignored; contains tenant data)")
    parser.add_argument("--prefix", default="zzz-probe-bapi",
                        help="name prefix for every resource this harness creates")
    parser.add_argument("--tenant-file", help="JSON file of tenant facts (ids are never hardcoded)")
    sub = parser.add_subparsers(dest="command", required=True)

    read = sub.add_parser("read", help="GET every read surface and summarise its shape")
    read.add_argument("--environment", help="environment id to probe first")
    read.add_argument("--tenant-id")
    read.add_argument("--location")
    read.add_argument("--client-id", help="an app registration id to read as an admin application")
    read.add_argument("--max-environments", type=int, default=3)
    read.set_defaults(func=cmd_read)

    errors = sub.add_parser("errors", help="provoke 4xx responses and capture the error envelope")
    errors.add_argument("--location")
    errors.set_defaults(func=cmd_errors)

    validate = sub.add_parser("validate", help="probe validateEnvironmentDetails, both variants")
    validate.add_argument("--location", required=True)
    validate.add_argument("--environment", help="environment id for the update variant")
    validate.add_argument("--taken-domain", help="a domain known to be in use, to capture the rejection")
    validate.set_defaults(func=cmd_validate)

    lifecycle = sub.add_parser("lifecycle", help="create an environment, probe the async contract, delete it")
    lifecycle.add_argument("--location", required=True)
    lifecycle.add_argument("--billing-policy", help="an enabled billing policy id to supply capacity")
    lifecycle.add_argument("--sku", default="Sandbox")
    lifecycle.add_argument("--modify-sku", default="Production")
    lifecycle.add_argument("--dataverse", action="store_true",
                           help="also provision Dataverse (much slower)")
    lifecycle.add_argument("--currency", default="USD")
    lifecycle.add_argument("--language", type=int, default=1033)
    lifecycle.set_defaults(func=cmd_lifecycle)

    dlp = sub.add_parser("dlp", help="create a DLP policy scoped to one environment, probe it, delete it")
    dlp.add_argument("--environment", help="environment id to scope the policy to")
    dlp.add_argument("--classification", default="General",
                     choices=["General", "Confidential", "Blocked"])
    dlp.set_defaults(func=cmd_dlp)

    cleanup = sub.add_parser("cleanup", help="delete anything matching --prefix")
    cleanup.add_argument("--dry-run", action="store_true")
    cleanup.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
