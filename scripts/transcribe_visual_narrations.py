#!/usr/bin/env python3
"""Audit chapter narrations with one cached local MLX Whisper model load."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from mlx_whisper import transcribe


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
        value.get("validation_state") == "pass"
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
    return (
        value.get("audio_sha256") == sha256(audio)
        and value.get("receipt_sha256") == sha256(receipt)
        and value.get("asr_sha256") == sha256(asr)
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
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-non-pilots", action="store_true")
    parser.add_argument("--all-chapters", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    selected = (
        chapters(include_pilots=args.all_chapters)
        if args.all_non_pilots or args.all_chapters
        else args.chapter
    )
    if not selected:
        raise SystemExit("Select --chapter or --all-non-pilots")
    if not (MODEL / "config.json").is_file() or not (MODEL / "weights.npz").is_file():
        raise SystemExit("Pinned local Whisper model is missing")
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
            except subprocess.CalledProcessError:
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
        output = AUDIO / f"{slug}-narration-master.json"
        output.write_text(
            json.dumps(result, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        try:
            validate(slug)
        except subprocess.CalledProcessError:
            failures.append(slug)
            print(f"[{index}/{len(selected)}] {slug}: AUDIT FAILED", flush=True)
    if failures:
        raise SystemExit(
            "Narration audit failures:\n - " + "\n - ".join(failures)
        )


if __name__ == "__main__":
    main()
