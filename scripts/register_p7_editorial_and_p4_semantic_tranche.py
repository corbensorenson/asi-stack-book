#!/usr/bin/env python3
"""Register the terminal P7.1a and first two P4 semantic-audit packets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
REGISTER = "scripts/register_p7_editorial_and_p4_semantic_tranche.py"

UNITS = [
    {
        "script": "validate_p7_1a_w1_editorial_boundary_audit.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p7_1a_w1_editorial_boundary_audit.py",
            "scripts/reconcile_p7_chapter_evidence.py",
            "evidence_quality/p7_1a_w1_editorial_boundary_audit.json",
            "docs/p7_1a_w1_editorial_boundary_audit.md",
            "chapters/living-book-methodology.qmd",
        ],
        "input_contract": "Activation-era 55-chapter compact evidence packets, immutable terminal atom custody, one declared baseline tokenizer, two bounded boundary additions, and consolidation-provenance repairs.",
        "output_contract": "Recompute baseline/final repetition, preserve all 3,745 protected atoms and packet fields, bind the compact digest, and reject deletion, source, support, or provenance drift.",
        "output_assertions": ["55 chapter packets", "3,745 protected atoms", "1,142 to 727 repeated 12-grams", "8 mutations reject", "support effect none"],
        "claim_scope": "P7.1a-W1 editorial and evidence-boundary custody only.",
        "negative_controls": "validator_owned_eight_packet_source_provenance_and_support_mutations",
        "negative_control_cases": ["packet field deletion", "source-boundary erasure", "atom-denominator drift", "support laundering"],
        "prohibited_inference": "Compression and boundary coverage do not establish chapter truth, empirical support, release, or publication.",
        "contract_precision": "exact_packet_digest_and_recomputed_baseline",
        "semantic_review_state": "checked_terminal_editorial_boundary_semantics",
    },
    {
        "script": "validate_p7_1a_w2_narrative_audit.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p7_1a_w2_narrative_audit.py",
            "evidence_quality/p7_1a_w2_narrative_audit.json",
            "docs/p7_1a_w2_narrative_audit.md",
            "index.qmd",
            "docs/book_outline.md",
            "chapters/asi-is-a-stack-not-a-model.qmd",
            "chapters/the-efficient-asi-hypothesis.qmd",
            "chapters/failure-modes-of-ungoverned-intelligence.qmd",
        ],
        "input_contract": "Commit-bound 59-chapter prose baseline, six frozen opening phrase families, exact role partition, three depth-leveling chapters, overview/handoff surfaces, and protected meaning/evidence custody.",
        "output_contract": "Reduce the frozen opening families from eight occurrences to zero, classify every manifest chapter once, require substantive central-argument additions, preserve claims/sources/equations/proof tags/protocol refs/support, and reject nine mutations.",
        "output_assertions": ["59 chapters classified once", "11 thesis, 30 reference, 7 implementation, 11 speculative/deferred", "8 opening formulas to 0", "710/728/664 token additions", "9 mutations reject", "support effect none"],
        "claim_scope": "P7.1a-W2 case-independent narrative quality and meaning preservation only.",
        "negative_controls": "validator_owned_nine_role_opening_depth_meaning_overview_and_support_mutations",
        "negative_control_cases": ["role omission or duplication", "formula restoration", "depth heading erasure", "claim or source deletion", "support laundering", "flagship precommitment"],
        "prohibited_inference": "Reader roles and deeper argument do not establish empirical or formal support, flagship evidence, release, or publication.",
        "contract_precision": "exact_commit_bound_meaning_preservation",
        "semantic_review_state": "checked_terminal_narrative_role_depth_and_handoff_semantics",
    },
    {
        "script": "validate_p4_c1_semantic_proof_cluster.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p4_c1_semantic_proof_cluster.py",
            "proofs/semantic_cluster_audits/evidence_claim_and_proof_custody.json",
            "docs/p4_c1_evidence_claim_and_proof_custody_semantic_audit.md",
        ],
        "input_contract": "Frozen evidence/claim/proof-custody cluster of four modules and sixteen public targets with exact propositions, assumptions, countermodels, consumers, and inference ceilings.",
        "output_contract": "Require one terminal disposition per module, execute six consumers, preserve target/theorem denominators and chapter ceilings, and reject nine semantic-cluster mutations.",
        "output_assertions": ["4 modules", "16 public targets", "2 adequate and 2 reclassified", "6 consumers pass", "9 mutations reject", "support effect none"],
        "claim_scope": "Bounded finite evidence, claim-ledger, proof-carrying-claim, and proof-envelope semantics only.",
        "negative_controls": "validator_owned_nine_cluster_denominator_disposition_semantic_and_support_mutations",
        "negative_control_cases": ["module deletion", "invented disposition", "semantic-field erasure", "target inflation", "support laundering", "status reopening"],
        "prohibited_inference": "The cluster does not prove evidence or claim truth, verifier soundness, runtime enforcement, empirical behavior, safety, or support movement.",
        "contract_precision": "exact_module_target_and_semantic_disposition",
        "semantic_review_state": "checked_terminal_bounded_evidence_claim_and_proof_custody_semantics",
    },
    {
        "script": "validate_p4_c2_semantic_proof_cluster.py",
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "artifacts": [
            "scripts/validate_p4_c2_semantic_proof_cluster.py",
            "proofs/semantic_cluster_audits/safety_assurance_and_oversight.json",
            "docs/p4_c2_safety_assurance_and_oversight_semantic_audit.md",
            "lean/AsiStackProofs/SafetyCriticalLifecycle.lean",
            "lean/AsiStackProofs/SafetyCaseRefinement.lean",
            "lean/AsiStackProofs/ScalableOversightRefinement.lean",
            "lean/AsiStackProofs/AdversarialEvaluationRefinement.lean",
        ],
        "input_contract": "Frozen safety/assurance/oversight cluster of four modules and thirty-one public targets with exact propositions, modeled state, assumptions, countermodels, consumers, mutation evidence, and maximum inference.",
        "output_contract": "Require four terminal bounded dispositions, execute five independent consumers, preserve target/theorem denominators and chapter limitation surfaces, and reject nine semantic-cluster mutations.",
        "output_assertions": ["4 modules", "31 public targets", "4 adequate bounded dispositions", "5 consumers pass", "9 mutations reject", "support effect none"],
        "claim_scope": "Bounded finite safety-critical, safety-case, oversight, and adversarial-evaluation lifecycle semantics only.",
        "negative_controls": "validator_owned_nine_cluster_denominator_disposition_semantic_and_support_mutations",
        "negative_control_cases": ["module deletion", "invented disposition", "semantic-field erasure", "target inflation", "support laundering", "status reopening"],
        "prohibited_inference": "The cluster does not prove protected predicates sufficient, safety cases valid, reviewers independent, deception detected, controls effective, deployment safe, or support moved.",
        "contract_precision": "exact_module_target_and_semantic_disposition",
        "semantic_review_state": "checked_terminal_bounded_safety_assurance_and_oversight_semantics",
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
    print(f"Registered four P7/P4 terminal validators: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
