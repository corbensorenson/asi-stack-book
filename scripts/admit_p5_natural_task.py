#!/usr/bin/env python3
"""Admit one eligible natural task into the frozen P5 campaign."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any

from jsonschema import Draft202012Validator


CAMPAIGN_ID = "governed-operations-natural-service-campaign-001"
ASSIGNMENT_SEED = 20260728
ARMS = [
    "direct_model_tooling",
    "stop_only",
    "competent_generic_sre",
    "proposal_plus_independent_acceptance",
    "governed_operations",
]
FAMILY_QUOTA = {"development": 3, "heldout": 8}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def seeded_order(values: list[str], namespace: str) -> list[str]:
    return sorted(
        values,
        key=lambda value: sha_bytes(
            f"{ASSIGNMENT_SEED}:{namespace}:{value}".encode("utf-8")
        ),
    )


def assignment_schedule(family: str) -> list[str]:
    slots = [f"development:{index}" for index in range(FAMILY_QUOTA["development"])]
    slots += [f"heldout:{index}" for index in range(FAMILY_QUOTA["heldout"])]
    return [slot.split(":", 1)[0] for slot in seeded_order(slots, family)]


def admission_records(admissions_dir: Path) -> list[dict[str, Any]]:
    records = []
    if admissions_dir.is_dir():
        for path in sorted(admissions_dir.glob("*/admission.json")):
            records.append(load(path))
    return records


@contextmanager
def admission_lock(custody_path: Path):
    """Serialize canonical writes; a surviving lock fails closed for reconciliation."""
    lock_path = custody_path.with_suffix(custody_path.suffix + ".admission.lock")
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ValueError(f"admission lock already exists: {lock_path}") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        os.close(descriptor)
        descriptor = -1
        yield
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        lock_path.unlink(missing_ok=True)


def validate_schema(value: Any, schema_path: Path, label: str) -> None:
    errors = sorted(
        Draft202012Validator(load(schema_path)).iter_errors(value),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"{label} schema failed: {details}")


def verify_existing_custody(
    custody: dict[str, Any],
    existing: list[dict[str, Any]],
    faults: list[str],
) -> None:
    development_ids = set(custody["development_task_ids"])
    heldout_ids = set(custody["heldout_task_ids"])
    if development_ids & heldout_ids:
        raise ValueError("development and heldout custody identities overlap")
    if custody["task_content_opened"] != len(development_ids):
        raise ValueError("development task-content count differs from custody identities")
    existing_ids = {row["task_id"] for row in existing}
    if len(existing_ids) != len(existing):
        raise ValueError("duplicate admission receipt identity requires reconciliation")
    if existing_ids != development_ids | heldout_ids:
        raise ValueError("custody and admission receipt identities require reconciliation")

    family_indexes: dict[str, set[int]] = {
        family: set() for family in custody["task_families"]
    }
    for row in existing:
        task_id = row["task_id"]
        expected_assignment = "development" if task_id in development_ids else "heldout"
        if row["assignment"] != expected_assignment:
            raise ValueError(f"admission assignment differs from custody: {task_id}")
        if row["family"] not in family_indexes:
            raise ValueError(f"admission family differs from frozen custody: {task_id}")
        index = row["family_eligible_index"]
        if index in family_indexes[row["family"]]:
            raise ValueError(f"duplicate family admission index: {row['family']}:{index}")
        family_indexes[row["family"]].add(index)
        schedule = assignment_schedule(row["family"])
        if index >= len(schedule) or row["assignment"] != schedule[index]:
            raise ValueError(f"admission assignment differs from frozen schedule: {task_id}")
        if row["assigned_fault"] not in faults:
            raise ValueError(f"admission fault differs from frozen envelope: {task_id}")
        if set(row["arm_execution_order"]) != set(ARMS):
            raise ValueError(f"admission arm set differs from frozen campaign: {task_id}")
    for family, indexes in family_indexes.items():
        if indexes != set(range(len(indexes))):
            raise ValueError(f"family admission indexes are not contiguous: {family}")


def verify_candidate(
    *,
    root: Path,
    candidate_path: Path,
    candidate: dict[str, Any],
    candidate_schema: Path,
) -> None:
    validate_schema(candidate, candidate_schema, "candidate")
    if inside(candidate_path, root):
        raise ValueError("candidate must remain outside the tracked repository until assignment")

    discovered = datetime.fromisoformat(
        candidate["discovered_at_utc"].replace("Z", "+00:00")
    )
    if discovered.tzinfo is None or discovered > datetime.now(timezone.utc):
        raise ValueError("discovery timestamp must be timezone-aware and not in the future")

    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("tracked source worktree must be clean before task admission")
    head = git(root, "rev-parse", "HEAD")
    tree = git(root, "rev-parse", "HEAD^{tree}")
    snapshot = candidate["source_snapshot"]
    if snapshot["commit"] != head or snapshot["tree"] != tree:
        raise ValueError("candidate source commit/tree does not match the clean admission root")

    for surface in snapshot["surfaces"]:
        path = (root / surface["path"]).resolve()
        if not inside(path, root) or not path.is_file():
            raise ValueError(f"source surface is missing or escapes root: {surface['path']}")
        if sha_file(path) != surface["sha256"]:
            raise ValueError(f"source surface digest drift: {surface['path']}")

    locator = Path(candidate["discovery_evidence"]["locator"]).expanduser()
    if not locator.is_absolute():
        locator = root / locator
    if not locator.is_file() or sha_file(locator) != candidate["discovery_evidence"]["sha256"]:
        raise ValueError("discovery evidence is missing or digest-mismatched")


def build_admission(
    *,
    root: Path,
    candidate_path: Path,
    custody_path: Path,
    admissions_dir: Path,
    candidate_schema: Path,
    custody_schema: Path,
    admission_schema: Path,
    admitted_at_utc: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = load(candidate_path)
    custody = load(custody_path)
    verify_candidate(
        root=root,
        candidate_path=candidate_path,
        candidate=candidate,
        candidate_schema=candidate_schema,
    )
    validate_schema(custody, custody_schema, "custody")
    if custody["campaign_id"] != CAMPAIGN_ID or candidate["campaign_id"] != CAMPAIGN_ID:
        raise ValueError("campaign identity mismatch")
    if candidate["family"] not in custody["task_families"]:
        raise ValueError("task family is outside frozen custody")

    prereg = load(root / "experiments/governed_operations_argument_exit/preregistration.json")
    faults = prereg["fault_envelope"]
    existing = admission_records(admissions_dir)
    for row in existing:
        validate_schema(row, admission_schema, "existing admission")
    verify_existing_custody(custody, existing, faults)
    existing_ids = {row["task_id"] for row in existing}
    candidate_sha = sha_bytes(canonical_bytes(candidate))
    task_statement_sha = sha_bytes(candidate["task_statement"].encode("utf-8"))
    acceptance_contract_sha = sha_bytes(canonical_bytes(candidate["acceptance_contract"]))
    discovery_evidence_sha = candidate["discovery_evidence"]["sha256"]
    task_id = f"p5-natural-{candidate_sha[:20]}"
    if task_id in existing_ids or task_id in custody["development_task_ids"] or task_id in custody["heldout_task_ids"]:
        raise ValueError("candidate is already admitted")
    for row in existing:
        if row["task_statement_sha256"] == task_statement_sha:
            raise ValueError("task statement identity is already admitted")
        if row["discovery_evidence_sha256"] == discovery_evidence_sha:
            raise ValueError("discovery evidence identity is already admitted")
    family = candidate["family"]
    family_index = sum(row.get("family") == family for row in existing)
    schedule = assignment_schedule(family)
    if family_index >= len(schedule):
        raise ValueError(f"frozen family denominator is full: {family}")
    assignment = schedule[family_index]

    next_custody = json.loads(json.dumps(custody))
    target = f"{assignment}_task_ids"
    if len(next_custody[target]) >= next_custody[f"{assignment}_capacity"]:
        raise ValueError(f"frozen {assignment} denominator is full")
    next_custody[target].append(task_id)
    next_custody["task_content_opened"] = len(next_custody["development_task_ids"])
    if len(next_custody["development_task_ids"]) + len(next_custody["heldout_task_ids"]) == 55:
        next_custody["state"] = "denominator_full_outcomes_closed"
    elif assignment == "heldout":
        next_custody["state"] = "heldout_intake_active"
    else:
        next_custody["state"] = "development_intake_active"
    validate_schema(next_custody, custody_schema, "post-admission custody")

    fault = seeded_order(faults, f"{task_id}:fault")[0]
    arm_order = seeded_order(ARMS, f"{task_id}:arms")
    snapshot = candidate["source_snapshot"]
    is_heldout = assignment == "heldout"
    record = {
        "schema_version": "asi_stack.p5_natural_task_admission.v1",
        "campaign_id": CAMPAIGN_ID,
        "task_id": task_id,
        "candidate_sha256": candidate_sha,
        "admitted_at_utc": admitted_at_utc or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "family": family,
        "family_eligible_index": family_index,
        "assignment": assignment,
        "assigned_fault": fault,
        "arm_execution_order": arm_order,
        "source_snapshot": {
            "commit": snapshot["commit"],
            "tree": snapshot["tree"],
            "surface_count": len(snapshot["surfaces"]),
            "surfaces_sha256": sha_bytes(canonical_bytes(snapshot["surfaces"])),
        },
        "discovery_evidence_sha256": discovery_evidence_sha,
        "task_statement_sha256": task_statement_sha,
        "acceptance_contract_sha256": acceptance_contract_sha,
        "development_content": None if is_heldout else {
            "task_statement": candidate["task_statement"],
            "independently_needed_reason": candidate["independently_needed_reason"],
            "acceptance_contract": candidate["acceptance_contract"],
            "effect_surfaces": candidate["effect_surfaces"],
        },
        "heldout_content_redacted": is_heldout,
        "pre_custody_sha256": sha_file(custody_path),
        "post_custody_sha256": sha_bytes(
            json.dumps(next_custody, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        ),
        "natural_task_outcome_opened": False,
        "fault_outcome_opened": False,
        "requalification_required_before_execution": True,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Admission records prospective task identity and custody; it does not establish task success.",
            "The eligibility attestations remain operator assertions and do not prove naturality by themselves.",
            "A development assignment does not authorize execution before campaign requalification.",
            "A held-out assignment exposes only digests and does not open protected task content or outcomes.",
            "No admission establishes usefulness, safety, causal superiority, transfer, support, release, AGI, or ASI.",
        ],
    }
    validate_schema(record, admission_schema, "admission")
    return record, next_custody


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--custody", type=Path)
    parser.add_argument("--admissions-dir", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    custody = args.custody or root / "experiments/governed_operations_argument_exit/intake_custody.json"
    admissions = args.admissions_dir or root / "experiments/governed_operations_argument_exit/task_admissions"
    schemas = root / "schemas"
    def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
        return build_admission(
            root=root,
            candidate_path=args.candidate.resolve(),
            custody_path=custody.resolve(),
            admissions_dir=admissions.resolve(),
            candidate_schema=schemas / "p5_natural_task_candidate.schema.json",
            custody_schema=schemas / "p5_natural_task_intake_custody.schema.json",
            admission_schema=schemas / "p5_natural_task_admission.schema.json",
        )

    if not args.write:
        record, _ = prepare()
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return

    with admission_lock(custody.resolve()):
        record, next_custody = prepare()
        receipt = admissions / record["task_id"] / "admission.json"
        if receipt.exists():
            raise SystemExit("admission receipt already exists")
        atomic_write(receipt, record)
        atomic_write(custody, next_custody)
    print(f"admitted {record['task_id']} as {record['assignment']}; outcomes remain closed")


if __name__ == "__main__":
    main()
