#!/usr/bin/env python3
"""Build the public Corben-paper library from an explicit publication manifest.

The manifest is the publication authority. Each record points to a private/local
canonical source for authoring custody and to a tracked exact-byte publication
copy. Reader pages are deterministic presentation projections; they may remove
front matter, demote headings, and replace unavailable image references with an
explicit notice, but they never replace the exact publication copy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "papers" / "paper_library.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
STRUCTURE = ROOT / "book_structure.json"
CLOSURE = ROOT / "sources" / "corben_paper_corpus_closure.json"
RECEIPTS = ROOT / "sources" / "corben_raw_source_receipts.json"
INDEX = ROOT / "papers" / "index.qmd"
QUARTO_CONFIG = ROOT / "papers" / "_quarto.yml"

FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
ATX_HEADING_RE = re.compile(r"^(#{1,5})(\s+)", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[^)]*)?\)(?:\{[^}]*\})?")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def yaml_string(value: object) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def html_path(qmd_path: str) -> str:
    return str(Path(qmd_path).with_suffix(".html"))


def resolved_asset_root(record: dict) -> Path | None:
    """Resolve local canonical assets with a tracked-public fallback.

    Raw author packages are deliberately not tracked.  The paper library does
    track exact publication copies of referenced assets, so fresh checkouts
    must be able to reproduce and validate the same reader page without the
    author's private/local source tree.
    """
    asset_root_value = record.get("canonical_asset_root")
    if not asset_root_value:
        return None
    canonical_asset_root = ROOT / str(asset_root_value)
    if canonical_asset_root.is_dir():
        return canonical_asset_root
    public_asset_root = ROOT / "papers" / "assets" / str(record["source_id"])
    if public_asset_root.is_dir():
        return public_asset_root
    return canonical_asset_root


def flatten_chapters(structure: dict) -> list[dict]:
    return [
        chapter
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def chapter_links(source_id: str, structure: dict, *, from_paper: bool) -> list[str]:
    prefix = "../chapters" if from_paper else "../chapters"
    links: list[str] = []
    for chapter in flatten_chapters(structure):
        if source_id not in chapter.get("source_ids", []):
            continue
        label = qmd_escape(chapter.get("title", chapter.get("id", "chapter")))
        file_name = Path(str(chapter["file"])).with_suffix(".html").name
        links.append(f"[{label}]({prefix}/{file_name})")
    return links


def strip_front_matter(text: str) -> tuple[str, bool]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return text, False
    return text[match.end():], True


def render_body(
    exact_bytes: bytes,
    source_dir: Path,
    *,
    canonical_asset_root: Path | None = None,
    public_asset_prefix: str | None = None,
) -> tuple[str, int, bool]:
    text = exact_bytes.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    text, stripped_front_matter = strip_front_matter(text)
    text = text.replace("\\newpage", "<!-- page break in original manuscript -->")
    # Quarto's book-navigation metadata probe can misread manuscript horizontal
    # rules as nested YAML documents. Preserve the visual separator in HTML
    # while keeping the exact original bytes available in papers/source/.
    text = re.sub(r"(?m)^---\s*$", "<hr>", text)
    text = ATX_HEADING_RE.sub(lambda match: "#" + match.group(0), text)

    missing_images = 0

    def image_replacement(match: re.Match[str]) -> str:
        nonlocal missing_images
        alt, target = match.group(1).strip(), match.group(2).strip()
        if target.startswith(("http://", "https://", "data:")):
            return match.group(0)
        relative = Path(target)
        if relative.is_absolute() or ".." in relative.parts:
            missing_images += 1
            caption = alt or "Figure"
            return (
                "\n\n::: {.callout-warning title=\"Unsafe figure path withheld\"}\n"
                f"**{caption}**  \nThe original manuscript references `{target}` outside its publication root. "
                "The reference is preserved in the exact source but is not copied into the public site.\n:::\n\n"
            )
        target_path = (canonical_asset_root or source_dir) / relative
        if target_path.is_file():
            if canonical_asset_root is not None and public_asset_prefix:
                rewritten = f"{public_asset_prefix}/{relative.as_posix()}"
                return match.group(0).replace(f"]({target}", f"]({rewritten}", 1)
            return match.group(0)
        missing_images += 1
        caption = alt or "Figure"
        return (
            "\n\n::: {.callout-note title=\"Figure asset unavailable in the supplied source package\"}\n"
            f"**{caption}**  \n"
            f"The original manuscript references `{target}`, but that asset was not present in the publication source package. "
            "The reference is preserved here rather than replaced with a reconstructed image.\n"
            ":::\n\n"
        )

    text = IMAGE_RE.sub(image_replacement, text)
    # Exact source bytes retain their original whitespace. The QMD projection
    # removes incidental trailing whitespace so repository checks remain useful;
    # explicit Markdown hard breaks are retained as HTML breaks.
    normalized_lines: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in text.splitlines():
        cleaned = line.rstrip(" \t")
        fence = re.match(r"^\s*(`{3,}|~{3,})", cleaned)
        if not in_fence and fence:
            in_fence = True
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
        elif in_fence and re.match(rf"^\s*{re.escape(fence_char)}{{{fence_len},}}\s*$", cleaned):
            in_fence = False
        trailing = line[len(cleaned):]
        if not in_fence and cleaned and (trailing.count(" ") >= 2 or "\t" in trailing):
            cleaned += "<br>"
        normalized_lines.append(cleaned)
    text = "\n".join(normalized_lines)
    return text.strip() + "\n", missing_images, stripped_front_matter


def expected_page(record: dict, inventory_record: dict, structure: dict, exact_bytes: bytes) -> str:
    source_copy = ROOT / record["published_source"]
    canonical_asset_root = resolved_asset_root(record)
    body, missing_images, stripped_front_matter = render_body(
        exact_bytes,
        source_copy.parent,
        canonical_asset_root=canonical_asset_root,
        public_asset_prefix=f"assets/{record['source_id']}" if canonical_asset_root else None,
    )
    chapter_refs = chapter_links(record["source_id"], structure, from_paper=True)
    chapter_text = ", ".join(chapter_refs) if chapter_refs else "No current chapter assignment."
    date = inventory_record.get("published") or inventory_record.get("updated") or "Date not normalized"
    updated = inventory_record.get("updated") or "Not separately recorded"
    source_type = inventory_record.get("source_type", "author paper")
    document_class = record.get("document_class", "paper_or_architecture_source")
    source_note = record.get("source_note", f"sources/source_notes/{record['source_id']}.md")
    source_note_link = "https://github.com/corbensorenson/asi-stack-book/blob/main/" + source_note
    exact_link = "source/" + Path(record["published_source"]).name
    presentation_notes = [
        "The HTML page normalizes line endings and trailing whitespace, preserves explicit Markdown hard breaks, and demotes manuscript headings beneath the page title."
    ]
    if stripped_front_matter:
        presentation_notes.append("The manuscript YAML front matter is represented by the provenance panel rather than repeated in the body.")
    if missing_images:
        presentation_notes.append(
            f"{missing_images} referenced figure asset{'s were' if missing_images != 1 else ' was'} absent from the supplied source package and "
            f"{'are' if missing_images != 1 else 'is'} marked in place."
        )
    if canonical_asset_root and not missing_images:
        presentation_notes.append("Supplied local figure assets are copied byte-for-byte and their relative paths are rewritten into this reader page.")
    presentation = " ".join(presentation_notes)
    status_note = record.get(
        "status_note",
        "Archived author paper; its claims retain the status and limits stated in the paper and do not inherit the living book's current evidence state.",
    )

    return f"""---
title: {yaml_string(record['title'])}
author: "Corben Sorenson — original collaborator credits preserved in the manuscript"
date: {yaml_string(date)}
page-layout: article
toc: true
toc-depth: 3
number-sections: false
description: {yaml_string('Original Corben Sorenson paper published as part of The ASI Stack source and lineage library.')}
---

[← Corben Papers and Architecture Sources](index.qmd)

::: {{.callout-important title="Original paper, not rewritten book prose"}}
This page publishes Corben Sorenson's original source manuscript so readers can inspect the ideas that preceded or informed the living book. The text may contain historical terminology, claims, confidence, citations, or implementation status that the book later narrows, revises, tests, or rejects. Publication here establishes provenance and access—not correctness, novelty, replication, or support-state promotion.
:::

## Publication and provenance

| Field | Record |
|---|---|
| Source ID | `{qmd_escape(record['source_id'])}` |
| Source class | `{qmd_escape(source_type)}` |
| Library class | `{qmd_escape(document_class)}` |
| Manuscript date | {qmd_escape(date)} |
| Inventory updated | {qmd_escape(updated)} |
| Exact published-source SHA-256 | `{qmd_escape(record['sha256'])}` |
| Exact published-source bytes | {record['bytes']:,} |
| Exact source text | [Download/view the tracked Markdown source]({exact_link}) |
| Book's source note | [Read the bounded mining note]({source_note_link}) |
| Authorship and collaborator credits | Preserved from the exact original manuscript; this library wrapper does not replace or simplify them. |
| Rights | No new license grant. Corben Sorenson's rights are reserved; collaborator, quotation, source-title, and third-party rights remain with their holders. |

**Current publication boundary.** {qmd_escape(status_note)}

**HTML presentation note.** {qmd_escape(presentation)} The digest above applies to the linked exact source text, not to this presentation wrapper.

## Where this paper enters the living book

{chapter_text}

<hr>

## Original manuscript

{body}
""".rstrip() + "\n"


def expected_index(records: list[dict], inventory: dict[str, dict], structure: dict) -> str:
    rows: list[str] = []
    for record in records:
        source_id = record["source_id"]
        inv = inventory[source_id]
        date = inv.get("published") or inv.get("updated") or "date not normalized"
        chapters = chapter_links(source_id, structure, from_paper=False)
        title = qmd_escape(record["title"])
        page = Path(record["page"]).name
        rows.append(
            f"| [{title}]({page}) | {qmd_escape(record.get('document_class', 'paper or architecture source'))} | `{qmd_escape(source_id)}` | {qmd_escape(date)} | "
            f"{len(chapters)} | `{qmd_escape(record['sha256'][:12])}…` |"
        )
    return f"""# Corben Papers and Architecture Sources

This library publishes the original author manuscripts that directly preceded or informed *The ASI Stack*. It exists so a reader can inspect the source ideas rather than seeing only the book's later synthesis. The current tranche contains **{len(records)} exact, digest-bound manuscripts** with HTML reading pages.

The library is a provenance surface, not an evidence shortcut. A paper can be historically important and still be speculative, superseded, incomplete, or wrong. The living chapters, source notes, claim ledger, tests, and later evidence records control the book's current conclusions. The paper pages preserve what was proposed at the time.

## How to read the library

- **Original text stays identifiable.** Every page links an exact tracked source copy and reports its SHA-256 digest and byte count.
- **Book interpretation stays separate.** A provenance panel links the source note and every current chapter assignment; no paper silently becomes current book prose.
- **Historical negatives stay visible.** Deprecated or failed designs such as SpiderSynapse remain readable alongside their successors.
- **Presentation changes are disclosed.** HTML pages may normalize line endings, move YAML metadata into the provenance panel, demote headings, or mark unavailable figures. They do not pretend missing assets were recovered.
- **Credits remain authoritative.** Authorship and collaborator credits in each exact manuscript control; the library wrapper does not silently rewrite them.
- **Rights remain explicit.** Publication makes the manuscripts readable but grants no new license. Corben Sorenson's rights are reserved, while collaborator and third-party rights remain with their holders.

## Read the papers

| Paper or architecture source | Library class | Source ID | Manuscript date | Current chapter assignments | Exact-source digest |
|---|---|---|---|---:|---|
{chr(10).join(rows)}

## Corpus boundary

This is the public **paper and architecture-source** subset, not every item Corben has supplied. Standalone conversation records, private project dumps, transient notes, credentials, and third-party documents are excluded. A manuscript may still preserve its own quoted sources, drafting history, or collaborator dialogue where those are part of the paper itself. [Appendix G](../appendices/G_corben_source_corpus.html) remains the complete public-safe Corben/local source crosswalk; entries with a paper reader route link back into this library.

New papers enter only through `papers/paper_library.json` with an explicit source ID, exact byte identity, source note, and publication path. Publication does not change any claim's evidence state.
"""


def expected_quarto_config(records: list[dict]) -> str:
    render = ["index.qmd", *[f"{record['source_id']}.qmd" for record in records]]
    sidebar = [
        "      - index.qmd",
        '      - section: "Original manuscripts"',
        "        contents:",
        *[f"          - {record['source_id']}.qmd" for record in records],
    ]
    return "\n".join(
        [
            "# Generated by scripts/sync_paper_library.py from paper_library.json.",
            "project:",
            "  type: website",
            "  output-dir: ../_site/papers",
            "  resources:",
            '    - "source/*"',
            '    - "assets/**"',
            "  render:",
            *[f"    - {path}" for path in render],
            "",
            "lang: en-US",
            "",
            "website:",
            '  title: "The ASI Stack — Corben Papers"',
            '  site-url: "https://corbensorenson.github.io/asi-stack-book/papers/"',
            "  search: true",
            "  navbar:",
            "    left:",
            '      - text: "Living book"',
            "        href: ../index.html",
            '      - text: "Paper library"',
            "        href: index.qmd",
            "  sidebar:",
            '    title: "Papers and source lineage"',
            "    contents:",
            *sidebar,
            "",
            "format:",
            "  html:",
            "    theme:",
            "      - cosmo",
            "      - styles.scss",
            "    toc: true",
            "    link-external-newwindow: true",
            "",
        ]
    )


def validate_manifest(
    data: object,
    inventory: dict[str, dict],
    closure: dict[str, dict],
    receipts: dict[str, dict],
) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema_version") != "asi_stack.paper_library.v1":
        return [], ["papers/paper_library.json must use schema_version asi_stack.paper_library.v1"]
    records = data.get("records")
    if not isinstance(records, list) or not records:
        return [], ["paper library records must be a non-empty array"]
    seen: set[str] = set()
    hydrated: list[dict] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index} is not an object")
            continue
        source_id = str(record.get("source_id", ""))
        if not source_id or source_id in seen:
            errors.append(f"record {index} has a missing or duplicate source_id: {source_id!r}")
        seen.add(source_id)
        if source_id not in inventory:
            errors.append(f"{source_id}: missing source inventory record")
        for key in ("document_class",):
            if record.get(key) in (None, ""):
                errors.append(f"{source_id or index}: missing {key}")
        closure_record = closure.get(source_id, {})
        receipt = receipts.get(source_id, {})
        derived = dict(record)
        derived.update(
            {
                "title": inventory.get(source_id, {}).get("title", source_id),
                "canonical_source": record.get("canonical_source") or closure_record.get("raw_source", ""),
                "published_source": f"papers/source/{source_id}.md",
                "page": f"papers/{source_id}.qmd",
                "source_note": record.get("source_note") or closure_record.get("source_note", f"sources/source_notes/{source_id}.md"),
                "sha256": record.get("sha256") or receipt.get("sha256", ""),
                "bytes": record.get("bytes") or receipt.get("bytes", 0),
            }
        )
        for key in ("title", "canonical_source", "source_note", "sha256", "bytes"):
            if derived.get(key) in (None, ""):
                errors.append(f"{source_id or index}: missing derived {key}")
        for key in ("canonical_source", "published_source", "page", "source_note"):
            value = str(derived.get(key, ""))
            if value.startswith("/") or ".." in Path(value).parts:
                errors.append(f"{source_id or index}: unsafe {key} path {value!r}")
        asset_root = derived.get("canonical_asset_root")
        if asset_root:
            value = str(asset_root)
            if not value.startswith("sources/raw/") or value.startswith("/") or ".." in Path(value).parts:
                errors.append(f"{source_id or index}: unsafe canonical_asset_root path {value!r}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(derived.get("sha256", ""))):
            errors.append(f"{source_id}: sha256 must be lowercase hexadecimal")
        if not isinstance(derived.get("bytes"), int) or derived.get("bytes", 0) <= 0:
            errors.append(f"{source_id}: bytes must be a positive integer")
        hydrated.append(derived)
    return hydrated, errors


def synchronize(check: bool) -> list[str]:
    manifest = load_json(MANIFEST)
    raw_inventory = load_json(INVENTORY)
    structure = load_json(STRUCTURE)
    closure_data = load_json(CLOSURE)
    receipt_data = load_json(RECEIPTS)
    if not isinstance(raw_inventory, list) or not isinstance(structure, dict) or not isinstance(closure_data, dict) or not isinstance(receipt_data, dict):
        return ["source inventory must be an array; structure, closure, and receipts must be objects"]
    inventory = {str(row.get("id")): row for row in raw_inventory if isinstance(row, dict) and row.get("id")}
    closure = {str(row.get("source_id")): row for row in closure_data.get("records", []) if isinstance(row, dict) and row.get("source_id")}
    receipts = {str(row.get("source_id")): row for row in receipt_data.get("records", []) if isinstance(row, dict) and row.get("source_id")}
    records, errors = validate_manifest(manifest, inventory, closure, receipts)
    if errors:
        return errors

    expected_paths = {ROOT / record["page"] for record in records}
    expected_sources = {ROOT / record["published_source"] for record in records}
    actual_pages = set((ROOT / "papers").glob("*.qmd")) - {INDEX}
    actual_sources = set((ROOT / "papers" / "source").glob("*.md")) if (ROOT / "papers" / "source").exists() else set()
    for stale in sorted((actual_pages - expected_paths) | (actual_sources - expected_sources)):
        errors.append(f"stale paper-library artifact not declared by manifest: {stale.relative_to(ROOT)}")

    for record in records:
        source_id = record["source_id"]
        canonical = ROOT / record["canonical_source"]
        published_source = ROOT / record["published_source"]
        page = ROOT / record["page"]
        if canonical.exists():
            canonical_bytes = canonical.read_bytes()
            if digest(canonical_bytes) != record["sha256"] or len(canonical_bytes) != record["bytes"]:
                errors.append(f"{source_id}: canonical source bytes do not match manifest identity")
                continue
        elif not published_source.exists():
            errors.append(f"{source_id}: neither local canonical source nor tracked publication copy exists")
            continue
        else:
            canonical_bytes = published_source.read_bytes()

        if digest(canonical_bytes) != record["sha256"] or len(canonical_bytes) != record["bytes"]:
            errors.append(f"{source_id}: candidate publication bytes do not match manifest identity")
            continue
        source_note = ROOT / record["source_note"]
        if not source_note.exists():
            errors.append(f"{source_id}: source note is missing: {record['source_note']}")
            continue

        asset_root_value = record.get("canonical_asset_root")
        expected_assets: set[Path] = set()
        if asset_root_value:
            public_asset_root = ROOT / "papers" / "assets" / source_id
            asset_root = resolved_asset_root(record)
            if asset_root is None or not asset_root.is_dir():
                errors.append(f"{source_id}: canonical asset root is missing: {asset_root_value}")
                continue
            text = canonical_bytes.decode("utf-8-sig", errors="replace")
            for match in IMAGE_RE.finditer(text):
                target = match.group(2).strip()
                if target.startswith(("http://", "https://", "data:")):
                    continue
                relative = Path(target)
                if relative.is_absolute() or ".." in relative.parts:
                    continue
                candidate = asset_root / relative
                if not candidate.is_file():
                    continue
                published_asset = ROOT / "papers" / "assets" / source_id / relative
                expected_assets.add(published_asset)
                if check:
                    if not published_asset.is_file() or published_asset.read_bytes() != candidate.read_bytes():
                        errors.append(f"{source_id}: published figure asset is missing or stale: {relative.as_posix()}")
                else:
                    published_asset.parent.mkdir(parents=True, exist_ok=True)
                    if not published_asset.exists() or published_asset.read_bytes() != candidate.read_bytes():
                        shutil.copyfile(candidate, published_asset)
            actual_assets = {path for path in public_asset_root.rglob("*") if path.is_file()} if public_asset_root.exists() else set()
            for stale in sorted(actual_assets - expected_assets):
                if check:
                    errors.append(f"{source_id}: stale published figure asset: {stale.relative_to(public_asset_root)}")
                else:
                    stale.unlink()

        expected = expected_page(record, inventory[source_id], structure, canonical_bytes)
        if check:
            if not published_source.exists() or published_source.read_bytes() != canonical_bytes:
                errors.append(f"{source_id}: exact publication copy is missing or stale")
            if not page.exists() or page.read_text(encoding="utf-8") != expected:
                errors.append(f"{source_id}: HTML-reader QMD projection is missing or stale")
        else:
            published_source.parent.mkdir(parents=True, exist_ok=True)
            page.parent.mkdir(parents=True, exist_ok=True)
            if not published_source.exists() or published_source.read_bytes() != canonical_bytes:
                if canonical.exists():
                    shutil.copyfile(canonical, published_source)
                else:
                    published_source.write_bytes(canonical_bytes)
            page.write_text(expected, encoding="utf-8")

    index_expected = expected_index(records, inventory, structure)
    if check:
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != index_expected:
            errors.append("papers/index.qmd is missing or stale")
    else:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(index_expected, encoding="utf-8")

    config_expected = expected_quarto_config(records)
    if check:
        if not QUARTO_CONFIG.exists() or QUARTO_CONFIG.read_text(encoding="utf-8") != config_expected:
            errors.append("papers/_quarto.yml is missing or stale")
    else:
        QUARTO_CONFIG.write_text(config_expected, encoding="utf-8")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check generated paper-library artifacts without writing.")
    args = parser.parse_args()
    errors = synchronize(check=args.check)
    if errors:
        print("Paper library synchronization failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    mode = "validated" if args.check else "synchronized"
    count = len(load_json(MANIFEST)["records"])
    print(f"Paper library {mode}: {count} exact author manuscripts and HTML reader routes.")


if __name__ == "__main__":
    main()
