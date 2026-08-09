#!/usr/bin/env python3
"""Audit VTT cue structure and build a risk-prioritized simulated-overlay sheet.

The generated overlay is a layout diagnostic. It cannot prove behavior in a
specific player or prove that captions avoid the active teaching region.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


TIMESTAMP = re.compile(
    r"(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2})\.(?P<sms>\d{3})\s+-->\s+"
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2})\.(?P<ems>\d{3})(?:\s+.*)?"
)
TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"\b[\w'-]+\b")
AUDITOR_PATH = "skills/asi-stack-manim-videos/scripts/build_caption_review_sheet.py"
GOVERNED_THRESHOLDS = {
    "max_lines": 2,
    "max_line_characters": 42,
    "max_words_per_minute": 180.0,
    "minimum_duration_seconds": 0.32,
    "minimum_risk_samples": 12,
}


def discover_repository_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents):
        if (candidate / "book_structure.json").is_file() and (
            candidate / AUDITOR_PATH
        ).is_file():
            return candidate.resolve()
    raise RuntimeError("ASI Stack repository root is unavailable")


ROOT = discover_repository_root()
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned_ffmpeg() -> dict[str, str]:
    value = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    binding = value.get("media_tools", {}).get("ffmpeg", {})
    path = Path(binding.get("path", ""))
    if not path.is_file() or digest(path) != binding.get("sha256"):
        raise RuntimeError("pinned FFmpeg executable identity drift")
    try:
        version = subprocess.check_output(
            [str(path), "-version"],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=30,
        ).splitlines()[0]
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("pinned FFmpeg executable version probe failed") from exc
    if not version.startswith(f"ffmpeg version {binding.get('version')} "):
        raise RuntimeError("pinned FFmpeg executable version drift")
    return binding


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    lines: tuple[str, ...]

    @property
    def text(self) -> str:
        return " ".join(self.lines)

    @property
    def duration(self) -> float:
        return self.end - self.start

    @property
    def word_count(self) -> int:
        return len(WORD.findall(self.text))

    @property
    def words_per_minute(self) -> float:
        return self.word_count / self.duration * 60 if self.duration > 0 else float("inf")


def seconds(groups: dict[str, str], prefix: str) -> float:
    return (
        int(groups[f"{prefix}h"]) * 3600
        + int(groups[f"{prefix}m"]) * 60
        + int(groups[f"{prefix}s"])
        + int(groups[f"{prefix}ms"]) / 1000
    )


def visible_text(value: str) -> str:
    return " ".join(html.unescape(TAG.sub("", value)).split())


def parse_vtt_text(value: str) -> list[Cue]:
    blocks = re.split(r"\n\s*\n", value.replace("\r\n", "\n").strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = block.splitlines()
        timing_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        match = TIMESTAMP.fullmatch(lines[timing_index].strip())
        if not match:
            raise ValueError(f"unsupported VTT timestamp: {lines[timing_index]}")
        caption_lines = tuple(
            text for text in (visible_text(line) for line in lines[timing_index + 1 :]) if text
        )
        if caption_lines:
            cues.append(Cue(seconds(match.groupdict(), "s"), seconds(match.groupdict(), "e"), caption_lines))
    if not cues:
        raise ValueError("no caption cues found")
    return cues


def parse_vtt(path: Path) -> list[Cue]:
    return parse_vtt_text(path.read_text(encoding="utf-8"))


def audit_cues(
    cues: list[Cue],
    *,
    max_lines: int,
    max_line_chars: int,
    max_wpm: float,
    min_duration: float,
) -> tuple[list[str], list[str], list[dict]]:
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict] = []
    for index, cue in enumerate(cues):
        number = index + 1
        if cue.duration <= 0:
            errors.append(f"cue {number}: non-positive duration")
        if index and cue.start < cues[index - 1].end - 1e-6:
            errors.append(f"cue {number}: overlaps cue {index}")
        if len(cue.lines) > max_lines:
            errors.append(f"cue {number}: {len(cue.lines)} lines exceeds project limit {max_lines}")
        for line_number, line in enumerate(cue.lines, start=1):
            if len(line) > max_line_chars:
                errors.append(
                    f"cue {number} line {line_number}: {len(line)} characters exceeds project limit {max_line_chars}"
                )
        if cue.duration < min_duration:
            errors.append(f"cue {number}: {cue.duration:.3f}s is below project minimum {min_duration:.3f}s")
        if cue.words_per_minute > max_wpm:
            errors.append(
                f"cue {number}: {cue.words_per_minute:.1f} WPM exceeds project review threshold {max_wpm:.1f}"
            )
        if cue.duration > 7:
            warnings.append(f"cue {number}: {cue.duration:.2f}s is long; verify phrase boundaries and sync")
        rows.append({
            "cue": number,
            "start_seconds": round(cue.start, 3),
            "end_seconds": round(cue.end, 3),
            "duration_seconds": round(cue.duration, 3),
            "line_count": len(cue.lines),
            "line_lengths": [len(line) for line in cue.lines],
            "word_count": cue.word_count,
            "words_per_minute": round(cue.words_per_minute, 2),
            "text": cue.text,
        })
    return errors, warnings, rows


def risk_sample_indices(cues: list[Cue], requested: int) -> tuple[list[int], dict[int, list[str]]]:
    reasons: dict[int, list[str]] = {}

    def select(index: int, reason: str) -> None:
        reasons.setdefault(index, []).append(reason)

    select(0, "first cue")
    select(len(cues) - 1, "last cue")
    select(max(range(len(cues)), key=lambda i: len(cues[i].text)), "most characters")
    select(max(range(len(cues)), key=lambda i: cues[i].words_per_minute), "highest reading rate")
    select(min(range(len(cues)), key=lambda i: cues[i].duration), "shortest duration")
    select(max(range(len(cues)), key=lambda i: len(cues[i].lines)), "most authored lines")
    target = min(requested, len(cues))
    if target > 1:
        for slot in range(target):
            select(round(slot * (len(cues) - 1) / (target - 1)), "distributed coverage")
    if len(reasons) > target:
        risk_order = sorted(
            reasons,
            key=lambda i: (
                i not in {0, len(cues) - 1},
                -cues[i].words_per_minute,
                -len(cues[i].text),
            ),
        )
        keep = set(risk_order[:target])
        reasons = {index: value for index, value in reasons.items() if index in keep}
    return sorted(reasons), reasons


def video_frame(
    video: Path, at_seconds: float, ffmpeg: dict[str, str]
) -> Image.Image:
    command = [
        ffmpeg["path"], "-v", "error", "-ss", f"{at_seconds:.3f}", "-i", str(video),
        "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-",
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, check=False, timeout=30
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("caption frame extraction exceeded 30 seconds") from exc
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace")[-1000:]
        raise RuntimeError(f"caption frame extraction failed: {detail}")
    return Image.open(io.BytesIO(completed.stdout)).convert("RGB")


def font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def captioned_tile(
    video: Path,
    cue: Cue,
    cue_number: int,
    reasons: list[str],
    ffmpeg: dict[str, str],
) -> Image.Image:
    tile = video_frame(video, (cue.start + cue.end) / 2, ffmpeg).resize(
        (640, 360), Image.Resampling.LANCZOS
    )
    draw = ImageDraw.Draw(tile, "RGBA")
    caption_font = font(21)
    metadata_font = font(14)
    line_height = 27
    caption_height = len(cue.lines) * line_height + 24
    y0 = 360 - caption_height - 22
    draw.rounded_rectangle((24, y0, 616, 338), radius=8, fill=(8, 14, 19, 220), outline=(88, 183, 211, 220), width=2)
    y = y0 + 11
    for line in cue.lines:
        box = draw.textbbox((0, 0), line, font=caption_font)
        draw.text(((640 - (box[2] - box[0])) / 2, y), line, font=caption_font, fill=(245, 248, 250, 255))
        y += line_height
    stamp = f"cue {cue_number:02d} | {cue.start:06.2f}-{cue.end:06.2f}s | {cue.words_per_minute:.0f} WPM"
    reason = ", ".join(reasons)
    draw.rectangle((0, 0, 640, 48), fill=(8, 14, 19, 225))
    draw.text((12, 6), stamp, font=metadata_font, fill=(245, 248, 250, 255))
    draw.text((12, 26), f"SIMULATED OVERLAY: {reason}", font=metadata_font, fill=(242, 193, 78, 255))
    return tile


def self_test() -> None:
    value = """WEBVTT

00:00:00.000 --> 00:00:02.000
One short line

00:00:02.100 --> 00:00:05.100 align:middle
Two authored lines
remain separate

00:00:05.200 --> 00:00:08.200
The final cue completes the thought
"""
    cues = parse_vtt_text(value)
    if len(cues) != 3 or cues[1].lines != ("Two authored lines", "remain separate"):
        raise AssertionError(f"line preservation failed: {cues}")
    errors, _, rows = audit_cues(cues, max_lines=2, max_line_chars=42, max_wpm=180, min_duration=0.32)
    if errors or rows[1]["line_count"] != 2:
        raise AssertionError(f"valid fixture failed: {errors}, {rows}")
    broken = list(cues) + [Cue(8.1, 8.2, ("This line is intentionally much longer than forty two characters",))]
    errors, _, _ = audit_cues(broken, max_lines=2, max_line_chars=42, max_wpm=180, min_duration=0.32)
    for fragment in ("overlaps", "characters exceeds", "below project minimum", "WPM exceeds"):
        if not any(fragment in error for error in errors):
            raise AssertionError(f"negative fixture missed {fragment!r}: {errors}")
    indices, reasons = risk_sample_indices(cues, 3)
    if 0 not in indices or len(indices) != 3 or not reasons:
        raise AssertionError(f"risk sampling failed: {indices}, {reasons}")
    print("Self-test passed.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path, nargs="?")
    parser.add_argument("captions", type=Path, nargs="?")
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--max-lines", type=int, default=2)
    parser.add_argument("--max-line-chars", type=int, default=42)
    parser.add_argument("--max-wpm", type=float, default=180.0)
    parser.add_argument("--min-duration", type=float, default=0.32)
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.video is None or args.captions is None or args.output is None:
        parser.error("video, captions, and output are required unless --self-test is used")
    if Path(__file__).resolve() != (ROOT / AUDITOR_PATH).resolve():
        raise SystemExit(
            "governed caption diagnostics must use the repository-tracked auditor"
        )
    if (
        args.samples < GOVERNED_THRESHOLDS["minimum_risk_samples"]
        or args.max_lines > GOVERNED_THRESHOLDS["max_lines"]
        or args.max_line_chars > GOVERNED_THRESHOLDS["max_line_characters"]
        or args.max_wpm > GOVERNED_THRESHOLDS["max_words_per_minute"]
        or args.min_duration < GOVERNED_THRESHOLDS["minimum_duration_seconds"]
    ):
        raise SystemExit("caption diagnostic settings weaken the governed thresholds")
    if args.report_json is None:
        raise SystemExit("--report-json is required for governed caption diagnostics")

    video = args.video.resolve()
    captions = args.captions.resolve()
    output = args.output.resolve()
    report_path = args.report_json.resolve()
    chapter_id = video.stem
    expected_video = (
        ROOT / f"build/visual_edition/generation-2/final/{chapter_id}.mp4"
    ).resolve()
    generation = (
        ROOT / f"visual_edition/chapters/{chapter_id}/generation-2"
    ).resolve()
    expected_captions = generation / "captions.vtt"
    expected_output = generation / "receipts/caption-overlay.png"
    expected_report = generation / "receipts/caption-diagnostics.json"
    if (
        video != expected_video
        or captions != expected_captions
        or output != expected_output
        or report_path != expected_report
    ):
        raise SystemExit("caption diagnostic paths do not match one canonical final chapter")
    if not video.is_file() or not captions.is_file():
        raise SystemExit("canonical final video or captions are missing")
    ffmpeg = pinned_ffmpeg()

    cues = parse_vtt(captions)
    errors, warnings, rows = audit_cues(
        cues,
        max_lines=args.max_lines,
        max_line_chars=args.max_line_chars,
        max_wpm=args.max_wpm,
        min_duration=args.min_duration,
    )
    report = {
        "schema_version": "asi_stack.caption_review_diagnostics.v2",
        "auditor": {"path": AUDITOR_PATH, "sha256": digest(Path(__file__))},
        "media_tools": {"ffmpeg": ffmpeg},
        "video": video.relative_to(ROOT).as_posix(),
        "video_sha256": digest(video),
        "captions": captions.relative_to(ROOT).as_posix(),
        "captions_sha256": digest(captions),
        "validation_state": "fail" if errors else "needs_review" if warnings else "pass",
        "simulated_overlay": None,
        "project_thresholds": {
            "max_lines": args.max_lines,
            "max_line_characters": args.max_line_chars,
            "max_words_per_minute": args.max_wpm,
            "minimum_duration_seconds": args.min_duration,
        },
        "cues": rows,
        "errors": errors,
        "warnings": warnings,
        "required_manual_checks": [
            "Play the exact final captions in the target player at normal speed.",
            "Verify line breaks, synchronization, reading comfort, phone legibility, and speaker changes.",
            "Verify captions do not obscure the active mechanism; the simulated sheet cannot establish this.",
        ],
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "This simulated overlay diagnoses caption risks only; it does not prove "
            "player behavior, accessibility, human learning, or chapter truth."
        ),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if errors:
        report_pending = report_path.with_suffix(".tmp.json")
        report_pending.write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        report_pending.replace(report_path)
        raise SystemExit("Caption audit failed:\n - " + "\n - ".join(errors))

    indices, reasons = risk_sample_indices(cues, min(args.samples, len(cues)))
    tiles = [
        captioned_tile(video, cues[index], index + 1, reasons[index], ffmpeg)
        for index in indices
    ]
    columns = 3
    rows_count = math.ceil(len(tiles) / columns)
    sheet = Image.new("RGB", (columns * 640, rows_count * 360), "#101820")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * 640, (index // columns) * 360))
    output.parent.mkdir(parents=True, exist_ok=True)
    output_pending = output.with_name(f".{output.stem}.pending.png")
    sheet.save(output_pending)
    output_pending.replace(output)
    report["simulated_overlay"] = {
        "path": output.relative_to(ROOT).as_posix(),
        "sha256": digest(output),
    }
    report_pending = report_path.with_suffix(".tmp.json")
    report_pending.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    report_pending.replace(report_path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    print(
        f"Caption structure audit passed for {len(cues)} cues; wrote {len(tiles)} risk-prioritized "
        f"simulated overlays to {output}. Actual-player review remains required."
    )


if __name__ == "__main__":
    main()
