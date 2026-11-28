#!/usr/bin/env python3
"""Bind generated reading routes to the rendered site and tested source revision."""

from __future__ import annotations

import argparse
import agent_reading
import research_dictionary
from hashlib import sha256
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
GRAPH = "products/evidence-registry/knowledge-graph"
CATALOG = "evidence-catalog.json"
SEARCH_INDEXES = ("search.json", "reader/search.json", "papers/search.json")
QUARTO_SEARCH_SCRIPT = "site_libs/quarto-search/quarto-search.js"
SEARCH_ADAPTER_ASSETS = ("assets/research-evidence-search.js", "assets/quarto-evidence-search.js")
ADAPTER_END = "/* End ASI Stack evidence-search adapter. */\n"
EVIDENCE_LABELS = {
    "study": "Research study",
    "study_run": "Study run",
    "transition": "Bounded claim",
    "evidence_passage": "Evidence passage",
    "evidence_case": "Paired case",
    "proof_target": "Proof target",
}

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


def evidence_entries(site: Path, commit: str) -> list[dict]:
    directory = site / GRAPH
    manifest = load(directory / "manifest.json")
    raw = (directory / CATALOG).read_bytes()
    catalog = json.loads(raw)
    if (manifest.get("evidence_catalog") != CATALOG or manifest["source_commit"] != commit
            or catalog["source_commit"] != commit or catalog["snapshot_id"] != manifest["snapshot_id"]
            or manifest["files"][CATALOG]["sha256"] != sha256(raw).hexdigest()):
        raise ValueError("Evidence search catalog differs from the site's graph snapshot or source revision")
    pages = {}
    entries = []
    for record in catalog["records"]:
        title = record.get("citation_title", record["title"])
        category = EVIDENCE_LABELS[record["kind"]]
        body = " ".join(record[key] for key in ("question", "summary", "limit", "disposition") if record.get(key))
        aliases = [record["id"], record["id"].split(":", 1)[1],
                   *record.get("aliases", []), *record.get("unmeasured", [])]
        for position, destination in enumerate([{"url": record["url"]}, *record.get("locators", [])]):
            uri = urlsplit(destination["url"])
            if uri.scheme or uri.netloc or uri.path.startswith("/") or ".." in Path(uri.path).parts:
                raise ValueError(f'Invalid research search destination: {destination["url"]}')
            if uri.path not in pages:
                pages[uri.path] = (site / uri.path).read_text(encoding="utf-8")
            if uri.fragment and f'id="{uri.fragment}"' not in pages[uri.path]:
                raise ValueError(f'Research search anchor missing: {destination["url"]}')
            if record.get("measurement") == "Case identifier":
                # The full graph packet retains outcomes, source, scope and citation.
                # Search only needs the exact identity and its landing page.
                compact = {key: record[key] for key in ("id","title","aliases","measurement","url")}
                entries.append({"objectID": "asi-evidence:" + record["id"], "href": destination["url"],
                                "title": title, "section": category, "text": record["question"], "crumbs": [],
                                "evidence_id":record["id"], "evidence_kind":category, "asi_scope":"evidence",
                                "evidence_primary":True, "evidence":compact})
                continue
            entries.append({"objectID": f'asi-evidence:{record["id"]}:{destination["url"]}',
                            "href": destination["url"], "title": title,
                            "section": destination.get("label", category),
                            "text": " ".join((body, *aliases)), "crumbs": [],
                            "evidence_id": record["id"], "evidence_kind": category, "asi_scope": "evidence",
                            "evidence_primary": position == 0, "evidence": record})
    return entries


def scientific_identifiers(site):
    """Index each scored claim and every returned paper, including unfeatured cases."""
    registry = "products/evidence-registry"
    release = [json.loads(line) for line in (ROOT / "experiments/scifact_citation_check/reserved.jsonl").read_text().splitlines()]
    fresh = load(ROOT / "experiments/scifact_retrieval_followup/cases.json")["cases"]
    selection = load(ROOT / "experiments/scifact_three_papers/observations.json")["cases"]
    entries = []
    for study, run, records in (("scientific-citation", "scifact-release", release),
                                ("citation-retrieval", "fresh-citation-retrieval", fresh),
                                ("citation-retrieval", "three-paper-selection", selection)):
        path = f"{registry}/study-{study}.html"
        html = (site / path).read_text()
        for row in records:
            claim = str(row["id"])
            candidates = row.get("candidates") or row.get("arms", {}).values() or [row]
            papers = sorted({str(a["doc"]) for a in candidates})
            for suffix in (("",) if study == "citation-retrieval" else ("-triage","-publication")):
                anchor = f"run-{run}--case-{claim}{suffix}"
                if f'id="{anchor}"' not in html:
                    raise ValueError(f"Scientific identifier destination missing: {anchor}")
                entries.append({"objectID":"asi-evidence:identifier:"+anchor, "href":path+"#"+anchor,
                                "identifier_keys":["claim:"+claim, *["paper:"+paper for paper in papers]],
                                "title":f"SciFact claim {claim}" + suffix.replace("-", " · "),
                                "section":"Paired study case", "text":"Returned paper IDs: " + ", ".join(papers),
                                "asi_scope":"evidence","crumbs":[]})
    return entries


def index_projection(site: Path, index: str, entries: list[dict]) -> str:
    rows = [row for row in load(site / index) if not row["objectID"].startswith("asi-evidence:")]
    for row in rows:
        target = urlsplit(row["href"])
        row["asi_scope"] = "history" if target.path == "appendices/F_changelog.html" else "reading"
        if (target.path.startswith("chapters/") and target.fragment in RESEARCH_SECTIONS
                and not target.query):
            row["href"] = urlunsplit(("", "", target.path, "view=ai", target.fragment))

    directory = posixpath.dirname(index) or "."
    local_alternates = {}
    if directory != ".":
        for row in entries:
            if "evidence_id" in row and urlsplit(row["href"]).path.startswith(directory + "/"):
                local_alternates.setdefault(row["evidence_id"], row["objectID"])
    local = []
    for row in entries:
        target = urlsplit(row["href"])
        href = urlunsplit(("", "", posixpath.relpath(target.path, directory), target.query, target.fragment))
        preferred = local_alternates.get(row.get("evidence_id"))
        local.append({**row, "href": href, **({"evidence_primary": row["objectID"] == preferred} if preferred else {})})
    return json.dumps(local + rows, ensure_ascii=False, separators=(",", ":")) + "\n"


def quarto_search_links(text: str, adapter: str) -> str:
    # The pinned Quarto template only recognizes ?q=. A result already carrying
    # a reading-mode query has &q=, so the template appends a second search term.
    old = """if (item.text && item.href && !item.href.includes('?q=')) {
                const [main, hash] = item.href.split('#')
                const hashAppend = hash ? '#' + hash : ''
                item.href = main + '?q=' + encodeURIComponent(state.query) + hashAppend
              }"""
    fixed = """if (item.text && item.href && !new URL(item.href, document.baseURI).searchParams.has(kQueryArg)) {
                const [main, hash] = item.href.split('#')
                const hashAppend = hash ? '#' + hash : ''
                item.href = main + (main.includes('?') ? '&' : '?') + 'q=' + encodeURIComponent(state.query) + hashAppend
              }"""
    text = text.split(ADAPTER_END, 1)[-1]

    def render(before: str, after: str) -> None:
        nonlocal text
        if text.count(before) == 1:
            text = text.replace(before, after)
        elif text.count(after) != 1:
            raise ValueError("The pinned Quarto search integration points have changed")

    render(old, fixed)
    render('            const baseHref = hrefParts[0];',
           '            const baseHref = item.evidenceId || hrefParts[0];')
    render('  window.history.replaceState({}, "", replacementUrl);\n}',
           '  window.history.replaceState({}, "", replacementUrl);\n'
           '  // Preserve the copied search URL after Quarto has resolved the page links.\n'
           '  window.addEventListener("load", () => {\n'
           '    const sharedUrl = new URL(window.location);\n'
           '    sharedUrl.searchParams.set(kQueryArg, kQuery);\n'
           '    window.history.replaceState(window.history.state, "", sharedUrl);\n'
           '  }, { once: true });\n}')
    previous = """return asiReadSearchData().then(() =>
                asiSearchResults(query, state.context.asiScope || "", fuseSearchOptions));"""
    lookup = 'return asiLookup(query, asiCurrentScope(state), fuseSearchOptions, refresh);'
    text = text.replace('return asiLookup(query, state.context.asiScope || "", fuseSearchOptions, refresh);', lookup)
    if previous in text:
        render(previous, lookup)
    else:
        render("""return readSearchData().then(function (fuse) {
                return fuseSearch(query, fuse, fuseSearchOptions);
              });""", lookup)
    render('                language["search-no-results-text"]',
           '                [asiSearchScopes(createElement, state, setContext, refresh), '
           'language["search-no-results-text"]]')
    render('                  `${count} ${language["search-matching-documents-text"]}`',
           '                  [asiSearchScopes(createElement, state, setContext, refresh), '
           '`${count} ${language["search-matching-documents-text"]}`]')
    return adapter + "\n" + ADAPTER_END + text


def book_citation_entries(site: Path, chapters: list[dict], sources: list[dict]) -> list[dict]:
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
    return entries


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
    research = evidence_entries(site, commit)
    citations = book_citation_entries(site, chapters, load(ROOT / "sources/source_inventory.json"))
    adapter = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in SEARCH_ADAPTER_ASSETS)
    identifiers = scientific_identifiers(site)
    dictionary = load(site / GRAPH / "dictionary.json")
    if dictionary["source_commit"] != commit:
        raise ValueError("Dictionary revision differs")
    for term in dictionary["terms"]:
        identifiers.append(dict(objectID="asi-evidence:dictionary:"+term["id"], href=term["url"],
                                title=term["term"], section="AI dictionary", text=term["definition"], crumbs=[],
                                dictionary_record=True, identifier_keys=["term:"+name.casefold() for name in (term["term"],*term["aliases"])]))
    reader = load(ROOT / "editions/reader_manuscript/current/manifest.json")
    volumes = [(c["id"],c["title"],c["file"].replace(".qmd",".html")) for c in chapters]
    volumes += [(u["unit_id"],u["title"],"reader/"+u["source_file"].replace(".qmd",".html")) for u in reader["units"]]
    research_dictionary.subject_index(site, volumes, files, commit)
    agent_reading.publish(site, files, commit, lambda path: (ROOT / path).read_bytes())
    for index in SEARCH_INDEXES:
        entries = (citations + research if index == "search.json" else research) + identifiers
        projected = index_projection(site, index, entries)
        files.write(site / index, projected)
        small = [row for row in json.loads(projected) if row.get("evidence_primary") or row.get("dictionary_record")]
        files.write(site / Path(index).with_name("evidence-search.json"),
                    json.dumps(small, ensure_ascii=False, separators=(",", ":")) + "\n")
        script = site / Path(index).parent / QUARTO_SEARCH_SCRIPT
        files.write(script, quarto_search_links(files.text(script), adapter))
    changes = files.changes(site)
    if changes:
        raise SystemExit(f"Public reading routes are stale: {[row['path'] for row in changes]}")
    print("Public documentation, citation paths and evidence search are bound to the site.")


if __name__ == "__main__":
    main()
