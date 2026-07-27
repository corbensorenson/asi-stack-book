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
    "lean/AsiStackProofs/EvidenceTransitionRefinement.lean",
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
    "scripts/validate_evidence_transition_refinement.py",
    "scripts/integrate_c6_efficiency_route_economy_consolidation.py",
    "scripts/integrate_c6_evidence_transition_consolidation.py",
    "scripts/integrate_c6_theseus_repository_mirror_retirements.py",
    "scripts/validate_retired_theseus_formal_mirrors.py",
    "proofs/c6_remaining_stronger_model_audit.json",
    "lean/AsiStackProofs/TheseusReference.lean",
    "scripts/validate_theseus_public_task_bundle_import.py",
    "scripts/validate_theseus_fast_support_lane.py",
    "scripts/validate_theseus_artifact_retention_replay_import.py",
    "scripts/validate_theseus_module_definition_of_done_import.py",
    "scripts/validate_theseus_project_registry_import.py",
    "scripts/validate_theseus_assistant_reference_trace_import.py",
    "scripts/validate_theseus_accelerator_parity_manifest_import.py",
    "scripts/validate_theseus_book_crosswalk_import.py",
    "scripts/validate_theseus_work_board_import.py",
    "experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json",
    "experiments/substrate_adoption_trace/results/2026-07-02-local.json",
    "experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json",
    "experiments/failure_taxonomy_detector/results/2026-07-02-local.json",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
    "experiments/planning_scheduler_state/results/2026-07-02-local.json",
    "experiments/planning_runtime_replan_delta/results/2026-07-02-local.json",
    "experiments/policy_update_lease/results/2026-07-02-local.json",
    "experiments/policy_optimization_refinement/results/2026-07-16-local.json",
    "experiments/evidence_transition_refinement/results/2026-07-26-local.json",
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
            "One immutable 1,370-theorem baseline; 151 exact, ordered transactions; "
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
            "or result-summary theorems, sixteen legacy evidence-transition fixture "
            "theorems retired after reachable-refinement rebinding, two redundant "
            "authored fixture witnesses, and 43 Project Theseus repository-import "
            "summary mirrors retired while their executable receipts remain; "
            "the current overlay; frozen historical registry; and reconciled target, "
            "roadmap, and status surfaces."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require immutable baseline and theorem-block digests, exact same-model "
            "statement identity for the duplicate, dependency-and-consumer-safe removals, "
            "ten counterexample, five decision-model, thirteen scope-narrowing, eleven "
            "validator-route-family migrations, and 43 formal-target-to-executable-only "
            "migrations, retained or honestly replanned target ownership, a 1,227-theorem "
            "current estate, an exact nine-action remaining "
            "queue, meta-audit exclusion from implementation binding, and no support or "
            "release effect."
        ),
        "output_assertions": [
            "baseline commit and artifact digests exact",
            "retired and retained declarations share one authored model",
            "normalized theorem statements exact",
            "retired theorem has no theorem consumer",
            "149 retired declarations absent, twenty-five proposition-preserving or replacement-bound actions, and 126 intentionally null replacements",
            "two bibliography targets migrated to derived counterexample gates",
            "two benchmark targets migrated to derived decision-model gates",
            "two Stable Capability Fields targets narrowed to retained derived routes",
            "seven Evidence States targets consolidated into two reachable lifecycle targets and one retained foundational blocker",
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
            "sixteen legacy evidence-transition fixture theorems replaced by projection-aware reachable lifecycle and independent consumer custody",
            "forty-three Project Theseus repository-import summary mirrors and nine formal targets retired while executable validators and result receipts remain",
            "proof-custody meta-audit does not inflate semantic implementation depth",
            "1,227 current theorem declarations",
            "nine stronger-model actions remain",
            "frozen 1,151-theorem and 298-target registry preserved",
            "16 mutations reject",
            "no support or release effect",
        ],
        "claim_scope": (
            "149 dependency-safe declaration retirements: one exact same-model "
            "duplicate, sixty-two premise-restating projections, and twenty-five legacy fixture "
            "or checklist theorems, sixteen evidence-transition fixture theorems, two "
            "redundant authored witnesses, and 43 copied Project Theseus repository "
            "summaries. Two theorem names are rewritten without proposition drift. Ninety public "
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
        "semantic_review_state": "checked_one_hundred_forty_nine_c6_retirements_two_scope_rewrites_and_ninety_target_migrations",
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
