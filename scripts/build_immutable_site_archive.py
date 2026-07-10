#!/usr/bin/env python3
"""Build a deterministic tar.gz candidate from an exact tested-site bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile
from typing import Any, Iterable

from build_canonical_public_status import ROOT, load_json
from build_tested_site_bundle import MANIFEST_NAME


POLICY = ROOT / "status" / "versioned_release_policy.json"
CANDIDATE_MANIFEST = "immutable-site-archive-candidate.json"


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_member(name: str) -> PurePosixPath:
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts or not member.parts:
        raise ValueError(f"archive member path is unsafe: {name!r}")
    return member


def tar_info(name: str, size: int, *, directory: bool = False) -> tarfile.TarInfo:
    normalized_member(name)
    info = tarfile.TarInfo(name.rstrip("/") + "/" if directory else name)
    info.type = tarfile.DIRTYPE if directory else tarfile.REGTYPE
    info.size = 0 if directory else size
    info.mode = 0o755 if directory else 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info


def source_members(bundle: Path, root_directory: str) -> list[tuple[str, bytes]]:
    site = bundle / "site"
    manifest = bundle / MANIFEST_NAME
    if not site.is_dir() or not manifest.is_file():
        raise ValueError(f"tested bundle must contain site/ and {MANIFEST_NAME}")
    members = [(f"{root_directory}/{MANIFEST_NAME}", manifest.read_bytes())]
    for path in sorted(candidate for candidate in site.rglob("*") if candidate.is_file()):
        if path.is_symlink():
            raise ValueError(f"immutable archive refuses symlinked site file: {path.relative_to(site)}")
        relative = path.relative_to(site).as_posix()
        normalized_member(relative)
        members.append((f"{root_directory}/site/{relative}", path.read_bytes()))
    return members


def archive_bytes(members: Iterable[tuple[str, bytes]], root_directory: str) -> bytes:
    member_rows = list(members)
    directories = {root_directory, f"{root_directory}/site"}
    for name, _ in member_rows:
        parent = PurePosixPath(name).parent
        while len(parent.parts) > 1:
            directories.add(parent.as_posix())
            parent = parent.parent
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0, compresslevel=9) as zipped:
        with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for directory in sorted(directories, key=lambda value: (len(PurePosixPath(value).parts), value)):
                archive.addfile(tar_info(directory, 0, directory=True))
            for name, body in sorted(member_rows):
                archive.addfile(tar_info(name, len(body)), io.BytesIO(body))
    return output.getvalue()


def policy_release(version: str, source_commit: str, policy: dict[str, Any]) -> dict[str, Any]:
    if not re.fullmatch(str(policy["immutable_channel"]["tag_pattern"]), version):
        raise ValueError(f"version does not satisfy immutable tag policy: {version}")
    matches = [row for row in policy.get("known_releases", []) if row.get("version") == version]
    if len(matches) != 1:
        raise ValueError(f"version must have exactly one known-release policy row before archive preparation: {version}")
    row = matches[0]
    if row.get("source_commit") != source_commit:
        raise ValueError(f"{version}: tested bundle commit does not match release policy")
    if row.get("site_artifact_state") != "not_published":
        raise ValueError(f"{version}: archive preparation refuses an already-published policy row")
    if row.get("archive_backfill_decision") == "declined_historical_render_not_available":
        raise ValueError(f"{version}: archive backfill was declined because the historical tested site bundle is unavailable")
    return row


def build_candidate(
    bundle: Path,
    output: Path,
    version: str,
    *,
    allow_local: bool,
    policy_path: Path = POLICY,
) -> dict[str, Any]:
    bundle_manifest_path = bundle / MANIFEST_NAME
    bundle_manifest = load_json(bundle_manifest_path)
    if not isinstance(bundle_manifest, dict):
        raise TypeError("tested-site bundle manifest must contain an object")
    clean = bundle_manifest.get("source_tree_state") == "clean" and bundle_manifest.get("build_context") == "tested_commit"
    if not clean and not allow_local:
        raise ValueError("immutable archive requires a clean tested-commit bundle")
    source_commit = str(bundle_manifest.get("source_commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("tested-site bundle source commit is malformed")
    policy = load_json(policy_path)
    release = policy_release(version, source_commit, policy)
    template = str(policy["immutable_channel"]["artifact_name_template"])
    filename = template.format(version=version, source_commit=source_commit)
    if not filename.endswith(".tar.gz") or Path(filename).name != filename:
        raise ValueError("immutable archive template must produce one safe .tar.gz filename")
    root_directory = f"asi-stack-site-{version}-{source_commit}"
    members = source_members(bundle, root_directory)
    body = archive_bytes(members, root_directory)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    archive_path = output / filename
    archive_path.write_bytes(body)
    candidate = {
        "schema_version": "asi_stack.immutable_site_archive_candidate.v0",
        "candidate_state": "publishable_clean_candidate" if clean else "diagnostic_dirty_local_candidate",
        "version": version,
        "source_commit": source_commit,
        "source_tree_state": bundle_manifest.get("source_tree_state"),
        "build_context": bundle_manifest.get("build_context"),
        "release_policy": {
            "path": (
                policy_path.relative_to(ROOT).as_posix()
                if policy_path.is_relative_to(ROOT)
                else policy_path.name
            ),
            "sha256": sha256_file(policy_path),
        },
        "archive": {
            "filename": filename,
            "root_directory": root_directory,
            "media_type": "application/gzip",
            "size": len(body),
            "sha256": sha256_bytes(body),
            "member_count": len(members),
            "timestamp_epoch": 0,
        },
        "source_bundle": {
            "manifest_filename": MANIFEST_NAME,
            "manifest_sha256": sha256_file(bundle_manifest_path),
            "site_file_count": bundle_manifest["site"]["file_count"],
            "site_total_bytes": bundle_manifest["site"]["total_bytes"],
            "site_tree_sha256": bundle_manifest["site"]["tree_sha256"],
        },
        "publication": {
            "state": "local_candidate_not_published",
            "storage_authority": policy["immutable_channel"]["storage_authority"],
            "release_record": release["release_record"],
            "url": "",
            "authorization_required": True,
        },
        "non_claims": [
            "A local archive candidate is not a published immutable release.",
            "Archive identity and deterministic replay do not prove chapter claims, runtime behavior, safety, or durability of future storage.",
            "Publication requires explicit authorization, upload to the exact tag release, post-upload digest verification, and atomic policy/release-record reconciliation.",
        ],
    }
    (output / CANDIDATE_MANIFEST).write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / f"{filename}.sha256").write_text(f"{candidate['archive']['sha256']}  {filename}\n", encoding="utf-8")
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--output", type=Path, default=Path("build/immutable-site-archive"))
    parser.add_argument("--version", required=True)
    parser.add_argument("--policy", type=Path, default=POLICY)
    parser.add_argument("--allow-local", action="store_true")
    args = parser.parse_args()
    bundle = args.bundle if args.bundle.is_absolute() else ROOT / args.bundle
    output = args.output if args.output.is_absolute() else ROOT / args.output
    policy_path = args.policy if args.policy.is_absolute() else ROOT / args.policy
    try:
        candidate = build_candidate(
            bundle,
            output,
            args.version,
            allow_local=args.allow_local,
            policy_path=policy_path,
        )
    except (KeyError, OSError, TypeError, ValueError) as exc:
        raise SystemExit(f"could not build immutable site archive: {exc}") from exc
    print(
        f"Built {candidate['candidate_state']} {candidate['archive']['filename']}: "
        f"{candidate['archive']['member_count']} members, {candidate['archive']['size']} bytes, "
        f"sha256 {candidate['archive']['sha256'][:16]}."
    )


if __name__ == "__main__":
    main()
