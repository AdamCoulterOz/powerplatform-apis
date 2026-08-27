#!/usr/bin/env python3
"""Check each spec against recorded responses from the live service.

`conform.py` asks whether the corpus is internally consistent. This asks the
harder question: does it match what the service actually returned.

It exists because it was needed. `bapi` `LocationProperties` carried
`x-probe-verified: true` while omitting `hasFirstReleaseIslandAvailableForProvisioning`,
a field present on every row of a real response -- the probe ran, the capture
existed, and the schema was written from the Terraform provider's model of the
API instead. Nothing detected the gap for months, because a schema missing a
field looks exactly like a schema.

The assertion is one-directional: **every field observed on the wire must be
declared**. The converse is not required -- a spec may legitimately model
fields a single tenant's response does not exercise (another SKU, another
cloud, an $expand). Absence of evidence is not a defect; contradicted evidence
is.

Evidence lives in `<spec>/evidence/`, with a `manifest.json` binding each file
to the schema it should satisfy. That directory is deliberately NOT `captures/`,
which is git-ignored because raw probe output is full of tenant data. Publishing
a clean capture by adding an exception to that ignore rule would leave the next
person to judge, by eye, whether the following one is safe. So `evidence/` is a
separate channel with its own contract -- nothing enters it that identifies a
tenant -- and this script enforces that rather than trusting it.

Run: scripts/verify_captures.py [spec ...]
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
failures: list[str] = []


def pick(node, path):
    """Walk a manifest path, where '*' fans out over a list."""
    if not path:
        return [node] if isinstance(node, dict) else []
    head, rest = path[0], path[1:]
    if head == "*":
        if not isinstance(node, list):
            return []
        return [x for item in node for x in pick(item, rest)]
    if isinstance(node, dict) and head in node:
        return pick(node[head], rest)
    return []


def declared_fields(spec: dict, name: str) -> set[str] | None:
    s = spec.get("components", {}).get("schemas", {}).get(name)
    if s is None:
        return None
    fields = set(s.get("properties", {}))
    for sub in s.get("allOf", []) or []:
        if isinstance(sub, dict):
            if "properties" in sub:
                fields |= set(sub["properties"])
            ref = sub.get("$ref", "")
            if ref.startswith("#/components/schemas/"):
                inner = declared_fields(spec, ref.rsplit("/", 1)[-1])
                if inner:
                    fields |= inner
    return fields


# Markers that must never appear in published evidence. This list is REMEMBERED,
# not derived, so it is the one thing here that can go stale: it cannot know about
# an identifier nobody has thought of. It is a floor, not a guarantee -- read a
# file before adding it.
TENANT_MARKERS = ("adamcoulter", "a098ad4f-34e6", "Bearer ", "eyJ0eXAi", "@")


_gated: set[pathlib.Path] = set()


def redaction_gate(spec_id: str, path: pathlib.Path) -> None:
    if path in _gated:
        return
    _gated.add(path)
    text = path.read_text()
    hits = sorted({m for m in TENANT_MARKERS if m in text})
    if hits:
        failures.append(
            f"{spec_id}: {path.name} contains {hits} -- evidence/ is published, so it must "
            f"not identify a tenant. Redact it, or leave it in the git-ignored captures/.")


def check(spec_id: str) -> int:
    cap_dir = ROOT / spec_id / "evidence"
    manifest = cap_dir / "manifest.json"
    if not manifest.exists():
        return 0
    spec = json.loads((ROOT / spec_id / "oas" / "openapi.json").read_text())
    entries = json.loads(manifest.read_text())

    # Gate every file in the directory, not only the ones a manifest names.
    # Checking the listed ones is a presence question answered from a list, and
    # a file nobody listed is exactly the file that slips through -- which it
    # did: a provenance document carrying a tenant id was copied in beside the
    # bodies and was not covered until this loop existed.
    for f in sorted(cap_dir.iterdir()):
        if f.is_file() and f.name != "manifest.json":
            redaction_gate(spec_id, f)
    for e in entries:
        body_path = cap_dir / e["file"]
        if not body_path.exists():
            failures.append(f"{spec_id}: manifest names {e['file']}, which is not in evidence/")
            continue
        redaction_gate(spec_id, body_path)
        body = json.loads(body_path.read_text())
        items = pick(body, e["items"])
        if not items:
            failures.append(f"{spec_id}: {e['file']} path {e['items']} selected nothing "
                            f"-- the capture's shape changed, or the path is wrong")
            continue
        declared = declared_fields(spec, e["schema"])
        if declared is None:
            failures.append(f"{spec_id}: manifest names schema {e['schema']}, which the spec does not define")
            continue
        observed = set()
        for item in items:
            observed |= set(item)
        undeclared = observed - declared
        if undeclared:
            failures.append(
                f"{spec_id}: {e['schema']} does not declare {sorted(undeclared)}, "
                f"observed on the wire in {e['file']} ({len(items)} item(s))")
    return len(entries)


def main() -> int:
    specs = sys.argv[1:] or [s["id"] for s in json.loads((ROOT / "specs.json").read_text())]
    checked = sum(check(s) for s in specs)
    covered = [s for s in specs if (ROOT / s / "evidence" / "manifest.json").exists()]
    if failures:
        print(f"captures: {len(failures)} contradiction(s)\n")
        for f in failures:
            print(f"  {f}")
        return 1
    # Say what was NOT covered: a green run over two specs must not read as ten.
    print(f"captures: {checked} assertion(s) across {len(covered)} spec(s) "
          f"({', '.join(covered) or 'none'}); no capture evidence for "
          f"{', '.join(s for s in specs if s not in covered) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
