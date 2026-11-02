"""Authored filesystem/receipt controls, not scientific chapter approval.

The full-runner observations here are synthetic fixtures. A real valid birth
must separately pass the actual book/deep consumers before D02 can close.
"""

import json
import copy
import multiprocessing
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import admission_guard as guard
import canonical_admission_transaction as transaction
import prepare_chapter_admission as admission
from tests import test_chapter_admission_staging as fixtures


class CanonicalAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.AdmissionStagingTests(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.stage, self.candidate = self.fixture.root, self.fixture.stage, self.fixture.patch
        self.fixture.write(self.root, "docs/adjacency.md", "Original authored fixture boundary.\n")
        self.fixture.run_git("add", "docs/adjacency.md")
        self.fixture.run_git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Known adjacency fixture")
        self.fixture.write(self.candidate, "docs/adjacency.md", "Candidate authored fixture boundary.\n")
        self.fixture.write(self.candidate, "products/new-owner/reference.txt", "Candidate data fixture only.\n")
        registry = copy.deepcopy(self.fixture.registry)
        registry["required_artifacts"].extend(["chapters/candidate-owner.qmd", "products/new-owner/reference.txt"])
        registry["summary"]["required_artifact_count"] = len(registry["required_artifacts"])
        self.fixture.write(self.candidate, "validation/registry.json", registry)
        self.before = {name: transaction.physical(self.root / name) for name in
                       ("book_structure.json", "docs/adjacency.md", "chapters/candidate-owner.qmd", "validation/registry.json")}

    def install(self):
        with patch.object(admission, "execute", side_effect=self.fixture.successful_report):
            return self.fixture.prepare(install=True)

    def interrupt_after_swap(self, name="docs/adjacency.md"):
        original = transaction.exchange_directories
        def fail(slot, target):
            original(slot, target)
            if target == self.root / name:
                raise OSError("authored post-exchange interruption")
        with patch.object(transaction, "exchange_directories", side_effect=fail):
            with self.assertRaisesRegex(OSError, "post-exchange"):
                self.install()

    def assert_original_objects(self):
        for name, prior in self.before.items():
            self.assertEqual(prior, transaction.physical(self.root / name), name)
        self.assertFalse((self.root / guard.ACTIVE).exists())
        self.assertEqual("keep private fixture\n", (self.root / "personal/unknown.txt").read_text())

    def test_full_fixture_gate_installs_only_intended_diff_and_commits_manifest_last(self):
        original = transaction.exchange_directories
        calls = []
        def observe(slot, target):
            calls.append(target.relative_to(self.root).as_posix())
            if target.name != "book_structure.json":
                self.assertEqual(self.before["book_structure.json"], transaction.physical(self.root / "book_structure.json"))
            original(slot, target)
        git_before = admission.git_identity(self.root)
        with patch.object(transaction, "exchange_directories", side_effect=observe):
            receipt = self.install()
        self.assertEqual("installed", receipt["status"])
        self.assertEqual("admitted", receipt["admission_state"])
        self.assertEqual("none", receipt["support_state_effect"])
        self.assertEqual("book_structure.json", calls[-1])
        self.assertEqual(self.fixture.candidate, json.loads((self.root / "book_structure.json").read_text()))
        self.assertEqual(git_before, admission.git_identity(self.root))
        self.assertFalse((self.root / guard.ACTIVE).exists())
        self.assertTrue((self.stage / "transaction/before/book_structure.json").is_file())
        self.assertFalse((self.stage / "workspace/personal/unknown.txt").exists())

    def test_failed_or_incomplete_full_gate_cannot_begin_canonical_transaction(self):
        def incomplete(command, **kwargs):
            result = self.fixture.successful_report(command, **kwargs)
            target = Path(command[command.index("--report") + 1])
            value = json.loads(target.read_text()); value["units"].pop(); target.write_text(json.dumps(value))
            return result
        with patch.object(admission, "execute", side_effect=incomplete):
            with self.assertRaisesRegex(ValueError, "every selected full-deep gate"):
                self.fixture.prepare(install=True)
        self.assert_original_objects()
        self.assertFalse((self.stage / "transaction").exists())

    def test_inventory_patch_cannot_change_checking_contracts_or_existing_ownership(self):
        baseline = json.loads((self.candidate / "validation/registry.json").read_text())
        mutations = [
            lambda row: row["units"][0].update(args=["--weaken-fixture"]),
            lambda row: row["units"][0].update(execution_tier="release"),
            lambda row: row["base_gate"].update(script="forged-check.py"),
            lambda row: row.update(input_coverage="fabricated"),
            lambda row: row["summary"].update(other_count=0),
            lambda row: row["summary"].update(required_artifact_count=True),
            lambda row: row["required_artifacts"].remove("book_structure.json"),
            lambda row: row["required_artifacts"].reverse(),
            lambda row: row["required_artifacts"].append("book_structure.json"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                value = copy.deepcopy(baseline); mutate(value)
                self.fixture.write(self.candidate, "validation/registry.json", value)
                with patch.object(admission, "execute", side_effect=AssertionError("must reject before validation")):
                    with self.assertRaises(ValueError):
                        self.fixture.prepare(install=True)
                self.assertFalse(self.stage.exists())
                self.assert_original_objects()

    def test_inventory_addition_requires_candidate_data_and_cannot_register_checkers_or_custody(self):
        baseline = json.loads((self.candidate / "validation/registry.json").read_text())
        for name in ("docs/missing.md", "scripts/forged.py", "tests/forged.py", "sources/forged.json",
                     "validation/forged.json", "docs/../unknown.md"):
            with self.subTest(artifact=name):
                value = copy.deepcopy(baseline)
                value["required_artifacts"].append(name)
                value["summary"]["required_artifact_count"] += 1
                self.fixture.write(self.candidate, "validation/registry.json", value)
                with self.assertRaises(ValueError):
                    self.fixture.prepare(install=True)
                self.assertFalse(self.stage.exists())
                self.assert_original_objects()

    def test_unregistered_new_payload_cannot_begin_install_but_can_remain_diagnostic(self):
        (self.candidate / "validation/registry.json").unlink()
        with self.assertRaisesRegex(ValueError, "registration of every new"):
            self.fixture.prepare(install=True)
        self.assertFalse(self.stage.exists())
        receipt = self.fixture.prepare()
        self.assertEqual("prepared_unvalidated", receipt["status"])
        self.assertEqual("not_admitted", receipt["admission_state"])
        self.assert_original_objects()

    def test_full_report_must_bind_candidate_inventory_not_original_registry(self):
        def wrong_registry(command, **kwargs):
            result = self.fixture.successful_report(command, **kwargs)
            report = Path(command[command.index("--report") + 1])
            value = json.loads(report.read_text())
            value["registry_sha256"]["validation/registry.json"] = admission.digest(self.root / "validation/registry.json")
            report.write_text(json.dumps(value))
            return result
        with patch.object(admission, "execute", side_effect=wrong_registry):
            with self.assertRaisesRegex(ValueError, "every selected full-deep gate"):
                self.fixture.prepare(install=True)
        self.assertFalse((self.stage / "transaction").exists())
        self.assert_original_objects()

    def test_unknown_new_target_is_preserved_before_marker_creation(self):
        def create_unknown(command, **kwargs):
            result = self.fixture.successful_report(command, **kwargs)
            (self.root / "chapters/candidate-owner.qmd").write_text("User-owned later file.\n")
            return result
        with patch.object(admission, "execute", side_effect=create_unknown):
            with self.assertRaisesRegex(ValueError, "repository object"):
                self.fixture.prepare(install=True)
        self.assertEqual("User-owned later file.\n", (self.root / "chapters/candidate-owner.qmd").read_text())
        self.assertEqual(self.before["book_structure.json"], transaction.physical(self.root / "book_structure.json"))
        self.assertFalse((self.root / guard.ACTIVE).exists())

    def test_post_exchange_failure_blocks_readers_and_rollback_restores_original_objects(self):
        self.interrupt_after_swap()
        with self.assertRaisesRegex(ValueError, "pending"):
            with guard.canonical_access(self.root):
                self.fail("a pending transaction must not be readable")
        result = transaction.rollback(self.root)
        self.assertEqual("rolled_back", result["status"])
        self.assert_original_objects()
        self.assertFalse((self.root / "products").exists())

    def test_abrupt_process_exit_after_manifest_keeps_gate_and_recovers_original_manifest(self):
        def child():
            original = transaction.exchange_directories
            def abrupt(slot, target):
                original(slot, target)
                if target == self.root / "book_structure.json":
                    os._exit(71)
            with patch.object(transaction, "exchange_directories", side_effect=abrupt):
                self.install()
        process = multiprocessing.get_context("fork").Process(target=child)
        process.start(); process.join(30)
        if process.is_alive():
            process.terminate(); process.join(5)
            self.fail("authored admission child did not terminate")
        self.assertEqual(71, process.exitcode)
        self.assertEqual(self.fixture.candidate, json.loads((self.root / "book_structure.json").read_text()))
        with self.assertRaisesRegex(ValueError, "pending"):
            guard.ensure_ready(self.root)
        transaction.rollback(self.root)
        self.assert_original_objects()

    def test_later_edit_refuses_recovery_before_any_restore(self):
        self.interrupt_after_swap("book_structure.json")
        (self.root / "chapters/candidate-owner.qmd").write_text("Preserve the later user edit.\n")
        observed = {name: transaction.physical(self.root / name) for name in self.before}
        with self.assertRaisesRegex(ValueError, "changed"):
            transaction.rollback(self.root)
        self.assertEqual(observed, {name: transaction.physical(self.root / name) for name in self.before})
        self.assertTrue((self.root / guard.ACTIVE).exists())

    def test_concurrent_edit_to_displaced_prior_object_is_retained_and_restored(self):
        original = transaction.exchange_directories
        def mutate_before_swap(slot, target):
            if target == self.root / "docs/adjacency.md":
                target.write_text("Concurrent prior-object edit must survive.\n")
            original(slot, target)
        with patch.object(transaction, "exchange_directories", side_effect=mutate_before_swap):
            with self.assertRaisesRegex(ValueError, "concurrently edited"):
                self.install()
        transaction.rollback(self.root)
        self.assertEqual("Concurrent prior-object edit must survive.\n", (self.root / "docs/adjacency.md").read_text())
        self.assertEqual(self.before["book_structure.json"], transaction.physical(self.root / "book_structure.json"))

    def test_damaged_receipt_or_unrelated_directory_cannot_be_used_to_recover(self):
        self.interrupt_after_swap("book_structure.json")
        journal_path = self.stage / "transaction/journal.json"
        value = json.loads(journal_path.read_text())
        value["directories"]["sources/unknown"] = None
        journal_path.write_text(json.dumps(value))
        observed = transaction.physical(self.root / "book_structure.json")
        with self.assertRaisesRegex(ValueError, "candidate target parent"):
            transaction.rollback(self.root)
        self.assertEqual(observed, transaction.physical(self.root / "book_structure.json"))
        value["directories"].pop("sources/unknown"); journal_path.write_text(json.dumps(value))
        (self.stage / "admission.json").write_text("unknown receipt bytes\n")
        with self.assertRaises(ValueError):
            transaction.rollback(self.root)
        self.assertEqual(observed, transaction.physical(self.root / "book_structure.json"))


class CanonicalLeaseTests(unittest.TestCase):
    def test_wrapper_hard_exit_cannot_release_source_while_owned_command_can_write(self):
        self.hard_exit_control(write=False)

    def test_exclusive_wrapper_hard_exit_stops_command_even_if_it_closes_fds(self):
        self.hard_exit_control(write=True, close_fds=True)

    def hard_exit_control(self, *, write, close_fds=False):
        import signal
        import tempfile
        import time
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            ready, release, effect = root / "ready.json", root / "release", root / "orphan-effect"
            code = ("import os,json,time; from pathlib import Path; "
                    + ("import signal; signal.signal(signal.SIGTERM,signal.SIG_IGN); os.closerange(3,256); " if close_fds else "") +
                    f"Path({str(ready.with_suffix('.pending'))!r}).write_text(json.dumps({{'group':os.getpgrp()}})); "
                    f"os.replace({str(ready.with_suffix('.pending'))!r}, {str(ready)!r}); "
                    f"release=Path({str(release)!r}); "
                    "exec('while not release.exists(): time.sleep(0.02)'); "
                    f"Path({str(effect)!r}).write_text('escaped')")
            def child():
                guard.run_command(root, [sys.executable, "-c", code], write=write)
            process = multiprocessing.get_context("fork").Process(target=child)
            process.start()
            group = None
            try:
                deadline = time.monotonic() + 30
                while not ready.exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(ready.exists(), "owned command never became ready")
                group = json.loads(ready.read_text())["group"]
                os.kill(process.pid, signal.SIGKILL)
                process.join(10)
                self.assertEqual(-signal.SIGKILL, process.exitcode)
                # A writer may proceed only after command cleanup. Releasing
                # the fixture then cannot allow a surviving command effect.
                deadline = time.monotonic() + 10
                while True:
                    try:
                        with guard.canonical_access(root, write=True):
                            release.write_text("the writer now owns the source")
                        break
                    except ValueError:
                        if time.monotonic() >= deadline:
                            self.fail("command cleanup did not release the source lease")
                        time.sleep(0.02)
                time.sleep(1)
                self.assertFalse(effect.exists(), "wrapper death released the lease while its command survived")
            finally:
                if process.is_alive():
                    process.terminate(); process.join(5)
                if group is not None:
                    try:
                        os.killpg(group, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_command_exit_is_preserved_without_creating_control_files(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.assertEqual(7, guard.run_command(root, [sys.executable, "-c", "raise SystemExit(7)"]))
            self.assertEqual([], list(root.iterdir()))

    def test_command_signal_exit_is_preserved_and_spawn_failure_rejects(self):
        import signal
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.assertEqual(-signal.SIGKILL, guard.run_command(root, [sys.executable, "-c",
                              "import os,signal; os.kill(os.getpid(),signal.SIGKILL)"]))
            self.assertNotEqual(0, guard.run_command(root, [str(root / "absent-command")]))
            with guard.canonical_access(root, write=True):
                pass
            self.assertEqual([], list(root.iterdir()))

    def test_natural_leader_exit_cannot_leave_a_descendant_effect(self):
        import signal
        import tempfile
        import time
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            ready, release, effect = root / "ready.json", root / "release", root / "orphan-effect"
            descendant = ("import os,json,time; from pathlib import Path; "
                          f"Path({str(ready.with_suffix('.pending'))!r}).write_text(json.dumps({{'group':os.getpgrp()}})); "
                    f"os.replace({str(ready.with_suffix('.pending'))!r}, {str(ready)!r}); "
                          f"release=Path({str(release)!r}); "
                          "exec('while not release.exists(): time.sleep(0.02)'); "
                          f"Path({str(effect)!r}).write_text('escaped')")
            leader = (f"import subprocess,sys,time; from pathlib import Path; "
                      f"subprocess.Popen([sys.executable,'-c',{descendant!r}]); "
                      f"ready=Path({str(ready)!r}); "
                      "exec('while not ready.exists(): time.sleep(0.02)')")
            group = None
            try:
                self.assertEqual(0, guard.run_command(root, [sys.executable, "-c", leader]))
                self.assertTrue(ready.exists())
                group = json.loads(ready.read_text())["group"]
                with guard.canonical_access(root, write=True):
                    release.write_text("writer now owns source")
                time.sleep(0.5)
                self.assertFalse(effect.exists())
            finally:
                if group is not None:
                    try:
                        os.killpg(group, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_interrupted_command_group_cannot_leave_a_descendant_effect(self):
        import signal
        import tempfile
        import time
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            ready, release, effect = root / "ready.json", root / "release", root / "orphan-effect"
            code = ("import os,json,time; from pathlib import Path; "
                    f"Path({str(ready.with_suffix('.pending'))!r}).write_text(json.dumps({{'group':os.getpgrp()}})); "
                    f"os.replace({str(ready.with_suffix('.pending'))!r}, {str(ready)!r}); "
                    f"release=Path({str(release)!r}); "
                    "exec('while not release.exists(): time.sleep(0.02)'); "
                    f"Path({str(effect)!r}).write_text('escaped'); time.sleep(30)")
            parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{code!r}]); time.sleep(30)"
            def child():
                try:
                    guard.run_command(root, [sys.executable, "-c", parent])
                except KeyboardInterrupt:
                    os._exit(72)
            process = multiprocessing.get_context("fork").Process(target=child)
            process.start()
            group = None
            try:
                deadline = time.monotonic() + 30
                while not ready.exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(ready.exists(), "descendant never became ready")
                group = json.loads(ready.read_text())["group"]
                os.kill(process.pid, signal.SIGINT)
                process.join(30)
                self.assertFalse(process.is_alive())
                self.assertEqual(72, process.exitcode)
                release.write_text("effect is now possible only for an escaped descendant")
                time.sleep(0.5)
                self.assertFalse(effect.exists())
                with guard.canonical_access(root, write=True):
                    pass
            finally:
                if process.is_alive():
                    process.terminate(); process.join(5)
                if group is not None:
                    try:
                        os.killpg(group, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_read_lease_is_nonwriting_and_excludes_writer(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with guard.canonical_access(root):
                with guard.canonical_access(root):
                    self.assertEqual([], list(root.iterdir()))
                with self.assertRaisesRegex(ValueError, "directory lock"):
                    with guard.canonical_access(root, write=True):
                        self.fail("writer entered a read lease")
            self.assertEqual([], list(root.iterdir()))

    def test_unknown_pending_marker_is_preserved_and_refuses_reads(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve(); (root / "build").mkdir()
            (root / guard.ACTIVE).write_text("preserve unknown bytes\n")
            with self.assertRaisesRegex(ValueError, "pending"):
                with guard.canonical_access(root):
                    self.fail("unknown marker admitted")
            with self.assertRaises(ValueError):
                transaction.rollback(root)
            self.assertEqual("preserve unknown bytes\n", (root / guard.ACTIVE).read_text())


if __name__ == "__main__":
    unittest.main()
