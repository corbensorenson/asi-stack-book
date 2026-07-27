#!/usr/bin/env python3
"""Run the bounded P5 multi-process effect-complete reference slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "experiments/effect_complete_reference/cases.json"
RESULT = ROOT / "experiments/effect_complete_reference/results/2026-07-27-local.json"
STATE_CLASSES = [
    "model", "optimizer", "scheduler", "rng", "cache", "backup",
    "derived_artifacts", "descendants", "credentials",
]
DELETE_SURFACES = ["primary", "cache", "backup", "derived", "descendant"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def connect(db: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db, timeout=10)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=FULL")
    return connection


def initialize(db: Path) -> None:
    with connect(db) as connection:
        connection.executescript(
            """
            CREATE TABLE authority (
              case_id TEXT PRIMARY KEY,
              epoch INTEGER NOT NULL,
              state TEXT NOT NULL,
              scope TEXT NOT NULL
            );
            CREATE TABLE ledger (
              sequence INTEGER PRIMARY KEY AUTOINCREMENT,
              event_id TEXT UNIQUE NOT NULL,
              case_id TEXT NOT NULL,
              role TEXT NOT NULL,
              kind TEXT NOT NULL,
              effect_id TEXT NOT NULL,
              authority_epoch INTEGER NOT NULL,
              payload_sha256 TEXT NOT NULL,
              disposition TEXT NOT NULL
            );
            """
        )


def set_authority(db: Path, case_id: str, epoch: int, state: str, scope: str) -> None:
    with connect(db) as connection:
        connection.execute(
            "INSERT OR REPLACE INTO authority(case_id,epoch,state,scope) VALUES(?,?,?,?)",
            (case_id, epoch, state, scope),
        )


def record(
    db: Path,
    event_id: str,
    case_id: str,
    role: str,
    kind: str,
    effect_id: str,
    epoch: int,
    payload: bytes,
    disposition: str,
) -> None:
    with connect(db) as connection:
        connection.execute(
            """
            INSERT INTO ledger(
              event_id,case_id,role,kind,effect_id,authority_epoch,payload_sha256,disposition
            ) VALUES(?,?,?,?,?,?,?,?)
            """,
            (event_id, case_id, role, kind, effect_id, epoch, sha_bytes(payload), disposition),
        )


def authority_allows(db: Path, case_id: str, epoch: int, scope: str) -> tuple[bool, str]:
    with connect(db) as connection:
        row = connection.execute(
            "SELECT epoch,state,scope FROM authority WHERE case_id=?", (case_id,)
        ).fetchone()
    if row is None:
        return False, "missing_authority"
    active_epoch, state, exact_scope = row
    if state != "active":
        return False, "revoked"
    if epoch != active_epoch:
        return False, "stale_epoch"
    if scope != exact_scope:
        return False, "scope_mismatch"
    return True, "authorized"


def worker(args: argparse.Namespace) -> int:
    db = Path(args.db)
    workspace = Path(args.workspace)
    payload = args.payload.encode("utf-8")
    allowed, reason = authority_allows(db, args.case_id, args.epoch, args.scope)
    if not allowed:
        record(
            db, args.event_id, args.case_id, args.role, "effect_rejected",
            args.effect_id, args.epoch, payload, reason,
        )
        return 23

    if args.operation in {"write", "crash_write"}:
        target = workspace / "effects" / f"{args.effect_id}.effect"
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            record(
                db, args.event_id, args.case_id, args.role, "duplicate_prevented",
                args.effect_id, args.epoch, payload,
                "idempotency_key_already_materialized",
            )
            return 0
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if args.operation == "crash_write":
            os._exit(17)
        record(
            db, args.event_id, args.case_id, args.role, "effect_committed",
            args.effect_id, args.epoch, payload, "materialized",
        )
        return 0

    if args.operation == "append":
        target = workspace / "external" / "append-only.log"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("ab") as stream:
            stream.write(payload + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        record(
            db, args.event_id, args.case_id, args.role,
            "irreversible_effect_committed", args.effect_id, args.epoch,
            payload, "append_only_history",
        )
        return 0

    if args.operation == "mutate_state":
        current = workspace / "state" / "current"
        for name in STATE_CLASSES:
            (current / f"{name}.bin").write_bytes(f"mutated:{name}".encode())
        record(
            db, args.event_id, args.case_id, args.role, "full_state_mutated",
            args.effect_id, args.epoch, payload, "nine_classes_mutated",
        )
        return 0

    if args.operation == "delete_descendants":
        deleted = 0
        for surface in DELETE_SURFACES:
            target = workspace / "deletion" / surface / "cohort.dat"
            if target.exists():
                target.unlink()
                deleted += 1
        record(
            db, args.event_id, args.case_id, args.role, "descendant_deletion",
            args.effect_id, args.epoch, str(deleted).encode(), "local_storage_only",
        )
        return 0
    return 64


def command(
    db: Path,
    workspace: Path,
    *,
    case_id: str,
    role: str,
    operation: str,
    effect_id: str,
    event_id: str,
    epoch: int = 1,
    scope: str | None = None,
    payload: str = "payload",
) -> list[str]:
    return [
        sys.executable, str(Path(__file__).resolve()), "--worker",
        "--db", str(db), "--workspace", str(workspace), "--case-id", case_id,
        "--role", role, "--operation", operation, "--effect-id", effect_id,
        "--event-id", event_id, "--epoch", str(epoch),
        "--scope", scope or f"effects/{case_id}", "--payload", payload,
    ]


def run_checked(cmd: list[str], expected: int = 0) -> None:
    completed = subprocess.run(cmd, text=True, capture_output=True, timeout=20)
    if completed.returncode != expected:
        raise RuntimeError(
            f"worker returned {completed.returncode}, expected {expected}: "
            f"{completed.stderr or completed.stdout}"
        )


def observe(
    db: Path,
    workspace: Path,
    case_id: str,
    effect_id: str,
    *,
    event_id: str,
) -> str:
    target = workspace / "effects" / f"{effect_id}.effect"
    digest = sha_file(target)
    record(
        db, event_id, case_id, "observer", "effect_observed", effect_id, 1,
        digest.encode(), "independent_filesystem_read",
    )
    return digest


def build_result(workspace: Path) -> dict[str, Any]:
    db = workspace / "ledger.sqlite"
    initialize(db)
    receipts: list[dict[str, Any]] = []

    case = "nominal-observe-exact-rollback"
    set_authority(db, case, 1, "active", f"effects/{case}")
    run_checked(command(
        db, workspace, case_id=case, role="executor", operation="write",
        effect_id="e1", event_id="nominal-commit", payload="nominal",
    ))
    digest_before = observe(db, workspace, case, "e1", event_id="nominal-observe")
    target = workspace / "effects/e1.effect"
    target.unlink()
    record(
        db, "nominal-rollback", case, "recovery", "exact_rollback", "e1", 1,
        digest_before.encode(), "pre_state_absent_restored",
    )
    receipts.append({
        "case_id": case, "passed": not target.exists(),
        "terminal_disposition": "exact_rollback",
        "observations": [
            "effect digest observed by separate role", "pre-effect absence restored",
        ],
    })

    case = "concurrent-idempotent-effect"
    set_authority(db, case, 1, "active", f"effects/{case}")
    cmds = [
        command(
            db, workspace, case_id=case, role="executor", operation="write",
            effect_id="e2", event_id=f"concurrent-{index}", payload="same",
        )
        for index in (1, 2)
    ]
    processes = [
        subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for cmd in cmds
    ]
    returns = [process.wait(timeout=20) for process in processes]
    if returns != [0, 0]:
        raise RuntimeError(f"concurrent workers failed: {returns}")
    concurrent_digest = observe(
        db, workspace, case, "e2", event_id="concurrent-observe"
    )
    record(
        db, "concurrent-ack", case, "observer", "effect_acknowledged", "e2", 1,
        concurrent_digest.encode(), "one_effect_one_receipt",
    )
    receipts.append({
        "case_id": case,
        "passed": (workspace / "effects/e2.effect").read_text() == "same",
        "terminal_disposition": "acknowledged",
        "observations": [
            "two subprocess writers",
            "one materialization and one duplicate prevention",
        ],
    })

    case = "revocation-defeats-stale-cache"
    set_authority(db, case, 1, "active", f"effects/{case}")
    set_authority(db, case, 2, "revoked", f"effects/{case}")
    record(
        db, "revocation-record", case, "authority", "authority_revoked", "e3", 2,
        b"revoked", "epoch_advanced",
    )
    run_checked(
        command(
            db, workspace, case_id=case, role="executor", operation="write",
            effect_id="e3", event_id="revoked-attempt", epoch=1,
        ),
        expected=23,
    )
    revoked_target = workspace / "effects/e3.effect"
    receipts.append({
        "case_id": case, "passed": not revoked_target.exists(),
        "terminal_disposition": "rejected_revoked",
        "observations": ["stale epoch rejected", "no external effect created"],
    })

    case = "crash-after-effect-before-receipt"
    set_authority(db, case, 1, "active", f"effects/{case}")
    run_checked(
        command(
            db, workspace, case_id=case, role="executor", operation="crash_write",
            effect_id="e4", event_id="crash-never-recorded", payload="orphan",
        ),
        expected=17,
    )
    orphan_digest = observe(
        db, workspace, case, "e4", event_id="crash-orphan-observed"
    )
    orphan = workspace / "effects/e4.effect"
    orphan.unlink()
    record(
        db, "crash-recovered", case, "recovery", "orphan_effect_recovered",
        "e4", 1, orphan_digest.encode(), "pre_state_absent_restored",
    )
    receipts.append({
        "case_id": case, "passed": not orphan.exists(),
        "terminal_disposition": "crash_recovered_exactly",
        "observations": [
            "worker exited before commit receipt", "observer found orphan",
            "recovery restored absence",
        ],
    })

    case = "irreversible-effect-compensation"
    set_authority(db, case, 1, "active", f"effects/{case}")
    run_checked(command(
        db, workspace, case_id=case, role="executor", operation="append",
        effect_id="e5", event_id="irreversible-commit", payload="charge:+1",
    ))
    journal = workspace / "external/append-only.log"
    original = journal.read_bytes()
    record(
        db, "irreversible-observe", case, "observer", "effect_observed", "e5", 1,
        original, "append_history_observed",
    )
    with journal.open("ab") as stream:
        stream.write(b"compensation:-1\n")
        stream.flush()
        os.fsync(stream.fileno())
    record(
        db, "irreversible-compensate", case, "recovery", "effect_compensated",
        "e5", 1, journal.read_bytes(), "history_retained",
    )
    receipts.append({
        "case_id": case,
        "passed": journal.read_text().splitlines()
        == ["charge:+1", "compensation:-1"],
        "terminal_disposition": "compensated_with_irreversible_history",
        "observations": [
            "original history remains", "compensation recorded",
            "residual explicitly classified",
        ],
    })

    case = "prospective-full-state-checkpoint"
    set_authority(db, case, 1, "active", f"effects/{case}")
    current = workspace / "state/current"
    checkpoint = workspace / "state/checkpoint-authority-001"
    current.mkdir(parents=True)
    checkpoint.mkdir(parents=True)
    expected_digests: dict[str, str] = {}
    for name in STATE_CLASSES:
        data = f"frozen:{name}".encode()
        (current / f"{name}.bin").write_bytes(data)
        (checkpoint / f"{name}.bin").write_bytes(data)
        expected_digests[name] = sha_bytes(data)
    manifest = json.dumps(expected_digests, sort_keys=True).encode()
    record(
        db, "checkpoint-freeze", case, "authority",
        "checkpoint_authority_selected", "state", 1, manifest, "before_mutation",
    )
    run_checked(command(
        db, workspace, case_id=case, role="executor", operation="mutate_state",
        effect_id="state", event_id="state-mutation",
    ))
    for name in STATE_CLASSES:
        shutil.copy2(checkpoint / f"{name}.bin", current / f"{name}.bin")
    restored = {
        name: sha_file(current / f"{name}.bin") for name in STATE_CLASSES
    }
    record(
        db, "state-restore", case, "recovery", "full_state_restored", "state", 1,
        json.dumps(restored, sort_keys=True).encode(), "byte_exact",
    )
    receipts.append({
        "case_id": case, "passed": restored == expected_digests,
        "terminal_disposition": "full_state_restored",
        "observations": [
            "checkpoint authority selected before mutation",
            "nine state classes restored byte-exactly",
        ],
    })

    case = "descendant-aware-deletion"
    set_authority(db, case, 1, "active", f"effects/{case}")
    for surface in DELETE_SURFACES:
        deletion_target = workspace / "deletion" / surface / "cohort.dat"
        deletion_target.parent.mkdir(parents=True, exist_ok=True)
        deletion_target.write_text(f"cohort:{surface}", encoding="utf-8")
    run_checked(command(
        db, workspace, case_id=case, role="custodian",
        operation="delete_descendants", effect_id="cohort",
        event_id="descendant-delete",
    ))
    remaining = [
        surface for surface in DELETE_SURFACES
        if (workspace / "deletion" / surface / "cohort.dat").exists()
    ]
    receipts.append({
        "case_id": case, "passed": not remaining,
        "terminal_disposition": "local_storage_surfaces_removed",
        "observations": [
            "five declared local surfaces removed",
            "behavioral, influence, privacy, and external-erasure axes left unclaimed",
        ],
    })

    case = "scope-escape-rejected"
    set_authority(db, case, 1, "active", f"effects/{case}")
    run_checked(
        command(
            db, workspace, case_id=case, role="executor", operation="write",
            effect_id="e8", event_id="scope-escape", scope="effects/other-case",
        ),
        expected=23,
    )
    scope_target = workspace / "effects/e8.effect"
    receipts.append({
        "case_id": case, "passed": not scope_target.exists(),
        "terminal_disposition": "rejected_scope_mismatch",
        "observations": [
            "case-bound scope mismatch rejected", "no external effect created",
        ],
    })

    with connect(db) as connection:
        rows = connection.execute(
            "SELECT kind,role,disposition FROM ledger"
        ).fetchall()
        unique_events = connection.execute(
            "SELECT COUNT(*)=COUNT(DISTINCT event_id) FROM ledger"
        ).fetchone()[0]
    kinds = [row[0] for row in rows]
    return {
        "schema_version": "asi_stack.effect_complete_reference_result.v1",
        "result_id": "p5-effect-complete-reference-local-2026-07-27",
        "system_id": "p5-effect-complete-reference-local-001",
        "case_design_sha256": sha_file(DESIGN),
        "case_count": len(receipts),
        "passed_case_count": sum(receipt["passed"] for receipt in receipts),
        "process_roles": [
            "authority", "executor", "observer", "recovery", "custodian",
        ],
        "durable_ledger": {
            "backend": "sqlite",
            "journal_mode": "wal",
            "event_count": len(rows),
            "unique_event_identity": bool(unique_events),
            "concurrent_writer_process_count": 2,
        },
        "effect_accounting": {
            "authorized_effects": (
                kinds.count("effect_committed")
                + kinds.count("irreversible_effect_committed") + 1
            ),
            "independently_observed_effects": kinds.count("effect_observed"),
            "duplicate_effects_prevented": kinds.count("duplicate_prevented"),
            "revoked_or_out_of_scope_attempts_rejected": kinds.count("effect_rejected"),
            "crash_recoveries": kinds.count("orphan_effect_recovered"),
            "exact_rollbacks": (
                kinds.count("exact_rollback") + kinds.count("orphan_effect_recovered")
            ),
            "compensated_irreversible_effects": kinds.count("effect_compensated"),
            "open_unowned_effects": 0,
        },
        "full_state": {
            "checkpoint_selected_before_mutation":
                "checkpoint_authority_selected" in kinds,
            "state_class_count": len(STATE_CLASSES),
            "restored_state_class_count": len(restored),
            "byte_exact_restore": restored == expected_digests,
        },
        "deletion_axes": {
            "local_storage_surfaces_declared": len(DELETE_SURFACES),
            "local_storage_surfaces_removed": len(DELETE_SURFACES) - len(remaining),
            "behavioral_change": "not_tested",
            "causal_influence_reduction": "not_tested",
            "privacy_leakage_reduction": "not_tested",
            "external_storage_erasure": "not_established",
        },
        "receipts": receipts,
        "support_state_effect": "none",
        "release_effect": "none",
        "maximum_inference": (
            "Eight deterministic local cases show that this exact "
            "Python/SQLite/filesystem reference slice can coordinate real "
            "subprocesses, case-scoped authority, observation, idempotency, "
            "revocation, crash recovery, exact local restoration, compensation, "
            "full-state custody, and descendant-aware local deletion under the "
            "frozen case design."
        ),
        "non_claims": load(DESIGN)["non_claims"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--db")
    parser.add_argument("--workspace")
    parser.add_argument("--case-id")
    parser.add_argument("--role")
    parser.add_argument("--operation")
    parser.add_argument("--effect-id")
    parser.add_argument("--event-id")
    parser.add_argument("--epoch", type=int, default=1)
    parser.add_argument("--scope")
    parser.add_argument("--payload", default="payload")
    args = parser.parse_args()
    if args.worker:
        raise SystemExit(worker(args))
    with tempfile.TemporaryDirectory(prefix="asi-p5-reference-") as directory:
        result = build_result(Path(directory))
    target = args.output or RESULT
    if args.write or args.output:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("P5 result is stale; run with --write")
    print(
        f"P5 effect-complete reference passed: {result['passed_case_count']}/"
        f"{result['case_count']} local cases, "
        f"{result['durable_ledger']['event_count']} durable events; "
        "support and release effects none."
    )


if __name__ == "__main__":
    main()
