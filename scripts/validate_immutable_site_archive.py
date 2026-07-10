#!/usr/bin/env python3
"""Validate deterministic immutable-site archive candidates and rejection controls."""

from __future__ import annotations

import argparse
import copy
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
import tempfile

from build_canonical_public_status import ROOT, build_status, load_json, validate_against_schema
from build_immutable_site_archive import (
    CANDIDATE_MANIFEST,
    POLICY,
    archive_bytes,
    build_candidate,
    normalized_member,
    sha256_bytes,
    sha256_file,
    source_members,
)
from build_tested_site_bundle import MANIFEST_NAME, build_manifest


SCHEMA = ROOT / "schemas" / "immutable_site_archive_manifest.schema.json"
DOC = ROOT / "docs" / "immutable_site_archive_pipeline.md"


def build_self_test_bundle(root: Path) -> Path:
    bundle = root / "bundle"
    site = bundle / "site"
    (site / "status").mkdir(parents=True)
    status = build_status(
        timestamp="2000-01-01T00:00:00Z",
        source_commit_override="a" * 40,
        source_tree_state_override="clean",
    )
    (site / "status" / "canonical-public-status.json").write_text(
        json.dumps(status, indent=2) + "\n",
        encoding="utf-8",
    )
    (site / "index.html").write_text("<!doctype html><title>Archive fixture</title>\n", encoding="utf-8")
    manifest = build_manifest(site, allow_local=False)
    (bundle / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return bundle


def archive_member_bytes(path: Path) -> tuple[dict[str, bytes], list[str]]:
    files: dict[str, bytes] = {}
    errors: list[str] = []
    try:
        with tarfile.open(path, mode="r:gz") as archive:
            for member in archive.getmembers():
                try:
                    normalized_member(member.name)
                except ValueError as exc:
                    errors.append(str(exc))
                    continue
                if member.issym() or member.islnk() or member.isdev():
                    errors.append(f"archive member type is forbidden: {member.name}")
                    continue
                if member.isfile():
                    handle = archive.extractfile(member)
                    if handle is None:
                        errors.append(f"archive file member cannot be read: {member.name}")
                    else:
                        files[member.name] = handle.read()
    except (OSError, tarfile.TarError) as exc:
        errors.append(f"archive cannot be parsed: {exc}")
    return files, errors


def validate_candidate(
    candidate: dict,
    output: Path,
    bundle: Path,
    *,
    allow_local: bool,
    policy_path: Path = POLICY,
) -> list[str]:
    errors = validate_against_schema(candidate, load_json(SCHEMA), CANDIDATE_MANIFEST)
    publication = candidate.get("publication", {})
    if publication.get("state") != "local_candidate_not_published":
        errors.append("archive candidate must remain local_candidate_not_published before authorized upload")
    if publication.get("url") != "" or publication.get("authorization_required") is not True:
        errors.append("unpublished archive candidate must have an empty URL and require authorization")
    archive_path = output / str(candidate.get("archive", {}).get("filename", ""))
    if not archive_path.is_file():
        return errors + ["archive candidate file is missing"]
    if sha256_file(archive_path) != candidate.get("archive", {}).get("sha256"):
        errors.append("archive SHA-256 differs from candidate manifest")
    if archive_path.stat().st_size != candidate.get("archive", {}).get("size"):
        errors.append("archive size differs from candidate manifest")
    bundle_manifest_path = bundle / MANIFEST_NAME
    bundle_manifest = load_json(bundle_manifest_path)
    policy = load_json(policy_path)
    if sha256_file(policy_path) != candidate.get("release_policy", {}).get("sha256"):
        errors.append("candidate release-policy digest mismatch")
    release_rows = [
        row for row in policy.get("known_releases", [])
        if row.get("version") == candidate.get("version")
    ]
    if len(release_rows) != 1:
        errors.append("candidate version does not resolve exactly one release-policy row")
    else:
        release = release_rows[0]
        if release.get("source_commit") != candidate.get("source_commit"):
            errors.append("candidate source commit differs from release-policy row")
        if release.get("release_record") != candidate.get("publication", {}).get("release_record"):
            errors.append("candidate release record differs from release-policy row")
        if release.get("site_artifact_state") != "not_published":
            errors.append("candidate policy row must remain not_published before authorized upload")
        if release.get("archive_backfill_decision") == "declined_historical_render_not_available":
            errors.append("candidate policy row declines historical archive backfill")
        expected_filename = str(policy["immutable_channel"]["artifact_name_template"]).format(
            version=candidate.get("version"),
            source_commit=candidate.get("source_commit"),
        )
        if candidate.get("archive", {}).get("filename") != expected_filename:
            errors.append("candidate archive filename differs from release policy template")
    source_bundle = candidate.get("source_bundle", {})
    if sha256_file(bundle_manifest_path) != source_bundle.get("manifest_sha256"):
        errors.append("candidate source-bundle manifest digest mismatch")
    expected_source = {
        "site_file_count": bundle_manifest["site"]["file_count"],
        "site_total_bytes": bundle_manifest["site"]["total_bytes"],
        "site_tree_sha256": bundle_manifest["site"]["tree_sha256"],
    }
    for field, expected in expected_source.items():
        if source_bundle.get(field) != expected:
            errors.append(f"candidate source-bundle {field} mismatch")
    if candidate.get("source_commit") != bundle_manifest.get("source_commit"):
        errors.append("candidate commit differs from tested bundle commit")
    clean = bundle_manifest.get("source_tree_state") == "clean" and bundle_manifest.get("build_context") == "tested_commit"
    if not allow_local and not clean:
        errors.append("publishable immutable archive must derive from a clean tested commit")
    expected_state = "publishable_clean_candidate" if clean else "diagnostic_dirty_local_candidate"
    if candidate.get("candidate_state") != expected_state:
        errors.append("candidate state does not match tested bundle tree/build context")
    root_directory = str(candidate.get("archive", {}).get("root_directory", ""))
    expected_members = dict(source_members(bundle, root_directory))
    actual_members, member_errors = archive_member_bytes(archive_path)
    errors.extend(member_errors)
    if actual_members != expected_members:
        missing = sorted(set(expected_members) - set(actual_members))
        extra = sorted(set(actual_members) - set(expected_members))
        changed = sorted(name for name in set(actual_members) & set(expected_members) if actual_members[name] != expected_members[name])
        errors.append(f"archive contents differ from tested bundle: missing={missing[:3]}, extra={extra[:3]}, changed={changed[:3]}")
    if len(actual_members) != candidate.get("archive", {}).get("member_count"):
        errors.append("archive member_count differs from regular file members")
    replay = archive_bytes(source_members(bundle, root_directory), root_directory)
    if sha256_bytes(replay) != candidate.get("archive", {}).get("sha256"):
        errors.append("deterministic archive replay digest differs")
    return errors


def path_traversal_archive(path: Path) -> None:
    with tarfile.open(path, mode="w:gz") as archive:
        body = b"escape"
        info = tarfile.TarInfo("../escape.txt")
        info.size = len(body)
        archive.addfile(info, io.BytesIO(body))


def negative_controls(
    candidate: dict,
    output: Path,
    bundle: Path,
    *,
    allow_local: bool,
    policy_path: Path = POLICY,
) -> list[str]:
    failures: list[str] = []
    wrong_commit = copy.deepcopy(candidate)
    wrong_commit["source_commit"] = "f" * 40
    if not validate_candidate(wrong_commit, output, bundle, allow_local=allow_local, policy_path=policy_path):
        failures.append("negative control incorrectly accepted: wrong source commit")

    published_without_url = copy.deepcopy(candidate)
    published_without_url["publication"]["state"] = "published"
    if not validate_candidate(published_without_url, output, bundle, allow_local=allow_local, policy_path=policy_path):
        failures.append("negative control incorrectly accepted: false published state")

    original_archive = output / candidate["archive"]["filename"]
    mutated_archive = output / "mutated.tar.gz"
    mutated_archive.write_bytes(original_archive.read_bytes() + b"mutation")
    changed = copy.deepcopy(candidate)
    changed["archive"]["filename"] = mutated_archive.name
    if not validate_candidate(changed, output, bundle, allow_local=allow_local, policy_path=policy_path):
        failures.append("negative control incorrectly accepted: archive byte mutation")

    traversal_path = output / "traversal.tar.gz"
    path_traversal_archive(traversal_path)
    files, traversal_errors = archive_member_bytes(traversal_path)
    if files or not traversal_errors:
        failures.append("negative control incorrectly accepted: path traversal member")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--candidate", type=Path, default=Path("build/immutable-site-archive"))
    parser.add_argument("--version", default="v1.0.0")
    parser.add_argument("--policy", type=Path, default=POLICY)
    parser.add_argument("--allow-local", action="store_true")
    parser.add_argument("--self-test", action="store_true", help="build a temporary candidate before validation")
    args = parser.parse_args()
    bundle = args.bundle if args.bundle.is_absolute() else ROOT / args.bundle
    policy_path = args.policy if args.policy.is_absolute() else ROOT / args.policy
    if args.self_test:
        self_test_version = "v9.9.9" if args.version == "v1.0.0" else args.version
        with tempfile.TemporaryDirectory(prefix="asi-immutable-archive-") as temp:
            temp_root = Path(temp)
            output = temp_root / "candidate"
            bundle = build_self_test_bundle(temp_root)
            bundle_manifest = load_json(bundle / MANIFEST_NAME)
            policy = copy.deepcopy(load_json(policy_path))
            matches = [
                row for row in policy.get("known_releases", [])
                if row.get("version") == self_test_version
                and row.get("source_commit") == bundle_manifest.get("source_commit")
            ]
            if len(matches) != 1:
                policy["known_releases"] = [
                    {
                        "version": self_test_version,
                        "source_commit": bundle_manifest["source_commit"],
                        "release_record": policy["known_releases"][0]["release_record"],
                        "source_release_url": "https://example.invalid/self-test-release",
                        "site_artifact_state": "not_published",
                        "site_artifact_url": "",
                        "site_artifact_sha256": "",
                        "archive_backfill_decision": "not_applicable_archive_expected",
                        "archive_backfill_decision_date": "2000-01-01",
                        "archive_backfill_rationale": "Synthetic self-test release expects a clean archive candidate.",
                        "non_claim": "Synthetic self-test policy row; no release or archive is published."
                    }
                ]
            self_test_policy = temp_root / "self-test-policy.json"
            self_test_policy.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
            try:
                candidate = build_candidate(
                    bundle,
                    output,
                    self_test_version,
                    allow_local=False,
                    policy_path=self_test_policy,
                )
            except (KeyError, OSError, TypeError, ValueError) as exc:
                raise SystemExit(f"could not build archive self-test candidate: {exc}") from exc
            errors = validate_candidate(
                candidate,
                output,
                bundle,
                allow_local=False,
                policy_path=self_test_policy,
            )
            errors.extend(negative_controls(
                candidate,
                output,
                bundle,
                allow_local=False,
                policy_path=self_test_policy,
            ))
    else:
        output = args.candidate if args.candidate.is_absolute() else ROOT / args.candidate
        manifest_path = output / CANDIDATE_MANIFEST
        if not manifest_path.is_file():
            raise SystemExit(f"archive candidate manifest is missing: {manifest_path}")
        candidate = load_json(manifest_path)
        errors = validate_candidate(candidate, output, bundle, allow_local=args.allow_local, policy_path=policy_path)
        errors.extend(negative_controls(candidate, output, bundle, allow_local=args.allow_local, policy_path=policy_path))
    if not DOC.is_file():
        errors.append(f"missing {DOC.relative_to(ROOT)}")
    if errors:
        print("Immutable site archive validation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)
    print(
        f"Immutable site archive validation passed: {candidate['version']} {candidate['candidate_state']}, "
        f"{candidate['archive']['member_count']} members, deterministic SHA-256 replay, "
        "and 4 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
