#!/usr/bin/env python3
"""Extract interpolation-aware frames for every beat and build a review sheet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


SAMPLER_PATH = "skills/asi-stack-manim-videos/scripts/sample_video_beats.py"
SAMPLE_SETS = {"animatic", "final"}
NEGATIVE_CONTROL_COUNT = 3


def discover_repository_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents):
        if (candidate / "book_structure.json").is_file() and (
            candidate / SAMPLER_PATH
        ).is_file():
            return candidate.resolve()
    raise RuntimeError("ASI Stack repository root is unavailable")


ROOT = discover_repository_root()
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
SCHEMA = ROOT / "schemas/manim_frame_sample_manifest.schema.json"
SAMPLE_ROOT = ROOT / "build/visual_edition/review-samples"

def sample_times(start: float, end: float, count: int = 5) -> list[tuple[str, float]]:
    if count != 5:
        raise ValueError("governed review requires exactly five samples per beat")
    duration = end - start
    inset = min(0.15, max(0.01, duration * 0.05))
    fractions = (
        ("start", 0.0),
        ("quarter", 0.25),
        ("middle", 0.5),
        ("three-quarter", 0.75),
        ("end", 1.0),
    )
    low = start + inset
    high = max(low, end - inset)
    return [(label, min(high, max(low, start + duration * fraction))) for label, fraction in fractions]


def review_style(samples: int) -> str:
    if samples != 5:
        raise ValueError("governed review requires exactly five samples per beat")
    return """
body{margin:0;background:#101820;color:#f4f6f7;font:16px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:32px}
section{background:#182630;border:1px solid #36505e;border-radius:16px;margin:24px 0;padding:20px}h1,h2{margin:.2em 0 .5em}p{color:#d9e1e5}
.frames{display:grid;grid-template-columns:repeat(__SAMPLES__,minmax(0,1fr));gap:14px}figure{margin:0}img{width:100%;border-radius:8px;background:#000}figcaption{color:#aebbc2;margin-top:6px}
@media(max-width:800px){.frames{grid-template-columns:1fr}main{padding:14px}}
""".replace("__SAMPLES__", str(samples))


def self_test() -> None:
    values = sample_times(10.0, 14.0)
    expected = [
        ("start", 10.15),
        ("quarter", 11.0),
        ("middle", 12.0),
        ("three-quarter", 13.0),
        ("end", 13.85),
    ]
    if any(label != want_label or abs(value - want_value) > 1e-6 for (label, value), (want_label, want_value) in zip(values, expected)):
        raise AssertionError(f"unexpected sample times: {values}")
    if parse_target("b03=12.75") != ("b03", 12.75):
        raise AssertionError("targeted sample parser failed")
    style = review_style(5)
    if "repeat(5," not in style or "width:100%" not in style or "__SAMPLES__" in style:
        raise AssertionError("review-sheet CSS construction failed")
    failures = schema_negative_control_failures()
    if failures:
        raise AssertionError("; ".join(failures))
    print("Self-test passed.")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_target(value: str) -> tuple[str, float]:
    try:
        beat_id, timestamp = value.split("=", 1)
        result = (beat_id.strip(), float(timestamp))
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("target must use BEAT_ID=SECONDS") from exc
    if not result[0] or result[1] < 0:
        raise argparse.ArgumentTypeError("target must use a beat id and non-negative time")
    return result


def schema_negative_control_failures() -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    positions = ("start", "quarter", "middle", "three-quarter", "end")
    baseline = {
        "schema_version": "asi_stack.manim_frame_sample_manifest.v1",
        "chapter_id": "fixture",
        "sample_set": "final",
        "sampler": {"path": SAMPLER_PATH, "sha256": "a" * 64},
        "media_tools": {
            "ffmpeg": {"path": "/opt/ffmpeg", "version": "8.0.1", "sha256": "b" * 64}
        },
        "video_path": "build/visual_edition/generation-2/final/fixture.mp4",
        "video_sha256": "c" * 64,
        "beat_plan_path": "visual_edition/chapters/fixture/generation-2/beat_plan.json",
        "beat_plan_sha256": "d" * 64,
        "expected_beat_count": 1,
        "sampled_beat_count": 1,
        "samples_per_beat": 5,
        "beats": [{
            "beat_id": "b01",
            "start_seconds": 0.0,
            "end_seconds": 5.0,
            "samples": [
                {
                    "position": position,
                    "timestamp_seconds": float(index),
                    "path": f"build/visual_edition/review-samples/fixture/final/b01-{position}.png",
                    "sha256": hashlib.sha256(position.encode()).hexdigest(),
                }
                for index, position in enumerate(positions)
            ],
        }],
        "targeted_transition_samples": [],
        "interpretation": "Frame samples diagnose composition and interpolation; full-speed motion and sound review remain required.",
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "This deterministic fixture tests frame-sample custody only and proves no "
            "motion quality, synchronization, learning, or chapter truth."
        ),
    }
    if list(Draft202012Validator(schema).iter_errors(baseline)):
        return ["valid frame-sample fixture failed schema validation"]
    controls = (
        ("reduced coverage", lambda row: row.__setitem__("samples_per_beat", 3)),
        ("sampler omission", lambda row: row.pop("sampler")),
        ("sample-set omission", lambda row: row.pop("sample_set")),
    )
    failures: list[str] = []
    for label, mutate in controls:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        if not list(Draft202012Validator(schema).iter_errors(candidate)):
            failures.append(f"frame-sample negative control did not trigger: {label}")
    return failures


def pinned_ffmpeg() -> dict[str, str]:
    toolchain = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    binding = toolchain.get("media_tools", {}).get("ffmpeg", {})
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


def sample_set_current(
    manifest_path: Path,
    index_path: Path,
    output_dir: Path,
    video: Path,
    plan_path: Path,
    sample_set: str,
    targeted: list[tuple[str, float]],
    ffmpeg: dict[str, str],
) -> bool:
    if not manifest_path.is_file() or not index_path.is_file():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if list(Draft202012Validator(schema).iter_errors(manifest)):
        return False
    expected = {
        "chapter_id": json.loads(plan_path.read_text(encoding="utf-8")).get(
            "chapter_id"
        ),
        "sample_set": sample_set,
        "sampler": {"path": SAMPLER_PATH, "sha256": digest(Path(__file__))},
        "media_tools": {"ffmpeg": ffmpeg},
        "video_path": video.relative_to(ROOT).as_posix(),
        "video_sha256": digest(video),
        "beat_plan_path": plan_path.relative_to(ROOT).as_posix(),
        "beat_plan_sha256": digest(plan_path),
        "samples_per_beat": 5,
    }
    if any(manifest.get(name) != value for name, value in expected.items()):
        return False
    actual_targets = [
        (row.get("beat_id"), row.get("timestamp_seconds"))
        for row in manifest.get("targeted_transition_samples", [])
        if isinstance(row, dict)
    ]
    expected_targets = [
        (beat_id, round(timestamp, 3)) for beat_id, timestamp in targeted
    ]
    if actual_targets != expected_targets:
        return False
    rows = [
        sample
        for beat in manifest.get("beats", [])
        if isinstance(beat, dict)
        for sample in beat.get("samples", [])
        if isinstance(sample, dict)
    ]
    rows.extend(
        row
        for row in manifest.get("targeted_transition_samples", [])
        if isinstance(row, dict)
    )
    for row in rows:
        relative = row.get("path")
        if not isinstance(relative, str):
            return False
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(output_dir.resolve())
        except ValueError:
            return False
        if not path.is_file() or digest(path) != row.get("sha256"):
            return False
    return bool(rows)


def extract(
    video: Path,
    time_seconds: float,
    output: Path,
    ffmpeg: dict[str, str],
) -> None:
    pending = output.with_name(f".{output.stem}.pending.png")
    pending.unlink(missing_ok=True)
    command = [
        ffmpeg["path"],
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{time_seconds:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-vf",
        "scale=640:-2:flags=lanczos",
        "-y",
        str(pending),
    ]
    try:
        process = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=30
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"ffmpeg frame extraction exceeded 30 seconds at {time_seconds:.3f}s"
        ) from exc
    if process.returncode:
        pending.unlink(missing_ok=True)
        raise RuntimeError(process.stderr.strip() or "ffmpeg frame extraction failed")
    pending.replace(output)


def build(
    video: Path,
    plan_path: Path,
    output_dir: Path,
    manifest_path: Path,
    sample_set: str,
    ffmpeg: dict[str, str],
    samples: int = 5,
    targeted: list[tuple[str, float]] | None = None,
) -> tuple[Path, Path, int]:
    if samples != 5:
        raise ValueError("governed review manifests require exactly five samples per beat")
    if sample_set not in SAMPLE_SETS:
        raise ValueError("sample set must be animatic or final")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    beats = plan.get("beats")
    if not isinstance(beats, list) or not beats:
        raise ValueError("beat plan has no beats")
    output_dir.mkdir(parents=True, exist_ok=True)
    cards: list[str] = []
    manifest_beats: list[dict] = []
    image_count = 0
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            raise ValueError(f"beat[{index}] is not an object")
        beat_id = str(beat.get("id") or f"beat-{index + 1:03d}")
        start = beat.get("start_seconds")
        end = beat.get("end_seconds")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            raise ValueError(f"{beat_id} has invalid timing")
        figures: list[str] = []
        sample_rows: list[dict] = []
        for position, timestamp in sample_times(float(start), float(end), samples):
            # PNG avoids FFmpeg 8's refusal to emit non-full-range JPEG frames
            # from the usual limited-range H.264 YouTube/Manim source. Review
            # sheets are diagnostic artifacts, so predictable extraction is
            # more valuable than JPEG's smaller files.
            filename = f"{index + 1:03d}_{beat_id}_{position}.png"
            extract(video, timestamp, output_dir / filename, ffmpeg)
            image_count += 1
            sample_rows.append({
                "position": position,
                "timestamp_seconds": round(timestamp, 3),
                "path": (output_dir / filename).relative_to(ROOT).as_posix(),
                "sha256": digest(output_dir / filename),
            })
            figures.append(
                f'<figure><img src="{html.escape(filename)}" alt="{html.escape(beat_id)} {position} frame">'
                f'<figcaption>{position} · {timestamp:.2f}s</figcaption></figure>'
            )
        narration = html.escape(str(beat.get("narration", "")))
        target = html.escape(str(beat.get("attention_target", "")))
        purpose = html.escape(str(beat.get("visual_purpose", "")))
        cards.append(
            f'<section><h2>{html.escape(beat_id)} · {html.escape(str(beat.get("story_function", "")))}</h2>'
            f'<p><strong>Attention:</strong> {target}</p><p><strong>Purpose:</strong> {purpose}</p>'
            f'<p><strong>Narration:</strong> {narration}</p><div class="frames">{"".join(figures)}</div></section>'
        )
        manifest_beats.append({
            "beat_id": beat_id,
            "start_seconds": float(start),
            "end_seconds": float(end),
            "samples": sample_rows,
        })
    targeted_rows: list[dict] = []
    known_beats = {
        str(beat.get("id")): beat for beat in beats
        if isinstance(beat, dict) and beat.get("id")
    }
    for target_index, (beat_id, timestamp) in enumerate(targeted or [], start=1):
        if beat_id not in known_beats:
            raise ValueError(f"targeted sample refers to unknown beat {beat_id!r}")
        beat = known_beats[beat_id]
        if not beat["start_seconds"] <= timestamp <= beat["end_seconds"]:
            raise ValueError(
                f"targeted sample {timestamp:.3f}s is outside {beat_id} "
                f"[{beat['start_seconds']:.3f}, {beat['end_seconds']:.3f}]"
            )
        filename = f"targeted_{target_index:03d}_{beat_id}_{timestamp:.3f}.png"
        extract(video, timestamp, output_dir / filename, ffmpeg)
        image_count += 1
        targeted_rows.append({
            "beat_id": beat_id,
            "timestamp_seconds": round(timestamp, 3),
            "path": (output_dir / filename).relative_to(ROOT).as_posix(),
            "sha256": digest(output_dir / filename),
        })
    style = review_style(samples)
    title = html.escape(str(plan.get("chapter_id", "chapter")))
    document = f"<!doctype html><meta charset='utf-8'><title>{title} beat review</title><style>{style}</style><main><h1>{title} · beat review</h1>{''.join(cards)}</main>"
    index_path = output_dir / "index.html"
    index_pending = output_dir / ".index.pending.html"
    index_pending.write_text(document, encoding="utf-8")
    index_pending.replace(index_path)
    manifest = {
        "schema_version": "asi_stack.manim_frame_sample_manifest.v1",
        "chapter_id": plan.get("chapter_id"),
        "sample_set": sample_set,
        "sampler": {"path": SAMPLER_PATH, "sha256": digest(Path(__file__))},
        "media_tools": {"ffmpeg": ffmpeg},
        "video_path": video.resolve().relative_to(ROOT).as_posix(),
        "video_sha256": digest(video),
        "beat_plan_path": plan_path.resolve().relative_to(ROOT).as_posix(),
        "beat_plan_sha256": digest(plan_path),
        "expected_beat_count": len(beats),
        "sampled_beat_count": len(manifest_beats),
        "samples_per_beat": samples,
        "beats": manifest_beats,
        "targeted_transition_samples": targeted_rows,
        "interpretation": "Frame samples diagnose composition and interpolation; full-speed motion and sound review remain required.",
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": (
            "These deterministic frame samples support visual review only; they do not "
            "establish motion quality, synchronization, human learning, or chapter truth."
        ),
    }
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    schema_errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest),
        key=lambda error: tuple(map(str, error.path)),
    )
    if schema_errors:
        detail = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in schema_errors
        )
        raise ValueError(f"frame sample manifest is schema-invalid: {detail}")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_pending = manifest_path.with_suffix(".tmp.json")
    manifest_pending.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    manifest_pending.replace(manifest_path)
    return index_path, manifest_path, image_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path, nargs="?")
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("--sample-set", choices=tuple(sorted(SAMPLE_SETS)))
    parser.add_argument("--samples", type=int, choices=(5,), default=5)
    parser.add_argument(
        "--target-time",
        action="append",
        type=parse_target,
        default=[],
        metavar="BEAT_ID=SECONDS",
        help="add a targeted interpolation sample around a risky transition",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.video is None or args.plan is None or args.sample_set is None:
        parser.error("video, plan, and --sample-set are required unless --self-test is used")
    if Path(__file__).resolve() != (ROOT / SAMPLER_PATH).resolve():
        raise SystemExit(
            "governed frame samples must use the repository-tracked sampler"
        )
    video = args.video.resolve()
    plan = args.plan.resolve()
    if not video.is_file() or not plan.is_file():
        raise SystemExit("video and beat plan must exist")
    try:
        plan.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit("beat plan must remain in the repository") from exc
    plan_value = json.loads(plan.read_text(encoding="utf-8"))
    chapter_id = plan_value.get("chapter_id")
    if not isinstance(chapter_id, str) or not chapter_id or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789-"
        for character in chapter_id
    ) or chapter_id.startswith("-") or chapter_id.endswith("-") or "--" in chapter_id:
        raise SystemExit("beat plan chapter_id is not a canonical lowercase slug")
    expected_plan = (
        ROOT / f"visual_edition/chapters/{chapter_id}/generation-2/beat_plan.json"
    ).resolve()
    if plan != expected_plan:
        raise SystemExit("beat plan does not use the canonical chapter path")
    sample_set = args.sample_set
    output_dir = (SAMPLE_ROOT / chapter_id / sample_set).resolve()
    manifest_path = (
        expected_plan.parent / "receipts" / f"{sample_set}-sample-manifest.json"
    ).resolve()
    expected_video = (
        ROOT
        / f"build/visual_edition/isolated-renders/{chapter_id}/draft/{chapter_id}-animatic.mp4"
        if sample_set == "animatic"
        else ROOT / f"build/visual_edition/generation-2/final/{chapter_id}.mp4"
    ).resolve()
    if video != expected_video:
        raise SystemExit("sample video does not match the governed sample set")
    try:
        ffmpeg = pinned_ffmpeg()
        if sample_set_current(
            manifest_path,
            output_dir / "index.html",
            output_dir,
            video,
            plan,
            sample_set,
            args.target_time,
            ffmpeg,
        ):
            print(
                f"Sample set is current; reused {output_dir / 'index.html'} and "
                f"{manifest_path} ({digest(manifest_path)})."
            )
            return
        index_path, manifest_path, image_count = build(
            video,
            plan,
            output_dir,
            manifest_path,
            sample_set,
            ffmpeg,
            args.samples,
            args.target_time,
        )
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        raise SystemExit(f"Unable to build beat review sheet: {exc}") from exc
    print(
        f"Wrote {image_count} samples, {index_path}, and bound manifest {manifest_path} "
        f"({digest(manifest_path)})."
    )


if __name__ == "__main__":
    main()
