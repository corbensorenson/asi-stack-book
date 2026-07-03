#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "resource_governance_tax_tradeoff" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "resource_governance_tax_tradeoff.md"
CHAPTER = ROOT / "chapters" / "resource-economics-and-token-budgets.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "resource-economics-and-token-budgets.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"

COMMAND = "python3 scripts/validate_resource_governance_tax_tradeoff.py"
CODEX_TEST_NAME = "Resource governance-tax trade-off model"
PROOF_TAG = "lean:resource.governance_tax.tradeoff_bridge"
LEAN_THEOREMS = [
    "resource_governance_tax_tradeoff_fixture_valid",
    "resource_governance_tax_tradeoff_shows_governance_can_pay",
    "resource_governance_tax_tradeoff_allows_low_risk_shortcut",
    "resource_governance_tax_tradeoff_preserves_no_promotion_boundary",
]

REQUIRED_NON_CLAIMS = [
    "does not prove deployed scheduler behavior",
    "does not measure real verification tax",
    "does not prove economic optimality",
    "does not promote the Resource Economics chapter core claim",
    "does not create a support-state transition",
]

SCENARIOS: list[dict[str, Any]] = [
    {
        "scenario_id": "valid_low_risk_shortcut_allowed",
        "expect_valid": True,
        "risk_class": "low",
        "required_protected_gate": False,
        "selected_route": "ungoverned_shortcut",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 34,
                "verification_cost": 12,
                "protected_review_cost": 10,
                "reviewer_burden_cost": 4,
                "expected_error_cost": 3,
                "fallback_cost": 1,
                "residual_discharge_cost": 0,
            },
            "ungoverned_shortcut": {
                "visible_cost": 10,
                "verification_cost": 2,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 0,
                "expected_error_cost": 6,
                "fallback_cost": 2,
                "residual_discharge_cost": 1,
            },
        },
    },
    {
        "scenario_id": "valid_high_risk_governance_pays",
        "expect_valid": True,
        "risk_class": "high",
        "required_protected_gate": True,
        "selected_route": "governed",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 38,
                "verification_cost": 16,
                "protected_review_cost": 12,
                "reviewer_burden_cost": 8,
                "expected_error_cost": 5,
                "fallback_cost": 3,
                "residual_discharge_cost": 2,
            },
            "ungoverned_shortcut": {
                "visible_cost": 14,
                "verification_cost": 0,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 2,
                "expected_error_cost": 70,
                "fallback_cost": 25,
                "residual_discharge_cost": 30,
            },
        },
    },
    {
        "scenario_id": "valid_hidden_residual_flips_selection",
        "expect_valid": True,
        "risk_class": "medium",
        "required_protected_gate": False,
        "selected_route": "governed",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 28,
                "verification_cost": 12,
                "protected_review_cost": 6,
                "reviewer_burden_cost": 5,
                "expected_error_cost": 8,
                "fallback_cost": 4,
                "residual_discharge_cost": 3,
            },
            "ungoverned_shortcut": {
                "visible_cost": 9,
                "verification_cost": 0,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 4,
                "expected_error_cost": 35,
                "fallback_cost": 20,
                "residual_discharge_cost": 25,
            },
        },
    },
    {
        "scenario_id": "invalid_tax_erasure_selected_shortcut",
        "expect_valid": False,
        "risk_class": "high",
        "required_protected_gate": False,
        "selected_route": "ungoverned_shortcut",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 30,
                "verification_cost": 10,
                "protected_review_cost": 8,
                "reviewer_burden_cost": 6,
                "expected_error_cost": 5,
                "fallback_cost": 3,
                "residual_discharge_cost": 2,
            },
            "ungoverned_shortcut": {
                "visible_cost": 12,
                "verification_cost": 0,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 3,
                "expected_error_cost": 55,
                "fallback_cost": 18,
                "residual_discharge_cost": 20,
            },
        },
    },
    {
        "scenario_id": "invalid_protected_gate_deleted",
        "expect_valid": False,
        "risk_class": "critical",
        "required_protected_gate": True,
        "selected_route": "governed",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 20,
                "verification_cost": 8,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 4,
                "expected_error_cost": 10,
                "fallback_cost": 4,
                "residual_discharge_cost": 2,
            },
            "ungoverned_shortcut": {
                "visible_cost": 11,
                "verification_cost": 0,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 2,
                "expected_error_cost": 120,
                "fallback_cost": 40,
                "residual_discharge_cost": 35,
            },
        },
    },
    {
        "scenario_id": "invalid_residual_unpriced",
        "expect_valid": False,
        "risk_class": "medium",
        "required_protected_gate": False,
        "selected_route": "ungoverned_shortcut",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 28,
                "verification_cost": 10,
                "protected_review_cost": 5,
                "reviewer_burden_cost": 5,
                "expected_error_cost": 8,
                "fallback_cost": 4,
                "residual_discharge_cost": 2,
            },
            "ungoverned_shortcut": {
                "visible_cost": 8,
                "verification_cost": 0,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 3,
                "expected_error_cost": 28,
                "fallback_cost": 12,
            },
        },
    },
    {
        "scenario_id": "invalid_support_state_promotion",
        "expect_valid": False,
        "risk_class": "low",
        "required_protected_gate": False,
        "selected_route": "ungoverned_shortcut",
        "support_state_effect": "promote",
        "chapter_core_support_effect": "promote",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 34,
                "verification_cost": 12,
                "protected_review_cost": 10,
                "reviewer_burden_cost": 4,
                "expected_error_cost": 3,
                "fallback_cost": 1,
                "residual_discharge_cost": 0,
            },
            "ungoverned_shortcut": {
                "visible_cost": 10,
                "verification_cost": 2,
                "protected_review_cost": 0,
                "reviewer_burden_cost": 0,
                "expected_error_cost": 6,
                "fallback_cost": 2,
                "residual_discharge_cost": 1,
            },
        },
    },
    {
        "scenario_id": "invalid_missing_comparator",
        "expect_valid": False,
        "risk_class": "high",
        "required_protected_gate": True,
        "selected_route": "governed",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claim_boundary": True,
        "routes": {
            "governed": {
                "visible_cost": 38,
                "verification_cost": 16,
                "protected_review_cost": 12,
                "reviewer_burden_cost": 8,
                "expected_error_cost": 5,
                "fallback_cost": 3,
                "residual_discharge_cost": 2,
            }
        },
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Resource governance-tax trade-off validation failed:")
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


def full_cost(route: dict[str, Any], reasons: list[str], route_name: str) -> int:
    fields = [
        "visible_cost",
        "verification_cost",
        "protected_review_cost",
        "reviewer_burden_cost",
        "expected_error_cost",
        "fallback_cost",
        "residual_discharge_cost",
    ]
    total = 0
    for field in fields:
        value = route.get(field)
        if not isinstance(value, int) or value < 0:
            reasons.append(f"{route_name}_{field}_missing_or_invalid")
            continue
        total += value
    return total


def scenario_rejection_reasons(scenario: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    reasons: list[str] = []
    routes = scenario.get("routes")
    if not isinstance(routes, dict):
        routes = {}
        reasons.append("routes_missing")
    governed = routes.get("governed")
    ungoverned = routes.get("ungoverned_shortcut")
    if not isinstance(governed, dict):
        governed = {}
        reasons.append("governed_comparator_missing")
    if not isinstance(ungoverned, dict):
        ungoverned = {}
        reasons.append("ungoverned_comparator_missing")

    governed_full = full_cost(governed, reasons, "governed")
    ungoverned_full = full_cost(ungoverned, reasons, "ungoverned")
    governed_visible = governed.get("visible_cost") if isinstance(governed.get("visible_cost"), int) else None
    ungoverned_visible = (
        ungoverned.get("visible_cost") if isinstance(ungoverned.get("visible_cost"), int) else None
    )
    selected = scenario.get("selected_route")
    required_gate = scenario.get("required_protected_gate") is True

    if selected not in {"governed", "ungoverned_shortcut"}:
        reasons.append("selected_route_unknown")
    if required_gate and selected != "governed":
        reasons.append("required_protected_gate_cannot_select_shortcut")
    if required_gate and governed.get("protected_review_cost") != 0 and not isinstance(
        governed.get("protected_review_cost"), int
    ):
        reasons.append("governed_protected_review_cost_missing")
    if required_gate and governed.get("protected_review_cost") == 0:
        reasons.append("required_protected_gate_deleted")

    comparator_complete = isinstance(routes.get("governed"), dict) and isinstance(
        routes.get("ungoverned_shortcut"), dict
    )
    if comparator_complete and selected == "governed" and ungoverned_full < governed_full and not required_gate:
        reasons.append("selected_governed_while_shortcut_full_cost_lower")
    if comparator_complete and selected == "ungoverned_shortcut" and governed_full <= ungoverned_full:
        reasons.append("selected_shortcut_while_governed_full_cost_lower")
    if scenario.get("support_state_effect") != "none":
        reasons.append("support_state_promotion_attempt")
    if scenario.get("chapter_core_support_effect") != "none":
        reasons.append("chapter_core_promotion_attempt")
    if scenario.get("non_claim_boundary") is not True:
        reasons.append("missing_non_claim_boundary")

    analysis = {
        "governed_full_cost": governed_full,
        "ungoverned_full_cost": ungoverned_full,
        "governed_visible_cost": governed_visible,
        "ungoverned_visible_cost": ungoverned_visible,
        "governance_pays": comparator_complete and governed_full <= ungoverned_full,
        "shortcut_visible_cost_lower": isinstance(governed_visible, int)
        and isinstance(ungoverned_visible, int)
        and ungoverned_visible < governed_visible,
        "selected_route": selected,
        "rejection_reasons": sorted(set(reasons)),
    }
    return sorted(set(reasons)), analysis


def build_result(errors: list[str]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    valid_scenarios: list[str] = []
    rejected_controls: list[dict[str, Any]] = []

    for scenario in SCENARIOS:
        reasons, analysis = scenario_rejection_reasons(scenario)
        actual_valid = not reasons
        expected_valid = scenario.get("expect_valid") is True
        scenario_id = str(scenario.get("scenario_id", ""))
        if expected_valid and not actual_valid:
            errors.append(f"{scenario_id}: expected valid but rejected: {', '.join(reasons)}.")
        if not expected_valid and actual_valid:
            errors.append(f"{scenario_id}: expected invalid but no rejection reason was produced.")
        if expected_valid:
            valid_scenarios.append(scenario_id)
        else:
            rejected_controls.append({"scenario_id": scenario_id, "rejection_reasons": reasons})
        rows.append(
            {
                "scenario_id": scenario_id,
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "risk_class": scenario.get("risk_class"),
                "required_protected_gate": scenario.get("required_protected_gate"),
                **analysis,
            }
        )

    by_id = {row["scenario_id"]: row for row in rows}
    assertions = {
        "governed_selected_when_full_ungoverned_cost_exceeds_governed_cost": by_id[
            "valid_high_risk_governance_pays"
        ]["selected_route"]
        == "governed"
        and by_id["valid_high_risk_governance_pays"]["governance_pays"],
        "low_risk_shortcut_allowed_when_full_cost_lower_and_no_required_gate": by_id[
            "valid_low_risk_shortcut_allowed"
        ]["selected_route"]
        == "ungoverned_shortcut"
        and not by_id["valid_low_risk_shortcut_allowed"]["governance_pays"],
        "hidden_residual_flips_selection": by_id["valid_hidden_residual_flips_selection"][
            "shortcut_visible_cost_lower"
        ]
        and by_id["valid_hidden_residual_flips_selection"]["governance_pays"],
        "protected_gate_deletion_rejected": any(
            row["scenario_id"] == "invalid_protected_gate_deleted"
            and "required_protected_gate_deleted" in row["rejection_reasons"]
            for row in rows
        ),
        "residual_pricing_required": any(
            row["scenario_id"] == "invalid_residual_unpriced"
            and "ungoverned_residual_discharge_cost_missing_or_invalid" in row["rejection_reasons"]
            for row in rows
        ),
        "reviewer_burden_priced": all(
            isinstance(route.get("reviewer_burden_cost"), int)
            for scenario in SCENARIOS
            for route in scenario.get("routes", {}).values()
        ),
        "support_state_effect_none": all(
            row["expected_valid"] is False or SCENARIOS[index]["support_state_effect"] == "none"
            for index, row in enumerate(rows)
        ),
        "chapter_core_support_effect_none": all(
            row["expected_valid"] is False or SCENARIOS[index]["chapter_core_support_effect"] == "none"
            for index, row in enumerate(rows)
        ),
        "non_claim_boundary": all(
            row["expected_valid"] is False or SCENARIOS[index]["non_claim_boundary"] is True
            for index, row in enumerate(rows)
        ),
    }
    for key, value in assertions.items():
        if value is not True:
            errors.append(f"tradeoff_assertions.{key} must be true.")

    return {
        "schema_version": "asi_stack.resource_governance_tax_tradeoff.v0",
        "result_id": "2026-07-03-resource-governance-tax-tradeoff",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_governance_tax_tradeoff",
        "valid_scenario_count": len(valid_scenarios),
        "expected_invalid_control_count": len(rejected_controls),
        "valid_scenarios": sorted(valid_scenarios),
        "rejected_controls": rejected_controls,
        "scenario_results": rows,
        "tradeoff_assertions": assertions,
        "lean_fixture_alignment": {
            "proof_tag": PROOF_TAG,
            "valid_scenario_count": 3,
            "expected_invalid_control_count": 5,
            "governed_selected_count": 2,
            "ungoverned_allowed_count": 1,
            "theorem_refs": LEAN_THEOREMS,
        },
        "weakening_condition": (
            "The governance-tax argument weakens if hidden review, fallback, residual, "
            "or reviewer-burden costs do not change route choice, or if protected "
            "gates can be deleted without a recorded residual and rejection."
        ),
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_record(record: dict[str, Any], errors: list[str]) -> None:
    if record.get("schema_version") != "asi_stack.resource_governance_tax_tradeoff.v0":
        errors.append(f"{rel(RESULT)} schema_version mismatch.")
    if record.get("result_id") != "2026-07-03-resource-governance-tax-tradeoff":
        errors.append(f"{rel(RESULT)} result_id mismatch.")
    if record.get("recorded_date") != "2026-07-03":
        errors.append(f"{rel(RESULT)} recorded_date mismatch.")
    if record.get("command") != COMMAND:
        errors.append(f"{rel(RESULT)} command mismatch.")
    if record.get("valid_scenario_count") != 3:
        errors.append(f"{rel(RESULT)} valid_scenario_count must be 3.")
    if record.get("expected_invalid_control_count") != 5:
        errors.append(f"{rel(RESULT)} expected_invalid_control_count must be 5.")
    assertions = record.get("tradeoff_assertions")
    if not isinstance(assertions, dict) or not all(value is True for value in assertions.values()):
        errors.append(f"{rel(RESULT)} tradeoff_assertions must all be true.")
    alignment = record.get("lean_fixture_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)} lean_fixture_alignment must be an object.")
    else:
        if alignment.get("proof_tag") != PROOF_TAG:
            errors.append(f"{rel(RESULT)} lean proof tag mismatch.")
        if alignment.get("theorem_refs") != LEAN_THEOREMS:
            errors.append(f"{rel(RESULT)} theorem refs mismatch.")
    non_claim_text = text_blob(record.get("non_claims"))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def require_text(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"{rel(path)} missing.")
        return
    text = path.read_text(encoding="utf-8")
    normalized = " ".join(text.lower().split())
    for phrase in phrases:
        if " ".join(phrase.lower().split()) not in normalized:
            errors.append(f"{rel(path)} missing required phrase: {phrase}")


def validate_surfaces(errors: list[str]) -> None:
    require_text(
        LEAN_FILE,
        [
            "GovernanceTaxTradeoffSummary",
            "resourceGovernanceTaxTradeoffFixture",
            *LEAN_THEOREMS,
        ],
        errors,
    )
    require_text(
        DOC,
        [
            "Resource Governance-Tax Trade-Off Model",
            COMMAND,
            "valid_low_risk_shortcut_allowed",
            "valid_high_risk_governance_pays",
            "valid_hidden_residual_flips_selection",
            "invalid_protected_gate_deleted",
            "does not prove economic optimality",
        ],
        errors,
    )
    require_text(
        CHAPTER,
        [
            CODEX_TEST_NAME,
            COMMAND,
            PROOF_TAG,
            "governance tax pays for itself",
            "does not measure real verification tax",
        ],
        errors,
    )
    require_text(
        READER,
        [
            "governance tax pays for itself",
            "low-risk shortcut",
            "does not prove deployed scheduler behavior",
        ],
        errors,
    )
    require_text(
        OUTLINE,
        [
            CODEX_TEST_NAME,
            COMMAND,
            PROOF_TAG,
            "risk, route quality, hidden verification and fallback cost, reviewer burden, residual discharge, and low-risk shortcut allowance",
        ],
        errors,
    )
    require_text(
        ROADMAP,
        [
            "first bounded governance-tax trade-off model",
            "live or externally reviewable workload",
            "do not redo the bounded governance-tax model",
        ],
        errors,
    )
    require_text(
        CHANGELOG,
        [
            "Resource governance-tax trade-off model",
            COMMAND,
            PROOF_TAG,
        ],
        errors,
    )
    require_text(
        VALIDATE_BOOK,
        [
            "scripts/validate_resource_governance_tax_tradeoff.py",
            "docs/resource_governance_tax_tradeoff.md",
            "experiments/resource_governance_tax_tradeoff/results/2026-07-03-local.json",
            'run_validator("validate_resource_governance_tax_tradeoff.py")',
        ],
        errors,
    )

    manifest = load_json(MANIFEST)
    manifest_text = text_blob(manifest)
    for phrase in [CODEX_TEST_NAME.lower(), PROOF_TAG.lower(), COMMAND.lower()]:
        if phrase not in manifest_text:
            errors.append(f"{rel(MANIFEST)} missing {phrase}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    built = build_result(errors)
    if errors:
        fail(errors)
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} missing; run {COMMAND} --write-result.")
    else:
        recorded = load_json(RESULT)
        validate_record(recorded, errors)
        if recorded != built:
            errors.append(f"{rel(RESULT)} is stale; rerun {COMMAND} --write-result.")

    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Resource governance-tax trade-off validation passed.")


if __name__ == "__main__":
    main()
