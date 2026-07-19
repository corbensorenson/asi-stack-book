#!/usr/bin/env python3
"""Register the terminal P7.2-T1 reader packet and P4-C3 semantic audit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
REGISTER = "scripts/register_p7_2_t1_and_p4_c3_tranche.py"

UNITS = [
    {
        "script": "validate_white_box_evidence_contract.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_white_box_evidence_contract.py",
            "schemas/white_box_evidence_packet.schema.json",
            "tests/fixtures/protocol_records/white_box_evidence_packet.valid.json",
            "experiments/white_box_argument_exit/preregistration.json",
            "lean/AsiStackProofs/WhiteBoxEvidence.lean",
            "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
        ],
        "input_contract": "One typed record-shape fixture, a prospectively frozen but unexecuted two-method white-box campaign, and a finite admission/non-authority model.",
        "output_contract": "Require exact model/method identity, controls, stability, residuals, expiry, non-authority, protected outcome closure, seven competence gates, and an N3 exact ceiling; compile eight Lean declarations and reject twelve semantic mutations.",
        "output_assertions": ["1 record-shape fixture", "2 independently owned method families", "7 competence gates", "8 Lean declarations", "12 mutations reject", "empirical and support effects none"],
        "claim_scope": "White-box packet shape, campaign custody, and finite governance-route semantics only.",
        "negative_controls": "validator_owned_twelve_identity_control_custody_authority_and_support_mutations",
        "negative_control_cases": ["release grant", "authority widening", "completeness claim", "control deletion", "outcome opening", "negative-scope inflation", "P2 displacement", "support laundering"],
        "prohibited_inference": "The fixture and protocol do not establish any feature, circuit, interpretation, causal result, governance efficacy, support transition, release, AGI, or ASI claim.",
        "contract_precision": "exact_record_protocol_and_finite_route_contract",
        "semantic_review_state": "checked_white_box_record_custody_and_non_authority_semantics",
    },
    {
        "script": "validate_p7_2_t1_white_box_reader_integration.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p7_2_t1_white_box_reader_integration.py",
            "evidence_quality/p7_2_t1_white_box_reader_integration.json",
            "docs/p7_2_t1_white_box_reader_integration.md",
            "book_structure.json",
            "sources/source_inventory.json",
            "proofs/proof_manifest.json",
            "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
            "index.qmd",
            "docs/book_outline.md",
            "appendices/B_glossary.qmd",
            "appendices/C_claim_evidence_matrix.qmd",
            "appendices/G_corben_source_corpus.qmd",
            "appendices/H_external_sources.qmd",
            "chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd",
            "chapters/capability-thresholds-and-deployment-commitments.qmd",
            "chapters/integrated-reference-architecture.qmd",
        ],
        "input_contract": "The admitted white-box chapter, eight exact source mappings, two implemented public proof targets, a closed protected campaign, and all adjacent reader surfaces.",
        "output_contract": "Bind artifact digests, preserve source/role/proof denominators, require both handoffs and synthesis surfaces, keep protected outcomes closed, and reject twelve integration mutations.",
        "output_assertions": ["1 terminal argument-level chapter", "8 source mappings", "2 implemented proof targets", "8 Lean declarations", "12 integration mutations reject", "support effect none"],
        "claim_scope": "P7.2-T1 chapter necessity, argument-level integration, traceability, and reader continuity only.",
        "negative_controls": "validator_owned_twelve_manifest_source_digest_proof_custody_role_and_support_mutations",
        "negative_control_cases": ["chapter deletion", "source-target deletion", "digest drift", "proof-count reduction", "outcome opening", "P2 displacement", "role deletion", "support laundering"],
        "prohibited_inference": "Terminal reader integration does not establish an interpretability result, mechanism completeness, empirical support, release, publication, AGI, or ASI.",
        "contract_precision": "digest_bound_reader_and_evidence_custody",
        "semantic_review_state": "checked_terminal_white_box_argument_chapter_integration",
    },
    {
        "script": "validate_p4_c3_semantic_proof_cluster.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p4_c3_semantic_proof_cluster.py",
            "proofs/semantic_cluster_audits/authority_effect_rollback_and_corrigibility.json",
            "docs/p4_c3_authority_effect_rollback_and_corrigibility_semantic_audit.md",
            "lean/AsiStackProofs/AuthorityEffectRefinement.lean",
            "lean/AsiStackProofs/Replacement.lean",
            "lean/AsiStackProofs/Corrigibility.lean",
            "lean/AsiStackProofs/IntentExecutionRefinement.lean",
            "chapters/system-boundaries-and-authority.qmd",
            "chapters/capability-replacement-and-rollback.qmd",
            "chapters/constitutional-alignment-substrate.qmd",
            "chapters/intent-to-execution-contracts.qmd",
        ],
        "input_contract": "A frozen four-module authority/effect/replacement/corrigibility/intent-execution cluster with eleven public targets and sixty-five theorem declarations.",
        "output_contract": "Require exact propositions, modeled state, assumptions, countermodels, consumers, mutation evidence, and ceilings; preserve three adequate dispositions and one countermodel-only reclassification; execute six consumers and reject ten mutations.",
        "output_assertions": ["4 modules", "11 public targets", "65 theorem declarations", "3 adequate and 1 reclassified", "6 consumers pass", "10 mutations reject", "support effect none"],
        "claim_scope": "Bounded finite authority-to-effect, replacement, corrigibility-countermodel, and intent-execution semantics only.",
        "negative_controls": "validator_owned_ten_cluster_denominator_disposition_semantic_status_and_support_mutations",
        "negative_control_cases": ["module deletion", "corrigibility inflation", "semantic-field erasure", "target inflation", "theorem inflation", "status reopening", "support laundering"],
        "prohibited_inference": "The audit proves no identity or receipt authentic, effect inventory complete, rollback effective, monitor valid, deployment safe, support transition, release, or publication.",
        "contract_precision": "exact_module_target_theorem_and_semantic_disposition",
        "semantic_review_state": "checked_terminal_bounded_authority_effect_replacement_and_corrigibility_semantics",
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
    print(f"Registered three P7.2/P4-C3 validators: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
