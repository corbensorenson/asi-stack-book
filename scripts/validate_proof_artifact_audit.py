#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
RATIONALIZATION = ROOT / "proofs" / "proof_rationalization_registry.json"
ROOT_LEAN_MODULE = ROOT / "lean" / "AsiStackProofs.lean"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
REPORT = ROOT / "docs" / "proof_artifact_audit.md"
PROOF_ENVELOPE = ROOT / "lean" / "AsiStackProofs" / "ProofEnvelope.lean"
LEAN_ROOT = ROOT / "lean"
EXPECTED_PROOF_ENVELOPE_THEOREM_COUNT = 28
REQUIRED_PROOF_ENVELOPE_THEOREMS = {
    "artifact_change_invalidates_active_lease",
    "complete_proof_lease_trace_reissues_changed_artifact_then_revokes",
    "complete_proof_lease_transport_is_injective",
    "complete_proof_lease_transport_preserves_step",
    "complete_proof_lease_transport_round_trips",
    "expired_issue_is_rejected",
    "external_effect_issue_is_rejected",
    "external_theorem_without_ids_or_boundary_rejected",
    "initial_issue_trace_reaches_active_lease",
    "implemented_target_missing_module_or_build_rejected",
    "no_thin_proof_lease_classifier_recovers_boundary_state",
    "non_lean_artifact_cannot_claim_lean_proof",
    "non_operational_target_not_implemented",
    "proof_lease_accepted_step_adds_exactly_one_receipt",
    "proof_lease_custody_is_transitive",
    "proof_lease_rejected_event_is_noninterfering",
    "proof_lease_step_preserves_custody",
    "proof_lease_step_preserves_non_authority",
    "revocation_without_reason_is_rejected",
    "revoked_proof_lease_is_absorbing",
    "run_proof_lease_append",
    "run_proof_lease_preserves_custody",
    "run_proof_lease_preserves_non_authority",
    "stale_artifact_verification_is_rejected",
    "support_promotion_issue_is_rejected",
    "support_promotion_without_transition_or_boundaries_rejected",
    "thin_proof_lease_summary_has_issue_collision",
    "wrong_consumer_binding_is_rejected",
}

LIMITATION_MARKERS = [
    "does not prove",
    "does not implement",
    "does not evaluate",
    "do not prove",
    "do not claim",
    "not a proof",
    "not prove",
    "only the record-level",
    "scope is narrow",
    "finite-record",
    "finite record",
    "not the truth",
    "still require",
]

SECTION_END_RE = re.compile(r"^##\s+", re.MULTILINE)


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def root_imports() -> set[str]:
    imports: set[str] = set()
    for line in ROOT_LEAN_MODULE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.add(stripped.removeprefix("import ").strip())
    return imports


def formalization_section(text: str) -> str:
    match = re.search(r"^#{2,3}\s+Formalization hooks\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    rest = text[match.start() :]
    end = SECTION_END_RE.search(rest, pos=match.end() - match.start() + 1)
    return rest[: end.start()] if end else rest


def has_limitation_boundary(section: str) -> bool:
    lower = section.lower()
    return any(marker in lower for marker in LIMITATION_MARKERS)


def qmd_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def module_stats(module_path: Path) -> dict[str, int]:
    if not module_path.exists():
        return {"theorems": 0, "defs": 0, "structures": 0}
    text = module_path.read_text(encoding="utf-8", errors="ignore")
    return {
        "theorems": len(re.findall(r"\btheorem\s+", text)),
        "defs": len(re.findall(r"\bdef\s+", text)),
        "structures": len(re.findall(r"\bstructure\s+", text)),
    }


PROOF_LEASE_FIELDS = (
    "stage",
    "target_id",
    "proposition_version",
    "artifact_version",
    "verifier_version",
    "consumer_id",
    "implementation_version",
    "environment_version",
    "logical_time",
    "expiry_time",
    "artifact_valid",
    "adequacy_accepted",
    "consumer_requirements_matched",
    "limitations_recorded",
    "non_claims_recorded",
    "revocation_reason_present",
    "support_state_effect",
    "external_effect_authorized",
    "receipt_count",
)


def proof_lease_initial_state() -> dict[str, Any]:
    return {
        "stage": "registered",
        "target_id": 9001,
        "proposition_version": 7,
        "artifact_version": 1,
        "verifier_version": 3,
        "consumer_id": 42,
        "implementation_version": 11,
        "environment_version": 13,
        "logical_time": 0,
        "expiry_time": 10,
        "artifact_valid": True,
        "adequacy_accepted": True,
        "consumer_requirements_matched": True,
        "limitations_recorded": True,
        "non_claims_recorded": True,
        "revocation_reason_present": True,
        "support_state_effect": "noChange",
        "external_effect_authorized": False,
        "receipt_count": 0,
    }


def proof_lease_step(
    state: dict[str, Any], event: tuple[Any, ...]
) -> tuple[str, dict[str, Any]]:
    kind, *args = event
    next_state = copy.deepcopy(state)

    def accepted(stage: str) -> tuple[str, dict[str, Any]]:
        next_state["stage"] = stage
        next_state["receipt_count"] += 1
        return "accepted", next_state

    if kind == "verify":
        target_id, artifact_version, verifier_version = args
        if state["stage"] != "registered":
            return "rejectStage", state
        if (
            target_id != state["target_id"]
            or artifact_version != state["artifact_version"]
            or verifier_version != state["verifier_version"]
        ):
            return "rejectIdentity", state
        if not state["artifact_valid"]:
            return "rejectBoundary", state
        return accepted("verified")
    if kind == "adequacy":
        target_id, proposition_version = args
        if state["stage"] != "verified":
            return "rejectStage", state
        if (
            target_id != state["target_id"]
            or proposition_version != state["proposition_version"]
        ):
            return "rejectIdentity", state
        if not all(
            state[field]
            for field in (
                "adequacy_accepted",
                "limitations_recorded",
                "non_claims_recorded",
            )
        ):
            return "rejectBoundary", state
        return accepted("adequacyReviewed")
    if kind == "bind":
        (consumer_id,) = args
        if state["stage"] != "adequacyReviewed":
            return "rejectStage", state
        if consumer_id != state["consumer_id"]:
            return "rejectIdentity", state
        if not state["consumer_requirements_matched"]:
            return "rejectBoundary", state
        return accepted("consumerBound")
    if kind == "issue":
        consumer_id, implementation_version, environment_version = args
        if state["stage"] != "consumerBound":
            return "rejectStage", state
        if (
            consumer_id != state["consumer_id"]
            or implementation_version != state["implementation_version"]
            or environment_version != state["environment_version"]
        ):
            return "rejectIdentity", state
        if not all(
            state[field]
            for field in (
                "artifact_valid",
                "adequacy_accepted",
                "consumer_requirements_matched",
                "limitations_recorded",
                "non_claims_recorded",
            )
        ):
            return "rejectBoundary", state
        if state["expiry_time"] <= state["logical_time"]:
            return "rejectBoundary", state
        if (
            state["support_state_effect"] != "noChange"
            or state["external_effect_authorized"]
        ):
            return "rejectAuthority", state
        return accepted("active")
    if kind == "change":
        (new_artifact_version,) = args
        if state["stage"] != "active":
            return "rejectStage", state
        if new_artifact_version <= state["artifact_version"]:
            return "rejectVersion", state
        next_state["artifact_version"] = new_artifact_version
        return accepted("registered")
    if kind == "revoke":
        if state["stage"] != "active":
            return "rejectStage", state
        if not state["revocation_reason_present"]:
            return "rejectBoundary", state
        return accepted("revoked")
    if kind == "expire":
        if state["stage"] != "active":
            return "rejectStage", state
        if state["logical_time"] < state["expiry_time"]:
            return "rejectBoundary", state
        return accepted("expired")
    raise ValueError(f"unknown proof-lease event: {kind}")


def run_proof_lease(
    state: dict[str, Any], events: list[tuple[Any, ...]]
) -> dict[str, Any]:
    current = copy.deepcopy(state)
    for event in events:
        _, current = proof_lease_step(current, event)
    return current


def proof_lease_transport(state: dict[str, Any]) -> dict[str, Any]:
    return {field: copy.deepcopy(state[field]) for field in PROOF_LEASE_FIELDS}


def proof_lease_state_from_transport(transport: dict[str, Any]) -> dict[str, Any]:
    return {field: copy.deepcopy(transport[field]) for field in PROOF_LEASE_FIELDS}


def validate_proof_lease_lifecycle(errors: list[str]) -> dict[str, int]:
    source = PROOF_ENVELOPE.read_text(encoding="utf-8", errors="ignore")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_]+)", source))
    if theorem_names != REQUIRED_PROOF_ENVELOPE_THEOREMS:
        errors.append(
            "ProofEnvelope theorem surface drifted: "
            f"expected {EXPECTED_PROOF_ENVELOPE_THEOREM_COUNT}, got {len(theorem_names)}."
        )

    compile_result = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/ProofEnvelope.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if compile_result.returncode != 0:
        errors.append(
            "ProofEnvelope exact Lean compilation failed: "
            + (compile_result.stderr or compile_result.stdout).strip()
        )

    initial = proof_lease_initial_state()
    trace = [
        ("verify", 9001, 1, 3),
        ("adequacy", 9001, 7),
        ("bind", 42),
        ("issue", 42, 11, 13),
        ("change", 2),
        ("verify", 9001, 2, 3),
        ("adequacy", 9001, 7),
        ("bind", 42),
        ("issue", 42, 11, 13),
        ("revoke",),
    ]
    final = run_proof_lease(initial, trace)
    if not (
        final["stage"] == "revoked"
        and final["artifact_version"] == 2
        and final["receipt_count"] == 10
        and final["support_state_effect"] == "noChange"
        and final["external_effect_authorized"] is False
    ):
        errors.append("proof-lease complete reissue-and-revocation witness drifted")

    composition_split_count = 0
    for split in range(len(trace) + 1):
        if run_proof_lease(initial, trace) != run_proof_lease(
            run_proof_lease(initial, trace[:split]), trace[split:]
        ):
            errors.append(f"proof-lease composition failed at split {split}")
        composition_split_count += 1

    active = run_proof_lease(initial, trace[:4])
    reviewed = run_proof_lease(initial, trace[:2])
    verified = run_proof_lease(initial, trace[:1])
    issue_ready = copy.deepcopy(active)
    issue_ready["stage"] = "consumerBound"
    expired_active = copy.deepcopy(active)
    expired_active["logical_time"] = 10

    def changed(state: dict[str, Any], **updates: Any) -> dict[str, Any]:
        candidate = copy.deepcopy(state)
        candidate.update(updates)
        return candidate

    reject_cases = [
        (active, ("verify", 9001, 1, 3), "rejectStage"),
        (initial, ("verify", 9002, 1, 3), "rejectIdentity"),
        (initial, ("verify", 9001, 2, 3), "rejectIdentity"),
        (initial, ("verify", 9001, 1, 4), "rejectIdentity"),
        (changed(initial, artifact_valid=False), ("verify", 9001, 1, 3), "rejectBoundary"),
        (initial, ("adequacy", 9001, 7), "rejectStage"),
        (verified, ("adequacy", 9002, 7), "rejectIdentity"),
        (verified, ("adequacy", 9001, 8), "rejectIdentity"),
        (changed(verified, adequacy_accepted=False), ("adequacy", 9001, 7), "rejectBoundary"),
        (changed(verified, limitations_recorded=False), ("adequacy", 9001, 7), "rejectBoundary"),
        (changed(verified, non_claims_recorded=False), ("adequacy", 9001, 7), "rejectBoundary"),
        (verified, ("bind", 42), "rejectStage"),
        (reviewed, ("bind", 43), "rejectIdentity"),
        (changed(reviewed, consumer_requirements_matched=False), ("bind", 42), "rejectBoundary"),
        (reviewed, ("issue", 42, 11, 13), "rejectStage"),
        (issue_ready, ("issue", 43, 11, 13), "rejectIdentity"),
        (issue_ready, ("issue", 42, 12, 13), "rejectIdentity"),
        (issue_ready, ("issue", 42, 11, 14), "rejectIdentity"),
        (changed(issue_ready, artifact_valid=False), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, adequacy_accepted=False), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, consumer_requirements_matched=False), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, limitations_recorded=False), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, non_claims_recorded=False), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, logical_time=10), ("issue", 42, 11, 13), "rejectBoundary"),
        (changed(issue_ready, support_state_effect="supportPromotion"), ("issue", 42, 11, 13), "rejectAuthority"),
        (changed(issue_ready, external_effect_authorized=True), ("issue", 42, 11, 13), "rejectAuthority"),
        (issue_ready, ("change", 2), "rejectStage"),
        (active, ("change", 1), "rejectVersion"),
        (active, ("change", 0), "rejectVersion"),
        (issue_ready, ("revoke",), "rejectStage"),
        (changed(active, revocation_reason_present=False), ("revoke",), "rejectBoundary"),
        (issue_ready, ("expire",), "rejectStage"),
        (active, ("expire",), "rejectBoundary"),
    ]
    rejected_route_count = 0
    for index, (state, event, expected_route) in enumerate(reject_cases):
        route, after = proof_lease_step(state, event)
        if route != expected_route or after != state:
            errors.append(
                f"proof-lease rejecting case {index} drifted: {route}, state_changed={after != state}"
            )
        rejected_route_count += 1

    expire_route, expired = proof_lease_step(expired_active, ("expire",))
    if not (
        expire_route == "accepted"
        and expired["stage"] == "expired"
        and expired["receipt_count"] == expired_active["receipt_count"] + 1
    ):
        errors.append("proof-lease expiration witness drifted")

    thin_fields = ("target_id", "artifact_version", "consumer_id", "stage", "expiry_time")
    missing_non_claims = changed(issue_ready, non_claims_recorded=False)
    thin_ready = tuple(issue_ready[field] for field in thin_fields)
    thin_missing = tuple(missing_non_claims[field] for field in thin_fields)
    ready_route = proof_lease_step(issue_ready, ("issue", 42, 11, 13))[0]
    missing_route = proof_lease_step(missing_non_claims, ("issue", 42, 11, 13))[0]
    if not (
        issue_ready != missing_non_claims
        and thin_ready == thin_missing
        and ready_route == "accepted"
        and missing_route == "rejectBoundary"
    ):
        errors.append("proof-lease thin-summary collision drifted")

    transport = proof_lease_transport(final)
    if proof_lease_state_from_transport(transport) != final:
        errors.append("proof-lease complete transport failed to round-trip")
    transport_mutation_rejection_count = 0
    for field in PROOF_LEASE_FIELDS:
        mutation = copy.deepcopy(transport)
        value = mutation[field]
        if isinstance(value, bool):
            mutation[field] = not value
        elif isinstance(value, int):
            mutation[field] = value + 1
        else:
            mutation[field] = "active" if field == "stage" else "supportPromotion"
        if proof_lease_state_from_transport(mutation) == final:
            errors.append(f"proof-lease transport mutation escaped: {field}")
        transport_mutation_rejection_count += 1

    return {
        "theorem_count": len(theorem_names),
        "accepted_trace_event_count": len(trace),
        "composition_split_count": composition_split_count,
        "rejected_route_count": rejected_route_count,
        "thin_summary_collision_count": 1,
        "transport_mutation_rejection_count": transport_mutation_rejection_count,
        "expiration_witness_count": 1,
    }


def build_report() -> tuple[str, list[str]]:
    structure = read_json(STRUCTURE)
    manifest = read_json(MANIFEST)
    triage = read_json(TRIAGE)
    rationalization = read_json(RATIONALIZATION)

    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("records"), list):
        raise TypeError("proofs/proof_manifest.json must contain a records list")
    if not isinstance(triage, dict) or not isinstance(triage.get("records"), list):
        raise TypeError("proofs/proof_triage.json must contain a records list")
    if not isinstance(rationalization, dict) or not isinstance(rationalization.get("baseline_targets"), list):
        raise TypeError("proofs/proof_rationalization_registry.json must contain a baseline_targets list")

    records = [record for record in manifest["records"] if isinstance(record, dict)]
    triage_records = [record for record in triage["records"] if isinstance(record, dict)]
    rationalization_targets = {
        str(record.get("target_id", "")): record
        for record in rationalization["baseline_targets"]
        if isinstance(record, dict)
    }
    chapters = {chapter["id"]: chapter for chapter in flatten_chapters(structure)}
    imported_modules = root_imports()
    triage_by_tag = {record.get("tag"): record for record in triage_records}
    target_count = len(records)

    errors: list[str] = []
    warnings: list[str] = []
    target_rows: list[str] = []
    chapter_results: dict[str, dict[str, int]] = defaultdict(lambda: Counter())
    implemented_records = [record for record in records if record.get("status") == "implemented"]
    module_target_counts = Counter(str(record.get("module_path", "")) for record in implemented_records)
    module_target_tags: dict[str, list[str]] = defaultdict(list)
    for record in implemented_records:
        module_target_tags[str(record.get("module_path", ""))].append(str(record.get("tag", "")))
    module_rows: list[str] = []

    proof_envelope_text = PROOF_ENVELOPE.read_text(encoding="utf-8", errors="ignore")
    for theorem in sorted(REQUIRED_PROOF_ENVELOPE_THEOREMS):
        if f"theorem {theorem}" not in proof_envelope_text:
            errors.append(
                f"{PROOF_ENVELOPE.relative_to(ROOT)} is missing retained theorem {theorem}."
            )
    proof_lease_metrics = validate_proof_lease_lifecycle(errors)

    duplicate_tags = [tag for tag, count in Counter(record.get("tag") for record in records).items() if count > 1]
    for tag in sorted(str(tag) for tag in duplicate_tags):
        errors.append(f"Duplicate proof target tag: {tag}")

    appendix_text = APPENDIX_E.read_text(encoding="utf-8", errors="ignore") if APPENDIX_E.exists() else ""
    if str(target_count) not in appendix_text:
        errors.append(f"Appendix E does not mention the current proof target count {target_count}.")
    if "Proof-readiness validation" not in appendix_text:
        errors.append("Appendix E is missing the Proof-readiness validation repository-level check.")
    if "Proof artifact traceability audit" not in appendix_text:
        errors.append("Appendix E is missing the Proof artifact traceability audit repository-level check.")
    if "Proof target coverage summary" not in appendix_text:
        errors.append("Appendix E is missing the Proof target coverage summary repository-level check.")

    for module_path_str, count in sorted(module_target_counts.items()):
        module_path = ROOT / module_path_str
        stats = module_stats(module_path)
        if not module_path.exists():
            errors.append(f"{module_path_str}: referenced Lean module file is missing.")
        rationalized_count = 0
        if stats["theorems"] < count:
            for tag in module_target_tags[module_path_str]:
                review = rationalization_targets.get(tag, {})
                replacement_refs = set(review.get("replacement_refs", []))
                if (
                    review.get("review_state") in {"semantically_reviewed", "terminally_dispositioned"}
                    and review.get("disposition")
                    in {"retain_refinement_or_executable_bridge", "replace_with_stronger_model"}
                    and module_path_str in replacement_refs
                ):
                    rationalized_count += 1
            if rationalized_count != count:
                errors.append(
                    f"{module_path_str}: has {stats['theorems']} theorem declarations for {count} proof targets, "
                    f"but only {rationalized_count} targets have reviewed consolidation lineage to the module."
                )
        module_rows.append(
            f"| `{qmd_escape(module_path_str)}` | {count} | {stats['theorems']} | {rationalized_count} | {stats['defs']} | {stats['structures']} |"
        )

    for record in records:
        tag = str(record.get("tag", ""))
        chapter_id = str(record.get("chapter_id", ""))
        module = str(record.get("module", ""))
        module_path = ROOT / str(record.get("module_path", ""))
        status = str(record.get("status", ""))
        chapter = chapters.get(chapter_id)
        trace_bits: list[str] = []

        if not tag.startswith("lean:"):
            errors.append(f"{tag}: proof tag must start with lean:")

        triage_record = triage_by_tag.get(tag)
        if triage_record is None:
            errors.append(f"{tag}: missing proof triage record.")
            trace_bits.append("triage missing")
        else:
            for field in ("chapter_id", "module", "formal_target"):
                if triage_record.get(field) != record.get(field):
                    errors.append(f"{tag}: triage {field} does not match manifest.")
            if triage_record.get("target_status") != status:
                errors.append(f"{tag}: triage target_status does not match manifest status.")
            trace_bits.append("triage ok")

        if status == "implemented":
            if not module_path.exists():
                errors.append(f"{tag}: implemented target missing {record.get('module_path')}.")
            elif module != "AsiStackProofs" and module not in imported_modules:
                errors.append(f"{tag}: implemented module {module} is not imported by lean/AsiStackProofs.lean.")
            else:
                trace_bits.append("module ok")

        if chapter is None:
            errors.append(f"{tag}: chapter {chapter_id!r} is missing from book_structure.json.")
            target_rows.append(f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | missing chapter |")
            continue

        chapter_path = ROOT / str(chapter.get("file", ""))
        if not chapter_path.exists():
            errors.append(f"{tag}: chapter file {chapter.get('file')} is missing.")
            target_rows.append(f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | missing chapter file |")
            continue

        chapter_text = chapter_path.read_text(encoding="utf-8", errors="ignore")
        section = formalization_section(chapter_text)
        if tag not in chapter_text:
            errors.append(f"{tag}: tag missing from chapter file {chapter.get('file')}.")
            chapter_results[chapter_id]["missing_tag"] += 1
        else:
            chapter_results[chapter_id]["tag_present"] += 1
            trace_bits.append("chapter tag ok")
        if status == "implemented":
            if not section:
                errors.append(f"{tag}: chapter {chapter_id} has no Formalization hooks section.")
                chapter_results[chapter_id]["missing_section"] += 1
            elif not has_limitation_boundary(section):
                errors.append(f"{tag}: chapter {chapter_id} formalization section lacks an explicit limitation/non-claim boundary.")
                chapter_results[chapter_id]["missing_limitation"] += 1
            else:
                chapter_results[chapter_id]["limitation_present"] += 1
                trace_bits.append("limitation ok")
        else:
            trace_bits.append(f"{status} target; module and formalization implementation checks deferred")

        target_rows.append(
            f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | {qmd_escape('; '.join(trace_bits))} |"
        )

    chapter_rows = []
    for chapter_id in sorted(chapter_results):
        result = chapter_results[chapter_id]
        chapter_rows.append(
            f"| `{qmd_escape(chapter_id)}` | {result['tag_present']} | {result['limitation_present']} | {result['missing_tag']} | {result['missing_limitation']} |"
        )

    status_counts = Counter(str(record.get("status", "missing")) for record in records)
    triage_counts = Counter(str(record.get("triage", "missing")) for record in triage_records)
    summary_rows = [
        f"| Proof targets audited | {target_count} |",
        f"| Manifest status counts | {qmd_escape(json.dumps(dict(sorted(status_counts.items()))))} |",
        f"| Triage class counts | {qmd_escape(json.dumps(dict(sorted(triage_counts.items()))))} |",
        f"| Lean modules referenced | {len(module_target_counts)} |",
        f"| Chapters with proof targets | {len(chapter_results)} |",
        f"| Validation errors | {len(errors)} |",
        f"| Warnings | {len(warnings)} |",
        f"| ProofEnvelope theorem declarations | {proof_lease_metrics['theorem_count']} |",
        f"| Proof-lease accepted trace events | {proof_lease_metrics['accepted_trace_event_count']} |",
        f"| Proof-lease composition splits | {proof_lease_metrics['composition_split_count']} |",
        f"| Proof-lease rejecting route cases | {proof_lease_metrics['rejected_route_count']} |",
        f"| Proof-lease thin-summary collisions | {proof_lease_metrics['thin_summary_collision_count']} |",
        f"| Proof-lease complete-transport mutations rejected | {proof_lease_metrics['transport_mutation_rejection_count']} |",
    ]

    error_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."
    warning_text = "\n".join(f"- {qmd_escape(warning)}" for warning in warnings) if warnings else "- None."

    report = f"""# Proof Artifact Audit

Generated by `python3 scripts/validate_proof_artifact_audit.py --write`.

This report audits traceability for implemented proof targets. It checks that the generated manifest, proof triage, Lean module files, root Lean imports, chapter formalization-hook tables, and chapter limitation/non-claim prose stay aligned.

It does **not** prove semantic adequacy, source interpretation, model quality, deployed enforcement, benchmark results, external theorem validity, or broad ASI Stack behavior. A passing audit means the proof artifacts are traceable and explicitly bounded.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Checked Boundaries

- Every manifest tag must have a matching proof-triage record with the same chapter, module, target, and status.
- Every implemented target must reference an existing Lean module imported by `lean/AsiStackProofs.lean`.
- Each referenced Lean module must contain at least as many theorem declarations as implemented targets assigned to that module, unless every consolidated target has a semantically reviewed rationalization record that points to the stronger current module.
- Every implemented target tag must appear in its chapter file.
- Every chapter formalization-hook section with implemented targets must include explicit limitation or non-claim language.
- Appendix E must expose the current proof target count, proof-readiness coverage boundary, and proof artifact traceability audit.
- The exact 28-declaration `ProofEnvelope` module must compile, and the independent consumer must reproduce the ten-event artifact-change/reissue/revocation trace, all eleven composition splits, 33 rejecting routes with exact state preservation, one expiration witness, one thin-summary/opposite-decision collision, and all nineteen complete-transport mutations.

## Proof-Envelope Lifecycle Alignment

The independent consumer reconstructs a formal-artifact authority lease without
copying Lean outcomes. It requires exact target, proposition, artifact,
verifier, consumer, implementation, and environment identity; adequacy,
limitation, non-claim, and consumer-boundary review; unexpired least-authority
issuance; artifact-change invalidation and re-review; and explicit revocation or
expiry. The checked finite trace changes artifact version once, reissues only
after repeating verification and review, then revokes with ten receipts.

This alignment proves no theorem meaning, filesystem truth, semantic adequacy,
implementation refinement, deployed enforcement, support movement, external
effect, safety, transfer, SOTA, AGI, or ASI.

## Module Coverage

| Lean module path | Targets | Theorems | Rationalized targets | Defs | Structures |
|---|---:|---:|---:|---:|---:|
{chr(10).join(module_rows)}

## Chapter Coverage

| Chapter ID | Tags present | Limitation references | Missing tags | Missing limitation references |
|---|---:|---:|---:|---:|
{chr(10).join(chapter_rows)}

## Target Trace

| Tag | Chapter ID | Lean module | Trace status |
|---|---|---|---|
{chr(10).join(target_rows)}

## Validation Errors

{error_text}

## Warnings

{warning_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/proof_artifact_audit.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Proof artifact audit failed: {exc}")
        sys.exit(1)

    if args.write:
        REPORT.write_text(report, encoding="utf-8")
    elif not REPORT.exists():
        print(f"{REPORT.relative_to(ROOT)} is missing; run scripts/validate_proof_artifact_audit.py --write")
        sys.exit(1)
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; run scripts/validate_proof_artifact_audit.py --write")
            sys.exit(1)

    if errors:
        print("Proof artifact audit failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    action = "wrote" if args.write else "validated"
    print(f"Proof artifact audit {action}: {len(read_json(MANIFEST)['records'])} targets.")


if __name__ == "__main__":
    main()
