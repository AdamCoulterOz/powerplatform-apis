#!/usr/bin/env python3
"""Extract the BAPI surface from the Terraform provider's Go client.

BAPI has no published reference, so the spec was bootstrapped from the one
well-tested client in the open: microsoft/terraform-provider-power-platform.
Since its client-library refactor, every BAPI call lives in one package
(internal/clients/bapi) behind one harness, which makes the shape mechanical:

    apiUrl := &url.URL{ Scheme: constants.HTTPS, Host: client.host(),
        Path: fmt.Sprintf("/providers/.../environments/%s", environmentId) }
    values.Add(constants.API_VERSION_PARAM, constants.BAP_API_VERSION)
    _, err := client.Api.Execute(ctx, client.scopes(), "GET", apiUrl.String(),
        nil, body, []int{http.StatusOK}, &responseDto)

Unlike ppapi (whose generator re-runs over a refreshed docs mirror, with hand
edits carried in enrichment.json), bapi's oas/openapi.json is owned directly:
this script seeded it once and now serves as a drift audit. Run

    extract.py <provider-checkout>            # print the extracted inventory
    extract.py <provider-checkout> --check    # diff it against oas/openapi.json

--check exits non-zero when the provider knows operations the spec lacks, or
the spec claims provider-sourced operations that no longer exist. Curated
content (names, descriptions, tags, schema polish) lives only in the spec.

Execute sites whose URL is not path-built (lifecycle polls that GET a
Location header) are out of scope; the spec documents those through the
LifecycleOperation schema on their initiating 202 responses.
"""
import json
import pathlib
import re
import sys

GO_SCALARS = {
    "string": {"type": "string"},
    "bool": {"type": "boolean"},
    "int": {"type": "integer"},
    "int32": {"type": "integer", "format": "int32"},
    "int64": {"type": "integer", "format": "int64"},
    "float32": {"type": "number", "format": "float"},
    "float64": {"type": "number", "format": "double"},
    "time.Time": {"type": "string", "format": "date-time"},
    "any": {},
    "interface{}": {},
}

HTTP_STATUS = {
    "StatusOK": 200, "StatusCreated": 201, "StatusAccepted": 202,
    "StatusNoContent": 204, "StatusBadRequest": 400, "StatusUnauthorized": 401,
    "StatusForbidden": 403, "StatusNotFound": 404, "StatusMethodNotAllowed": 405,
    "StatusConflict": 409, "StatusPreconditionFailed": 412,
    "StatusInternalServerError": 500, "StatusServiceUnavailable": 503,
}

FUNC_RE = re.compile(r"^func (?:\(client \*Client\) )?([A-Za-z0-9_]+)\(", re.M)
EXECUTE_RE = re.compile(
    r'client\.Api\.(Execute|ExecuteWithoutRetry)\(\s*ctx,\s*client\.scopes\(\),\s*"(\w+)",\s*(\S+?),\s*'
    r'(\S+),\s*([^,]+?),\s*((?:\[\]int\{[^}]*\})|[A-Za-z0-9_]+),\s*([^)]+?)\)',
    re.S,
)


def load_constants(provider: pathlib.Path) -> dict:
    """NAME = \"value\" pairs from internal/constants/constants.go."""
    text = (provider / "internal/constants/constants.go").read_text(encoding="utf-8")
    return dict(re.findall(r"^\t([A-Z][A-Z0-9_]*)\s*=\s*\"([^\"]*)\"", text, re.M))


def split_functions(text: str):
    starts = list(FUNC_RE.finditer(text))
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        yield m.group(1), text[m.start():end]


def camel(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9]", " ", name).split()[-1]
    return name[0].lower() + name[1:]


def parse_path_expr(expr: str):
    """A path expression -> (template, [param names]).

    Handles "literal", fmt.Sprintf("...%s...", args...), and
    "literal" + var concatenation.
    """
    expr = expr.strip().rstrip(",")
    lit = re.match(r'^"([^"]*)"$', expr)
    if lit:
        return lit.group(1), []
    m = re.match(r'^fmt\.Sprintf\("([^"]*)"\s*,\s*(.+)\)$', expr, re.S)
    if m:
        template, args = m.group(1), [camel(a) for a in m.group(2).split(",")]
        out, i = "", 0
        for piece in re.split(r"(%s|%d)", template):
            if piece in ("%s", "%d"):
                out += "{" + args[i] + "}"
                i += 1
            else:
                out += piece
        return out, args
    concat = re.match(r'^"([^"]*)"\s*\+\s*([A-Za-z0-9_.]+)$', expr)
    if concat:
        param = camel(concat.group(2))
        return concat.group(1) + "{" + param + "}", [param]
    return None, []


def path_builders(text: str, constants: dict):
    """String-returning helper funcs that build a URL -> name: (template, params, query).

    Matches both `return fmt.Sprintf("...", ...)` and the url.URL + values.Add
    + `return apiUrl.String()` shape; query defaults declared inside the
    builder ride along with its template.
    """
    builders = {}
    for name, body in split_functions(text):
        sig = body.split("{", 1)[0]
        if ") string" not in sig:
            continue
        template, params = None, []
        pm = re.search(r"Path:\s*(.+?)\n", body)
        if pm:
            template, params = parse_path_expr(pm.group(1))
        else:
            rm = re.search(r'return (fmt\.Sprintf\("[^"]*"\s*,\s*.+?\))\s*$', body, re.M | re.S)
            if rm:
                template, params = parse_path_expr(rm.group(1))
                if template:
                    template = re.sub(r"^https?://\{[^}]+\}", "", template)
        if not template:
            continue
        query = {}
        for qm in re.finditer(r'values\.Add\((.+?),\s*(.+?)\)\n', body):
            key_expr, val_expr = qm.group(1).strip(), qm.group(2).strip()
            key = {"constants.API_VERSION_PARAM": "api-version"}.get(key_expr) or key_expr.strip('"')
            if val_expr.startswith("constants."):
                query[key] = constants.get(val_expr.split(".", 1)[1])
            elif val_expr.startswith('"'):
                query[key] = val_expr.strip('"')
            else:
                query[key] = None
        builders[name] = (template, params, query)
    return builders


def resolve_statuses(segment: str, expr: str):
    expr = expr.strip()
    if not expr.startswith("[]int{"):
        m = re.search(rf"{re.escape(expr)}\s*:?=\s*\[\]int\{{([^}}]*)\}}", segment)
        expr = "[]int{" + (m.group(1) if m else "") + "}"
    statuses = []
    for s in expr[len("[]int{"):-1].split(","):
        s = s.strip().rsplit(".", 1)[-1]
        if s in HTTP_STATUS:
            statuses.append(HTTP_STATUS[s])
        elif s.isdigit():
            statuses.append(int(s))
    return sorted(statuses)


def resolve_var_type(segment: str, expr: str):
    """Map an Execute body/response argument back to its declared Go type."""
    expr = expr.strip().lstrip("&")
    if expr in ("nil", ""):
        return None
    var = expr.split(".")[0].split("[")[0]
    for pat in (
        rf"{var}\s*:=\s*&?(map\[[^\]{{]+\][A-Za-z0-9_.\[\]]*)\{{",
        rf"{var}\s*:=\s*&?(\[\][A-Za-z0-9_.]+)\{{",
        rf"{var}\s*:=\s*&?([A-Za-z0-9_.]+)\{{",
        rf"var {var}\s+([\[\]A-Za-z0-9_.]+)",
        rf"\b{var}\s+([\[\]*A-Za-z0-9_.]+)[,)]",
    ):
        m = re.search(pat, segment)
        if m:
            return m.group(1).lstrip("*")
    return None


def parse_operations(path: pathlib.Path, constants: dict):
    """All Execute sites in one ops file, each with the URL built nearest above it."""
    text = path.read_text(encoding="utf-8")
    builders = path_builders(text, constants)
    ops = []
    for func_name, body in split_functions(text):
        for em in EXECUTE_RE.finditer(body):
            retry, method, url_arg, _hdr, body_arg, statuses_expr, resp_arg = em.groups()
            segment = body[: em.start()]

            template, params, base_query = None, [], {}
            url_var = url_arg.split(".")[0]
            helper = re.search(rf"{url_var}\s*:?=\s*client\.(\w+)\(", segment)
            if helper and helper.group(1) in builders:
                template, params, base_query = builders[helper.group(1)]
            elif (hb := re.search(rf"{url_var}\s*:?=\s*helpers\.\w+Url\(\s*client\.host\(\),\s*(.+?),\s*values\)", segment, re.S)):
                template, params = parse_path_expr(hb.group(1))
            elif re.search(rf"{url_var}\s*:?=\s*&url\.URL\{{", segment):
                pm = None
                for pm in re.finditer(r"Path:\s*(.+?)\n", segment):
                    pass  # keep the last Path assignment before this Execute
                if pm:
                    template, params = parse_path_expr(pm.group(1))
            if template is None:
                continue  # Location-header polls etc.: not path-addressable
            if not template.startswith("/"):
                template = "/" + template

            query = dict(base_query)
            q_segment = segment[segment.rfind("Path:"):] if "Path:" in segment else segment
            for qm in re.finditer(r'values\.Add\((.+?),\s*(.+?)\)\n', q_segment):
                key_expr, val_expr = qm.group(1).strip(), qm.group(2).strip()
                key = {"constants.API_VERSION_PARAM": "api-version"}.get(key_expr) or key_expr.strip('"')
                if val_expr.startswith("constants."):
                    val = constants.get(val_expr.split(".", 1)[1])
                elif val_expr.startswith('"'):
                    val = val_expr.strip('"')
                else:
                    val = None  # runtime value (e.g. caller-supplied api-version)
                query[key] = val

            resp_type = resolve_var_type(body, resp_arg)
            if resp_type is None:
                after = body[em.end():]
                um = re.search(r"json\.Unmarshal\(response\.BodyAsBytes,\s*&(\w+)\)", after)
                if um:
                    resp_type = resolve_var_type(body, um.group(1))

            ops.append({
                "file": path.name, "func": func_name,
                "method": method, "path": template, "pathParams": params,
                "query": query, "statuses": resolve_statuses(body, statuses_expr),
                "requestType": resolve_var_type(body, body_arg),
                "responseType": resp_type,
                "noRetry": retry == "ExecuteWithoutRetry",
            })
    return ops


def go_type_to_schema(go_type: str):
    go_type = go_type.strip()
    if go_type.startswith("*"):
        return go_type_to_schema(go_type[1:])
    if go_type.startswith("[]"):
        return {"type": "array", "items": go_type_to_schema(go_type[2:])}
    if go_type.startswith("map["):
        return {"type": "object", "additionalProperties": True}
    if go_type in GO_SCALARS:
        return dict(GO_SCALARS[go_type])
    return {"$ref": f"#/components/schemas/{go_type}"}


def parse_schemas(pkg_dir: pathlib.Path):
    """Every struct with json tags in the package -> name: schema."""
    schemas = {}
    struct_re = re.compile(r"^type ([A-Za-z0-9_]+) struct \{\n(.*?)^\}", re.M | re.S)
    field_re = re.compile(r'^\t([A-Za-z0-9_]+)\s+([\[\]\*A-Za-z0-9_.{}\[\]]+)\s+`json:"([^"]+)"`', re.M)
    for f in sorted(pkg_dir.glob("*.go")):
        if f.name.endswith("_test.go"):
            continue
        for name, body in struct_re.findall(f.read_text(encoding="utf-8")):
            props = {}
            for _go_name, go_type, tag in field_re.findall(body):
                json_name = tag.split(",")[0]
                if json_name == "-":
                    continue
                props[json_name] = go_type_to_schema(go_type)
            schemas[name] = {"type": "object", "properties": props} if props else {"type": "object"}
    return schemas


def extract(provider: pathlib.Path):
    pkg = provider / "internal/clients/bapi"
    if not pkg.is_dir():
        sys.exit(f"not a provider checkout (missing {pkg})")
    constants = load_constants(provider)
    ops = []
    for f in sorted(pkg.glob("*.go")):
        if f.name.endswith("_test.go") or f.name in ("client.go", "doc.go") or f.name.endswith("_dtos.go"):
            continue
        ops.extend(parse_operations(f, constants))
    return {"operations": ops, "schemas": parse_schemas(pkg)}


def normalize(path: str) -> str:
    """Path template with positional placeholders so param names don't matter."""
    return re.sub(r"\{[^}]+\}", "{}", path)


def is_provider_claim(op: dict) -> bool:
    """Whether the spec attributes this operation to the provider.

    This used to be "anything not hand-marked x-provider-unsourced", which was a
    remembered fact rather than a derived one, and it went stale the moment the
    spec outgrew its seed: 64 operations arrived from the PowerShell module, the
    admin centre bundles and live traffic, nobody marked them, and the audit
    reported all of them as operations the provider had "no longer". A check that
    is permanently red is a check nobody reads.

    The spec already records where each operation came from. x-source names the
    STRONGEST source, so any grade other than "provider" means something better
    than the provider witnesses it -- that is not a provider claim. bapi's
    baseline was seeded from the provider by this script and carries no x-source,
    so an ungraded operation still counts as a provider claim. The explicit
    marker is kept and still wins, for the cases where that baseline assumption
    is wrong."""
    if op.get("x-provider-unsourced"):
        return False
    return op.get("x-source", "provider") == "provider"


def check(provider: pathlib.Path) -> int:
    spec_path = pathlib.Path(__file__).resolve().parent.parent / "oas" / "openapi.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    inventory = extract(provider)

    extracted = {(o["method"].lower(), normalize(o["path"])) for o in inventory["operations"]}
    documented = set()      # every operation the spec describes, whatever its source
    claimed = set()         # the subset the spec attributes to the provider
    for p, item in spec.get("paths", {}).items():
        for verb, op in item.items():
            if verb not in ("get", "put", "post", "patch", "delete"):
                continue
            documented.add((verb, normalize(p)))
            if is_provider_claim(op):
                claimed.add((verb, normalize(p)))

    # The two questions are not symmetric, and answering them with one set was
    # the second defect. "Is anything the provider calls undocumented?" is about
    # the WHOLE spec -- an operation the provider has and ps-admin also witnesses
    # is graded ps-admin, and asking it of the provider-attributed subset alone
    # would report it missing while it sits in the file. "Does the spec attribute
    # something to the provider that the provider no longer has?" is about the
    # attributed subset only.
    missing = sorted(extracted - documented)
    stale = sorted(claimed - extracted)
    for verb, p in missing:
        print(f"MISSING from spec: {verb.upper()} {p}")
    for verb, p in stale:
        print(f"STALE in spec (no longer in provider): {verb.upper()} {p}")
    if not missing and not stale:
        print(f"in sync: {len(documented)} operations documented, "
              f"{len(claimed)} attributed to the provider, "
              f"{len(extracted)} found in the checkout")
    return 1 if (missing or stale) else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--check"]
    if not args:
        sys.exit("usage: extract.py <path-to-terraform-provider-power-platform> [--check]")
    provider_path = pathlib.Path(args[0]).expanduser()
    if "--check" in sys.argv:
        sys.exit(check(provider_path))
    print(json.dumps(extract(provider_path), indent=1))
