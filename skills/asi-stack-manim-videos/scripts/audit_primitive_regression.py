#!/usr/bin/env python3
"""Render and compare content-addressed ASI Stack primitive reference frames."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import socket
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


def discover_repository_root() -> Path:
    configured = os.environ.get("ASI_STACK_BOOK_ROOT")
    candidates = [] if not configured else [Path(configured)]
    candidates.extend((Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents))
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
MANIFEST = ROOT / "visual_edition/primitive_regression_manifest.json"
SCHEMA = ROOT / "schemas/manim_primitive_regression.schema.json"
ABSOLUTE_TOLERANCE = 1.01
MISMATCH_RATIO_TOLERANCE = 1e-5
CREDENTIAL_MARKERS = (
    "API_KEY", "AUTH", "BEARER", "CREDENTIAL", "GITHUB_TOKEN", "KEYCHAIN",
    "PASSWORD", "PRIVATE_KEY", "SECRET", "SESSION", "SSH_", "TOKEN",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_repo_path(value: str) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return module


def public_factory_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    }


def referenced_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def regression_source_errors(manifest: dict[str, Any]) -> list[str]:
    scene_path = safe_repo_path(manifest.get("regression_scenes", {}).get("path", ""))
    if scene_path is None or not scene_path.is_file():
        return ["regression scene path is missing or escapes the repository"]
    auditor = load_module(
        ROOT / "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
        "asi_stack_primitive_scene_source_auditor",
    )
    report = auditor.audit_scene(scene_path, root=ROOT)
    return [
        f"regression-scene-source:{row.get('code')}:{row.get('line')}: {row.get('message')}"
        for row in report.get("findings", [])
    ]


def assert_isolated_worker(output: Path) -> None:
    if os.environ.get("ASI_STACK_PRIMITIVE_WORKER") != "1":
        raise RuntimeError("primitive render worker lacks its isolated-parent marker")
    if any(
        any(marker in key.upper() for marker in CREDENTIAL_MARKERS)
        for key in os.environ
    ):
        raise RuntimeError("primitive render worker inherited credential-like environment")
    try:
        output.resolve().relative_to((ROOT / "build/visual_edition").resolve())
    except ValueError as exc:
        raise RuntimeError("primitive render output escapes the governed build root") from exc
    denied_write = ROOT / ".asi-primitive-worker-denied"
    try:
        denied_write.write_text("denied", encoding="utf-8")
    except PermissionError:
        pass
    else:
        denied_write.unlink(missing_ok=True)
        raise RuntimeError("primitive render worker can write outside the build root")
    try:
        (ROOT / "book_structure.json").read_bytes()
    except PermissionError:
        pass
    else:
        raise RuntimeError("primitive render worker can read unlisted repository content")
    connection = socket.socket()
    connection.settimeout(0.2)
    try:
        connection.connect(("127.0.0.1", 9))
    except PermissionError:
        pass
    except OSError as exc:
        raise RuntimeError(
            f"primitive render worker network denial is not OS-enforced: {type(exc).__name__}"
        ) from exc
    else:
        raise RuntimeError("primitive render worker unexpectedly opened a network connection")
    finally:
        connection.close()


def manifest_errors(manifest: dict[str, Any]) -> list[str]:
    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(manifest)
    ]
    expected_paths = {
        "toolchain": ROOT / "visual_edition/toolchain.json",
        "visual_grammar": ROOT / "visual_edition/visual_grammar.json",
        "primitive_library": ROOT / "visual_edition/lib/asi_visuals.py",
        "regression_scenes": ROOT / "visual_edition/tests/primitive_regression_scenes.py",
    }
    for name, expected_path in expected_paths.items():
        binding = manifest.get(name, {})
        path = safe_repo_path(binding.get("path", "")) if isinstance(binding, dict) else None
        if path != expected_path.resolve():
            errors.append(f"{name} binds the wrong path")
        elif not path.is_file() or binding.get("sha256") != digest(path):
            errors.append(f"{name} digest drift")

    baseline = manifest.get("baseline", {})
    baseline_path = safe_repo_path(baseline.get("path", "")) if isinstance(baseline, dict) else None
    if baseline_path is None or not baseline_path.is_file():
        errors.append("primitive baseline is missing")
    elif baseline.get("sha256") != digest(baseline_path):
        errors.append("primitive baseline digest drift")

    library_path = expected_paths["primitive_library"]
    scene_path = expected_paths["regression_scenes"]
    public = public_factory_symbols(library_path)
    declared = set(manifest.get("covered_factory_symbols", []))
    if declared != public:
        errors.append(
            "covered_factory_symbols must exactly equal the public primitive factories: "
            + ", ".join(sorted(public))
        )
    missing_references = public - referenced_names(scene_path)
    if missing_references:
        errors.append(
            "regression scenes do not exercise public factories: "
            + ", ".join(sorted(missing_references))
        )
    return errors


def baseline_array_errors(
    baseline: np.ndarray,
    manifest: dict[str, Any],
) -> list[str]:
    contract = manifest.get("frame_contract", {})
    baseline_contract = manifest.get("baseline", {})
    expected_shape = (
        baseline_contract.get("frame_count"),
        contract.get("pixel_height"),
        contract.get("pixel_width"),
        contract.get("channels"),
    )
    errors: list[str] = []
    if baseline.shape != expected_shape:
        errors.append(
            f"reviewed baseline shape {baseline.shape} does not match {expected_shape}"
        )
    if baseline.dtype != np.uint8:
        errors.append(
            f"reviewed baseline dtype {baseline.dtype} must be uint8"
        )
    return errors


def static_audit_errors(manifest_path: Path = MANIFEST) -> list[str]:
    """Validate portable regression custody without claiming a render replay."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = manifest_errors(manifest)
    errors.extend(regression_source_errors(manifest))
    baseline_path = safe_repo_path(manifest.get("baseline", {}).get("path", ""))
    if baseline_path is None or not baseline_path.is_file():
        return errors
    try:
        with np.load(baseline_path) as data:
            if set(data.files) != {"frame_data"}:
                errors.append("reviewed baseline must contain only frame_data")
            elif "frame_data" in data:
                errors.extend(baseline_array_errors(data["frame_data"], manifest))
    except (OSError, ValueError) as exc:
        errors.append(f"reviewed baseline cannot be loaded safely: {exc}")
    return errors


def render_frames_in_current_runtime(manifest: dict[str, Any]) -> np.ndarray:
    from manim import tempconfig
    from manim.renderer.cairo_renderer import CairoRenderer

    scene_path = safe_repo_path(manifest["regression_scenes"]["path"])
    if scene_path is None:
        raise RuntimeError("regression scene path escapes the repository")
    module = load_module(scene_path, "asi_stack_primitive_regression_scenes")
    frame_contract = manifest["frame_contract"]
    frames: list[np.ndarray] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        config = {
            "renderer": "cairo",
            "pixel_width": frame_contract["pixel_width"],
            "pixel_height": frame_contract["pixel_height"],
            "frame_rate": 1,
            "background_color": frame_contract["background_color"],
            "dry_run": True,
            "write_to_movie": False,
            "disable_caching": True,
            "media_dir": temp_dir,
            "text_dir": temp_dir,
            "tex_dir": temp_dir,
        }
        with tempconfig(config):
            for class_name in manifest["scene_classes"]:
                scene_class = getattr(module, class_name)
                renderer = CairoRenderer()
                scene = scene_class(renderer=renderer, skip_animations=True)
                scene.render()
                frames.append(np.asarray(renderer.get_frame(), dtype=np.uint8).copy())
    return np.stack(frames)


def render_frames(
    manifest: dict[str, Any],
    *,
    manifest_path: Path = MANIFEST,
) -> np.ndarray:
    source_errors = regression_source_errors(manifest)
    if source_errors:
        raise RuntimeError("; ".join(source_errors))
    toolchain_path = safe_repo_path(manifest["toolchain"]["path"])
    if toolchain_path is None:
        raise RuntimeError("toolchain path escapes the repository")
    toolchain = json.loads(toolchain_path.read_text(encoding="utf-8"))
    python_relative = Path(toolchain["python"]["canonical_relative_path"])
    python_path = ROOT / python_relative
    if python_relative.is_absolute() or ".." in python_relative.parts or not python_path.is_file():
        raise RuntimeError("pinned Manim Python runtime is missing")
    runner = load_module(
        ROOT / "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py",
        "asi_stack_primitive_isolated_runner",
    )
    if not runner.SANDBOX_EXEC.is_file():
        raise RuntimeError("primitive regression requires the pinned macOS sandbox adapter")
    runner.BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=runner.BUILD_ROOT) as temp_dir:
        work_root = Path(temp_dir)
        output = work_root / "frames.npz"
        home = work_root / "home"
        temporary = work_root / "tmp"
        home.mkdir()
        temporary.mkdir()
        environment = runner.sanitized_environment(home, temporary)
        environment["ASI_STACK_PRIMITIVE_WORKER"] = "1"
        read_paths = [
            Path(__file__).resolve(),
            manifest_path.resolve(),
            SCHEMA.resolve(),
            ROOT / "visual_edition/__init__.py",
            ROOT / "visual_edition/lib/__init__.py",
        ]
        for name in (
            "toolchain", "visual_grammar", "primitive_library",
            "regression_scenes", "baseline",
        ):
            path = safe_repo_path(manifest.get(name, {}).get("path", ""))
            if path is not None:
                read_paths.append(path)
        policy = work_root / "primitive-regression.sb"
        policy.write_text(runner.build_policy(read_paths), encoding="utf-8")
        runner.policy_self_test(policy, environment, work_root)
        runner.resource_limit_self_test(
            policy,
            environment,
            work_root,
            cpu_seconds=300,
            file_size_bytes=256 * 1024 * 1024,
        )
        command = [
            str(python_path),
            str(Path(__file__).resolve()),
            "--manifest",
            str(manifest_path.resolve()),
            "--render-worker",
            str(output),
        ]
        code, _ = runner.run_guarded(
            command,
            policy_path=policy,
            environment=environment,
            log_path=work_root / "primitive-regression.log",
            timeout_seconds=300,
            cpu_seconds=300,
            file_size_bytes=256 * 1024 * 1024,
        )
        if code != 0 or not output.is_file():
            detail = (work_root / "primitive-regression.log").read_text(
                encoding="utf-8", errors="replace"
            )[-3000:]
            raise RuntimeError(
                f"isolated primitive render worker failed with exit {code}:\n{detail}"
            )
        with np.load(output) as data:
            return data["frame_data"].copy()


def audit_regression(manifest_path: Path = MANIFEST) -> list[str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = static_audit_errors(manifest_path)
    if errors:
        return errors
    candidate = render_frames(manifest, manifest_path=manifest_path)
    baseline_path = safe_repo_path(manifest["baseline"]["path"])
    if baseline_path is None:
        return ["primitive baseline path escapes the repository"]
    with np.load(baseline_path) as data:
        baseline = data["frame_data"]
    return comparison_errors(candidate, baseline)


def comparison_errors(candidate: np.ndarray, baseline: np.ndarray) -> list[str]:
    if candidate.shape != baseline.shape:
        return [f"frame shape drift: candidate {candidate.shape}, baseline {baseline.shape}"]
    close = np.isclose(candidate, baseline, atol=ABSOLUTE_TOLERANCE)
    errors: list[str] = []
    for index in range(candidate.shape[0]):
        mismatch_ratio = 1.0 - float(close[index].sum()) / float(close[index].size)
        if mismatch_ratio >= MISMATCH_RATIO_TOLERANCE:
            errors.append(
                f"frame {index} mismatch ratio {mismatch_ratio:.8f} exceeds "
                f"{MISMATCH_RATIO_TOLERANCE:.8f}"
            )
    return errors


def save_contact_sheet(frames: np.ndarray, path: Path) -> None:
    images = [Image.fromarray(frame, mode="RGBA").convert("RGB") for frame in frames]
    sheet = Image.new("RGB", (images[0].width, images[0].height * len(images)), "black")
    for index, frame in enumerate(images):
        sheet.paste(frame, (0, index * frame.height))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def self_test() -> list[str]:
    failures: list[str] = []
    try:
        auditor = load_module(
            ROOT / "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
            "asi_stack_primitive_loader_self_test",
        )
        if auditor.Finding.__module__ != "asi_stack_primitive_loader_self_test":
            failures.append("dynamic auditor module identity was not preserved")
    except Exception as exc:
        failures.append(f"dynamic auditor module loading failed: {exc}")
    baseline = np.zeros((2, 12, 12, 4), dtype=np.uint8)
    if comparison_errors(baseline.copy(), baseline):
        failures.append("identical frames did not compare equal")
    mutation = baseline.copy()
    mutation[0, :, :, :] = 255
    if not comparison_errors(mutation, baseline):
        failures.append("material frame mutation was not rejected")
    shape_mutation = np.zeros((1, 12, 12, 4), dtype=np.uint8)
    if not comparison_errors(shape_mutation, baseline):
        failures.append("frame-count mutation was not rejected")
    contract = {
        "frame_contract": {
            "pixel_height": 12,
            "pixel_width": 12,
            "channels": 4,
        },
        "baseline": {"frame_count": 2},
    }
    if baseline_array_errors(baseline, contract):
        failures.append("valid baseline array contract was rejected")
    if not baseline_array_errors(shape_mutation, contract):
        failures.append("static baseline shape mutation was not rejected")
    dtype_mutation = baseline.astype(np.float32)
    if not baseline_array_errors(dtype_mutation, contract):
        failures.append("static baseline dtype mutation was not rejected")
    try:
        assert_isolated_worker(ROOT / "build/visual_edition/worker-bypass.npz")
    except RuntimeError as exc:
        if "isolated-parent marker" not in str(exc):
            failures.append(f"worker bypass failed for the wrong reason: {exc}")
    else:
        failures.append("direct primitive worker bypass was not rejected")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--capture-candidate", type=Path)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--render-worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Validate portable baseline custody without replaying the macOS render",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.render_worker:
        assert_isolated_worker(args.render_worker)
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        frames = render_frames_in_current_runtime(manifest)
        args.render_worker.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.render_worker, frame_data=frames)
        return
    if args.self_test:
        failures = self_test()
        if failures:
            raise SystemExit("Primitive-regression self-test failed:\n - " + "\n - ".join(failures))
        print(
            "Self-test passed: identical positive fixture and "
            f"{NEGATIVE_CONTROL_COUNT} rejecting controls behave correctly."
        )
        return

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = static_audit_errors(args.manifest)
    source_errors = [error for error in errors if error.startswith("regression-scene-source:")]
    if source_errors:
        raise SystemExit("Primitive regression source preflight failed:\n - " + "\n - ".join(source_errors))
    if errors and not args.capture_candidate:
        raise SystemExit("Primitive-regression manifest failed:\n - " + "\n - ".join(errors))
    if args.static_only:
        if args.capture_candidate or args.contact_sheet:
            raise SystemExit("--static-only cannot capture candidate frames")
        print(
            "Primitive regression custody passed: reviewed baseline identity, frame "
            "contract, source preflight, and public-factory coverage; no render replay claimed."
        )
        return
    candidate = render_frames(manifest, manifest_path=args.manifest)
    if args.capture_candidate:
        args.capture_candidate.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.capture_candidate, frame_data=candidate)
        if args.contact_sheet:
            save_contact_sheet(candidate, args.contact_sheet)
        print(
            f"Captured {candidate.shape[0]} candidate frames; inspect them before updating "
            "the reviewed baseline manifest."
        )
        return

    baseline_path = safe_repo_path(manifest["baseline"]["path"])
    if baseline_path is None:
        raise SystemExit("Primitive baseline path escapes the repository")
    with np.load(baseline_path) as data:
        baseline = data["frame_data"]
    errors.extend(comparison_errors(candidate, baseline))
    if errors:
        raise SystemExit("Primitive graphical regression failed:\n - " + "\n - ".join(errors))
    print(
        f"Primitive graphical regression passed: {candidate.shape[0]} reviewed frames, "
        f"{len(manifest['covered_factory_symbols'])} public factories."
    )


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
