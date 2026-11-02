#!/usr/bin/env python3
"""Build a deterministic tar.gz candidate from an exact tested-site bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
from typing import Any, Iterable

from build_canonical_public_status import ROOT, load_json
from build_tested_site_bundle import MANIFEST_NAME, build_manifest, file_rows, ordinary_path, tree_sha256
from generated_directory import install as install_directory, relative
from validate_tested_site_bundle import compare as bundle_errors


POLICY = ROOT / "status" / "versioned_release_policy.json"
CANDIDATE_MANIFEST = "immutable-site-archive-candidate.json"
FAMILY = "immutable_site_archive"
SCHEMA = ROOT / "schemas/immutable_site_archive_manifest.schema.json"
RUNTIME_INPUTS = (
    "scripts/build_immutable_site_archive.py", "scripts/validate_immutable_site_archive.py",
    "scripts/build_tested_site_bundle.py", "scripts/validate_tested_site_bundle.py",
    "scripts/generated_directory.py", "scripts/projection_files.py",
    "scripts/build_canonical_public_status.py", "scripts/schema_validation.py", "scripts/admission_guard.py",
    "schemas/immutable_site_archive_manifest.schema.json", "schemas/tested_site_bundle.schema.json",
)


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(read_regular(path))


def normalized_member(name: str) -> PurePosixPath:
    member = PurePosixPath(name)
    if (not name or member.is_absolute() or ".." in member.parts or not member.parts
            or member.as_posix() != name or "\\" in name or member == PurePosixPath(".")
            or any(ord(char) < 32 or ord(char) == 127 for char in name)):
        raise ValueError(f"archive member path is unsafe: {name!r}")
    return member


def read_regular(path: Path) -> bytes:
    """Inspect ancestry and the opened object without blocking on a FIFO."""
    ordinary_path(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"archive input requires a regular file: {path}")
        return stream.read()


def policy_label(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name


def inspect_bundle(bundle: Path, *, allow_local: bool) -> dict:
    ordinary_path(bundle)
    if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != {"site", MANIFEST_NAME}:
        raise ValueError("archive source bundle must contain only its manifest and site directory")
    bundle = bundle.resolve()
    rows = file_rows(bundle)
    data = {row["path"]: read_regular(bundle / row["path"]) for row in rows}
    if any(len(data[row["path"]]) != row["size"] or sha256_bytes(data[row["path"]]) != row["sha256"]
           for row in rows):
        raise ValueError("archive source bundle changed while capturing bytes")
    manifest = json.loads(data[MANIFEST_NAME])
    if not isinstance(manifest, dict):
        raise ValueError("archive source bundle manifest must be an object")
    errors = bundle_errors(manifest, build_manifest(bundle / "site", allow_local=allow_local), None)
    if errors:
        raise ValueError("archive source bundle failed integrity: " + "; ".join(errors))
    if file_rows(bundle) != rows:
        raise ValueError("archive source bundle changed during inspection")
    return {"root": bundle, "rows": rows, "data": data, "manifest": manifest}


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


def source_members(bundle: Path, root_directory: str, *, inspected: dict | None = None) -> list[tuple[str, bytes]]:
    if len(normalized_member(root_directory).parts) != 1:
        raise ValueError("archive root must be one safe directory name")
    inspected = inspect_bundle(bundle, allow_local=True) if inspected is None else inspected
    return [(f"{root_directory}/{name}", body) for name, body in sorted(inspected["data"].items())]


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
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("archive version must be a three-component semantic version tag")
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
    check: bool = False,
) -> dict[str, Any]:
    for path in (bundle, output, policy_path):
        ordinary_path(path)
    bundle, output, policy_path = bundle.resolve(), output.resolve(), policy_path.resolve()
    if (bundle == output or bundle in output.parents or output in bundle.parents
            or output == policy_path or output in policy_path.parents):
        raise ValueError("archive output must not overlap source bundle or policy inputs")
    inspected = inspect_bundle(bundle, allow_local=allow_local)
    bundle_manifest = inspected["manifest"]
    clean = bundle_manifest.get("source_tree_state") == "clean" and bundle_manifest.get("build_context") == "tested_commit"
    if not clean and not allow_local:
        raise ValueError("immutable archive requires a clean tested-commit bundle")
    source_commit = str(bundle_manifest.get("source_commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("tested-site bundle source commit is malformed")
    policy_bytes = read_regular(policy_path)
    policy = json.loads(policy_bytes)
    runtime = {name: read_regular(ROOT / name) for name in RUNTIME_INPUTS}
    release = policy_release(version, source_commit, policy)
    template = str(policy["immutable_channel"]["artifact_name_template"])
    filename = template.format(version=version, source_commit=source_commit)
    if not filename.endswith(".tar.gz") or Path(filename).name != filename:
        raise ValueError("immutable archive template must produce one safe .tar.gz filename")
    relative(filename)
    root_directory = f"asi-stack-site-{version}-{source_commit}"
    members = source_members(bundle, root_directory, inspected=inspected)
    body = archive_bytes(members, root_directory)
    candidate = {
        "schema_version": "asi_stack.immutable_site_archive_candidate.v0",
        "candidate_state": "publishable_clean_candidate" if clean else "diagnostic_dirty_local_candidate",
        "version": version,
        "source_commit": source_commit,
        "source_tree_state": bundle_manifest.get("source_tree_state"),
        "build_context": bundle_manifest.get("build_context"),
        "release_policy": {
            "path": policy_label(policy_path),
            "sha256": sha256_bytes(policy_bytes),
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
            "manifest_sha256": sha256_bytes(inspected["data"][MANIFEST_NAME]),
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
    payload = {filename: body,
               CANDIDATE_MANIFEST: (json.dumps(candidate, indent=2, ensure_ascii=False) + "\n").encode(),
               f"{filename}.sha256": f"{candidate['archive']['sha256']}  {filename}\n".encode()}
    inputs = {"source/bundle_tree": tree_sha256(inspected["rows"]),
              "source/release_policy": sha256_bytes(policy_bytes),
              **{name: sha256_bytes(data) for name, data in runtime.items()}}
    def guard():
        if (file_rows(bundle) != inspected["rows"] or read_regular(policy_path) != policy_bytes
                or any(read_regular(ROOT / name) != data for name, data in runtime.items())):
            raise ValueError("archive source bundle, policy or checking code changed during preparation")
    def accept_previous(previous):
        prior = json.loads(read_regular(previous / CANDIDATE_MANIFEST))
        if (not isinstance(prior, dict) or not isinstance(prior.get("publication"), dict)
                or not isinstance(prior.get("archive"), dict) or not isinstance(prior.get("source_bundle"), dict)
                or prior.get("version") != version or prior.get("source_commit") != source_commit
                or prior["archive"].get("sha256") != candidate["archive"]["sha256"]
                or prior["source_bundle"].get("manifest_sha256") != candidate["source_bundle"]["manifest_sha256"]
                or prior.get("publication", {}).get("state") != "local_candidate_not_published"
                or prior.get("publication", {}).get("url") != ""):
            raise ValueError("preserve the prior archive identity; choose a fresh output for another version/commit")
    guard()
    from validate_immutable_site_archive import validate_candidate_payload
    errors = validate_candidate_payload(candidate, payload, inspected, policy, policy_bytes,
                                        policy_label(policy_path), allow_local=allow_local,
                                        schema=json.loads(runtime["schemas/immutable_site_archive_manifest.schema.json"]))
    if errors:
        raise ValueError("prepared archive failed domain acceptance: " + "; ".join(errors))
    install_directory(output, family=FAMILY, payload=payload, inputs=inputs, guard=guard,
                      check=check, accept_previous=accept_previous)
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--output", type=Path, default=Path("build/immutable-site-archive"))
    parser.add_argument("--version", required=True)
    parser.add_argument("--policy", type=Path, default=POLICY)
    parser.add_argument("--allow-local", action="store_true")
    parser.add_argument("--check", action="store_true", help="Verify the current installed candidate without writing")
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
            check=args.check,
        )
    except (KeyError, OSError, TypeError, ValueError) as exc:
        raise SystemExit(f"could not build immutable site archive: {exc}") from exc
    print(
        f"{'Checked' if args.check else 'Built'} {candidate['candidate_state']} {candidate['archive']['filename']}: "
        f"{candidate['archive']['member_count']} members, {candidate['archive']['size']} bytes, "
        f"sha256 {candidate['archive']['sha256'][:16]}."
    )


if __name__ == "__main__":
    try:
        from admission_guard import canonical_access
        with canonical_access(ROOT):
            main()
    except (OSError, TypeError, ValueError) as error:
        raise SystemExit(f"Archive operation refused: {error}") from error
