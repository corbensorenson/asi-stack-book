#!/usr/bin/env python3
"""Run the P5 stateful-service, partition, custody, and recovery slice."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from typing import Any
from urllib import error, request


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "experiments/effect_complete_service/cases.json"
RESULT = ROOT / "experiments/effect_complete_service/results/2026-07-27-local.json"
SCHEMA = ROOT / "schemas/effect_complete_service_result.schema.json"
SOURCE_FILES = [
    "experiments/effect_complete_service/cases.json",
    "schemas/effect_complete_service_result.schema.json",
    "scripts/run_p5_stateful_service_reference.py",
]
STATE_FILES = {
    "model": "model.json",
    "optimizer": "optimizer.json",
    "scheduler": "scheduler.json",
    "rng": "rng.json",
    "cache": "cache.json",
    "backup": "backup.json",
    "derived_artifacts": "derived_artifacts.json",
    "descendants": "descendants.json",
    "credentials": "credentials.json",
}
TRAINING_DATA = [(-2.0, -3.0), (-1.0, -1.0), (0.0, 1.0), (1.0, 3.0), (2.0, 5.0)]
TOKEN = "p5-local-epoch-1-token"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def run_git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    ).stdout


def attest_source(commit: str) -> dict[str, Any]:
    commit = run_git("rev-parse", f"{commit}^{{commit}}").decode().strip()
    digests: dict[str, str] = {}
    for relative in SOURCE_FILES:
        committed = run_git("show", f"{commit}:{relative}")
        current = (ROOT / relative).read_bytes()
        if committed != current:
            raise RuntimeError(
                f"current source differs from attested commit {commit}: {relative}"
            )
        digests[relative] = sha_bytes(committed)
    branches = run_git("branch", "--contains", commit).decode().split()
    if "main" not in [branch.lstrip("*") for branch in branches]:
        raise RuntimeError("attested source commit is not on main")
    return {
        "attested_source_commit": commit,
        "attested_branch": "main",
        "source_file_count": len(digests),
        "source_files_match_commit": True,
        "source_file_sha256": digests,
    }


def state_dir(workspace: Path) -> Path:
    return workspace / "service-state"


def initialize_state(workspace: Path) -> None:
    directory = state_dir(workspace)
    directory.mkdir(parents=True, exist_ok=True)
    write_json(directory / STATE_FILES["model"], {
        "architecture": "scalar_linear_v1", "w": 0.25, "b": 0.10,
        "revision": "prior-v1",
    })
    write_json(directory / STATE_FILES["optimizer"], {
        "algorithm": "adam", "step": 0, "m_w": 0.0, "v_w": 0.0,
        "m_b": 0.0, "v_b": 0.0, "beta1": 0.9, "beta2": 0.999,
        "epsilon": 1e-8,
    })
    write_json(directory / STATE_FILES["scheduler"], {
        "algorithm": "exponential", "base_lr": 0.08, "decay": 0.97, "step": 0,
    })
    write_json(directory / STATE_FILES["rng"], {
        "algorithm": "lcg32", "state": 1729, "draw_count": 0,
    })
    write_json(directory / STATE_FILES["cache"], {
        "model_revision": "prior-v1", "predictions": {},
    })
    write_json(directory / STATE_FILES["backup"], {
        "active_backup": "prior-v1", "weight_sha256": "",
    })
    write_json(directory / STATE_FILES["derived_artifacts"], {
        "evaluation_revision": "prior-v1", "mse": None,
    })
    write_json(directory / STATE_FILES["descendants"], {
        "adapter_revision": "prior-adapter-v1", "parent_revision": "prior-v1",
        "delta_w": 0.0,
    })
    write_json(directory / STATE_FILES["credentials"], {
        "epoch": 1, "state": "active", "scope": "effects/model-decision",
        "token_sha256": sha_bytes(TOKEN.encode()),
    })
    model_digest = sha_file(directory / STATE_FILES["model"])
    backup = load(directory / STATE_FILES["backup"])
    backup["weight_sha256"] = model_digest
    write_json(directory / STATE_FILES["backup"], backup)
    write_json(workspace / "environment.lock.json", {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "implementation": sys.implementation.name,
        "dependencies": "stdlib-only",
        "service_contract": "p5-stateful-service-v1",
    })


def state_digests(directory: Path) -> dict[str, str]:
    return {
        name: sha_file(directory / filename)
        for name, filename in STATE_FILES.items()
    }


def predict(model: dict[str, Any], value: float) -> float:
    return model["w"] * value + model["b"]


def mse(model: dict[str, Any]) -> float:
    return sum(
        (predict(model, x) - target) ** 2 for x, target in TRAINING_DATA
    ) / len(TRAINING_DATA)


def lcg_next(rng: dict[str, Any]) -> int:
    rng["state"] = (1664525 * rng["state"] + 1013904223) % (2 ** 32)
    rng["draw_count"] += 1
    return rng["state"]


def train_steps(workspace: Path, steps: int) -> dict[str, float]:
    directory = state_dir(workspace)
    model = load(directory / STATE_FILES["model"])
    optimizer = load(directory / STATE_FILES["optimizer"])
    scheduler = load(directory / STATE_FILES["scheduler"])
    rng = load(directory / STATE_FILES["rng"])
    before = mse(model)
    prior_w = model["w"]
    for _ in range(steps):
        index = lcg_next(rng) % len(TRAINING_DATA)
        x, target = TRAINING_DATA[index]
        prediction = predict(model, x)
        gradient_w = 2.0 * (prediction - target) * x
        gradient_b = 2.0 * (prediction - target)
        optimizer["step"] += 1
        scheduler["step"] += 1
        step = optimizer["step"]
        for key, gradient in (("w", gradient_w), ("b", gradient_b)):
            m_key = f"m_{key}"
            v_key = f"v_{key}"
            optimizer[m_key] = (
                optimizer["beta1"] * optimizer[m_key]
                + (1.0 - optimizer["beta1"]) * gradient
            )
            optimizer[v_key] = (
                optimizer["beta2"] * optimizer[v_key]
                + (1.0 - optimizer["beta2"]) * gradient * gradient
            )
            corrected_m = optimizer[m_key] / (1.0 - optimizer["beta1"] ** step)
            corrected_v = optimizer[v_key] / (1.0 - optimizer["beta2"] ** step)
            learning_rate = scheduler["base_lr"] * scheduler["decay"] ** (
                scheduler["step"] - 1
            )
            model[key] -= learning_rate * corrected_m / (
                math.sqrt(corrected_v) + optimizer["epsilon"]
            )
    model["revision"] = f"candidate-step-{optimizer['step']}"
    after = mse(model)
    write_json(directory / STATE_FILES["model"], model)
    write_json(directory / STATE_FILES["optimizer"], optimizer)
    write_json(directory / STATE_FILES["scheduler"], scheduler)
    write_json(directory / STATE_FILES["rng"], rng)
    write_json(directory / STATE_FILES["cache"], {
        "model_revision": model["revision"],
        "predictions": {
            str(x): round(predict(model, x), 12) for x, _ in TRAINING_DATA
        },
    })
    write_json(directory / STATE_FILES["backup"], {
        "active_backup": model["revision"],
        "weight_sha256": sha_file(directory / STATE_FILES["model"]),
    })
    write_json(directory / STATE_FILES["derived_artifacts"], {
        "evaluation_revision": model["revision"], "mse": round(after, 12),
    })
    write_json(directory / STATE_FILES["descendants"], {
        "adapter_revision": f"adapter-step-{optimizer['step']}",
        "parent_revision": model["revision"], "delta_w": round(model["w"] - prior_w, 12),
    })
    credentials = load(directory / STATE_FILES["credentials"])
    credentials["last_model_revision"] = model["revision"]
    write_json(directory / STATE_FILES["credentials"], credentials)
    return {"loss_before": before, "loss_after": after}


def freeze_checkpoint(workspace: Path) -> tuple[Path, dict[str, str]]:
    source = state_dir(workspace)
    checkpoint = workspace / "checkpoint-authority-001"
    shutil.copytree(source, checkpoint)
    manifest = state_digests(checkpoint)
    write_json(workspace / "checkpoint-authority.json", {
        "checkpoint_id": "checkpoint-authority-001",
        "selected_before_mutation": True,
        "state_digests": manifest,
    })
    return checkpoint, manifest


def restore_checkpoint(workspace: Path) -> None:
    current = state_dir(workspace)
    checkpoint = workspace / "checkpoint-authority-001"
    shutil.rmtree(current)
    shutil.copytree(checkpoint, current)
    write_json(workspace / "restart-receipt.json", {
        "new_process": True,
        "checkpoint_id": "checkpoint-authority-001",
        "restored_state_digests": state_digests(current),
    })


def custody_manifest(workspace: Path) -> dict[str, Any]:
    directory = state_dir(workspace)
    return {
        "model_weight_sha256": sha_file(directory / STATE_FILES["model"]),
        "environment_lock_sha256": sha_file(workspace / "environment.lock.json"),
    }


def verify_custody(workspace: Path, manifest: dict[str, Any]) -> tuple[bool, str]:
    directory = state_dir(workspace)
    if sha_file(directory / STATE_FILES["model"]) != manifest["model_weight_sha256"]:
        return False, "model_weight_digest_mismatch"
    if sha_file(workspace / "environment.lock.json") != manifest[
        "environment_lock_sha256"
    ]:
        return False, "dependency_lock_digest_mismatch"
    return True, "custody_valid"


class SinkHandler(BaseHTTPRequestHandler):
    server_version = "P5EffectSink/1"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = canonical(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/effect":
            self.send_json(404, {"status": "not_found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        token = self.headers.get("Authorization", "").removeprefix("Bearer ")
        if token != self.server.expected_token:  # type: ignore[attr-defined]
            self.send_json(403, {"status": "revoked_or_invalid_credential"})
            return
        effect_id = self.headers.get("Idempotency-Key", "")
        if not effect_id:
            self.send_json(400, {"status": "missing_effect_identity"})
            return
        with sqlite3.connect(self.server.sink_db) as connection:  # type: ignore[attr-defined]
            try:
                connection.execute(
                    "INSERT INTO effects(effect_id,payload_sha256,payload) VALUES(?,?,?)",
                    (effect_id, sha_bytes(body), body.decode()),
                )
                disposition = "accepted"
                status = 201
            except sqlite3.IntegrityError:
                disposition = "duplicate"
                status = 200
        self.send_json(status, {"status": disposition, "effect_id": effect_id})

    def do_GET(self) -> None:
        if not self.path.startswith("/effect/"):
            self.send_json(404, {"status": "not_found"})
            return
        effect_id = self.path.split("/", 2)[-1]
        with sqlite3.connect(self.server.sink_db) as connection:  # type: ignore[attr-defined]
            row = connection.execute(
                "SELECT payload_sha256,payload FROM effects WHERE effect_id=?",
                (effect_id,),
            ).fetchone()
        if row is None:
            self.send_json(404, {"status": "missing"})
            return
        self.send_json(200, {
            "status": "observed", "effect_id": effect_id,
            "payload_sha256": row[0], "payload": json.loads(row[1]),
        })


def sink_server(args: argparse.Namespace) -> int:
    db = Path(args.sink_db)
    with sqlite3.connect(db) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS effects("
            "effect_id TEXT PRIMARY KEY,payload_sha256 TEXT NOT NULL,payload TEXT NOT NULL)"
        )
    server = ThreadingHTTPServer(("127.0.0.1", args.port), SinkHandler)
    server.sink_db = str(db)  # type: ignore[attr-defined]
    server.expected_token = args.token  # type: ignore[attr-defined]
    write_json(Path(args.ready_file), {"port": server.server_port})
    server.serve_forever()
    return 0


def send_effect(
    port: int, effect_id: str, payload: dict[str, Any], token: str
) -> tuple[bool, str]:
    req = request.Request(
        f"http://127.0.0.1:{port}/effect",
        data=canonical(payload),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Idempotency-Key": effect_id,
            "Authorization": f"Bearer {token}",
        },
    )
    try:
        with request.urlopen(req, timeout=1.5) as response:
            return True, load_response(response.read())
    except error.HTTPError as exc:
        return False, load_response(exc.read())
    except (error.URLError, TimeoutError, ConnectionError):
        return False, "partition_or_unavailable"


def load_response(body: bytes) -> str:
    return json.loads(body.decode())["status"]


def observer(args: argparse.Namespace) -> int:
    try:
        with request.urlopen(
            f"http://127.0.0.1:{args.port}/effect/{args.effect_id}", timeout=2
        ) as response:
            payload = json.loads(response.read().decode())
    except Exception as exc:
        write_json(Path(args.observer_output), {
            "observed": False, "error": type(exc).__name__,
        })
        return 31
    write_json(Path(args.observer_output), {
        "observed": payload["status"] == "observed",
        "effect_id": payload["effect_id"],
        "payload_sha256": payload["payload_sha256"],
        "payload": payload["payload"],
    })
    return 0


def worker(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)
    if args.operation == "train-crash":
        train_steps(workspace, args.steps)
        os._exit(17)
    if args.operation == "train":
        metrics = train_steps(workspace, args.steps)
        write_json(Path(args.worker_output), metrics)
        return 0
    if args.operation == "restore":
        restore_checkpoint(workspace)
        return 0
    if args.operation == "infer":
        model = load(state_dir(workspace) / STATE_FILES["model"])
        write_json(Path(args.worker_output), {
            "prediction": predict(model, args.input_value),
            "model_revision": model["revision"],
        })
        return 0
    return 64


def worker_command(
    workspace: Path, operation: str, *, output: Path | None = None,
    steps: int = 8, input_value: float = 1.5,
) -> list[str]:
    command = [
        sys.executable, str(Path(__file__).resolve()), "--worker",
        "--workspace", str(workspace), "--operation", operation,
        "--steps", str(steps), "--input-value", str(input_value),
    ]
    if output is not None:
        command.extend(["--worker-output", str(output)])
    return command


def allocate_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def count_effects(db: Path) -> int:
    with sqlite3.connect(db) as connection:
        return int(connection.execute("SELECT COUNT(*) FROM effects").fetchone()[0])


def build_result(workspace: Path, attested_commit: str) -> dict[str, Any]:
    source_attestation = attest_source(attested_commit)
    initialize_state(workspace)
    checkpoint, checkpoint_digests = freeze_checkpoint(workspace)
    prior_model = load(state_dir(workspace) / STATE_FILES["model"])
    prior_prediction = predict(prior_model, 1.5)
    prior_loss = mse(prior_model)

    crash = subprocess.run(
        worker_command(workspace, "train-crash", steps=24),
        cwd=ROOT, capture_output=True, timeout=20,
    )
    if crash.returncode != 17:
        raise RuntimeError(f"expected crash exit 17, got {crash.returncode}")
    mutated_digests = state_digests(state_dir(workspace))
    mutated_classes = [
        name for name in STATE_FILES
        if mutated_digests[name] != checkpoint_digests[name]
    ]
    mutated_model = (
        state_dir(workspace) / STATE_FILES["model"]
    ).read_bytes()

    shutil.copy2(
        checkpoint / STATE_FILES["model"],
        state_dir(workspace) / STATE_FILES["model"],
    )
    artifact_only_digests = state_digests(state_dir(workspace))
    artifact_only_mismatches = [
        name for name in STATE_FILES
        if artifact_only_digests[name] != checkpoint_digests[name]
    ]
    artifact_only_rejected = bool(artifact_only_mismatches)
    (state_dir(workspace) / STATE_FILES["model"]).write_bytes(mutated_model)

    restart = subprocess.run(
        worker_command(workspace, "restore"), cwd=ROOT,
        capture_output=True, timeout=20,
    )
    if restart.returncode:
        raise RuntimeError(restart.stderr.decode() or "restore worker failed")
    restored_digests = state_digests(state_dir(workspace))
    inference_output = workspace / "restored-inference.json"
    inference = subprocess.run(
        worker_command(workspace, "infer", output=inference_output),
        cwd=ROOT, capture_output=True, timeout=20,
    )
    if inference.returncode:
        raise RuntimeError(inference.stderr.decode() or "inference worker failed")
    restored_prediction = load(inference_output)["prediction"]

    training_output = workspace / "training-result.json"
    trained = subprocess.run(
        worker_command(workspace, "train", output=training_output, steps=24),
        cwd=ROOT, capture_output=True, timeout=20,
    )
    if trained.returncode:
        raise RuntimeError(trained.stderr.decode() or "training worker failed")
    metrics = load(training_output)
    final_digests = state_digests(state_dir(workspace))
    final_model = load(state_dir(workspace) / STATE_FILES["model"])
    if not metrics["loss_after"] < metrics["loss_before"]:
        raise RuntimeError("learning positive control failed")

    manifest = custody_manifest(workspace)
    valid, _ = verify_custody(workspace, manifest)
    if not valid:
        raise RuntimeError("fresh custody manifest did not verify")
    model_path = state_dir(workspace) / STATE_FILES["model"]
    original_model = model_path.read_bytes()
    model_path.write_bytes(original_model + b" ")
    weight_tamper_valid, weight_tamper_reason = verify_custody(workspace, manifest)
    model_path.write_bytes(original_model)
    lock_path = workspace / "environment.lock.json"
    original_lock = lock_path.read_bytes()
    lock_path.write_bytes(original_lock + b" ")
    dependency_tamper_valid, dependency_tamper_reason = verify_custody(
        workspace, manifest
    )
    lock_path.write_bytes(original_lock)

    sink_db = workspace / "external-sink.sqlite"
    effect_id = "model-decision-001"
    effect_payload = {
        "model_revision": final_model["revision"],
        "prediction": round(predict(final_model, 1.5), 12),
        "purpose": "bounded-lifecycle-positive-control",
    }
    port = allocate_port()
    partition_ok, partition_reason = send_effect(
        port, effect_id, effect_payload, TOKEN
    )
    outbox = workspace / "effect-outbox.json"
    write_json(outbox, {
        "items": [{
            "effect_id": effect_id, "payload": effect_payload,
            "state": "pending", "owner": "effect-adapter",
        }]
    })

    ready = workspace / "sink-ready.json"
    sink = subprocess.Popen(
        [
            sys.executable, str(Path(__file__).resolve()), "--sink-server",
            "--sink-db", str(sink_db), "--ready-file", str(ready),
            "--port", str(port), "--token", TOKEN,
        ],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        for _ in range(100):
            if ready.exists():
                break
            if sink.poll() is not None:
                raise RuntimeError("external sink exited before readiness")
            time.sleep(0.05)
        if not ready.exists():
            raise RuntimeError("external sink did not become ready")
        accepted_ok, accepted_reason = send_effect(
            port, effect_id, effect_payload, TOKEN
        )
        duplicate_ok, duplicate_reason = send_effect(
            port, effect_id, effect_payload, TOKEN
        )
        revoked_ok, revoked_reason = send_effect(
            port, "revoked-effect-001", effect_payload, "revoked-token"
        )
        outbox_payload = load(outbox)
        outbox_payload["items"][0]["state"] = "acknowledged"
        write_json(outbox, outbox_payload)
        observer_output = workspace / "observer-receipt.json"
        observed = subprocess.run(
            [
                sys.executable, str(Path(__file__).resolve()), "--observer",
                "--port", str(port), "--effect-id", effect_id,
                "--observer-output", str(observer_output),
            ],
            cwd=ROOT, capture_output=True, timeout=20,
        )
        if observed.returncode:
            raise RuntimeError(observed.stderr.decode() or "observer failed")
        observer_receipt = load(observer_output)
        external_count = count_effects(sink_db)
    finally:
        sink.terminate()
        try:
            sink.wait(timeout=5)
        except subprocess.TimeoutExpired:
            sink.kill()
            sink.wait(timeout=5)

    expected_payload_digest = sha_bytes(canonical(effect_payload))
    receipts = [
        {
            "case_id": "actual-learning-state-mutation",
            "passed": (
                len(mutated_classes) == len(STATE_FILES)
                and metrics["loss_after"] < metrics["loss_before"]
            ),
            "terminal_disposition": "bounded_learning_positive_control_passed",
            "observations": [
                "bias-corrected Adam updated a real two-parameter predictor",
                "all nine declared state classes changed",
                "the frozen authored objective improved",
            ],
        },
        {
            "case_id": "artifact-only-rollback-rejected",
            "passed": artifact_only_rejected and len(artifact_only_mismatches) >= 8,
            "terminal_disposition": "incomplete_restore_rejected",
            "observations": [
                "weights alone matched the checkpoint",
                f"{len(artifact_only_mismatches)} non-model classes still differed",
            ],
        },
        {
            "case_id": "crash-restart-full-state-recovery",
            "passed": (
                crash.returncode == 17
                and restored_digests == checkpoint_digests
                and restored_prediction == prior_prediction
            ),
            "terminal_disposition": "new_process_restored_prospective_checkpoint",
            "observations": [
                "trainer exited after mutation and before acknowledgement",
                "a separate restart process restored nine classes byte-exactly",
                "restored inference matched the prior prediction exactly",
            ],
        },
        {
            "case_id": "partition-outbox-exactly-once",
            "passed": (
                not partition_ok and partition_reason == "partition_or_unavailable"
                and accepted_ok and accepted_reason == "accepted"
                and duplicate_ok and duplicate_reason == "duplicate"
                and external_count == 1
            ),
            "terminal_disposition": "partition_recovered_exactly_once",
            "observations": [
                "unavailable sink left one durable owned outbox item",
                "retry after recovery created one external effect",
                "duplicate retry created no second effect",
            ],
        },
        {
            "case_id": "revoked-credential-effect-rejected",
            "passed": (
                not revoked_ok and revoked_reason == "revoked_or_invalid_credential"
                and external_count == 1
            ),
            "terminal_disposition": "revoked_effect_rejected",
            "observations": [
                "stale token received an explicit rejection",
                "no revoked effect entered the external ledger",
            ],
        },
        {
            "case_id": "weight-and-environment-custody-tamper-rejected",
            "passed": (
                not weight_tamper_valid
                and weight_tamper_reason == "model_weight_digest_mismatch"
                and not dependency_tamper_valid
                and dependency_tamper_reason == "dependency_lock_digest_mismatch"
            ),
            "terminal_disposition": "custody_drift_rejected_before_release",
            "observations": [
                "model-weight byte drift failed the frozen digest",
                "dependency-lock byte drift failed the frozen digest",
            ],
        },
        {
            "case_id": "independent-observation-and-source-attestation",
            "passed": (
                observer_receipt["observed"]
                and observer_receipt["payload_sha256"] == expected_payload_digest
                and source_attestation["source_files_match_commit"]
            ),
            "terminal_disposition": "effect_observed_and_source_identity_bound",
            "observations": [
                "a separately executed observer read the external sink",
                "observer payload digest matched the released payload",
                "source files matched an exact commit on main",
            ],
        },
    ]
    if not all(receipt["passed"] for receipt in receipts):
        raise RuntimeError("one or more stateful-service cases failed")

    return {
        "schema_version": "asi_stack.effect_complete_service_result.v1",
        "result_id": "p5-effect-complete-stateful-service-2026-07-27",
        "system_id": "p5-effect-complete-stateful-service-001",
        "case_design_sha256": sha_file(DESIGN),
        "case_count": len(receipts),
        "passed_case_count": sum(receipt["passed"] for receipt in receipts),
        "process_roles": [
            "checkpoint_authority", "trainer", "restart_supervisor",
            "inference_service", "effect_adapter", "external_effect_service",
            "independent_observer",
        ],
        "learning_state": {
            "state_class_count": len(STATE_FILES),
            "mutated_state_class_count": len(mutated_classes),
            "training_steps": 24,
            "loss_before": round(prior_loss, 12),
            "loss_after": round(metrics["loss_after"], 12),
            "positive_control_passed": metrics["loss_after"] < metrics["loss_before"],
        },
        "rollback": {
            "checkpoint_selected_before_mutation": True,
            "artifact_only_control_rejected": artifact_only_rejected,
            "artifact_only_mismatched_state_classes": len(
                artifact_only_mismatches
            ),
            "crash_exit_code": crash.returncode,
            "restart_process_used": True,
            "restored_state_class_count": sum(
                restored_digests[name] == checkpoint_digests[name]
                for name in STATE_FILES
            ),
            "byte_exact_restore": restored_digests == checkpoint_digests,
            "restored_prediction_exact": restored_prediction == prior_prediction,
        },
        "external_effect": {
            "partition_attempt_failed_closed": (
                not partition_ok and partition_reason == "partition_or_unavailable"
            ),
            "owned_outbox_count_during_partition": 1,
            "accepted_effect_count": external_count,
            "duplicate_retry_count": int(duplicate_reason == "duplicate"),
            "revoked_attempt_count": 1,
            "revoked_effect_count": 0,
            "independent_observer_process": True,
            "observer_digest_match": (
                observer_receipt["payload_sha256"] == expected_payload_digest
            ),
            "open_unowned_effects": 0,
        },
        "custody": {
            **source_attestation,
            "model_weight_digest_bound": bool(manifest["model_weight_sha256"]),
            "dependency_lock_digest_bound": bool(
                manifest["environment_lock_sha256"]
            ),
            "weight_tamper_rejected": not weight_tamper_valid,
            "dependency_tamper_rejected": not dependency_tamper_valid,
            "attestation_scope": "local_source_and_runtime_identity_not_deployment",
        },
        "receipts": receipts,
        "support_state_effect": "none",
        "release_effect": "none",
        "maximum_inference": (
            "Seven deterministic local cases show that this exact commit-bound "
            "Python service slice can mutate and restore actual model and Adam "
            "learning state, reject weights-only recovery, recover a crashed "
            "trainer in a new process, retain an owned outbox during a localhost "
            "partition, deliver one idempotent external effect, reject a revoked "
            "credential, detect weight and environment drift, and expose the "
            "effect to a separately executed observer."
        ),
        "non_claims": load(DESIGN)["non_claims"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--attested-source-commit")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--workspace")
    parser.add_argument("--operation")
    parser.add_argument("--worker-output")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--input-value", type=float, default=1.5)
    parser.add_argument("--sink-server", action="store_true")
    parser.add_argument("--sink-db")
    parser.add_argument("--ready-file")
    parser.add_argument("--port", type=int)
    parser.add_argument("--token")
    parser.add_argument("--observer", action="store_true")
    parser.add_argument("--effect-id")
    parser.add_argument("--observer-output")
    args = parser.parse_args()
    if args.worker:
        raise SystemExit(worker(args))
    if args.sink_server:
        raise SystemExit(sink_server(args))
    if args.observer:
        raise SystemExit(observer(args))
    if not args.attested_source_commit:
        raise SystemExit("--attested-source-commit is required")
    with tempfile.TemporaryDirectory(prefix="asi-p5-stateful-service-") as directory:
        result = build_result(Path(directory), args.attested_source_commit)
    target = args.output or RESULT
    if args.write or args.output:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("P5 stateful service result is stale; run with --write")
    print(
        f"P5 stateful service passed: {result['passed_case_count']}/"
        f"{result['case_count']} cases; actual learning state, restart, "
        "partition, external observation, and custody boundaries exercised; "
        "support and release effects none."
    )


if __name__ == "__main__":
    main()
