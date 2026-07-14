#!/usr/bin/env python3
"""Audit the exact v2 reader EPUB package without granting application approval."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET
from zipfile import ZIP_STORED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPUB = ROOT / "build/curated_reader_v2_0_formats/format_artifacts/epub/_reader_site/The-ASI-Stack.epub"
MANIFEST = ROOT / "editions/reader_manuscript/v2_0/manifest.json"
REPORT = ROOT / "editions/reader_manuscript/v2_0/epub_structural_inspection.json"
LIVE_MARKERS = ("Chapter status", "Drafting guardrail", "Codex test plan", "Source crosswalk", "Formalization hooks")
CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]")
NS = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/", "x": "http://www.w3.org/1999/xhtml"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(owner: str, href: str) -> tuple[str | None, str]:
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return None, ""
    target, _, fragment = href.partition("#")
    if not target:
        return owner, fragment
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target)), fragment


def observe(epub: Path) -> dict:
    if not epub.is_file():
        raise SystemExit(f"missing EPUB: {epub}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    with ZipFile(epub) as z:
        infos = z.infolist()
        names = [i.filename for i in infos if not i.is_dir()]
        name_set = set(names)
        unsafe = [n for n in names if PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts]
        if unsafe:
            errors.append("unsafe archive member paths")
        required = {"mimetype", "META-INF/container.xml", "EPUB/content.opf", "EPUB/nav.xhtml", "EPUB/toc.ncx"}
        missing = sorted(required - name_set)
        if missing:
            errors.append("missing required members: " + ", ".join(missing))
        if not infos or infos[0].filename != "mimetype" or infos[0].compress_type != ZIP_STORED:
            errors.append("mimetype is not first and stored")
        if z.read("mimetype") != b"application/epub+zip":
            errors.append("invalid mimetype payload")

        opf = ET.fromstring(z.read("EPUB/content.opf"))
        title = [x.text or "" for x in opf.findall(".//dc:title", NS)]
        creator = [x.text or "" for x in opf.findall(".//dc:creator", NS)]
        language = [x.text or "" for x in opf.findall(".//dc:language", NS)]
        if title != ["The ASI Stack"] or creator != ["Corben Sorenson"] or language != ["en-US"]:
            errors.append("OPF title/creator/language metadata drift")
        manifest_items = opf.findall(".//opf:manifest/opf:item", NS)
        spine_items = opf.findall(".//opf:spine/opf:itemref", NS)
        manifest_ids = [item.attrib.get("id", "") for item in manifest_items]
        manifest_hrefs = [item.attrib.get("href", "") for item in manifest_items]
        manifest_by_id = {item.attrib.get("id", ""): item for item in manifest_items}
        duplicate_manifest_ids = len(manifest_ids) - len(set(manifest_ids))
        duplicate_manifest_hrefs = len(manifest_hrefs) - len(set(manifest_hrefs))
        missing_manifest_targets = []
        for href in manifest_hrefs:
            target = posixpath.normpath(posixpath.join("EPUB", href.split("#", 1)[0]))
            if target not in name_set:
                missing_manifest_targets.append(target)
        missing_spine_idrefs = [
            item.attrib.get("idref", "")
            for item in spine_items
            if item.attrib.get("idref", "") not in manifest_by_id
        ]
        nav_items = [item for item in manifest_items if "nav" in item.attrib.get("properties", "").split()]
        cover_items = [item for item in manifest_items if "cover-image" in item.attrib.get("properties", "").split()]
        if duplicate_manifest_ids or duplicate_manifest_hrefs:
            errors.append(
                f"duplicate OPF manifest ids/hrefs: {duplicate_manifest_ids}/{duplicate_manifest_hrefs}"
            )
        if missing_manifest_targets:
            errors.append(f"missing OPF manifest targets: {len(missing_manifest_targets)}")
        if missing_spine_idrefs:
            errors.append(f"missing OPF spine idrefs: {len(missing_spine_idrefs)}")
        if len(nav_items) != 1 or len(cover_items) != 1:
            errors.append(f"unexpected nav/cover manifest item counts: {len(nav_items)}/{len(cover_items)}")

        nav_tree = ET.fromstring(z.read("EPUB/nav.xhtml"))
        epub_type = "{http://www.idpf.org/2007/ops}type"
        nav_types = [
            node.attrib.get(epub_type, "")
            for node in nav_tree.iter()
            if node.tag.rsplit("}", 1)[-1] == "nav"
        ]
        landmark_links = [
            node.attrib.get(epub_type, "")
            for node in nav_tree.iter()
            if node.tag.rsplit("}", 1)[-1] == "a" and node.attrib.get(epub_type)
        ]
        if "toc" not in nav_types or "landmarks" not in nav_types:
            errors.append("EPUB navigation lacks toc or landmarks nav")
        if not {"cover", "titlepage", "toc", "bodymatter"}.issubset(set(landmark_links)):
            errors.append("EPUB landmarks lack cover, titlepage, toc, or bodymatter")

        xhtml = sorted(n for n in names if n.endswith(".xhtml"))
        content = sorted(n for n in xhtml if n.startswith("EPUB/text/ch"))
        ids: dict[str, set[str]] = {}
        hrefs: list[tuple[str, str]] = []
        live_hits = raw_claim_hits = empty = replacement = missing_alt = table_without_headers = 0
        image_count = table_count = code_count = math_count = text_chars = 0
        noteref_count = note_count = 0
        all_text = ""
        first_heading_text: dict[str, str] = {}
        for name in xhtml:
            raw = z.read(name).decode("utf-8", errors="replace")
            replacement += raw.count("\ufffd")
            try:
                tree = ET.fromstring(raw)
            except ET.ParseError as exc:
                errors.append(f"XML parse error {name}: {exc}")
                continue
            text = " ".join(tree.itertext())
            all_text += " " + text
            text_chars += len(text)
            empty += int(not text.strip())
            live_hits += sum(raw.count(marker) for marker in LIVE_MARKERS)
            raw_claim_hits += len(CLAIM_RE.findall(raw))
            ids[name] = {node.attrib["id"] for node in tree.iter() if "id" in node.attrib}
            first_heading = next(
                (
                    " ".join(node.itertext()).strip()
                    for node in tree.iter()
                    if node.tag.rsplit("}", 1)[-1] == "h1"
                ),
                "",
            )
            first_heading_text[name] = first_heading
            for node in tree.iter():
                tag = node.tag.rsplit("}", 1)[-1]
                node_epub_type = node.attrib.get(epub_type, "")
                if "noteref" in node_epub_type.split():
                    noteref_count += 1
                if {"footnote", "endnote"}.intersection(node_epub_type.split()):
                    note_count += 1
                if tag == "a" and node.attrib.get("href"):
                    hrefs.append((name, node.attrib["href"]))
                elif tag == "img":
                    image_count += 1
                    if not node.attrib.get("alt", "").strip():
                        missing_alt += 1
                elif tag == "table":
                    table_count += 1
                    if not any(child.tag.rsplit("}", 1)[-1] == "th" for child in node.iter()):
                        table_without_headers += 1
                elif tag in {"code", "pre"}:
                    code_count += 1
                elif tag == "math":
                    math_count += 1

        unresolved = missing_fragments = 0
        unresolved_details: list[dict[str, str]] = []
        missing_fragment_details: list[dict[str, str]] = []
        for owner, href in hrefs:
            target, fragment = resolve(owner, href)
            if target is None:
                continue
            if target not in name_set:
                unresolved += 1
                unresolved_details.append({"owner": owner, "href": href, "resolved_target": target})
            elif fragment and fragment not in ids.get(target, set()):
                missing_fragments += 1
                missing_fragment_details.append(
                    {"owner": owner, "href": href, "resolved_target": target, "fragment": fragment}
                )
        missing_titles = [r["title"] for r in manifest["chapter_records"] if r["title"] not in all_text]
        chapter_entry_names = content[2:56]
        chapter_order_mismatches = [
            {
                "position": index,
                "entry": name,
                "expected_title": record["title"],
                "observed_heading": first_heading_text.get(name, ""),
            }
            for index, (name, record) in enumerate(
                zip(chapter_entry_names, manifest["chapter_records"]), start=1
            )
            if record["title"] not in first_heading_text.get(name, "")
        ]
        if len(xhtml) != 62 or len(content) != 59 or len(spine_items) != 62:
            errors.append(f"unexpected XHTML/content/spine counts: {len(xhtml)}/{len(content)}/{len(spine_items)}")
        if len(chapter_entry_names) != 54 or chapter_order_mismatches:
            errors.append(
                f"chapter entry/order mismatch: {len(chapter_entry_names)} entries, "
                f"{len(chapter_order_mismatches)} mismatches"
            )
        if noteref_count != note_count:
            errors.append(f"footnote/endnote reference/body count mismatch: {noteref_count}/{note_count}")
        for label, value in {
            "empty XHTML": empty,
            "replacement characters": replacement,
            "live markers": live_hits,
            "raw claim markers": raw_claim_hits,
            "missing image alt": missing_alt,
            "tables without headers": table_without_headers,
            "unresolved hrefs": unresolved,
            "missing fragments": missing_fragments,
            "missing chapter titles": len(missing_titles),
        }.items():
            if value:
                errors.append(f"{label}: {value}")

    return {
        "schema_version": "asi_stack.reader_epub_structural_inspection.v1",
        "edition_id": manifest["edition_id"],
        "state": "passed_structural_application_review_pending" if not errors else "failed_structural",
        "artifact": str(epub.relative_to(ROOT)) if epub.is_relative_to(ROOT) else str(epub),
        "sha256": sha256(epub),
        "bytes": epub.stat().st_size,
        "archive_members": len(names),
        "xhtml_entries": len(xhtml),
        "content_entries": len(content),
        "opf_manifest_items": len(manifest_items),
        "opf_spine_items": len(spine_items),
        "opf_missing_manifest_targets": missing_manifest_targets,
        "opf_missing_spine_idrefs": missing_spine_idrefs,
        "navigation_types": nav_types,
        "landmark_types": landmark_links,
        "internal_hrefs_checked": len(hrefs),
        "images_checked": image_count,
        "tables_checked": table_count,
        "code_elements_checked": code_count,
        "math_elements_checked": math_count,
        "footnote_noterefs_checked": noteref_count,
        "footnote_or_endnote_bodies_checked": note_count,
        "text_characters_checked": text_chars,
        "chapter_titles_checked": 54,
        "chapter_entry_points_checked": len(chapter_entry_names),
        "chapter_order_mismatches": chapter_order_mismatches,
        "unresolved_href_details": unresolved_details,
        "missing_fragment_details": missing_fragment_details,
        "missing_chapter_titles": missing_titles,
        "errors": errors,
        "application_review": "pending_apple_books",
        "support_state_effect": "none",
        "release_effect": "none",
        "review_boundary": "All package members and XHTML were parsed; metadata, spine, internal links/fragments, chapter titles, images/alt text, tables, code, math, and reader-only leakage were checked. This is not Apple Books, screen-reader, device-family, independent-human, legal-WCAG, or release approval."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--epub", type=Path, default=DEFAULT_EPUB)
    args = parser.parse_args()
    epub = args.epub if args.epub.is_absolute() else ROOT / args.epub
    observed = observe(epub)
    if args.write:
        REPORT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
    elif not REPORT.is_file() or json.loads(REPORT.read_text()) != observed:
        raise SystemExit("EPUB structural inspection report is missing or stale; run with --write")
    if observed["errors"]:
        raise SystemExit("EPUB structural inspection failed:\n - " + "\n - ".join(observed["errors"]))
    print(f"EPUB structural inspection passed: {observed['xhtml_entries']} XHTML, {observed['internal_hrefs_checked']} hrefs, {observed['sha256'][:12]}.")


if __name__ == "__main__":
    main()
