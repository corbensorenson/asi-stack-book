#!/usr/bin/env python3
"""Produce and locally validate one or more non-pilot chapter A/V masters."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TTS_PYTHON = ROOT / "build/visual_edition/tts_venv/bin/python"
MANIM = ROOT / "build/visual_edition/venv/bin/manim"
WHISPER = ROOT / "build/visual_edition/tts_venv/bin/mlx_whisper"
WHISPER_MODEL = ROOT / "build/visual_edition/models/whisper-small.en-mlx"
FFMPEG = Path("/opt/homebrew/bin/ffmpeg")
FFPROBE = Path("/opt/homebrew/bin/ffprobe")
FINAL_DIR = ROOT / "build/visual_edition/final"
AUDIO_DIR = ROOT / "build/visual_edition/audio"
RENDER_DIR = ROOT / "build/visual_edition/render"
REVIEW_DIR = ROOT / "build/visual_edition/review/generated"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}


def run(command: list[str], log: Path | None = None) -> None:
    print("+", " ".join(command), flush=True)
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("w", encoding="utf-8") as stream:
            subprocess.run(command, cwd=ROOT, check=True, stdout=stream, stderr=subprocess.STDOUT)
    else:
        subprocess.run(command, cwd=ROOT, check=True)


def receipt(slug: str) -> dict:
    return json.loads(
        (AUDIO_DIR / f"{slug}-narration-master.receipt.json").read_text(encoding="utf-8")
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def narration(slug: str, force: bool) -> None:
    source = ROOT / f"visual_edition/chapters/{slug}/narration.txt"
    output = AUDIO_DIR / f"{slug}-narration-master.wav"
    receipt_path = output.with_suffix(".receipt.json")
    if not force and output.is_file() and receipt_path.is_file():
        import hashlib

        current = hashlib.sha256(source.read_bytes()).hexdigest()
        value = json.loads(receipt_path.read_text(encoding="utf-8"))
        renderer_digest = hashlib.sha256(
            (ROOT / "scripts/render_visual_narration.py").read_bytes()
        ).hexdigest()
        lexicon_digest = hashlib.sha256(
            (ROOT / "visual_edition/narration_pronunciations.json").read_bytes()
        ).hexdigest()
        if (
            value.get("input_sha256") == current
            and value.get("renderer_sha256") == renderer_digest
            and value.get("lexicon_sha256") == lexicon_digest
            and value.get("voice") == "af_heart"
            and value.get("speed") == 1.08
            and value.get("sample_rate") == 24000
            and value.get("segmentation") == {
                "maximum_characters": 300,
                "maximum_observed_characters": value.get(
                    "segmentation", {}
                ).get("maximum_observed_characters"),
                "sentence_pause_seconds": 0.22,
                "paragraph_pause_seconds": 0.48,
            }
        ):
            print(f"{slug}: narration current", flush=True)
            return
    run([
        str(TTS_PYTHON),
        "scripts/render_visual_narration.py",
        "--text", f"visual_edition/chapters/{slug}/narration.txt",
        "--output", f"build/visual_edition/audio/{slug}-narration-master.wav",
        "--speed", "1.08",
    ])


def captions(slug: str) -> None:
    run([
        "python3",
        "scripts/build_visual_captions_from_narration_receipt.py",
        "--receipt", f"build/visual_edition/audio/{slug}-narration-master.receipt.json",
        "--output", f"visual_edition/chapters/{slug}/captions.vtt",
    ])


def asr(slug: str, force: bool) -> None:
    output = AUDIO_DIR / f"{slug}-narration-master.json"
    if force or not output.is_file():
        run([
            str(WHISPER),
            f"build/visual_edition/audio/{slug}-narration-master.wav",
            "--model", "build/visual_edition/models/whisper-small.en-mlx",
            "--output-name", f"{slug}-narration-master",
            "--output-dir", "build/visual_edition/audio",
            "--output-format", "json",
            "--language", "en",
            "--verbose", "False",
        ])
    run([
        str(TTS_PYTHON),
        "scripts/validate_visual_narration.py",
        "--audio", f"build/visual_edition/audio/{slug}-narration-master.wav",
        "--receipt", f"build/visual_edition/audio/{slug}-narration-master.receipt.json",
        "--asr", f"build/visual_edition/audio/{slug}-narration-master.json",
        "--report", f"build/visual_edition/audio/{slug}-narration-master.validation.json",
    ])


def visual(slug: str, force: bool) -> Path:
    output = RENDER_DIR / slug / "videos/scene/1080p30/ChapterVisualAbstract.mp4"
    inputs = [
        ROOT / f"visual_edition/chapters/{slug}/scene.py",
        ROOT / f"visual_edition/chapters/{slug}/scene_spec.json",
        ROOT / "visual_edition/lib/chapter_scene.py",
        ROOT / "visual_edition/lib/asi_visuals.py",
        ROOT / "visual_edition/manim.cfg",
    ]
    current = (
        output.is_file()
        and output.stat().st_mtime >= max(path.stat().st_mtime for path in inputs)
    )
    if force or not current:
        run([
            str(MANIM),
            "--config_file", "visual_edition/manim.cfg",
            "--disable_caching",
            f"visual_edition/chapters/{slug}/scene.py",
            "ChapterVisualAbstract",
            "--media_dir", f"build/visual_edition/render/{slug}",
        ], RENDER_DIR / slug / "manim.log")
    if not output.is_file():
        raise SystemExit(f"Manim output missing: {output}")
    return output


def mux(
    slug: str,
    visual_path: Path,
    visual_endpoints: list[float] | None = None,
) -> Path:
    data = receipt(slug)
    audio_duration = float(data["duration_seconds"])
    audio_endpoints = []
    cursor = 0.0
    for segment in data["segments"]:
        cursor += float(segment["generated_duration_seconds"])
        cursor += float(segment["following_pause_seconds"])
        if segment["paragraph_end"]:
            audio_endpoints.append(cursor)
    probe = subprocess.check_output(
        [
            str(FFPROBE), "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(visual_path),
        ],
        cwd=ROOT,
        text=True,
    ).strip()
    visual_duration = float(probe)
    if visual_duration <= 0:
        raise RuntimeError(f"invalid visual duration for {slug}: {visual_duration}")
    final = FINAL_DIR / f"{slug}.mp4"
    final.parent.mkdir(parents=True, exist_ok=True)
    segment_ratios = []
    if visual_endpoints is None:
        source_endpoints = json.loads(
            (
                ROOT / f"visual_edition/chapters/{slug}/scene_spec.json"
            ).read_text(encoding="utf-8")
        )["timing"]["scene_endpoints_seconds"]
        if len(source_endpoints) != 7 or len(audio_endpoints) != 7:
            raise RuntimeError(f"non-pilot endpoint count drift: {slug}")
        # The scene specification is already synchronized to the exact seven
        # narration paragraph boundaries. Container duration can differ by one
        # encoded frame, so using it as a time-scale authority would needlessly
        # move otherwise exact internal boundaries. Preserve the source timing;
        # the existing tpad/-t pair handles only the terminal frame rounding.
        ratio = audio_endpoints[-1] / source_endpoints[-1]
        aligned_endpoints = [value * ratio for value in source_endpoints]
        segment_ratios = [ratio] * 7
        alignment_method = "source_exact_timing_with_tail_frame_correction"
        video_filter = (
            f"[0:v]setpts={ratio:.12f}*PTS,fps=30,scale=1920:1080,"
            "tpad=stop_mode=clone:stop_duration=1,format=yuv420p[v]"
        )
    else:
        if len(visual_endpoints) != 7 or len(audio_endpoints) != 7:
            raise RuntimeError(f"pilot endpoint count drift: {slug}")
        if visual_endpoints[-1] > visual_duration + 0.05:
            raise RuntimeError(
                f"pilot endpoint exceeds source visual duration: {slug}"
            )
        filters = []
        labels = []
        source_endpoints = visual_endpoints
        aligned_endpoints = audio_endpoints
        alignment_method = "piecewise_seven_scene_paragraph_binding"
        visual_start = audio_start = 0.0
        for index, (visual_end, audio_end) in enumerate(
            zip(visual_endpoints, audio_endpoints)
        ):
            visual_span = visual_end - visual_start
            audio_span = audio_end - audio_start
            if visual_span <= 0 or audio_span <= 0:
                raise RuntimeError(f"non-positive pilot scene span: {slug}")
            ratio = audio_span / visual_span
            segment_ratios.append(ratio)
            filters.append(
                f"[0:v]trim=start={visual_start:.6f}:end={visual_end:.6f},"
                f"setpts={ratio:.12f}*(PTS-STARTPTS),fps=30,format=yuv420p[v{index}]"
            )
            labels.append(f"[v{index}]")
            visual_start, audio_start = visual_end, audio_end
        filters.append(
            "".join(labels)
            + "concat=n=7:v=1:a=0,"
            "scale=1920:1080,tpad=stop_mode=clone:stop_duration=1,"
            "format=yuv420p[v]"
        )
        video_filter = ";".join(filters)
    run([
        str(FFMPEG),
        "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(visual_path),
        "-i", f"build/visual_edition/audio/{slug}-narration-master.wav",
        "-filter_complex",
        video_filter,
        "-map", "[v]", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1",
        "-movflags", "+faststart",
        "-t", f"{audio_duration:.6f}",
        str(final),
    ])
    maximum_error = max(
        abs(actual - expected)
        for actual, expected in zip(aligned_endpoints, audio_endpoints)
    )
    mux_receipt = {
        "schema_version": "asi_stack.local_visual_mux.v1",
        "chapter_id": slug,
        "alignment_method": alignment_method,
        "source_visual_path": str(visual_path.relative_to(ROOT)),
        "source_visual_sha256": sha256(visual_path),
        "source_visual_duration_seconds": visual_duration,
        "source_visual_scene_endpoints_seconds": source_endpoints,
        "audio_path": f"build/visual_edition/audio/{slug}-narration-master.wav",
        "audio_sha256": data["output_sha256"],
        "audio_receipt_sha256": sha256(
            AUDIO_DIR / f"{slug}-narration-master.receipt.json"
        ),
        "audio_scene_endpoints_seconds": audio_endpoints,
        "segment_time_scale_ratios": segment_ratios,
        "aligned_scene_endpoints_seconds": aligned_endpoints,
        "maximum_scene_endpoint_error_seconds": maximum_error,
        "output_path": str(final.relative_to(ROOT)),
        "output_sha256": sha256(final),
    }
    (FINAL_DIR / f"{slug}.mux.json").write_text(
        json.dumps(mux_receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    return final


def extract_review_frames(slug: str, final: Path) -> None:
    """Extract one stable midpoint frame from each exact narration scene."""
    mux_path = FINAL_DIR / f"{slug}.mux.json"
    if not mux_path.exists():
        raise SystemExit(f"Missing mux receipt for review extraction: {mux_path}")
    mux_receipt = json.loads(mux_path.read_text(encoding="utf-8"))
    endpoints = [
        float(value)
        for value in mux_receipt["audio_scene_endpoints_seconds"]
    ]
    if len(endpoints) != 7:
        raise SystemExit(
            f"{slug}: expected seven audio scene endpoints, got {len(endpoints)}"
        )
    starts = [0.0, *endpoints[:-1]]
    sample_times = [
        start + ((end - start) / 2.0)
        for start, end in zip(starts, endpoints)
    ]
    review = REVIEW_DIR / slug
    review.mkdir(parents=True, exist_ok=True)
    for index, sample_time in enumerate(sample_times, start=1):
        run([
            str(FFMPEG),
            "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{sample_time:.3f}",
            "-i", str(final),
            "-frames:v", "1",
            str(review / f"{index:02d}.png"),
        ])


def validate_master(slug: str, final: Path) -> None:
    report = FINAL_DIR / f"{slug}.validation.json"
    run([
        "python3",
        "scripts/validate_visual_master.py",
        "--video", str(final.relative_to(ROOT)),
        "--captions", f"visual_edition/chapters/{slug}/captions.vtt",
        "--narration-validation",
        f"build/visual_edition/audio/{slug}-narration-master.validation.json",
        "--mux-receipt", f"build/visual_edition/final/{slug}.mux.json",
        "--report", str(report.relative_to(ROOT)),
    ])
    extract_review_frames(slug, final)


def chapter_ids(include_pilots: bool = False) -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
        if include_pilots or chapter["id"] not in PILOTS
    ]


def produce(slug: str, phases: set[str], force: bool) -> None:
    print(f"=== {slug} ===", flush=True)
    if "narration" in phases:
        narration(slug, force)
    if "captions" in phases:
        captions(slug)
    if "asr" in phases:
        asr(slug, force)
    visual_path = None
    if "visual" in phases:
        visual_path = visual(slug, force)
    if "mux" in phases:
        visual_path = visual_path or visual(slug, False)
        final = mux(slug, visual_path)
        validate_master(slug, final)
    elif "review" in phases:
        final = FINAL_DIR / f"{slug}.mp4"
        if not final.exists():
            raise SystemExit(f"Missing final master for review extraction: {final}")
        extract_review_frames(slug, final)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-non-pilots", action="store_true")
    parser.add_argument("--all-chapters", action="store_true")
    parser.add_argument(
        "--phases",
        default="narration,captions,asr,visual,mux",
        help="Comma-separated narration,captions,asr,visual,mux,review",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    selected = (
        chapter_ids(include_pilots=args.all_chapters)
        if args.all_non_pilots or args.all_chapters
        else args.chapter
    )
    if not selected:
        raise SystemExit("Select --chapter or --all-non-pilots")
    phases = {item.strip() for item in args.phases.split(",") if item.strip()}
    unknown = phases - {"narration", "captions", "asr", "visual", "mux", "review"}
    if unknown:
        raise SystemExit(f"Unknown phases: {sorted(unknown)}")
    for slug in selected:
        produce(slug, phases, args.force)


if __name__ == "__main__":
    main()
