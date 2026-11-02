"""Owned publication-process fixtures; no release, reviewer or experiment work."""
import contextlib
import io
import importlib.util
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_publication as publication
import validation_runtime as runtime
from admission_guard import canonical_access


class SeparateLogTests(unittest.TestCase):
    def test_binary_stdout_stderr_and_child_exit_remain_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = runtime.execute([sys.executable, "-c",
                "import os,sys; os.write(1,b'a\\0b\\0'); os.write(2,b'warning\\n'); sys.exit(7)"],
                cwd=root, log=root / "stdout", stderr_log=root / "stderr", timeout=5)
            self.assertEqual("failed", result["status"])
            self.assertEqual(7, result["exit_code"])
            self.assertEqual(b"a\0b\0", (root / "stdout").read_bytes())
            self.assertEqual(b"warning\n", (root / "stderr").read_bytes())
            self.assertEqual(4, result["log_bytes"])
            self.assertEqual(8, result["stderr_log_bytes"])
            self.assertEqual(12, result["retained_log_bytes"])

    def test_total_retention_budget_drains_both_channels(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = runtime.execute([sys.executable, "-c",
                "import os; os.write(1,b'o'*200000); os.write(2,b'e'*200000)"],
                cwd=root, log=root / "stdout", stderr_log=root / "stderr", timeout=5,
                max_log_bytes=1024)
            self.assertEqual("passed", result["status"])
            self.assertTrue(result["log_truncated"])
            self.assertEqual(1024, sum((root / name).stat().st_size for name in ("stdout", "stderr")))
            self.assertEqual(1024, result["retained_log_bytes"])

    def test_unwritable_second_log_refuses_before_child_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "stderr-directory").mkdir()
            marker = root / "must-not-start"
            command = [sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).write_text('started')"]
            with patch.object(runtime.subprocess, "Popen", wraps=subprocess.Popen) as launch:
                with self.assertRaises(IsADirectoryError):
                    runtime.execute(command, cwd=root, log=root / "stdout",
                                    stderr_log=root / "stderr-directory", timeout=5)
                launch.assert_not_called()
            self.assertFalse(marker.exists())


class PublicationProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="asi-publication-process-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "scripts").mkdir()
        self.root_patch = patch.object(publication, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.quiet = contextlib.redirect_stdout(io.StringIO())
        self.quiet.__enter__()
        self.addCleanup(self.quiet.__exit__, None, None, None)

    def write_check(self, body):
        (self.root / "scripts/check.py").write_text(body)

    def wait_for_write_lease(self, root=None):
        root = root or self.root
        deadline = time.monotonic() + 10
        while True:
            try:
                with canonical_access(root, write=True):
                    return
            except ValueError:
                if time.monotonic() >= deadline:
                    self.fail("guarded command did not release its source lease")
                time.sleep(.02)

    def test_exact_interpreter_and_repeated_logs_are_retained(self):
        self.write_check("import sys; print(sys.prefix); print('stderr evidence',file=sys.stderr)")
        commands = publication.PublicationProcesses(self.root)
        publication.run_validator("check.py", commands)
        publication.run_validator("check.py", commands)
        rows = json.loads((commands.directory / "results.json").read_text())
        self.assertEqual(2, len(rows))
        self.assertNotEqual(rows[0]["log"], rows[1]["log"])
        for row in rows:
            self.assertEqual("passed", row["status"])
            self.assertEqual(sys.executable, row["inner_command"][0])
            self.assertEqual(sys.prefix, Path(row["log"]).read_text().strip())
            self.assertEqual("stderr evidence\n", Path(row["stderr_log"]).read_text())
        self.wait_for_write_lease()

    def test_real_git_nul_protocol_preserves_spaces_and_newlines(self):
        env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
        subprocess.run(["git", "init", str(self.root)], env=env, capture_output=True, check=True, timeout=10)
        names = ["file with spaces.txt", "file\nwith newline.txt"]
        for name in names:
            (self.root / name).write_text("owned fixture")
        subprocess.run(["git", "-C", str(self.root), "add", "--", *names], env=env,
                       capture_output=True, check=True, timeout=10)
        self.assertEqual(sorted(names), sorted(publication.git_ls_files()))

    def test_git_protocol_refusal_is_machine_visible_even_with_zero_exit(self):
        binary = self.root / "bin"
        binary.mkdir()
        git = binary / "git"
        for label, body in (("unterminated", b"missing delimiter"), ("empty segment", b"first\0\0"),
                            ("truncated", b"x" * (4 * 1024 * 1024) + b"\0")):
            with self.subTest(label=label):
                git.write_text(f"#!{sys.executable}\nimport os\nos.write(1,{body!r})\nos.write(2,b'warning is not a filename\\n')\n")
                git.chmod(0o755)
                commands = publication.PublicationProcesses(self.root)
                with patch.dict(os.environ, {"PATH": str(binary) + os.pathsep + os.environ.get("PATH", "")}):
                    with self.assertRaises(SystemExit) as exit_state:
                        publication.git_ls_files(commands)
                self.assertEqual(1, exit_state.exception.code)
                row = json.loads((commands.directory / "results.json").read_text())[-1]
                self.assertEqual("failed", row["status"])
                self.assertEqual("passed", row["process_status"])
                self.assertEqual(0, row["exit_code"])
                self.assertIn(row["diagnostic_id"], {"invalid_git_protocol", "invalid_or_truncated_git_protocol"})
                if label == "truncated":
                    self.assertTrue(row["log_truncated"])
                    self.assertEqual(4 * 1024 * 1024, row["retained_log_bytes"])
                else:
                    self.assertEqual(b"warning is not a filename\n", Path(row["stderr_log"]).read_bytes())

    def test_stuck_subcheck_times_out_and_stops_its_descendant(self):
        ready = self.root / "descendant-ready"
        effect = self.root / "must-not-escape"
        descendant = (f"import time;from pathlib import Path;Path({str(ready)!r}).write_text('ready');"
                      f"time.sleep(4);Path({str(effect)!r}).write_text('escaped');time.sleep(30)")
        self.write_check(f"import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c',{descendant!r}])\nprint('leader ready',flush=True)\ntime.sleep(30)\n")
        commands = publication.PublicationProcesses(self.root)
        with patch.object(publication, "CHILD_BUDGET_SECONDS", 2):
            with self.assertRaises(SystemExit):
                publication.run_validator("check.py", commands)
        row = json.loads((commands.directory / "results.json").read_text())[-1]
        self.assertEqual("timed_out", row["status"])
        self.assertEqual("timed_out", row["diagnostic_id"])
        self.assertTrue(ready.exists(), "fixture did not exercise a live descendant")
        self.assertIn("leader ready", Path(row["log"]).read_text())
        self.wait_for_write_lease()
        time.sleep(4.1)
        self.assertFalse(effect.exists())

    def parent_death_case(self, death_signal):
        ready, release, effect = [self.root / name for name in ("ready.json", "release", "effect")]
        self.write_check("import json,os,time\nfrom pathlib import Path\n"
            f"Path({str(ready.with_suffix('.pending'))!r}).write_text(json.dumps({{'group':os.getpgrp()}}))\n"
            f"os.replace({str(ready.with_suffix('.pending'))!r},{str(ready)!r})\n"
            f"while not Path({str(release)!r}).exists(): time.sleep(.02)\n"
            f"Path({str(effect)!r}).write_text('escaped parent')\ntime.sleep(30)\n")
        source = Path(publication.__file__).resolve().parent
        code = (f"import sys\nfrom pathlib import Path\nsys.path.insert(0,{str(source)!r})\n"
                f"import validate_publication as p\np.ROOT=Path({str(self.root)!r})\np.run_validator('check.py')\n")
        parent = subprocess.Popen([sys.executable, "-c", code], start_new_session=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        group = None
        try:
            deadline = time.monotonic() + 10
            while not ready.exists() and time.monotonic() < deadline:
                time.sleep(.02)
            self.assertTrue(ready.exists(), "guarded payload did not start")
            group = json.loads(ready.read_text())["group"]
            os.kill(parent.pid, death_signal)
            parent.wait(timeout=10)
            self.wait_for_write_lease()
            journals = list((self.root / "build").glob("publication-source-*/results.json"))
            self.assertEqual(1, len(journals))
            self.assertEqual("running", json.loads(journals[0].read_text())[-1]["status"])
            release.write_text("effect now possible only for an escaped payload")
            time.sleep(.3)
            self.assertFalse(effect.exists())
        finally:
            if parent.poll() is None:
                parent.kill()
            parent.wait(timeout=5)
            if group is not None:
                try:
                    os.killpg(group, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_parent_sigkill_does_not_abandon_guarded_payload(self):
        self.parent_death_case(signal.SIGKILL)

    def test_parent_sigterm_does_not_abandon_guarded_payload(self):
        self.parent_death_case(signal.SIGTERM)

    def test_linked_log_parent_preserves_foreign_directory(self):
        foreign = self.root / "foreign-fixture"
        foreign.mkdir()
        sentinel = foreign / "keep"
        sentinel.write_bytes(b"retain foreign fixture")
        (self.root / "build").symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, "link"):
            publication.PublicationProcesses(self.root)
        self.assertEqual(["keep"], [p.name for p in foreign.iterdir()])
        self.assertEqual(b"retain foreign fixture", sentinel.read_bytes())


class SharedGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="asi-shared-guard-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.cwd = self.root / "lean"
        self.cwd.mkdir()
        (self.root / "build").mkdir()

    def execute(self, code, budget=5):
        return runtime.execute_guarded([sys.executable, "-c", code], source_root=self.root,
            cwd=self.cwd, log=self.root / "build/stdout", stderr_log=self.root / "build/stderr",
            timeout=budget)

    def lease_released(self):
        deadline = time.monotonic() + 10
        while True:
            try:
                with canonical_access(self.root, write=True):
                    return
            except ValueError:
                if time.monotonic() > deadline:
                    self.fail("payload source-root lease remains unresolved")
                time.sleep(.02)

    def test_nested_cwd_preserves_root_lease_interpreter_and_private_fds(self):
        result, data = self.descriptor_observation(runtime)
        self.assertEqual("passed", result["status"])
        self.assertEqual(str(self.cwd), data["cwd"])
        self.assertEqual(sys.prefix, data["prefix"])
        self.assertTrue(data["blocked"], "lease incorrectly bound only to lean cwd")
        self.assertEqual([], data["private_leaks"], data)
        self.assertEqual("separate evidence\n", (self.root / "build/stderr").read_text())
        self.lease_released()

    def descriptor_observation(self, executor):
        # Enumerate the live private object identities, not all descriptors.
        # Emulators may open their own executable/runtime handles after exec.
        manifest = self.root / "private-descriptor-identities.json"
        setup = ("import json,stat\n"
                 "def fingerprint(s): return [s.st_dev,s.st_ino,stat.S_IFMT(s.st_mode)]\n"
                 "private=[fingerprint(Path(sys.argv[2]).stat()),fingerprint(os.fstat(int(sys.argv[1])))]\n"
                 "original_pipe=os.pipe\n"
                 "def observed_pipe():\n"
                 "    pair=original_pipe()\n"
                 "    private.append(fingerprint(os.fstat(pair[0])))\n"
                 f"    Path({str(manifest)!r}).write_text(json.dumps(private))\n"
                 "    return pair\n"
                 "os.pipe=observed_pipe\n")
        original_execute = executor.execute
        def observe(command, **kwargs):
            command = command[:]
            needle = "raise SystemExit(run_command(Path(sys.argv[2]),sys.argv[3:],cwd=Path.cwd()))"
            self.assertEqual(1, command[2].count(needle))
            command[2] = command[2].replace(needle, setup + needle)
            return original_execute(command, **kwargs)
        code = ("import os,sys,json,fcntl,stat\nfrom pathlib import Path\n"
                f"private={{tuple(v) for v in json.loads(Path({str(manifest)!r}).read_text())}}\n"
                f"fd=os.open({str(self.root)!r},os.O_RDONLY|os.O_DIRECTORY)\n"
                "try:\n fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB); blocked=False\n"
                "except BlockingIOError: blocked=True\n"
                "os.close(fd)\nopened=[]\nleaks=[]\n"
                "for candidate in range(3,256):\n"
                " try:\n"
                "  s=os.fstat(candidate); identity=(s.st_dev,s.st_ino,stat.S_IFMT(s.st_mode))\n"
                "  opened.append({'fd':candidate,'identity':identity})\n"
                "  if identity in private: leaks.append({'fd':candidate,'identity':identity})\n"
                " except OSError: pass\n"
                "print(json.dumps({'cwd':str(Path.cwd()),'prefix':sys.prefix,'blocked':blocked,'fds':opened,'private_leaks':leaks}))\n"
                "print('separate evidence',file=sys.stderr)\n")
        with patch.object(executor, "execute", side_effect=observe):
            result = executor.execute_guarded([sys.executable, "-c", code], source_root=self.root,
                cwd=self.cwd, log=self.root / "build/stdout", stderr_log=self.root / "build/stderr", timeout=5)
        data = json.loads((self.root / "build/stdout").read_text())
        return result, data

    def test_descriptor_oracle_rejects_actual_leaked_lease_and_control(self):
        # Authored broken producer, confined to this fixture's helper copies.
        import admission_guard as guard
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "validation_runtime.py").write_bytes(Path(runtime.__file__).read_bytes())
        source = Path(guard.__file__).read_text()
        needle = "process = subprocess.Popen(command, cwd=directory, start_new_session=True)"
        self.assertEqual(1, source.count(needle))
        source = source.replace(needle, "process = subprocess.Popen(command, cwd=directory, start_new_session=True, pass_fds=(lease, control))")
        (scripts / "admission_guard.py").write_text(source)
        spec = importlib.util.spec_from_file_location("authored_leaking_runtime", scripts / "validation_runtime.py")
        mutant = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mutant)
        result, data = self.descriptor_observation(mutant)
        self.assertEqual("passed", result["status"], "fixture must reach the payload")
        kinds = {row["identity"][2] for row in data["private_leaks"]}
        self.assertIn(stat.S_IFDIR, kinds, "oracle missed the leaked source lease")
        self.assertIn(stat.S_IFIFO, kinds, "oracle missed the leaked private control pipe")
        self.lease_released()

    def test_outside_dotdot_missing_and_linked_cwd_refuse_before_launch(self):
        outside = self.root.parent
        linked = self.root / "linked"
        linked.symlink_to(self.cwd)
        marker = self.root / "must-not-start"
        command = [sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).write_text('bad')"]
        for cwd in [outside, self.cwd / "../..", linked, self.root / "missing"]:
            with self.subTest(cwd=cwd), patch.object(runtime.subprocess, "Popen", wraps=subprocess.Popen) as launch:
                with self.assertRaises(ValueError):
                    runtime.execute_guarded(command, source_root=self.root, cwd=cwd,
                                            log=self.root / "build/stdout", timeout=5)
                launch.assert_not_called()
                self.assertFalse(marker.exists())

    def death_case(self, death_signal):
        ready, release, effect = [self.root / name for name in ("ready", "release", "effect")]
        payload = ("import os,json,time\nfrom pathlib import Path\n"
                   f"Path({str(ready.with_suffix('.pending'))!r}).write_text(json.dumps({{'group':os.getpgrp()}}))\n"
                   f"os.replace({str(ready.with_suffix('.pending'))!r},{str(ready)!r})\n"
                   f"while not Path({str(release)!r}).exists(): time.sleep(.02)\n"
                   f"Path({str(effect)!r}).write_text('escaped')\ntime.sleep(30)\n")
        source = Path(runtime.__file__).resolve().parent
        code = (f"import sys\nfrom pathlib import Path\nsys.path.insert(0,{str(source)!r})\n"
                "from validation_runtime import execute_guarded\n"
                f"execute_guarded([sys.executable,'-c',{payload!r}],source_root=Path({str(self.root)!r}),"
                f"cwd=Path({str(self.cwd)!r}),log=Path({str(self.root / 'build/stdout')!r}),timeout=30)\n")
        parent = subprocess.Popen([sys.executable, "-c", code], start_new_session=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        group = None
        try:
            deadline = time.monotonic() + 10
            while not ready.exists() and time.monotonic() < deadline:
                time.sleep(.02)
            self.assertTrue(ready.exists())
            group = json.loads(ready.read_text())["group"]
            with self.assertRaises(ValueError):
                with canonical_access(self.root, write=True):
                    pass
            os.kill(parent.pid, death_signal)
            parent.wait(timeout=10)
            self.lease_released()
            release.write_text("only an escaped payload can now act")
            time.sleep(.3)
            self.assertFalse(effect.exists())
        finally:
            if parent.poll() is None:
                parent.kill()
            parent.wait(timeout=5)
            if group is not None:
                try:
                    os.killpg(group, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_nested_cwd_owner_sigkill_stops_payload_and_releases_root(self):
        self.death_case(signal.SIGKILL)

    def test_nested_cwd_owner_sigterm_stops_payload_and_releases_root(self):
        self.death_case(signal.SIGTERM)

    def test_nested_cwd_deadline_stops_ready_descendant(self):
        ready, release, effect = [self.root / name for name in ("ready", "release", "effect")]
        payload = ("import time\nfrom pathlib import Path\n"
                   f"Path({str(ready)!r}).write_text('ready')\n"
                   f"while not Path({str(release)!r}).exists(): time.sleep(.02)\n"
                   f"Path({str(effect)!r}).write_text('escaped')\ntime.sleep(30)\n")
        result = self.execute(f"import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c',{payload!r}])\nprint('ready leader',flush=True)\ntime.sleep(30)", budget=2)
        self.assertEqual("timed_out", result["status"])
        self.assertTrue(ready.exists())
        self.lease_released()
        release.write_text("effect only possible after deadline")
        time.sleep(.3)
        self.assertFalse(effect.exists())
        self.assertIn("ready leader", (self.root / "build/stdout").read_text())

    def test_log_setup_refusal_closes_both_owner_pipe_descriptors(self):
        directory = self.root / "build/not-a-log"
        directory.mkdir()
        real_pipe = os.pipe
        descriptors = []
        def record_pipe():
            pair = real_pipe()
            descriptors.extend(pair)
            return pair
        with patch.object(runtime.os, "pipe", side_effect=record_pipe):
            with self.assertRaises(IsADirectoryError):
                runtime.execute_guarded([sys.executable, "-c", "raise RuntimeError('must not run')"],
                    source_root=self.root, cwd=self.cwd, log=self.root / "build/stdout",
                    stderr_log=directory, timeout=5)
        self.assertEqual(2, len(descriptors))
        for fd in descriptors:
            with self.assertRaises(OSError):
                os.fstat(fd)


class CompilerDiagnosticTests(unittest.TestCase):
    def axiom_protocol_case(self, *, wrong_version):
        import build_proof_axiom_audit as module
        with tempfile.TemporaryDirectory(prefix="asi-axiom-protocol-") as temporary:
            root = Path(temporary).resolve()
            (root / "lean").mkdir()
            tool = root / "lean/tools/AxiomDependencies.lean"
            tool.parent.mkdir()
            tool.write_text("-- owned compiler protocol fixture\n")
            (root / "lean/lean-toolchain").write_text("leanprover/lean4:v4.31.0\n")
            binary = root / "bin"
            binary.mkdir()
            lake = binary / "lake"
            version = "9.9.9" if wrong_version else "4.31.0"
            lake.write_text(f"#!{sys.executable}\nimport sys\n"
                f"if '--version' in sys.argv: print('Lean (version {version}, authored fixture)')\n"
                "elif sys.argv[1]=='build': print('authored fixture build')\n"
                "else: print('malformed environment rather than JSON')\n")
            lake.chmod(0o755)
            code = "compiler_identity_unverified" if wrong_version else "invalid_axiom_environment"
            stage = "compiler-version" if wrong_version else "environment"
            with patch.object(module, "ROOT", root), patch.object(module, "TOOL", tool), \
                 patch.dict(os.environ, {"PATH": str(binary) + os.pathsep + os.environ.get("PATH", "")}):
                with self.assertRaisesRegex(ValueError, code):
                    module.build()
            directories = list((root / "build/proof_axiom_audit").glob("run-*"))
            self.assertEqual(1, len(directories))
            result = json.loads((directories[0] / (stage + "-execution.json")).read_text())
            self.assertEqual("failed", result["status"])
            self.assertEqual("passed", result["process_status"])
            self.assertEqual(0, result["exit_code"])
            self.assertEqual(code, result["diagnostic_id"])
            if wrong_version:
                self.assertFalse((directories[0] / "environment-execution.json").exists())
            else:
                self.assertIn("malformed environment", Path(result["log"]).read_text())

    def test_zero_exit_wrong_compiler_identity_is_machine_visible_failure(self):
        self.axiom_protocol_case(wrong_version=True)

    def test_zero_exit_invalid_axiom_environment_is_machine_visible_failure(self):
        self.axiom_protocol_case(wrong_version=False)

    def test_axiom_diagnostic_link_refuses_before_compiler_launch(self):
        import build_proof_axiom_audit as module
        with tempfile.TemporaryDirectory(prefix="asi-axiom-output-refusal-") as temporary:
            root = Path(temporary).resolve()
            (root / "build").mkdir()
            tool = root / "lean/tools/AxiomDependencies.lean"
            tool.parent.mkdir(parents=True)
            tool.write_text("-- owned compiler output fixture\n")
            foreign = root / "foreign"
            foreign.mkdir()
            (foreign / "keep").write_bytes(b"foreign diagnostics")
            (root / "build/proof_axiom_audit").symlink_to(foreign)
            with patch.object(module, "ROOT", root), patch.object(module, "TOOL", tool), \
                 patch.object(runtime.subprocess, "Popen") as launch:
                with self.assertRaisesRegex(ValueError, "canonical admission must not traverse a link"):
                    module.build()
                launch.assert_not_called()
            self.assertEqual(["keep"], [p.name for p in foreign.iterdir()])
            self.assertEqual(b"foreign diagnostics", (foreign / "keep").read_bytes())

    def check_compiler_refusal(self, module, function, source_attribute, source_name, diagnostic_prefix):
        with tempfile.TemporaryDirectory(prefix="asi-compiler-refusal-") as temporary:
            root = Path(temporary).resolve()
            lean = root / "lean"
            lean.mkdir()
            source = lean / source_name
            source.write_bytes(getattr(module, source_attribute).read_bytes())
            binary = root / "bin"
            binary.mkdir()
            lake = binary / "lake"
            lake.write_text(f"#!{sys.executable}\nimport sys\nprint('authored compiler refusal',file=sys.stderr)\nsys.exit(7)\n")
            lake.chmod(0o755)
            errors = []
            with patch.object(module, "ROOT", root), patch.object(module, "LEAN_ROOT", lean), \
                 patch.object(module, source_attribute, source), \
                 patch.dict(os.environ, {"PATH": str(binary) + os.pathsep + os.environ.get("PATH", "")}), \
                 contextlib.redirect_stdout(io.StringIO()):
                getattr(module, function)(errors)
            self.assertEqual(1, len(errors), errors)
            self.assertIn("failed (unit_rejected)", errors[0])
            directories = list((root / "build").glob(diagnostic_prefix + "-*"))
            self.assertEqual(1, len(directories))
            result = json.loads((directories[0] / "result.json").read_text())
            self.assertEqual("failed", result["status"])
            self.assertEqual(7, result["exit_code"])
            self.assertEqual(300, result["timeout_seconds"])
            self.assertIn("authored compiler refusal", (directories[0] / "compiler.log").read_text())

    def test_proof_envelope_compile_refusal_is_classified_with_retained_log(self):
        import validate_proof_artifact_audit as module
        self.check_compiler_refusal(module, "validate_proof_lease_lifecycle", "PROOF_ENVELOPE",
                                    "ProofEnvelope.lean", "proof-envelope-compile")

    def test_living_book_compile_refusal_is_classified_with_retained_log(self):
        import validate_living_book_change_packets as module
        self.check_compiler_refusal(module, "validate_formal_lifecycle", "LEAN",
                                    "LivingBook.lean", "living-book-compile")


if __name__ == "__main__":
    unittest.main()
