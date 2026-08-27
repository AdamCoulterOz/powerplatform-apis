#!/usr/bin/env python3
"""Extract an API inventory for one host from a directory of browser HAR captures.

The athena surface cannot be probed: it has no read operations that are also
safe, and provisioning one needs a Fabric workspace and a Fabric-to-Dataverse
connection. Recorded traffic is the alternative, and a better one -- a HAR of
the maker portal driving a real Link to Fabric shows the service's genuine
request and response bodies under its own client, which a synthetic probe never
could.

This is the tool that turned 18 HAR files into the inventory `oas/openapi.json`
was written from. It is generic: point it at any directory of HARs and give it a
host substring.

    har_extract.py ~/Desktop --match athenawebservice
    har_extract.py ~/Desktop --match athenawebservice --json inventory.json
    har_extract.py ~/Downloads --match api.bap.microsoft.com --bodies

Two things it does that a naive reader of a HAR gets wrong:

  * **Transport encoding.** A HAR entry may carry `response.content.encoding ==
    "base64"`, which is the *capture format*, not the API's. Decode it before
    reading, and do not conclude from it that the service returns base64. An
    earlier revision of the athena spec documented a plain JSON response as a
    base64-encoded string for exactly this reason.
  * **Redaction.** HARs of a real tenant are full of real ids, names and bearer
    tokens. Everything printed here is a shape, a count, a status, a hostname or
    a URL template with its GUIDs and query *values* stripped; `--bodies` prints
    body *keys* and value *types*, never values. Hostnames are printed intact
    because the route inventory is useless without them -- for this API they
    name the island scale unit, so redact them by hand before publishing.
    `--json` writes raw bodies and is intended for local analysis only -- never
    commit its output.

Nothing here touches the network, and it opens the HAR files read-only.
"""

from __future__ import annotations

import argparse
import base64
import collections
import glob
import json
import os
import re
import sys
import urllib.parse

GUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

# Headers worth keeping. Authorization is deliberately absent.
KEEP_REQUEST_HEADERS = (
    "accept",
    "content-type",
    "x-ms-client-request-id",
    "x-ms-client-session-id",
    "x-ms-correlation-id",
    "x-ms-organization-id",
    "x-d365-root-activity-id",
    "x-d365-session-id",
)
KEEP_RESPONSE_HEADERS = (
    "content-type",
    "location",
    "retry-after",
    "access-control-allow-methods",
    "access-control-allow-headers",
)


def load_har(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except Exception as exc:  # a directory of HARs usually has one dud in it
        print("  skip %-50s %s" % (os.path.basename(path), exc), file=sys.stderr)
        return None


def body_text(content):
    """Return the response body, undoing HAR's own base64 transport encoding."""
    text = (content or {}).get("text") or ""
    if (content or {}).get("encoding") == "base64":
        try:
            text = base64.b64decode(text).decode("utf-8", "replace")
        except Exception:
            pass
    return text


def entries(directory, match):
    for path in sorted(glob.glob(os.path.join(os.path.expanduser(directory), "*.har"))):
        har = load_har(path)
        if har is None:
            continue
        for entry in har.get("log", {}).get("entries", []):
            request = entry.get("request", {})
            url = request.get("url", "")
            if match not in url:
                continue
            response = entry.get("response", {}) or {}
            content = response.get("content") or {}
            yield {
                "file": os.path.basename(path),
                "started": entry.get("startedDateTime", ""),
                "method": request.get("method"),
                "url": url,
                "status": response.get("status"),
                "requestHeaders": pick(request.get("headers"), KEEP_REQUEST_HEADERS),
                "responseHeaders": pick(response.get("headers"), KEEP_RESPONSE_HEADERS),
                "requestBody": (request.get("postData") or {}).get("text", ""),
                "responseBody": body_text(content),
                "harEncoding": content.get("encoding"),
                "mimeType": content.get("mimeType"),
            }


def pick(headers, wanted):
    out = {}
    for header in headers or []:
        name = header.get("name", "").lower()
        if name in wanted:
            out[name] = header.get("value")
    return out


def template(url):
    """A redacted route template: GUIDs collapsed, query values dropped."""
    parsed = urllib.parse.urlparse(url)
    path = GUID.sub("{id}", parsed.path)
    keys = sorted(urllib.parse.parse_qs(parsed.query))
    return path, tuple(keys)


def shape(value, depth=0):
    """Describe a JSON value structurally. Never returns a scalar's value."""
    if isinstance(value, dict):
        if depth >= 3:
            return "{...}"
        return {k: shape(v, depth + 1) for k, v in sorted(value.items())}
    if isinstance(value, list):
        if not value:
            return []
        return [shape(value[0], depth + 1)]
    if value is None:
        return "null"
    return type(value).__name__


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory", help="Directory containing *.har files.")
    ap.add_argument("--match", required=True, help="Substring of the URL identifying the API (e.g. a hostname).")
    ap.add_argument("--bodies", action="store_true", help="Also print request/response body shapes per route (keys and types, no values).")
    ap.add_argument("--timeline", action="store_true", help="Print each capture's calls in order, to read the client's workflow.")
    ap.add_argument("--json", metavar="PATH", help="Write the full inventory, raw bodies included, for local analysis. Do not commit it.")
    args = ap.parse_args(argv)

    found = list(entries(args.directory, args.match))
    if not found:
        print("no entries matching %r under %s" % (args.match, args.directory))
        return 1

    hosts = collections.Counter(urllib.parse.urlparse(e["url"]).netloc for e in found)
    print("%d calls in %d captures, %d host(s)" % (
        len(found), len({e["file"] for e in found}), len(hosts)))
    for host, count in hosts.most_common():
        print("  %5d  %s" % (count, GUID.sub("{id}", host)))

    print("\nroutes")
    routes = collections.Counter()
    for e in found:
        path, keys = template(e["url"])
        routes[(e["method"], path, e["status"], keys)] += 1
    for (method, path, status, keys) in sorted(routes, key=lambda k: (k[1], k[0], k[2] or 0)):
        query = ("?" + "&".join(keys)) if keys else ""
        print("  %5d  %-7s %-4s %s%s" % (routes[(method, path, status, keys)], method, status, path, query))

    encodings = collections.Counter(e["harEncoding"] for e in found)
    if encodings.get("base64"):
        print("\n%d of %d response bodies were base64 in the capture and have been decoded."
              % (encodings["base64"], len(found)))
        print("That is the HAR's transport encoding. Do not document it as the API's.")

    if args.bodies:
        print("\nbody shapes")
        shapes = collections.defaultdict(lambda: {"request": set(), "response": set()})
        for e in found:
            if e["method"] == "OPTIONS":
                continue
            path, _ = template(e["url"])
            key = (e["method"], path)
            for which, raw in (("request", e["requestBody"]), ("response", e["responseBody"])):
                if not (raw or "").strip():
                    continue
                try:
                    shapes[key][which].add(json.dumps(shape(json.loads(raw)), sort_keys=True))
                except ValueError:
                    shapes[key][which].add('"<not json>"')
        for key in sorted(shapes):
            print("  %s %s" % key)
            for which in ("request", "response"):
                for variant in sorted(shapes[key][which]):
                    print("      %-8s %s" % (which, variant[:2000]))

    if args.timeline:
        print("\ntimeline")
        by_file = collections.defaultdict(list)
        for e in found:
            by_file[e["file"]].append(e)
        for name in sorted(by_file):
            print("  %s" % name)
            for e in sorted(by_file[name], key=lambda x: x["started"]):
                if e["method"] == "OPTIONS":
                    continue
                path, keys = template(e["url"])
                query = ("?" + "&".join(keys)) if keys else ""
                print("      %s %-7s %-4s %s%s" % (
                    e["started"][11:23], e["method"], e["status"], path, query))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(found, fh, indent=1, ensure_ascii=False)
        print("\nwrote %s -- contains raw bodies from a real tenant. Do not commit it." % args.json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
