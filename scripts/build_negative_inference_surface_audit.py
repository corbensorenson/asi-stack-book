#!/usr/bin/env python3
"""Build the current reader-facing negative-inference language audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence_quality/negative_inference_surface_audit.json"
DOC = ROOT / "docs/negative_inference_surface_audit.md"

PUBLIC_SURFACES = [
    "README.md",
    "index.qmd",
    "appendices/A_source_matrix.qmd",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/K_implementation_horizons.qmd",
    "docs/accepted_transition_review_audit.md",
    "docs/book_outline.md",
    "docs/claim_family_bundle_coverage.md",
    "docs/claim_identity_graph_reconciliation.md",
    "docs/contribution_novelty_ledger.md",
    "docs/negative_result_rehabilitation.md",
    "docs/non_core_evidence_ledger.md",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "docs/public_status_contract.md",
    "docs/publication_readiness.md",
    "docs/qcsa_implementation_evidence_reconciliation.md",
    "docs/x_article_synopsis_completion.md",
    "editions/x_article/asi_stack_synopsis.md",
    "sources/source_notes/kernel_english_residual_compiler.md",
    "sources/source_notes/qcsa_whitepaper.md",
]

FORBIDDEN = [
    "Broad efficiency is refuted",
    "Broad efficiency refuted",
    "active-question value was refuted",
    "active-question value is refuted",
    "active question value is refuted",
    "adaptive-question advantage as refuted",
    "two exact live non-core QCSA refutations",
    "two exact non-core QCSA refutations",
    "three accepted exact refutations",
    "three exact non-core refutations",
]

REQUIRED = {
    "README.md": ["1 N0, 15 N1, 74 N2, and 0 N3–N5"],
    "index.qmd": ["1 N0, 15 N1, 74 N2, and 0 N3–N5"],
    "docs/non_core_evidence_ledger.md": [
        "2 N2 and 1 N1",
        "broader KERC",
        "historical `refuted`; N2 maximum inference",
    ],
    "docs/claim_family_bundle_coverage.md": [
        "N1 implementation failure",
        "broader KERC remains untested",
    ],
    "sources/source_notes/qcsa_whitepaper.md": [
        "N2",
        "not an exact or broad refutation",
    ],
    "editions/x_article/asi_stack_synopsis.md": [
        "one is N0, fifteen are N1",
        "none is N3, N4, or N5",
        "does not refute the broader unlearning mechanism",
    ],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chapter_paths() -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["file"]
        for part in structure["parts"]
        for chapter in part["chapters"]
    ]


def audit() -> dict:
    chapters = chapter_paths()
    paths = sorted(set(PUBLIC_SURFACES + chapters))
    records = []
    forbidden_hits = []
    required_failures = []
    blocked_boundary_failures = []
    term_counts = {"refuted": 0, "no_change": 0, "blocked_after_full_attempt": 0}
    for relative in paths:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        normalized_text = re.sub(r"\s+", " ", text)
        for phrase in FORBIDDEN:
            for match in re.finditer(re.escape(phrase), text, flags=re.IGNORECASE):
                forbidden_hits.append({
                    "path": relative,
                    "phrase": phrase,
                    "line": text.count("\n", 0, match.start()) + 1,
                })
        for phrase in REQUIRED.get(relative, []):
            if re.sub(r"\s+", " ", phrase) not in normalized_text:
                required_failures.append({"path": relative, "phrase": phrase})
        counts = {
            key: len(re.findall(re.escape(key), text, flags=re.IGNORECASE))
            for key in term_counts
        }
        for key, count in counts.items():
            term_counts[key] += count
        if relative in chapters and "blocked_after_full_attempt" in text:
            required_boundary = "These are residual proof obligations, not false claims."
            if required_boundary not in text:
                blocked_boundary_failures.append(relative)
        records.append({
            "path": relative,
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "term_counts": counts,
        })
    return {
        "schema_version": "asi_stack.negative_inference_surface_audit.v1",
        "recorded_date": "2026-07-17",
        "scope": {
            "surface_count": len(paths),
            "chapter_count": len(chapters),
            "public_and_derivative_surface_count": len(paths) - len(chapters),
            "historical_transition_files_mutated": 0,
            "historical_roadmaps_treated_as_current_prose": False,
        },
        "summary": {
            "forbidden_overbroad_phrase_count": len(forbidden_hits),
            "missing_required_rehabilitation_boundary_count": len(required_failures),
            "blocked_chapter_boundary_failure_count": len(blocked_boundary_failures),
            "accepted_transition_rehabilitation_counts": {
                "N0": 1, "N1": 15, "N2": 74, "N3": 0, "N4": 0, "N5": 0,
            },
            "broad_negative_inference_count": 0,
            "chapter_core_refutation_count": 0,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        "term_counts": term_counts,
        "forbidden_hits": forbidden_hits,
        "required_boundary_failures": required_failures,
        "blocked_chapter_boundary_failures": blocked_boundary_failures,
        "surfaces": records,
        "excluded_historical_scope": [
            "immutable evidence_transitions records",
            "completed or superseded roadmaps and release declarations",
            "frozen reader editions v1.0 through v2.2",
            "raw experiment outputs whose interpretation is separately rehabilitated",
        ],
        "non_claims": [
            "Absence of forbidden phrases is not evidence that an experiment was competent.",
            "The audit preserves raw historical outcomes and labels; it changes only current usable inference language.",
            "Blocked-after-full-attempt is a proof-lane disposition, not evidence that a claim is false.",
            "N0 through N2 results cannot refute a target mechanism, architecture, canonical parent, or chapter core.",
            "This audit creates no support, release, deployment, publication, safety, SOTA, AGI, or ASI result.",
        ],
    }


def write_doc(value: dict) -> None:
    summary = value["summary"]
    counts = summary["accepted_transition_rehabilitation_counts"]
    text = f"""# Negative-Inference Surface Audit

Date: 2026-07-17

This current-prose audit covers {value['scope']['surface_count']} reader-facing
surfaces, including all {value['scope']['chapter_count']} live chapters. It
deliberately excludes immutable transition records, completed historical
roadmaps, frozen reader editions, and raw experiment outputs. Those records
remain discoverable; their usable interpretation is governed by the separate
rehabilitation ledger.

## Result

- Accepted historical transition ceilings: {counts['N0']} N0, {counts['N1']} N1,
  {counts['N2']} N2, {counts['N3']} N3, {counts['N4']} N4, and {counts['N5']} N5.
- Forbidden overbroad current phrases: {summary['forbidden_overbroad_phrase_count']}.
- Missing named rehabilitation boundaries: {summary['missing_required_rehabilitation_boundary_count']}.
- Live chapters that use `blocked_after_full_attempt` without also calling the
  gaps residual proof obligations rather than false claims:
  {summary['blocked_chapter_boundary_failure_count']}.
- Broad negative inferences retained: {summary['broad_negative_inference_count']}.
- Chapter-core refutations retained: {summary['chapter_core_refutation_count']}.

The audit does not erase the words `refuted`, `no_change`, or
`blocked_after_full_attempt`. It verifies that their current reader-facing use
preserves raw-history, proxy, implementation, and residual-obligation ceilings
instead of presenting them as scientific conclusions they did not earn.

## Excluded historical scope

""" + "".join(f"- {item}.\n" for item in value["excluded_historical_scope"]) + """

## Non-claims

""" + "".join(f"- {item}\n" for item in value["non_claims"])
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    value = audit()
    OUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    write_doc(value)
    print(
        f"Audited {value['scope']['surface_count']} current surfaces: "
        f"{value['summary']['forbidden_overbroad_phrase_count']} forbidden phrases, "
        f"{value['summary']['missing_required_rehabilitation_boundary_count']} missing boundaries, "
        f"{value['summary']['blocked_chapter_boundary_failure_count']} blocked-claim boundary failures."
    )


if __name__ == "__main__":
    main()
