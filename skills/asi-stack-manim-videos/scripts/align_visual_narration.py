#!/usr/bin/env python3
"""Align exact ASI Stack narration text and emit a fail-closed phrase receipt."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ALIGNER_ID = "stable-ts-2.19.1-mlx-whisper-exact-text-phrase-v1"
MLX_WHISPER_COMMIT = "796f5b53cab69a3d48a44233ce21aae889e94a08"
MAX_INSTANT_WORD_FRACTION = 0.025
MAX_EDGE_GAP_SECONDS = 1.5
MAX_JOIN_DRIFT_SECONDS = 1.5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def normalized_words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", value.lower())


def beat_contract_sha256(beat_plan: dict[str, Any]) -> str:
    projection = {
        "chapter_id": beat_plan.get("chapter_id"),
        "narration_sha256": beat_plan.get("narration_sha256"),
        "target_duration_seconds": beat_plan.get("target_duration_seconds"),
        "beats": [
            {
                key: beat.get(key)
                for key in (
                    "id", "macro_move_id", "performance_block_id", "start_seconds",
                    "end_seconds", "narration", "sync_anchor",
                )
            }
            for beat in beat_plan.get("beats", [])
        ],
    }
    payload = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative(path)} must contain a JSON object")
    return value


def flatten_words(alignment: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    terms: list[str] = []
    owners: list[dict[str, Any]] = []
    words: list[dict[str, Any]] = []
    for segment in alignment.get("segments", []):
        for word in segment.get("words", []):
            if not isinstance(word, dict):
                continue
            word_terms = normalized_words(str(word.get("word", "")))
            if not word_terms:
                continue
            words.append(word)
            terms.extend(word_terms)
            owners.extend([word] * len(word_terms))
    return terms, owners, words


def unique_phrase(
    phrase: str,
    terms: list[str],
    owners: list[dict[str, Any]],
) -> tuple[int, int, dict[str, Any]]:
    query = normalized_words(phrase)
    hits = [
        index
        for index in range(len(terms) - len(query) + 1)
        if terms[index:index + len(query)] == query
    ]
    if len(hits) != 1:
        raise ValueError(f"alignment phrase must occur exactly once: {phrase!r}; hits={hits}")
    start_index = hits[0]
    end_index = start_index + len(query) - 1
    phrase_owners = owners[start_index:end_index + 1]
    unique_owners = list({id(word): word for word in phrase_owners}.values())
    start = float(owners[start_index]["start"])
    end = float(owners[end_index]["end"])
    return start_index, end_index, {
        "start_seconds": round(start, 3),
        "end_seconds": round(end, 3),
        "duration_seconds": round(end - start, 3),
        "instant_word_count": sum(
            float(word["end"]) <= float(word["start"]) for word in unique_owners
        ),
    }


def evaluate_alignment(
    alignment: dict[str, Any],
    transcript: str,
    beat_plan: dict[str, Any],
    narration_receipt: dict[str, Any],
    audio_duration: float,
) -> dict[str, Any]:
    expected_terms = normalized_words(transcript)
    aligned_terms, owners, words = flatten_words(alignment)
    instant_words = [word for word in words if float(word["end"]) <= float(word["start"])]
    overlap_count = sum(
        float(current["start"]) < float(previous["end"]) - 0.001
        for previous, current in zip(words, words[1:])
    )
    reverse_count = sum(
        float(current["start"]) < float(previous["start"])
        for previous, current in zip(words, words[1:])
    )

    anchors = []
    anchor_errors = []
    for beat in beat_plan.get("beats", []):
        phrase = str(beat.get("sync_anchor", ""))
        try:
            _, _, timing = unique_phrase(phrase, aligned_terms, owners)
        except ValueError as exc:
            anchor_errors.append(str(exc))
            continue
        if timing["duration_seconds"] <= 0:
            anchor_errors.append(f"{beat.get('id')}: non-positive phrase duration")
        anchors.append({
            "beat_id": beat.get("id"),
            "phrase": phrase,
            **timing,
        })

    joins = []
    cumulative_terms = 0
    block_start = 0.0
    source_segments = narration_receipt.get("segments", [])
    for index, segment in enumerate(source_segments):
        block_terms = normalized_words(str(segment.get("written_text", "")))
        first_term = cumulative_terms
        last_term = cumulative_terms + len(block_terms) - 1
        generated_end = block_start + float(segment.get("generated_duration_seconds", 0.0))
        next_start = generated_end + float(segment.get("following_pause_seconds", 0.0))
        if first_term < len(owners) and last_term < len(owners):
            observed_start = float(owners[first_term]["start"])
            observed_end = float(owners[last_term]["end"])
            start_drift = abs(observed_start - block_start)
            end_drift = abs(observed_end - generated_end)
            passed = start_drift <= MAX_JOIN_DRIFT_SECONDS and end_drift <= MAX_JOIN_DRIFT_SECONDS
        else:
            observed_start = observed_end = None
            start_drift = end_drift = None
            passed = False
        joins.append({
            "segment_index": segment.get("index", index + 1),
            "expected_start_seconds": round(block_start, 3),
            "expected_generated_end_seconds": round(generated_end, 3),
            "observed_first_word_start_seconds": None if observed_start is None else round(observed_start, 3),
            "observed_last_word_end_seconds": None if observed_end is None else round(observed_end, 3),
            "start_drift_seconds": None if start_drift is None else round(start_drift, 3),
            "end_drift_seconds": None if end_drift is None else round(end_drift, 3),
            "passed": passed,
        })
        cumulative_terms += len(block_terms)
        block_start = next_start

    first_start = float(words[0]["start"]) if words else audio_duration
    last_end = float(words[-1]["end"]) if words else 0.0
    checks = {
        "exact_normalized_transcript": aligned_terms == expected_terms,
        "aligned_term_count": len(aligned_terms),
        "expected_term_count": len(expected_terms),
        "nonempty_alignment": bool(words),
        "monotonic_word_starts": reverse_count == 0,
        "nonoverlapping_words": overlap_count == 0,
        "instant_word_count": len(instant_words),
        "instant_word_fraction": round(len(instant_words) / max(1, len(words)), 6),
        "instant_word_fraction_within_phrase_scope": (
            len(instant_words) / max(1, len(words)) <= MAX_INSTANT_WORD_FRACTION
        ),
        "beginning_gap_seconds": round(first_start, 3),
        "ending_gap_seconds": round(audio_duration - last_end, 3),
        "edge_coverage_passed": (
            first_start <= MAX_EDGE_GAP_SECONDS
            and 0 <= audio_duration - last_end <= MAX_EDGE_GAP_SECONDS
        ),
        "sync_anchor_count": len(anchors),
        "expected_sync_anchor_count": len(beat_plan.get("beats", [])),
        "all_sync_anchors_unique_and_positive": (
            not anchor_errors and len(anchors) == len(beat_plan.get("beats", []))
        ),
        "generation_join_count": len(joins),
        "all_generation_joins_within_tolerance": bool(joins) and all(row["passed"] for row in joins),
    }
    passed = all([
        checks["exact_normalized_transcript"],
        checks["nonempty_alignment"],
        checks["monotonic_word_starts"],
        checks["nonoverlapping_words"],
        checks["instant_word_fraction_within_phrase_scope"],
        checks["edge_coverage_passed"],
        checks["all_sync_anchors_unique_and_positive"],
        checks["all_generation_joins_within_tolerance"],
    ])
    return {
        "verdict": "pass" if passed else "fail",
        "checks": checks,
        "anchors": anchors,
        "anchor_errors": anchor_errors,
        "instant_words": [
            {
                "word": str(word["word"]).strip(),
                "start_seconds": round(float(word["start"]), 3),
                "end_seconds": round(float(word["end"]), 3),
            }
            for word in instant_words
        ],
        "generation_joins": joins,
    }


def run_alignment(audio: Path, transcript: str, model_path: Path, output: Path) -> dict[str, Any]:
    # stable-ts 2.19.1 names the public MLX N_FRAMES constant N_FRAMES_MLX.
    # The alias is explicit and receipt-bound; installed package files stay untouched.
    import mlx_whisper.audio as mlx_audio

    mlx_audio.N_FRAMES_MLX = mlx_audio.N_FRAMES
    import stable_whisper

    model = stable_whisper.load_mlx_whisper(str(model_path))
    result = model.align(str(audio), transcript.strip(), language="en", original_split=True)
    if result is None:
        raise RuntimeError("stable-ts returned no alignment")
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save_as_json(str(output))
    return read_json(output)


def build_receipt(args: argparse.Namespace) -> dict[str, Any]:
    audio = args.audio.resolve()
    narration = args.narration.resolve()
    beat_plan_path = args.beat_plan.resolve()
    narration_receipt_path = args.narration_receipt.resolve()
    narration_verification_path = args.narration_verification.resolve()
    model_path = args.model.resolve()
    output = args.output.resolve()
    transcript = narration.read_text(encoding="utf-8").strip()
    beat_plan = read_json(beat_plan_path)
    narration_receipt = read_json(narration_receipt_path)
    alignment = run_alignment(audio, transcript, model_path, output)
    duration = float(narration_receipt["duration_seconds"])
    evaluation = evaluate_alignment(alignment, transcript, beat_plan, narration_receipt, duration)
    config = model_path / "config.json"
    weights = model_path / "weights.npz"
    lock = (ROOT / "visual_edition/alignment_requirements.lock.txt").resolve()
    receipt = {
        "schema_version": "asi_stack.manim_alignment_receipt.v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "chapter_id": beat_plan.get("chapter_id"),
        "aligner": {
            "aligner_id": ALIGNER_ID,
            "stable_ts_version": importlib.metadata.version("stable-ts"),
            "mlx_whisper_version": importlib.metadata.version("mlx-whisper"),
            "mlx_whisper_commit": MLX_WHISPER_COMMIT,
            "python_version": sys.version.split()[0],
            "method": "exact-transcript-constrained cross-attention dynamic-time-warping phrase alignment",
            "compatibility_alias": "mlx_whisper.audio.N_FRAMES_MLX = mlx_whisper.audio.N_FRAMES",
            "options": {
                "language": "en",
                "original_split": True,
                "terminal_transcript_whitespace": "stripped",
            },
            "requirements_lock_path": relative(lock),
            "requirements_lock_sha256": sha256(lock),
        },
        "model": {
            "path": relative(model_path),
            "config_sha256": sha256(config),
            "weights_sha256": sha256(weights),
        },
        "inputs": {
            "audio_path": relative(audio),
            "audio_sha256": sha256(audio),
            "narration_path": relative(narration),
            "narration_sha256": sha256(narration),
            "beat_plan_path": relative(beat_plan_path),
            "beat_contract_sha256": beat_contract_sha256(beat_plan),
            "narration_receipt_path": relative(narration_receipt_path),
            "narration_receipt_sha256": sha256(narration_receipt_path),
            "narration_verification_path": relative(narration_verification_path),
            "narration_verification_sha256": sha256(narration_verification_path),
        },
        "raw_alignment": {
            "path": relative(output),
            "sha256": sha256(output),
            "tracked": False,
        },
        **evaluation,
        "qualified_scope": "phrase anchors, caption lines, and generation-block joins only",
        "single_word_cue_policy": "instantaneous word boundaries are not qualified; use a reviewed phrase span",
        "forced_phoneme_alignment_claimed": False,
        "manual_review_required": True,
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "This receipt checks one synthetic narration against exact text and declared phrase anchors. "
            "It does not establish phoneme timing, listener comprehension, teaching quality, chapter truth, "
            "or publication authority."
        ),
    }
    return receipt


def self_test() -> None:
    transcript = "Alpha boundary. Beta joins."
    alignment = {
        "segments": [{"words": [
            {"word": " Alpha", "start": 0.1, "end": 0.4},
            {"word": " boundary.", "start": 0.4, "end": 0.8},
            {"word": " Beta", "start": 1.0, "end": 1.2},
            {"word": " joins.", "start": 1.2, "end": 1.6},
        ]}],
    }
    beat_plan = {"beats": [{"id": "b01", "sync_anchor": "Beta joins"}]}
    narration_receipt = {"segments": [{
        "index": 1,
        "written_text": transcript,
        "generated_duration_seconds": 1.7,
        "following_pause_seconds": 0.0,
    }]}
    result = evaluate_alignment(alignment, transcript, beat_plan, narration_receipt, 1.7)
    if result["verdict"] != "pass":
        raise AssertionError(result)
    bad = json.loads(json.dumps(alignment))
    bad["segments"][0]["words"][-1]["word"] = " drifts."
    if evaluate_alignment(bad, transcript, beat_plan, narration_receipt, 1.7)["verdict"] != "fail":
        raise AssertionError("transcript drift was not rejected")
    print("align_visual_narration self-test passed: valid phrase timing accepted; transcript drift rejected.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--narration", type=Path)
    parser.add_argument("--beat-plan", type=Path)
    parser.add_argument("--narration-receipt", type=Path)
    parser.add_argument("--narration-verification", type=Path)
    parser.add_argument("--model", type=Path, default=ROOT / "build/visual_edition/models/whisper-small.en-mlx")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        missing = [
            name for name in (
                "audio", "narration", "beat_plan", "narration_receipt",
                "narration_verification", "output", "receipt",
            ) if getattr(args, name) is None
        ]
        if missing:
            parser.error(f"missing required arguments: {', '.join(missing)}")
    return args


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0
    receipt = build_receipt(args)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {relative(args.receipt)}: {receipt['verdict']}")
    return 0 if receipt["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
