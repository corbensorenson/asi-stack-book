#!/usr/bin/env python3
"""Register the maintenance/transfer/publication roadmap validator."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_post_v2_3_maintenance_transfer_and_publication_roadmap.py"
ARTIFACTS = [
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "docs/structural_completeness_chapter_research_2026_07_19.md",
    "sources/source_inventory.json",
    "sources/source_notes/ext_circuit_tracing_2025.md",
    "sources/source_notes/ext_scaling_sparse_autoencoders_2024.md",
    "sources/source_notes/ext_world_models_2018.md",
    "sources/source_notes/ext_dreamer_v3_2025.md",
    "sources/source_notes/ext_meaningful_human_control_actionable_2022.md",
    "sources/source_notes/ext_agentic_oversight_practice_2026.md",
    "sources/source_notes/ext_nist_deployed_ai_monitoring_2026.md",
    "docs/claim_bearing_experiment_competence_standard.md",
    "evidence_quality/claim_identity_graph.json",
    "schemas/claim_identity_graph.schema.json",
    "docs/claim_identity_graph_reconciliation.md",
    "scripts/validate_claim_identity_graph.py",
    "evidence_quality/negative_result_rehabilitation.json",
    "schemas/negative_result_rehabilitation.schema.json",
    "docs/negative_result_rehabilitation.md",
    "scripts/validate_negative_result_rehabilitation.py",
    "evidence_quality/negative_inference_surface_audit.json",
    "schemas/negative_inference_surface_audit.schema.json",
    "docs/negative_inference_surface_audit.md",
    "scripts/validate_negative_inference_surface_audit.py",
    "evidence_quality/p2_frontier_selection.json",
    "schemas/p2_frontier_selection.schema.json",
    "docs/p2_frontier_selection.md",
    "scripts/validate_p2_frontier_selection.py",
    "evidence_quality/p2_development_corpus_preflight.json",
    "schemas/p2_development_corpus_preflight.schema.json",
    "docs/p2_development_corpus_preflight.md",
    "scripts/validate_p2_development_corpus_preflight.py",
    "evidence_quality/p2_gold_preflight_diagnosis.json",
    "schemas/p2_gold_preflight_diagnosis.schema.json",
    "docs/p2_gold_preflight_diagnosis.md",
    "scripts/validate_p2_gold_preflight_diagnosis.py",
    "evidence_quality/p2_task_qualification_and_replacement_policy.json",
    "schemas/p2_task_qualification_and_replacement_policy.schema.json",
    "docs/p2_task_qualification_and_replacement_policy.md",
    "scripts/validate_p2_task_qualification_and_replacement_policy.py",
    "evidence_quality/p2_resource_ceiling.json",
    "schemas/p2_resource_ceiling.schema.json",
    "docs/p2_resource_ceiling.md",
    "scripts/validate_p2_resource_ceiling.py",
    "experiments/p2_governed_repository_admission/corpus/replacement_queue.json",
    "schemas/p2_replacement_queue.schema.json",
    "docs/p2_replacement_queue.md",
    "scripts/build_p2_replacement_queue.py",
    "scripts/validate_p2_replacement_queue.py",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json",
    "scripts/validate_post_v2_3_maintenance_transfer_and_publication_roadmap.py",
    "scripts/register_post_v2_3_maintenance_transfer_and_publication_roadmap.py",
    "evidence_quality/p7_1a_w2_narrative_audit.json",
    "scripts/validate_p7_1a_w2_narrative_audit.py",
    "proofs/semantic_cluster_audits/safety_assurance_and_oversight.json",
    "scripts/validate_p4_c2_semantic_proof_cluster.py",
    "evidence_quality/p7_2_t1_white_box_reader_integration.json",
    "scripts/validate_p7_2_t1_white_box_reader_integration.py",
    "proofs/semantic_cluster_audits/authority_effect_rollback_and_corrigibility.json",
    "scripts/validate_p4_c3_semantic_proof_cluster.py",
    "evidence_quality/p7_2_t2_governed_world_models_reader_integration.json",
    "scripts/validate_p7_2_t2_governed_world_models_reader_integration.py",
    "proofs/semantic_cluster_audits/learning_update_state_and_unlearning.json",
    "scripts/validate_p4_c4_semantic_proof_cluster.py",
    "docs/x_article_synopsis_completion.md",
    "release_records/2026-07-16-post-v2-3-claim-proof-sota-roadmap-complete-no-public-release.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [u for u in registry["units"] if u.get("script") != SCRIPT]
    used = {u["order"] for u in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "publication_gate",
        "input_contract": "Completed claim-proof predecessor; exact no-release terminal record; active unfinished-work successor; 3,745 canonical atoms; all 117 transition files and 115 accepted transitions; complete 25-direct/90-indirect claim identity graph; retrospective N0-N5 rehabilitation of all 90 accepted negative/no-change results; prospective P2 selection, natural development-corpus custody, fixed-denominator gold diagnosis, frozen replacement policy and resource ceiling, and deterministic metadata-only replacement queue; terminal P7.1a W1/W2 audits; terminal P7.2-T1/T2 reader integrations with protected outcomes closed; four terminal bounded semantic proof clusters; current proof-depth receipt; N0-N5 experiment-competence contract; stale main attestation boundary; X derivative disposition; and four public truth surfaces.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject multiple active roadmaps, stale public pointers, invented transition identity, false-negative laundering, weakened broad-refutation gates, proof-baseline drift, false clean attestation, branch widening, conversational/private-review dependencies, and invented support/publication authority.",
        "output_assertions": ["P0 authority wait, P1/M1 complete, active P2/M2", "115 accepted transitions with 25 direct and 90 indirect identities resolved and zero unmapped", "90 accepted negative/no-change transitions classified as 1 N0, 15 N1, 74 N2, and 0 N3-N5", "75 current surfaces including 55 chapters reconciled", "zero broad or chapter-core negative inference", "P2 prospectively selected from five candidates", "1117-task post-snapshot corpus universe and 12-task development pool", "fixed P2 gold denominator fully dispositioned as 8 qualified and 4 N0 replacements", "62 verified arm logs and 8 attempts", "replacement policy and monitored resource ceiling frozen before draw", "metadata-only queue contains 30 unique repositories while candidate content remains unopened", "construct and resource gates pending with heldout closed", "P7.2-T1/T2 terminal with P7.2-T3 next", "four of six semantic proof clusters terminal at bounded adequate scope with P4-C5 next", "N0-N5 competence contract", "current proof snapshot", "main-only stale attestation truth", "v2.3.0 latest public release", "X source current and historical platform draft stale", "no support or release effect", "sixty mutations reject"],
        "claim_scope": "Roadmap continuity, experiment-competence governance, claim-identity truth, public-state maintenance, and owner-gated external actions only.",
        "negative_controls": "validator_owned_sixty_competence_identity_rehabilitation_surface_p2_editorial_semantic_proof_and_attestation_mutations",
        "negative_control_cases": ["false publication", "support laundering", "hosted-chat dependency", "private-review gate", "authority widening", "claim mapping erasure", "unresolved mapping regression", "natural empirical invention", "exploration promotion", "rehabilitation reopening", "broad-refutation weakening", "N3 invention", "broad-negative inference laundering", "surface language regression", "P2 selected-claim drift", "P2 premature heldout opening", "P2 development-final laundering", "P2 gold denominator shrink", "P2 N0 mechanism laundering", "P2 outcome-aware replacement", "P2 replacement queue state erased", "P2 replacement queue content leak", "P2 replacement queue repository reuse", "P2 resource premature pass", "P2 resource claim laundering", "P7 next-packet rollback", "P4 next-packet rollback", "semantic-cluster progress drift", "false clean attestation", "branch permission", "N5 deletion", "false-negative rule deletion", "missing successor continuity", "stale predecessor"],
        "prohibited_inference": "An active competence roadmap or installed contract is not evidence that an experiment is competent, a negative result is rehabilitated, a claim is mapped or supported, a proof is semantically adequate, or any research, reader, publication, safety, SOTA, AGI, or ASI objective is complete.",
        "contract_precision": "exact", "semantic_review_state": "checked_false_negative_competence_claim_identity_semantic_proof_attestation_public_truth_and_non_claim_boundaries",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda u: u["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
