#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "experiments" / "residual_ledger_trace" / "input" / "artifact_manifest.json"
RESULT = ROOT / "experiments" / "residual_ledger_trace" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "residual_ledger_trace.md"
RESOURCE_FLAGSHIP = ROOT / "experiments" / "resource_flagship_lane" / "results" / "2026-07-01-local.json"
RESOURCE_WORKFLOW = ROOT / "experiments" / "resource_workflow_trace" / "results" / "2026-07-01-local.json"
COMPACT_GVR = ROOT / "experiments" / "compact_gvr_slice" / "results" / "2026-07-01-local.json"
READINESS_RESULT = ROOT / "experiments" / "readiness_residual_gates" / "results" / "2026-06-28-local.md"
RESIDUAL_CONSERVATION = (
    ROOT / "experiments" / "residual_honesty_conservation" / "results" / "2026-07-03-local.json"
)
CHAPTER = ROOT / "chapters" / "compact-generative-systems-and-residual-honesty.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "compact-generative-systems-and-residual-honesty.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "CompactGenerativeSystems.lean"

COMMAND = "python3 scripts/validate_residual_ledger_trace.py"
CODEX_TEST_NAME = "Residual ledger trace"
LEAN_THEOREM = "residual_ledger_trace_surface_bridge"
EXPECTED_SOURCE_REFS = {
    "experiments/resource_flagship_lane/results/2026-07-01-local.json",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/compact_gvr_slice/results/2026-07-01-local.json",
    "experiments/readiness_residual_gates/results/2026-06-28-local.md",
    "experiments/residual_honesty_conservation/results/2026-07-03-local.json",
}
EXPECTED_SUBLANE_DECISIONS = {
    "resource_ci_cost_profile_no_change",
    "resource_live_probe_no_change",
    "resource_load_stability_probe_no_change",
    "resource_workflow_trace_no_change",
    "resource_workload_quality_probe_no_change",
}
REQUIRED_NON_CLAIMS = [
    "does not prove deployed residual-ledger behavior",
    "does not prove safety",
    "does not promote any chapter core claim",
    "does not prove model quality or benchmark performance",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Residual ledger trace validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("schema_version") != "asi_stack.residual_ledger_trace.manifest.v0":
        errors.append(f"{rel(MANIFEST)} has unexpected schema_version.")
    refs = manifest.get("source_artifact_refs")
    if set(refs or []) != EXPECTED_SOURCE_REFS:
        errors.append(f"{rel(MANIFEST)} source_artifact_refs do not match expected artifact set.")
    boundary_blob = text_blob(manifest.get("required_boundaries", []))
    for phrase in (
        "no deployed residual-ledger behavior claim",
        "no safety proof claim",
        "no chapter-core support-state promotion",
        "no model-quality or benchmark claim",
    ):
        if phrase not in boundary_blob:
            errors.append(f"{rel(MANIFEST)} missing boundary {phrase!r}.")


def build_result(errors: list[str]) -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    validate_manifest(manifest, errors)

    resource_flagship = load_json(RESOURCE_FLAGSHIP)
    resource_workflow = load_json(RESOURCE_WORKFLOW)
    compact_gvr = load_json(COMPACT_GVR)
    residual_conservation = load_json(RESIDUAL_CONSERVATION)
    readiness_text = READINESS_RESULT.read_text(encoding="utf-8")

    if resource_flagship.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(RESOURCE_FLAGSHIP)} must preserve chapter_core_support_effect=none.")
    sublane_decisions = (
        resource_flagship.get("component_summary", {}).get("sublane_no_promotion_decisions", {})
    )
    if set(sublane_decisions) != EXPECTED_SUBLANE_DECISIONS:
        errors.append(f"{rel(RESOURCE_FLAGSHIP)} sublane decisions do not match expected set.")
    for name, decision in sorted(sublane_decisions.items()):
        if decision.get("transition_validity_state") != "review_accepted":
            errors.append(f"{name} is not review_accepted.")
        if decision.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{name} does not block promotion.")
        if decision.get("verification_result") != "pass":
            errors.append(f"{name} verification_result is not pass.")

    load_probe = resource_flagship.get("component_summary", {}).get("load_stability_probe", {})
    if load_probe.get("selected_residualized_deferred_task_ticks") != 7:
        errors.append(f"{rel(RESOURCE_FLAGSHIP)} missing seven selected residualized deferrals.")
    if load_probe.get("negative_hidden_deferred_task_ticks") != 7:
        errors.append(f"{rel(RESOURCE_FLAGSHIP)} missing hidden-deferral negative-control burden.")

    workflow_alignment = (
        resource_workflow.get("lean_fixture_alignment", {}).get("field_alignment", {})
    )
    if workflow_alignment.get("displaced_costs_residualized") is not True:
        errors.append(f"{rel(RESOURCE_WORKFLOW)} does not preserve displaced-cost residualization.")
    if "invalid_displaced_cost_erased.json" not in resource_workflow.get(
        "expected_invalid_controls", []
    ):
        errors.append(f"{rel(RESOURCE_WORKFLOW)} does not name the erased-displaced-cost control.")

    compact_residual_blob = text_blob(compact_gvr.get("residuals", []))
    if "explicit repair residual and fallback path" not in compact_residual_blob:
        errors.append(f"{rel(COMPACT_GVR)} missing explicit repair residual/fallback surface.")
    if compact_gvr.get("selected_receipt") != "receipt://repeat-generator-plus-repair":
        errors.append(f"{rel(COMPACT_GVR)} selected receipt changed unexpectedly.")
    if set(compact_gvr.get("negative_control_receipts", [])) != {
        "receipt://bounded-search-overrun",
        "receipt://lossy-summary-marked-exact",
        "receipt://negative-rate-no-fallback",
    }:
        errors.append(f"{rel(COMPACT_GVR)} negative controls changed unexpectedly.")

    readiness_required = [
        "canary-with-residual-escrow",
        "lost-residual-escrow",
        "No live-book support state changed.",
        "does not prove routing accuracy",
        "does not promote any Appendix C claim",
    ]
    for fragment in readiness_required:
        require_fragment(rel(READINESS_RESULT), readiness_text, fragment, errors)

    if residual_conservation.get("valid_case_count") != 3:
        errors.append(f"{rel(RESIDUAL_CONSERVATION)} valid_case_count must remain 3.")
    if residual_conservation.get("expected_invalid_control_count") != 5:
        errors.append(f"{rel(RESIDUAL_CONSERVATION)} expected_invalid_control_count must remain 5.")

    trace_entries = [
        {
            "entry_id": "resource-flagship-residualized-deferrals",
            "artifact_ref": rel(RESOURCE_FLAGSHIP),
            "residual_surface": "selected route residualizes seven deferred task-ticks and rejects a hidden-deferral review-erasure control",
            "visible_burden": {"selected_residualized_deferred_task_ticks": 7},
            "negative_control": {
                "name": "route://negative-latency-only-review-erasure",
                "hidden_deferred_task_ticks": 7,
            },
            "decision_refs": sorted(sublane_decisions),
            "support_state_effect": "none",
        },
        {
            "entry_id": "resource-workflow-displaced-costs",
            "artifact_ref": rel(RESOURCE_WORKFLOW),
            "residual_surface": "workflow trace preserves displaced-cost residualization and rejects erased displaced costs",
            "visible_burden": {"displaced_costs_residualized": True},
            "negative_control": {"name": "invalid_displaced_cost_erased.json"},
            "support_state_effect": "none",
        },
        {
            "entry_id": "compact-gvr-repair-residual",
            "artifact_ref": rel(COMPACT_GVR),
            "residual_surface": "selected compact receipt keeps explicit repair residual and fallback path visible",
            "visible_burden": {"selected_receipt": compact_gvr.get("selected_receipt")},
            "negative_control": {
                "names": sorted(compact_gvr.get("negative_control_receipts", []))
            },
            "support_state_effect": compact_gvr.get("support_state_effect"),
        },
        {
            "entry_id": "readiness-residual-escrow",
            "artifact_ref": rel(READINESS_RESULT),
            "residual_surface": "readiness harness admits residual escrow/quarantine cases and rejects lost residual escrow",
            "visible_burden": {"canary_with_residual_escrow": True},
            "negative_control": {"name": "invalid_residual_lost_on_promotion.json"},
            "support_state_effect": "none",
        },
    ]

    summary = {
        "resourceFlagshipArtifactRead": True,
        "resourceSublaneDecisionsRecorded": set(sublane_decisions) == EXPECTED_SUBLANE_DECISIONS,
        "resourceResidualizedDeferralsVisible": load_probe.get(
            "selected_residualized_deferred_task_ticks"
        )
        == 7,
        "resourceDisplacedCostsResidualized": workflow_alignment.get(
            "displaced_costs_residualized"
        )
        is True,
        "compactGvrResidualsVisible": "explicit repair residual and fallback path"
        in compact_residual_blob,
        "compactGvrControlsVisible": len(compact_gvr.get("negative_control_receipts", [])) == 3,
        "readinessResidualEscrowVisible": "canary-with-residual-escrow" in readiness_text,
        "readinessLostResidualControlRejected": "lost-residual-escrow" in readiness_text,
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
        "deployedLedgerNotClaimed": True,
    }

    result = {
        "schema_version": "asi_stack.residual_ledger_trace.result.v0",
        "result_id": "2026-07-03-residual-ledger-trace",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "manifest_ref": rel(MANIFEST),
        "result_kind": "cross_artifact_residual_ledger_trace",
        "source_artifact_hashes": {
            rel(path): sha256_file(path)
            for path in [
                RESOURCE_FLAGSHIP,
                RESOURCE_WORKFLOW,
                COMPACT_GVR,
                READINESS_RESULT,
                RESIDUAL_CONSERVATION,
            ]
        },
        "trace_entry_count": len(trace_entries),
        "trace_entries": trace_entries,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.CompactGenerativeSystems",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "This trace reads already committed Resource, Compact GVR, and Readiness artifacts instead of inventing a fresh synthetic residual record set.",
            "The trace verifies that residualized deferrals, displaced costs, repair residuals, readiness escrow, rejected hidden burdens, and no-promotion decisions stay visible across artifact boundaries.",
            "The trace is still local repository evidence and does not establish deployed residual-ledger storage or runtime residual detection.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }
    return result


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    actual = RESULT.read_text(encoding="utf-8")
    if actual != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Residual Ledger Trace",
                COMMAND,
                rel(RESULT),
                "Resource flagship",
                "Compact GVR",
                "Readiness/residual gate",
                "not a new synthetic record fixture",
                "does not prove deployed residual-ledger behavior",
            ],
        ),
        rel(CHAPTER): (
            CHAPTER,
            [
                "Residual ledger trace",
                COMMAND,
                rel(RESULT),
                "real repository trace",
                "Resource flagship",
                "Compact GVR",
                "Readiness/residual gate",
            ],
        ),
        rel(READER): (
            READER,
            [
                "residual-ledger trace",
                "not proof that a deployed ledger exists",
                "seven deferred task-ticks",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented residual-ledger trace",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "real residual-ledger trace",
                rel(RESULT),
                "Resource flagship, Compact GVR, and Readiness artifacts",
                "does not prove deployed residual-ledger behavior",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add residual ledger trace",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "residual_storage_replay_backed_not_deployed",
                rel(RESULT),
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_residual_ledger_trace.py",
                "docs/residual_ledger_trace.md",
                rel(RESULT),
                '"script": "validate_residual_ledger_trace.py"',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "ResidualLedgerTraceSummary",
                "residualLedgerTraceSummary",
                LEAN_THEOREM,
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
    tests: list[dict[str, Any]] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            maybe_tests = value.get("codex_tests")
            if isinstance(maybe_tests, list):
                tests.extend(test for test in maybe_tests if isinstance(test, dict))
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(data)
    matches = [
        test for test in tests if isinstance(test, dict) and test.get("name") == CODEX_TEST_NAME
    ]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        "implemented",
        COMMAND,
        "no deployed residual-ledger behavior",
        "no support-state promotion",
    ):
        if phrase not in blob:
            errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")


def validate_ledger_json(errors: list[str]) -> None:
    data = load_json(LEDGER_JSON)
    entries = data.get("records", [])
    matches = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("idea_id") == "residual_honesty"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} missing residual honesty contribution row.")
        return
    entry = matches[0]
    blob = text_blob(entry)
    for phrase in (
        "residual_storage_replay_backed_not_deployed",
        rel(RESULT),
        "does not prove deployed residual-ledger behavior",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} residual row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "resourceFlagshipArtifactRead",
        "resourceSublaneDecisionsRecorded",
        "resourceResidualizedDeferralsVisible",
        "resourceDisplacedCostsResidualized",
        "compactGvrResidualsVisible",
        "compactGvrControlsVisible",
        "readinessResidualEscrowVisible",
        "readinessLostResidualControlRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
        "deployedLedgerNotClaimed",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing residual ledger field {field}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    for path in [MANIFEST, RESOURCE_FLAGSHIP, RESOURCE_WORKFLOW, COMPACT_GVR, READINESS_RESULT, RESIDUAL_CONSERVATION]:
        if not path.exists():
            errors.append(f"Missing required artifact {rel(path)}.")
    if errors:
        fail(errors)

    expected = build_result(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_book_structure(errors)
        validate_ledger_json(errors)
        validate_lean_shape(errors)

    if errors:
        fail(errors)
    print(
        "Residual ledger trace validation passed: "
        f"{expected['trace_entry_count']} artifact trace entries, "
        "Resource/Compact GVR/Readiness residual surfaces visible, no support-state effect."
    )


if __name__ == "__main__":
    main()
