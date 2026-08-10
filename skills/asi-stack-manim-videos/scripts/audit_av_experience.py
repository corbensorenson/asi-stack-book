#!/usr/bin/env python3
"""Report mechanical audiovisual risks in a rendered chapter video.

The report deliberately does not issue an aesthetic verdict. It detects
conditions that deserve playback review: freezes, black intervals, silence,
loudness outliers, true-peak overs, missing streams, and plan-duration drift.
Final-master mode writes the schema-governed diagnostic. Animatic-preflight
mode is canonical-path constrained, stdout-only, and cannot pass a review gate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


AUDITOR_PATH = "skills/asi-stack-manim-videos/scripts/audit_av_experience.py"
SCHEMA_PATH = "schemas/manim_av_diagnostics.schema.json"
DETECTION_CONTRACT = {
    "freeze_filter": "freezedetect=n=-50dB:d=6",
    "black_filter": "blackdetect=d=1:pix_th=0.10",
    "silence_filter": "silencedetect=n=-45dB:d=3",
    "loudness_filter": "ebur128=peak=true",
    "target_integrated_lufs": -16.0,
    "lufs_tolerance": 1.5,
    "true_peak_ceiling_dbtp": -1.0,
    "maximum_plan_duration_drift_seconds": 0.25,
    "declared_interval_boundary_tolerance_seconds": 0.15,
}
NEGATIVE_CONTROL_COUNT = 3


def discover_repository_root() -> Path:
    configured = os.environ.get("ASI_STACK_BOOK_ROOT")
    candidates = [] if not configured else [Path(configured)]
    candidates.extend((Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents))
    for candidate in candidates:
        if (candidate / "book_structure.json").is_file() and (candidate / AUDITOR_PATH).is_file():
            return candidate.resolve()
    raise RuntimeError("ASI Stack repository root is unavailable")


ROOT = discover_repository_root()
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
FINAL_ROOT = (ROOT / "build/visual_edition/generation-2/final").resolve()
ANIMATIC_ROOT = (ROOT / "build/visual_edition/isolated-renders").resolve()


def run(command: list[str]) -> str:
    try:
        process = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=300
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command exceeded 300 seconds: {' '.join(command)}") from exc
    if process.returncode:
        detail = (process.stderr or process.stdout).strip()
        raise RuntimeError(f"command failed ({process.returncode}): {' '.join(command)}\n{detail}")
    return (process.stderr or "") + (process.stdout or "")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def media_tool_identities() -> dict[str, dict[str, str]]:
    value = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    identities = value.get("media_tools", {})
    for name in ("ffmpeg", "ffprobe"):
        binding = identities.get(name, {})
        path = Path(binding.get("path", ""))
        if not path.is_file() or digest(path) != binding.get("sha256"):
            raise RuntimeError(f"pinned {name} executable identity drift")
        version = run([str(path), "-version"]).splitlines()[0]
        if not version.startswith(f"{name} version {binding.get('version')} "):
            raise RuntimeError(f"pinned {name} executable version drift")
    return identities


def ffprobe(path: Path, media_tools: dict[str, dict[str, str]]) -> dict:
    output = run(
        [
            media_tools["ffprobe"]["path"],
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


def detect(
    path: Path,
    filter_expression: str,
    media_tools: dict[str, dict[str, str]],
) -> str:
    return run([media_tools["ffmpeg"]["path"], "-hide_banner", "-nostats", "-i", str(path), "-af" if filter_expression.startswith("silence") or filter_expression.startswith("ebur") else "-vf", filter_expression, "-f", "null", "-"])


def load_plan(path: Path | None) -> dict | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    duration = value.get("target_duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool):
        raise ValueError("beat plan has no numeric target_duration_seconds")
    return value


def classify_declared_intervals(
    intervals: list[dict],
    beats: list[dict],
    *,
    kind: str,
    boundary_tolerance_seconds: float = DETECTION_CONTRACT[
        "declared_interval_boundary_tolerance_seconds"
    ],
) -> tuple[list[dict], list[dict]]:
    if kind not in {"freeze", "silence"}:
        raise ValueError("interval kind must be freeze or silence")
    declared: list[dict] = []
    undeclared: list[dict] = []
    for interval in intervals:
        owner = None
        for beat in beats:
            start = beat.get("start_seconds")
            end = beat.get("end_seconds")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                continue
            contained = (
                interval["start"] >= float(start) - boundary_tolerance_seconds
                and interval["end"] <= float(end) + boundary_tolerance_seconds
            )
            if not contained:
                continue
            if kind == "freeze" and beat.get("mode") == "hold" and beat.get("hold_purpose"):
                owner = beat.get("id")
                break
            pause = beat.get("reasoning_pause_seconds")
            if (
                kind == "silence"
                and isinstance(pause, (int, float))
                and not isinstance(pause, bool)
                and float(pause) + boundary_tolerance_seconds >= float(interval["duration"])
            ):
                owner = beat.get("id")
                break
        if owner is None:
            undeclared.append(interval)
        else:
            declared.append({**interval, "declared_by_beat_id": owner})
    return declared, undeclared


def negative_control_failures() -> list[str]:
    schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
    baseline = {
        "schema_version": "asi_stack.av_experience_diagnostics.v1",
        "generated_at_utc": "2026-08-09T00:00:00Z",
        "validation_state": "pass",
        "auditor": {"path": AUDITOR_PATH, "sha256": "a" * 64},
        "media_tools": {
            "ffmpeg": {"path": "/opt/ffmpeg", "version": "8.0.1", "sha256": "b" * 64},
            "ffprobe": {"path": "/opt/ffprobe", "version": "8.0.1", "sha256": "c" * 64},
        },
        "video": "build/visual_edition/generation-2/final/fixture.mp4",
        "video_sha256": "d" * 64,
        "beat_plan": "visual_edition/chapters/fixture/generation-2/beat_plan.json",
        "beat_plan_sha256": "e" * 64,
        "detection_contract": dict(DETECTION_CONTRACT),
        "duration_seconds": 120.0,
        "plan_duration_seconds": 120.0,
        "video_stream_count": 1,
        "audio_stream_count": 1,
        "freezes": [],
        "declared_freezes": [],
        "undeclared_freezes": [],
        "black_intervals": [],
        "silences": [],
        "declared_silences": [],
        "undeclared_silences": [],
        "loudness": {
            "integrated_lufs": -16.0,
            "loudness_range_lu": 4.0,
            "true_peak_dbtp": -1.5,
        },
        "warnings": [],
        "errors": [],
        "interpretation": "Mechanical diagnostics only; complete playback and experience scoring remain required.",
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "This deterministic fixture tests diagnostics custody only and proves no "
            "teaching quality, chapter truth, or publication authority."
        ),
    }
    controls = (
        (
            "weakened freeze threshold",
            lambda row: row["detection_contract"].__setitem__(
                "freeze_filter", "freezedetect=n=-50dB:d=12"
            ),
        ),
        (
            "missing loudness evidence",
            lambda row: row["loudness"].pop("integrated_lufs"),
        ),
        (
            "warning laundered as pass",
            lambda row: row["warnings"].append("A material warning remains unresolved."),
        ),
    )
    failures: list[str] = []
    if list(Draft202012Validator(schema).iter_errors(baseline)):
        return ["valid A/V diagnostic fixture failed schema validation"]
    for label, mutate in controls:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        if not list(Draft202012Validator(schema).iter_errors(candidate)):
            failures.append(f"A/V diagnostic negative control did not trigger: {label}")
    return failures


def self_test() -> None:
    media_tool_identities()
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
    beats = [
        {
            "id": "b01", "mode": "hold", "hold_purpose": "Let the viewer predict.",
            "start_seconds": 4.1, "end_seconds": 10.6,
        },
        {
            "id": "b02", "mode": "change", "reasoning_pause_seconds": 4.0,
            "start_seconds": 12.0, "end_seconds": 16.0,
        },
    ]
    declared_freezes, undeclared_freezes = classify_declared_intervals(
        freezes, beats, kind="freeze"
    )
    declared_silences, undeclared_silences = classify_declared_intervals(
        silences, beats, kind="silence"
    )
    if (
        [row.get("declared_by_beat_id") for row in declared_freezes] != ["b01"]
        or [row.get("declared_by_beat_id") for row in declared_silences] != ["b02"]
        or undeclared_freezes
        or undeclared_silences
    ):
        raise AssertionError("declared interval classification failed")
    if classify_declared_intervals(freezes, [], kind="freeze") != ([], freezes):
        raise AssertionError("undeclared freeze was not retained")
    loudness = parse_loudness("I: -15.8 LUFS\nLRA: 5.1 LU\nPeak: -1.2 dBFS")
    if loudness != {"integrated_lufs": -15.8, "loudness_range_lu": 5.1, "true_peak_dbtp": -1.2}:
        raise AssertionError(f"unexpected loudness parse: {loudness}")
    schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    failures = negative_control_failures()
    if failures:
        raise AssertionError("; ".join(failures))
    preflight = as_animatic_preflight(
        {
            "schema_version": "asi_stack.av_experience_diagnostics.v1",
            "validation_state": "pass",
            "interpretation": "Mechanical diagnostics only.",
        }
    )
    if (
        "validation_state" in preflight
        or preflight.get("mechanical_result") != "pass"
        or preflight.get("review_gate_effect") != "none"
    ):
        raise AssertionError("animatic preflight authority boundary failed")
    print("Self-test passed.")


def audit(path: Path, plan: Path | None, target_lufs: float | None, tolerance: float) -> tuple[dict, list[str], list[str]]:
    media_tools = media_tool_identities()
    metadata = ffprobe(path, media_tools)
    streams = metadata.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    errors: list[str] = []
    warnings: list[str] = []
    if len(video_streams) != 1:
        errors.append(
            f"exactly one video stream is required; found {len(video_streams)}"
        )
    if len(audio_streams) != 1:
        errors.append(
            f"exactly one audio stream is required; found {len(audio_streams)}"
        )
    duration = float(metadata.get("format", {}).get("duration") or 0)
    if duration <= 0:
        errors.append("container duration is missing or non-positive")

    plan_value = load_plan(plan)
    plan_duration = (
        float(plan_value["target_duration_seconds"])
        if plan_value is not None else None
    )
    if (
        plan_duration is not None
        and abs(duration - plan_duration)
        > DETECTION_CONTRACT["maximum_plan_duration_drift_seconds"]
    ):
        errors.append(f"media duration {duration:.3f}s differs from beat plan {plan_duration:.3f}s")

    freezes: list[dict] = []
    black_intervals: list[dict] = []
    silences: list[dict] = []
    loudness = {"integrated_lufs": None, "loudness_range_lu": None, "true_peak_dbtp": None}
    if video_streams:
        freezes = parse_interval_events(
            detect(path, DETECTION_CONTRACT["freeze_filter"], media_tools),
            "freeze",
        )
        black_intervals = parse_interval_events(
            detect(path, DETECTION_CONTRACT["black_filter"], media_tools),
            "black",
        )
    if audio_streams:
        silences = parse_interval_events(
            detect(path, DETECTION_CONTRACT["silence_filter"], media_tools),
            "silence",
        )
        loudness = parse_loudness(
            detect(path, DETECTION_CONTRACT["loudness_filter"], media_tools)
        )

    beats = plan_value.get("beats", []) if isinstance(plan_value, dict) else []
    declared_freezes, undeclared_freezes = classify_declared_intervals(
        freezes, beats, kind="freeze"
    )
    declared_silences, undeclared_silences = classify_declared_intervals(
        silences, beats, kind="silence"
    )
    if undeclared_freezes:
        warnings.append(
            f"{len(undeclared_freezes)} undeclared freeze interval(s) at least 6s "
            "require pedagogical review"
        )
    if black_intervals:
        warnings.append(f"{len(black_intervals)} black interval(s) at least 1s require transition review")
    if undeclared_silences:
        warnings.append(
            f"{len(undeclared_silences)} undeclared silence interval(s) at least 3s "
            "require pacing review"
        )
    peak = loudness.get("true_peak_dbtp")
    if not isinstance(peak, (int, float)):
        errors.append("true peak could not be measured")
    elif peak > DETECTION_CONTRACT["true_peak_ceiling_dbtp"]:
        errors.append(
            f"true peak {peak:.1f} dBTP exceeds the "
            f"{DETECTION_CONTRACT['true_peak_ceiling_dbtp']:.1f} dBTP ceiling"
        )
    integrated = loudness.get("integrated_lufs")
    if not isinstance(integrated, (int, float)):
        errors.append("integrated loudness could not be measured")
    elif target_lufs is not None:
        if abs(integrated - target_lufs) > tolerance:
            warnings.append(
                f"integrated loudness {integrated:.1f} LUFS differs from target {target_lufs:.1f} by more than {tolerance:.1f} LU"
            )

    report = {
        "schema_version": "asi_stack.av_experience_diagnostics.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "validation_state": "fail" if errors else "needs_review" if warnings else "pass",
        "auditor": {"path": AUDITOR_PATH, "sha256": digest(Path(__file__))},
        "media_tools": media_tools,
        "video": path.resolve().relative_to(ROOT).as_posix(),
        "video_sha256": digest(path),
        "beat_plan": plan.resolve().relative_to(ROOT).as_posix() if plan else None,
        "beat_plan_sha256": digest(plan) if plan else None,
        "detection_contract": {
            **DETECTION_CONTRACT,
            "target_integrated_lufs": target_lufs,
            "lufs_tolerance": tolerance,
        },
        "duration_seconds": round(duration, 3),
        "plan_duration_seconds": plan_duration,
        "video_stream_count": len(video_streams),
        "audio_stream_count": len(audio_streams),
        "freezes": freezes,
        "declared_freezes": declared_freezes,
        "undeclared_freezes": undeclared_freezes,
        "black_intervals": black_intervals,
        "silences": silences,
        "declared_silences": declared_silences,
        "undeclared_silences": undeclared_silences,
        "loudness": loudness,
        "warnings": warnings,
        "errors": errors,
        "interpretation": "Mechanical diagnostics only; complete playback and experience scoring remain required.",
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "This deterministic diagnostic identifies mechanical review risks; it does not "
            "establish teaching quality, human learning, chapter truth, or publication authority."
        ),
    }
    return report, warnings, errors


def as_animatic_preflight(report: dict) -> dict:
    """Relabel a mechanical result so it cannot resemble a review verdict."""
    value = copy.deepcopy(report)
    value["schema_version"] = "asi_stack.av_experience_preflight.v1"
    value["mechanical_result"] = value.pop("validation_state")
    value["diagnostic_scope"] = "ephemeral_animatic_preflight"
    value["review_gate_effect"] = "none"
    value["interpretation"] = (
        "Ephemeral mechanical animatic preflight only; this is not the governed final "
        "A/V diagnostic and cannot pass an experience-review gate."
    )
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path, nargs="?")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--target-lufs", type=float)
    parser.add_argument("--lufs-tolerance", type=float, default=1.5)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument(
        "--animatic-preflight",
        action="store_true",
        help="inspect the canonical ignored-build animatic without creating a governed A/V artifact",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.video is None:
        parser.error("video is required unless --self-test is used")
    if args.plan is None or args.target_lufs is None or (
        args.json_out is None and not args.animatic_preflight
    ):
        parser.error(
            "--plan and --target-lufs are required; governed final diagnostics also require --json-out"
        )
    if args.animatic_preflight and args.json_out is not None:
        parser.error("--animatic-preflight is ephemeral and must not write --json-out")
    video = args.video.resolve()
    plan = args.plan.resolve()
    output = args.json_out.resolve() if args.json_out is not None else None
    if not video.is_file():
        raise SystemExit(f"video does not exist: {args.video}")
    if args.animatic_preflight:
        chapter_id = video.stem.removesuffix("-animatic")
        expected_video = (
            ANIMATIC_ROOT / chapter_id / "draft" / f"{chapter_id}-animatic.mp4"
        ).resolve()
        if video != expected_video:
            raise SystemExit("video must be the canonical isolated draft animatic")
    else:
        try:
            video.relative_to(FINAL_ROOT)
        except ValueError as exc:
            raise SystemExit(
                "video must be a canonical generation-two final master"
            ) from exc
        chapter_id = video.stem
    expected_plan = (
        ROOT / f"visual_edition/chapters/{chapter_id}/generation-2/beat_plan.json"
    ).resolve()
    expected_output = expected_plan.with_name("av_diagnostics.json")
    if plan != expected_plan or (
        not args.animatic_preflight and output != expected_output
    ):
        raise SystemExit(
            "A/V plan or report path does not match the master chapter identity"
        )
    narration_toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    governed_target = narration_toolchain["synthesis"]["integrated_lufs_target"]
    if (
        args.target_lufs != governed_target
        or args.target_lufs != DETECTION_CONTRACT["target_integrated_lufs"]
    ):
        raise SystemExit(
            "A/V loudness target differs from the pinned narration toolchain"
        )
    if args.lufs_tolerance != DETECTION_CONTRACT["lufs_tolerance"]:
        raise SystemExit(
            "A/V loudness tolerance differs from the governed diagnostic contract"
        )
    try:
        report, warnings, errors = audit(
            video, plan, args.target_lufs, args.lufs_tolerance
        )
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        raise SystemExit(f"Unable to audit video: {exc}") from exc
    if args.animatic_preflight:
        report = as_animatic_preflight(report)
    else:
        schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
        schema_errors = sorted(
            Draft202012Validator(schema).iter_errors(report),
            key=lambda error: tuple(map(str, error.path)),
        )
        if schema_errors:
            detail = "; ".join(
                f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in schema_errors
            )
            raise SystemExit(f"A/V diagnostics failed schema validation: {detail}")
    rendered = json.dumps(report, indent=2)
    print(rendered)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output_temp = output.with_suffix(".tmp.json")
        output_temp.write_text(rendered + "\n", encoding="utf-8")
        output_temp.replace(output)
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
