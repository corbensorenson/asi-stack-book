#!/usr/bin/env python3
"""Capture the exact local P7.3 Manim runtime without tracking the environment."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visual_edition/toolchain.json"
LOCK = ROOT / "visual_edition/requirements.lock.txt"
CONFIG = ROOT / "visual_edition/manim.cfg"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_version(command: str, *args: str) -> str:
    try:
        output = run(command, *args)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "absent"
    match = re.search(r"\d+(?:\.\d+){1,3}", output)
    return match.group(0) if match else output.splitlines()[0][:120]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default="build/visual_edition/venv/bin/python")
    args = parser.parse_args()
    # Do not resolve the venv launcher symlink: resolving it to the base
    # interpreter discards the virtual-environment prefix and package graph.
    python = str(ROOT / args.python) if not Path(args.python).is_absolute() else args.python

    probe = json.loads(run(
        python,
        "-c",
        (
            "import json,manim,numpy,platform,sys;"
            "print(json.dumps({'machine':platform.machine(),'python':platform.python_version(),"
            "'implementation':platform.python_implementation(),'manim':manim.__version__,"
            "'numpy':numpy.__version__}))"
        ),
    ).splitlines()[-1])
    if probe["machine"] != "arm64":
        raise SystemExit(f"Refusing non-ARM runtime: {probe}")
    freeze = sorted(
        line
        for line in run(python, "-m", "pip", "freeze").splitlines()
        if line.strip() and "==" in line and not line.startswith("WARNING:")
    )
    locked = sorted(
        line.strip()
        for line in LOCK.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    )
    if sorted(line.lower() for line in freeze) != sorted(line.lower() for line in locked):
        raise SystemExit("requirements.lock.txt does not exactly match the isolated runtime")

    value = json.loads(OUT.read_text(encoding="utf-8"))
    value["captured_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    value["host"].update({
        "operating_system_version": run("sw_vers", "-productVersion"),
        "operating_system_build": run("sw_vers", "-buildVersion"),
        "architecture": probe["machine"],
    })
    value["python"].update({
        "implementation": probe["implementation"],
        "version": probe["python"],
        "architecture": probe["machine"],
    })
    value["manim"]["version"] = probe["manim"]
    value["native_dependencies"].update({
        "cairo": run("pkg-config", "--modversion", "cairo"),
        "pango": run("pkg-config", "--modversion", "pango"),
        "ffmpeg": first_version("ffmpeg", "-version"),
        "latex": first_version("latex", "--version"),
        "dvisvgm": first_version("dvisvgm", "--version"),
    })
    value["requirements_lock_sha256"] = digest(LOCK)
    value["configuration_sha256"] = digest(CONFIG)
    OUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        f"Captured {value['toolchain_id']}: Python {probe['python']} {probe['machine']}, "
        f"ManimCE {probe['manim']}, NumPy {probe['numpy']}, FFmpeg {value['native_dependencies']['ffmpeg']}."
    )


if __name__ == "__main__":
    main()
