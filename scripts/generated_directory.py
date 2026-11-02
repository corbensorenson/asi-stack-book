"""Install an already inspected generated payload as one complete directory.

Ownership is a family marker plus exact file integrity, not authorship or
release attestation. Source acquisition and domain acceptance stay with the
caller. This shares the existing tested-bundle locking/exchange primitives.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Callable

from build_tested_site_bundle import bundle_lock, exchange_directories, install_directory_noreplace, file_rows, sync_directory, sync_stage, tree_sha256
from projection_files import ProjectionFiles

RECEIPT = "projection-install-manifest.json"
VERSION = "asi_stack.generated_directory_install.v1"


def ordinary(path: Path) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"generated directory must not traverse a symlink: {path}")


def relative(value: str) -> str:
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or path.as_posix() != value or ".." in path.parts
            or "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value)
            or path == PurePosixPath(".")):
        raise ValueError(f"invalid generated payload path: {value!r}")
    return value


def desired_receipt(family: str, payload: dict[str, bytes], inputs: dict[str, str | None]) -> dict:
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", family):
        raise ValueError("invalid generated-directory family")
    if RECEIPT in payload or not payload:
        raise ValueError("generated payload is empty or collides with the installation receipt")
    rows = []
    names = set(payload)
    for name, data in sorted(payload.items()):
        relative(name)
        if any(parent.as_posix() in names for parent in PurePosixPath(name).parents if parent != PurePosixPath(".")):
            raise ValueError("generated file paths collide with parent files")
        if not isinstance(data, bytes):
            raise ValueError("generated payload must contain inspected bytes")
        rows.append({"path": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    for name, digest in inputs.items():
        relative(name)
        if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest)):
            raise ValueError("generated input identity must contain SHA-256 digests or explicit absence")
    return {"schema_version": VERSION, "family": family, "input_sha256": dict(inputs),
            "files": rows, "payload_tree_sha256": tree_sha256(rows),
            "support_state_effect": "none", "release_effect": "none"}


def payload_rows(output: Path) -> list[dict]:
    return [row for row in file_rows(output) if row["path"] != RECEIPT]


def previous_is_owned(output: Path, desired: dict) -> bool:
    ordinary(output)
    if not output.exists():
        return False
    rows = payload_rows(output)
    marker = output / RECEIPT
    if marker.is_file():
        prior = json.loads(marker.read_bytes())
        if (not isinstance(prior, dict) or set(prior) != set(desired)
                or prior.get("schema_version") != VERSION or prior.get("family") != desired["family"]
                or prior.get("support_state_effect") != "none" or prior.get("release_effect") != "none"
                or prior.get("files") != rows or prior.get("payload_tree_sha256") != tree_sha256(rows)
                or not isinstance(prior.get("input_sha256"), dict)):
            raise ValueError("previous generated directory failed ownership/integrity checks; preserve it")
        if any(type(row["size"]) is not int for row in prior["files"]):
            raise ValueError("previous generated inventory has invalid byte-count types")
        # Check the prior identity's shape without requiring it to be current:
        # a valid older projection must remain eligible for a real update.
        desired_receipt(prior["family"], {row["path"]: b"shape-only" for row in rows}, prior["input_sha256"])
    elif rows != desired["files"]:
        raise ValueError("legacy generated directory is not an exact current payload; preserve it and use a fresh output")
    return True


def install(output: Path, *, family: str, payload: dict[str, bytes], inputs: dict[str, str | None],
            guard: Callable[[], None], check: bool = False, lock_root: Path | None = None,
            accept_previous: Callable[[Path], None] | None = None) -> dict:
    ordinary(output)
    payload = dict(payload)
    inputs = dict(inputs)
    output = output.resolve()
    lock_root = output if lock_root is None else lock_root
    ordinary(lock_root)
    lock_root = lock_root.resolve()
    desired = desired_receipt(family, payload, inputs)
    guard()
    if check:
        if previous_is_owned(output, desired) and accept_previous is not None:
            accept_previous(output)
        if not (output / RECEIPT).is_file() or json.loads((output / RECEIPT).read_bytes()) != desired:
            raise ValueError("generated directory is stale or unreceipted; rebuild this family")
        guard()
        ordinary(output)
        if payload_rows(output) != desired["files"] or json.loads((output / RECEIPT).read_bytes()) != desired:
            raise ValueError("generated directory changed during its read-only check")
        return desired
    # Parent creation happens only after the caller's input/path inspection.
    output.parent.mkdir(parents=True, exist_ok=True)
    lock_root.parent.mkdir(parents=True, exist_ok=True)
    with bundle_lock(lock_root):
        before = file_rows(output) if output.exists() else None
        existed = previous_is_owned(output, desired)
        if existed and accept_previous is not None:
            # Family integrity is established first. Domain owners may then
            # forbid replacing another version or an already published object.
            accept_previous(output)
        if (file_rows(output) if output.exists() else None) != before:
            raise ValueError("generated directory changed during ownership inspection")
        if existed and (output / RECEIPT).is_file() and json.loads((output / RECEIPT).read_bytes()) == desired:
            guard()
            if (file_rows(output) != before
                    or [row for row in before if row["path"] != RECEIPT] != desired["files"]):
                raise ValueError("generated directory changed during no-op installation")
            return desired
        container = Path(tempfile.mkdtemp(prefix=f".{lock_root.name}-{family}-stage-", dir=lock_root.parent))
        stage = container / "payload"
        stage.mkdir()
        state = {"schema_version": "asi_stack.generated_directory_stage.v1", "state": "incomplete",
                 "family": family, "destination": str(output),
                 "prior_tree_sha256": tree_sha256(before) if before is not None else None,
                 "expected_payload_tree_sha256": desired["payload_tree_sha256"]}
        files = ProjectionFiles()
        files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
        sync_directory(container)
        attempted = installed = False
        durable = False
        try:
            for name, data in sorted(payload.items()):
                path = stage / name
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as stream:
                    stream.write(data)
            files.write(stage / RECEIPT, json.dumps(desired, indent=2, ensure_ascii=False) + "\n")
            if payload_rows(stage) != desired["files"]:
                raise ValueError("staged generated payload differs from inspected bytes")
            staged_rows = file_rows(stage)
            sync_stage(stage)
            state["state"] = "prepared"
            files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            sync_directory(container)
            guard()
            ordinary(output)
            if (file_rows(output) if output.exists() else None) != before:
                raise ValueError("previous generated directory changed; preserving concurrent edits")
            state["state"] = "installation_attempted"
            files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            sync_directory(container)
            attempted = True
            if existed:
                exchange_directories(stage, output)
            else:
                install_directory_noreplace(stage, output)
            installed = True
            if existed and file_rows(stage) != before:
                raise ValueError("concurrently changed prior generated directory is retained for inspection")
            if file_rows(output) != staged_rows:
                raise ValueError("installed generated directory changed")
            guard()
            sync_directory(output.parent)
            durable = True
            return desired
        finally:
            if attempted and not durable:
                state["state"] = ("installed_durability_unconfirmed" if installed
                                  else "installation_outcome_unconfirmed")
                files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            else:
                shutil.rmtree(container)
