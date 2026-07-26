#!/usr/bin/env python3
"""Register the cumulative C6 dependency-safe rationalization ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "validate_proof_semantic_rationalization_ledger.py"
REGISTER = "scripts/register_proof_semantic_rationalization_ledger.py"
ARTIFACTS = [
    "scripts/validate_proof_semantic_rationalization_ledger.py",
    "scripts/build_proof_semantic_depth_overlay.py",
    "schemas/proof_semantic_rationalization_ledger.schema.json",
    "proofs/proof_semantic_rationalization_ledger.json",
    "proofs/proof_semantic_depth_overlay.json",
    "proofs/proof_rationalization_registry.json",
    "lean/AsiStackProofs/ScalableOversightRefinement.lean",
    "lean/AsiStackProofs/SafetyCriticalLifecycle.lean",
    "lean/AsiStackProofs/BibliographyPlan.lean",
    "lean/AsiStackProofs/BenchmarkRatchets.lean",
    "lean/AsiStackProofs/StableCapabilityFields.lean",
    "lean/AsiStackProofs/RuntimeAdapters.lean",
    "lean/AsiStackProofs/SearchSubstrates.lean",
    "lean/AsiStackProofs/ArtifactStewardAgents.lean",
    "lean/AsiStackProofs/CoilAttentionMemory.lean",
    "lean/AsiStackProofs/CyclicMixers.lean",
    "lean/AsiStackProofs/Efficiency.lean",
    "lean/AsiStackProofs/FailureModes.lean",
    "lean/AsiStackProofs/IntentToExecution.lean",
    "lean/AsiStackProofs/Planning.lean",
    "lean/AsiStackProofs/LivingBook.lean",
    "lean/AsiStackProofs/PlanForge.lean",
    "lean/AsiStackProofs/ProofEnvelope.lean",
    "lean/AsiStackProofs/PrototypeRoadmap.lean",
    "lean/AsiStackProofs/SecurityKernel.lean",
    "lean/AsiStackProofs/PolicyOptimization.lean",
    "lean/AsiStackProofs/PolicyOptimizationRefinement.lean",
    "lean/AsiStackProofs/ResourceEconomicsRefinement.lean",
    "scripts/validate_runtime_adapter_adversarial_boundary_probe.py",
    "scripts/validate_substrate_adoption_trace.py",
    "scripts/validate_artifact_steward_lifecycle_probe.py",
    "scripts/validate_efficiency_route_search_probe.py",
    "scripts/validate_architecture_red_team.py",
    "scripts/validate_failure_taxonomy_detector_probe.py",
    "scripts/validate_intent_execution_handoff_probe.py",
    "scripts/validate_planning_scheduler_state_probe.py",
    "scripts/validate_planning_runtime_replan_delta.py",
    "scripts/validate_living_book_change_packets.py",
    "scripts/validate_proof_artifact_audit.py",
    "scripts/validate_prototype_phase_gates.py",
    "scripts/validate_security_kernel.py",
    "scripts/validate_policy_update_lease_probe.py",
    "scripts/validate_policy_optimization_refinement.py",
    "scripts/validate_resource_economics_refinement.py",
    "scripts/integrate_c6_efficiency_route_economy_consolidation.py",
    "experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json",
    "experiments/substrate_adoption_trace/results/2026-07-02-local.json",
    "experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json",
    "experiments/failure_taxonomy_detector/results/2026-07-02-local.json",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
    "experiments/planning_scheduler_state/results/2026-07-02-local.json",
    "experiments/planning_runtime_replan_delta/results/2026-07-02-local.json",
    "experiments/policy_update_lease/results/2026-07-02-local.json",
    "experiments/policy_optimization_refinement/results/2026-07-16-local.json",
    "docs/substrate_adoption_trace.md",
    "docs/artifact_steward_lifecycle_probe.md",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
    "book_structure.json",
    "docs/book_outline.md",
    "chapters/open-research-agenda-and-bibliography-plan.qmd",
    "chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd",
    "chapters/runtime-adapters-tool-permissions-and-human-approval.qmd",
    "chapters/mathematical-and-search-substrates.qmd",
    "chapters/artifact-steward-agents-and-living-project-governance.qmd",
    "chapters/coil-attention-cyclic-memory-and-recurrence-contracts.qmd",
    "chapters/coilra-multicoil-rope-and-cyclic-mixers.qmd",
    "chapters/the-efficient-asi-hypothesis.qmd",
    "chapters/failure-modes-of-ungoverned-intelligence.qmd",
    "chapters/intent-to-execution-contracts.qmd",
    "chapters/planning-as-a-control-layer.qmd",
    "chapters/executable-specifications-and-lean-proof-envelope.qmd",
    "chapters/prototype-roadmap.qmd",
    "chapters/living-book-methodology.qmd",
    "chapters/security-kernel-and-digital-scifs.qmd",
    "chapters/policy-optimization-and-learning-from-feedback.qmd",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "validation/registry.json",
]


def main() -> None:
    path = ROOT / "validation" / "registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    existing_order = next(
        (row["order"] for row in registry["units"] if row.get("script") == SCRIPT),
        None,
    )
    registry["units"] = [
        row for row in registry["units"] if row.get("script") != SCRIPT
    ]
    order = (
        existing_order
        if existing_order is not None
        else max(row["order"] for row in registry["units"]) + 1
    )
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": (
            "One immutable 1,370-theorem baseline; ninety exact, ordered transactions; "
            "the baseline Scalable Oversight, Bibliography Plan, Benchmark Ratchets, and "
            "Policy Optimization, Stable Capability Fields, Evidence States, and Runtime "
            "Adapters, Search Substrates, Artifact Steward Agents, Coil Attention Memory, "
            "and Cyclic Mixers, Efficiency, Failure Modes, Intent to Execution, Planning, "
            "Living Book, PlanForge, Proof Envelope, Prototype Roadmap, and Security Kernel "
            "modules; one same-model normalized duplicate pair; sixty-five "
            "premise-restating projections, twenty-two with derived "
            "replacements, twenty-three retired after public-target narrowing, five unused projections retired without target "
            "change, twelve summary projections retired after route-family validator rebinding, "
            "two proposition-preserving theorem-name scope rewrites, three legacy "
            "policy-lease fixture theorems, and twenty-two legacy efficiency checklist "
            "or result-summary theorems retired after reachable-refinement rebinding; "
            "the current overlay; frozen historical registry; and reconciled target, "
            "roadmap, and status surfaces."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require immutable baseline and theorem-block digests, exact same-model "
            "statement identity for the duplicate, dependency-and-consumer-safe removals, "
            "ten counterexample, five decision-model, thirteen scope-narrowing, and eleven "
            "validator-route-family target migrations, retained or honestly replanned "
            "target ownership, a 1,282-theorem current estate, an exact 70-action remaining "
            "queue, meta-audit exclusion from implementation binding, and no support or "
            "release effect."
        ),
        "output_assertions": [
            "baseline commit and artifact digests exact",
            "retired and retained declarations share one authored model",
            "normalized theorem statements exact",
            "retired theorem has no theorem consumer",
            "eighty-eight retired declarations absent, twenty-five proposition-preserving or replacement-bound actions, and sixty-five intentionally null replacements",
            "two bibliography targets migrated to derived counterexample gates",
            "two benchmark targets migrated to derived decision-model gates",
            "two Stable Capability Fields targets narrowed to retained derived routes",
            "five Evidence States targets narrowed to planned reachable or independently implemented models",
            "Runtime adapter validator bound to fifteen route theorems rather than a summary projection",
            "Search Substrates targets bound to two finite counterexamples and one honestly planned reachable route model",
            "Artifact Steward targets bound to two retained lifecycle routes and two honestly planned reachable models",
            "Coil memory targets bound to two derived finite negative cases",
            "Cyclic mixer targets bound to two derived finite negative cases",
            "Efficiency targets split between two derived finite negative cases and the reachable route-economy lifecycle plus independent route-search consumer",
            "Failure Modes authority target bound to one retained finite decision route",
            "Failure Modes detector consumer bound to fifteen retained route theorems",
            "Intent-to-Execution handoff consumer bound to nine retained route theorems",
            "Planning scheduler consumer bound to fourteen retained admission-route theorems",
            "Planning replan consumer bound to four retained delta-route theorems",
            "Living Book targets bound to retained manifest and synchronization rejection cases",
            "PlanForge target narrowed to listed-edge ordering and self-edge exclusion",
            "Proof Envelope targets split between independent validators and retained negative cases",
            "Prototype Roadmap targets bound to retained research-only and promotion-rejection routes",
            "Security Kernel target bound to retained unauthorized and missing-permission denial routes",
            "Circle receipt target narrowed to the retained missing-boundary rejection",
            "Theseus artifact-surface target narrowed to the retained missing-surface rejection",
            "Stable Capability Fields readiness lemma retained because five concrete negative cases consume it",
            "two misleading theorem names replaced without changing their normalized propositions",
            "three legacy policy-lease fixture theorems replaced by reachable refinement and independent consumer custody",
            "twenty-two legacy efficiency checklist and summary theorems replaced by reachable route-economy and independent consumer custody",
            "proof-custody meta-audit does not inflate semantic implementation depth",
            "1,282 current theorem declarations",
            "70 stronger-model actions remain",
            "frozen 1,151-theorem and 298-target registry preserved",
            "16 mutations reject",
            "no support or release effect",
        ],
        "claim_scope": (
            "Eighty-eight dependency-safe declaration retirements: one exact same-model "
            "duplicate, sixty-two premise-restating projections, and twenty-five legacy fixture "
            "or checklist theorems. Two theorem names are rewritten without proposition drift. Forty-one public "
            "targets migrate to counterexample, decision-model, narrower retained-route, "
            "or honestly planned stronger-model wording; the runtime-adapter target remains "
            "implemented through its fifteen explicit route theorems."
        ),
        "negative_controls": (
            "validator_owned_sixteen_baseline_digest_sequence_identity_statement_dependency_"
            "consumer_relation_target_denominator_and_support_mutations"
        ),
        "negative_control_cases": [
            "baseline commit substitution",
            "overlay digest substitution",
            "action deletion or reordering",
            "retired or replacement identity substitution",
            "statement substitution",
            "dependency laundering",
            "consumer laundering",
            "target migration erasure",
            "decision semantic laundering",
            "null replacement laundering",
            "scope-rewrite proposition substitution",
            "refinement rebinding erasure",
            "remaining denominator inflation",
            "support promotion",
        ],
        "prohibited_inference": (
            "This transaction does not strengthen the retained finite-model theorem or "
            "establish reviewer competence, implementation correctness, useful oversight, "
            "deployment, transfer, safety, SOTA, AGI, ASI, or claim support."
        ),
        "contract_precision": "exact_immutable_cumulative_dependency_safe_retirement_ledger",
        "semantic_review_state": "checked_eighty_eight_c6_retirements_two_scope_rewrites_and_forty_one_target_migrations",
    })
    required = registry["required_artifacts"]
    for artifact in ARTIFACTS + [REGISTER]:
        if artifact not in required:
            required.append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(registry["units"]),
    }
    path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "Registered cumulative proof semantic-rationalization ledger: "
        f"{len(registry['units'])} units, {len(required)} artifacts."
    )


if __name__ == "__main__":
    main()
