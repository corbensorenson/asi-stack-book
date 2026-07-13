#!/usr/bin/env python3
"""Validate the exact v2.0 curated-reader HTML archive and inspection packet."""

from __future__ import annotations

import copy
import hashlib
import json
import posixpath
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "editions/reader_manuscript/v2_0"
SITE = ROOT / "build/curated_reader_v2_0/_reader_site"
MANIFEST = EDITION / "manifest.json"
ARTIFACT = EDITION / "html_artifact_manifest.json"
BROWSER = EDITION / "html_browser_report.json"
ACCESSIBILITY = EDITION / "html_accessibility_tree_report.json"
KEYBOARD = EDITION / "html_keyboard_report.json"
WCAG = EDITION / "html_wcag_report.json"
REPORT = EDITION / "html_release_inspection.json"
EXPECTED_PAGES = 59
EXPECTED_CHAPTERS = 54
EXPECTED_PAIRS = 118


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def validate_reports(manifest: dict, artifact: dict, browser: dict, access: dict, keyboard: dict, wcag: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("selected_initial_format") != "canonical_curated_html":
        errors.append("canonical curated HTML is not the prospectively selected format")
    if len(manifest.get("chapter_records", [])) != EXPECTED_CHAPTERS:
        errors.append("source manifest does not contain 54 chapter records")
    if manifest.get("support_state_effect") != "none":
        errors.append("source manifest launders support movement")
    expected_artifact = {
        "edition_id": "asi-stack-curated-reader-v2.0",
        "format": "canonical_curated_html",
        "html_page_count": EXPECTED_PAGES,
        "chapter_entry_point_count": EXPECTED_CHAPTERS,
        "support_state_effect": "none",
    }
    for key, expected in expected_artifact.items():
        if artifact.get(key) != expected:
            errors.append(f"artifact {key} must be {expected!r}; found {artifact.get(key)!r}")

    if browser.get("status") != "passed" or browser.get("page_count") != EXPECTED_PAGES:
        errors.append("browser report does not pass the 59-page artifact")
    if browser.get("expected_page_count") != EXPECTED_PAGES or browser.get("page_view_pairs") != EXPECTED_PAIRS:
        errors.append("browser report denominator drift")
    if browser.get("failures"):
        errors.append("browser report contains failed page views")
    browser_rows = browser.get("results", [])
    if len(browser_rows) != EXPECTED_PAIRS or any(row.get("status") != "passed" for row in browser_rows):
        errors.append("browser result rows are incomplete or failed")
    if any(int(row.get("horizontal_overflow_px", 0)) > 0 for row in browser_rows):
        errors.append("browser report contains horizontal reflow overflow")

    access_summary = access.get("summary", {})
    if access.get("status") != "passed_accessibility_tree_release_preparation_probe":
        errors.append("accessibility-tree report is not passing")
    for key, expected in {
        "pages_checked": EXPECTED_PAGES,
        "expected_pages": EXPECTED_PAGES,
        "page_view_pairs": EXPECTED_PAIRS,
        "failed_page_view_pairs": 0,
        "lang_en_us_pairs": EXPECTED_PAIRS,
        "titled_pairs": EXPECTED_PAIRS,
        "one_h1_pairs": EXPECTED_PAIRS,
        "main_landmark_pairs": EXPECTED_PAIRS,
        "navigation_landmark_pairs": EXPECTED_PAIRS,
        "skip_link_pairs": EXPECTED_PAIRS,
        "focus_visible_rule_pairs": EXPECTED_PAIRS,
        "accessibility_tree_pairs": EXPECTED_PAIRS,
        "unnamed_interactive_elements": 0,
        "image_alt_failures": 0,
        "table_header_failures": 0,
        "duplicate_id_page_views": 0,
        "live_marker_leak_pairs": 0,
        "raw_core_claim_marker_leak_pairs": 0,
    }.items():
        if access_summary.get(key) != expected:
            errors.append(f"accessibility summary {key} must be {expected}; found {access_summary.get(key)}")

    keyboard_summary = keyboard.get("summary", {})
    if keyboard.get("status") != "passed_automated_keyboard_traversal_review":
        errors.append("keyboard report is not passing")
    for key, expected in {
        "pages_checked": EXPECTED_PAGES,
        "expected_pages": EXPECTED_PAGES,
        "page_view_pairs": EXPECTED_PAIRS,
        "failed_page_view_pairs": 0,
        "skip_link_reached_pairs": EXPECTED_PAIRS,
        "skip_link_activated_pairs": EXPECTED_PAIRS,
        "main_content_route_available_pairs": EXPECTED_PAIRS,
        "navigation_focus_reached_pairs": EXPECTED_PAIRS,
        "search_focus_reached_pairs": EXPECTED_PAIRS,
        "keyboard_trap_candidates": 0,
    }.items():
        if keyboard_summary.get(key) != expected:
            errors.append(f"keyboard summary {key} must be {expected}; found {keyboard_summary.get(key)}")

    wcag_summary = wcag.get("summary", {})
    if wcag.get("status") != "accepted_wcag_automation_evidence_for_release_preparation":
        errors.append("WCAG-preparation report is not accepted")
    for key, expected in {
        "pages_checked": EXPECTED_PAGES,
        "expected_pages": EXPECTED_PAGES,
        "page_view_pairs": EXPECTED_PAIRS,
        "failed_page_view_pairs": 0,
        "contrast_failure_samples": 0,
        "duplicate_id_page_views": 0,
        "unnamed_interactive_elements": 0,
        "image_alt_failures": 0,
        "table_header_failures": 0,
    }.items():
        if wcag_summary.get(key) != expected:
            errors.append(f"WCAG summary {key} must be {expected}; found {wcag_summary.get(key)}")
    if int(wcag_summary.get("text_contrast_samples", 0)) < 4000:
        errors.append("WCAG report contains fewer than 4,000 rendered-text contrast samples")
    if float(wcag_summary.get("minimum_contrast_ratio", 0)) < 4.5:
        errors.append("minimum rendered-text contrast is below 4.5:1")
    return errors


def resolve_target(source: str, href: str, files: set[str]) -> tuple[str | None, str]:
    split = urlsplit(href)
    if split.scheme or split.netloc or href.startswith("//"):
        return None, ""
    raw_path = unquote(split.path)
    fragment = unquote(split.fragment)
    if not raw_path:
        target = source
    elif raw_path.startswith("/"):
        target = posixpath.normpath(raw_path.lstrip("/"))
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), raw_path))
    candidates = [target]
    if target in ("", "."):
        candidates.append("index.html")
    elif target.endswith("/"):
        candidates.append(target + "index.html")
    elif "." not in posixpath.basename(target):
        candidates.extend([target + ".html", target + "/index.html"])
    for candidate in candidates:
        if candidate in files:
            return candidate, fragment
    return target, fragment


def inspect_links(site: Path) -> tuple[int, int, list[str]]:
    files = {path.relative_to(site).as_posix() for path in site.rglob("*") if path.is_file()}
    html_files = sorted(path for path in files if path.endswith(".html"))
    ids: dict[str, set[str]] = {}
    soups: dict[str, BeautifulSoup] = {}
    for rel in html_files:
        soup = BeautifulSoup((site / rel).read_text(errors="replace"), "html.parser")
        soups[rel] = soup
        ids[rel] = {
            str(node.get("id"))
            for node in soup.find_all(attrs={"id": True})
            if str(node.get("id")).strip()
        } | {
            str(node.get("name"))
            for node in soup.find_all(attrs={"name": True})
            if str(node.get("name")).strip()
        }
    checked = 0
    anchors = 0
    errors: list[str] = []
    ignored_schemes = ("mailto:", "tel:", "javascript:", "data:")
    for source, soup in soups.items():
        for node in soup.find_all(href=True):
            href = str(node.get("href", "")).strip()
            if not href or href.startswith(ignored_schemes):
                continue
            target, fragment = resolve_target(source, href, files)
            if target is None:
                continue
            checked += 1
            if target not in files:
                errors.append(f"{source}: unresolved internal link {href!r} -> {target!r}")
                continue
            if fragment and target.endswith(".html"):
                anchors += 1
                if fragment not in ids.get(target, set()):
                    errors.append(f"{source}: unresolved anchor {href!r} -> {target}#{fragment}")
    return checked, anchors, errors


def main() -> None:
    required = [MANIFEST, ARTIFACT, BROWSER, ACCESSIBILITY, KEYBOARD, WCAG]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Reader HTML validation failed; missing: " + ", ".join(missing))
    manifest, artifact, browser, access, keyboard, wcag = map(load, required)
    errors = validate_reports(manifest, artifact, browser, access, keyboard, wcag)

    archive = ROOT / artifact.get("archive", "")
    link_count = 0
    anchor_count = 0
    link_errors: list[str] = []
    if not archive.is_file():
        errors.append("deterministic archive is missing")
    else:
        if sha256(archive) != artifact.get("archive_sha256"):
            errors.append("archive digest drift")
        if archive.stat().st_size != artifact.get("archive_bytes"):
            errors.append("archive byte-count drift")
        with zipfile.ZipFile(archive) as zipped:
            names = {name for name in zipped.namelist() if not name.endswith("/")}
            unsafe = [
                name
                for name in names
                if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
            ]
            if unsafe:
                errors.append("archive contains unsafe absolute or parent-traversal members")
            else:
                with tempfile.TemporaryDirectory(prefix="asi-reader-v2-") as tmp:
                    replay_site = Path(tmp)
                    zipped.extractall(replay_site)
                    if tree_digest(replay_site) != artifact.get("site_tree_sha256"):
                        errors.append("archive-replayed site-tree digest drift")
                    link_count, anchor_count, link_errors = inspect_links(replay_site)
                    if SITE.is_dir():
                        disk = {
                            path.relative_to(SITE).as_posix(): path.read_bytes()
                            for path in SITE.rglob("*")
                            if path.is_file()
                        }
                        if tree_digest(SITE) != artifact.get("site_tree_sha256"):
                            errors.append("local site-tree digest drift")
                        if names != set(disk):
                            errors.append("archive member set differs from inspected local site")
                        elif any(zipped.read(name) != body for name, body in disk.items()):
                            errors.append("archive bytes differ from inspected local site")

    errors.extend(link_errors)

    mutation_count = 0
    mutations = [
        (1, None, "archive_sha256", "0" * 64),
        (2, None, "page_count", 58),
        (3, "summary", "duplicate_id_page_views", 1),
        (4, "summary", "keyboard_trap_candidates", 1),
        (5, "summary", "contrast_failure_samples", 1),
        (0, None, "selected_initial_format", "epub"),
    ]
    for target, section, key, value in mutations:
        docs = [copy.deepcopy(manifest), copy.deepcopy(artifact), copy.deepcopy(browser), copy.deepcopy(access), copy.deepcopy(keyboard), copy.deepcopy(wcag)]
        if section:
            docs[target][section][key] = value
        else:
            docs[target][key] = value
        caught = bool(validate_reports(*docs))
        if target == 1 and key == "archive_sha256":
            caught = docs[1][key] != sha256(ROOT / artifact["archive"])
        if not caught:
            errors.append(f"negative mutation was accepted: {key}")
        mutation_count += 1

    report = {
        "schema_version": "asi_stack.curated_reader_html_release_inspection.v2",
        "edition_id": "asi-stack-curated-reader-v2.0",
        "status": "passed_exact_html_release_inspection" if not errors else "failed_exact_html_release_inspection",
        "artifact_archive": artifact.get("archive"),
        "archive_sha256": artifact.get("archive_sha256"),
        "site_tree_sha256": artifact.get("site_tree_sha256"),
        "html_page_count": EXPECTED_PAGES,
        "chapter_entry_point_count": EXPECTED_CHAPTERS,
        "page_view_pairs": EXPECTED_PAIRS,
        "internal_links_checked": link_count,
        "internal_anchors_checked": anchor_count,
        "unresolved_internal_links_or_anchors": len(link_errors),
        "report_digests": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [BROWSER, ACCESSIBILITY, KEYBOARD, WCAG]
        },
        "negative_mutations_rejected": mutation_count,
        "review_boundary": "Exact deterministic HTML archive replay plus local-render parity when present, browser, automated accessibility-tree, automated keyboard, rendered contrast, reflow, link, anchor, heading, landmark, language, alt-text, table-header, and duplicate-ID inspection. This is not independent external-human review, screen-reader use, third-party WCAG certification, or approval of another format.",
        "support_state_effect": "none",
        "errors": errors,
        "non_claims": [
            "Does not approve EPUB, DOCX, PDF, audio, or embedded-audio artifacts.",
            "Does not claim independent external-human, screen-reader, assistive-technology, or legal WCAG review.",
            "Does not promote any chapter claim or establish model quality, safety, readiness, AGI, or ASI.",
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    if errors:
        raise SystemExit("Reader HTML validation failed:\n - " + "\n - ".join(errors[:60]))
    print(
        f"Reader HTML release inspection passed: {EXPECTED_PAGES} pages, {EXPECTED_PAIRS} browser/accessibility views, "
        f"{link_count} internal links, {anchor_count} anchors, exact archive bytes, and {mutation_count} rejecting mutations."
    )


if __name__ == "__main__":
    main()
