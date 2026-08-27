#!/usr/bin/env python3
"""Assert the invariants the spec browser is entitled to rely on.

The browser consumes this corpus without defensive parsing, so anything it
would silently mis-render is a build failure here rather than a rendering
surprise there. Every check exists because a real violation shipped.

Run: scripts/conform.py [spec ...]      (default: every spec in specs.json)
"""
import json
import pathlib
import sys
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The evidence grades. In the extracted design a corpus declares its own
# vocabulary and this becomes agreement-with-declaration; until then the
# triple lives here, in one place, so generalising it is one edit.
GRADES = {"live", "pac-cli", "provider"}


def stale(value, known) -> str:
    """Failure text for an assertion whose expectation is *remembered* rather
    than derived from the document.

    Every other check here reads its answer out of the data and cannot be out
    of date. This one holds a literal, so when it fires there are two suspects,
    not one -- and the dangerous reading is the wrong one: a stale checker
    looks exactly like a data defect, and the corpus gets edited to satisfy it.
    Naming both suspects is what stops a correct value being "fixed" away.
    """
    return (f"{value!r} is not in the known grade set {sorted(known)}. "
            f"Either the value is wrong, or this checker predates a grade the "
            f"corpus now declares -- check which before editing the spec.")

failures: list[str] = []


def fail(spec: str, where: str, msg: str) -> None:
    failures.append(f"{spec}: {msg}\n    at {where}")


def walk(node, path, fn):
    fn(node, path)
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, f"{path}/{k}", fn)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", fn)


def resolve(doc, ref):
    if not ref.startswith("#/"):
        return None
    node = doc
    for tok in ref[2:].split("/"):
        tok = urllib.parse.unquote(tok).replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict) and tok in node:
            node = node[tok]
        elif isinstance(node, list) and tok.isdigit() and int(tok) < len(node):
            node = node[int(tok)]
        else:
            return None
    return node


def check(spec: str, doc: dict) -> None:
    # 1. x-source carries a grade, never prose.
    def grade(n, path):
        if isinstance(n, dict) and "x-source" in n:
            v = n["x-source"]
            if not isinstance(v, str) or v not in GRADES:
                shown = (v[:60] + "...") if isinstance(v, str) and len(v) > 60 else v
                fail(spec, path, "x-source " + stale(shown, GRADES))
    walk(doc, "", grade)

    # 2. x-notes: a string, or {note, source} with a known grade.
    def notes(n, path):
        if not (isinstance(n, dict) and "x-notes" in n):
            return
        v = n["x-notes"]
        if not isinstance(v, list):
            fail(spec, path, f"x-notes is {type(v).__name__}, expected a list")
            return
        for i, e in enumerate(v):
            at = f"{path}/x-notes[{i}]"
            if isinstance(e, str):
                continue
            if not isinstance(e, dict):
                fail(spec, at, f"note is {type(e).__name__}, expected string or object")
            elif not isinstance(e.get("note"), str) or not e["note"].strip():
                fail(spec, at, "note object has no non-empty 'note'")
            elif "source" in e and e["source"] not in GRADES:
                fail(spec, at, "note source " + stale(e["source"], GRADES))
    walk(doc, "", notes)

    # 3. Every local $ref resolves. An unresolvable one renders as a bare
    #    pointer with the content behind it gone.
    def refs(n, path):
        if isinstance(n, dict) and isinstance(n.get("$ref"), str):
            r = n["$ref"]
            if r.startswith("#/") and resolve(doc, r) is None:
                fail(spec, path, f"$ref does not resolve: {r}")
    walk(doc, "", refs)

    # 4. A key used as a node-level extension must not reappear at the
    #    document root or on info meaning something else. athena held a
    #    derivation paragraph under x-source, which would have rendered as
    #    a grade titled with the first line of the paragraph.
    node_level = set()

    def collect(n, path):
        if isinstance(n, dict) and path not in ("", "/info"):
            node_level.update(k for k in n if k.startswith("x-"))
    walk(doc, "", collect)
    # An extension this checker independently polices is safe at any scope: its
    # meaning is pinned by a rule rather than by where it sits, so the same key
    # at document level is the same extension applied more broadly. Everything
    # else is only a name, and a name reused at two scopes is the athena defect
    # -- x-source holding a grade on nodes and a paragraph of prose on info.
    #
    # This set is DERIVED from the checks above rather than listed: an extension
    # earns document scope by being validated, so adding a check extends it and
    # there is no second place to update.
    policed = {"x-source", "x-notes"}   # == the keys checks 1 and 2 walk
    for scope in ("", "/info"):
        holder = doc if scope == "" else doc.get("info", {})
        for k in holder:
            if k.startswith("x-") and k in node_level and k not in policed:
                fail(spec, f"{scope or '(root)'}/{k}",
                     f"{k} is also a node-level extension and nothing here validates its "
                     f"meaning, so the same name at two scopes can mean two things -- give "
                     f"the document-scoped one its own name, or add a check that pins it")

    # 5. x-probe-verified is a boolean. The string "false" is truthy.
    def verified(n, path):
        if isinstance(n, dict) and "x-probe-verified" in n:
            v = n["x-probe-verified"]
            if not isinstance(v, bool):
                fail(spec, path, f"x-probe-verified is {type(v).__name__} ({v!r}), expected boolean")
    walk(doc, "", verified)


SPEC_LINK = re.compile(r"\bspec:([A-Za-z0-9_-]+)(#/[^\s)\"']*)?")
MD_LINK = re.compile(r"\]\((?!https?://|#|mailto:|spec:)([^)]+)\)")


def targets(doc: dict) -> dict:
    """Everything a spec: fragment is allowed to name, read out of the spec."""
    tags = {t["name"] for t in doc.get("tags", []) if isinstance(t, dict) and "name" in t}
    schemas = set(doc.get("components", {}).get("schemas", {}))
    ops = set()
    for item in doc.get("paths", {}).values():
        for method, op in item.items():
            if method in ("get", "put", "post", "patch", "delete") and isinstance(op, dict):
                if isinstance(op.get("operationId"), str):
                    ops.add(op["operationId"])
    return {"resources": tags, "schemas": schemas, "operations": ops}


def check_links(spec: str, doc: dict, corpus: dict) -> None:
    """Cross-spec references must resolve, and must use the spec: scheme.

    A relative markdown link is the bug this exists for: ten of them shipped
    pointing outside the site, because a broken link renders exactly like a
    working one and nobody had followed one. Both halves are derived -- the
    catalogue and the specs are read here -- so neither can go stale.
    """
    def walk_strings(n, path=""):
        if isinstance(n, dict):
            for k, v in n.items():
                if isinstance(v, str):
                    at = f"{path}/{k}"
                    for rel in MD_LINK.findall(v):
                        if rel.startswith(("..", "/")) or rel.endswith((".md", ".json")):
                            fail(spec, at, f"relative link {rel!r}: cross-spec references "
                                           f"use the spec: scheme, which the app resolves; a "
                                           f"relative path resolves against the site and 404s")
                    for sid, frag in SPEC_LINK.findall(v):
                        if sid not in corpus:
                            fail(spec, at, f"spec:{sid} names no spec in specs.json "
                                           f"({', '.join(sorted(corpus))})")
                        elif frag:
                            kind, _, name = frag[2:].partition("/")
                            allowed = targets(corpus[sid])
                            if kind not in allowed:
                                fail(spec, at, f"spec:{sid}{frag}: fragment kind {kind!r} is not "
                                               f"one of {sorted(allowed)}")
                            elif urllib.parse.unquote(name) not in allowed[kind]:
                                fail(spec, at, f"spec:{sid}{frag}: no {kind[:-1]} named "
                                               f"{urllib.parse.unquote(name)!r} in {sid}")
                else:
                    walk_strings(v, f"{path}/{k}")
        elif isinstance(n, list):
            for i, v in enumerate(n):
                walk_strings(v, f"{path}[{i}]")
    walk_strings(doc)


def main() -> int:
    specs = sys.argv[1:] or [s["id"] for s in json.loads((ROOT / "specs.json").read_text())]
    corpus = {}
    for spec in specs:
        f = ROOT / spec / "oas" / "openapi.json"
        if not f.exists():
            failures.append(f"{spec}: no spec at {f.relative_to(ROOT)}")
            continue
        corpus[spec] = json.loads(f.read_text())

    for spec, doc in corpus.items():
        check(spec, doc)
        check_links(spec, doc, corpus)

    if failures:
        print(f"conformance: {len(failures)} violation(s)\n")
        for f_ in failures:
            print(f"  {f_}")
        return 1
    print(f"conformance: {len(specs)} specs, all invariants hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
