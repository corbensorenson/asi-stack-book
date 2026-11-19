#!/usr/bin/env python3
"""Bind generated reading routes to the rendered site and tested source revision."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import quote, urlsplit, urlunsplit

from projection_files import ProjectionFiles

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/corbensorenson/asi-stack-book"
LOG = "docs/project_improvements.md"
SOURCE_APP = "appendices/H_external_sources.html"
CLAIM_APP = "appendices/C_claim_evidence_matrix.html"

# These are section identities hidden by the technical Condensed projection.
RESEARCH_SECTIONS = {
    "chapter-status", "drafting-guardrail", "codex-test-plan", "external-literature-queue",
    "source-crosswalk", "claim-labels", "why-codex-tests-matter", "formalization-hooks",
    "claim-source-mapping-status",
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def log_projection(site: Path, commit: str, tracked: set[str]) -> str:
    text = (ROOT / LOG).read_text(encoding="utf-8")

    def rewrite(match: re.Match[str]) -> str:
        link = urlsplit(match[1])
        if link.scheme or link.netloc or not link.path or link.path.startswith("/"):
            return match[0]
        path = posixpath.normpath(posixpath.join("docs", link.path))
        rendered = path
        if path.startswith("editions/reader_manuscript/current/"):
            rendered = "reader/" + path.removeprefix("editions/reader_manuscript/current/")
        if rendered.endswith(".qmd"):
            rendered = rendered.removesuffix(".qmd") + ".html"
        if (site / rendered).is_dir():
            rendered = rendered.rstrip("/") + "/index.html"
        if (site / rendered).is_file():
            target = posixpath.relpath(rendered, "docs")
        elif path in tracked:
            target = f"{REPO}/blob/{commit}/{quote(path)}"
        elif any(name.startswith(path.rstrip("/") + "/") for name in tracked):
            target = f"{REPO}/tree/{commit}/{quote(path)}"
        else:
            raise ValueError(f"Unresolved improvement-log link: {match[1]}")
        return "](" + urlunsplit((*urlsplit(target)[:3], link.query, link.fragment)) + ")"

    text = re.sub(r"\]\(([^\s)]+)\)", rewrite, text)
    return f"[Read this audit on GitHub]({REPO}/blob/{commit}/{LOG}).\n\n{text}"


def index_projection(site: Path, chapters: list[dict], sources: list[dict]) -> str:
    rows = [row for row in load(site / "search.json") if not row["objectID"].startswith("asi-evidence:")]
    for row in rows:
        target = urlsplit(row["href"])
        if (target.path.startswith("chapters/") and target.fragment in RESEARCH_SECTIONS
                and not target.query):
            row["href"] = urlunsplit(("", "", target.path, "view=ai", target.fragment))

    pages = {name: (site / name).read_text(encoding="utf-8") for name in (SOURCE_APP, CLAIM_APP)}
    entries = []

    def add(title: str, section: str, text: str, page: str, anchor: str) -> None:
        if page not in pages:
            pages[page] = (site / page).read_text(encoding="utf-8")
        if f'id="{anchor}"' not in pages[page]:
            raise ValueError(f"Search target missing: {page}#{anchor}")
        href = f"{page}#{anchor}"
        entries.append({"objectID": f"asi-evidence:{href}", "href": href, "title": title,
                        "section": section, "text": text, "crumbs": []})

    for source in sources:
        if source.get("priority") == "external_literature":
            add(source["id"], "External source", source["title"], SOURCE_APP, source["id"])
    for chapter in chapters:
        claim = chapter["id"] + ".core"
        add(claim, "Core claim", chapter["title"], CLAIM_APP, claim)
    add("e-means", "Clustering the retrieval index",
        "e-means, centroids, and the release-note index rebuild",
        "chapters/virtual-context-abi.html", "clustering-the-retrieval-index")
    return json.dumps(entries + rows, ensure_ascii=False, separators=(",", ":")) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    site = args.site.resolve()
    status = load(site / "status/canonical-public-status.json")
    commit = status["source_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("Canonical status must provide a full source commit.")
    tracked = set(subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit], cwd=ROOT, text=True
    ).splitlines())
    structure = load(ROOT / "book_structure.json")
    chapters = [chapter for part in structure["parts"] for chapter in part["chapters"]]
    notes = (site / SOURCE_APP).read_text(encoding="utf-8")
    files = ProjectionFiles(write=not args.check)
    files.write(site / LOG, log_projection(site, commit, tracked))
    files.write(site / SOURCE_APP, re.sub(
        re.escape(REPO) + r"/blob/(?:main|[0-9a-f]{40})/sources/source_notes/",
        f"{REPO}/blob/{commit}/sources/source_notes/", notes
    ))
    files.write(site / "search.json", index_projection(site, chapters, load(ROOT / "sources/source_inventory.json")))
    changes = files.changes(site)
    if changes:
        raise SystemExit(f"Public reading routes are stale: {[row['path'] for row in changes]}")
    print("Public documentation, citation paths and evidence search are bound to the site.")


if __name__ == "__main__":
    main()
