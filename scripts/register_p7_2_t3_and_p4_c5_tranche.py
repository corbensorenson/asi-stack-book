#!/usr/bin/env python3
"""Register the terminal P7.2-T3 reader packet and P4-C5 semantic audit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
REGISTER = "scripts/register_p7_2_t3_and_p4_c5_tranche.py"

UNITS = [
    {
        "script": "validate_human_oversight_control_contract.py",
        "artifacts": [
            "scripts/validate_human_oversight_control_contract.py",
            "schemas/human_oversight_control_packet.schema.json",
            "tests/fixtures/protocol_records/human_oversight_control_packet.valid.json",
            "experiments/human_factors_argument_exit/preregistration.json",
            "lean/AsiStackProofs/HumanFactorsOversight.lean",
            "lean/AsiStackProofs.lean",
            "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
        ],
        "input_contract": "One typed safe-hold record-shape fixture with zero human observations, a prospectively frozen but unexecuted four-arm minimal-risk human-factors campaign, and a finite necessary-condition/responsibility/non-authority model.",
        "output_contract": "Require exact task, evidence, workload, time, authority, intervention, conflict, privacy, responsibility, and lifecycle custody; ethics/privacy authority before recruitment; nine competence gates; six rescue steps; an N3 exact ceiling; nine Lean declarations; and fifteen rejecting mutations.",
        "output_assertions": ["1 safe-hold no-human fixture", "4 matched arms", "9 competence gates", "5 positive controls", "7 adversarial controls", "9 Lean declarations", "15 mutations reject", "support/effect/release authority none"],
        "claim_scope": "Human control-envelope packet shape, campaign custody, and finite necessary-condition/responsibility-route semantics only.",
        "negative_controls": "validator_owned_fifteen_authority_responsibility_privacy_surveillance_participant_outcome_competence_scope_and_isolation_mutations",
        "negative_control_cases": ["effect authorization", "support grant", "responsibility laundering", "punitive inference", "biometric inference", "participant invention", "outcome opening", "ethics deletion", "surveillance enablement", "negative-scope inflation", "P2 displacement"],
        "prohibited_inference": "The fixture, theorem, and protocol do not establish comprehension, workload calibration, consent, privacy adequacy, moral responsibility, intervention efficacy, meaningful control, safety, support, release, publication, AGI, or ASI.",
        "semantic_review_state": "checked_human_control_envelope_responsibility_privacy_and_non_authority_semantics",
    },
    {
        "script": "validate_p7_2_t3_human_factors_reader_integration.py",
        "artifacts": [
            "scripts/validate_p7_2_t3_human_factors_reader_integration.py",
            "evidence_quality/p7_2_t3_human_factors_reader_integration.json",
            "docs/p7_2_t3_human_factors_reader_integration.md",
            "book_structure.json", "sources/source_inventory.json", "proofs/proof_manifest.json",
            "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
            "index.qmd", "appendices/B_glossary.qmd", "appendices/C_claim_evidence_matrix.qmd",
            "appendices/G_corben_source_corpus.qmd", "appendices/H_external_sources.qmd",
            "chapters/human-intent-as-a-formal-input.qmd",
            "chapters/constitutional-alignment-substrate.qmd",
            "chapters/integrated-reference-architecture.qmd",
        ],
        "input_contract": "The admitted Human Factors chapter, ten exact source mappings, two implemented public proof targets, a no-human safe-hold fixture, a closed ethics-gated campaign, and adjacent reader surfaces.",
        "output_contract": "Bind artifact digests, preserve source/role/proof/participant denominators, require handoffs and synthesis surfaces, keep recruitment and protected outcomes closed, and reject thirteen integration mutations.",
        "output_assertions": ["1 terminal argument-level chapter", "10 source mappings", "2 implemented proof targets", "9 Lean declarations", "4 claim-bearing arms", "0 participants", "13 integration mutations reject", "support effect none"],
        "claim_scope": "P7.2-T3 chapter necessity, argument-level integration, traceability, ethics boundary, and reader continuity only.",
        "negative_controls": "validator_owned_thirteen_manifest_source_digest_proof_participant_outcome_isolation_role_status_and_support_mutations",
        "negative_control_cases": ["terminal removal", "source deletion", "digest drift", "proof reduction", "participant invention", "outcome opening", "P2 displacement", "review substitution", "role deletion", "status reopening", "support laundering"],
        "prohibited_inference": "Terminal reader integration does not establish human comprehension, workload, trust, control efficacy, responsibility, privacy, meaningful control, safety, empirical support, release, publication, AGI, or ASI.",
        "semantic_review_state": "checked_terminal_human_factors_argument_chapter_integration",
    },
    {
        "script": "validate_p4_c5_semantic_proof_cluster.py",
        "artifacts": [
            "scripts/validate_p4_c5_semantic_proof_cluster.py",
            "proofs/semantic_cluster_audits/self_improvement_and_readiness.json",
            "docs/p4_c5_self_improvement_and_readiness_semantic_audit.md",
            "lean/AsiStackProofs/SelfImprovementRefinement.lean",
            "lean/AsiStackProofs/OpenEndedImprovementRefinement.lean",
            "lean/AsiStackProofs/ReadinessRefinement.lean",
            "lean/AsiStackProofs/CapabilityThresholdRefinement.lean",
            "chapters/recursive-self-improvement-boundaries.qmd",
            "chapters/open-ended-improvement-engines.qmd",
            "chapters/readiness-gates-residual-escrow-and-quarantine.qmd",
            "chapters/capability-thresholds-and-deployment-commitments.qmd",
        ],
        "input_contract": "A frozen four-module self-improvement/open-ended/readiness/threshold cluster with 21 public targets and 36 theorem declarations.",
        "output_contract": "Require exact propositions, modeled state, assumptions, countermodels, consumers, mutation evidence, semantic separations, and ceilings; execute four consumers and reject twelve audit mutations.",
        "output_assertions": ["4 adequate modules", "21 public targets", "36 theorem declarations", "6 semantic separations", "4 consumers pass", "12 mutations reject", "support effect none"],
        "claim_scope": "Bounded finite proposal, campaign, threshold, readiness, quarantine, invalidation, handoff, and readmission semantics only.",
        "negative_controls": "validator_owned_twelve_cluster_denominator_disposition_semantic_separation_status_and_support_mutations",
        "negative_control_cases": ["module deletion", "semantic-field erasure", "target inflation", "theorem inflation", "proposal/improvement merger", "assessment/crossing merger", "status reopening", "support laundering"],
        "prohibited_inference": "The audit proves no legitimate objective, adaptive or open-ended improvement, capability threshold, effective safeguard or rollback, readiness, safety, deployment, transfer, support, release, or publication.",
        "semantic_review_state": "checked_terminal_bounded_self_improvement_campaign_threshold_and_readiness_semantics",
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
    print(f"Registered three P7.2-T3/P4-C5 validators: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
