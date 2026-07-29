#!/usr/bin/env python3
"""Validate the tracked Manim lock and optionally probe the ignored runtime."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
SCHEMA = ROOT / "schemas/manim_toolchain.schema.json"
LOCK = ROOT / "visual_edition/requirements.lock.txt"
CONFIG = ROOT / "visual_edition/manim.cfg"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(value: dict) -> list[str]:
    failures = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(value)
    ]
    if value.get("requirements_lock_sha256") != digest(LOCK):
        failures.append("requirements lock digest drift")
    if value.get("configuration_sha256") != digest(CONFIG):
        failures.append("Manim configuration digest drift")
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
                    "import json,manim,platform;"
                    "print(json.dumps({'machine':platform.machine(),"
                    "'python':platform.python_version(),'manim':manim.__version__}))"
                ),
            ],
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
        )
        actual = json.loads(output.splitlines()[-1])
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return [f"runtime probe failed: {exc}"]
    expected = {
        "machine": value["python"]["architecture"],
        "python": value["python"]["version"],
        "manim": value["manim"]["version"],
    }
    return [] if actual == expected else [f"runtime identity mismatch: expected {expected}, got {actual}"]


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
        ("1080p60 shortcut substitution", lambda d: d["render_profiles"]["release"].__setitem__("quality_flag", "-qh")),
        ("support promotion", lambda d: d.__setitem__("support_state_effect", "promotion")),
    ):
        candidate = copy.deepcopy(value)
        edit(candidate)
        mutations.append((label, candidate))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Manim toolchain validation failed:\n - " + "\n - ".join(failures))
    suffix = " with live ARM runtime probe" if args.probe_runtime else ""
    print(
        f"Manim toolchain validation passed{suffix}: {value['toolchain_id']}, "
        f"qualification={value['qualification_state']}, 7/7 mutations rejected."
    )


if __name__ == "__main__":
    main()
