"""Runner behavior is tested independently of the book's domain validators."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_validation_registry as runner
import validation_runtime as runtime
from validation_runtime import execute


class ExecutionTests(unittest.TestCase):
    def test_darwin_exited_group_refusal_requires_observed_disappearance(self):
        process = Mock(pid=123456); process.poll.return_value = 0
        with patch.object(runtime.sys, "platform", "darwin"), patch.object(runtime.os, "killpg",
             side_effect=[PermissionError("authored exited-group refusal"), PermissionError("still present"), ProcessLookupError("gone")]) as kill:
            runtime.signal_owned_group(process, 9)
        self.assertEqual([(123456, 9), (123456, 0), (123456, 0)], [call.args for call in kill.call_args_list])

    def test_persistent_live_and_non_darwin_signal_refusals_never_count_as_cleanup(self):
        for platform, alive in (("darwin", False), ("darwin", True), ("linux", False)):
            with self.subTest(platform=platform, alive=alive):
                process = Mock(pid=123456); process.poll.return_value = None if alive else 0
                with patch.object(runtime.sys, "platform", platform), patch.object(runtime.os, "killpg",
                     side_effect=PermissionError("authored persistent refusal")) as kill:
                    with self.assertRaises(PermissionError):
                        runtime.signal_owned_group(process, 9)
                if platform != "darwin" or alive:
                    self.assertEqual(1, kill.call_count)

    def test_cleanup_refusal_retains_log_and_rejects_successful_leader_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = runtime.terminate
            def rejected_cleanup(process):
                original(process)  # No actual child is left alive by the fixture.
                raise PermissionError("authored signal refusal")
            with patch.object(runtime, "terminate", side_effect=rejected_cleanup):
                result = execute([sys.executable, "-c", "print('completed leader')"], cwd=root,
                                 log=root / "run.log", timeout=5)
            self.assertEqual(0, result["exit_code"])
            self.assertEqual("failed", result["status"])
            self.assertEqual("cleanup_failed", result["diagnostic_id"])
            self.assertIs(False, result["cleanup_confirmed"])
            self.assertIn("PermissionError", result["cleanup_errors"][0])
            self.assertEqual("completed leader\n", (root / "run.log").read_text())

    def test_timeout_terminates_descendants_and_preserves_log(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "orphan-effect"
            # A 200ms budget can expire before Python starts on a busy host;
            # that observes no descendant and cannot test group termination.
            # Require both processes to start, with an effect delayed beyond
            # the runner's budget, then observe the complete escape window.
            child = f"import time; from pathlib import Path; print('child-ready',flush=True); time.sleep(3); Path({str(marker)!r}).write_text('escaped')"
            parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); print('parent-ready',flush=True); time.sleep(30)"
            result = execute([sys.executable, "-c", parent], cwd=root, log=root / "run.log", timeout=2)
            self.assertEqual("timed_out", result["status"], result)
            retained = (root / "run.log").read_text()
            self.assertIn("parent-ready", retained)
            self.assertIn("child-ready", retained)
            time.sleep(3.1)
            self.assertFalse(marker.exists(), "a descendant survived the timeout")

    def test_output_is_drained_but_retained_log_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = execute([sys.executable, "-c", "print('x' * 200000)"], cwd=root,
                             log=root / "run.log", timeout=5, max_log_bytes=1024)
            self.assertEqual("passed", result["status"])
            self.assertTrue(result["log_truncated"])
            self.assertEqual(1024, (root / "run.log").stat().st_size)

    def test_nested_python_uses_the_runner_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            code = "import subprocess; subprocess.run(['python3','-c','import sys; print(sys.prefix)'],check=True)"
            result = execute([sys.executable, "-c", code], cwd=root, log=root / "run.log", timeout=5)
            self.assertEqual("passed", result["status"])
            self.assertEqual(sys.prefix, (root / "run.log").read_text().strip())


class AggregateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "scripts").mkdir()
        for script, code in {"base.py": "pass", "pass.py": "print('ok')", "fail.py": "raise SystemExit(7)"}.items():
            (self.root / "scripts" / script).write_text(code)
        self.registry = {"base_gate": {"script": "base.py"}, "tier_order": ["pr", "deep", "release"],
                         "execution_defaults": {"capabilities": ["python", "unix_process_groups"],
                            "side_effects": "read_only", "review_state": "reviewed", "timeout_seconds": 5,
                            "depends_on": ["base-gate"], "network": "none", "historical_mode": "current"},
                         "units": []}

    def unit(self, identifier, script="pass.py", **execution):
        return {"id": identifier, "script": script, "args": [], "execution_tier": "pr", "execution": execution}

    def run_units(self, units, diagnostic=True):
        with patch.object(runner, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            return runner.run_selected(self.registry, units, diagnostic=diagnostic, output=self.root / "outputs")

    def test_independent_failure_does_not_hide_later_results(self):
        report = self.run_units([self.unit("bad", "fail.py"), self.unit("good"), self.unit("blocked", depends_on=["bad"])])
        self.assertEqual("fail", report["status"])
        self.assertEqual({"passed": 2, "failed": 1, "skipped": 0, "timed_out": 0, "cancelled": 0, "not_run": 1}, report["counts"])
        self.assertEqual("dependency_blocked", report["units"][-1]["diagnostic_id"])
        self.assertEqual(sys.executable, report["units"][1]["command"][0])

    def test_cleanup_failure_remains_failed_in_aggregate_even_with_zero_exit(self):
        original = runtime.terminate
        calls = []
        def rejected_cleanup(process):
            original(process)
            calls.append(process.pid)
            if len(calls) == 2:
                raise PermissionError("authored aggregate cleanup refusal")
        with patch.object(runtime, "terminate", side_effect=rejected_cleanup):
            report = self.run_units([self.unit("cleanup-refused"), self.unit("must-not-run", depends_on=[])])
        self.assertEqual("fail", report["status"])
        self.assertEqual(1, report["counts"]["failed"])
        self.assertEqual("cleanup_failed", report["units"][1]["diagnostic_id"])
        self.assertIs(False, report["units"][1]["cleanup_confirmed"])
        self.assertEqual("not_run", report["units"][2]["status"])
        self.assertEqual("fail_fast_stop", report["units"][2]["diagnostic_id"])

    def test_fail_fast_records_unstarted_units(self):
        report = self.run_units([self.unit("bad", "fail.py"), self.unit("good")], diagnostic=False)
        self.assertFalse(report["units"][-1]["started"])
        self.assertEqual("fail_fast_stop", report["units"][-1]["diagnostic_id"])

    def test_unknown_effects_and_missing_capabilities_are_not_passes(self):
        report = self.run_units([self.unit("unsafe", side_effects="unreviewed", review_state="unreviewed"),
                                 self.unit("unavailable", capabilities=["module:missing_validation_test_dependency"])])
        self.assertEqual(2, report["counts"]["not_run"])
        self.assertEqual("fail", report["status"])
        self.assertEqual("missing_capability", report["units"][-1]["diagnostic_id"])

    def test_selection_is_exact_and_preserves_tier_boundary(self):
        self.registry["units"] = [self.unit("one"), {**self.unit("two"), "execution_tier": "release"}]
        self.assertEqual([self.registry["units"][0]], runner.select_units(self.registry, "pr", ["one"]))
        with self.assertRaises(ValueError):
            runner.select_units(self.registry, "pr", ["two"])

    def test_loaded_registry_drift_stops_later_units_and_preserves_identity(self):
        (self.root / "validation").mkdir()
        path = self.root / "validation/registry.json"
        original = json.dumps(self.registry).encode()
        path.write_bytes(original)
        digest = hashlib.sha256(original).hexdigest()
        (self.root / "scripts/change.py").write_text(
            "from pathlib import Path; Path('validation/registry.json').write_text('{}')")
        with patch.object(runner, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            report = runner.run_selected(self.registry, [self.unit("change", "change.py"), self.unit("later")],
                                         diagnostic=True, output=self.root / "outputs", loaded_registry_sha256=digest)
        self.assertEqual("fail", report["status"])
        self.assertTrue(report["registry_drift"])
        self.assertEqual({"validation/registry.json": digest}, report["registry_sha256"])
        self.assertEqual("registry_drift", report["units"][-1]["diagnostic_id"])
        self.assertFalse(report["units"][-1]["started"])

    def test_final_unit_registry_deletion_cannot_be_reported_as_pass(self):
        (self.root / "validation").mkdir()
        path = self.root / "validation/registry.json"
        original = json.dumps(self.registry).encode()
        path.write_bytes(original)
        (self.root / "scripts/delete.py").write_text(
            "from pathlib import Path; Path('validation/registry.json').unlink()")
        with patch.object(runner, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            report = runner.run_selected(self.registry, [self.unit("last", "delete.py")], diagnostic=False,
                                         output=self.root / "outputs", loaded_registry_sha256=hashlib.sha256(original).hexdigest())
        self.assertEqual(2, report["counts"]["passed"])
        self.assertEqual("fail", report["status"])
        self.assertEqual({}, report["registry_sha256_after"])
        self.assertEqual("registry_drift", report["diagnostics"][0]["diagnostic_id"])


if __name__ == "__main__":
    unittest.main()
