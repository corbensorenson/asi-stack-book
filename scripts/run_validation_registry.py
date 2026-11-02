#!/usr/bin/env python3
"""Execute validation units from the declarative registry by tier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
from urllib.parse import quote

from validation_runtime import capability_error, execute, identity


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"


def execution_contract(registry: dict, unit: dict) -> dict:
    return {**registry["execution_defaults"], **unit.get("execution", {})}


def select_units(registry: dict, tier: str, names: list[str]) -> list[dict]:
    ranks = {name: index for index, name in enumerate(registry["tier_order"])}
    selected = [unit for unit in registry["units"] if ranks[unit["execution_tier"]] <= ranks[tier]]
    if names:
        known = {name for unit in selected for name in (unit["id"], unit["script"])}
        unknown = set(names) - known
        if unknown:
            raise ValueError(f"unknown or out-of-tier selections: {sorted(unknown)}")
        selected = [unit for unit in selected if unit["id"] in names or unit["script"] in names]
    return selected


def run_selected(registry: dict, selected: list[dict], *, diagnostic: bool,
                 output: Path, timeout_override: float | None = None,
                 loaded_registry_sha256: str | None = None) -> dict:
    from admission_guard import canonical_access
    with canonical_access(ROOT):
        return _run_selected(registry, selected, diagnostic=diagnostic, output=output,
                             timeout_override=timeout_override, loaded_registry_sha256=loaded_registry_sha256)


def _run_selected(registry: dict, selected: list[dict], *, diagnostic: bool,
                  output: Path, timeout_override: float | None = None,
                  loaded_registry_sha256: str | None = None) -> dict:
    records = []
    outcomes = {}
    halted = False
    registry_drift = False
    # The report must identify the bytes actually parsed, not whatever happens
    # to occupy the registry path when the final unit exits. In-memory callers
    # (including independent tests) have no filesystem custody assertion.
    loaded_identity = ({"validation/registry.json": loaded_registry_sha256}
                       if loaded_registry_sha256 is not None else {})

    def registry_changed() -> bool:
        return (loaded_registry_sha256 is not None and
                identity(ROOT, ["validation/registry.json"]) != loaded_identity)
    base = {"id": "base-gate", "script": registry["base_gate"]["script"], "args": [],
            "execution": {"side_effects": "read_only", "review_state": "reviewed", "depends_on": []}}
    for unit in [base, *selected]:
        registry_drift |= registry_changed()
        contract = execution_contract(registry, unit)
        record = {"unit_id": unit["id"], "script": unit["script"], "selected": True,
                  "started": False, "execution_contract": contract,
                  "input_sha256": identity(ROOT, unit.get("input_artifacts", []))}
        missing = [f"{name}: {error}" for name in contract["capabilities"]
                   if (error := capability_error(name))]
        dependencies = contract["depends_on"]
        blocked = [name for name in dependencies if outcomes.get(name) != "passed"]
        reason = None
        code = None
        if registry_drift:
            reason, code = "loaded registry changed during execution; restart against stable inputs", "registry_drift"
        elif halted:
            reason, code = "previous required unit failed; fail-fast execution stopped", "fail_fast_stop"
        elif blocked:
            reason, code = f"unresolved or failed dependencies: {blocked}", "dependency_blocked"
        elif missing:
            reason, code = "; ".join(missing), "missing_capability"
        elif diagnostic and (contract["review_state"] != "reviewed" or contract["side_effects"] != "read_only"):
            reason, code = "read-only diagnostic requires a reviewed read-only execution contract", "unsafe_diagnostic_selection"
        if reason:
            record.update(status="not_run", diagnostic_id=code, reason=reason, duration_seconds=0)
        else:
            record["started"] = True
            print(f"+ {unit['id']} {unit['script']} {' '.join(unit['args'])}", flush=True)
            try:
                record.update(execute([sys.executable, str(ROOT / "scripts" / unit["script"]), *unit["args"]],
                                      cwd=ROOT, log=output / "logs" / f"{quote(unit['id'], safe='-_.')}.log",
                                      timeout=timeout_override or contract["timeout_seconds"]))
            except OSError as error:
                record.update(status="failed", diagnostic_id="execution_error", reason=str(error), duration_seconds=0)
            print(f"  {record['status']}: {record.get('log', record.get('reason'))}", flush=True)
        records.append(record)
        outcomes[unit["id"]] = record["status"]
        registry_drift |= registry_changed()
        if (record["status"] == "cancelled" or record.get("cleanup_confirmed") is False
                or record["status"] != "passed" and not diagnostic):
            halted = True
    states = ("passed", "failed", "skipped", "timed_out", "cancelled", "not_run")
    counts = {state: sum(record["status"] == state for record in records) for state in states}
    return {"schema_version": "asi_stack.validation_run.v1", "mode": "diagnostic" if diagnostic else "gate",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "status": "pass" if counts["passed"] == len(records) and not registry_drift else "fail",
            "python_executable": sys.executable, "registry_sha256": loaded_identity,
            "registry_identity_scope": "loaded_file_bytes" if loaded_registry_sha256 is not None else "in_memory_no_file_custody",
            "registry_sha256_after": identity(ROOT, ["validation/registry.json"]),
            "registry_drift": registry_drift,
            "diagnostics": ([{"diagnostic_id": "registry_drift", "reason": "Registry changed after loading; this run cannot gate publication."}]
                            if registry_drift else []),
            "selected": len(records), "started": sum(record["started"] for record in records),
            "counts": counts, "units": records,
            "scope": "Executed repository checks only; no claim promotion or release approval."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=("pr", "deep", "release"), required=True)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--select", action="append", default=[], help="Exact unit ID or script name; repeat to select several")
    parser.add_argument("--plan", action="store_true", help="Show capability and side-effect contracts without executing")
    parser.add_argument("--preflight", action="store_true", help="Check selected capabilities without running validators")
    parser.add_argument("--diagnostic", action="store_true", help="Continue reviewed read-only independent units; unresolved units still fail")
    parser.add_argument("--report", type=Path, default=ROOT / "build/validation_registry_report.json")
    parser.add_argument("--timeout", type=float, help="Explicit per-unit override in seconds")
    args = parser.parse_args()
    registry_bytes = REGISTRY.read_bytes()
    registry = json.loads(registry_bytes)
    loaded_registry_sha256 = hashlib.sha256(registry_bytes).hexdigest()
    try:
        selected = select_units(registry, args.tier, args.select)
    except ValueError as error:
        parser.error(str(error))
    if args.timeout is not None and args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.list:
        for unit in selected:
            print(f"{unit['order']:03d} {unit['execution_tier']:7s} {unit['validation_class']:24s} {unit['script']} {' '.join(unit['args'])}")
        print(f"Selected {len(selected)} registry units for tier {args.tier}.")
        return
    if args.plan or args.preflight:
        units = [{"id": unit["id"], "script": unit["script"], **execution_contract(registry, unit)} for unit in selected]
        capabilities = sorted({name for unit in units for name in unit["capabilities"]})
        errors = {name: error for name in capabilities if (error := capability_error(name))}
        print(json.dumps({"tier": args.tier, "python": sys.executable, "capabilities": capabilities,
                          "unavailable": errors, "units": units}, indent=2))
        if args.preflight and errors:
            raise SystemExit(1)
        return
    report_path = args.report.resolve()
    # Reports are disposable diagnostics, never an arbitrary tracked overwrite.
    if not report_path.is_relative_to(ROOT / "build"):
        parser.error("--report must be below the ignored repository build directory")
    output = report_path.parent / (report_path.stem + "-outputs")
    report = run_selected(registry, selected, diagnostic=args.diagnostic, output=output,
                          timeout_override=args.timeout, loaded_registry_sha256=loaded_registry_sha256)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Validation registry tier {args.tier}: {report['status']}; {report['counts']}; report {report_path}")
    if report["counts"]["cancelled"]:
        raise SystemExit(130)
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        from admission_guard import canonical_access
        with canonical_access(ROOT):
            main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Validation registry execution refused: {error}")
