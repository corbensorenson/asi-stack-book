#!/usr/bin/env python3
"""Generate and validate the v1.0 test-harness status ledger.

The v1.0 candidate status page should stay readable. This ledger carries the
long harness inventory that used to live inside one status-table cell.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
LEDGER = ROOT / "docs" / "test_harness_status_ledger.md"
REGISTRY = ROOT / "experiments" / "phase5_harness_registry.json"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"


BOOK_GATE_CHECKS = [
    {
        "name": "Stack layer traceability audit",
        "doc": "docs/stack_layer_traceability_audit.md",
        "script": "scripts/validate_stack_layer_traceability.py",
        "summary": "Layer-boundary fixture, source-to-layer visibility, Appendix C labels, and no-promotion markers.",
        "boundary": "Repository traceability audit only; no runtime stack-separation claim.",
    },
    {
        "name": "Artifact graph replay harness",
        "doc": "docs/artifact_graph_replay_harness.md",
        "script": "scripts/validate_artifact_graph_replay.py",
        "summary": "Synthetic replay metadata completeness and negative replay cases.",
        "boundary": "No deployed replay-engine or open-world receipt-faithfulness claim.",
    },
    {
        "name": "Artifact graph record-reality sequence bridge",
        "doc": "docs/artifact_graph_record_reality_sequence.md",
        "script": "scripts/validate_artifact_graph_record_reality_sequence.py",
        "summary": "One valid stale/partial/fresh replay sequence and four expected-invalid controls.",
        "boundary": "No evidence transition, verifier-correctness claim, or support-state promotion.",
    },
    {
        "name": "Artifact live attestation probe",
        "doc": "docs/artifact_live_attestation_probe.md",
        "script": "scripts/validate_artifact_live_attestation_probe.py",
        "summary": "One current produced artifact checked by filesystem bytes, git object bytes, command replay, trap receipt, and seven controls.",
        "boundary": "No deployed attestation, open-world receipt-faithfulness, verifier-correctness, or support-state claim.",
    },
    {
        "name": "Artifact randomized attestation audit",
        "doc": "docs/artifact_randomized_attestation_audit.md",
        "script": "scripts/validate_artifact_randomized_attestation_audit.py",
        "command": "python3 scripts/validate_artifact_randomized_attestation_audit.py",
        "summary": "Deterministic pseudo-random sample of four public-safe repository artifacts checked through filesystem bytes, git object bytes, command replay, trap receipts, and eight controls.",
        "boundary": "No deployed attestation, external review, open-world receipt-faithfulness, verifier-correctness, or support-state claim.",
    },
    {
        "name": "Artifact public deployed-site attestation",
        "doc": "docs/artifact_public_site_attestation.md",
        "script": "scripts/validate_artifact_public_site_attestation.py",
        "summary": "Public GitHub Pages Artifact Graphs chapter fetched and checked for record-reality, epistemic-TCB, attestation, and boundary fragments.",
        "boundary": "Served-page evidence only; no deployed attestation, external review, reader release, or support-state claim.",
    },
    {
        "name": "Procedural memory loop harness",
        "doc": "docs/procedural_memory_loop_harness.md",
        "script": "scripts/validate_procedural_memory_loop.py",
        "summary": "Procedural-memory valid and expected-invalid loop records.",
        "boundary": "No deployed loop detector, tool synthesis, or regression-quality claim.",
    },
    {
        "name": "Routing decision lease harness",
        "doc": "docs/routing_decision_lease_harness.md",
        "script": "scripts/validate_routing_decision_lease.py",
        "summary": "Lease-bounded route packets, fallback/residual ownership, and authority-envelope checks.",
        "boundary": "No learned-router, route-quality, MoECOT replay, or deployed authority-enforcement claim.",
    },
    {
        "name": "Cyclic memory contract harness",
        "doc": "docs/cyclic_memory_contract_harness.md",
        "script": "scripts/validate_cyclic_memory_contracts.py",
        "summary": "Cyclic-memory contract fixtures and expected-invalid controls.",
        "boundary": "No deployed memory system, retrieval-quality, or support-state claim.",
    },
    {
        "name": "Benchmark anti-Goodhart fixture bridge",
        "doc": "docs/benchmark_antigoodhart_harness.md",
        "script": "scripts/validate_benchmark_fixture_bridge.py",
        "summary": "Two valid fixture paths and five expected-invalid anti-Goodhart controls.",
        "boundary": "Finite fixture bridge only; no benchmark-quality or support-state promotion.",
    },
    {
        "name": "Circle cyclic-memory receipt slice",
        "doc": "docs/circle_cyclic_memory_receipt_slice.md",
        "script": "scripts/validate_circle_cyclic_memory_receipt_slice.py",
        "summary": "Public-safe Circle cyclic-memory receipt slice for `CC-AI-CONTRACT-MEMORY-001`.",
        "boundary": "No retrieval-quality, model-quality, memory-scaling, deployment-safety, or ASI claim.",
    },
    {
        "name": "Circle KV-cache receipt slice",
        "doc": "docs/circle_kv_cache_receipt_slice.md",
        "script": "scripts/validate_circle_kv_cache_receipt_slice.py",
        "summary": "Public-safe Circle KV-cache ring-buffer receipt slice for `CC-AI-CONTRACT-KV-001`.",
        "boundary": "No deployed KV-cache behavior, serving-throughput, memory-savings, paging, retrieval-quality, model-quality, deployment-safety, or ASI claim.",
    },
    {
        "name": "Circle recurrence receipt slice",
        "doc": "docs/circle_recurrence_receipt_slice.md",
        "script": "scripts/validate_circle_recurrence_receipt_slice.py",
        "summary": "Public-safe Circle recurrence-schedule receipt slice for `CC-AI-CONTRACT-RECURRENCE-001`.",
        "boundary": "No deployed recurrence behavior, reasoning-quality, retrieval-quality, learned-memory, convergence, model-quality, deployment-safety, or ASI claim.",
    },
    {
        "name": "Circle sparse-attention receipt slice",
        "doc": "docs/circle_sparse_attention_receipt_slice.md",
        "script": "scripts/validate_circle_sparse_attention_receipt_slice.py",
        "summary": "Public-safe Circle sparse-attention gap and repair/fallback receipt slice for `CC-AI-CONTRACT-SPARSE-001`.",
        "boundary": "No sparse-attention coverage success, deployed sparse-attention behavior, retrieval-quality, long-context, model-quality, speed, deployment-safety, or ASI claim.",
    },
    {
        "name": "Circle contract-pack archive",
        "doc": "docs/circle_contract_pack_archive.md",
        "script": "scripts/validate_circle_contract_pack_archive.py",
        "summary": "Public-safe Circle contract-pack archive with 9 archived contracts, 4 acceptance-policy receipts, pinned pack/report digests, and five expected-invalid controls.",
        "boundary": "No local Circle Lean replay, deployed proof-contract transport, model-quality, context-length, runtime-speed, memory-scaling, deployment-safety, transfer, safety, ASI, or support-state claim.",
    },
    {
        "name": "Context transaction memory-store harness",
        "doc": "docs/context_transaction_memory_store_harness.md",
        "script": "scripts/validate_context_transaction_memory_store.py",
        "summary": "Context-transaction memory-store fixtures and negative controls.",
        "boundary": "No deployed memory store, isolation, deletion-enforcement, or support-state claim.",
    },
    {
        "name": "VCM resolver/certificate probe",
        "doc": "docs/vcm_resolver_certificate_probe.md",
        "script": "scripts/validate_vcm_resolver_certificate_probe.py",
        "summary": "Checks `valid_resolver_materialization_receipt`, `valid_mandatory_miss_typed_fault`, `invalid_address_mismatch_materialization_denied`, `invalid_version_mismatch_materialization_denied`, `invalid_snapshot_mismatch_materialization_denied`, `invalid_mount_policy_denied`, `invalid_lease_expired_reuse_blocked`, `invalid_certificate_source_binding_mismatch_denied`, `invalid_certificate_authority_escalation_denied`, `invalid_certificate_truthfulness_overclaim_denied`, and `invalid_summary_fidelity_omission_denied`.",
        "boundary": "no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim",
    },
    {
        "name": "Simulation transfer boundary harness",
        "doc": "docs/simulation_transfer_boundary_harness.md",
        "script": "scripts/validate_simulation_transfer_boundaries.py",
        "summary": "Simulation-transfer valid and expected-invalid boundary fixtures.",
        "boundary": "No simulator adequacy, real-world transfer, or deployment claim.",
    },
    {
        "name": "Resource workflow trace harness",
        "doc": "docs/resource_workflow_trace.md",
        "script": "scripts/validate_resource_workflow_trace.py",
        "summary": "Three-step local Resource Economics workflow trace and negative controls.",
        "boundary": "No production scheduler, physical-feasibility, or economic claim.",
    },
    {
        "name": "Resource live probe",
        "doc": "docs/resource_live_probe.md",
        "script": "scripts/validate_resource_live_probe.py",
        "summary": "Five local Resource Economics validator replays with command-output digests.",
        "boundary": "Local replay accountability only; no stable-speedup or live workload claim.",
    },
    {
        "name": "Resource workload-quality probe",
        "doc": "docs/resource_workload_quality_probe.md",
        "script": "scripts/validate_resource_workload_quality_probe.py",
        "summary": "Three local route candidates across five measured samples each.",
        "boundary": "No broad workload-quality or model-quality claim.",
    },
    {
        "name": "Resource load-stability probe",
        "doc": "docs/resource_load_stability_probe.md",
        "script": "scripts/validate_resource_load_stability_probe.py",
        "summary": "Ten-task local synthetic burst-review workload and protected-capacity smoothing selector.",
        "boundary": "No live/external load-stability or production scheduler claim.",
    },
    {
        "name": "Theseus support replay probe",
        "doc": "docs/theseus_support_replay_probe.md",
        "script": "scripts/validate_theseus_support_replay_probe.py",
        "summary": "Local replay wrapper for imported Theseus architecture and generation-mode validators.",
        "boundary": "No clean live Theseus replay, model-quality, or support-state transition claim.",
    },
    {
        "name": "Theseus report-bundle audit",
        "doc": "docs/theseus_report_bundle_audit.md",
        "script": "scripts/validate_theseus_report_bundle_audit.py",
        "summary": "Public-safe bundle-shaped Theseus fixture with seven expected-invalid controls.",
        "boundary": "No clean live Theseus replay or support-state transition claim.",
    },
    {
        "name": "Theseus public task-bundle import",
        "doc": "docs/theseus_public_task_bundle_import.md",
        "script": "scripts/validate_theseus_public_task_bundle_import.py",
        "summary": "Sixty-four public BigCodeBench metadata-only tasks, benchmark gates, residuals, and seven controls.",
        "boundary": "No clean live replay, model-quality, speed, useful-solution-per-second, or support-state claim.",
    },
    {
        "name": "Theseus artifact-retention replay import",
        "doc": "docs/theseus_artifact_retention_replay_import.md",
        "script": "scripts/validate_theseus_artifact_retention_replay_import.py",
        "summary": "Sanitized exact-hash artifact-retention replay import with record counts, redaction checks, and seven controls.",
        "boundary": "No clean live replay, deployed residual-ledger or artifact-graph behavior, model-quality, benchmark, safety, ASI, or chapter-core claim.",
    },
    {
        "name": "Theseus governance-rights receipt suite import",
        "doc": "docs/theseus_governance_rights_receipt_suite_import.md",
        "script": "scripts/validate_theseus_governance_rights_receipt_suite_import.py",
        "summary": "Sanitized governance-rights receipt suite import with governance and constitutional-predicate fixture counts, record counts, public-safety checks, and seven controls.",
        "boundary": "No legal rights, institutional governance, reviewer independence, export usability, fork safety, deployed governance, clean live replay, safety, ASI, or chapter-core claim.",
    },
    {
        "name": "Theseus simulation-fidelity receipt suite import",
        "doc": "docs/theseus_simulation_fidelity_receipt_suite_import.md",
        "script": "scripts/validate_theseus_simulation_fidelity_receipt_suite_import.py",
        "summary": "Sanitized simulation-fidelity receipt suite import with fixture, contract, adapter, transfer-boundary, public-safety, and seven-control coverage.",
        "boundary": "No simulator adequacy, physical feasibility, benchmark transfer, native KV parity, deployment, model quality, clean live replay, safety, ASI, or chapter-core claim.",
    },
    {
        "name": "Compact GVR synthetic slice",
        "doc": "docs/compact_gvr_slice.md",
        "script": "scripts/validate_compact_gvr_slice.py",
        "summary": "Five compact-generation receipt records with selected compact receipt and negative controls.",
        "boundary": "No deployed compression, codec-correctness, semantic-utility, or chapter-core claim.",
    },
    {
        "name": "Residual ledger storage replay",
        "doc": "docs/residual_ledger_storage_replay.md",
        "script": "scripts/validate_residual_ledger_storage_replay.py",
        "summary": "Four append-only residual replay entries with owner handoff, discharge review, workload context, digest-chain construction, and five rejected controls.",
        "boundary": "No deployed residual-ledger storage, live residual detection, safety, model-quality, benchmark, or chapter-core claim.",
    },
    {
        "name": "Hive admission harness",
        "doc": "docs/hive_admission_harness.md",
        "script": "scripts/validate_hive_admission.py",
        "summary": "Personal Compute Hive admission fixtures and expected-invalid policy controls.",
        "boundary": "No deployed hive, network, scheduling, or support-state claim.",
    },
    {
        "name": "Runtime adapter effect replay probe",
        "doc": "docs/runtime_adapter_effect_probe.md",
        "script": "scripts/validate_runtime_adapter_effect_probe.py",
        "summary": "Checks `valid_low_impact_local_write_effect_replay`, rollback-exact temp-file restoration, `invalid_missing_permission_no_mutation`, and `invalid_expired_approval_no_mutation`.",
        "boundary": "No deployed adapter, sandbox, approval-service, rollback-service, or benchmark claim.",
    },
    {
        "name": "Runtime adapter adversarial boundary probe",
        "doc": "docs/runtime_adapter_adversarial_boundary_probe.md",
        "script": "scripts/validate_runtime_adapter_adversarial_boundary_probe.py",
        "summary": "Two valid adapter boundary reviews and twelve expected-invalid controls.",
        "boundary": "No deployed adapter, policy-enforcement, rollback, security-review, or support-state claim.",
    },
    {
        "name": "Artifact steward lifecycle probe",
        "doc": "docs/artifact_steward_lifecycle_probe.md",
        "script": "scripts/validate_artifact_steward_lifecycle_probe.py",
        "summary": "Checks `valid_clean_release_review_proposal`, `valid_sunset_review_route`, `invalid_tainted_event_without_review`, `invalid_over_policy_treasury_spend`, `invalid_contribution_governance_laundering`, `invalid_unscoped_federation_contract`, `invalid_release_without_gate_evidence`, and `invalid_sunset_criteria_ordinary_work`.",
        "boundary": "no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim",
    },
    {
        "name": "Intent re-contract trigger probe",
        "doc": "docs/intent_recontract_probe.md",
        "script": "scripts/validate_intent_recontract_probe.py",
        "summary": "Checks `valid_no_material_delta_continue`, `valid_publication_surface_delta_recontracts`, `invalid_authority_delta_without_recontract`, `invalid_private_source_delta_without_recontract`, `invalid_stop_condition_erasure_without_recontract`, `invalid_evidence_bar_weakening_without_recontract`, `invalid_affected_party_widening_without_recontract`, `invalid_means_expansion_without_recontract`, and `invalid_support_state_promotion_without_recontract`.",
        "boundary": "no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim",
    },
    {
        "name": "SCIF sanitized commit replay probe",
        "doc": "docs/security_scif_commit_probe.md",
        "script": "scripts/validate_security_scif_commit_probe.py",
        "summary": "Checks `valid_sanitized_commit_replay`, `valid_prompt_injection_blocked_commit`, `invalid_unsanitized_secret_commit_blocked`, `invalid_handle_leak_commit_blocked`, `invalid_missing_zeroize_commit_blocked`, `invalid_overbroad_context_commit_blocked`, `invalid_unapproved_destination_commit_blocked`, and `invalid_missing_residual_commit_blocked`.",
        "boundary": "no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim",
    },
    {
        "name": "Fast Generation task-bundle validation",
        "doc": "docs/fast_generation_task_bundle.md",
        "script": "scripts/validate_fast_generation_task_bundle.py",
        "summary": "Deterministic route selection over task-bundle candidates and latency-only rejection.",
        "boundary": "No model-speed, useful-solution-per-second, deployment, or support-state claim.",
    },
    {
        "name": "Cognitive compilation trace harness",
        "doc": "docs/cognitive_compilation_trace_harness.md",
        "script": "scripts/validate_cognitive_compilation_traces.py",
        "summary": "Cognitive Compilation trace fixtures and expected-invalid controls.",
        "boundary": "No deployed compiler, semantic-equivalence, or support-state claim.",
    },
    {
        "name": "RankFold public-safe replay probe",
        "doc": "docs/rankfold_public_safe_probe.md",
        "script": "scripts/validate_rankfold_public_safe_probe.py",
        "summary": "RAW0 roundtrip-exact public-safe archive replay plus mutation rejection.",
        "boundary": "No NeuralFold compression, compression advantage, codec-correctness, or deployed claim.",
    },
    {
        "name": "RankFold artifact import",
        "doc": "docs/rankfold_artifact_import.md",
        "script": "scripts/validate_rankfold_artifact_import.py",
        "summary": "Three local RankFold archive observations over a large decoded artifact digest.",
        "boundary": "No downstream utility, deployed compression, or support-state claim.",
    },
    {
        "name": "Prototype phase gate harness",
        "doc": "docs/prototype_phase_gate_harness.md",
        "script": "scripts/validate_prototype_phase_gates.py",
        "summary": "Phase acceptance, research-only phase debt, and six expected-invalid controls.",
        "boundary": "No phase-completion, deployed build-controller, benchmark, or release-readiness claim.",
    },
    {
        "name": "Typed job durable lifecycle probe",
        "doc": "docs/typed_job_durable_lifecycle_probe.md",
        "script": "scripts/validate_typed_job_durable_lifecycle_probe.py",
        "summary": "Two durable lifecycle traces and nine expected-invalid controls.",
        "boundary": "No deployed job service, retry engine, or support-state claim.",
    },
    {
        "name": "Readiness lifecycle probe",
        "doc": "docs/readiness_lifecycle_probe.md",
        "script": "scripts/validate_readiness_lifecycle_probe.py",
        "summary": "Six readiness lifecycle transitions and twelve expected-invalid controls.",
        "boundary": "No deployed readiness engine or support-state promotion.",
    },
    {
        "name": "Living-book change-packet harness",
        "doc": "docs/living_book_change_packet_harness.md",
        "script": "scripts/validate_living_book_change_packets.py",
        "summary": "Three valid living-book change packets and six expected-invalid controls.",
        "boundary": "No manuscript-quality, source-interpretation, release-approval, or future-agent-correctness claim.",
    },
    {
        "name": "Authority revocation propagation trace",
        "doc": "docs/authority_revocation_trace.md",
        "script": "scripts/validate_authority_revocation_trace.py",
        "summary": "Revoked authority receipt, expired approval, and SCIF inactive approval blockers.",
        "boundary": "No deployed revocation propagation or support-state promotion.",
    },
    {
        "name": "Epistemic trusted computing base fixture",
        "doc": "docs/epistemic_trusted_computing_base_fixture.md",
        "script": "scripts/validate_epistemic_trusted_computing_base.py",
        "summary": "Three bounded trust-base records and six expected-invalid trust-boundary controls.",
        "boundary": "No verifier-correctness, deployed trust-base, or support-state claim.",
    },
    {
        "name": "Human oversight degradation fixture",
        "doc": "docs/human_oversight_degradation_fixture.md",
        "script": "scripts/validate_human_oversight_degradation.py",
        "summary": "Three valid records, seven human-factors degradation controls, and accepted no-promotion decision.",
        "boundary": "No approval-service quality, reviewer-correctness, alert-quality, deployed human-factors, or chapter-core claim.",
    },
    {
        "name": "Partitioned authority fixture",
        "doc": "docs/partitioned_authority_fixture.md",
        "script": "scripts/validate_partitioned_authority_fixture.py",
        "summary": "Three finite records and six partitioned-authority expected-invalid controls.",
        "boundary": "No deployed partition tolerance, consensus, availability, revocation-propagation, or support-state claim.",
    },
]


BOOK_GATE_RESULTS_BY_SCRIPT = {
    "scripts/validate_stack_layer_traceability.py": "experiments/stack_layer_traceability/results/2026-07-02-local.md",
    "scripts/validate_artifact_graph_replay.py": "experiments/artifact_graph_replay/results/2026-06-30-local.md",
    "scripts/validate_artifact_graph_record_reality_sequence.py": "experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json",
    "scripts/validate_artifact_live_attestation_probe.py": "experiments/artifact_live_attestation/results/2026-07-04-local.json",
    "scripts/validate_artifact_randomized_attestation_audit.py": "experiments/artifact_randomized_attestation/results/2026-07-04-local.json",
    "scripts/validate_artifact_public_site_attestation.py": "experiments/artifact_public_site_attestation/results/2026-07-05-live.json",
    "scripts/validate_procedural_memory_loop.py": "experiments/procedural_memory_loop/results/2026-06-30-local.md",
    "scripts/validate_routing_decision_lease.py": "experiments/routing_decision_lease/results/2026-07-01-local.md",
    "scripts/validate_cyclic_memory_contracts.py": "experiments/cyclic_memory_contracts/results/2026-06-30-local.md",
    "scripts/validate_benchmark_fixture_bridge.py": "experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json",
    "scripts/validate_circle_cyclic_memory_receipt_slice.py": "experiments/circle_cyclic_memory_receipt_slice/results/2026-07-02-local.json",
    "scripts/validate_circle_kv_cache_receipt_slice.py": "experiments/circle_kv_cache_receipt_slice/results/2026-07-05-local.json",
    "scripts/validate_circle_recurrence_receipt_slice.py": "experiments/circle_recurrence_receipt_slice/results/2026-07-05-local.json",
    "scripts/validate_circle_sparse_attention_receipt_slice.py": "experiments/circle_sparse_attention_receipt_slice/results/2026-07-05-local.json",
    "scripts/validate_circle_contract_pack_archive.py": "experiments/circle_contract_pack_archive/results/2026-07-05-local.json",
    "scripts/validate_context_transaction_memory_store.py": "experiments/context_transaction_memory_store/results/2026-07-01-local.md",
    "scripts/validate_vcm_resolver_certificate_probe.py": "experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json",
    "scripts/validate_simulation_transfer_boundaries.py": "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
    "scripts/validate_resource_workflow_trace.py": "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "scripts/validate_resource_live_probe.py": "experiments/resource_live_probe/results/2026-07-01-local.json",
    "scripts/validate_resource_workload_quality_probe.py": "experiments/resource_workload_quality_probe/results/2026-07-01-local.json",
    "scripts/validate_resource_load_stability_probe.py": "experiments/resource_load_stability_probe/results/2026-07-01-local.json",
    "scripts/validate_theseus_support_replay_probe.py": "experiments/theseus_support_replay_probe/results/2026-07-01-local.json",
    "scripts/validate_theseus_report_bundle_audit.py": "experiments/theseus_report_bundle_audit/results/2026-07-02-local.json",
    "scripts/validate_theseus_public_task_bundle_import.py": "experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json",
    "scripts/validate_theseus_artifact_retention_replay_import.py": "experiments/theseus_artifact_retention_replay_import/results/2026-07-05-local.json",
    "scripts/validate_theseus_governance_rights_receipt_suite_import.py": "experiments/theseus_governance_rights_receipt_suite_import/results/2026-07-05-local.json",
    "scripts/validate_theseus_simulation_fidelity_receipt_suite_import.py": "experiments/theseus_simulation_fidelity_receipt_suite_import/results/2026-07-05-local.json",
    "scripts/validate_compact_gvr_slice.py": "experiments/compact_gvr_slice/results/2026-07-01-local.json",
    "scripts/validate_residual_ledger_storage_replay.py": "experiments/residual_ledger_storage_replay/results/2026-07-04-local.json",
    "scripts/validate_hive_admission.py": "experiments/hive_admission/results/2026-07-01-local.md",
    "scripts/validate_runtime_adapter_effect_probe.py": "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "scripts/validate_runtime_adapter_adversarial_boundary_probe.py": "experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json",
    "scripts/validate_artifact_steward_lifecycle_probe.py": "experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json",
    "scripts/validate_intent_recontract_probe.py": "experiments/intent_recontract_probe/results/2026-07-02-local.json",
    "scripts/validate_security_scif_commit_probe.py": "experiments/security_scif_commit_probe/results/2026-07-02-local.json",
    "scripts/validate_fast_generation_task_bundle.py": "experiments/fast_generation_task_bundle/results/2026-07-02-local.json",
    "scripts/validate_cognitive_compilation_traces.py": "experiments/cognitive_compilation_traces/results/2026-07-02-local.md",
    "scripts/validate_rankfold_public_safe_probe.py": "experiments/rankfold_public_safe_probe/results/2026-07-02-local.json",
    "scripts/validate_rankfold_artifact_import.py": "experiments/rankfold_artifact_import/results/2026-07-02-local.json",
    "scripts/validate_prototype_phase_gates.py": "experiments/prototype_phase_gates/results/2026-07-02-local.json",
    "scripts/validate_typed_job_durable_lifecycle_probe.py": "experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json",
    "scripts/validate_readiness_lifecycle_probe.py": "experiments/readiness_lifecycle_probe/results/2026-07-02-local.json",
    "scripts/validate_living_book_change_packets.py": "experiments/living_book_change_packets/results/2026-07-02-local.md",
    "scripts/validate_authority_revocation_trace.py": "experiments/authority_revocation_trace/results/2026-07-03-local.json",
    "scripts/validate_epistemic_trusted_computing_base.py": "experiments/epistemic_tcb/results/2026-07-03-local.json",
    "scripts/validate_human_oversight_degradation.py": "experiments/human_oversight_degradation/results/2026-07-03-local.json",
    "scripts/validate_partitioned_authority_fixture.py": "experiments/partitioned_authority/results/2026-07-03-local.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path | str) -> str:
    path = Path(path)
    if path.is_absolute():
        return str(path.relative_to(ROOT))
    return str(path)


def compact_status_row() -> str:
    total = len(load_json(REGISTRY)) + len(BOOK_GATE_CHECKS)
    return (
        f"| Test harnesses | {total} wired checks: {len(load_json(REGISTRY))} Phase 5 registry harnesses "
        f"and {len(BOOK_GATE_CHECKS)} chapter-specific/support book-gate checks. Detailed harness summaries, "
        "artifact references, and non-claim boundaries are generated in `docs/test_harness_status_ledger.md`; "
        "Appendix E remains the per-harness source of truth. None of these harnesses promotes chapter core claims. | "
        "`docs/test_harness_status_ledger.md`; `appendices/E_codex_test_specs.qmd`; "
        "`experiments/phase5_harness_registry.json`; `docs/phase5_harness_registry.md`; "
        "`python3 scripts/validate_test_harness_status_ledger.py`; "
        "`python3 scripts/validate_phase5_harness_registry.py`; `python3 scripts/validate_book.py` |"
    )


def phase5_rows(registry: list[dict[str, Any]]) -> list[str]:
    rows = [
        "| Harness | Command | Fixture expectation | Result record | Boundary |",
        "|---|---|---:|---|---|",
    ]
    for record in registry:
        valid = record.get("expected_valid_fixtures")
        invalid = record.get("expected_invalid_fixtures")
        boundary = " ".join(str(item) for item in record.get("non_claims", []))
        rows.append(
            "| "
            + " | ".join(
                [
                    str(record.get("name", "")),
                    f"`{record.get('command', '')}`",
                    f"{valid} valid, {invalid} expected-invalid",
                    f"`{record.get('result_record', '')}`",
                    boundary,
                ]
            )
            + " |"
        )
    return rows


def book_gate_rows() -> list[str]:
    rows = [
        "| Check | Public note | Command | Result record | Summary | Boundary |",
        "|---|---|---|---|---|---|",
    ]
    for check in BOOK_GATE_CHECKS:
        result = BOOK_GATE_RESULTS_BY_SCRIPT.get(check["script"], "")
        rows.append(
            "| "
            + " | ".join(
                [
                    check["name"],
                    f"`{check['doc']}`",
                    f"`python3 {check['script']}`",
                    f"`{result}`",
                    check["summary"],
                    check["boundary"],
                ]
            )
            + " |"
        )
    return rows


def render_ledger() -> str:
    registry = load_json(REGISTRY)
    if not isinstance(registry, list):
        raise TypeError("phase5 registry must be a list")
    total = len(registry) + len(BOOK_GATE_CHECKS)
    lines = [
        "# Test Harness Status Ledger",
        "",
        "Generated by `python3 scripts/validate_test_harness_status_ledger.py --write`.",
        "",
        "This ledger replaces the former long `Test harnesses` cell in `docs/v1_0_candidate_status.md`.",
        "It records implementation wiring and non-claim boundaries only; it does not promote any chapter core claim.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Total wired checks | {total} |",
        f"| Phase 5 registry harnesses | {len(registry)} |",
        f"| Chapter-specific/support book-gate checks | {len(BOOK_GATE_CHECKS)} |",
        "",
        "## Status-Page Row",
        "",
        compact_status_row(),
        "",
        "## Phase 5 Registry Harnesses",
        "",
        *phase5_rows(registry),
        "",
        "## Chapter-Specific And Support Book-Gate Checks",
        "",
        *book_gate_rows(),
        "",
        "## Non-Claims",
        "",
        "- This ledger does not prove runtime behavior, benchmark quality, model quality, proof adequacy, source interpretation, deployed enforcement, publication approval, or ASI safety.",
        "- This ledger does not create evidence transitions or promote Appendix C support states.",
        "- Appendix E remains the detailed per-chapter test-spec source of truth.",
        "",
    ]
    return "\n".join(lines)


def validate_path(path: str, errors: list[str]) -> None:
    if not (ROOT / path).exists():
        errors.append(f"Missing referenced path: {path}")


def validate(args: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    registry = load_json(REGISTRY)
    if not isinstance(registry, list):
        return ["experiments/phase5_harness_registry.json must contain a list."]
    if len(registry) != 22:
        errors.append(f"Expected 22 Phase 5 registry harnesses, found {len(registry)}.")
    if len(BOOK_GATE_CHECKS) != 48:
        errors.append(f"Expected 48 book-gate checks, found {len(BOOK_GATE_CHECKS)}.")

    names = [check["name"] for check in BOOK_GATE_CHECKS]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        errors.append(f"Duplicate book-gate check names: {duplicates}")

    for check in BOOK_GATE_CHECKS:
        validate_path(check["doc"], errors)
        validate_path(check["script"], errors)
        result = BOOK_GATE_RESULTS_BY_SCRIPT.get(check["script"])
        if not result:
            errors.append(f"Missing result mapping for book-gate check: {check['name']}")
        else:
            validate_path(result, errors)

    appendix_text = APPENDIX_E.read_text(encoding="utf-8")
    for required_fragment in (
        "# Codex Test Specs",
        "No result is recorded here unless a test has actually been implemented and run.",
        "| Chapter ID | Chapter | Test spec | Implementation status | Result status |",
    ):
        if required_fragment not in appendix_text:
            errors.append(f"Appendix E is missing required generated-test-spec fragment: {required_fragment}")

    expected = render_ledger()
    if args.write:
        LEDGER.write_text(expected, encoding="utf-8")
    elif not LEDGER.exists():
        errors.append(f"{rel(LEDGER)} is missing; run with --write.")
    elif LEDGER.read_text(encoding="utf-8") != expected:
        errors.append(f"{rel(LEDGER)} is out of date; run with --write.")

    status_text = STATUS.read_text(encoding="utf-8")
    status_row = compact_status_row()
    if status_row not in status_text:
        errors.append(f"{rel(STATUS)} is missing the compact test-harness status row.")
    for stale in (
        "| Test harnesses | Fifty-nine synthetic",
        "The artifact graph record-reality sequence bridge checks one valid stale/partial/fresh replay sequence",
    ):
        if stale in status_text:
            errors.append(f"{rel(STATUS)} still contains stale expanded test-harness text: {stale}")
    for line in status_text.splitlines():
        if line.startswith("| Test harnesses |") and len(line) > 900:
            errors.append(f"{rel(STATUS)} Test harnesses row is still too long: {len(line)} characters.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    errors = validate(args)
    if errors:
        print("Test harness status ledger validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    total = len(load_json(REGISTRY)) + len(BOOK_GATE_CHECKS)
    action = "wrote" if args.write else "validated"
    print(
        f"Test harness status ledger {action}: {total} wired checks "
        f"({len(load_json(REGISTRY))} Phase 5, {len(BOOK_GATE_CHECKS)} book-gate)."
    )


if __name__ == "__main__":
    main()
