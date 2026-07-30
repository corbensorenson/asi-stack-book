#!/usr/bin/env python3
"""Validate one ignored-build ASI Stack final A/V master and caption track."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seconds(timestamp: str) -> float:
    hours, minutes, remainder = timestamp.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(remainder)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--captions", required=True)
    parser.add_argument("--narration-validation", required=True)
    parser.add_argument("--mux-receipt", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--ffprobe", default="/opt/homebrew/bin/ffprobe")
    args = parser.parse_args()

    video_path = ROOT / args.video
    captions_path = ROOT / args.captions
    narration_validation_path = ROOT / args.narration_validation
    mux_receipt_path = ROOT / args.mux_receipt
    report_path = ROOT / args.report
    probe = json.loads(
        subprocess.run(
            [
                args.ffprobe,
                "-v",
                "error",
                "-show_entries",
                (
                    "format=duration,size,bit_rate:"
                    "stream=index,codec_name,width,height,pix_fmt,"
                    "avg_frame_rate,sample_rate,channels,duration"
                ),
                "-of",
                "json",
                str(video_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    narration = json.loads(narration_validation_path.read_text(encoding="utf-8"))
    mux_receipt = json.loads(mux_receipt_path.read_text(encoding="utf-8"))
    video_streams = [item for item in probe["streams"] if item["codec_name"] == "h264"]
    audio_streams = [item for item in probe["streams"] if item["codec_name"] == "aac"]
    duration = float(probe["format"]["duration"])
    video_duration = float(video_streams[0]["duration"]) if video_streams else 0
    audio_duration = float(audio_streams[0]["duration"]) if audio_streams else 0
    caption_pairs = [
        (seconds(start), seconds(end))
        for start, end in re.findall(
            r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+"
            r"(\d{2}:\d{2}:\d{2}\.\d{3})",
            captions_path.read_text(encoding="utf-8"),
        )
    ]
    captions_ordered = all(
        start < end and (index == 0 or start >= caption_pairs[index - 1][1])
        for index, (start, end) in enumerate(caption_pairs)
    )
    last_caption_end = caption_pairs[-1][1] if caption_pairs else 0
    checks = {
        "video_inside_ignored_build_boundary": args.video.startswith(
            "build/visual_edition/"
        ),
        "duration_within_contract": 180 <= duration <= 360,
        "one_h264_video_stream": len(video_streams) == 1,
        "one_aac_audio_stream": len(audio_streams) == 1,
        "video_1920x1080": bool(
            video_streams
            and video_streams[0].get("width") == 1920
            and video_streams[0].get("height") == 1080
        ),
        "video_yuv420p": bool(
            video_streams and video_streams[0].get("pix_fmt") == "yuv420p"
        ),
        "video_30_fps": bool(
            video_streams and video_streams[0].get("avg_frame_rate") == "30/1"
        ),
        "audio_48khz_mono": bool(
            audio_streams
            and audio_streams[0].get("sample_rate") == "48000"
            and audio_streams[0].get("channels") == 1
        ),
        "audio_spans_container_to_one_frame": (
            abs(audio_duration - duration) <= 1 / 30
        ),
        "video_spans_container_to_one_frame": 0 <= duration - video_duration <= 0.04,
        "captions_present_and_ordered": bool(caption_pairs) and captions_ordered,
        "captions_span_master": 0 <= duration - last_caption_end <= 1,
        "narration_validation_passed": narration.get("validation_state") == "pass",
        "narration_duration_matches_master": abs(
            float(narration.get("duration_seconds", 0)) - duration
        )
        <= 1 / 30,
        "mux_receipt_binds_final_video": (
            mux_receipt.get("output_path") == args.video
            and mux_receipt.get("output_sha256") == sha256(video_path)
        ),
        "mux_receipt_binds_narration": (
            mux_receipt.get("audio_sha256") == narration.get("audio_sha256")
        ),
        "seven_scene_timing_bound": (
            len(mux_receipt.get("audio_scene_endpoints_seconds", [])) == 7
            and len(mux_receipt.get("aligned_scene_endpoints_seconds", [])) == 7
            and float(
                mux_receipt.get("maximum_scene_endpoint_error_seconds", 999)
            )
            <= 1 / 30
        ),
    }
    report = {
        "schema_version": "asi_stack.local_visual_master_validation.v1",
        "validation_state": "pass" if all(checks.values()) else "fail",
        "validator_sha256": sha256(Path(__file__)),
        "video_path": args.video,
        "video_sha256": sha256(video_path),
        "caption_path": args.captions,
        "caption_sha256": sha256(captions_path),
        "narration_validation_sha256": sha256(narration_validation_path),
        "mux_receipt_path": args.mux_receipt,
        "mux_receipt_sha256": sha256(mux_receipt_path),
        "narration_audio_sha256": narration.get("audio_sha256"),
        "duration_seconds": duration,
        "video_duration_seconds": video_duration,
        "audio_duration_seconds": audio_duration,
        "last_caption_end_seconds": last_caption_end,
        "format_size_bytes": int(probe["format"]["size"]),
        "format_bit_rate": int(probe["format"]["bit_rate"]),
        "checks": checks,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["validation_state"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
