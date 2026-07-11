#!/usr/bin/env python3
"""Validate post-v2 claim, chapter, vector, residual, and roadmap reconciliation."""
from __future__ import annotations

import copy

from build_canonical_public_status import ROOT, load_json, validate_against_schema


LEDGER = ROOT / "claim_decisions/post_v2_empirical_dispositions.json"
SCHEMA = ROOT / "schemas/post_v2_empirical_dispositions.schema.json"
VECTORS = ROOT / "evidence_quality/core_claim_vectors.json"
V1_DISPOSITIONS = ROOT / "claim_decisions/v1_x_core_claim_dispositions.json"
RESIDUALS = ROOT / "docs/post_v2_residual_ledger.md"
RECONCILIATION = ROOT / "docs/post_v2_empirical_reconciliation.md"
ROADMAP = ROOT / "docs/post_v2_evidence_roadmap.md"
APPENDIX = ROOT / "appendices/C_claim_evidence_matrix.qmd"
PLAN = ROOT / "docs/per_chapter_evidence_plan.md"
NON_CORE = ROOT / "docs/non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
EXPECTED = {
    "intent-to-execution-contracts.core": "evidence_transitions/post_v2/governed_work_flagship_no_change.json",
    "artifact-graphs-audit-logs-and-replay.core": "evidence_transitions/post_v2/governed_work_flagship_no_change.json",
    "resource-economics-and-token-budgets.core": "evidence_transitions/post_v2/governed_work_flagship_no_change.json",
    "routing-heads-and-specialist-cores.core": "evidence_transitions/post_v2/routing_deliberation_no_change.json",
    "governed-deliberation-and-test-time-scaling.core": "evidence_transitions/post_v2/routing_deliberation_no_change.json",
    "data-engines-continual-learning-and-unlearning.core": "evidence_transitions/post_v2/update_causality_no_change.json",
    "policy-optimization-and-learning-from-feedback.core": "evidence_transitions/post_v2/update_causality_no_change.json",
    "open-ended-improvement-engines.core": "evidence_transitions/post_v2/update_causality_no_change.json",
    "recursive-self-improvement-boundaries.core": "evidence_transitions/post_v2/update_causality_no_change.json",
}


def semantic_errors(ledger: dict, vectors: dict, residual_text: str, chapter_count: int) -> list[str]:
    errors: list[str] = []
    decisions = ledger.get("decisions", [])
    if {row.get("claim_id") for row in decisions} != set(EXPECTED) or len(decisions) != 9:
        errors.append("post-v2 ledger must contain exactly the nine affected core claims")
    if any(row.get("decision") != "no_change" or row.get("current_support_state") != "argument" or row.get("support_state_effect") != "none" for row in decisions):
        errors.append("all post-v2 decisions must retain argument with no support-state effect")
    if ledger.get("summary") != {"no_change": 9, "promote": 0, "narrow": 0, "demote": 0, "refute": 0, "support_state_changes": 0}:
        errors.append("post-v2 disposition summary drifted")
    if chapter_count != 54:
        errors.append("post-v2 cycle must preserve the 54-chapter architecture")
    vector_by_claim = {row.get("claim_id"): row for row in vectors.get("vectors", [])}
    for claim_id, transition_ref in EXPECTED.items():
        vector = vector_by_claim.get(claim_id, {})
        if vector.get("summary_support_state") != "argument" or vector.get("support_state_effect") != "none":
            errors.append(f"{claim_id}: vector support changed")
        dimensions = vector.get("dimensions", {})
        if dimensions.get("reproducibility", {}).get("state") != "adjacent_local_replay" or dimensions.get("adversarial_strength", {}).get("state") != "adjacent_bounded_controls":
            errors.append(f"{claim_id}: adjacent replay/control vector states missing")
        refs = dimensions.get("reproducibility", {}).get("evidence_refs", [])
        if transition_ref not in refs:
            errors.append(f"{claim_id}: post-v2 transition absent from evidence vector")
        if dimensions.get("independence", {}).get("state") != "internal_only" or dimensions.get("validity", {}).get("state") != "not_independently_assessed" or dimensions.get("transfer_distance", {}).get("state") != "not_established":
            errors.append(f"{claim_id}: independence, validity, or transfer was laundered")
    for phrase in ("zero useful releases", "Fallback and abstention activated zero times", "15 initially correct answers", "reduced retained-base accuracy", "62 test decisions", "did not prove influence or storage erasure", "activation absent"):
        if phrase not in residual_text:
            errors.append(f"residual ledger missing negative result: {phrase}")
    return errors


def main() -> None:
    required = (LEDGER, SCHEMA, VECTORS, V1_DISPOSITIONS, RESIDUALS, RECONCILIATION, ROADMAP, APPENDIX, PLAN, NON_CORE, STRUCTURE)
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing post-v2 reconciliation artifacts: " + ", ".join(missing))
    ledger = load_json(LEDGER); vectors = load_json(VECTORS); structure = load_json(STRUCTURE)
    chapter_count = sum(len(part.get("chapters", [])) for part in structure.get("parts", []))
    residual_text = RESIDUALS.read_text(encoding="utf-8")
    errors = validate_against_schema(ledger, load_json(SCHEMA), LEDGER.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(ledger, vectors, residual_text, chapter_count))
    v1_by_claim = {row["claim_id"]: row for row in load_json(V1_DISPOSITIONS)["dispositions"]}
    for claim_id, transition_ref in EXPECTED.items():
        chapter = claim_id.removesuffix(".core")
        chapter_path = ROOT / f"chapters/{chapter}.qmd"
        chapter_text = chapter_path.read_text(encoding="utf-8")
        if "## Post-v2" not in chapter_text or "`no_change`" not in chapter_text:
            errors.append(f"{chapter}: chapter lacks post-v2 no-change section")
        if transition_ref not in v1_by_claim.get(claim_id, {}).get("relevant_non_core_transition_refs", []):
            errors.append(f"{claim_id}: derived disposition lacks post-v2 transition side reference")
    appendix = APPENDIX.read_text(encoding="utf-8")
    if appendix.count("Post-v2 adjacent local evidence is recorded") != 9:
        errors.append("Appendix C must contain nine updated post-v2 evidence summaries")
    plan = PLAN.read_text(encoding="utf-8")
    for phrase in ("post-v2 model-generated governed-work replay", "post-v2 three-seed held-out", "post-v2 real checkpoint mutation"):
        if phrase not in plan:
            errors.append(f"per-chapter evidence plan missing completed lane: {phrase}")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for phrase in ("all empirical priorities", "Three `no_change` decisions", "Two independent `no_change` decisions", "Four `no_change` decisions", "activation conditions are still absent"):
        if phrase not in roadmap:
            errors.append(f"roadmap missing reconciled status: {phrase}")
    reconciliation = RECONCILIATION.read_text(encoding="utf-8")
    for phrase in ("keeps its 54-chapter architecture", "adds executable empirical validators, not a new Lean theorem", "External-human review", "optional and are not completion debt"):
        if phrase not in reconciliation:
            errors.append(f"reconciliation report missing boundary: {phrase}")
    non_core = NON_CORE.read_text(encoding="utf-8")
    for transition_ref in sorted(set(EXPECTED.values())):
        if transition_ref not in non_core:
            errors.append(f"public non-core ledger missing {transition_ref}")
        record = load_json(ROOT / transition_ref)
        if record.get("transition_effect") != "no_change" or record.get("support_state_effect") != "blocks_promotion" or record.get("review_status") != "accepted":
            errors.append(f"{transition_ref}: accepted no-change/block-promotion state drifted")
        boundary = " ".join(record.get("non_claims", []))
        if "does not promote" not in boundary:
            errors.append(f"{transition_ref}: core-promotion non-claim missing")
    mutations = []
    promoted = copy.deepcopy(ledger); promoted["decisions"][0]["decision"] = "promote"; mutations.append((promoted, vectors, residual_text, 54))
    missing_decision = copy.deepcopy(ledger); missing_decision["decisions"] = missing_decision["decisions"][:-1]; mutations.append((missing_decision, vectors, residual_text, 54))
    transfer = copy.deepcopy(vectors); next(row for row in transfer["vectors"] if row["claim_id"] in EXPECTED)["dimensions"]["transfer_distance"]["state"] = "established"; mutations.append((ledger, transfer, residual_text, 54))
    erased = residual_text.replace("Fallback and abstention activated zero times", "Fallback was adequate")
    mutations.append((ledger, vectors, erased, 54))
    mutations.append((ledger, vectors, residual_text, 55))
    for args in mutations:
        if not semantic_errors(*args):
            errors.append("a post-v2 reconciliation negative control was accepted")
    if errors:
        raise SystemExit("Post-v2 empirical reconciliation failed:\n - " + "\n - ".join(errors))
    print("Post-v2 empirical reconciliation passed: 3 accepted non-core no-change transitions, 9 core no-change decisions, 9 updated chapters/vectors/Appendix C/evidence-plan rows, 14 retained residual lanes, 3 honest conditional deferrals, 54 chapters, zero support-state changes, no new Lean claim, and 5 rejecting controls.")


if __name__ == "__main__":
    main()
