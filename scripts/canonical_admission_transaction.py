"""Manifest-last canonical admission with retained objects and explicit rollback.

Cooperating canonical readers are excluded by the repository directory lease.
This is a recoverable multi-file transaction, not a single filesystem exchange
or a certificate of physical power-loss behavior or scientific adequacy.
"""

from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import uuid

from admission_guard import ACTIVE, canonical_access, ensure_ready, ordinary
from build_tested_site_bundle import exchange_directories, sync_directory, sync_stage
from projection_files import ProjectionFiles
import prepare_chapter_admission as domain

VERSION = "asi_stack.canonical_admission_transaction.v1"
MAX_CONTROL_BYTES = 32 * 1024 * 1024


def control_with_digest(path: Path) -> tuple[dict, str]:
    ordinary(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"admission control is not a regular file: {path}")
        body = stream.read(MAX_CONTROL_BYTES + 1)
    if len(body) > MAX_CONTROL_BYTES:
        raise ValueError("admission control exceeds its byte budget")
    value = json.loads(body, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-finite JSON: {value}")))
    if not isinstance(value, dict):
        raise ValueError("admission control must be an object")
    return value, hashlib.sha256(body).hexdigest()


def control(path: Path) -> dict:
    return control_with_digest(path)[0]


def save(path: Path, value: dict) -> None:
    ProjectionFiles().write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    sync_directory(path.parent)


def physical(path: Path) -> dict | None:
    ordinary(path)
    if not os.path.lexists(path):
        return None
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError(f"admission target is not a regular file: {path}")
    return {"sha256": domain.digest(path), "bytes": info.st_size,
            "mode": stat.S_IMODE(info.st_mode), "device": info.st_dev, "inode": info.st_ino}


def content(row: dict | None) -> dict | None:
    return None if row is None else {key: row[key] for key in ("sha256", "bytes", "mode")}


def same_object(left: dict | None, right: dict | None) -> bool:
    return left is not None and right is not None and all(left[key] == right[key] for key in ("device", "inode"))


def write_payload(path: Path, body: bytes, mode: int) -> None:
    ordinary(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(body)
        stream.flush()
        os.fchmod(stream.fileno(), mode)
        os.fsync(stream.fileno())


def source_guard(root: Path, receipt: dict, installed: set[str]) -> None:
    registry = json.loads(domain.regular_file(root, "validation/registry.json").read_bytes())
    expected = {name: receipt["patch_files"][name] if name in installed else row
                for name, row in receipt["source_files"].items()}
    if "validation/registry.json" in installed:
        expected.update({name: receipt["patch_files"][name] for name in registry["required_artifacts"]
                         if name in receipt["patch_files"] and name not in receipt["source_files"]})
    if (domain.source_paths(root, registry) != sorted(expected)
            or domain.snapshot(root, sorted(expected)) != expected
            or domain.git_identity(root) != receipt["source_git"]):
        raise ValueError("canonical source or Git index/HEAD changed during admission; preserve the journal and recover")


def verify(root: Path, stage: Path, receipt: dict) -> None:
    ordinary(stage)
    if not stage.is_relative_to(root / "build") or not stage.is_dir():
        raise ValueError("admission stage must be an ordinary directory below build/")
    if (receipt.get("schema_version") != domain.STAGE_VERSION
            or receipt.get("status") != "full_deep_passed_not_admitted"
            or receipt.get("admission_state") != "not_admitted"
            or receipt.get("support_state_effect") != "none"
            or receipt.get("validation", {}).get("mode") != "full_deep"
            or receipt["validation"]["execution"].get("status") != "passed"):
        raise ValueError("canonical admission requires the full validated candidate receipt")
    if control(stage / "admission.json") != receipt:
        raise ValueError("candidate receipt changed before admission")
    for name in receipt["patch_files"]:
        domain.check_patch_path(name)
    domain.check_registry_patch(root, stage / "workspace", list(receipt["patch_files"]),
                                list(receipt["source_files"]), require_new=True)
    domain.candidate_manifest(root, receipt["proposal"], stage / "workspace")
    expected = {**receipt["source_files"], **receipt["patch_files"]}
    if domain.snapshot(stage / "workspace", sorted(expected)) != expected:
        raise ValueError("validated candidate workspace changed before admission")
    report_path = stage / "workspace/build/chapter-admission-validation.json"
    report, report_digest = control_with_digest(report_path)
    registry = json.loads(domain.regular_file(root, "validation/registry.json").read_bytes())
    from run_validation_registry import select_units
    units = {"base-gate", *(row["id"] for row in select_units(registry, "deep", []))}
    observations = report.get("units", [])
    if (report_digest != receipt["validation"]["report_sha256"]
            or report.get("status") != "pass" or report.get("registry_drift") is not False
            or report.get("registry_sha256") != {"validation/registry.json": expected["validation/registry.json"]["sha256"]}
            or len(observations) != len(units) or {row.get("unit_id") for row in observations} != units
            or any(row.get("status") != "passed" for row in observations)):
        raise ValueError("full deep report custody or complete unit acceptance failed")
    source_guard(root, receipt, set())


def install_candidate(root: Path, stage: Path, receipt: dict, *, lease: int) -> dict:
    # The live preparation command keeps this exclusive lease through its
    # actual full validation. No CLI admits an arbitrary saved stage receipt.
    info = os.fstat(lease)
    if (info.st_dev, info.st_ino) != (root.stat().st_dev, root.stat().st_ino):
        raise ValueError("canonical admission requires the source directory lease")
    fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ensure_ready(root)
    verify(root, stage, receipt)
    transaction = stage / "transaction"
    if os.path.lexists(transaction):
        raise ValueError("preserving existing admission transaction; use a fresh stage")
    rows = []
    device = root.stat().st_dev
    for name, desired in receipt["patch_files"].items():
        prior = physical(root / name)
        if content(prior) != receipt["source_files"].get(name):
            raise ValueError(f"unknown or changed canonical target is preserved: {name}")
        if content(prior) == desired:
            continue
        if prior is not None and prior["device"] != device:
            raise ValueError("canonical admission targets must share the transaction filesystem")
        rows.append({"path": name, "before": prior, "after": desired})
    rows.sort(key=lambda row: (row["path"] == "book_structure.json", row["path"]))
    if not rows or rows[-1]["path"] != "book_structure.json":
        raise ValueError("admission must commit the intended manifest insertion last")
    needed = sum((row["before"] or {}).get("bytes", 0) + 2 * row["after"]["bytes"] for row in rows)
    if shutil.disk_usage(root).free < needed + 128 * 1024 * 1024:
        raise ValueError("insufficient space for durable admission payload and prior custody")
    transaction.mkdir(mode=0o700)
    token = uuid.uuid4().hex
    journal_path = transaction / "journal.json"
    journal = {"schema_version": VERSION, "transaction_id": token, "state": "preparing",
               "stage": stage.relative_to(root).as_posix(), "rows": rows, "directories": {},
               "source_git": receipt["source_git"], "support_state_effect": "none", "release_effect": "none"}
    save(journal_path, journal)
    for row in rows:
        name = row["path"]
        body = domain.regular_file(stage / "workspace", name).read_bytes()
        if hashlib.sha256(body).hexdigest() != row["after"]["sha256"]:
            raise ValueError("candidate payload changed while preparing canonical admission")
        write_payload(transaction / "after" / name, body, row["after"]["mode"])
        write_payload(transaction / "exchange" / name, body, row["after"]["mode"])
        row["incoming"] = physical(transaction / "exchange" / name)
        if content(row["incoming"]) != row["after"] or content(physical(transaction / "after" / name)) != row["after"]:
            raise ValueError("prepared payload differs from the validated candidate")
        if row["incoming"]["device"] != device:
            raise ValueError("admission stage and canonical targets must share one filesystem")
        if row["before"] is not None:
            write_payload(transaction / "before" / name, (root / name).read_bytes(), row["before"]["mode"])
            if content(physical(transaction / "before" / name)) != content(row["before"]):
                raise ValueError("prior canonical bytes changed while retaining custody")
        for parent in (root / name).parents:
            if parent == root:
                break
            ordinary(parent)
            if not parent.exists():
                journal["directories"][parent.relative_to(root).as_posix()] = None
            elif not parent.is_dir() or parent.stat().st_dev != device:
                raise ValueError("canonical admission parent is not an ordinary same-filesystem directory")
    journal["state"] = "prepared"
    save(journal_path, journal)
    sync_stage(transaction)
    sync_directory(stage)
    verify(root, stage, receipt)
    for row in rows:
        if physical(root / row["path"]) != row["before"]:
            raise ValueError("canonical target object changed before the transaction began")
    active = root / ACTIVE
    ordinary(active)
    pointer = {"schema_version": VERSION, "transaction_id": token, "stage": journal["stage"]}
    # Exclusive creation preserves every existing marker, including unknown
    # objects. This is durable before the first canonical directory/file write.
    with active.open("xb") as stream:
        stream.write((json.dumps(pointer) + "\n").encode())
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(active.parent)
    installed = set()
    try:
        for name in sorted(journal["directories"], key=lambda value: (len(Path(value).parts), value)):
            parent = root / name
            ordinary(parent)
            parent.mkdir(mode=0o755)
            data = parent.stat()
            journal["directories"][name] = {"device": data.st_dev, "inode": data.st_ino}
            sync_directory(parent.parent)
            save(journal_path, journal)
        for row in rows:
            name = row["path"]
            if not installed or name == "book_structure.json":
                source_guard(root, receipt, installed)
            if physical(root / name) != row["before"]:
                raise ValueError(f"canonical target changed before replacement: {name}")
            slot = transaction / "exchange" / name
            if physical(slot) != row["incoming"]:
                raise ValueError("prepared exchange object changed")
            if row["before"] is None:
                # Atomic no-replace installation. The owned slot retains the
                # object identity; source/workspace files are never hard-linked.
                os.link(slot, root / name, follow_symlinks=False)
            else:
                exchange_directories(slot, root / name)
            if (physical(root / name) != row["incoming"] or
                    row["before"] is not None and physical(slot) != row["before"]):
                raise ValueError("a concurrently edited object was displaced; it is retained for recovery")
            sync_directory((root / name).parent)
            sync_directory(slot.parent)
            installed.add(name)
            journal["state"] = "installing"
            save(journal_path, journal)
        source_guard(root, receipt, installed)
        for row in rows:
            if physical(root / row["path"]) != row["incoming"]:
                raise ValueError("installed candidate changed before commit")
        final = copy.deepcopy(receipt)
        final.update(status="installed", admission_state="admitted", canonical_source_unchanged=False,
                     transaction_id=token, scope="Validated local manifest admission; no publication, evidence transition or support promotion.")
        journal["state"] = "committed"
        save(journal_path, journal)
        save(stage / "admission.json", final)
        clear_pointer(active, pointer)
        return final
    except BaseException as error:
        journal.update(state="recovery_required", error=f"{type(error).__name__}: {error}")
        save(journal_path, journal)
        raise


def clear_pointer(active: Path, expected: dict) -> None:
    if control(active) != expected:
        raise ValueError("admission pointer changed; preserving it")
    active.unlink()
    try:
        sync_directory(active.parent)
    except OSError:
        # Preserve a runtime gate if cleanup durability cannot be confirmed.
        # Never replace an object introduced by another actor in the gap.
        if not os.path.lexists(active):
            with active.open("xb") as stream:
                stream.write((json.dumps(expected) + "\n").encode())
                stream.flush()
                os.fsync(stream.fileno())
        raise


def rollback(root: Path) -> dict:
    with canonical_access(root, write=True, recovery=True):
        active = root / ACTIVE
        pointer = control(active)
        if set(pointer) != {"schema_version", "transaction_id", "stage"} or pointer["schema_version"] != VERSION:
            raise ValueError("unknown admission pointer is preserved")
        relative = Path(pointer["stage"])
        if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != pointer["stage"] or relative.parts[:1] != ("build",):
            raise ValueError("unsafe admission stage pointer is preserved")
        stage = root / relative
        journal_path = stage / "transaction/journal.json"
        journal = control(journal_path)
        if (journal.get("schema_version") != VERSION or journal.get("transaction_id") != pointer["transaction_id"]
                or journal.get("stage") != pointer["stage"] or journal.get("support_state_effect") != "none"
                or journal.get("release_effect") != "none" or domain.git_identity(root) != journal.get("source_git")):
            raise ValueError("admission journal or Git custody changed; recovery requires inspection")
        rows = journal["rows"]
        if not rows or rows[-1]["path"] != "book_structure.json" or len({row["path"] for row in rows}) != len(rows):
            raise ValueError("invalid admission transaction order")
        allowed_parents = {parent.as_posix() for row in rows for parent in Path(row["path"]).parents
                           if parent.as_posix() != "."}
        if set(journal["directories"]) - allowed_parents:
            raise ValueError("recovery directory is not a candidate target parent")
        receipt = control(stage / "admission.json")
        if receipt.get("schema_version") != domain.STAGE_VERSION or receipt.get("support_state_effect") != "none":
            raise ValueError("candidate receipt custody changed before recovery")
        states = {}
        # Preflight every target before restoring any target. A later edit to an
        # installed file is never silently removed, even if another row is safe.
        for row in rows:
            name = domain.relative_path(row["path"])
            domain.check_patch_path(name)
            target = physical(root / name)
            slot = physical(stage / "transaction/exchange" / name)
            if row["before"] is None:
                if slot != row["incoming"] or target is not None and target != row["incoming"]:
                    raise ValueError(f"new canonical target or retained object changed: {name}")
                states[name] = target is not None
            elif same_object(target, row["before"]) and slot == row["incoming"]:
                states[name] = False
            elif target == row["incoming"] and same_object(slot, row["before"]):
                states[name] = True
            else:
                raise ValueError(f"canonical target or retained object changed: {name}")
        for row in reversed(rows):  # Restore original manifest first.
            name = row["path"]
            if not states[name]:
                continue
            if physical(root / name) != row["incoming"]:
                raise ValueError("canonical target changed after recovery preflight")
            slot = stage / "transaction/exchange" / name
            if row["before"] is None:
                (root / name).unlink()
            else:
                if not same_object(physical(slot), row["before"]):
                    raise ValueError("retained prior object changed after recovery preflight")
                exchange_directories(slot, root / name)
            sync_directory((root / name).parent)
            sync_directory(slot.parent)
        retained_directories = []
        for name, expected in sorted(journal["directories"].items(), key=lambda row: len(Path(row[0]).parts), reverse=True):
            domain.relative_path(name)
            parent = root / name
            ordinary(parent)
            if not parent.exists():
                continue
            info = parent.stat()
            if expected is None or {"device": info.st_dev, "inode": info.st_ino} != expected:
                retained_directories.append(name)
                continue
            try:
                parent.rmdir()
                sync_directory(parent.parent)
            except OSError:
                retained_directories.append(name)  # Preserve any new user content.
        journal.update(state="rolled_back", retained_directories=retained_directories)
        save(journal_path, journal)
        receipt.update(status="rolled_back", admission_state="not_admitted", transaction_id=pointer["transaction_id"])
        save(stage / "admission.json", receipt)
        clear_pointer(active, pointer)
        return {"status": "rolled_back", "stage": pointer["stage"], "retained_directories": retained_directories,
                "support_state_effect": "none", "release_effect": "none"}
