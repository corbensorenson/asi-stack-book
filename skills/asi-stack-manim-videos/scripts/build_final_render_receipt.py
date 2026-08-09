#!/usr/bin/env python3
"""Compile a final Manim render receipt from governed release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from audit_av_experience import (
    AUDITOR_PATH,
    DETECTION_CONTRACT,
    classify_declared_intervals,
    media_tool_identities,
)


COMPILER = Path(__file__).resolve()


def discover_repository_root() -> Path:
    configured = os.environ.get("ASI_STACK_BOOK_ROOT")
    candidates = [] if not configured else [Path(configured)]
    candidates.extend((Path.cwd(), *Path.cwd().parents, *COMPILER.parents))
    for candidate in candidates:
        if (
            (candidate / "book_structure.json").is_file()
            and (candidate / "visual_edition").is_dir()
        ):
            return candidate.resolve()
    raise RuntimeError(
        "ASI Stack repository root is unavailable; run from the book repository or set ASI_STACK_BOOK_ROOT"
    )


ROOT = discover_repository_root()
NEGATIVE_CONTROL_COUNT = 4
TRACKED_COMPILER = ROOT / "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py"
LEDGER = ROOT / "visual_edition/manim_v2_production_ledger.json"
RECEIPT_SCHEMA = ROOT / "schemas/manim_render_receipt.schema.json"
SANDBOX_SCHEMA = ROOT / "schemas/manim_sandbox_policy_receipt.schema.json"
AV_DIAGNOSTICS_SCHEMA = ROOT / "schemas/manim_av_diagnostics.schema.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def checked_repo_file(value: str | Path) -> Path:
    path = (ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes the repository: {value}") from exc
    if not path.is_file():
        raise ValueError(f"required file is missing: {relative(path)}")
    return path


def binding(path: Path) -> dict[str, str]:
    return {"path": relative(path), "sha256": sha256(path)}


def bound_file(value: Any, label: str) -> Path:
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not an artifact binding")
    path = checked_repo_file(value.get("path", ""))
    if sha256(path) != value.get("sha256"):
        raise ValueError(f"{label} digest drift")
    return path


def run_json(argv: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            argv, capture_output=True, text=True, check=False, timeout=30
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command exceeded 30 seconds: {' '.join(argv)}") from exc
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(argv)}\n{detail}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("command returned unreadable JSON") from exc


def parse_rate(value: Any) -> float:
    if not isinstance(value, str) or not value or value == "0/0":
        raise ValueError("video stream has no usable frame rate")
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"video stream has invalid frame rate {value!r}") from exc


def media_metadata(probe: dict[str, Any]) -> dict[str, Any]:
    streams = probe.get("streams", [])
    videos = [row for row in streams if isinstance(row, dict) and row.get("codec_type") == "video"]
    audios = [row for row in streams if isinstance(row, dict) and row.get("codec_type") == "audio"]
    if len(videos) != 1 or len(audios) != 1:
        raise ValueError("release master must contain exactly one video stream and one audio stream")
    video, audio = videos[0], audios[0]
    duration = float(probe.get("format", {}).get("duration") or 0)
    frame_rate = parse_rate(video.get("avg_frame_rate"))
    metadata = {
        "duration_seconds": round(duration, 3),
        "pixel_width": video.get("width"),
        "pixel_height": video.get("height"),
        "frame_rate": int(frame_rate) if frame_rate.is_integer() else frame_rate,
        "video_codec": video.get("codec_name"),
        "pixel_format": video.get("pix_fmt"),
        "audio_codec": audio.get("codec_name"),
        "audio_channels": audio.get("channels"),
        "audio_sample_rate_hz": int(audio.get("sample_rate") or 0),
    }
    expected = {
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 30,
        "video_codec": "h264",
        "pixel_format": "yuv420p",
        "audio_codec": "aac",
        "audio_sample_rate_hz": 48000,
    }
    mismatches = [
        f"{name}={metadata.get(name)!r}, expected {wanted!r}"
        for name, wanted in expected.items()
        if metadata.get(name) != wanted
    ]
    if metadata["audio_channels"] not in {1, 2}:
        mismatches.append(f"audio_channels={metadata['audio_channels']!r}, expected 1 or 2")
    if duration <= 0:
        mismatches.append("duration_seconds must be positive")
    if mismatches:
        raise ValueError("release master metadata mismatch: " + "; ".join(mismatches))
    return metadata


def probe_master(path: Path) -> dict[str, Any]:
    media_tools = media_tool_identities()
    return media_metadata(
        run_json([
            media_tools["ffprobe"]["path"],
            "-v", "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,sample_rate,channels",
            "-of", "json",
            str(path),
        ])
    )


def canonical_entry(ledger: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    matches = [row for row in ledger.get("entries", []) if row.get("chapter_id") == chapter_id]
    if len(matches) != 1:
        raise ValueError(f"ledger must contain exactly one entry for {chapter_id!r}")
    return matches[0]


def exact_ledger_binding(ledger: dict[str, Any], path_key: str, digest_key: str) -> dict[str, str]:
    value = {"path": ledger.get(path_key), "sha256": ledger.get(digest_key)}
    bound_file(value, path_key)
    return value


def compile_receipt(
    sandbox_receipt_path: Path,
    diagnostics_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    if COMPILER != TRACKED_COMPILER.resolve():
        raise RuntimeError(
            "final receipts must execute the repository-tracked compiler, not an installed skill copy"
        )
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    sandbox_receipt = json.loads(sandbox_receipt_path.read_text(encoding="utf-8"))
    sandbox_schema = json.loads(SANDBOX_SCHEMA.read_text(encoding="utf-8"))
    schema_errors = sorted(
        Draft202012Validator(sandbox_schema).iter_errors(sandbox_receipt),
        key=lambda error: tuple(map(str, error.path)),
    )
    if schema_errors:
        detail = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in schema_errors
        )
        raise ValueError(f"sandbox receipt is schema-invalid: {detail}")
    if sandbox_receipt.get("profile") != "release":
        raise ValueError("final receipt requires a release-profile sandbox receipt")

    chapter_id = sandbox_receipt.get("chapter_id")
    entry = canonical_entry(ledger, chapter_id)
    target = entry["target"]
    expected_output = ROOT / target["render_receipt_path"]
    if output_path.resolve() != expected_output.resolve():
        raise ValueError("final receipt output must use the canonical generation-2 path")

    chapter_path = bound_file(
        {"path": entry.get("chapter_path"), "sha256": entry.get("chapter_sha256")},
        "chapter",
    )
    treatment_path = bound_file(
        {"path": target.get("treatment_path"), "sha256": target.get("treatment_sha256")},
        "treatment",
    )
    plan_path = bound_file(
        {"path": target.get("beat_plan_path"), "sha256": target.get("beat_plan_sha256")},
        "beat plan",
    )
    scene_path = bound_file(
        {"path": target.get("scene_path"), "sha256": target.get("scene_sha256")},
        "scene",
    )
    narration_path = bound_file(
        {"path": target.get("narration_path"), "sha256": target.get("narration_sha256")},
        "narration",
    )
    treatment = json.loads(treatment_path.read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if treatment.get("chapter_id") != chapter_id or plan.get("chapter_id") != chapter_id:
        raise ValueError("treatment or beat-plan chapter identity drift")
    if plan.get("timing", {}).get("state") != "forced_aligned":
        raise ValueError("final receipt requires a forced-aligned beat plan")
    timing = plan["timing"]
    timing_path = bound_file(
        {"path": timing.get("receipt_path"), "sha256": timing.get("receipt_sha256")},
        "timing receipt",
    )
    narration_receipt_path = bound_file(
        {
            "path": timing.get("narration_receipt_path"),
            "sha256": timing.get("narration_receipt_sha256"),
        },
        "narration render receipt",
    )
    narration_verification_path = bound_file(
        {
            "path": timing.get("narration_verification_report_path"),
            "sha256": timing.get("narration_verification_report_sha256"),
        },
        "narration verification report",
    )
    anchor_path = bound_file(
        {
            "path": timing.get("manual_anchor_review_path"),
            "sha256": timing.get("manual_anchor_review_sha256"),
        },
        "manual anchor review",
    )
    if timing.get("manual_anchor_failures") != 0:
        raise ValueError("manual anchor review retains alignment failures")

    policy_runner = sandbox_receipt.get("runner", {})
    expected_runner = {
        "path": ledger.get("isolated_render_runner_path"),
        "sha256": ledger.get("isolated_render_runner_sha256"),
    }
    if policy_runner != expected_runner:
        raise ValueError("sandbox receipt does not bind the ledger-owned isolated runner")
    bound_file(expected_runner, "isolated render runner")
    if sandbox_receipt.get("scene") != binding(scene_path):
        raise ValueError("sandbox receipt does not bind the ledger-owned scene")
    if sandbox_receipt.get("treatment") != binding(treatment_path):
        raise ValueError("sandbox receipt does not bind the ledger-owned treatment")
    audio_path = bound_file(sandbox_receipt.get("audio_master"), "audio master")
    narration_receipt = json.loads(
        narration_receipt_path.read_text(encoding="utf-8")
    )
    narration_verification = json.loads(
        narration_verification_path.read_text(encoding="utf-8")
    )
    if (
        narration_receipt.get("output_path") != relative(audio_path)
        or narration_receipt.get("output_sha256") != sha256(audio_path)
    ):
        raise ValueError("sandbox audio master differs from the narration render receipt")
    if (
        narration_verification.get("validation_state") != "pass"
        or narration_verification.get("receipt_sha256") != sha256(narration_receipt_path)
        or narration_verification.get("audio_sha256") != sha256(audio_path)
        or not narration_verification.get("checks")
        or not all(narration_verification.get("checks", {}).values())
    ):
        raise ValueError("narration verification report is stale or retains a failing check")
    if sandbox_receipt.get("network_access") is not False:
        raise ValueError("sandbox receipt does not record denied network access")
    if sandbox_receipt.get("credential_environment_inherited") is not False:
        raise ValueError("sandbox receipt inherited credential-bearing environment")
    if sandbox_receipt.get("repository_writable_roots") != ["build/visual_edition"]:
        raise ValueError("sandbox receipt widens the repository write boundary")
    bound_file(sandbox_receipt.get("policy"), "sandbox policy")
    expected_auditor = {
        "path": ledger.get("scene_source_auditor_path"),
        "sha256": ledger.get("scene_source_auditor_sha256"),
    }
    if sandbox_receipt.get("source_preflight", {}).get("auditor") != expected_auditor:
        raise ValueError("sandbox receipt does not bind the ledger-owned scene auditor")
    bound_file(expected_auditor, "scene source auditor")

    outputs = {
        row.get("role"): row
        for row in sandbox_receipt.get("outputs", [])
        if isinstance(row, dict)
    }
    visual_path = bound_file(outputs.get("visual_track"), "visual track")
    master_path = bound_file(outputs.get("muxed_master"), "muxed master")
    for role, path in (("visual_track", visual_path), ("muxed_master", master_path)):
        if outputs[role].get("size_bytes") != path.stat().st_size:
            raise ValueError(f"sandbox receipt {role} size drift")
    if (
        relative(master_path) != target.get("master_path")
        or sha256(master_path) != target.get("master_sha256")
    ):
        raise ValueError("sync the production ledger after rendering; master identity is stale")

    diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))
    diagnostics_schema = json.loads(AV_DIAGNOSTICS_SCHEMA.read_text(encoding="utf-8"))
    diagnostics_schema_errors = sorted(
        Draft202012Validator(diagnostics_schema).iter_errors(diagnostics),
        key=lambda error: tuple(map(str, error.path)),
    )
    if diagnostics_schema_errors:
        detail = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in diagnostics_schema_errors
        )
        raise ValueError(f"A/V diagnostics are schema-invalid: {detail}")
    expected_auditor = {"path": AUDITOR_PATH, "sha256": sha256(ROOT / AUDITOR_PATH)}
    if diagnostics.get("auditor") != expected_auditor:
        raise ValueError("A/V diagnostics do not bind the current tracked auditor")
    if ledger.get("authoring_component_sha256", {}).get(AUDITOR_PATH) != expected_auditor["sha256"]:
        raise ValueError("production ledger does not bind the current A/V auditor")
    if diagnostics.get("video_sha256") != sha256(master_path):
        raise ValueError("A/V diagnostics bind a different master")
    if diagnostics.get("beat_plan_sha256") != sha256(plan_path):
        raise ValueError("A/V diagnostics bind a different beat plan")
    if diagnostics.get("video") != relative(master_path):
        raise ValueError("A/V diagnostics name a noncanonical master path")
    if diagnostics.get("beat_plan") != relative(plan_path):
        raise ValueError("A/V diagnostics name a noncanonical beat-plan path")
    visual_toolchain = json.loads(
        (ROOT / ledger["visual_toolchain_path"]).read_text(encoding="utf-8")
    )
    if sandbox_receipt.get("media_tools") != visual_toolchain.get("media_tools"):
        raise ValueError(
            "sandbox receipt does not bind the pinned FFmpeg and FFprobe identities"
        )
    if diagnostics.get("media_tools") != visual_toolchain.get("media_tools"):
        raise ValueError("A/V diagnostics do not bind the pinned FFmpeg and FFprobe identities")
    if diagnostics.get("detection_contract") != DETECTION_CONTRACT:
        raise ValueError("A/V diagnostics weaken or alter the governed detection contract")
    if diagnostics.get("validation_state") != "pass":
        raise ValueError("A/V diagnostics have not reached a warning-free pass state")
    try:
        declared_freezes, undeclared_freezes = classify_declared_intervals(
            diagnostics.get("freezes", []), plan.get("beats", []), kind="freeze"
        )
        declared_silences, undeclared_silences = classify_declared_intervals(
            diagnostics.get("silences", []), plan.get("beats", []), kind="silence"
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("A/V diagnostics contain malformed interval custody") from exc
    if (
        diagnostics.get("declared_freezes") != declared_freezes
        or diagnostics.get("undeclared_freezes") != undeclared_freezes
        or diagnostics.get("declared_silences") != declared_silences
        or diagnostics.get("undeclared_silences") != undeclared_silences
    ):
        raise ValueError("A/V diagnostic interval classifications do not reproduce from the beat plan")
    if diagnostics.get("errors"):
        raise ValueError("A/V diagnostics retain mechanical errors")
    if diagnostics.get("warnings"):
        raise ValueError("A/V diagnostics retain warnings; resolve the cause before final receipt compilation")

    metadata = probe_master(master_path)
    if abs(metadata["duration_seconds"] - float(plan["target_duration_seconds"])) > 0.25:
        raise ValueError("master duration differs from the forced-aligned beat plan")
    compiler_binding = {
        "path": relative(TRACKED_COMPILER),
        "sha256": sha256(TRACKED_COMPILER),
    }
    if ledger.get("authoring_component_sha256", {}).get(compiler_binding["path"]) != compiler_binding["sha256"]:
        raise ValueError("sync the production ledger; final-receipt compiler identity is stale")

    assets = treatment.get("art_direction", {}).get("asset_plan", [])
    for row in assets if isinstance(assets, list) else []:
        if (
            not isinstance(row, dict)
            or row.get("status") not in {"original", "rights_cleared"}
            or row.get("security_review") not in {"pass", "not_applicable"}
        ):
            raise ValueError("final receipt cannot claim rights clearance for a planned or unreviewed asset")
        asset_path = checked_repo_file(row.get("path_or_source", ""))
        if sha256(asset_path) != row.get("sha256"):
            raise ValueError(f"cleared asset digest drift: {relative(asset_path)}")

    input_bindings = {
        "chapter": binding(chapter_path),
        "treatment": binding(treatment_path),
        "beat_plan": binding(plan_path),
        "scene": binding(scene_path),
        "narration": binding(narration_path),
        "visual_grammar": exact_ledger_binding(ledger, "visual_grammar_path", "visual_grammar_sha256"),
        "visual_toolchain": exact_ledger_binding(ledger, "visual_toolchain_path", "visual_toolchain_sha256"),
        "primitive_library": exact_ledger_binding(ledger, "primitive_library_path", "primitive_library_sha256"),
        "scene_source_auditor": exact_ledger_binding(ledger, "scene_source_auditor_path", "scene_source_auditor_sha256"),
        "isolated_render_runner": expected_runner,
        "final_receipt_compiler": compiler_binding,
        "av_auditor": expected_auditor,
        "av_diagnostics_schema": exact_ledger_binding(
            ledger, "av_diagnostics_schema_path", "av_diagnostics_schema_sha256"
        ),
        "sandbox_policy_receipt_schema": exact_ledger_binding(
            ledger, "sandbox_policy_receipt_schema_path", "sandbox_policy_receipt_schema_sha256"
        ),
        "primitive_regression_manifest": exact_ledger_binding(
            ledger, "primitive_regression_manifest_path", "primitive_regression_manifest_sha256"
        ),
        "narration_toolchain": exact_ledger_binding(
            ledger, "narration_toolchain_path", "narration_toolchain_sha256"
        ),
        "timing_receipt": binding(timing_path),
        "narration_render_receipt": binding(narration_receipt_path),
        "narration_verification_report": binding(narration_verification_path),
        "audio_master": binding(audio_path),
    }
    scene_step = sandbox_receipt["render_steps"][0]
    try:
        random_seed = int(scene_step["command_argv"][scene_step["command_argv"].index("--seed") + 1])
    except (ValueError, IndexError) as exc:
        raise ValueError("sandbox receipt lacks a parseable render seed") from exc
    prior_timestamp = None
    if output_path.is_file():
        try:
            prior_timestamp = json.loads(output_path.read_text(encoding="utf-8")).get("rendered_at_utc")
        except json.JSONDecodeError:
            prior_timestamp = None
    value = {
        "schema_version": "asi_stack.manim_render_receipt.v1",
        "chapter_id": chapter_id,
        "generation": 2,
        "rendered_at_utc": prior_timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_commit": treatment["source_commit"],
        "render": {
            "render_steps": [
                {
                    "phase": row["phase"],
                    "command_argv": row["command_argv"],
                    "exit_code": row["exit_code"],
                }
                for row in sandbox_receipt["render_steps"]
            ],
            "toolchain_id": sandbox_receipt["toolchain_id"],
            "random_seed": random_seed,
            "timezone": "UTC",
            "cache_policy": "clean",
        },
        "execution_security": {
            "isolation_mode": sandbox_receipt["isolation_mode"],
            "network_access": sandbox_receipt["network_access"],
            "credential_environment_inherited": sandbox_receipt["credential_environment_inherited"],
            "repository_writable_roots": sandbox_receipt["repository_writable_roots"],
            "sandbox_policy_receipt": binding(sandbox_receipt_path),
            "source_preflight_scene_sha256": sandbox_receipt["source_preflight"]["scene_sha256"],
            "source_preflight_verdict": sandbox_receipt["source_preflight"]["verdict"],
            "source_preflight_finding_count": sandbox_receipt["source_preflight"]["finding_count"],
        },
        "input_bindings": input_bindings,
        "output": {"path": relative(master_path), "sha256": sha256(master_path), **metadata},
        "av_diagnostics": binding(diagnostics_path),
        "unresolved_material_warnings": 0,
        "asset_rights_state": (
            "no_external_assets"
            if not assets
            else "cleared"
        ),
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": "This receipt establishes exact release-artifact custody only; it does not prove chapter truth, teaching effectiveness, safety, or publication authority.",
    }
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: tuple(map(str, error.path)),
    )
    if errors:
        detail = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"compiled final receipt is schema-invalid: {detail}")
    if anchor_path == timing_path:
        raise ValueError("manual anchor review must be distinct from the timing receipt")
    return value


def self_test() -> list[str]:
    valid_probe = {
        "format": {"duration": "120.000"},
        "streams": [
            {
                "codec_type": "video", "codec_name": "h264", "width": 1920,
                "height": 1080, "pix_fmt": "yuv420p", "avg_frame_rate": "30/1",
            },
            {
                "codec_type": "audio", "codec_name": "aac", "channels": 1,
                "sample_rate": "48000",
            },
        ],
    }
    failures: list[str] = []
    try:
        metadata = media_metadata(valid_probe)
    except Exception as exc:
        return [f"valid media probe failed: {exc}"]
    if metadata.get("duration_seconds") != 120.0:
        failures.append("valid media probe changed duration")
    controls = (
        ("missing audio", lambda row: row["streams"].pop(), "exactly one"),
        ("wrong frame rate", lambda row: row["streams"][0].update(avg_frame_rate="24/1"), "frame_rate"),
        ("wrong pixel format", lambda row: row["streams"][0].update(pix_fmt="yuv444p"), "pixel_format"),
        ("wrong sample rate", lambda row: row["streams"][1].update(sample_rate="44100"), "audio_sample_rate_hz"),
    )
    for label, mutate, expected in controls:
        candidate = json.loads(json.dumps(valid_probe))
        mutate(candidate)
        try:
            media_metadata(candidate)
        except ValueError as exc:
            if expected not in str(exc):
                failures.append(f"{label} raised the wrong error: {exc}")
        else:
            failures.append(f"media metadata negative control did not trigger: {label}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sandbox-receipt", type=Path)
    parser.add_argument("--av-diagnostics", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        failures = self_test()
        if failures:
            raise SystemExit("Final-render-receipt compiler self-test failed:\n - " + "\n - ".join(failures))
        print(
            "Self-test passed: valid release metadata accepted and "
            f"{NEGATIVE_CONTROL_COUNT} malformed probes rejected."
        )
        return
    if not all((args.sandbox_receipt, args.av_diagnostics, args.output)):
        parser.error("--sandbox-receipt, --av-diagnostics, and --output are required")
    try:
        sandbox_receipt = checked_repo_file(args.sandbox_receipt)
        diagnostics = checked_repo_file(args.av_diagnostics)
        output = (ROOT / args.output).resolve() if not args.output.is_absolute() else args.output.resolve()
        output.relative_to(ROOT.resolve())
        value = compile_receipt(sandbox_receipt, diagnostics, output)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to compile final render receipt: {exc}") from exc
    rendered = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            raise SystemExit("Final render receipt is stale or missing.")
        print(f"Final render receipt is current: {relative(output)}")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    pending = output.with_suffix(".tmp.json")
    pending.write_text(rendered, encoding="utf-8")
    pending.replace(output)
    print(f"Wrote final render receipt: {relative(output)}")


if __name__ == "__main__":
    main()
