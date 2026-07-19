#!/usr/bin/env python3
"""Calibrate P2 independent parsers against expected and pinned upstream outputs."""

from __future__ import annotations

import __future__
import gzip
import hashlib
import json
import sys
import types
from pathlib import Path

from p2_independent_test_log_evaluator import evaluate


ROOT = Path(__file__).resolve().parents[1]
HARNESS = Path("/tmp/swe-rebench-v2-code.7ixeFl")
UPSTREAM_COMMIT = "c71902a8cf8d2b725f63d51f199f4d3e56f68d2d"
OUT = ROOT / "evidence_quality/p2_independent_test_log_evaluator_calibration.json"


def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def upstream_module():
    if __import__("subprocess").run(["git", "-C", str(HARNESS), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() != UPSTREAM_COMMIT: raise SystemExit("harness commit drift")
    sys.path.insert(0, str(HARNESS)); sys.path.insert(0, str(HARNESS / "lib"))
    source = HARNESS / "lib/agent/log_parsers.py"; module = types.ModuleType("p2_calibration_upstream"); module.__file__ = str(source)
    exec(compile(source.read_text(), str(source), "exec", flags=__future__.annotations.compiler_flag), module.__dict__); return module


FIXTURES = [
    ("cargo_pass_fail", "parse_log_cargo", 101, "test a::b ... ok\ntest c::d ... FAILED\n", {"a::b": "PASSED", "c::d": "FAILED"}),
    ("cargo_ignored_and_noise", "parse_log_cargo", 0, "noise\ntest a::b ... ignored\ntest c ... ok\n", {"c": "PASSED"}),
    ("go_pass_fail_skip", "parse_log_gotest", 1, "--- PASS: TestA (0.00s)\n--- FAIL: TestB/sub (1.20s)\n--- SKIP: TestC (0.00s)\n", {"TestA": "PASSED", "TestB/sub": "FAILED", "TestC": "SKIPPED"}),
    ("go_duplicate_last_status", "parse_log_gotest", 0, "--- FAIL: TestA (0.00s)\n--- PASS: TestA (0.01s)\n", {"TestA": "PASSED"}),
    ("maven_pass_summary", "parse_java_mvn", 0, "[INFO] Running a.b.C\n[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1 s -- in a.b.C\n", {"a.b.C": "PASSED"}),
    ("maven_failed_method", "parse_java_mvn", 1, "[INFO] Running a.b.C\n[ERROR] a.b.C.testThing:42 expected x\nTests run: 1, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 1 s -- in a.b.C\n", {"a.b.C.testThing": "FAILED", "a.b.C": "FAILED"}),
    ("maven_exception_method", "parse_java_mvn", 1, "[ERROR] a.b.C.testThing:42 RuntimeException\n", {"a.b.C.testThing": "ERROR", "a.b.C": "FAILED"}),
    ("maven_skipped_summary", "parse_java_mvn", 0, "Running a.b.C\nTests run: 1, Failures: 0, Errors: 0, Skipped: 1\n", {"a.b.C": "SKIPPED"}),
    ("maven_dtest_success", "parse_java_mvn", 0, "+ mvn -Dtest=a.b.C test\n[INFO] BUILD SUCCESS\n", {"a.b.C": "PASSED"}),
    ("zero_exit_visible_failure", "parse_log_gotest", 0, "--- FAIL: TestA (0.00s)\n", {"TestA": "FAILED"}),
    ("nonzero_no_status", "parse_log_cargo", 101, "error: could not compile crate\n", {}),
    ("malformed_zero_no_status", "parse_log_gotest", 0, "--- MAYBE: TestA\n", {}),
]


def main() -> None:
    upstream = upstream_module(); fixtures = []
    for fixture_id, parser_name, exit_code, text, expected in FIXTURES:
        independent = evaluate(text, parser_name, exit_code); upstream_status = {k: v for k, v in upstream.NAME_TO_PARSER[parser_name](text).items()}
        passed = independent["statuses"] == expected == upstream_status
        fixtures.append({"fixture_id": fixture_id, "parser_name": parser_name, "exit_code": exit_code, "input_sha256": hashlib.sha256(text.encode()).hexdigest(), "expected": expected, "independent": independent, "upstream_statuses": upstream_status, "exact_agreement": passed})
    historical = []
    patterns = {
        "parse_log_cargo": ["aleph-alpha__ts-rs-422.*.log.gz"],
        "parse_log_gotest": ["compose-spec__compose-go-792.*.log.gz", "gitleaks__gitleaks-1845.*.log.gz", "google__yamlfmt-259.*.log.gz"],
        "parse_java_mvn": ["thealgorithms__java-6333.*.log.gz"],
    }
    base = ROOT / "experiments/p2_governed_repository_admission/gold_preflight/logs"
    for parser_name, globs in patterns.items():
        for pattern in globs:
            for path in sorted(base.glob(pattern)):
                with gzip.open(path, "rt", encoding="utf-8") as handle: text = handle.read()
                independent = evaluate(text, parser_name, 0)["statuses"]; upstream_status = dict(upstream.NAME_TO_PARSER[parser_name](text))
                historical.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha_file(path), "parser_name": parser_name, "status_count": len(independent), "exact_agreement": independent == upstream_status})
    output = {
        "schema_version": "asi_stack.p2_independent_test_log_evaluator_calibration.v1", "recorded_date": "2026-07-17", "state": "passed" if all(r["exact_agreement"] for r in fixtures + historical) else "failed",
        "independent_evaluator_path": "scripts/p2_independent_test_log_evaluator.py", "independent_evaluator_sha256": sha_file(ROOT / "scripts/p2_independent_test_log_evaluator.py"),
        "upstream_harness_commit": UPSTREAM_COMMIT, "authored_fixture_count": len(fixtures), "historical_log_count": len(historical), "exact_agreement_count": sum(r["exact_agreement"] for r in fixtures + historical), "total_case_count": len(fixtures) + len(historical),
        "fixtures": fixtures, "historical_logs": historical,
        "candidate_execution_started": False, "candidate_outcome_opened": False, "final_pool_selected": False, "final_pool_opened": False, "support_state_effect": "none", "release_effect": "none",
        "non_claims": ["Authored and historical calibration does not prove parser completeness for unseen output grammars.", "Exact agreement between two parsers can preserve a shared conceptual mistake; exact expected-set and execution controls remain required.", "Calibration is not task qualification or claim evidence."]
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"P2 independent evaluator calibration {output['state']}: {output['exact_agreement_count']}/{output['total_case_count']} exact agreements.")
    if output["state"] != "passed": raise SystemExit(2)


if __name__ == "__main__": main()
