#!/usr/bin/env python3
"""Update canonical Appendix C and per-chapter evidence-plan cells post-v2."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / "appendices/C_claim_evidence_matrix.qmd"
PLAN = ROOT / "docs/per_chapter_evidence_plan.md"

UPDATES = {
    "intent-to-execution-contracts": ("Command-contract fixtures, Lean semantic-interface crosswalk, and the post-v2 model-generated governed-work replay", "Extend the 16-run local plan/code and Git-worktree comparison toward deployed approval, sandbox, effect, and rollback services while preserving the zero-release and failed-rollback results.", "A broader deployed or externally reviewable intent-to-effect comparison preserves authority, observed effects, receipt/path reconciliation, residuals, useful throughput, and rollback under natural workloads."),
    "artifact-graphs-audit-logs-and-replay": ("Artifact graph harnesses, Theseus reports, and post-v2 content-addressed model/worktree route replays", "Extend the 16 content-addressed runs, observed paths, effect digests, residuals, and rollback records toward deployed audit reconstruction, verifier-quality, durability, and open-world revocation completeness.", "A deployed or externally reviewable artifact service reconstructs real work and revocation effects without erasing verifier limits, failed rollback, or residuals."),
    "resource-economics-and-token-budgets": ("Costed-route/resource fixtures plus post-v2 wall-time, token, candidate-operation, usefulness, harm, and governance-tax measurements", "Extend local Apple M1 and synthetic candidate-operation measurements toward production scheduler, serving, review-capacity, verification-tax, and cost-quality evidence.", "Production or externally reviewable workloads jointly report useful output, unsafe release, verification cost, latency, review burden, residuals, and displaced work."),
    "routing-heads-and-specialist-cores": ("Routing harness, MoE/MoECOT crosswalk, and post-v2 three-seed held-out specialist/generalist comparison", "Build a harder ambiguous workload that exercises fallback and abstention, trained-specialist interference, authority leases, and model-scale transfer; preserve the current zero-fallback coverage gap.", "Learned, rule, specialist, generalist, fallback, and abstention routes separate under ambiguous held-out work with matched cost, calibration, interference, residual, and authority records."),
    "governed-deliberation-and-test-time-scaling": ("Test-time-compute sources plus post-v2 adaptive/fixed/no-deliberation comparison with first/last hits and extra-compute harm", "Repeat the matched stopping study with language-model candidates, independent verifier-quality assessment, safety failures, latency, and transfer while retaining fixed-step harms.", "A language-model workload shows when verifier-gated stopping helps or harms relative to fixed and no deliberation under matched budgets and independently assessed verification."),
    "data-engines-continual-learning-and-unlearning": ("Data-admission/unlearning sources plus post-v2 real checkpoint mutation, poisoned-cohort exclusion, forgetting, and rollback campaign", "Extend the 1,200-example local policy workload toward real data admission, continual-learning comparisons, deletion propagation through checkpoints/adapters/caches/derivatives, privacy tests, and independent replay.", "A real governed data pipeline traces deletion and retained utility through every affected descendant and storage surface with contamination, privacy, rollback, and independent verification."),
    "policy-optimization-and-learning-from-feedback": ("Policy-optimization fixtures/literature plus post-v2 three-seed real parameter/checkpoint/output-causality campaign", "Add actual human/model feedback, reward-hacking probes, evaluator separation, deployment canaries, rollback, and retained-task measurement beyond the synthetic policy labels.", "A feedback-driven policy update improves held-out utility without reward laundering or hidden forgetting and survives independent evaluation, canary, rollback, and residual review."),
    "open-ended-improvement-engines": ("Open-ended-improvement sources plus the post-v2 fixed stopped four-arm mutation campaign", "Move from a fixed campaign to bounded task/candidate generation with evaluator evolution controls, archive diversity, independent qualification, stop authority, resources, failures, and admission decisions.", "A bounded open-ended campaign demonstrates useful novelty and transfer while preserving evaluator scope, archive negatives, resource limits, stop authority, and independent admission."),
    "recursive-self-improvement-boundaries": ("Safety-critical Lean/Theseus gates plus post-v2 real checkpoint mutation, exact rollback, and descendant invalidation at the transaction boundary", "Extend exact local rollback/invalidation toward self-proposed changes, protected-invariant deltas, independent evaluators, authority enforcement, canaries, monitor windows, and deployed recovery.", "A self-proposed real implementation change cannot widen authority or weaken protected invariants, and failed canaries roll back exact state while invalidating descendants under independent evaluation."),
}


def rewrite_table(path: Path, kind: str) -> None:
    output = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            output.append(line); continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if kind == "appendix" and len(cells) == 11:
            chapter = cells[1].strip("`")
            if chapter in UPDATES:
                lane, work, move = UPDATES[chapter]
                cells[6] = f"Post-v2 adjacent local evidence is recorded in the affected chapter and accepted no-change transition; core support remains argument. {lane}."
                cells[9] = work
                line = "| " + " | ".join(cells) + " |"
        elif kind == "plan" and len(cells) == 6:
            chapter = cells[1].strip("`")
            if chapter in UPDATES:
                lane, work, move = UPDATES[chapter]
                cells[2], cells[3], cells[5] = lane, work, move
                line = "| " + " | ".join(cells) + " |"
        output.append(line)
    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def main() -> None:
    rewrite_table(APPENDIX, "appendix")
    rewrite_table(PLAN, "plan")
    print("updated 9 Appendix C rows and 9 per-chapter evidence-plan rows")


if __name__ == "__main__":
    main()
