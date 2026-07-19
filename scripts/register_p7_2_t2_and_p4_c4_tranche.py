#!/usr/bin/env python3
"""Register the terminal P7.2-T2 reader packet and P4-C4 semantic audit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
REGISTER = "scripts/register_p7_2_t2_and_p4_c4_tranche.py"

UNITS = [
    {
        "script": "validate_governed_world_model_contract.py",
        "artifacts": [
            "scripts/validate_governed_world_model_contract.py",
            "schemas/governed_world_model_packet.schema.json",
            "tests/fixtures/protocol_records/governed_world_model_packet.valid.json",
            "experiments/governed_world_model_argument_exit/preregistration.json",
            "lean/AsiStackProofs/GovernedWorldModels.lean",
            "chapters/governed-world-models-and-reality-grounding.qmd",
        ],
        "input_contract": "One typed safe-hold record-shape fixture, a prospectively frozen but unexecuted six-arm world-model campaign, and a finite admission/residual/non-authority model.",
        "output_contract": "Require exact model/observation/rollout/residual custody, protected outcome closure, eight competence gates, seven rescue steps, an N3 exact ceiling, nine Lean declarations, and thirteen rejecting mutations.",
        "output_assertions": ["1 safe-hold record fixture", "6 matched arms", "8 competence gates", "7 rescue steps", "9 Lean declarations", "13 mutations reject", "support/effect authority none"],
        "claim_scope": "Qualified-branch packet shape, campaign custody, and finite admission/residual-route semantics only.",
        "negative_controls": "validator_owned_thirteen_identity_freshness_support_authority_residual_protocol_and_predecessor_mutations",
        "negative_control_cases": ["effect authorization", "release grant", "freshness laundering", "unsupported admission", "residual deletion", "outcome opening", "negative-scope inflation", "predecessor support borrowing", "P2 displacement"],
        "prohibited_inference": "The fixture, theorem, and protocol do not establish prediction quality, grounding, calibration, useful planning, safe control, support, release, publication, AGI, or ASI.",
        "semantic_review_state": "checked_world_model_packet_residual_and_non_authority_semantics",
    },
    {
        "script": "validate_p7_2_t2_governed_world_models_reader_integration.py",
        "artifacts": [
            "scripts/validate_p7_2_t2_governed_world_models_reader_integration.py",
            "evidence_quality/p7_2_t2_governed_world_models_reader_integration.json",
            "docs/p7_2_t2_governed_world_models_reader_integration.md",
            "book_structure.json", "sources/source_inventory.json", "proofs/proof_manifest.json",
            "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
            "index.qmd", "appendices/B_glossary.qmd", "appendices/C_claim_evidence_matrix.qmd",
            "appendices/G_corben_source_corpus.qmd", "appendices/H_external_sources.qmd",
            "chapters/planning-as-a-control-layer.qmd",
            "chapters/cognitive-compilation-and-semantic-ir.qmd",
            "chapters/integrated-reference-architecture.qmd",
        ],
        "input_contract": "The admitted world-model chapter, nine exact source mappings, two implemented public proof targets, bounded predecessor evidence, a closed protected campaign, and adjacent reader surfaces.",
        "output_contract": "Bind artifact digests, preserve source/role/proof/predecessor denominators, require handoffs and synthesis surfaces, keep protected outcomes closed, and reject thirteen integration mutations.",
        "output_assertions": ["1 terminal argument-level chapter", "9 source mappings", "2 implemented proof targets", "9 Lean declarations", "6 claim-bearing arms", "13 integration mutations reject", "support effect none"],
        "claim_scope": "P7.2-T2 chapter necessity, argument-level integration, traceability, and reader continuity only.",
        "negative_controls": "validator_owned_thirteen_manifest_source_digest_proof_predecessor_custody_role_and_support_mutations",
        "negative_control_cases": ["chapter deletion", "source-target deletion", "digest drift", "proof reduction", "predecessor borrowing", "outcome opening", "P2 displacement", "role deletion", "support laundering"],
        "prohibited_inference": "Terminal reader integration does not establish a world-model, grounding, causal, control, safety, empirical, release, publication, AGI, or ASI result.",
        "semantic_review_state": "checked_terminal_governed_world_models_argument_chapter_integration",
    },
    {
        "script": "validate_p4_c4_semantic_proof_cluster.py",
        "artifacts": [
            "scripts/validate_p4_c4_semantic_proof_cluster.py",
            "proofs/semantic_cluster_audits/learning_update_state_and_unlearning.json",
            "docs/p4_c4_learning_update_state_and_unlearning_semantic_audit.md",
            "lean/AsiStackProofs/DataEngineLifecycleRefinement.lean",
            "lean/AsiStackProofs/PolicyOptimizationRefinement.lean",
            "lean/AsiStackProofs/ModelWeightCustody.lean",
            "lean/AsiStackProofs/ContextTransactionRefinement.lean",
            "chapters/data-engines-continual-learning-and-unlearning.qmd",
            "chapters/policy-optimization-and-learning-from-feedback.qmd",
            "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd",
            "chapters/context-transactions-snapshots-mounts-and-taint.qmd",
        ],
        "input_contract": "A frozen four-module data/update/weight/context cluster with 31 public targets and 39 theorem declarations.",
        "output_contract": "Require exact propositions, modeled state, assumptions, countermodels, consumers, mutation evidence, claim-axis separation, and ceilings; execute four consumers and reject twelve audit mutations.",
        "output_assertions": ["4 adequate modules", "31 public targets", "39 theorem declarations", "7 unlearning claim axes separated", "4 consumers pass", "12 mutations reject", "support effect none"],
        "claim_scope": "Bounded finite data/update custody, policy lease, weight custody, context transaction, and unlearning claim-axis semantics only.",
        "negative_controls": "validator_owned_twelve_cluster_denominator_disposition_semantic_axis_status_and_support_mutations",
        "negative_control_cases": ["module deletion", "semantic-field erasure", "target inflation", "theorem inflation", "behavior/influence merger", "storage/backup merger", "status reopening", "support laundering"],
        "prohibited_inference": "The audit proves no learning, forgetting, influence removal, privacy reduction, storage or backup erasure, legal compliance, rollback efficacy, deployment, support, release, or publication.",
        "semantic_review_state": "checked_terminal_bounded_learning_update_weight_context_and_unlearning_axis_semantics",
    },
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    scripts = {row["script"] for row in UNITS}
    value["units"] = [row for row in value["units"] if row.get("script") not in scripts]
    next_order = len(value["units"]) + 1
    for offset, spec in enumerate(UNITS):
        unit = {key: item for key, item in spec.items() if key != "artifacts"}
        unit.update({
            "id": f"{spec['script']}:{next_order + offset}",
            "order": next_order + offset,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "contract_precision": "exact_record_denominator_and_semantic_disposition_contract",
            "input_artifacts": spec["artifacts"] + [REGISTER],
        })
        value["units"].append(unit)
    required = list(value["required_artifacts"])
    for spec in UNITS:
        for artifact in spec["artifacts"] + [REGISTER]:
            if artifact not in required:
                required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered three P7.2-T2/P4-C4 validators: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
