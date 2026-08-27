#!/usr/bin/env python3
"""Mirror the Microsoft Power Platform API reference as markdown.

Discovers every page from the Learn REST TOC, fetches each as markdown
(learn.microsoft.com serves clean source markdown to 'Accept: text/markdown'),
lays them out as a linked tree under docs/, and rewrites links so they resolve
locally. The whole tree is replaced atomically only when every fetch succeeds,
so a partial outage never produces a partial mirror.

Stdlib only. Deterministic output: volatile build metadata (updated_at,
gitcommit, git_commit_id) is stripped so commits happen only on real changes.
"""
import concurrent.futures as cf
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TOC_URL = "https://learn.microsoft.com/en-us/rest/api/toc.json"
PAGE_BASE = "https://learn.microsoft.com/en-us/rest/api/"
CHANGELOG = "https://learn.microsoft.com/en-us/power-platform/admin/programmability-whats-new-changed"
HEADERS = {"User-Agent": "pp-api-mirror (github.com/AdamCoulterOz)", "Accept": "text/markdown"}
VOLATILE = ("updated_at", "gitcommit", "git_commit_id")


def get(url, accept_md=True, attempts=4):
    last = None
    for i in range(attempts):
        try:
            hdrs = dict(HEADERS) if accept_md else {"User-Agent": HEADERS["User-Agent"]}
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdrs), timeout=60) as r:
                body = r.read()
            if accept_md and body[:200].lstrip().startswith(b"<!DOCTYPE"):
                raise RuntimeError("HTML returned where markdown expected")
            return body
        except Exception as e:  # noqa: BLE001 - retry everything, report last
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"fetch failed after {attempts} attempts: {url}: {last}")


def discover():
    toc = json.loads(get(TOC_URL, accept_md=False))
    flat = []

    def collect(items):
        for it in items:
            href = (it.get("href") or "").strip("/")
            if href.startswith("power-platform"):
                flat.append(href)
            collect(it.get("children") or [])

    collect(toc.get("items", []))
    out = []
    for href in sorted(set(flat)):
        parts = href.split("/")
        if len(parts) == 4:
            out.append((href, pathlib.Path(parts[1]) / parts[2] / f"{parts[3]}.md"))
        elif len(parts) == 3:
            out.append((href, pathlib.Path(parts[1]) / f"{parts[2]}.md"))
        elif href in ("power-platform",):
            out.append((href + "/", pathlib.Path("index.md")))
    if not any(p[1].name == "index.md" for p in out):
        out.append(("power-platform/", pathlib.Path("index.md")))
    return out


def strip_volatile(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return text
    front = "\n".join(
        line for line in m.group(1).splitlines()
        if not line.startswith(tuple(f"{k}:" for k in VOLATILE))
    )
    return f"---\n{front}\n---\n" + text[m.end():]


LINK = re.compile(r"(\]\()([^)\s]+)(\))")


def rewrite_links(text, self_rel, known):
    """known: site path ('power-platform/ns/group[/op]' or '' for index) -> tree relpath."""
    self_dir = pathlib.PurePosixPath(str(self_rel)).parent

    def rel_to(target_rel):
        return os.path.relpath(str(target_rel), str(self_dir)).replace(os.sep, "/")

    def fix(m):
        url = m.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        base, frag = (url.split("#", 1) + [""])[:2]
        frag = f"#{frag}" if frag else ""
        base = base.split("?", 1)[0]
        if base.startswith("/"):
            clean = re.sub(r"^/en-us/", "", base).strip("/")
            if clean == "power-platform/admin/programmability-whats-new-changed":
                return f"{m.group(1)}{rel_to('whats-new-changed.md')}{frag}{m.group(3)}"
            if clean.startswith("rest/api/"):
                site = clean.replace("rest/api/", "", 1).rstrip("/")
                if site in known:
                    return f"{m.group(1)}{rel_to(known[site])}{frag}{m.group(3)}"
            return f"{m.group(1)}https://learn.microsoft.com{base}{frag}{m.group(3)}"
        own_site_dir = pathlib.PurePosixPath("power-platform")
        if str(self_dir) != ".":
            own_site_dir = own_site_dir / str(self_dir)
        site = str(pathlib.PurePosixPath(os.path.normpath(str(own_site_dir / base))))
        if site in known:
            return f"{m.group(1)}{rel_to(known[site])}{frag}{m.group(3)}"
        return m.group(0)

    return LINK.sub(fix, text)


def main():
    pages = discover()
    known = {}
    for site, rel in pages:
        key = site.rstrip("/") if site != "power-platform/" else "power-platform"
        known[key] = rel
    print(f"discovered {len(pages)} pages")

    results = {}

    def fetch_one(item):
        site, rel = item
        body = get(PAGE_BASE + site).decode("utf-8", errors="replace")
        return rel, strip_volatile(body)

    with cf.ThreadPoolExecutor(12) as ex:
        for rel, text in ex.map(fetch_one, pages):
            results[rel] = text
    results[pathlib.Path("whats-new-changed.md")] = strip_volatile(
        get(CHANGELOG).decode("utf-8", errors="replace"))
    print(f"fetched {len(results)} pages")

    staged = pathlib.Path(tempfile.mkdtemp(prefix="docs-", dir=str(ROOT)))
    try:
        for rel, text in sorted(results.items()):
            out = staged / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rewrite_links(text, rel, known), encoding="utf-8")
        if DOCS.exists():
            shutil.rmtree(DOCS)
        staged.rename(DOCS)
    finally:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)
    print(f"docs/ replaced: {sum(1 for _ in DOCS.rglob('*.md'))} files")


if __name__ == "__main__":
    sys.exit(main())
