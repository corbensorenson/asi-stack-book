#!/usr/bin/env python3
"""Rebind semantically unchanged visual abstracts after manuscript/source updates.

This is deliberately narrower than regeneration.  A packet may be rebound only
when its visual argument is unchanged: generated packets must still match the
current manifest-derived semantic contract byte for byte, while the five
hand-authored pilots require an explicit reviewed rationale below.  The script
updates identity fields only and emits an auditable report; it does not rewrite
storyboards, narration, media, evidence state, or publication state.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from generate_visual_chapter_packets import build_content, chapter_list
from visual_chapter_source import canonical_chapter_sha256


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
PREVIEW = ROOT / "visual_edition/youtube_preview_bindings.json"
REPORT = ROOT / "visual_edition/chapter_binding_revalidation.json"

PILOT_RATIONALES = {
    "asi-is-a-stack-not-a-model": (
        "Only source-loading and passage-review status changed; the seven-layer "
        "stack argument, worked trace, failure boundary, evidence ceiling, and "
        "handoff represented by the visual are unchanged."
    ),
    "capability-replacement-and-rollback": (
        "The Capability Ratchet was added as same-author source lineage, but the "
        "visual's phase-gated replacement transaction, rollback trace, evidence "
        "ceiling, non-claims, and handoff remain the current chapter abstraction."
    ),
    "context-transactions-snapshots-mounts-and-taint": (
        "The chapter's current transaction, taint-propagation, deletion-boundary, "
        "evidence, non-claim, and handoff semantics remain exactly those narrated "
        "by the reviewed pilot."
    ),
    "replaceable-cognitive-substrates-beyond-transformer-monoculture": (
        "The current substrate-ABI argument, heterogeneous routing trace, comparison "
        "boundary, evidence ceiling, non-claims, and handoff remain exactly those "
        "represented by the reviewed pilot."
    ),
    "living-book-methodology": (
        "Source-corpus counts and audit coverage changed, but the publication "
        "transaction, withdrawal trace, non-substitutability boundary, evidence "
        "ceiling, non-claims, and handoff represented by the visual are unchanged."
    ),
}

SEMANTIC_KEYS = (
    "problem",
    "core_mechanism",
    "worked_trace",
    "failure_boundary",
    "evidence_state",
    "non_claims",
    "handoff",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    structure = load(STRUCTURE)
    chapters = chapter_list(structure)
    source_commit = git_head()
    preview = load(PREVIEW)
    preview_by_chapter = {entry["chapter_id"]: entry for entry in preview["entries"]}
    rows = []

    for index, (_, chapter) in enumerate(chapters):
        packet_path = ROOT / f"visual_edition/chapters/{chapter['id']}/packet.json"
        packet = load(packet_path)
        current_digest = canonical_chapter_sha256(ROOT / chapter["file"])
        source_drift = packet.get("assigned_source_ids") != chapter.get("source_ids")
        digest_drift = packet.get("chapter_sha256") != current_digest
        if not source_drift and not digest_drift:
            continue

        if chapter["id"] in PILOT_RATIONALES:
            basis = "explicit_pilot_semantic_review"
            rationale = PILOT_RATIONALES[chapter["id"]]
        else:
            next_chapter = chapters[(index + 1) % len(chapters)][1]
            expected = build_content(chapter, next_chapter, index)["required_content"]
            mismatches = [
                key
                for key in SEMANTIC_KEYS
                if packet.get("required_content", {}).get(key) != expected.get(key)
            ]
            if mismatches:
                raise SystemExit(
                    f"{chapter['id']}: visual semantic contract drift in {mismatches}; "
                    "regeneration is required instead of rebinding"
                )
            basis = "exact_generated_semantic_contract_match"
            rationale = (
                "All seven manifest-derived visual semantic fields match the current "
                "chapter contract byte for byte; only chapter/source identity changed."
            )

        old_digest = packet["chapter_sha256"]
        old_commit = packet["source_commit"]
        packet["chapter_sha256"] = current_digest
        packet["source_commit"] = source_commit
        packet["assigned_source_ids"] = chapter["source_ids"]
        packet["staleness"]["state"] = "current"
        packet["staleness"]["checked_chapter_sha256"] = current_digest
        write(packet_path, packet)

        preview_entry = preview_by_chapter.get(chapter["id"])
        if preview_entry is not None:
            preview_entry["bound_chapter_sha256"] = current_digest
            preview_entry["bound_source_commit"] = source_commit

        rows.append(
            {
                "chapter_id": chapter["id"],
                "chapter_path": chapter["file"],
                "old_chapter_sha256": old_digest,
                "new_chapter_sha256": current_digest,
                "old_source_commit": old_commit,
                "new_source_commit": source_commit,
                "source_assignment_changed": source_drift,
                "semantic_review_basis": basis,
                "semantic_contract_sha256": sha256_text(
                    json.dumps(packet["required_content"], sort_keys=True, ensure_ascii=False)
                ),
                "rationale": rationale,
                "lifecycle_state_preserved": packet["lifecycle_state"],
                "render_receipt_preserved": packet.get("render_receipt") is not None,
                "support_state_effect": "none",
                "release_effect": "none",
            }
        )

    write(PREVIEW, preview)
    report = {
        "schema_version": "asi_stack.visual_chapter_binding_revalidation.v1",
        "generated_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "source_commit_at_review": source_commit,
        "reviewed_packet_count": len(rows),
        "generated_exact_match_count": sum(
            row["semantic_review_basis"] == "exact_generated_semantic_contract_match"
            for row in rows
        ),
        "explicit_pilot_review_count": sum(
            row["semantic_review_basis"] == "explicit_pilot_semantic_review"
            for row in rows
        ),
        "rows": rows,
        "decision": (
            "Preserve validated local masters and current preview projection only where "
            "the visual argument remains semantically current; rebind chapter and source "
            "identity without altering media or claim support."
        ),
        "non_claims": [
            "Digest rebinding does not prove that every sentence or new source appears in a visual abstract.",
            "Semantic review of a derivative does not validate the chapter's claims or evidence.",
            "This reconciliation does not upload, publish, replace, or mutate any YouTube object.",
            "No claim, evidence, safety, performance, deployment, AGI, or ASI state moves.",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
    }
    write(REPORT, report)
    print(
        f"Rebound {len(rows)} semantically current visual packet(s): "
        f"{report['generated_exact_match_count']} exact generated contracts and "
        f"{report['explicit_pilot_review_count']} explicitly reviewed pilots."
    )


if __name__ == "__main__":
    main()
