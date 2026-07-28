#!/usr/bin/env python3
"""Register the terminal P6.9 raw-scaffold and proof/evidence handoff gates."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
UNITS = [
    {
        "script": "validate_p6_9_raw_scaffold_ownership_audit.py",
        "input_contract": (
            "The terminal W3 reader/raw split, every exact 12-token fingerprint at "
            "the current maximum raw-QMD spread, its complete chapter set, visibility, "
            "generation and structure state, owner, regeneration route, semantic "
            "purpose, and disposition."
        ),
        "input_artifacts": [
            "evidence_quality/p6_9_raw_scaffold_ownership_audit.json",
            "docs/p6_9_raw_scaffold_ownership_audit.md",
            "schemas/p6_9_raw_scaffold_ownership_audit.schema.json",
            "scripts/build_p6_9_raw_scaffold_ownership_audit.py",
            "scripts/validate_p6_9_raw_scaffold_ownership_audit.py",
            "scripts/register_p6_9_depth_exit_artifacts.py",
            "evidence_quality/p7_1a_w3_inheritance_guard.json",
            "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd",
        ],
        "output_contract": (
            "Classify every widest raw scaffold exactly, reject reader-visible or "
            "unowned repetition, and close only when every retained maximum-spread "
            "block is a generated source-reconciliation projection with an explicit "
            "owner and regeneration path."
        ),
        "output_assertions": [
            "twenty-one exact widest fingerprints classified",
            "twenty-one generated source-reconciliation fingerprints",
            "zero reader-visible widest fingerprints",
            "zero unjustified widest fingerprints",
            "copied reader-facing scaffold remains a rejecting negative control",
            "twelve mutations reject",
            "no support or release movement",
        ],
        "claim_scope": (
            "Raw-QMD scaffold ownership and the W3 reader/raw boundary only."
        ),
        "negative_controls": (
            "validator_owned_state_denominator_digest_identity_visibility_generation_"
            "ownership_exit_and_support_mutations_plus_copied_reader_scaffold"
        ),
        "negative_control_cases": [
            "active-state laundering",
            "raw denominator drift",
            "raw spread drift",
            "W3 digest drift",
            "fingerprint deletion",
            "fingerprint substitution",
            "chapter-set truncation",
            "reader-visibility laundering",
            "generated-state laundering",
            "owner erasure",
            "exit forgery",
            "support promotion",
            "copied reader-facing scaffold",
        ],
        "prohibited_inference": (
            "Generated-scaffold ownership does not establish manuscript truth, "
            "semantic quality, proof, empirical support, safety, deployment, release, "
            "SOTA, AGI, or ASI."
        ),
        "semantic_review_state": (
            "all_twenty_one_widest_fingerprints_exactly_classified_and_owned"
        ),
    },
    {
        "script": "validate_p6_9_proof_evidence_handoff.py",
        "input_contract": (
            "All 184 concept-complete records across twenty-three exact chapter "
            "digests, their exact atom and source identities, falsifiers, future "
            "evidence lanes and routes, maximum inferences, unresolved challenges, "
            "and terminal raw-scaffold and W3 bindings."
        ),
        "input_artifacts": [
            "evidence_quality/p6_9_proof_evidence_handoff.json",
            "docs/p6_9_proof_evidence_handoff.md",
            "schemas/p6_9_proof_evidence_handoff.schema.json",
            "scripts/build_p6_9_proof_evidence_handoff.py",
            "scripts/validate_p6_9_proof_evidence_handoff.py",
            "scripts/register_p6_9_depth_exit_artifacts.py",
            "evidence_quality/chapter_substance_contract.json",
            "evidence_quality/p6_9_raw_scaffold_ownership_audit.json",
            "evidence_quality/p7_1a_w3_inheritance_guard.json",
        ],
        "output_contract": (
            "Hand every concept from editorial completion to later proof/evidence "
            "work without losing chapter, concept, atom, source, falsifier, evidence "
            "lane, inference ceiling, or unresolved-challenge identity, and without "
            "claiming that the handoff itself supplies evidence."
        ),
        "output_assertions": [
            "twenty-three exact chapter digests",
            "184 exact concept identities",
            "184 source-bearing concept records",
            "184 atom-bearing concept records",
            "184 falsifier-bearing concept records",
            "184 evidence-lane-bearing concept records",
            "184 maximum-inference-bearing concept records",
            "184 unresolved-challenge-bearing concept records",
            "zero missing handoff identities",
            "fourteen mutations reject",
            "no support or release movement",
        ],
        "claim_scope": (
            "Editorial-to-proof/evidence identity transfer for the terminal P6.9 "
            "concept-completion tranche only."
        ),
        "negative_controls": (
            "validator_owned_state_digest_denominator_source_atom_falsifier_lane_"
            "inference_challenge_exit_and_support_mutations"
        ),
        "negative_control_cases": [
            "active-state laundering",
            "chapter-substance digest drift",
            "raw-audit digest drift",
            "W3 digest drift",
            "chapter deletion",
            "concept deletion",
            "source identity deletion",
            "atom identity deletion",
            "falsifier deletion",
            "evidence-lane deletion",
            "maximum-inference deletion",
            "unresolved-challenge deletion",
            "raw-exit bypass",
            "support promotion",
        ],
        "prohibited_inference": (
            "A complete handoff is not proof, empirical evidence, formal evidence, "
            "safety, deployment, release authority, SOTA, AGI, or ASI."
        ),
        "semantic_review_state": (
            "all_184_concepts_exactly_handed_off_at_current_reviewed_digests"
        ),
    },
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    scripts = {spec["script"] for spec in UNITS}
    registry["units"] = [
        unit for unit in registry["units"] if unit.get("script") not in scripts
    ]
    used = {unit["order"] for unit in registry["units"]}
    next_order = max(used, default=0) + 1
    for spec in UNITS:
        while next_order in used:
            next_order += 1
        artifacts = spec["input_artifacts"]
        registry["units"].append(
            {
                "id": f"{spec['script']}:{next_order}",
                "order": next_order,
                "script": spec["script"],
                "args": [],
                "execution_tier": "pr",
                "validation_class": "proof_or_evidence_gate",
                "input_contract": spec["input_contract"],
                "input_artifacts": artifacts,
                "output_contract": spec["output_contract"],
                "output_assertions": spec["output_assertions"],
                "claim_scope": spec["claim_scope"],
                "negative_controls": spec["negative_controls"],
                "negative_control_cases": spec["negative_control_cases"],
                "prohibited_inference": spec["prohibited_inference"],
                "contract_precision": "exact",
                "semantic_review_state": spec["semantic_review_state"],
            }
        )
        used.add(next_order)
        for artifact in artifacts:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
        next_order += 1
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        "Registered P6.9 terminal depth exits: "
        f"{registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
