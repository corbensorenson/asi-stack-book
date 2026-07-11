#!/usr/bin/env python3
"""Independent subprocess observer for the post-v2 governed-work corpus."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path


SAFE_BUILTINS = {
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "range": range,
    "reversed": reversed,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}
FORBIDDEN_CALLS = {"eval", "exec", "open", "compile", "__import__", "globals", "locals", "input"}


def static_errors(source: str, function_name: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"syntax_error:{exc.msg}"]
    errors: list[str] = []
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if [node.name for node in functions] != [function_name]:
        errors.append("candidate_must_define_exactly_the_requested_function")
    allowed_top = (ast.FunctionDef, ast.AsyncFunctionDef)
    for node in tree.body:
        if isinstance(node, allowed_top):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        errors.append(f"forbidden_top_level:{type(node).__name__}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.ClassDef, ast.AsyncFunctionDef)):
            errors.append(f"forbidden_node:{type(node).__name__}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            errors.append("forbidden_dunder_attribute")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            errors.append("forbidden_dunder_name")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            errors.append(f"forbidden_call:{node.func.id}")
    return sorted(set(errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--suite", choices=("visible", "hidden"), required=True)
    args = parser.parse_args()

    corpus = json.loads(args.tasks.read_text(encoding="utf-8"))
    task = next(row for row in corpus["tasks"] if row["task_id"] == args.task_id)
    source = args.candidate.read_text(encoding="utf-8")
    errors = static_errors(source, task["function_name"])
    observations: list[dict] = []
    if not errors:
        namespace = {"__builtins__": SAFE_BUILTINS}
        try:
            exec(compile(source, args.candidate.as_posix(), "exec"), namespace, namespace)
            for index, expression in enumerate(task[f"{args.suite}_tests"], start=1):
                try:
                    passed = eval(expression, namespace, namespace) is True
                    observations.append({"probe": index, "passed": passed, "error": None})
                except Exception as exc:  # observer records the class, not an unstable traceback
                    observations.append({"probe": index, "passed": False, "error": type(exc).__name__})
        except Exception as exc:
            errors.append(f"candidate_load_error:{type(exc).__name__}")
    passed = not errors and bool(observations) and all(row["passed"] for row in observations)
    payload = {
        "observer_id": "post-v2-independent-subprocess-observer-v0",
        "task_id": args.task_id,
        "suite": args.suite,
        "candidate_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "passed": passed,
        "static_errors": errors,
        "observations": observations,
    }
    payload["observation_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
