#!/usr/bin/env python3
"""Build and validate the terminal P4 no-public-release transaction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release_records/2026-07-14-post-v2-3-handoff-reader-formats-evidence-renewal-no-public-release.json"
SCHEMA = ROOT / "schemas/post_v2_3_handoff_reader_formats_evidence_renewal_terminal_record.schema.json"
SUBSTANTIVE_COMMIT = "f93a4d8fa51ac7cafa0db180d7360ee1fb2c498c"
CLOSURE_PATHS = [
    "docs/post_v2_3_clean_handoff_receipt.md",
    "docs/post_v2_3_handoff_reader_formats_evidence_renewal_attestation_receipt.md",
    "editions/reader_manuscript/v2_0/reader_release_record.json",
    "editions/reader_manuscript/v2_0/text_format_profile.json",
    "editions/reader_manuscript/v2_0/format_review_matrix.json",
    "editions/reader_manuscript/v2_0/epub_disposition.json",
    "editions/reader_manuscript/v2_0/pdf_disposition.json",
    "editions/reader_manuscript/v2_0/docx_disposition.json",
    "editions/reader_manuscript/v2_1/manifest.json",
    "docs/post_v2_3_external_anchoring_and_completeness_audit.md",
    "experiments/post_v2_3_evidence_protocol_renewal/preflight/attempt_1_result.json",
    "experiments/post_v2_3_evidence_protocol_renewal/flagship/results/adjudication.json",
    "docs/post_v2_3_governance_tax_flagship_renewal_results.md",
    "evidence_transitions/post_v2_3/governance_tax_natural_work_renewal_no_change.json",
    "experiments/theseus_pretraining_readiness_currentness_import/results/2026-07-14-local.json",
    "docs/theseus_pretraining_readiness_currentness_import.md",
    "claim_decisions/v1_x_core_claim_dispositions.json",
    "docs/non_core_evidence_ledger.md",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    return {
        "schema_version": "asi_stack.post_v2_3_handoff_reader_formats_evidence_renewal_terminal.v0",
        "record_id": "2026-07-14-post-v2-3-handoff-reader-formats-evidence-renewal-no-public-release",
        "recorded_date": "2026-07-14",
        "roadmap_id": "asi-stack-post-v2-3-handoff-reader-formats-evidence-renewal-2026-07-13",
        "decision": "exact_local_reader_multiformat_disposition_no_public_release",
        "substantive_source_commit": SUBSTANTIVE_COMMIT,
        "latest_public_living_book_release": {
            "version": "v2.3.0",
            "tag": "v2.3.0",
            "source_commit": "e27661166e9105f37cb36d63b15795f80715ca24",
            "release_record": "release_records/2026-07-13-v2.3.0-qcsa-e2766116.json",
            "unchanged": True,
        },
        "reader_disposition": {
            "chapter_count": 54,
            "approved_exact_local_formats": ["canonical_html", "docx"],
            "blocked_formats": ["epub", "pdf"],
            "deferred_formats": ["audio", "embedded_audio"],
            "source_only_successor": "editions/reader_manuscript/v2_1/manifest.json",
            "public_release": False,
        },
        "source_disposition": {
            "chapter_audit_count": 10,
            "tier_2_rows": 37,
            "accepted_new_sources": 4,
            "inserted_controls": 9,
            "new_chapters": 0,
            "support_state_effect": "none",
        },
        "evidence_disposition": {
            "preflight_parseable_finals": 4,
            "flagship_candidates": 32,
            "flagship_calls": 64,
            "independently_correct": 2,
            "useful_releases": 0,
            "unsafe_releases": 0,
            "exact_rollbacks": 32,
            "metadata_erratum": "declared_8_of_8_exact_task_file_9_of_9_blocks_promotion",
            "transition": "no_change_blocks_promotion",
            "theseus_readiness": "YELLOW_12_wired_2_implemented_5_partial_1_frozen",
            "core_claim_count": 54,
            "core_support_state": "argument",
            "support_state_effect": "none",
        },
        "closure_artifacts": [
            {"path": path, "sha256": sha(ROOT / path)} for path in CLOSURE_PATHS
        ],
        "publication_effect": {
            "source_tag_created": False,
            "public_reader_deployment_performed": False,
            "immutable_site_archive_created": False,
            "rights_grant_created": False,
            "living_book_version_changed": False,
        },
        "validation_status": "pass",
        "residuals": [
            "EPUB structural and deterministic replay checks pass, but Apple Books application inspection remains blocked by the native accessibility bridge.",
            "PDF structural, deterministic, page-complete, and internal visual checks pass, but Preview application inspection remains blocked by the native control bridge.",
            "DOCX is an approved exact local artifact; this record does not claim Microsoft Word review, public deployment, or a public rights grant.",
            "The v2.1 reader workspace contains the source-renewal delta only and has no approved format artifact or release identity.",
            "Only two of 32 flagship candidates were independently correct, so neither route produced a useful release denominator.",
            "The post-outcome 8-of-8 metadata declaration disagrees with the immutable 9-of-9 task file and independently blocks evidence promotion.",
            "Project Theseus readiness is YELLOW and bounded to one clean same-commit report replay; runtime, model, deployment, and safety transfer remain unestablished.",
            "No successor roadmap is activated by this terminal transaction.",
        ],
        "non_claims": [
            "does not publish or publicly deploy a new reader edition",
            "does not create a new living-book version, source tag, or immutable site archive",
            "does not grant a repository-wide, reader, or source license",
            "does not approve EPUB or PDF for release",
            "does not infer safety from zero unsafe releases when useful releases are also zero",
            "does not generalize the exact governance-tax result beyond the frozen local tasks, model, evaluator, and rollback surfaces",
            "does not promote any of the 54 chapter-core claims above argument",
            "does not establish external-human review, screen-reader review, legal clearance, or WCAG certification",
            "does not establish model quality, production readiness, governance efficacy, AGI, or ASI",
        ],
    }


def errors(actual: dict, expected: dict) -> list[str]:
    failures: list[str] = []
    try:
        jsonschema.validate(actual, load(SCHEMA))
    except jsonschema.ValidationError as exc:
        failures.append(f"schema: {exc.message}")
    if actual != expected:
        failures.append("record differs from exact P0-P3 artifact recomputation")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.write:
        OUT.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    if not OUT.is_file():
        raise SystemExit("terminal record absent; run with --write")
    actual = load(OUT)
    failures = errors(actual, expected)
    mutations = [
        ("false public release", lambda x: x["publication_effect"].__setitem__("public_reader_deployment_performed", True)),
        ("false EPUB approval", lambda x: x["reader_disposition"]["blocked_formats"].remove("epub")),
        ("support promotion", lambda x: x["evidence_disposition"].__setitem__("core_support_state", "prototype-backed")),
        ("unsafe denominator laundering", lambda x: x["evidence_disposition"].__setitem__("useful_releases", 2)),
        ("erratum erased", lambda x: x["evidence_disposition"].__setitem__("metadata_erratum", "none")),
        ("artifact omission", lambda x: x.__setitem__("closure_artifacts", x["closure_artifacts"][:-1])),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(actual)
        mutate(candidate)
        if not errors(candidate, expected):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Post-v2.3 terminal record failed:\n - " + "\n - ".join(failures))
    print("Post-v2.3 terminal record passed: exact local HTML+DOCX disposition, EPUB/PDF blocked, 4-source/9-control renewal, 32-candidate flagship no-change, YELLOW Theseus import, v2.3.0 unchanged, and 6 rejecting mutations.")


if __name__ == "__main__":
    main()
