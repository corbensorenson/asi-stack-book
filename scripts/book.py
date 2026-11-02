#!/usr/bin/env python3
"""Concise contributor commands over the existing validation authority."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import shlex
import tempfile

from run_validation_registry import execution_contract, select_units
from validation_projection_plan import plan
from validation_runtime import capability_error, execute, identity
from build_tested_site_bundle import file_rows


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"

# These are reviewed post-render interfaces, not a second publication pipeline.
# The actual commands must still exist, unchanged, in the canonical workflow.
HTML_INTERFACES = {
    "build_human_reader_public_site.py": ["--site", "_site", "--check"],
    "validate_paper_library.py": ["--site", "_site"],
    "validate_product_projections.py": ["--site", "_site"],
    "validate_release_channels.py": ["--site", "_site", "--require-clean"],
    "validate_public_status_consistency.py": ["--site", "_site", "--require-clean"],
    "validate_live_human_view.py": [],
    "validate_live_human_view_browser.js": ["--strict", "--all-chapters", "--all-viewports"],
    "validate_live_human_view_browser_report.py": ["--site", "_site"],
}


def html_plan(root: Path, site: Path, *, local: bool) -> dict:
    if error := capability_error("module:yaml"):
        raise ValueError(error)
    import yaml
    workflow = root / ".github/workflows/build-pages-artifact.yml"
    workflow_bytes = workflow.read_bytes()
    data = yaml.safe_load(workflow_bytes)
    checks = []
    found = set()
    for step in data["jobs"]["build"]["steps"]:
        for line in step.get("run", "").splitlines():
            tokens = shlex.split(line)
            if len(tokens) < 2 or tokens[0] not in {"python3", "node"}:
                continue
            script = Path(tokens[1]).name
            if script == "build_human_reader_public_site.py" and "--check" not in tokens[2:]:
                continue  # The workflow's preceding installer is a producer.
            if script in {"run_validation_registry.py", "validate_tested_site_bundle.py"}:
                continue  # Pre-render source gate / final clean bundle custody.
            if script not in HTML_INTERFACES:
                if script.startswith("validate_"):
                    raise ValueError(f"workflow has an unreviewed HTML check interface: {script}")
                continue
            if "if" in step or step.get("continue-on-error", False):
                raise ValueError(f"required HTML check is conditional or ignores failure: {script}")
            runtime = "node" if script.endswith(".js") else "python3"
            if (script in found or tokens[0] != runtime or tokens[1] != f"scripts/{script}"
                    or tokens[2:] != HTML_INTERFACES[script]):
                raise ValueError(f"HTML interface drifted in canonical workflow: {script}; review the adapter")
            found.add(script)
            args = [str(site) if value == "_site" else value for value in tokens[2:]
                    if not (local and value == "--require-clean")]
            if "--site" not in args:
                args.extend(["--site", str(site)])
            checks.append({"script": script, "workflow_step": step["name"], "args": args,
                           "runtime": runtime, "timeout_seconds": 900 if runtime == "node" else 180,
                           "side_effects": "ignored_outputs" if runtime == "node" else "read_only",
                           "capabilities": ["unix_process_groups", "tool:node"] if runtime == "node" else ["python", "unix_process_groups", "tool:git", "module:yaml", "module:jsonschema"]})
    if found != set(HTML_INTERFACES):
        raise ValueError(f"canonical workflow is missing reviewed HTML checks: {sorted(set(HTML_INTERFACES) - found)}")
    return {"schema_version": "asi_stack.html_check_plan.v1", "workflow": str(workflow),
            "workflow_sha256": hashlib.sha256(workflow_bytes).hexdigest(), "site": str(site),
            "mode": "local_diagnostic" if local else "clean_tested_commit_required", "checks": checks,
            "scope": "Post-render checks taken from the canonical Pages workflow; no rendering, installations, uploads, deployments or derivative-format work. Local mode relaxes only the two clean-commit status requirements."}


def html_files(site: Path) -> dict[str, str]:
    files = {row["path"]: row["sha256"] for row in file_rows(site)}
    if "index.html" not in files:
        raise ValueError("rendered HTML index.html is missing")
    return files


def html_inputs(root: Path, checks: list[dict]) -> dict:
    # Capture the manuscripts and explicit runtime interfaces in addition to
    # the complete site bytes. This is a declared-input check, not a whole-Git
    # snapshot assertion or proof of render provenance.
    inputs = ["book_structure.json", "validation/registry.json", "assets/styles.scss",
              "_quarto.yml", "assets/filters/chapter-freshness.lua", "scripts/chapter_freshness.py",
              ".github/workflows/build-pages-artifact.yml",
              "editions/reader_manuscript/current/conclusion_claim_crosswalk.json",
              "scripts/book.py", "scripts/validation_runtime.py", "scripts/schema_validation.py", "scripts/admission_guard.py",
              "scripts/build_product_projections.py", "scripts/generated_directory.py", "scripts/projection_files.py",
              "scripts/build_tested_site_bundle.py", "scripts/build_release_channels.py",
              "scripts/build_canonical_public_status.py", "schemas/product_projection_manifest.schema.json",
              "schemas/canonical_public_status.schema.json", "schemas/narrative_product_spine.schema.json",
              *[f"scripts/{row['script']}" for row in checks],
              *[path.relative_to(root).as_posix() for path in (root / "chapters").glob("*.qmd")],
              *[path.relative_to(root).as_posix() for path in (root / "editions/reader_manuscript/current").glob("*.qmd")]]
    result = identity(root, inputs)
    rendered = root / "editions/reader_manuscript/current/_book"
    if rendered.exists() or rendered.is_symlink():
        if rendered.is_symlink():
            raise ValueError("rendered reader input must not be a link")
        result.update({f"editions/reader_manuscript/current/_book/{path}": value for path, value in html_files(rendered).items()})
    return result


def check_html(result: dict, root: Path, site: Path) -> dict:
    before = html_files(site)
    input_before = html_inputs(root, result["checks"])
    if input_before.get(".github/workflows/build-pages-artifact.yml") != result["workflow_sha256"]:
        raise ValueError("workflow changed after planning")
    build = root / "build"
    if build.is_symlink():
        raise ValueError("diagnostics directory must not be a link")
    build.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="book-html-check-", dir=build))
    records = []
    halted = False
    for row in result["checks"]:
        missing = [f"{name}: {error}" for name in row["capabilities"] if (error := capability_error(name))]
        record = dict(row)
        if halted:
            record.update(status="not_run", diagnostic_id="fail_fast_stop")
        elif missing:
            record.update(status="not_run", diagnostic_id="missing_capability", reason="; ".join(missing))
            halted = True
        else:
            command = ["node" if row["runtime"] == "node" else sys.executable,
                       str(root / "scripts" / row["script"]), *row["args"]]
            if row["runtime"] == "node":
                command.extend(["--report", str(output / "browser.json")])
            elif row["script"] == "validate_live_human_view_browser_report.py":
                command.extend(["--report", str(output / "browser.json")])
            print(f"Checking {row['script']} from {row['workflow_step']}", flush=True)
            try:
                record.update(execute(command, cwd=root, log=output / f"{row['script']}.log", timeout=row["timeout_seconds"]))
            except OSError as error:
                record.update(status="failed", diagnostic_id="execution_error", reason=str(error))
            halted = record["status"] != "passed"
        records.append(record)
    unchanged = html_files(site) == before and html_inputs(root, result["checks"]) == input_before
    report = {"schema_version": "asi_stack.html_check_run.v1", "status": "pass" if not halted and unchanged else "fail",
              "plan": result, "units": records, "site_sha256": before, "input_sha256": input_before,
              "declared_inputs_and_site_unchanged": unchanged,
              "scope": "Post-render repository checks only; no clean build provenance, CI success, release approval or support movement is inferred."}
    path = output / "report.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"HTML checks: {report['status']}; report {path}", flush=True)
    return report


def changed_paths(base: str) -> list[str]:
    # Accept Git revisions as structured argv, never as shell text. Resolve a
    # user-supplied base before diffing both the index and working tree.
    commit = subprocess.run(["git", "rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"],
                            cwd=ROOT, capture_output=True, check=True, timeout=30).stdout.decode().strip()
    result = subprocess.run(["git", "diff", "--no-renames", "--name-only", "-z", commit, "--"],
                            cwd=ROOT, capture_output=True, check=True, timeout=30)
    return [path.decode("utf-8") for path in result.stdout.split(b"\0") if path]


def delegate(tier: str, names: list[str], report: str) -> None:
    command = [sys.executable, str(ROOT / "scripts/run_validation_registry.py"), "--tier", tier,
               "--report", str(ROOT / "build" / report)]
    for name in names:
        command.extend(["--select", name])
    # Replace the wrapper: the runner owns budgets, logs, process groups and
    # truthful exit codes without an extra unbounded parent subprocess.
    os.execv(sys.executable, command)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="Inspect tier capabilities, review gaps and side effects; do not run checks")
    doctor.add_argument("--tier", choices=("pr", "deep", "release"), default="pr")
    for name in ("plan", "check"):
        sub = commands.add_parser(name, help="Inspect affected current owners" if name == "plan" else "Run named affected checks after required reviews/rebuilds")
        sub.add_argument("--changed", action="append", default=[], help="Normalized repository-relative changed path; repeatable, including a proposed new file")
        sub.add_argument("--base", help="Git base revision for tracked index/worktree changes; untracked proposals require --changed")
        if name == "check":
            sub.add_argument("--tier", choices=("pr", "deep", "release"), default="deep")
            sub.add_argument("--full", action="store_true", help="Run the full tier instead of a targeted plan")
    projections = commands.add_parser("projections", help="List current rebuild owners or run their existing consumers")
    projections.add_argument("--check", action="store_true", help="Run all named current-projection checks without running rebuild commands")
    history = commands.add_parser("history", help="List reviewed retained-history checks or replay one explicitly selected check")
    history.add_argument("--select", help="Exact reviewed retained-history unit ID or script")
    html = commands.add_parser("html", help="Plan or run the canonical workflow's post-render checks against an existing local site")
    html.add_argument("--site", type=Path, default=Path("_site"))
    html.add_argument("--plan", action="store_true", help="Preview existing workflow checks, budgets and output effects without running them")
    html.add_argument("--local", action="store_true", help="Permit diagnostic dirty-worktree status; this cannot certify a deployable tested commit")
    args = parser.parse_args()
    if args.command == "html":
        site = args.site if args.site.is_absolute() else ROOT / args.site
        if site.is_symlink() or any(parent.is_symlink() for parent in site.parents):
            parser.error("rendered site must not traverse a symlink")
        site = site.resolve()
        if site != ROOT / "_site" and (not site.is_relative_to(ROOT / "build") or site == ROOT / "build"):
            parser.error("rendered site must be _site or a directory below ignored build/")
        result = html_plan(ROOT, site, local=args.local)
        if args.plan:
            print(json.dumps(result, indent=2))
        else:
            report = check_html(result, ROOT, site)
            if report["status"] != "pass":
                raise SystemExit(1)
        return
    registry_bytes = REGISTRY.read_bytes()
    registry = json.loads(registry_bytes)
    if args.command == "doctor":
        units = select_units(registry, args.tier, [])
        contracts = [execution_contract(registry, unit) for unit in units]
        capabilities = sorted({name for contract in contracts for name in contract["capabilities"]})
        missing = {name: error for name in capabilities if (error := capability_error(name))}
        unreviewed = [unit["id"] for unit, contract in zip(units, contracts) if contract["review_state"] != "reviewed"]
        print(json.dumps({"status": "missing_capability" if missing else "incomplete_contract_review" if unreviewed else "preflight_only",
                          "python": sys.executable, "python_version": sys.version.split()[0], "tier": args.tier,
                          "selected_units": len(units), "capabilities": capabilities, "missing": missing,
                          "unreviewed_contract_count": len(unreviewed), "unreviewed_contracts": unreviewed,
                          "side_effect_counts": dict(Counter(contract["side_effects"] for contract in contracts)),
                          "scope": "Capability availability only; unreviewed contracts prevent a complete environment or safe-concurrency assertion."}, indent=2))
        if missing:
            raise SystemExit(1)
        return
    if args.command == "history":
        eligible = [unit for unit in registry["units"] if
                    (contract := execution_contract(registry, unit))["review_state"] == "reviewed" and
                    contract["historical_mode"] in {"retained_commit", "frozen_bytes"} and contract["side_effects"] == "read_only"]
        if args.select:
            matches = [unit for unit in eligible if args.select in {unit["id"], unit["script"]}]
            if not matches:
                parser.error("selection is not a reviewed read-only retained-history check; inspect the named historical owner directly")
            delegate("release", [unit["id"] for unit in matches], "book-history-report.json")
        print(json.dumps({"retained_history_checks": [{"id": unit["id"], "script": unit["script"], "args": unit["args"]} for unit in eligible],
                          "scope": "Reviewed replay commands only; no historical builder --write or terminal receipt rewriting."}, indent=2))
        return
    if args.command == "projections":
        nodes = registry.get("current_projections", [])
        if args.check:
            delegate("release", sorted({name for node in nodes for name in node["checks"]}), "book-projection-report.json")
        print(json.dumps({"current_projections": nodes, "scope": "Commands are a preview; manual review boundaries remain required. No writes performed."}, indent=2))
        return
    if args.command == "check" and args.full:
        if args.changed or args.base:
            parser.error("--full does not accept changed-path selection")
        delegate(args.tier, [], "book-full-check-report.json")
    paths = args.changed + (changed_paths(args.base) if args.base else [])
    if not paths:
        parser.error("provide --changed or --base; use check --full for the complete tier")
    result = plan(registry, paths, ROOT)
    result["registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
    if args.command == "plan":
        print(json.dumps(result, indent=2))
        return
    allowed = {unit["id"] for unit in select_units(registry, args.tier, [])}
    names = [row["id"] for row in result["checks"] if row["id"] in allowed]
    outside = [row["id"] for row in result["checks"] if row["id"] not in allowed]
    if outside:
        parser.error(f"affected checks exceed --tier {args.tier}: {outside}; select a sufficient tier")
    if not names:
        parser.error("no checks have declared this input; use check --full rather than treating unknown coverage as pass")
    print("Running declared affected checks. Review-required rebuilds are not performed; full CI still gates admission.", flush=True)
    delegate(args.tier, names, "book-targeted-check-report.json")


if __name__ == "__main__":
    try:
        from admission_guard import canonical_access
        with canonical_access(ROOT):
            main()
    except (OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        raise SystemExit(f"Contributor command failed: {error}")
