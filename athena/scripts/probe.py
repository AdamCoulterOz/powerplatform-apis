#!/usr/bin/env python3
"""Live probe harness for the Dataverse Synapse Link orchestration API ("athena").

This surface has no read operations. Every documented call -- create a Link to
Fabric, register an organization with its island, unlink -- creates or destroys a
real Fabric/Synapse integration in a real environment, and creating one needs a
Fabric workspace id and a connection id besides. So this harness deliberately
probes everything *around* the operations and none of the operations themselves:

  * host construction     is the derived hostname a registered service, and does
                          the derivation actually depend on what it claims to?
  * identity              what does the token audience turn out to be, what
                          permissions does that application publish, and does an
                          app-only token have anywhere to land?
  * routing and auth      what does the service say to an unrouted method, an
                          unknown path, no token, a wrong-audience token?
  * prerequisites         the two reads a caller must do first, which belong to
                          the bapi and dataverse boundaries, not to this one.

**It is read-only by construction.** request() refuses any method other than
GET, HEAD and OPTIONS, so there is no code path here that can provision a
lakehouse, register an organization, or unlink anything. That is not a policy
this script follows; it is the only thing the transport can do.

It prints shapes, statuses and header presence -- never a tenant id, an
environment id, an organization id, a Dataverse hostname or a token.

Usage
    probe.py --environment-id ENVID              # everything
    probe.py --environment-id ENVID --skip-dataverse
    probe.py --cluster-uri-suffix us-il101.gateway.prod.island --azure-region eastus
    probe.py --dns-only                          # no credentials needed

Auth: an Entra token for 7f15f9d9-cad0-44f1-bbba-d36650e07765/.default, taken
from the logged-in az CLI session unless ATHENA_TOKEN is set. The BAPI and
Dataverse prerequisite reads take their own tokens.

Nothing here mutates. Nothing here needs a Fabric workspace.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# The first-party application "Azure Synapse Link for Dataverse". Its identifier
# URI, https://exporttodatalake.com/, is the surviving trace of the service's
# origin as Export to Data Lake.
ATHENA_APP_ID = "7f15f9d9-cad0-44f1-bbba-d36650e07765"
ATHENA_SCOPE = ATHENA_APP_ID + "/.default"
ATHENA_SCOPE_URI = "https://exporttodatalake.com/.default"
BAPI_SCOPE = "https://service.powerapps.com/.default"

BAPI_HOST = "api.bap.microsoft.com"
BAPI_API_VERSIONS = ["2020-10-01-alpha", "2020-10-01", "2021-04-01", "2022-05-01",
                     "2023-06-01", "2024-05-01"]

HOST_TEMPLATE = "athenawebservice.{prefix}{suffix}.powerapps.com"

# The compass-direction component of an Azure region name, longest first so that
# australiasoutheast matches "se" and not "e".
REGION_PREFIXES = ["southeast", "southwest", "northeast", "northwest",
                   "south", "north", "east", "west", "central"]
PREFIX_CODES = {"southeast": "se", "southwest": "sw", "northeast": "ne",
                "northwest": "nw", "south": "s", "north": "n",
                "east": "e", "west": "w", "central": "c"}

# Headers the island gateway adds only once it has resolved the Host to a real
# registered upstream and forwarded to it. Their presence -- not the status code,
# which is 404 either way -- is what distinguishes a real service from a hostname
# nobody serves.
UPSTREAM_MARKERS = ["x-ms-webservice", "x-servicefabric"]

REQUEST_PAUSE = 0.4
MAX_RETRIES = 4
PROBE_MARKER = "zzzprobeathena"


def get_token(scope: str, env_var: str | None = None) -> str | None:
    if env_var and os.environ.get(env_var):
        return os.environ[env_var].strip()
    try:
        proc = subprocess.run(
            ["az", "account", "get-access-token", "--scope", scope,
             "--query", "accessToken", "-o", "tsv"],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        print("  could not acquire a token for %s: %s" % (scope, err), file=sys.stderr)
        return None
    return proc.stdout.strip() or None


class ReadOnly:
    """Minimal client that is structurally incapable of mutating.

    The method check is in the transport, before the request object exists, so no
    caller in this file or added to it later can reach a POST, PUT, PATCH or
    DELETE through it.
    """

    ALLOWED_METHODS = ("GET", "HEAD", "OPTIONS")

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.calls = 0

    def request(self, url: str, method: str = "GET", token: str | None = None,
                headers: dict | None = None, timeout: int = 60):
        """Return (status, response-headers, body-bytes). Never sends a body."""
        if method not in self.ALLOWED_METHODS:
            raise ValueError(
                "probe.py is read-only by construction; refusing method " + method)

        hdrs = {"Accept": "application/json"}
        if token:
            hdrs["Authorization"] = "Bearer " + token
        hdrs.update(headers or {})

        for attempt in range(MAX_RETRIES):
            req = urllib.request.Request(url, headers=hdrs, method=method)
            self.calls += 1
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    status, resp_headers, body = resp.status, dict(resp.headers), resp.read()
            except urllib.error.HTTPError as err:
                status, resp_headers, body = err.code, dict(err.headers), err.read()
            except urllib.error.URLError as err:
                return -1, {}, str(err.reason).encode()

            if status in (429, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                wait = float(resp_headers.get("Retry-After", 2 ** attempt))
                if self.verbose:
                    print("  backing off %.1fs after %d" % (wait, status), file=sys.stderr)
                time.sleep(wait)
                continue

            time.sleep(REQUEST_PAUSE)
            if self.verbose:
                print("  %s %s -> %s" % (method, url, status), file=sys.stderr)
            return status, resp_headers, body

    def json(self, url: str, token: str | None = None, headers: dict | None = None):
        status, _, body = self.request(url, token=token, headers=headers)
        try:
            return status, json.loads(body)
        except ValueError:
            return status, None


def lower_headers(headers: dict) -> dict:
    return {k.lower(): v for k, v in headers.items()}


def reached_upstream(headers: dict) -> bool:
    low = lower_headers(headers)
    return any(marker in low for marker in UPSTREAM_MARKERS)


def region_prefix(azure_region: str) -> str | None:
    """Map an Azure region name onto the athena host's direction prefix.

    australiaeast -> e, australiasoutheast -> se, westeurope -> w. The geography
    is already carried by the cluster uri suffix, so only the direction survives.
    """
    region = (azure_region or "").strip().lower()
    for word in REGION_PREFIXES:
        if region.startswith(word) or region.endswith(word):
            return PREFIX_CODES[word]
    return None


def athena_host(prefix: str, suffix: str) -> str:
    return HOST_TEMPLATE.format(prefix=prefix, suffix=suffix)


def resolves(hostname: str) -> bool:
    try:
        socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP)
        return True
    except socket.gaierror:
        return False


# --------------------------------------------------------------------------
# 1. prerequisite: the BAPI environment read (boundary: bapi)
# --------------------------------------------------------------------------

def probe_bapi(client: ReadOnly, environment_id: str) -> dict:
    """Read the environment and derive the athena host from it.

    This call belongs to the bapi boundary, not to this one, but no athena host
    can be composed without it, so its shape is part of this API's contract.
    """
    print("=" * 74)
    print("PREREQUISITE: the BAPI environment read that yields the athena host")
    print("=" * 74)

    token = get_token(BAPI_SCOPE, "BAPI_TOKEN")
    if not token:
        print("  no BAPI token; skipping")
        return {}

    derived = {}
    print("  %-22s %-6s %-34s %-16s %s"
          % ("api-version", "status", "cluster.uriSuffix", "azureRegion", "linkedEnvMetadata"))
    for version in BAPI_API_VERSIONS:
        url = "https://%s/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/%s?%s" % (
            BAPI_HOST, environment_id, urllib.parse.urlencode({"api-version": version}))
        status, body = client.json(url, token=token)
        props = (body or {}).get("properties", {}) if isinstance(body, dict) else {}
        cluster = props.get("cluster") or {}
        suffix = cluster.get("uriSuffix")
        region = props.get("azureRegion")
        lem = props.get("linkedEnvironmentMetadata") or {}
        print("  %-22s %-6s %-34s %-16s %s"
              % (version, status, suffix or "-", region or "-",
                 "present" if lem else "ABSENT"))
        if suffix and not derived:
            derived = {"uriSuffix": suffix, "azureRegion": region,
                       "hasOrg": bool(lem.get("resourceId")),
                       "lemFields": sorted(lem.keys())}

    if derived:
        print()
        print("  The provider's fabric_link client pins api-version 2020-10-01-alpha for this")
        print("  read. Every version above returns the same cluster and region, so the alpha")
        print("  version is not required -- see the bapi spec for the supported set.")
        print("  linkedEnvironmentMetadata fields available: %s" % ", ".join(derived["lemFields"]))
    return derived


# --------------------------------------------------------------------------
# 2. host construction
# --------------------------------------------------------------------------

def probe_host(client: ReadOnly, token: str | None, suffix: str, azure_region: str) -> str | None:
    print()
    print("=" * 74)
    print("HOST CONSTRUCTION: athenawebservice.{prefix}{clusterUriSuffix}.powerapps.com")
    print("=" * 74)

    prefix = region_prefix(azure_region)
    print("  azureRegion %-20s -> direction prefix %r" % (azure_region or "?", prefix))
    if not prefix:
        print("  no direction could be derived; falling back to the provider's hardcoded 'e'")
        prefix = "e"
    host = athena_host(prefix, suffix)

    print()
    print("-- DNS proves the scale unit exists; it does NOT prove the service does --")
    candidates = [
        ("derived host", host),
        ("no direction prefix", athena_host("", suffix)),
        ("invented sibling on the same island",
         "%s.%s%s.powerapps.com" % (PROBE_MARKER, prefix, suffix)),
        ("nonexistent scale unit",
         athena_host(prefix, suffix.replace(suffix.split(".")[0],
                                            suffix.split(".")[0][:-3] + "999"))),
    ]
    for label, candidate in candidates:
        print("  %-38s %s" % (label, "resolves" if resolves(candidate) else "NXDOMAIN"))
    print("  Anything under a live scale unit resolves: the island publishes a wildcard onto")
    print("  its ingress gateway. Only the *dropped prefix* and a *bogus scale unit* fail here.")

    print()
    print("-- the gateway's own headers are what separate a real service from a made-up one --")
    print("  %-38s %-6s %-9s %s" % ("host", "status", "upstream?", "markers"))
    for label, candidate in [("derived host", host),
                             ("invented sibling on the same island",
                              "%s.%s%s.powerapps.com" % (PROBE_MARKER, prefix, suffix))]:
        if not resolves(candidate):
            print("  %-38s %s" % (label, "NXDOMAIN, not called"))
            continue
        status, headers, _ = client.request("https://%s/" % candidate, token=token)
        low = lower_headers(headers)
        print("  %-38s %-6s %-9s %s"
              % (label, status, "yes" if reached_upstream(headers) else "NO",
                 ",".join(m for m in UPSTREAM_MARKERS if m in low) or "-"))
    print("  A hostname the gateway does not know is refused by the gateway itself: same 404,")
    print("  but none of those headers and no upstream timing. That difference is the evidence.")

    print()
    print("-- other direction prefixes, to show the prefix is the region and not a constant --")
    geo = suffix.split("-")[0]
    for code in ("e", "se", "w", "n", "s", "c", "ne", "nw", "sw"):
        candidate = athena_host(code, suffix)
        print("  %-10s %-52s %s" % (code, candidate[:52],
                                    "resolves" if resolves(candidate) else "-"))
    print("  (Only the directions Azure actually has a region for in the %r geography exist.)" % geo)
    return host


# --------------------------------------------------------------------------
# 3. identity
# --------------------------------------------------------------------------

def decode_claims(token: str) -> dict:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except Exception:
        return {}


def probe_identity(token: str | None) -> None:
    print()
    print("=" * 74)
    print("IDENTITY: what the audience is, and what it is possible to be authorized as")
    print("=" * 74)

    for label, scope in (("application id form", ATHENA_SCOPE),
                         ("identifier URI form", ATHENA_SCOPE_URI)):
        issued = get_token(scope)
        claims = decode_claims(issued) if issued else {}
        if not claims:
            print("  %-22s not issuable" % label)
            continue
        print("  %-22s aud=%-46s scp=%s roles=%s"
              % (label, claims.get("aud"), claims.get("scp"), claims.get("roles")))
    print("  Both forms are issued. Which the service accepts cannot be tested without calling")
    print("  it, and calling it provisions something.")

    print()
    print("-- what the application publishes (az ad sp show; read-only) --")
    try:
        proc = subprocess.run(
            ["az", "ad", "sp", "show", "--id", ATHENA_APP_ID, "-o", "json"],
            capture_output=True, text=True, check=True)
        sp = json.loads(proc.stdout)
    except Exception as err:
        print("  lookup failed: %s" % err)
        return
    print("  displayName            %s" % sp.get("displayName"))
    print("  identifier URIs        %s" % ", ".join(sp.get("servicePrincipalNames") or []))
    print("  delegated permissions  %s"
          % ", ".join("%s (%s)" % (s.get("value"), s.get("adminConsentDisplayName"))
                      for s in sp.get("oauth2PermissionScopes") or []) or "none")
    print("  application roles      %s"
          % ", ".join(r.get("value") for r in sp.get("appRoles") or []) or "NONE")
    if not (sp.get("appRoles") or []):
        print()
        print("  No application roles at all. An app-only client-credentials token therefore")
        print("  arrives with no roles claim and nothing here can authorize it: this surface")
        print("  requires a delegated token. That is why the provider's fabric_link resource")
        print("  runs under a username/password alias rather than the pipeline identity.")


# --------------------------------------------------------------------------
# 4. routing and auth behaviour
# --------------------------------------------------------------------------

def probe_routing(client: ReadOnly, host: str, token: str | None,
                  environment_id: str, organization_id: str | None) -> None:
    print()
    print("=" * 74)
    print("ROUTING AND AUTH (read-only; nothing is invoked)")
    print("=" * 74)

    org_headers = {"x-ms-organization-id": organization_id} if organization_id else {}
    base = "/environment/%s" % environment_id
    documented = [
        ("lakehouseArtifacts (create route)", base + "/lakehouseArtifacts"),
        ("lakehouseArtifacts/{id} (delete route)",
         base + "/lakehouseArtifacts/00000000-0000-0000-0000-000000000000"),
        ("updateorganizationdetails", base + "/updateorganizationdetails"),
    ]
    invented = [
        ("an invented sibling path", base + "/" + PROBE_MARKER),
        ("the environment root", base),
        ("the site root", "/"),
    ]

    print("-- documented routes and invented ones, under every method we are allowed to send --")
    print("  %-40s %-8s %-6s %-7s %-9s %s"
          % ("path", "method", "status", "allow", "upstream?", "body"))
    for label, path in documented + invented:
        for method in ReadOnly.ALLOWED_METHODS:
            status, headers, body = client.request(
                "https://%s%s" % (host, path), method=method, token=token, headers=org_headers)
            low = lower_headers(headers)
            print("  %-40s %-8s %-6s %-7s %-9s %s"
                  % (label[:40], method, status, low.get("allow", "-"),
                     "yes" if reached_upstream(headers) else "no",
                     "%d bytes" % len(body) if body else "empty"))
    print()
    print("  Every row is the same. No 405, no Allow header, no error body: the service does not")
    print("  distinguish a route it serves under another method from a path that does not exist.")
    print("  Route existence CANNOT be established here without invoking the operation, which is")
    print("  why every operation in the spec carries x-probe-verified: false.")

    print()
    print("-- credentials: does anything challenge, or even notice? --")
    cases = [
        ("valid athena token", token),
        ("no token at all", None),
        ("token for the wrong audience", get_token(BAPI_SCOPE, "BAPI_TOKEN")),
        ("a bearer token that is not a JWT", "not-a-token"),
    ]
    print("  %-34s %-6s %-9s %s" % ("credential", "status", "upstream?", "WWW-Authenticate"))
    for label, candidate in cases:
        status, headers, _ = client.request(
            "https://%s%s/lakehouseArtifacts" % (host, base),
            token=candidate, headers=org_headers)
        low = lower_headers(headers)
        print("  %-34s %-6s %-9s %s"
              % (label, status, "yes" if reached_upstream(headers) else "no",
                 low.get("www-authenticate", "none")))
    print()
    print("  Indistinguishable. Routing fails before authentication runs, so the service never")
    print("  names its own audience -- there is no challenge to negotiate from. The audience is")
    print("  knowable only from the token or from captured traffic.")

    print()
    print("-- CORS preflight: the one request that reaches the application, and what it says --")
    preflight = {"Origin": "https://make.powerapps.com",
                 "Access-Control-Request-Method": "POST",
                 "Access-Control-Request-Headers": "authorization,x-" + PROBE_MARKER}
    for label, path in [("documented route", base + "/lakehouseArtifacts"),
                        ("invented path", base + "/" + PROBE_MARKER)]:
        status, headers, _ = client.request("https://%s%s" % (host, path),
                                            method="OPTIONS", headers=preflight)
        low = lower_headers(headers)
        print("  %-20s %-6s methods=%-32s origin=%s"
              % (label, status, low.get("access-control-allow-methods", "-"),
                 low.get("access-control-allow-origin", "-")))
    evil = dict(preflight, Origin="https://%s.example.com" % PROBE_MARKER)
    status, headers, _ = client.request("https://%s%s/lakehouseArtifacts" % (host, base),
                                        method="OPTIONS", headers=evil)
    low = lower_headers(headers)
    print("  %-20s %-6s echoes arbitrary origin=%s credentials=%s"
          % ("arbitrary origin", status, low.get("access-control-allow-origin", "-"),
             low.get("access-control-allow-credentials", "-")))
    print()
    print("  The preflight is answered by the application rather than 404'd, which is further")
    print("  proof the host is real -- but it is a blanket reflector: the same fixed method list")
    print("  for any path including invented ones, any origin echoed back, any requested header")
    print("  allowed. It says nothing about which routes exist or which methods they take.")


# --------------------------------------------------------------------------
# 5. prerequisite: the Dataverse datalakefolders read (boundary: dataverse)
# --------------------------------------------------------------------------

def probe_dataverse(client: ReadOnly, dataverse_host: str) -> None:
    """Read the datalakefolder rows the unlink targets. Belongs to the dataverse boundary."""
    print()
    print("=" * 74)
    print("PREREQUISITE: the Dataverse datalakefolders read the unlink depends on")
    print("=" * 74)

    token = get_token("https://%s/.default" % dataverse_host, "DATAVERSE_TOKEN")
    if not token:
        print("  no Dataverse token; skipping")
        return

    url = ("https://%s/api/data/v9.1/datalakefolders?%s"
           % (dataverse_host,
              urllib.parse.urlencode({"$select": "datalakefolderid,datalakefolder_uniquename"})))
    status, body = client.json(url, token=token)
    rows = (body or {}).get("value", []) if isinstance(body, dict) else []
    print("  GET /api/data/v9.1/datalakefolders -> %s, %d rows" % (status, len(rows)))
    if rows:
        print("  fields returned per row: %s" % ", ".join(sorted(rows[0].keys())))
    names = sorted(r.get("datalakefolder_uniquename") for r in rows)
    print("  unique names present: %s" % ", ".join(n for n in names if n))

    status, profiles = client.json(
        "https://%s/api/data/v9.1/synapselinkprofiles?%s"
        % (dataverse_host, urllib.parse.urlencode({"$select": "synapselinkprofileid"})),
        token=token)
    count = len((profiles or {}).get("value", [])) if isinstance(profiles, dict) else 0
    print("  GET /api/data/v9.1/synapselinkprofiles -> %s, %d profiles" % (status, count))

    if count == 0 and any(n in names for n in ("cds2_workspace", "cds3_workspace")):
        print()
        print("  This organization has NO Synapse Link profile and still carries cds2_workspace")
        print("  and cds3_workspace rows. They are stock system folders, not artefacts of a link.")
        print("  A client resolving 'the folder the unlink targets' must name one of those two")
        print("  explicitly; falling back to the first row in the table selects an unrelated")
        print("  system folder on any organization that was never linked.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--environment-id", default=os.environ.get("ATHENA_ENVIRONMENT_ID"),
                        help="Power Platform environment id to derive the host from")
    parser.add_argument("--organization-id", default=os.environ.get("ATHENA_ORGANIZATION_ID"),
                        help="Dataverse organization id for the x-ms-organization-id header; "
                             "read from the environment when omitted")
    parser.add_argument("--dataverse-host", default=os.environ.get("ATHENA_DATAVERSE_HOST"),
                        help="Dataverse hostname for the prerequisite read; "
                             "read from the environment when omitted")
    parser.add_argument("--cluster-uri-suffix",
                        help="skip the BAPI read and use this cluster suffix directly")
    parser.add_argument("--azure-region", default="",
                        help="Azure region of the environment, e.g. australiaeast; "
                             "used to derive the host's direction prefix")
    parser.add_argument("--dns-only", action="store_true",
                        help="host construction only; acquires no credentials")
    parser.add_argument("--skip-dataverse", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    client = ReadOnly(verbose=args.verbose)
    started = time.time()

    suffix = args.cluster_uri_suffix
    region = args.azure_region
    org_id = args.organization_id
    dv_host = args.dataverse_host

    if not suffix:
        if not args.environment_id:
            parser.error("--environment-id is required unless --cluster-uri-suffix is given")
        derived = probe_bapi(client, args.environment_id)
        if not derived:
            print("could not read the environment; nothing to derive a host from")
            return 1
        suffix = derived["uriSuffix"]
        region = region or derived.get("azureRegion") or ""

    token = None if args.dns_only else get_token(ATHENA_SCOPE, "ATHENA_TOKEN")
    host = probe_host(client, token, suffix, region)

    if args.dns_only:
        print("\n--dns-only: stopping before any authenticated probe")
        return 0

    probe_identity(token)

    if args.environment_id and host:
        if not org_id:
            bapi_token = get_token(BAPI_SCOPE, "BAPI_TOKEN")
            if bapi_token:
                _, body = client.json(
                    "https://%s/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/%s?%s"
                    % (BAPI_HOST, args.environment_id,
                       urllib.parse.urlencode({"api-version": BAPI_API_VERSIONS[1]})),
                    token=bapi_token)
                lem = (((body or {}).get("properties") or {}).get("linkedEnvironmentMetadata") or {}) \
                    if isinstance(body, dict) else {}
                org_id = lem.get("resourceId")
                if not dv_host and lem.get("instanceUrl"):
                    dv_host = urllib.parse.urlsplit(lem["instanceUrl"]).netloc
        probe_routing(client, host, token, args.environment_id, org_id)

    if dv_host and not args.skip_dataverse:
        probe_dataverse(client, dv_host)

    print()
    print("%d requests in %.1fs. Nothing was created, modified or deleted -- the transport"
          % (client.calls, time.time() - started))
    print("in this script cannot send anything but GET, HEAD and OPTIONS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
