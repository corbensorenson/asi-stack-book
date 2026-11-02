#!/usr/bin/env python3
"""Stage chapter candidates; explicitly requested admission requires the full deep gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys

from projection_files import ProjectionFiles
from schema_validation import validate_value
from validation_runtime import execute
from admission_guard import canonical_access

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_VERSION = "asi_stack.chapter_proposal.v1"
STAGE_VERSION = "asi_stack.chapter_admission_stage.v2"
# Candidate data cannot replace the acceptance machinery that checks it. Any
# necessary validator change is a separate reviewed repository change first.
CHECKING_OWNERS = {"scripts", "schemas", "validation", "ci", ".github", "lean", "skills", "prompts", "tests"}
# Chapter admission consumes existing evidence and source identities. It is
# not an evidence transition, campaign, release, source-ingestion or authority
# update. Make those changes through their named owners before a new proposal.
CUSTODY_OWNERS = {
    "_archive", "archive", "experiments", "sources", "release_records",
    "evidence_transitions", "external_reviews", "claim_revisions",
    "roadmap_records", "status", "governance",
}
REQUIRED_CHECKS = {
    "validate_publication.py", "validate_chapter_handoffs.py",
    "validate_chapter_substance_contract.py", "validate_chapter_review_burndown.py",
    "validate_core_claim_decisions.py", "validate_claim_atom_registry.py",
    "audit_reader_continuity.py", "validate_human_reader_current.py",
    "validate_p6_9_proof_evidence_handoff.py",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or path.as_posix() != value or any(
        part in {".", "..", ".git", ".lake"} for part in path.parts
    ) or path.parts[0] in {"build", "_site", ".quarto"} or "\\" in value or any(ord(character) < 32 for character in value):
        raise ValueError(f"not a canonical source path: {value!r}")
    return value


def regular_file(root: Path, relative: str) -> Path:
    path = root / relative_path(relative)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"source path traverses a link: {relative}")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"source path is not a regular file: {relative}")
    return path


def chapter_rows(structure: dict) -> list[dict]:
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def candidate_manifest(root: Path, proposal: dict, patch: Path) -> tuple[dict, dict, dict, str]:
    if proposal.get("schema_version") != PROPOSAL_VERSION or proposal.get("admission_state") != "not_admitted":
        raise ValueError("candidate requires a non-admitted chapter proposal")
    inputs = {relative: regular_file(root, relative).read_bytes() for relative in
              ("book_structure.json", "sources/source_inventory.json", "schemas/book_structure.schema.json")}
    input_hashes = {relative: hashlib.sha256(body).hexdigest() for relative, body in inputs.items()}
    for key, relative in (("manifest_sha256", "book_structure.json"),
                          ("source_inventory_sha256", "sources/source_inventory.json")):
        if proposal.get(key) != input_hashes[relative]:
            raise ValueError(f"proposal is stale against {relative}; prepare a new proposal")
    current = json.loads(inputs["book_structure.json"])
    candidate_bytes = regular_file(patch, "book_structure.json").read_bytes()
    candidate = json.loads(candidate_bytes)
    schema = json.loads(inputs["schemas/book_structure.schema.json"])
    baseline_errors = validate_value(current, schema, "current book_structure.json")
    if baseline_errors:
        raise ValueError("original manifest is not usable: " + "; ".join(baseline_errors[:12]))
    errors = validate_value(candidate, schema, "candidate book_structure.json")
    if errors:
        raise ValueError("incomplete candidate manifest: " + "; ".join(errors[:12]))
    chapter_id = proposal.get("chapter", {}).get("id", "")
    if not isinstance(chapter_id, str) or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", chapter_id):
        raise ValueError("proposal has an invalid chapter ID")
    matches = [chapter for chapter in chapter_rows(candidate) if chapter["id"] == chapter_id]
    if len(matches) != 1 or any(chapter["id"] == chapter_id for chapter in chapter_rows(current)):
        raise ValueError("candidate must introduce exactly one previously unowned chapter ID")
    chapter = matches[0]
    if chapter["title"] != proposal["chapter"]["title"] or chapter["file"] != f"chapters/{chapter_id}.qmd":
        raise ValueError("candidate changed the proposal title or canonical chapter path")
    destination = root / chapter["file"]
    if destination.exists() or destination.is_symlink():
        raise ValueError("candidate chapter path already has a repository object")
    if chapter["evidence_level"] != "argument" or chapter["claim_label"] not in {"Design rationale", "Speculative", "Hypothesized"}:
        raise ValueError("chapter birth cannot infer stronger evidence from successful infrastructure checks")
    inventory = json.loads(inputs["sources/source_inventory.json"])
    known = {record["id"] for record in inventory}
    used = set(chapter["source_ids"])
    used.update(mapping["source_id"] for mapping in chapter["claim_source_mappings"])
    for key in ("primary", "supporting", "variants", "connector_or_recovery"):
        used.update(chapter["source_queue"][key])
    if used - known:
        raise ValueError(f"candidate references unknown sources: {sorted(used - known)}")
    # Remove only the declared insertion. All old owners/order and book-level
    # metadata must survive unchanged, including every old support state.
    restored = copy.deepcopy(candidate)
    part = next((part for part in restored["parts"] if part["id"] == proposal.get("part_id")), None)
    position = proposal.get("insert_at")
    if part is None or type(position) is not int or not 0 <= position < len(part["chapters"]) or part["chapters"][position]["id"] != chapter_id:
        raise ValueError("candidate insertion does not match the proposal part and adjacency")
    part["chapters"].pop(position)
    if restored != current:
        raise ValueError("candidate must preserve existing manifest owners, order, metadata and support states")
    body = regular_file(patch, chapter["file"]).read_text(encoding="utf-8")
    if not body.strip() or "No manifest " in body:
        raise ValueError("candidate requires authored chapter prose, not a generated placeholder")
    return candidate, chapter, input_hashes, hashlib.sha256(candidate_bytes).hexdigest()


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True, timeout=120).stdout


def git_identity(root: Path) -> dict:
    return {"head": git(root, "rev-parse", "HEAD").decode().strip(),
            "index_sha256": hashlib.sha256(git(root, "ls-files", "--stage", "-z")).hexdigest()}


def source_paths(root: Path, registry: dict) -> list[str]:
    # Include dirty tracked source bytes and explicitly registered new files.
    # Untracked personal/attempt directories and ignored protected caches are
    # deliberately absent, rather than discovered by a recursive copytree.
    paths = {relative_path(value.decode()) for value in git(root, "ls-files", "--cached", "-z").split(b"\0") if value}
    for value in registry["required_artifacts"]:
        relative = relative_path(value)
        path = root / relative
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f"registered source path traverses a link: {relative}")
        if path.is_dir():
            # Required directories add no authority to copy unknown descendants.
            continue
        regular_file(root, relative)
        paths.add(relative)
    for relative in paths:
        regular_file(root, relative)
    return sorted(paths)


def snapshot(root: Path, paths: list[str]) -> dict[str, dict]:
    return {relative: {"sha256": digest(path := regular_file(root, relative)),
                       "bytes": path.stat().st_size, "mode": stat.S_IMODE(path.stat().st_mode)}
            for relative in paths}


def check_patch_path(relative: str) -> None:
    parts = PurePosixPath(relative_path(relative)).parts
    # Registry inventory is data, but its acceptance contracts are machinery.
    # The separate structural check below admits only artifact additions.
    if (parts[0] in CHECKING_OWNERS and relative != "validation/registry.json") or relative in {".gitignore", ".gitattributes"}:
        raise ValueError(f"candidate patch cannot replace checking machinery: {relative}")
    historical_reader = (parts[:2] == ("editions", "reader_manuscript") and
                         (len(parts) < 3 or parts[2] != "current"))
    if parts[0] in CUSTODY_OWNERS or historical_reader or any(
        name in {"raw", "results", "attempts", "protected"} for name in parts
    ):
        raise ValueError(f"candidate patch cannot change protected custody: {relative}")


def check_registry_patch(root: Path, patch: Path, patches: list[str], source_names: list[str], *, require_new: bool) -> None:
    before = json.loads(regular_file(root, "validation/registry.json").read_bytes())
    after = (json.loads(regular_file(patch, "validation/registry.json").read_bytes())
             if "validation/registry.json" in patches else before)
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise ValueError("registry inventory must be an object")
    old, new = before.get("required_artifacts"), after.get("required_artifacts")
    if (not isinstance(old, list) or any(not isinstance(name, str) for name in old)
            or not isinstance(new, list) or any(not isinstance(name, str) for name in new)
            or len(new) != len(set(new)) or [name for name in new if name in old] != old):
        raise ValueError("registry inventory must retain every existing artifact in order without duplicates")
    added = set(new) - set(old)
    for name in added:
        check_patch_path(name)
        if name not in patches:
            raise ValueError(f"new registry artifact must be a candidate data file: {name}")
        regular_file(patch, name)
    if "validation/registry.json" in patches:
        normalized = copy.deepcopy(after)
        normalized["required_artifacts"] = old
        summary = normalized.get("summary")
        if (not isinstance(summary, dict) or type(summary.get("required_artifact_count")) is not int
                or summary["required_artifact_count"] != len(new)):
            raise ValueError("candidate registry inventory count must match its artifact list")
        summary["required_artifact_count"] = before.get("summary", {}).get("required_artifact_count")
        if (json.dumps(normalized, sort_keys=True, allow_nan=False, separators=(",", ":")) !=
                json.dumps(before, sort_keys=True, allow_nan=False, separators=(",", ":"))):
            raise ValueError("candidate registry cannot change validator units, contracts, arguments or other checking machinery")
    if require_new:
        missing = set(patches) - set(source_names) - set(new)
        if missing:
            raise ValueError(f"canonical admission requires registration of every new candidate file: {sorted(missing)}")


def patch_paths(patch: Path) -> list[str]:
    paths = []
    for path in patch.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"candidate patch contains a link: {path}")
        if path.is_dir():
            continue
        relative = relative_path(path.relative_to(patch).as_posix())
        regular_file(patch, relative)
        check_patch_path(relative)
        paths.append(relative)
    return sorted(paths)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    # Never hard-link: validators and generators may change staged files.
    if sys.platform == "darwin":
        result = subprocess.run(["cp", "-c", "-p", str(source), str(target)],
                                capture_output=True, timeout=30, check=False)
        if result.returncode == 0:
            return
    shutil.copy2(source, target)


def prepare(root: Path, proposal: dict, patch: Path, stage: Path, *, validate: bool = False, full: bool = False,
            install: bool = False) -> dict:
    with canonical_access(root, write=install) as lease:
        return _prepare(root, proposal, patch, stage, validate=validate, full=full or install, install=install, lease=lease)


def _prepare(root: Path, proposal: dict, patch: Path, stage: Path, *, validate: bool, full: bool, install: bool, lease: int) -> dict:
    if not patch.is_dir() or patch.is_symlink() or any(parent.is_symlink() for parent in patch.parents):
        raise ValueError("candidate patch must be a real directory without link traversal")
    root, patch = root.resolve(), patch.resolve()
    # Never enumerate the source repository (or an arbitrary ancestor) as a
    # patch. Only the explicitly authored ignored candidate tree is inspected.
    if not patch.is_relative_to(root / "build"):
        raise ValueError("choose a separate candidate patch below build/")
    # Check the lexical path too; resolving a link must not authorize replacing
    # its target or traversing an existing diagnostic directory.
    if stage.is_symlink() or any(parent.is_symlink() for parent in stage.parents):
        raise ValueError("staging path must not traverse a link")
    stage = stage.resolve()
    if not stage.is_relative_to(root / "build") or stage.exists() or patch == stage or patch.is_relative_to(stage) or stage.is_relative_to(patch):
        raise ValueError("choose a fresh staging directory below build/; existing content is preserved")
    patches = patch_paths(patch)
    patch_before = snapshot(patch, patches)
    _, chapter, inspected_hashes, candidate_hash = candidate_manifest(root, proposal, patch)
    registry_bytes = regular_file(root, "validation/registry.json").read_bytes()
    registry = json.loads(registry_bytes)
    actual = {unit["script"] for unit in registry["units"]}
    if REQUIRED_CHECKS - actual:
        raise ValueError(f"admission checks are not registered: {sorted(REQUIRED_CHECKS - actual)}")
    paths = source_paths(root, registry)
    check_registry_patch(root, patch, patches, paths, require_new=install)
    before = snapshot(root, paths)
    source_git = git_identity(root)
    inspected_hashes["validation/registry.json"] = hashlib.sha256(registry_bytes).hexdigest()
    if (any(before.get(relative, {}).get("sha256") != value for relative, value in inspected_hashes.items())
        or candidate_hash != patch_before["book_structure.json"]["sha256"]
        or snapshot(patch, patches) != patch_before or patch_paths(patch) != patches):
        raise ValueError("inspected candidate, registry or source changed before preparation")
    # Fallback filesystems need a complete independent copy; reserve its
    # uncompressed size even when APFS will normally use copy-on-write clones.
    needed = sum(row["bytes"] for row in before.values()) + sum(row["bytes"] for row in patch_before.values())
    if shutil.disk_usage(root).free < needed + 128 * 1024 * 1024:
        raise ValueError("insufficient space for an independent candidate workspace and diagnostics")
    stage.mkdir(parents=True, mode=0o700)
    receipt_path = stage / "admission.json"
    receipt = {"schema_version": STAGE_VERSION, "admission_state": "not_admitted", "status": "incomplete",
               "chapter_id": chapter["id"], "proposal": proposal, "source_files": before, "source_git": source_git,
               "patch_files": patch_before, "support_state_effect": "none", "validation": None,
               "scope": "Isolated candidate preparation; no canonical install or publication. Selected checks do not substitute for full CI or authored review."}
    files = ProjectionFiles()
    files.write(receipt_path, json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    try:
        workspace = stage / "workspace"
        # Local, read-only object alternates provide historical custody without
        # copying protected caches, Git hooks/config, or changing the source index.
        git(root, "clone", "--shared", "--no-checkout", "--no-hardlinks", "--", str(root), str(workspace))
        git(workspace, "read-tree", "HEAD")
        origin = git(root, "remote", "get-url", "origin").decode().strip()
        git(workspace, "remote", "set-url", "origin", origin)
        for relative in paths:
            copy_file(regular_file(root, relative), workspace / relative)
        for relative in patches:
            copy_file(regular_file(patch, relative), workspace / relative)
        expected = {**before, **patch_before}
        if snapshot(root, paths) != before or source_paths(root, registry) != paths or git_identity(root) != source_git or snapshot(patch, patches) != patch_before or patch_paths(patch) != patches:
            raise ValueError("source or candidate patch changed during preparation; start with a stable snapshot")
        if snapshot(workspace, list(expected)) != expected:
            raise ValueError("candidate workspace differs from the inspected source and patch")
        receipt["status"] = "prepared_unvalidated"
        if validate or full:
            command = [sys.executable, str(workspace / "scripts/run_validation_registry.py"), "--tier", "deep",
                       "--report", str(workspace / "build/chapter-admission-validation.json")]
            if not full:
                for script in sorted(REQUIRED_CHECKS):
                    command.extend(["--select", script])
            result = execute(command, cwd=workspace, log=stage / "validation.log", timeout=7200 if full else 1800)
            report_path = workspace / "build/chapter-admission-validation.json"
            from canonical_admission_transaction import control_with_digest
            report, report_digest = control_with_digest(report_path) if report_path.is_file() else (None, None)
            receipt["validation"] = {"mode": "full_deep" if full else "selected_birth_checks", "execution": result,
                                     "report_sha256": report_digest}
            # A zero exit cannot stand in for a complete runner report. A check
            # that changes copied source data also cannot accept its own rewrite.
            from run_validation_registry import select_units
            selected = select_units(registry, "deep", [] if full else sorted(REQUIRED_CHECKS))
            expected_units = {"base-gate", *(unit["id"] for unit in selected)}
            observations = report.get("units", []) if isinstance(report, dict) else []
            observed_units = {row.get("unit_id") for row in observations}
            accepted = (result["status"] == "passed" and isinstance(report, dict) and report.get("status") == "pass"
                        and report.get("registry_sha256") == {"validation/registry.json": expected["validation/registry.json"]["sha256"]}
                        and report.get("registry_drift") is False
                        and observed_units == expected_units and len(observations) == len(expected_units)
                        and all(row.get("status") == "passed" for row in observations)
                        and control_with_digest(report_path)[1] == report_digest
                        and snapshot(workspace, list(expected)) == expected)
            receipt["status"] = "full_deep_passed_not_admitted" if accepted and full else "birth_checks_passed_not_admitted" if accepted else "rejected"
        if snapshot(root, paths) != before or source_paths(root, registry) != paths or git_identity(root) != source_git or snapshot(patch, patches) != patch_before or patch_paths(patch) != patches:
            raise ValueError("source or candidate changed while staged validation ran; candidate is stale")
        receipt["canonical_source_unchanged"] = True
    except BaseException as error:
        receipt["status"] = "incomplete"
        receipt["error"] = f"{type(error).__name__}: {error}"
        files.write(receipt_path, json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
        raise
    files.write(receipt_path, json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    if install:
        if receipt["status"] != "full_deep_passed_not_admitted":
            raise ValueError("canonical admission requires every selected full-deep gate to pass; candidate remains unadmitted")
        from canonical_admission_transaction import install_candidate
        receipt = install_candidate(root, stage, receipt, lease=lease)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path, help="Separate authored patch tree below build/, including complete book_structure.json and chapter/birth artifact edits")
    parser.add_argument("--stage", required=True, type=Path, help="Fresh diagnostic directory below build/")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--validate", action="store_true", help="Run registered birth checks against the copied workspace")
    mode.add_argument("--full", action="store_true", help="Run the entire deep tier, including PR checks, against the copied workspace")
    mode.add_argument("--install", action="store_true", help="Run the full deep gate and install the intended candidate with a manifest-last recovery journal")
    args = parser.parse_args()
    receipt = prepare(ROOT, json.loads(args.proposal.read_text()), args.candidate, args.stage,
                      validate=args.validate, full=args.full, install=args.install)
    print(json.dumps({key: receipt[key] for key in ("chapter_id", "admission_state", "status", "support_state_effect")}, indent=2))
    if receipt["status"] == "rejected":
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Chapter candidate rejected: {error}")
