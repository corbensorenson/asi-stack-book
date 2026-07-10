#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "sandboxed_adapter_capability_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "sandboxed_adapter_capability_record.valid.json"
MUTATIONS = ROOT / "experiments" / "sandboxed_adapter_capability" / "fixtures"
EXPECTED_SOURCES = {"moecot_manifest_project", "beastbrain_project", "bugbrain_project", "corbens_trainer_project", "corbens_best_model_possible_project"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def under(value: str, prefixes: list[str]) -> bool:
    return any(value == prefix or value.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("sandboxed-adapter lineage must name the five historical-project sources exactly")
    identity = record.get("adapter_identity", {})
    envelope = record.get("capability_envelope", {})
    executable = identity.get("executable_path", "")
    if executable not in envelope.get("executable_allowlist", []):
        errors.append("adapter executable must be present in the exact executable allowlist")
    network = envelope.get("network", {})
    if network.get("mode") == "denied" and network.get("allowed_endpoints"):
        errors.append("denied network mode cannot retain allowed endpoints")
    if network.get("mode") == "allowlist" and not network.get("allowed_endpoints"):
        errors.append("allowlist network mode requires at least one endpoint")

    for probe in record.get("enforcement_observation", {}).get("probe_results", []):
        kind = probe.get("probe")
        value = probe.get("requested_value", "")
        allowed = probe.get("allowed")
        if kind == "executable" and allowed != (value in envelope.get("executable_allowlist", [])):
            errors.append("executable probe result must match the declared allowlist")
        elif kind == "read_path" and allowed != under(value, envelope.get("read_path_prefixes", [])):
            errors.append("read-path probe result must match the declared prefixes")
        elif kind == "write_path" and allowed != under(value, envelope.get("write_path_prefixes", [])):
            errors.append("write-path probe result must match the declared prefixes")
        elif kind == "network":
            expected = network.get("mode") == "unrestricted" or (network.get("mode") == "allowlist" and value in network.get("allowed_endpoints", []))
            if allowed != expected:
                errors.append("network probe result must match denied, allowlist, or unrestricted scope")
        elif kind == "clock":
            expected = envelope.get("clock") == "wall_clock" or (envelope.get("clock") == "monotonic_only" and value == "monotonic")
            if allowed != expected:
                errors.append("clock probe result must match the declared clock scope")
        elif kind == "randomness":
            expected = envelope.get("randomness") == "os_random" or (envelope.get("randomness") == "deterministic_seeded" and value.startswith("seed:"))
            if allowed != expected:
                errors.append("randomness probe result must match the declared randomness scope")

    observation = record.get("enforcement_observation", {})
    if observation.get("claim") != "os_enforced_observed" and observation.get("os_enforcement_claim_allowed"):
        errors.append("declared, simulated, or process-observed policy cannot claim OS enforcement")
    if observation.get("claim") == "os_enforced_observed" and not observation.get("sandbox_instance_ref"):
        errors.append("OS-enforced observation requires a sandbox instance reference")

    replay = record.get("replay_grade", {})
    if replay.get("grade") == "record_playback":
        if not replay.get("playback_only") or replay.get("effect_reobserved") or replay.get("rollback_reobserved"):
            errors.append("record playback cannot be described as live effect or rollback reobservation")
    if replay.get("grade") in {"bounded_live_reexecution", "deployed_live_reexecution"}:
        if replay.get("playback_only") or not replay.get("same_inputs") or not replay.get("effect_reobserved"):
            errors.append("live reexecution requires same inputs and a reobserved effect rather than playback")
    if replay.get("grade") == "deployed_live_reexecution" and (not replay.get("same_executable_digest") or observation.get("claim") != "os_enforced_observed"):
        errors.append("deployed live reexecution requires executable-digest parity and observed OS enforcement")

    residuals = record.get("irreversible_residuals", {})
    if residuals.get("state") == "none_observed_in_bounded_probe" and residuals.get("items"):
        errors.append("none-observed residual state must carry an empty item list")
    if residuals.get("state") == "present" and not residuals.get("items"):
        errors.append("present irreversible residuals require named items")
    decision = record.get("decision", {})
    if observation.get("claim") != "os_enforced_observed" and decision.get("sandbox_claim_allowed"):
        errors.append("sandbox claim must remain blocked without observed OS enforcement")
    if decision.get("state") == "bounded_probe_only" and decision.get("ordinary_dispatch_allowed"):
        errors.append("bounded probe record cannot authorize ordinary dispatch")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored sandbox capability fixtures cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("sandbox capability record must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    target[mutation["path"][-1]] = mutation["value"]
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid sandboxed-adapter capability record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No sandboxed-adapter capability mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"Sandboxed-adapter capability harness passed: 1 bounded five-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
