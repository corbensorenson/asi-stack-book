#!/usr/bin/env python3
"""Validate the public-safe Circle seed-rule receipt slice.

This is a structural evidence-surface check. It keeps the Compact Generative
Systems chapter concrete about finite exact-regeneration and storage-accounting
facts without allowing those facts to turn into useful-compression,
codec-correctness, semantic-utility, deployed-generator, model-quality, or
support-state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_seed_rule_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_seed_rule_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_seed_rule_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_seed_rule_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "compact-generative-systems-and-residual-honesty.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "compact-generative-systems-and-residual-honesty.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
README_ROOT = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-seed-rule-receipt-slice",
    "slice_id": "circle_seed_rule_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-SEED-RULE-001",
    "kind": "seed_rule_exact_regeneration",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5",
    "receipt_content_fingerprint": "f0087293579f743e2d78c9bb6a1b64f6a699a73ae36b279595c7b29334e46c14",
    "pytest_summary": "2 passed in 4.52s",
    "contract_ready_pytest_summary": "1 passed in 2.80s",
    "transition_id": "v1_x_measured.circle_seed_rule_receipt.no_change",
    "claim_id": "compact-generative-systems.seed_rule_exact_regeneration_receipt_slice",
}

THEOREMS = ("GEN-T0001", "GEN-T0040", "GEN-T0041", "GEN-T0046", "GEN-T0048", "GEN-T0050")
RECOMMENDATIONS = (
    "SEED-RULE-USE-EXACT-REGENERATION-RECIPE",
    "SEED-RULE-SELECT-BOUNDED-SHORTER-CANDIDATE",
)
OUTPUT_HASHES = {
    "0f7f9f872d5aada01540380a5e8c18a0d61176b9de01707ee3e80b62fd7c855b": 21190,
    "1eda082a6f9d87e19e470e2046478f38b32deac8d1655f005a3de0d58add2b64": 4481,
    "00023e90230fe8011f1457fcc3076dfac56f1c4a84a6162cd99d4e12a56398e5": 8074,
    "332824b14a1db65ddb4941f1dfbb570c5802e6bf59aa69977dd46aa97fbfe2be": 1813,
    "2913a9256c7c7676b44688501dcd29a9fc0b0a43324fd130eeecd61cde09a2da": 98,
    "e02723e582d6fd1e9e052b5f1c9ac4683c27236b02a035a5fb640e5b0ba8a4c6": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "useful compression",
    "codec correctness",
    "semantic utility",
    "deployed generator behavior",
    "fallback execution",
    "downstream utility",
    "optimal search",
    "model quality",
    "context length",
    "runtime speed",
    "memory scaling",
    "benchmark performance",
    "transfer",
    "safety",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "fixture_n=128",
    "exact_regeneration=true",
    "generator_length=383",
    "explicit_length=454",
    "storage_saving=71",
    "bounded_search_candidate_count=3",
    "bounded_search_exact_candidate_count=2",
    "bounded_search_best_shorter_generator_shorter=true",
    "theorem_count=32",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
    "circle_seed_rule_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "seed-rule receipt",
    "exact-regeneration",
    "storage accounting",
    EXPECTED["contract_id"],
    EXPECTED["contract_content_fingerprint"],
    "fixture_n=128",
    "storage_saving=71",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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

    fixture = result.get("seed_rule_fixture", {})
    expected_fixture = {
        "artifact_id": "finite_circle",
        "fixture_n": 128,
        "exact_regeneration": True,
        "generator_length": 383,
        "explicit_length": 454,
        "storage_saving": 71,
        "storage_saving_positive": True,
        "generator_shorter": True,
        "generator_shorter_iff_positive_saving": True,
        "storage_saving_add_generator_length_eq_explicit_length": True,
        "bounded_search_candidate_count": 3,
        "bounded_search_exact_candidate_count": 2,
        "bounded_search_shorter_candidate_count": 1,
        "bounded_search_has_best_exact": True,
        "bounded_search_has_best_shorter": True,
        "bounded_search_exact_candidate_count_le_candidate_count": True,
        "bounded_search_best_exact_exists_iff_exact_count_positive": True,
        "bounded_search_best_exact_regenerates": True,
        "bounded_search_best_shorter_generator_shorter": True,
        "contract_ready_theorem_count": 32,
        "circle_ai_receipt_theorem_count": 32,
    }
    for key, expected in expected_fixture.items():
        if fixture.get(key) != expected:
            errors.append(f"{rel(RESULT)} seed_rule_fixture.{key} must remain {expected!r}.")
    if fixture.get("generated_object_length") != 128 or fixture.get("regenerated_object_matches_generated_object") is not True:
        errors.append(f"{rel(RESULT)} must preserve the finite exact-regeneration summary fields.")

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
    if receipt.get("theorem_count") != 32:
        errors.append(f"{rel(RESULT)} theorem_count must remain 32.")
    if receipt.get("evidence_fields") != {
        "fixture_n": 128,
        "exact_regeneration": True,
        "generator_length": 383,
        "explicit_length": 454,
        "storage_saving": 71,
        "bounded_search_candidate_count": 3,
        "bounded_search_exact_candidate_count": 2,
        "bounded_search_best_shorter_generator_shorter": True,
        "generator_shorter_iff_positive_saving": True,
    }:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded seed-rule receipt facts.")

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
                "not a codec",
                "not compression utility",
                "not semantic utility",
                "not a deployed generator",
                "not benchmark evidence",
                "not model-quality proof",
            ),
            errors,
        )

    boundary = result.get("circle_ai_certifier_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("request_passed") is not True:
        errors.append(f"{rel(RESULT)} must preserve request_passed=true for the seed-rule boundary.")
    require_fragments(
        rel(RESULT),
        text_blob(boundary),
        (
            "unsupported_fields",
            "model quality",
            "reasoning ability",
            "context length",
            "speed or memory scaling",
            "not compression utility",
            "not codec correctness",
            "not semantic utility",
            "not deployed generator behavior",
        ),
        errors,
    )

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 6:
        errors.append(f"{rel(RESULT)} must record exactly six successful commands.")
    else:
        seen_hashes: dict[str, int] = {}
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
        require_fragments(
            rel(RESULT),
            text_blob(commands),
            (
                "scripts/seed_rule_certify.py --format json",
                "ready=True fields=34 missing=0 theorems=32",
                "strict seed-rule acceptance receipt accepted",
                EXPECTED["pytest_summary"],
                EXPECTED["contract_ready_pytest_summary"],
            ),
            errors,
        )

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
    return result


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    transition = load_json(TRANSITION)
    checks = {
        "transition_id": EXPECTED["transition_id"],
        "claim_id": EXPECTED["claim_id"],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "support_state_effect": "blocks_promotion",
        "review_status": "accepted",
    }
    for key, expected in checks.items():
        if transition.get(key) != expected:
            errors.append(f"{rel(TRANSITION)} {key} must be {expected!r}.")
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            EXPECTED["contract_id"],
            EXPECTED["contract_content_fingerprint"],
            "fixture_n=128",
            "exact_regeneration=true",
            "storage_saving=71",
            "does not create an upward support-state transition",
            "chapter-core promotion",
            "no deployed generator",
            "no codec benchmark",
            "no downstream utility measurement",
            "no independent review",
            "does not prove useful compression",
            "does not promote the Compact Generative Systems chapter core claim",
        ),
        errors,
    )


def validate_surfaces(errors: list[str]) -> None:
    surface_files = (SUMMARY, README, CHAPTER, OUTLINE, APPENDIX_E, LEDGER, ROADMAP, README_ROOT, INDEX, STATUS, CHANGELOG)
    for path in surface_files:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        require_fragments(rel(path), text, SURFACE_FRAGMENTS, errors)

    reader_text = READER.read_text(encoding="utf-8", errors="ignore")
    require_fragments(rel(READER), reader_text, READER_FRAGMENTS, errors)

    structure = load_json(STRUCTURE)
    chapter = chapter_record(structure, "compact-generative-systems-and-residual-honesty")
    if not chapter:
        errors.append("book_structure.json missing compact-generative-systems-and-residual-honesty chapter.")
        return
    require_fragments(
        "book_structure.json compact chapter",
        text_blob(chapter),
        (
            "Circle seed-rule receipt-slice validation",
            "validate_circle_seed_rule_receipt_slice.py",
            EXPECTED["contract_id"],
            EXPECTED["kind"],
            EXPECTED["contract_content_fingerprint"],
            "fixture_n=128",
            "storage_saving=71",
            "no chapter-core promotion",
        ) + NON_CLAIMS,
        errors,
    )


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_surfaces(errors)
    if errors:
        print("Circle seed-rule receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Circle seed-rule receipt slice validation passed.")


if __name__ == "__main__":
    main()
