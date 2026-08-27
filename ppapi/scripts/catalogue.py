#!/usr/bin/env python3
"""Build a machine-readable operation catalogue from the docs/ mirror.

Every operation page yields one row: namespace, group, operation, method,
path, api-version, preview flag, introduction date (from the what's-new
changelog when announced there), and a logical-resource remap that groups
Microsoft's UI-shaped namespaces into the resources they actually manage.
Groups not yet in the map fall through as '(unmapped)' rather than failing,
so new namespaces surface in the diff instead of breaking the mirror job.

Outputs: catalogue/catalogue.json and catalogue/catalogue.csv. Deterministic;
no timestamps in file content (the git history carries the dates).
"""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "catalogue"

LOGICAL = {
    # "Environment" = convergent resource lifecycle; "Environment Operations" =
    # ephemeral / non-convergent actions and reference-data reads. Two groups
    # (provisioning, failover) are mixed and split per-operation in logical_for.
    ("environmentmanagement", "environments"): ("Environment", "Read model"),
    ("environmentmanagement", "environment-delete"): ("Environment", "Delete"),
    ("environmentmanagement", "modify-environment-sku"): ("Environment", "SKU"),
    ("environmentmanagement", "environment-managed-governance"): ("Environment", "Managed governance"),
    ("environmentmanagement", "environment-management-settings"): ("Environment", "Management settings"),
    ("environmentmanagement", "environment-state"): ("Environment", "State"),
    ("environmentmanagement", "environment-provisioning"): ("Environment Operations", "Provisioning reference data"),
    ("environmentmanagement", "failover"): ("Environment Operations", "DR drills and failover"),
    ("environmentmanagement", "environment-backup"): ("Environment Operations", "Backups"),
    ("environmentmanagement", "environment-copy"): ("Environment Operations", "Copy"),
    ("environmentmanagement", "environment-restore"): ("Environment Operations", "Restore"),
    ("environmentmanagement", "environment-recover"): ("Environment Operations", "Recover"),
    ("environmentmanagement", "environment-reset"): ("Environment Operations", "Reset"),
    ("environmentmanagement", "environment-groups"): ("Environment Group", "CRUD and membership"),
    ("environmentmanagement", "operation"): ("Async Operation", "Job polling"),
    ("authorization", "role-based-access-control"): ("Role Based Access Control", "Assignments and definitions; tenant, environment group and environment scopes"),
    ("licensing", "billing-policy"): ("Billing Policy", "CRUD"),
    ("licensing", "billing-policy-environment"): ("Billing Policy to Environment link", "Policy side"),
    ("licensing", "environment-billing-policy"): ("Billing Policy to Environment link", "Environment side"),
    ("licensing", "allocation"): ("Capacity Allocation", "Add-on allocation"),
    ("licensing", "allocations-by-environment"): ("Capacity Allocation", "Environment view"),
    ("licensing", "currency-allocation"): ("Currency Allocation", "Allocation"),
    ("licensing", "currency-reports"): ("Currency Allocation", "Reports"),
    ("licensing", "temporary-currency-entitlement"): ("Currency Allocation", "Temporary entitlement"),
    ("licensing", "entitlement"): ("Entitlement", "Entitlements"),
    ("licensing", "entitlement-insight"): ("Entitlement", "Insights"),
    ("licensing", "tenant-capacity-details"): ("Tenant Capacity", "Capacity"),
    ("licensing", "storage-warnings"): ("Tenant Capacity", "Storage warnings"),
    ("licensing", "resource-threshold"): ("Tenant Capacity", "Thresholds"),
    ("licensing", "user-per-flow-capacity-source"): ("Per-Flow Capacity", "Per-user-per-flow capacity"),
    ("licensing", "fin-ops-licensing"): ("FinOps Licensing", "F&O licensing"),
    ("licensing", "isv-contract"): ("ISV Contract", "Pay-as-you-go contracts"),
    ("governance", "rule-based-policies"): ("Rule-Based Policy", "Policy and assignments"),
    ("governance", "rule-sets"): ("Rule Set", "Group rule sets"),
    ("governance", "cross-tenant-connection-reports"): ("Cross-Tenant Connection Report", "Reports"),
    ("appmanagement", "applications"): ("Application Package", "Tenant and environment app install"),
    ("copilotstudio", "bots"): ("Copilot Agent", "Agent admin and quarantine"),
    ("copilotstudio", "agent-channels"): ("Copilot Agent", "Channels"),
    ("powerpages", "websites"): ("Power Pages Website", "Site admin, security, scanning"),
    ("connectivity", "connections"): ("Connection", "Connections"),
    ("connectivity", "connectors"): ("Connector", "Connector catalogue"),
    ("powerautomate", "cloud-flows"): ("Cloud Flow", "Flows"),
    ("powerautomate", "flow-runs"): ("Cloud Flow", "Runs"),
    ("powerautomate", "flow-actions"): ("Cloud Flow", "Actions"),
    ("powerapps", "apps"): ("Canvas App", "App admin"),
    ("usermanagement", "users"): ("User", "Admin user operations"),
    ("analytics", "recommendations"): ("Advisor Recommendation", "Recommendations and actions"),
    ("workflowsagent", "dsr-compliance"): ("DSR Compliance Request", "DSR workflows"),
    ("dynamics", "finance-and-operations-maintenance-settings"): ("F&O Environment", "Maintenance settings"),
    ("dynamics", "finance-and-operations-operation-errors"): ("F&O Environment", "Operation errors"),
    ("dynamics", "finance-and-operations-properties"): ("F&O Environment", "Properties"),
    ("dynamics", "finance-and-operations-versions"): ("F&O Environment", "Versions"),
    ("resourcequery", "resource-query"): ("Resource Query", "Cross-resource query"),
}


# operations that stay on the convergent "Environment" tag inside otherwise-ephemeral groups
_ENV_CONVERGENT = {
    ("environment-provisioning", "provision-new-environment"): "Create",
    ("environment-provisioning", "link-dataverse"): "Link Dataverse",
    ("failover", "enable-disaster-recovery"): "Disaster recovery configuration",
    ("failover", "disable-disaster-recovery"): "Disaster recovery configuration",
}


def logical_for(ns, group, slug):
    """Map an operation to its logical resource + facet. Most groups map wholesale
    via LOGICAL; provisioning and failover are split per-operation so their
    convergent members (create, link Dataverse, enable/disable DR) sit under
    "Environment" while the ephemeral rest sit under "Environment Operations"."""
    facet_override = _ENV_CONVERGENT.get((group, slug))
    if facet_override:
        return ("Environment", facet_override)
    return LOGICAL.get((ns, group), ("(unmapped)", group))


def crud(method, title):
    t = title.lower()
    if method == "GET":
        return "Read (list)" if t.startswith(("list", "get all")) else "Read"
    if method == "DELETE":
        return "Delete"
    if method in ("PATCH", "PUT"):
        return "Update"
    if t.startswith(("create", "provision", "generate", "submit", "install", "add", "invite")):
        return "Create"
    return "Action"


def load_dates():
    cl = DOCS / "whats-new-changed.md"
    dates = {}
    if not cl.exists():
        return dates
    cur = None
    for line in cl.read_text(encoding="utf-8").splitlines():
        hm = re.match(r"^##\s+([A-Z][a-z]+ \d{4})", line)
        if hm:
            cur = hm.group(1)
            continue
        for lm in re.finditer(r"New endpoint: \[[^\]]+\]\(([^)]+)\)", line):
            u = lm.group(1).split("?")[0].rstrip("/")
            u = re.sub(r"^https://learn\.microsoft\.com", "", u)
            u = re.sub(r"^/en-us", "", u)
            u = u.replace("/rest/api/power-platform/", "")
            dates.setdefault(u, cur)
    return dates


def main():
    dates = load_dates()
    rows = []
    for f in sorted(DOCS.glob("*/*/*.md")):
        ns, group, slug = f.parent.parent.name, f.parent.name, f.stem
        text = f.read_text(encoding="utf-8")
        reqs = re.findall(r"```http\s*\n(GET|POST|PATCH|PUT|DELETE)\s+(\S+)", text)
        if not reqs:
            continue
        method, url = reqs[0]
        m = re.match(r"https://api\.powerplatform\.com([^?]+)\??(.*)$", url)
        path = m.group(1) if m else url
        vm = re.search(r"api-version=([\w.-]+)", m.group(2)) if m else None
        title_m = re.search(r"^# .*? - (.+?)(?:\s*\(preview\))?\s*$", text, re.M)
        title = title_m.group(1) if title_m else slug.replace("-", " ").title()
        logical, facet = logical_for(ns, group, slug)
        rows.append({
            "logical_resource": logical,
            "facet": facet,
            "operation": title,
            "crud": crud(method, title),
            "method": method,
            "path": path,
            "api_version": vm.group(1) if vm else "",
            "preview": "(preview)" in text[:2000].lower(),
            "introduced": dates.get(f"{ns}/{group}/{slug}", ""),
            "namespace": ns,
            "group": group,
            "doc": str(f.relative_to(ROOT)),
        })
    rows.sort(key=lambda r: (r["logical_resource"], r["facet"], r["method"], r["operation"]))
    OUT.mkdir(exist_ok=True)
    (OUT / "catalogue.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    with open(OUT / "catalogue.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    unmapped = sorted({(r["namespace"], r["group"]) for r in rows if r["logical_resource"] == "(unmapped)"})
    print(f"catalogue: {len(rows)} operations, {len(unmapped)} unmapped groups")
    for u in unmapped:
        print("  unmapped:", "/".join(u))


if __name__ == "__main__":
    main()
