#!/usr/bin/env python3
"""Build and validate the exact post-v2.3 no-public-release closure record."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json"
SCHEMA = ROOT / "schemas/post_v2_3_cycle_no_release_record.schema.json"
READER_RECORD = ROOT / "editions/reader_manuscript/v2_0/reader_release_record.json"
CAMPAIGN = ROOT / "experiments/post_v2_3_evidence_campaigns/results/adjudication.json"
LEDGER = ROOT / "docs/post_v2_3_evidence_candidate_ledger.json"

CLOSURE_PATHS = [
    "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md",
    "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json",
    "docs/post_v2_3_chapter_quality_packets.md",
    "docs/post_v2_3_evidence_candidate_ledger.json",
    "docs/post_v2_3_evidence_candidate_ledger.md",
    "docs/post_v2_3_campaign_results.md",
    "experiments/post_v2_3_evidence_campaigns/preregistration.json",
    "experiments/post_v2_3_evidence_campaigns/results/program_result.json",
    "experiments/post_v2_3_evidence_campaigns/results/adjudication.json",
    "editions/reader_manuscript/v2_0/manifest.json",
    "editions/reader_manuscript/v2_0/reconciliation_approval.json",
    "editions/reader_manuscript/v2_0/reader_release_record.json",
    "editions/reader_manuscript/v2_0/html_artifact_manifest.json",
    "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0-html.zip",
    "docs/non_core_evidence_ledger.md",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    reader = load(READER_RECORD)
    campaign = load(CAMPAIGN)
    ledger = load(LEDGER)
    archive = ROOT / "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0-html.zip"
    return {
        "schema_version": "asi_stack.post_v2_3_cycle_no_release.v0",
        "record_id": "2026-07-13-post-v2-3-quality-reader-cycle-no-public-release",
        "recorded_date": "2026-07-13",
        "roadmap_id": "asi-stack-post-v2-3-quality-floor-reader-completion-2026-07-13",
        "decision": "no_public_living_book_release",
        "decision_basis": [
            "The cycle raises the editorial and formal quality floor without changing the 54-chapter architecture or book thesis.",
            "Five exact QCSA findings move only as narrow non-core synthetic evidence; all 54 chapter-core claims remain at argument.",
            "Both newly preregistered model comparisons ended in preserved structured-output protocol failures and accepted no-change dispositions.",
            "The selected 54-chapter curated HTML reader is already dispositioned by its own exact local artifact record and is not a public living-book deployment.",
            "Creating a new minor version merely for accumulated maintenance would violate the roadmap's coherent-delta version rule.",
        ],
        "latest_public_living_book_release": {
            "version": "v2.3.0",
            "tag": "v2.3.0",
            "source_commit": "e27661166e9105f37cb36d63b15795f80715ca24",
            "release_record": "release_records/2026-07-13-v2.3.0-qcsa-e2766116.json",
            "unchanged": True,
        },
        "local_reader_release": {
            "decision": reader["decision"],
            "release_id": reader["release_id"],
            "record_path": str(READER_RECORD.relative_to(ROOT)),
            "record_sha256": sha(READER_RECORD),
            "format": "curated_html",
            "chapter_records": 54,
            "archive_path": str(archive.relative_to(ROOT)),
            "archive_sha256": sha(archive),
            "archive_bytes": archive.stat().st_size,
            "public_deployment": False,
        },
        "evidence_disposition": {
            "candidate_count": ledger["candidate_count"],
            "candidate_dispositions": ledger["disposition_counts"],
            "accepted_transition_records": ledger["accepted_transition_count"],
            "campaign_status": campaign["status"],
            "campaign_dispositions": campaign["dispositions"],
            "chapter_core_claims": 54,
            "chapter_core_support_state": "argument",
            "support_state_effect": "none",
        },
        "closure_artifacts": [{"path": path, "sha256": sha(ROOT / path)} for path in CLOSURE_PATHS],
        "publication_effect": {
            "source_tag_created": False,
            "public_deployment_performed": False,
            "immutable_site_archive_created": False,
            "rights_grant_created": False,
            "source_commit_claimed": False,
        },
        "validation_status": "pass",
        "residuals": [
            "The mutable public living book remains the previously attested v2.3.0 release until a later explicit release transaction succeeds.",
            "The v2.0 curated-reader HTML archive is exact and locally released but is not publicly deployed or licensed by this cycle record.",
            "All 36 post-v2.3 model calls exhausted their output cap; 34 ended in unclosed reasoning blocks and two closed reasoning without producing an admissible final structured output.",
            "Governance-tax, useful-throughput, unsafe-release, and residual-pressure effects are not estimable from the failed output protocol.",
            "The 12/12 rollback result is limited to the declared disposable nine-surface local harness and its omission controls.",
            "No external-human prepublication review, independent institutional audit, screen-reader review, or legal opinion is claimed or required.",
            "No successor roadmap or empirical rerun is activated by closure.",
        ],
        "non_claims": [
            "does not publish, deploy, tag, or archive a new living-book release",
            "does not change, move, or overwrite the immutable v2.3.0 release history",
            "does not publicly deploy or grant rights to the local curated-reader archive",
            "does not promote any of the 54 chapter-core claims above argument",
            "does not convert raw reasoning text into final residual disclosure or task completion",
            "does not infer safety from zero unsafe releases when total releases are also zero",
            "does not establish model quality, production transfer, governance efficacy, residual honesty, AGI, or ASI",
            "does not claim independent external review, WCAG certification, or legal clearance",
        ],
    }


def validate(actual: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    try:
        jsonschema.validate(actual, load(SCHEMA))
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
    if actual != expected:
        errors.append("record differs from exact closure-artifact recomputation")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.write:
        OUT.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    if not OUT.is_file():
        raise SystemExit("no-release record absent; run with --write")
    actual = load(OUT)
    errors = validate(actual, expected)
    mutations = [
        ("false release", lambda x: x.__setitem__("decision", "public_release")),
        ("false deployment", lambda x: x["publication_effect"].__setitem__("public_deployment_performed", True)),
        ("support promotion", lambda x: x["evidence_disposition"].__setitem__("chapter_core_support_state", "prototype-backed")),
        ("reader digest drift", lambda x: x["local_reader_release"].__setitem__("archive_sha256", "0" * 64)),
        ("artifact omission", lambda x: x.__setitem__("closure_artifacts", x["closure_artifacts"][:-1])),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(actual)
        mutate(candidate)
        if not validate(candidate, expected):
            errors.append(f"negative mutation accepted: {label}")
    if errors:
        raise SystemExit("Post-v2.3 no-release record failed:\n - " + "\n - ".join(errors))
    print("Post-v2.3 no-release record passed: v2.3.0 remains latest public, exact local 54-chapter reader preserved, zero public publication effects, 54 argument-state cores, and 5 rejecting mutations.")


if __name__ == "__main__":
    main()
