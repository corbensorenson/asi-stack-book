#!/usr/bin/env python3
"""Generate non-aggregating evidence-quality vectors for all chapter-core claims."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "evidence_quality" / "vector_policy.json"
DISPOSITIONS = ROOT / "claim_decisions" / "v1_x_core_claim_dispositions.json"
OUTPUT = ROOT / "evidence_quality" / "core_claim_vectors.json"
POST_V2_1_DISPOSITIONS = ROOT / "claim_decisions" / "post_v2_1_empirical_dispositions.json"
QCSA_DISPOSITIONS = ROOT / "claim_decisions" / "qcsa_reference_evaluation_dispositions.json"
QCSA_CORE_CLAIMS = {
    "cognitive-compilation-and-semantic-ir.core",
    "virtual-context-abi.core",
    "claim-ledgers-and-belief-revision.core",
    "runtime-adapters-tool-permissions-and-human-approval.core",
    "inter-stack-protocols-identity-and-economic-exchange.core",
    "routing-heads-and-specialist-cores.core",
    "compact-generative-systems-and-residual-honesty.core",
    "data-engines-continual-learning-and-unlearning.core",
    "integrated-reference-architecture.core",
}
QCSA_REFS = [
    "experiments/qcsa_reference/results/evaluation_results.json",
    "claim_decisions/qcsa_reference_evaluation_dispositions.json",
    "docs/qcsa_reference_evaluation_report.md",
    "experiments/qcsa_vertical_reference/results/vertical_result.json",
    "docs/qcsa_governed_vertical_reference_report.md",
]
SNAPSHOT_DATE = "2026-07-13"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dimension(state: str, rationale: str, refs: list[str], residual: str) -> dict[str, Any]:
    return {"state": state, "rationale": rationale, "evidence_refs": refs, "residuals": [residual]}


def build_registry() -> dict[str, Any]:
    policy = load(POLICY)
    dispositions = load(DISPOSITIONS)
    post_v2_1 = load(POST_V2_1_DISPOSITIONS) if POST_V2_1_DISPOSITIONS.exists() else {"decisions": []}
    post_v2_1_by_claim = {row["claim_id"]: row for row in post_v2_1.get("decisions", [])}
    qcsa_dispositions = load(QCSA_DISPOSITIONS) if QCSA_DISPOSITIONS.exists() else {"core_claim_decisions": []}
    qcsa_by_claim = {row["claim_id"]: row for row in qcsa_dispositions.get("core_claim_decisions", [])}
    vectors: list[dict[str, Any]] = []
    for row in dispositions["dispositions"]:
        claim_id = row["claim_id"]
        chapter_file = row["chapter_file"]
        transition_refs = list(row.get("relevant_non_core_transition_refs", []))
        post_v2_1_row = post_v2_1_by_claim.get(claim_id)
        if post_v2_1_row:
            transition_refs.extend(ref for ref in post_v2_1_row.get("transition_refs", []) if ref not in transition_refs)
        qcsa_row = qcsa_by_claim.get(claim_id) if claim_id in QCSA_CORE_CLAIMS else None
        if qcsa_row:
            transition_refs.extend(ref for ref in QCSA_REFS if ref not in transition_refs)
        adjacent = bool(transition_refs)
        common_refs = [chapter_file, "appendices/C_claim_evidence_matrix.qmd", str(DISPOSITIONS.relative_to(ROOT))]
        if post_v2_1_row:
            common_refs.append(str(POST_V2_1_DISPOSITIONS.relative_to(ROOT)))
        if qcsa_row:
            common_refs.append(str(QCSA_DISPOSITIONS.relative_to(ROOT)))
        vector = {
            "vector_id": f"{claim_id}.quality.{SNAPSHOT_DATE}",
            "claim_id": claim_id,
            "chapter_id": row["chapter_id"],
            "chapter_file": chapter_file,
            "summary_support_state": row["current_support_state"],
            "summary_source": str(DISPOSITIONS.relative_to(ROOT)),
            "dimensions": {
                "independence": dimension(
                    "internal_only",
                    "The book, mappings, checks, and disposition were produced inside the author/AI project; no accepted independent human review is recorded.",
                    ["docs/external_review_status.md", *common_refs],
                    "Shared project incentives and correlated review remain unresolved.",
                ),
                "reproducibility": dimension(
                    "adjacent_local_replay" if adjacent else "not_demonstrated_for_claim",
                    "Related non-core records have local replay references, but they do not reproduce this broad chapter-core claim." if adjacent else "No accepted replay directly reproduces this chapter-core architectural claim.",
                    [*transition_refs, *common_refs],
                    "Direct independent reproduction of the claim-bounded result is absent.",
                ),
                "recency": dimension(
                    "repository_snapshot_current",
                    f"The vector and active disposition were regenerated for the {SNAPSHOT_DATE} repository snapshot.",
                    common_refs,
                    "Repository freshness does not establish empirical recency or protect against future drift.",
                ),
                "coverage": dimension(
                    "claim_scope_unmeasured",
                    (
                        "The bounded QCSA package, synthetic evaluation, and vertical trace exercise a related mechanism, "
                        "but their hand-authored template scope does not cover the broad chapter-core claim population."
                        if qcsa_row
                        else f"The recorded lane is {row.get('primary_evidence_lane', 'unspecified')}; current artifacts do not cover the broad chapter-core claim population."
                    ),
                    [*transition_refs, *common_refs],
                    (
                        f"{qcsa_row['basis']} Natural workloads, learned models, and broader mechanism-specific coverage remain open."
                        if qcsa_row
                        else row.get("promotion_burden", "Claim-bounded coverage remains open.")
                    ),
                ),
                "adversarial_strength": dimension(
                    "adjacent_bounded_controls" if adjacent else "not_demonstrated_for_claim",
                    "Related narrow records include bounded controls, but no accepted attack directly validates the chapter-core claim." if adjacent else "No accepted adversarial program directly tests the chapter-core claim.",
                    [*transition_refs, *common_refs],
                    "Adaptive and independent claim-bounded red-team evidence is absent.",
                ),
                "validity": dimension(
                    "not_independently_assessed",
                    (
                        "The QCSA observer is separately implemented but internally authored; synthetic labels and validators do not establish that the artifacts measure or prove the broad construct expressed by the core claim."
                        if qcsa_row
                        else "Internal mappings and validators do not establish that available artifacts measure or prove the construct expressed by the core claim."
                    ),
                    [*transition_refs, *common_refs],
                    "Construct and criterion validity require independent, claim-specific assessment; QCSA's internal separation is not external independence.",
                ),
                "artifact_access": dimension(
                    "public_claim_records_partial_evidence",
                    "The chapter, Appendix C row, disposition, and public-safe references are accessible, while complete claim-bounded evidence is not available because it has not been produced.",
                    common_refs,
                    "Public metadata and partial artifacts are not a complete reproducibility bundle.",
                ),
                "transfer_distance": dimension(
                    "not_established",
                    (
                        "The bounded QCSA result and one temporary-effect vertical replay do not establish transfer from synthetic fixtures to natural, learned-model, distributed, or deployed settings named by the core claim."
                        if qcsa_row
                        else "No accepted evidence establishes transfer from narrow fixtures, sources, or local records to the broad architecture setting named by the core claim."
                    ),
                    [*transition_refs, *common_refs],
                    "External-context and deployed-context transfer remain unknown.",
                ),
            },
            "aggregation": {
                "policy": "non_aggregating",
                "scalar_score": "prohibited",
                "automatic_support_state_derivation": "prohibited",
            },
            "support_state_effect": "none",
            "non_claims": [
                "This vector does not promote the chapter-core claim.",
                "Current, public, or locally replayed records do not imply independent validity or transfer.",
            ],
        }
        vectors.append(vector)

    state_counts = {
        dimension_id: dict(sorted(Counter(row["dimensions"][dimension_id]["state"] for row in vectors).items()))
        for dimension_id in policy["dimension_order"]
    }
    return {
        "schema_version": "asi_stack.evidence_quality_vector_registry.v0",
        "policy_ref": str(POLICY.relative_to(ROOT)),
        "snapshot_date": SNAPSHOT_DATE,
        "scope": "All active chapter-core claims; vectors expose quality dimensions without changing the authoritative support summary.",
        "summary": {
            "vector_count": len(vectors),
            "dimension_count": len(policy["dimension_order"]),
            "summary_support_states": dict(sorted(Counter(row["summary_support_state"] for row in vectors).items())),
            "dimension_state_counts": state_counts,
            "numeric_aggregate_count": 0,
            "automatic_support_state_changes": 0,
        },
        "vectors": vectors,
        "support_state_effect": "none",
        "non_claims": policy["non_claims"],
    }


def main() -> None:
    registry = build_registry()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)} with "
        f"{len(registry['vectors'])} non-aggregating claim vectors."
    )


if __name__ == "__main__":
    main()
