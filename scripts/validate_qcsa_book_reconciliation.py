#!/usr/bin/env python3
"""Validate the QCSA implementation/evaluation fold across book truth surfaces."""

from __future__ import annotations

import copy
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OWNERS = {
    "cognitive-compilation-and-semantic-ir",
    "virtual-context-abi",
    "claim-ledgers-and-belief-revision",
    "runtime-adapters-tool-permissions-and-human-approval",
    "inter-stack-protocols-identity-and-economic-exchange",
    "routing-heads-and-specialist-cores",
    "compact-generative-systems-and-residual-honesty",
    "data-engines-continual-learning-and-unlearning",
    "integrated-reference-architecture",
}
QCSA_CROSSWALK = "later repository adds a bounded local 12-lane implementation"
CHAPTERS = {owner: ROOT / "chapters" / f"{owner}.qmd" for owner in OWNERS}
DISPOSITIONS = ROOT / "claim_decisions/qcsa_reference_evaluation_dispositions.json"
RESULT = ROOT / "experiments/qcsa_reference/results/evaluation_results.json"
VERTICAL = ROOT / "experiments/qcsa_vertical_reference/results/vertical_result.json"
VECTORS = ROOT / "evidence_quality/core_claim_vectors.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCE_NOTE = ROOT / "sources/source_notes/qcsa_whitepaper.md"
APPENDIX = ROOT / "appendices/C_claim_evidence_matrix.qmd"
PLAN = ROOT / "docs/per_chapter_evidence_plan.md"
RESIDUALS = ROOT / "docs/post_v2_residual_ledger.md"
CHANGELOG = ROOT / "appendices/F_changelog.qmd"
REPORT = ROOT / "docs/qcsa_implementation_evidence_reconciliation.md"
ACTIVE_STATUS = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
MAINTENANCE_STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
PROOF_MANIFEST = ROOT / "proofs/proof_manifest.json"
HISTORICAL_55TH_CHAPTER = "replaceable-cognitive-substrates-beyond-transformer-monoculture"
ACTIVE_MAINTENANCE_ROADMAP = "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def snapshot() -> dict[str, Any]:
    return {
        "chapters": {owner: text(path) for owner, path in CHAPTERS.items()},
        "dispositions": load(DISPOSITIONS),
        "result": load(RESULT),
        "vertical": load(VERTICAL),
        "vectors": load(VECTORS),
        "structure": load(STRUCTURE),
        "source_note": text(SOURCE_NOTE),
        "appendix": text(APPENDIX),
        "plan": text(PLAN),
        "residuals": text(RESIDUALS),
        "changelog": text(CHANGELOG),
        "report": text(REPORT),
        "historical_status": load(ACTIVE_STATUS),
        "maintenance_status": load(MAINTENANCE_STATUS),
        "proof_manifest": load(PROOF_MANIFEST),
    }


def semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    chapters = data["chapters"]
    if set(chapters) != OWNERS:
        errors.append("the nine exact QCSA chapter owners are not loaded")
    crosswalk = QCSA_CROSSWALK
    stale = "Conceptual architecture only; no implementation"
    for owner in sorted(OWNERS):
        chapter = chapters.get(owner, "")
        if "QCSA" not in chapter or crosswalk not in chapter:
            errors.append(f"{owner} lacks the reconciled QCSA evidence/crosswalk")
        if "core claim remains at `argument`" not in chapter and "claim remains at `argument`" not in chapter:
            errors.append(f"{owner} lacks an explicit argument-state boundary")
        if stale in chapter:
            errors.append(f"{owner} retains the stale no-implementation crosswalk")
    for owner in {"routing-heads-and-specialist-cores", "compact-generative-systems-and-residual-honesty"}:
        if "1.913386" not in chapters.get(owner, ""):
            errors.append(f"{owner} hides the failed resource ratio")
    if "Removing active questions" not in chapters.get("cognitive-compilation-and-semantic-ir", ""):
        errors.append("cognitive compiler chapter hides the active-question null result")

    dispositions = data["dispositions"]
    non_core = dispositions.get("non_core_dispositions", [])
    counts = Counter(row.get("disposition") for row in non_core)
    if counts != Counter({"promote": 5, "narrow": 2, "refute": 2, "no_change": 1}):
        errors.append("non-core QCSA disposition accounting drifted")
    core = dispositions.get("core_claim_decisions", [])
    if {row.get("chapter_id") for row in core} != OWNERS:
        errors.append("nine exact QCSA core decisions are not present")
    if any(row.get("decision") != "no_change" or row.get("current_support_state") != "argument" or row.get("support_state_effect") != "none" for row in core):
        errors.append("a QCSA chapter-core decision moves above argument")
    if dispositions.get("summary", {}).get("support_state_changes") != 0 or dispositions.get("support_state_effect") != "none":
        errors.append("QCSA dispositions claim an automatic support-state change")

    result = data["result"]
    rules = result.get("decision_rules", {})
    if rules.get("overall_disposition") != "narrow_no_matched_advantage_claim" or rules.get("advantage_gate_pass") is not False or rules.get("resource_gate_pass") is not False or rules.get("operation_ratio") != 1.913386:
        errors.append("exact failed advantage/resource disposition drifted")
    if result.get("aggregate", {}).get("qcsa_without_active_questions", {}).get("task_decision_accuracy") != 1.0:
        errors.append("active-question null result was erased")

    vertical = data["vertical"]
    if len(vertical.get("stage_order", [])) != 13 or len(vertical.get("adversarial_matrix", [])) != 10:
        errors.append("vertical 13-stage/10-attack result is missing")
    if not vertical.get("migration_and_rollback", {}).get("byte_exact_rollback") or vertical.get("support_state_effect") != "none":
        errors.append("vertical exact rollback or no-promotion boundary drifted")

    source_note = data["source_note"]
    for phrase in ["Local Implementation And Evaluation Update (2026-07-13)", "1.913386", "N2", "do not warrant a standalone QCSA chapter"]:
        if phrase not in source_note:
            errors.append(f"QCSA source note lacks repository/source boundary: {phrase}")
    appendix = data["appendix"]
    if "QCSA P2–P3 Evidence Reconciliation (2026-07-13)" not in appendix:
        errors.append("Appendix C lacks QCSA reconciliation overlay")
    for owner in OWNERS:
        if f"| `{owner}` |" not in appendix:
            errors.append(f"Appendix C overlay lacks {owner}")
    if "automatic support-state transition has occurred" not in appendix:
        errors.append("Appendix C lacks automatic-transition boundary")
    plan = data["plan"]
    if "QCSA P2–P3 Completion Overlay" not in plan:
        errors.append("per-chapter plan lacks QCSA completion overlay")
    for owner in OWNERS:
        if f"| `{owner}` |" not in plan:
            errors.append(f"QCSA evidence plan lacks {owner}")
    residuals = data["residuals"]
    for index in range(1, 9):
        if f"`QCSA-{index:02d}`" not in residuals:
            errors.append(f"residual ledger lacks QCSA-{index:02d}")
    if "Implement, evaluate, and vertically integrate QCSA" not in data["changelog"]:
        errors.append("changelog lacks QCSA completion transaction")

    vectors = data["vectors"]
    structure = data["structure"]
    raw_chapter_rows = [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    chapter_rows = [chapter for chapter in raw_chapter_rows if isinstance(chapter, dict)]
    chapter_count = len(raw_chapter_rows)
    chapter_ids = {chapter.get("id") for chapter in chapter_rows}
    if len(chapter_rows) != chapter_count or len(chapter_ids) != chapter_count:
        errors.append("live manifest contains malformed entries or duplicate chapter identifiers")
    vector_rows = vectors.get("vectors", [])
    vector_summary = vectors.get("summary", {})
    if (
        len(vector_rows) != chapter_count
        or vector_summary.get("vector_count") != chapter_count
        or vector_summary.get("summary_support_states") != {"argument": chapter_count}
        or vector_summary.get("automatic_support_state_changes") != 0
        or any(row.get("summary_support_state") != "argument" for row in vector_rows)
    ):
        errors.append("evidence-quality vector summary drifted")
    vector_by_claim = {row.get("claim_id"): row for row in vector_rows}
    for owner in OWNERS:
        vector = vector_by_claim.get(f"{owner}.core", {})
        refs = json.dumps(vector, sort_keys=True)
        if vector.get("summary_support_state") != "argument" or "qcsa_reference_evaluation_dispositions.json" not in refs or "qcsa_vertical_reference/results/vertical_result.json" not in refs:
            errors.append(f"evidence-quality vector lacks bounded QCSA refs/boundary: {owner}")
        if vector.get("dimensions", {}).get("transfer_distance", {}).get("state") != "not_established":
            errors.append(f"QCSA vector overstates transfer: {owner}")

    historical_status = data["historical_status"]
    historical_activation = historical_status.get("activation_baseline", {})
    if historical_activation.get("active_chapter_count") != 54 or historical_activation.get("proof_target_count") != 298:
        errors.append("historical 54-chapter QCSA reconciliation baseline drifted")
    historical_expansion = historical_status.get("structural_expansion_contract", {})
    if (
        historical_expansion.get("live_chapter_count") != 55
        or historical_expansion.get("chapter_id") != HISTORICAL_55TH_CHAPTER
        or historical_expansion.get("support_state_effect") != "none"
    ):
        errors.append("historical authorized 55th-chapter expansion drifted")
    maintenance_status = data["maintenance_status"]
    activation_truth = maintenance_status.get("activation_truth", {})
    structural_tranche = maintenance_status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    first_tranche = structural_tranche.get("first_tranche", {})
    admitted_chapter_ids = set(first_tranche.get("candidate_ids", []))
    if (
        maintenance_status.get("status") != "active"
        or maintenance_status.get("roadmap_path") != ACTIVE_MAINTENANCE_ROADMAP
        or activation_truth.get("live_working_chapter_count") != chapter_count
        or activation_truth.get("chapter_core_argument_count") != chapter_count
        or activation_truth.get("chapter_core_promotion_count") != 0
        or structural_tranche.get("current_manifest_chapter_count") != chapter_count
        or first_tranche.get("manifest_admitted_count") != len(admitted_chapter_ids)
        or chapter_count != historical_expansion.get("live_chapter_count") + len(admitted_chapter_ids)
        or not admitted_chapter_ids.issubset(chapter_ids)
    ):
        errors.append("current live chapters escaped later manifest-admitted structural authority")
    proof_manifest = data["proof_manifest"]
    proof_records = proof_manifest.get("records", [])
    proof_status_counts = proof_manifest.get("status_counts", {})
    record_status_counts = Counter(row.get("status") for row in proof_records)
    current_proof_count = proof_manifest.get("proof_target_count")
    historical_proof_count = historical_activation.get("proof_target_count")
    added_proof_count = (
        current_proof_count - historical_proof_count
        if isinstance(current_proof_count, int) and isinstance(historical_proof_count, int)
        else -1
    )
    planned_records = [row for row in proof_records if row.get("status") == "planned"]
    later_admitted_records = [
        row for row in proof_records if row.get("chapter_id") in admitted_chapter_ids
    ]
    later_implemented_records = [
        row for row in later_admitted_records if row.get("status") == "implemented"
    ]
    if (
        current_proof_count != activation_truth.get("proof_target_count")
        or current_proof_count != len(proof_records)
        or proof_status_counts != dict(record_status_counts)
        or len(later_admitted_records) != added_proof_count
        or {row.get("chapter_id") for row in later_admitted_records} != admitted_chapter_ids
        or proof_status_counts
        != {
            "implemented": historical_proof_count + len(later_implemented_records),
            "planned": len(planned_records),
        }
        or len(planned_records) + len(later_implemented_records) != added_proof_count
        or not {row.get("chapter_id") for row in planned_records}.issubset(admitted_chapter_ids)
    ):
        errors.append("current proof additions escaped historical baseline or admitted chapters")
    if any(
        "qcsa" in f"{chapter.get('id', '')} {chapter.get('file', '')}".casefold()
        for part in data["structure"].get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ):
        errors.append("a standalone QCSA chapter was added")
    for phrase in ["P1–P4 complete", "five bounded `promote` recommendations", "All nine chapter-core decisions are `no_change`", "adds no chapter", "1.913386"]:
        if phrase not in data["report"]:
            errors.append(f"reconciliation report lacks required decision: {phrase}")
    return errors


def negative_controls(base: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(label: str, fn: Callable[[dict[str, Any]], None]) -> None:
        value = copy.deepcopy(base)
        fn(value)
        mutations.append((label, value))

    owner = "cognitive-compilation-and-semantic-ir"
    mutate("chapter evidence erased", lambda d: d["chapters"].__setitem__(owner, d["chapters"][owner].replace("QCSA", "ERASED")))
    mutate("crosswalk regressed", lambda d: d["chapters"].__setitem__(owner, d["chapters"][owner].replace(QCSA_CROSSWALK, "Conceptual architecture only; no implementation")))
    mutate("resource failure hidden", lambda d: d["chapters"].__setitem__("routing-heads-and-specialist-cores", d["chapters"]["routing-heads-and-specialist-cores"].replace("1.913386", "1.000000")))
    mutate("active-question null hidden", lambda d: d["chapters"].__setitem__(owner, d["chapters"][owner].replace("Removing active questions", "Ignoring a removed mechanism")))
    mutate("core promoted", lambda d: d["dispositions"]["core_claim_decisions"][0].__setitem__("current_support_state", "prototype-backed"))
    mutate("automatic transition", lambda d: d["dispositions"]["summary"].__setitem__("support_state_changes", 5))
    mutate("matched advantage promoted", lambda d: d["result"]["decision_rules"].__setitem__("overall_disposition", "promote"))
    mutate("resource gate promoted", lambda d: d["result"]["decision_rules"].__setitem__("resource_gate_pass", True))
    mutate("question result rewritten", lambda d: d["result"]["aggregate"]["qcsa_without_active_questions"].__setitem__("task_decision_accuracy", 0.0))
    mutate("vertical rollback erased", lambda d: d["vertical"]["migration_and_rollback"].__setitem__("byte_exact_rollback", False))
    mutate("appendix overlay erased", lambda d: d.__setitem__("appendix", d["appendix"].replace("QCSA P2–P3 Evidence Reconciliation (2026-07-13)", "ERASED")))
    mutate("evidence plan owner erased", lambda d: d.__setitem__("plan", d["plan"].replace("| `virtual-context-abi` |", "| `erased-owner` |")))
    mutate("residual erased", lambda d: d.__setitem__("residuals", d["residuals"].replace("`QCSA-08`", "`ERASED`")))
    mutate("vector transfer promoted", lambda d: next(row for row in d["vectors"]["vectors"] if row["claim_id"] == f"{owner}.core")["dimensions"]["transfer_distance"].__setitem__("state", "established"))
    mutate("new QCSA chapter", lambda d: d["structure"]["parts"][0]["chapters"].append("chapters/qcsa.qmd"))
    mutate("proof target invention", lambda d: d["proof_manifest"].__setitem__("proof_target_count", 307))
    mutate("planned proof escapes admitted chapter", lambda d: next(row for row in d["proof_manifest"]["records"] if row.get("status") == "planned").__setitem__("chapter_id", owner))
    mutate("current authority promotion", lambda d: d["maintenance_status"]["activation_truth"].__setitem__("chapter_core_promotion_count", 1))
    failures = []
    for label, value in mutations:
        if not semantic_errors(value):
            failures.append(f"negative control accepted: {label}")
    return failures


def main() -> None:
    required = [*CHAPTERS.values(), DISPOSITIONS, RESULT, VERTICAL, VECTORS, STRUCTURE, SOURCE_NOTE, APPENDIX, PLAN, RESIDUALS, CHANGELOG, REPORT, ACTIVE_STATUS, MAINTENANCE_STATUS, PROOF_MANIFEST]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA reconciliation artifacts: " + ", ".join(missing))
    data = snapshot()
    errors = semantic_errors(data)
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("QCSA book reconciliation validation failed:\n - " + "\n - ".join(errors))
    live_chapter_count = sum(
        len(part.get("chapters", []))
        for part in data["structure"].get("parts", [])
    )
    proof_manifest = data["proof_manifest"]
    print(f"QCSA book reconciliation passed: 9 existing chapter owners, 5 bounded review candidates, 2 narrowed claims, 2 exact refutations, 1 no-change transfer boundary, 8 explicit residuals, preserved 54-chapter/298-target historical baseline and authorized 55th-chapter expansion, {live_chapter_count} live core claims still at argument, {proof_manifest.get('proof_target_count')} current proof targets constrained to {proof_manifest.get('status_counts', {}).get('implemented')} implemented plus {proof_manifest.get('status_counts', {}).get('planned')} planned on later admitted chapters, no standalone QCSA chapter, and 18 rejecting mutations.")


if __name__ == "__main__":
    main()
