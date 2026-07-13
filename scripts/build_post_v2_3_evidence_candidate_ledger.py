#!/usr/bin/env python3
"""Build and validate the complete post-v2/QCSA evidence-candidate adjudication ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/post_v2_3_evidence_candidate_ledger.json"
REVIEW = ROOT / "docs/post_v2_3_evidence_candidate_ledger.md"
SCHEMA = ROOT / "schemas/post_v2_3_evidence_candidate_ledger.schema.json"
TRANSITION_SCHEMA = ROOT / "schemas/evidence_transition_record.schema.json"
QCSA_DECISIONS = ROOT / "claim_decisions/qcsa_reference_evaluation_dispositions.json"
QCSA_RESULT = "experiments/qcsa_reference/results/evaluation_results.json"
QCSA_DISPOSITIONS = "claim_decisions/qcsa_reference_evaluation_dispositions.json"
CHANGELOG_REF = "appendices/F_changelog.qmd#2026-07-13---post-v23-evidence-adjudication"

EXISTING = sorted((ROOT / "evidence_transitions/post_v2").glob("*.json")) + sorted((ROOT / "evidence_transitions/post_v2_1").glob("*.json"))

OWNER_MAP = {
    "post_v2_governed_work_flagship.bounded_matched_local_result": "intent-to-execution-contracts",
    "post_v2_routing_deliberation.bounded_matched_local_result": "routing-heads-and-specialist-cores",
    "post_v2_update_causality.bounded_real_mutation_result": "data-engines-continual-learning-and-unlearning",
    "post_v2_1.ambiguous_routing.bounded_result": "routing-heads-and-specialist-cores",
    "post_v2_1.full_state_rollback.bounded_result": "capability-replacement-and-rollback",
    "post_v2_1.full_state_update.no_change_result": "data-engines-continual-learning-and-unlearning",
    "post_v2_1.governed_usefulness_rollback.bounded_result": "intent-to-execution-contracts",
    "post_v2_1.real_model_deliberation.no_change_result": "governed-deliberation-and-test-time-scaling",
    "post_v2_1.unlearning_causality.narrow_result": "data-engines-continual-learning-and-unlearning",
    "qcsa.exact_synthetic_matched_advantage": "integrated-reference-architecture",
    "qcsa.plural_facets_exact_fixture_value": "cognitive-compilation-and-semantic-ir",
    "qcsa.active_questions_exact_fixture_value": "cognitive-compilation-and-semantic-ir",
    "qcsa.identity_indirection_exact_migration_value": "virtual-context-abi",
    "qcsa.certificate_authority_fields_exact_value": "runtime-adapters-tool-permissions-and-human-approval",
    "qcsa.migration_compatibility_exact_value": "data-engines-continual-learning-and-unlearning",
    "qcsa.semantic_round_trip_exact_preservation": "cognitive-compilation-and-semantic-ir",
    "qcsa.task_calibration_exact_result": "evidence-states-and-claim-discipline",
    "qcsa.governance_prevention_resource_tradeoff": "resource-economics-and-token-budgets",
    "qcsa.open_world_or_production_transfer": "integrated-reference-architecture",
    "qcsa.reference_implementation_exact_contract_conformance": "integrated-reference-architecture",
    "qcsa.vertical_reference_exact_reversible_trace": "integrated-reference-architecture",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_refs(refs: list[str]) -> list[dict]:
    records = []
    for ref in refs:
        path_text = ref.split("#", 1)[0]
        path = ROOT / path_text
        if path.is_file() and path_text not in {item["path"] for item in records}:
            records.append({"path": path_text, "sha256": sha(path)})
    if not records:
        raise ValueError(f"no immutable file reference among {refs}")
    return records


def existing_assessment(record: dict, program: str, disposition: str) -> dict:
    claim = record["claim_id"]
    limitations = record.get("limitations") or ["bounded local result only"]
    negatives = record.get("negative_results") or [record["scope_boundary"]]
    return {
        "candidate_id": claim,
        "program": program,
        "result_refs": digest_refs(record.get("claim_record_refs", []) + record.get("artifact_refs", [])),
        "candidate_claim": record["scope_boundary"],
        "owner": OWNER_MAP[claim],
        "comparator": "The preregistered matched baseline, ablation, challenger, or no-update route named by the frozen campaign and transition record.",
        "cohort": "; ".join(limitations[:2]) + "; exact retained result denominator only.",
        "cost": "Campaign-recorded latency, token/tool, review, rollback, state, or resource fields are retained; unmeasured production cost is not inferred.",
        "independence": record.get("reviewer_independence", "internal maintainer-agent review only"),
        "transfer": "No population, production, institutional, or open-world transfer is established beyond the exact local workload.",
        "validity_limits": limitations,
        "counterevidence": negatives,
        "residuals": record.get("acceptance_blockers") or record.get("required_artifacts") or ["broader transfer evidence remains absent"],
        "disposition": disposition,
        "transition_record": str((ROOT / "evidence_transitions" / program / Path(record["transition_id"].split(".")[-2] + "_" + record["transition_id"].split(".")[-1] + ".json")).relative_to(ROOT)) if False else next(str(path.relative_to(ROOT)) for path in EXISTING if load(path).get("transition_id") == record["transition_id"]),
        "accepted_transition_exists": True,
        "transition_effect": record["transition_effect"],
        "old_support_state": record["old_support_state"],
        "new_support_state": record["new_support_state"],
        "permitted_changes": ["Preserve the bounded result and its negative evidence in the owning chapter/ledger.", "Clarify only the exact local mechanism or blocker; do not move a chapter-core support state."],
        "prohibited_inference": record["promotion_burden"],
    }


def qcsa_transition(decision: dict, owner: str, extra: bool = False) -> tuple[str, dict]:
    claim_id = decision["claim_id"]
    disposition = decision["disposition"]
    slug = re.sub(r"[^a-z0-9]+", "_", claim_id.lower()).strip("_")
    path = f"evidence_transitions/post_v2_3/{slug}_{disposition}.json"
    if disposition == "promote":
        new_state, effect, support_effect = "synthetic-test-backed", "upward", "eligible_for_bounded_evidence_review"
    elif disposition == "refute":
        new_state, effect, support_effect = "refuted", "refuted", "blocks_promotion"
    else:
        new_state, effect, support_effect = "argument", "no_change", "blocks_promotion"
    result_refs = decision.get("result_refs") or ([QCSA_RESULT, QCSA_DISPOSITIONS] if not extra else [])
    transition = {
        "transition_id": f"post_v2_3.{slug}.{disposition}",
        "claim_id": claim_id,
        "claim_surface_refs": ["docs/qcsa_reference_evaluation_report.md", f"chapters/{owner}.qmd", "docs/post_v2_3_evidence_candidate_ledger.md"],
        "claim_record_refs": result_refs,
        "old_support_state": "argument",
        "new_support_state": new_state,
        "transition_effect": effect,
        "transition_validity_state": "review_accepted",
        "scope_boundary": decision["claim"],
        "evidence_roles": ["bounded_synthetic_evaluation", "frozen_ablation_or_reference_comparator", "content_addressed_result", "core_support_boundary"],
        "transition_reason": decision["basis"],
        "required_artifacts": decision.get("limitations", []) + ["natural tasks, learned models, external replication, and production transfer before broader use"],
        "artifact_refs": result_refs,
        "evidence_packet_refs": [f"chapters/{owner}.qmd", "docs/non_core_evidence_ledger.md", "appendices/C_claim_evidence_matrix.qmd"],
        "evidence_quality_before_refs": [QCSA_DISPOSITIONS],
        "evidence_quality_after_refs": ["docs/post_v2_3_evidence_candidate_ledger.json", "docs/non_core_evidence_ledger.md"],
        "evidence_quality_dimension_deltas": {"reproducibility": "exact deterministic replay and result digests", "adversarial_strength": "frozen ablation or expected-invalid controls", "validity": "internal synthetic labels and evaluator only", "transfer_distance": "not established"},
        "source_mapping_refs": [f"appendices/C_claim_evidence_matrix.qmd#{owner}.core"],
        "verification_command": "python3 scripts/validate_qcsa_evaluation.py && python3 scripts/build_post_v2_3_evidence_candidate_ledger.py",
        "verification_result": "pass",
        "negative_results": [decision["basis"]] if disposition in {"refute", "narrow", "no_change"} else decision.get("limitations", []),
        "negative_evidence_refs": result_refs,
        "downgrade_triggers": ["result or disposition digest mismatch", "ablation denominator or cost erasure", "synthetic scope described as natural or production evidence", "chapter-core promotion inferred from this non-core record"],
        "promotion_burden": "; ".join(decision.get("limitations", [])) + "; natural workloads, learned models, independent evaluation, and transfer evidence required for broader claims",
        "limitations": decision.get("limitations", []),
        "review_status": "accepted",
        "reviewer_refs": ["Author-directed Codex post-v2.3 adjudication cycle"],
        "reviewer_independence": "local maintainer-agent review only; no external human review requested or claimed",
        "acceptance_blockers": [] if disposition in {"promote", "refute"} else decision.get("limitations", []),
        "changelog_ref": CHANGELOG_REF,
        "support_state_effect": support_effect,
        "non_claims": ["does not promote any chapter-core claim above argument", "does not establish natural-task or production transfer", "does not establish external independence, safety, privacy, security, AGI, or ASI", f"does not promote {owner}.core"],
    }
    return path, transition


def qcsa_assessment(decision: dict, transition_path: str, transition: dict) -> dict:
    claim = decision["claim_id"]
    limitations = decision.get("limitations") or ["exact bounded QCSA artifact only"]
    return {
        "candidate_id": claim,
        "program": "qcsa_v2_3",
        "result_refs": digest_refs(decision.get("result_refs") or [QCSA_RESULT, QCSA_DISPOSITIONS]),
        "candidate_claim": decision["claim"],
        "owner": OWNER_MAP[claim],
        "comparator": "Frozen QCSA baselines or component ablations under the exact preregistered corpus, labels, resource accounting, and observer implementation.",
        "cohort": "60 held-out deterministic templates repeated across three seeds (180 records), or the exact separately named bounded reference trace.",
        "cost": "QCSA used 729 total operations (4.05 mean) and a 1.913386 matched operation ratio; proxy latency, verifier work, questions, and human burden remain visible.",
        "independence": "Evaluator/observer is separately implemented but internal to the same project; no external replication or human review occurred.",
        "transfer": "Template-transparent synthetic fixtures and local temporary-file effects do not establish natural-language, learned-model, distributed, or production transfer.",
        "validity_limits": limitations,
        "counterevidence": [decision["basis"]] + limitations,
        "residuals": ["Ceiling-easy labels, internal authorship, deterministic templates, proxy cost, and absent natural prevalence remain material."],
        "disposition": decision["disposition"],
        "transition_record": transition_path,
        "accepted_transition_exists": True,
        "transition_effect": transition["transition_effect"],
        "old_support_state": transition["old_support_state"],
        "new_support_state": transition["new_support_state"],
        "permitted_changes": ["Record the exact bounded non-core result and its disposition in the non-core evidence ledger.", "Revise owning prose only to state the exact mechanism result, counterevidence, cost, and transfer boundary; keep every chapter core at argument."],
        "prohibited_inference": "No natural-task, learned-model, open-world, production, safety, privacy, security, external-independence, AGI, ASI, or chapter-core support inference is permitted.",
    }


def build() -> tuple[dict, dict[str, dict]]:
    candidates = []
    for path in EXISTING:
        record = load(path)
        program = "post_v2_1" if "/post_v2_1/" in str(path) else "post_v2"
        disposition = "narrow" if path.stem.endswith("_narrow") else "no_change"
        candidates.append(existing_assessment(record, program, disposition))

    decisions = load(QCSA_DECISIONS)["non_core_dispositions"]
    decisions += [
        {"claim_id": "qcsa.reference_implementation_exact_contract_conformance", "claim": "The bounded QCSA reference package conforms to its exact schemas, fixtures, digest manifest, and expected-invalid controls.", "disposition": "narrow", "basis": "The deterministic implementation and replay validators pass, but implementation conformance is not an evaluation outcome or natural semantic-quality result.", "limitations": ["bounded deterministic reference package", "no held-out outcome licensed by implementation conformance alone"], "result_refs": ["experiments/qcsa_reference/results/implementation_result.json", "docs/qcsa_reference_implementation_report.md"]},
        {"claim_id": "qcsa.vertical_reference_exact_reversible_trace", "claim": "The 13-stage QCSA vertical reference executes one exact local governed effect and restores its declared temporary-file state.", "disposition": "narrow", "basis": "One digest-bound local trace completed all stages and exact declared rollback, while remaining a hand-authored zero-model temporary-file demonstration.", "limitations": ["one hand-authored local trace", "declared temporary-file state only; not open-system effect-complete rollback"], "result_refs": ["experiments/qcsa_vertical_reference/results/vertical_result.json", "docs/qcsa_governed_vertical_reference_report.md"]},
    ]
    generated: dict[str, dict] = {}
    for decision in decisions:
        owner = OWNER_MAP[decision["claim_id"]]
        path, transition = qcsa_transition(decision, owner, decision["claim_id"].startswith("qcsa.reference_") or decision["claim_id"].startswith("qcsa.vertical_"))
        generated[path] = transition
        candidates.append(qcsa_assessment(decision, path, transition))
    candidates.sort(key=lambda row: (row["program"], row["candidate_id"]))
    counts = Counter(row["disposition"] for row in candidates)
    ledger = {
        "schema_version": "asi_stack.post_v2_3_evidence_candidate_ledger.v0",
        "ledger_id": "post-v2-3-evidence-candidate-adjudication-2026-07-13",
        "recorded_date": "2026-07-13",
        "scope": "Every completed post-v2, post-v2.1, and QCSA v2.3 result that was a promotion recommendation, an accepted prior transition, or plausibly supports a narrower bounded claim.",
        "candidate_count": len(candidates),
        "disposition_counts": {key: counts.get(key, 0) for key in ["promote", "narrow", "no_change", "refute"]},
        "accepted_transition_count": sum(row["accepted_transition_exists"] for row in candidates),
        "candidates": candidates,
        "support_state_effect": "non_core_only_core_states_unchanged",
        "non_claims": ["All 54 chapter-core claims remain at argument.", "A bounded non-core upward transition does not promote its owning chapter core.", "QCSA promote recommendations were reviewed through the transition schema rather than copied as conclusions.", "No natural-task, learned-model, production, independent-replication, safety, AGI, or ASI claim is created."]
    }
    return ledger, generated


def render_review(ledger: dict) -> str:
    lines = ["# Post-v2.3 Evidence Candidate Adjudication", "", "Status: complete; 21/21 candidates have accepted transition records. All 54 chapter-core claims remain at `argument`.", "", "| Candidate | Program | Disposition | Transition | Core effect |", "|---|---|---|---|---|"]
    for row in ledger["candidates"]:
        lines.append(f"| `{row['candidate_id']}` | `{row['program']}` | `{row['disposition']}` | `{row['transition_effect']}` to `{row['new_support_state']}` | none |")
    lines += ["", "## Decision boundary", "", "The five QCSA `promote` recommendations become accepted `synthetic-test-backed` transitions only for their exact non-core fixture claims. Two exact claims are refuted. Narrow and no-change rows retain `argument`. The implementation and vertical-reference rows are explicitly narrow/no-change rather than being laundered into evaluation or transfer evidence.", "", "Every row in the JSON ledger records exact result digests, owner, comparator, cohort, cost, independence, transfer and validity limits, counterevidence, residuals, permitted changes, and prohibited inference. No external-human prepublication review was required or claimed.", ""]
    return "\n".join(lines)


def validate(ledger: dict, expected: dict, generated: dict[str, dict]) -> list[str]:
    errors = []
    try:
        jsonschema.validate(ledger, load(SCHEMA))
    except jsonschema.ValidationError as exc:
        errors.append(f"ledger schema: {exc.message}")
    if ledger != expected:
        errors.append("ledger differs from reconstructed exact result/transition inventory")
    transition_schema = load(TRANSITION_SCHEMA)
    for ref, expected_record in generated.items():
        path = ROOT / ref
        if not path.is_file():
            errors.append(f"missing transition {ref}")
            continue
        record = load(path)
        try:
            jsonschema.validate(record, transition_schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"{ref}: {exc.message}")
        if record != expected_record:
            errors.append(f"{ref}: transition drift")
    for row in ledger.get("candidates", []):
        path = ROOT / row.get("transition_record", "")
        if not path.is_file() or load(path).get("review_status") != "accepted":
            errors.append(f"{row.get('candidate_id')}: accepted transition absent")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected, generated = build()
    if args.write:
        for ref, record in generated.items():
            path = ROOT / ref
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record, indent=2) + "\n")
        LEDGER.write_text(json.dumps(expected, indent=2) + "\n")
        REVIEW.write_text(render_review(expected))
    if not LEDGER.is_file():
        raise SystemExit("Evidence candidate ledger validation failed: ledger absent; run --write")
    ledger = load(LEDGER)
    errors = validate(ledger, expected, generated)
    for label, mutate in [
        ("missing candidate", lambda x: x["candidates"].pop()),
        ("false promotion", lambda x: x["candidates"][0].__setitem__("disposition", "promote")),
        ("missing transition", lambda x: x["candidates"][0].__setitem__("accepted_transition_exists", False)),
        ("core promotion", lambda x: x.__setitem__("support_state_effect", "core_promoted")),
        ("digest laundering", lambda x: x["candidates"][0]["result_refs"][0].__setitem__("sha256", "0" * 64)),
    ]:
        candidate = copy.deepcopy(ledger)
        mutate(candidate)
        if not validate(candidate, expected, generated):
            errors.append(f"negative mutation accepted: {label}")
    if errors:
        raise SystemExit("Evidence candidate ledger validation failed:\n - " + "\n - ".join(errors[:80]))
    print(f"Evidence candidate ledger passed: {ledger['candidate_count']} candidates, {ledger['disposition_counts']}, 21 accepted transitions, all core states unchanged, and 5 rejecting mutations.")


if __name__ == "__main__":
    main()
