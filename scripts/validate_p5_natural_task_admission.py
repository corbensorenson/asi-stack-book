#!/usr/bin/env python3
"""Validate P5 natural-task admission without opening a canonical task."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/admit_p5_natural_task.py"
CANDIDATE_SCHEMA = ROOT / "schemas/p5_natural_task_candidate.schema.json"
ADMISSION_SCHEMA = ROOT / "schemas/p5_natural_task_admission.schema.json"
CUSTODY_SCHEMA = ROOT / "schemas/p5_natural_task_intake_custody.schema.json"
CUSTODY = ROOT / "experiments/governed_operations_argument_exit/intake_custody.json"
PREREG = ROOT / "experiments/governed_operations_argument_exit/preregistration.json"
ADMISSIONS = ROOT / "experiments/governed_operations_argument_exit/task_admissions"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def schema_errors(value: Any, schema: Path) -> list[str]:
    return [
        error.message
        for error in sorted(
            Draft202012Validator(load(schema)).iter_errors(value),
            key=lambda error: list(error.absolute_path),
        )
    ]


def load_admitter():
    spec = importlib.util.spec_from_file_location("admit_p5_natural_task", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import admission script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate(
    *,
    family: str,
    index: int,
    head: str,
    tree: str,
    root: Path,
) -> dict[str, Any]:
    discovery = root / "discovery" / f"{family}-{index}.txt"
    surface = root / "surface.txt"
    return {
        "schema_version": "asi_stack.p5_natural_task_candidate.v1",
        "campaign_id": "governed-operations-natural-service-campaign-001",
        "discovered_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "family": family,
        "task_statement": f"Repair independently observed maintenance defect {index} in {family} while preserving the frozen acceptance surface.",
        "independently_needed_reason": "The committed discovery evidence records a maintenance defect that must be resolved for the maintained repository, independent of campaign demand.",
        "discovery_evidence": {
            "kind": "tracked_surface",
            "locator": str(discovery.relative_to(root)),
            "sha256": sha(discovery),
            "observed_before_solution_investigation": True,
        },
        "source_snapshot": {
            "commit": head,
            "tree": tree,
            "surfaces": [{"path": "surface.txt", "sha256": sha(surface)}],
        },
        "acceptance_contract": {
            "checks": [{"argv": ["python3", "-c", "raise SystemExit(0)"], "expected_exit_code": 0}],
            "terminal_conditions": ["The committed source surface matches its frozen expected digest after repair."],
        },
        "effect_surfaces": ["filesystem", "validation_worker"],
        "eligibility_attestations": {
            "independently_necessary": True,
            "invented_for_campaign": False,
            "already_solved": False,
            "solution_investigated": False,
            "outcome_inspected": False,
            "acceptance_defined_before_outcome": True,
            "public_safe": True,
            "requires_another_human": False,
            "uncontrolled_public_effect": False,
            "p2_q1_q2_overlap": False,
            "prior_p4_p5_prompt_exposure": False,
            "subjective_preference_required": False,
        },
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    failures: list[str] = []
    custody = load(CUSTODY)
    failures.extend(f"canonical custody schema: {message}" for message in schema_errors(custody, CUSTODY_SCHEMA))
    if (
        custody.get("state") != "future_intake_initialized_content_closed"
        or custody.get("development_task_ids") != []
        or custody.get("heldout_task_ids") != []
        or custody.get("task_content_opened") != 0
        or custody.get("protected_outcomes_opened") is not False
        or ADMISSIONS.exists()
    ):
        failures.append("canonical campaign custody opened task content or outcomes")
    script_text = SCRIPT.read_text(encoding="utf-8")
    for fragment in [
        "--candidate",
        "--write",
        "admission_lock",
        "requalification_required_before_execution",
        "heldout_content_redacted",
    ]:
        if fragment not in script_text:
            failures.append(f"admission command missing required contract fragment: {fragment}")

    admitter = load_admitter()
    with tempfile.TemporaryDirectory(prefix="p5-natural-admission-") as tmp:
        base = Path(tmp)
        lock_target = base / "lock-target.json"
        with admitter.admission_lock(lock_target):
            try:
                with admitter.admission_lock(lock_target):
                    failures.append("concurrent admission lock was accepted")
            except ValueError:
                pass
        if lock_target.with_suffix(".json.admission.lock").exists():
            failures.append("admission lock was not released")
        repo = base / "repo"
        candidate_dir = base / "candidate-inputs"
        custody_path = base / "intake_custody.json"
        admissions_dir = base / "admissions"
        (repo / "experiments/governed_operations_argument_exit").mkdir(parents=True)
        shutil.copy2(PREREG, repo / "experiments/governed_operations_argument_exit/preregistration.json")
        (repo / "discovery").mkdir()
        (repo / "surface.txt").write_text("frozen source surface\n", encoding="utf-8")
        families = load(PREREG)["service"]["task_families"]
        for family in families:
            for index in range(11):
                (repo / "discovery" / f"{family}-{index}.txt").write_text(
                    f"observed defect {family} {index}\n", encoding="utf-8"
                )
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        git(repo, "config", "user.name", "P5 admission validator")
        git(repo, "config", "user.email", "p5-admission@example.invalid")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "freeze validation fixture")
        head = git(repo, "rev-parse", "HEAD")
        tree = git(repo, "rev-parse", "HEAD^{tree}")
        write_json(custody_path, custody)

        records: list[dict[str, Any]] = []
        first_candidate: dict[str, Any] | None = None
        first_candidate_path: Path | None = None
        for family in families:
            family_records = []
            for index in range(11):
                value = candidate(family=family, index=index, head=head, tree=tree, root=repo)
                candidate_path = candidate_dir / f"{family}-{index}.json"
                write_json(candidate_path, value)
                if first_candidate is None:
                    first_candidate = deepcopy(value)
                    first_candidate_path = candidate_path
                record, next_custody = admitter.build_admission(
                    root=repo,
                    candidate_path=candidate_path,
                    custody_path=custody_path,
                    admissions_dir=admissions_dir,
                    candidate_schema=CANDIDATE_SCHEMA,
                    custody_schema=CUSTODY_SCHEMA,
                    admission_schema=ADMISSION_SCHEMA,
                    admitted_at_utc="2026-08-14T00:00:00Z",
                )
                if schema_errors(record, ADMISSION_SCHEMA):
                    failures.append(f"valid admission failed schema: {record['task_id']}")
                receipt = admissions_dir / record["task_id"] / "admission.json"
                write_json(receipt, record)
                write_json(custody_path, next_custody)
                records.append(record)
                family_records.append(record)
            counts = {
                assignment: sum(row["assignment"] == assignment for row in family_records)
                for assignment in ("development", "heldout")
            }
            if counts != {"development": 3, "heldout": 8}:
                failures.append(f"seeded family assignment drift: {family}: {counts}")

        final_custody = load(custody_path)
        if (
            len(final_custody["development_task_ids"]) != 15
            or len(final_custody["heldout_task_ids"]) != 40
            or final_custody["task_content_opened"] != 15
            or final_custody["state"] != "denominator_full_outcomes_closed"
        ):
            failures.append("full seeded denominator did not reconcile to 15 development and 40 heldout")
        if any(row["development_content"] is not None or not row["heldout_content_redacted"] for row in records if row["assignment"] == "heldout"):
            failures.append("heldout admission leaked protected task content")
        if any(row["development_content"] is None or row["heldout_content_redacted"] for row in records if row["assignment"] == "development"):
            failures.append("development admission omitted its executable task contract")
        if any(row["natural_task_outcome_opened"] or row["fault_outcome_opened"] for row in records):
            failures.append("admission opened an outcome")
        if len({tuple(row["arm_execution_order"]) for row in records}) < 2:
            failures.append("seeded arm order did not vary across task identities")

        assert first_candidate is not None and first_candidate_path is not None
        negative_controls = [
            ("invented task", ("eligibility_attestations", "invented_for_campaign"), True),
            ("already solved", ("eligibility_attestations", "already_solved"), True),
            ("solution investigated", ("eligibility_attestations", "solution_investigated"), True),
            ("outcome inspected", ("eligibility_attestations", "outcome_inspected"), True),
            ("late acceptance", ("eligibility_attestations", "acceptance_defined_before_outcome"), False),
            ("private task", ("eligibility_attestations", "public_safe"), False),
            ("human dependency", ("eligibility_attestations", "requires_another_human"), True),
            ("public effect", ("eligibility_attestations", "uncontrolled_public_effect"), True),
            ("P2 overlap", ("eligibility_attestations", "p2_q1_q2_overlap"), True),
            ("prior exposure", ("eligibility_attestations", "prior_p4_p5_prompt_exposure"), True),
            ("subjective preference", ("eligibility_attestations", "subjective_preference_required"), True),
            ("false necessity", ("eligibility_attestations", "independently_necessary"), False),
            ("source commit drift", ("source_snapshot", "commit"), "0" * 40),
            ("surface digest drift", ("source_snapshot", "surfaces", 0, "sha256"), "0" * 64),
            ("discovery digest drift", ("discovery_evidence", "sha256"), "0" * 64),
        ]
        rejected = 0
        empty_custody = base / "negative-custody.json"
        write_json(empty_custody, custody)
        for index, (name, path, replacement) in enumerate(negative_controls):
            mutated = deepcopy(first_candidate)
            target: Any = mutated
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            mutation_path = candidate_dir / f"negative-{index}.json"
            write_json(mutation_path, mutated)
            try:
                admitter.build_admission(
                    root=repo,
                    candidate_path=mutation_path,
                    custody_path=empty_custody,
                    admissions_dir=base / f"negative-admissions-{index}",
                    candidate_schema=CANDIDATE_SCHEMA,
                    custody_schema=CUSTODY_SCHEMA,
                    admission_schema=ADMISSION_SCHEMA,
                    admitted_at_utc="2026-08-14T00:00:00Z",
                )
            except (ValueError, KeyError):
                rejected += 1
            else:
                failures.append(f"negative control accepted: {name}")

        duplicate_rejected = False
        duplicate_variant = deepcopy(first_candidate)
        duplicate_variant["discovered_at_utc"] = "2026-08-13T00:00:00Z"
        duplicate_variant_path = candidate_dir / "duplicate-metadata-variant.json"
        write_json(duplicate_variant_path, duplicate_variant)
        try:
            admitter.build_admission(
                root=repo,
                candidate_path=duplicate_variant_path,
                custody_path=custody_path,
                admissions_dir=admissions_dir,
                candidate_schema=CANDIDATE_SCHEMA,
                custody_schema=CUSTODY_SCHEMA,
                admission_schema=ADMISSION_SCHEMA,
                admitted_at_utc="2026-08-14T00:00:00Z",
            )
        except ValueError:
            duplicate_rejected = True
        if not duplicate_rejected:
            failures.append("duplicate admission was accepted")

        orphan_dir = base / "orphan-admission"
        write_json(orphan_dir / records[0]["task_id"] / "admission.json", records[0])
        try:
            admitter.build_admission(
                root=repo,
                candidate_path=first_candidate_path,
                custody_path=empty_custody,
                admissions_dir=orphan_dir,
                candidate_schema=CANDIDATE_SCHEMA,
                custody_schema=CUSTODY_SCHEMA,
                admission_schema=ADMISSION_SCHEMA,
                admitted_at_utc="2026-08-14T00:00:00Z",
            )
        except ValueError:
            rejected += 1
        else:
            failures.append("orphan admission receipt was accepted")

        missing_receipt_custody = deepcopy(custody)
        missing_receipt_custody["state"] = "development_intake_active"
        missing_receipt_custody["development_task_ids"] = [records[0]["task_id"]]
        missing_receipt_custody["task_content_opened"] = 1
        missing_receipt_path = base / "missing-receipt-custody.json"
        write_json(missing_receipt_path, missing_receipt_custody)
        try:
            admitter.build_admission(
                root=repo,
                candidate_path=first_candidate_path,
                custody_path=missing_receipt_path,
                admissions_dir=base / "missing-receipt-admissions",
                candidate_schema=CANDIDATE_SCHEMA,
                custody_schema=CUSTODY_SCHEMA,
                admission_schema=ADMISSION_SCHEMA,
                admitted_at_utc="2026-08-14T00:00:00Z",
            )
        except ValueError:
            rejected += 1
        else:
            failures.append("custody identity without an admission receipt was accepted")

    if failures:
        raise SystemExit("P5 natural-task admission validation failed:\n - " + "\n - ".join(failures))
    print(
        "P5 natural-task admission passed: canonical custody remains 0 tasks; "
        "seeded 15-development/40-heldout fixture allocation, heldout redaction, "
        f"five-arm/fault binding, {rejected + 1} rejecting controls, and no outcome/support/release effect."
    )


if __name__ == "__main__":
    main()
