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
    }


def semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    chapters = data["chapters"]
    if set(chapters) != OWNERS:
        errors.append("the nine exact QCSA chapter owners are not loaded")
    crosswalk = "The later repository adds a bounded local 12-lane implementation"
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
    for phrase in ["Local Implementation And Evaluation Update (2026-07-13)", "1.913386", "active-question value was refuted", "do not warrant a standalone QCSA chapter"]:
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
    if vectors.get("summary", {}).get("vector_count") != 54 or vectors.get("summary", {}).get("automatic_support_state_changes") != 0:
        errors.append("evidence-quality vector summary drifted")
    vector_by_claim = {row.get("claim_id"): row for row in vectors.get("vectors", [])}
    for owner in OWNERS:
        vector = vector_by_claim.get(f"{owner}.core", {})
        refs = json.dumps(vector, sort_keys=True)
        if vector.get("summary_support_state") != "argument" or "qcsa_reference_evaluation_dispositions.json" not in refs or "qcsa_vertical_reference/results/vertical_result.json" not in refs:
            errors.append(f"evidence-quality vector lacks bounded QCSA refs/boundary: {owner}")
        if vector.get("dimensions", {}).get("transfer_distance", {}).get("state") != "not_established":
            errors.append(f"QCSA vector overstates transfer: {owner}")

    chapter_count = sum(len(part.get("chapters", [])) for part in data["structure"].get("parts", []))
    if chapter_count != 54:
        errors.append("chapter count changed while folding QCSA")
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
    mutate("crosswalk regressed", lambda d: d["chapters"].__setitem__(owner, d["chapters"][owner].replace("The later repository adds a bounded local 12-lane implementation", "Conceptual architecture only; no implementation")))
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
    failures = []
    for label, value in mutations:
        if not semantic_errors(value):
            failures.append(f"negative control accepted: {label}")
    return failures


def main() -> None:
    required = [*CHAPTERS.values(), DISPOSITIONS, RESULT, VERTICAL, VECTORS, STRUCTURE, SOURCE_NOTE, APPENDIX, PLAN, RESIDUALS, CHANGELOG, REPORT]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA reconciliation artifacts: " + ", ".join(missing))
    data = snapshot()
    errors = semantic_errors(data)
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("QCSA book reconciliation validation failed:\n - " + "\n - ".join(errors))
    print("QCSA book reconciliation passed: 9 existing chapter owners, 5 bounded review candidates, 2 narrowed claims, 2 exact refutations, 1 no-change transfer boundary, 8 explicit residuals, 54 core claims still at argument, no new chapter, and 15 rejecting mutations.")


if __name__ == "__main__":
    main()
