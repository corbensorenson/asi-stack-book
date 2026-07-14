#!/usr/bin/env python3
"""Install the passage-reviewed post-v2.3 P2 source mappings.

The integration is deliberately idempotent.  It adds only sources that change
an interface, failure boundary, objection, or evidence design; it does not use
citation count as an acceptance criterion.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "sources/source_inventory.json"
STRUCTURE = ROOT / "book_structure.json"


RECORDS = [
    {
        "id": "ext_faithfulness_information_flow_2026",
        "title": "Faithfulness as Information Flow: Evaluating and Training Faithful Chain-of-Thought Reasoning",
        "priority": "external_literature",
        "layer": "reasoning_trace_faithfulness",
        "chapter_targets": [
            "artifact-graphs-audit-logs-and-replay",
            "adversarial-evaluation-sandbagging-and-training-time-deception",
            "governed-deliberation-and-test-time-scaling",
            "policy-optimization-and-learning-from-feedback",
        ],
        "url": "https://arxiv.org/abs/2605.24286",
        "notes": "Primary 2026 comparator that separates chain-of-thought sufficiency, completeness, and interventional necessity, demonstrates prompt-to-answer shortcuts and transparent reward-hacking diagnostics, and documents low-entropy and reference-model limits. It does not make a reasoning transcript an authoritative receipt or establish local monitorability.",
        "source_type": "preprint",
        "arxiv_id": "2605.24286",
        "published": "2026-05-22",
        "updated": "2026-05-22",
        "citation_label": "Jia, Benton, and Easley (2026), Faithfulness as Information Flow",
        "doi": "10.48550/arXiv.2605.24286",
    },
    {
        "id": "ext_monitorbench_2026",
        "title": "MonitorBench: A Comprehensive Benchmark for Chain-of-Thought Monitorability in Large Language Models",
        "priority": "external_literature",
        "layer": "reasoning_trace_monitorability_evaluation",
        "chapter_targets": [
            "scalable-oversight-and-adversarial-ai-control",
            "adversarial-evaluation-sandbagging-and-training-time-deception",
        ],
        "url": "https://arxiv.org/abs/2603.28590",
        "notes": "Primary open benchmark comparator with 1,514 instances across 19 tasks and seven categories plus two stress-test settings; its reported capability/monitorability relation and up-to-30-percent degradation motivate held-out trace-action stress tests. The benchmark does not establish local monitoring quality, causal trace faithfulness, or safety.",
        "source_type": "preprint",
        "arxiv_id": "2603.28590",
        "published": "2026-03-30",
        "updated": "2026-04-02",
        "citation_label": "Wang et al. (2026), MonitorBench",
        "doi": "10.48550/arXiv.2603.28590",
    },
    {
        "id": "ext_v_jepa_2_2025",
        "title": "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning",
        "priority": "external_literature",
        "layer": "latent_world_models_and_model_predictive_control",
        "chapter_targets": [
            "mathematical-and-search-substrates",
            "planning-as-a-control-layer",
            "data-engines-continual-learning-and-unlearning",
            "integrated-reference-architecture",
        ],
        "url": "https://arxiv.org/abs/2506.09985",
        "notes": "Primary empirical comparator for action-free latent video pretraining, a small action-conditioned predictor, and model-predictive control. Camera sensitivity, autoregressive error accumulation, action-search cost, image-goal assumptions, and representation-bounded capability remain explicit limits; no local world model or robot-control result is established.",
        "source_type": "preprint",
        "arxiv_id": "2506.09985",
        "published": "2025-06-11",
        "updated": "2026-04-26",
        "citation_label": "Assran et al. (2025), V-JEPA 2",
        "doi": "10.48550/arXiv.2506.09985",
    },
    {
        "id": "ext_embedded_agency_2019",
        "title": "Embedded Agency",
        "priority": "external_literature",
        "layer": "embedded_agency_foundations",
        "chapter_targets": [
            "asi-is-a-stack-not-a-model",
            "constitutional-alignment-substrate",
            "recursive-self-improvement-boundaries",
            "evidence-states-and-claim-discipline",
            "integrated-reference-architecture",
        ],
        "url": "https://arxiv.org/abs/1902.09469",
        "notes": "Primary informal survey of the obstacles that arise when agents are physical parts of the worlds they model, must use smaller internal models, and reason about modifiable internal parts. It supplies a foundations boundary; the book's finite records, authority ceilings, and proofs do not solve embedded agency.",
        "source_type": "preprint",
        "arxiv_id": "1902.09469",
        "published": "2019-02-25",
        "updated": "2019-02-25",
        "citation_label": "Demski and Garrabrant (2019), Embedded Agency",
        "doi": "10.48550/arXiv.1902.09469",
    },
]


MAPPINGS = {
    "artifact-graphs-audit-logs-and-replay": {
        "source_id": "ext_faithfulness_information_flow_2026",
        "mapped_support": "Separates a plausible reasoning transcript from causal reliance by distinguishing sufficiency, completeness, and interventional necessity; this sharpens the artifact graph's private-reasoning, reported-rationale, action-trace, receipt, and authoritative-effect boundaries.",
        "limits": "The paper's metrics and training interventions are model- and task-bounded; they do not make a chain of thought a receipt or prove local record-reality faithfulness.",
        "passage_refs": ["arXiv:2605.24286v1, Sections 1 and 3, HTML lines 76-95 and 109-139", "arXiv:2605.24286v1, Sections 4 and 6.3, HTML lines 140-183 and 244-252", "arXiv:2605.24286v1, Limitations, HTML lines 333-345"],
    },
    "governed-deliberation-and-test-time-scaling": {
        "source_id": "ext_faithfulness_information_flow_2026",
        "mapped_support": "Provides a causal-information-flow objection to treating longer or more plausible deliberation traces as faithful, and supplies sufficiency, completeness, and necessity as separate evaluation targets.",
        "limits": "The reported interventions do not establish that any ASI Stack deliberation route is faithful, useful, or safe, and transcript inspection alone cannot establish necessity.",
        "passage_refs": ["arXiv:2605.24286v1, Sections 1 and 3, HTML lines 76-95 and 109-139", "arXiv:2605.24286v1, Section 4, HTML lines 140-183"],
    },
    "policy-optimization-and-learning-from-feedback": {
        "source_id": "ext_faithfulness_information_flow_2026",
        "mapped_support": "Shows that reward improvement can coexist with shortcut use and under-verbalized reward hacking, and tests update-time interventions that change information flow without changing rollout rewards.",
        "limits": "The intervention results are bounded to the reported arithmetic, code-repair, and DAPO-Math settings; they do not validate local policy optimization or eliminate reward hacking.",
        "passage_refs": ["arXiv:2605.24286v1, Sections 5-6.3, HTML lines 184-252", "arXiv:2605.24286v1, Limitations, HTML lines 333-345"],
    },
    "adversarial-evaluation-sandbagging-and-training-time-deception": {
        "source_id": "ext_faithfulness_information_flow_2026",
        "mapped_support": "Supplies trace/action inconsistency controls and the boundary that a transcript may correlate with an answer without being causally necessary, including a reward-hackable code-repair setting.",
        "limits": "The study is not evidence that a local model sandbags or deceives, and its diagnostics have low-entropy and reference-model confounds.",
        "passage_refs": ["arXiv:2605.24286v1, Sections 3-4, HTML lines 109-183", "arXiv:2605.24286v1, Section 6.3, HTML lines 244-252", "arXiv:2605.24286v1, Limitations, HTML lines 333-345"],
    },
    "scalable-oversight-and-adversarial-ai-control": {
        "source_id": "ext_monitorbench_2026",
        "mapped_support": "Provides a held-out, multi-task monitorability benchmark and adversarial stress-test design showing that visible reasoning can become less monitorable under pressure and that stronger capability does not imply better monitorability.",
        "limits": "Reported benchmark associations do not establish causal faithfulness, local oversight quality, model safety, or a general law across future systems.",
        "passage_refs": ["arXiv:2603.28590v2, Abstract and Introduction, HTML lines 105-120", "arXiv:2603.28590v2, benchmark and stress-test design sections", "arXiv:2603.28590v2, limitations section"],
    },
}


def add_mapping(chapter: dict, mapping: dict) -> None:
    sid = mapping["source_id"]
    if sid not in chapter["source_ids"]:
        chapter["source_ids"].append(sid)
    rows = chapter.setdefault("claim_source_mappings", [])
    record = {
        **mapping,
        "passage_review_state": "reviewed",
        "passage_review_note": "Primary-source passages were reviewed for the stated comparator contribution and limits; no local implementation, reproduction, safety result, or support-state promotion is inferred.",
    }
    for index, row in enumerate(rows):
        if row.get("source_id") == sid:
            rows[index] = record
            return
    rows.append(record)


def add_simple_mapping(chapter: dict, sid: str, support: str, limits: str, refs: list[str]) -> None:
    add_mapping(chapter, {"source_id": sid, "mapped_support": support, "limits": limits, "passage_refs": refs})


def main() -> None:
    inventory = json.loads(INVENTORY.read_text())
    by_id = {row["id"]: row for row in inventory}
    for record in RECORDS:
        by_id[record["id"]] = record
    existing_order = [row["id"] for row in inventory if row["id"] not in {r["id"] for r in RECORDS}]
    inventory = [by_id[sid] for sid in existing_order] + RECORDS

    structure = json.loads(STRUCTURE.read_text())
    chapters = {chapter["id"]: chapter for part in structure["parts"] for chapter in part["chapters"]}
    for cid, mapping in MAPPINGS.items():
        add_mapping(chapters[cid], mapping)
    add_simple_mapping(
        chapters["adversarial-evaluation-sandbagging-and-training-time-deception"],
        "ext_monitorbench_2026",
        "Adds a multi-task held-out monitorability benchmark and adversarial stress-test design, complementing causal trace/action inconsistency controls with cross-task monitor degradation evidence.",
        "The reported benchmark relations do not prove causal trace faithfulness, local deception, evaluator quality, safety, or a general capability/monitorability law.",
        ["arXiv:2603.28590v2, Abstract and Introduction, HTML lines 105-120", "arXiv:2603.28590v2, benchmark and stress-test design sections", "arXiv:2603.28590v2, limitations section"],
    )

    vjepa_support = {
        "mathematical-and-search-substrates": "Adds a concrete latent-prediction architecture family to the substrate adoption gate: action-free representation learning, an action-conditioned predictor, and explicit separation between structural design and capability evidence.",
        "planning-as-a-control-layer": "Provides a concrete model-predictive-control comparator that scores candidate action sequences in learned representation space and replans from observations.",
        "data-engines-continual-learning-and-unlearning": "Shows why world-model data lineage must separate action-free pretraining, action-conditioned adaptation, predictor versions, and error/residual records.",
        "integrated-reference-architecture": "Supplies the external predictive-state-to-planning interface for a governed world-model lane while preserving camera, search-cost, representation, and sim-to-real residuals.",
    }
    for cid, support in vjepa_support.items():
        add_simple_mapping(chapters[cid], "ext_v_jepa_2_2025", support, "The reported video and robot results do not establish local model quality, causal understanding, safe control, transfer, deployment, or an ASI Stack result.", ["arXiv:2506.09985, Abstract and Sections 1-3, HTML lines 128-175", "arXiv:2506.09985, planning results and limitations, HTML lines 368-396"])

    embedded_support = {
        "asi-is-a-stack-not-a-model": "Provides a foundations-level objection to a clean agent/environment boundary and motivates explicit ownership of internal models, subcomponents, and self-reference limits.",
        "constitutional-alignment-substrate": "Shows why corrigibility and alignment cannot assume an external, fully informed agent model when the system and its modifiable parts are embedded in the governed world.",
        "recursive-self-improvement-boundaries": "Grounds the boundary that a self-modifying system reasons about itself with models smaller than the world and may contain parts with divergent objectives.",
        "evidence-states-and-claim-discipline": "Motivates separating finite record-level guarantees from claims about the complete embedded agent, environment, self-model, or future descendants.",
        "integrated-reference-architecture": "Supplies the open-world foundations residual beneath the finite reference trace: the stack is inside the world it records and cannot treat its own ledger as an external omniscient model.",
    }
    for cid, support in embedded_support.items():
        add_simple_mapping(chapters[cid], "ext_embedded_agency_2019", support, "The paper is an informal obstacle survey, not a solved theory; the ASI Stack's finite records and proofs do not solve logical uncertainty, self-reference, robust delegation, subsystem alignment, or open-world embedded agency.", ["arXiv:1902.09469v1, Abstract", "Demski and Garrabrant (2018/2019), Embedded Agency full-text sections on embedded world-models, robust delegation, and subsystem alignment"])

    INVENTORY.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n")
    print("Integrated 4 P2 source records and 14 claim-specific chapter mappings.")


if __name__ == "__main__":
    main()
