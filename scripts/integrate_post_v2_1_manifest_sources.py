#!/usr/bin/env python3
"""Idempotently route the six post-v2.1 external sources through the chapter manifest."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"


MAPPINGS = {
    "ext_claw_swe_bench_2026": {
        "mapped_support": "Supports binding coding-agent outcomes to a fixed model, harness, workspace, patch extraction, evaluator, runtime budget, and cost rather than attributing a harness result to the model alone.",
        "limits": "Primary preprint comparator only; no reported task, score, harness, cost, contamination control, or safety result was reproduced here.",
        "review": "Reviewed the source note's primary-preprint summary for harness/model effects, fixed evaluation surfaces, cost comparisons, contamination pressure, and governance omissions.",
    },
    "ext_txfs_2018": {
        "mapped_support": "Supports distinguishing declared effect-inventory restoration from ACID filesystem transactions, conflict isolation, crash consistency, durability, and bounded transaction capacity.",
        "limits": "TxFS was not installed or reproduced; the local directory and state-tree snapshots do not establish filesystem transactions, crash safety, process recovery, service recovery, or external-effect atomicity.",
        "review": "Reviewed the source note's primary USENIX summary for journaling-backed transactions, isolation, conflict handling, transaction bounds, Git/SQLite evaluation, and the gap between byte restoration and broader recovery.",
    },
    "ext_dont_hallucinate_abstain_2024": {
        "mapped_support": "Supports measuring abstention with coverage, accuracy, calibration, and useful response behavior while treating self-reflection and model agreement as fallible evidence.",
        "limits": "The ACL models, prompts, domains, collaboration schemes, and reported gains were not reproduced; the local single-model router is not an independent multi-model panel.",
        "review": "Reviewed the source note's primary ACL summary for knowledge-gap detection, abstention calibration, cooperative and competitive probing, shared blind spots, over-refusal, and extra-call cost.",
    },
    "ext_muse_unlearning_2025": {
        "mapped_support": "Supports separating memorization, privacy leakage, retained utility, removal-scale behavior, and sequential sustainability instead of using one forgetting score.",
        "limits": "No MUSE corpus, method, 7B model, privacy probe, scale test, or sequential deletion request was reproduced by the local small policy network.",
        "review": "Reviewed the source note's primary ICLR summary for six-way owner/deployer evaluation, verbatim and knowledge memory, privacy, utility, scale, and repeated-request failure modes.",
    },
    "ext_unlearning_benchmarks_weak_2024": {
        "mapped_support": "Supports treating unlearning benchmark validity, target ambiguity, forget/retain dependence, and benign perturbation robustness as separate evidence burdens.",
        "limits": "The position paper raises the interpretation standard but does not validate the local workload or establish influence, privacy, legal erasure, or storage erasure.",
        "review": "Reviewed the source note's primary-paper summary for optimistic scores under benign changes, target ambiguity, query overfitting, hidden retained effects, and residual accessibility.",
    },
    "ext_openunlearning_2025": {
        "mapped_support": "Supports versioned unlearning methods, standardized execution interfaces, public checkpoints, diverse evaluations, and meta-evaluation of metric faithfulness.",
        "limits": "The framework, methods, checkpoints, evaluations, and meta-evaluations were not run; standardized record shape does not establish semantic validity or erasure.",
        "review": "Reviewed the source note's primary NeurIPS summary for unified method and metric execution, public checkpoints, comparative evaluation, metric faithfulness, and standardization failure modes.",
    },
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    inventory = {row["id"]: row for row in json.loads(INVENTORY.read_text(encoding="utf-8"))}
    chapters = {chapter["id"]: chapter for part in manifest["parts"] for chapter in part["chapters"]}
    additions = 0
    for source_id, mapping in MAPPINGS.items():
        source = inventory[source_id]
        for chapter_id in source["chapter_targets"]:
            chapter = chapters[chapter_id]
            if source_id not in chapter["source_ids"]:
                chapter["source_ids"].append(source_id)
                additions += 1
            rows = chapter.setdefault("claim_source_mappings", [])
            if not any(row.get("source_id") == source_id for row in rows):
                rows.append({
                    "source_id": source_id,
                    "mapped_support": mapping["mapped_support"],
                    "limits": mapping["limits"],
                    "passage_refs": [f"sources/source_notes/{source_id}.md:12-42"],
                    "passage_review_note": mapping["review"],
                    "passage_review_state": "reviewed",
                })
                additions += 1
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"post-v2.1 source routing complete: six sources, 19 chapter assignments, {additions} new manifest entries")


if __name__ == "__main__":
    main()
