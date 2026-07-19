#!/usr/bin/env python3
"""Build the reviewed accepted-transition to canonical-claim identity graph."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence_quality/claim_identity_graph.json"
DOC = ROOT / "docs/claim_identity_graph_reconciliation.md"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
ADDENDUM = ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"

# Every non-direct identity below was semantically adjudicated against the
# transition's scope, surfaces, artifacts, and current chapter owner. This is
# intentionally exhaustive. Prefix matching and first-surface inference are
# forbidden because both silently mis-own multi-chapter and retired claims.
PARENT_BY_CLAIM = {
    "post_v2_governed_work_flagship.bounded_matched_local_result": "intent-to-execution-contracts.core",
    "post_v2_routing_deliberation.bounded_matched_local_result": "routing-heads-and-specialist-cores.core",
    "post_v2_update_causality.bounded_real_mutation_result": "data-engines-continual-learning-and-unlearning.core",
    "post_v2_1.ambiguous_routing.bounded_result": "routing-heads-and-specialist-cores.core",
    "post_v2_1.full_state_rollback.bounded_result": "capability-replacement-and-rollback.core",
    "post_v2_1.full_state_update.no_change_result": "data-engines-continual-learning-and-unlearning.core",
    "post_v2_1.governed_usefulness_rollback.bounded_result": "resource-economics-and-token-budgets.core",
    "post_v2_1.real_model_deliberation.no_change_result": "governed-deliberation-and-test-time-scaling.core",
    "post_v2_1.unlearning_causality.narrow_result": "data-engines-continual-learning-and-unlearning.core",
    "post_v2_3.governance_tax_natural_work.bounded_result": "resource-economics-and-token-budgets.core",
    "resource_economics.governed_useful_throughput_under_natural_work": "resource-economics-and-token-budgets.core",
    "governed-usefulness.held-out-local-policy-effect": "resource-economics-and-token-budgets.core",
    "kerc.broad_matched_total_system_efficiency": "replaceable-cognitive-substrates-beyond-transformer-monoculture.total-system-kiss",
    "kerc.protected_exact_handle_preservation": "replaceable-cognitive-substrates-beyond-transformer-monoculture.exact-latent-separation",
    "kerc.interaction_shared_glossary_break_even": "compact-generative-systems-and-residual-honesty.core",
    "qcsa.active_questions_exact_fixture_value": "cognitive-compilation-and-semantic-ir.core",
    "qcsa.certificate_authority_fields_exact_value": "runtime-adapters-tool-permissions-and-human-approval.core",
    "qcsa.exact_synthetic_matched_advantage": "integrated-reference-architecture.core",
    "qcsa.governance_prevention_resource_tradeoff": "resource-economics-and-token-budgets.core",
    "qcsa.identity_indirection_exact_migration_value": "virtual-context-abi.core",
    "qcsa.migration_compatibility_exact_value": "data-engines-continual-learning-and-unlearning.core",
    "qcsa.open_world_or_production_transfer": "integrated-reference-architecture.core",
    "qcsa.plural_facets_exact_fixture_value": "cognitive-compilation-and-semantic-ir.core",
    "qcsa.reference_implementation_exact_contract_conformance": "integrated-reference-architecture.core",
    "qcsa.semantic_round_trip_exact_preservation": "cognitive-compilation-and-semantic-ir.core",
    "qcsa.task_calibration_exact_result": "evidence-states-and-claim-discipline.core",
    "qcsa.vertical_reference_exact_reversible_trace": "integrated-reference-architecture.core",
    "post_v2_3.residual_honesty_under_pressure.bounded_result": "compact-generative-systems-and-residual-honesty.core",
    "residual-verifier-capacity.heldout-pressure-effect": "verification-bandwidth-and-context-adequacy.core",
    "routing-deliberation.heldout-local-policy-effect": "routing-heads-and-specialist-cores.core",
    "situated-world-model.finite-pomdp-governed-acquisition-and-consolidation": "procedural-memory-and-cognitive-loop-closure.core",
    "update-unlearning.full-state-local-axis-separation": "data-engines-continual-learning-and-unlearning.core",
    "circle-calculus.external_rope_receipt_replay": "circle-calculus-and-proof-carrying-ai-contracts.core",
    "resource-economics.costed_route_budget_slice": "resource-economics-and-token-budgets.core",
    "living-book-methodology.phase5_harness_registry_runner": "living-book-methodology.core",
    "agency-dignity-and-corrigibility.core": "constitutional-alignment-substrate.core",
    "command-contracts-and-semantic-interfaces.core": "intent-to-execution-contracts.core",
    "governance-rights-fork-exit-and-audit.core": "moral-uncertainty-and-value-conflict.core",
    "unified-adaptive-tribunal-and-adversarial-review.core": "scalable-oversight-and-adversarial-ai-control.core",
    "artifact-graphs.epistemic_tcb_fixture": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.github_pages_ci_attestation": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.live_artifact_attestation_probe": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.public_site_record_reality_attestation": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.randomized_artifact_attestation_audit": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.receipt_faithfulness_adversarial_fixture": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.receipt_repository_audit_challenge": "artifact-graphs-audit-logs-and-replay.core",
    "artifact-graphs.record_reality_sequence_bridge": "artifact-graphs-audit-logs-and-replay.core",
    "system-boundaries.authority_revocation_trace": "system-boundaries-and-authority.core",
    "circle-calculus.contract_pack_archive": "circle-calculus-and-proof-carrying-ai-contracts.core",
    "circle-calculus.cyclic_mixer_receipt_slice": "coilra-multicoil-rope-and-cyclic-mixers.core",
    "circle-calculus.kv_cache_ring_buffer_receipt_slice": "coil-attention-cyclic-memory-and-recurrence-contracts.core",
    "circle-calculus.multicoil_phase_receipt_slice": "coilra-multicoil-rope-and-cyclic-mixers.core",
    "circle-calculus.public_consumer_gate": "circle-calculus-and-proof-carrying-ai-contracts.core",
    "circle-calculus.recurrence_schedule_receipt_slice": "coil-attention-cyclic-memory-and-recurrence-contracts.core",
    "compact-generative-systems.seed_rule_exact_regeneration_receipt_slice": "compact-generative-systems-and-residual-honesty.core",
    "circle-calculus.sparse_attention_receipt_slice": "coil-attention-cyclic-memory-and-recurrence-contracts.core",
    "circle-calculus.strided_fanout_receipt_slice": "coil-attention-cyclic-memory-and-recurrence-contracts.core",
    "compact-generative-systems.compact_gvr_receipt_slice": "compact-generative-systems-and-residual-honesty.core",
    "fast-generation-architectures.public_safe_task_bundle_accounting": "fast-generation-architectures.core",
    "runtime-adapters.human_oversight_degradation": "runtime-adapters-tool-permissions-and-human-approval.core",
    "personal-compute-hives.partitioned_authority_fixture": "personal-compute-hives-and-federated-edge-intelligence.core",
    "planning.runtime_replan_delta_audit": "planning-as-a-control-layer.core",
    "planning.scheduler_state_probe": "planning-as-a-control-layer.core",
    "rankfold-neuralfold.local_artifact_import_metadata": "rankfold-neuralfold-and-artifact-compression.core",
    "rankfold-neuralfold.public_safe_replay_probe": "rankfold-neuralfold-and-artifact-compression.core",
    "readiness-gates.readiness_lifecycle_probe": "readiness-gates-residual-escrow-and-quarantine.core",
    "compact-generative-systems.residual_ledger_storage_replay": "compact-generative-systems-and-residual-honesty.core",
    "resource-economics.publication_pipeline_cost_profile": "resource-economics-and-token-budgets.core",
    "resource-economics.local_replay_probe": "resource-economics-and-token-budgets.core",
    "resource-economics.synthetic_load_stability_route_selection": "resource-economics-and-token-budgets.core",
    "resource-economics.finite_burst_load_smoothing_selector": "resource-economics-and-token-budgets.core",
    "resource-economics.workflow_trace_dispatch_accounting": "resource-economics-and-token-budgets.core",
    "resource-economics.local_workload_quality_route_selection": "resource-economics-and-token-budgets.core",
    "resource-economics.scoped_workflow_trace_route_selector": "resource-economics-and-token-budgets.core",
    "routing-heads.synthetic_routing_decision_lease": "routing-heads-and-specialist-cores.core",
    "runtime-adapters.adversarial_boundary_probe": "runtime-adapters-tool-permissions-and-human-approval.core",
    "runtime-adapters.local_effect_replay_probe": "runtime-adapters-tool-permissions-and-human-approval.core",
    "security-kernel.scif_sanitized_commit_replay": "security-kernel-and-digital-scifs.core",
    "project-theseus-as-report-first-implementation-reference.accelerator_parity_manifest_import": "project-theseus-as-report-first-implementation-reference.core",
    "project-theseus-as-report-first-implementation-reference.artifact_retention_replay_gate_import": "project-theseus-as-report-first-implementation-reference.core",
    "project-theseus-as-report-first-implementation-reference.assistant_reference_trace_import": "project-theseus-as-report-first-implementation-reference.core",
    "project-theseus-as-report-first-implementation-reference.book_to_theseus_crosswalk_pointer": "project-theseus-as-report-first-implementation-reference.core",
    "moral-uncertainty-and-value-conflict.theseus_governance_rights_receipt_suite_import": "moral-uncertainty-and-value-conflict.core",
    "project-theseus-as-report-first-implementation-reference.module_definition_of_done_gate_import": "project-theseus-as-report-first-implementation-reference.core",
    "project-theseus-as-report-first-implementation-reference.project_registry_reality_import": "project-theseus-as-report-first-implementation-reference.core",
    "project-theseus-as-report-first-implementation-reference.public_task_bundle_import_summary": "project-theseus-as-report-first-implementation-reference.core",
    "resource-economics.theseus_rlds_minari_trace_export_import": "resource-economics-and-token-budgets.core",
    "resource-economics.simulation_fidelity_receipt_suite_import": "resource-economics-and-token-budgets.core",
    "project-theseus-as-report-first-implementation-reference.work_board_currentness_import": "project-theseus-as-report-first-implementation-reference.core",
    "labor-os.typed_job_durable_lifecycle_probe": "labor-os-and-typed-jobs.core",
}

PROXY_FOR = {
    "post_v2_governed_work_flagship.bounded_matched_local_result",
    "post_v2_routing_deliberation.bounded_matched_local_result",
    "post_v2_update_causality.bounded_real_mutation_result",
    "post_v2_1.ambiguous_routing.bounded_result",
    "post_v2_1.full_state_rollback.bounded_result",
    "post_v2_1.full_state_update.no_change_result",
    "post_v2_1.governed_usefulness_rollback.bounded_result",
    "post_v2_1.real_model_deliberation.no_change_result",
    "post_v2_1.unlearning_causality.narrow_result",
    "post_v2_3.governance_tax_natural_work.bounded_result",
    "resource_economics.governed_useful_throughput_under_natural_work",
    "governed-usefulness.held-out-local-policy-effect",
    "kerc.broad_matched_total_system_efficiency",
    "kerc.interaction_shared_glossary_break_even",
    "qcsa.active_questions_exact_fixture_value",
    "qcsa.exact_synthetic_matched_advantage",
    "qcsa.governance_prevention_resource_tradeoff",
    "qcsa.open_world_or_production_transfer",
    "qcsa.semantic_round_trip_exact_preservation",
    "post_v2_3.residual_honesty_under_pressure.bounded_result",
    "residual-verifier-capacity.heldout-pressure-effect",
    "routing-deliberation.heldout-local-policy-effect",
    "resource-economics.publication_pipeline_cost_profile",
    "resource-economics.local_replay_probe",
    "resource-economics.synthetic_load_stability_route_selection",
    "resource-economics.finite_burst_load_smoothing_selector",
    "resource-economics.workflow_trace_dispatch_accounting",
    "resource-economics.local_workload_quality_route_selection",
    "resource-economics.scoped_workflow_trace_route_selector",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_atoms() -> dict[str, dict]:
    registry = load(REGISTRY)
    atoms = {
        row["atom_id"]: {
            "chapter_id": row["chapter_id"],
            "proposition": row["proposition"],
            "source": REGISTRY.relative_to(ROOT).as_posix(),
        }
        for row in registry["atoms"]
    }
    addendum = load(ADDENDUM)
    for row in addendum["atoms"]:
        atoms[row["id"]] = {
            "chapter_id": addendum["chapter_id"],
            "proposition": row["claim"],
            "source": ADDENDUM.relative_to(ROOT).as_posix(),
        }
    return atoms


def accepted_transitions() -> list[tuple[Path, dict]]:
    rows = []
    for path in sorted((ROOT / "evidence_transitions").glob("**/*.json")):
        item = load(path)
        if item.get("review_status") == "accepted" and item.get("transition_validity_state") == "review_accepted":
            rows.append((path, item))
    return rows


def scope_record(item: dict, relation: str) -> dict:
    artifacts = item.get("artifact_refs", [])
    limitations = item.get("limitations", [])
    non_claims = item.get("non_claims", [])
    negative = item.get("negative_results", [])
    return {
        "population": item["scope_boundary"],
        "environment": "Only the environments, fixtures, corpora, tasks, and execution contexts explicitly identified by the transition and its cited artifacts.",
        "model": (
            "Only the implementation and model identities frozen by the transition artifacts; retained limitations: "
            + "; ".join(limitations)
            if limitations
            else "Only the implementation and model identities frozen by the transition artifacts; no model-family or architecture transfer is implied."
        ),
        "intervention": item["transition_reason"],
        "outcome": (
            f"Recorded transition effect `{item['transition_effect']}` from `{item['old_support_state']}` "
            f"to `{item['new_support_state']}`. Retained negative outcomes: "
            + ("; ".join(negative) if negative else "none recorded beyond the bounded disposition")
        ),
        "authority": "Local repository evidence-review authority only; no deployment, release, rights, institutional, or external-action authority is created.",
        "time": item.get("changelog_ref", "Historical time boundary retained by the transition record and artifact digests."),
        "artifact": artifacts,
        "maximum_inference": item["scope_boundary"] + " Prohibited extensions: " + "; ".join(non_claims),
        "parent_nonpromotion_rationale": (
            "Not applicable to identity: this is the exact canonical atom. Any support movement still requires accepted-transition and registry reconciliation."
            if relation == "atom"
            else "The campaign claim is narrower or instrument-dependent: its parent quantifies over broader implementations, tasks, environments, mechanisms, or lifecycle effects. This edge supplies ownership and traceability only and has no parent support-state effect."
        ),
    }


def build() -> dict:
    atoms = canonical_atoms()
    accepted = accepted_transitions()
    accepted_ids = {item["claim_id"] for _, item in accepted}
    direct_ids = accepted_ids & set(atoms)
    indirect_ids = accepted_ids - set(atoms)
    if set(PARENT_BY_CLAIM) != indirect_ids:
        missing = sorted(indirect_ids - set(PARENT_BY_CLAIM))
        stale = sorted(set(PARENT_BY_CLAIM) - indirect_ids)
        raise ValueError(f"manual identity adjudication drift; missing={missing}, stale={stale}")
    if not PROXY_FOR <= indirect_ids:
        raise ValueError("proxy adjudication includes a direct or absent claim")

    records = []
    for path, item in accepted:
        claim_id = item["claim_id"]
        if claim_id in atoms:
            relation = "atom"
            parent_id = claim_id
        else:
            relation = "proxy_for" if claim_id in PROXY_FOR else "subclaim_of"
            parent_id = PARENT_BY_CLAIM[claim_id]
        if parent_id not in atoms:
            raise ValueError(f"unknown canonical parent {parent_id} for {claim_id}")
        parent = atoms[parent_id]
        records.append({
            "transition_id": item["transition_id"],
            "transition_path": path.relative_to(ROOT).as_posix(),
            "transition_sha256": sha256(path),
            "claim_id": claim_id,
            "primary_relation": relation,
            "canonical_parent_id": parent_id,
            "canonical_parent_kind": "atom",
            "owner_chapter_id": parent["chapter_id"],
            "canonical_parent_proposition": parent["proposition"],
            "canonical_parent_source": parent["source"],
            "identity_scope": scope_record(item, relation),
            "parent_support_state_effect": (
                "exact_transition_record_subject_to_registry_reconciliation"
                if relation == "atom"
                else "none"
            ),
            "identity_decision_method": "manual_semantic_transition_surface_and_scope_review_2026_07_17",
            "resolution_state": "resolved",
        })

    relations = Counter(row["primary_relation"] for row in records)
    owners = Counter(row["owner_chapter_id"] for row in records)
    return {
        "schema_version": "asi_stack.claim_identity_graph.v1",
        "snapshot_date": "2026-07-17",
        "authority": "Corben Sorenson",
        "source_transition_root": "evidence_transitions",
        "canonical_atom_sources": [
            REGISTRY.relative_to(ROOT).as_posix(),
            ADDENDUM.relative_to(ROOT).as_posix(),
        ],
        "identity_policy": {
            "allowed_primary_relations": ["atom", "subclaim_of", "alias_of", "proxy_for"],
            "exactly_one_primary_relation_required": True,
            "implicit_prefix_or_surface_mapping_allowed": False,
            "indirect_parent_support_movement_allowed": False,
            "proxy_to_target_inference_allowed": False,
            "mapping_is_evidence": False,
        },
        "summary": {
            "transition_file_count": len(list((ROOT / "evidence_transitions").glob("**/*.json"))),
            "review_accepted_transition_count": len(records),
            "canonical_atom_count": len(atoms),
            "direct_atom_relation_count": len(direct_ids),
            "indirect_relation_count": len(indirect_ids),
            "resolved_transition_count": len(records),
            "unresolved_transition_count": 0,
            "relation_counts": dict(sorted(relations.items())),
            "owner_chapter_counts": dict(sorted(owners.items())),
            "support_state_effect": "none",
            "release_effect": "none",
        },
        "records": records,
        "non_claims": [
            "Identity resolution does not promote, refute, rehabilitate, or validate any claim.",
            "An indirect relation does not transfer support from a campaign claim to its canonical parent.",
            "A proxy result remains evidence only about its declared proxy until construct validity is separately established.",
            "Historical negative and no-change transitions still require N0-N5 competence rehabilitation.",
        ],
    }


def render_doc(value: dict) -> str:
    summary = value["summary"]
    lines = [
        "# Accepted-Transition Claim Identity Reconciliation",
        "",
        "Status: complete identity-resolution tranche; no support or release effect  ",
        "Snapshot: 2026-07-17  ",
        "Machine graph: `evidence_quality/claim_identity_graph.json`  ",
        "Governing roadmap: `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`",
        "",
        "## Result",
        "",
        f"All {summary['review_accepted_transition_count']} review-accepted transitions now have exactly one primary canonical identity relation. "
        f"There are {summary['direct_atom_relation_count']} exact atom relations, "
        f"{summary['relation_counts']['subclaim_of']} bounded subclaim relations, and "
        f"{summary['relation_counts']['proxy_for']} proxy relations. Zero accepted transitions remain unmapped.",
        "",
        "This resolves ownership and traceability; it does not create evidence. An exact `atom` relation still uses the accepted-transition and registry-reconciliation process. A `subclaim_of` or `proxy_for` edge has no support-state effect on its parent. Proxy results cannot become target results without separate construct-validity evidence.",
        "",
        "## Adjudication method",
        "",
        "The 90 non-direct claims were reviewed against their transition scope, named chapter surfaces, result artifacts, limitations, non-claims, and current manifest owner. No prefix matcher, first-chapter heuristic, or automatic parent promotion was used. Retired chapter-core claims were assigned to their current consolidated owner as bounded subclaims rather than aliases, because consolidation did not prove proposition identity.",
        "",
        "Each graph row preserves population, environment, model, intervention, outcome, authority, time, artifact, maximum-inference, and parent-nonpromotion fields. The transition file digest makes silent outcome or scope rewriting detectable.",
        "",
        "## High-risk decisions",
        "",
        "- `kerc.broad_matched_total_system_efficiency` is a `proxy_for` the total-system KISS atom, not an exact architecture refutation. Its competence and N-level remain pending.",
        "- `kerc.protected_exact_handle_preservation` is a bounded `subclaim_of` exact latent-state separation; it does not establish general semantic, security, or architecture behavior.",
        "- QCSA exact-fixture claims remain subclaims or proxies under their current chapter owners; they do not promote QCSA, the integrated architecture, or any chapter core.",
        "- The retired Agency, Command Contracts, Governance Rights, and Unified Tribunal core IDs are bounded subclaims under their consolidated owners, not identity aliases.",
        "- The one existing `empirical-test-backed` local selector transition resolves as a proxy for Resource Economics; it is not the roadmap's still-missing competence-qualified natural, non-authored empirical result.",
        "",
        "## Complete crosswalk",
        "",
        "| Transition | Campaign claim | Relation | Canonical parent | Owner | Parent effect |",
        "|---|---|---|---|---|---|",
    ]
    for row in value["records"]:
        lines.append(
            f"| `{row['transition_id']}` | `{row['claim_id']}` | `{row['primary_relation']}` | "
            f"`{row['canonical_parent_id']}` | `{row['owner_chapter_id']}` | "
            f"`{row['parent_support_state_effect']}` |"
        )
    lines.extend([
        "",
        "## Validation boundary",
        "",
        "`python3 scripts/validate_claim_identity_graph.py` checks the exact accepted-transition denominator, transition digests, canonical parent existence and proposition, owner consistency, preserved artifacts and non-claims, zero indirect parent movement, deterministic regeneration, and twelve adversarial mutations.",
        "",
        "This reconciliation does not rehabilitate historical negative results. P1 must still assign N0–N5 using the claim-bearing experiment competence standard before any negative or no-change result supports broader inference.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    encoded = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    rendered = render_doc(value)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != encoded:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale; run scripts/build_claim_identity_graph.py")
        if not DOC.exists() or DOC.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"{DOC.relative_to(ROOT)} is stale; run scripts/build_claim_identity_graph.py")
        print(
            "Claim identity graph current: "
            f"{value['summary']['resolved_transition_count']} resolved, "
            f"{value['summary']['direct_atom_relation_count']} direct, "
            f"{value['summary']['indirect_relation_count']} indirect, 0 unresolved."
        )
        return
    OUT.write_text(encoded, encoding="utf-8")
    DOC.write_text(rendered, encoding="utf-8")
    print(
        "Claim identity graph wrote: "
        f"{value['summary']['resolved_transition_count']} resolved, "
        f"{value['summary']['direct_atom_relation_count']} direct, "
        f"{value['summary']['indirect_relation_count']} indirect, 0 unresolved."
    )


if __name__ == "__main__":
    main()
