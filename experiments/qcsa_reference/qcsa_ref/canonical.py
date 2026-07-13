"""Canonical JSON and shared QCSA artifact-envelope behavior."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


LANES = tuple(f"QI-{index:02d}" for index in range(1, 13))
OPAQUE_ID = re.compile(r"^qa:[0-9a-f]{16}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")


class ContractError(ValueError):
    """Raised when a QCSA contract must fail closed."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def artifact_id(namespace: str) -> str:
    return "qa:" + hashlib.sha256(namespace.encode("utf-8")).hexdigest()[:16]


def body_digest(artifact: dict[str, Any]) -> str:
    body = {key: value for key, value in artifact.items() if key != "content_digest"}
    return sha256(body)


def make_envelope(
    lane_id: str,
    namespace: str,
    owners: list[str],
    payload: dict[str, Any],
    *,
    input_digests: list[str] | None = None,
    non_claim_boundary: str,
) -> dict[str, Any]:
    artifact = {
        "schema_version": "asi_stack.qcsa_reference_artifact.v0",
        "lane_id": lane_id,
        "artifact_id": artifact_id(namespace),
        "artifact_version": "0.1.0",
        "owner_chapters": owners,
        "created_by": "qcsa_ref",
        "input_digests": sorted(set(input_digests or [])),
        "payload": payload,
        "non_claim_boundary": non_claim_boundary,
    }
    artifact["content_digest"] = body_digest(artifact)
    verify_envelope(artifact)
    return artifact


def verify_envelope(artifact: dict[str, Any]) -> None:
    required = {
        "schema_version", "lane_id", "artifact_id", "artifact_version",
        "owner_chapters", "created_by", "input_digests", "payload",
        "non_claim_boundary", "content_digest",
    }
    if set(artifact) != required:
        raise ContractError(f"artifact envelope fields differ: {sorted(set(artifact) ^ required)}")
    if artifact["schema_version"] != "asi_stack.qcsa_reference_artifact.v0":
        raise ContractError("unsupported artifact schema version")
    if artifact["lane_id"] not in LANES:
        raise ContractError("unknown QCSA lane")
    if not OPAQUE_ID.fullmatch(artifact["artifact_id"]):
        raise ContractError("artifact identity is not opaque")
    if not artifact["owner_chapters"] or len(artifact["owner_chapters"]) != len(set(artifact["owner_chapters"])):
        raise ContractError("artifact must have distinct owners")
    if artifact["created_by"] not in {"fixture", "qcsa_ref"}:
        raise ContractError("unsupported artifact creator")
    if not isinstance(artifact["payload"], dict):
        raise ContractError("artifact payload must be an object")
    if len(artifact["non_claim_boundary"]) < 40:
        raise ContractError("artifact non-claim boundary is inadequate")
    if any(not DIGEST.fullmatch(value) for value in artifact["input_digests"]):
        raise ContractError("input digest is malformed")
    if not DIGEST.fullmatch(artifact["content_digest"]):
        raise ContractError("content digest is malformed")
    if artifact["content_digest"] != body_digest(artifact):
        raise ContractError("content digest mismatch")
