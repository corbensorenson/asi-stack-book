#!/usr/bin/env python3
"""Build the retrospective N0-N5 competence audit for accepted negative outcomes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence_quality/negative_result_rehabilitation.json"
DOC = ROOT / "docs/negative_result_rehabilitation.md"
IDENTITY = ROOT / "evidence_quality/claim_identity_graph.json"

# These sets are an explicit retrospective adjudication, not a keyword
# classifier. Absence of a current competence dossier fails closed below N3.
N0_CLAIMS = {
    "residual-verifier-capacity.heldout-pressure-effect",
}

N1_CLAIMS = {
    "kerc.broad_matched_total_system_efficiency",
    "post_v2_governed_work_flagship.bounded_matched_local_result",
    "post_v2_routing_deliberation.bounded_matched_local_result",
    "post_v2_update_causality.bounded_real_mutation_result",
    "post_v2_1.ambiguous_routing.bounded_result",
    "post_v2_1.full_state_rollback.bounded_result",
    "post_v2_1.full_state_update.no_change_result",
    "post_v2_1.governed_usefulness_rollback.bounded_result",
    "post_v2_1.real_model_deliberation.no_change_result",
    "post_v2_1.unlearning_causality.narrow_result",
    "post_v2_3.governance_tax_natural_work.bounded_result",
    "post_v2_3.residual_honesty_under_pressure.bounded_result",
    "resource_economics.governed_useful_throughput_under_natural_work",
    "routing-deliberation.heldout-local-policy-effect",
    "update-unlearning.full-state-local-axis-separation",
}

N2_CLAIMS = {
    "agency-dignity-and-corrigibility.core",
    "artifact-graphs.epistemic_tcb_fixture",
    "artifact-graphs.github_pages_ci_attestation",
    "artifact-graphs.live_artifact_attestation_probe",
    "artifact-graphs.public_site_record_reality_attestation",
    "artifact-graphs.randomized_artifact_attestation_audit",
    "artifact-graphs.receipt_faithfulness_adversarial_fixture",
    "artifact-graphs.receipt_repository_audit_challenge",
    "artifact-graphs.record_reality_sequence_bridge",
    "benchmark-ratchets-and-anti-goodhart-evidence.core",
    "capability-replacement-and-rollback.core",
    "capability-replacement-and-rollback.invariant.011",
    "circle-calculus.contract_pack_archive",
    "circle-calculus.cyclic_mixer_receipt_slice",
    "circle-calculus.kv_cache_ring_buffer_receipt_slice",
    "circle-calculus.multicoil_phase_receipt_slice",
    "circle-calculus.public_consumer_gate",
    "circle-calculus.recurrence_schedule_receipt_slice",
    "circle-calculus.sparse_attention_receipt_slice",
    "circle-calculus.strided_fanout_receipt_slice",
    "claim-ledgers-and-belief-revision.core",
    "command-contracts-and-semantic-interfaces.core",
    "compact-generative-systems.residual_ledger_storage_replay",
    "compact-generative-systems.seed_rule_exact_regeneration_receipt_slice",
    "constitutional-alignment-substrate.core",
    "evidence-states-and-claim-discipline.core",
    "executable-specifications-and-lean-proof-envelope.core",
    "fast-generation-architectures.core",
    "fast-generation-architectures.public_safe_task_bundle_accounting",
    "governance-rights-fork-exit-and-audit.core",
    "intent-to-execution-contracts.core",
    "labor-os.typed_job_durable_lifecycle_probe",
    "living-book-methodology.core",
    "moral-uncertainty-and-value-conflict.core",
    "open-research-agenda-and-bibliography-plan.core",
    "personal-compute-hives.partitioned_authority_fixture",
    "planning-as-a-control-layer.core",
    "planning.runtime_replan_delta_audit",
    "planning.scheduler_state_probe",
    "project-theseus-as-report-first-implementation-reference.book_to_theseus_crosswalk_pointer",
    "project-theseus-as-report-first-implementation-reference.public_task_bundle_import_summary",
    "project-theseus-as-report-first-implementation-reference.work_board_currentness_import",
    "qcsa.active_questions_exact_fixture_value",
    "qcsa.exact_synthetic_matched_advantage",
    "qcsa.governance_prevention_resource_tradeoff",
    "qcsa.open_world_or_production_transfer",
    "qcsa.reference_implementation_exact_contract_conformance",
    "qcsa.semantic_round_trip_exact_preservation",
    "qcsa.vertical_reference_exact_reversible_trace",
    "rankfold-neuralfold.local_artifact_import_metadata",
    "rankfold-neuralfold.public_safe_replay_probe",
    "readiness-gates-residual-escrow-and-quarantine.core",
    "readiness-gates.readiness_lifecycle_probe",
    "recursive-self-improvement-boundaries.core",
    "resource-economics-and-token-budgets.core",
    "resource-economics.local_replay_probe",
    "resource-economics.local_workload_quality_route_selection",
    "resource-economics.publication_pipeline_cost_profile",
    "resource-economics.synthetic_load_stability_route_selection",
    "resource-economics.workflow_trace_dispatch_accounting",
    "routing-heads.synthetic_routing_decision_lease",
    "runtime-adapters-tool-permissions-and-human-approval.core",
    "runtime-adapters.adversarial_boundary_probe",
    "runtime-adapters.human_oversight_degradation",
    "runtime-adapters.local_effect_replay_probe",
    "security-kernel-and-digital-scifs.core",
    "security-kernel.scif_sanitized_commit_replay",
    "spinoza-verification-and-proof-carrying-claims.core",
    "stable-capability-fields.core",
    "system-boundaries-and-authority.core",
    "system-boundaries.authority_revocation_trace",
    "the-efficient-asi-hypothesis.core",
    "unified-adaptive-tribunal-and-adversarial-review.core",
    "virtual-context-abi.core",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def negative_transitions() -> list[tuple[Path, dict]]:
    rows = []
    for path in sorted((ROOT / "evidence_transitions").glob("**/*.json")):
        item = load(path)
        if (
            item.get("review_status") == "accepted"
            and item.get("transition_validity_state") == "review_accepted"
            and item.get("transition_effect") in {"no_change", "refuted"}
        ):
            rows.append((path, item))
    return rows


def level_for(claim_id: str) -> str:
    if claim_id in N0_CLAIMS:
        return "N0"
    if claim_id in N1_CLAIMS:
        return "N1"
    if claim_id in N2_CLAIMS:
        return "N2"
    raise ValueError(f"unadjudicated negative claim: {claim_id}")


def competence(level: str) -> dict:
    if level == "N0":
        implementation = "not_adjudicable_because_instrument_failed"
        activation = "not_reliably_observed"
        construct = "invalid_denominator_or_evaluator"
        inference = "No claim inference. The instrument must be rebuilt under a new prospective protocol."
        next_action = "Repair and recalibrate the instrument on sacrificial data, then create a new claim identity and held-out protocol."
    elif level == "N1":
        implementation = "not_demonstrated_to_claim_commensurate_standard"
        activation = "partial_unknown_or_not_sufficiently_traced"
        construct = "idea_not_competently_instantiated"
        inference = "This implementation is inadequate or unqualified; the mechanism or architecture remains untested."
        next_action = "Build a materially competent implementation with activation traces, favorable controls, matched tuning, and a new frozen denominator."
    else:
        implementation = "bounded_fixture_or_artifact_path_executed_only"
        activation = "exact_fixture_path_observed_not_parent_mechanism"
        construct = "proxy_or_regime_does_not_instantiate_target_parent"
        inference = "Retain the exact proxy or regime outcome; no target mechanism, architecture, or broad parent refutation follows."
        next_action = "Design a construct-valid natural task for the canonical parent with strong baselines, sensitivity, independent evaluation, and transfer."
    return {
        "implementation_competence": implementation,
        "mechanism_activation": activation,
        "construct_validity": construct,
        "matched_engineering_and_tuning": "not_demonstrated_under_current_contract",
        "oracle_or_favorable_upper_bound": "not_demonstrated_under_current_contract",
        "positive_control_status": "not_requalified_under_current_contract",
        "negative_control_status": "historical_controls_retained_but_not_a_current_competence_dossier",
        "evaluator_competence": "not_independently_requalified_under_current_contract",
        "prospective_sensitivity_or_power": "not_demonstrated_under_current_contract",
        "fair_rescue_ladder": "not_prospectively_complete_under_current_contract",
        "natural_non_authored_corpus": "not_established_as_claim_commensurate_under_current_contract",
        "heldout_custody": "historical_denominator_retained_and_must_not_be_reopened",
        "independent_alternate_implementation": "absent_or_not_demonstrated",
        "independent_reproduction": "absent",
        "materially_different_transfer_settings": 0,
        "maximum_usable_negative_inference": inference,
        "required_next_action": next_action,
    }


def build() -> dict:
    identity = load(IDENTITY)
    identity_by_transition = {row["transition_id"]: row for row in identity["records"]}
    transitions = negative_transitions()
    claims = {item["claim_id"] for _, item in transitions}
    adjudicated = N0_CLAIMS | N1_CLAIMS | N2_CLAIMS
    if claims != adjudicated:
        raise ValueError(
            f"negative rehabilitation table drift; missing={sorted(claims-adjudicated)}, "
            f"stale={sorted(adjudicated-claims)}"
        )
    if (N0_CLAIMS & N1_CLAIMS) or (N0_CLAIMS & N2_CLAIMS) or (N1_CLAIMS & N2_CLAIMS):
        raise ValueError("N-level adjudication sets overlap")

    records = []
    for path, item in transitions:
        identity_row = identity_by_transition[item["transition_id"]]
        level = level_for(item["claim_id"])
        records.append({
            "transition_id": item["transition_id"],
            "transition_path": path.relative_to(ROOT).as_posix(),
            "transition_sha256": sha256(path),
            "claim_id": item["claim_id"],
            "historical_transition_effect": item["transition_effect"],
            "historical_support_state": item["new_support_state"],
            "historical_transition_label_preserved": True,
            "canonical_parent_id": identity_row["canonical_parent_id"],
            "identity_relation": identity_row["primary_relation"],
            "owner_chapter_id": identity_row["owner_chapter_id"],
            "assigned_n_level": level,
            "competence_audit": competence(level),
            "raw_scope_boundary": item["scope_boundary"],
            "raw_negative_results": item.get("negative_results", []),
            "raw_limitations": item.get("limitations", []),
            "raw_non_claims": item.get("non_claims", []),
            "broad_negative_inference_state": "quarantined",
            "chapter_reconciliation_state": "bounded_language_required",
            "support_state_effect": "none",
            "release_effect": "none",
            "audit_method": "manual_retrospective_claim_identity_scope_artifact_and_competence_review_2026_07_17",
        })

    counts = Counter(row["assigned_n_level"] for row in records)
    historical_effects = Counter(row["historical_transition_effect"] for row in records)
    return {
        "schema_version": "asi_stack.negative_result_rehabilitation.v1",
        "snapshot_date": "2026-07-17",
        "authority": "Corben Sorenson",
        "governing_contract": "docs/claim_bearing_experiment_competence_standard.md",
        "identity_graph": "evidence_quality/claim_identity_graph.json",
        "policy": {
            "historical_raw_outcomes_immutable": True,
            "post_hoc_missing_competence_evidence_may_be_invented": False,
            "heldout_denominators_may_be_reopened": False,
            "n_level_required_for_negative_inference": True,
            "broad_negative_inference_quarantined": True,
            "N3_or_higher_count": 0,
            "N4_or_higher_count": 0,
            "N5_count": 0,
        },
        "summary": {
            "accepted_negative_or_no_change_transition_count": len(records),
            "historical_no_change_count": historical_effects["no_change"],
            "historical_refuted_label_count": historical_effects["refuted"],
            "rehabilitated_record_count": len(records),
            "unclassified_record_count": 0,
            "n_level_counts": {level: counts.get(level, 0) for level in ["N0", "N1", "N2", "N3", "N4", "N5"]},
            "broad_negative_inference_count": 0,
            "chapter_core_negative_inference_count": 0,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        "records": records,
        "non_claims": [
            "Rehabilitation does not erase or rewrite any historical transition or raw outcome.",
            "An N0-N2 classification does not refute the target mechanism, architecture, or canonical parent.",
            "The absence of any N3-N5 result is a competence boundary, not evidence that every idea succeeds.",
            "This audit does not create support, publication, deployment, reproduction, transfer, or release authority.",
        ],
    }


def render_doc(value: dict) -> str:
    counts = value["summary"]["n_level_counts"]
    lines = [
        "# Historical Negative-Result Rehabilitation",
        "",
        "Status: P1 accepted-transition rehabilitation complete; broader historical scan remains separately owned  ",
        "Snapshot: 2026-07-17  ",
        "Machine ledger: `evidence_quality/negative_result_rehabilitation.json`  ",
        "Contract: `docs/claim_bearing_experiment_competence_standard.md`",
        "",
        "## Result",
        "",
        "All 90 accepted transitions carrying a historical `no_change` or `refuted` effect now have a retrospective N0–N5 classification. The audit assigns "
        f"{counts['N0']} N0 instrument failure, {counts['N1']} N1 implementation failures, and {counts['N2']} N2 proxy/regime failures. "
        "No historical result earns N3, N4, or N5 under the current competence standard.",
        "",
        "The raw transition files and labels remain immutable. What changes is their usable interpretation: none of the 90 records may currently refute a target mechanism, architecture, broad canonical parent, or chapter core. The three historical `refuted` labels remain discoverable, but KERC is N1 and the two QCSA refutations are N2. They are not N3 exact competent refutations under the new standard.",
        "",
        "## Why the audit fails closed",
        "",
        "- N0 records have an invalid instrument, evaluator, denominator, or harness and carry no claim inference.",
        "- N1 records do not demonstrate claim-commensurate implementation competence or mechanism activation; the idea remains untested.",
        "- N2 records retain exact bounded fixture or proxy observations, but their task, corpus, metric, or regime cannot refute the target parent.",
        "- Missing historical evidence is not reconstructed from intent or plausible narrative. No post-hoc rescue ladder, power analysis, evaluator independence, or mechanism trace is invented.",
        "- Historical held-out sets remain sealed. A serious reattempt requires a new claim identity, competent implementation, development-data rescue ladder, and new prospective denominator.",
        "",
        "## KERC correction",
        "",
        "`kerc.broad_matched_total_system_efficiency` is N1. The historical 714-byte versus 73.25-byte packet result and 0.5 task score remain real observations, but the chance-level task performance, absent adversarial-polarity training class, small linear cores, jointly authored compiler/verifier, redundant residual storage, and uncalibrated energy fail implementation-competence gates. The tested implementation is inadequate; Kernel English, learned cognitive compilation, hierarchical residuals, and the broader architecture remain untested by that run.",
        "",
        "## Complete rehabilitation table",
        "",
        "| Transition | Claim | Identity | N-level | Maximum usable inference |",
        "|---|---|---|---|---|",
    ]
    for row in value["records"]:
        inference = row["competence_audit"]["maximum_usable_negative_inference"].replace("|", "\\|")
        lines.append(
            f"| `{row['transition_id']}` | `{row['claim_id']}` | `{row['identity_relation']}` → "
            f"`{row['canonical_parent_id']}` | `{row['assigned_n_level']}` | {inference} |"
        )
    lines.extend([
        "",
        "## Remaining P1 work",
        "",
        "This tranche covers the complete accepted-transition denominator. P1 still owns a broader prose and `blocked_after_full_attempt` scan so no unregistered historical negative conclusion survives outside the accepted-transition ledger. Chapter, Appendix C, non-core ledger, synopsis, and public language must all use the same bounded interpretation.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    encoded = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    rendered = render_doc(value)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != encoded:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale; run scripts/build_negative_result_rehabilitation.py")
        if not DOC.exists() or DOC.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"{DOC.relative_to(ROOT)} is stale; run scripts/build_negative_result_rehabilitation.py")
        print("Negative-result rehabilitation current: 90 classified, 0 N3-N5, 0 broad negative inferences.")
        return
    OUT.write_text(encoded, encoding="utf-8")
    DOC.write_text(rendered, encoding="utf-8")
    print("Negative-result rehabilitation wrote: 90 classified, 0 N3-N5, 0 broad negative inferences.")


if __name__ == "__main__":
    main()
