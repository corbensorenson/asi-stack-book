#!/usr/bin/env python3
"""Validate cumulative dependency-safe C6 proof-rationalization transactions."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from build_proof_rationalization_registry import current_theorems, normalize
from build_proof_semantic_depth_overlay import statement_key, theorem_graph, validation_index


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "proofs" / "proof_semantic_rationalization_ledger.json"
SCHEMA = ROOT / "schemas" / "proof_semantic_rationalization_ledger.schema.json"
CURRENT_OVERLAY = ROOT / "proofs" / "proof_semantic_depth_overlay.json"
HISTORICAL = ROOT / "proofs" / "proof_rationalization_registry.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_maintenance_transfer_and_publication_status.json"
ROADMAP = ROOT / "docs" / "post_v2_3_maintenance_transfer_and_publication_roadmap.md"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)
EXPECTED_ACTION_IDS = [
    "C6-R1-scalable-oversight-same-model-duplicate",
    "C6-R2-bibliography-source-evidence-projection",
    "C6-R3-bibliography-chapter-assignment-projection",
    "C6-R4-benchmark-readiness-projection",
    "C6-R5-benchmark-saturation-projection",
    "C6-R6-policy-promotion-evidence-projection",
    "C6-R7-policy-reward-proxy-projection",
    "C6-R8-policy-authority-expansion-projection",
    "C6-R9-scf-qualification-projection",
    "C6-R10-scf-identity-projection",
    "C6-R11-scf-forward-route-projection",
    "C6-R12-scf-canary-readiness-projection",
    "C6-R13-scf-qualified-readiness-projection",
    "C6-R14-scf-deprecation-notice-projection",
    "C6-R15-scf-retirement-receipt-projection",
    "C6-R16-evidence-support-requirement-projection",
    "C6-R17-evidence-terminal-negative-projection",
    "C6-R18-evidence-downgrade-negative-trigger-projection",
    "C6-R19-evidence-bundle-summary-projection",
    "C6-R20-claim-ledger-summary-projection",
    "C6-R21-accepted-transition-summary-projection",
    "C6-R22-claim-state-negative-evidence-projection",
    "C6-R23-claim-state-no-live-movement-projection",
    "C6-R24-claim-state-nonclaim-projection",
    "C6-R25-runtime-adapter-permission-projection",
    "C6-R26-runtime-adapter-approval-projection",
    "C6-R27-runtime-adapter-lease-scope-projection",
    "C6-R28-runtime-adapter-rollback-projection",
    "C6-R29-runtime-adapter-adversarial-summary-projection",
    "C6-R30-substrate-adoption-fields-projection",
    "C6-R31-substrate-non-core-projection",
    "C6-R32-substrate-qualified-evidence-projection",
    "C6-R33-substrate-axis-summary-projection",
    "C6-R34-substrate-no-promotion-summary-projection",
    "C6-R35-artifact-steward-work-contract-projection",
    "C6-R36-artifact-steward-treasury-projection",
    "C6-R37-artifact-steward-release-projection",
    "C6-R38-artifact-steward-sunset-projection",
    "C6-R39-coil-memory-alias-projection",
    "C6-R40-coil-memory-quality-projection",
    "C6-R41-cyclic-mixer-partition-projection",
    "C6-R42-cyclic-mixer-promotion-projection",
    "C6-R43-efficiency-minimum-route-projection",
    "C6-R44-efficiency-residual-projection",
    "C6-R45-failure-authority-projection",
]
EXPECTED_LEVELS = {
    "P0": 42,
    "P1": 765,
    "P2": 25,
    "P3": 319,
    "P4": 93,
    "P5": 81,
    "P6": 0,
}
EXPECTED_DISPOSITIONS = {
    "retain": 1209,
    "retire_narrow_projection": 19,
    "rewrite_scope_language": 2,
    "rewrite_with_stronger_model": 95,
}
EXPECTED_TARGETS = {
    "lean:bibliography.plan.operational_invariant": (
        "A source-derived claim with neither a source note nor an ingested artifact "
        "fails the finite source-evidence predicate."
    ),
    "lean:bibliography.plan.failure_blocks_promotion": (
        "An accepted new-source assignment to a nonexistent chapter fails the finite "
        "assignment predicate."
    ),
    "lean:benchmarks.ratchet.operational_invariant": (
        "An accepted readiness-promotion decision in the finite ratchet model requires "
        "transfer-or-mutation checks, preserved negative evidence, and preserved "
        "regression records."
    ),
    "lean:benchmarks.ratchet.failure_blocks_promotion": (
        "An accepted contaminated benchmark review cannot select readiness promotion "
        "in the finite ratchet model."
    ),
    "lean:scf.field_identity.operational_invariant": (
        "A lifecycle review with a mismatched field identity routes to explicit "
        "replacement rejection."
    ),
    "lean:scf.lifecycle.route_envelope": (
        "A structured SCF lifecycle review routes identity mismatch, missing evidence, "
        "stale leases, evaluator capture, authority expansion, and open incidents to "
        "explicit nondefault outcomes; the finite transition predicate rejects retired "
        "restart and default promotion without qualification evidence, preserved "
        "regressions, authority within ceiling, rollback readiness, or incident closure."
    ),
    "lean:evidence.support_state.operational_invariant": (
        "A reachable evidence-admission model derives state-specific artifact "
        "requirements from the requested support state and inspected evidence bundle "
        "rather than assuming the RequiredEvidence predicate."
    ),
    "lean:evidence.bundle.completeness_probe_bridge": (
        "An independently implemented formal bridge derives the evidence-bundle "
        "probe's accepted and rejected outcomes from exact bundle inputs and audit "
        "logic rather than assuming a valid summary predicate."
    ),
    "lean:evidence.claim_ledger.completeness_audit_bridge": (
        "An independently implemented formal bridge derives claim-ledger completeness "
        "and rejection outcomes from exact manifest and Appendix C inputs rather than "
        "assuming a valid summary predicate."
    ),
    "lean:evidence.accepted_transition.review_audit_bridge": (
        "An independently implemented formal bridge derives accepted-transition audit "
        "outcomes from exact transition, no-promotion, changelog, and evidence inputs "
        "rather than assuming a valid summary predicate."
    ),
    "lean:evidence.claim_state.transition_bridge": (
        "A reachable claim-state lifecycle model derives negative-evidence, "
        "no-live-movement, and non-claim conclusions from narrowing, downgrade, and "
        "refutation cases rather than projecting fields from a hand-authored summary "
        "predicate."
    ),
    "lean:substrates.search.operational_invariant": (
        "A substrate adoption record missing a baseline reference, measured target, "
        "or falsification criterion fails the finite adoption-fields predicate."
    ),
    "lean:substrates.search.failure_blocks_promotion": (
        "A substrate record marked qualified without passing evidence fails the finite "
        "core-adoption predicate."
    ),
    "lean:substrates.search.adoption_trace_bridge": (
        "A reachable formal substrate-adoption route model derives the four accepted "
        "states and eight rejected controls from exact trace inputs rather than "
        "projecting fields from a hand-authored valid-summary predicate."
    ),
    "lean:artifact_stewards.work_contract.operational_invariant": (
        "A reachable steward dispatch model derives contract repair or refusal when "
        "objective, authority, tool, verification, budget, or non-claim boundaries "
        "are missing."
    ),
    "lean:artifact_stewards.treasury_boundary.failure_blocks_promotion": (
        "A finite steward lifecycle decision with requested treasury spend outside "
        "policy routes to approval."
    ),
    "lean:artifact_stewards.release_gate.operational_invariant": (
        "A reachable steward release model derives refusal when test, evidence, "
        "changelog, residual, or approval records are missing."
    ),
    "lean:artifact_stewards.sunset_review.failure_blocks_promotion": (
        "A finite steward lifecycle decision with sunset criteria met and no open "
        "review routes to sunset review."
    ),
    "lean:coil_memory.alias_boundary.operational_invariant": (
        "A reused cyclic slot with missing residue or winding and no visible alias "
        "residual fails the finite alias-boundary predicate."
    ),
    "lean:coil_attention.coverage_not_quality.failure_blocks_promotion": (
        "A retrieval-quality record that promotes from sparse coverage and freshness "
        "while semantic-quality evidence is absent fails the finite quality-promotion "
        "predicate."
    ),
    "lean:cyclic_mixers.structural_not_quality.operational_invariant": (
        "A cyclic mixer review missing any structural, quality, runtime, memory, or "
        "parameter partition fails the finite structural-claim predicate."
    ),
    "lean:cyclic_mixers.baseline_required.failure_blocks_promotion": (
        "A promoted cyclic substrate missing baseline references or tradeoff metrics "
        "fails the finite promotion predicate."
    ),
    "lean:efficiency.minimum_viable.operational_invariant": (
        "A listed lower-cost authorized quality-preserving candidate causes the finite "
        "minimum-viable-route predicate to fail."
    ),
    "lean:efficiency.minimum_viable.failure_blocks_promotion": (
        "A promoted result with open obligations and no residual record causes the "
        "finite residual-promotion predicate to fail."
    ),
    "lean:failure.invariant_violation.failure_blocks_promotion": (
        "A finite incident whose authority exceeds its ceiling routes to explicit "
        "authority review."
    ),
}
PLANNED_TARGETS = {
    "lean:evidence.support_state.operational_invariant",
    "lean:evidence.bundle.completeness_probe_bridge",
    "lean:evidence.claim_ledger.completeness_audit_bridge",
    "lean:evidence.accepted_transition.review_audit_bridge",
    "lean:evidence.claim_state.transition_bridge",
    "lean:substrates.search.adoption_trace_bridge",
    "lean:artifact_stewards.work_contract.operational_invariant",
    "lean:artifact_stewards.release_gate.operational_invariant",
}
EXPECTED_RELATIONS = {
    "retire_exact_same_model_duplicate": "exact_same_model_normalized_statement",
    "retire_projection_after_counterexample_consumer_migration": (
        "premise_restatement_replaced_by_derived_counterexample_gate"
    ),
    "retire_projection_after_decision_model_consumer_migration": (
        "premise_restatement_replaced_by_derived_decision_gate"
    ),
    "retire_projection_after_public_target_narrowing": (
        "premise_restatement_retired_after_target_scope_reduction"
    ),
    "retire_unconsumed_projection": (
        "premise_restatement_removed_without_public_target_change"
    ),
    "retire_projection_after_validator_route_family_rebinding": (
        "summary_projection_replaced_by_route_family_validation"
    ),
}
EXPECTED_MIGRATION_COUNTS = {
    action_id: int(action_id in {
        "C6-R2-bibliography-source-evidence-projection",
        "C6-R3-bibliography-chapter-assignment-projection",
        "C6-R4-benchmark-readiness-projection",
        "C6-R5-benchmark-saturation-projection",
        "C6-R9-scf-qualification-projection",
        "C6-R10-scf-identity-projection",
        "C6-R16-evidence-support-requirement-projection",
        "C6-R19-evidence-bundle-summary-projection",
        "C6-R20-claim-ledger-summary-projection",
        "C6-R21-accepted-transition-summary-projection",
        "C6-R22-claim-state-negative-evidence-projection",
        "C6-R30-substrate-adoption-fields-projection",
        "C6-R31-substrate-non-core-projection",
        "C6-R33-substrate-axis-summary-projection",
        "C6-R35-artifact-steward-work-contract-projection",
        "C6-R36-artifact-steward-treasury-projection",
        "C6-R37-artifact-steward-release-projection",
        "C6-R38-artifact-steward-sunset-projection",
        "C6-R39-coil-memory-alias-projection",
        "C6-R40-coil-memory-quality-projection",
        "C6-R41-cyclic-mixer-partition-projection",
        "C6-R42-cyclic-mixer-promotion-projection",
        "C6-R43-efficiency-minimum-route-projection",
        "C6-R44-efficiency-residual-projection",
        "C6-R45-failure-authority-projection",
    })
    for action_id in EXPECTED_ACTION_IDS
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def theorem_blocks(text: str) -> dict[str, dict[str, str]]:
    declarations = list(DECL_START.finditer(text))
    rows: dict[str, dict[str, str]] = {}
    for match in THEOREM_START.finditer(text):
        end = next(
            (candidate.start() for candidate in declarations if candidate.start() > match.start()),
            len(text),
        )
        block = text[match.start():end]
        signature = normalize(block.split(":= by", 1)[0])
        rows[match.group(1)] = {
            "block": block,
            "signature": signature,
            "statement_sha256": sha256_bytes(statement_key(signature).encode("utf-8")),
        }
    return rows


def schema_errors(ledger: dict[str, Any]) -> list[str]:
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(ledger)
    except jsonschema.ValidationError as exc:
        return [f"schema: {exc.message}"]
    return []


def validation_errors(ledger: dict[str, Any], *, check_files: bool = True) -> list[str]:
    out = schema_errors(ledger)
    if out or not check_files:
        return out

    baseline = ledger["classification_baseline"]
    actions = ledger["actions"]
    if [row["action_id"] for row in actions] != EXPECTED_ACTION_IDS:
        out.append("action sequence or identity drifted")
    if [row["sequence"] for row in actions] != list(range(1, 46)):
        out.append("action sequence numbers drifted")

    try:
        baseline_overlay_bytes = git_show(baseline["commit"], baseline["overlay_path"])
    except subprocess.CalledProcessError as exc:
        return out + [f"immutable classification baseline cannot be read: {exc}"]
    if sha256_bytes(baseline_overlay_bytes) != baseline["overlay_sha256"]:
        out.append("classification-baseline overlay digest drifted")
    baseline_overlay = json.loads(baseline_overlay_bytes)
    baseline_rows = {
        row["theorem_id"]: row for row in baseline_overlay.get("records", [])
    }
    if len(baseline_rows) != baseline["live_theorem_count"]:
        out.append("classification-baseline theorem denominator drifted")
    if sum(row.get("disposition") != "retain" for row in baseline_rows.values()) != baseline[
        "rewrite_or_retire_count"
    ]:
        out.append("classification-baseline action denominator drifted")

    module_cache: dict[str, dict[str, dict[str, str]]] = {}
    module_bytes_cache: dict[str, bytes] = {}
    for action in actions:
        if action["semantic_relation"] != EXPECTED_RELATIONS[action["action"]]:
            out.append(f"{action['action_id']}: action and semantic relation disagree")
        module = action["module_path"]
        retired_id = action["retired_theorem_id"]
        replacement_id = action["replacement_theorem_id"]
        if retired_id.split("::", 1)[0] != module:
            out.append(f"{action['action_id']}: participants are not bound to one module")
            continue
        if replacement_id is not None and replacement_id.split("::", 1)[0] != module:
            out.append(f"{action['action_id']}: participants are not bound to one module")
            continue
        if module not in module_cache:
            try:
                module_bytes_cache[module] = git_show(baseline["commit"], module)
            except subprocess.CalledProcessError as exc:
                out.append(f"{action['action_id']}: baseline module cannot be read: {exc}")
                continue
            module_cache[module] = theorem_blocks(module_bytes_cache[module].decode("utf-8"))
        if sha256_bytes(module_bytes_cache[module]) != action["baseline_module_sha256"]:
            out.append(f"{action['action_id']}: baseline module digest drifted")
        retired_name = retired_id.split("::", 1)[1]
        retired_block = module_cache[module].get(retired_name)
        replacement_block = (
            module_cache[module].get(replacement_id.split("::", 1)[1])
            if replacement_id is not None
            else None
        )
        if retired_block is None or (replacement_id is not None and replacement_block is None):
            out.append(f"{action['action_id']}: baseline theorem block is missing")
            continue
        if sha256_bytes(retired_block["block"].encode("utf-8")) != action["retired_block_sha256"]:
            out.append(f"{action['action_id']}: retired block digest drifted")
        if retired_block["statement_sha256"] != action["retired_statement_sha256"]:
            out.append(f"{action['action_id']}: retired statement digest drifted")
        if replacement_id is None:
            if (
                action["replacement_block_sha256"] is not None
                or action["replacement_statement_sha256"] is not None
            ):
                out.append(f"{action['action_id']}: null replacement carries replacement digests")
        else:
            if sha256_bytes(replacement_block["block"].encode("utf-8")) != action[
                "replacement_block_sha256"
            ]:
                out.append(f"{action['action_id']}: replacement block digest drifted")
            if replacement_block["statement_sha256"] != action["replacement_statement_sha256"]:
                out.append(f"{action['action_id']}: replacement statement digest drifted")

        retired_row = baseline_rows.get(retired_id)
        replacement_row = baseline_rows.get(replacement_id) if replacement_id is not None else None
        if retired_row is None or (replacement_id is not None and replacement_row is None):
            out.append(f"{action['action_id']}: classification baseline lacks a participant")
            continue
        expected_disposition = (
            "retire_duplicate"
            if action["action"] == "retire_exact_same_model_duplicate"
            else "retire_narrow_projection"
        )
        if retired_row.get("disposition") != expected_disposition:
            out.append(f"{action['action_id']}: baseline retirement disposition drifted")
        if replacement_row is not None and replacement_row.get("disposition") != "retain":
            out.append(f"{action['action_id']}: replacement was not retained at baseline")
        if action["dependency_check"]["retired_theorem_dependency_refs"] != retired_row.get(
            "theorem_dependency_refs"
        ):
            out.append(f"{action['action_id']}: baseline dependency custody drifted")
        if retired_row.get("theorem_dependency_refs") != []:
            out.append(f"{action['action_id']}: retired theorem had theorem dependencies")
        if action["dependency_check"]["retired_theorem_consumer_refs"] != retired_row.get(
            "theorem_consumer_refs"
        ):
            out.append(f"{action['action_id']}: baseline consumer custody drifted")

        if len(action["target_migrations"]) != EXPECTED_MIGRATION_COUNTS[action["action_id"]]:
            out.append(f"{action['action_id']}: target migration count drifted")

        if action["action"] == "retire_exact_same_model_duplicate":
            if statement_key(retired_block["signature"]) != statement_key(
                replacement_block["signature"]
            ):
                out.append(f"{action['action_id']}: exact duplicate statements differ")
        elif action["action"] == "retire_projection_after_counterexample_consumer_migration":
            if "exact " not in retired_block["block"]:
                out.append(f"{action['action_id']}: retired theorem is not the audited projection")
            if (
                not any(token in replacement_block["block"] for token in ("have ", "cases ", "rcases "))
                or not any(token in replacement_block["block"] for token in ("rw [", "exact "))
            ):
                out.append(f"{action['action_id']}: replacement lacks derived counterexample steps")
        elif action["action"] == "retire_projection_after_decision_model_consumer_migration":
            if "exact " not in retired_block["block"]:
                out.append(f"{action['action_id']}: retired theorem is not the audited projection")
            ratchet_derivation = (
                "unfold RatchetDecisionAccepted" in replacement_block["block"]
                and "rw [" in replacement_block["block"]
            )
            steward_route_derivation = (
                "unfold StewardLifecycleRouteFor" in replacement_block["block"]
                and "simp [" in replacement_block["block"]
            )
            failure_route_derivation = (
                "unfold FailureIncidentRouteFor" in replacement_block["block"]
                and "simp [" in replacement_block["block"]
            )
            if not (
                ratchet_derivation
                or steward_route_derivation
                or failure_route_derivation
            ):
                out.append(f"{action['action_id']}: replacement lacks decision-model derivation")
        elif action["action"] in {
            "retire_projection_after_public_target_narrowing",
            "retire_unconsumed_projection",
            "retire_projection_after_validator_route_family_rebinding",
        }:
            if replacement_id is not None or replacement_block is not None:
                out.append(f"{action['action_id']}: null-replacement retirement invented a replacement")
            if (
                "exact " not in retired_block["block"]
                and "rcases valid with" not in retired_block["block"]
            ):
                out.append(f"{action['action_id']}: retired theorem is not a direct projection")
        else:
            out.append(f"{action['action_id']}: unsupported action kind")

    current_rows = current_theorems()
    current_ids = {row["theorem_id"] for row in current_rows}
    _, current_consumers = theorem_graph(current_rows)
    for action in actions:
        if action["retired_theorem_id"] in current_ids:
            out.append(f"{action['action_id']}: retired theorem remains live")
        if (
            action["replacement_theorem_id"] is not None
            and action["replacement_theorem_id"] not in current_ids
        ):
            out.append(f"{action['action_id']}: replacement theorem is not live")
        if current_consumers.get(action["retired_theorem_id"], []):
            out.append(f"{action['action_id']}: retired theorem has a current Lean consumer")

    overlay = load(CURRENT_OVERLAY)
    summary = overlay.get("summary", {})
    if summary.get("current_theorem_count") != 1325:
        out.append("current theorem denominator drifted")
    if summary.get("semantic_level_counts") != EXPECTED_LEVELS:
        out.append("current semantic-level counts drifted")
    if summary.get("disposition_counts") != EXPECTED_DISPOSITIONS:
        out.append("current disposition counts drifted")
    if sum(value for key, value in EXPECTED_DISPOSITIONS.items() if key != "retain") != 116:
        out.append("expected remaining-action denominator is internally inconsistent")
    if ledger["summary"]["remaining_action_counts"] != {
        key: value for key, value in EXPECTED_DISPOSITIONS.items() if key != "retain"
    }:
        out.append("ledger remaining-action family counts drifted")
    if summary.get("duplicate_group_count") != 0:
        out.append("same-model exact duplicate group remains")
    meta_validator_ref = "scripts/validate_proof_semantic_rationalization_ledger.py"
    binding_index = validation_index()
    for module in {action["module_path"] for action in actions}:
        if meta_validator_ref in binding_index.get(module, {}).get("validator_refs", []):
            out.append(f"{module}: proof-custody meta-audit inflated implementation binding")

    bibliography_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/BibliographyPlan.lean"
    ]
    if len(bibliography_rows) != 2:
        out.append("BibliographyPlan must retain exactly the two derived counterexample theorems")
    if any(row.get("depth_class") != "derived_or_decomposed" for row in bibliography_rows):
        out.append("BibliographyPlan retained a direct projection")

    benchmark_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/BenchmarkRatchets.lean"
    ]
    if len(benchmark_rows) != 6:
        out.append("BenchmarkRatchets must retain exactly six derived declarations")
    if any(row.get("depth_class") == "direct_or_projection" for row in benchmark_rows):
        out.append("BenchmarkRatchets retained a direct projection")

    policy_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/PolicyOptimization.lean"
    ]
    if len(policy_rows) != 16:
        out.append("PolicyOptimization must retain exactly sixteen declarations")
    retired_policy_names = {
        "promoted_policy_update_records_holdouts_probes_regressions_and_rollback",
        "reward_proxy_promotion_requires_target_evaluation",
        "authority_expanding_policy_update_requires_approval_and_rollback",
    }
    if retired_policy_names & {row["name"] for row in policy_rows}:
        out.append("PolicyOptimization retained an executed narrow projection")

    scf_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/StableCapabilityFields.lean"
    ]
    if len(scf_rows) != 18:
        out.append("StableCapabilityFields must retain exactly eighteen declarations")
    retired_scf_names = {
        "replacement_requires_field_qualification",
        "allowed_transition_preserves_field_identity",
        "allowed_transition_must_be_forward_or_quarantine",
        "canary_transition_requires_evidence_and_rollback",
        "qualified_transition_requires_evidence_and_regression_floor",
        "deprecated_transition_requires_notice",
        "retirement_transition_requires_receipt",
    }
    if retired_scf_names & {row["name"] for row in scf_rows}:
        out.append("StableCapabilityFields retained an executed narrow projection")

    evidence_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/EvidenceStates.lean"
    ]
    if len(evidence_rows) != 22:
        out.append("EvidenceStates must retain exactly twenty-two declarations")
    retired_evidence_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/EvidenceStates.lean"
    }
    if retired_evidence_names & {row["name"] for row in evidence_rows}:
        out.append("EvidenceStates retained an executed premise or summary projection")

    runtime_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/RuntimeAdapters.lean"
    ]
    retired_runtime_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/RuntimeAdapters.lean"
    }
    if retired_runtime_names & {row["name"] for row in runtime_rows}:
        out.append("RuntimeAdapters retained an executed premise or summary projection")

    substrate_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/SearchSubstrates.lean"
    ]
    retired_substrate_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/SearchSubstrates.lean"
    }
    if len(substrate_rows) != 6:
        out.append("SearchSubstrates must retain exactly six declarations")
    if retired_substrate_names & {row["name"] for row in substrate_rows}:
        out.append("SearchSubstrates retained an executed premise or summary projection")

    steward_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/ArtifactStewardAgents.lean"
    ]
    retired_steward_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/ArtifactStewardAgents.lean"
    }
    if len(steward_rows) != 12:
        out.append("ArtifactStewardAgents must retain exactly twelve route declarations")
    if retired_steward_names & {row["name"] for row in steward_rows}:
        out.append("ArtifactStewardAgents retained an executed premise projection")
    steward_source = (ROOT / "lean/AsiStackProofs/ArtifactStewardAgents.lean").read_text(
        encoding="utf-8"
    )
    for removed_model_name in [
        "StewardWorkContractReview",
        "DispatchedContractHasRequiredBoundary",
        "StewardProtectedActionReview",
        "MissingApprovalBlocksProtectedAction",
        "StewardReleaseGateReview",
        "PublishedReleaseRequiresEvidenceGate",
        "StewardSunsetReview",
        "SunsetCriteriaBlocksOrdinaryWork",
    ]:
        if removed_model_name in steward_source:
            out.append(f"ArtifactStewardAgents retained dead projection model {removed_model_name}")

    coil_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/CoilAttentionMemory.lean"
    ]
    retired_coil_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/CoilAttentionMemory.lean"
    }
    if len(coil_rows) != 4:
        out.append("CoilAttentionMemory must retain exactly four derived negative cases")
    if retired_coil_names & {row["name"] for row in coil_rows}:
        out.append("CoilAttentionMemory retained an executed premise projection")

    cyclic_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/CyclicMixers.lean"
    ]
    retired_cyclic_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/CyclicMixers.lean"
    }
    if len(cyclic_rows) != 5:
        out.append("CyclicMixers must retain exactly five derived negative cases")
    if retired_cyclic_names & {row["name"] for row in cyclic_rows}:
        out.append("CyclicMixers retained an executed premise projection")

    efficiency_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/Efficiency.lean"
    ]
    retired_efficiency_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/Efficiency.lean"
    }
    if len(efficiency_rows) != 24:
        out.append("Efficiency must retain exactly twenty-four declarations")
    if retired_efficiency_names & {row["name"] for row in efficiency_rows}:
        out.append("Efficiency retained an executed premise projection")

    failure_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/FailureModes.lean"
    ]
    retired_failure_names = {
        action["retired_theorem_id"].split("::", 1)[1]
        for action in actions
        if action["module_path"] == "lean/AsiStackProofs/FailureModes.lean"
    }
    if len(failure_rows) != 22:
        out.append("FailureModes must retain exactly twenty-two declarations")
    if retired_failure_names & {row["name"] for row in failure_rows}:
        out.append("FailureModes retained an executed premise projection")

    manifest_rows = {
        row["tag"]: row
        for row in load(MANIFEST).get("records", [])
    }
    for target, expected in EXPECTED_TARGETS.items():
        if manifest_rows.get(target, {}).get("formal_target") != expected:
            out.append(f"proof target did not migrate to the counterexample gate: {target}")
        expected_status = "planned" if target in PLANNED_TARGETS else "implemented"
        if manifest_rows.get(target, {}).get("status") != expected_status:
            out.append(f"proof target status did not reconcile after migration: {target}")
    triage_rows = {row["tag"]: row for row in load(TRIAGE).get("records", [])}
    for target, expected in EXPECTED_TARGETS.items():
        if triage_rows.get(target, {}).get("formal_target") != expected:
            out.append(f"proof triage did not migrate to the counterexample gate: {target}")
        expected_status = "planned" if target in PLANNED_TARGETS else "implemented"
        if triage_rows.get(target, {}).get("target_status") != expected_status:
            out.append(f"proof triage status did not reconcile after migration: {target}")
    for action in actions:
        for migration in action["target_migrations"]:
            expected = migration["new_target_text"]
            for relative_path in migration["consumer_paths"]:
                if relative_path in {
                    "proofs/proof_manifest.json",
                    "proofs/proof_triage.json",
                }:
                    continue
                path = ROOT / relative_path
                if expected not in path.read_text(encoding="utf-8"):
                    out.append(f"{relative_path} lacks migrated target {migration['target_ref']}")

    historical = load(HISTORICAL)
    if len(historical.get("baseline_theorems", [])) != 1151:
        out.append("frozen historical theorem denominator changed")
    if len(historical.get("baseline_targets", [])) != 298:
        out.append("frozen historical target denominator changed")

    status = load(STATUS)["quality_uplift_program"]["post_review_convergence"][
        "c6_current_semantic_overlay"
    ]
    if status.get("rationalization_ledger_path") != str(LEDGER.relative_to(ROOT)):
        out.append("status does not bind the cumulative rationalization ledger")
    if (
        status.get("theorem_count") != 1325
        or status.get("executed_retirement_count") != 45
        or status.get("remaining_action_count") != 116
    ):
        out.append("status does not report the cumulative post-transaction denominator")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    roadmap_flat = " ".join(roadmap.split())
    for phrase in [
        "tenth narrow-projection tranche",
        "1,325 live theorem declarations",
        "116 rewrite-or-retire actions remain",
        "`proofs/proof_semantic_rationalization_ledger.json`",
    ]:
        if phrase not in roadmap_flat:
            out.append(f"roadmap does not report the cumulative transaction: {phrase}")
    if ledger["support_state_effect"] != "none" or ledger["release_effect"] != "none":
        out.append("rationalization transactions changed support or release state")
    return out


def main() -> None:
    ledger = load(LEDGER)
    failures = validation_errors(ledger)
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(label: str, fn: Any) -> None:
        candidate = copy.deepcopy(ledger)
        fn(candidate)
        mutations.append((label, candidate))

    mutate("baseline commit substitution", lambda c: c["classification_baseline"].__setitem__("commit", "0" * 40))
    mutate("overlay digest substitution", lambda c: c["classification_baseline"].__setitem__("overlay_sha256", "0" * 64))
    mutate("action deletion", lambda c: c["actions"].pop())
    mutate("action reordering", lambda c: c["actions"].reverse())
    mutate("retired identity substitution", lambda c: c["actions"][1].__setitem__("retired_theorem_id", c["actions"][1]["replacement_theorem_id"]))
    mutate("replacement identity substitution", lambda c: c["actions"][2].__setitem__("replacement_theorem_id", c["actions"][2]["retired_theorem_id"]))
    mutate("statement substitution", lambda c: c["actions"][1].__setitem__("retired_statement_sha256", "0" * 64))
    mutate("dependency laundering", lambda c: c["actions"][1]["dependency_check"]["retired_theorem_dependency_refs"].append("theorem:x"))
    mutate("consumer laundering", lambda c: c["actions"][2]["dependency_check"]["retired_theorem_consumer_refs"].append("theorem:x"))
    mutate("target migration erasure", lambda c: c["actions"][1].__setitem__("target_migrations", []))
    mutate(
        "decision semantic laundering",
        lambda c: c["actions"][3].__setitem__(
            "semantic_relation",
            "premise_restatement_replaced_by_derived_counterexample_gate",
        ),
    )
    mutate("remaining denominator inflation", lambda c: c["summary"].__setitem__("remaining_action_count", 148))
    mutate("support promotion", lambda c: c.__setitem__("support_state_effect", "promotion"))
    mutate(
        "null replacement laundering",
        lambda c: c["actions"][10].__setitem__(
            "replacement_theorem_id",
            c["actions"][0]["replacement_theorem_id"],
        ),
    )

    for label, candidate in mutations:
        if not validation_errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Proof semantic-rationalization ledger validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "Proof semantic-rationalization ledger passed: forty-five dependency-safe "
        "retirements, twenty-five public-target migrations, 1,325 live theorems, "
        "116 actions remain, 14 rejecting mutations, no support or release effect."
    )


if __name__ == "__main__":
    main()
