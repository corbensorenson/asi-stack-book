#!/usr/bin/env python3
"""Report mechanical audiovisual risks in a rendered chapter video.

The report deliberately does not issue an aesthetic verdict. It detects
conditions that deserve playback review: freezes, black intervals, silence,
loudness outliers, true-peak overs, missing streams, and plan-duration drift.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> str:
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    if process.returncode:
        detail = (process.stderr or process.stdout).strip()
        raise RuntimeError(f"command failed ({process.returncode}): {' '.join(command)}\n{detail}")
    return (process.stderr or "") + (process.stdout or "")


def ffprobe(path: Path) -> dict:
    output = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(output)


def parse_interval_events(log: str, prefix: str) -> list[dict]:
    starts: list[float] = []
    events: list[dict] = []
    start_re = re.compile(rf"{re.escape(prefix)}_start:\s*(-?\d+(?:\.\d+)?)")
    end_re = re.compile(
        rf"{re.escape(prefix)}_end:\s*(-?\d+(?:\.\d+)?)(?:\s*\|\s*{re.escape(prefix)}_duration:\s*(\d+(?:\.\d+)?))?"
    )
    for line in log.splitlines():
        start_match = start_re.search(line)
        if start_match:
            starts.append(float(start_match.group(1)))
        end_match = end_re.search(line)
        if end_match:
            end = float(end_match.group(1))
            start = starts.pop(0) if starts else end
            duration = float(end_match.group(2)) if end_match.group(2) else max(0.0, end - start)
            events.append({"start": round(start, 3), "end": round(end, 3), "duration": round(duration, 3)})
    return events


def parse_loudness(log: str) -> dict:
    integrated = re.findall(r"\bI:\s*(-?\d+(?:\.\d+)?)\s*LUFS", log)
    range_values = re.findall(r"\bLRA:\s*(\d+(?:\.\d+)?)\s*LU", log)
    true_peaks = re.findall(r"\bPeak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", log)
    return {
        "integrated_lufs": float(integrated[-1]) if integrated else None,
        "loudness_range_lu": float(range_values[-1]) if range_values else None,
        "true_peak_dbtp": float(true_peaks[-1]) if true_peaks else None,
    }


def detect(path: Path, filter_expression: str) -> str:
    return run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af" if filter_expression.startswith("silence") or filter_expression.startswith("ebur") else "-vf", filter_expression, "-f", "null", "-"])


def load_plan_duration(path: Path | None) -> float | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    duration = value.get("target_duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool):
        raise ValueError("beat plan has no numeric target_duration_seconds")
    return float(duration)


def self_test() -> None:
    interval_log = """
[freezedetect @ 0x0] freeze_start: 4.200
[freezedetect @ 0x0] freeze_duration: 6.300
[freezedetect @ 0x0] freeze_end: 10.500
[silencedetect @ 0x0] silence_start: 12.1
[silencedetect @ 0x0] silence_end: 15.8 | silence_duration: 3.7
"""
    freezes = parse_interval_events(interval_log, "freeze")
    silences = parse_interval_events(interval_log, "silence")
    if freezes != [{"start": 4.2, "end": 10.5, "duration": 6.3}]:
        raise AssertionError(f"unexpected freeze parse: {freezes}")
    if silences != [{"start": 12.1, "end": 15.8, "duration": 3.7}]:
        raise AssertionError(f"unexpected silence parse: {silences}")
    loudness = parse_loudness("I: -15.8 LUFS\nLRA: 5.1 LU\nPeak: -1.2 dBFS")
    if loudness != {"integrated_lufs": -15.8, "loudness_range_lu": 5.1, "true_peak_dbtp": -1.2}:
        raise AssertionError(f"unexpected loudness parse: {loudness}")
    print("Self-test passed.")


def audit(path: Path, plan: Path | None, target_lufs: float | None, tolerance: float) -> tuple[dict, list[str], list[str]]:
    metadata = ffprobe(path)
    streams = metadata.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    errors: list[str] = []
    warnings: list[str] = []
    if not video_streams:
        errors.append("video stream is missing")
    if not audio_streams:
        errors.append("audio stream is missing")
    duration = float(metadata.get("format", {}).get("duration") or 0)
    if duration <= 0:
        errors.append("container duration is missing or non-positive")

    plan_duration = load_plan_duration(plan)
    if plan_duration is not None and abs(duration - plan_duration) > 0.25:
        errors.append(f"media duration {duration:.3f}s differs from beat plan {plan_duration:.3f}s")

    freezes: list[dict] = []
    black_intervals: list[dict] = []
    silences: list[dict] = []
    loudness = {"integrated_lufs": None, "loudness_range_lu": None, "true_peak_dbtp": None}
    if video_streams:
        freezes = parse_interval_events(detect(path, "freezedetect=n=-50dB:d=6"), "freeze")
        black_intervals = parse_interval_events(detect(path, "blackdetect=d=1:pix_th=0.10"), "black")
    if audio_streams:
        silences = parse_interval_events(detect(path, "silencedetect=n=-45dB:d=3"), "silence")
        loudness = parse_loudness(detect(path, "ebur128=peak=true"))

    if freezes:
        warnings.append(f"{len(freezes)} freeze interval(s) at least 6s require pedagogical review")
    if black_intervals:
        warnings.append(f"{len(black_intervals)} black interval(s) at least 1s require transition review")
    if silences:
        warnings.append(f"{len(silences)} silence interval(s) at least 3s require pacing review")
    peak = loudness.get("true_peak_dbtp")
    if isinstance(peak, (int, float)) and peak > -1:
        errors.append(f"true peak {peak:.1f} dBTP exceeds the -1 dBTP ceiling")
    integrated = loudness.get("integrated_lufs")
    if target_lufs is not None and isinstance(integrated, (int, float)):
        if abs(integrated - target_lufs) > tolerance:
            warnings.append(
                f"integrated loudness {integrated:.1f} LUFS differs from target {target_lufs:.1f} by more than {tolerance:.1f} LU"
            )

    report = {
        "schema_version": "asi_stack.av_experience_diagnostics.v1",
        "video": str(path.resolve()),
        "duration_seconds": round(duration, 3),
        "plan_duration_seconds": plan_duration,
        "video_stream_count": len(video_streams),
        "audio_stream_count": len(audio_streams),
        "freezes": freezes,
        "black_intervals": black_intervals,
        "silences": silences,
        "loudness": loudness,
        "interpretation": "Mechanical diagnostics only; complete playback and experience scoring remain required.",
    }
    return report, warnings, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path, nargs="?")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--target-lufs", type=float)
    parser.add_argument("--lufs-tolerance", type=float, default=1.5)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.video is None:
        parser.error("video is required unless --self-test is used")
    for executable in ("ffmpeg", "ffprobe"):
        if shutil.which(executable) is None:
            raise SystemExit(f"required executable is unavailable: {executable}")
    if not args.video.is_file():
        raise SystemExit(f"video does not exist: {args.video}")
    try:
        report, warnings, errors = audit(args.video, args.plan, args.target_lufs, args.lufs_tolerance)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        raise SystemExit(f"Unable to audit video: {exc}") from exc
    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Audiovisual diagnostics failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Audiovisual diagnostics completed; aesthetic review is still required.")


if __name__ == "__main__":
    main()
