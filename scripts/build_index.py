#!/usr/bin/env python3
"""Generate index.json: which spec owns each operation, schema and tag id.

A bare deep link -- `#/<kind>/<id>` with no spec -- resolves against the
catalogue's declared default. When the default has no such id the browser
consults this index rather than searching the corpus, which would let a
crafted link plus an attacker-supplied catalogue fan a reader's browser out
across arbitrary origins.

Values are always lists, including the single-owner case. Ids do collide
across specs -- 14 of 1249 remain ambiguous even after the default resolves
first -- and a scalar shape would encode this corpus's collision profile as
of today into the format.

Generated, never edited: it is derived from the specs on every run, so a
renamed tag or a new spec is picked up rather than remembered.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KINDS = ("operations", "schemas", "resources")


def build() -> dict:
    cat = json.loads((ROOT / "specs.json").read_text())
    entries = cat["specs"] if isinstance(cat, dict) else cat
    index = {k: {} for k in KINDS}
    for e in entries:
        doc = json.loads((ROOT / e["url"]).read_text())
        sid = e["id"]
        for item in doc.get("paths", {}).values():
            for method, op in item.items():
                if method in ("get", "put", "post", "patch", "delete") and isinstance(op, dict):
                    if isinstance(op.get("operationId"), str):
                        index["operations"].setdefault(op["operationId"], []).append(sid)
        for name in doc.get("components", {}).get("schemas", {}):
            index["schemas"].setdefault(name, []).append(sid)
        for tag in doc.get("tags", []):
            if isinstance(tag, dict) and "name" in tag:
                index["resources"].setdefault(tag["name"], []).append(sid)
    return {k: {i: sorted(set(v)) for i, v in sorted(index[k].items())} for k in KINDS}


if __name__ == "__main__":
    idx = build()
    out = ROOT / "index.json"
    if "--check" in sys.argv:
        current = json.loads(out.read_text()) if out.exists() else None
        if current != idx:
            print("index.json is stale; run scripts/build_index.py")
            raise SystemExit(1)
        print("index.json is current")
    else:
        out.write_text(json.dumps(idx, indent=1, sort_keys=True) + "\n")
        for k in KINDS:
            amb = sum(1 for v in idx[k].values() if len(v) > 1)
            print(f"  {k}: {len(idx[k])} ids, {amb} owned by more than one spec")
