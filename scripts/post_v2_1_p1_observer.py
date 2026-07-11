#!/usr/bin/env python3
"""Separate candidate/effect observer for the post-v2.1 P1 program."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import stat
from pathlib import Path


SAFE_BUILTINS = {
    "abs": abs, "bool": bool, "float": float, "int": int, "len": len,
    "max": max, "min": min, "round": round, "str": str, "sum": sum,
}
FORBIDDEN_NODES = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.ClassDef, ast.AsyncFunctionDef)
FORBIDDEN_CALLS = {"eval", "exec", "open", "compile", "__import__", "globals", "locals", "input"}


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def static_errors(source: str, function_name: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"syntax_error:{exc.msg}"]
    errors: list[str] = []
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if [node.name for node in functions] != [function_name]:
        errors.append("candidate_must_define_exactly_requested_function")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        errors.append(f"forbidden_top_level:{type(node).__name__}")
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            errors.append(f"forbidden_node:{type(node).__name__}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            errors.append("forbidden_dunder_attribute")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            errors.append("forbidden_dunder_name")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            errors.append(f"forbidden_call:{node.func.id}")
    return sorted(set(errors))


def observe_candidate(corpus: Path, candidate: Path, task_id: str, suite: str) -> dict:
    task = next(row for row in json.loads(corpus.read_text())["tasks"] if row["task_id"] == task_id)
    source = candidate.read_text(encoding="utf-8")
    errors = static_errors(source, task["function_name"])
    observations = []
    if not errors:
        namespace = {"__builtins__": SAFE_BUILTINS}
        try:
            exec(compile(source, candidate.as_posix(), "exec"), namespace, namespace)
            function = namespace[task["function_name"]]
            cases = task["visible_cases"] if suite == "visible" else task["observer_only_cases"]
            for index, (argument, expected) in enumerate(cases, start=1):
                try:
                    actual = function(argument)
                    observations.append({"probe": index, "passed": actual == expected, "actual": actual, "expected": expected, "error": None})
                except Exception as exc:
                    observations.append({"probe": index, "passed": False, "actual": None, "expected": expected, "error": type(exc).__name__})
        except Exception as exc:
            errors.append(f"candidate_load_error:{type(exc).__name__}")
    payload = {
        "observer_id": "post-v2-1-p1-separate-observer-v0",
        "task_id": task_id,
        "suite": suite,
        "candidate_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "passed": not errors and bool(observations) and all(row["passed"] for row in observations),
        "static_errors": errors,
        "observations": observations,
    }
    payload["observation_sha256"] = canonical_sha(payload)
    return payload


def observe_inventory(root: Path) -> dict:
    rows = []
    for path in sorted(root.rglob("*"), key=lambda value: value.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        if path.is_symlink():
            row = {"path": relative, "type": "symlink", "target": os.readlink(path), "mode": stat.S_IMODE(metadata.st_mode)}
        elif path.is_file():
            row = {"path": relative, "type": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "size": metadata.st_size, "mode": stat.S_IMODE(metadata.st_mode)}
        elif path.is_dir():
            row = {"path": relative, "type": "directory", "mode": stat.S_IMODE(metadata.st_mode)}
        else:
            row = {"path": relative, "type": "other", "mode": stat.S_IMODE(metadata.st_mode)}
        rows.append(row)
    payload = {"observer_id": "post-v2-1-p1-separate-observer-v0", "root_name": root.name, "entries": rows}
    payload["inventory_sha256"] = canonical_sha(rows)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    candidate = subparsers.add_parser("candidate")
    candidate.add_argument("--corpus", type=Path, required=True)
    candidate.add_argument("--candidate", type=Path, required=True)
    candidate.add_argument("--task-id", required=True)
    candidate.add_argument("--suite", choices=("visible", "hidden"), required=True)
    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    payload = observe_candidate(args.corpus, args.candidate, args.task_id, args.suite) if args.mode == "candidate" else observe_inventory(args.root)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
