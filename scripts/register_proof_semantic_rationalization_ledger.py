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
    "lean/AsiStackProofs/BibliographyPlan.lean",
    "lean/AsiStackProofs/BenchmarkRatchets.lean",
    "lean/AsiStackProofs/StableCapabilityFields.lean",
    "lean/AsiStackProofs/RuntimeAdapters.lean",
    "lean/AsiStackProofs/SearchSubstrates.lean",
    "lean/AsiStackProofs/ArtifactStewardAgents.lean",
    "scripts/validate_runtime_adapter_adversarial_boundary_probe.py",
    "scripts/validate_substrate_adoption_trace.py",
    "scripts/validate_artifact_steward_lifecycle_probe.py",
    "experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json",
    "experiments/substrate_adoption_trace/results/2026-07-02-local.json",
    "experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json",
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
            "One immutable 1,370-theorem baseline; thirty-eight exact, ordered transactions; "
            "the baseline Scalable Oversight, Bibliography Plan, Benchmark Ratchets, and "
            "Policy Optimization, Stable Capability Fields, Evidence States, and Runtime "
            "Adapters, Search Substrates, and Artifact Steward Agents modules; one same-model normalized duplicate "
            "pair; thirty-seven premise-restating projections, fifteen with derived "
            "replacements, twenty retired after public-target narrowing, one unused projection retired without target "
            "change, and one summary projection retired after route-family validator rebinding; "
            "the current overlay; frozen historical registry; and reconciled target, "
            "roadmap, and status surfaces."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require immutable baseline and theorem-block digests, exact same-model "
            "statement identity for the duplicate, dependency-and-consumer-safe removals, "
            "four counterexample, four decision-model, and ten scope-narrowing target "
            "migrations, retained or honestly replanned target ownership, a 1,332-theorem "
            "current estate, an exact 123-action remaining "
            "queue, meta-audit exclusion from implementation binding, and no support or "
            "release effect."
        ),
        "output_assertions": [
            "baseline commit and artifact digests exact",
            "retired and retained declarations share one authored model",
            "normalized theorem statements exact",
            "retired theorem has no theorem consumer",
            "thirty-eight retired declarations absent, sixteen replacement-bound retirements, and twenty-two intentionally null replacements",
            "two bibliography targets migrated to derived counterexample gates",
            "two benchmark targets migrated to derived decision-model gates",
            "two Stable Capability Fields targets narrowed to retained derived routes",
            "five Evidence States targets narrowed to planned reachable or independently implemented models",
            "Runtime adapter validator bound to fifteen route theorems rather than a summary projection",
            "Search Substrates targets bound to two finite counterexamples and one honestly planned reachable route model",
            "Artifact Steward targets bound to two retained lifecycle routes and two honestly planned reachable models",
            "proof-custody meta-audit does not inflate semantic implementation depth",
            "1,332 current theorem declarations",
            "123 rewrite-or-retire actions remain",
            "frozen 1,151-theorem and 298-target registry preserved",
            "14 mutations reject",
            "no support or release effect",
        ],
        "claim_scope": (
            "Thirty-eight dependency-safe declaration retirements: one exact same-model "
            "duplicate and thirty-seven premise-restating projections. Eighteen public "
            "targets migrate to counterexample, decision-model, narrower retained-route, "
            "or honestly planned stronger-model wording; the runtime-adapter target remains "
            "implemented through its fifteen explicit route theorems."
        ),
        "negative_controls": (
            "validator_owned_fourteen_baseline_digest_sequence_identity_statement_dependency_"
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
            "remaining denominator inflation",
            "support promotion",
        ],
        "prohibited_inference": (
            "This transaction does not strengthen the retained finite-model theorem or "
            "establish reviewer competence, implementation correctness, useful oversight, "
            "deployment, transfer, safety, SOTA, AGI, ASI, or claim support."
        ),
        "contract_precision": "exact_immutable_cumulative_dependency_safe_retirement_ledger",
        "semantic_review_state": "checked_thirty_eight_c6_retirements_and_eighteen_target_migrations",
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
