#!/usr/bin/env python3
"""Reverse-engineer a single OpenAPI 3.0.3 spec from the docs/ mirror.

One spec for the whole API, not one per namespace: Microsoft's namespaces are
transport and org-chart artifacts, and the resources people actually manage
span them (the billing policy to environment edge alone lives in two). Tags
carry the logical-resource taxonomy from catalogue.py; each operation keeps
x-ms-namespace as provenance of where Microsoft filed it.

The Learn pages are generated from an internal OpenAPI, so their tables invert
mechanically: URI Parameters (Name|In|Required|Type|Description), Request Body
(Name|Required|Type|Description), Responses (Name|Type|Description) and
Definitions sections that self-declare Object or Enumeration. Known docs bugs
handled: constraints concatenated without separators, and Swagger-2 formData
parameters (converted to multipart request bodies).

Schema names collide across namespaces. Identical bodies merge; conflicting
bodies keep the plain name for the most common variant and qualify the rest as
{Name}_{namespace}, rewriting refs within that namespace. Models referenced but
never defined become x-stub schemas so the spec always validates structurally.

Output: oas/openapi.json. Deterministic; no timestamps. Unofficial and not
verified against the service; a map, not a contract.
"""
import json
import pathlib
import re

from catalogue import LOGICAL, logical_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "oas"

ENRICH_PATH = ROOT / "enrichment.json"
ENRICH = {"operations": {}, "tags": {}}
if ENRICH_PATH.exists():
    ENRICH = json.loads(ENRICH_PATH.read_text(encoding="utf-8"))
ENRICH_USED = set()

SCALARS = {
    "string": {"type": "string"},
    "file": {"type": "string", "format": "binary"},
    "boolean": {"type": "boolean"},
    "object": {"type": "object"},
    "number": {"type": "number"},
    "integer": {"type": "integer"},
}


def parse_constraints(text):
    """The docs concatenate constraints without separators (e.g. 'minLength: 10maxLength: 64pattern: /x/').
    Slice values between key positions instead of trusting any delimiter."""
    keys = list(re.finditer(r"(minLength|maxLength|minimum|maximum|pattern|format|default):\s*", text))
    out = {}
    for i, km in enumerate(keys):
        end = keys[i + 1].start() if i + 1 < len(keys) else len(text)
        val = text[km.end():end].strip()
        key = km.group(1)
        if key in ("minLength", "maxLength", "minimum", "maximum"):
            nm = re.match(r"\d+", val)
            if nm:
                out[key] = int(nm.group(0))
        elif key == "pattern":
            out[key] = val[1:-1] if len(val) > 1 and val.startswith("/") and val.endswith("/") else val
        elif val:
            out[key] = val
    return out


def with_desc(schema, desc):
    """Attach a description without putting siblings next to a $ref (illegal in OAS 3.0)."""
    if not desc:
        return schema
    if "$ref" in schema:
        return {"allOf": [schema], "description": desc}
    schema.setdefault("description", desc)
    return schema


def parse_type(raw, schemas_seen):
    """Map a docs type cell to an OAS schema fragment.

    The docs express several shapes that are not named models and must not
    become $refs: inline enums (`enum:<br>- A<br>- B`), dictionaries
    (`<string, FieldError>`), formatted scalars and arrays (`string (uuid)`,
    `string[] (uri)`), and unnamed nested objects the docs mislabel with the
    page's own uid (`api.powerplatform.com...`)."""
    raw = (raw or "").strip().replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    parts = [p.strip() for p in re.split(r"<br\s*/?>", raw) if p.strip()]
    base = parts[0] if parts else "string"

    # inline enum: "enum:" then one "- value" per <br> line
    if re.match(r"^enum\b", base, re.I):
        values = [re.sub(r"^-\s*", "", p).strip() for p in parts[1:]]
        values = [v for v in values if v]
        return {"type": "string", "enum": values} if values else {"type": "string"}

    constraints = parse_constraints(" ".join(parts[1:]))

    # dictionary / map: <keyType, valueType> -> additionalProperties
    mm = re.match(r"^<\s*\w+\s*,\s*(.+?)\s*>$", base)
    if mm:
        return {"type": "object", "additionalProperties": parse_type(mm.group(1), schemas_seen)}

    # unnamed nested object the docs labelled with the page's own uid
    if base.startswith("api.powerplatform.com") or base.startswith("api."):
        schema = {"type": "object"}
        schema.update(constraints)
        return schema

    # array of formatted scalars: "string[] (uri)"
    am = re.match(r"^([a-z]+)\[\]\s*\(([\w-]+)\)$", base)
    if am:
        item = dict(SCALARS.get(am.group(1), {"type": "string"}))
        item["format"] = am.group(2)
        return {"type": "array", "items": item}

    # formatted scalar: "string (uuid)"
    fm = re.match(r"^([a-z]+)\s*\(([\w-]+)\)$", base)
    if fm:
        schema = dict(SCALARS.get(fm.group(1), {"type": "string"}))
        schema["format"] = fm.group(2)
        schema.update(constraints)
        return schema
    if base.endswith("[]"):
        return {"type": "array", "items": parse_type(base[:-2], schemas_seen)}
    if base in SCALARS:
        schema = dict(SCALARS[base])
        schema.update(constraints)
        return schema
    name = re.sub(r"[^\w.-]", "", base)
    if not name:
        return {"type": "string"}
    schemas_seen.add(name)
    return {"$ref": f"#/components/schemas/{name}"}


def parse_table(lines, start):
    i = start
    while i < len(lines) and not lines[i].startswith("|"):
        if lines[i].startswith("#"):
            return [], [], start
        i += 1
    if i >= len(lines):
        return [], [], start
    header = [c.strip() for c in lines[i].strip("|").split("|")]
    i += 2
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        rows.append([c.strip() for c in lines[i].strip("|").split("|")])
        i += 1
    return rows, header, i


def section(lines, heading):
    for i, line in enumerate(lines):
        if line.strip() == heading:
            return i
    return -1


def col(header, name, default):
    """Index of a column by (case-insensitive) header name. The docs tables vary
    in shape - request bodies are sometimes Name|Type|Description and sometimes
    Name|Required|Type|Description - so columns must be found by name, never by
    fixed position."""
    low = [h.strip().lower() for h in header]
    return low.index(name) if name in low else default


def parse_definitions(lines, schemas, seen):
    di = section(lines, "## Definitions")
    if di < 0:
        return
    i = di + 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and line.strip() != "## Definitions":
            break
        hm = re.match(r"^### ([\w.-]+)", line)
        if hm:
            current = hm.group(1)
            kind = None
            desc = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith(("|", "###", "## ")):
                t = lines[j].strip()
                if t in ("Object", "Enumeration"):
                    kind = t
                elif t:
                    desc.append(t)
                j += 1
            rows, header, _ = parse_table(lines, j)
            if kind == "Enumeration" or (header and header[0] == "Value"):
                schema = {"type": "string", "enum": [r[0] for r in rows if r and r[0]]}
            else:
                ti = col(header, "type", 1)
                di = col(header, "description", 2)
                props = {}
                for r in rows:
                    if len(r) < 2 or not r[0]:
                        continue
                    pname = r[0].strip("`")
                    ptype = r[ti] if ti < len(r) else "string"
                    pdesc = r[di] if di < len(r) else ""
                    props[pname] = with_desc(parse_type(ptype, seen), pdesc)
                schema = {"type": "object", "properties": props}
            if desc:
                schema["description"] = " ".join(desc)
            if current not in schemas:
                schemas[current] = schema
            i = j
        i += 1


def camel(slug):
    parts = re.split(r"[^0-9A-Za-z]+", slug)
    return parts[0].lower() + "".join(p.title() for p in parts[1:] if p)


_VERBS = {"Create", "Read", "List", "Update", "Delete", "Add", "Remove", "Link", "Unlink", "Enable",
          "Disable", "Copy", "Restore", "Recover", "Reset", "Execute", "Get", "Set", "Install",
          "Uninstall", "Download", "Upload", "Generate", "Submit", "Refresh", "Convert", "Provision",
          "Validate", "Apply", "Assign", "Query", "Search", "Cancel", "Approve", "Reject", "Modify"}
_QUAL = {"By", "For", "With", "Across"}  # introduces a variant qualifier clause
_NAME_KEEP = {"Set Bot As Quarantined", "Set Bot As Unquarantined"}


def verb_last(name):
    """Reorder a name noun-first with the verb last (Dataverse Link, Management
    Settings Create). A variant qualifier clause introduced by By/For/With/Across
    is pulled to a trailing parenthetical so families sort together, e.g.
    Rule Assignments List (By Environment Id)."""
    if name in _NAME_KEEP:
        return name
    m = re.match(r"^(.*?)(\s*\([^)]*\))?$", name)
    core, paren = m.group(1).strip(), (m.group(2) or "").strip()
    words = core.split()
    qual = ""
    for i, w in enumerate(words):
        if i > 0 and w in _QUAL:
            qual = " ".join(words[i:])
            words = words[:i]
            break
    if len(words) >= 2 and words[0] in _VERBS:
        words = words[1:] + [words[0]]
    parts = [" ".join(words)]
    if qual:
        parts.append(f"({qual})")
    if paren:
        parts.append(paren)
    return " ".join(p for p in parts if p).strip()


def parse_operation(f, paths, schemas, seen):
    ns, group = f.parent.parent.name, f.parent.name
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    reqs = re.findall(r"```http\s*\n(GET|POST|PATCH|PUT|DELETE)\s+(\S+)", text)
    if not reqs:
        return
    method, url = reqs[0]
    um = re.match(r"https://api\.powerplatform\.com([^?]+)\??(.*)$", url)
    if not um:
        return
    path = um.group(1)
    vm = re.search(r"api-version=([\w.-]+)", um.group(2))
    title_m = re.search(r"^# (.+?)\s*$", text, re.M)
    title = title_m.group(1) if title_m else f.stem
    desc_m = re.search(r"^# .+?\n+([^\n#|>`-][^\n]{5,300})", text)
    preview = "(preview)" in text[:2000].lower()

    params = []
    form_props = {}
    form_req = []
    pi = section(lines, "## URI Parameters")
    if pi >= 0:
        rows, header, _ = parse_table(lines, pi + 1)
        ci_in, ci_req = col(header, "in", 1), col(header, "required", 2)
        ci_type, ci_desc = col(header, "type", 3), col(header, "description", 4)
        for r in rows:
            if len(r) <= ci_type or not r[0]:
                continue
            name = r[0].strip("`")
            where = (r[ci_in] if ci_in < len(r) else "query") or "query"
            required = ci_req < len(r) and r[ci_req].lower() == "true"
            desc = r[ci_desc] if ci_desc < len(r) else ""
            if where == "formData":
                # Swagger-2 leftover in the docs: model as multipart/form-data body
                form_props[name] = with_desc(parse_type(r[ci_type], seen), desc)
                if required:
                    form_req.append(name)
                continue
            p = {
                "name": name,
                "in": where,
                "required": required,
                "schema": parse_type(r[ci_type], seen),
            }
            if desc:
                p["description"] = desc
            if name == "api-version" and vm:
                p["schema"]["default"] = vm.group(1)
            params.append(p)

    body = None
    bi = section(lines, "## Request Body")
    if bi >= 0:
        rows, header, _ = parse_table(lines, bi + 1)
        ti = col(header, "type", 2)
        di = col(header, "description", ti + 1)
        ri_req = col(header, "required", -1)
        props, req = {}, []
        for r in rows:
            if len(r) <= ti or not r[0] or "." in r[0]:
                continue  # dotted rows re-expand referenced models
            pname = r[0].strip("`")
            desc = r[di] if di < len(r) else ""
            props[pname] = with_desc(parse_type(r[ti], seen), desc)
            if 0 <= ri_req < len(r) and r[ri_req].lower() == "true":
                req.append(pname)
        if props:
            schema = {"type": "object", "properties": props}
            if req:
                schema["required"] = req
            body = {"required": True, "content": {"application/json": {"schema": schema}}}
    if form_props and body is None:
        fschema = {"type": "object", "properties": form_props}
        if form_req:
            fschema["required"] = form_req
        body = {"required": True, "content": {"multipart/form-data": {"schema": fschema}}}

    responses = {}
    ri = section(lines, "## Responses")
    if ri >= 0:
        rows, header, _ = parse_table(lines, ri + 1)
        for r in rows:
            if not r or not r[0]:
                continue
            cm = re.match(r"(\d{3})", r[0])
            if not cm:
                continue
            full_desc = r[2] if len(r) > 2 else ""
            resp = {"description": (full_desc.split("<br>")[0] if full_desc else r[0])}
            if len(r) > 1 and r[1]:
                resp["content"] = {"application/json": {"schema": parse_type(r[1], seen)}}
            # a few pages document response headers as free text in the description
            # cell: "...Headers<br><br>Operation-Location: string"
            hm2 = re.search(r"Headers(?:<br\s*/?>)+(.+)$", full_desc)
            if hm2:
                headers = {}
                for hname, htype in re.findall(r"([A-Za-z][\w-]*):\s*(\w+)", hm2.group(1)):
                    headers[hname] = {"schema": {"type": htype if htype in ("string", "integer", "boolean") else "string"}}
                if headers:
                    resp["headers"] = headers
            responses[cm.group(1)] = resp
    if not responses:
        responses["200"] = {"description": "OK"}

    parse_definitions(lines, schemas, seen)

    logical, _facet = logical_for(ns, group, f.stem)
    # baseline: docs titles are "{Group} - {Operation}"; keep only the operation half
    summary = re.sub(r"\s*\(preview\)\s*$", "", title, flags=re.I)
    if " - " in summary:
        summary = summary.split(" - ", 1)[1].strip()
    summary = verb_last(summary)
    key = f"{ns}/{group}/{f.stem}"
    enrich = ENRICH.get("operations", {}).get(key)
    tags = [logical]
    description = desc_m.group(1).strip() if desc_m else ""
    notes = []
    if enrich:
        ENRICH_USED.add(key)
        summary = enrich.get("summary", summary)
        tags = enrich.get("tags", tags)
        description = enrich.get("description", description)
        notes = enrich.get("notes", [])
        # add/override response bodies, headers and status codes from shapes
        # discovered against the live API (the docs model many of these wrongly)
        for code, ov in enrich.get("responses", {}).items():
            resp = responses.get(code, {"description": ov.get("description", code)})
            if ov.get("description"):
                resp["description"] = ov["description"]
            if ov.get("schema"):
                sch = ov["schema"]
                if isinstance(sch, dict) and set(sch) == {"$ref"} and not sch["$ref"].startswith("#"):
                    sch = {"$ref": f"#/components/schemas/{sch['$ref']}"}
                resp["content"] = {"application/json": {"schema": sch}}
            if ov.get("headers"):
                resp.setdefault("headers", {}).update(ov["headers"])
            responses[code] = resp
    op = {
        "operationId": f"{camel(ns)}_{camel(f.stem)}",
        "tags": tags,
        "summary": summary,
        "parameters": params,
        "responses": responses,
        "x-ms-namespace": f"{ns}/{group}",
    }
    if notes:
        # verified doc-vs-reality findings: structured on x-notes, and folded
        # into the description as a single blockquote (one callout, bulleted)
        # so a spec browser renders one note box rather than several.
        op["x-notes"] = notes
        lines = ["> **Verified against the live API**", ">"]
        lines += [f"> - {n}" for n in notes]
        block = "\n".join(lines)
        description = (description + "\n\n" + block).strip() if description else block
    if description:
        op["description"] = description
    if preview:
        op["x-ms-preview"] = True
    if body:
        op["requestBody"] = body
    op["externalDocs"] = {
        "url": f"https://learn.microsoft.com/en-us/rest/api/power-platform/{ns}/{group}/{f.stem}"}
    paths.setdefault(path, {})[method.lower()] = op


def rewrite_refs(node, rename):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                name = v.rsplit("/", 1)[-1]
                if name in rename:
                    node[k] = f"#/components/schemas/{rename[name]}"
            else:
                rewrite_refs(v, rename)
    elif isinstance(node, list):
        for item in node:
            rewrite_refs(item, rename)


def main():
    OUT.mkdir(exist_ok=True)
    for stale in OUT.glob("*.json"):
        stale.unlink()

    namespaces = sorted({p.parent.parent.name for p in DOCS.glob("*/*/*.md")})
    staged = {}  # ns -> (paths, schemas, seen)
    for ns in namespaces:
        paths, schemas, seen = {}, {}, set()
        for f in sorted(DOCS.glob(f"{ns}/*/*.md")):
            parse_operation(f, paths, schemas, seen)
        if paths:
            staged[ns] = (paths, schemas, seen)

    # merge schemas: identical bodies share the plain name; conflicting bodies
    # keep the plain name for the most common variant, the rest get {Name}_{ns}
    variants = {}  # name -> canon_body -> [ns, ...]
    for ns, (_p, schemas, _s) in staged.items():
        for name, schema in schemas.items():
            canon = json.dumps(schema, sort_keys=True)
            variants.setdefault(name, {}).setdefault(canon, []).append(ns)

    global_schemas = {}
    renames = {ns: {} for ns in staged}
    conflicts = 0
    for name, bodies in sorted(variants.items()):
        groups = sorted(bodies.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        keep_canon = groups[0][0]
        global_schemas[name] = json.loads(keep_canon)
        for canon, ns_list in groups[1:]:
            conflicts += 1
            qualified = f"{name}_{sorted(ns_list)[0]}"
            global_schemas[qualified] = json.loads(canon)
            for ns in ns_list:
                renames[ns][name] = qualified

    all_paths = {}
    all_seen = set()
    for ns, (paths, _schemas, seen) in staged.items():
        if renames[ns]:
            rewrite_refs(paths, renames[ns])
        all_seen |= seen
        for path, ops in paths.items():
            all_paths.setdefault(path, {}).update(ops)

    for name in sorted(all_seen):
        global_schemas.setdefault(name, {
            "type": "object", "x-stub": True,
            "description": "Referenced by the docs but not defined on any page."})

    # curated schema renames: the docs auto-name some models generically (the
    # OData envelope item type becomes "Value"); rename them meaningfully here.
    applied = {}
    for old, cfg in ENRICH.get("schemas", {}).items():
        if old not in global_schemas:
            print(f"WARNING: enrichment schema '{old}' matches no schema")
            continue
        cfg = {"rename": cfg} if isinstance(cfg, str) else dict(cfg)
        new = cfg.get("rename", old)
        if new != old and new in global_schemas:
            print(f"WARNING: enrichment schema rename target '{new}' already exists; keeping '{old}'")
            new = old
        target = global_schemas.pop(old)
        if cfg.get("notes"):
            target["x-notes"] = cfg["notes"]
            block = " ".join(cfg["notes"])
            target["description"] = (target.get("description", "") + " Note (verified against the live API): " + block).strip()
        if cfg.get("description"):
            target["description"] = cfg["description"]
        global_schemas[new] = target
        if new != old:
            applied[old] = new
    if applied:
        rewrite_refs(all_paths, applied)
        rewrite_refs(global_schemas, applied)

    # schemas for live-discovered shapes the docs do not model (or model wrongly)
    for name, schema in ENRICH.get("addSchemas", {}).items():
        if name in global_schemas and not global_schemas[name].get("x-stub"):
            print(f"WARNING: addSchemas '{name}' overwrites an existing schema")
        global_schemas[name] = schema

    tag_facets = {}
    for f in DOCS.glob("*/*/*.md"):
        res, facet = logical_for(f.parent.parent.name, f.parent.name, f.stem)
        tag_facets.setdefault(res, set()).add(facet)
    used_tags = sorted({t for ops in all_paths.values() for op in ops.values() for t in op["tags"]})
    tags = []
    for t in used_tags:
        desc = ENRICH.get("tags", {}).get(t, {}).get("description") \
            or "; ".join(sorted(tag_facets.get(t, {"unmapped"})))
        tags.append({"name": t, "description": desc})

    versions = sorted({p["schema"]["default"]
                       for ops in all_paths.values() for op in ops.values()
                       for p in op.get("parameters", [])
                       if p.get("name") == "api-version" and "default" in p.get("schema", {})})

    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Power Platform API",
            "version": versions[-1] if versions else "unversioned",
            "description": "Unofficial. Reverse-engineered from the public Microsoft Learn "
                           "documentation (learn.microsoft.com) and not verified against the live "
                           "service. Tags group operations by logical resource; x-ms-namespace "
                           "records the namespace Microsoft files each under.",
            "x-api-versions": versions,
        },
        "servers": [{"url": "https://api.powerplatform.com"}],
        "security": [{"azure_auth": ["https://api.powerplatform.com/.default"]}],
        "tags": tags,
        "paths": {k: all_paths[k] for k in sorted(all_paths)},
        "components": {
            "securitySchemes": {
                "azure_auth": {
                    "type": "oauth2",
                    "description": "Microsoft Entra ID OAuth2",
                    "flows": {"authorizationCode": {
                        "authorizationUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                        "tokenUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                        "scopes": {"https://api.powerplatform.com/.default": "Power Platform API"},
                    }},
                }
            },
            "schemas": {k: global_schemas[k] for k in sorted(global_schemas)},
        },
    }
    (OUT / "openapi.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8")
    stale = set(ENRICH.get("operations", {})) - ENRICH_USED
    for k in sorted(stale):
        print(f"WARNING: enrichment key matches no operation (docs renamed?): {k}")
    total_ops = sum(len(v) for v in all_paths.values())
    print(f"enrichment: {len(ENRICH_USED)}/{total_ops} operations enriched, {len(stale)} stale keys")
    stubs = sum(1 for s in global_schemas.values() if s.get("x-stub"))
    nops = sum(len(v) for v in all_paths.values())
    print(f"oas/openapi.json: {nops} operations, {len(tags)} logical-resource tags, "
          f"{len(global_schemas)} schemas ({stubs} stubs, {conflicts} cross-namespace conflicts qualified)")

    try:
        from openapi_spec_validator import validate  # type: ignore
        validate(json.loads((OUT / "openapi.json").read_text(encoding="utf-8")))
        print("spec validates (openapi-spec-validator)")
    except ImportError:
        print("openapi-spec-validator not installed; structural validation skipped")


if __name__ == "__main__":
    main()
