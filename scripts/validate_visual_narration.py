#!/usr/bin/env python3
"""Validate a local narration master against its script, receipt, and ASR audit."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import soundfile as sf


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = (ROOT / "build/visual_edition/audio").resolve()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_audio_path(value: str, *, label: str, must_exist: bool) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        raise ValueError(f"{label} must be repository-relative")
    path = (ROOT / candidate).resolve()
    try:
        path.relative_to(AUDIO_ROOT)
    except ValueError as exc:
        raise ValueError(f"{label} escapes build/visual_edition/audio") from exc
    if must_exist and not path.is_file():
        raise ValueError(f"{label} is missing")
    return path


def tokens(text: str) -> list[str]:
    return re.findall(
        r"[a-z0-9]+(?:'[a-z0-9]+)?",
        text.lower().replace("’", "'"),
    )


def edit_distance(expected: list[str], actual: list[str]) -> int:
    previous = list(range(len(actual) + 1))
    for row, expected_token in enumerate(expected, start=1):
        current = [row]
        for column, actual_token in enumerate(actual, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (expected_token != actual_token),
                )
            )
        previous = current
    return previous[-1]


def collapse_letter_runs(values: list[str]) -> list[str]:
    """Treat ASR-normalized acronyms and spoken letter runs as equivalent."""
    result: list[str] = []
    run: list[str] = []
    for value in values:
        if len(value) == 1 and value.isalpha():
            run.append(value)
            continue
        if run:
            result.append("".join(run))
            run = []
        result.append(value)
    if run:
        result.append("".join(run))
    return result


def normalize_number_words(values: list[str]) -> list[str]:
    """Normalize ordinary spoken integers so ASR digit formatting is neutral."""
    units = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
    }
    tens = {
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }
    result: list[str] = []
    index = 0
    while index < len(values):
        value = values[index]
        if (
            value in units
            and 0 < units[value] < 10
            and index + 2 < len(values)
            and values[index + 1] == "oh"
            and values[index + 2] in units
            and units[values[index + 2]] < 10
        ):
            result.append(f"{units[value]}0{units[values[index + 2]]}")
            index += 3
            continue
        if (
            value in units
            and 0 < units[value] < 10
            and index + 1 < len(values)
            and values[index + 1] == "hundred"
        ):
            number = units[value] * 100
            index += 2
            if index < len(values) and values[index] in tens:
                number += tens[values[index]]
                index += 1
                if index < len(values) and values[index] in units:
                    number += units[values[index]]
                    index += 1
            elif index < len(values) and values[index] in units:
                number += units[values[index]]
                index += 1
            result.append(str(number))
            continue
        if value in tens:
            number = tens[value]
            if index + 1 < len(values) and values[index + 1] in units:
                number += units[values[index + 1]]
                index += 1
            result.append(str(number))
        elif value in units:
            result.append(str(units[value]))
        else:
            result.append(value)
        index += 1
    return result


def normalize_compounds(values: list[str]) -> list[str]:
    """Neutralize a small, explicit set of ordinary ASR spacing variants."""
    compounds = {
        ("data", "set"): "dataset",
        ("re", "contract"): "recontract",
        ("non", "versioned"): "nonversioned",
        ("non", "claims"): "nonclaims",
        ("rank", "fold"): "rankfold",
        ("neural", "fold"): "neuralfold",
        ("counter", "models"): "countermodels",
        ("counter", "cases"): "countercases",
        ("life", "cycle"): "lifecycle",
        ("fan", "out"): "fanout",
        ("check", "out"): "checkout",
        ("a", "si"): "asi",
        ("as", "i"): "asi",
    }
    result: list[str] = []
    index = 0
    while index < len(values):
        pair = tuple(values[index:index + 2])
        if pair in compounds:
            result.append(compounds[pair])
            index += 2
        else:
            result.append(values[index])
            index += 1
    return result


def normalize_audio_homophones(values: list[str]) -> list[str]:
    """Neutralize spellings that no audio-only audit can distinguish."""
    canonical = {
        "cash": "cache",
        "root": "route",
    }
    return [canonical.get(value, value) for value in values]


def normalize_version_labels(values: list[str]) -> list[str]:
    """Neutralize punctuation loss in labels such as ``v2.1`` versus ``v21``."""
    result: list[str] = []
    index = 0
    while index < len(values):
        value = values[index]
        if (
            re.fullmatch(r"v\d+", value)
            and index + 1 < len(values)
            and re.fullmatch(r"\d+", values[index + 1])
        ):
            result.append(value + values[index + 1])
            index += 2
            continue
        result.append(value)
        index += 1
    return result


def normalize_content_tokens(values: list[str]) -> list[str]:
    """Apply the exact content-equivalence pipeline used by the ASR gate."""
    return normalize_version_labels(
        normalize_audio_homophones(
            normalize_compounds(
                normalize_number_words(collapse_letter_runs(values))
            )
        )
    )


def normalization_self_test() -> None:
    equivalent = (
        ("two hundred forty dollars", "240 dollars"),
        ("nine hundred nineteen", "919"),
        ("two oh five", "205"),
        ("check out", "checkout"),
        ("twenty four", "24"),
    )
    distinct = (
        ("two hundred forty", "241"),
        ("two oh five", "206"),
        ("check in", "checkout"),
        ("nineteen", "90"),
    )
    for written, recognized in equivalent:
        if normalize_content_tokens(tokens(written)) != normalize_content_tokens(tokens(recognized)):
            raise AssertionError(f"equivalent narration forms diverged: {written!r}, {recognized!r}")
    for written, recognized in distinct:
        if normalize_content_tokens(tokens(written)) == normalize_content_tokens(tokens(recognized)):
            raise AssertionError(f"distinct narration forms collapsed: {written!r}, {recognized!r}")
    print(
        "Narration normalization self-test passed: "
        f"{len(equivalent)} equivalent pairs accepted and {len(distinct)} controls rejected."
    )


def boundary_covered(
    expected: list[str],
    actual: list[str],
    *,
    beginning: bool,
    window: int = 12,
) -> bool:
    """Detect a missing beginning/end without requiring flawless ASR spelling.

    The global WER gate remains unchanged.  This independent boundary gate
    allows at most two edits in a twelve-token anchor, which tolerates one
    recognizer substitution or omission but still rejects a clipped sentence
    or missing tail.
    """
    size = min(window, len(expected), len(actual))
    if size < 5:
        return False
    expected_anchor = expected[:size] if beginning else expected[-size:]
    actual_anchor = actual[:size] if beginning else actual[-size:]
    return edit_distance(expected_anchor, actual_anchor) <= max(1, size // 6)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio")
    parser.add_argument("--receipt")
    parser.add_argument("--asr")
    parser.add_argument("--report")
    parser.add_argument("--maximum-wer", type=float, default=0.03)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        normalization_self_test()
        return
    missing = [name for name in ("audio", "receipt", "asr", "report") if not getattr(args, name)]
    if missing:
        parser.error("the following arguments are required: " + ", ".join(f"--{name}" for name in missing))

    audio_path = checked_audio_path(args.audio, label="audio", must_exist=True)
    receipt_path = checked_audio_path(args.receipt, label="receipt", must_exist=True)
    asr_path = checked_audio_path(args.asr, label="ASR transcript", must_exist=True)
    report_path = checked_audio_path(args.report, label="validation report", must_exist=False)
    stem = audio_path.name.removesuffix(".wav")
    expected_siblings = {
        receipt_path: f"{stem}.receipt.json",
        asr_path: f"{stem}.json",
        report_path: f"{stem}.validation.json",
    }
    for path, expected_name in expected_siblings.items():
        if path.name != expected_name or path.parent != audio_path.parent:
            raise ValueError("narration validation artifacts do not share one canonical audio identity")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    asr = json.loads(asr_path.read_text(encoding="utf-8"))
    toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    verification = toolchain["verification"]
    synthesis = toolchain["synthesis"]
    tracked_inputs = toolchain["tracked_inputs"]
    if args.maximum_wer != verification["maximum_content_normalized_word_error_rate"]:
        raise ValueError("--maximum-wer cannot weaken or alter the pinned toolchain threshold")
    asr_receipt = asr.get("_asi_stack_receipt", {})
    audio, sample_rate = sf.read(audio_path, always_2d=True)
    duration = len(audio) / sample_rate
    peak = float(np.max(np.abs(audio)))
    clipped_samples = int(np.count_nonzero(np.abs(audio) >= 0.999))
    expected_text = " ".join(item["spoken_text"] for item in receipt["segments"])
    expected_tokens = tokens(expected_text)
    actual_tokens = tokens(asr["text"])
    raw_word_errors = edit_distance(expected_tokens, actual_tokens)
    raw_wer = raw_word_errors / max(1, len(expected_tokens))
    normalized_expected = normalize_content_tokens(expected_tokens)
    normalized_actual = normalize_content_tokens(actual_tokens)
    word_errors = edit_distance(normalized_expected, normalized_actual)
    wer = word_errors / max(1, len(normalized_expected))
    expected_gaps = [
        i2 - i1
        for tag, i1, i2, _j1, _j2 in difflib.SequenceMatcher(
            a=normalized_expected,
            b=normalized_actual,
        ).get_opcodes()
        if tag != "equal"
    ]
    maximum_expected_gap = max(expected_gaps, default=0)

    checks = {
        "renderer_digest_matches_current": (
            receipt.get("renderer_sha256")
            == tracked_inputs["renderer_sha256"]
            == sha256(ROOT / "scripts/render_visual_narration.py")
        ),
        "synthesis_toolchain_identity_matches": (
            receipt.get("toolchain_id") == toolchain["toolchain_id"]
            and receipt.get("implementation") == synthesis["implementation"]
            and receipt.get("implementation_version") == synthesis["version"]
            and receipt.get("model_repository") == synthesis["model_repository"]
            and receipt.get("model_revision") == synthesis["model_revision"]
            and receipt.get("voice") == synthesis["voice"]
            and receipt.get("speed") == synthesis["speed"]
            and receipt.get("sample_rate") == synthesis["sample_rate"]
        ),
        "synthesis_model_files_match_toolchain": (
            receipt.get("model_file_sha256") == {
                f"{synthesis['model_directory']}/config.json": synthesis["config_sha256"],
                f"{synthesis['model_directory']}/kokoro-v1_0.safetensors": synthesis["weights_sha256"],
                f"{synthesis['model_directory']}/voices/{synthesis['voice']}.safetensors": synthesis["voice_sha256"],
            }
        ),
        "normalizer_identity_matches_toolchain": (
            receipt.get("normalization", {}).get("filter")
            == synthesis["normalizer_implementation"]
            and receipt.get("normalization", {}).get("ffmpeg_path")
            == synthesis["normalizer_path"]
            and receipt.get("normalization", {}).get("ffmpeg_version")
            == synthesis["normalizer_version"]
            and receipt.get("normalization", {}).get("ffmpeg_sha256")
            == synthesis["normalizer_sha256"]
            and Path(synthesis["normalizer_path"]).is_file()
            and sha256(Path(synthesis["normalizer_path"]))
            == synthesis["normalizer_sha256"]
        ),
        "normalization_settings_match_toolchain": (
            receipt.get("normalization", {}).get("integrated_lufs_target")
            == synthesis["integrated_lufs_target"]
            and receipt.get("normalization", {}).get("true_peak_dbtp_target")
            == synthesis["true_peak_dbtp_target"]
            and receipt.get("normalization", {}).get("loudness_range_target")
            == synthesis["loudness_range_target"]
        ),
        "audio_path_matches_receipt": (
            receipt.get("output_path") == args.audio
        ),
        "audio_digest_matches_receipt": sha256(audio_path) == receipt["output_sha256"],
        "asr_receipt_schema_current": (
            asr_receipt.get("schema_version") == "asi_stack.local_asr_transcript.v1"
        ),
        "asr_runner_bound_and_current": (
            asr_receipt.get("runner_path") == tracked_inputs["transcription_runner"]
            and asr_receipt.get("runner_sha256")
            == tracked_inputs["transcription_runner_sha256"]
            == sha256(ROOT / tracked_inputs["transcription_runner"])
        ),
        "asr_toolchain_identity_matches": (
            asr_receipt.get("toolchain_id") == toolchain["toolchain_id"]
            and asr_receipt.get("implementation") == verification["implementation"]
            and asr_receipt.get("implementation_version") == verification["version"]
            and asr_receipt.get("model_repository") == verification["model_repository"]
            and asr_receipt.get("model_revision") == verification["model_revision"]
        ),
        "asr_model_files_match_toolchain": (
            asr_receipt.get("model_file_sha256") == {
                "build/visual_edition/models/whisper-small.en-mlx/config.json":
                    verification["model_config_sha256"],
                "build/visual_edition/models/whisper-small.en-mlx/weights.npz":
                    verification["model_weights_sha256"],
            }
        ),
        "asr_audio_identity_matches": (
            asr_receipt.get("audio_path") == args.audio
            and asr_receipt.get("audio_sha256") == sha256(audio_path)
            and asr_receipt.get("language") == "en"
        ),
        "duration_matches_receipt": abs(duration - receipt["duration_seconds"]) <= 0.001,
        "duration_is_positive": duration > 0,
        "sample_rate_matches_receipt": sample_rate == receipt["sample_rate"],
        "mono": audio.shape[1] == 1,
        "finite_samples": bool(np.isfinite(audio).all()),
        "no_clipped_samples": clipped_samples == 0,
        "peak_within_digital_range": peak <= 1,
        "synthesis_segments_within_declared_limit": (
            bool(receipt.get("segments"))
            and max(len(item["written_text"]) for item in receipt["segments"])
            <= receipt.get("segmentation", {}).get("maximum_characters", 0)
            <= 300
            and receipt.get("segmentation", {}).get("maximum_observed_characters")
            == max(len(item["written_text"]) for item in receipt["segments"])
        ),
        "asr_content_word_error_rate_within_limit": wer <= args.maximum_wer,
        "asr_has_no_long_internal_omission": maximum_expected_gap <= 8,
        "asr_covers_beginning": boundary_covered(
            normalized_expected,
            normalized_actual,
            beginning=True,
        ),
        "asr_covers_ending": boundary_covered(
            normalized_expected,
            normalized_actual,
            beginning=False,
        ),
    }
    report = {
        "schema_version": "asi_stack.local_narration_validation.v1",
        "validation_state": "pass" if all(checks.values()) else "fail",
        "validator_sha256": sha256(Path(__file__)),
        "receipt_sha256": sha256(receipt_path),
        "asr_sha256": sha256(asr_path),
        "audio_path": args.audio,
        "audio_sha256": sha256(audio_path),
        "duration_seconds": round(duration, 6),
        "duration_guidance": {
            "normal_minimum_seconds": 150,
            "normal_maximum_seconds": 270,
            "position": (
                "below_normal_range"
                if duration < 150
                else "above_normal_range"
                if duration > 270
                else "within_normal_range"
            ),
            "outside_normal_range_seconds": round(
                max(150 - duration, duration - 270, 0.0), 6
            ),
            "gate_effect": "diagnostic_only_no_minimum_duration",
        },
        "sample_rate": sample_rate,
        "channels": audio.shape[1],
        "peak": round(peak, 8),
        "clipped_samples": clipped_samples,
        "expected_words_raw": len(expected_tokens),
        "asr_words_raw": len(actual_tokens),
        "raw_word_errors": raw_word_errors,
        "raw_word_error_rate": round(raw_wer, 6),
        "expected_words_content_normalized": len(normalized_expected),
        "asr_words_content_normalized": len(normalized_actual),
        "content_word_errors": word_errors,
        "content_word_error_rate": round(wer, 6),
        "maximum_content_word_error_rate": args.maximum_wer,
        "maximum_contiguous_expected_token_gap": maximum_expected_gap,
        "maximum_allowed_contiguous_expected_token_gap": 8,
        "checks": checks,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_temp = report_path.with_suffix(".tmp.json")
    report_temp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    report_temp.replace(report_path)
    print(json.dumps(report, indent=2))
    if report["validation_state"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
