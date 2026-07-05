#!/usr/bin/env python3
"""Validate the curated reader HTML keyboard-only evidence decision."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
KEYBOARD = ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_navigation_manifest.json"
ACCESSIBILITY_TREE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_tree_manifest.json"
HTML_REVIEW = ROOT / "docs" / "curated_reader_html_artifact_browser_review.md"
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_only_decision_manifest.json"
REVIEW = ROOT / "docs" / "reader_keyboard_only_decision.md"
COMMAND = "python3 scripts/validate_reader_keyboard_only_decision.py"
STATUS = "accepted_keyboard_only_evidence_for_release_preparation"
HTML_DIGEST = "2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34"
CLEARED = ["manual_keyboard_only_review_not_completed"]
PRESERVED = [
    "screen_reader_review_not_completed",
    "wcag_conformance_review_not_completed",
    "reader_release_approval_not_created",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    print("Reader keyboard-only evidence decision validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_contains_all(label: str, text: str, fragments: list[str], errors: list[str]) -> None:
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{label} missing required fragment: {fragment!r}")


def build_decision() -> dict[str, Any]:
    keyboard = load_json(KEYBOARD)
    accessibility_tree = load_json(ACCESSIBILITY_TREE)
    html_review = HTML_REVIEW.read_text(encoding="utf-8")
    keyboard_summary = keyboard.get("summary", {})
    accessibility_summary = accessibility_tree.get("summary", {})
    if not isinstance(keyboard_summary, dict):
        keyboard_summary = {}
    if not isinstance(accessibility_summary, dict):
        accessibility_summary = {}

    digest_matches = re.findall(r"`([0-9a-f]{64})`", html_review)
    html_digest = digest_matches[0] if digest_matches else ""

    return {
        "schema_version": "asi_stack.reader_keyboard_only_decision.v0",
        "decision_id": "curated-reader-keyboard-only-decision-2026-07-05",
        "status": STATUS,
        "command": COMMAND,
        "source_artifact_root": "build/curated_reader_edition/format_artifacts/html/_reader_site",
        "source_review_refs": [
            rel(KEYBOARD),
            rel(ACCESSIBILITY_TREE),
            rel(HTML_REVIEW),
        ],
        "html_review_digest": html_digest,
        "keyboard_navigation_status": keyboard.get("status"),
        "keyboard_page_view_pairs": keyboard_summary.get("page_view_pairs"),
        "keyboard_failed_pairs": keyboard_summary.get("failed_page_view_pairs"),
        "keyboard_skip_link_activated_pairs": keyboard_summary.get("skip_link_activated_pairs"),
        "keyboard_main_route_pairs": keyboard_summary.get("main_content_route_available_pairs"),
        "keyboard_navigation_pairs": keyboard_summary.get("navigation_focus_reached_pairs"),
        "keyboard_search_pairs": keyboard_summary.get("search_focus_reached_pairs"),
        "keyboard_trap_candidates": keyboard_summary.get("keyboard_trap_candidates"),
        "accessibility_tree_status": accessibility_tree.get("status"),
        "accessibility_tree_page_view_pairs": accessibility_summary.get("page_view_pairs"),
        "accessibility_tree_failed_pairs": accessibility_summary.get("failed_page_view_pairs"),
        "accessibility_tree_unnamed_interactive": accessibility_summary.get("unnamed_interactive_elements"),
        "accessibility_tree_duplicate_id_hits": accessibility_summary.get("duplicate_id_page_views"),
        "cleared_blockers": CLEARED,
        "preserved_blockers": PRESERVED,
        "decision_basis": (
            "The current curated reader HTML candidate has a passing automated Chromium "
            "keyboard traversal review over 98 desktop/mobile page-view pairs, a passing "
            "accessibility-tree release-preparation probe over the same page-view pairs, "
            "zero keyboard-trap candidates, zero unnamed interactive elements, and a passing "
            "strict local HTML browser viability sweep. This is enough to clear only the "
            "keyboard-only review blocker for release preparation."
        ),
        "release_boundary": (
            "This decision clears only `manual_keyboard_only_review_not_completed` for the current "
            "curated reader HTML candidate. It does not perform screen-reader review, does not "
            "certify WCAG conformance, does not approve reader release, does not approve EPUB, "
            "DOCX, PDF, e-reader, audio, or audiobook artifacts, and does not promote any "
            "chapter core claim or support state."
        ),
        "non_claims": [
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not create reader release approval",
            "does not publish or approve curated reader HTML",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or audiobook artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_decision(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "asi_stack.reader_keyboard_only_decision.v0",
        "decision_id": "curated-reader-keyboard-only-decision-2026-07-05",
        "status": STATUS,
        "command": COMMAND,
        "source_artifact_root": "build/curated_reader_edition/format_artifacts/html/_reader_site",
        "html_review_digest": HTML_DIGEST,
        "keyboard_navigation_status": "passed_automated_keyboard_traversal_review",
        "keyboard_page_view_pairs": 98,
        "keyboard_failed_pairs": 0,
        "keyboard_skip_link_activated_pairs": 98,
        "keyboard_main_route_pairs": 98,
        "keyboard_navigation_pairs": 98,
        "keyboard_search_pairs": 98,
        "keyboard_trap_candidates": 0,
        "accessibility_tree_status": "passed_accessibility_tree_release_preparation_probe",
        "accessibility_tree_page_view_pairs": 98,
        "accessibility_tree_failed_pairs": 0,
        "accessibility_tree_unnamed_interactive": 0,
        "accessibility_tree_duplicate_id_hits": 0,
        "cleared_blockers": CLEARED,
        "preserved_blockers": PRESERVED,
    }
    for key, value in expected.items():
        if decision.get(key) != value:
            errors.append(f"{key} must be {value!r}; found {decision.get(key)!r}.")

    refs = decision.get("source_review_refs", [])
    if refs != [rel(KEYBOARD), rel(ACCESSIBILITY_TREE), rel(HTML_REVIEW)]:
        errors.append("source_review_refs must name keyboard, accessibility-tree, and HTML browser review evidence.")
    for label in ("decision_basis", "release_boundary"):
        if not isinstance(decision.get(label), str) or len(str(decision.get(label)).split()) < 20:
            errors.append(f"{label} must be a substantive string.")
    text_contains_all(
        "release_boundary",
        str(decision.get("release_boundary", "")),
        [
            "clears only `manual_keyboard_only_review_not_completed`",
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not approve reader release",
            "does not promote any chapter core claim",
        ],
        errors,
    )
    non_claim_text = " ".join(str(item) for item in decision.get("non_claims", [])).lower()
    for fragment in (
        "does not perform screen-reader review",
        "does not certify wcag",
        "does not create reader release approval",
        "does not publish or approve curated reader html",
        "does not promote any chapter core claim",
    ):
        if fragment not in non_claim_text:
            errors.append(f"non_claims missing {fragment!r}.")
    return errors


def render_doc(decision: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Reader Keyboard-Only Evidence Decision",
            "",
            "Last checked: 2026-07-05",
            "",
            "Command:",
            "",
            "```bash",
            COMMAND,
            "```",
            "",
            f"Tracked result: `{rel(MANIFEST)}`",
            "",
            "This decision accepts the current automated keyboard-only browser evidence as sufficient to clear the current curated-reader HTML keyboard-only release-preparation blocker. It is not screen-reader review, WCAG conformance review, reader release approval, or artifact publication.",
            "",
            "## Decision",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{decision['status']}` |",
            f"| HTML digest | `{decision['html_review_digest']}` |",
            f"| Keyboard page-view pairs | {decision['keyboard_page_view_pairs']} |",
            f"| Keyboard failed pairs | {decision['keyboard_failed_pairs']} |",
            f"| Skip-link activations | {decision['keyboard_skip_link_activated_pairs']} |",
            f"| Main-content routes | {decision['keyboard_main_route_pairs']} |",
            f"| Navigation/search reached | {decision['keyboard_navigation_pairs']} / {decision['keyboard_search_pairs']} |",
            f"| Keyboard-trap candidates | {decision['keyboard_trap_candidates']} |",
            f"| Accessibility-tree page-view pairs | {decision['accessibility_tree_page_view_pairs']} |",
            f"| Unnamed interactive elements | {decision['accessibility_tree_unnamed_interactive']} |",
            f"| Duplicate-ID hits | {decision['accessibility_tree_duplicate_id_hits']} |",
            f"| Cleared blockers | {', '.join(decision['cleared_blockers'])} |",
            f"| Preserved blockers | {len(decision['preserved_blockers'])} |",
            "",
            "## Basis",
            "",
            decision["decision_basis"],
            "",
            "## Release Boundary",
            "",
            decision["release_boundary"],
            "",
            "## Non-Claims",
            "",
            "- This decision does not perform screen-reader review.",
            "- This decision does not certify WCAG conformance.",
            "- This decision does not create reader release approval.",
            "- This decision does not publish or approve curated reader HTML.",
            "- This decision does not approve EPUB, DOCX, PDF, e-reader, audio, or audiobook artifacts.",
            "- This decision does not promote any chapter core claim or support state.",
            "",
        ]
    )


def validate_doc(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not REVIEW.exists():
        return [f"{rel(REVIEW)} is missing."]
    text = REVIEW.read_text(encoding="utf-8")
    text_contains_all(
        rel(REVIEW),
        text,
        [
            "Reader Keyboard-Only Evidence Decision",
            STATUS,
            HTML_DIGEST,
            "Keyboard page-view pairs | 98",
            "Keyboard failed pairs | 0",
            "Keyboard-trap candidates | 0",
            "Unnamed interactive elements | 0",
            "Cleared blockers | manual_keyboard_only_review_not_completed",
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not create reader release approval",
            "does not publish or approve curated reader HTML",
        ],
        errors,
    )
    expected_doc = render_doc(decision)
    if text != expected_doc:
        errors.append(f"{rel(REVIEW)} is stale; run `{COMMAND} --write-result`.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="write the tracked decision manifest and review doc")
    args = parser.parse_args()

    for path in (KEYBOARD, ACCESSIBILITY_TREE, HTML_REVIEW):
        if not path.exists():
            fail([f"{rel(path)} is missing."])

    decision = build_decision()
    errors = validate_decision(decision)
    if args.write_result:
        MANIFEST.write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
        REVIEW.write_text(render_doc(decision), encoding="utf-8")
    else:
        if not MANIFEST.exists():
            errors.append(f"{rel(MANIFEST)} is missing; run `{COMMAND} --write-result`.")
        else:
            tracked = load_json(MANIFEST)
            if tracked != decision:
                errors.append(f"{rel(MANIFEST)} is stale; run `{COMMAND} --write-result`.")
        errors.extend(validate_doc(decision))

    if errors:
        fail(errors)
    print(
        "Reader keyboard-only evidence decision validation passed: "
        f"{decision['keyboard_page_view_pairs']} keyboard page-view pairs, "
        f"{decision['keyboard_trap_candidates']} trap candidates, "
        f"cleared {decision['cleared_blockers'][0]}."
    )


if __name__ == "__main__":
    main()
