#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "proof_contract_receipt_record.schema.json"
VALID_DIR = ROOT / "experiments" / "circle_public_replay" / "fixtures" / "valid"
INVALID_DIR = ROOT / "experiments" / "circle_public_replay" / "fixtures" / "invalid"
RESULT = ROOT / "experiments" / "circle_public_replay" / "results" / "2026-06-29-local.json"
SUMMARY = ROOT / "docs" / "circle_public_replay_consumer_gate.md"

EXPECTED_RECEIPT_ID = "circle.rope.CC-AI-CONTRACT-ROPE-001.public_consumer_gate"
EXPECTED_CONTENT_FINGERPRINT = "a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468"
REQUIRED_THEOREMS = {
    "AIRA-T0058",
    "AIRA-T0059",
    "AIRA-T0171",
    "AIRA-T0172",
    "AIRA-T0239",
    "AIRA-T0240",
    "AIRA-T0241",
}
REQUIRED_FIELD_FRAGMENTS = (
    "d19_proved_request_status=proved",
    "d19_proved_first_channel_bank_transfer=true",
    "real_phase_dirichlet_witness_guardrail=true",
    "receipt_content_fingerprint=91b72a6dcf821a9733f21800cd1093a3d0665588022031ba72c94893800330c3",
    "normalized_request_fingerprint=20e68c5f787e267c6611bc57b8d8e98e1cb0f5a74f272379716a5d83e761407d",
    "contract_pack_fingerprint=df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint=a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468",
    "ROPE-USE-D19-MARGIN-FRONTIER",
)
REQUIRED_BLOCKED_USES = (
    "chapter-core claim promotion",
    "model-quality promotion",
    "runtime promotion",
    "context-length promotion",
    "deployment-readiness claim",
    "transfer claim",
    "ASI claim",
)
FORBIDDEN_ALLOWED_USE_FRAGMENTS = (
    "chapter-core",
    "model-quality",
    "runtime promotion",
    "context-length",
    "deployment",
    "transfer claim",
    "ASI claim",
)
REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not prove model quality, reasoning ability, context length, speed, memory scaling, deployment safety, transfer, or ASI",
    "does not prove deployed proof-contract transport inside The ASI Stack",
    "does not create a new accepted support-state transition",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Circle public consumer-gate validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def set_path(value: dict[str, Any], path: str, new_value: Any) -> None:
    cursor: Any = value
    parts = path.split(".")
    for part in parts[:-1]:
        if not isinstance(cursor, dict) or part not in cursor:
            raise KeyError(path)
        cursor = cursor[part]
    if not isinstance(cursor, dict):
        raise KeyError(path)
    cursor[parts[-1]] = new_value


def validate_non_claims(owner: str, non_claims: Any, errors: list[str]) -> None:
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def validate_receipt(receipt: dict[str, Any], schema: dict[str, Any], owner: str) -> list[str]:
    errors = validate_value(receipt, schema, owner)
    if errors:
        return errors

    expected = {
        "receipt_id": EXPECTED_RECEIPT_ID,
        "receipt_state": "consumer_gated",
        "source_project": "Circle Calculus",
        "contract_family": "rope_position_distinguishability",
        "engineering_object": "CC-AI-CONTRACT-ROPE-001",
        "proof_status": "external_resolved",
        "content_fingerprint": EXPECTED_CONTENT_FINGERPRINT,
        "fingerprint_status": "computed",
        "verifier_command": "python3 scripts/validate_circle_public_replay.py",
        "verifier_result": "pass",
        "resolver_status": "resolved_external",
        "replay_status": "replayed",
        "consumer_state": "eligible_for_downstream_review",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for key, expected_value in expected.items():
        if receipt.get(key) != expected_value:
            errors.append(f"{owner}: {key} must be {expected_value!r}.")

    if "63b0f511" not in str(receipt.get("source_version", "")):
        errors.append(f"{owner}: source_version must reference Circle commit 63b0f511.")

    theorem_refs = receipt.get("theorem_refs", [])
    if set(theorem_refs) != REQUIRED_THEOREMS or len(theorem_refs) != len(REQUIRED_THEOREMS):
        errors.append(f"{owner}: theorem set does not match required Circle theorem IDs.")

    field_blob = text_blob(receipt.get("deterministic_fields", []))
    for fragment in REQUIRED_FIELD_FRAGMENTS:
        if fragment not in field_blob:
            errors.append(f"{owner}: deterministic_fields missing {fragment!r}.")

    proof_boundary = str(receipt.get("proof_boundary", ""))
    for fragment in ("does not rerun Circle Lean", "does not convert proof-contract legality"):
        if fragment not in proof_boundary:
            errors.append(f"{owner}: proof_boundary missing {fragment!r}.")

    consumer_gate = receipt.get("consumer_gate", {})
    allowed = text_blob(consumer_gate.get("allowed_uses", []) if isinstance(consumer_gate, dict) else [])
    blocked = text_blob(consumer_gate.get("blocked_uses", []) if isinstance(consumer_gate, dict) else [])
    downstream = text_blob(consumer_gate.get("required_downstream_evidence", []) if isinstance(consumer_gate, dict) else [])
    for fragment in FORBIDDEN_ALLOWED_USE_FRAGMENTS:
        if fragment in allowed:
            errors.append(f"{owner}: allowed_uses must not contain blocked promotion language {fragment!r}.")
    for blocked_use in REQUIRED_BLOCKED_USES:
        if blocked_use not in blocked:
            errors.append(f"{owner}: blocked_uses missing {blocked_use!r}.")
    for phrase in (
        "workload, baseline, metric, and report",
        "fresh Circle replay",
        "accepted evidence-transition record",
        "deployed ASI proof-contract transport",
    ):
        if phrase not in downstream:
            errors.append(f"{owner}: required_downstream_evidence missing {phrase!r}.")

    source_refs = text_blob(receipt.get("source_refs", []))
    evidence_refs = text_blob(receipt.get("evidence_refs", []))
    for ref in (
        "docs/circle_external_receipt_slice.md",
        "experiments/circle_external_receipt_slice/results/2026-06-29-local.json",
        "evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json",
    ):
        if ref not in source_refs:
            errors.append(f"{owner}: source_refs missing {ref}.")
    for ref in (
        "experiments/circle_public_replay/results/2026-06-29-local.json",
        "scripts/validate_circle_public_replay.py",
    ):
        if ref not in evidence_refs:
            errors.append(f"{owner}: evidence_refs missing {ref}.")

    validate_non_claims(owner, receipt.get("non_claims"), errors)
    return errors


def validate_invalid_fixture(path: Path, schema: dict[str, Any], errors: list[str]) -> None:
    spec = load_json(path)
    owner = rel(path)
    if not isinstance(spec, dict):
        errors.append(f"{owner}: expected object.")
        return
    for key in ("case_id", "base_receipt", "mutation", "expected_error_fragment"):
        if key not in spec:
            errors.append(f"{owner}: missing {key}.")
            return
    base_path = ROOT / str(spec["base_receipt"])
    if not base_path.exists():
        errors.append(f"{owner}: base_receipt does not exist.")
        return
    receipt = load_json(base_path)
    if not isinstance(receipt, dict):
        errors.append(f"{owner}: base_receipt must contain object.")
        return
    mutation = spec["mutation"]
    if not isinstance(mutation, dict) or not isinstance(mutation.get("path"), str) or "value" not in mutation:
        errors.append(f"{owner}: mutation must contain path and value.")
        return
    mutated = copy.deepcopy(receipt)
    try:
        set_path(mutated, mutation["path"], mutation["value"])
    except KeyError:
        errors.append(f"{owner}: mutation path {mutation['path']!r} does not exist.")
        return
    observed_errors = validate_receipt(mutated, schema, owner)
    if not observed_errors:
        errors.append(f"{owner}: expected invalid mutation passed validation.")
        return
    expected_fragment = str(spec["expected_error_fragment"])
    if expected_fragment not in "\n".join(observed_errors):
        errors.append(f"{owner}: expected error fragment {expected_fragment!r}; got {observed_errors}.")


def validate_result(expected: dict[str, Any], errors: list[str]) -> None:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain an object.")
        return
    for key, expected_value in expected.items():
        if result.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    validate_non_claims(rel(RESULT), result.get("non_claims"), errors)


def validate_summary(expected_digest: str, errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required = (
        "Circle Public Consumer Gate",
        EXPECTED_RECEIPT_ID,
        EXPECTED_CONTENT_FINGERPRINT,
        expected_digest,
        "63b0f511",
        "CC-AI-CONTRACT-ROPE-001",
        "AIRA-T0058",
        "AIRA-T0241",
        "ROPE-USE-D19-MARGIN-FRONTIER",
        "digest mismatch",
        "unsupported transfer-claim use",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove deployed proof-contract transport inside The ASI Stack.",
        "python3 scripts/validate_circle_public_replay.py",
    )
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    schema = load_json(SCHEMA)
    valid_paths = sorted(VALID_DIR.glob("*.valid.json"))
    invalid_paths = sorted(INVALID_DIR.glob("*.invalid.json"))
    errors: list[str] = []

    if len(valid_paths) != 1:
        errors.append(f"{rel(VALID_DIR)} must contain exactly one valid receipt fixture.")
    if len(invalid_paths) != 4:
        errors.append(f"{rel(INVALID_DIR)} must contain exactly four expected-invalid mutation fixtures.")

    receipt_digest = ""
    for path in valid_paths:
        value = load_json(path)
        if not isinstance(value, dict):
            errors.append(f"{rel(path)} must contain an object.")
            continue
        receipt_errors = validate_receipt(value, schema, rel(path))
        errors.extend(receipt_errors)
        if not receipt_errors:
            receipt_digest = stable_hash(value)

    for path in invalid_paths:
        validate_invalid_fixture(path, schema, errors)

    if receipt_digest:
        expected_result = {
            "schema_version": "0.1",
            "result_id": "2026-06-29-circle-public-consumer-gate",
            "slice_id": "circle_public_replay_consumer_gate",
            "validation_result": "pass",
            "accepted_receipt_id": EXPECTED_RECEIPT_ID,
            "accepted_public_receipt_sha256": receipt_digest,
            "contract_content_fingerprint": EXPECTED_CONTENT_FINGERPRINT,
            "valid_receipt_count": len(valid_paths),
            "expected_invalid_count": len(invalid_paths),
            "required_theorem_count": len(REQUIRED_THEOREMS),
            "support_state_effect": "eligible_for_bounded_evidence_review",
            "ci_verification_command": "python3 scripts/validate_circle_public_replay.py",
        }
        validate_result(expected_result, errors)
        validate_summary(receipt_digest, errors)

    if errors:
        fail(errors)

    print(
        "Circle public consumer-gate validation passed: "
        f"{len(valid_paths)} valid receipt, {len(invalid_paths)} expected-invalid controls, "
        f"digest {receipt_digest}."
    )


if __name__ == "__main__":
    main()
