"""Reject unsafe installer archives before any executable can run."""

import copy
import contextlib
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install_lean_runtime import binary_record, extract_verified, require_current_review, version_matches
import install_lean_runtime as installer


class LeanRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def archive(self, names, *, linked=False):
        path = self.root / "archive.tar.gz"
        with tarfile.open(path, "w:gz") as archive:
            for name in names:
                member = tarfile.TarInfo(name)
                if linked:
                    member.type = tarfile.SYMTYPE
                    member.linkname = "../outside"
                    archive.addfile(member)
                else:
                    data = b"a bounded authored executable fixture"
                    member.size = len(data)
                    archive.addfile(member, io.BytesIO(data))
        return path, {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}

    def test_digest_mismatch_cannot_materialize_an_executable(self):
        path, artifact = self.archive(["elan-init"])
        artifact["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            extract_verified(path, artifact, self.root)
        self.assertFalse((self.root / "elan-init").exists())

    def test_traversal_link_or_extra_payload_cannot_be_extracted(self):
        for names, linked in [(["../outside"], False), (["elan-init"], True), (["elan-init", "extra"], False)]:
            path, artifact = self.archive(names, linked=linked)
            with self.assertRaises(ValueError):
                extract_verified(path, artifact, self.root)
            self.assertFalse((self.root / "elan-init").exists())

    def test_verified_single_executable_is_materialized_without_execution(self):
        path, artifact = self.archive(["elan-init"])
        binary = extract_verified(path, artifact, self.root)
        self.assertEqual(b"a bounded authored executable fixture", binary.read_bytes())
        self.assertEqual(0o755, binary.stat().st_mode & 0o777)

    def test_moving_release_url_or_duplicate_platform_rejects(self):
        target = "x86_64-unknown-linux-gnu"
        record = {"version": "v4.2.4", "source_commit": "1" * 40, "artifacts": [{
            "target": target, "url": f"https://github.com/leanprover/elan/releases/download/v4.2.4/elan-{target}.tar.gz",
            "sha256": "2" * 64, "bytes": 123}]}
        inventory = {"pins": [{"repository": "leanprover/elan", "runtime_binary": record}]}
        self.assertEqual(record, binary_record(inventory))
        for mutate in [lambda row: row["artifacts"][0].update(url="https://github.com/leanprover/elan/releases/latest/download/elan.tar.gz"),
                       lambda row: row["artifacts"].append(copy.deepcopy(row["artifacts"][0]))]:
            candidate = copy.deepcopy(inventory)
            mutate(candidate["pins"][0]["runtime_binary"])
            with self.assertRaises(ValueError):
                binary_record(candidate)

    def test_expired_or_future_review_cannot_open_installer_execution(self):
        inventory = {"review_policy": {"max_review_age_days": 90}, "pins": [{
            "repository": "leanprover/elan", "reviewed_on": "2026-07-10", "review_due_on": "2026-10-08",
            "runtime_binary": {"observed_on": "2026-10-02"}}]}
        require_current_review(inventory, date(2026, 10, 2))
        for as_of in [date(2026, 10, 9), date(2026, 7, 9), date(2026, 10, 1)]:
            with self.assertRaises(ValueError):
                require_current_review(inventory, as_of)

    def test_same_version_with_wrong_source_context_is_not_accepted(self):
        record = {"version": "v4.2.4", "source_commit": "227caca133724d5516bee25c2aeb3e609478f2d8"}
        self.assertTrue(version_matches("elan-init 4.2.4 (227caca13 2026-08-25)", record))
        self.assertFalse(version_matches("elan-init 4.2.4 (different 2026-08-25)", record))
        self.assertFalse(version_matches("elan-init 4.2.3 (227caca13 2026-08-25)", record))

    def runtime_fixture(self):
        (self.root / "lean").mkdir()
        (self.root / "lean/lean-toolchain").write_text("leanprover/lean4:v4.31.0\n")
        inventory = json.loads(installer.INVENTORY.read_text())
        binary = self.root / "elan-init"
        binary.write_text("authored executable placeholder; intercepted before execution")
        return inventory, binary

    def intercepted_execution(self, *, decline_toolchain=False, compiler_version="4.31.0"):
        def run(command, *, cwd, log, timeout):
            log.parent.mkdir(parents=True, exist_ok=True)
            if command[-1] == "--version" and "run" not in command:
                text = "elan-init 4.2.4 (227caca13 2026-08-25)"
            elif "toolchain" in command and "install" in command:
                text = "authored toolchain download refusal" if decline_toolchain else "authored installed toolchain"
                if decline_toolchain:
                    log.write_text(text)
                    return {"status": "failed", "exit_code": 1, "log": str(log)}
            elif "run" in command:
                self.assertNotIn("--install", command)
                self.assertIn("leanprover/lean4:v4.31.0", command)
                text = (f"Lean (version {compiler_version}, aarch64-unknown-linux-gnu, commit fixture, Release)"
                        if command[-2] == "lean" else f"Lake version 5.0.0-src (Lean version {compiler_version})")
            else:
                text = "default toolchain set; compiler not installed by initialization"
            log.write_text(text)
            return {"status": "passed", "exit_code": 0, "log": str(log)}
        return run

    def invoke_fixture(self, inventory, binary, execute):
        output = io.StringIO()
        with patch.object(installer, "ROOT", self.root), patch.object(installer, "INVENTORY", self.root / "inventory.json"), \
             patch.object(installer, "download"), patch.object(installer, "extract_verified", return_value=binary), \
             patch.object(installer, "execute", side_effect=execute), patch.object(installer, "require_current_review"), \
             patch.object(installer, "current_target", return_value="aarch64-unknown-linux-gnu"), \
             patch.object(sys, "argv", ["install_lean_runtime.py", "--install", "--elan-home", str(self.root / "tool-home")]), \
             contextlib.redirect_stdout(output):
            (self.root / "inventory.json").write_text(json.dumps(inventory))
            installer.main()
        return output.getvalue()

    def test_default_selection_cannot_claim_ready_when_toolchain_install_declines(self):
        inventory, binary = self.runtime_fixture()
        with self.assertRaisesRegex(ValueError, "toolchain provisioning"):
            self.invoke_fixture(inventory, binary, self.intercepted_execution(decline_toolchain=True))

    def test_wrong_compiler_version_rejects_after_successful_toolchain_install(self):
        inventory, binary = self.runtime_fixture()
        with self.assertRaisesRegex(ValueError, "does not report the pinned"):
            self.invoke_fixture(inventory, binary, self.intercepted_execution(compiler_version="4.30.0"))


if __name__ == "__main__":
    unittest.main()
