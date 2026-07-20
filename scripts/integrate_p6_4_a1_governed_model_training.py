#!/usr/bin/env python3
"""Idempotently admit and reconcile the terminal P6.4-A1 reader packet."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "governed-model-training-distributed-optimization-and-scaling"
NEXT_PACKET = "P6.4-A2-privacy-data-rights-and-information-flow-governance-adjudication"
SOURCE_IDS = [
    "ext_llama3_herd_2024",
    "ext_megatron_distributed_training_2021",
    "ext_zero_optimizer_2019",
    "ext_gspmd_2021",
    "ext_datastates_llm_2024",
    "ext_pytorch_distributed_checkpoint_2026",
    "ext_mlperf_training_v6_2026",
]
LOCAL_SOURCE_ID = "corbens_trainer_project"


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def mapping(source_id: str, support: str, limits: str) -> dict:
    return {
        "source_id": source_id,
        "mapped_support": support,
        "limits": limits,
        "passage_refs": [f"sources/source_notes/{source_id}.md"],
        "passage_review_note": "Reviewed the primary paper or official documentation at the bounded passages recorded in the source note; no source-reported result is treated as local evidence.",
        "passage_review_state": "reviewed",
    }


SOURCES = [
    {
        "id": "ext_megatron_distributed_training_2021",
        "title": "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID],
        "url": "https://arxiv.org/abs/2104.04473",
        "notes": "Primary composed-parallelism mechanism source. It grounds tensor, pipeline, and data parallel interactions, strict optimizer semantics, microbatch and topology tradeoffs. Reported trillion-parameter and throughput results are configuration-bound and not locally reproduced.",
        "source_type": "conference_paper", "arxiv_id": "2104.04473", "published": "2021-04-09", "updated": "2021-08-30",
        "citation_label": "Narayanan et al. (2021), Efficient Large-Scale Language Model Training", "doi": "10.1145/3458817.3476209",
    },
    {
        "id": "ext_zero_optimizer_2019", "title": "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID],
        "url": "https://arxiv.org/abs/1910.02054",
        "notes": "Primary competing sharded-state design for optimizer, gradient, parameter, activation, and residual memory. It motivates explicit state closure and shard reconstruction; source-reported scale and speed are not locally reproduced or treated as universal superiority.",
        "source_type": "conference_paper", "arxiv_id": "1910.02054", "published": "2019-10-04", "updated": "2020-05-13",
        "citation_label": "Rajbhandari et al. (2020), ZeRO", "doi": "10.1109/SC41405.2020.00024",
    },
    {
        "id": "ext_gspmd_2021", "title": "GSPMD: General and Scalable Parallelization for ML Computation Graphs",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID],
        "url": "https://arxiv.org/abs/2105.04663",
        "notes": "Primary compiler-mediated competing design for general SPMD sharding and mixed parallelism. It motivates versioning inferred plans and inserted collectives; reported TPU utilization and scaling are not locally reproduced.",
        "source_type": "preprint", "arxiv_id": "2105.04663", "published": "2021-05-10", "updated": "2021-12-14",
        "citation_label": "Xu et al. (2021), GSPMD", "doi": "10.48550/arXiv.2105.04663",
    },
    {
        "id": "ext_datastates_llm_2024", "title": "DataStates-LLM: Lazy Asynchronous Checkpointing for Large Language Models",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID],
        "url": "https://arxiv.org/abs/2406.10707",
        "notes": "Primary limitation and checkpoint-mechanism source for asynchronous multi-level copies, distributed shard consistency, and checkpoint overhead. It does not establish complete application state or exact trajectory-equivalent resume, and no result is locally reproduced.",
        "source_type": "conference_paper", "arxiv_id": "2406.10707", "published": "2024-06-15", "updated": "2024-06-15",
        "citation_label": "Maurya et al. (2024), DataStates-LLM", "doi": "10.1145/3625549.3658685",
    },
    {
        "id": "ext_pytorch_distributed_checkpoint_2026", "title": "Distributed Checkpoint — PyTorch documentation",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID],
        "url": "https://docs.pytorch.org/docs/stable/distributed.checkpoint.html",
        "notes": "Official current implementation documentation for SPMD save/load, asynchronous completion, canonical model and optimizer state, resharding, strict load, and call-order constraints. Documentation is not benchmark or full-state resume evidence.",
        "source_type": "official_docs", "published": "2026-07-19", "updated": "2026-07-19",
        "citation_label": "PyTorch (2026), Distributed Checkpoint",
    },
    {
        "id": "ext_mlperf_training_v6_2026", "title": "MLPerf Training v6.0",
        "priority": "external_literature", "layer": "governed_distributed_model_training_and_scaling", "chapter_targets": [CHAPTER_ID, "benchmark-ratchets-and-anti-goodhart-evidence", "resource-economics-and-token-budgets"],
        "url": "https://mlcommons.org/benchmarks/training/",
        "notes": "Official current measurement comparator for fixed datasets and quality targets, repeated time-to-quality, system metadata, divisions, variance, and corrected results. No MLPerf run is performed and the benchmark does not establish safety or complete run integrity.",
        "source_type": "official_benchmark", "published": "2026-06-16", "updated": "2026-07-19",
        "citation_label": "MLCommons (2026), MLPerf Training v6.0",
    },
]


CHAPTER = {
    "id": CHAPTER_ID,
    "title": "Governed Model Training, Distributed Optimization, and Scaling",
    "file": f"chapters/{CHAPTER_ID}.qmd",
    "status": "conceptual", "evidence_level": "argument", "claim_label": "Design rationale",
    "source_ids": SOURCE_IDS + [LOCAL_SOURCE_ID],
    "source_queue": {
        "primary": SOURCE_IDS,
        "supporting": [LOCAL_SOURCE_ID], "variants": [], "connector_or_recovery": [],
        "handoff_or_recovery_notes": ["Receives a selected substrate, data lease, authorized objective, supply-chain identities, and resource budget; returns one exact candidate and complete run receipt to independent qualification without model-quality, support, readiness, or release authority."],
    },
    "problem": "A checkpoint can load and a loss curve can converge even when data order, optimizer state, numerical policy, distributed topology, failure recovery, or checkpoint selection no longer matches the training process claimed.",
    "insufficient": "Code, data, weights, final loss, peak throughput, a framework save call, successful restart, or one retained checkpoint does not identify the full stateful distributed run or separate candidate selection from independent qualification.",
    "core_claim": "A model-training candidate is eligible for qualification only when a prospectively frozen run contract binds architecture, data lease and order, objective, optimizer, scheduler, numerical policy, device and parallelism topology, code and environment, budget, stopping and fault policy, complete attempted-run denominator, full declared checkpoint state, commit consistency, resume equivalence class, candidate-checkpoint family, validation-only selection, independent unopened qualification, and residual ownership; a loss reduction, completed job, high utilization, checkpoint file, successful load, recovered run, selected candidate, formal record proof, or source-reported scale result alone establishes neither faithful training, model quality, optimizer superiority, fault tolerance, safety, support, readiness, release, transfer, nor SOTA.",
    "claim_source_mappings": [
        mapping("ext_llama3_herd_2024", "Supplies a paper-body-reviewed large-run case covering 4D parallelism, network-aware topology, numerical stability interventions, checkpoint infrastructure, interruption denominators, and effective training time.", "Provider-reported scale, utilization, interruption, and recovery results are not locally reproduced and do not establish exact resume."),
        mapping("ext_megatron_distributed_training_2021", "Grounds composed tensor, pipeline, and data parallelism, strict optimizer semantics, microbatch scheduling, communication, and topology tradeoffs.", "Its measured cluster and model envelope is not universal, and no throughput result is reproduced."),
        mapping("ext_zero_optimizer_2019", "Grounds progressive sharding and separate accounting for optimizer, gradient, parameter, activation, and residual state.", "Sharding does not prove complete application state, checkpoint integrity, or universal efficiency."),
        mapping("ext_gspmd_2021", "Grounds compiler-mediated SPMD sharding and mixed parallelism as a serious alternative to manually composed plans.", "Automatic completion does not prove semantic equivalence, optimal topology, or transfer."),
        mapping("ext_datastates_llm_2024", "Grounds asynchronous distributed checkpoint creation, logical consistency, storage-tier movement, and checkpoint overhead.", "Checkpoint consistency over model and optimizer shards does not by itself establish full-state or trajectory-equivalent resume."),
        mapping("ext_pytorch_distributed_checkpoint_2026", "Grounds current save/load, asynchronous future, canonical state, strict load, and resharding interface requirements.", "Official API documentation is not scientific performance evidence or proof that every application state is captured."),
        mapping("ext_mlperf_training_v6_2026", "Grounds fixed quality targets, repeated time-to-quality, system metadata, variance, divisions, and correction of published training results.", "No local MLPerf submission exists, and benchmark conformance would not establish safety, full run integrity, or release merit."),
        mapping("corbens_trainer_project", "Supplies a pinned local implementation and failure comparator for typed campaigns, training-truth gates, content-addressed checkpoint lineage, complete run facts, retained quarantines, and acknowledged-checkpoint requirements.", "Its external dependencies and natural training were not reproduced; retained null seed/code identities, later-quarantined claims, and unacknowledged asynchronous checkpoints are negative implementation evidence, not model-quality or distributed-training results."),
    ],
    "mechanism": [
        "Freeze exact run identity, data order, topology, numerical policy, budget, faults, selection, qualification, and nonclaims before execution.",
        "Compile and record the executed device mesh, parallelism dimensions, collective/compiler plan, batch arithmetic, and optimizer-step semantics.",
        "Enumerate complete base and architecture-specific model, optimizer, scheduler, scaler, RNG, sampler, data-cursor, topology, and compiler state.",
        "Record every attempt, failure, interruption, recovery, batch, anomaly, intervention, and actual resource cost without censoring failed runs.",
        "Advance checkpoints through request, staging, durable commit, shard and completeness validation, and resume authority.",
        "Test resume under a prospectively named bitwise, operation-order-bounded, or statistical equivalence class.",
        "Retain the full checkpoint family and select only on validation under a frozen rule.",
        "Hand the exact selected candidate to unopened independent qualification without support or release authority.",
    ],
    "interfaces": ["authorized objective", "rights-bearing data lease", "substrate state schema", "supply-chain identity", "resource budget", "topology and numerical plan", "execution and fault ledger", "checkpoint-family custody", "independent qualification handoff"],
    "invariants": ["inputs freeze before outcomes", "topology and numerics are semantic run inputs", "global batch arithmetic reconciles", "data order and multiplicity remain reconstructable", "declared checkpoint state closure is complete", "checkpoint shards share one logical step and durable commit", "resume equivalence class is prospective", "failed runs and candidate checkpoints stay in denominators", "qualification cannot select checkpoints", "training confers no support or release authority"],
    "failure_modes": ["run identity drift", "silent data replay or skip", "torn checkpoint", "state amnesia", "topology drift", "numerical drift laundering", "stale or duplicated update", "loss-spike intervention censorship", "checkpoint cherry-picking", "failed-run censorship", "peak-throughput substitution", "capacity-to-capability inference", "trainer self-certification", "record-completeness theater"],
    "minimal_implementation": "Build a training-run transaction record, validator, and replay workflow around a competent open natural workload with uninterrupted, standard distributed, deliberately weight-only recovery, full-state governed, and strong alternative-topology arms; inject thirteen fault families across at least three seeds and multiple timings; keep qualification hidden; retain every attempt and checkpoint; and measure time-to-quality, resume distance, drift detection, downstream qualification, resources, operator work, and governance cost jointly.",
    "beyond_state_of_art": "The mature operational contract is a substrate-neutral training transaction whose kernel-specific state schema, compiler-emitted topology, data order, update ledger, checkpoint commits, equivalence probes, complete denominators, and independent qualification boundary are replayable across dense, sparse, recurrent, state-space, graph, and hybrid architectures. It requires independent reproduction and cross-framework, hardware, topology, scale, fault, and time transfer while preserving rights, lineage, residual, rollback, candidate-family, and no-release-authority boundaries.",
    "codex_tests": [
        {"name": "Training-run transaction contract", "purpose": "Check topology and batch arithmetic, ten-class state closure, full denominator, checkpoint family, qualification separation, sources, non-authorities, and 21 rejecting mutations.", "implementation_status": "implemented", "result_status": "authored_record_only_no_training_effect"},
        {"name": "Natural distributed fault campaign", "purpose": "Compare five strong matched arms across thirteen faults, at least three seeds, hidden qualification, and joint integrity, quality, resource, and operator outcomes.", "implementation_status": "planned", "result_status": "prospectively_frozen_unexecuted"},
        {"name": "Independent run replay", "purpose": "Reconstruct data order, topology, complete checkpoint state, selection, and reported metrics from retained artifacts.", "implementation_status": "planned", "result_status": "blocked_by_valid_campaign"},
    ],
    "lean_module": "AsiStackProofs.GovernedModelTraining",
    "proof_targets": [
        {"tag": "lean:governed_training.run_admission_invariants", "module": "AsiStackProofs.GovernedModelTraining", "target": "An accepted finite handoff requires exact declared identity, topology/numerical identity, complete committed checkpoint state, complete failure denominator, and no support or release request.", "status": "implemented"},
        {"tag": "lean:governed_training.resume_and_handoff_separation", "module": "AsiStackProofs.GovernedModelTraining", "target": "An accepted finite handoff requires accounted resume state, retained checkpoint and failure families, validation-only selection, and unopened independent qualification.", "status": "implemented"},
    ],
    "draft_maturity": "integrated_argument_chapter_formal_and_protocol_contract_complete",
    "open_evidence_gaps": ["No ASI Stack distributed model-training campaign has run for this chapter.", "No natural checkpoint resume equivalence, fault-tolerance, model-quality, efficiency, reproduction, or transfer result is recorded.", "The authored transaction fixture and finite Lean model establish record consequences only."],
}

TRIAGE_RECORDS = [
    {
        "tag": "lean:governed_training.run_admission_invariants",
        "chapter_id": CHAPTER_ID,
        "module": "AsiStackProofs.GovernedModelTraining",
        "formal_target": "An accepted finite handoff requires exact declared identity, topology/numerical identity, complete committed checkpoint state, complete failure denominator, and no support or release request.",
        "target_status": "implemented",
        "triage": "formal-invariant",
        "recommended_route": "lean-candidate",
        "rationale": "Implemented as finite training-run admission implications over declared identity, topology, numerical policy, checkpoint state, denominator, and requested authority. The proof trusts the record predicates and establishes no distributed execution, state completeness, resume fidelity, model quality, efficiency, safety, reproduction, transfer, or release result.",
    },
    {
        "tag": "lean:governed_training.resume_and_handoff_separation",
        "chapter_id": CHAPTER_ID,
        "module": "AsiStackProofs.GovernedModelTraining",
        "formal_target": "An accepted finite handoff requires accounted resume state, retained checkpoint and failure families, validation-only selection, and unopened independent qualification.",
        "target_status": "implemented",
        "triage": "formal-invariant",
        "recommended_route": "lean-candidate",
        "rationale": "Implemented as a bounded separation theorem over authored resume, retention, selection, and qualification fields. It cannot establish trajectory equivalence, evaluator independence in practice, downstream qualification, checkpoint usefulness, training competence, safety, reproduction, transfer, or readiness.",
    },
]


def main() -> None:
    inventory_path = ROOT / "sources/source_inventory.json"
    inventory = json.loads(inventory_path.read_text())
    by_id = {row["id"]: row for row in inventory}
    for source in SOURCES:
        by_id[source["id"]] = source
    for row in inventory:
        if row["id"] == "ext_llama3_herd_2024":
            row["notes"] = "Paper-body-reviewed large-run case: Sections 3.3.1--3.3.4 expose 4D topology, numerical policy, checkpoint infrastructure, interruption denominators, and effective training time. Provider-reported scale, utilization, failures, and recovery are not locally reproduced and do not establish exact resume."
            row["chapter_targets"] = sorted(set(row.get("chapter_targets", [])) | {CHAPTER_ID})
        if row["id"] == LOCAL_SOURCE_ID:
            row["chapter_targets"] = sorted(set(row.get("chapter_targets", [])) | {CHAPTER_ID})
    existing_order = [row["id"] for row in inventory]
    inventory = [by_id[source_id] for source_id in existing_order]
    for source in SOURCES:
        if source["id"] not in existing_order:
            inventory.append(source)
    dump(inventory_path, inventory)

    structure_path = ROOT / "book_structure.json"
    structure = json.loads(structure_path.read_text())
    for part in structure["parts"]:
        part["chapters"] = [chapter for chapter in part["chapters"] if chapter["id"] != CHAPTER_ID]
    part = next(p for p in structure["parts"] if any(c["id"] == "replaceable-cognitive-substrates-beyond-transformer-monoculture" for c in p["chapters"]))
    index = next(i for i, c in enumerate(part["chapters"]) if c["id"] == "replaceable-cognitive-substrates-beyond-transformer-monoculture") + 1
    part["chapters"].insert(index, CHAPTER)
    for chapter in (c for p in structure["parts"] for c in p["chapters"]):
        if chapter["id"] in {"benchmark-ratchets-and-anti-goodhart-evidence", "resource-economics-and-token-budgets"} and "ext_mlperf_training_v6_2026" not in chapter.get("source_ids", []):
            chapter.setdefault("source_ids", []).append("ext_mlperf_training_v6_2026")
            chapter.setdefault("source_queue", {}).setdefault("variants", []).append("ext_mlperf_training_v6_2026")
    dump(structure_path, structure)

    triage_path = ROOT / "proofs/proof_triage.json"
    triage = json.loads(triage_path.read_text())
    replacements = {row["tag"]: row for row in TRIAGE_RECORDS}
    triage["records"] = [
        replacements.pop(row["tag"], row) for row in triage["records"]
    ]
    triage["records"].extend(replacements.values())
    triage["record_count"] = len(triage["records"])
    dump(triage_path, triage)

    status_path = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
    status = json.loads(status_path.read_text())
    status["schema_version"] = "asi_stack.post_v2_3_maintenance_transfer_publication_status.v15"
    status["execution_readiness"]["immediate_book_packet"] = NEXT_PACKET
    narrative = status["quality_uplift_program"]["narrative_quality_gate"]
    narrative["case_independent_compression_state"] = "first_tranche_terminal_second_tranche_a1_terminal_a2_ready"
    tranche = status["quality_uplift_program"]["structural_completeness_tranche"]
    tranche["state"] = "first_tranche_terminal_second_tranche_a1_terminal"
    tranche["current_manifest_chapter_count"] = 60
    second = tranche["second_tranche"]
    second["state"] = "a1_terminal_twelve_manifest_gated"
    second["manifest_admitted_count"] = 1
    second["primary_source_record_count_added"] = 23
    second["adjudicated_candidate_ids"] = [CHAPTER_ID]
    second["terminal_candidate_dispositions"] = {CHAPTER_ID: "admitted_terminal_argument_reader_chapter"}
    second["active_candidate_id"] = "privacy-data-rights-and-information-flow-governance"
    second["remaining_candidate_ids"] = [candidate for candidate in second["candidate_ids"] if candidate != CHAPTER_ID]
    second["a1_decision_packet"] = "docs/p6_4_a1_governed_model_training_adjudication.md"
    status["activation_truth"]["live_working_chapter_count"] = 60
    status["activation_truth"]["chapter_core_argument_count"] = 60
    status["activation_truth"]["proof_target_count"] = 308
    status["activation_truth"]["lean_module_count"] = 103
    status["activation_truth"]["theorem_declaration_count"] = 1359
    status["activation_truth"]["derived_or_decomposed_theorem_count"] = 921
    status["activation_truth"]["direct_or_projection_theorem_count"] = 230
    status["activation_truth"]["unknown_or_mixed_theorem_count"] = 208
    status["negative_result_rehabilitation"]["current_surface_count"] = 80
    status["negative_result_rehabilitation"]["live_chapter_surface_count"] = 60
    dump(status_path, status)

    schema_path = ROOT / "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json"
    schema = json.loads(schema_path.read_text())
    schema["properties"]["schema_version"]["const"] = status["schema_version"]
    execution_schema = schema["properties"]["execution_readiness"]["properties"]
    execution_schema["immediate_book_packet"]["const"] = NEXT_PACKET
    q = schema["properties"]["quality_uplift_program"]["properties"]
    q["narrative_quality_gate"]["properties"]["case_independent_compression_state"]["const"] = narrative["case_independent_compression_state"]
    tranche_schema = q["structural_completeness_tranche"]
    tranche_schema["properties"]["state"]["const"] = tranche["state"]
    tranche_schema["properties"]["current_manifest_chapter_count"]["const"] = 60
    second_schema = tranche_schema["properties"]["second_tranche"]
    for key in ("adjudicated_candidate_ids", "terminal_candidate_dispositions", "active_candidate_id", "remaining_candidate_ids", "a1_decision_packet"):
        if key not in second_schema["required"]:
            second_schema["required"].append(key)
        second_schema["properties"][key] = {"const": second[key]}
    second_schema["properties"]["state"]["const"] = second["state"]
    second_schema["properties"]["manifest_admitted_count"]["const"] = 1
    second_schema["properties"]["primary_source_record_count_added"]["const"] = 23
    activation = schema["properties"]["activation_truth"]["properties"]
    for key in ("live_working_chapter_count", "chapter_core_argument_count", "proof_target_count", "lean_module_count", "theorem_declaration_count", "derived_or_decomposed_theorem_count", "direct_or_projection_theorem_count"):
        activation[key]["const"] = status["activation_truth"][key]
    rehab = schema["properties"]["negative_result_rehabilitation"]["properties"]
    rehab["current_surface_count"]["const"] = 80
    rehab["live_chapter_surface_count"]["const"] = 60
    dump(schema_path, schema)

    audit_path = ROOT / "evidence_quality/p6_4_a1_governed_model_training_reader_integration.json"
    audit = json.loads(audit_path.read_text())
    audit["artifact_sha256"] = {relative: sha(relative) for relative in audit["artifacts"].values()}
    audit["source_note_sha256"] = {source_id: sha(f"sources/source_notes/{source_id}.md") for source_id in SOURCE_IDS}
    dump(audit_path, audit)
    print(f"Integrated terminal P6.4-A1: {sum(len(p['chapters']) for p in structure['parts'])} chapters, {len(inventory)} sources; next packet {NEXT_PACKET}.")


if __name__ == "__main__":
    main()
