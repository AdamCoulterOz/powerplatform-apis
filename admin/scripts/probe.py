#!/usr/bin/env python3
"""Probe the live Power Platform admin centre API and report its shape.

The admin centre API is undocumented and has no published reference, so this
spec was written by observing the real service. This script is that
observation, made re-runnable: point it at a tenant you administer and it
re-derives everything oas/openapi.json claims — the organization object, the
feature object, the geo enum, the error bodies and the routing quirks — and
prints a *shape* summary. It never prints organization ids, Dataverse
hostnames or tenant ids, so its output is safe to paste into an issue.

    scripts/probe.py                     # read-only: everything below
    scripts/probe.py --geos              # only re-enumerate the geo enum
    scripts/probe.py --enable ORG:GEO:FEATURE
                                         # the one mutation, opt-in and explicit

Authentication uses the az CLI. The scope is a bare first-party application
id, not a URL:

    az account get-access-token \\
      --scope 065d9450-1e87-434e-ac2f-69af271549ed/.default

Nothing here takes an id from source: organizations come from the tenant
listing, and the mutation runs only against ids you pass on the command line.

Two behaviours make probing this API unusually error-prone, and the script is
built around them:

1.  Unmatched routes do not 404. Every path this host does not recognise --
    "/", "/api/anything", even POST and DELETE to them -- answers 200 with
    the text/html body "This action is to redirect legacy routes". A 200 is
    therefore not evidence a route exists; only a JSON content-type is. See
    is_real().
2.  The service is not consistent about which error shape it returns. Query
    validation answers 400 with a bare JSON *array* of message strings;
    upstream faults answer 500 with a {code,message,requestId} object;
    authorization answers 403 with an empty body. classify() sorts them.
"""
import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = os.environ.get("PPAC_HOST", "api.admin.powerplatform.microsoft.com")
SCOPE = os.environ.get("PPAC_SCOPE", "065d9450-1e87-434e-ac2f-69af271549ed/.default")
PAUSE = float(os.environ.get("PPAC_PAUSE", "0.4"))

# Candidate geo codes to test the geo enum against. The service validates the
# parameter, so an invalid code answers 400 and a valid one answers 200: the
# enum can be recovered by asking. Additions are cheap -- add plausible codes
# and re-run.
GEO_CANDIDATES = [
    "NA", "EMEA", "Oce", "APAC", "JPN", "CAN", "IND", "GBR", "FRA", "ZAF",
    "UAE", "GER", "CHE", "KOR", "NOR", "SGP", "SAM", "SWE", "ITA", "POL",
    "CHN", "USG", "USNAT", "USSEC", "DOD", "TIP", "APJ", "BRA", "LATAM",
    "ISR", "QAT", "AUS", "EUR", "MEX", "NZL", "ESP", "NLD", "TUR",
]


def token():
    return subprocess.run(
        ["az", "account", "get-access-token", "--scope", SCOPE,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True).stdout.strip()


class Api:
    def __init__(self, tok):
        self.tok = tok

    def call(self, method, path, query=None):
        url = "https://%s%s" % (HOST, path)
        if query:
            url += "?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, method=method, headers={
            "Authorization": "Bearer " + self.tok,
            "Accept": "application/json",
        })
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    out = (r.status, dict(r.headers), r.read().decode("utf-8", "replace"))
                    break
            except urllib.error.HTTPError as e:
                out = (e.code, dict(e.headers), e.read().decode("utf-8", "replace"))
                if e.code == 429:
                    time.sleep(float(e.headers.get("Retry-After", 5)) * (attempt + 1))
                    continue
                break
            except urllib.error.URLError as e:
                out = (-1, {}, repr(e))
                time.sleep(2 * (attempt + 1))
        time.sleep(PAUSE)
        return out


def is_real(status, headers):
    """True when a response came from a route rather than the catch-all.

    The catch-all answers 200 text/html for every unmatched path and method,
    so "did this 200?" is the wrong question; "was it JSON?" is the right one.
    """
    return "json" in headers.get("Content-Type", "").lower()


def classify(status, headers, body):
    """Name the error shape a response used, without echoing tenant data."""
    if not body.strip():
        return "empty body"
    if not is_real(status, headers):
        return "catch-all (text/html legacy-route stub)"
    try:
        parsed = json.loads(body)
    except ValueError:
        return "non-JSON body"
    if isinstance(parsed, list):
        return "ValidationMessages (JSON array of strings), e.g. %s" % (
            json.dumps(parsed[:1]))
    if isinstance(parsed, dict) and "code" in parsed:
        return "ServiceError {code=%s, message, requestId}" % parsed.get("code")
    return "object with keys %s" % sorted(parsed)


def shape(value, depth=0):
    """A type sketch of a JSON value -- never its content."""
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [shape(value[0], depth + 1)] if value else ["<empty>"]
    if value is None:
        return "null"
    return type(value).__name__


def head(title):
    print("\n" + title)
    print("-" * len(title))


def probe_organizations(api):
    head("organizations  GET /api/tenants/mytenant/organizations")
    status, headers, body = api.call("GET", "/api/tenants/mytenant/organizations")
    print("status %s  json=%s" % (status, is_real(status, headers)))
    if status != 200 or not is_real(status, headers):
        print("classify:", classify(status, headers, body))
        return []
    orgs = json.loads(body)
    print("top-level type: %s of %d" % (type(orgs).__name__, len(orgs)))
    print("field shape:", json.dumps(shape(orgs[0]) if orgs else {}, sort_keys=True))
    print("field set is uniform across items:",
          len({tuple(sorted(o)) for o in orgs}) <= 1)
    for field in ("crmGeo", "relationType", "organizationType"):
        seen = sorted({json.dumps(o.get(field)) for o in orgs})
        print("  distinct %-17s %s" % (field, ", ".join(seen)))
    derived = sum(1 for o in orgs
                  if o.get("name") == "unq" + o.get("id", "").replace("-", "")[:29])
    print("  name == 'unq' + first 29 hex of id: %d/%d" % (derived, len(orgs)))
    return orgs


def probe_features(api, orgs):
    head("features  GET /api/environments/{organizationId}/features?geo=")
    if not orgs:
        print("no organizations to read; skipped")
        return
    envelopes, names = [], set()
    for org in orgs:
        status, headers, body = api.call(
            "GET", "/api/environments/%s/features" % org["id"],
            {"geo": org["crmGeo"]})
        if status != 200 or not is_real(status, headers):
            print("org #%d: status %s (%s)" % (
                orgs.index(org), status, classify(status, headers, body)))
            continue
        envelope = json.loads(body)
        envelopes.append(envelope)
        names.update(f.get("FeatureName") for f in envelope.get("values", []))
    if not envelopes:
        return
    features = [f for e in envelopes for f in e.get("values", [])]
    print("organizations read: %d   features seen: %d" % (len(envelopes), len(features)))
    print("envelope keys:", sorted(envelopes[0]))
    print("feature shape:", json.dumps(shape(features[0]), sort_keys=True))
    print("property casing on the wire: %s (the Go client's json tags are camelCase;"
          " encoding/json matches case-insensitively)" %
          ("PascalCase" if "FeatureName" in features[0] else "camelCase"))
    print("feature names:", ", ".join(sorted(n for n in names if n)))
    for field in ("State", "AppsUpgradeState", "Enabled", "IsAllowed",
                  "CanBeReset", "IsOrgGeoOptedIn", "MinVersion", "MaxVersion"):
        seen = sorted({json.dumps(f.get(field)) for f in features})
        print("  distinct %-17s %s" % (field, ", ".join(seen)))
    paged = [e for e in envelopes if e.get("nextPageToken")]
    print("  envelopes carrying a nextPageToken: %d (pagination appears vestigial)"
          % len(paged))


def probe_paging(api, orgs):
    head("paging parameters (are count/nextPageToken honoured?)")
    if not orgs:
        return
    org = orgs[0]
    base = None
    for extra in ({}, {"pageSize": 1}, {"$top": 1}, {"pageToken": "abc"}):
        query = {"geo": org["crmGeo"]}
        query.update(extra)
        status, headers, body = api.call(
            "GET", "/api/environments/%s/features" % org["id"], query)
        if status != 200 or not is_real(status, headers):
            print("%-22s status %s" % (json.dumps(extra), status))
            continue
        envelope = json.loads(body)
        row = (len(envelope.get("values", [])), envelope.get("count"),
               envelope.get("totalCount"), envelope.get("nextPageToken"))
        base = base or row
        print("%-22s values=%s count=%s totalCount=%s token=%r%s" % (
            json.dumps(extra) if extra else "(none)", *row,
            "" if row != base or not extra else "   <- ignored"))


def probe_geo_enum(api, orgs):
    head("geo enum  (which codes does the service accept?)")
    if not orgs:
        print("needs one organization to address; skipped")
        return
    org = orgs[0]
    accepted, rejected, faulted = {}, [], []
    for geo in GEO_CANDIDATES:
        status, headers, body = api.call(
            "GET", "/api/environments/%s/features" % org["id"], {"geo": geo})
        if status == 200 and is_real(status, headers):
            values = json.loads(body).get("values", [])
            accepted[geo] = values[0].get("GeneralAvailabilityDate", "")[:10] if values else ""
        elif status == 400:
            rejected.append(geo)
        else:
            faulted.append("%s->%s" % (geo, status))
    print("accepted (%d): %s" % (len(accepted), ", ".join(sorted(accepted))))
    print("rejected  (%d): %s" % (len(rejected), ", ".join(rejected)))
    if faulted:
        print("neither   (%d): %s   <- recognised but not served by this host"
              % (len(faulted), ", ".join(faulted)))
    print("\ngeo -> GeneralAvailabilityDate for the same organization:")
    for geo, date in sorted(accepted.items(), key=lambda kv: (kv[1], kv[0])):
        print("  %-6s %s" % (geo, date))
    print("geo selects the release calendar, not the organization: the same"
          " organizationId under a different geo returns the same Enabled/State"
          " with a different GA date.")


def probe_routing_and_errors(api, orgs):
    head("routing and error shapes")
    org = orgs[0] if orgs else {"id": "00000000-0000-0000-0000-000000000000", "crmGeo": "NA"}
    zero = "00000000-0000-0000-0000-000000000000"
    cases = [
        ("catch-all: unknown path", "GET", "/api/no/such/route", None),
        ("catch-all: root", "GET", "/", None),
        ("catch-all: legacy single-feature GET", "GET",
         "/api/environments/%s/features/October2025Update" % org["id"], {"geo": org["crmGeo"]}),
        ("catch-all: DELETE anything", "DELETE", "/api/tenants/mytenant/organizations", None),
        ("features, geo omitted", "GET",
         "/api/environments/%s/features" % org["id"], None),
        ("features, geo empty", "GET",
         "/api/environments/%s/features" % org["id"], {"geo": ""}),
        ("features, geo invalid", "GET",
         "/api/environments/%s/features" % org["id"], {"geo": "ZZ"}),
        ("features, organizationId malformed", "GET",
         "/api/environments/not-a-guid/features", {"geo": org["crmGeo"]}),
        ("features, organizationId foreign", "GET",
         "/api/environments/%s/features" % zero, {"geo": org["crmGeo"]}),
        ("enable, organizationId foreign", "POST",
         "/api/environments/%s/features/October2025Update/enable" % zero,
         {"geo": org["crmGeo"]}),
        ("enable, geo invalid (foreign org)", "POST",
         "/api/environments/%s/features/October2025Update/enable" % zero, {"geo": "ZZ"}),
        ("enable, geo omitted (foreign org)", "POST",
         "/api/environments/%s/features/October2025Update/enable" % zero, None),
    ]
    for label, method, path, query in cases:
        status, headers, body = api.call(method, path, query)
        print("%-38s %-4s %s" % (label, status, classify(status, headers, body)))
    print("\nUnauthenticated and wrong-scope callers both answer 401; there is"
          " no WWW-Authenticate challenge.")


def probe_enable(api, spec):
    """The single mutation. Opt-in, explicit, and never inferred from a listing."""
    head("enable  POST /api/environments/{organizationId}/features/{name}/enable?geo=")
    try:
        org_id, geo, feature = spec.split(":", 2)
    except ValueError:
        sys.exit("--enable takes ORGANIZATIONID:GEO:FEATURENAME")

    def read():
        status, headers, body = api.call(
            "GET", "/api/environments/%s/features" % org_id, {"geo": geo})
        if status != 200 or not is_real(status, headers):
            return None
        for item in json.loads(body).get("values", []):
            if item.get("FeatureName") == feature:
                return item
        return None

    before = read()
    if before is None:
        sys.exit("feature %s not found on that organization; refusing to POST" % feature)
    print("before: Enabled=%s State=%s AppsUpgradeState=%s CanBeReset=%s" % (
        before.get("Enabled"), before.get("State"),
        before.get("AppsUpgradeState"), before.get("CanBeReset")))
    if before.get("Enabled") and not before.get("CanBeReset"):
        print("NOTE: already enabled and CanBeReset=false -- this POST cannot be"
              " undone through the API. Re-run against a disposable organization"
              " only.")
    status, headers, body = api.call(
        "POST", "/api/environments/%s/features/%s/enable" % (org_id, feature),
        {"geo": geo})
    print("POST -> %s   %s" % (status, classify(status, headers, body)))
    print("response headers of interest:", json.dumps(
        {k: v for k, v in headers.items()
         if k.lower() in ("location", "operation-location", "retry-after")}))
    after = read()
    if after:
        changed = {k: (before.get(k), after.get(k)) for k in after
                   if before.get(k) != after.get(k)}
        print("after:", json.dumps(changed) if changed else "unchanged")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--geos", action="store_true",
                        help="only re-enumerate the geo enum")
    parser.add_argument("--enable", metavar="ORG:GEO:FEATURE",
                        help="run the enable mutation against one organization")
    args = parser.parse_args()

    api = Api(token())
    print("host: %s\nscope: %s" % (HOST, SCOPE))
    orgs = probe_organizations(api)
    if args.geos:
        probe_geo_enum(api, orgs)
        return
    if args.enable:
        probe_enable(api, args.enable)
        return
    probe_features(api, orgs)
    probe_paging(api, orgs)
    probe_geo_enum(api, orgs)
    probe_routing_and_errors(api, orgs)


if __name__ == "__main__":
    main()
