#!/usr/bin/env python3
"""Record the C6 Efficiency-to-route-economy semantic consolidation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from build_proof_rationalization_registry import normalize
from build_proof_semantic_depth_overlay import statement_key


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "proofs/proof_semantic_rationalization_ledger.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "lean/AsiStackProofs/Efficiency.lean"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)

NAMES = [
    "no_efficiency_claim_request_stays_idle",
    "missing_task_contract_requests_contract",
    "missing_quality_predicate_requests_predicate",
    "missing_selected_route_requests_route_record",
    "missing_candidate_set_requests_candidate_set",
    "missing_lower_cost_comparisons_requests_comparisons",
    "missing_cost_classes_requests_cost_ledger",
    "incomplete_visible_costs_request_complete_costs",
    "missing_verification_result_requests_verification",
    "failed_quality_blocks_efficiency_claim",
    "authority_bypass_blocks_efficiency_claim",
    "missing_residuals_request_residual_record",
    "missing_fallback_route_requests_fallback",
    "missing_hidden_cost_audit_requests_audit",
    "missing_benchmark_or_trace_requests_trace",
    "missing_negative_controls_requests_controls",
    "promotion_request_without_efficiency_evidence_transition_requests_transition",
    "efficiency_claim_without_nonclaim_boundary_preserves_boundary",
    "complete_efficiency_claim_admission_allows_claim_record",
    "efficiency_route_search_probe_fixture_valid",
    "efficiency_route_search_probe_rejects_invalid_savings",
    "efficiency_route_search_probe_preserves_no_promotion_boundary",
]

TARGETS = {
    "no_efficiency_claim_request_stays_idle": {
        "target_ref": "proof-target:lean:efficiency.claim_admission_lifecycle_route",
        "old_target_text": (
            "Modeled efficiency-claim admission routes missing task contracts, quality "
            "predicates, selected routes, candidate sets, lower-cost comparisons, cost "
            "ledgers, complete visible costs, verification results, failed quality, "
            "authority bypass, residual gaps, fallback gaps, hidden-cost audit gaps, "
            "benchmark or trace gaps, negative-control gaps, evidence-transition gaps, "
            "and non-claim-boundary gaps to explicit outcomes."
        ),
        "new_target_text": (
            "A reachable nine-stage route-economy lifecycle requires scoped request "
            "identities, complete resource and hidden-cost accounting, protected "
            "capacity, fallback, actual spend, useful-outcome and resource-bill "
            "separation, verification, residual and recovery records, reconciliation, "
            "evidence transition, and closure without support or external-effect authority."
        ),
    },
    "efficiency_route_search_probe_fixture_valid": {
        "target_ref": "proof-target:lean:efficiency.route_search.probe_fixture_bridge",
        "old_target_text": (
            "The synthetic efficiency route-search probe summary records two valid "
            "traces, six expected-invalid controls, fourteen checked candidate routes, "
            "minimum verified route selection, rejection of cheap failed quality, hidden "
            "residual, authority bypass, and compression-utility overclaim controls, "
            "hidden-cost class audit coverage, and no route-search-completeness, "
            "measured-efficiency, or support-state-promotion claim."
        ),
        "new_target_text": (
            "The independent synthetic route-search consumer computes two valid and six "
            "expected-invalid outcomes over fourteen candidates, while the reachable "
            "lifecycle supplies the formal cost, verification, residual, fallback, "
            "reconciliation, and no-authority boundary; neither asset is treated as "
            "measured efficiency or complete search."
        ),
    },
}


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def blocks(text: str) -> dict[str, dict[str, str]]:
    declarations = list(DECL_START.finditer(text))
    result: dict[str, dict[str, str]] = {}
    for match in THEOREM_START.finditer(text):
        end = next(
            (candidate.start() for candidate in declarations if candidate.start() > match.start()),
            len(text),
        )
        block = text[match.start():end]
        signature = normalize(block.split(":= by", 1)[0])
        result[match.group(1)] = {
            "block_sha256": sha256(block.encode("utf-8")),
            "statement_sha256": sha256(statement_key(signature).encode("utf-8")),
        }
    return result


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def slug(name: str) -> str:
    return name.replace("_", "-")


def main() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger["actions"] = [
        row for row in ledger["actions"] if row["sequence"] < 69
    ]
    baseline_commit = ledger["classification_baseline"]["commit"]
    module_bytes = git_show(baseline_commit, MODULE)
    baseline_blocks = blocks(module_bytes.decode("utf-8"))
    overlay = json.loads(
        git_show(
            baseline_commit,
            ledger["classification_baseline"]["overlay_path"],
        )
    )
    overlay_rows = {row["theorem_id"]: row for row in overlay["records"]}
    module_sha = sha256(module_bytes)
    consumer_paths = [
        "book_structure.json",
        "docs/book_outline.md",
        "chapters/the-efficient-asi-hypothesis.qmd",
        "proofs/proof_manifest.json",
        "proofs/proof_triage.json",
    ]

    for offset, name in enumerate(NAMES, start=69):
        theorem_id = f"{MODULE}::{name}"
        source = baseline_blocks[name]
        baseline_row = overlay_rows[theorem_id]
        is_probe = name.startswith("efficiency_route_search_probe_")
        migration = TARGETS.get(name)
        semantic_basis = [
            (
                "The retired theorem normalizes one edited Boolean field in a single "
                "hand-authored complete review."
                if not is_probe
                else "The retired theorem proves a conjunction or projection over one hand-authored summary literal."
            ),
            "The immutable semantic overlay records no Lean dependency or theorem consumer for the declaration.",
            (
                "The reachable ResourceEconomicsRefinement model carries identity-bound "
                "request, allocation, execution, verification, transfer, reconciliation, "
                "closure, support, and external-effect semantics."
            ),
            (
                "The independent efficiency route-search consumer derives accepted and "
                "rejected outcomes from candidate eligibility, complete cost arithmetic, "
                "residuals, authority, and negative controls instead of trusting copied fields."
            ),
            (
                "Retirement preserves the bounded policy and result as prose, executable "
                "evidence, and a stronger lifecycle without presenting checklist "
                "normalization as semantic proof."
            ),
            (
                "No route-search completeness, cost-estimate accuracy, measured "
                "efficiency, model quality, compression utility, deployment, transfer, "
                "or support-state promotion follows."
            ),
        ]
        ledger["actions"].append(
            {
                "action_id": f"C6-R{offset}-efficiency-{slug(name)}",
                "sequence": offset,
                "state": "executed",
                "action": "retire_legacy_fixture_theorem_after_reachable_refinement_rebinding",
                "semantic_relation": (
                    "legacy_fixture_statement_replaced_by_reachable_refinement_and_independent_consumer"
                ),
                "module_path": MODULE,
                "baseline_module_sha256": module_sha,
                "retired_theorem_id": theorem_id,
                "replacement_theorem_id": None,
                "retired_block_sha256": source["block_sha256"],
                "replacement_block_sha256": None,
                "retired_statement_sha256": source["statement_sha256"],
                "replacement_statement_sha256": None,
                "semantic_basis": semantic_basis,
                "dependency_check": {
                    "same_module": True,
                    "retired_theorem_dependency_refs": baseline_row.get(
                        "theorem_dependency_refs", []
                    ),
                    "retired_theorem_consumer_refs": baseline_row.get(
                        "theorem_consumer_refs", []
                    ),
                    "current_fully_qualified_consumer_refs": [],
                },
                "target_migrations": (
                    [{**migration, "consumer_paths": consumer_paths}]
                    if migration is not None
                    else []
                ),
                "maximum_inference_preserved": (
                    "The independent synthetic consumer still computes the bounded route "
                    "outcomes, and the reachable resource lifecycle governs accounting, "
                    "verification, residual, reconciliation, and authority boundaries; "
                    "no empirical efficiency or complete-search result follows."
                ),
                "validation_refs": [
                    "scripts/validate_proof_semantic_rationalization_ledger.py",
                    "scripts/validate_proof_semantic_depth_overlay.py",
                    "scripts/validate_efficiency_route_search_probe.py",
                    "scripts/validate_resource_economics_refinement.py",
                    "lean:lake-build",
                ],
                "support_state_effect": "none",
            }
        )

    ledger["summary"].update(
        {
            "executed_retirement_count": 88,
            "executed_scope_rewrite_count": 2,
            "current_live_theorem_count": 1282,
            "remaining_action_count": 70,
            "remaining_action_counts": {"rewrite_with_stronger_model": 70},
        }
    )
    LEDGER.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for name in NAMES:
        row = reviews["theorem_reviews"][f"{MODULE}::{name}"]
        row["review_state"] = "terminally_dispositioned"
        row["disposition"] = "replace_with_stronger_model"
        row["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("replacement_refs", []),
                    "proof-model:resource-economics.request-to-closure-refinement.v1",
                    "lean/AsiStackProofs/ResourceEconomicsRefinement.lean",
                    "scripts/validate_efficiency_route_search_probe.py",
                ]
            )
        )
        row["runtime_consumer_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("runtime_consumer_refs", []),
                    "scripts/validate_efficiency_route_search_probe.py",
                    "scripts/validate_resource_economics_refinement.py",
                ]
            )
        )
        row["review_rationale"] = (
            "Declaration physically retired: copied checklist or result-summary "
            "normalization is superseded by the reachable route-economy lifecycle and "
            "independently computed synthetic route outcomes."
        )
    for tag in (
        "lean:efficiency.claim_admission_lifecycle_route",
        "lean:efficiency.route_search.probe_fixture_bridge",
    ):
        row = reviews["target_reviews"][tag]
        row["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("replacement_refs", []),
                    "proof-model:resource-economics.request-to-closure-refinement.v1",
                    "lean/AsiStackProofs/ResourceEconomicsRefinement.lean",
                ]
            )
        )
        row["runtime_consumer_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("runtime_consumer_refs", []),
                    "scripts/validate_efficiency_route_search_probe.py",
                    "scripts/validate_resource_economics_refinement.py",
                ]
            )
        )
        row["semantic_role"] = (
            "Reachable route-economy lifecycle plus independently computed bounded "
            "route-search outcomes; copied summary normalization is excluded."
        )
        row["review_rationale"] = (
            "Rebound from the legacy Boolean checklist and literal summary theorems to "
            "the stronger lifecycle and independent executable consumer."
        )
    REVIEWS.write_text(
        json.dumps(reviews, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Recorded 22 Efficiency retirements and two target migrations.")


if __name__ == "__main__":
    main()
