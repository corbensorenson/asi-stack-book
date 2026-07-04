#!/usr/bin/env python3
"""Generate and validate the live Human-view status ledger.

The live-book status snapshot should stay readable. This ledger carries the
long Human-view contract behind a compact row without making `validate_book.py`
depend on rendered `_site` output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
LEDGER = ROOT / "docs" / "live_human_view_status_ledger.md"

BOOK_STRUCTURE = ROOT / "book_structure.json"
QUARTO = ROOT / "_quarto.yml"
READER_OVERLAY_MANIFEST = ROOT / "editions" / "reader_overlays" / "v1_0" / "manifest.json"
READER_OVERLAY_DIR = ROOT / "editions" / "reader_overlays" / "v1_0" / "chapters"
READER_OVERLAYS_ASSET = ROOT / "assets" / "reader-overlays.html"
READING_MODE_ASSET = ROOT / "assets" / "reading-mode.html"
STYLES_ASSET = ROOT / "assets" / "styles.scss"

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
HUMAN_BLOCK_RE = re.compile(r"::: \{\.asi-human-only\}\n## Human Reading Path\n\n(.*?)\n:::", re.DOTALL)
OVERLAY_ASSET_RE = re.compile(
    r'<script\s+type="application/json"\s+id="asi-reader-overlays">\s*(.*?)\s*</script>',
    re.DOTALL,
)
TEMPLATE_BRIDGE_PHRASES = (
    "The useful",
    "The practical",
    "The point is",
    "useful only when",
    "The mature test",
    "The mature version is",
    "the book",
    "this book",
    "Part I",
    "Part II",
    "Part III",
    "Part IV",
    "previous chapter",
    "previous chapters",
    "previous layers",
    "first two chapters",
    "first half",
    "closing move",
    "begins by",
    "ended by",
)
SOURCE_VALIDATORS = (
    "python3 scripts/validate_reading_mode_toggle.py",
    "python3 scripts/validate_human_reading_paths.py",
    "python3 scripts/validate_reader_spine.py --check",
    "python3 scripts/validate_reader_evidence_boundaries.py --check",
    "python3 scripts/sync_reader_overlay_asset.py --check",
    "python3 scripts/validate_reader_overlays.py --check",
    "python3 scripts/validate_live_human_view_status_ledger.py",
)
POST_RENDER_VALIDATORS = (
    "python3 scripts/validate_live_human_view.py",
    "node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Live Human-view status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def bridge_metrics(chapters: list[dict[str, Any]]) -> tuple[int, int, int, int, int, list[str]]:
    values: list[int] = []
    opening_values: list[int] = []
    closing_values: list[int] = []
    template_phrase_hits = 0
    missing: list[str] = []
    for chapter in chapters:
        path = ROOT / str(chapter.get("file", ""))
        text = path.read_text(encoding="utf-8", errors="ignore")
        matches = HUMAN_BLOCK_RE.findall(text)
        if len(matches) != 1:
            missing.append(str(chapter.get("id", chapter.get("file", ""))))
            continue
        bridge_text = re.sub(r"\s+", " ", matches[0].strip())
        normalized_bridge = bridge_text.lower()
        template_phrase_hits += sum(
            normalized_bridge.count(phrase.lower()) for phrase in TEMPLATE_BRIDGE_PHRASES
        )
        values.append(len(WORD_RE.findall(bridge_text)))
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", bridge_text)
            if sentence.strip()
        ]
        if sentences:
            opening_values.append(len(WORD_RE.findall(sentences[0])))
            closing_values.append(len(WORD_RE.findall(sentences[-1])))
    return (
        len(values),
        min(values) if values else 0,
        min(opening_values) if opening_values else 0,
        min(closing_values) if closing_values else 0,
        template_phrase_hits,
        missing,
    )


def overlay_asset_payload(errors: list[str]) -> dict[str, Any]:
    asset_text = READER_OVERLAYS_ASSET.read_text(encoding="utf-8", errors="ignore")
    match = OVERLAY_ASSET_RE.search(asset_text)
    if not match:
        errors.append(f"{rel(READER_OVERLAYS_ASSET)} is missing the asi-reader-overlays JSON payload.")
        return {}
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(READER_OVERLAYS_ASSET)} payload is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{rel(READER_OVERLAYS_ASSET)} payload must be a JSON object.")
        return {}
    return payload


def collect_metrics() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    required_paths = [
        BOOK_STRUCTURE,
        QUARTO,
        READER_OVERLAY_MANIFEST,
        READER_OVERLAYS_ASSET,
        READING_MODE_ASSET,
        STYLES_ASSET,
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return {}, errors

    structure = load_json(BOOK_STRUCTURE)
    if not isinstance(structure, dict):
        return {}, ["book_structure.json must contain a JSON object."]
    chapters = flatten_chapters(structure)
    appendices = structure.get("appendices", [])
    front_matter = structure.get("front_matter", [])
    if not isinstance(appendices, list):
        errors.append("book_structure.json appendices must be a list.")
        appendices = []
    if not isinstance(front_matter, list):
        errors.append("book_structure.json front_matter must be a list.")
        front_matter = []
    page_count = len(front_matter) + len(chapters) + len(appendices)

    human_count, human_min_words, human_min_opening, human_min_closing, template_hits, missing = bridge_metrics(chapters)
    if missing:
        errors.append(f"chapters missing exactly one Human Reading Path block: {missing[:5]}")
    if human_min_words < 170:
        errors.append(f"Human Reading Path body minimum is {human_min_words}, below 170.")
    if human_min_opening < 11:
        errors.append(f"Human Reading Path opening-sentence minimum is {human_min_opening}, below 11.")
    if human_min_closing < 11:
        errors.append(f"Human Reading Path closing-sentence minimum is {human_min_closing}, below 11.")
    if template_hits != 0:
        errors.append(f"Human Reading Path template-phrase hits must remain 0; found {template_hits}.")

    overlay_manifest = load_json(READER_OVERLAY_MANIFEST)
    if not isinstance(overlay_manifest, dict):
        errors.append("reader overlay manifest must contain an object.")
        overlay_manifest = {}
    if overlay_manifest.get("status") != "active":
        errors.append("reader overlay manifest status must remain active.")
    if overlay_manifest.get("applies_to_profile") != "reader_release":
        errors.append("reader overlay manifest must apply to reader_release.")

    active_overlay_operations = 0
    active_overlay_chapters: set[str] = set()
    for overlay_path in sorted(READER_OVERLAY_DIR.glob("*.json")):
        overlay_record = load_json(overlay_path)
        if not isinstance(overlay_record, dict):
            errors.append(f"{rel(overlay_path)} must contain an object.")
            continue
        target_file = str(overlay_record.get("target_file", ""))
        operations = overlay_record.get("operations", [])
        if not isinstance(operations, list):
            errors.append(f"{rel(overlay_path)} operations must be a list.")
            continue
        active_count = sum(
            1 for operation in operations if isinstance(operation, dict) and operation.get("status") == "active"
        )
        if active_count:
            active_overlay_operations += active_count
            active_overlay_chapters.add(target_file)

    overlay_payload = overlay_asset_payload(errors)
    asset_operations = overlay_payload.get("operations", []) if isinstance(overlay_payload, dict) else []
    if isinstance(overlay_payload, dict):
        if overlay_payload.get("manifest_path") != "editions/reader_overlays/v1_0/manifest.json":
            errors.append("reader overlay asset manifest_path drifted.")
        if overlay_payload.get("manifest_id") != "v1_0_reader_overlay":
            errors.append("reader overlay asset manifest_id drifted.")
        if overlay_payload.get("operation_count") != active_overlay_operations:
            errors.append("reader overlay asset operation_count does not match active overlay source operations.")
        if not isinstance(asset_operations, list) or len(asset_operations) != active_overlay_operations:
            errors.append("reader overlay asset operations length does not match active overlay source operations.")

    quarto_text = QUARTO.read_text(encoding="utf-8", errors="ignore")
    expected_include = "include-after-body:\n      - assets/reader-overlays.html\n      - assets/reading-mode.html"
    if expected_include not in quarto_text:
        errors.append("_quarto.yml must include reader-overlays.html before reading-mode.html.")

    reading_mode_text = READING_MODE_ASSET.read_text(encoding="utf-8", errors="ignore")
    for fragment in (
        'const queryParam = "view"',
        'const humanMode = "human"',
        'const aiMode = "ai"',
        "applyReaderOverlays",
        "data-asi-live-section",
        "data-asi-live-toc-link",
        "asi-core-claim-marker",
        "asi-support-boundary-human",
        "overlayProcessedAttribute",
        "setReaderOverlayMetrics",
    ):
        if fragment not in reading_mode_text:
            errors.append(f"{rel(READING_MODE_ASSET)} is missing required fragment: {fragment}")

    styles_text = STYLES_ASSET.read_text(encoding="utf-8", errors="ignore")
    for fragment in (
        'html[data-asi-reading-mode="human"] section[data-asi-live-section="true"]',
        'html[data-asi-reading-mode="human"] [data-asi-live-toc-link="true"]',
        ".asi-support-boundary-human",
        ".asi-reader-overlay-only",
        'html[data-asi-reading-mode="human"] .asi-reader-overlay-original',
        'html[data-asi-reading-mode="ai"] .asi-human-only',
    ):
        if fragment not in styles_text:
            errors.append(f"{rel(STYLES_ASSET)} is missing required fragment: {fragment}")

    appendix_toggle_count = sum(
        1
        for appendix in appendices
        if isinstance(appendix, dict)
        and appendix.get("id") in {"corben-source-corpus", "external-sources-and-literature"}
    )
    browser_page_view_pairs = (len(chapters) + appendix_toggle_count) * 2

    metrics = {
        "page_count": page_count,
        "chapter_count": len(chapters),
        "appendix_count": len(appendices),
        "human_path_count": human_count,
        "human_min_words": human_min_words,
        "human_min_opening_words": human_min_opening,
        "human_min_closing_words": human_min_closing,
        "human_template_phrase_hits": template_hits,
        "active_overlay_operations": active_overlay_operations,
        "active_overlay_chapters": len(active_overlay_chapters),
        "asset_overlay_operations": len(asset_operations) if isinstance(asset_operations, list) else 0,
        "post_render_static_page_count": page_count,
        "browser_page_view_pairs": browser_page_view_pairs,
        "browser_toggle_appendix_pages": appendix_toggle_count,
    }
    return metrics, errors


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            raise RuntimeError("; ".join(errors))
    return (
        "| Live Human view | "
        "Live/Human-view detail is generated in `docs/live_human_view_status_ledger.md`: "
        f"{metrics['page_count']} expected book pages, "
        f"{metrics['chapter_count']} manifest chapters with one Human Reading Path each, "
        f"{metrics['active_overlay_operations']} active reader-overlay operations across "
        f"{metrics['active_overlay_chapters']} chapters, bridge minima "
        f"{metrics['human_min_words']}/{metrics['human_min_opening_words']}/"
        f"{metrics['human_min_closing_words']} words with "
        f"{metrics['human_template_phrase_hits']} template hits, and post-render static/browser gates "
        "remain required for hiding, restoration, overlay processing, and overflow checks. "
        "| `docs/live_human_view_status_ledger.md`; "
        "`assets/reader-overlays.html`; "
        "`assets/reading-mode.html`; "
        "`assets/styles.scss`; "
        "`python3 scripts/validate_live_human_view_status_ledger.py`; "
        "`python3 scripts/validate_live_human_view.py`; "
        "`node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` |"
    )


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    validation_lines = ["- None."] if not errors else [f"- {error}" for error in errors]
    source_validator_lines = [f"- `{validator}`" for validator in SOURCE_VALIDATORS]
    post_render_validator_lines = [f"- `{validator}`" for validator in POST_RENDER_VALIDATORS]
    return "\n".join(
        [
            "# Live Human-View Status Ledger",
            "",
            "Generated by `python3 scripts/validate_live_human_view_status_ledger.py --write`.",
            "",
            "This ledger replaces the former long `Live Human view` cell in `docs/v1_0_candidate_status.md`. It records the source-side contract for the live-book AI/Human switch, Human Reading Path bridges, reader-overlay payload, and required post-render gates without turning the pre-render status check into a rendered-site result.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Expected rendered book pages | {metrics['page_count']} |",
            f"| Manifest chapters | {metrics['chapter_count']} |",
            f"| Appendices | {metrics['appendix_count']} |",
            f"| Human Reading Path blocks | {metrics['human_path_count']} |",
            f"| Human bridge minimum words | {metrics['human_min_words']} |",
            f"| Human bridge minimum opening-sentence words | {metrics['human_min_opening_words']} |",
            f"| Human bridge minimum closing-sentence words | {metrics['human_min_closing_words']} |",
            f"| Targeted template-phrase hits | {metrics['human_template_phrase_hits']} |",
            f"| Active reader-overlay operations | {metrics['active_overlay_operations']} |",
            f"| Active reader-overlay chapters | {metrics['active_overlay_chapters']} |",
            f"| Overlay operations embedded in live asset | {metrics['asset_overlay_operations']} |",
            f"| Post-render static pages expected | {metrics['post_render_static_page_count']} |",
            f"| Browser page-view pairs expected with all chapters/viewports | {metrics['browser_page_view_pairs']} |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Source Contract",
            "",
            "- `_quarto.yml` includes `assets/reader-overlays.html` before `assets/reading-mode.html` so the runtime switch can read the overlay payload before applying view-mode behavior.",
            "- `assets/reader-overlays.html` embeds the active `v1_0_reader_overlay` payload for the reader-release profile and must match the editable overlay JSON sources.",
            "- `assets/reading-mode.html` owns the `?view=ai` / `?view=human` switch, live-section marking, TOC hiding, raw core-claim marker treatment, support-boundary treatment, and runtime overlay processing metrics.",
            "- `assets/styles.scss` owns the Human-view hiding/restoration rules, support-boundary visibility, reader-overlay replacement visibility, and mobile overflow containment used by the browser gate.",
            "- Each manifest chapter has exactly one source-side `.asi-human-only` Human Reading Path bridge, with the bridge minima shown above.",
            "",
            "## Required Source Validators",
            "",
            *source_validator_lines,
            "",
            "## Required Post-Render Gates",
            "",
            "These gates are intentionally not run inside `validate_book.py` because they require the rendered `_site` directory. They must run after `quarto render --to html` for public-surface changes.",
            "",
            *post_render_validator_lines,
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not claim a reader-edition release, ebook, DOCX, PDF, e-reader approval, audio artifact, accessibility compliance, final figure approval, model behavior, or support-state movement.",
            "- This ledger is not a substitute for the rendered-site static check or the Playwright/Chrome browser check.",
            "- Human view is a presentation layer over the live book plus reader overlays; canonical claims, source interpretation, and support states remain governed by the live source and evidence ledgers.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def write_status_row(row: str) -> None:
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.startswith("| Live Human view |")]
    if len(matches) != 1:
        fail([f"{rel(STATUS)} must contain exactly one Live Human view row; found {len(matches)}."])
    lines[matches[0]] = row
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(args: argparse.Namespace) -> list[str]:
    metrics, errors = collect_metrics()
    if not metrics:
        return errors
    report = build_report(metrics, errors)
    row = compact_status_row(metrics)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
    if args.write_status_row:
        write_status_row(row)
    if args.write or args.write_status_row:
        return errors

    if not LEDGER.exists():
        errors.append(f"{rel(LEDGER)} is missing; run with --write.")
    elif LEDGER.read_text(encoding="utf-8") != report:
        errors.append(f"{rel(LEDGER)} is out of date; run with --write.")

    status_text = STATUS.read_text(encoding="utf-8")
    if row not in status_text:
        errors.append(f"{rel(STATUS)} is missing the compact Live Human view row.")
    stale_fragments = (
        "All 57 rendered book pages carry the persistent and shareable `AI view` / `Human view` switch",
        "bridge prose is guarded against meta-reader and meta-book scaffolding",
        "browser smoke validation can exercise every manifest chapter across desktop and mobile viewports",
        "chapter Human view hides live-only headings, matching page-TOC entries",
    )
    for stale in stale_fragments:
        if stale in status_text:
            errors.append(f"{rel(STATUS)} still contains stale expanded Live Human view text: {stale}")
    for line in status_text.splitlines():
        if line.startswith("| Live Human view |") and len(line) > 1200:
            errors.append(f"{rel(STATUS)} Live Human view row is still too long: {len(line)} characters.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="rewrite the tracked ledger")
    parser.add_argument("--write-status-row", action="store_true", help="rewrite the compact status row")
    args = parser.parse_args()
    errors = validate(args)
    if errors:
        fail(errors)
    action = "wrote" if args.write or args.write_status_row else "validated"
    metrics, _ = collect_metrics()
    print(
        "Live Human-view status ledger "
        f"{action}: {metrics['page_count']} expected pages, "
        f"{metrics['chapter_count']} chapters, "
        f"{metrics['active_overlay_operations']} overlay operations, "
        f"{metrics['browser_page_view_pairs']} browser page-view pairs."
    )


if __name__ == "__main__":
    main()
