#!/usr/bin/env python3
"""Render deterministic local narration for an ASI Stack visual-edition script."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def speech_text(text: str, lexicon: dict[str, str]) -> str:
    """Apply visible, versioned pronunciation substitutions."""
    for written in sorted(lexicon, key=len, reverse=True):
        text = re.sub(
            rf"(?<![\w-]){re.escape(written)}(?![\w-])",
            lexicon[written],
            text,
        )
    return text


def split_long_unit(value: str, maximum_characters: int) -> list[str]:
    """Hard-split an overlong sentence at the strongest available boundary."""
    value = re.sub(r"\s+", " ", value).strip()
    result: list[str] = []
    minimum_boundary = max(40, maximum_characters // 2)
    while len(value) > maximum_characters:
        window = value[:maximum_characters]
        candidates = [
            match.end()
            for match in re.finditer(r"[;:,.!?]", window)
            if match.end() >= minimum_boundary
        ]
        cut = max(candidates) if candidates else window.rfind(" ")
        if cut < minimum_boundary:
            cut = maximum_characters
        piece = value[:cut].strip()
        if not piece:
            raise ValueError("unable to split an overlong narration unit")
        result.append(piece)
        value = value[cut:].strip()
    if value:
        result.append(value)
    if any(len(item) > maximum_characters for item in result):
        raise ValueError("narration hard-cap split failed")
    return result


def segments(text: str, maximum_characters: int) -> list[tuple[str, bool]]:
    """Split prose at paragraph and sentence boundaries.

    The boolean marks the final segment in a source paragraph so the renderer
    can insert a longer semantic pause without feeding oversized text to TTS.
    """
    result: list[tuple[str, bool]] = []
    paragraphs = [
        re.sub(r"\s+", " ", paragraph.strip())
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]
    for paragraph in paragraphs:
        sentences = []
        for item in re.split(r"(?<=[.!?])\s+", paragraph):
            if item.strip():
                sentences.extend(split_long_unit(item, maximum_characters))
        paragraph_segments: list[str] = []
        buffer = ""
        for sentence in sentences:
            candidate = f"{buffer} {sentence}".strip()
            if buffer and len(candidate) > maximum_characters:
                paragraph_segments.append(buffer)
                buffer = sentence
            else:
                buffer = candidate
        if buffer:
            paragraph_segments.append(buffer)
        for index, item in enumerate(paragraph_segments):
            result.append((item, index == len(paragraph_segments) - 1))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Repository-relative narration text")
    parser.add_argument("--output", required=True, help="Ignored-build WAV destination")
    parser.add_argument(
        "--model-dir",
        default="build/visual_edition/models/Kokoro-82M-bf16",
    )
    parser.add_argument(
        "--lexicon",
        default="visual_edition/narration_pronunciations.json",
    )
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--sample-rate", type=int, choices=(24000, 48000), default=24000)
    parser.add_argument("--sentence-pause", type=float, default=0.22)
    parser.add_argument("--paragraph-pause", type=float, default=0.48)
    parser.add_argument("--maximum-characters", type=int, default=300)
    parser.add_argument("--ffmpeg", default="/opt/homebrew/bin/ffmpeg")
    parser.add_argument("--integrated-lufs", type=float, default=-16.0)
    parser.add_argument("--true-peak-dbtp", type=float, default=-1.5)
    parser.add_argument("--loudness-range", type=float, default=11.0)
    args = parser.parse_args()

    text_path = ROOT / args.text
    output_path = ROOT / args.output
    model_dir = ROOT / args.model_dir
    lexicon_path = ROOT / args.lexicon
    receipt_path = output_path.with_suffix(".receipt.json")

    source_text = text_path.read_text(encoding="utf-8").strip()
    lexicon_document = json.loads(lexicon_path.read_text(encoding="utf-8"))
    lexicon = lexicon_document["substitutions"]
    work = segments(source_text, args.maximum_characters)
    if not work:
        raise SystemExit("Narration text is empty")

    from kokoro_mlx import KokoroTTS

    rendered: list[np.ndarray] = []
    segment_receipts = []
    with KokoroTTS.from_pretrained(model_dir) as tts:
        if args.voice not in tts.list_voices():
            raise SystemExit(f"Voice is not installed: {args.voice}")
        for index, (written_text, paragraph_end) in enumerate(work, start=1):
            spoken_text = speech_text(written_text, lexicon)
            result = tts.generate(
                spoken_text,
                voice=args.voice,
                speed=args.speed,
                sample_rate=args.sample_rate,
                language="en-us",
            )
            audio = np.asarray(result.audio, dtype=np.float32)
            rendered.append(audio)
            pause_seconds = (
                args.paragraph_pause if paragraph_end else args.sentence_pause
            )
            if index != len(work):
                rendered.append(
                    np.zeros(round(args.sample_rate * pause_seconds), dtype=np.float32)
                )
            segment_receipts.append(
                {
                    "index": index,
                    "written_text": written_text,
                    "spoken_text": spoken_text,
                    "paragraph_end": paragraph_end,
                    "generated_duration_seconds": round(result.duration, 6),
                    "following_pause_seconds": (
                        0 if index == len(work) else pause_seconds
                    ),
                }
            )

    master = np.concatenate(rendered)
    peak = float(np.max(np.abs(master)))
    if peak >= 1:
        master = master / (peak * 1.001)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path = output_path.with_suffix(".unnormalized.wav")
    sf.write(raw_path, master, args.sample_rate, subtype="PCM_24")
    subprocess.run(
        [
            args.ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(raw_path),
            "-af",
            (
                f"loudnorm=I={args.integrated_lufs}:"
                f"TP={args.true_peak_dbtp}:LRA={args.loudness_range}"
            ),
            "-ar",
            str(args.sample_rate),
            "-ac",
            "1",
            "-c:a",
            "pcm_s24le",
            str(output_path),
        ],
        check=True,
    )
    raw_path.unlink()
    normalized, normalized_sample_rate = sf.read(output_path, always_2d=True)
    if normalized_sample_rate != args.sample_rate:
        raise SystemExit("FFmpeg changed the narration sample rate")
    normalized_peak = float(np.max(np.abs(normalized)))

    model_files = [
        model_dir / "config.json",
        model_dir / "kokoro-v1_0.safetensors",
        model_dir / "voices" / f"{args.voice}.safetensors",
    ]
    receipt = {
        "schema_version": "asi_stack.local_narration_render.v1",
        "rendered_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "renderer_sha256": sha256(Path(__file__)),
        "input_path": args.text,
        "input_sha256": sha256(text_path),
        "lexicon_path": args.lexicon,
        "lexicon_sha256": sha256(lexicon_path),
        "model_dir": args.model_dir,
        "model_file_sha256": {
            str(path.relative_to(ROOT)): sha256(path) for path in model_files
        },
        "voice": args.voice,
        "speed": args.speed,
        "sample_rate": args.sample_rate,
        "segmentation": {
            "maximum_characters": args.maximum_characters,
            "maximum_observed_characters": max(
                len(item["written_text"]) for item in segment_receipts
            ),
            "sentence_pause_seconds": args.sentence_pause,
            "paragraph_pause_seconds": args.paragraph_pause,
        },
        "duration_seconds": round(len(master) / args.sample_rate, 6),
        "peak_before_safety_limit": round(peak, 8),
        "normalization": {
            "filter": "ffmpeg_loudnorm_single_pass",
            "integrated_lufs_target": args.integrated_lufs,
            "true_peak_dbtp_target": args.true_peak_dbtp,
            "loudness_range_target": args.loudness_range,
            "normalized_sample_peak": round(normalized_peak, 8),
        },
        "output_path": args.output,
        "output_sha256": sha256(output_path),
        "segments": segment_receipts,
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Rendered {len(work)} segments, {receipt['duration_seconds']:.3f}s, "
        f"{args.voice} -> {args.output}"
    )


if __name__ == "__main__":
    main()
