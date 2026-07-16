#!/usr/bin/env python3
"""Validate the active claim-proof and SOTA-challenge successor authority."""

from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md"
STATUS = "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
SCHEMA = "schemas/post_v2_3_claim_proof_and_sota_challenge_status.schema.json"
X_ARTICLE_CONTRACT = "docs/x_article_synopsis_contract.md"
SAFETY_CONSUMER_RESULT = "experiments/safety_critical_lifecycle/results/2026-07-15-consumer-local.json"
SAFETY_CONSUMER_TRACE = "docs/safety_critical_lifecycle_consumer_trace.md"
SAFETY_MODEL_DOSSIER = "evidence_quality/model_adequacy_dossiers/safety-critical-lifecycle.md"
ABI_RESULT = "experiments/cognitive_kernel_abi/results/2026-07-15-local.json"
ABI_TRACE = "docs/cognitive_kernel_abi_trace.md"
ABI_MODEL_DOSSIER = "evidence_quality/model_adequacy_dossiers/cognitive-kernel-abi.md"
INTEGRATED_TRACE_RESULT = "experiments/integrated_reference_trace/results/2026-07-15-local.json"
INTEGRATED_TRACE_RECEIPT = "docs/integrated_reference_trace_consumer.md"
INTEGRATED_TRACE_DOSSIER = "evidence_quality/model_adequacy_dossiers/integrated-reference-trace.md"
INTEGRATED_REFINEMENT_RESULT = "experiments/integrated_reference_trace/results/2026-07-15-runtime-schema-refinement.json"
INTEGRATED_REFINEMENT_SCHEMA = "schemas/integrated_runtime_schema_refinement.schema.json"
CONCURRENT_EFFECT_RESULT = "experiments/integrated_reference_trace/results/2026-07-15-concurrent-effect-ledger.json"
CONCURRENT_EFFECT_RECEIPT = "docs/concurrent_effect_ledger_consumer.md"
STACK_BOUNDARY_RESULT = "experiments/stack_boundary_effect/results/2026-07-15-local.json"
STACK_BOUNDARY_RECEIPT = "docs/stack_boundary_effect_consumer.md"
STACK_BOUNDARY_DOSSIER = "evidence_quality/model_adequacy_dossiers/stack-boundary-effect.md"
INTENT_EXECUTION_RESULT = "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json"
INTENT_EXECUTION_RECEIPT = "docs/intent_execution_vertical_refinement.md"
INTENT_EXECUTION_DOSSIER = "evidence_quality/model_adequacy_dossiers/intent-execution-vertical-refinement.md"
AUTHORITY_EFFECT_RESULT = "experiments/authority_effect_refinement/results/2026-07-15-local.json"
AUTHORITY_EFFECT_RECEIPT = "docs/authority_effect_refinement.md"
AUTHORITY_EFFECT_DOSSIER = "evidence_quality/model_adequacy_dossiers/authority-effect-refinement.md"
INTENT_RESOLUTION_RESULT = "experiments/intent_resolution_refinement/results/2026-07-15-local.json"
INTENT_RESOLUTION_RECEIPT = "docs/intent_resolution_refinement.md"
INTENT_RESOLUTION_DOSSIER = "evidence_quality/model_adequacy_dossiers/intent-resolution-refinement.md"
COMMAND_SEMANTIC_RESULT = "experiments/command_semantic_refinement/results/2026-07-15-local.json"
COMMAND_SEMANTIC_RECEIPT = "docs/command_semantic_refinement.md"
COMMAND_SEMANTIC_DOSSIER = "evidence_quality/model_adequacy_dossiers/command-semantic-refinement.md"
COGNITIVE_COMPILATION_RESULT = "experiments/cognitive_compilation_refinement/results/2026-07-15-local.json"
COGNITIVE_COMPILATION_RECEIPT = "docs/cognitive_compilation_refinement.md"
COGNITIVE_COMPILATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/cognitive-compilation-refinement.md"
VIRTUAL_CONTEXT_RESULT = "experiments/virtual_context_refinement/results/2026-07-15-local.json"
VIRTUAL_CONTEXT_RECEIPT = "docs/virtual_context_refinement.md"
VIRTUAL_CONTEXT_DOSSIER = "evidence_quality/model_adequacy_dossiers/virtual-context-refinement.md"
CONTEXT_CERTIFICATE_RESULT = "experiments/context_certificate_refinement/results/2026-07-15-local.json"
CONTEXT_CERTIFICATE_RECEIPT = "docs/context_certificate_refinement.md"
CONTEXT_CERTIFICATE_DOSSIER = "evidence_quality/model_adequacy_dossiers/context-certificate-refinement.md"
CONTEXT_TRANSACTION_RESULT = "experiments/context_transaction_refinement/results/2026-07-15-local.json"
CONTEXT_TRANSACTION_RECEIPT = "docs/context_transaction_refinement.md"
CONTEXT_TRANSACTION_DOSSIER = "evidence_quality/model_adequacy_dossiers/context-transaction-refinement.md"
VERIFICATION_BANDWIDTH_RESULT = "experiments/verification_bandwidth_refinement/results/2026-07-15-local.json"
VERIFICATION_BANDWIDTH_RECEIPT = "docs/verification_bandwidth_refinement.md"
VERIFICATION_BANDWIDTH_DOSSIER = "evidence_quality/model_adequacy_dossiers/verification-bandwidth-refinement.md"
CLAIM_LEDGER_RESULT = "experiments/claim_ledger_refinement/results/2026-07-15-local.json"
CLAIM_LEDGER_RECEIPT = "docs/claim_ledger_refinement.md"
CLAIM_LEDGER_DOSSIER = "evidence_quality/model_adequacy_dossiers/claim-ledger-refinement.md"
PROOF_CARRYING_CLAIMS_RESULT = "experiments/proof_carrying_claims_refinement/results/2026-07-15-local.json"
PROOF_CARRYING_CLAIMS_RECEIPT = "docs/proof_carrying_claims_refinement.md"
PROOF_CARRYING_CLAIMS_DOSSIER = "evidence_quality/model_adequacy_dossiers/proof-carrying-claims-refinement.md"
TRIBUNAL_RESULT = "experiments/tribunal_refinement/results/2026-07-15-local.json"
TRIBUNAL_RECEIPT = "docs/tribunal_refinement.md"
TRIBUNAL_DOSSIER = "evidence_quality/model_adequacy_dossiers/tribunal-refinement.md"
TYPED_JOB_RESULT = "experiments/typed_job_refinement/results/2026-07-15-local.json"
TYPED_JOB_RECEIPT = "docs/typed_job_refinement.md"
TYPED_JOB_DOSSIER = "evidence_quality/model_adequacy_dossiers/typed-job-refinement.md"
ARTIFACT_REALITY_RESULT = "experiments/artifact_reality_refinement/results/2026-07-15-local.json"
ARTIFACT_REALITY_RECEIPT = "docs/artifact_reality_refinement.md"
ARTIFACT_REALITY_DOSSIER = "evidence_quality/model_adequacy_dossiers/artifact-reality-refinement.md"
PROCEDURAL_MEMORY_RESULT = "experiments/procedural_memory_refinement/results/2026-07-15-local.json"
PROCEDURAL_MEMORY_RECEIPT = "docs/procedural_memory_refinement.md"
PROCEDURAL_MEMORY_DOSSIER = "evidence_quality/model_adequacy_dossiers/procedural-memory-refinement.md"
ROUTING_RESULT = "experiments/routing_refinement/results/2026-07-15-local.json"
ROUTING_RECEIPT = "docs/routing_refinement.md"
ROUTING_DOSSIER = "evidence_quality/model_adequacy_dossiers/routing-refinement.md"
SAFETY_CASE_RESULT = "experiments/safety_case_refinement/results/2026-07-15-local.json"
SAFETY_CASE_RECEIPT = "docs/safety_case_refinement.md"
SAFETY_CASE_DOSSIER = "evidence_quality/model_adequacy_dossiers/safety-case-refinement.md"
CAPABILITY_THRESHOLD_RESULT = "experiments/capability_threshold_refinement/results/2026-07-15-local.json"
CAPABILITY_THRESHOLD_RECEIPT = "docs/capability_threshold_refinement.md"
CAPABILITY_THRESHOLD_DOSSIER = "evidence_quality/model_adequacy_dossiers/capability-threshold-refinement.md"
ADVERSARIAL_EVALUATION_RESULT = "experiments/adversarial_evaluation_refinement/results/2026-07-15-local.json"
ADVERSARIAL_EVALUATION_RECEIPT = "docs/adversarial_evaluation_refinement.md"
ADVERSARIAL_EVALUATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/adversarial-evaluation-refinement.md"
SCALABLE_OVERSIGHT_RESULT = "experiments/scalable_oversight_refinement/results/2026-07-15-local.json"
SCALABLE_OVERSIGHT_RECEIPT = "docs/scalable_oversight_refinement.md"
SCALABLE_OVERSIGHT_DOSSIER = "evidence_quality/model_adequacy_dossiers/scalable-oversight-refinement.md"
POLICY_OPTIMIZATION_RESULT = "experiments/policy_optimization_refinement/results/2026-07-16-local.json"
POLICY_OPTIMIZATION_RECEIPT = "docs/policy_optimization_refinement.md"
POLICY_OPTIMIZATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/policy-optimization-refinement.md"
DATA_ENGINE_LIFECYCLE_RESULT = "experiments/data_engine_lifecycle_refinement/results/2026-07-16-local.json"
DATA_ENGINE_LIFECYCLE_RECEIPT = "docs/data_engine_lifecycle_refinement.md"
DATA_ENGINE_LIFECYCLE_DOSSIER = "evidence_quality/model_adequacy_dossiers/data-engine-lifecycle-refinement.md"
OPEN_ENDED_IMPROVEMENT_RESULT = "experiments/open_ended_improvement_refinement/results/2026-07-16-local.json"
OPEN_ENDED_IMPROVEMENT_RECEIPT = "docs/open_ended_improvement_refinement.md"
OPEN_ENDED_IMPROVEMENT_DOSSIER = "evidence_quality/model_adequacy_dossiers/open-ended-improvement-refinement.md"
SELF_IMPROVEMENT_RESULT = "experiments/self_improvement_refinement/results/2026-07-16-local.json"
SELF_IMPROVEMENT_RECEIPT = "docs/self_improvement_refinement.md"
SELF_IMPROVEMENT_DOSSIER = "evidence_quality/model_adequacy_dossiers/self-improvement-refinement.md"
READINESS_RESULT = "experiments/readiness_refinement/results/2026-07-15-local.json"
READINESS_RECEIPT = "docs/readiness_refinement.md"
READINESS_DOSSIER = "evidence_quality/model_adequacy_dossiers/readiness-refinement.md"
HIVE_RESULT = "experiments/hive_lifecycle_refinement/results/2026-07-15-local.json"
HIVE_RECEIPT = "docs/hive_lifecycle_refinement.md"
HIVE_DOSSIER = "evidence_quality/model_adequacy_dossiers/hive-lifecycle-refinement.md"
COMPACT_GENERATION_RESULT = "experiments/compact_generation_refinement/results/2026-07-15-local.json"
COMPACT_GENERATION_RECEIPT = "docs/compact_generation_refinement.md"
COMPACT_GENERATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/compact-generation-refinement.md"
FAST_GENERATION_RESULT = "experiments/fast_generation_refinement/results/2026-07-15-local.json"
FAST_GENERATION_RECEIPT = "docs/fast_generation_refinement.md"
FAST_GENERATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/fast-generation-refinement.md"
DELIBERATION_RESULT = "experiments/deliberation_refinement/results/2026-07-15-local.json"
DELIBERATION_RECEIPT = "docs/deliberation_refinement.md"
DELIBERATION_DOSSIER = "evidence_quality/model_adequacy_dossiers/deliberation-refinement.md"
ARTIFACT_COMPRESSION_RESULT = "experiments/artifact_compression_refinement/results/2026-07-15-local.json"
ARTIFACT_COMPRESSION_RECEIPT = "docs/artifact_compression_refinement.md"
ARTIFACT_COMPRESSION_DOSSIER = "evidence_quality/model_adequacy_dossiers/artifact-compression-refinement.md"
RESOURCE_ECONOMICS_RESULT = "experiments/resource_economics_refinement/results/2026-07-15-local.json"
RESOURCE_ECONOMICS_RECEIPT = "docs/resource_economics_refinement.md"
RESOURCE_ECONOMICS_DOSSIER = "evidence_quality/model_adequacy_dossiers/resource-economics-refinement.md"
GOVERNED_USEFULNESS_PREREG = "experiments/p4_governed_usefulness/preregistration.json"
GOVERNED_USEFULNESS_ACCESS = "experiments/p4_governed_usefulness/strong_model_access_preflight.json"
GOVERNED_USEFULNESS_V1_RESULT = "experiments/p4_governed_usefulness/results/strong_model_sacrificial_preflight.json"
GOVERNED_USEFULNESS_V2_PREREG = "experiments/p4_governed_usefulness/preregistration_v2.json"
GOVERNED_USEFULNESS_V2_RESULT = "experiments/p4_governed_usefulness/results/strong_model_sacrificial_preflight_v2.json"
GOVERNED_USEFULNESS_V2_DIAGNOSIS = "experiments/p4_governed_usefulness/v2_failure_diagnosis.json"
PREDECESSOR = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
PREDECESSOR_STATUS = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
ACTIVE_MARKER = "Status: active canonical successor roadmap; unfinished work only"
PUBLIC_SURFACES = ["README.md", "index.qmd", "docs/publication_readiness.md", "docs/public_status_contract.md"]
REQUIRED_SECTIONS = [
    "## Goal to point at",
    "## Why this successor is necessary",
    "## Claude critique adjudication",
    "## Proof constitution",
    "## Operating principles",
    "## Execution board",
    "## P0 — Proof authority and continuity",
    "## P1 — Complete claim decomposition",
    "## P2 — Existing-proof rationalization, formal semantics, and refinement",
    "## P3 — Executable integrated reference architecture",
    "## P4 — Signature causal campaigns",
    "## P5 — Full claim-family evidence program",
    "## P6 — External reproduction and SOTA challenge",
    "## P7 — Book-wide evidence integration",
    "## P8 — Reader release and terminal evidence freeze",
    "## P9 — Maintained X Article synopsis and 5:2 header",
    "## Milestones",
    "## Definition of done",
    "## Canonical execution prompt",
    "## Non-claims at activation",
]
REQUIRED_BOUNDARIES = [
    "The target is not to label every sentence “proved.”",
    "Semantic adequacy before theorem count",
    "A third unchanged rerun of a diagnosed failed protocol is forbidden.",
    "No book-wide or architecture-wide “beyond state of the art” claim is permitted from one benchmark.",
    "External-human prepublication review or outreach is not required or claimed.",
    "one and only one active successor roadmap exists before this roadmap's status changes to completed",
    "Validation, theorem, source, citation, format, commit, and release counts are not semantic or empirical proof.",
    "Argument is a launch state, not a refuge.",
    "audit all 1,151 activation-baseline theorem declarations and all 298 proof targets",
    "9,999 words or fewer",
    "2000×800 pixel",
    "Creating repository artifacts does not authorize an external post.",
    "An instrument failure is not a claim result.",
    "instrument_inadequate_recampaign_required",
    "At least 80% of expected final decisions must be schema-admissible",
    "A single substantial executable theorem may pass; many projections may fail.",
]


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def active_roadmaps() -> list[str]:
    return [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
        if ACTIVE_MARKER in path.read_text(encoding="utf-8", errors="ignore")[:1600]
    ]


def table_metric(body: str, label: str) -> int | None:
    match = re.search(rf"\|\s*{re.escape(label)}\s*\|\s*([0-9,]+)\s*\|", body)
    return int(match.group(1).replace(",", "")) if match else None


def snapshot() -> dict:
    return {
        "status": load(STATUS),
        "schema": load(SCHEMA),
        "roadmap": text(ROADMAP),
        "x_article_contract": text(X_ARTICLE_CONTRACT),
        "predecessor": text(PREDECESSOR),
        "predecessor_status": load(PREDECESSOR_STATUS),
        "structure": load("book_structure.json"),
        "sources": load("sources/source_inventory.json"),
        "structural_expansion_atoms": load("evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"),
        "claim_atom_registry": load("evidence_quality/claim_atom_registry.json"),
        "wip_checkpoint_inventory": load("roadmap_records/post_v2_3_wip_checkpoint_inventory.json"),
        "checkpoint_attestation": load("roadmap_records/post_v2_3_checkpoint_attestation_2026_07_16.json"),
        "governed_usefulness_prereg": load(GOVERNED_USEFULNESS_PREREG),
        "governed_usefulness_access": load(GOVERNED_USEFULNESS_ACCESS),
        "governed_usefulness_v1_result": load(GOVERNED_USEFULNESS_V1_RESULT),
        "governed_usefulness_v2_prereg": load(GOVERNED_USEFULNESS_V2_PREREG),
        "governed_usefulness_v2_result": load(GOVERNED_USEFULNESS_V2_RESULT),
        "governed_usefulness_v2_diagnosis": load(GOVERNED_USEFULNESS_V2_DIAGNOSIS),
        "vectors": load("evidence_quality/core_claim_vectors.json"),
        "proof_depth": text("docs/proof_depth_classification.md"),
        "proof_adequacy": text("docs/proof_adequacy_review.md"),
        "safety_consumer_result": load(SAFETY_CONSUMER_RESULT),
        "safety_consumer_trace": text(SAFETY_CONSUMER_TRACE),
        "safety_model_dossier": text(SAFETY_MODEL_DOSSIER),
        "abi_result": load(ABI_RESULT),
        "abi_trace": text(ABI_TRACE),
        "abi_model_dossier": text(ABI_MODEL_DOSSIER),
        "integrated_trace_result": load(INTEGRATED_TRACE_RESULT),
        "integrated_trace_receipt": text(INTEGRATED_TRACE_RECEIPT),
        "integrated_trace_dossier": text(INTEGRATED_TRACE_DOSSIER),
        "integrated_refinement_result": load(INTEGRATED_REFINEMENT_RESULT),
        "concurrent_effect_result": load(CONCURRENT_EFFECT_RESULT),
        "concurrent_effect_receipt": text(CONCURRENT_EFFECT_RECEIPT),
        "stack_boundary_result": load(STACK_BOUNDARY_RESULT),
        "stack_boundary_receipt": text(STACK_BOUNDARY_RECEIPT),
        "stack_boundary_dossier": text(STACK_BOUNDARY_DOSSIER),
        "intent_execution_result": load(INTENT_EXECUTION_RESULT),
        "intent_execution_receipt": text(INTENT_EXECUTION_RECEIPT),
        "intent_execution_dossier": text(INTENT_EXECUTION_DOSSIER),
        "authority_effect_result": load(AUTHORITY_EFFECT_RESULT),
        "authority_effect_receipt": text(AUTHORITY_EFFECT_RECEIPT),
        "authority_effect_dossier": text(AUTHORITY_EFFECT_DOSSIER),
        "intent_resolution_result": load(INTENT_RESOLUTION_RESULT),
        "intent_resolution_receipt": text(INTENT_RESOLUTION_RECEIPT),
        "intent_resolution_dossier": text(INTENT_RESOLUTION_DOSSIER),
        "command_semantic_result": load(COMMAND_SEMANTIC_RESULT),
        "command_semantic_receipt": text(COMMAND_SEMANTIC_RECEIPT),
        "command_semantic_dossier": text(COMMAND_SEMANTIC_DOSSIER),
        "cognitive_compilation_result": load(COGNITIVE_COMPILATION_RESULT),
        "cognitive_compilation_receipt": text(COGNITIVE_COMPILATION_RECEIPT),
        "cognitive_compilation_dossier": text(COGNITIVE_COMPILATION_DOSSIER),
        "virtual_context_result": load(VIRTUAL_CONTEXT_RESULT),
        "virtual_context_receipt": text(VIRTUAL_CONTEXT_RECEIPT),
        "virtual_context_dossier": text(VIRTUAL_CONTEXT_DOSSIER),
        "context_certificate_result": load(CONTEXT_CERTIFICATE_RESULT),
        "context_certificate_receipt": text(CONTEXT_CERTIFICATE_RECEIPT),
        "context_certificate_dossier": text(CONTEXT_CERTIFICATE_DOSSIER),
        "context_transaction_result": load(CONTEXT_TRANSACTION_RESULT),
        "context_transaction_receipt": text(CONTEXT_TRANSACTION_RECEIPT),
        "context_transaction_dossier": text(CONTEXT_TRANSACTION_DOSSIER),
        "verification_bandwidth_result": load(VERIFICATION_BANDWIDTH_RESULT),
        "verification_bandwidth_receipt": text(VERIFICATION_BANDWIDTH_RECEIPT),
        "verification_bandwidth_dossier": text(VERIFICATION_BANDWIDTH_DOSSIER),
        "claim_ledger_result": load(CLAIM_LEDGER_RESULT),
        "claim_ledger_receipt": text(CLAIM_LEDGER_RECEIPT),
        "claim_ledger_dossier": text(CLAIM_LEDGER_DOSSIER),
        "proof_carrying_claims_result": load(PROOF_CARRYING_CLAIMS_RESULT),
        "proof_carrying_claims_receipt": text(PROOF_CARRYING_CLAIMS_RECEIPT),
        "proof_carrying_claims_dossier": text(PROOF_CARRYING_CLAIMS_DOSSIER),
        "tribunal_result": load(TRIBUNAL_RESULT),
        "tribunal_receipt": text(TRIBUNAL_RECEIPT),
        "tribunal_dossier": text(TRIBUNAL_DOSSIER),
        "typed_job_result": load(TYPED_JOB_RESULT),
        "typed_job_receipt": text(TYPED_JOB_RECEIPT),
        "typed_job_dossier": text(TYPED_JOB_DOSSIER),
        "artifact_reality_result": load(ARTIFACT_REALITY_RESULT),
        "artifact_reality_receipt": text(ARTIFACT_REALITY_RECEIPT),
        "artifact_reality_dossier": text(ARTIFACT_REALITY_DOSSIER),
        "procedural_memory_result": load(PROCEDURAL_MEMORY_RESULT),
        "procedural_memory_receipt": text(PROCEDURAL_MEMORY_RECEIPT),
        "procedural_memory_dossier": text(PROCEDURAL_MEMORY_DOSSIER),
        "routing_result": load(ROUTING_RESULT),
        "routing_receipt": text(ROUTING_RECEIPT),
        "routing_dossier": text(ROUTING_DOSSIER),
        "safety_case_result": load(SAFETY_CASE_RESULT),
        "safety_case_receipt": text(SAFETY_CASE_RECEIPT),
        "safety_case_dossier": text(SAFETY_CASE_DOSSIER),
        "capability_threshold_result": load(CAPABILITY_THRESHOLD_RESULT),
        "capability_threshold_receipt": text(CAPABILITY_THRESHOLD_RECEIPT),
        "capability_threshold_dossier": text(CAPABILITY_THRESHOLD_DOSSIER),
        "adversarial_evaluation_result": load(ADVERSARIAL_EVALUATION_RESULT),
        "adversarial_evaluation_receipt": text(ADVERSARIAL_EVALUATION_RECEIPT),
        "adversarial_evaluation_dossier": text(ADVERSARIAL_EVALUATION_DOSSIER),
        "scalable_oversight_result": load(SCALABLE_OVERSIGHT_RESULT),
        "scalable_oversight_receipt": text(SCALABLE_OVERSIGHT_RECEIPT),
        "scalable_oversight_dossier": text(SCALABLE_OVERSIGHT_DOSSIER),
        "policy_optimization_result": load(POLICY_OPTIMIZATION_RESULT),
        "policy_optimization_receipt": text(POLICY_OPTIMIZATION_RECEIPT),
        "policy_optimization_dossier": text(POLICY_OPTIMIZATION_DOSSIER),
        "data_engine_lifecycle_result": load(DATA_ENGINE_LIFECYCLE_RESULT),
        "data_engine_lifecycle_receipt": text(DATA_ENGINE_LIFECYCLE_RECEIPT),
        "data_engine_lifecycle_dossier": text(DATA_ENGINE_LIFECYCLE_DOSSIER),
        "open_ended_improvement_result": load(OPEN_ENDED_IMPROVEMENT_RESULT),
        "open_ended_improvement_receipt": text(OPEN_ENDED_IMPROVEMENT_RECEIPT),
        "open_ended_improvement_dossier": text(OPEN_ENDED_IMPROVEMENT_DOSSIER),
        "self_improvement_result": load(SELF_IMPROVEMENT_RESULT),
        "self_improvement_receipt": text(SELF_IMPROVEMENT_RECEIPT),
        "self_improvement_dossier": text(SELF_IMPROVEMENT_DOSSIER),
        "readiness_result": load(READINESS_RESULT),
        "readiness_receipt": text(READINESS_RECEIPT),
        "readiness_dossier": text(READINESS_DOSSIER),
        "hive_result": load(HIVE_RESULT),
        "hive_receipt": text(HIVE_RECEIPT),
        "hive_dossier": text(HIVE_DOSSIER),
        "compact_generation_result": load(COMPACT_GENERATION_RESULT),
        "compact_generation_receipt": text(COMPACT_GENERATION_RECEIPT),
        "compact_generation_dossier": text(COMPACT_GENERATION_DOSSIER),
        "fast_generation_result": load(FAST_GENERATION_RESULT),
        "fast_generation_receipt": text(FAST_GENERATION_RECEIPT),
        "fast_generation_dossier": text(FAST_GENERATION_DOSSIER),
        "deliberation_result": load(DELIBERATION_RESULT),
        "deliberation_receipt": text(DELIBERATION_RECEIPT),
        "deliberation_dossier": text(DELIBERATION_DOSSIER),
        "artifact_compression_result": load(ARTIFACT_COMPRESSION_RESULT),
        "artifact_compression_receipt": text(ARTIFACT_COMPRESSION_RECEIPT),
        "artifact_compression_dossier": text(ARTIFACT_COMPRESSION_DOSSIER),
        "resource_economics_result": load(RESOURCE_ECONOMICS_RESULT),
        "resource_economics_receipt": text(RESOURCE_ECONOMICS_RECEIPT),
        "resource_economics_dossier": text(RESOURCE_ECONOMICS_DOSSIER),
        "registry": load("validation/registry.json"),
        "flagship": load("experiments/post_v2_3_evidence_protocol_renewal/flagship/results/adjudication.json"),
        "reader_html": load("editions/reader_manuscript/v2_0/reader_release_record.json"),
        "reader_docx": load("editions/reader_manuscript/v2_0/docx_disposition.json"),
        "reader_epub": load("editions/reader_manuscript/v2_0/epub_disposition.json"),
        "reader_pdf": load("editions/reader_manuscript/v2_0/pdf_disposition.json"),
        "workflow": text("docs/living_update_workflow.md"),
        "master": text("prompts/MASTER_CODEX_PROMPT.md"),
        "outline": text("docs/book_outline.md"),
        "changelog": text("appendices/F_changelog.qmd"),
        "public": {path: text(path) for path in PUBLIC_SURFACES},
        "active_roadmaps": active_roadmaps(),
    }


def errors(data: dict) -> list[str]:
    out: list[str] = []
    status = data["status"]
    try:
        jsonschema.Draft202012Validator(data["schema"]).validate(status)
    except jsonschema.ValidationError as exc:
        out.append(f"status schema: {exc.message}")

    if status.get("status") != "active":
        out.append("roadmap must remain active until terminal closure and successor activation")
    if data["active_roadmaps"] != [ROADMAP]:
        out.append("there must be exactly one active canonical roadmap and it must be this successor")
    if status.get("predecessor", {}).get("path") != PREDECESSOR or data["predecessor_status"].get("status") != "completed":
        out.append("completed predecessor authority is absent or drifted")
    if "Status: completed 2026-07-14; no active successor" not in data["predecessor"]:
        out.append("predecessor historical completion text drifted")

    structure_rows = chapters(data["structure"])
    chapter_ids = [row.get("id") for row in structure_rows]
    source_rows = data["sources"] if isinstance(data["sources"], list) else data["sources"].get("sources", [])
    program = status.get("chapter_claim_program", [])
    program_ids = [row.get("chapter_id") for row in program]
    if len(chapter_ids) != 55 or program_ids != chapter_ids:
        out.append("the live machine proof program must cover all 55 manifest chapters once and in order")
    if len(set(program_ids)) != 55:
        out.append("chapter proof-program ownership is missing or duplicated")
    for row in program:
        if row.get("claim_id") != f"{row.get('chapter_id')}.core":
            out.append(f"{row.get('chapter_id')}: core claim identity drifted")
    family_ids = [row.get("id") for row in status.get("claim_families", [])]
    if family_ids != [f"CF-{index:02d}" for index in range(1, 9)]:
        out.append("claim-family order must be CF-01 through CF-08")
    if set(row.get("family_id") for row in program) != set(family_ids):
        out.append("every claim family must own at least one chapter and no unknown family may appear")

    remediation = status.get("latest_review_remediation_contract", {})
    expected_remediation = {
        "state": "installed",
        "review_kind": "claude_claim_proof_cycle_review",
        "wip_changed_path_soft_limit": 250,
        "wip_independent_work_package_limit": 3,
        "scope_expansion_blocked_above_limit": True,
        "checkpoint_inventory_required": True,
        "checkpoint_inventory_path": "roadmap_records/post_v2_3_wip_checkpoint_inventory.json",
        "checkpoint_inventory_state": "checkpoint_blocked_no_commit_authority",
        "commit_requires_explicit_authorization": True,
        "no_commit_authority_disposition": "checkpoint_blocked_no_commit_authority",
        "first_campaign_minimum_terminal_atom_count": 3,
        "first_campaign_promotion_required": False,
        "broad_p5_expansion_blocked_until_batch_terminal": True,
        "p6_claim_atoms_frozen_before_run": True,
        "p6_dated_comparator_ledger_required_before_run": True,
        "p6_reproduction_range_frozen_before_comparison": True,
        "p6_onecell_defeat_prediction_required_before_run": True,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    for key, value in expected_remediation.items():
        if remediation.get(key) != value:
            out.append(f"latest-review remediation drifted: {key}")
    expected_first_atoms = [
        "circle-calculus-and-proof-carrying-ai-contracts.mechanism.003",
        "system-boundaries-and-authority.invariant.001",
        "capability-replacement-and-rollback.invariant.011",
    ]
    if remediation.get("first_campaign_atom_ids") != expected_first_atoms:
        out.append("latest-review first campaign batch drifted")
    registered_atom_ids = {row.get("atom_id") for row in data["claim_atom_registry"].get("atoms", [])}
    if not set(expected_first_atoms).issubset(registered_atom_ids):
        out.append("latest-review first campaign batch contains an unregistered atom")

    instrument = status.get("instrument_adequacy_and_disposition_contract", {})
    expected_instrument = {
        "state": "installed_and_historical_lineage_corrected",
        "review_kind": "claude_evidence_transition_and_instrument_review",
        "historical_instrument_limited_result_path": "docs/post_v2_3_campaign_results.md",
        "historical_claim_label": "no_change",
        "required_superseding_protocol_outcome": "instrument_inadequate_recampaign_required",
        "supersession_path": "evidence_transitions/post_v2_3/instrument_failure_supersession.json",
        "superseded_historical_transition_count": 2,
        "superseded_transition_claim_attempt_count": 0,
        "separate_repaired_governance_tax_transition_preserved": True,
        "history_rewrite_allowed": False,
        "instrument_failure_counts_as_claim_attempt": False,
        "reasoning_and_final_decision_channels_separate": True,
        "schema_constrained_final_decoding_required_where_supported": True,
        "reasoning_and_answer_budgets_separate": True,
        "minimum_schema_admissible_rate": 0.8,
        "zero_candidate_arm_allowed": False,
        "strong_current_model_required_for_claim_bearing_work": True,
        "small_local_model_allowed_as_floor_or_control_only": True,
        "syntax_validity_counts_as_semantic_correctness": False,
        "new_top_level_outcome_requires_schema_migration_and_rejecting_test": True,
        "refinement_module_requires_consumed_nonrestating_property_or_retirement": True,
        "review_named_refinement_module_gate_state": "completed",
        "review_named_composition_theorem_count": 6,
        "review_named_cross_stage_mutation_count": 9,
        "review_named_cross_stage_mutation_rejection_count": 9,
        "review_named_support_state_effect": "none",
        "top_level_theorem_count_counts_as_semantic_adequacy": False,
        "local_reader_artifact_completion_required": True,
        "external_publication_authorized": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    for key, value in expected_instrument.items():
        if instrument.get(key) != value:
            out.append(f"instrument-adequacy contract drifted: {key}")
    if instrument.get("canonical_protocol_outcomes") != [
        "instrument_adequate",
        "instrument_inadequate_recampaign_required",
    ]:
        out.append("canonical protocol outcomes drifted")
    if instrument.get("canonical_claim_outcomes") != [
        "support_raised",
        "support_retained",
        "claim_narrowed",
        "claim_refuted",
        "claim_deprecated",
        "blocked_after_full_attempt",
    ]:
        out.append("canonical claim outcomes drifted")
    if instrument.get("review_named_refinement_modules") != [
        "PolicyOptimizationRefinement",
        "DataEngineLifecycleRefinement",
        "OpenEndedImprovementRefinement",
    ]:
        out.append("review-named refinement-module gate membership drifted")
    historical_campaign = data["roadmap"]
    for phrase in [
        "All 36 calls exhausted the 256-token cap",
        "The later repaired 32-candidate governance-tax campaign remains a separate valid `no_change` result",
        "schema-, or type-constrained decoding",
        "An instrument failure is not a claim result.",
    ]:
        if phrase not in historical_campaign:
            out.append(f"roadmap missing instrument-remediation boundary: {phrase}")
    wip = data["wip_checkpoint_inventory"]
    if wip.get("base_commit") != "1faacc14d1134192a5776715a38d704c16fbb62b":
        out.append("WIP checkpoint base commit drifted")
    if wip.get("independent_work_package_count") != len(wip.get("packages", [])) or len(wip.get("packages", [])) != 7:
        out.append("WIP checkpoint package inventory drifted")
    if wip.get("changed_path_count") != 296 or wip.get("threshold_exceeded") is not True or wip.get("scope_expansion_blocked") is not False:
        out.append("current inventoried WIP snapshot drifted")
    checkpoint_commit = "9b06a40e5028ad5636c254aba00c11490011cabe"
    checkpoint_tree = "d1efe9f9731ffbddaebea900b24c4c1cc50d25e0"
    if wip.get("checkpoint_disposition") != "checkpoint_committed_attested_closure_recorded" or wip.get("commit_authorized") is not True:
        out.append("authorized WIP checkpoint disposition drifted")
    if wip.get("checkpoint_commit") != checkpoint_commit or wip.get("closure_commit") != "self_commit_containing_this_record":
        out.append("WIP checkpoint or symbolic closure identity drifted")
    closure = wip.get("checkpoint_closure", {})
    if closure.get("attestation_result_path") != "roadmap_records/post_v2_3_checkpoint_attestation_2026_07_16.json":
        out.append("authorized WIP checkpoint attestation path drifted")
    if closure.get("attestation_state") != "passed_committed_object_and_clean_worktree":
        out.append("authorized WIP checkpoint attestation state drifted")
    if closure.get("dependent_artifact_reality_state") != "committed_object_attested":
        out.append("authorized WIP dependent-attestation boundary drifted")
    if closure.get("closure_commit_parent_is_checkpoint_commit") is not True:
        out.append("authorized WIP parent/closure assertion drifted")
    if closure.get("worktree_was_clean_after_closure_commit") is not True or closure.get("external_actions_authorized") is not True:
        out.append("authorized WIP closure boundary drifted")
    attestation = data["checkpoint_attestation"]
    if attestation.get("checkpoint_commit") != checkpoint_commit or attestation.get("checkpoint_tree") != checkpoint_tree:
        out.append("checkpoint attestation identity drifted")
    if attestation.get("closure_commit_required_parent") != checkpoint_commit:
        out.append("checkpoint attestation closure-parent binding drifted")
    checks = attestation.get("committed_object_checks", {})
    if not checks or not all(checks.values()):
        out.append("checkpoint committed-object checks are incomplete")
    if attestation.get("raw_kerc_source_tracked") is not False:
        out.append("checkpoint attestation invented raw KERC publication")
    if wip.get("support_state_effect") != "none" or wip.get("release_effect") != "none":
        out.append("WIP checkpoint invented support or release effect")

    reflexive_source = status.get("reflexive_router_source_contract", {})
    expected_reflexive_source = {
        "state": "integrated_argument_only_existing_chapters_first",
        "source_id": "reflexive_router_whitepaper",
        "source_note_path": "sources/source_notes/reflexive_router_whitepaper.md",
        "backlog_path": "research_backlog_records/reflexive_router_whitepaper_2026_07_16.json",
        "triage_path": "new_paper_triage_scenarios/reflexive_router_whitepaper_2026_07_16.json",
        "canonical_local_markdown_path": "sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.md",
        "canonical_local_markdown_sha256": "003a693741c40ca96ec3aece5b76ee90ec95a1d6c27ec81a970cff175f509068",
        "local_docx_path": "sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.docx",
        "local_docx_sha256": "52bc04a1bfedaa0fe3a7e530570703bd973849f46b806529f2534509101ace9b",
        "primary_chapter_owner": "routing-heads-and-specialist-cores",
        "existing_chapter_target_count": 12,
        "manifest_assigned_chapter_count": 12,
        "chapter_decision": "update_existing_chapters",
        "new_chapter_state": "deferred_pending_observed_distinct_interface",
        "campaign_owner": "P4.Campaign2",
        "book_integration_owner": "P7",
        "passage_review_state": "complete_chapter_mapped",
        "book_integration_state": "completed_argument_only_2026_07_16",
        "trace_schema_path": "schemas/reflexive_dispatch_trace_record.schema.json",
        "trace_fixture_path": "tests/fixtures/protocol_records/reflexive_dispatch_trace_record.valid.json",
        "trace_validator_path": "scripts/validate_reflexive_dispatch_trace.py",
        "trace_negative_mutation_count": 11,
        "external_reference_review_state": "pending_current_primary_source_verification",
        "support_state_effect": "none",
        "raw_source_publication_authority": "none",
        "release_authority": "none",
    }
    for key, expected_value in expected_reflexive_source.items():
        if reflexive_source.get(key) != expected_value:
            out.append(f"Reflexive Router source contract drifted: {key}")
    for key in ["source_note_path", "backlog_path", "triage_path", "canonical_local_markdown_path", "local_docx_path", "trace_schema_path", "trace_fixture_path", "trace_validator_path"]:
        if not (ROOT / reflexive_source.get(key, "missing")).exists():
            out.append(f"Reflexive Router source artifact is missing: {key}")
    for phrase in [
        "Accepted source integration — The Reflexive Router v1.2",
        "fails the new-chapter test",
        "argument-only prose integration is complete",
        "Reflexive Dispatch Trace",
        "Reflexive routing, ambiguous dispatch, and real-model deliberation",
        "bypass inference but may not bypass authorization",
        "observed distinct-interface gate",
    ]:
        if phrase not in data["roadmap"]:
            out.append(f"roadmap missing Reflexive Router integration boundary: {phrase}")

    execution_contract = status.get("self_contained_execution_contract", {})
    expected_execution_contract = {
        "state": "active_no_external_conversational_dependencies",
        "future_chatgpt_browser_runs_required": False,
        "future_external_conversation_runs_required": False,
        "routine_local_work_additional_user_authorization_required": False,
        "optional_model_unavailability_blocks_roadmap": False,
        "model_substitution_policy": "prospectively_freeze_available_codex_local_or_open_weight_role_with_exact_identity_limitations_and_claim_ceiling",
        "instrument_repair_mode": "local_versioned_repair_with_candidate_before_label_closure_independent_evaluators_mutations_and_replay",
        "historical_chat_pro_receipts_retained": True,
        "browser_scope": "automated_local_render_validation_only_not_hosted_conversation",
        "external_publication_completion_route": "ready_not_published",
        "support_state_effect": "none",
        "release_authority": "none",
    }
    if execution_contract != expected_execution_contract:
        out.append("self-contained execution contract drifted or restored an artificial dependency")

    governed_contract = status.get("governed_usefulness_campaign_contract", {})
    expected_governed_contract = {
        "state": "m5_bounded_local_confirmatory_support_complete",
        "preregistration_path": GOVERNED_USEFULNESS_PREREG,
        "access_preflight_path": GOVERNED_USEFULNESS_ACCESS,
        "v1_result_path": GOVERNED_USEFULNESS_V1_RESULT,
        "v1_protocol_outcome": "instrument_inadequate_recampaign_required",
        "v1_schema_admissible_task_count": 6,
        "v1_semantically_correct_task_count": 1,
        "v1_elapsed_seconds": 171.865,
        "v2_preregistration_path": GOVERNED_USEFULNESS_V2_PREREG,
        "v2_raw_response_path": "experiments/p4_governed_usefulness/raw/strong_model_sacrificial_preflight_v2.json",
        "v2_result_path": GOVERNED_USEFULNESS_V2_RESULT,
        "v2_diagnosis_path": GOVERNED_USEFULNESS_V2_DIAGNOSIS,
        "v2_protocol_outcome": "instrument_inadequate_recampaign_required",
        "v2_schema_admissible_task_count": 6,
        "v2_semantically_correct_task_count": 3,
        "v2_exact_residual_match_count": 6,
        "v2_evaluator_disagreement_count": 0,
        "v2_identity_drift_detected": False,
        "v2_elapsed_seconds": 170.996,
        "local_instrument_repair_state": "qualified_v9_eligibility_and_residual_only",
        "local_instrument_protocol_id": "p4-gu-local-instrument-qualification-v9",
        "local_instrument_result_path": "experiments/p4_governed_usefulness/results/local_instrument_qualification_v9.json",
        "local_instrument_protocol_outcome": "instrument_adequate_for_terminal_eligibility_and_residual_contract_only",
        "local_instrument_schema_admissible_task_count": 8,
        "local_instrument_semantically_correct_task_count": 8,
        "local_instrument_exact_remediation_action_count": 6,
        "local_instrument_failed_protocol_count": 5,
        "local_instrument_abandoned_protocol_count": 1,
        "future_chat_pro_run_required": False,
        "external_submission_authority_required": False,
        "difficulty_sweep_design_path": "experiments/p4_governed_usefulness/difficulty_sweep_design.json",
        "difficulty_sweep_design_state": "terminal_pool_adequate_confirmatory_completed",
        "difficulty_sweep_result_path": "experiments/p4_governed_usefulness/results/difficulty_sweep_result.json",
        "difficulty_sweep_protocol_outcome": "non_estimable_operating_range_repair_required",
        "difficulty_sweep_schema_admissible_candidate_count": 14,
        "difficulty_sweep_useful_safe_count": 1,
        "difficulty_sweep_useful_unsafe_count": 0,
        "difficulty_sweep_useless_safe_count": 10,
        "difficulty_sweep_useless_unsafe_count": 3,
        "difficulty_sweep_task_count": 16,
        "difficulty_sweep_family_count": 8,
        "difficulty_sweep_policy_arm_count": 6,
        "difficulty_sweep_four_cell_count": 4,
        "difficulty_sweep_evaluator_implementation_count": 2,
        "difficulty_sweep_required_effect_probe_count": 5,
        "difficulty_sweep_runner_state": "executed_once_and_closed_after_non_estimable_result",
        "difficulty_sweep_runner_self_test_cell_count": 4,
        "difficulty_sweep_runner_self_test_effect_probe_count": 5,
        "difficulty_sweep_runner_candidate_mutation_rejection_count": 6,
        "difficulty_sweep_normal_execution_allowed": False,
        "difficulty_sweep_result_exists": True,
        "sacrificial_task_count": 6,
        "minimum_schema_admissible_rate": 0.8,
        "minimum_semantically_correct_admissible_task_count": 4,
        "v2_minimum_semantically_correct_admissible_task_count": 5,
        "difficulty_sweep_state": "terminal_tuning_pool_adequate_after_v2_through_v5",
        "tuning_pool_result_path": "experiments/p4_governed_usefulness/results/difficulty_sweep_v2_v5_pool_result.json",
        "tuning_pool_protocol_outcome": "operating_range_adequate_to_freeze_fresh_held_out_confirmatory_design",
        "tuning_pool_expected_candidate_count": 40,
        "tuning_pool_schema_admissible_candidate_count": 32,
        "tuning_pool_useful_safe_count": 9,
        "tuning_pool_useful_unsafe_count": 2,
        "tuning_pool_useless_safe_count": 10,
        "tuning_pool_useless_unsafe_count": 11,
        "tuning_pool_evaluator_disagreement_count": 0,
        "tuning_pool_effect_probe_count": 20,
        "confirmatory_result_path": "experiments/p4_governed_usefulness/results/confirmatory_result.json",
        "confirmatory_protocol_outcome": "bounded_local_governance_effect_supported",
        "confirmatory_expected_task_count": 16,
        "confirmatory_schema_admissible_candidate_count": 15,
        "confirmatory_evaluator_disagreement_count": 0,
        "confirmatory_full_governance_useful_release_count": 9,
        "confirmatory_full_governance_unsafe_release_count": 0,
        "confirmatory_simple_baseline_useful_release_count": 0,
        "confirmatory_evidence_freshness_ablation_unsafe_release_count": 1,
        "confirmatory_denominator_state": "opened_once_and_terminally_closed",
        "model_inference_call_count": 14,
        "claim_attempt_count": 1,
        "support_state_effect": "eligible_for_bounded_local_non_core_promotion_after_reconciliation",
        "publication_authority": "none",
        "release_authority": "none",
    }
    for key, expected_value in expected_governed_contract.items():
        if governed_contract.get(key) != expected_value:
            out.append(f"governed-usefulness campaign contract drifted: {key}")
    for key in ["local_instrument_result_path", "difficulty_sweep_result_path", "tuning_pool_result_path", "confirmatory_result_path"]:
        if not (ROOT / governed_contract.get(key, "missing")).exists():
            out.append(f"governed-usefulness current result artifact missing: {key}")
    governed_prereg = data["governed_usefulness_prereg"]
    governed_access = data["governed_usefulness_access"]
    governed_v1_result = data["governed_usefulness_v1_result"]
    governed_v2_prereg = data["governed_usefulness_v2_prereg"]
    governed_v2_result = data["governed_usefulness_v2_result"]
    governed_v2_diagnosis = data["governed_usefulness_v2_diagnosis"]
    if governed_prereg.get("state") != "terminal_instrument_inadequate_recampaign_required":
        out.append("governed-usefulness v1 preregistration erases its terminal instrument failure")
    if governed_v1_result.get("protocol_outcome") != "instrument_inadequate_recampaign_required" or governed_v1_result.get("claim_attempt_counted") is not False:
        out.append("governed-usefulness v1 result was laundered into a claim result")
    if governed_v2_prereg.get("state") != "authorized_before_v2_strong_model_submission" or governed_v2_prereg.get("authorization", {}).get("prompt_submission_authority") != "explicit_user_authority_2026-07-16_run_v2_in_chat_pro":
        out.append("governed-usefulness v2 repair lacks the user's distinct action-time authority")
    if (
        governed_v2_result.get("protocol_outcome") != "instrument_inadequate_recampaign_required"
        or governed_v2_result.get("schema_admissible_task_count") != 6
        or governed_v2_result.get("semantically_correct_admissible_task_count") != 3
        or governed_v2_result.get("evaluator_disagreement_count") != 0
        or governed_v2_result.get("model_surface", {}).get("identity_drift_detected") is not False
        or governed_v2_result.get("claim_attempt_counted") is not False
        or governed_v2_result.get("difficulty_sweep_opened") is not False
    ):
        out.append("governed-usefulness v2 terminal instrument-failure result drifted or was laundered")
    if (
        governed_v2_diagnosis.get("observations", {}).get("exact_residual_match_count") != 6
        or governed_v2_diagnosis.get("adjudication", {}).get("decision_taxonomy") != "not_mutually_exclusive_under_the_task_wording"
        or governed_v2_diagnosis.get("retrospective_rescore_allowed") is not False
        or governed_v2_diagnosis.get("adjudication", {}).get("difficulty_sweep_effect") != "remains_closed"
    ):
        out.append("governed-usefulness v2 diagnosis erased label ambiguity, no-rescore, or closed-gate boundaries")
    if governed_access.get("displayed_model") != "GPT-5.6 Sol" or governed_access.get("displayed_mode") != "Pro":
        out.append("strong-model Chat Pro access observation drifted")
    if governed_access.get("prompt_submitted") is not True or governed_access.get("response_observed") is not True or governed_access.get("account_identifier_recorded") is not False:
        out.append("strong-model access receipt erases v1 inference or retains account identity")
    for phrase in [
        "M5 campaign-readiness receipt at 2026-07-16",
        "selects Chat `Pro`",
        "only one of six matched",
        "V1 is",
        "new v2 protocol is frozen",
        "6/6 exact residual classes",
        "only 3/6 exact decision classes",
        "closed historical instrument audits",
        "self-contained local instrument qualification",
        "V7 was abandoned before generation",
        "V9",
        "sixteen tasks",
        "one shared candidate per task/seed",
        "at least two",
        "observed cells were 1 useful-safe",
        "non_estimable_operating_range_repair_required",
        "Four prospectively frozen repair identities followed",
        "32/40 admitted candidates",
        "fresh confirmatory design",
        "released 9 useful and 0 unsafe candidates",
        "M5 is therefore complete",
    ]:
        if phrase not in data["roadmap"]:
            out.append(f"roadmap missing governed-usefulness boundary: {phrase}")
    for phrase in [
        "Finish from the repository, without conversational dependencies",
        "No new hosted-chat submission",
        "another conversational browser session an",
        "ready_not_published",
    ]:
        if phrase not in data["roadmap"]:
            out.append(f"roadmap missing self-contained execution boundary: {phrase}")

    vectors = data["vectors"].get("vectors", [])
    summary = data["vectors"].get("summary", {})
    registry_units = data["registry"].get("units", [])
    exact_contracts = sum(row.get("contract_precision") == "exact_high_impact" for row in registry_units)
    baseline = status.get("activation_baseline", {})
    expected = {
        "head_commit": "5eddb15d56b0c813666ed2b2ea41e7c87f1cf297",
        "latest_public_living_book_release": "v2.3.0",
        "active_chapter_count": 54,
        "public_safe_source_count": 287,
        "core_claim_count": 54,
        "core_argument_count": 54,
        "promoted_core_claim_count": 0,
        "refuted_core_claim_count": 0,
        "proof_target_count": 298,
        "lean_module_count": 65,
        "theorem_declaration_count": 1151,
        "direct_or_projection_theorem_count": 187,
        "derived_or_decomposed_theorem_count": 952,
        "unknown_or_mixed_theorem_count": 12,
        "adequate_finite_record_target_count": 13,
        "useful_but_too_narrow_target_count": 212,
        "richer_state_machine_needed_target_count": 18,
        "executable_tests_first_target_count": 35,
        "empirical_tests_first_target_count": 18,
        "research_agenda_target_count": 2,
        "external_positioned_chapter_count": 54,
        "externally_reproduced_core_claim_count": 0,
        "internal_only_evidence_vector_count": 54,
        "claim_scope_unmeasured_vector_count": 54,
        "transfer_not_established_vector_count": 54,
        "validation_unit_count": 313,
        "validation_required_artifact_count": 1352,
        "exact_high_impact_contract_count": 88,
    }
    for key, value in expected.items():
        if baseline.get(key) != value:
            out.append(f"activation baseline drifted: {key} expected {value!r}, got {baseline.get(key)!r}")
    current_units = {row.get("script") for row in registry_units}
    if "validate_post_v2_3_claim_proof_and_sota_challenge_roadmap.py" not in current_units:
        out.append("active roadmap validator is absent from the authoritative validation registry")
    if exact_contracts != 88:
        out.append("activation must not silently alter the 88 exact high-impact contract baseline")
    if len(vectors) != 55 or any(row.get("summary_support_state") != "argument" for row in vectors):
        out.append("live successor must preserve 55 argument-level chapter-core claims while the 54-claim activation baseline stays frozen")

    outcomes = data["flagship"].get("outcomes", {})
    task_quality = outcomes.get("task_quality", {})
    governed = outcomes.get("governed", {})
    baseline_arm = outcomes.get("baseline", {})
    if (
        baseline.get("governance_tax_independently_correct_candidate_count"),
        baseline.get("governance_tax_candidate_count"),
        baseline.get("governance_tax_baseline_useful_release_count"),
        baseline.get("governance_tax_governed_useful_release_count"),
    ) != (
        task_quality.get("independently_correct"),
        baseline_arm.get("runs"),
        baseline_arm.get("useful_releases"),
        governed.get("useful_releases"),
    ):
        out.append("governance-tax activation facts drifted")
    if data["reader_html"].get("decision") != "approved_exact_local_html_archive" or data["reader_docx"].get("decision") != "approved_exact_local_artifact":
        out.append("approved exact local HTML/DOCX reader history drifted")
    if data["reader_epub"].get("decision") != "blocked" or data["reader_pdf"].get("decision") != "blocked":
        out.append("EPUB/PDF application blockers were erased or laundered")

    priority_ids = [row.get("id") for row in status.get("priorities", [])]
    milestone_ids = [row.get("id") for row in status.get("milestones", [])]
    if priority_ids != [f"P{index}" for index in range(10)]:
        out.append("priority order must be P0 through P9")
    if milestone_ids != [f"M{index}" for index in range(14)]:
        out.append("milestone order must be M0 through M13")
    priority_states = [row.get("state") for row in status.get("priorities", [])]
    milestone_states = [row.get("state") for row in status.get("milestones", [])]
    in_progress_priorities = [index for index, state in enumerate(priority_states) if state == "in_progress"]
    if len(in_progress_priorities) != 1:
        out.append("exactly one priority must be in progress while the roadmap is active")
    else:
        current_index = in_progress_priorities[0]
        expected_states = ["completed"] * current_index + ["in_progress"] + ["pending"] * (9 - current_index)
        if priority_states != expected_states or status.get("current_priority") != f"P{current_index}":
            out.append("priority states and current_priority must form one monotone P0-P9 frontier")
    if milestone_states.count("in_progress") != 1:
        out.append("exactly one milestone must be in progress while the roadmap is active")
    if milestone_states and milestone_states[0] != "completed":
        out.append("M0 successor activation must remain completed")
    p1 = status.get("p1_claim_atom_program", {})
    expansion = status.get("structural_expansion_contract", {})
    expansion_atoms = data["structural_expansion_atoms"]
    expansion_chapter = next(
        (row for row in structure_rows if row.get("id") == "replaceable-cognitive-substrates-beyond-transformer-monoculture"),
        {},
    )
    abi_expected = {
        "abi_proof_state": "implemented_bounded_finite_model",
        "abi_lean_model_path": "lean/AsiStackProofs/ReplaceableCognitiveSubstrates.lean",
        "abi_model_adequacy_dossier_path": ABI_MODEL_DOSSIER,
        "abi_consumer_trace_path": ABI_TRACE,
        "abi_corpus_path": "experiments/cognitive_kernel_abi/corpus/2026-07-15.json",
        "abi_result_path": ABI_RESULT,
        "abi_case_count": 16,
        "abi_accepted_case_count": 1,
        "abi_rejected_case_count": 15,
        "abi_accepted_event_count": 9,
        "abi_committed_effect_count": 2,
        "abi_proposal_effect_count": 0,
        "abi_mutation_rejection_count": 12,
        "abi_support_state_effect": "none",
    }
    abi_result_expected = {
        "case_count": 16,
        "accepted_case_count": 1,
        "rejected_case_count": 15,
        "accepted_event_count": 9,
        "committed_effect_count": 2,
        "proposal_effect_count": 0,
        "mutation_rejection_count": 12,
        "support_state_effect": "none",
    }
    abi_target = next(
        (row for row in expansion_chapter.get("proof_targets", []) if row.get("tag") == "lean:cognitive_kernel.abi_trace_invariants"),
        {},
    )
    expansion_complete = (
        expansion.get("state") == "inserted_source_reviewed_and_atomized"
        and expansion.get("live_chapter_count") == len(chapter_ids) == 55
        and expansion.get("assigned_source_count") == 33
        and expansion.get("atom_count") == len(expansion_atoms.get("atoms", [])) == 15
        and expansion.get("pending_semantic_review_count") == 0
        and expansion_atoms.get("summary", {}).get("pending_semantic_review_count") == 0
        and expansion.get("support_state_effect") == "none"
        and expansion_atoms.get("support_state_effect") == "none"
        and all(expansion.get(key) == value for key, value in abi_expected.items())
        and all(data["abi_result"].get(key) == value for key, value in abi_result_expected.items())
        and abi_target.get("status") == "implemented"
        and (ROOT / expansion.get("intake_path", "missing")).exists()
        and (ROOT / expansion.get("claim_dossier_path", "missing")).exists()
    )
    if not expansion_complete:
        out.append("the accepted 55th chapter must remain inserted, source-reviewed, atomized, bounded-ABI validated, and non-promoted")
    for phrase in ["Adequacy adjudication", "Executable refinement boundary", "does not establish"]:
        if phrase.casefold() not in data["abi_model_dossier"].casefold():
            out.append(f"Cognitive Kernel ABI dossier missing adequacy boundary: {phrase}")
    for phrase in ["nine-event", "fifteen", "twelve", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["abi_trace"].casefold():
            out.append(f"Cognitive Kernel ABI trace receipt missing exact boundary: {phrase}")
    p1_complete = (
        p1.get("state") == "completed"
        and p1.get("structured_machine_candidate_count") == 0
        and p1.get("pending_prose_candidate_count") == 0
        and p1.get("semantic_chapter_sweep_completed_count") == 54
        and expansion_complete
    )
    if (priority_states[1] == "completed" or milestone_states[1] == "completed") and not p1_complete:
        out.append("P1/M1 completion requires zero machine and prose candidates and all chapter sweeps")
    if p1_complete and (priority_states[1] != "completed" or milestone_states[1] != "completed"):
        out.append("completed claim decomposition must be reflected by completed P1 and M1")
    if status.get("current_priority") == "P2":
        if milestone_states[3] != "in_progress" or status.get("proof_rationalization_contract", {}).get("state") != "in_progress":
            out.append("active P2 must activate M3 and the proof-rationalization contract")
    if status.get("external_human_prepublication_required") is not False:
        out.append("roadmap silently requires external-human prepublication review")
    if status.get("closure_requires_active_successor") is not True:
        out.append("same-transaction successor continuity is not machine-required")
    if status.get("support_state_effect") != "none" or status.get("release_effect") != "none":
        out.append("roadmap activation invented a support or release effect")

    proof_contract = status.get("proof_rationalization_contract", {})
    if proof_contract.get("baseline_theorem_declaration_count") != baseline.get("theorem_declaration_count"):
        out.append("proof-rationalization theorem baseline does not match activation truth")
    if proof_contract.get("baseline_proof_target_count") != baseline.get("proof_target_count"):
        out.append("proof-rationalization target baseline does not match activation truth")
    if proof_contract.get("chapter_dossier_count_required") != 54:
        out.append("proof rationalization must preserve all 54 activation-era dossiers; the authorized expansion has a separate live dossier")
    if proof_contract.get("argument_exit_campaign_required") is not True:
        out.append("argument-exit promotion-or-refutation campaigns are not required")
    if proof_contract.get("orphan_retained_theorem_allowed") is not False:
        out.append("orphan retained theorems were silently permitted")
    if proof_contract.get("projection_or_assumption_restatement_counts_as_semantic_proof") is not False:
        out.append("projection or assumption restatement was laundered as semantic proof")
    expected_safety_contract = {
        "shared_safety_model_adequacy_dossier_path": SAFETY_MODEL_DOSSIER,
        "shared_safety_consumer_trace_path": SAFETY_CONSUMER_TRACE,
        "shared_safety_consumer_result_path": SAFETY_CONSUMER_RESULT,
        "shared_safety_consumer_state": "validated_local_fixture_consumer_not_deployed",
        "shared_safety_consumer_receipt_count": 10,
        "shared_safety_committed_effect_count": 5,
        "shared_safety_denied_effect_count": 5,
        "shared_safety_support_state_effect": "none",
    }
    for key, value in expected_safety_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"shared safety consumer contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    safety_summary = data["safety_consumer_result"].get("summary", {})
    expected_safety_summary = {
        "receipt_count": 10,
        "committed_effect_count": 5,
        "denied_effect_count": 5,
        "residual_count": 5,
        "support_promotion_count": 0,
    }
    if safety_summary != expected_safety_summary:
        out.append(f"shared safety consumer summary drifted: expected {expected_safety_summary!r}, got {safety_summary!r}")
    if data["safety_consumer_result"].get("support_state_effect") != "none":
        out.append("shared safety consumer invented a support-state effect")
    for phrase in ["local finite consumer", "not a deployed", "no chapter-core support transition"]:
        if phrase.casefold() not in " ".join(data["safety_consumer_result"].get("non_claims", [])).casefold():
            out.append(f"shared safety consumer result missing non-claim: {phrase}")
    for phrase in ["Adequacy adjudication", "Executable refinement boundary", "does not establish"]:
        if phrase.casefold() not in data["safety_model_dossier"].casefold():
            out.append(f"shared safety model dossier missing adequacy boundary: {phrase}")
    for phrase in ["10", "5", "support-state effect", "none"]:
        if phrase.casefold() not in data["safety_consumer_trace"].casefold():
            out.append(f"shared safety consumer trace missing receipt fact: {phrase}")

    expected_integrated_contract = {
        "integrated_trace_model_path": "lean/AsiStackProofs/IntegratedReferenceTrace.lean",
        "integrated_trace_model_adequacy_dossier_path": INTEGRATED_TRACE_DOSSIER,
        "integrated_trace_consumer_path": INTEGRATED_TRACE_RECEIPT,
        "integrated_trace_consumer_result_path": INTEGRATED_TRACE_RESULT,
        "integrated_trace_consumer_state": "validated_source_anchored_finite_consumer_not_deployed",
        "integrated_trace_case_count": 18,
        "integrated_trace_accepted_case_count": 4,
        "integrated_trace_rejected_case_count": 14,
        "integrated_trace_accepted_event_count": 35,
        "integrated_trace_mutation_rejection_count": 15,
        "integrated_trace_support_state_effect": "none",
        "integrated_runtime_refinement_result_path": INTEGRATED_REFINEMENT_RESULT,
        "integrated_runtime_refinement_schema_path": INTEGRATED_REFINEMENT_SCHEMA,
        "integrated_runtime_refinement_state": "validated_one_projected_governed_result_schema_not_lean_verified_or_deployed",
        "integrated_runtime_refinement_scenario_count": 9,
        "integrated_runtime_refinement_round_trip_count": 9,
        "integrated_runtime_refinement_mutation_rejection_count": 20,
        "integrated_runtime_refinement_support_state_effect": "none",
        "concurrent_effect_consumer_path": CONCURRENT_EFFECT_RECEIPT,
        "concurrent_effect_result_path": CONCURRENT_EFFECT_RESULT,
        "concurrent_effect_state": "validated_finite_linearizable_consumer_not_distributed_or_deployed",
        "concurrent_effect_case_count": 16,
        "concurrent_effect_accepted_case_count": 4,
        "concurrent_effect_rejected_case_count": 12,
        "concurrent_effect_mutation_rejection_count": 12,
        "concurrent_effect_support_state_effect": "none",
    }
    for key, value in expected_integrated_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"integrated trace contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    integrated_summary = data["integrated_trace_result"]
    expected_integrated_summary = {
        "case_count": 18,
        "accepted_case_count": 4,
        "rejected_case_count": 14,
        "accepted_event_count": 35,
        "effect_attempt_count": 3,
        "final_net_effect_count": 2,
        "final_acknowledged_effect_count": 1,
        "final_open_residual_count": 3,
        "terminal_receipt_count": 4,
        "rolled_back_case_count": 1,
        "quarantined_case_count": 2,
        "support_transition_count": 0,
        "mutation_rejection_count": 15,
        "source_scenario_count": 6,
    }
    for key, value in expected_integrated_summary.items():
        if integrated_summary.get(key) != value:
            out.append(f"integrated trace summary drifted: {key} expected {value!r}, got {integrated_summary.get(key)!r}")
    if data["integrated_trace_result"].get("support_state_effect") != "none":
        out.append("integrated trace consumer invented a support-state effect")
    for phrase in ["Adequacy adjudication", "Executable refinement boundary", "does not establish"]:
        if phrase.casefold() not in data["integrated_trace_dossier"].casefold():
            out.append(f"integrated trace dossier missing adequacy boundary: {phrase}")
    for phrase in ["eighteen", "four accepted", "fourteen rejected", "fifteen", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["integrated_trace_receipt"].casefold():
            out.append(f"integrated trace receipt missing exact boundary: {phrase}")
    refinement = data["integrated_refinement_result"]
    expected_refinement = {
        "scenario_count": 9,
        "round_trip_count": 9,
        "mutation_count": 20,
        "mutation_rejection_count": 20,
        "support_state_effect": "none",
    }
    for key, value in expected_refinement.items():
        if refinement.get(key) != value:
            out.append(f"integrated runtime refinement drifted: {key} expected {value!r}, got {refinement.get(key)!r}")
    if refinement.get("trace_class_counts") != {
        "approved_completion": 3,
        "pre_effect_refusal": 3,
        "exact_rollback": 2,
        "failed_rollback_quarantine": 1,
    }:
        out.append("integrated runtime refinement trace-class counts drifted")
    concurrent = data["concurrent_effect_result"]
    for key, value in {
        "case_count": 16,
        "accepted_case_count": 4,
        "rejected_case_count": 12,
        "accepted_event_count": 17,
        "unique_effect_attempt_count": 5,
        "acknowledged_effect_count": 3,
        "compensated_effect_count": 1,
        "residualized_effect_count": 1,
        "mutation_rejection_count": 12,
        "support_state_effect": "none",
    }.items():
        if concurrent.get(key) != value:
            out.append(f"concurrent effect consumer drifted: {key} expected {value!r}, got {concurrent.get(key)!r}")
    for phrase in ["sixteen", "four accepted", "twelve rejected", "idempotency", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["concurrent_effect_receipt"].casefold():
            out.append(f"concurrent effect receipt missing exact boundary: {phrase}")

    expected_stack_contract = {
        "stack_boundary_model_path": "lean/AsiStackProofs/StackBoundaries.lean",
        "stack_boundary_dossier_path": STACK_BOUNDARY_DOSSIER,
        "stack_boundary_consumer_path": STACK_BOUNDARY_RECEIPT,
        "stack_boundary_result_path": STACK_BOUNDARY_RESULT,
        "stack_boundary_state": "validated_source_anchored_finite_consumer_not_deployed",
        "stack_boundary_layer_contract_case_count": 18,
        "stack_boundary_authority_fixture_count": 6,
        "stack_boundary_accepted_fixture_count": 3,
        "stack_boundary_rejected_fixture_count": 3,
        "stack_boundary_runtime_path_count": 3,
        "stack_boundary_accepted_event_count": 10,
        "stack_boundary_material_effect_count": 1,
        "stack_boundary_observed_effect_count": 1,
        "stack_boundary_exact_rollback_count": 1,
        "stack_boundary_no_mutation_denial_count": 2,
        "stack_boundary_revocation_entry_count": 5,
        "stack_boundary_mutation_rejection_count": 12,
        "stack_boundary_support_state_effect": "none",
    }
    for key, value in expected_stack_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"stack-boundary contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    stack_boundary = data["stack_boundary_result"]
    for key, value in {
        "layer_contract_case_count": 18,
        "layer_contract_route_match_count": 18,
        "authority_fixture_count": 6,
        "authority_fixture_accepted_count": 3,
        "authority_fixture_rejected_count": 3,
        "runtime_case_count": 3,
        "runtime_accepted_event_count": 10,
        "executed_effect_count": 1,
        "independently_observed_effect_count": 1,
        "exact_rollback_count": 1,
        "no_mutation_denial_count": 2,
        "revocation_trace_entry_count": 5,
        "mutation_rejection_count": 12,
        "support_state_effect": "none",
    }.items():
        if stack_boundary.get(key) != value:
            out.append(f"stack-boundary result drifted: {key} expected {value!r}, got {stack_boundary.get(key)!r}")
    for phrase in ["eighteen generated", "one material local temp-file effect", "twelve targeted", "support-state effect is `none`"]:
        if phrase.casefold() not in data["stack_boundary_receipt"].casefold():
            out.append(f"stack-boundary receipt missing exact boundary: {phrase}")
    for phrase in ["Adequacy adjudication", "Trusted computing base", "does not establish", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["stack_boundary_dossier"].casefold():
            out.append(f"stack-boundary dossier missing adequacy boundary: {phrase}")

    expected_intent_contract = {
        "intent_execution_model_path": "lean/AsiStackProofs/IntentExecutionRefinement.lean",
        "intent_execution_dossier_path": INTENT_EXECUTION_DOSSIER,
        "intent_execution_consumer_path": INTENT_EXECUTION_RECEIPT,
        "intent_execution_result_path": INTENT_EXECUTION_RESULT,
        "intent_execution_state": "validated_single_executed_schema_vertical_refinement_not_general_or_deployed",
        "intent_execution_scenario_count": 9,
        "intent_execution_event_count": 89,
        "intent_execution_release_count": 3,
        "intent_execution_pre_effect_refusal_count": 3,
        "intent_execution_exact_rollback_refusal_count": 2,
        "intent_execution_failed_rollback_quarantine_count": 1,
        "intent_execution_material_effect_count": 6,
        "intent_execution_observed_effect_count": 6,
        "intent_execution_residual_scenario_count": 2,
        "intent_execution_mutation_rejection_count": 30,
        "intent_execution_support_state_effect": "none",
    }
    for key, value in expected_intent_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"intent-execution contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    intent_result = data["intent_execution_result"]
    for key, value in {
        "scenario_count": 9, "release_count": 3, "pre_effect_refusal_count": 3,
        "exact_rollback_refusal_count": 2, "failed_rollback_quarantine_count": 1,
        "accepted_event_count": 89, "material_effect_count": 6,
        "independently_observed_effect_count": 6, "exact_rollback_count": 2,
        "open_residual_scenario_count": 2, "mutation_rejection_count": 30,
        "support_state_effect": "none",
    }.items():
        if intent_result.get(key) != value:
            out.append(f"intent-execution result drifted: {key} expected {value!r}, got {intent_result.get(key)!r}")
    for phrase in ["all nine", "all 89", "thirty", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["intent_execution_receipt"].casefold():
            out.append(f"intent-execution receipt missing exact boundary: {phrase}")
    for phrase in ["Adequacy adjudication", "Trusted computing base", "does not establish", "support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["intent_execution_dossier"].casefold():
            out.append(f"intent-execution dossier missing adequacy boundary: {phrase}")

    expected_authority_contract = {
        "authority_effect_model_path": "lean/AsiStackProofs/AuthorityEffectRefinement.lean",
        "authority_effect_dossier_path": AUTHORITY_EFFECT_DOSSIER,
        "authority_effect_consumer_path": AUTHORITY_EFFECT_RECEIPT,
        "authority_effect_result_path": AUTHORITY_EFFECT_RESULT,
        "authority_effect_state": "validated_finite_grant_effect_refinement_not_authentic_concurrent_or_deployed",
        "authority_effect_fixture_count": 6,
        "authority_effect_reachable_event_count": 6,
        "authority_effect_executed_effect_count": 1,
        "authority_effect_observed_effect_count": 1,
        "authority_effect_exact_rollback_count": 1,
        "authority_effect_pre_effect_denial_count": 2,
        "authority_effect_revocation_entry_count": 5,
        "authority_effect_governed_scenario_count": 9,
        "authority_effect_governed_release_count": 3,
        "authority_effect_governed_unsafe_release_count": 0,
        "authority_effect_mutation_rejection_count": 38,
        "authority_effect_support_state_effect": "none",
    }
    for key, value in expected_authority_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"authority-effect contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    authority_result = data["authority_effect_result"]
    for key, value in {
        "authority_fixture_count": 6, "reachable_trace_event_count": 6,
        "executed_local_effect_count": 1, "independently_observed_effect_count": 1,
        "exact_rollback_count": 1, "pre_effect_denial_count": 2,
        "revocation_trace_entry_count": 5, "governed_scenario_count": 9,
        "governed_release_count": 3, "governed_unsafe_release_count": 0,
        "mutation_rejection_count": 38, "support_state_effect": "none",
    }.items():
        if authority_result.get(key) != value:
            out.append(f"authority-effect result drifted: {key} expected {value!r}, got {authority_result.get(key)!r}")
    for phrase in ["six authority-decision fixtures", "nine governed repository-change scenarios", "38 single-fault", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["authority_effect_receipt"].casefold():
            out.append(f"authority-effect receipt missing exact boundary: {phrase}")
    for phrase in ["State, transitions, and reachable consequences", "Assumptions and exclusions", "does not establish completeness", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["authority_effect_dossier"].casefold():
            out.append(f"authority-effect dossier missing adequacy boundary: {phrase}")

    expected_intent_resolution_contract = {
        "intent_resolution_model_path": "lean/AsiStackProofs/IntentResolutionRefinement.lean",
        "intent_resolution_dossier_path": INTENT_RESOLUTION_DOSSIER,
        "intent_resolution_consumer_path": INTENT_RESOLUTION_RECEIPT,
        "intent_resolution_result_path": INTENT_RESOLUTION_RESULT,
        "intent_resolution_state": "validated_structured_request_contract_refinement_not_natural_language_or_deployed",
        "intent_resolution_intake_valid_count": 4,
        "intent_resolution_intake_invalid_count": 6,
        "intent_resolution_signal_count": 6,
        "intent_resolution_recontract_valid_count": 2,
        "intent_resolution_recontract_invalid_count": 7,
        "intent_resolution_plan_fixture_count": 13,
        "intent_resolution_reachable_event_count": 5,
        "intent_resolution_accepted_contract_version": 2,
        "intent_resolution_mutation_rejection_count": 30,
        "intent_resolution_support_state_effect": "none",
    }
    for key, value in expected_intent_resolution_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"intent-resolution contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    intent_resolution = data["intent_resolution_result"]
    for key, value in {
        "intake_valid_scenario_count": 4, "intake_invalid_control_count": 6,
        "intake_signal_count": 6, "recontract_valid_scenario_count": 2,
        "recontract_invalid_control_count": 7, "plan_fixture_count": 13,
        "reachable_trace_event_count": 5, "accepted_contract_version": 2,
        "mutation_rejection_count": 30, "support_state_effect": "none",
    }.items():
        if intent_resolution.get(key) != value:
            out.append(f"intent-resolution result drifted: {key} expected {value!r}, got {intent_resolution.get(key)!r}")
    for phrase in ["4 valid and 6 invalid intake cases", "2 valid and 7 invalid re-contract cases", "30 of 30", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["intent_resolution_receipt"].casefold():
            out.append(f"intent-resolution receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions and exclusions", "Hashes are abstract equality tokens", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["intent_resolution_dossier"].casefold():
            out.append(f"intent-resolution dossier missing adequacy boundary: {phrase}")

    expected_command_semantic_contract = {
        "command_semantic_model_path": "lean/AsiStackProofs/CommandSemanticRefinement.lean",
        "command_semantic_dossier_path": COMMAND_SEMANTIC_DOSSIER,
        "command_semantic_consumer_path": COMMAND_SEMANTIC_RECEIPT,
        "command_semantic_result_path": COMMAND_SEMANTIC_RESULT,
        "command_semantic_state": "validated_structured_command_boundary_not_natural_language_or_deployed",
        "command_semantic_plan_fixture_count": 13,
        "command_semantic_schema_valid_fixture_count": 13,
        "command_semantic_interface_violation_count": 5,
        "command_semantic_correct_block_count": 2,
        "command_semantic_interface_admissible_count": 6,
        "command_semantic_reachable_event_count": 5,
        "command_semantic_mutation_rejection_count": 38,
        "command_semantic_support_state_effect": "none",
    }
    for key, value in expected_command_semantic_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"command-semantic contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    command_semantic = data["command_semantic_result"]
    for key, value in {
        "plan_fixture_count": 13, "command_schema_valid_fixture_count": 13,
        "command_interface_violation_count": 5,
        "correctly_blocked_at_command_interface_count": 2,
        "command_interface_admissible_count": 6, "reachable_trace_event_count": 5,
        "mutation_rejection_count": 38, "support_state_effect": "none",
    }.items():
        if command_semantic.get(key) != value:
            out.append(f"command-semantic result drifted: {key} expected {value!r}, got {command_semantic.get(key)!r}")
    for phrase in ["all 13 command records", "five command-interface violations", "38 of 38 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["command_semantic_receipt"].casefold():
            out.append(f"command-semantic receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "Admissibility is deliberately consumer-relative", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["command_semantic_dossier"].casefold():
            out.append(f"command-semantic dossier missing adequacy boundary: {phrase}")

    expected_cognitive_compilation_contract = {
        "cognitive_compilation_model_path": "lean/AsiStackProofs/CognitiveCompilationRefinement.lean",
        "cognitive_compilation_dossier_path": COGNITIVE_COMPILATION_DOSSIER,
        "cognitive_compilation_consumer_path": COGNITIVE_COMPILATION_RECEIPT,
        "cognitive_compilation_result_path": COGNITIVE_COMPILATION_RESULT,
        "cognitive_compilation_state": "validated_structured_obligation_refinement_not_natural_language_or_backend",
        "cognitive_compilation_fixture_count": 6,
        "cognitive_compilation_accepted_fixture_count": 2,
        "cognitive_compilation_rejected_fixture_count": 4,
        "cognitive_compilation_reachable_event_count": 7,
        "cognitive_compilation_mutation_rejection_count": 47,
        "cognitive_compilation_support_state_effect": "none",
    }
    for key, value in expected_cognitive_compilation_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"cognitive-compilation contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    cognitive_compilation = data["cognitive_compilation_result"]
    for key, value in {"fixture_count": 6, "accepted_fixture_count": 2,
                       "rejected_fixture_count": 4, "reachable_trace_event_count": 7,
                       "mutation_rejection_count": 47, "support_state_effect": "none"}.items():
        if cognitive_compilation.get(key) != value:
            out.append(f"cognitive-compilation result drifted: {key} expected {value!r}, got {cognitive_compilation.get(key)!r}")
    for phrase in ["accepts exactly the two intended fixtures", "rejects the four expected-invalid fixtures", "47 of 47 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["cognitive_compilation_receipt"].casefold():
            out.append(f"cognitive-compilation receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "Schema validity alone", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["cognitive_compilation_dossier"].casefold():
            out.append(f"cognitive-compilation dossier missing adequacy boundary: {phrase}")

    expected_virtual_context_contract = {
        "virtual_context_model_path": "lean/AsiStackProofs/VirtualContextRefinement.lean",
        "virtual_context_dossier_path": VIRTUAL_CONTEXT_DOSSIER,
        "virtual_context_consumer_path": VIRTUAL_CONTEXT_RECEIPT,
        "virtual_context_result_path": VIRTUAL_CONTEXT_RESULT,
        "virtual_context_state": "validated_structured_binding_materialization_fault_refinement_not_real_payload_or_deployed",
        "virtual_context_resolver_scenario_count": 11,
        "virtual_context_resolver_valid_count": 2,
        "virtual_context_resolver_invalid_count": 9,
        "virtual_context_admission_fixture_count": 8,
        "virtual_context_admission_valid_count": 3,
        "virtual_context_admission_invalid_count": 5,
        "virtual_context_materialization_event_count": 4,
        "virtual_context_mandatory_miss_event_count": 2,
        "virtual_context_mutation_rejection_count": 55,
        "virtual_context_support_state_effect": "none",
    }
    for key, value in expected_virtual_context_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"virtual-context contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    virtual_context = data["virtual_context_result"]
    for key, value in {"resolver_scenario_count": 11, "resolver_valid_count": 2,
                       "resolver_invalid_count": 9, "admission_fixture_count": 8,
                       "admission_valid_fixture_count": 3, "admission_invalid_fixture_count": 5,
                       "materialization_trace_event_count": 4, "mandatory_miss_trace_event_count": 2,
                       "mutation_rejection_count": 55, "support_state_effect": "none"}.items():
        if virtual_context.get(key) != value:
            out.append(f"virtual-context result drifted: {key} expected {value!r}, got {virtual_context.get(key)!r}")
    for phrase in ["two valid and nine expected-invalid", "three-valid/five-invalid", "55 of 55 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["virtual_context_receipt"].casefold():
            out.append(f"virtual-context receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "admission validity is never treated as resolver correctness", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["virtual_context_dossier"].casefold():
            out.append(f"virtual-context dossier missing adequacy boundary: {phrase}")

    expected_context_certificate_contract = {
        "context_certificate_model_path": "lean/AsiStackProofs/ContextCertificateRefinement.lean",
        "context_certificate_dossier_path": CONTEXT_CERTIFICATE_DOSSIER,
        "context_certificate_consumer_path": CONTEXT_CERTIFICATE_RECEIPT,
        "context_certificate_result_path": CONTEXT_CERTIFICATE_RESULT,
        "context_certificate_state": "validated_structured_provenance_lifecycle_refinement_not_content_truth_or_deployed",
        "context_certificate_scenario_certificate_count": 12,
        "context_certificate_active_count": 11,
        "context_certificate_stale_count": 1,
        "context_certificate_admission_fixture_count": 8,
        "context_certificate_admission_valid_count": 3,
        "context_certificate_admission_invalid_count": 5,
        "context_certificate_reachable_event_count": 5,
        "context_certificate_mutation_rejection_count": 64,
        "context_certificate_support_state_effect": "none",
    }
    for key, value in expected_context_certificate_contract.items():
        if proof_contract.get(key) != value:
            out.append(f"context-certificate contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    context_certificate = data["context_certificate_result"]
    for key, value in {"scenario_certificate_count":12,"active_certificate_count":11,
                       "stale_certificate_count":1,"admission_valid_fixture_count":3,
                       "admission_invalid_fixture_count":5,"reachable_trace_event_count":5,
                       "mutation_rejection_count":64,"support_state_effect":"none"}.items():
        if context_certificate.get(key) != value:
            out.append(f"context-certificate result drifted: {key} expected {value!r}, got {context_certificate.get(key)!r}")
    for phrase in ["all 12 certificate records", "three-valid/five-invalid", "64 of 64 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["context_certificate_receipt"].casefold():
            out.append(f"context-certificate receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "do not classify the whole scenarios", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["context_certificate_dossier"].casefold():
            out.append(f"context-certificate dossier missing adequacy boundary: {phrase}")

    expected_context_transaction_contract = {
        "context_transaction_model_path":"lean/AsiStackProofs/ContextTransactionRefinement.lean",
        "context_transaction_dossier_path":CONTEXT_TRANSACTION_DOSSIER,
        "context_transaction_consumer_path":CONTEXT_TRANSACTION_RECEIPT,
        "context_transaction_result_path":CONTEXT_TRANSACTION_RESULT,
        "context_transaction_state":"validated_finite_sequential_snapshot_transaction_refinement_not_concurrent_or_deployed",
        "context_transaction_store_fixture_count":9,"context_transaction_store_valid_count":3,
        "context_transaction_store_invalid_count":6,"context_transaction_sequence_fixture_count":6,
        "context_transaction_sequence_valid_count":2,"context_transaction_sequence_invalid_count":4,
        "context_transaction_reachable_event_count":6,"context_transaction_mutation_rejection_count":78,
        "context_transaction_support_state_effect":"none"}
    for key,value in expected_context_transaction_contract.items():
        if proof_contract.get(key)!=value: out.append(f"context-transaction contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    transaction=data["context_transaction_result"]
    if transaction.get("store_suite",{}).get("valid_count")!=3 or transaction.get("store_suite",{}).get("invalid_count")!=6: out.append("context-transaction store suite drifted")
    if transaction.get("sequence_suite",{}).get("valid_count")!=2 or transaction.get("sequence_suite",{}).get("invalid_count")!=4: out.append("context-transaction sequence suite drifted")
    for key,value in {"reachable_trace_event_count":6,"mutation_rejection_count":78,"support_state_effect":"none"}.items():
        if transaction.get(key)!=value: out.append(f"context-transaction result drifted: {key}")
    for phrase in ["three-valid/six-invalid", "two-valid/four-invalid", "78 of 78 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["context_transaction_receipt"].casefold(): out.append(f"context-transaction receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "single-cell, sequential, and deterministic", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["context_transaction_dossier"].casefold(): out.append(f"context-transaction dossier missing adequacy boundary: {phrase}")

    expected_verification_bandwidth_contract = {
        "verification_bandwidth_model_path":"lean/AsiStackProofs/VerificationBandwidthRefinement.lean",
        "verification_bandwidth_dossier_path":VERIFICATION_BANDWIDTH_DOSSIER,
        "verification_bandwidth_consumer_path":VERIFICATION_BANDWIDTH_RECEIPT,
        "verification_bandwidth_result_path":VERIFICATION_BANDWIDTH_RESULT,
        "verification_bandwidth_state":"validated_finite_authored_evidence_gate_lifecycle_not_model_measured_or_deployed",
        "verification_bandwidth_admission_valid_count":3,"verification_bandwidth_admission_invalid_count":5,
        "verification_bandwidth_contradiction_valid_count":2,"verification_bandwidth_contradiction_invalid_count":7,
        "verification_bandwidth_capacity_valid_count":3,"verification_bandwidth_capacity_invalid_count":5,
        "verification_bandwidth_reachable_stage_count":5,"verification_bandwidth_route_case_count":12,
        "verification_bandwidth_mutation_rejection_count":31,
        "verification_bandwidth_strongest_effect":"handoff_to_independent_evidence_gate",
        "verification_bandwidth_support_state_effect":"none"}
    for key,value in expected_verification_bandwidth_contract.items():
        if proof_contract.get(key)!=value: out.append(f"verification-bandwidth contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    verification_bandwidth=data["verification_bandwidth_result"]
    for key,value in {"reachable_stage_count":5,"route_case_count":12,"mutation_rejection_count":31,
                      "strongest_effect":"handoff_to_independent_evidence_gate","support_state_effect":"none"}.items():
        if verification_bandwidth.get(key)!=value: out.append(f"verification-bandwidth result drifted: {key}")
    suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in verification_bandwidth.get("input_suites",[])}
    if suites!={"context_admission_adequacy":(3,5),"verification_bandwidth_probe":(2,7),"verification_bandwidth_capacity":(3,5)}: out.append("verification-bandwidth consumed-suite counts drifted")
    for phrase in ["3-valid/5-invalid admission", "2-valid/7-invalid contradiction", "3-valid/5-invalid capacity", "31 of 31", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["verification_bandwidth_receipt"].casefold(): out.append(f"verification-bandwidth receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "never owns evidence promotion", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["verification_bandwidth_dossier"].casefold(): out.append(f"verification-bandwidth dossier missing adequacy boundary: {phrase}")

    expected_claim_ledger_contract = {
        "current_missing_or_changed_theorem_count":296,
        "current_missing_or_changed_target_count":181,
        "current_live_theorem_declaration_count":1300,
        "current_live_proof_target_count":298,
        "claim_ledger_model_path":"lean/AsiStackProofs/ClaimLedgerRefinement.lean",
        "claim_ledger_dossier_path":CLAIM_LEDGER_DOSSIER,
        "claim_ledger_consumer_path":CLAIM_LEDGER_RECEIPT,
        "claim_ledger_result_path":CLAIM_LEDGER_RESULT,
        "claim_ledger_state":"validated_finite_authored_append_only_revision_lifecycle_not_semantic_concurrent_or_deployed",
        "claim_ledger_revision_valid_count":5,"claim_ledger_revision_invalid_count":7,
        "claim_ledger_historical_valid_count":1,"claim_ledger_historical_invalid_count":11,
        "claim_ledger_reachable_stage_count":5,"claim_ledger_route_case_count":17,
        "claim_ledger_mutation_rejection_count":29,
        "claim_ledger_retired_baseline_declaration_count":16,
        "claim_ledger_retained_legacy_theorem_count":4,
        "claim_ledger_support_state_effect":"none"}
    for key,value in expected_claim_ledger_contract.items():
        if proof_contract.get(key)!=value: out.append(f"claim-ledger contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    claim_ledger=data["claim_ledger_result"]
    for key,value in {"reachable_stage_count":5,"route_case_count":17,"mutation_count":29,
                      "mutation_rejection_count":29,"support_state_effect":"none"}.items():
        if claim_ledger.get(key)!=value: out.append(f"claim-ledger result drifted: {key}")
    claim_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in claim_ledger.get("input_suites",[])}
    if claim_suites!={"claim_ledger_revision":(5,7),"contradiction_revision_lifecycle":(1,11)}: out.append("claim-ledger consumed-suite counts drifted")
    for phrase in ["all seventeen routes", "five-valid/seven-invalid", "one-valid/eleven-invalid", "all 29 lifecycle mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["claim_ledger_receipt"].casefold(): out.append(f"claim-ledger receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "single-claim append-only event lifecycle", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["claim_ledger_dossier"].casefold(): out.append(f"claim-ledger dossier missing adequacy boundary: {phrase}")
    ledger_chapter=next((row for row in structure_rows if row.get("id")=="claim-ledgers-and-belief-revision"),{})
    ledger_target_modules={row.get("module") for row in ledger_chapter.get("proof_targets",[])}
    if ledger_target_modules!={"AsiStackProofs.ClaimLedgerRefinement"}: out.append("claim-ledger public targets do not all resolve to the refinement module")

    expected_proof_carrying_claims_contract = {
        "proof_carrying_claims_model_path":"lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean",
        "proof_carrying_claims_dossier_path":PROOF_CARRYING_CLAIMS_DOSSIER,
        "proof_carrying_claims_consumer_path":PROOF_CARRYING_CLAIMS_RECEIPT,
        "proof_carrying_claims_result_path":PROOF_CARRYING_CLAIMS_RESULT,
        "proof_carrying_claims_state":"validated_finite_authored_target_to_writeback_lifecycle_not_semantic_sound_natural_or_deployed",
        "proof_carrying_claims_fixture_valid_count":3,"proof_carrying_claims_fixture_invalid_count":5,
        "proof_carrying_claims_dossier_valid_count":2,"proof_carrying_claims_dossier_invalid_count":7,
        "proof_carrying_claims_reachable_stage_count":6,"proof_carrying_claims_route_case_count":23,
        "proof_carrying_claims_mutation_rejection_count":36,
        "proof_carrying_claims_retired_baseline_declaration_count":4,
        "proof_carrying_claims_retained_legacy_theorem_count":4,
        "proof_carrying_claims_support_state_effect":"none"}
    for key,value in expected_proof_carrying_claims_contract.items():
        if proof_contract.get(key)!=value: out.append(f"proof-carrying-claims contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    proof_carrying_claims=data["proof_carrying_claims_result"]
    for key,value in {"reachable_stage_count":6,"route_case_count":23,"mutation_count":36,
                      "mutation_rejection_count":36,"support_state_effect":"none"}.items():
        if proof_carrying_claims.get(key)!=value: out.append(f"proof-carrying-claims result drifted: {key}")
    proof_carrying_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in proof_carrying_claims.get("input_suites",[])}
    if proof_carrying_suites!={"proof_carrying_claims":(3,5),"adversarial_review_dossier":(2,7)}: out.append("proof-carrying-claims consumed-suite counts drifted")
    for phrase in ["all twenty-three routes", "three-valid/five-invalid", "two-valid/seven-invalid", "all 36 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["proof_carrying_claims_receipt"].casefold(): out.append(f"proof-carrying-claims receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "one target-specific verification event", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["proof_carrying_claims_dossier"].casefold(): out.append(f"proof-carrying-claims dossier missing adequacy boundary: {phrase}")
    proof_chapter=next((row for row in structure_rows if row.get("id")=="spinoza-verification-and-proof-carrying-claims"),{})
    proof_modules={row.get("tag"):row.get("module") for row in proof_chapter.get("proof_targets",[])}
    for tag in ("lean:spinoza.proof_carrying.operational_invariant","lean:spinoza.proof_carrying.failure_blocks_promotion","lean:spinoza.adversarial_review.dossier_probe_bridge"):
        if proof_modules.get(tag)!="AsiStackProofs.ProofCarryingClaimsRefinement": out.append(f"proof-carrying-claims target does not resolve to refinement: {tag}")

    expected_tribunal_contract = {
        "tribunal_model_path":"lean/AsiStackProofs/TribunalRefinement.lean",
        "tribunal_dossier_path":TRIBUNAL_DOSSIER,
        "tribunal_consumer_path":TRIBUNAL_RECEIPT,
        "tribunal_result_path":TRIBUNAL_RESULT,
        "tribunal_state":"validated_finite_authored_versioned_verdict_appeal_lifecycle_not_competence_correctness_or_deployed",
        "tribunal_review_valid_count":3,"tribunal_review_invalid_count":5,
        "tribunal_method_valid_count":1,"tribunal_method_invalid_count":11,
        "tribunal_reachable_stage_count":7,"tribunal_route_case_count":28,
        "tribunal_mutation_rejection_count":45,
        "tribunal_retired_baseline_declaration_count":10,
        "tribunal_retained_legacy_theorem_count":3,
        "tribunal_support_state_effect":"none"}
    for key,value in expected_tribunal_contract.items():
        if proof_contract.get(key)!=value: out.append(f"Tribunal contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    tribunal=data["tribunal_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":28,"mutation_count":45,
                      "mutation_rejection_count":45,"support_state_effect":"none"}.items():
        if tribunal.get(key)!=value: out.append(f"Tribunal result drifted: {key}")
    tribunal_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in tribunal.get("input_suites",[])}
    if tribunal_suites!={"tribunal_review":(3,5),"tribunal_method_independence":(1,11)}: out.append("Tribunal consumed-suite counts drifted")
    for phrase in ["twenty-eight routes", "three-valid/five-invalid", "one-valid/eleven-invalid", "all 45 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["tribunal_receipt"].casefold(): out.append(f"Tribunal receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "independence in fact", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["tribunal_dossier"].casefold(): out.append(f"Tribunal dossier missing adequacy boundary: {phrase}")
    for tag in ("lean:tribunal.review.operational_invariant","lean:tribunal.review.failure_blocks_promotion"):
        if proof_modules.get(tag)!="AsiStackProofs.TribunalRefinement": out.append(f"Tribunal target does not resolve to refinement: {tag}")

    expected_typed_job_contract = {
        "typed_job_model_path":"lean/AsiStackProofs/TypedJobRefinement.lean",
        "typed_job_dossier_path":TYPED_JOB_DOSSIER,
        "typed_job_consumer_path":TYPED_JOB_RECEIPT,
        "typed_job_result_path":TYPED_JOB_RESULT,
        "typed_job_state":"validated_finite_authored_versioned_execution_closure_lifecycle_not_task_success_enforcement_or_deployed",
        "typed_job_delivery_valid_count":2,"typed_job_delivery_invalid_count":7,
        "typed_job_durable_valid_count":2,"typed_job_durable_invalid_count":9,
        "typed_job_reachable_stage_count":7,"typed_job_route_case_count":28,
        "typed_job_mutation_rejection_count":42,
        "typed_job_retired_baseline_declaration_count":3,
        "typed_job_retained_legacy_theorem_count":24,
        "typed_job_support_state_effect":"none"}
    for key,value in expected_typed_job_contract.items():
        if proof_contract.get(key)!=value: out.append(f"typed-job contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    typed_job=data["typed_job_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":28,"mutation_count":42,
                      "mutation_rejection_count":42,"support_state_effect":"none"}.items():
        if typed_job.get(key)!=value: out.append(f"typed-job result drifted: {key}")
    typed_job_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in typed_job.get("input_suites",[])}
    if typed_job_suites!={"typed_job_delivery":(2,7),"typed_job_durable_lifecycle":(2,9)}: out.append("typed-job consumed-suite counts drifted")
    for phrase in ["twenty-eight routes", "two-valid/seven-invalid", "two-valid/nine-invalid", "all 42 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["typed_job_receipt"].casefold(): out.append(f"typed-job receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "task success", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["typed_job_dossier"].casefold(): out.append(f"typed-job dossier missing adequacy boundary: {phrase}")
    typed_job_chapter=next((row for row in structure_rows if row.get("id")=="labor-os-and-typed-jobs"),{})
    typed_job_modules={row.get("module") for row in typed_job_chapter.get("proof_targets",[])}
    if typed_job_modules!={"AsiStackProofs.TypedJobRefinement"}: out.append("typed-job public targets do not all resolve to the refinement module")

    expected_artifact_reality_contract = {
        "artifact_reality_model_path":"lean/AsiStackProofs/ArtifactRealityRefinement.lean",
        "artifact_reality_dossier_path":ARTIFACT_REALITY_DOSSIER,
        "artifact_reality_consumer_path":ARTIFACT_REALITY_RECEIPT,
        "artifact_reality_result_path":ARTIFACT_REALITY_RESULT,
        "artifact_reality_state":"validated_finite_authored_record_reality_trust_lifecycle_not_open_world_truth_replay_or_deployed",
        "artifact_reality_artifact_replay_valid_count":2,"artifact_reality_artifact_replay_invalid_count":6,
        "artifact_reality_record_sequence_valid_count":1,"artifact_reality_record_sequence_invalid_count":4,
        "artifact_reality_receipt_valid_count":3,"artifact_reality_receipt_invalid_count":6,
        "artifact_reality_repository_audit_valid_count":4,"artifact_reality_repository_audit_invalid_count":5,
        "artifact_reality_repository_challenge_valid_count":4,"artifact_reality_repository_challenge_invalid_count":5,
        "artifact_reality_live_attestation_valid_count":1,"artifact_reality_live_attestation_invalid_count":7,
        "artifact_reality_randomized_attestation_valid_count":4,"artifact_reality_randomized_attestation_invalid_count":8,
        "artifact_reality_tcb_valid_count":3,"artifact_reality_tcb_invalid_count":6,
        "artifact_reality_reachable_stage_count":7,"artifact_reality_route_case_count":33,
        "artifact_reality_mutation_rejection_count":53,
        "artifact_reality_retired_baseline_declaration_count":8,
        "artifact_reality_retained_legacy_theorem_count":35,
        "artifact_reality_support_state_effect":"none"}
    for key,value in expected_artifact_reality_contract.items():
        if proof_contract.get(key)!=value: out.append(f"artifact-reality contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    artifact_reality=data["artifact_reality_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":33,"mutation_count":53,
                      "mutation_rejection_count":53,"support_state_effect":"none"}.items():
        if artifact_reality.get(key)!=value: out.append(f"artifact-reality result drifted: {key}")
    artifact_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in artifact_reality.get("input_suites",[])}
    if artifact_suites!={"artifact_graph_replay":(2,6),"record_reality_sequence":(1,4),"receipt_faithfulness":(3,6),
                         "receipt_repository_audit":(4,5),"receipt_repository_challenge":(4,5),
                         "artifact_live_attestation":(1,7),"artifact_randomized_attestation":(4,8),"epistemic_tcb":(3,6)}:
        out.append("artifact-reality consumed-suite counts drifted")
    for phrase in ["thirty-three routes", "eight exact bounded suites", "all 53 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["artifact_reality_receipt"].casefold(): out.append(f"artifact-reality receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "inadequate for open-world provenance", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["artifact_reality_dossier"].casefold(): out.append(f"artifact-reality dossier missing adequacy boundary: {phrase}")
    artifact_chapter=next((row for row in structure_rows if row.get("id")=="artifact-graphs-audit-logs-and-replay"),{})
    artifact_modules={row.get("module") for row in artifact_chapter.get("proof_targets",[])}
    if artifact_modules!={"AsiStackProofs.ArtifactRealityRefinement"}: out.append("artifact-reality public targets do not all resolve to the refinement module")

    expected_procedural_memory_contract={
        "procedural_memory_model_path":"lean/AsiStackProofs/ProceduralMemoryRefinement.lean",
        "procedural_memory_dossier_path":PROCEDURAL_MEMORY_DOSSIER,
        "procedural_memory_consumer_path":PROCEDURAL_MEMORY_RECEIPT,
        "procedural_memory_result_path":PROCEDURAL_MEMORY_RESULT,
        "procedural_memory_state":"validated_finite_authored_promotion_retirement_lifecycle_not_natural_useful_or_deployed",
        "procedural_memory_loop_valid_count":3,"procedural_memory_loop_invalid_count":6,
        "procedural_memory_promotion_valid_count":1,"procedural_memory_promotion_invalid_count":10,
        "procedural_memory_reachable_stage_count":7,"procedural_memory_route_case_count":32,
        "procedural_memory_mutation_rejection_count":33,
        "procedural_memory_retired_baseline_declaration_count":5,
        "procedural_memory_retained_legacy_theorem_count":14,
        "procedural_memory_support_state_effect":"none"}
    for key,value in expected_procedural_memory_contract.items():
        if proof_contract.get(key)!=value: out.append(f"procedural-memory contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    procedural=data["procedural_memory_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":32,"mutation_count":33,"mutation_rejection_count":33,"support_state_effect":"none"}.items():
        if procedural.get(key)!=value: out.append(f"procedural-memory result drifted: {key}")
    procedural_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in procedural.get("input_suites",[])}
    if procedural_suites!={"procedural_memory_loop":(3,6),"procedural_trace_promotion":(1,10)}: out.append("procedural-memory consumed-suite counts drifted")
    for phrase in ["thirty-two routes", "all 33 mutations", "Support-state effect: `none`"]:
        if phrase.casefold() not in data["procedural_memory_receipt"].casefold(): out.append(f"procedural-memory receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "inadequate for natural trace discovery", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["procedural_memory_dossier"].casefold(): out.append(f"procedural-memory dossier missing adequacy boundary: {phrase}")
    procedural_chapter=next((row for row in structure_rows if row.get("id")=="procedural-memory-and-cognitive-loop-closure"),{})
    procedural_modules={row.get("module") for row in procedural_chapter.get("proof_targets",[])}
    if procedural_modules!={"AsiStackProofs.ProceduralMemoryRefinement"}: out.append("procedural-memory public targets do not all resolve to refinement")

    expected_routing_contract={
        "routing_model_path":"lean/AsiStackProofs/RoutingRefinement.lean",
        "routing_dossier_path":ROUTING_DOSSIER,
        "routing_consumer_path":ROUTING_RECEIPT,
        "routing_result_path":ROUTING_RESULT,
        "routing_state":"validated_finite_authored_request_lease_dispatch_outcome_lifecycle_not_useful_natural_or_deployed",
        "routing_lease_valid_count":3,"routing_lease_invalid_count":7,
        "routing_readiness_valid_count":4,"routing_readiness_invalid_count":5,
        "routing_reachable_stage_count":7,"routing_route_case_count":42,
        "routing_mutation_rejection_count":47,
        "routing_retired_baseline_declaration_count":16,
        "routing_retained_legacy_theorem_count":4,
        "routing_dispatch_count":1,"routing_route_outcome_count":1,"routing_answer_outcome_count":1,
        "routing_support_state_effect":"none"}
    for key,value in expected_routing_contract.items():
        if proof_contract.get(key)!=value: out.append(f"routing contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    routing=data["routing_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":42,"mutation_count":47,"mutation_rejection_count":47,"support_state_effect":"none"}.items():
        if routing.get(key)!=value: out.append(f"routing result drifted: {key}")
    routing_suites={row.get("suite_id"):row for row in routing.get("input_suites",[])}
    lease=routing_suites.get("routing_decision_lease",{})
    readiness=routing_suites.get("readiness_residual_gates",{})
    post_v2=routing_suites.get("post_v2_routing_deliberation",{})
    if (lease.get("valid_count"),lease.get("expected_invalid_count"))!=(3,7): out.append("routing lease consumed-suite counts drifted")
    if (readiness.get("valid_count"),readiness.get("expected_invalid_count"))!=(4,5): out.append("routing readiness consumed-suite counts drifted")
    expected_post_v2={"seed_count":3,"routing_record_count":900,"deliberation_record_count":540,
                      "learned_router_correct":162,"generalist_correct":130,"fallback_activation_count":0,
                      "adaptive_correct":179,"adaptive_candidate_operations":236,"fixed_correct":154,
                      "fixed_candidate_operations":540,"fixed_extra_compute_harm":15,
                      "no_change_disposition_count":2,"support_state_effect":"none"}
    for key,value in expected_post_v2.items():
        if post_v2.get(key)!=value: out.append(f"routing post-v2 exact result drifted: {key}")
    witness=routing.get("witness",{})
    for key,value in {"terminal_stage":"closed","receipt_count":6,"dispatch_count":1,"route_outcome_count":1,
                      "answer_outcome_count":1,"support_assignment_count":0,"external_effect_count":0}.items():
        if witness.get(key)!=value: out.append(f"routing witness drifted: {key}")
    for phrase in ["forty-two routes", "forty-seven registered mutations", "Route quality and answer quality", "no chapter-core support change"]:
        if phrase.casefold() not in data["routing_receipt"].casefold(): out.append(f"routing receipt missing exact boundary: {phrase}")
    for phrase in ["seven reachable stages", "forty-seven identity", "Inadequate for natural-task usefulness", "Do not infer"]:
        if phrase.casefold() not in data["routing_dossier"].casefold(): out.append(f"routing dossier missing adequacy boundary: {phrase}")
    routing_chapter=next((row for row in structure_rows if row.get("id")=="routing-heads-and-specialist-cores"),{})
    routing_modules={row.get("module") for row in routing_chapter.get("proof_targets",[])}
    if routing_modules!={"AsiStackProofs.RoutingRefinement"}: out.append("Routing/MoECOT public targets do not all resolve to refinement")

    expected_safety_case_contract={
        "safety_case_model_path":"lean/AsiStackProofs/SafetyCaseRefinement.lean",
        "safety_case_dossier_path":SAFETY_CASE_DOSSIER,
        "safety_case_consumer_path":SAFETY_CASE_RECEIPT,
        "safety_case_result_path":SAFETY_CASE_RESULT,
        "safety_case_state":"validated_finite_authored_case_readiness_invalidation_lifecycle_not_truth_safe_or_deployed",
        "safety_case_inherited_case_count":8,"safety_case_reachable_stage_count":6,
        "safety_case_route_case_count":30,"safety_case_mutation_rejection_count":35,
        "safety_case_retained_legacy_theorem_count":8,"safety_case_readiness_handoff_count":1,
        "safety_case_invalidation_count":1,"safety_case_support_state_effect":"none"}
    for key,value in expected_safety_case_contract.items():
        if proof_contract.get(key)!=value: out.append(f"safety-case contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    safety_case=data["safety_case_result"]
    for key,value in {"reachable_stage_count":6,"route_case_count":30,"mutation_count":35,
                      "mutation_rejection_count":35,"support_state_effect":"none"}.items():
        if safety_case.get(key)!=value: out.append(f"safety-case result drifted: {key}")
    if safety_case.get("input_suite")!={"suite_id":"safety_case_assurance","case_count":8,"passed_count":8}:
        out.append("safety-case inherited-suite counts drifted")
    for phrase in ["six-stage case lifecycle", "all 30 lifecycle routes", "35/35", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["safety_case_receipt"].casefold(): out.append(f"safety-case receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Assumptions, exclusions, and adequacy verdict", "Inadequate for assurance-argument truth", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["safety_case_dossier"].casefold(): out.append(f"safety-case dossier missing adequacy boundary: {phrase}")
    safety_case_chapter=next((row for row in structure_rows if row.get("id")=="safety-cases-and-structured-assurance"),{})
    if {row.get("module") for row in safety_case_chapter.get("proof_targets",[])}!={"AsiStackProofs.SafetyCaseRefinement"}:
        out.append("Safety Case public targets do not all resolve to refinement")

    expected_capability_threshold_contract={
        "capability_threshold_model_path":"lean/AsiStackProofs/CapabilityThresholdRefinement.lean",
        "capability_threshold_dossier_path":CAPABILITY_THRESHOLD_DOSSIER,
        "capability_threshold_consumer_path":CAPABILITY_THRESHOLD_RECEIPT,
        "capability_threshold_result_path":CAPABILITY_THRESHOLD_RESULT,
        "capability_threshold_state":"validated_finite_authored_repeated_assessment_lifecycle_not_capability_valid_or_deployed",
        "capability_threshold_inherited_case_count":8,"capability_threshold_reachable_stage_count":6,
        "capability_threshold_route_case_count":43,"capability_threshold_mutation_rejection_count":48,
        "capability_threshold_retained_legacy_theorem_count":8,"capability_threshold_readiness_handoff_count":1,
        "capability_threshold_reassessment_count":1,"capability_threshold_support_state_effect":"none"}
    for key,value in expected_capability_threshold_contract.items():
        if proof_contract.get(key)!=value: out.append(f"capability-threshold contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    capability_threshold=data["capability_threshold_result"]
    for key,value in {"reachable_stage_count":6,"route_case_count":43,"mutation_count":48,
                      "mutation_rejection_count":48,"support_state_effect":"none"}.items():
        if capability_threshold.get(key)!=value: out.append(f"capability-threshold result drifted: {key}")
    if capability_threshold.get("input_suite")!={"suite_id":"capability_threshold_commitment","case_count":8,"passed_count":8}:
        out.append("capability-threshold inherited-suite counts drifted")
    for phrase in ["six-stage lifecycle", "all 43 routes", "48/48", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["capability_threshold_receipt"].casefold(): out.append(f"capability-threshold receipt missing exact boundary: {phrase}")
    for phrase in ["Six stages", "Forty-three routes", "Inadequate for capability measurement", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["capability_threshold_dossier"].casefold(): out.append(f"capability-threshold dossier missing adequacy boundary: {phrase}")
    capability_threshold_chapter=next((row for row in structure_rows if row.get("id")=="capability-thresholds-and-deployment-commitments"),{})
    if {row.get("module") for row in capability_threshold_chapter.get("proof_targets",[])}!={"AsiStackProofs.CapabilityThresholdRefinement"}:
        out.append("Capability Threshold public targets do not all resolve to refinement")

    expected_adversarial_evaluation_contract={
        "adversarial_evaluation_model_path":"lean/AsiStackProofs/AdversarialEvaluationRefinement.lean",
        "adversarial_evaluation_dossier_path":ADVERSARIAL_EVALUATION_DOSSIER,
        "adversarial_evaluation_consumer_path":ADVERSARIAL_EVALUATION_RECEIPT,
        "adversarial_evaluation_result_path":ADVERSARIAL_EVALUATION_RESULT,
        "adversarial_evaluation_state":"validated_finite_authored_observation_reevaluation_lifecycle_not_detection_empirical_or_deployed",
        "adversarial_evaluation_inherited_case_count":8,"adversarial_evaluation_reachable_stage_count":7,
        "adversarial_evaluation_route_case_count":56,"adversarial_evaluation_mutation_rejection_count":60,
        "adversarial_evaluation_retained_legacy_theorem_count":8,"adversarial_evaluation_decision_handoff_count":1,
        "adversarial_evaluation_reevaluation_count":1,"adversarial_evaluation_support_state_effect":"none"}
    for key,value in expected_adversarial_evaluation_contract.items():
        if proof_contract.get(key)!=value: out.append(f"adversarial-evaluation contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    adversarial_evaluation=data["adversarial_evaluation_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":56,"mutation_count":60,
                      "mutation_rejection_count":60,"support_state_effect":"none"}.items():
        if adversarial_evaluation.get(key)!=value: out.append(f"adversarial-evaluation result drifted: {key}")
    if adversarial_evaluation.get("input_suite")!={"suite_id":"adversarial_evaluation_integrity","case_count":8,"passed_count":8}:
        out.append("adversarial-evaluation inherited-suite counts drifted")
    for phrase in ["seven-stage lifecycle", "all 56 routes", "60/60", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["adversarial_evaluation_receipt"].casefold(): out.append(f"adversarial-evaluation receipt missing exact boundary: {phrase}")
    for phrase in ["Seven stages", "Fifty-six routes", "Inadequate for deception detection", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["adversarial_evaluation_dossier"].casefold(): out.append(f"adversarial-evaluation dossier missing adequacy boundary: {phrase}")
    adversarial_evaluation_chapter=next((row for row in structure_rows if row.get("id")=="adversarial-evaluation-sandbagging-and-training-time-deception"),{})
    if {row.get("module") for row in adversarial_evaluation_chapter.get("proof_targets",[])}!={"AsiStackProofs.AdversarialEvaluationRefinement"}:
        out.append("Adversarial Evaluation public targets do not all resolve to refinement")

    expected_scalable_oversight_contract={
        "scalable_oversight_model_path":"lean/AsiStackProofs/ScalableOversightRefinement.lean",
        "scalable_oversight_dossier_path":SCALABLE_OVERSIGHT_DOSSIER,
        "scalable_oversight_consumer_path":SCALABLE_OVERSIGHT_RECEIPT,
        "scalable_oversight_result_path":SCALABLE_OVERSIGHT_RESULT,
        "scalable_oversight_state":"validated_finite_authored_oversight_review_readmission_lifecycle_not_competence_empirical_or_deployed",
        "scalable_oversight_inherited_case_count":7,"scalable_oversight_reachable_stage_count":7,
        "scalable_oversight_route_case_count":58,"scalable_oversight_mutation_rejection_count":65,
        "scalable_oversight_retained_legacy_theorem_count":8,"scalable_oversight_bounded_use_handoff_count":1,
        "scalable_oversight_readmission_count":1,"scalable_oversight_support_state_effect":"none"}
    for key,value in expected_scalable_oversight_contract.items():
        if proof_contract.get(key)!=value: out.append(f"scalable-oversight contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    scalable_oversight=data["scalable_oversight_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":58,"mutation_count":65,
                      "mutation_rejection_count":65,"support_state_effect":"none"}.items():
        if scalable_oversight.get(key)!=value: out.append(f"scalable-oversight result drifted: {key}")
    if scalable_oversight.get("input_suite")!={"suite_id":"scalable_oversight_protocol","case_count":7,"passed_count":7}:
        out.append("scalable-oversight inherited-suite counts drifted")
    for phrase in ["seven-stage lifecycle", "all 58 routes", "65/65", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["scalable_oversight_receipt"].casefold(): out.append(f"scalable-oversight receipt missing exact boundary: {phrase}")
    for phrase in ["Seven stages", "Fifty-eight routes", "Inadequate for reviewer competence", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["scalable_oversight_dossier"].casefold(): out.append(f"scalable-oversight dossier missing adequacy boundary: {phrase}")
    scalable_oversight_chapter=next((row for row in structure_rows if row.get("id")=="scalable-oversight-and-adversarial-ai-control"),{})
    if {row.get("module") for row in scalable_oversight_chapter.get("proof_targets",[])}!={"AsiStackProofs.ScalableOversightRefinement"}:
        out.append("Scalable Oversight public targets do not all resolve to refinement")

    expected_policy_optimization_contract={
        "policy_optimization_model_path":"lean/AsiStackProofs/PolicyOptimizationRefinement.lean",
        "policy_optimization_dossier_path":POLICY_OPTIMIZATION_DOSSIER,
        "policy_optimization_consumer_path":POLICY_OPTIMIZATION_RECEIPT,
        "policy_optimization_result_path":POLICY_OPTIMIZATION_RESULT,
        "policy_optimization_state":"validated_finite_authored_governed_update_readmission_lifecycle_not_learning_empirical_or_deployed",
        "policy_optimization_inherited_sample_count":6,"policy_optimization_inherited_candidate_count":5,
        "policy_optimization_reachable_stage_count":7,"policy_optimization_route_case_count":63,
        "policy_optimization_mutation_rejection_count":73,"policy_optimization_retained_legacy_theorem_count":11,
        "policy_optimization_bounded_lease_count":1,"policy_optimization_readmission_count":1,
        "policy_optimization_support_state_effect":"none"}
    for key,value in expected_policy_optimization_contract.items():
        if proof_contract.get(key)!=value: out.append(f"policy-optimization contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    policy_optimization=data["policy_optimization_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":63,"mutation_count":73,
                      "mutation_rejection_count":73,"cross_stage_mutation_count":3,
                      "cross_stage_mutation_rejection_count":3,"support_state_effect":"none"}.items():
        if policy_optimization.get(key)!=value: out.append(f"policy-optimization result drifted: {key}")
    if policy_optimization.get("composition_theorems") != [
        "policy_update_full_cycle_composes",
        "policy_update_failed_evaluation_blocks_downstream_handoff",
    ]: out.append("policy-optimization composition theorem binding drifted")
    inherited_policy=policy_optimization.get("inherited_lease_probe",{})
    for key,value in {"workload_sample_count":6,"holdout_sample_count":2,"candidate_count":5,
                      "rejected_negative_control_count":3,"selected_canary_promotion_decision":"keep_experimental",
                      "support_state_effect":"none"}.items():
        if inherited_policy.get(key)!=value: out.append(f"policy-optimization inherited result drifted: {key}")
    for phrase in ["seven-stage", "all 63 lifecycle routes", "73/73", "3/3 cross-stage", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["policy_optimization_receipt"].casefold(): out.append(f"policy-optimization receipt missing exact boundary: {phrase}")
    for phrase in ["Seven reachable stages", "all 63 routes", "Inadequate for policy improvement", "No support transition"]:
        if phrase.casefold() not in data["policy_optimization_dossier"].casefold(): out.append(f"policy-optimization dossier missing adequacy boundary: {phrase}")
    policy_optimization_chapter=next((row for row in structure_rows if row.get("id")=="policy-optimization-and-learning-from-feedback"),{})
    if {row.get("module") for row in policy_optimization_chapter.get("proof_targets",[])}!={"AsiStackProofs.PolicyOptimizationRefinement"}:
        out.append("Policy Optimization public targets do not all resolve to refinement")

    expected_data_engine_lifecycle_contract={
        "data_engine_lifecycle_model_path":"lean/AsiStackProofs/DataEngineLifecycleRefinement.lean",
        "data_engine_lifecycle_dossier_path":DATA_ENGINE_LIFECYCLE_DOSSIER,
        "data_engine_lifecycle_consumer_path":DATA_ENGINE_LIFECYCLE_RECEIPT,
        "data_engine_lifecycle_result_path":DATA_ENGINE_LIFECYCLE_RESULT,
        "data_engine_lifecycle_state":"validated_finite_authored_custody_update_deletion_readmission_lifecycle_not_learning_erasure_or_deployed",
        "data_engine_lifecycle_admission_scenario_count":4,
        "data_engine_lifecycle_full_state_surface_count":24,
        "data_engine_lifecycle_full_state_transaction_count":15,
        "data_engine_lifecycle_update_seed_count":3,
        "data_engine_lifecycle_update_arm_count":12,
        "data_engine_lifecycle_reachable_stage_count":8,
        "data_engine_lifecycle_route_case_count":82,
        "data_engine_lifecycle_mutation_rejection_count":96,
        "data_engine_lifecycle_retained_legacy_theorem_count":15,
        "data_engine_lifecycle_bounded_custody_count":1,
        "data_engine_lifecycle_readmission_count":1,
        "data_engine_lifecycle_support_state_effect":"none"}
    for key,value in expected_data_engine_lifecycle_contract.items():
        if proof_contract.get(key)!=value: out.append(f"data-engine lifecycle contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    data_engine_lifecycle=data["data_engine_lifecycle_result"]
    for key,value in {"reachable_stage_count":8,"route_case_count":82,"mutation_count":96,
                      "mutation_rejection_count":96,"cross_stage_mutation_count":3,
                      "cross_stage_mutation_rejection_count":3,"support_state_effect":"none"}.items():
        if data_engine_lifecycle.get(key)!=value: out.append(f"data-engine lifecycle result drifted: {key}")
    if data_engine_lifecycle.get("composition_theorems") != [
        "data_engine_full_cycle_composes",
        "data_engine_axis_laundering_blocks_custody_and_readmission",
    ]: out.append("data-engine lifecycle composition theorem binding drifted")
    inherited_data_engine=data_engine_lifecycle.get("inherited_results",{})
    for key,value in {"admission_scenario_count":4,"full_state_surface_count":24,
                      "full_state_transaction_count":15,"full_state_exact_rollback_count":15,
                      "full_state_storage_erasure_count":0,"update_seed_count":3,
                      "update_arm_count":12,"update_no_change_disposition_count":4,
                      "support_state_effect":"none"}.items():
        if inherited_data_engine.get(key)!=value: out.append(f"data-engine inherited result drifted: {key}")
    data_engine_witness=data_engine_lifecycle.get("witness",{})
    for key,value in {"terminal_stage":"scoped","protocol_version":2,"bounded_custody_count":1,
                      "readmission_count":1,"support_assignment_count":0,"external_effect_count":0}.items():
        if data_engine_witness.get(key)!=value: out.append(f"data-engine lifecycle witness drifted: {key}")
    for phrase in ["eight-stage custody lifecycle", "all 82 routes", "96/96", "3/3 cross-stage", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["data_engine_lifecycle_receipt"].casefold(): out.append(f"data-engine lifecycle receipt missing exact boundary: {phrase}")
    for phrase in ["Eight reachable stages", "all 82 routes", "Inadequate for source or rights truth", "No support transition"]:
        if phrase.casefold() not in data["data_engine_lifecycle_dossier"].casefold(): out.append(f"data-engine lifecycle dossier missing adequacy boundary: {phrase}")
    data_engine_chapter=next((row for row in structure_rows if row.get("id")=="data-engines-continual-learning-and-unlearning"),{})
    if {row.get("module") for row in data_engine_chapter.get("proof_targets",[])}!={"AsiStackProofs.DataEngineLifecycleRefinement"}:
        out.append("Data Engines public targets do not all resolve to refinement")

    expected_open_ended_improvement_contract={
        "open_ended_improvement_model_path":"lean/AsiStackProofs/OpenEndedImprovementRefinement.lean",
        "open_ended_improvement_dossier_path":OPEN_ENDED_IMPROVEMENT_DOSSIER,
        "open_ended_improvement_consumer_path":OPEN_ENDED_IMPROVEMENT_RECEIPT,
        "open_ended_improvement_result_path":OPEN_ENDED_IMPROVEMENT_RESULT,
        "open_ended_improvement_state":"validated_finite_authored_campaign_governor_readmission_lifecycle_not_adaptive_useful_safe_or_deployed",
        "open_ended_improvement_admission_case_count":7,
        "open_ended_improvement_update_seed_count":3,
        "open_ended_improvement_update_arm_count":12,
        "open_ended_improvement_stopped_seed_count":3,
        "open_ended_improvement_stopped_arm_count":15,
        "open_ended_improvement_stopped_model_call_count":332,
        "open_ended_improvement_stopped_threshold_pass_count":0,
        "open_ended_improvement_reachable_stage_count":7,
        "open_ended_improvement_route_case_count":81,
        "open_ended_improvement_mutation_rejection_count":91,
        "open_ended_improvement_retained_legacy_theorem_count":7,
        "open_ended_improvement_governor_handoff_count":1,
        "open_ended_improvement_readmission_count":1,
        "open_ended_improvement_support_state_effect":"none"}
    for key,value in expected_open_ended_improvement_contract.items():
        if proof_contract.get(key)!=value: out.append(f"open-ended-improvement contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    open_ended_improvement=data["open_ended_improvement_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":81,"mutation_count":91,
                      "mutation_rejection_count":91,"cross_stage_mutation_count":3,
                      "cross_stage_mutation_rejection_count":3,"support_state_effect":"none"}.items():
        if open_ended_improvement.get(key)!=value: out.append(f"open-ended-improvement result drifted: {key}")
    if open_ended_improvement.get("composition_theorems") != [
        "open_ended_improvement_full_cycle_composes",
        "open_ended_improvement_budget_reset_blocks_handoff_and_readmission",
    ]: out.append("open-ended-improvement composition theorem binding drifted")
    inherited_open_ended=open_ended_improvement.get("inherited_results",{})
    for key,value in {"admission_case_count":7,"update_seed_count":3,"update_arm_count":12,
                      "update_no_change_disposition_count":4,"stopped_seed_count":3,
                      "stopped_arm_count":15,"stopped_model_call_count":332,
                      "stopped_eligible_challenger_seed_arm_count":9,
                      "stopped_threshold_pass_count":0,"stopped_update_disposition":"no_change",
                      "support_state_effect":"none"}.items():
        if inherited_open_ended.get(key)!=value: out.append(f"open-ended-improvement inherited result drifted: {key}")
    open_ended_witness=open_ended_improvement.get("witness",{})
    for key,value in {"terminal_stage":"scoped","protocol_version":2,"governor_handoff_count":1,
                      "readmission_count":1,"support_assignment_count":0,"external_effect_count":0}.items():
        if open_ended_witness.get(key)!=value: out.append(f"open-ended-improvement witness drifted: {key}")
    for phrase in ["seven-stage lifecycle", "all 81 routes", "91/91", "3/3 cross-stage", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["open_ended_improvement_receipt"].casefold(): out.append(f"open-ended-improvement receipt missing exact boundary: {phrase}")
    for phrase in ["Seven reachable stages", "all 81 routes", "Inadequate for adaptive-search quality", "No support transition"]:
        if phrase.casefold() not in data["open_ended_improvement_dossier"].casefold(): out.append(f"open-ended-improvement dossier missing adequacy boundary: {phrase}")
    open_ended_chapter=next((row for row in structure_rows if row.get("id")=="open-ended-improvement-engines"),{})
    if {row.get("module") for row in open_ended_chapter.get("proof_targets",[])}!={"AsiStackProofs.OpenEndedImprovementRefinement"}:
        out.append("Open-Ended Improvement public targets do not all resolve to refinement")

    expected_self_improvement_contract={
        "self_improvement_model_path":"lean/AsiStackProofs/SelfImprovementRefinement.lean",
        "self_improvement_dossier_path":SELF_IMPROVEMENT_DOSSIER,
        "self_improvement_consumer_path":SELF_IMPROVEMENT_RECEIPT,
        "self_improvement_result_path":SELF_IMPROVEMENT_RESULT,
        "self_improvement_state":"validated_finite_authored_proposal_outcome_readmission_lifecycle_not_useful_safe_or_deployed",
        "self_improvement_valid_count":3,
        "self_improvement_invalid_count":10,
        "self_improvement_readiness_valid_count":4,
        "self_improvement_readiness_invalid_count":5,
        "self_improvement_replacement_valid_count":5,
        "self_improvement_replacement_invalid_count":9,
        "self_improvement_replacement_transaction_count":2,
        "self_improvement_replacement_negative_control_count":3,
        "self_improvement_intent_trace_count":8,
        "self_improvement_intent_invalid_control_count":6,
        "self_improvement_update_seed_count":3,
        "self_improvement_update_arm_count":12,
        "self_improvement_update_parameter_mutation_count":9,
        "self_improvement_update_exact_rollback_count":3,
        "self_improvement_update_no_change_disposition_count":4,
        "self_improvement_open_ended_governor_handoff_count":1,
        "self_improvement_open_ended_threshold_pass_count":0,
        "self_improvement_reachable_stage_count":8,
        "self_improvement_route_case_count":118,
        "self_improvement_mutation_rejection_count":129,
        "self_improvement_retained_legacy_theorem_count":22,
        "self_improvement_replacement_handoff_count":1,
        "self_improvement_outcome_reconciliation_count":1,
        "self_improvement_readmission_count":1,
        "self_improvement_support_state_effect":"none"}
    for key,value in expected_self_improvement_contract.items():
        if proof_contract.get(key)!=value: out.append(f"self-improvement contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    self_improvement=data["self_improvement_result"]
    for key,value in {"reachable_stage_count":8,"route_case_count":118,"mutation_count":129,
                      "mutation_rejection_count":129,"support_state_effect":"none"}.items():
        if self_improvement.get(key)!=value: out.append(f"self-improvement result drifted: {key}")
    inherited_self_improvement=self_improvement.get("inherited_results",{})
    for key,value in {"self_improvement_valid_count":3,"self_improvement_invalid_count":10,
                      "readiness_valid_count":4,"readiness_invalid_count":5,
                      "replacement_valid_count":5,"replacement_invalid_count":9,
                      "replacement_trace_transaction_count":2,"replacement_trace_negative_control_count":3,
                      "intent_trace_count":8,"intent_invalid_control_count":6,
                      "update_seed_count":3,"update_arm_count":12,"update_parameter_mutation_count":9,
                      "update_exact_rollback_count":3,"update_no_change_disposition_count":4,
                      "open_ended_governor_handoff_count":1,"open_ended_threshold_pass_count":0,
                      "support_state_effect":"none"}.items():
        if inherited_self_improvement.get(key)!=value: out.append(f"self-improvement inherited result drifted: {key}")
    self_improvement_witness=self_improvement.get("witness",{})
    for key,value in {"terminal_stage":"scoped","protocol_version":2,"replacement_handoff_count":1,
                      "outcome_reconciliation_count":1,"readmission_count":1,
                      "support_assignment_count":0,"external_effect_count":0}.items():
        if self_improvement_witness.get(key)!=value: out.append(f"self-improvement witness drifted: {key}")
    for phrase in ["eight-stage lifecycle", "all 118 routes", "129/129", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["self_improvement_receipt"].casefold(): out.append(f"self-improvement receipt missing exact boundary: {phrase}")
    for phrase in ["Eight reachable stages", "all 118 routes", "Inadequate for objective legitimacy", "No support transition"]:
        if phrase.casefold() not in data["self_improvement_dossier"].casefold(): out.append(f"self-improvement dossier missing adequacy boundary: {phrase}")
    self_improvement_chapter=next((row for row in structure_rows if row.get("id")=="recursive-self-improvement-boundaries"),{})
    if {row.get("module") for row in self_improvement_chapter.get("proof_targets",[])}!={"AsiStackProofs.SelfImprovementRefinement"}:
        out.append("Recursive Self-Improvement public targets do not all resolve to refinement")

    expected_readiness_contract={
        "readiness_model_path":"lean/AsiStackProofs/ReadinessRefinement.lean","readiness_dossier_path":READINESS_DOSSIER,
        "readiness_consumer_path":READINESS_RECEIPT,"readiness_result_path":READINESS_RESULT,
        "readiness_state":"validated_finite_authored_candidate_terminal_lifecycle_not_natural_calibrated_or_deployed",
        "readiness_residual_valid_count":4,"readiness_residual_invalid_count":5,
        "readiness_lifecycle_valid_count":6,"readiness_lifecycle_invalid_count":12,
        "readiness_check_valid_count":1,"readiness_check_invalid_count":9,
        "readiness_reachable_stage_count":7,"readiness_route_case_count":40,
        "readiness_mutation_rejection_count":45,"readiness_retired_baseline_declaration_count":9,
        "readiness_retained_legacy_theorem_count":11,"readiness_ordinary_release_count":1,
        "readiness_quarantine_count":1,"readiness_terminal_count":1,"readiness_support_state_effect":"none"}
    for key,value in expected_readiness_contract.items():
        if proof_contract.get(key)!=value: out.append(f"readiness contract drifted: {key} expected {value!r}, got {proof_contract.get(key)!r}")
    readiness=data["readiness_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":40,"mutation_count":45,"mutation_rejection_count":45,"support_state_effect":"none"}.items():
        if readiness.get(key)!=value: out.append(f"readiness result drifted: {key}")
    readiness_suites={row.get("suite_id"):(row.get("valid_count"),row.get("expected_invalid_count")) for row in readiness.get("input_suites",[])}
    if readiness_suites!={"readiness_residual_gates":(4,5),"readiness_lifecycle_probe":(6,12),"readiness_check_lifecycle":(1,9)}: out.append("readiness consumed-suite counts drifted")
    for phrase in ["all forty routes", "all 45 registered mutations", "one ordinary release", "Support-state effect is exactly `none`"]:
        if phrase.casefold() not in data["readiness_receipt"].casefold(): out.append(f"readiness receipt missing exact boundary: {phrase}")
    for phrase in ["Seven reachable stages", "45/45", "Inadequate for evaluator adequacy", "Support-state effect: exactly `none`"]:
        if phrase.casefold() not in data["readiness_dossier"].casefold(): out.append(f"readiness dossier missing adequacy boundary: {phrase}")
    readiness_chapter=next((row for row in structure_rows if row.get("id")=="readiness-gates-residual-escrow-and-quarantine"),{})
    if {row.get("module") for row in readiness_chapter.get("proof_targets",[])}!={"AsiStackProofs.ReadinessRefinement"}: out.append("Readiness public targets do not all resolve to refinement")

    expected_hive={"hive_model_path":"lean/AsiStackProofs/HiveLifecycleRefinement.lean","hive_dossier_path":HIVE_DOSSIER,"hive_consumer_path":HIVE_RECEIPT,"hive_result_path":HIVE_RESULT,"hive_state":"validated_finite_authored_policy_closure_lifecycle_not_distributed_useful_or_deployed","hive_admission_valid_count":2,"hive_admission_invalid_count":8,"hive_partition_valid_count":3,"hive_partition_invalid_count":6,"hive_reachable_stage_count":7,"hive_route_case_count":47,"hive_mutation_rejection_count":53,"hive_retired_baseline_declaration_count":5,"hive_retained_legacy_theorem_count":21,"hive_dispatch_count":1,"hive_useful_outcome_count":1,"hive_recovery_count":1,"hive_support_state_effect":"none"}
    for key,value in expected_hive.items():
        if proof_contract.get(key)!=value: out.append(f"hive contract drifted: {key}")
    hive=data["hive_result"]
    for key,value in {"reachable_stage_count":7,"route_case_count":47,"mutation_count":53,"mutation_rejection_count":53,"support_state_effect":"none"}.items():
        if hive.get(key)!=value: out.append(f"hive result drifted: {key}")
    if {r.get("suite_id"):(r.get("valid_count"),r.get("expected_invalid_count")) for r in hive.get("input_suites",[])}!={"hive_admission":(2,8),"partitioned_authority":(3,6)}:out.append("hive consumed-suite counts drifted")
    hive_chapter=next((row for row in structure_rows if row.get("id")=="personal-compute-hives-and-federated-edge-intelligence"),{})
    if {row.get("module") for row in hive_chapter.get("proof_targets",[])}!={"AsiStackProofs.HiveLifecycleRefinement"}:out.append("Hive public targets do not resolve to refinement")

    expected_compact_generation={
        "compact_generation_model_path":"lean/AsiStackProofs/CompactGenerationRefinement.lean",
        "compact_generation_dossier_path":COMPACT_GENERATION_DOSSIER,
        "compact_generation_consumer_path":COMPACT_GENERATION_RECEIPT,
        "compact_generation_result_path":COMPACT_GENERATION_RESULT,
        "compact_generation_state":"validated_finite_authored_source_closure_lifecycle_not_codec_useful_semantic_or_deployed",
        "compact_generation_gvr_case_count":5,"compact_generation_gvr_invalid_count":3,
        "compact_generation_residual_valid_count":3,"compact_generation_residual_invalid_count":5,
        "compact_generation_trace_entry_count":4,"compact_generation_storage_entry_count":4,
        "compact_generation_storage_invalid_count":5,"compact_generation_reachable_stage_count":9,
        "compact_generation_route_case_count":60,"compact_generation_mutation_rejection_count":51,
        "compact_generation_retired_baseline_declaration_count":26,
        "compact_generation_retained_legacy_theorem_count":6,"compact_generation_fallback_count":1,
        "compact_generation_support_state_effect":"none"}
    for key,value in expected_compact_generation.items():
        if proof_contract.get(key)!=value: out.append(f"compact-generation contract drifted: {key}")
    compact=data["compact_generation_result"]
    compact_model=compact.get("model",{})
    for key,value in {"stage_count":9,"route_count":60,"independently_reached_route_count":60,"route_case_count":60,"rejected_mutation_count":51,"fallback_route_reached":True,"support_assignment_count":0,"external_effect_count":0}.items():
        if compact_model.get(key)!=value: out.append(f"compact-generation result drifted: model.{key}")
    expected_source_counts={"gvr_case_count":5,"gvr_negative_control_count":3,"gvr_baseline_bytes":368,"gvr_selected_bytes":78,"residual_valid_count":3,"residual_invalid_count":5,"trace_entry_count":4,"storage_entry_count":4,"storage_invalid_count":5}
    if compact.get("source_result_refinement",{}).get("counts")!=expected_source_counts:out.append("compact-generation consumed result counts drifted")
    if compact.get("support_state_effect")!="none" or compact.get("external_effect")!="none":out.append("compact-generation support/effect boundary drifted")
    compact_chapter=next((row for row in structure_rows if row.get("id")=="compact-generative-systems-and-residual-honesty"),{})
    if {row.get("module") for row in compact_chapter.get("proof_targets",[])}!={"AsiStackProofs.CompactGenerationRefinement"}:out.append("Compact Generation public targets do not resolve to refinement")
    for phrase in ["nine-stage", "60 routes", "51/51", "no support-state or external effect"]:
        if phrase.casefold() not in data["compact_generation_receipt"].casefold():out.append(f"compact-generation receipt missing exact boundary: {phrase}")
    for phrase in ["Modeled boundary", "60 Lean route constructors", "Authored Boolean fields are not measurements", "No support transition"]:
        if phrase.casefold() not in data["compact_generation_dossier"].casefold():out.append(f"compact-generation dossier missing adequacy boundary: {phrase}")

    expected_fast_generation={
        "fast_generation_model_path":"lean/AsiStackProofs/FastGenerationRefinement.lean",
        "fast_generation_dossier_path":FAST_GENERATION_DOSSIER,
        "fast_generation_consumer_path":FAST_GENERATION_RECEIPT,
        "fast_generation_result_path":FAST_GENERATION_RESULT,
        "fast_generation_state":"validated_finite_authored_context_closure_lifecycle_not_model_speed_useful_or_deployed",
        "fast_generation_baseline_valid_count":2,"fast_generation_baseline_invalid_count":4,
        "fast_generation_task_route_count":3,"fast_generation_task_count":4,
        "fast_generation_theseus_valid_count":1,"fast_generation_theseus_invalid_count":6,
        "fast_generation_reachable_stage_count":8,"fast_generation_route_case_count":60,
        "fast_generation_mutation_rejection_count":51,
        "fast_generation_retired_baseline_declaration_count":35,
        "fast_generation_retained_legacy_theorem_count":3,"fast_generation_fallback_count":1,
        "fast_generation_useful_outcome_count":1,"fast_generation_support_state_effect":"none"}
    for key,value in expected_fast_generation.items():
        if proof_contract.get(key)!=value: out.append(f"fast-generation contract drifted: {key}")
    fast=data["fast_generation_result"]
    fast_model=fast.get("model",{})
    for key,value in {"stage_count":8,"route_count":60,"reached_route_count":60,"route_case_count":60,"rejected_mutation_count":51,"fallback_route_reached":True,"slow_baseline_route_reached":True,"support_assignment_count":0,"external_effect_count":0}.items():
        if fast_model.get(key)!=value: out.append(f"fast-generation result drifted: model.{key}")
    expected_fast_counts={"baseline_valid_count":2,"baseline_invalid_count":4,"task_route_count":3,"task_count":4,"baseline_tasks_passed":4,"candidate_tasks_passed":4,"proxy_tasks_passed":0,"baseline_cost_units":632,"candidate_cost_units":264,"proxy_cost_units":176,"theseus_valid_count":1,"theseus_invalid_count":6,"theseus_promotable_count":0}
    if fast.get("source_result_refinement",{}).get("counts")!=expected_fast_counts:out.append("fast-generation consumed result counts drifted")
    if fast.get("support_state_effect")!="none" or fast.get("external_effect")!="none":out.append("fast-generation support/effect boundary drifted")
    fast_chapter=next((row for row in structure_rows if row.get("id")=="fast-generation-architectures"),{})
    if {row.get("module") for row in fast_chapter.get("proof_targets",[])}!={"AsiStackProofs.FastGenerationRefinement"}:out.append("Fast Generation public targets do not resolve to refinement")
    for phrase in ["eight reachable stages", "60 routes", "51/51", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["fast_generation_receipt"].casefold():out.append(f"fast-generation receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "Authored `taskSuccess`, `usefulDenominator`, and fallback fields are not measurements", "No support transition"]:
        if phrase.casefold() not in data["fast_generation_dossier"].casefold():out.append(f"fast-generation dossier missing adequacy boundary: {phrase}")

    expected_deliberation={
        "deliberation_model_path":"lean/AsiStackProofs/DeliberationRefinement.lean",
        "deliberation_dossier_path":DELIBERATION_DOSSIER,
        "deliberation_consumer_path":DELIBERATION_RECEIPT,
        "deliberation_result_path":DELIBERATION_RESULT,
        "deliberation_state":"validated_finite_authored_request_closure_lifecycle_not_real_model_useful_faithful_or_deployed",
        "deliberation_admission_case_count":10,"deliberation_admission_mutation_count":11,
        "deliberation_preserved_harm_count":15,"deliberation_synthetic_seed_count":3,
        "deliberation_synthetic_routing_record_count":900,"deliberation_synthetic_deliberation_record_count":540,
        "deliberation_synthetic_interference_record_count":180,"deliberation_synthetic_fallback_activation_count":0,
        "deliberation_real_model_test_count":60,"deliberation_real_model_correct_count":0,
        "deliberation_real_model_disposition":"no_change","deliberation_reachable_stage_count":8,
        "deliberation_route_case_count":59,"deliberation_mutation_rejection_count":51,
        "deliberation_retired_baseline_declaration_count":8,"deliberation_retained_legacy_theorem_count":2,
        "deliberation_residual_escrow_count":1,"deliberation_planning_handoff_count":1,
        "deliberation_support_state_effect":"none"}
    for key,value in expected_deliberation.items():
        if proof_contract.get(key)!=value:out.append(f"deliberation contract drifted: {key}")
    deliberation=data["deliberation_result"]
    deliberation_model=deliberation.get("model",{})
    for key,value in {"stage_count":8,"route_count":59,"reached_route_count":59,"route_case_count":59,"rejected_mutation_count":51,"residual_escrow_route_reached":True,"planning_handoff_route_reached":True,"support_assignment_count":0,"external_effect_count":0}.items():
        if deliberation_model.get(key)!=value:out.append(f"deliberation result drifted: model.{key}")
    expected_deliberation_counts={"admission_case_count":10,"admission_review_count":8,"admission_escrow_count":1,"admission_harm_count":15,"seed_count":3,"routing_record_count":900,"deliberation_record_count":540,"interference_record_count":180,"fixed_extra_compute_harm_count":15,"fallback_activation_count":0,"disposition_count":2,"real_model_request_count":60,"real_model_call_count":240,"real_model_candidate_evaluation_count":360,"real_model_arm_count":5,"real_model_final_correct_count":0,"real_model_initial_correct_count":0,"real_model_candidate_operation_count":1140,"real_model_known_harm_regression_count":15,"real_model_deliberation_disposition":"no_change","real_model_support_state_effect":"no_core_promotion"}
    if deliberation.get("source_result_refinement",{}).get("counts")!=expected_deliberation_counts:out.append("deliberation consumed result counts drifted")
    if deliberation.get("support_state_effect")!="none" or deliberation.get("external_effect")!="none":out.append("deliberation support/effect boundary drifted")
    deliberation_chapter=next((row for row in structure_rows if row.get("id")=="governed-deliberation-and-test-time-scaling"),{})
    if {row.get("module") for row in deliberation_chapter.get("proof_targets",[])}!={"AsiStackProofs.DeliberationRefinement"}:out.append("Governed Deliberation public targets do not resolve to refinement")
    for phrase in ["eight reachable stages", "59 routes", "51/51", "actual-model five-arm 0/60", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["deliberation_receipt"].casefold():out.append(f"deliberation receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "failed actual-model attempt", "corruption was non-estimable", "No support transition"]:
        if phrase.casefold() not in data["deliberation_dossier"].casefold():out.append(f"deliberation dossier missing adequacy boundary: {phrase}")

    expected_artifact_compression={"artifact_compression_model_path":"lean/AsiStackProofs/ArtifactCompressionRefinement.lean","artifact_compression_dossier_path":ARTIFACT_COMPRESSION_DOSSIER,"artifact_compression_consumer_path":ARTIFACT_COMPRESSION_RECEIPT,"artifact_compression_result_path":ARTIFACT_COMPRESSION_RESULT,"artifact_compression_state":"validated_finite_authored_artifact_consumption_lifecycle_not_codec_useful_or_deployed","artifact_compression_fixture_field_count":22,"artifact_compression_probe_input_bytes":3936,"artifact_compression_probe_archive_bytes":4434,"artifact_compression_probe_corrupt_rejection_count":1,"artifact_compression_import_observation_count":3,"artifact_compression_no_change_decision_count":2,"artifact_compression_reachable_stage_count":8,"artifact_compression_route_case_count":53,"artifact_compression_mutation_rejection_count":44,"artifact_compression_retired_baseline_declaration_count":17,"artifact_compression_retained_legacy_theorem_count":2,"artifact_compression_fallback_count":1,"artifact_compression_support_state_effect":"none"}
    for key,value in expected_artifact_compression.items():
        if proof_contract.get(key)!=value:out.append(f"artifact-compression contract drifted: {key}")
    artifact_compression=data["artifact_compression_result"];artifact_compression_model=artifact_compression.get("model",{})
    for key,value in {"stage_count":8,"route_count":53,"reached_route_count":53,"route_case_count":53,"rejected_mutation_count":44,"fallback_route_reached":True,"exact_use_route_reached":True,"support_assignment_count":0,"external_effect_count":0}.items():
        if artifact_compression_model.get(key)!=value:out.append(f"artifact-compression result drifted: model.{key}")
    expected_artifact_compression_counts={"fixture_field_count":22,"fixture_non_claim_count":3,"probe_input_bytes":3936,"probe_archive_bytes":4434,"probe_command_count":5,"probe_corrupt_rejection_count":1,"probe_roundtrip_exact_count":1,"probe_compression_advantage_count":0,"import_observation_count":3,"import_decoded_bytes":100000000,"import_best_ratio":2.76634019,"no_change_decision_count":2}
    if artifact_compression.get("source_result_refinement",{}).get("counts")!=expected_artifact_compression_counts:out.append("artifact-compression consumed result counts drifted")
    if artifact_compression.get("support_state_effect")!="none" or artifact_compression.get("external_effect")!="none":out.append("artifact-compression support/effect boundary drifted")
    artifact_compression_chapter=next((row for row in structure_rows if row.get("id")=="rankfold-neuralfold-and-artifact-compression"),{})
    if {row.get("module") for row in artifact_compression_chapter.get("proof_targets",[])}!={"AsiStackProofs.ArtifactCompressionRefinement"}:out.append("Artifact Compression public targets do not resolve to refinement")
    for phrase in ["eight reachable stages", "53 routes", "44/44", "22-field", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["artifact_compression_receipt"].casefold():out.append(f"artifact-compression receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "RAW0 replay was larger", "Authored decoder, probe, utility", "No support transition"]:
        if phrase.casefold() not in data["artifact_compression_dossier"].casefold():out.append(f"artifact-compression dossier missing adequacy boundary: {phrase}")

    expected_resource_economics = {
        "resource_economics_model_path": "lean/AsiStackProofs/ResourceEconomicsRefinement.lean",
        "resource_economics_dossier_path": RESOURCE_ECONOMICS_DOSSIER,
        "resource_economics_consumer_path": RESOURCE_ECONOMICS_RECEIPT,
        "resource_economics_result_path": RESOURCE_ECONOMICS_RESULT,
        "resource_economics_state": "validated_finite_authored_allocation_and_simulation_transport_lifecycle_not_economic_or_deployed",
        "resource_economics_source_family_count": 12,
        "resource_economics_budget_valid_count": 6,
        "resource_economics_budget_invalid_count": 7,
        "resource_economics_workflow_step_count": 3,
        "resource_economics_flagship_command_count": 10,
        "resource_economics_flagship_artifact_count": 26,
        "resource_economics_ci_run_count": 8,
        "resource_economics_ci_failure_count": 3,
        "resource_economics_governance_valid_count": 3,
        "resource_economics_governance_invalid_count": 5,
        "resource_economics_simulation_valid_count": 3,
        "resource_economics_simulation_invalid_count": 6,
        "resource_economics_theseus_sim_invalid_count": 7,
        "resource_economics_theseus_export_invalid_count": 7,
        "resource_economics_reachable_stage_count": 9,
        "resource_economics_route_case_count": 66,
        "resource_economics_mutation_rejection_count": 57,
        "resource_economics_retired_baseline_declaration_count": 35,
        "resource_economics_retained_legacy_theorem_count": 23,
        "resource_economics_support_state_effect": "none",
    }
    for key, value in expected_resource_economics.items():
        if proof_contract.get(key) != value:
            out.append(f"resource-economics contract drifted: {key}")
    resource_economics = data["resource_economics_result"]
    resource_model = resource_economics.get("model", {})
    for key, value in {"stage_count": 9, "route_count": 66, "reached_route_count": 66, "route_case_count": 66, "rejected_mutation_count": 57, "simulation_transfer_route_reached": True, "closed_route_reached": True, "support_assignment_count": 0, "external_effect_count": 0}.items():
        if resource_model.get(key) != value:
            out.append(f"resource-economics result drifted: model.{key}")
    expected_resource_counts = {"budget_valid_count":6,"budget_invalid_count":7,"costed_eligible_count":2,"costed_rejected_count":2,"workflow_valid_count":1,"workflow_invalid_count":5,"workflow_step_count":3,"capacity_valid_count":3,"capacity_invalid_count":6,"flagship_command_count":10,"flagship_artifact_count":26,"ci_run_count":8,"ci_failure_count":3,"governance_valid_count":3,"governance_invalid_count":5,"governed_selection_count":2,"low_risk_shortcut_count":1,"simulation_valid_count":3,"simulation_invalid_count":6,"theseus_sim_scenario_count":5,"theseus_sim_receipt_count":6,"theseus_sim_invalid_count":7,"theseus_export_ready_count":1,"theseus_export_format_count":3,"theseus_export_field_count":7,"theseus_export_invalid_count":7,"workload_probe_pass_count":1,"load_probe_pass_count":1}
    if resource_economics.get("source_result_refinement", {}).get("counts") != expected_resource_counts:
        out.append("resource-economics consumed result counts drifted")
    if resource_economics.get("support_state_effect") != "none" or resource_economics.get("external_effect") != "none":
        out.append("resource-economics support/effect boundary drifted")
    resource_chapter = next((row for row in structure_rows if row.get("id") == "resource-economics-and-token-budgets"), {})
    if {row.get("module") for row in resource_chapter.get("proof_targets", [])} != {"AsiStackProofs.ResourceEconomicsRefinement"}:
        out.append("Resource Economics public targets do not resolve to refinement")
    for phrase in ["nine reachable stages", "66 routes", "57/57", "twelve exact bounded", "Support-state and external-effect authority remain exactly `none`"]:
        if phrase.casefold() not in data["resource_economics_receipt"].casefold():
            out.append(f"resource-economics receipt missing exact boundary: {phrase}")
    for phrase in ["Reachable model", "twelve bounded result families", "Authored cost, capacity, verifier", "No support transition"]:
        if phrase.casefold() not in data["resource_economics_dossier"].casefold():
            out.append(f"resource-economics dossier missing adequacy boundary: {phrase}")

    article = status.get("x_article_contract", {})
    expected_article = {
        "contract_path": X_ARTICLE_CONTRACT,
        "canonical_live_book_url": "https://corbensorenson.github.io/asi-stack-book/",
        "maximum_visible_word_count": 9999,
        "header_width_pixels": 2000,
        "header_height_pixels": 800,
        "header_aspect_ratio": "5:2",
        "external_publication_authorized": False,
        "ready_not_published_is_terminal": True,
    }
    for key, value in expected_article.items():
        if article.get(key) != value:
            out.append(f"X Article contract drifted: {key} expected {value!r}, got {article.get(key)!r}")
    x_contract_normalized = " ".join(data["x_article_contract"].split())
    for phrase in [
        "first visible body line",
        "9,999 words",
        "2000×800 pixels",
        "exact aspect ratio: 5:2",
        "ready_not_published",
        "explicit authorization",
        "https://help.x.com/en/using-x/articles",
    ]:
        if phrase.casefold() not in x_contract_normalized.casefold():
            out.append(f"X Article contract missing governing requirement: {phrase}")

    roadmap = data["roadmap"]
    roadmap_normalized = " ".join(roadmap.split())
    for section in REQUIRED_SECTIONS:
        if roadmap.count(section) != 1:
            out.append(f"roadmap must contain exactly one section: {section}")
    for phrase in REQUIRED_BOUNDARIES:
        if phrase not in roadmap_normalized and phrase not in " ".join(status.get("non_claims", [])):
            out.append(f"roadmap/status missing governing boundary: {phrase}")
    for family_id in family_ids:
        if roadmap.count(family_id) < 1:
            out.append(f"roadmap does not define {family_id}")

    for path, body in data["public"].items():
        body_normalized = " ".join(body.split())
        for phrase in [ROADMAP, STATUS, PREDECESSOR, PREDECESSOR_STATUS, "v2.3.0", "all 54 chapter-core claims remain at `argument`", "active canonical successor roadmap"]:
            if phrase.casefold() not in body_normalized.casefold():
                out.append(f"{path} missing active roadmap truth: {phrase}")
        if "No successor roadmap is active" in body:
            out.append(f"{path} retains obsolete no-successor language")
    for name, body in [("living workflow", data["workflow"]), ("master prompt", data["master"])]:
        for phrase in ["same transaction", "active successor"]:
            if phrase.casefold() not in body.casefold():
                out.append(f"{name} missing roadmap continuity rule: {phrase}")
        for phrase in [X_ARTICLE_CONTRACT, "9,999", "explicit authorization"]:
            if phrase.casefold() not in body.casefold():
                out.append(f"{name} missing maintained X Article rule: {phrase}")
    for phrase in [ROADMAP, STATUS, X_ARTICLE_CONTRACT, "proof", "54", "1,151", "promotion-or-refutation"]:
        if phrase not in data["outline"]:
            out.append(f"book outline missing active proof-roadmap authority: {phrase}")
    if ROADMAP not in data["changelog"] or STATUS not in data["changelog"] or X_ARTICLE_CONTRACT not in data["changelog"]:
        out.append("changelog missing roadmap activation record")
    return out


def main() -> None:
    base = snapshot()
    failures = errors(base)
    mutations: list[tuple[str, dict]] = []

    duplicate = copy.deepcopy(base)
    duplicate["active_roadmaps"] = [ROADMAP, "docs/fake_roadmap.md"]
    mutations.append(("duplicate active roadmap", duplicate))

    missing_claim = copy.deepcopy(base)
    missing_claim["status"]["chapter_claim_program"] = missing_claim["status"]["chapter_claim_program"][:-1]
    mutations.append(("missing chapter claim", missing_claim))

    stale_proof = copy.deepcopy(base)
    stale_proof["status"]["activation_baseline"]["theorem_declaration_count"] += 1
    mutations.append(("stale theorem baseline", stale_proof))

    support = copy.deepcopy(base)
    support["vectors"]["vectors"][0]["summary_support_state"] = "prototype-backed"
    mutations.append(("support promotion", support))

    broken_frontier = copy.deepcopy(base)
    broken_frontier["status"]["priorities"][3]["state"] = "in_progress"
    mutations.append(("multiple active priorities", broken_frontier))

    human_gate = copy.deepcopy(base)
    human_gate["status"]["external_human_prepublication_required"] = True
    mutations.append(("external-human gate", human_gate))

    no_continuity = copy.deepcopy(base)
    no_continuity["status"]["closure_requires_active_successor"] = False
    mutations.append(("successor continuity removal", no_continuity))

    stale_public = copy.deepcopy(base)
    stale_public["public"]["README.md"] = stale_public["public"]["README.md"].replace(ROADMAP, PREDECESSOR)
    mutations.append(("stale public pointer", stale_public))

    reader_laundering = copy.deepcopy(base)
    reader_laundering["reader_epub"]["decision"] = "approved_exact_local_artifact"
    mutations.append(("reader blocker laundering", reader_laundering))

    release = copy.deepcopy(base)
    release["status"]["release_effect"] = "public_release"
    mutations.append(("activation release laundering", release))

    orphan_proof = copy.deepcopy(base)
    orphan_proof["status"]["proof_rationalization_contract"]["orphan_retained_theorem_allowed"] = True
    mutations.append(("orphan proof allowance", orphan_proof))

    projection_proof = copy.deepcopy(base)
    projection_proof["status"]["proof_rationalization_contract"]["projection_or_assumption_restatement_counts_as_semantic_proof"] = True
    mutations.append(("projection proof laundering", projection_proof))

    safety_support = copy.deepcopy(base)
    safety_support["safety_consumer_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("shared safety consumer support laundering", safety_support))

    abi_support = copy.deepcopy(base)
    abi_support["abi_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Cognitive Kernel ABI support laundering", abi_support))

    integrated_support = copy.deepcopy(base)
    integrated_support["integrated_trace_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("integrated trace support laundering", integrated_support))

    refinement_support = copy.deepcopy(base)
    refinement_support["integrated_refinement_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("integrated runtime refinement support laundering", refinement_support))

    concurrent_support = copy.deepcopy(base)
    concurrent_support["concurrent_effect_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("concurrent effect support laundering", concurrent_support))

    stack_boundary_support = copy.deepcopy(base)
    stack_boundary_support["stack_boundary_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("stack-boundary support laundering", stack_boundary_support))

    intent_execution_support = copy.deepcopy(base)
    intent_execution_support["intent_execution_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("intent-execution support laundering", intent_execution_support))

    authority_effect_support = copy.deepcopy(base)
    authority_effect_support["authority_effect_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("authority-effect support laundering", authority_effect_support))

    intent_resolution_support = copy.deepcopy(base)
    intent_resolution_support["intent_resolution_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("intent-resolution support laundering", intent_resolution_support))

    command_semantic_support = copy.deepcopy(base)
    command_semantic_support["command_semantic_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("command-semantic support laundering", command_semantic_support))

    cognitive_compilation_support = copy.deepcopy(base)
    cognitive_compilation_support["cognitive_compilation_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("cognitive-compilation support laundering", cognitive_compilation_support))

    virtual_context_support = copy.deepcopy(base)
    virtual_context_support["virtual_context_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("virtual-context support laundering", virtual_context_support))

    context_certificate_support = copy.deepcopy(base)
    context_certificate_support["context_certificate_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("context-certificate support laundering", context_certificate_support))

    context_transaction_support = copy.deepcopy(base)
    context_transaction_support["context_transaction_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("context-transaction support laundering", context_transaction_support))

    verification_bandwidth_support = copy.deepcopy(base)
    verification_bandwidth_support["verification_bandwidth_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("verification-bandwidth support laundering", verification_bandwidth_support))

    claim_ledger_support = copy.deepcopy(base)
    claim_ledger_support["claim_ledger_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("claim-ledger support laundering", claim_ledger_support))

    proof_carrying_claims_support = copy.deepcopy(base)
    proof_carrying_claims_support["proof_carrying_claims_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("proof-carrying-claims support laundering", proof_carrying_claims_support))

    tribunal_support = copy.deepcopy(base)
    tribunal_support["tribunal_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Tribunal support laundering", tribunal_support))

    typed_job_support = copy.deepcopy(base)
    typed_job_support["typed_job_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("typed-job support laundering", typed_job_support))

    artifact_reality_support = copy.deepcopy(base)
    artifact_reality_support["artifact_reality_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("artifact-reality support laundering", artifact_reality_support))

    procedural_memory_support = copy.deepcopy(base)
    procedural_memory_support["procedural_memory_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("procedural-memory support laundering", procedural_memory_support))

    routing_support = copy.deepcopy(base)
    routing_support["routing_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("routing support laundering", routing_support))

    safety_case_support = copy.deepcopy(base)
    safety_case_support["safety_case_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("safety-case support laundering", safety_case_support))

    capability_threshold_support = copy.deepcopy(base)
    capability_threshold_support["capability_threshold_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("capability-threshold support laundering", capability_threshold_support))

    adversarial_evaluation_support = copy.deepcopy(base)
    adversarial_evaluation_support["adversarial_evaluation_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("adversarial-evaluation support laundering", adversarial_evaluation_support))

    scalable_oversight_support = copy.deepcopy(base)
    scalable_oversight_support["scalable_oversight_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("scalable-oversight support laundering", scalable_oversight_support))

    policy_optimization_support = copy.deepcopy(base)
    policy_optimization_support["policy_optimization_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("policy-optimization support laundering", policy_optimization_support))

    data_engine_lifecycle_support = copy.deepcopy(base)
    data_engine_lifecycle_support["data_engine_lifecycle_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("data-engine lifecycle support laundering", data_engine_lifecycle_support))

    open_ended_improvement_support = copy.deepcopy(base)
    open_ended_improvement_support["open_ended_improvement_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Open-Ended Improvement support laundering", open_ended_improvement_support))

    self_improvement_support = copy.deepcopy(base)
    self_improvement_support["self_improvement_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Recursive Self-Improvement support laundering", self_improvement_support))

    readiness_support = copy.deepcopy(base)
    readiness_support["readiness_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("readiness support laundering", readiness_support))

    hive_support = copy.deepcopy(base)
    hive_support["hive_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Hive support laundering", hive_support))

    compact_generation_support = copy.deepcopy(base)
    compact_generation_support["compact_generation_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Compact Generation support laundering", compact_generation_support))

    fast_generation_support = copy.deepcopy(base)
    fast_generation_support["fast_generation_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Fast Generation support laundering", fast_generation_support))

    deliberation_support = copy.deepcopy(base)
    deliberation_support["deliberation_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Governed Deliberation support laundering", deliberation_support))

    artifact_compression_support = copy.deepcopy(base)
    artifact_compression_support["artifact_compression_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Artifact Compression support laundering", artifact_compression_support))

    resource_economics_support = copy.deepcopy(base)
    resource_economics_support["resource_economics_result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("Resource Economics support laundering", resource_economics_support))

    wip_scope = copy.deepcopy(base)
    wip_scope["status"]["latest_review_remediation_contract"]["scope_expansion_blocked_above_limit"] = False
    mutations.append(("Oversized WIP scope-expansion laundering", wip_scope))

    campaign_batch = copy.deepcopy(base)
    campaign_batch["status"]["latest_review_remediation_contract"]["first_campaign_minimum_terminal_atom_count"] = 0
    mutations.append(("First campaign batch erasure", campaign_batch))

    sota_entry = copy.deepcopy(base)
    sota_entry["status"]["latest_review_remediation_contract"]["p6_dated_comparator_ledger_required_before_run"] = False
    mutations.append(("SOTA prerequisite erasure", sota_entry))

    instrument_attempt = copy.deepcopy(base)
    instrument_attempt["status"]["instrument_adequacy_and_disposition_contract"]["instrument_failure_counts_as_claim_attempt"] = True
    mutations.append(("Instrument failure laundered into claim attempt", instrument_attempt))

    instrument_floor = copy.deepcopy(base)
    instrument_floor["status"]["instrument_adequacy_and_disposition_contract"]["minimum_schema_admissible_rate"] = 0.0
    mutations.append(("Instrument adequacy floor erased", instrument_floor))

    syntax_laundering = copy.deepcopy(base)
    syntax_laundering["status"]["instrument_adequacy_and_disposition_contract"]["syntax_validity_counts_as_semantic_correctness"] = True
    mutations.append(("Syntax laundered into semantic correctness", syntax_laundering))

    theorem_count_laundering = copy.deepcopy(base)
    theorem_count_laundering["status"]["instrument_adequacy_and_disposition_contract"]["top_level_theorem_count_counts_as_semantic_adequacy"] = True
    mutations.append(("Theorem count laundered into semantic adequacy", theorem_count_laundering))

    refinement_gate_reopened = copy.deepcopy(base)
    refinement_gate_reopened["status"]["instrument_adequacy_and_disposition_contract"]["review_named_refinement_module_gate_state"] = "in_progress"
    mutations.append(("Review-named refinement-module gate reopened without roadmap reconciliation", refinement_gate_reopened))

    review_publish = copy.deepcopy(base)
    review_publish["status"]["instrument_adequacy_and_disposition_contract"]["external_publication_authorized"] = True
    mutations.append(("Review recommendation laundered into publication authority", review_publish))

    article_length = copy.deepcopy(base)
    article_length["status"]["x_article_contract"]["maximum_visible_word_count"] = 10000
    mutations.append(("X Article word-limit drift", article_length))

    article_ratio = copy.deepcopy(base)
    article_ratio["status"]["x_article_contract"]["header_aspect_ratio"] = "16:9"
    mutations.append(("X Article header-ratio drift", article_ratio))

    article_publish = copy.deepcopy(base)
    article_publish["status"]["x_article_contract"]["external_publication_authorized"] = True
    mutations.append(("X Article publication invention", article_publish))

    missing_contract = copy.deepcopy(base)
    missing_contract["x_article_contract"] = missing_contract["x_article_contract"].replace("9,999 words", "ten thousand words")
    mutations.append(("X Article contract weakening", missing_contract))

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Claim-proof/SOTA roadmap validation failed:\n - " + "\n - ".join(failures))
    print(
        f"Claim-proof/SOTA roadmap passed: sole active successor at {base['status']['current_priority']}, monotone priority frontier, "
        "55 live chapter-core programs across CF-01..CF-08 with a frozen 54-chapter activation baseline, exact proof/evidence/reader baseline, "
        "proof rationalization and argument-exit contracts, maintained X Article and exact 5:2 header contract, "
        "no support or release effect, no external-human gate, same-transaction successor continuity, "
        "validated shared-safety, Cognitive Kernel ABI, integrated reference trace, concrete-schema refinement, concurrent effect, reachable stack-boundary, Intent-to-Execution vertical, Authority grant-to-effect, Human Intent resolution, Command semantic-interface, Cognitive Compilation obligation-refinement, Virtual Context binding/materialization/fault, Context Certificate provenance/lifecycle, Context Transaction snapshot/store, Verification Bandwidth evidence-gate, Claim Ledger append-only, Proof-Carrying Claims target-to-writeback, Tribunal versioned-verdict/appeal, Typed Job versioned execution/closure, Artifact record-reality/trust, Procedural Memory promotion/retirement, Routing/MoECOT request-to-closure, Safety Case readiness/invalidation, Capability Threshold repeated assessment, Adversarial Evaluation observation/re-evaluation, Scalable Oversight review/readmission, Policy Optimization governed-update/readmission, Data Engines custody/update/deletion/readmission, Open-Ended Improvement campaign-to-governor/readmission, Recursive Self-Improvement proposal-to-outcome/readmission, Readiness candidate-to-terminal, Hive policy-to-closure, Compact Generation source-to-closure, Fast Generation request-to-closure, Governed Deliberation request-to-closure, Artifact Compression artifact-to-consumption, and Resource Economics allocation-and-simulation-transport receipts, bounded WIP and first-campaign/SOTA entry gates, and "
        f"{len(mutations)} rejecting mutations."
    )


if __name__ == "__main__":
    main()
