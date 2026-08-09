#!/usr/bin/env python3
"""Validate the tracked Manim lock and optionally probe the ignored runtime."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
SCHEMA = ROOT / "schemas/manim_toolchain.schema.json"
LOCK = ROOT / "visual_edition/requirements.lock.txt"
CONFIG = ROOT / "visual_edition/manim.cfg"
GRAMMAR = ROOT / "visual_edition/visual_grammar.json"
GRAMMAR_SCHEMA = ROOT / "schemas/visual_grammar.schema.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_luminance(color: str) -> float:
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        raise ValueError(f"invalid sRGB color {color!r}")
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    high, low = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (high + 0.05) / (low + 0.05)


def visual_grammar_errors(grammar: dict) -> list[str]:
    schema = json.loads(GRAMMAR_SCHEMA.read_text(encoding="utf-8"))
    failures = [
        f"visual-grammar-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(grammar)
    ]
    palette = grammar.get("palette", {})
    contrast = grammar.get("contrast", {})
    minimum = contrast.get("normal_text_minimum_ratio")
    if isinstance(minimum, (int, float)):
        for foreground_role in contrast.get("normal_text_roles", []):
            foreground = palette.get(foreground_role)
            for background_role in contrast.get("background_roles", []):
                background = palette.get(background_role)
                if not isinstance(foreground, str) or not isinstance(background, str):
                    continue
                try:
                    actual = contrast_ratio(foreground, background)
                except ValueError as exc:
                    failures.append(str(exc))
                    continue
                if actual + 1e-9 < float(minimum):
                    failures.append(
                        f"{foreground_role} on {background_role} contrast {actual:.2f}:1 "
                        f"is below {float(minimum):.2f}:1"
                    )
    if grammar.get("motion", {}).get("maximum_flashes_per_second") != 0:
        failures.append("visual grammar must prohibit deliberate flashing")
    accessibility = grammar.get("accessibility", {})
    for field in (
        "motion_never_sole_carrier",
        "color_never_sole_carrier",
        "reviewed_captions_required",
        "descriptive_transcript_required",
        "material_visual_changes_described",
    ):
        if accessibility.get(field) is not True:
            failures.append(f"visual grammar must keep {field}=true")
    return failures


def errors(value: dict) -> list[str]:
    failures = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(value)
    ]
    if value.get("requirements_lock_sha256") != digest(LOCK):
        failures.append("requirements lock digest drift")
    if value.get("configuration_sha256") != digest(CONFIG):
        failures.append("Manim configuration digest drift")
    if value.get("visual_grammar_sha256") != digest(GRAMMAR):
        failures.append("visual grammar digest drift")
    captured_host = value.get("host", {})
    on_captured_host_class = (
        platform.system() == "Darwin"
        and platform.machine() == captured_host.get("architecture")
    )
    # The schema is the cross-platform lock for the exact qualified macOS/ARM
    # binaries.  Only dereference and execute those absolute paths on the host
    # class that can actually own them; Linux CI validates the lock, not a
    # fictitious local render runtime.
    if on_captured_host_class:
        for name, binding in value.get("media_tools", {}).items():
            path = Path(binding.get("path", ""))
            if not path.is_file() or digest(path) != binding.get("sha256"):
                failures.append(f"{name} executable identity drift")
                continue
            try:
                version_line = subprocess.check_output(
                    [str(path), "-version"], text=True, stderr=subprocess.STDOUT,
                    timeout=30,
                ).splitlines()[0]
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                failures.append(f"{name} executable version probe failed")
            else:
                if not version_line.startswith(f"{name} version {binding.get('version')} "):
                    failures.append(f"{name} executable version drift")
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    failures.extend(visual_grammar_errors(grammar))
    typography = grammar.get("typography", {})
    grammar_fonts = {
        role: typography.get(role) for role in ("primary", "fallback", "monospace")
    }
    if value.get("font_contract", {}) != {
        **grammar_fonts,
        "math_strategy_until_latex_qualification": "pango_unicode_and_prevalidated_svg_only",
    }:
        failures.append("font contract drifted from the ratified visual grammar")
    lock = LOCK.read_text(encoding="utf-8").lower()
    for required in ("manim==0.20.1", "numpy==2.5.1", "manimpango==0.6.1", "pycairo==1.29.0"):
        if required not in lock:
            failures.append(f"missing pinned dependency: {required}")
    config = CONFIG.read_text(encoding="utf-8")
    if "renderer = cairo" not in config or "media_dir = build/visual_edition/media" not in config:
        failures.append("Manim config does not bind Cairo and ignored build media")
    expected_release = {
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 30,
        "quality_flag": "none_use_exact_config",
        "video_codec": "h264",
        "pixel_format": "yuv420p",
    }
    if value.get("render_profiles", {}).get("release") != expected_release:
        failures.append("release profile drifted from exact 1080p30 config contract")
    if value.get("qualification_state") == "qualified_for_all_pilots":
        native = value.get("native_dependencies", {})
        if native.get("latex") == "absent" or native.get("dvisvgm") == "absent":
            failures.append("all-pilot qualification requires LaTeX and dvisvgm")
    return failures


def probe_runtime(value: dict, python: str) -> list[str]:
    # Preserve the venv launcher path rather than resolving its interpreter
    # symlink and accidentally probing the global package graph.
    executable = str(ROOT / python) if not Path(python).is_absolute() else python
    try:
        output = subprocess.check_output(
            [
                executable,
                "-c",
                (
                    "import json,manim,manimpango,platform;"
                    "print(json.dumps({'machine':platform.machine(),"
                    "'python':platform.python_version(),'manim':manim.__version__,"
                    "'fonts':sorted(manimpango.list_fonts())}))"
                ),
            ],
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        actual = json.loads(output.splitlines()[-1])
    except (
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        json.JSONDecodeError,
    ) as exc:
        return [f"runtime probe failed: {exc}"]
    expected = {
        "machine": value["python"]["architecture"],
        "python": value["python"]["version"],
        "manim": value["manim"]["version"],
    }
    actual_identity = {key: actual.get(key) for key in expected}
    failures = [] if actual_identity == expected else [
        f"runtime identity mismatch: expected {expected}, got {actual_identity}"
    ]
    installed_fonts = set(actual.get("fonts", []))
    for role, font in value.get("font_contract", {}).items():
        if role == "math_strategy_until_latex_qualification":
            continue
        if font not in installed_fonts:
            failures.append(f"required {role} font is unavailable to Manim/Pango: {font}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-runtime", action="store_true")
    parser.add_argument("--python", default="build/visual_edition/venv/bin/python")
    args = parser.parse_args()
    value = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    failures = errors(value)
    if args.probe_runtime:
        failures.extend(probe_runtime(value, args.python))

    mutations = []
    for label, edit in (
        ("architecture widening", lambda d: d["python"].__setitem__("architecture", "x86_64")),
        ("ManimGL substitution", lambda d: d["manim"].__setitem__("manimgl", True)),
        ("version drift", lambda d: d["manim"].__setitem__("version", "0.19.0")),
        ("global environment", lambda d: d["python"].__setitem__("environment_class", "global")),
        ("binary path drift", lambda d: d.__setitem__("configuration_sha256", "0" * 64)),
        ("silent font substitution", lambda d: d["font_contract"].__setitem__("fallback", "DejaVu Sans")),
        ("1080p60 shortcut substitution", lambda d: d["render_profiles"]["release"].__setitem__("quality_flag", "-qh")),
        ("support promotion", lambda d: d.__setitem__("support_state_effect", "promotion")),
        ("FFmpeg executable drift", lambda d: d["media_tools"]["ffmpeg"].__setitem__("sha256", "0" * 64)),
        ("FFprobe executable drift", lambda d: d["media_tools"]["ffprobe"].__setitem__("sha256", "0" * 64)),
        ("visual grammar identity drift", lambda d: d.__setitem__("visual_grammar_sha256", "0" * 64)),
    ):
        candidate = copy.deepcopy(value)
        edit(candidate)
        mutations.append((label, candidate))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    grammar_mutations = (
        (
            "low-contrast foreground",
            lambda d: d["palette"].__setitem__("accent", d["palette"]["background"]),
        ),
        (
            "flashing allowance",
            lambda d: d["motion"].__setitem__("maximum_flashes_per_second", 3),
        ),
        (
            "color-only meaning",
            lambda d: d["accessibility"].__setitem__("color_never_sole_carrier", False),
        ),
    )
    for label, edit in grammar_mutations:
        candidate = copy.deepcopy(grammar)
        edit(candidate)
        if not visual_grammar_errors(candidate):
            failures.append(f"visual-grammar negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Manim toolchain validation failed:\n - " + "\n - ".join(failures))
    suffix = " with live ARM runtime probe" if args.probe_runtime else ""
    print(
        f"Manim toolchain validation passed{suffix}: {value['toolchain_id']}, "
        f"qualification={value['qualification_state']}, 14/14 mutations rejected."
    )


if __name__ == "__main__":
    main()
