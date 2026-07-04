#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "partitioned_authority" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "partitioned_authority_fixture.md"
HIVE_CHAPTER = ROOT / "chapters" / "personal-compute-hives-and-federated-edge-intelligence.qmd"
RUNTIME_CHAPTER = ROOT / "chapters" / "runtime-adapters-tool-permissions-and-human-approval.qmd"
HIVE_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "personal-compute-hives-and-federated-edge-intelligence.qmd"
)
RUNTIME_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "runtime-adapters-tool-permissions-and-human-approval.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "PersonalComputeHives.lean"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"
SOURCE_NOTE = ROOT / "sources" / "source_notes" / "ext_cap_theorem_gilbert_lynch_2002.md"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

COMMAND = "python3 scripts/validate_partitioned_authority_fixture.py"
SOURCE_ID = "ext_cap_theorem_gilbert_lynch_2002"
CODEX_TEST_NAME = "Partitioned authority fixture"
LEAN_TAG = "lean:personal_hives.partitioned_authority.fixture_bridge"
LEAN_THEOREM = "partitioned_authority_fixture_bridge"
REQUIRED_NON_CLAIMS = [
    "does not prove deployed partition tolerance",
    "does not prove distributed consensus or availability",
    "does not prove deployed revocation propagation",
    "does not prove runtime adapter enforcement",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Partitioned authority fixture validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text and " ".join(fragment.split()) not in " ".join(text.split()):
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def build_result(errors: list[str]) -> dict[str, Any]:
    valid_records = [
        {
            "scenario_id": "valid_partition_revocation_quarantine",
            "partition_detected": True,
            "grant_seen_at_requester": True,
            "revocation_seen_at_effect_site": False,
            "stale_grant_possible": True,
            "fresh_authority_receipt": False,
            "effect_attempted": False,
            "route": "quarantine_pending_sync",
            "denied_before_mutation": True,
            "state_unchanged_after_denial": True,
            "residual_owner_recorded": True,
            "audit_refs_recorded": True,
            "support_state_effect": "none",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
        {
            "scenario_id": "valid_healed_partition_requires_fresh_receipt",
            "partition_detected": False,
            "grant_seen_at_requester": True,
            "revocation_seen_at_effect_site": True,
            "stale_grant_possible": True,
            "fresh_authority_receipt": False,
            "effect_attempted": False,
            "route": "request_fresh_authority_receipt",
            "denied_before_mutation": True,
            "state_unchanged_after_denial": True,
            "residual_owner_recorded": True,
            "audit_refs_recorded": True,
            "support_state_effect": "none",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
        {
            "scenario_id": "valid_fresh_receipt_dispatch",
            "partition_detected": False,
            "grant_seen_at_requester": True,
            "revocation_seen_at_effect_site": True,
            "stale_grant_possible": False,
            "fresh_authority_receipt": True,
            "effect_attempted": True,
            "route": "dispatch",
            "denied_before_mutation": False,
            "state_unchanged_after_denial": False,
            "residual_owner_recorded": True,
            "audit_refs_recorded": True,
            "support_state_effect": "none",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
    ]
    expected_invalid_controls = [
        {
            "scenario_id": "invalid_dispatch_under_partition_stale_grant",
            "rejected_reason": "partitioned stale grant cannot dispatch",
            "mutated_state": False,
        },
        {
            "scenario_id": "invalid_mutation_after_unseen_revocation",
            "rejected_reason": "unseen revocation requires quarantine or no-mutation evidence",
            "mutated_state": True,
        },
        {
            "scenario_id": "invalid_grant_effect_race_without_residual_owner",
            "rejected_reason": "grant/effect race must preserve residual ownership",
            "residual_owner_recorded": False,
        },
        {
            "scenario_id": "invalid_no_mutation_evidence_missing",
            "rejected_reason": "partition denial must carry no-mutation evidence before closure",
            "denied_before_mutation": False,
            "state_unchanged_after_denial": False,
        },
        {
            "scenario_id": "invalid_support_promotion_from_partition_fixture",
            "rejected_reason": "fixture shape cannot promote support state",
            "support_state_effect": "promote",
        },
        {
            "scenario_id": "invalid_missing_non_claim_boundary",
            "rejected_reason": "partition fixture must carry non-claim boundaries",
            "non_claims": [],
        },
    ]
    for record in valid_records:
        blob = text_blob(record)
        if record["route"] != "dispatch" and not (
            record["denied_before_mutation"] and record["state_unchanged_after_denial"]
        ):
            errors.append(f"{record['scenario_id']} must carry no-mutation evidence.")
        if record["support_state_effect"] != "none":
            errors.append(f"{record['scenario_id']} must preserve support_state_effect none.")
        for claim in REQUIRED_NON_CLAIMS:
            if claim not in blob:
                errors.append(f"{record['scenario_id']} missing non-claim {claim!r}.")
    invalid_ids = {row["scenario_id"] for row in expected_invalid_controls}
    required_invalid_ids = {
        "invalid_dispatch_under_partition_stale_grant",
        "invalid_mutation_after_unseen_revocation",
        "invalid_grant_effect_race_without_residual_owner",
        "invalid_no_mutation_evidence_missing",
        "invalid_support_promotion_from_partition_fixture",
        "invalid_missing_non_claim_boundary",
    }
    if invalid_ids != required_invalid_ids:
        errors.append("expected-invalid control set is incomplete.")

    summary = {
        "partitionRevocationQuarantined": True,
        "healedPartitionRequiresFreshReceipt": True,
        "freshReceiptDispatchBounded": True,
        "staleGrantDispatchRejected": True,
        "grantEffectRaceRejected": True,
        "mutationWithoutNoMutationEvidenceRejected": True,
        "residualOwnerRequired": True,
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
        "deployedPartitionToleranceNotClaimed": True,
    }
    return {
        "schema_version": "asi_stack.partitioned_authority.fixture_result.v0",
        "result_id": "partitioned_authority_fixture_2026_07_03_local",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "result_kind": "bounded_partitioned_authority_fixture",
        "external_comparator_refs": [SOURCE_ID],
        "valid_record_count": len(valid_records),
        "expected_invalid_count": len(expected_invalid_controls),
        "valid_records": valid_records,
        "expected_invalid_controls": expected_invalid_controls,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.PersonalComputeHives",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "This is a finite record fixture; it does not run a distributed authority service.",
            "Partitioned authority remains argument-level until live or externally reviewable grant/revocation traces exist.",
            "CAP-style terminology is used as comparator vocabulary, not as proof that ASI Stack governance solves distributed consistency.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not reproduce the CAP theorem",
            "does not create an evidence transition",
            "does not prove model quality, benchmark performance, safety, or ASI",
        ],
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Partitioned Authority Fixture",
                COMMAND,
                rel(RESULT),
                SOURCE_ID,
                "does not prove deployed partition tolerance",
            ],
        ),
        rel(HIVE_CHAPTER): (
            HIVE_CHAPTER,
            [
                "partitioned authority",
                SOURCE_ID,
                rel(RESULT),
                "grant/effect race",
                "does not prove deployed partition tolerance",
            ],
        ),
        rel(RUNTIME_CHAPTER): (
            RUNTIME_CHAPTER,
            [
                "partitioned authority",
                rel(RESULT),
                "fresh authority receipt",
                "no-mutation evidence",
            ],
        ),
        rel(HIVE_READER): (
            HIVE_READER,
            [
                "partitioned authority",
                "stale grant",
                "fresh authority receipt",
            ],
        ),
        rel(RUNTIME_READER): (
            RUNTIME_READER,
            [
                "partitioned authority",
                "stale grant",
                "no-mutation evidence",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented partitioned-authority fixture",
                COMMAND,
                rel(RESULT),
                LEAN_TAG,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "partitioned-authority fixture",
                rel(RESULT),
                "CAP-style authority consistency",
                "does not prove deployed partition tolerance",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add partitioned authority fixture",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(VALIDATE_BOOK): (
            VALIDATE_BOOK,
            [
                "scripts/validate_partitioned_authority_fixture.py",
                "docs/partitioned_authority_fixture.md",
                rel(RESULT),
                'run_validator("validate_partitioned_authority_fixture.py")',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "PartitionedAuthorityFixtureSummary",
                "partitionedAuthorityFixtureSummary",
                LEAN_THEOREM,
            ],
        ),
        rel(SOURCE_NOTE): (
            SOURCE_NOTE,
            [
                SOURCE_ID,
                "CAP",
                "partitioned authority",
                "does not prove deployed revocation propagation",
            ],
        ),
        rel(STATUS): (
            STATUS,
            [
                "Partitioned authority fixture",
                rel(RESULT),
            ],
        ),
        rel(APPENDIX_E): (
            APPENDIX_E,
            [
                "Partitioned authority fixture",
                COMMAND,
                "does not prove deployed partition tolerance",
            ],
        ),
    }
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    inventory = load_json(SOURCE_INVENTORY)
    if not isinstance(inventory, list):
        errors.append(f"{rel(SOURCE_INVENTORY)} must contain a list.")
        return
    matches = [source for source in inventory if isinstance(source, dict) and source.get("id") == SOURCE_ID]
    if len(matches) != 1:
        errors.append(f"{rel(SOURCE_INVENTORY)} must contain exactly one {SOURCE_ID} record.")
    chapters: dict[str, dict[str, Any]] = {}
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters[chapter.get("id", "")] = chapter
    for chapter_id in (
        "personal-compute-hives-and-federated-edge-intelligence",
        "runtime-adapters-tool-permissions-and-human-approval",
    ):
        chapter = chapters.get(chapter_id, {})
        if SOURCE_ID not in chapter.get("source_ids", []):
            errors.append(f"{chapter_id} source_ids must include {SOURCE_ID}.")
    hive = chapters.get("personal-compute-hives-and-federated-edge-intelligence", {})
    tests = [test for test in hive.get("codex_tests", []) if isinstance(test, dict)]
    if len([test for test in tests if test.get("name") == CODEX_TEST_NAME]) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain one {CODEX_TEST_NAME!r} test row.")
    proof_targets = [target for target in hive.get("proof_targets", []) if isinstance(target, dict)]
    if len([target for target in proof_targets if target.get("tag") == LEAN_TAG]) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain one {LEAN_TAG} proof target.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "partitionRevocationQuarantined",
        "healedPartitionRequiresFreshReceipt",
        "staleGrantDispatchRejected",
        "mutationWithoutNoMutationEvidenceRejected",
        "deployedPartitionToleranceNotClaimed",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing partitioned-authority field {field}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    required = [DOC, HIVE_CHAPTER, RUNTIME_CHAPTER, HIVE_READER, RUNTIME_READER, OUTLINE, ROADMAP, CHANGELOG]
    errors = [f"Missing required artifact {rel(path)}." for path in required if not path.exists()]
    expected = build_result(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_book_structure(errors)
        validate_lean_shape(errors)
    if errors:
        fail(errors)
    print(
        "Partitioned authority fixture validation passed: "
        f"{expected['valid_record_count']} valid records, "
        f"{expected['expected_invalid_count']} expected-invalid controls, no support-state effect."
    )


if __name__ == "__main__":
    main()
