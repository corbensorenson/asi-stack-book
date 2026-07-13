"""QI-12: content-addressed descendant manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .canonical import ContractError, make_envelope


ROOT = Path(__file__).resolve().parents[3]


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(paths_by_kind: dict[str, list[str]], input_digests: list[str]) -> dict:
    required = {"code", "schemas", "fixtures", "corpora", "seeds", "configs", "results", "logs", "environment"}
    if set(paths_by_kind) != required:
        raise ContractError("artifact manifest category set incomplete")
    payload: dict[str, object] = {}
    missing = []
    for kind in sorted(required):
        rows = []
        for relative in sorted(paths_by_kind[kind]):
            path = ROOT / relative
            if not path.is_file():
                missing.append(relative)
            else:
                rows.append({"path": relative, "sha256": file_digest(path), "bytes": path.stat().st_size})
        payload[kind] = rows
    payload["missing_descendants"] = missing
    payload["mutated_descendants"] = []
    if missing:
        raise ContractError("artifact manifest has missing descendants")
    return make_envelope(
        "QI-12", "manifest:qcsa-reference-implementation", ["integrated-reference-architecture"], payload,
        input_digests=input_digests,
        non_claim_boundary="Content and presence integrity for the bounded local bundle only; no semantic adequacy or supply-chain trust claim.",
    )


def verify(artifact: dict) -> None:
    mutated = []
    missing = []
    for kind in ("code", "schemas", "fixtures", "corpora", "seeds", "configs", "results", "logs", "environment"):
        for row in artifact["payload"][kind]:
            path = ROOT / row["path"]
            if not path.is_file():
                missing.append(row["path"])
            elif file_digest(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
                mutated.append(row["path"])
    if missing or mutated:
        raise ContractError(f"manifest descendants invalid: missing={missing}, mutated={mutated}")
