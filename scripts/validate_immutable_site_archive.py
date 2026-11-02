#!/usr/bin/env python3
"""Validate deterministic immutable-site archive candidates and rejection controls."""

from __future__ import annotations

import argparse
import copy
import gzip
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
import tempfile

from build_canonical_public_status import ROOT, build_status, load_json, validate_against_schema
from build_immutable_site_archive import (
    CANDIDATE_MANIFEST,
    FAMILY,
    POLICY,
    archive_bytes,
    build_candidate,
    normalized_member,
    sha256_bytes,
    inspect_bundle, read_regular, policy_label, policy_release,
)
from build_tested_site_bundle import MANIFEST_NAME, build_manifest, file_rows
from generated_directory import RECEIPT, desired_receipt, previous_is_owned


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
    return archive_member_data(read_regular(path))


def archive_member_data(body: bytes, expected: dict[str, bytes] | None = None) -> tuple[dict[str, bytes], list[str]]:
    files: dict[str, bytes] = {}
    errors: list[str] = []
    directories = {parent.as_posix() for name in expected or {} for parent in PurePosixPath(name).parents
                   if parent != PurePosixPath(".")}
    # Bound expansion by the actual inspected bundle, never by untrusted
    # candidate size fields. Include generous header/PAX/block overhead.
    budget = (sum(len(data) for data in expected.values())
              + sum(len(name.encode()) for name in expected)
              + 4096 * (len(expected) + len(directories)) + 20480) if expected is not None else 10 * 1024 * 1024
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(body)) as zipped:
            expanded = zipped.read(budget + 1)
        if len(expanded) > budget:
            return {}, ["archive expansion exceeds the inspected member budget"]
        seen = set()
        with tarfile.open(fileobj=io.BytesIO(expanded), mode="r:") as archive:
            for member in archive:
                try:
                    name = member.name[:-1] if member.isdir() and member.name.endswith("/") else member.name
                    normalized_member(name)
                except ValueError as exc:
                    errors.append(str(exc))
                    break
                if name in seen:
                    errors.append(f"duplicate archive member: {name}")
                    break
                seen.add(name)
                if member.type not in {tarfile.REGTYPE, tarfile.DIRTYPE}:
                    errors.append(f"archive member type is forbidden: {member.name}")
                    break
                if expected is not None and (
                    member.isdir() and name not in directories
                    or member.isfile() and (name not in expected or member.size != len(expected[name]))
                ):
                    errors.append(f"archive member is outside the inspected inventory: {name}")
                    break
                if (member.uid != 0 or member.gid != 0 or member.uname != "" or member.gname != ""
                        or member.mtime != 0 or member.mode != (0o755 if member.isdir() else 0o644)
                        or member.isdir() and member.size != 0):
                    errors.append(f"archive member has noncanonical metadata: {name}")
                    break
                if member.isfile():
                    handle = archive.extractfile(member)
                    if handle is None:
                        errors.append(f"archive file member cannot be read: {member.name}")
                    else:
                        files[name] = handle.read()
    except (OSError, EOFError, tarfile.TarError) as exc:
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
    try:
        before = file_rows(output)
        payload = {row["path"]: read_regular(output / row["path"]) for row in before if row["path"] != RECEIPT}
        inspected = inspect_bundle(bundle, allow_local=allow_local)
        policy_bytes = read_regular(policy_path)
        errors = validate_candidate_payload(candidate, payload, inspected, json.loads(policy_bytes), policy_bytes,
                                            policy_label(policy_path.resolve()), allow_local=allow_local)
        if not errors:
            previous_is_owned(output, desired_receipt(FAMILY, payload, {}))
        if file_rows(output) != before or file_rows(inspected["root"]) != inspected["rows"] or read_regular(policy_path) != policy_bytes:
            errors.append("archive candidate or source inputs changed during validation")
        return errors
    except (OSError, KeyError, TypeError, ValueError) as error:
        return [f"archive candidate custody refused: {error}"]


def validate_candidate_payload(candidate: dict, payload: dict[str, bytes], inspected: dict,
                               policy: dict, policy_bytes: bytes, label: str, *,
                               allow_local: bool, schema: dict | None = None) -> list[str]:
    """Domain acceptance over captured bytes; no filesystem writes or reloads."""
    errors = validate_against_schema(candidate, load_json(SCHEMA) if schema is None else schema, CANDIDATE_MANIFEST)
    if errors:
        return errors
    publication = candidate.get("publication", {})
    if publication.get("state") != "local_candidate_not_published":
        errors.append("archive candidate must remain local_candidate_not_published before authorized upload")
    if publication.get("url") != "" or publication.get("authorization_required") is not True:
        errors.append("unpublished archive candidate must have an empty URL and require authorization")
    filename = candidate["archive"]["filename"]
    try:
        if len(normalized_member(filename).parts) != 1 or not filename.endswith(".tar.gz"):
            raise ValueError("archive filename must be one safe .tar.gz name")
    except ValueError as error:
        return errors + [str(error)]
    if set(payload) != {filename, CANDIDATE_MANIFEST, filename + ".sha256"}:
        errors.append("candidate payload must contain exactly its archive, manifest and checksum")
    if filename not in payload:
        return errors + ["archive candidate file is missing"]
    body = payload[filename]
    try:
        recorded = json.loads(payload.get(CANDIDATE_MANIFEST, b"null"))
        errors.extend(validate_against_schema(recorded, load_json(SCHEMA) if schema is None else schema,
                                             "captured " + CANDIDATE_MANIFEST))
        if recorded != candidate:
            errors.append("candidate manifest bytes differ from the supplied candidate")
    except (ValueError, TypeError) as error:
        errors.append(f"candidate manifest bytes are invalid: {error}")
    if payload.get(filename + ".sha256") != f"{candidate['archive']['sha256']}  {filename}\n".encode():
        errors.append("adjacent archive checksum differs from the candidate")
    if sha256_bytes(body) != candidate.get("archive", {}).get("sha256"):
        errors.append("archive SHA-256 differs from candidate manifest")
    if len(body) != candidate.get("archive", {}).get("size"):
        errors.append("archive size differs from candidate manifest")
    bundle_manifest = inspected["manifest"]
    if sha256_bytes(policy_bytes) != candidate.get("release_policy", {}).get("sha256"):
        errors.append("candidate release-policy digest mismatch")
    if candidate["release_policy"]["path"] != label:
        errors.append("candidate release-policy path label mismatch")
    if candidate["publication"]["storage_authority"] != policy["immutable_channel"]["storage_authority"]:
        errors.append("candidate storage authority differs from its release policy")
    try:
        policy_release(candidate["version"], candidate["source_commit"], policy)
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"candidate release policy rejects: {error}")
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
    if sha256_bytes(inspected["data"][MANIFEST_NAME]) != source_bundle.get("manifest_sha256"):
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
    for field in ("source_tree_state", "build_context"):
        if candidate[field] != bundle_manifest[field]:
            errors.append(f"candidate {field} differs from tested bundle")
    clean = bundle_manifest.get("source_tree_state") == "clean" and bundle_manifest.get("build_context") == "tested_commit"
    if not allow_local and not clean:
        errors.append("publishable immutable archive must derive from a clean tested commit")
    expected_state = "publishable_clean_candidate" if clean else "diagnostic_dirty_local_candidate"
    if candidate.get("candidate_state") != expected_state:
        errors.append("candidate state does not match tested bundle tree/build context")
    root_directory = str(candidate.get("archive", {}).get("root_directory", ""))
    if root_directory != f"asi-stack-site-{candidate['version']}-{candidate['source_commit']}":
        errors.append("archive root directory is not version/commit bound")
    try:
        if len(normalized_member(root_directory).parts) != 1:
            raise ValueError("archive root must be one safe directory name")
    except ValueError as error:
        return errors + [str(error)]
    # Derive completeness from captured bundle bytes, not the producer's
    # source_members transformation: a shared omission would validate itself.
    expected_members = {root_directory + "/" + name: data
                        for name, data in inspected["data"].items()}
    actual_members, member_errors = archive_member_data(body, expected_members)
    errors.extend(member_errors)
    if actual_members != expected_members:
        missing = sorted(set(expected_members) - set(actual_members))
        extra = sorted(set(actual_members) - set(expected_members))
        changed = sorted(name for name in set(actual_members) & set(expected_members) if actual_members[name] != expected_members[name])
        errors.append(f"archive contents differ from tested bundle: missing={missing[:3]}, extra={extra[:3]}, changed={changed[:3]}")
    if len(actual_members) != candidate.get("archive", {}).get("member_count"):
        errors.append("archive member_count differs from regular file members")
    # Byte-level determinism deliberately shares the serializer; independent
    # member/content/metadata checks above remain authoritative for completeness.
    replay = archive_bytes(sorted(expected_members.items()), root_directory)
    if sha256_bytes(replay) != candidate.get("archive", {}).get("sha256"):
        errors.append("deterministic archive replay digest differs")
    return errors


def path_traversal_archive(path: Path) -> None:
    path.write_bytes(path_traversal_bytes())


def path_traversal_bytes() -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:gz") as archive:
        body = b"escape"
        info = tarfile.TarInfo("../escape.txt")
        info.size = len(body)
        archive.addfile(info, io.BytesIO(body))
    return output.getvalue()


def negative_controls(
    candidate: dict,
    output: Path,
    bundle: Path,
    *,
    allow_local: bool,
    policy_path: Path = POLICY,
) -> list[str]:
    failures: list[str] = []
    payload = {row["path"]: read_regular(output / row["path"]) for row in file_rows(output) if row["path"] != RECEIPT}
    inspected = inspect_bundle(bundle, allow_local=allow_local)
    policy_bytes = read_regular(policy_path)
    policy = json.loads(policy_bytes)
    def reject(mutated, data):
        return validate_candidate_payload(mutated, data, inspected, policy, policy_bytes,
                                          policy_label(policy_path.resolve()), allow_local=allow_local)
    def metadata(mutated):
        return {**payload, CANDIDATE_MANIFEST: (json.dumps(mutated, indent=2, ensure_ascii=False) + "\n").encode()}
    wrong_commit = copy.deepcopy(candidate)
    wrong_commit["source_commit"] = "f" * 40
    if not reject(wrong_commit, metadata(wrong_commit)):
        failures.append("negative control incorrectly accepted: wrong source commit")

    published_without_url = copy.deepcopy(candidate)
    published_without_url["publication"]["state"] = "published"
    if not reject(published_without_url, metadata(published_without_url)):
        failures.append("negative control incorrectly accepted: false published state")

    name = candidate["archive"]["filename"]
    if not reject(candidate, {**payload, name: payload[name] + b"mutation"}):
        failures.append("negative control incorrectly accepted: archive byte mutation")

    files, traversal_errors = archive_member_data(path_traversal_bytes())
    if files or not traversal_errors:
        failures.append("negative control incorrectly accepted: path traversal member")
    return failures


def check_candidate(output: Path, bundle: Path, *, allow_local: bool,
                    policy_path: Path = POLICY) -> tuple[dict, list[str]]:
    """Bind the whole positive/control operation to unchanged candidate inputs."""
    before = file_rows(output)
    source_before = file_rows(bundle)
    policy_before = read_regular(policy_path)
    candidate = json.loads(read_regular(output / CANDIDATE_MANIFEST))
    errors = validate_candidate(candidate, output, bundle, allow_local=allow_local,
                                policy_path=policy_path)
    if not errors:
        errors.extend(negative_controls(candidate, output, bundle, allow_local=allow_local,
                                        policy_path=policy_path))
    if (file_rows(output) != before or file_rows(bundle) != source_before
            or read_regular(policy_path) != policy_before):
        errors.append("archive candidate, source bundle or policy changed during the complete validation/control operation")
    return candidate, errors


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
            temp_root = Path(temp).resolve()
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
            candidate, errors = check_candidate(output, bundle, allow_local=False,
                                                policy_path=self_test_policy)
    else:
        output = args.candidate if args.candidate.is_absolute() else ROOT / args.candidate
        candidate, errors = check_candidate(output, bundle, allow_local=args.allow_local,
                                            policy_path=policy_path)
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
    try:
        from admission_guard import canonical_access
        with canonical_access(ROOT):
            main()
    except (OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit(f"Immutable archive validation refused: {error}") from error
