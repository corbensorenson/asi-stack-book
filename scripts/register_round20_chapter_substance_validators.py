#!/usr/bin/env python3
"""Register the Round 20 atom-custody and chapter-substance validators."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
UNITS = [
    {
        "script": "validate_round20_four_chapter_claim_atom_addendum.py",
        "input_contract": (
            "The exact four current-manifest chapters not covered by the frozen base "
            "registry or prior addenda; five bounded manuscript-responsibility atoms per "
            "chapter; immutable prior atom custody."
        ),
        "input_artifacts": [
            "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
            "schemas/round20_four_chapter_claim_atom_addendum.schema.json",
            "scripts/build_round20_four_chapter_claim_atom_addendum.py",
            "scripts/validate_round20_four_chapter_claim_atom_addendum.py",
            "scripts/register_round20_chapter_substance_validators.py",
            "book_structure.json",
        ],
        "output_contract": (
            "Keep one core, boundary, mechanism, failure-boundary, and argument-exit "
            "atom for each of the four exact owners without rewriting historical packets "
            "or moving support."
        ),
        "output_assertions": [
            "four exact manifest owners",
            "twenty bounded atoms",
            "five distinct roles per owner",
            "zero support or release movement",
            "eight mutations reject",
        ],
        "negative_controls": "validator_owned_eight_identity_role_scope_and_support_mutations",
        "negative_control_cases": [
            "chapter deletion",
            "atom deletion",
            "duplicate atom identity",
            "wrong owner",
            "role denominator drift",
            "falsifier deletion",
            "support promotion",
            "release movement",
        ],
        "claim_scope": (
            "Append-only manuscript responsibility, ownership, falsification boundaries, "
            "and evidence routing for four chapters."
        ),
        "prohibited_inference": (
            "Atom coverage is not claim truth, proof, empirical evidence, implementation "
            "evidence, safety, release authority, SOTA, AGI, or ASI."
        ),
        "semantic_review_state": "manual_four_owner_core_boundary_mechanism_failure_and_exit_review",
    },
    {
        "script": "validate_chapter_substance_contract.py",
        "input_contract": (
            "The exact frozen 84-chapter manifest, the complete append-only atom-source "
            "set, current chapter text, named concept contracts, and static digest-bound "
            "semantic dispositions for the Round 21-hardened prose-repair tranche."
        ),
        "input_artifacts": [
            "evidence_quality/chapter_substance_contract.json",
            "schemas/chapter_substance_contract.schema.json",
            "scripts/build_chapter_substance_contract.py",
            "scripts/validate_chapter_substance_contract.py",
            "scripts/register_round20_chapter_substance_validators.py",
            "evidence_quality/claim_atom_registry.json",
            "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
            "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
            "evidence_quality/taxonomy_completion_claim_atoms_2026_07_24.json",
            "evidence_quality/round_18_breadth_completion_claim_atoms.json",
            "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
            "book_structure.json",
        ],
        "output_contract": (
            "Preserve 84/84 atom ownership and require every active named concept section "
            "to carry a mechanism, failure mode, explicit non-claim, declared-source "
            "engagement, minimum substantive span, and an exact-digest semantic review "
            "while keeping raw word count and atom counts diagnostic."
        ),
        "output_assertions": [
            "manifest frozen at 84 chapters",
            "84 of 84 chapters have an exact atom source",
            "24 of 24 active priority concepts pass",
            "three of three semantic reviews bind the current chapter digests",
            "word count remains independent from concept completion",
            "atom-count parity is not an acceptance target",
            "twelve mutations reject",
            "one low-word-count concept-completion positive control passes",
        ],
        "negative_controls": "validator_owned_twelve_rejecting_mutations_plus_one_word_independence_positive_control",
        "negative_control_cases": [
            "chapter deletion",
            "manifest freeze widening",
            "word trigger weakening",
            "atom source deletion",
            "concept deletion",
            "concept word laundering",
            "source grounding deletion",
            "semantic review deletion",
            "semantic review digest drift",
            "manual review bypass",
            "chapter growth authorization",
            "support promotion",
        ],
        "claim_scope": (
            "Editorial chapter substance, named-concept fidelity, and atom custody only."
        ),
        "prohibited_inference": (
            "Passing structure, labels, or word counts does not establish semantic quality, "
            "claim truth, empirical support, proof, safety, release, SOTA, AGI, or ASI."
        ),
        "semantic_review_state": "three_current_digest_bound_reviews_and_remaining_twenty_owner_reviews_required",
    },
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    scripts = {spec["script"] for spec in UNITS}
    registry["units"] = [
        unit for unit in registry["units"] if unit.get("script") not in scripts
    ]
    used = {unit["order"] for unit in registry["units"]}
    next_order = 1
    for spec in UNITS:
        while next_order in used:
            next_order += 1
        artifacts = spec.pop("input_artifacts")
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
        "Registered Round 20 validators: "
        f"{registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
