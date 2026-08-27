#!/usr/bin/env python3
"""Live probe harness for the Dataverse Web API.

Everything here is generic: the environment host comes from the command line or
``DATAVERSE_HOST``, tokens come from the logged-in ``az`` CLI session, and the
output is a *shape* summary (status codes, header names, property names, option
set values) rather than tenant data.

    scripts/probe.py read  <host>            # read-only probes, safe anywhere
    scripts/probe.py enums <host>            # dump the option sets the spec pins
    scripts/probe.py write <host> [--prefix zzzprobedv]

``write`` creates a publisher and a couple of records, exercises the
create/update/associate/disassociate/delete paths, and removes everything it
made in a ``finally`` block. Point it only at a throwaway environment.
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

API = "v9.2"
SLEEP = 0.3  # be a polite neighbour; the service is shared

_tokens: dict[str, str] = {}


def token(host: str) -> str:
    """Access token for a per-environment Dataverse audience."""
    if host not in _tokens:
        _tokens[host] = subprocess.run(
            ["az", "account", "get-access-token", "--scope", f"https://{host}/.default",
             "--query", "accessToken", "-o", "tsv"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    return _tokens[host]


def call(host, method, path, body=None, headers=None):
    """Returns (status, headers, parsed-body-or-text)."""
    url = path if path.startswith("http") else f"https://{host}{path}"
    hdrs = {
        "Authorization": "Bearer " + token(host),
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    time.sleep(SLEEP)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read()
                return resp.status, dict(resp.headers), (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            if exc.code == 429 and attempt < 3:
                time.sleep(float(exc.headers.get("Retry-After", 5)))
                continue
            try:
                parsed = json.loads(raw)
            except ValueError:
                parsed = raw.decode(errors="replace")[:500]
            return exc.code, dict(exc.headers), parsed
    raise RuntimeError("retries exhausted")


def shape(value, depth=0):
    """Property names and JSON types, never values."""
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in sorted(value.items())} if depth < 2 else "{...}"
    if isinstance(value, list):
        return [shape(value[0], depth + 1)] if value else []
    return type(value).__name__


def report(label, status, headers=None, body=None, keys=None):
    line = f"{label:<52} {status}"
    if headers:
        seen = [h for h in ("OData-EntityId", "Location", "Preference-Applied", "Retry-After",
                            "WWW-Authenticate", "401_error_reason")
                if any(k.lower() == h.lower() for k in headers)]
        if seen:
            line += "   hdrs=" + ",".join(seen)
    print(line)
    if keys and isinstance(body, dict):
        print("      keys:", ", ".join(k for k in sorted(body) if k.startswith("@") or k in keys))
    if isinstance(body, dict) and "error" in body:
        print("      error.code:", body["error"].get("code"))


# --------------------------------------------------------------------------- read


def probe_read(host):
    print("== envelope, metadata, paging ==")
    st, hd, bd = call(host, "GET", f"/api/data/{API}/WhoAmI")
    report("GET WhoAmI", st, hd, bd, keys={"UserId", "BusinessUnitId", "OrganizationId"})

    st, hd, bd = call(host, "GET",
                      f"/api/data/{API}/EntityDefinitions(LogicalName='account')"
                      "?$select=PrimaryIdAttribute,LogicalCollectionName")
    report("GET EntityDefinitions(account) $select", st, hd, bd,
           keys={"MetadataId", "PrimaryIdAttribute", "LogicalCollectionName"})

    st, hd, bd = call(host, "GET",
                      f"/api/data/{API}/EntityDefinitions(LogicalName='account')/Attributes"
                      "?$select=LogicalName&$top=3")
    rows = len(bd.get("value", [])) if isinstance(bd, dict) else 0
    print(f"{'GET .../Attributes $top=3':<52} {st}   rows={rows}  "
          f"(metadata endpoints ignore $top)")
    if rows:
        types = sorted({r.get("@odata.type") for r in bd["value"] if r.get("@odata.type")})
        print("      @odata.type discriminators:", len(types))

    st, hd, bd = call(host, "GET",
                      f"/api/data/{API}/EntityDefinitions(LogicalName='account')"
                      "?$expand=OneToManyRelationships,ManyToManyRelationships,ManyToOneRelationships")
    if st == 200:
        for rel in ("OneToManyRelationships", "ManyToOneRelationships", "ManyToManyRelationships"):
            entries = bd.get(rel) or []
            print(f"      {rel}: {len(entries)} entries, keys={sorted(entries[0])[:6] if entries else []}")

    pref = ('odata.include-annotations="Microsoft.Dynamics.CRM.totalrecordcount,'
            'Microsoft.Dynamics.CRM.totalrecordcountlimitexceeded"')
    for table, key in (("roles", "roleid"), ("stringmaps", "stringmapid")):
        st, hd, bd = call(host, "GET",
                          f"/api/data/{API}/{table}?$count=true&$select={key}&$top=1",
                          headers={"Prefer": pref})
        if st == 200:
            print(f"      {table}: @odata.count={bd.get('@odata.count')} "
                  f"totalrecordcount={bd.get('@Microsoft.Dynamics.CRM.totalrecordcount')} "
                  f"limitexceeded={bd.get('@Microsoft.Dynamics.CRM.totalrecordcountlimitexceeded')}")

    st, hd, bd = call(host, "GET", f"/api/data/{API}/roles?$select=roleid",
                      headers={"Prefer": "odata.maxpagesize=3"})
    print(f"{'GET roles Prefer: odata.maxpagesize=3':<52} {st}   "
          f"rows={len(bd.get('value', []))} nextLink={'@odata.nextLink' in bd}")

    print("\n== admin/ALM collections ==")
    for label, path in (
        ("solutions ($expand=publisherid)",
         f"/api/data/{API}/solutions?$expand=publisherid&$orderby=createdon desc&$top=1"),
        ("publishers", f"/api/data/{API}/publishers?$top=1"),
        ("systemusers (+roles)",
         f"/api/data/{API}/systemusers?$select=applicationid,systemuserid,fullname,isdisabled,"
         "deletedstate,_businessunitid_value"
         "&$expand=systemuserroles_association($select=roleid,name,_businessunitid_value)&$top=1"),
        ("roles", f"/api/data/{API}/roles?$select=roleid,name,_businessunitid_value&$top=1"),
        ("businessunits (root)",
         f"/api/data/{API}/businessunits?$select=businessunitid,name&$filter=parentbusinessunitid eq null"),
        ("environmentvariabledefinitions",
         f"/api/data/{API}/environmentvariabledefinitions?$select=schemaname,type,secretstore&$top=1"),
        ("environmentvariablevalues",
         f"/api/data/{API}/environmentvariablevalues?$select=schemaname,value&$top=1"),
        ("asyncoperations", f"/api/data/{API}/asyncoperations?$top=1&$orderby=createdon desc"),
        ("organizations (v9.0)", "/api/data/v9.0/organizations"),
        ("RetrieveSettingList() (v9.0)", "/api/data/v9.0/RetrieveSettingList()"),
    ):
        st, hd, bd = call(host, "GET", urllib.parse.quote(path, safe="/?$=&,'()"))
        extra = ""
        if st == 200 and isinstance(bd, dict):
            rows = bd.get("value") or bd.get("SettingDetailCollection")
            if isinstance(rows, list):
                extra = f"   rows={len(rows)} cols={len(rows[0]) if rows else 0}"
        print(f"GET {label:<48} {st}{extra}")

    print("\n== error shapes ==")
    zero = "00000000-0000-0000-0000-000000000001"
    for label, method, path in (
        ("record not found", "GET", f"/api/data/{API}/accounts({zero})"),
        ("entity metadata not found", "GET", f"/api/data/{API}/EntityDefinitions(LogicalName='zzznope')"),
        ("unknown entity set", "GET", f"/api/data/{API}/zzznopes"),
        ("unknown property in $select", "GET", f"/api/data/{API}/publishers?$select=zzznope"),
        ("delete missing publisher", "DELETE", f"/api/data/{API}/publishers({zero})"),
        ("unsupported api version", "GET", "/api/data/v9.3/publishers?$top=1"),
        ("missing api version", "GET", "/api/data/"),
    ):
        st, hd, bd = call(host, method, urllib.parse.quote(path, safe="/?$=&,'()"))
        code = bd.get("error", {}).get("code") if isinstance(bd, dict) else None
        envelope = "OData error" if code else ("non-OData" if isinstance(bd, dict) else "empty")
        print(f"{label:<52} {st}   {envelope} {code or ''}")


# --------------------------------------------------------------------------- enums


OPTION_SETS = [
    ("environmentvariabledefinition", "type", "PicklistAttributeMetadata"),
    ("environmentvariabledefinition", "secretstore", "PicklistAttributeMetadata"),
    ("asyncoperation", "statecode", "StateAttributeMetadata"),
    ("asyncoperation", "statuscode", "StatusAttributeMetadata"),
    ("systemuser", "accessmode", "PicklistAttributeMetadata"),
    ("systemuser", "deletedstate", "PicklistAttributeMetadata"),
]


def probe_enums(host):
    for entity, attribute, cast in OPTION_SETS:
        path = (f"/api/data/{API}/EntityDefinitions(LogicalName='{entity}')"
                f"/Attributes(LogicalName='{attribute}')/Microsoft.Dynamics.CRM.{cast}"
                "?$select=LogicalName&$expand=OptionSet($select=Options)")
        st, _, bd = call(host, "GET", urllib.parse.quote(path, safe="/?$=&,'()"))
        if st != 200:
            print(f"{entity}.{attribute}: {st}")
            continue
        options = (bd.get("OptionSet") or {}).get("Options", [])
        pairs = [(o["Value"], ((o.get("Label") or {}).get("UserLocalizedLabel") or {}).get("Label"))
                 for o in options]
        print(f"{entity}.{attribute}: {pairs}")


# --------------------------------------------------------------------------- write


def probe_write(host, prefix):
    """Create-update-delete probes. Everything created is named with `prefix`."""
    created_publishers, created_accounts, created_contacts = [], [], []
    try:
        print("== publishers ==")
        st, hd, bd = call(host, "POST", f"/api/data/{API}/publishers", {
            "uniquename": prefix,
            "friendlyname": prefix + " probe",
            "customizationprefix": prefix[:8],
            "customizationoptionvalueprefix": 72345,
        })
        report("POST publishers", st, hd, bd)
        entity_id = next((v for k, v in hd.items() if k.lower() == "odata-entityid"), "")
        publisher_id = entity_id.rsplit("(", 1)[-1].rstrip(")") if entity_id else None
        if publisher_id:
            created_publishers.append(publisher_id)
            print("      OData-EntityId parsed ->", "guid" if len(publisher_id) == 36 else publisher_id)

        st, hd, bd = call(host, "POST", f"/api/data/{API}/publishers", {
            "uniquename": prefix,
            "friendlyname": prefix + " duplicate",
            "customizationprefix": prefix[:8] + "2",
            "customizationoptionvalueprefix": 72346,
        })
        report("POST publishers (duplicate uniquename)", st, hd, bd)

        st, hd, bd = call(host, "POST", f"/api/data/{API}/publishers",
                          {"friendlyname": prefix + " nameless"})
        report("POST publishers (no uniquename)", st, hd, bd)

        if publisher_id:
            st, hd, bd = call(host, "PATCH", f"/api/data/{API}/publishers({publisher_id})",
                              {"description": "probe"})
            report("PATCH publishers", st, hd, bd)
            st, hd, bd = call(host, "PATCH", f"/api/data/{API}/publishers({publisher_id})",
                              {"description": "probe representation"},
                              headers={"Prefer": "return=representation"})
            report("PATCH publishers Prefer: return=representation", st, hd, bd)

        print("\n== records, upsert and relationships ==")
        st, hd, bd = call(host, "POST", f"/api/data/{API}/accounts",
                          {"name": prefix + "-account"},
                          headers={"Prefer": "return=representation"})
        report("POST accounts Prefer: return=representation", st, hd, bd)
        if isinstance(bd, dict) and bd.get("accountid"):
            created_accounts.append(bd["accountid"])

        st, hd, bd = call(host, "POST", f"/api/data/{API}/contacts", {"lastname": prefix + "-contact"})
        report("POST contacts", st, hd, bd)
        entity_id = next((v for k, v in hd.items() if k.lower() == "odata-entityid"), "")
        contact_id = entity_id.rsplit("(", 1)[-1].rstrip(")") if entity_id else None
        if contact_id:
            created_contacts.append(contact_id)

        if created_accounts and contact_id:
            account_id = created_accounts[0]
            st, hd, bd = call(host, "PATCH", f"/api/data/{API}/accounts({account_id})",
                              {"primarycontactid@odata.bind": f"/contacts({contact_id})"})
            report("PATCH accounts (@odata.bind lookup)", st, hd, bd)

            st, hd, bd = call(host, "POST",
                              f"/api/data/{API}/accounts({account_id})/contact_customer_accounts/$ref",
                              {"@odata.id": f"https://{host}/api/data/{API}/contacts({contact_id})"})
            report("POST .../$ref (associate)", st, hd, bd)

            st, hd, bd = call(host, "GET",
                              f"/api/data/{API}/accounts({account_id})/contact_customer_accounts/$ref")
            report("GET .../$ref", st, hd, bd)

            st, hd, bd = call(host, "DELETE",
                              f"/api/data/{API}/accounts({account_id})"
                              f"/contact_customer_accounts({contact_id})/$ref")
            report("DELETE .../{related}/$ref (disassociate)", st, hd, bd)

            # PUT-style upsert against an id the caller chose.
            st, hd, bd = call(host, "PATCH", f"/api/data/{API}/accounts({account_id})",
                              {"name": prefix + "-account-2"},
                              headers={"If-Match": "*"})
            report("PATCH If-Match:* (update only)", st, hd, bd)
            st, hd, bd = call(host, "PATCH", f"/api/data/{API}/accounts({'0' * 8}-0000-0000-0000-{'0' * 12})",
                              {"name": prefix + "-upsert"}, headers={"If-Match": "*"})
            report("PATCH missing id If-Match:*", st, hd, bd)

        print("\n== solution staging ==")
        st, hd, bd = call(host, "POST", f"/api/data/{API}/StageSolution",
                          {"CustomizationFile": "bm90LWEtc29sdXRpb24="})
        report("POST StageSolution (invalid package)", st, hd, bd)
        if isinstance(bd, dict) and "StageSolutionResults" in bd:
            print("      StageSolutionResults keys:", sorted(bd["StageSolutionResults"]))
    finally:
        print("\n== cleanup ==")
        for account_id in created_accounts:
            st, _, _ = call(host, "DELETE", f"/api/data/{API}/accounts({account_id})")
            print(f"DELETE accounts -> {st}")
        for contact_id in created_contacts:
            st, _, _ = call(host, "DELETE", f"/api/data/{API}/contacts({contact_id})")
            print(f"DELETE contacts -> {st}")
        for publisher_id in created_publishers:
            st, _, _ = call(host, "DELETE", f"/api/data/{API}/publishers({publisher_id})")
            print(f"DELETE publishers -> {st}")
        st, _, bd = call(host, "GET",
                         urllib.parse.quote(f"/api/data/{API}/publishers?$select=publisherid"
                                            f"&$filter=startswith(uniquename,'{prefix}')", safe="/?$=&,'()"))
        left = len(bd.get("value", [])) if isinstance(bd, dict) else "?"
        print(f"publishers still matching prefix: {left}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=["read", "enums", "write"])
    parser.add_argument("host", nargs="?", default=os.environ.get("DATAVERSE_HOST"),
                        help="environment host, e.g. contoso.crm.dynamics.com")
    parser.add_argument("--prefix", default=os.environ.get("PROBE_PREFIX", "zzzprobedv"))
    args = parser.parse_args()
    if not args.host:
        parser.error("pass a host or set DATAVERSE_HOST")

    if args.mode == "read":
        probe_read(args.host)
    elif args.mode == "enums":
        probe_enums(args.host)
    else:
        probe_write(args.host, args.prefix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
