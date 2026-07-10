#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "contestability_worked_example" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "contestability_worked_example.md"
CHAPTER = ROOT / "chapters" / "moral-uncertainty-and-value-conflict.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "moral-uncertainty-and-value-conflict.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ValueConflict.lean"

COMMAND = "python3 scripts/validate_contestability_worked_example.py"
PROOF_TAG = "lean:values.conflict.contestability_example_bridge"
CODEX_TEST_NAME = "Contestability worked example fixture"
SCENARIO_ID = "contestability://synthetic-care-memory-export-001"
REQUIRED_NON_CLAIMS = [
    "does not prove moral correctness",
    "does not prove legal rights",
    "does not prove reviewer independence",
    "does not prove export usability",
    "does not prove fork safety",
    "does not promote support state",
]


VALID_SCENARIO: dict[str, Any] = {
    "scenario_id": SCENARIO_ID,
    "scenario_kind": "synthetic_contestability_worked_example",
    "value_conflict_record": {
        "conflict_id": "value-conflict://care-memory-export-001",
        "value_axes": [
            "privacy",
            "safety",
            "autonomy",
            "accountability",
        ],
        "stakeholders": [
            "requesting user",
            "care team",
            "affected third party",
        ],
        "stakes": "high-impact because the request touches safety context, private memory, and third-party material",
        "reversibility": "partial; audit visibility is reversible, but disclosure and fork propagation are not fully reversible",
        "authority_or_consent_boundary": "the system may not disclose third-party private material or widen action authority without review",
        "evidence_required": [
            "audit-log digest",
            "source-memory inventory",
            "withheld-material explanation",
            "review receipt",
        ],
        "review_route": "independent human or tribunal review before high-impact disclosure or fork approval",
        "decision_state": "bounded_decision",
        "bounded_decision": {
            "allowed": [
                "redacted audit packet",
                "scoped exit export",
            ],
            "blocked": [
                "raw third-party memory export",
                "unreviewed fork",
            ],
        },
        "authority_effect": "narrow action to redacted audit plus scoped exit export; deny unsafe fork until safety obligations are recorded",
        "dissent_payload": [
            "requesting user contests withheld private context",
            "reviewer records that withholding is safety and privacy bounded, not moral settlement",
        ],
        "residual_uncertainty": [
            "whether the withheld material is necessary for meaningful exit",
            "whether a future fork can satisfy safety and privacy obligations",
        ],
        "expiry_or_revisit_condition": "revisit after review receipt or new consent artifact, no later than the next capability replacement gate",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    "governance_right_records": [
        {
            "right_id": "governance-right://care-memory-audit-001",
            "right_type": "audit",
            "request_state": "granted_redacted",
            "holder": "requesting user",
            "required_artifacts": [
                "decision receipt",
                "source inventory digest",
                "withheld-material boundary",
            ],
            "access_path": "redacted audit packet",
            "receipt_refs": [
                "receipt://contestability/audit-redacted-001",
            ],
            "appeal_path": "contest withheld boundary through review route",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
        {
            "right_id": "governance-right://care-memory-exit-001",
            "right_type": "exit",
            "request_state": "granted_scoped",
            "holder": "requesting user",
            "material_available": [
                "user-authored notes",
                "decision receipts",
                "portable preference summary",
            ],
            "material_withheld": [
                "third-party private context",
                "unreviewed safety notes",
            ],
            "safety_constraints": [
                "third-party privacy boundary",
                "no raw safety-sensitive memory export without review",
            ],
            "access_path": "scoped export bundle",
            "receipt_refs": [
                "receipt://contestability/exit-scoped-001",
            ],
            "appeal_path": "appeal withheld-material boundary",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
        {
            "right_id": "governance-right://care-memory-fork-001",
            "right_type": "fork",
            "request_state": "narrowed",
            "holder": "requesting user",
            "required_artifacts": [
                "lineage manifest",
                "privacy-boundary receipt",
                "safety-obligation receipt",
            ],
            "safety_constraints": [
                "no third-party private context in fork",
                "fork must preserve residual uncertainty and review receipt",
            ],
            "denial_or_redaction_reason": "raw fork denied until safety and privacy obligations are represented",
            "access_path": "sanitized fork candidate only",
            "receipt_refs": [
                "receipt://contestability/fork-narrowed-001",
            ],
            "appeal_path": "request review of fork boundary after new consent or safety evidence",
            "non_claims": REQUIRED_NON_CLAIMS,
        },
        {
            "right_id": "governance-right://care-memory-redaction-appeal-001",
            "right_type": "redaction_appeal",
            "request_state": "open",
            "holder": "requesting user",
            "denial_or_redaction_reason": "third-party private material withheld pending independent review",
            "material_withheld": [
                "third-party private context",
            ],
            "appeal_path": "review route can inspect withheld boundary without disclosing raw material",
            "receipt_refs": [
                "receipt://contestability/redaction-appeal-001",
            ],
            "non_claims": REQUIRED_NON_CLAIMS,
        },
    ],
    "replacement_preservation": {
        "candidate_replacement": "scf://memory-governance-v2",
        "route": "block_until_receipts_preserved",
        "preserves_conflict_residual": True,
        "preserves_governance_right_receipts": True,
        "preserves_revisit_condition": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    "support_state_effect": "none",
    "evidence_transition_created": False,
    "non_claims": REQUIRED_NON_CLAIMS,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Contestability worked example validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def scenario_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    label = str(record.get("scenario_id", "<unknown>"))
    conflict = record.get("value_conflict_record")
    rights = record.get("governance_right_records")
    replacement = record.get("replacement_preservation")

    if record.get("scenario_id") != SCENARIO_ID:
        errors.append(f"{label}: scenario_id must be {SCENARIO_ID}.")
    if record.get("scenario_kind") != "synthetic_contestability_worked_example":
        errors.append(f"{label}: scenario_kind must identify the synthetic worked example.")
    if not isinstance(conflict, dict):
        return errors + [f"{label}: value_conflict_record must be an object."]
    if not isinstance(rights, list) or not all(isinstance(item, dict) for item in rights):
        return errors + [f"{label}: governance_right_records must be a list of objects."]
    if not isinstance(replacement, dict):
        return errors + [f"{label}: replacement_preservation must be an object."]

    if len(conflict.get("value_axes", [])) < 3:
        errors.append(f"{label}: conflict must preserve at least three value axes.")
    if len(conflict.get("stakeholders", [])) < 2:
        errors.append(f"{label}: conflict must preserve affected stakeholders.")
    for field in (
        "authority_or_consent_boundary",
        "review_route",
        "authority_effect",
        "expiry_or_revisit_condition",
    ):
        if not nonempty_string(conflict.get(field)):
            errors.append(f"{label}: conflict.{field} must be a non-empty string.")
    for field in (
        "evidence_required",
        "dissent_payload",
        "residual_uncertainty",
        "non_claims",
    ):
        if not nonempty_list(conflict.get(field)):
            errors.append(f"{label}: conflict.{field} must be a non-empty list.")
    if conflict.get("decision_state") != "bounded_decision":
        errors.append(f"{label}: worked example must use a bounded_decision state.")
    if "narrow" not in str(conflict.get("authority_effect", "")).lower():
        errors.append(f"{label}: conflict authority_effect must narrow authority.")

    rights_by_type = {str(item.get("right_type", "")): item for item in rights}
    for right_type in ("audit", "exit", "fork", "redaction_appeal"):
        if right_type not in rights_by_type:
            errors.append(f"{label}: missing governance right record {right_type}.")
    audit = rights_by_type.get("audit", {})
    if not nonempty_list(audit.get("required_artifacts")) or not nonempty_list(audit.get("receipt_refs")):
        errors.append(f"{label}: audit right requires artifacts and receipt refs.")
    exit_right = rights_by_type.get("exit", {})
    if not nonempty_list(exit_right.get("material_available")):
        errors.append(f"{label}: exit right must name portable material.")
    if not nonempty_list(exit_right.get("material_withheld")):
        errors.append(f"{label}: exit right must name withheld material.")
    if not nonempty_string(exit_right.get("appeal_path")):
        errors.append(f"{label}: exit right must preserve an appeal path.")
    fork = rights_by_type.get("fork", {})
    if str(fork.get("request_state", "")) not in {"denied", "narrowed"}:
        errors.append(f"{label}: fork right must be denied or narrowed in this scenario.")
    if not nonempty_list(fork.get("safety_constraints")):
        errors.append(f"{label}: fork right must preserve safety constraints.")
    redaction = rights_by_type.get("redaction_appeal", {})
    if not nonempty_string(redaction.get("denial_or_redaction_reason")):
        errors.append(f"{label}: redaction appeal must preserve a redaction reason.")
    if not nonempty_string(redaction.get("appeal_path")):
        errors.append(f"{label}: redaction appeal must preserve an appeal path.")

    if replacement.get("route") != "block_until_receipts_preserved":
        errors.append(f"{label}: replacement route must block until receipts are preserved.")
    if replacement.get("preserves_conflict_residual") is not True:
        errors.append(f"{label}: replacement must preserve conflict residual.")
    if replacement.get("preserves_governance_right_receipts") is not True:
        errors.append(f"{label}: replacement must preserve governance-right receipts.")
    if replacement.get("preserves_revisit_condition") is not True:
        errors.append(f"{label}: replacement must preserve revisit condition.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{label}: support_state_effect must remain none.")
    if record.get("evidence_transition_created") is not False:
        errors.append(f"{label}: the worked example must not create an evidence transition.")

    all_text = text_blob(record)
    for non_claim in REQUIRED_NON_CLAIMS:
        if non_claim not in all_text:
            errors.append(f"{label}: missing non-claim boundary {non_claim!r}.")

    return errors


def mutation_controls() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    def missing_residual(record: dict[str, Any]) -> None:
        record["value_conflict_record"]["residual_uncertainty"] = []

    def exit_without_portable_material(record: dict[str, Any]) -> None:
        for right in record["governance_right_records"]:
            if right.get("right_type") == "exit":
                right["material_available"] = []

    def unsafe_fork(record: dict[str, Any]) -> None:
        for right in record["governance_right_records"]:
            if right.get("right_type") == "fork":
                right["safety_constraints"] = []

    def redaction_without_appeal(record: dict[str, Any]) -> None:
        for right in record["governance_right_records"]:
            if right.get("right_type") == "redaction_appeal":
                right["appeal_path"] = ""

    def replacement_drops_residual(record: dict[str, Any]) -> None:
        record["replacement_preservation"]["preserves_conflict_residual"] = False

    def support_promotion_overclaim(record: dict[str, Any]) -> None:
        record["support_state_effect"] = "promotes_chapter_core_claim"

    def missing_nonclaims(record: dict[str, Any]) -> None:
        record["non_claims"] = []
        record["value_conflict_record"]["non_claims"] = []

    return [
        ("missing_residual_rejected", missing_residual),
        ("exit_without_portable_material_rejected", exit_without_portable_material),
        ("unsafe_fork_rejected", unsafe_fork),
        ("redaction_without_appeal_rejected", redaction_without_appeal),
        ("replacement_drops_residual_rejected", replacement_drops_residual),
        ("support_promotion_overclaim_rejected", support_promotion_overclaim),
        ("missing_nonclaims_rejected", missing_nonclaims),
    ]


def required_surface_errors() -> list[str]:
    errors: list[str] = []
    required = {
        DOC: ["# Contestability Worked Example", COMMAND, SCENARIO_ID, *REQUIRED_NON_CLAIMS],
        CHAPTER: [CODEX_TEST_NAME, SCENARIO_ID, "care-memory export", "redaction appeal"],
        READER: [SCENARIO_ID, "care-memory export", "redacted audit packet"],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG],
        ROADMAP: [CODEX_TEST_NAME, "care-memory export"],
        CHANGELOG: ["Add contestability worked example fixture", PROOF_TAG],
        MANIFEST: [CODEX_TEST_NAME, PROOF_TAG],
        VALIDATION_REGISTRY: ["validate_contestability_worked_example.py"],
        LEAN_FILE: ["ContestabilityWorkedExampleSummary", "contestability_worked_example_bridge"],
    }
    for path, fragments in required.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{rel(path)} is missing required fragment: {fragment}")
    return errors


def build_result() -> dict[str, Any]:
    scenario = deepcopy(VALID_SCENARIO)
    errors = scenario_errors(scenario)
    if errors:
        fail(errors)

    negative_controls: dict[str, bool] = {}
    control_errors: list[str] = []
    for name, mutate in mutation_controls():
        mutated = deepcopy(VALID_SCENARIO)
        mutate(mutated)
        rejected = bool(scenario_errors(mutated))
        negative_controls[name] = rejected
        if not rejected:
            control_errors.append(f"mutation control {name} was not rejected.")
    if control_errors:
        fail(control_errors)

    rights = scenario["governance_right_records"]
    return {
        "result_id": "2026-07-02-contestability-worked-example",
        "schema_version": "asi_stack.contestability_worked_example.v0",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "scenario_id": scenario["scenario_id"],
        "scenario_kind": scenario["scenario_kind"],
        "valid_scenario_count": 1,
        "expected_invalid_mutation_control_count": len(negative_controls),
        "negative_controls": negative_controls,
        "right_types_checked": sorted(str(right.get("right_type", "")) for right in rights),
        "value_axes_checked": scenario["value_conflict_record"]["value_axes"],
        "support_state_effect": "none",
        "evidence_transition_created": False,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ValueConflict",
            "proof_tag": PROOF_TAG,
            "theorem_refs": ["contestability_worked_example_bridge"],
            "expected": {
                "conflict_residual_present": True,
                "audit_receipt_present": True,
                "exit_path_scoped": True,
                "fork_safety_bounded": True,
                "redaction_appeal_present": True,
                "replacement_preserves_receipts": True,
                "negative_controls_rejected": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "non_claims": REQUIRED_NON_CLAIMS,
        "residuals": [
            "Synthetic worked example only; no deployed contestability system is exercised.",
            "The fixture checks record discipline, not moral truth, legal validity, export usability, or fork safety.",
        ],
        "verification_result": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    result = build_result()
    errors = required_surface_errors()
    if errors:
        fail(errors)
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Contestability worked example result wrote: {rel(RESULT)}")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run {COMMAND} --write-result"])
        stored = json.loads(RESULT.read_text(encoding="utf-8"))
        if stored != result:
            fail([f"{rel(RESULT)} is stale; rerun {COMMAND} --write-result"])
        print("Contestability worked example validation passed.")


if __name__ == "__main__":
    main()
