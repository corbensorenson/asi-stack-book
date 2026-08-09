#!/usr/bin/env python3
"""Audit chapter narrations with one cached local MLX Whisper model load."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "build/visual_edition/audio"
MODEL = ROOT / "build/visual_edition/models/whisper-small.en-mlx"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asr_identity_current(
    receipt: dict,
    toolchain: dict,
    *,
    runner_sha256: str,
    audio_path: str,
    audio_sha256: str,
) -> bool:
    tracked = toolchain.get("tracked_inputs", {})
    verification = toolchain.get("verification", {})
    return (
        receipt.get("runner_path") == tracked.get("transcription_runner")
        and receipt.get("runner_sha256") == runner_sha256
        and receipt.get("toolchain_id") == toolchain.get("toolchain_id")
        and receipt.get("implementation") == verification.get("implementation")
        and receipt.get("implementation_version") == verification.get("version")
        and receipt.get("model_repository") == verification.get("model_repository")
        and receipt.get("model_revision") == verification.get("model_revision")
        and receipt.get("model_file_sha256") == {
            "build/visual_edition/models/whisper-small.en-mlx/config.json":
                verification.get("model_config_sha256"),
            "build/visual_edition/models/whisper-small.en-mlx/weights.npz":
                verification.get("model_weights_sha256"),
        }
        and receipt.get("audio_path") == audio_path
        and receipt.get("audio_sha256") == audio_sha256
        and receipt.get("language") == "en"
    )


def self_test() -> None:
    digest = "a" * 64
    audio_path = "build/visual_edition/audio/fixture-narration-master.wav"
    toolchain = {
        "toolchain_id": "fixture-toolchain",
        "tracked_inputs": {
            "transcription_runner": "scripts/transcribe_visual_narrations.py",
        },
        "verification": {
            "implementation": "mlx-whisper",
            "version": "0.4.3",
            "model_repository": "fixture/model",
            "model_revision": "b" * 40,
            "model_config_sha256": "c" * 64,
            "model_weights_sha256": "d" * 64,
        },
    }
    receipt = {
        "runner_path": "scripts/transcribe_visual_narrations.py",
        "runner_sha256": digest,
        "toolchain_id": "fixture-toolchain",
        "implementation": "mlx-whisper",
        "implementation_version": "0.4.3",
        "model_repository": "fixture/model",
        "model_revision": "b" * 40,
        "model_file_sha256": {
            "build/visual_edition/models/whisper-small.en-mlx/config.json": "c" * 64,
            "build/visual_edition/models/whisper-small.en-mlx/weights.npz": "d" * 64,
        },
        "audio_path": audio_path,
        "audio_sha256": digest,
        "language": "en",
    }
    kwargs = {
        "runner_sha256": digest,
        "audio_path": audio_path,
        "audio_sha256": digest,
    }
    if not asr_identity_current(receipt, toolchain, **kwargs):
        raise AssertionError("valid ASR identity fixture was rejected")
    mutations = (
        ("runner", lambda row: row.__setitem__("runner_sha256", "0" * 64)),
        ("toolchain", lambda row: row.__setitem__("toolchain_id", "stale")),
        ("implementation", lambda row: row.__setitem__("implementation_version", "0")),
        ("repository", lambda row: row.__setitem__("model_repository", "wrong/model")),
        ("revision", lambda row: row.__setitem__("model_revision", "0" * 40)),
        ("model files", lambda row: row["model_file_sha256"].update(
            {"build/visual_edition/models/whisper-small.en-mlx/weights.npz": "0" * 64}
        )),
        ("audio path", lambda row: row.__setitem__("audio_path", "wrong.wav")),
        ("audio digest", lambda row: row.__setitem__("audio_sha256", "0" * 64)),
        ("language", lambda row: row.__setitem__("language", "und")),
    )
    for label, mutate in mutations:
        candidate = copy.deepcopy(receipt)
        mutate(candidate)
        if asr_identity_current(candidate, toolchain, **kwargs):
            raise AssertionError(f"stale ASR {label} identity was accepted")
    print(f"Self-test passed: valid ASR custody accepted and {len(mutations)} stale identities rejected.")


def chapters(include_pilots: bool = False) -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
        if include_pilots or chapter["id"] not in PILOTS
    ]


def current(slug: str) -> bool:
    audio = AUDIO / f"{slug}-narration-master.wav"
    receipt = AUDIO / f"{slug}-narration-master.receipt.json"
    asr = AUDIO / f"{slug}-narration-master.json"
    report = AUDIO / f"{slug}-narration-master.validation.json"
    if not all(path.is_file() for path in (audio, receipt, asr, report)):
        return False
    value = json.loads(report.read_text(encoding="utf-8"))
    return (
        validation_inputs_current(slug)
        and value.get("validation_state") == "pass"
        and value.get("audio_sha256") == sha256(audio)
        and value.get("receipt_sha256") == sha256(receipt)
        and value.get("asr_sha256") == sha256(asr)
        and value.get("validator_sha256")
        == sha256(ROOT / "scripts/validate_visual_narration.py")
    )


def validation_inputs_current(slug: str) -> bool:
    """Allow validator-only replay without needlessly rerunning Whisper."""
    audio = AUDIO / f"{slug}-narration-master.wav"
    receipt = AUDIO / f"{slug}-narration-master.receipt.json"
    asr = AUDIO / f"{slug}-narration-master.json"
    report = AUDIO / f"{slug}-narration-master.validation.json"
    if not all(path.is_file() for path in (audio, receipt, asr, report)):
        return False
    value = json.loads(report.read_text(encoding="utf-8"))
    asr_value = json.loads(asr.read_text(encoding="utf-8"))
    asr_receipt = asr_value.get("_asi_stack_receipt", {})
    toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    return (
        value.get("audio_sha256") == sha256(audio)
        and value.get("receipt_sha256") == sha256(receipt)
        and value.get("asr_sha256") == sha256(asr)
        and asr_identity_current(
            asr_receipt,
            toolchain,
            runner_sha256=sha256(Path(__file__)),
            audio_path=str(audio.relative_to(ROOT)),
            audio_sha256=sha256(audio),
        )
    )


def validate(slug: str) -> None:
    subprocess.run(
        [
            str(Path(__file__).resolve().parent.parent / "build/visual_edition/tts_venv/bin/python"),
            "scripts/validate_visual_narration.py",
            "--audio", f"build/visual_edition/audio/{slug}-narration-master.wav",
            "--receipt", f"build/visual_edition/audio/{slug}-narration-master.receipt.json",
            "--asr", f"build/visual_edition/audio/{slug}-narration-master.json",
            "--report", f"build/visual_edition/audio/{slug}-narration-master.validation.json",
        ],
        cwd=ROOT,
        check=True,
        timeout=300,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-non-pilots", action="store_true")
    parser.add_argument("--all-chapters", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    selected = (
        chapters(include_pilots=args.all_chapters)
        if args.all_non_pilots or args.all_chapters
        else args.chapter
    )
    if not selected:
        raise SystemExit("Select --chapter or --all-non-pilots")
    canonical = set(chapters(include_pilots=True))
    invalid = sorted(set(selected) - canonical)
    if invalid:
        raise SystemExit(
            "Unknown or noncanonical chapter identity: " + ", ".join(invalid)
        )
    if len(selected) != len(set(selected)):
        raise SystemExit("Duplicate --chapter identities are not allowed")
    if not (MODEL / "config.json").is_file() or not (MODEL / "weights.npz").is_file():
        raise SystemExit("Pinned local Whisper model is missing")
    # Local model paths plus offline hints reduce accidental downloads. The
    # pinned ML runtime remains TCB; this is not OS-enforced network isolation.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    from mlx_whisper import transcribe

    toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    verification = toolchain["verification"]
    model_files = [MODEL / "config.json", MODEL / "weights.npz"]
    actual_model_digests = {
        str(path.relative_to(ROOT)): sha256(path) for path in model_files
    }
    expected_model_digests = {
        "build/visual_edition/models/whisper-small.en-mlx/config.json":
            verification["model_config_sha256"],
        "build/visual_edition/models/whisper-small.en-mlx/weights.npz":
            verification["model_weights_sha256"],
    }
    if actual_model_digests != expected_model_digests:
        raise SystemExit("Pinned local Whisper model identity drift")
    expected_runner = toolchain.get("tracked_inputs", {}).get(
        "transcription_runner_sha256"
    )
    if expected_runner != sha256(Path(__file__)):
        raise SystemExit("Narration toolchain does not bind the current transcription runner")
    failures = []
    for index, slug in enumerate(selected, start=1):
        audio = AUDIO / f"{slug}-narration-master.wav"
        if not audio.is_file():
            raise SystemExit(f"Narration is missing: {slug}")
        if not args.force and current(slug):
            print(f"[{index}/{len(selected)}] {slug}: audit current", flush=True)
            continue
        if not args.force and validation_inputs_current(slug):
            print(f"[{index}/{len(selected)}] {slug}: replaying validator", flush=True)
            try:
                validate(slug)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                failures.append(slug)
                print(f"[{index}/{len(selected)}] {slug}: AUDIT FAILED", flush=True)
            continue
        print(f"[{index}/{len(selected)}] {slug}: transcribing", flush=True)
        result = transcribe(
            str(audio),
            path_or_hf_repo=str(MODEL),
            language="en",
            verbose=False,
        )
        result["_asi_stack_receipt"] = {
            "schema_version": "asi_stack.local_asr_transcript.v1",
            "transcribed_at_utc": datetime.now(timezone.utc).replace(
                microsecond=0
            ).isoformat().replace("+00:00", "Z"),
            "runner_path": "scripts/transcribe_visual_narrations.py",
            "runner_sha256": sha256(Path(__file__)),
            "toolchain_id": toolchain["toolchain_id"],
            "implementation": verification["implementation"],
            "implementation_version": importlib.metadata.version("mlx-whisper"),
            "model_repository": verification["model_repository"],
            "model_revision": verification["model_revision"],
            "model_file_sha256": actual_model_digests,
            "audio_path": str(audio.relative_to(ROOT)),
            "audio_sha256": sha256(audio),
            "language": "en",
        }
        output = AUDIO / f"{slug}-narration-master.json"
        output_temp = output.with_suffix(".tmp.json")
        output_temp.write_text(
            json.dumps(result, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        output_temp.replace(output)
        try:
            validate(slug)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            failures.append(slug)
            print(f"[{index}/{len(selected)}] {slug}: AUDIT FAILED", flush=True)
    if failures:
        raise SystemExit(
            "Narration audit failures:\n - " + "\n - ".join(failures)
        )


if __name__ == "__main__":
    main()
