#!/usr/bin/env python3
"""Fail-closed static preflight for ASI Stack Manim scene source.

This catches unsafe or nondeterministic source patterns before a scene is
executed. It is deliberately not described as a sandbox: reviewed source must
still run with network denied, secrets absent, and write access constrained.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
NEGATIVE_CONTROL_COUNT = 10
ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "collections",
    "dataclasses",
    "decimal",
    "enum",
    "fractions",
    "functools",
    "itertools",
    "manim",
    "math",
    "numpy",
    "statistics",
    "typing",
    "visual_edition",
}
ALLOWED_LOCAL_MODULES = {"visual_edition.lib.asi_visuals"}
FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "asyncio",
    "ctypes",
    "ftplib",
    "http",
    "importlib",
    "marshal",
    "multiprocessing",
    "os",
    "pathlib",
    "pickle",
    "requests",
    "runpy",
    "shutil",
    "socket",
    "subprocess",
    "sys",
    "tempfile",
    "urllib",
    "webbrowser",
}
FORBIDDEN_CALL_NAMES = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "input",
    "locals",
    "open",
    "setattr",
    "vars",
}
FORBIDDEN_TERMINAL_ATTRIBUTES = {
    "connect",
    "dump",
    "dumps",
    "fromfile",
    "load",
    "loads",
    "memmap",
    "open",
    "popen",
    "run",
    "save",
    "savez",
    "savez_compressed",
    "savetxt",
    "system",
    "tofile",
    "urlopen",
}
ASSET_CONSTRUCTORS = {
    "ImageMobject",
    "OpenGLImageMobject",
    "SVGMobject",
}
LATEX_CONSTRUCTORS = {"MathTex", "SingleStringMathTex", "Tex", "TexTemplate"}
FORBIDDEN_ACCESSIBILITY_EFFECTS = {"Flash", "ShowPassingFlash"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dotted_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    cursor = node
    while isinstance(cursor, ast.Attribute):
        parts.append(cursor.attr)
        cursor = cursor.value
    if isinstance(cursor, ast.Name):
        parts.append(cursor.id)
        return ".".join(reversed(parts))
    return None


def literal_int(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool)


@dataclass(frozen=True)
class Finding:
    code: str
    line: int
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "line": self.line, "message": self.message}


class SceneSourceAuditor(ast.NodeVisitor):
    def __init__(self, *, latex_qualified: bool) -> None:
        self.findings: list[Finding] = []
        self.imports: set[str] = set()
        self.asset_literals: list[tuple[int, str]] = []
        self.random_use_lines: list[int] = []
        self.literal_seed_lines: list[int] = []
        self.scene_class_count = 0
        self.scope_depth = 0
        self.aliases: dict[str, str] = {}
        self.latex_qualified = latex_qualified

    def add(self, code: str, node: ast.AST, message: str) -> None:
        self.findings.append(Finding(code, getattr(node, "lineno", 0), message))

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root = alias.name.split(".", 1)[0]
            self.imports.add(alias.name)
            self.aliases[alias.asname or root] = alias.name
            if root in FORBIDDEN_IMPORT_ROOTS or root not in ALLOWED_IMPORT_ROOTS:
                self.add("unsafe-import", node, f"import {alias.name!r} is outside the scene allowlist")
            if root == "visual_edition" and alias.name not in ALLOWED_LOCAL_MODULES:
                self.add(
                    "unbound-local-import",
                    node,
                    f"local import {alias.name!r} is not the digest-bound primitive library",
                )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level:
            self.add("relative-import", node, "relative imports are not allowed in release scene source")
            return
        module = node.module or ""
        root = module.split(".", 1)[0]
        self.imports.add(module)
        for alias in node.names:
            if alias.name != "*":
                self.aliases[alias.asname or alias.name] = f"{module}.{alias.name}"
        if root in FORBIDDEN_IMPORT_ROOTS or root not in ALLOWED_IMPORT_ROOTS:
            self.add("unsafe-import", node, f"import from {module!r} is outside the scene allowlist")
        if root == "visual_edition" and module not in ALLOWED_LOCAL_MODULES:
            self.add(
                "unbound-local-import",
                node,
                f"local import {module!r} is not the digest-bound primitive library",
            )
        if any(alias.name == "*" for alias in node.names):
            self.add("wildcard-import", node, "wildcard imports hide the executable dependency surface")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = {dotted_name(base) for base in node.bases}
        if any(base and (base.endswith("Scene") or base == "AsiScene") for base in bases):
            self.scene_class_count += 1
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for statement in node.body:
            self.visit(statement)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        for default in [*node.args.defaults, *node.args.kw_defaults]:
            if default is not None:
                self.visit(default)
        self.scope_depth += 1
        for statement in node.body:
            self.visit(statement)
        self.scope_depth -= 1

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__"):
            self.add("dunder-access", node, "dunder attribute access is not allowed in scene source")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in {"__builtins__", "__loader__", "__spec__"}:
            self.add("runtime-introspection", node, f"{node.id} is not allowed in scene source")

    def visit_Call(self, node: ast.Call) -> None:
        name = dotted_name(node.func)
        terminal = name.rsplit(".", 1)[-1] if name else None
        root = name.split(".", 1)[0] if name else None
        resolved_name = (
            name.replace(root, self.aliases[root], 1)
            if name and root in self.aliases
            else name
        )
        resolved_root = resolved_name.split(".", 1)[0] if resolved_name else None
        if self.scope_depth == 0:
            self.add("module-execution", node, "module-scope calls execute before the scene is reviewed")
        if terminal in FORBIDDEN_CALL_NAMES:
            self.add("unsafe-call", node, f"call to {terminal!r} is not allowed in scene source")
        if resolved_root in FORBIDDEN_IMPORT_ROOTS or (
            resolved_root == "numpy" and terminal in FORBIDDEN_TERMINAL_ATTRIBUTES
        ):
            self.add("unsafe-effect", node, f"call to {name or terminal!r} may perform an external effect")

        if name and (".random." in f".{name}." or name.startswith("random.")):
            if terminal == "seed" and node.args and literal_int(node.args[0]):
                self.literal_seed_lines.append(node.lineno)
            elif terminal == "default_rng" and node.args and literal_int(node.args[0]):
                self.literal_seed_lines.append(node.lineno)
            else:
                self.random_use_lines.append(node.lineno)

        if terminal in ASSET_CONSTRUCTORS:
            first = node.args[0] if node.args else None
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                self.asset_literals.append((node.lineno, first.value))
            else:
                self.add(
                    "dynamic-asset-path",
                    node,
                    f"{terminal} requires a repository-relative string literal so provenance can be checked",
                )
        if terminal in LATEX_CONSTRUCTORS and not self.latex_qualified:
            self.add(
                "unqualified-latex",
                node,
                f"{terminal} requires a toolchain with qualified LaTeX and dvisvgm identities",
            )
        if terminal in FORBIDDEN_ACCESSIBILITY_EFFECTS:
            self.add(
                "unqualified-flash-effect",
                node,
                f"{terminal} is blocked until a qualified flash-threshold audit exists",
            )
        self.generic_visit(node)

    def finish(self) -> None:
        if self.random_use_lines and not self.literal_seed_lines:
            self.findings.append(Finding(
                "unseeded-randomness",
                min(self.random_use_lines),
                "randomness is used without a literal deterministic seed",
            ))
        if self.scene_class_count == 0:
            self.findings.append(Finding(
                "missing-scene",
                0,
                "scene source defines no class derived from Scene or AsiScene",
            ))


def cleared_asset_bindings(treatment: dict[str, Any] | None) -> dict[str, str]:
    if not isinstance(treatment, dict):
        return {}
    rows = treatment.get("art_direction", {}).get("asset_plan", [])
    if not isinstance(rows, list):
        return {}
    return {
        row["path_or_source"]: row["sha256"]
        for row in rows
        if isinstance(row, dict)
        and row.get("status") in {"original", "rights_cleared"}
        and row.get("security_review") in {"pass", "not_applicable"}
        and isinstance(row.get("path_or_source"), str)
        and isinstance(row.get("sha256"), str)
    }


def audit_scene(
    scene_path: Path,
    *,
    root: Path = ROOT,
    treatment_path: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    scene_path = scene_path.resolve()
    findings: list[Finding] = []
    try:
        scene_relative = scene_path.relative_to(root).as_posix()
    except ValueError:
        scene_relative = str(scene_path)
        findings.append(Finding("scene-outside-root", 0, "scene source is outside the repository root"))

    try:
        source = scene_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(scene_path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        return {
            "schema_version": "asi_stack.manim_scene_source_audit.v1",
            "scene_path": scene_relative,
            "scene_sha256": digest(scene_path) if scene_path.is_file() else None,
            "treatment_path": None,
            "treatment_sha256": None,
            "imports": [],
            "asset_paths": [],
            "finding_count": 1,
            "findings": [{"code": "unreadable-source", "line": 0, "message": str(exc)}],
            "verdict": "fail",
            "security_boundary": "Static source audit is a preflight, not an execution sandbox.",
        }

    latex_qualified = False
    toolchain_path = root / "visual_edition/toolchain.json"
    if toolchain_path.is_file():
        try:
            native = json.loads(toolchain_path.read_text(encoding="utf-8")).get(
                "native_dependencies", {}
            )
            latex_qualified = (
                native.get("latex") not in {None, "absent"}
                and native.get("dvisvgm") not in {None, "absent"}
            )
        except (OSError, json.JSONDecodeError):
            latex_qualified = False
    auditor = SceneSourceAuditor(latex_qualified=latex_qualified)
    auditor.visit(tree)
    auditor.finish()
    findings.extend(auditor.findings)

    treatment: dict[str, Any] | None = None
    treatment_relative: str | None = None
    treatment_sha: str | None = None
    if treatment_path is None:
        candidate = scene_path.with_name("treatment.json")
        treatment_path = candidate if candidate.is_file() else None
    if treatment_path is not None:
        treatment_path = treatment_path.resolve()
        try:
            treatment_relative = treatment_path.relative_to(root).as_posix()
            treatment = json.loads(treatment_path.read_text(encoding="utf-8"))
            treatment_sha = digest(treatment_path)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("invalid-treatment", 0, f"treatment cannot be verified: {exc}"))

    asset_bindings = cleared_asset_bindings(treatment)
    for line, asset_value in auditor.asset_literals:
        candidate = (root / asset_value).resolve()
        try:
            relative = candidate.relative_to(root).as_posix()
        except ValueError:
            findings.append(Finding("asset-outside-root", line, f"asset {asset_value!r} escapes the repository"))
            continue
        if asset_value != relative:
            findings.append(Finding("noncanonical-asset-path", line, f"asset path must be {relative!r}"))
        if not candidate.is_file():
            findings.append(Finding("missing-asset", line, f"asset {relative!r} does not exist"))
            continue
        expected = asset_bindings.get(relative)
        if expected is None:
            findings.append(Finding("unbound-asset", line, f"asset {relative!r} is not cleared in treatment.json"))
        elif digest(candidate) != expected:
            findings.append(Finding("asset-digest-drift", line, f"asset {relative!r} differs from treatment.json"))

    unique = sorted(
        {(row.code, row.line, row.message): row for row in findings}.values(),
        key=lambda row: (row.line, row.code, row.message),
    )
    return {
        "schema_version": "asi_stack.manim_scene_source_audit.v1",
        "scene_path": scene_relative,
        "scene_sha256": digest(scene_path),
        "treatment_path": treatment_relative,
        "treatment_sha256": treatment_sha,
        "imports": sorted(auditor.imports),
        "asset_paths": [value for _, value in auditor.asset_literals],
        "finding_count": len(unique),
        "findings": [row.as_dict() for row in unique],
        "verdict": "pass" if not unique else "fail",
        "security_boundary": "Static source audit is a preflight, not an execution sandbox.",
    }


def self_test() -> list[str]:
    failures: list[str] = []
    safe = """from manim import Scene, Circle\nfrom math import sin\nclass Demo(Scene):\n    def construct(self):\n        self.add(Circle().shift(sin(0)))\n"""
    mutations = {
        "unsafe import": ("import subprocess\n" + safe, "unsafe-import"),
        "wildcard import": (safe.replace("Scene, Circle", "*"), "wildcard-import"),
        "module call": ("from manim import config\nconfig.digest_args([])\n" + safe, "module-execution"),
        "dynamic execution": (safe.replace("self.add", "eval('self.add') or self.add"), "unsafe-call"),
        "file write": (safe.replace("self.add(Circle().shift(sin(0)))", "open('x', 'w')"), "unsafe-call"),
        "unseeded random": (safe.replace("sin(0)", "np.random.random()"), "unseeded-randomness"),
        "dynamic asset": (safe.replace("Circle().shift(sin(0))", "ImageMobject(asset_path)"), "dynamic-asset-path"),
        "unbound local helper": (
            "from visual_edition.lib.chapter_scene import ChapterScene\n" + safe,
            "unbound-local-import",
        ),
        "unqualified latex": (
            safe.replace("Circle().shift(sin(0))", "MathTex('x')"),
            "unqualified-latex",
        ),
        "unqualified flash effect": (
            safe.replace("Circle().shift(sin(0))", "Flash(ORIGIN)"),
            "unqualified-flash-effect",
        ),
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        scene = root / "scene.py"
        scene.write_text(safe, encoding="utf-8")
        report = audit_scene(scene, root=root)
        if report["verdict"] != "pass":
            failures.append("known-safe scene did not pass")
        scene.write_text(safe.replace("self.add", "self.run()\n        self.add"), encoding="utf-8")
        if audit_scene(scene, root=root)["verdict"] != "pass":
            failures.append("semantic method named run_visual_step caused a false positive")
        for label, (source, expected) in mutations.items():
            scene.write_text(source, encoding="utf-8")
            codes = {row["code"] for row in audit_scene(scene, root=root)["findings"]}
            if expected not in codes:
                failures.append(f"{label} did not trigger {expected}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", nargs="*", type=Path)
    parser.add_argument("--treatment", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        failures = self_test()
        if failures:
            raise SystemExit("Scene-source audit self-test failed:\n - " + "\n - ".join(failures))
        print(
            f"Self-test passed: {NEGATIVE_CONTROL_COUNT} unsafe or unqualified "
            "mutations rejected."
        )
        return
    if not args.scene:
        parser.error("provide at least one scene or use --self-test")
    if args.treatment and len(args.scene) != 1:
        parser.error("--treatment can be used only with one scene")
    reports = [
        audit_scene(path, treatment_path=args.treatment if len(args.scene) == 1 else None)
        for path in args.scene
    ]
    payload: dict[str, Any] | list[dict[str, Any]] = reports[0] if len(reports) == 1 else reports
    body = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    failed = [row["scene_path"] for row in reports if row["verdict"] != "pass"]
    if failed:
        raise SystemExit(f"Scene-source audit failed for {len(failed)} scene(s).")


if __name__ == "__main__":
    main()
