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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    parser.add_argument("--audio", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--asr", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--maximum-wer", type=float, default=0.03)
    args = parser.parse_args()

    audio_path = ROOT / args.audio
    receipt_path = ROOT / args.receipt
    asr_path = ROOT / args.asr
    report_path = ROOT / args.report
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    asr = json.loads(asr_path.read_text(encoding="utf-8"))
    audio, sample_rate = sf.read(audio_path, always_2d=True)
    duration = len(audio) / sample_rate
    peak = float(np.max(np.abs(audio)))
    clipped_samples = int(np.count_nonzero(np.abs(audio) >= 0.999))
    expected_text = " ".join(item["spoken_text"] for item in receipt["segments"])
    expected_tokens = tokens(expected_text)
    actual_tokens = tokens(asr["text"])
    raw_word_errors = edit_distance(expected_tokens, actual_tokens)
    raw_wer = raw_word_errors / max(1, len(expected_tokens))
    normalized_expected = normalize_version_labels(
        normalize_audio_homophones(
            normalize_compounds(
                normalize_number_words(collapse_letter_runs(expected_tokens))
            )
        )
    )
    normalized_actual = normalize_version_labels(
        normalize_audio_homophones(
            normalize_compounds(
                normalize_number_words(collapse_letter_runs(actual_tokens))
            )
        )
    )
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
            == sha256(ROOT / "scripts/render_visual_narration.py")
        ),
        "audio_digest_matches_receipt": sha256(audio_path) == receipt["output_sha256"],
        "duration_matches_receipt": abs(duration - receipt["duration_seconds"]) <= 0.001,
        "duration_within_visual_edition_contract": duration >= 180,
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
            "preferred_minimum_seconds": 180,
            "soft_target_maximum_seconds": 360,
            "position": (
                "below_preferred_range"
                if duration < 180
                else "above_soft_target"
                if duration > 360
                else "within_preferred_range"
            ),
            "over_soft_target_seconds": round(max(0.0, duration - 360), 6),
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
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["validation_state"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
