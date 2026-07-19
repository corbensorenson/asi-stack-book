#!/usr/bin/env python3
"""Validate and red-team post-v2.1 book-wide empirical reconciliation."""

from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LEDGER = "claim_decisions/post_v2_1_empirical_dispositions.json"
STATUS = "roadmap_records/post_v2_1_residual_and_transfer_status.json"
OUTCOME = "experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json"
TRANSITION_DIR = "evidence_transitions/post_v2_1"

CHAPTER_HEADINGS = {
    "intent-to-execution-contracts": "## Post-v2.1 usefulness frontier",
    "runtime-adapters-tool-permissions-and-human-approval": "## Post-v2.1 governed adapter boundary",
    "artifact-graphs-audit-logs-and-replay": "## Post-v2.1 state and effect replay",
    "capability-replacement-and-rollback": "## Post-v2.1 full-state rollback result",
    "readiness-gates-residual-escrow-and-quarantine": "## Post-v2.1 readiness calibration",
    "security-kernel-and-digital-scifs": "## Post-v2.1 security/usefulness boundary",
    "resource-economics-and-token-budgets": "## Post-v2.1 joint cost accounting",
    "routing-heads-and-specialist-cores": "## Post-v2.1 ambiguous routing result",
    "governed-deliberation-and-test-time-scaling": "## Post-v2.1 real-model deliberation result",
    "verification-bandwidth-and-context-adequacy": "## Post-v2.1 evaluator adequacy result",
    "data-engines-continual-learning-and-unlearning": "## Post-v2.1 full-state and unlearning result",
    "policy-optimization-and-learning-from-feedback": "## Post-v2.1 prospective update authority",
    "open-ended-improvement-engines": "## Post-v2.1 stopped improvement result",
    "recursive-self-improvement-boundaries": "## Post-v2.1 authority-preserving update result",
}

SOURCE_TARGETS = {
    "ext_claw_swe_bench_2026": ["artifact-graphs-audit-logs-and-replay", "runtime-adapters-tool-permissions-and-human-approval", "resource-economics-and-token-budgets", "benchmark-ratchets-and-anti-goodhart-evidence"],
    "ext_txfs_2018": ["capability-replacement-and-rollback", "artifact-graphs-audit-logs-and-replay", "runtime-adapters-tool-permissions-and-human-approval"],
    "ext_dont_hallucinate_abstain_2024": ["routing-heads-and-specialist-cores", "readiness-gates-residual-escrow-and-quarantine", "verification-bandwidth-and-context-adequacy"],
    "ext_muse_unlearning_2025": ["data-engines-continual-learning-and-unlearning", "policy-optimization-and-learning-from-feedback", "benchmark-ratchets-and-anti-goodhart-evidence"],
    "ext_unlearning_benchmarks_weak_2024": ["data-engines-continual-learning-and-unlearning", "benchmark-ratchets-and-anti-goodhart-evidence", "evidence-states-and-claim-discipline"],
    "ext_openunlearning_2025": ["data-engines-continual-learning-and-unlearning", "benchmark-ratchets-and-anti-goodhart-evidence", "living-book-methodology"],
}

RESIDUAL_STATES = {
    "GW-01": "persisted", "GW-02": "narrowed", "GW-03": "persisted",
    "RD-01": "narrowed", "RD-02": "closed", "RD-03": "narrowed", "RD-04": "persisted",
    "UU-01": "narrowed", "UU-02": "narrowed", "UU-03": "persisted", "UU-04": "closed",
}


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate(data: dict) -> list[str]:
    errors = []
    ledger, status, outcome, manifest, vectors = (data[key] for key in ("ledger", "status", "outcome", "manifest", "vectors"))
    active_status = data["active_status"]
    maintenance_status = data["maintenance_status"]
    ledger_schema = load("schemas/post_v2_1_empirical_dispositions.schema.json")
    transition_schema = load("schemas/evidence_transition_record.schema.json")
    errors.extend(f"disposition schema: {error.message}" for error in Draft202012Validator(ledger_schema).iter_errors(ledger))
    transitions = data["transitions"]
    if len(transitions) != 6:
        errors.append("exactly six post-v2.1 transitions are required")
    for name, transition in transitions.items():
        errors.extend(f"{name}: transition schema: {error.message}" for error in Draft202012Validator(transition_schema).iter_errors(transition))
        if transition.get("transition_effect") != "no_change" or transition.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{name}: transition support boundary drifted")
    decisions = ledger.get("decisions", [])
    if {row.get("chapter_id") for row in decisions} != set(CHAPTER_HEADINGS) or any(row.get("core_decision") != "no_change" for row in decisions):
        errors.append("fourteen chapter-core no-change decisions are not exact")
    if ledger.get("summary") != {"no_change": 14, "promote": 0, "narrow_core": 0, "demote": 0, "refute": 0, "support_state_changes": 0}:
        errors.append("core disposition summary drifted")
    chapter_rows = [chapter for part in manifest.get("parts", []) for chapter in part.get("chapters", [])]
    chapters = {chapter["id"]: chapter for chapter in chapter_rows}
    live_chapter_count = len(chapter_rows)
    if len(chapters) != live_chapter_count:
        errors.append("live manifest contains duplicate chapter identifiers")
    activation = active_status.get("activation_baseline", {})
    if activation.get("active_chapter_count") != 54 or activation.get("proof_target_count") != 298:
        errors.append("historical post-v2.1 54-chapter/298-target baseline drifted")
    historical_expansion = active_status.get("structural_expansion_contract", {})
    if historical_expansion.get("live_chapter_count") != 55 or historical_expansion.get("support_state_effect") != "none":
        errors.append("historical authorized 55th-chapter expansion drifted")
    activation_truth = maintenance_status.get("activation_truth", {})
    structural_tranche = maintenance_status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    first_tranche = structural_tranche.get("first_tranche", {})
    admitted_chapter_ids = set(first_tranche.get("candidate_ids", []))
    if (
        activation_truth.get("live_working_chapter_count") != live_chapter_count
        or structural_tranche.get("current_manifest_chapter_count") != live_chapter_count
        or first_tranche.get("manifest_admitted_count") != len(admitted_chapter_ids)
        or live_chapter_count != 55 + len(admitted_chapter_ids)
        or not admitted_chapter_ids.issubset(chapters)
    ):
        errors.append("current live manifest disagrees with the later manifest-admitted structural tranche")
    for chapter_id, heading in CHAPTER_HEADINGS.items():
        text = data["chapter_texts"].get(chapter_id, "")
        if text.count(heading) != 1 or "post-v2.1" not in text.lower():
            errors.append(f"{chapter_id}: exact post-v2.1 result section missing")
        if chapter_id not in data["appendix_c"] or chapter_id not in data["evidence_plan"]:
            errors.append(f"{chapter_id}: Appendix C or evidence-plan routing missing")
    vector_rows = vectors.get("vectors", [])
    vector_by_claim = {row["claim_id"]: row for row in vector_rows}
    if (
        len(vector_rows) != live_chapter_count
        or vectors.get("summary", {}).get("vector_count") != live_chapter_count
        or vectors.get("summary", {}).get("summary_support_states") != {"argument": live_chapter_count}
        or activation_truth.get("chapter_core_argument_count") != live_chapter_count
        or activation_truth.get("chapter_core_promotion_count") != 0
    ):
        errors.append("evidence vectors launder core support")
    # The completed post-v2.1 result originally covered 27 adjacent claims;
    # the later QCSA and post-v2.3 quality-floor/canonical-transition
    # reconciliations legitimately add adjacent local replay coverage without changing support,
    # independence, or transfer state.
    replay_state_counts: dict[str, int] = {}
    for row in vector_rows:
        state = row.get("dimensions", {}).get("reproducibility", {}).get("state")
        replay_state_counts[state] = replay_state_counts.get(state, 0) + 1
    if vectors.get("summary", {}).get("dimension_state_counts", {}).get("reproducibility") != replay_state_counts:
        errors.append("evidence-vector replay summary drifted")
    if any(row.get("dimensions", {}).get("independence", {}).get("state") != "internal_only" or row.get("dimensions", {}).get("transfer_distance", {}).get("state") != "not_established" for row in vectors.get("vectors", [])):
        errors.append("an evidence vector overstates independence or transfer")
    for decision in decisions:
        vector = vector_by_claim.get(decision["claim_id"], {})
        reproducibility = vector.get("dimensions", {}).get("reproducibility", {})
        refs = reproducibility.get("evidence_refs", [])
        if vector.get("summary_support_state") != "argument" or reproducibility.get("state") != "adjacent_local_replay" or not set(decision["transition_refs"]).issubset(refs):
            errors.append(f"{decision['claim_id']}: vector lacks transition refs or preserves wrong support")
        if vector.get("dimensions", {}).get("independence", {}).get("state") != "internal_only" or vector.get("dimensions", {}).get("transfer_distance", {}).get("state") != "not_established":
            errors.append(f"{decision['claim_id']}: vector overstates independence or transfer")
    status_residuals = {row["id"]: row["state"] for row in status.get("residuals", [])}
    outcome_residuals = {**outcome["P1"]["residual_dispositions"], **outcome["P2"]["residual_dispositions"], **outcome["P3"]["residual_dispositions"]}
    if status_residuals != RESIDUAL_STATES or outcome_residuals != RESIDUAL_STATES:
        errors.append("status, outcome, and canonical residual dispositions disagree")
    for residual_id, state in RESIDUAL_STATES.items():
        if f"`{residual_id}`" not in data["residual_ledger"] or state not in data["residual_ledger"]:
            errors.append(f"{residual_id}: readable residual disposition missing")
    for source_id, targets in SOURCE_TARGETS.items():
        source = next((row for row in data["source_inventory"] if row.get("id") == source_id), None)
        if not source or source.get("chapter_targets") != targets:
            errors.append(f"{source_id}: source inventory routing drifted")
        for target in targets:
            chapter = chapters.get(target, {})
            mapping_ids = {row.get("source_id") for row in chapter.get("claim_source_mappings", [])}
            if source_id not in chapter.get("source_ids", []) or source_id not in mapping_ids:
                errors.append(f"{source_id}: manifest mapping missing for {target}")
        if source_id not in data["appendix_h"] or source_id not in data["appendix_c"]:
            errors.append(f"{source_id}: generated Appendix H or C route missing")
    if "2026-07-11 - Post-v2.1 empirical execution and reconciliation" not in data["changelog"]:
        errors.append("changelog reconciliation entry missing")
    proof_manifest = data["proof_manifest"]
    proof_records = proof_manifest.get("records", [])
    proof_status_counts = proof_manifest.get("status_counts", {})
    current_proof_count = proof_manifest.get("proof_target_count")
    historical_proof_count = activation.get("proof_target_count")
    planned_records = [row for row in proof_records if row.get("status") == "planned"]
    record_status_counts: dict[str, int] = {}
    for row in proof_records:
        record_status = row.get("status")
        record_status_counts[record_status] = record_status_counts.get(record_status, 0) + 1
    added_proof_count = (
        current_proof_count - historical_proof_count
        if isinstance(current_proof_count, int) and isinstance(historical_proof_count, int)
        else -1
    )
    if (
        "no new lean theorem" not in data["reconciliation"].lower()
        or current_proof_count != activation_truth.get("proof_target_count")
        or current_proof_count != len(proof_records)
        or proof_status_counts != record_status_counts
        or proof_status_counts != {"implemented": historical_proof_count, "planned": added_proof_count}
        or len(planned_records) != added_proof_count
        or {row.get("chapter_id") for row in planned_records} != admitted_chapter_ids
        or any(row.get("summary_support_state") not in (None, "argument") for row in planned_records)
    ):
        errors.append("proof/no-new-theorem boundary drifted")
    if outcome.get("support_state_effect") != "none" or ledger.get("summary", {}).get("promote") != 0:
        errors.append("outcome or ledger invents promotion")
    return errors


def main() -> None:
    data = {
        "ledger": load(LEDGER), "status": load(STATUS), "outcome": load(OUTCOME),
        "active_status": load("roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"),
        "maintenance_status": load("roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"),
        "manifest": load("book_structure.json"), "vectors": load("evidence_quality/core_claim_vectors.json"),
        "source_inventory": load("sources/source_inventory.json"), "proof_manifest": load("proofs/proof_manifest.json"),
        "transitions": {path.name: json.loads(path.read_text()) for path in sorted((ROOT / TRANSITION_DIR).glob("*.json"))},
        "chapter_texts": {chapter: (ROOT / f"chapters/{chapter}.qmd").read_text() for chapter in CHAPTER_HEADINGS},
        "appendix_c": (ROOT / "appendices/C_claim_evidence_matrix.qmd").read_text(),
        "appendix_h": (ROOT / "appendices/H_external_sources.qmd").read_text(),
        "evidence_plan": (ROOT / "docs/per_chapter_evidence_plan.md").read_text(),
        "residual_ledger": (ROOT / "docs/post_v2_residual_ledger.md").read_text(),
        "changelog": (ROOT / "appendices/F_changelog.qmd").read_text(),
        "reconciliation": (ROOT / "docs/post_v2_1_empirical_reconciliation.md").read_text(),
    }
    errors = validate(data)
    mutations = [
        ("core promotion", lambda x: x["ledger"]["summary"].__setitem__("promote", 1)),
        ("decision erasure", lambda x: x["ledger"]["decisions"].pop()),
        ("transition promotion", lambda x: next(iter(x["transitions"].values())).__setitem__("transition_effect", "upward")),
        ("chapter addition", lambda x: x["manifest"]["parts"][0]["chapters"].append(copy.deepcopy(x["manifest"]["parts"][0]["chapters"][0]))),
        ("chapter result erasure", lambda x: x["chapter_texts"].__setitem__("intent-to-execution-contracts", "")),
        ("vector promotion", lambda x: x["vectors"]["summary"].__setitem__("summary_support_states", {"argument": 53, "empirical-test-backed": 1})),
        ("false independence", lambda x: x["vectors"]["vectors"][0]["dimensions"]["independence"].__setitem__("state", "externally_independent")),
        ("residual closure laundering", lambda x: x["status"]["residuals"][0].__setitem__("state", "closed")),
        ("source target erasure", lambda x: next(row for row in x["source_inventory"] if row["id"] == "ext_txfs_2018")["chapter_targets"].pop()),
        ("Appendix H erasure", lambda x: x.__setitem__("appendix_h", x["appendix_h"].replace("ext_muse_unlearning_2025", "erased"))),
        ("proof invention", lambda x: x["proof_manifest"].__setitem__("proof_target_count", 299)),
        ("unadmitted planned proof", lambda x: next(row for row in x["proof_manifest"]["records"] if row.get("status") == "planned").__setitem__("chapter_id", "intent-to-execution-contracts")),
        ("changelog erasure", lambda x: x.__setitem__("changelog", "")),
    ]
    for name, mutate in mutations:
        mutant = copy.deepcopy(data)
        mutate(mutant)
        if not validate(mutant):
            errors.append(f"reconciliation mutation accepted: {name}")
    result = subprocess.run(["python3", "scripts/validate_post_v2_1_outcomes.py"], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        errors.append("underlying outcome validator failed")
    if errors:
        print("Post-v2.1 empirical reconciliation validation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)
    live_chapter_count = sum(len(part.get("chapters", [])) for part in data["manifest"].get("parts", []))
    proof_manifest = data["proof_manifest"]
    print(f"Post-v2.1 reconciliation passed: 6 bounded transitions, 14 core no-change decisions and chapter owners, 11 residual dispositions, 19 modern-source routes, preserved 54-chapter/298-target activation and authorized 55th-chapter historical lineage, {live_chapter_count} live argument-state vectors, {proof_manifest.get('proof_target_count')} current targets ({proof_manifest.get('status_counts', {}).get('implemented')} implemented plus {proof_manifest.get('status_counts', {}).get('planned')} planned on later manifest-admitted chapters), no theorem invented by the historical cycle, and 13 rejecting mutations.")


if __name__ == "__main__":
    main()
