#!/usr/bin/env python3
"""Live probe harness for the Power Platform Licensing API.

Read-only by construction. The transport refuses any method other than GET,
HEAD and OPTIONS and never sends a request body, so no run of this script can
alter a billing policy, a currency allocation or anything else. The one write
route the surface is known to have (refreshProvisioningStatus) is located the
same way everything else is - by asking for it with GET and reading the 405 -
and is never invoked.

What it establishes:

  * the four operations recorded in first-party UI traffic still answer, and
    with the shapes the spec claims;
  * which of the three version segments (v0.1-alpha, v1.0, v2.0) each route
    registers, and whether the representations differ between them;
  * that the segment is a route prefix rather than an api-version, by playing
    the ?api-version query parameter against it;
  * the five error envelopes, and the route-existence oracle that tells a
    route that does not exist from an id that has no record;
  * that a Power Platform API token is rejected here.

It prints shapes, status codes, key names and enum vocabulary - never a tenant
id, an environment id, a user object id, a billing policy id or name, an Azure
subscription id or resource group, and never a token. Output is safe to paste
into an issue.

Usage
    probe.py --tenant TENANT_ID
    probe.py --tenant T --environment E --user U    # widen the coverage
    probe.py --tenant T --sections recorded,versioning
    probe.py --hosts                                # DNS-only sovereign sweep

Ids come from arguments or from LICENSING_TENANT_ID / LICENSING_ENVIRONMENT_ID
/ LICENSING_USER_ID in the environment. Nothing is hardcoded.

Auth: an Entra token for https://licensing.powerplatform.microsoft.com/.default,
taken from the logged-in az CLI session unless LICENSING_TOKEN is set. That
scope is a resource of its own - a token for https://api.powerplatform.com,
which serves the same resources under /licensing/, is rejected with 401.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCOPE = "https://licensing.powerplatform.microsoft.com/.default"
PPAPI_SCOPE = "https://api.powerplatform.com/.default"
HOST = "licensing.powerplatform.microsoft.com"

SEGMENTS = ["v0.1-alpha", "v1.0", "v2.0"]

# The seven hostnames microsoft/terraform-provider-power-platform declares for
# this API in internal/constants/constants.go - and never calls.
SOVEREIGN_HOSTS = [
    ("PUBLIC", "licensing.powerplatform.microsoft.com"),
    ("USGOV", "gov.licensing.powerplatform.microsoft.us"),
    ("USGOVHIGH", "high.licensing.powerplatform.microsoft.us"),
    ("USDOD", "licensing.appsplatform.us"),
    ("CHINA", "licensing.partner.microsoftonline.cn"),
    ("EX", "licensing.eaglex.ic.gov"),
    ("RX", "licensing.microsoft.scloud"),
]

REQUEST_PAUSE = 0.35
MAX_RETRIES = 4
READ_ONLY_METHODS = ("GET", "HEAD", "OPTIONS")

ZERO_GUID = "00000000-0000-0000-0000-000000000000"


# --------------------------------------------------------------------------- auth

def get_token(scope: str = SCOPE, env_var: str = "LICENSING_TOKEN") -> str:
    token = os.environ.get(env_var)
    if token:
        return token.strip()
    proc = subprocess.run(
        ["az", "account", "get-access-token", "--scope", scope,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


# --------------------------------------------------------------------------- transport

class Licensing:
    """Minimal read-only client with 429/5xx backoff.

    request() raises rather than sending anything that could change state.
    """

    def __init__(self, token: str, host: str = HOST, verbose: bool = False):
        self.token = token
        self.host = host
        self.verbose = verbose
        self.calls = 0

    def request(self, path: str, method: str = "GET", token: str | None = -1,
                headers: dict | None = None):
        """Return (status, headers, body-bytes). Never sends a request body."""
        if method not in READ_ONLY_METHODS:
            raise ValueError("probe.py is read-only; refusing method " + method)

        hdrs = {"Accept": "application/json"}
        bearer = self.token if token == -1 else token
        if bearer:
            hdrs["Authorization"] = "Bearer " + bearer
        hdrs.update(headers or {})
        url = "https://%s%s" % (self.host, path)

        for attempt in range(MAX_RETRIES):
            req = urllib.request.Request(url, headers=hdrs, method=method)
            self.calls += 1
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
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


# --------------------------------------------------------------------------- helpers

def lower_headers(headers: dict) -> dict:
    return {k.lower(): v for k, v in headers.items()}


def route_exists(headers: dict) -> bool:
    """The oracle: api-supported-versions is present iff a route matched.

    A 404 carrying it means the route exists and the bound id has no record;
    a 404 without it means this host has no such route.
    """
    return "api-supported-versions" in lower_headers(headers)


def as_json(body: bytes):
    try:
        return json.loads(body)
    except Exception:
        return None


def shape(value, depth: int = 0) -> str:
    """Describe a JSON value by its structure, never by its content."""
    if isinstance(value, dict):
        if depth >= 2:
            return "{%d keys}" % len(value)
        return "{" + ", ".join(
            "%s: %s" % (k, shape(v, depth + 1)) for k, v in list(value.items())[:12]) + "}"
    if isinstance(value, list):
        if not value:
            return "[]"
        return "[%d x %s]" % (len(value), shape(value[0], depth + 1))
    if value is None:
        return "null"
    return type(value).__name__


def key_set(value) -> list:
    """Key names, looking through a {value: [...]} envelope to the items."""
    if isinstance(value, dict):
        if list(value) == ["value"] and isinstance(value["value"], list):
            return key_set(value["value"])
        return sorted(value.keys())
    if isinstance(value, list) and value and isinstance(value[0], dict):
        keys = collections.Counter()
        for item in value:
            if isinstance(item, dict):
                keys.update(item.keys())
        return sorted(keys)
    return []


def envelope_of(status: int, headers: dict, body: bytes) -> str:
    """Name which of the five error envelopes this response used."""
    if not body:
        return "emptyBody"
    doc = as_json(body)
    if doc is None:
        return "non-JSON(%s)" % lower_headers(headers).get("content-type", "?")
    if isinstance(doc, list):
        if doc and isinstance(doc[0], dict) and set(doc[0]) >= {"key", "message"}:
            return "keyMessageArray"
        return "array"
    if isinstance(doc, dict):
        if "traceId" in doc and "title" in doc:
            return "problemDetails"
        err = doc.get("error")
        if isinstance(err, dict):
            if "namespace" in err:
                return "serviceFabricError"
            if "details" in err:
                return "nestedErrorWithDetails"
        return "object"
    return "scalar"


def dns_chain(host: str):
    """First hop of the CNAME chain, or None if the name does not resolve.

    `dig` gives the chain; `socket` only proves resolution, so the fallback
    reports that much and no more. No request is made either way.
    """
    try:
        proc = subprocess.run(["dig", "+short", host], capture_output=True,
                              text=True, timeout=15)
        lines = [l.strip().rstrip(".") for l in proc.stdout.splitlines() if l.strip()]
        if lines:
            return lines[0] if len(lines) == 1 else "%s ... (%d hops)" % (lines[0], len(lines))
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        socket.getaddrinfo(host, 443)
    except OSError:
        return None
    return "(resolves; install dig to see the CNAME chain)"


def banner(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------- routes

def routes(tenant: str, environment: str | None, user: str | None) -> list:
    """(label, path-suffix-after-the-version-segment) pairs.

    Suffixes that need an id the caller did not supply are dropped, so the
    script degrades to whatever coverage the arguments allow.
    """
    out = [
        ("BillingPolicies", "/tenants/%s/BillingPolicies" % tenant),
        ("TenantCapacity", "/tenants/%s/TenantCapacity" % tenant),
        ("Entitlements", "/tenants/%s/Entitlements" % tenant),
        ("CurrencyReports", "/tenants/%s/CurrencyReports" % tenant),
        ("allocationsByEnvironment", "/tenants/%s/allocationsByEnvironment" % tenant),
    ]
    if environment:
        out += [
            ("allocationsByEnvironment/{env}",
             "/tenants/%s/allocationsByEnvironment/%s" % (tenant, environment)),
            ("Environments/{env}/BillingPolicy",
             "/tenants/%s/Environments/%s/BillingPolicy" % (tenant, environment)),
        ]
    if user:
        out += [
            ("Users/{user}/Trials", "/tenants/%s/Users/%s/Trials" % (tenant, user)),
            ("Users/{user}/Trials/AI", "/tenants/%s/Users/%s/Trials/AI" % (tenant, user)),
        ]
    return out


# --------------------------------------------------------------------------- sections

def probe_recorded(client: Licensing, tenant: str, environment: str | None,
                   user: str | None) -> None:
    """The four calls captured from first-party UI traffic, re-issued."""
    banner("RECORDED OPERATIONS (from admin-center and maker-portal traffic)")
    recorded = [
        ("GET /v2.0/.../BillingPolicies", "/v2.0/tenants/%s/BillingPolicies" % tenant),
        ("GET /v0.1-alpha/.../CurrencyReports", "/v0.1-alpha/tenants/%s/CurrencyReports" % tenant),
    ]
    if environment:
        recorded.append(("GET /v0.1-alpha/.../allocationsByEnvironment/{env}",
                         "/v0.1-alpha/tenants/%s/allocationsByEnvironment/%s" % (tenant, environment)))
    if user:
        recorded.append(("GET /v1.0/.../Users/{user}/Trials/AI",
                         "/v1.0/tenants/%s/Users/%s/Trials/AI" % (tenant, user)))

    for label, path in recorded:
        status, headers, body = client.request(path)
        doc = as_json(body)
        low = lower_headers(headers)
        print("  %-46s %s  %s" % (label, status, low.get("content-type", "-")))
        print("  %-46s   api-supported-versions=%s  x-servicefabric=%s"
              % ("", low.get("api-supported-versions"), low.get("x-servicefabric")))
        if status == 200:
            print("  %-46s   shape %s" % ("", shape(doc)))
        else:
            print("  %-46s   envelope=%s" % ("", envelope_of(status, headers, body)))


def probe_versioning(client: Licensing, tenant: str, environment: str | None,
                     user: str | None) -> None:
    """Which segments each route registers, and whether they agree."""
    banner("VERSION SEGMENTS (the segment is a route prefix, not an api-version)")
    print("  200(n) = ok with n items or 'obj'; 404* = route exists, no record; 404 = no route")
    print()
    for label, suffix in routes(tenant, environment, user):
        cells, bodies = [], {}
        for segment in SEGMENTS:
            status, headers, body = client.request("/%s%s" % (segment, suffix))
            doc = as_json(body)
            if status == 200 and doc is not None:
                bodies[segment] = doc
                if isinstance(doc, list):
                    count = str(len(doc))
                elif isinstance(doc, dict) and isinstance(doc.get("value"), list):
                    count = str(len(doc["value"]))
                else:
                    count = "obj"
                cells.append("%s:200(%s)" % (segment, count))
            else:
                cells.append("%s:%d%s" % (segment, status, "*" if route_exists(headers) else ""))
        print("  %-34s %s" % (label, "  ".join(cells)))
        if len(bodies) > 1:
            keysets = {s: key_set(d) for s, d in bodies.items()}
            distinct = {tuple(v) for v in keysets.values()}
            if len(distinct) > 1:
                print("  %-34s   representations DIFFER:" % "")
                for segment, keys in keysets.items():
                    print("  %-34s     %-12s %s" % ("", segment, keys))
            else:
                print("  %-34s   representations identical across segments" % "")

    banner("api-version AS A QUERY PARAMETER (played against the /v2.0/ segment)")
    base = "/v2.0/tenants/%s/BillingPolicies" % tenant
    for label, query in [("omitted", ""), ("api-version=1.0", "?api-version=1.0"),
                         ("api-version=2.0", "?api-version=2.0"), ("api-version=2", "?api-version=2"),
                         ("api-version= (empty)", "?api-version=")]:
        status, headers, _ = client.request(base + query)
        print("  %-24s %s   api-supported-versions=%s"
              % (label, status, lower_headers(headers).get("api-supported-versions")))
    for label, hdr in [("api-version header", {"api-version": "2.0"}),
                       ("x-ms-api-version header", {"x-ms-api-version": "2.0"}),
                       ("Accept ;v=2.0", {"Accept": "application/json;v=2.0"})]:
        status, _, _ = client.request(base, headers=hdr)
        print("  %-24s %s   (ignored if 200)" % (label, status))

    banner("ROUTE MATCHING IS CASE-INSENSITIVE, SEGMENT INCLUDED")
    for label, path in [("as documented", base),
                        ("resource lowercased", "/v2.0/tenants/%s/billingpolicies" % tenant),
                        ("segment uppercased", "/V2.0/tenants/%s/BillingPolicies" % tenant)]:
        status, _, _ = client.request(path)
        print("  %-24s %s" % (label, status))


def probe_enums(client: Licensing, tenant: str, user: str | None) -> None:
    """Vocabulary the live service reports, and vocabulary it validates."""
    banner("ENUM VOCABULARY (names only; no tenant values are printed)")

    status, _, body = client.request("/v2.0/tenants/%s/BillingPolicies" % tenant)
    doc = as_json(body) or {}
    policies = doc.get("value") or []
    if policies:
        ents = [e for p in policies for e in p.get("payGoEntitlements", [])]
        print("  payGoEntitlements[].entitlementId : %s"
              % sorted({e.get("entitlementId") for e in ents}))
        print("  payGoEntitlements[].productCategory: %s"
              % sorted({e.get("productCategory") for e in ents}))
        print("  billingPolicy.type                : %s"
              % sorted({p.get("type") for p in policies}))
        print("  billingPolicy.status              : %s"
              % sorted({p.get("status") for p in policies}))
        print("  billingInstrument.provisioningStatus: %s"
              % sorted({(p.get("billingInstrument") or {}).get("provisioningStatus")
                        for p in policies}))
        caps = {e.get("value") for e in ents}
        print("  payGoEntitlements[].value sentinel : %s (Double.MaxValue means uncapped)"
              % sorted(caps))
    else:
        print("  no billing policies in this tenant; policy vocabulary not observable")

    status, _, body = client.request("/v0.1-alpha/tenants/%s/TenantCapacity" % tenant)
    cap = as_json(body) or {}
    meters = cap.get("tenantCapacities") or []
    if meters:
        print("  capacityType                      : %s"
              % sorted({m.get("capacityType") for m in meters}))
        print("  capacitySubType                   : %s"
              % sorted({ce.get("capacitySubType") for m in meters
                        for ce in m.get("capacityEntitlements", [])}))
        print("  capacityUnits                     : %s"
              % sorted({m.get("capacityUnits") for m in meters}))
        print("  meter status                      : %s"
              % sorted({m.get("status") for m in meters}))

    banner("ENTITLEMENT ID VOCABULARY (two subsystems, one name, different sets)")
    print("  Every id a billing policy lists, asked of Entitlements/{id}:")
    candidates = sorted({e.get("entitlementId") for p in policies
                         for e in p.get("payGoEntitlements", [])}) or \
        ["Database", "File", "Log", "W365APAYGO"]
    resolved, recognised, unrecognised = [], [], []
    for candidate in candidates:
        status, headers, body = client.request(
            "/v2.0/tenants/%s/Entitlements/%s" % (tenant, candidate))
        envelope = envelope_of(status, headers, body)
        if status == 200:
            resolved.append(candidate)
        elif envelope == "problemDetails":
            recognised.append(candidate)
        else:
            unrecognised.append(candidate)
    print("    resolve (200)                       : %s" % resolved)
    print("    recognised, tenant holds none (404 problemDetails): %s" % recognised)
    print("    not recognised at all (404 keyMessageArray)       : %s" % unrecognised)

    if user:
        banner("trialType BINDING (a validated .NET enum)")
        for candidate in ["AI", "ai", "Ai", "AI ", "1", "0", "None", "Copilot", "PowerApps"]:
            status, headers, body = client.request(
                "/v1.0/tenants/%s/Users/%s/Trials/%s"
                % (tenant, user, urllib.parse.quote(candidate)))
            note = ""
            if status == 200:
                doc = as_json(body) or {}
                note = "-> normalised to %r" % doc.get("trialType")
            print("    %-10r %s  %-24s %s"
                  % (candidate, status, envelope_of(status, headers, body), note))


def probe_errors(client: Licensing, tenant: str, environment: str | None,
                 user: str | None) -> None:
    """All five envelopes, plus the route-existence oracle."""
    banner("AUTH: THIS HOST IS ITS OWN ENTRA RESOURCE")
    base = "/v2.0/tenants/%s/BillingPolicies" % tenant
    for label, token in [("no Authorization header", None),
                         ("malformed bearer", "notatoken")]:
        status, headers, body = client.request(base, token=token)
        print("  %-30s %s  WWW-Authenticate=%s  body=%s"
              % (label, status, lower_headers(headers).get("www-authenticate", "-")[:46],
                 envelope_of(status, headers, body)))
    try:
        ppapi = get_token(PPAPI_SCOPE, "PPAPI_TOKEN")
    except Exception as err:
        print("  %-30s (could not acquire: %s)" % ("Power Platform API token", err))
    else:
        status, headers, body = client.request(base, token=ppapi)
        print("  %-30s %s  <- api.powerplatform.com serves the same resources under"
              % ("Power Platform API token", status))
        print("  %-30s     /licensing/ but its token is not accepted here" % "")

    banner("ROUTE-EXISTENCE ORACLE (404 with a body vs 404 without)")
    cases = [("unmatched route", "/v2.0/tenants/%s/ZzzNoSuchResource" % tenant),
             ("unmatched segment", "/v9.9/tenants/%s/BillingPolicies" % tenant),
             ("segment the route does not register", "/v1.0/tenants/%s/BillingPolicies" % tenant)]
    if environment:
        cases.append(("real route, id with no record",
                      "/v0.1-alpha/tenants/%s/allocationsByEnvironment/%s" % (tenant, environment)))
    for label, path in cases:
        status, headers, body = client.request(path)
        print("  %-38s %s  route_exists=%-5s envelope=%s"
              % (label, status, route_exists(headers), envelope_of(status, headers, body)))

    banner("ERROR ENVELOPES")
    probes = [("foreign tenant", "/v2.0/tenants/%s/BillingPolicies" % ZERO_GUID),
              ("malformed tenant", "/v2.0/tenants/notaguid/BillingPolicies"),
              ("unknown billing policy id",
               "/v2.0/tenants/%s/BillingPolicies/%s" % (tenant, ZERO_GUID)),
              ("unrecognised entitlement id",
               "/v2.0/tenants/%s/Entitlements/ZzzNoSuchMeter" % tenant),
              ("api-version=2.0 on the /v2.0/ route",
               "/v2.0/tenants/%s/BillingPolicies?api-version=2.0" % tenant)]
    if user:
        probes += [("invalid trialType",
                    "/v1.0/tenants/%s/Users/%s/Trials/ZzzNoSuchTrial" % (tenant, user)),
                   ("malformed user id",
                    "/v1.0/tenants/%s/Users/notaguid/Trials" % tenant)]
    for label, path in probes:
        status, headers, body = client.request(path)
        print("  %-38s %s  %s" % (label, status, envelope_of(status, headers, body)))

    banner("METHODS OTHER THAN GET")
    for method in ("HEAD", "OPTIONS"):
        status, headers, _ = client.request(base, method=method)
        print("  %-10s %s  Allow=%s" % (method, status, headers.get("Allow", "-")))
    print("  Browsers still get a 204 for a CORS preflight: the gateway answers OPTIONS")
    print("  only when Access-Control-Request-Method is present, and advertises")
    print("  Access-Control-Allow-Methods: *,POST,GET,PATCH,DELETE - which overstates")
    print("  what the routes accept. POST/PUT/PATCH/DELETE are never issued by this script.")

    banner("THE WRITE SURFACE, MAPPED WITHOUT WRITING")
    print("  HEAD is refused with 405 on every route, and the Allow header that comes")
    print("  back enumerates the methods that route does accept. That maps the whole")
    print("  write surface without issuing a single mutating request.")
    print()
    for label, suffix in routes(tenant, environment, user):
        for segment in SEGMENTS:
            status, headers, _ = client.request("/%s%s" % (segment, suffix), method="HEAD")
            if status == 405:
                print("  %-34s %-11s Allow=%s"
                      % (label, segment, headers.get("Allow", "-")))

    banner("WRITE ROUTES: LOCATED BY 405, NEVER INVOKED")
    status, _, body = client.request("/v2.0/tenants/%s/BillingPolicies" % tenant)
    doc = as_json(body) or {}
    policies = doc.get("value") or []
    if not policies:
        print("  no billing policy to probe against")
    else:
        policy_id = policies[0]["id"]
        for suffix in ("refreshProvisioningStatus", "Environments/add", "Environments/remove"):
            status, headers, body = client.request(
                "/v2.0/tenants/%s/BillingPolicies/%s/%s" % (tenant, policy_id, suffix))
            verdict = "POST route exists" if status == 405 else (
                "bound as {environmentId}, not a route" if route_exists(headers) else "no route")
            print("  GET %-28s -> %s Allow=%-6s %s"
                  % (suffix, status, headers.get("Allow", "-"), verdict))

    banner("THE OData ROOT IS A FALSE POSITIVE")
    for path in ("/", "/$metadata"):
        status, headers, body = client.request(path)
        print("  %-12s %s  %-34s %d bytes (inert; not part of this API)"
              % (path, status, lower_headers(headers).get("content-type", "-")[:34], len(body)))


def probe_hosts() -> None:
    """DNS only. No token is ever sent to a sovereign host."""
    banner("SOVEREIGN HOSTS (DNS only - no request is made)")
    print("  The seven names the Terraform provider declares for this API and never calls.")
    print()
    for cloud, host in SOVEREIGN_HOSTS:
        chain = dns_chain(host)
        if chain is None:
            print("  %-10s %-46s unresolved from the public internet" % (cloud, host))
            continue
        print("  %-10s %-46s -> %s" % (cloud, host, chain))
    print()
    print("  Naming is not uniform: USGOV and USGOVHIGH prefix the geo onto the")
    print("  commercial domain, while USDOD, CHINA, EX and RX replace the domain")
    print("  outright. These cannot be composed from the public host by substitution.")


SECTIONS = {
    "recorded": probe_recorded,
    "versioning": probe_versioning,
    "enums": probe_enums,
    "errors": probe_errors,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tenant", default=os.environ.get("LICENSING_TENANT_ID"),
                        help="tenant id to read; must be the token's own tenant")
    parser.add_argument("--environment", default=os.environ.get("LICENSING_ENVIRONMENT_ID"),
                        help="an environment id in that tenant (widens coverage)")
    parser.add_argument("--user", default=os.environ.get("LICENSING_USER_ID"),
                        help="a user object id in that tenant (widens coverage)")
    parser.add_argument("--host", default=HOST, help="licensing host to probe")
    parser.add_argument("--sections", default=",".join(SECTIONS),
                        help="comma-separated subset of: " + ", ".join(SECTIONS))
    parser.add_argument("--hosts", action="store_true",
                        help="sovereign host DNS sweep only; no token, no requests")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.hosts:
        probe_hosts()
        return 0
    if not args.tenant:
        parser.error("--tenant is required (or set LICENSING_TENANT_ID)")

    chosen = [s.strip() for s in args.sections.split(",") if s.strip()]
    unknown = [s for s in chosen if s not in SECTIONS]
    if unknown:
        parser.error("unknown section(s): %s" % ", ".join(unknown))

    client = Licensing(get_token(), host=args.host, verbose=args.verbose)
    started = time.time()

    for name in chosen:
        func = SECTIONS[name]
        if name == "enums":
            func(client, args.tenant, args.user)
        else:
            func(client, args.tenant, args.environment, args.user)

    probe_hosts()

    print()
    print("%d requests in %.1fs, all read-only" % (client.calls, time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main())
