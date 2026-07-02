#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "adversarial_review_dossier" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "adversarial_review_dossier_probe.md"
CHAPTER = ROOT / "chapters" / "spinoza-verification-and-proof-carrying-claims.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "spinoza-verification-and-proof-carrying-claims.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ProofCarryingClaims.lean"

COMMAND = "python3 scripts/validate_adversarial_review_dossier_probe.py"
PROOF_TAG = "lean:spinoza.adversarial_review.dossier_probe_bridge"
CODEX_TEST_NAME = "Adversarial review dossier and verdict-quality probe"
REQUIRED_THEOREMS = ["adversarial_review_dossier_probe_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not prove semantic equivalence",
    "does not prove reviewer independence",
    "does not prove adversarial-probe quality",
    "does not prove verdict correctness",
    "does not run an LLM judge",
    "does not run a debate system",
    "does not promote the chapter support state",
]


DOSSIERS: list[dict[str, Any]] = [
    {
        "dossier_id": "review://scoped-accept-dissent-preserved",
        "expect_valid": True,
        "claim_id": "claim://proof-carrying-scope",
        "risk_class": "high",
        "dossier_refs": ["dossier://scope-map", "dossier://evidence-pack"],
        "dossier_boundary": "bounded to record-shape and source-citation scope",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["contradiction probe", "citation probe", "omission probe"],
        "findings": ["record shape is bounded and source refs are present"],
        "evidence_refs": ["evidence://scope-map", "evidence://source-note"],
        "dissent": ["citation reviewer notes no deployed verifier evidence"],
        "unresolved_issues": ["deployment and semantic-equivalence evidence absent"],
        "verdict": "accept_scoped",
        "required_actions": ["limit prose to record-shape discipline"],
        "constraint_effects": ["scope constrained by dissent and unresolved deployment evidence"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "review://mismatch-rejection",
        "expect_valid": True,
        "claim_id": "claim://semantic-equivalence-overreach",
        "risk_class": "critical",
        "dossier_refs": ["dossier://semantic-map", "dossier://counterexample"],
        "dossier_boundary": "bounded to mismatch between prose claim and formal target",
        "reviewer_roles": ["logic reviewer", "formalization reviewer", "red-team reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["formalization mismatch probe", "scope overclaim probe", "counterexample probe"],
        "findings": ["formal target is narrower than the prose claim"],
        "evidence_refs": ["evidence://formal-target", "evidence://mismatch-note"],
        "dissent": ["no dissent on rejection"],
        "unresolved_issues": ["prose rewrite needed before reuse"],
        "verdict": "reject",
        "required_actions": ["rewrite claim boundary", "block support promotion"],
        "constraint_effects": ["dispatch blocked until corrected mapping is reviewed"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "mismatch",
        "ledger_effect": "block",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://missing-dossier-refs",
        "expect_valid": False,
        "claim_id": "claim://missing-dossier",
        "risk_class": "high",
        "dossier_refs": [],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["contradiction probe"],
        "findings": ["accepts with no dossier refs"],
        "evidence_refs": ["evidence://finding"],
        "dissent": [],
        "unresolved_issues": [],
        "verdict": "accept_scoped",
        "required_actions": ["limit scope"],
        "constraint_effects": ["scope constrained"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://llm-judge-only-acceptance",
        "expect_valid": False,
        "claim_id": "claim://judge-only",
        "risk_class": "high",
        "dossier_refs": ["dossier://judge-only"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["llm judge"],
        "reviewer_independence": False,
        "judge_route": "llm_judge_only",
        "adversarial_probes": ["single judge critique"],
        "findings": ["judge says acceptable"],
        "evidence_refs": ["evidence://judge-output"],
        "dissent": [],
        "unresolved_issues": [],
        "verdict": "accept_scoped",
        "required_actions": ["limit scope"],
        "constraint_effects": ["scope constrained"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://missing-probes",
        "expect_valid": False,
        "claim_id": "claim://missing-probes",
        "risk_class": "critical",
        "dossier_refs": ["dossier://risk"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": [],
        "findings": ["accepts without probes"],
        "evidence_refs": ["evidence://risk"],
        "dissent": [],
        "unresolved_issues": [],
        "verdict": "accept_scoped",
        "required_actions": ["limit scope"],
        "constraint_effects": ["scope constrained"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://dissent-scope-erased",
        "expect_valid": False,
        "claim_id": "claim://dissent-erased",
        "risk_class": "high",
        "dossier_refs": ["dossier://dissent"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["dissent probe"],
        "findings": ["accepts despite dissent"],
        "evidence_refs": ["evidence://dissent"],
        "dissent": ["reviewer says deployment evidence is absent"],
        "unresolved_issues": ["deployment evidence absent"],
        "verdict": "accept_scoped",
        "required_actions": ["publish as accepted"],
        "constraint_effects": ["no constraint"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://action-verdict-without-actions",
        "expect_valid": False,
        "claim_id": "claim://action-missing",
        "risk_class": "high",
        "dossier_refs": ["dossier://action"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["action probe"],
        "findings": ["requires revision"],
        "evidence_refs": ["evidence://action"],
        "dissent": [],
        "unresolved_issues": ["needs revision"],
        "verdict": "revise",
        "required_actions": [],
        "constraint_effects": [],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "inadequate",
        "ledger_effect": "revise",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://prior-review-without-guard",
        "expect_valid": False,
        "claim_id": "claim://prior-review",
        "risk_class": "high",
        "dossier_refs": ["dossier://prior"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["prior review probe"],
        "findings": ["reuse prior review"],
        "evidence_refs": ["evidence://prior"],
        "dissent": [],
        "unresolved_issues": [],
        "verdict": "accept_scoped",
        "required_actions": ["limit scope"],
        "constraint_effects": ["scope constrained"],
        "prior_review_refs": ["review://old-rejection"],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "no_support_promotion",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "dossier_id": "invalid://support-state-promotion",
        "expect_valid": False,
        "claim_id": "claim://support-promotion",
        "risk_class": "high",
        "dossier_refs": ["dossier://promotion"],
        "dossier_boundary": "bounded review",
        "reviewer_roles": ["logic reviewer", "citation reviewer", "omission reviewer"],
        "reviewer_independence": True,
        "judge_route": "human_review_record",
        "adversarial_probes": ["promotion probe"],
        "findings": ["record shape present"],
        "evidence_refs": ["evidence://promotion"],
        "dissent": [],
        "unresolved_issues": [],
        "verdict": "accept_scoped",
        "required_actions": ["limit scope"],
        "constraint_effects": ["scope constrained"],
        "prior_review_refs": [],
        "unchanged_evidence_guard": "",
        "semantic_adequacy": "narrow",
        "ledger_effect": "promote_chapter_core",
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Adversarial review dossier probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def dossier_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dossier_id = str(record.get("dossier_id", "<missing>"))
    risk = str(record.get("risk_class", ""))
    verdict = str(record.get("verdict", ""))
    semantic_adequacy = str(record.get("semantic_adequacy", ""))
    constraint_text = text_blob(record.get("constraint_effects", []))
    guard_text = str(record.get("unchanged_evidence_guard", "")).lower()

    if not str(record.get("claim_id", "")).startswith("claim://"):
        errors.append(f"{dossier_id}: claim_id must use claim://.")
    if not str(record.get("dossier_id", "")).startswith(("review://", "invalid://")):
        errors.append(f"{dossier_id}: dossier_id must use review:// or invalid://.")
    if not nonempty_list(record, "dossier_refs"):
        errors.append(f"{dossier_id}: dossier_refs are required.")
    if not str(record.get("dossier_boundary", "")).strip():
        errors.append(f"{dossier_id}: dossier_boundary is required.")
    if risk in {"high", "critical"}:
        if len(record.get("reviewer_roles", [])) < 3:
            errors.append(f"{dossier_id}: high-risk reviews need at least three reviewer roles.")
        if record.get("reviewer_independence") is not True:
            errors.append(f"{dossier_id}: high-risk reviews need reviewer_independence.")
        if not nonempty_list(record, "adversarial_probes"):
            errors.append(f"{dossier_id}: high-risk reviews need adversarial_probes.")
        if not nonempty_list(record, "evidence_refs"):
            errors.append(f"{dossier_id}: high-risk reviews need evidence_refs.")
    if record.get("judge_route") == "llm_judge_only" and verdict.startswith("accept"):
        errors.append(f"{dossier_id}: LLM-judge-only records cannot accept high-risk claims.")
    if verdict.startswith("accept"):
        if not nonempty_list(record, "findings"):
            errors.append(f"{dossier_id}: accepted verdicts need findings.")
        if nonempty_list(record, "dissent") or nonempty_list(record, "unresolved_issues"):
            if "scope" not in constraint_text or "dissent" not in constraint_text:
                errors.append(f"{dossier_id}: accepted verdicts with dissent or unresolved issues need scope and dissent constraints.")
        if semantic_adequacy == "mismatch":
            errors.append(f"{dossier_id}: mismatched semantic adequacy cannot be accepted.")
    if verdict in {"reject", "revise", "escalate", "block"}:
        if not nonempty_list(record, "required_actions"):
            errors.append(f"{dossier_id}: action verdicts need required_actions.")
        if not nonempty_list(record, "constraint_effects"):
            errors.append(f"{dossier_id}: action verdicts need constraint_effects.")
    if nonempty_list(record, "prior_review_refs"):
        if not any(term in guard_text for term in ("new evidence", "corrected mapping", "cannot promote", "block")):
            errors.append(f"{dossier_id}: prior_review_refs need an unchanged_evidence_guard.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{dossier_id}: support_state_effect must remain none.")
    if record.get("ledger_effect") == "promote_chapter_core":
        errors.append(f"{dossier_id}: ledger_effect must not promote the chapter core claim.")

    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{dossier_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.adversarial_review_dossier_probe.v0",
        "result_id": "2026-07-02-adversarial-review-dossier-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_review_dossier_probe",
        "valid_dossier_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "dossier_count": len(DOSSIERS),
        "negative_controls": {
            "missing_dossier_refs_rejected": True,
            "llm_judge_only_acceptance_rejected": True,
            "missing_adversarial_probes_rejected": True,
            "dissent_scope_erasure_rejected": True,
            "action_verdict_without_actions_rejected": True,
            "prior_review_without_guard_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "coverage": {
            "scoped_accept_with_dissent_preserved": True,
            "mismatch_rejection_present": True,
            "reviewer_role_requirement": True,
            "dossier_refs_required": True,
            "adversarial_probes_required": True,
            "prior_review_guard_required": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ProofCarryingClaims",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "scoped_accept_dossier_present": True,
                "mismatch_rejection_dossier_present": True,
                "negative_controls_rejected": True,
                "llm_judge_only_rejected": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic review-dossier fixture only; no real tribunal, LLM judge, debate system, semantic-equivalence checker, reviewer-independence measurement, or verdict-quality benchmark was run.",
            "The Proof-Carrying Claims and Adversarial Review chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
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
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "spinoza-verification-and-proof-carrying-claims":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Proof-Carrying Claims chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "scopedAcceptDossierPresent",
        "mismatchRejectionDossierPresent",
        "negativeControlsRejected",
        "llmJudgeOnlyRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Adversarial Review Dossier Probe",
            rel(RESULT),
            "two valid synthetic review dossiers",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Adversarial review dossier and verdict-quality probe",
            rel(RESULT),
            "two valid synthetic review dossiers",
            "seven expected-invalid controls",
        ],
        READER: [
            "adversarial review dossier and verdict-quality probe",
            "two synthetic review dossiers",
            "not a deployed tribunal result",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Adversarial review dossier and verdict-quality probe",
            "deterministic synthetic review-dossier fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Adversarial review dossier and verdict-quality probe", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_adversarial_review_dossier_probe.py",
            "docs/adversarial_review_dossier_probe.md",
            "experiments/adversarial_review_dossier/results/2026-07-02-local.json",
            'run_validator("validate_adversarial_review_dossier_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required adversarial-review dossier surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for dossier in DOSSIERS:
        expect_valid = bool(dossier.get("expect_valid"))
        current_errors = dossier_errors(dossier)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{dossier.get('dossier_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic review dossiers.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Adversarial review dossier probe validation passed.")


if __name__ == "__main__":
    main()
