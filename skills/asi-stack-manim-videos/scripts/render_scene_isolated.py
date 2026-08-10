#!/usr/bin/env python3
"""Render an audited ASI Stack Manim scene under a macOS Seatbelt policy.

The runner constructs the Manim command itself, strips the inherited
environment, denies network access, confines writes to build/visual_edition,
and emits a machine-checkable policy receipt. Static source review remains a
separate preflight; neither mechanism should be represented as a proof that
Manim or a generated scene is harmless.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from audit_scene_source import audit_scene


RUNNER = Path(__file__).resolve()


def discover_repository_root() -> Path:
    configured = os.environ.get("ASI_STACK_BOOK_ROOT")
    candidates = [] if not configured else [Path(configured)]
    candidates.extend((Path.cwd(), *Path.cwd().parents, *RUNNER.parents))
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
TRACKED_RUNNER = ROOT / "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py"
BUILD_ROOT = (ROOT / "build/visual_edition").resolve()
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
CONFIG = ROOT / "visual_edition/manim.cfg"
VENV_PYTHON = ROOT / "build/visual_edition/venv/bin/python"
SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
CREDENTIAL_MARKERS = (
    "API_KEY", "AUTH", "BEARER", "CREDENTIAL", "GITHUB_TOKEN", "KEYCHAIN",
    "PASSWORD", "PRIVATE_KEY", "SECRET", "SESSION", "SSH_", "TOKEN",
)
SYSTEM_READ_ROOTS = (
    Path("/System"),
    Path("/Library/ColorSync"),
    Path("/Library/Fonts"),
    Path("/Library/Frameworks"),
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/opt/homebrew"),
)
DEVICE_READ_PATHS = tuple(Path(value) for value in ("/dev/null", "/dev/random", "/dev/urandom", "/dev/zero"))
MAX_PROCESSES = 256
MEMORY_LIMIT_STATUS = "not_enforced_macos"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def checked_repo_path(value: str | Path, *, must_exist: bool = True) -> Path:
    path = (ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes the repository: {value}") from exc
    if must_exist and not path.is_file():
        raise ValueError(f"required file is missing: {relative(path)}")
    return path


def pinned_media_tools() -> dict[str, dict[str, str]]:
    toolchain = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    bindings = toolchain.get("media_tools", {})
    for name in ("ffmpeg", "ffprobe"):
        binding = bindings.get(name, {})
        path = Path(binding.get("path", ""))
        if not path.is_file() or sha256(path) != binding.get("sha256"):
            raise RuntimeError(f"pinned {name} executable identity drift")
        try:
            version_line = subprocess.check_output(
                [str(path), "-version"],
                text=True,
                stderr=subprocess.STDOUT,
                timeout=30,
            ).splitlines()[0]
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"pinned {name} executable version probe failed") from exc
        if not version_line.startswith(f"{name} version {binding.get('version')} "):
            raise RuntimeError(f"pinned {name} executable version drift")
    return bindings


def sbpl_string(path: Path) -> str:
    return json.dumps(str(path.resolve()))


def subpath_rule(operation: str, path: Path) -> str:
    return f"({operation} (subpath {sbpl_string(path)}))"


def literal_rule(operation: str, path: Path) -> str:
    return f"({operation} (literal {sbpl_string(path)}))"


def executable_paths() -> list[Path]:
    paths = [VENV_PYTHON, VENV_PYTHON.resolve()]
    framework_root = VENV_PYTHON.resolve().parent.parent
    framework_launcher = framework_root / "Resources/Python.app/Contents/MacOS/Python"
    if framework_launcher.is_file():
        paths.append(framework_launcher)
    ffmpeg = Path(pinned_media_tools()["ffmpeg"]["path"])
    paths.extend((ffmpeg, ffmpeg.resolve()))
    return sorted({path.resolve() for path in paths if path.exists()}, key=str)


def build_policy(read_paths: list[Path]) -> str:
    lines = [
        "(version 1)",
        "(deny default)",
        '(import "system.sb")',
        "(allow process-fork)",
        "(allow signal (target self))",
        "(allow sysctl-read)",
        "(allow file-read-metadata)",
    ]
    for path in SYSTEM_READ_ROOTS:
        if path.exists():
            lines.append(subpath_rule("allow file-read*", path))
    for path in DEVICE_READ_PATHS:
        if path.exists():
            lines.append(literal_rule("allow file-read*", path))
    resolved_reads: set[Path] = set()
    for item in read_paths:
        lexical = Path(os.path.abspath(item))
        resolved_reads.add(lexical)
        if lexical.is_symlink():
            resolved_reads.add(lexical.parent)
        resolved_reads.add(item.resolve())
    traversal_paths = {ROOT.resolve()}
    for path in resolved_reads:
        cursor = path if path.is_dir() else path.parent
        while cursor == ROOT.resolve() or ROOT.resolve() in cursor.parents:
            traversal_paths.add(cursor)
            if cursor == ROOT.resolve():
                break
            cursor = cursor.parent
    for path in sorted(traversal_paths, key=str):
        lines.append(literal_rule("allow file-read*", path))
    for path in sorted(resolved_reads, key=str):
        lines.append(literal_rule("allow file-read*", path))
        if path.is_dir():
            lines.append(subpath_rule("allow file-read*", path))
    for path in executable_paths():
        lines.append(literal_rule("allow process-exec", path))
    lines.extend(
        (
            subpath_rule("allow file-read*", BUILD_ROOT),
            subpath_rule("allow file-write*", BUILD_ROOT),
            literal_rule("allow file-write-data", Path("/dev/null")),
            "(deny network*)",
        )
    )
    return "\n".join(lines) + "\n"


def sanitized_environment(home: Path, temp: Path) -> dict[str, str]:
    environment = {
        "HOME": str(home),
        "LANG": "en_US.UTF-8",
        "LC_ALL": "en_US.UTF-8",
        "MPLCONFIGDIR": str(home / ".config/matplotlib"),
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "PYTHONPATH": str(ROOT),
        "PYTHONSAFEPATH": "1",
        "TMPDIR": str(temp),
        "TZ": "UTC",
        "XDG_CACHE_HOME": str(home / ".cache"),
        "XDG_CONFIG_HOME": str(home / ".config"),
    }
    if any(any(marker in key.upper() for marker in CREDENTIAL_MARKERS) for key in environment):
        raise RuntimeError("sanitized render environment accidentally retained a credential-like key")
    return environment


def resource_limiter(cpu_seconds: int, file_size_bytes: int) -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_size_bytes, file_size_bytes))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))


def run_guarded(
    argv: list[str],
    *,
    policy_path: Path,
    environment: dict[str, str],
    log_path: Path,
    timeout_seconds: int,
    cpu_seconds: int,
    file_size_bytes: int,
) -> tuple[int, float]:
    command = [str(SANDBOX_EXEC), "-f", str(policy_path), *argv]
    started = time.monotonic()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("wb") as log:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            preexec_fn=lambda: resource_limiter(cpu_seconds, file_size_bytes),
        )
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            raise RuntimeError(f"isolated command exceeded {timeout_seconds} wall-clock seconds")
    return return_code, round(time.monotonic() - started, 3)


def policy_self_test(
    policy_path: Path,
    environment: dict[str, str],
    work_root: Path,
) -> dict[str, str]:
    allowed = work_root / "policy-probe-allowed.txt"
    denied = ROOT / ".asi-manim-policy-probe-denied"
    denied.unlink(missing_ok=True)
    probe = r'''
import json, os, pathlib, socket, subprocess, sys
allowed, denied, denied_read = map(pathlib.Path, sys.argv[1:4])
results = {}
try:
    allowed.write_text("allowed", encoding="utf-8")
    results["allowed_write"] = "pass"
except Exception as exc:
    results["allowed_write"] = type(exc).__name__
try:
    denied.write_text("denied", encoding="utf-8")
    results["denied_write"] = "fail"
except PermissionError:
    results["denied_write"] = "pass"
except Exception as exc:
    results["denied_write"] = type(exc).__name__
try:
    denied_read.read_bytes()
    results["denied_read"] = "fail"
except PermissionError:
    results["denied_read"] = "pass"
except Exception as exc:
    results["denied_read"] = type(exc).__name__
escape_link = allowed.parent / "policy-probe-escape-link"
try:
    escape_link.unlink(missing_ok=True)
    escape_link.symlink_to(denied)
    escape_link.write_text("escaped", encoding="utf-8")
    results["symlink_escape_denied"] = "fail"
except PermissionError:
    results["symlink_escape_denied"] = "pass"
except Exception as exc:
    results["symlink_escape_denied"] = type(exc).__name__
finally:
    escape_link.unlink(missing_ok=True)
escape_read_link = allowed.parent / "policy-probe-read-escape-link"
try:
    escape_read_link.unlink(missing_ok=True)
    escape_read_link.symlink_to(denied_read)
    escape_read_link.read_bytes()
    results["symlink_read_escape_denied"] = "fail"
except PermissionError:
    results["symlink_read_escape_denied"] = "pass"
except Exception as exc:
    results["symlink_read_escape_denied"] = type(exc).__name__
finally:
    escape_read_link.unlink(missing_ok=True)
hardlink = allowed.parent / "policy-probe-hardlink-escape"
try:
    hardlink.unlink(missing_ok=True)
    os.link(denied_read, hardlink)
    try:
        hardlink.read_bytes()
        results["hardlink_escape_denied"] = "fail"
    except PermissionError:
        results["hardlink_escape_denied"] = "pass"
    except Exception as exc:
        results["hardlink_escape_denied"] = type(exc).__name__
except PermissionError:
    results["hardlink_escape_denied"] = "pass"
except Exception as exc:
    results["hardlink_escape_denied"] = type(exc).__name__
finally:
    hardlink.unlink(missing_ok=True)
try:
    subprocess.run(["/usr/bin/true"], check=False)
    results["unlisted_exec_denied"] = "fail"
except PermissionError:
    results["unlisted_exec_denied"] = "pass"
except Exception as exc:
    results["unlisted_exec_denied"] = type(exc).__name__
sock = socket.socket()
sock.settimeout(0.2)
try:
    sock.connect(("127.0.0.1", 9))
    results["network_denied"] = "fail"
except PermissionError:
    results["network_denied"] = "pass"
except Exception as exc:
    results["network_denied"] = type(exc).__name__
finally:
    sock.close()
credential_markers = ("API_KEY", "AUTH", "BEARER", "CREDENTIAL", "GITHUB_TOKEN", "KEYCHAIN", "PASSWORD", "PRIVATE_KEY", "SECRET", "SESSION", "SSH_", "TOKEN")
results["credentials_stripped"] = "pass" if not any(any(marker in key.upper() for marker in credential_markers) for key in os.environ) else "fail"
print(json.dumps(results, sort_keys=True))
'''
    command = [
        str(VENV_PYTHON), "-c", probe, str(allowed), str(denied),
        str(ROOT / "book_structure.json"),
    ]
    completed = subprocess.run(
        [str(SANDBOX_EXEC), "-f", str(policy_path), *command],
        cwd=ROOT,
        env=environment,
        input=b"",
        capture_output=True,
        timeout=30,
        check=False,
    )
    if denied.exists():
        denied.unlink()
        raise RuntimeError("sandbox policy self-test wrote outside build/visual_edition")
    try:
        payload = json.loads(completed.stdout.decode("utf-8").splitlines()[-1])
    except (IndexError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        detail = completed.stderr.decode("utf-8", errors="replace")[-1000:]
        raise RuntimeError(f"sandbox policy self-test produced no readable receipt: {detail}") from exc
    expected = {
        "allowed_write": "pass",
        "denied_write": "pass",
        "denied_read": "pass",
        "symlink_escape_denied": "pass",
        "symlink_read_escape_denied": "pass",
        "hardlink_escape_denied": "pass",
        "unlisted_exec_denied": "pass",
        "network_denied": "pass",
        "credentials_stripped": "pass",
    }
    if completed.returncode != 0 or payload != expected:
        raise RuntimeError(f"sandbox policy self-test failed: {payload}")
    return payload


def resource_limit_self_test(
    policy_path: Path,
    environment: dict[str, str],
    work_root: Path,
    *,
    cpu_seconds: int,
    file_size_bytes: int,
) -> dict[str, str]:
    probe = r'''
import json, resource
limits = {
    "core_dump_bytes": list(resource.getrlimit(resource.RLIMIT_CORE)),
    "cpu_seconds": list(resource.getrlimit(resource.RLIMIT_CPU)),
    "max_file_size_bytes": list(resource.getrlimit(resource.RLIMIT_FSIZE)),
    "max_open_files": list(resource.getrlimit(resource.RLIMIT_NOFILE)),
    "max_processes": list(resource.getrlimit(resource.RLIMIT_NPROC)),
}
print(json.dumps(limits, sort_keys=True))
'''
    log_path = work_root / "resource-limit-self-test.log"
    return_code, _ = run_guarded(
        [str(VENV_PYTHON), "-c", probe],
        policy_path=policy_path,
        environment=environment,
        log_path=log_path,
        timeout_seconds=30,
        cpu_seconds=cpu_seconds,
        file_size_bytes=file_size_bytes,
    )
    try:
        payload = json.loads(log_path.read_text(encoding="utf-8").splitlines()[-1])
    except (IndexError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        detail = log_path.read_text(encoding="utf-8", errors="replace")[-1000:]
        raise RuntimeError(
            f"resource-limit self-test produced no readable receipt: {detail}"
        ) from exc
    expected = {
        "core_dump_bytes": [0, 0],
        "cpu_seconds": [cpu_seconds, cpu_seconds],
        "max_file_size_bytes": [file_size_bytes, file_size_bytes],
        "max_open_files": [256, 256],
        "max_processes": [MAX_PROCESSES, MAX_PROCESSES],
    }
    if return_code != 0 or payload != expected:
        raise RuntimeError(f"resource-limit self-test failed: {payload}")
    checks = {name: "pass" for name in expected}
    checks["memory_bound"] = MEMORY_LIMIT_STATUS
    return checks


def cleared_assets(treatment: dict[str, Any]) -> list[Path]:
    rows = treatment.get("art_direction", {}).get("asset_plan", [])
    assets: list[Path] = []
    for row in rows if isinstance(rows, list) else []:
        if (
            not isinstance(row, dict)
            or row.get("status") not in {"original", "rights_cleared"}
            or row.get("security_review") not in {"pass", "not_applicable"}
        ):
            continue
        path = checked_repo_path(row.get("path_or_source", ""))
        if sha256(path) != row.get("sha256"):
            raise ValueError(f"cleared asset digest drift: {relative(path)}")
        assets.append(path)
    return assets


def find_rendered_video(media_root: Path, output_name: str) -> Path:
    matches = sorted(media_root.rglob(output_name))
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one rendered {output_name!r} under {relative(media_root)}, found {len(matches)}"
        )
    return matches[0]


def manim_command(
    scene: Path,
    scene_class: str,
    chapter_id: str,
    profile: str,
    seed: int,
    media_root: Path,
) -> list[str]:
    resolution = "1920,1080" if profile == "release" else "854,480"
    frame_rate = "30" if profile == "release" else "15"
    return [
        str(VENV_PYTHON), "-m", "manim", "render",
        "--config_file", str(CONFIG),
        "--renderer", "cairo",
        "--format", "mp4",
        "--resolution", resolution,
        "--fps", frame_rate,
        "--seed", str(seed),
        "--disable_caching",
        "--progress_bar", "none",
        "--media_dir", str(media_root),
        "--output_file", f"{chapter_id}-visual.mp4",
        str(scene), scene_class,
    ]


def mux_command(
    ffmpeg: str,
    visual_output: Path,
    audio_master: Path,
    final_output: Path,
    profile: str,
) -> list[str]:
    if profile not in {"draft", "release"}:
        raise ValueError("mux profile must be draft or release")
    frame_rate = "15" if profile == "draft" else "30"
    return [
        ffmpeg, "-hide_banner", "-nostdin", "-y",
        "-i", str(visual_output), "-i", str(audio_master),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", frame_rate,
        "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
        "-movflags", "+faststart", str(final_output),
    ]


def pending_mux_output(final_output: Path, profile: str) -> Path:
    if profile not in {"draft", "release"}:
        raise ValueError("mux profile must be draft or release")
    return final_output.with_name(f".{final_output.stem}.{profile}.pending.mp4")


def write_receipt(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(".tmp.json")
    pending.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    pending.replace(path)


def render(args: argparse.Namespace) -> dict[str, Any]:
    if platform.system() != "Darwin" or not SANDBOX_EXEC.is_file():
        raise RuntimeError("this runner requires macOS sandbox-exec; use a no-network container or restricted CI runner elsewhere")
    if RUNNER != TRACKED_RUNNER.resolve():
        raise RuntimeError(
            "accepted renders must execute the repository-tracked runner, not an installed skill copy"
        )
    scene = checked_repo_path(args.scene)
    treatment_path = checked_repo_path(args.treatment)
    treatment = json.loads(treatment_path.read_text(encoding="utf-8"))
    narration_value = treatment.get("script_gate", {}).get("narration_path")
    narration_path = checked_repo_path(narration_value) if isinstance(narration_value, str) else None
    if narration_path is None:
        raise ValueError("treatment script gate does not name a canonical narration")
    from audit_video_plan import audit_treatment
    treatment_errors, _, _ = audit_treatment(
        treatment, narration_path.read_text(encoding="utf-8"), repository_check=True
    )
    if treatment_errors:
        raise RuntimeError(
            "treatment and script gate failed before render:\n - "
            + "\n - ".join(treatment_errors)
        )
    report = audit_scene(scene, root=ROOT, treatment_path=treatment_path)
    if report["verdict"] != "pass":
        raise RuntimeError(f"scene source preflight failed with {report['finding_count']} finding(s)")
    if not VENV_PYTHON.is_file():
        raise RuntimeError(f"pinned Manim runtime is missing: {relative(VENV_PYTHON)}")
    media_tools = pinned_media_tools()

    chapter_id = treatment.get("chapter_id")
    if not isinstance(chapter_id, str) or scene.parent.name != "generation-2":
        raise ValueError("scene and treatment must use the canonical generation-2 topology")
    expected_scene = ROOT / f"visual_edition/chapters/{chapter_id}/generation-2/scene.py"
    if scene != expected_scene.resolve() or treatment_path != scene.with_name("treatment.json"):
        raise ValueError("scene and treatment do not match the treatment chapter_id")

    audio_master = checked_repo_path(args.audio_master) if args.audio_master else None
    if audio_master is None:
        raise ValueError(
            "governed draft and release renders require the canonical --audio-master"
        )
    if audio_master is not None:
        expected_audio = (
            ROOT / f"build/visual_edition/audio/{chapter_id}-narration-master.wav"
        ).resolve()
        if audio_master != expected_audio:
            raise ValueError("audio master does not match the canonical chapter identity")
    assets = cleared_assets(treatment)
    receipt_path = checked_repo_path(args.receipt, must_exist=False)
    if receipt_path.suffix != ".json":
        raise ValueError("policy receipt path must end in .json")
    if not str(receipt_path).startswith(str((scene.parent / "receipts").resolve()) + os.sep):
        raise ValueError("policy receipt must live in the chapter generation-2 receipts directory")

    work_root = BUILD_ROOT / "isolated-renders" / chapter_id / args.profile
    media_root = work_root / "media"
    sandbox_home = work_root / "home"
    sandbox_temp = work_root / "tmp"
    for path in (media_root, sandbox_home, sandbox_temp):
        path.mkdir(parents=True, exist_ok=True)
    environment = sanitized_environment(sandbox_home, sandbox_temp)
    read_paths = [
        scene,
        treatment_path,
        CONFIG,
        TOOLCHAIN,
        ROOT / "visual_edition/__init__.py",
        ROOT / "visual_edition/lib/__init__.py",
        ROOT / "visual_edition/lib/asi_visuals.py",
        *assets,
    ]
    if audio_master:
        read_paths.append(audio_master)
    policy_text = build_policy(read_paths)
    policy_path = receipt_path.with_suffix(".sb")
    policy_path.parent.mkdir(parents=True, exist_ok=True)
    policy_path.write_text(policy_text, encoding="utf-8")
    policy_checks = policy_self_test(policy_path, environment, work_root)

    output_name = f"{chapter_id}-visual.mp4"
    manim_argv = manim_command(
        scene, args.scene_class, chapter_id, args.profile, args.seed, media_root
    )
    file_size_bytes = args.max_file_size_mb * 1024 * 1024
    resource_checks = resource_limit_self_test(
        policy_path,
        environment,
        work_root,
        cpu_seconds=args.cpu_seconds,
        file_size_bytes=file_size_bytes,
    )
    render_log = work_root / "manim.log"
    render_started_ns = time.time_ns()
    return_code, render_seconds = run_guarded(
        manim_argv,
        policy_path=policy_path,
        environment=environment,
        log_path=render_log,
        timeout_seconds=args.timeout_seconds,
        cpu_seconds=args.cpu_seconds,
        file_size_bytes=file_size_bytes,
    )
    if return_code != 0:
        detail = render_log.read_text(encoding="utf-8", errors="replace")[-3000:]
        raise RuntimeError(f"isolated Manim render failed with exit {return_code}:\n{detail}")
    visual_output = find_rendered_video(media_root, output_name)
    if visual_output.stat().st_mtime_ns < render_started_ns:
        raise RuntimeError("Manim returned success without producing a fresh visual track")

    steps = [{
        "phase": "scene_render",
        "command_argv": manim_argv,
        "exit_code": return_code,
        "wall_seconds": render_seconds,
    }]
    outputs = [{
        "role": "visual_track",
        "path": relative(visual_output),
        "sha256": sha256(visual_output),
        "size_bytes": visual_output.stat().st_size,
    }]
    if audio_master is not None:
        ffmpeg = media_tools["ffmpeg"]["path"]
        final_output = (
            BUILD_ROOT / "generation-2/final" / f"{chapter_id}.mp4"
            if args.profile == "release"
            else work_root / f"{chapter_id}-animatic.mp4"
        )
        final_output.parent.mkdir(parents=True, exist_ok=True)
        pending_output = pending_mux_output(final_output, args.profile)
        pending_output.unlink(missing_ok=True)
        mux_argv = mux_command(
            ffmpeg, visual_output, audio_master, pending_output, args.profile
        )
        mux_log = work_root / "ffmpeg.log"
        mux_code, mux_seconds = run_guarded(
            mux_argv,
            policy_path=policy_path,
            environment=environment,
            log_path=mux_log,
            timeout_seconds=args.timeout_seconds,
            cpu_seconds=args.cpu_seconds,
            file_size_bytes=file_size_bytes,
        )
        if mux_code != 0:
            detail = mux_log.read_text(encoding="utf-8", errors="replace")[-3000:]
            raise RuntimeError(f"isolated ffmpeg mux failed with exit {mux_code}:\n{detail}")
        pending_output.replace(final_output)
        steps.append({
            "phase": "audio_mux",
            "command_argv": mux_argv,
            "exit_code": mux_code,
            "wall_seconds": mux_seconds,
        })
        outputs.append({
            "role": "muxed_master",
            "path": relative(final_output),
            "sha256": sha256(final_output),
            "size_bytes": final_output.stat().st_size,
        })

    toolchain = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    value = {
        "schema_version": "asi_stack.manim_sandbox_policy_receipt.v1",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "chapter_id": chapter_id,
        "profile": args.profile,
        "isolation_mode": "macos_sandbox_exec",
        "runner": {"path": relative(RUNNER), "sha256": sha256(RUNNER)},
        "policy": {"path": relative(policy_path), "sha256": sha256(policy_path)},
        "scene": {"path": relative(scene), "sha256": sha256(scene)},
        "treatment": {"path": relative(treatment_path), "sha256": sha256(treatment_path)},
        "audio_master": (
            {"path": relative(audio_master), "sha256": sha256(audio_master)}
            if audio_master else None
        ),
        "toolchain_id": toolchain["toolchain_id"],
        "media_tools": media_tools,
        "network_access": False,
        "credential_environment_inherited": False,
        "repository_writable_roots": ["build/visual_edition"],
        "filesystem_read_scope": {
            "global_metadata_lookup": True,
            "unlisted_repository_content_access": False,
            "repository_content_mode": "explicit_inputs_plus_build",
            "system_content_roots": [
                str(path) for path in SYSTEM_READ_ROOTS if path.exists()
            ],
            "rationale": (
                "The macOS Python launcher and native dependencies require the "
                "listed system content roots plus global metadata; unlisted "
                "repository file contents remain denied."
            ),
        },
        "resource_limits": {
            "wall_seconds": args.timeout_seconds,
            "cpu_seconds": args.cpu_seconds,
            "max_file_size_bytes": file_size_bytes,
            "max_open_files": 256,
            "max_processes": MAX_PROCESSES,
            "max_resident_memory_bytes": None,
            "memory_limit_status": MEMORY_LIMIT_STATUS,
            "core_dump_bytes": 0,
        },
        "policy_self_test": policy_checks,
        "resource_limit_self_test": resource_checks,
        "source_preflight": {
            "verdict": report["verdict"],
            "finding_count": report["finding_count"],
            "scene_sha256": report["scene_sha256"],
            "auditor": {
                "path": "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
                "sha256": sha256(RUNNER.with_name("audit_scene_source.py")),
            },
        },
        "render_steps": steps,
        "outputs": outputs,
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": "This receipt records one constrained execution and does not prove scene safety, teaching effectiveness, chapter truth, or publication authority.",
    }
    receipt_schema = json.loads(
        (ROOT / "schemas/manim_sandbox_policy_receipt.schema.json").read_text(encoding="utf-8")
    )
    schema_errors = sorted(
        Draft202012Validator(receipt_schema).iter_errors(value),
        key=lambda error: tuple(map(str, error.path)),
    )
    if schema_errors:
        details = [
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in schema_errors
        ]
        raise RuntimeError("runner generated an invalid policy receipt:\n - " + "\n - ".join(details))
    write_receipt(receipt_path, value)
    return value


def self_test() -> list[str]:
    failures: list[str] = []
    if platform.system() != "Darwin" or not SANDBOX_EXEC.is_file() or not VENV_PYTHON.is_file():
        return ["macOS sandbox-exec and the pinned visual runtime are required"]
    with tempfile.TemporaryDirectory(dir=BUILD_ROOT) as temporary:
        work_root = Path(temporary)
        home = work_root / "home"
        temp = work_root / "tmp"
        home.mkdir()
        temp.mkdir()
        environment = sanitized_environment(home, temp)
        policy = work_root / "policy.sb"
        policy_text = build_policy([VENV_PYTHON])
        policy.write_text(policy_text, encoding="utf-8")
        for forbidden_root in ("/Library", "/private/etc", "/private/var/db"):
            if f'(allow file-read* (subpath "{forbidden_root}"))' in policy_text:
                failures.append(f"sandbox policy restored broad content access to {forbidden_root}")
        if "(allow file-read-metadata)" not in policy_text:
            failures.append("sandbox policy does not disclose its required global metadata lookup")
        try:
            results = policy_self_test(policy, environment, work_root)
        except Exception as exc:
            failures.append(str(exc))
        else:
            if set(results.values()) != {"pass"}:
                failures.append(f"policy controls did not all pass: {results}")
        try:
            results = resource_limit_self_test(
                policy,
                environment,
                work_root,
                cpu_seconds=90,
                file_size_bytes=100 * 1024 * 1024,
            )
        except Exception as exc:
            failures.append(str(exc))
        else:
            expected_resource_results = {
                "core_dump_bytes": "pass",
                "cpu_seconds": "pass",
                "max_file_size_bytes": "pass",
                "max_open_files": "pass",
                "max_processes": "pass",
                "memory_bound": MEMORY_LIMIT_STATUS,
            }
            if results != expected_resource_results:
                failures.append(f"resource controls did not all pass: {results}")
        helper = ROOT / "visual_edition/lib/asi_visuals.py"
        policy.write_text(
            build_policy(
                [
                    ROOT / "visual_edition/__init__.py",
                    ROOT / "visual_edition/lib/__init__.py",
                    helper,
                ]
            ),
            encoding="utf-8",
        )
        helper_log = work_root / "shared-helper-import.log"
        try:
            code, _ = run_guarded(
                [
                    str(VENV_PYTHON),
                    "-c",
                    "from visual_edition.lib.asi_visuals import AsiScene; print(AsiScene.__name__)",
                ],
                policy_path=policy,
                environment=environment,
                log_path=helper_log,
                timeout_seconds=30,
                cpu_seconds=30,
                file_size_bytes=10 * 1024 * 1024,
            )
            helper_output = helper_log.read_text(encoding="utf-8", errors="replace").strip()
            if code != 0 or helper_output != "AsiScene":
                failures.append(
                    f"isolated shared-helper import failed with exit {code}: {helper_output[-500:]}"
                )
        except Exception as exc:
            failures.append(f"isolated shared-helper import failed: {exc}")
        scene = work_root / "sandbox_smoke.py"
        scene.write_text(
            "from manim import Circle, Scene\n\n"
            "class SandboxSmoke(Scene):\n"
            "    def construct(self):\n"
            "        self.add(Circle())\n"
            "        self.wait(0.2)\n",
            encoding="utf-8",
        )
        report = audit_scene(scene, root=ROOT)
        if report["verdict"] != "pass":
            failures.append("sandbox smoke scene failed static preflight")
        media_root = work_root / "media"
        policy.write_text(build_policy([scene, CONFIG, TOOLCHAIN]), encoding="utf-8")
        manim_argv = [
            str(VENV_PYTHON), "-m", "manim", "render",
            "--config_file", str(CONFIG), "--renderer", "cairo",
            "--format", "mp4", "--resolution", "160,90", "--fps", "5",
            "--seed", "0", "--disable_caching", "--progress_bar", "none",
            "--media_dir", str(media_root), "--output_file", "sandbox-smoke.mp4",
            str(scene), "SandboxSmoke",
        ]
        try:
            code, _ = run_guarded(
                manim_argv,
                policy_path=policy,
                environment=environment,
                log_path=work_root / "manim-smoke.log",
                timeout_seconds=90,
                cpu_seconds=90,
                file_size_bytes=100 * 1024 * 1024,
            )
            if code != 0:
                detail = (work_root / "manim-smoke.log").read_text(
                    encoding="utf-8", errors="replace"
                )[-1200:]
                failures.append(f"isolated Manim smoke render exited {code}: {detail}")
                visual = None
            else:
                visual = find_rendered_video(media_root, "sandbox-smoke.mp4")
        except Exception as exc:
            failures.append(f"isolated Manim smoke render failed: {exc}")
            visual = None
        try:
            ffmpeg = pinned_media_tools()["ffmpeg"]["path"]
        except RuntimeError as exc:
            failures.append(str(exc))
            ffmpeg = None
        if visual is not None and ffmpeg:
            muxed = work_root / "sandbox-smoke-muxed.mp4"
            mux_argv = [
                ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", str(visual),
                "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "0.2",
                "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-r", "5", "-c:a", "aac", "-ar", "48000",
                "-movflags", "+faststart", str(muxed),
            ]
            try:
                code, _ = run_guarded(
                    mux_argv,
                    policy_path=policy,
                    environment=environment,
                    log_path=work_root / "ffmpeg-smoke.log",
                    timeout_seconds=90,
                    cpu_seconds=90,
                    file_size_bytes=100 * 1024 * 1024,
                )
                if code != 0 or not muxed.is_file() or muxed.stat().st_size == 0:
                    failures.append(f"isolated FFmpeg smoke mux exited {code} without output")
            except Exception as exc:
                failures.append(f"isolated FFmpeg smoke mux failed: {exc}")
        elif visual is not None:
            failures.append("pinned FFmpeg is unavailable for isolated mux smoke test")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", nargs="?", type=Path)
    parser.add_argument("scene_class", nargs="?")
    parser.add_argument("--treatment", type=Path)
    parser.add_argument("--audio-master", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--profile", choices=("draft", "release"), default="draft")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--cpu-seconds", type=int, default=1800)
    parser.add_argument("--max-file-size-mb", type=int, default=4096)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        failures = self_test()
        if failures:
            raise SystemExit("Isolated-render self-test failed:\n - " + "\n - ".join(failures))
        print("Self-test passed: policy denials plus isolated Manim render and FFmpeg mux succeeded.")
        return
    if not all(
        (args.scene, args.scene_class, args.treatment, args.audio_master, args.receipt)
    ):
        parser.error(
            "scene, scene_class, --treatment, --audio-master, and --receipt are required"
        )
    if args.seed < 0 or min(args.timeout_seconds, args.cpu_seconds, args.max_file_size_mb) <= 0:
        parser.error("seed must be nonnegative and resource limits must be positive")
    try:
        value = render(args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Isolated render failed: {exc}") from exc
    print(
        f"Isolated {value['profile']} render passed for {value['chapter_id']}: "
        f"{len(value['render_steps'])} step(s), {len(value['outputs'])} output(s)."
    )


if __name__ == "__main__":
    main()
