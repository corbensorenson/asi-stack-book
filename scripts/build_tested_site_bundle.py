#!/usr/bin/env python3
"""Copy a rendered site into a commit-bound, content-addressed deployment bundle."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile
from typing import Any

from build_canonical_public_status import ROOT, load_json


MANIFEST_NAME = "tested-site-bundle.json"
STATUS_PATH = PurePosixPath("status/canonical-public-status.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordinary_path(path: Path) -> None:
    if any(item.is_symlink() for item in (path, *path.parents)):
        raise ValueError(f"site custody refuses symlink ancestry: {path}")


def file_rows(site: Path) -> list[dict[str, Any]]:
    ordinary_path(site)
    if site.is_symlink() or not site.is_dir():
        raise ValueError(f"site bundle requires an ordinary directory: {site}")
    rows: list[dict[str, Any]] = []
    directories = set()
    for path in sorted(site.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"site bundle refuses symlink: {path.relative_to(site)}")
        mode = path.stat().st_mode
        if stat.S_ISDIR(mode):
            directories.add(path.relative_to(site).as_posix())
            continue
        if not stat.S_ISREG(mode):
            raise ValueError(f"site bundle refuses special file: {path.relative_to(site)}")
        relative = path.relative_to(site).as_posix()
        if relative.startswith("../") or relative.startswith("/"):
            raise ValueError(f"site bundle path escapes root: {relative}")
        rows.append({"path": relative, "size": path.stat().st_size, "sha256": sha256_file(path)})
    # File inventories own their enclosing directories, not arbitrary empty
    # directory objects. Reject before adopting/replacing/copying that tree.
    implied = {parent.as_posix() for row in rows for parent in PurePosixPath(row["path"]).parents
               if parent != PurePosixPath(".")}
    if directories != implied:
        raise ValueError(f"site custody refuses unregistered directory objects: {sorted(directories - implied)[:8]}")
    return rows


def tree_sha256(rows: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{row['path']}\0{row['size']}\0{row['sha256']}\n".encode("utf-8"))
    return digest.hexdigest()


def build_manifest(site: Path, *, allow_local: bool) -> dict[str, Any]:
    # Inspect before reading status: it too may be a symlink or special file.
    rows = file_rows(site)
    status_file = site / STATUS_PATH
    if not status_file.exists():
        raise ValueError(f"rendered site is missing {STATUS_PATH}")
    status = load_json(status_file)
    if not isinstance(status, dict):
        raise TypeError("rendered canonical status must be an object")
    if not allow_local:
        if status.get("source_tree_state") != "clean" or status.get("build_context") != "tested_commit":
            raise ValueError("deployment bundle requires canonical status from a clean tested commit")
    commit = str(status.get("source_commit", ""))
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise ValueError("canonical status source_commit must be a full lowercase SHA")
    return {
        "schema_version": "asi_stack.tested_site_bundle.v0",
        "artifact_name": f"asi-stack-pages-{commit}",
        "source_commit": commit,
        "source_tree_state": status.get("source_tree_state"),
        "build_context": status.get("build_context"),
        "canonical_status": {
            "path": str(STATUS_PATH),
            "status_id": str(status.get("status_id", "")),
            "sha256": sha256_file(status_file),
        },
        "site": {
            "file_count": len(rows),
            "total_bytes": sum(int(row["size"]) for row in rows),
            "tree_sha256": tree_sha256(rows),
            "files": rows,
        },
        "non_claims": [
            "Bundle integrity identifies the tested files; it does not prove chapter claims, model quality, safety, or security.",
            "A successful deployment still requires independent post-deployment attestation.",
            "A local-worktree bundle produced with --allow-local is diagnostic and is not deployable.",
        ],
    }


def exchange_directories(left: Path, right: Path) -> None:
    """One namespace operation; unsupported filesystems fail without a gap.

    Linux renameat2(RENAME_EXCHANGE) and Darwin renamex_np(RENAME_SWAP)
    exchange two complete directories, including nonempty destinations.
    Never fall back to moving the destination away first.
    """
    _rename_directories(left, right, exchange=True)


def install_directory_noreplace(left: Path, right: Path) -> None:
    """Install into an absent name, atomically refusing any intervening object."""
    _rename_directories(left, right, exchange=False)


def _rename_directories(left: Path, right: Path, *, exchange: bool) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin" and hasattr(libc, "renamex_np"):
        call = libc.renamex_np
        call.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        # SDK sys/stdio.h: RENAME_SWAP=2, RENAME_EXCL=4.
        args = (os.fsencode(left), os.fsencode(right), 2 if exchange else 4)
    elif sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
        call = libc.renameat2
        call.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        args = (-100, os.fsencode(left), -100, os.fsencode(right), 2 if exchange else 1)
    else:
        raise OSError(errno.ENOTSUP, "atomic directory installation unavailable")
    call.restype = ctypes.c_int
    if call(*args) != 0:
        code = ctypes.get_errno()
        raise OSError(code, "atomic directory installation failed; destination retained")


def sync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def sync_stage(stage: Path) -> None:
    for path in stage.rglob("*"):
        if path.is_file():
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
    directories = [path for path in stage.rglob("*") if path.is_dir()]
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        sync_directory(path)
    sync_directory(stage)


@contextmanager
def bundle_lock(output: Path):
    # Keep the lock inode stable across runs. Removing it after unlocking can
    # let two builders lock different inodes for the same destination.
    lock_path = output.parent / f".{output.name}.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(f"another builder owns bundle destination: {output}") from exc
        yield
    finally:
        os.close(fd)


def build_bundle(site: Path, output: Path, *, allow_local: bool) -> dict[str, Any]:
    ordinary_path(site)
    ordinary_path(output)
    if site.is_symlink() or output.is_symlink():
        raise ValueError("site and bundle roots must not be symlinks")
    site, output = site.resolve(), output.resolve()
    if site == output or site in output.parents or output in site.parents:
        raise ValueError("site and bundle directories must be disjoint, without ancestor overlap")
    output.parent.mkdir(parents=True, exist_ok=True)
    with bundle_lock(output):
        return stage_bundle(site, output, allow_local=allow_local)


def stage_bundle(site: Path, output: Path, *, allow_local: bool) -> dict[str, Any]:
    ordinary_path(site)
    ordinary_path(output)
    if output.is_symlink() or output.exists() and (
        not output.is_dir()
        or {path.name for path in output.iterdir()} != {"site", MANIFEST_NAME}
    ):
        raise ValueError("refusing to replace a directory that is not an owned site bundle")
    if output.exists():
        # Inspect the metadata file too before reading it.
        previous_rows = file_rows(output)
        previous = load_json(output / MANIFEST_NAME)
        if previous != build_manifest(output / "site", allow_local=True):
            raise ValueError("previous bundle integrity failed; preserve it and use a new output path")
    else:
        previous_rows = None
    expected = build_manifest(site, allow_local=allow_local)
    container = Path(tempfile.mkdtemp(prefix=f".{output.name}-stage-", dir=output.parent))
    stage = container / "bundle"
    stage.mkdir()
    from projection_files import ProjectionFiles
    state = {"schema_version": "asi_stack.bundle_install_stage.v1", "state": "incomplete",
             "destination": str(output), "source_tree_sha256": expected["site"]["tree_sha256"],
             "support_state_effect": "none", "release_effect": "none"}
    def record():
        ProjectionFiles().write(container / "staging.json", json.dumps(state, indent=2) + "\n")
        sync_directory(container)
    record()
    attempted = installed = durable = False
    try:
        # Preserve links, including ones introduced after the source scan.
        # The staged scan rejects them instead of dereferencing outside bytes.
        shutil.copytree(site, stage / "site", symlinks=True)
        manifest = build_manifest(stage / "site", allow_local=allow_local)
        if manifest != expected:
            raise ValueError("source changed while the site bundle was being staged")
        (stage / MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        staged_rows = file_rows(stage)
        sync_stage(stage)
        state["state"] = "prepared"; record()
        if (file_rows(output) if output.exists() else None) != previous_rows:
            raise ValueError("previous bundle changed during staging; preserving concurrent edits")
        if build_manifest(site, allow_local=allow_local) != expected:
            raise ValueError("source changed before bundle installation")
        state["state"] = "installation_attempted"; record()
        attempted = True
        if previous_rows is not None:
            exchange_directories(stage, output)
        else:
            install_directory_noreplace(stage, output)
        installed = True
        if previous_rows is not None and file_rows(stage) != previous_rows:
            raise ValueError("concurrently changed prior bundle is retained for inspection")
        if file_rows(output) != staged_rows or build_manifest(output / "site", allow_local=allow_local) != expected:
            raise ValueError("installed bundle changed before acceptance")
        if build_manifest(site, allow_local=allow_local) != expected:
            raise ValueError("bundle source changed before acceptance; prior bundle retained")
        sync_directory(output.parent)
        durable = True
        return manifest
    finally:
        if attempted and not durable:
            state["state"] = ("installed_acceptance_or_durability_unconfirmed" if installed
                              else "installation_outcome_unconfirmed"); record()
        else:
            shutil.rmtree(container)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--output", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--allow-local", action="store_true")
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    output = args.output if args.output.is_absolute() else ROOT / args.output
    try:
        manifest = build_bundle(site, output, allow_local=args.allow_local)
    except (OSError, TypeError, ValueError) as exc:
        raise SystemExit(f"could not build tested site bundle: {exc}") from exc
    print(
        f"Built {manifest['artifact_name']}: {manifest['site']['file_count']} files, "
        f"{manifest['site']['total_bytes']} bytes, tree {manifest['site']['tree_sha256'][:16]}."
    )


if __name__ == "__main__":
    main()
