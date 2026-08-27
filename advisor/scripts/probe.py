#!/usr/bin/env python3
"""Live probe harness for the PowerApps Advisor API (solution checker).

Read-only by construction. It issues GETs against the rule and ruleset
catalogues, plus negative probes that establish the shape of the analysis job
routes *without invoking them*: a GET against a POST-only route answers 405
with an Allow header, and the wrong api-version answers 400
UnsupportedApiVersion, so both confirm a route exists without submitting work.
There is no code path here that POSTs, uploads, or starts an analysis.

It prints shapes, counts and enum distributions - never a tenant identifier,
an environment id, or a token.

Usage
    probe.py                                  # every known public geography
    probe.py --region unitedstates --region europe
    probe.py --host contoso.api.advisor.powerapps.com
    probe.py --ruleset "AppSource Certification"
    probe.py --skip-negative                  # catalogue survey only

Auth: an Entra token for https://advisor.powerapps.com/.default, taken from
the logged-in az CLI session unless ADVISOR_TOKEN is set in the environment.

Take the host for a specific environment from that environment's
PowerAppsAdvisor runtime endpoint (BAPI: GET
/providers/Microsoft.BusinessAppPlatform/scopes/admin/environments/{id}
?$expand=permissions) rather than composing it from the environment's
location - the mapping is not a string transform.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request

SCOPE = "https://advisor.powerapps.com/.default"
HOST_TEMPLATE = "{region}.api.advisor.powerapps.com"

# Public-cloud geographies. Sovereign clouds use different hostnames.
REGIONS = [
    "asia", "unitedstates", "canada", "europe", "france", "germany", "india",
    "japan", "korea", "norway", "singapore", "southafrica", "southamerica",
    "switzerland", "unitedarabemirates", "unitedkingdom", "unitedstates",
]

# Product constants, not tenant data: the ruleset the maker portal and the
# Terraform provider use. Overridable with --ruleset.
SOLUTION_CHECKER_RULESET = "0ad12346-e108-40b8-a956-9a8f95ea18c9"

CATALOGUE_API_VERSION = "2.0"
ANALYSIS_API_VERSION = "1.0"

SEVERITY_NAMES = {1: "Informational", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
CATEGORY_NAMES = {
    1: "Performance",
    2: "Upgrade Readiness",
    3: "Usage",
    4: "Security",
    5: "Design",
    6: "(unobserved; presumed Online Migration)",
    7: "Maintainability",
    8: "Supportability",
    9: "Accessibility",
    10: "(licensing; no published name)",
}

REQUEST_PAUSE = 0.6
MAX_RETRIES = 4


def get_token() -> str:
    token = os.environ.get("ADVISOR_TOKEN")
    if token:
        return token.strip()
    proc = subprocess.run(
        ["az", "account", "get-access-token", "--scope", SCOPE,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


class Advisor:
    """Minimal read-only client with 429/5xx backoff."""

    def __init__(self, token: str, verbose: bool = False):
        self.token = token
        self.verbose = verbose
        self.calls = 0

    def request(self, url: str, method: str = "GET", headers: dict | None = None,
                authenticated: bool = True):
        """Return (status, headers, body-bytes). Never sends a request body."""
        hdrs = {"Accept": "application/json"}
        if authenticated:
            hdrs["Authorization"] = "Bearer " + self.token
        hdrs.update(headers or {})
        if method not in ("GET", "HEAD", "OPTIONS"):
            raise ValueError("probe.py is read-only; refusing method " + method)

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

    def get_json(self, url: str, headers: dict | None = None):
        status, resp_headers, body = self.request(url, headers=headers)
        try:
            return status, json.loads(body)
        except ValueError:
            return status, None


def url_for(host: str, path: str, **params) -> str:
    query = {k: v for k, v in params.items() if v is not None}
    return "https://%s%s?%s" % (host, path, urllib.parse.urlencode(query))


def summarise_rules(rules: list) -> dict:
    presence = collections.Counter()
    for rule in rules:
        presence.update(rule.keys())
    return {
        "count": len(rules),
        "presence": dict(presence),
        "severity": collections.Counter(r.get("severity") for r in rules),
        "primaryCategory": collections.Counter(r.get("primaryCategory") for r in rules),
        "componentType": collections.Counter(r.get("componentType") for r in rules),
        "include": collections.Counter(r.get("include") for r in rules),
        "prefix": collections.Counter(r["code"].split("-")[0] for r in rules if "code" in r),
        "nulls": sum(1 for r in rules for v in r.values() if v is None),
        "codes": {r["code"] for r in rules if "code" in r},
    }


def probe_catalogue(client: Advisor, hosts: dict, ruleset: str) -> dict:
    print("=" * 72)
    print("RULESETS")
    print("=" * 72)
    for label, host in hosts.items():
        status, body = client.get_json(
            url_for(host, "/api/ruleset", **{"api-version": CATALOGUE_API_VERSION}))
        if status != 200 or body is None:
            print("  %-20s %s (no ruleset list)" % (label, status))
            continue
        names = ", ".join("%s=%s" % (r.get("name"), r.get("id")) for r in body)
        print("  %-20s %s  %s" % (label, status, names))

    print()
    print("=" * 72)
    print("RULES for ruleset %r" % ruleset)
    print("=" * 72)
    summaries = {}
    for label, host in hosts.items():
        status, body = client.get_json(url_for(
            host, "/api/rule", **{"api-version": CATALOGUE_API_VERSION, "ruleset": ruleset}))
        if status != 200 or body is None:
            print("  %-20s %s (no rules)" % (label, status))
            continue
        summaries[label] = summarise_rules(body)
        print("  %-20s %s  %d rules" % (label, status, len(body)))

    if not summaries:
        return summaries

    print()
    print("-- field presence (a field short of the rule count is optional) --")
    for label, s in summaries.items():
        optional = {k: v for k, v in s["presence"].items() if v != s["count"]}
        print("  %-20s n=%-4d always=%s" % (
            label, s["count"], sorted(k for k, v in s["presence"].items() if v == s["count"])))
        if optional:
            print("  %-20s   sometimes-absent: %s" % ("", optional))
        if s["nulls"]:
            print("  %-20s   explicit nulls: %d" % ("", s["nulls"]))

    merged = collections.Counter()
    merged_cat = collections.Counter()
    merged_ct = collections.Counter()
    merged_inc = collections.Counter()
    for s in summaries.values():
        merged.update(s["severity"])
        merged_cat.update(s["primaryCategory"])
        merged_ct.update(s["componentType"])
        merged_inc.update(s["include"])

    print()
    print("-- enum values observed across every probed host --")
    print("  severity:")
    for value in sorted(merged):
        print("    %-4s %-6d %s" % (value, merged[value], SEVERITY_NAMES.get(value, "?")))
    print("  primaryCategory:")
    for value in sorted(merged_cat):
        print("    %-4s %-6d %s" % (value, merged_cat[value], CATEGORY_NAMES.get(value, "?")))
    print("  componentType: %s" % dict(merged_ct))
    print("  include:       %s" % dict(merged_inc))

    if len(summaries) > 1:
        print()
        print("-- regional drift (the catalogue is NOT uniform across geographies) --")
        groups = collections.defaultdict(list)
        for label, s in summaries.items():
            groups[frozenset(s["codes"])].append(label)
        print("  %d distinct catalogues across %d hosts" % (len(groups), len(summaries)))
        ordered = sorted(groups.items(), key=lambda kv: -len(kv[0]))
        for codes, labels in ordered:
            print("    n=%-4d %s" % (len(codes), ", ".join(sorted(labels))))
        if len(ordered) > 1:
            widest = ordered[0][0]
            for codes, labels in ordered[1:]:
                missing = sorted(widest - codes)
                print("    missing from %s: %s" % (sorted(labels)[0], missing))
    return summaries


def probe_parameters(client: Advisor, host: str, ruleset: str) -> None:
    print()
    print("=" * 72)
    print("QUERY PARAMETER BEHAVIOUR (single host)")
    print("=" * 72)

    def rules(**params):
        status, body = client.get_json(url_for(host, "/api/rule", **params))
        return status, (len(body) if isinstance(body, list) else body)

    base = {"api-version": CATALOGUE_API_VERSION}
    cases = [
        ("ruleset omitted (every rule)", dict(base)),
        ("ruleset empty string", dict(base, ruleset="")),
        ("ruleset by id", dict(base, ruleset=ruleset)),
        ("ruleset id uppercased", dict(base, ruleset=ruleset.upper())),
        ("ruleset unrecognised (fails open)",
         dict(base, ruleset="00000000-0000-0000-0000-000000000000")),
        ("api-version omitted", {"ruleset": ruleset}),
        ("api-version 1.0", dict(base, **{"api-version": "1.0", "ruleset": ruleset})),
        ("api-version 3.0 (unsupported)",
         dict(base, **{"api-version": "3.0", "ruleset": ruleset})),
        ("includeMessageFormats=true", dict(base, ruleset=ruleset, includeMessageFormats="true")),
        ("includeMessageFormats=maybe (invalid)",
         dict(base, ruleset=ruleset, includeMessageFormats="maybe")),
    ]
    for label, params in cases:
        status, result = rules(**params)
        if isinstance(result, int):
            print("  %-38s %s  %d rules" % (label, status, result))
        else:
            keys = sorted(result) if isinstance(result, dict) else result
            print("  %-38s %s  error keys=%s" % (label, status, keys))

    print()
    print("-- localisation (Accept-Language) --")
    status, en = client.get_json(url_for(
        host, "/api/rule", **{"api-version": CATALOGUE_API_VERSION, "ruleset": ruleset}))
    status_fr, fr = client.get_json(
        url_for(host, "/api/rule", **{"api-version": CATALOGUE_API_VERSION, "ruleset": ruleset}),
        headers={"Accept-Language": "fr"})
    if isinstance(en, list) and isinstance(fr, list) and en and fr:
        by_code = {r["code"]: r for r in fr}
        changed = [f for f in ("summary", "description", "howToFix", "guidanceUrl",
                               "severity", "primaryCategory")
                   if any(r.get(f) != by_code.get(r["code"], {}).get(f) for r in en)]
        print("  fields that differ under Accept-Language: fr -> %s" % (changed or "none"))
    status_rs, rs_fr = client.get_json(
        url_for(host, "/api/ruleset", **{"api-version": CATALOGUE_API_VERSION}),
        headers={"Accept-Language": "fr"})
    if isinstance(rs_fr, list):
        print("  ruleset names under fr: %s" % [r.get("name") for r in rs_fr])

    print()
    print("-- message templates --")
    status, body = client.get_json(url_for(host, "/api/rule", **{
        "api-version": CATALOGUE_API_VERSION, "ruleset": ruleset,
        "includeMessageFormats": "true"}))
    if isinstance(body, list):
        templates = [t for r in body for t in r.get("messageTemplates", [])]
        keys = collections.Counter()
        for t in templates:
            keys.update(t.keys())
        with_templates = sum(1 for r in body if r.get("messageTemplates"))
        print("  %d templates over %d/%d rules, fields=%s"
              % (len(templates), with_templates, len(body), dict(keys)))


def probe_negative(client: Advisor, host: str, ruleset: str) -> None:
    """Establish route existence and error shapes without invoking anything."""
    print()
    print("=" * 72)
    print("ROUTE AND ERROR SHAPES (read-only; nothing is submitted)")
    print("=" * 72)

    print("-- unauthenticated: what does the service say the audience is? --")
    for path in ("/api/rule", "/api/ruleset"):
        status, headers, _ = client.request(
            url_for(host, path, **{"api-version": CATALOGUE_API_VERSION}), authenticated=False)
        print("  %-28s %s  WWW-Authenticate=%s"
              % (path, status, headers.get("WWW-Authenticate")))

    print()
    print("-- methods other than GET on the catalogue routes --")
    for method in ("HEAD", "OPTIONS"):
        status, headers, _ = client.request(
            url_for(host, "/api/rule", **{"api-version": CATALOGUE_API_VERSION,
                                          "ruleset": ruleset}), method=method)
        print("  %-28s %s  Allow=%s" % (method + " /api/rule", status, headers.get("Allow")))

    print()
    print("-- analysis routes: existence probed by version and method, never invoked --")
    for path in ("/api/analyze", "/api/upload"):
        status_v2, _, body_v2 = client.request(
            url_for(host, path, **{"api-version": CATALOGUE_API_VERSION}))
        status_v1, headers_v1, _ = client.request(
            url_for(host, path, **{"api-version": ANALYSIS_API_VERSION}))
        code = None
        try:
            code = json.loads(body_v2)["error"]["code"]
        except Exception:
            pass
        print("  %-28s GET@%s -> %s (%s);  GET@%s -> %s Allow=%s"
              % (path, CATALOGUE_API_VERSION, status_v2, code,
                 ANALYSIS_API_VERSION, status_v1, headers_v1.get("Allow")))

    print()
    print("-- analysis status: reading a job that does not exist --")
    unknown = str(uuid.uuid4())
    zero = "00000000-0000-0000-0000-000000000000"
    cases = [
        ("unknown job id", unknown, ANALYSIS_API_VERSION,
         {"x-ms-correlation-id": str(uuid.uuid4())}),
        ("unknown job id, no headers", unknown, ANALYSIS_API_VERSION, {}),
        ("all-zeros job id", zero, ANALYSIS_API_VERSION, {}),
        ("non-GUID job id", "notaguid", ANALYSIS_API_VERSION, {}),
        ("unknown job id, wrong api-version", unknown, CATALOGUE_API_VERSION, {}),
    ]
    for label, job_id, version, headers_in in cases:
        status, headers, body = client.request(
            url_for(host, "/api/status/" + job_id, **{"api-version": version}),
            headers=headers_in)
        print("  %-36s %s  content-type=%s keys=%s bytes=%d"
              % (label, status, headers.get("Content-Type"), _json_keys(body), len(body)))


def _json_keys(body: bytes):
    try:
        return sorted(json.loads(body).keys())
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--region", action="append", default=[],
                        help="public-cloud geography (repeatable); default: all known")
    parser.add_argument("--host", action="append", default=[],
                        help="explicit advisor host, e.g. from an environment's "
                             "PowerAppsAdvisor runtime endpoint (repeatable)")
    parser.add_argument("--ruleset", default=os.environ.get("ADVISOR_RULESET",
                                                            SOLUTION_CHECKER_RULESET),
                        help="ruleset id or name to survey (default: Solution Checker)")
    parser.add_argument("--skip-negative", action="store_true",
                        help="skip the route and error-shape probes")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    hosts = {}
    for host in args.host:
        hosts[urllib.parse.urlsplit(host if "//" in host else "//" + host).netloc] = \
            urllib.parse.urlsplit(host if "//" in host else "//" + host).netloc
    for region in (args.region or ([] if args.host else REGIONS)):
        hosts[region] = HOST_TEMPLATE.format(region=region)
    if not hosts:
        parser.error("no hosts resolved")

    client = Advisor(get_token(), verbose=args.verbose)
    started = time.time()

    probe_catalogue(client, hosts, args.ruleset)
    first_host = next(iter(hosts.values()))
    probe_parameters(client, first_host, args.ruleset)
    if not args.skip_negative:
        probe_negative(client, first_host, args.ruleset)

    print()
    print("%d requests in %.1fs" % (client.calls, time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main())
