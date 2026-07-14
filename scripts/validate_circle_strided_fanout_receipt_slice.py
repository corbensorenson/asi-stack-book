#!/usr/bin/env python3
"""Validate the public-safe Circle strided fanout receipt slice.

This is a structural evidence-surface check. It keeps the Coil Attention
chapter concrete about Circle finite stride-coverage and duplicate-budget
accounting facts without allowing those facts to turn into search-quality,
retrieval-quality, routing-quality, runtime, model-quality, or support-state
claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_strided_fanout_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_strided_fanout_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_strided_fanout_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_strided_fanout_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
README_ROOT = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
NO_PROMOTION_DIRS = (
    ROOT / "evidence_transitions" / "v1_x_measured",
    ROOT / "evidence_transitions" / "post_v2",
    ROOT / "evidence_transitions" / "post_v2_1",
    ROOT / "evidence_transitions" / "post_v2_3",
)

EXPECTED = {
    "result_id": "2026-07-05-local-circle-strided-fanout-receipt-slice",
    "slice_id": "circle_strided_fanout_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-FANOUT-001",
    "kind": "strided_candidate_fanout",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799",
    "receipt_content_fingerprint": "8df401cbc35c6446adac27650a661cfb3e8dd55da5dd4a13065bbb1faa1c07d9",
    "pytest_summary": "3 passed in 4.65s",
    "contract_ready_pytest_summary": "1 passed in 2.77s",
    "transition_id": "v1_x_measured.circle_strided_fanout_receipt.no_change",
    "claim_id": "circle-calculus.strided_fanout_receipt_slice",
}

THEOREMS = ("AIT-T0001", "AIT-T0002", "AIT-T0003", "AIT-T0173")
RECOMMENDATIONS = (
    "FANOUT-USE-FULL-COVERAGE-STRIDE-CYCLE",
    "FANOUT-AUDIT-DUPLICATE-COLLAPSED-BUDGET",
)
OUTPUT_HASHES = {
    "5c80d5fdcb74cb80702d7881a554b34fcb8a9f79c1425e7047177afc8b7ea7db": 6554,
    "3b0f37ab709e889d2c0fe48658c118b6d1a8a6a61680dbbb2b99960a08c634f5": 14727,
    "b42efb4930f735568765585283063ee713e940be7cf5ff65da185eaeaff75c5a": 2283,
    "fb0bc15ff5e6be109843aff1e8ea3bca0975c4c17162c6c2553629bd88b76515": 1519,
    "5e764caa97fd868cd3f2a2ed51ec2be309fe521a22c655d7a1c9aeb4dbd15f43": 98,
    "2f1cb16c1dd9bb60a700a651b751ec6de3233db6bb10901b373ae4748a9f114f": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "search quality",
    "retrieval quality",
    "routing quality",
    "sparse-attention quality",
    "model quality",
    "context length",
    "throughput",
    "latency",
    "runtime speed",
    "memory scaling",
    "deployment readiness",
    "transfer",
    "benchmark performance",
    "safety",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "context_length=12",
    "stride=5",
    "gcd=1",
    "predicted_reach=12",
    "full_coverage=true",
    "candidate_budget=12",
    "duplicate_count=0",
    "effective_candidate_budget=12",
    "theorem_count=4",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
    "circle_strided_fanout_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "strided fanout receipt",
    "finite stride cycle",
    "duplicate-collapse",
    EXPECTED["contract_id"],
    EXPECTED["contract_content_fingerprint"],
    "full_coverage=true",
    "duplicate_count=0",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def accepted_no_promotion_count() -> int:
    """Derive the live public count instead of freezing a historical total."""
    count = 0
    for directory in NO_PROMOTION_DIRS:
        for path in directory.glob("*.json"):
            record = load_json(path)
            if (
                isinstance(record, dict)
                and record.get("transition_effect") == "no_change"
                and record.get("support_state_effect") == "blocks_promotion"
                and record.get("transition_validity_state") == "review_accepted"
                and record.get("review_status") == "accepted"
            ):
                count += 1
    return count


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lower = " ".join(text.lower().split())
    for fragment in fragments:
        normalized = " ".join(fragment.lower().split())
        if normalized not in lower:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def validate_result(errors: list[str]) -> dict[str, Any]:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return {}
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain a JSON object.")
        return {}

    if "/Users/" in text_blob(result):
        errors.append(f"{rel(RESULT)} must not contain absolute local user paths.")
    for key in ("result_id", "slice_id"):
        if result.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} {key} must be {EXPECTED[key]!r}.")

    project = result.get("external_project", {})
    if not isinstance(project, dict) or project.get("git_commit") != EXPECTED["git_commit"]:
        errors.append(f"{rel(RESULT)} must record Circle commit {EXPECTED['git_commit']}.")
    if project.get("worktree_state") != "clean_before_commands":
        errors.append(f"{rel(RESULT)} must record the clean external worktree boundary.")

    fixture = result.get("fanout_fixture", {})
    expected_fixture = {
        "context_length": 12,
        "stride": 5,
        "start_index": 0,
        "path_length": 12,
        "gcd": 1,
        "orbit": [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7],
        "candidate_path": [7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5, 0],
        "candidate_budget": 12,
        "unique_candidate_count": 12,
        "effective_candidate_budget": 12,
        "duplicate_count": 0,
        "candidate_budget_accounting": True,
        "candidate_budget_shortfall": 0,
        "effective_budget_matches_unique_candidates": True,
        "effective_budget_reaches_predicted_reach": True,
        "predicted_reach": 12,
        "full_coverage": True,
        "ordinary_baselines": ["sequential_fanout", "random_fanout", "round_robin_fanout", "local_window"],
        "contract_ready_theorem_count": 4,
        "circle_ai_receipt_theorem_count": 4,
    }
    if fixture != expected_fixture:
        errors.append(f"{rel(RESULT)} fanout_fixture drifted from the recorded Circle fanout facts.")

    receipt = result.get("accepted_receipt", {})
    if not isinstance(receipt, dict):
        errors.append(f"{rel(RESULT)} accepted_receipt must be an object.")
        return result
    for key in (
        "contract_id",
        "kind",
        "receipt_schema",
        "schema_id",
        "pack_content_fingerprint",
        "contract_content_fingerprint",
        "receipt_content_fingerprint",
    ):
        if receipt.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} accepted_receipt.{key} must be {EXPECTED[key]!r}.")
    if receipt.get("accepted") is not True:
        errors.append(f"{rel(RESULT)} accepted_receipt.accepted must be true.")
    if tuple(receipt.get("required_theorem_ids", [])) != THEOREMS:
        errors.append(f"{rel(RESULT)} theorem IDs must remain {THEOREMS}.")
    if tuple(receipt.get("required_recommendation_ids", [])) != RECOMMENDATIONS:
        errors.append(f"{rel(RESULT)} recommendation IDs must remain {RECOMMENDATIONS}.")
    if receipt.get("theorem_count") != 4:
        errors.append(f"{rel(RESULT)} theorem_count must remain 4.")
    if receipt.get("evidence_fields") != {
        "context_length": 12,
        "stride": 5,
        "predicted_reach": 12,
        "full_coverage": True,
        "duplicate_count": 0,
        "effective_candidate_budget": 12,
    }:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded fanout receipt facts.")

    recommendations = receipt.get("planner_recommendations", [])
    if not isinstance(recommendations, list) or len(recommendations) != 2:
        errors.append(f"{rel(RESULT)} planner_recommendations must record exactly two recommendations.")
    else:
        ids = [rec.get("id") for rec in recommendations if isinstance(rec, dict)]
        if tuple(ids) != RECOMMENDATIONS:
            errors.append(f"{rel(RESULT)} planner_recommendations must remain {RECOMMENDATIONS}.")
        require_fragments(
            rel(RESULT),
            text_blob(recommendations),
            (
                "not a search, retrieval, routing-quality, runtime, or model-quality proof",
                "not a ranking, recall, retrieval-quality, throughput, or model-quality theorem",
            ),
            errors,
        )

    boundary = result.get("circle_ai_certifier_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("request_passed") is not True:
        errors.append(f"{rel(RESULT)} must preserve request_passed=true for the fanout boundary.")
    require_fragments(
        rel(RESULT),
        text_blob(boundary),
        ("unsupported_fields", "model-quality improvement", "search-quality improvement", "throughput or latency", "optimal candidate schedule"),
        errors,
    )

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 6:
        errors.append(f"{rel(RESULT)} must record exactly six successful commands.")
    else:
        seen_hashes: dict[str, int] = {}
        command_text = text_blob(commands)
        for command in commands:
            if not isinstance(command, dict):
                errors.append(f"{rel(RESULT)} commands must be objects.")
                continue
            if command.get("verification_result") != "pass":
                errors.append(f"{rel(RESULT)} command {command.get('command')} did not record pass.")
            sha = command.get("output_sha256")
            size = command.get("output_bytes")
            if isinstance(sha, str) and isinstance(size, int):
                seen_hashes[sha] = size
        for sha, size in OUTPUT_HASHES.items():
            if seen_hashes.get(sha) != size:
                errors.append(f"{rel(RESULT)} missing output hash {sha} with byte size {size}.")
        for fragment in (
            "PYTHONPATH=. python3 scripts/strided_candidate_fanout_certify.py --context-length 12 --stride 5",
            "ready=True fields=12 missing=0 theorems=4",
            "strict strided fanout acceptance receipt accepted",
            EXPECTED["pytest_summary"],
            EXPECTED["contract_ready_pytest_summary"],
        ):
            if fragment not in command_text:
                errors.append(f"{rel(RESULT)} command summaries missing {fragment!r}.")

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
    return result


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    transition = load_json(TRANSITION)
    if not isinstance(transition, dict):
        errors.append(f"{rel(TRANSITION)} must contain a JSON object.")
        return
    expected_pairs = {
        "transition_id": EXPECTED["transition_id"],
        "claim_id": EXPECTED["claim_id"],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "support_state_effect": "blocks_promotion",
        "review_status": "accepted",
    }
    for key, expected in expected_pairs.items():
        if transition.get(key) != expected:
            errors.append(f"{rel(TRANSITION)} {key} must be {expected!r}.")
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            "does not create an upward support-state transition",
            "chapter core",
            "search quality",
            "retrieval quality",
            "routing quality",
            "optimal candidate schedule",
            "no deployed candidate-fanout trace",
            rel(SUMMARY),
            rel(RESULT),
            "scripts/validate_circle_strided_fanout_receipt_slice.py",
        ),
        errors,
    )


def validate_surfaces(errors: list[str]) -> None:
    no_promotion_count = accepted_no_promotion_count()
    for path in (SUMMARY, README):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        require_fragments(rel(path), path.read_text(encoding="utf-8", errors="ignore"), SURFACE_FRAGMENTS, errors)

    surface_requirements = {
        CHAPTER: SURFACE_FRAGMENTS,
        READER: READER_FRAGMENTS,
        OUTLINE: SURFACE_FRAGMENTS,
        APPENDIX_E: ("Circle strided fanout receipt-slice validation", EXPECTED["contract_id"], "circle_strided_fanout_receipt_no_change.json"),
        LEDGER: (
            f"Accepted no-promotion side-lane decisions | {no_promotion_count} accepted `blocks_promotion` decisions; no support-state movement.",
            EXPECTED["claim_id"],
            rel(SUMMARY),
            rel(TRANSITION),
            EXPECTED["contract_id"],
            "full_coverage=true",
            "duplicate_count=0",
            "does not promote any chapter core claim",
        ),
        STATUS: (f"{no_promotion_count} accepted `blocks_promotion`", rel(SUMMARY), "strided candidate-fanout"),
        ROADMAP: (EXPECTED["contract_id"], "strided candidate-fanout", "circle_strided_fanout_receipt_no_change.json", "56 accepted"),
        CHANGELOG: ("Import Circle strided fanout receipt slice", EXPECTED["contract_id"], "3 passed in 4.65s", "1 passed in 2.77s"),
    }
    for path, fragments in surface_requirements.items():
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        require_fragments(rel(path), path.read_text(encoding="utf-8", errors="ignore"), fragments, errors)

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain a JSON object.")
        return
    chapter = chapter_record(structure, "coil-attention-cyclic-memory-and-recurrence-contracts")
    if not chapter:
        errors.append("Missing Coil Attention chapter record in book_structure.json.")
        return
    tests = text_blob(chapter.get("codex_tests", []))
    require_fragments(
        f"{rel(STRUCTURE)} coil-attention codex_tests",
        tests,
        (
            "Circle strided fanout receipt-slice validation",
            "CC-AI-CONTRACT-FANOUT-001",
            "full_coverage=true",
            "duplicate_count=0",
            "circle_strided_fanout_receipt_no_change.json",
            "no search-quality, retrieval-quality, routing-quality",
        ),
        errors,
    )
    gaps = text_blob(chapter.get("open_evidence_gaps", []))
    require_fragments(
        f"{rel(STRUCTURE)} coil-attention open_evidence_gaps",
        gaps,
        (
            "Circle strided fanout receipt slice",
            "CC-AI-CONTRACT-FANOUT-001",
            "full_coverage=true",
            "duplicate_count=0",
            "no search quality",
        ),
        errors,
    )


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_surfaces(errors)
    if errors:
        print("Circle strided fanout receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Circle strided fanout receipt slice validation passed: "
        "1 structural external-project fanout receipt, 2 recommendations, "
        "4 theorem IDs, 0 support-state promotions."
    )


if __name__ == "__main__":
    main()
