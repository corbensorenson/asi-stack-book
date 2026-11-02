"""Public reader replacement keeps complete custody across bounded failures."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_human_reader_public_site as reader


class ReaderSiteTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.site = self.root / "site"
        self.site.mkdir()
        (self.site / "technical.html").write_text("technical fixture\n")
        self.rendered = self.root / "rendered"
        self.rendered.mkdir()
        (self.rendered / "chapters").mkdir()
        (self.rendered / "index.html").write_text('<a href="chapters/unit.html">Unit</a>')
        (self.rendered / "chapters/unit.html").write_text(
            'Unit Title asi-edition-switch AI / researcher Human Reader '
            '<a href="../../technical.html">Technical</a> old complete payload\n')
        self.crosswalk = self.root / "crosswalk.json"
        self.crosswalk.write_text(json.dumps({"edition_id": "fixture-edition", "units": [{
            "public_path": "reader/chapters/unit.html", "unit_id": "unit", "title": "Unit Title", "owners": [{
                "chapter_id": "owner", "technical_source_file": "chapters/owner.qmd", "live_technical_path": "technical.html"}]}]}))
        self.patches = [patch.object(reader, "RENDERED", self.rendered), patch.object(reader, "CROSSWALK", self.crosswalk)]
        for patched in self.patches:
            patched.start()
            self.addCleanup(patched.stop)
        reader.install(self.site)
        self.destination = self.site / "reader"
        self.before = reader.file_rows(self.destination)

    def update(self):
        page = self.rendered / "chapters/unit.html"
        page.write_text(page.read_text().replace("old complete payload", "new complete payload"))

    def stages(self):
        return list(self.root.glob(".site-reader-stage-*"))

    def test_complete_atomic_replacement_noops_and_readonly_check(self):
        self.update()
        reader.install(self.site)
        self.assertIn("new complete payload", (self.destination / "chapters/unit.html").read_text())
        times = {path: path.stat().st_mtime_ns for path in self.destination.rglob("*")}
        reader.install(self.site, check=True)
        reader.install(self.site)
        self.assertEqual(times, {path: path.stat().st_mtime_ns for path in self.destination.rglob("*")})
        self.assertEqual([], self.stages())
        self.assertFalse((self.site / ".site.lock").exists())
        self.assertTrue((self.root / ".site.lock").is_file())

    def test_source_copy_failure_keeps_complete_previous_reader(self):
        self.update()
        with patch.object(reader.shutil, "copytree", side_effect=OSError("copy interrupted")):
            with self.assertRaises(OSError):
                reader.install(self.site)
        self.assertEqual(self.before, reader.file_rows(self.destination))
        self.assertEqual([], self.stages())

    def test_noop_cannot_adopt_an_edit_after_the_ownership_check(self):
        inspect = reader.previous_is_owned
        page = self.destination / "chapters/unit.html"
        def changed(*args, **kwargs):
            result = inspect(*args, **kwargs)
            page.write_text(page.read_text() + " concurrent authored edit")
            return result
        original = page.read_text()
        for check in (False, True):
            with self.subTest(check=check):
                page.write_text(original)
                with patch.object(reader, "previous_is_owned", side_effect=changed):
                    with self.assertRaisesRegex(ValueError, "changed"):
                        reader.install(self.site, check=check)
                self.assertIn("concurrent authored edit", page.read_text())

    def test_unknown_empty_directory_is_preserved(self):
        empty = self.destination / "personal-empty"
        empty.mkdir()
        identity = (empty.stat().st_dev, empty.stat().st_ino)
        self.update()
        with self.assertRaisesRegex(ValueError, "directory"):
            reader.install(self.site)
        self.assertEqual(identity, (empty.stat().st_dev, empty.stat().st_ino))
        self.assertIn("old complete payload", (self.destination / "chapters/unit.html").read_text())

    def test_post_swap_exception_or_prior_edit_preserves_displaced_reader(self):
        self.update()
        exchange = reader.exchange_directories
        def interrupted(left, right):
            (right / "personal-empty").mkdir()
            exchange(left, right)
            raise OSError("authored post-swap exception")
        with patch.object(reader, "exchange_directories", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "post-swap"):
                reader.install(self.site)
        stage = self.stages()[0]
        self.assertTrue((stage / "reader/personal-empty").is_dir())
        self.assertIn("old complete payload", (stage / "reader/chapters/unit.html").read_text())
        self.assertIn("new complete payload", (self.destination / "chapters/unit.html").read_text())
        self.assertEqual("installation_outcome_unconfirmed", json.loads((stage / "staging.json").read_bytes())["state"])

    def test_absent_reader_destination_race_preserves_new_empty_directory(self):
        # Delete only this test's previously installed fixture.
        shutil.rmtree(self.destination)
        rename = reader.install_directory_noreplace
        identity = None
        def collided(left, right):
            nonlocal identity
            right.mkdir()
            identity = (right.stat().st_dev, right.stat().st_ino)
            rename(left, right)
        with patch.object(reader, "install_directory_noreplace", side_effect=collided):
            with self.assertRaises(FileExistsError):
                reader.install(self.site)
        self.assertEqual(identity, (self.destination.stat().st_dev, self.destination.stat().st_ino))
        self.assertEqual([], list(self.destination.iterdir()))

    def test_invalid_render_or_broken_staged_link_keeps_previous(self):
        page = self.rendered / "chapters/unit.html"
        original = page.read_text()
        for content in (original.replace("Human Reader", "missing required fragment"),
                        original + '<a href="missing.html">Missing target</a>'):
            page.write_text(content)
            with self.assertRaises(ValueError):
                reader.install(self.site)
            self.assertEqual(self.before, reader.file_rows(self.destination))

    def test_escape_link_and_source_links_refuse_without_outside_bytes(self):
        sentinel = self.root / "private.txt"
        sentinel.write_text("never copy private fixture")
        page = self.rendered / "chapters/unit.html"
        original = page.read_text()
        page.write_text(original + '<a href="../../../private.txt">Escaping target</a>')
        with self.assertRaisesRegex(ValueError, "escapes"):
            reader.install(self.site)
        page.write_text(original)
        link = self.rendered / "link"
        link.symlink_to(sentinel)
        with patch.object(reader.shutil, "copytree") as copy:
            with self.assertRaisesRegex(ValueError, "symlink"):
                reader.install(self.site)
        copy.assert_not_called()
        self.assertEqual(self.before, reader.file_rows(self.destination))

    def test_render_or_crosswalk_drift_during_copy_keeps_previous(self):
        self.update()
        original_copy = shutil.copytree
        for kind in ("render", "crosswalk"):
            crosswalk_before = self.crosswalk.read_bytes()
            def mutate(*args, **kwargs):
                result = original_copy(*args, **kwargs)
                if Path(args[0]) == self.rendered:
                    if kind == "render":
                        self.update()
                        (self.rendered / "index.html").write_text("changed during copy\n")
                    else:
                        self.crosswalk.write_bytes(crosswalk_before + b"\n")
                return result
            with patch.object(reader.shutil, "copytree", side_effect=mutate):
                with self.assertRaisesRegex(ValueError, "changed"):
                    reader.install(self.site)
            self.assertEqual(self.before, reader.file_rows(self.destination))
            self.crosswalk.write_bytes(crosswalk_before)

    def test_unknown_prior_content_and_damaged_receipt_are_preserved(self):
        sentinel = self.destination / "personal.txt"
        sentinel.write_text("keep")
        with self.assertRaisesRegex(ValueError, "integrity"):
            reader.install(self.site)
        self.assertEqual("keep", sentinel.read_text())
        sentinel.unlink()
        receipt = self.destination / reader.INSTALL_MANIFEST
        receipt.write_text('{"schema_version":"unknown"}')
        with self.assertRaisesRegex(ValueError, "integrity"):
            reader.install(self.site)
        self.assertEqual('{"schema_version":"unknown"}', receipt.read_text())

    def test_legacy_adoption_requires_exact_known_payload(self):
        (self.destination / reader.INSTALL_MANIFEST).unlink()
        with self.assertRaisesRegex(ValueError, "stale"):
            reader.install(self.site, check=True)
        reader.install(self.site)
        self.assertTrue((self.destination / reader.INSTALL_MANIFEST).is_file())
        (self.destination / reader.INSTALL_MANIFEST).unlink()
        self.update()
        with self.assertRaisesRegex(ValueError, "legacy"):
            reader.install(self.site)
        self.assertIn("old complete payload", (self.destination / "chapters/unit.html").read_text())

    def test_failed_exchange_competing_writer_and_ancestry_overlap_refuse(self):
        self.update()
        with patch.object(reader, "exchange_directories", side_effect=OSError("unsupported")):
            with self.assertRaises(OSError):
                reader.install(self.site)
        with reader.bundle_lock(self.site):
            with self.assertRaisesRegex(ValueError, "another builder"):
                reader.install(self.site)
        with self.assertRaisesRegex(ValueError, "overlap"):
            reader.install(self.rendered)
        forbidden = self.rendered / "new-public-site"
        before_source = reader.file_rows(self.rendered)
        with patch.object(sys, "argv", ["reader", "--site", str(forbidden)]):
            with self.assertRaisesRegex(SystemExit, "overlap"):
                reader.main()
        self.assertFalse(forbidden.exists())
        self.assertEqual(before_source, reader.file_rows(self.rendered))
        self.assertEqual(self.before, reader.file_rows(self.destination))

    def test_source_and_destination_root_links_are_not_followed(self):
        linked_site = self.root / "linked-site"
        linked_site.symlink_to(self.site, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            reader.install(linked_site)
        source = self.rendered / "../linked-render"
        source.symlink_to(self.rendered, target_is_directory=True)
        with patch.object(reader, "RENDERED", source):
            with self.assertRaisesRegex(ValueError, "symlink"):
                reader.install(self.site)
        self.assertEqual(self.before, reader.file_rows(self.destination))

    def test_concurrent_prior_edit_is_preserved_instead_of_replaced(self):
        self.update()
        original_sync = reader.sync_stage
        def mutate(stage):
            original_sync(stage)
            (self.destination / "index.html").write_text("concurrent personal change\n")
        with patch.object(reader, "sync_stage", side_effect=mutate):
            with self.assertRaisesRegex(ValueError, "previous reader changed"):
                reader.install(self.site)
        self.assertEqual("concurrent personal change\n", (self.destination / "index.html").read_text())

    def test_process_exit_before_and_after_exchange_has_complete_output_and_visible_stage(self):
        self.update()
        script = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import build_human_reader_public_site as r
r.RENDERED, r.CROSSWALK = Path(sys.argv[2]), Path(sys.argv[3])
exchange = r.exchange_directories
def interrupted(left, right):
    if sys.argv[5] == 'before': os._exit(90)
    exchange(left, right)
    os._exit(91)
r.exchange_directories = interrupted
r.install(Path(sys.argv[4]))
'''
        for phase, code, content in (("before", 90, "old complete payload"), ("after", 91, "new complete payload")):
            result = subprocess.run([sys.executable, "-c", script, str(Path(reader.__file__).parent),
                                     str(self.rendered), str(self.crosswalk), str(self.site), phase],
                                    capture_output=True, timeout=30)
            self.assertEqual(code, result.returncode, result.stderr.decode())
            self.assertIn(content, (self.destination / "chapters/unit.html").read_text())
            manifest = json.loads((self.destination / reader.INSTALL_MANIFEST).read_text())
            self.assertEqual(manifest["files"], reader.payload_rows(self.destination))
            self.assertTrue(self.stages())
            self.assertTrue(all(json.loads((stage / "staging.json").read_text())["state"] == "installation_attempted" for stage in self.stages()))

    def test_post_exchange_fsync_failure_retains_prior_custody_and_uncertainty(self):
        self.update()
        original_sync = reader.sync_directory
        def fail_site(path):
            if path == self.site:
                raise OSError("directory fsync failed after exchange")
            original_sync(path)
        with patch.object(reader, "sync_directory", side_effect=fail_site):
            with self.assertRaises(OSError):
                reader.install(self.site)
        self.assertIn("new complete payload", (self.destination / "chapters/unit.html").read_text())
        stages = self.stages()
        self.assertEqual(1, len(stages))
        state = json.loads((stages[0] / "staging.json").read_text())
        self.assertEqual("installed_durability_unconfirmed", state["state"])
        self.assertEqual(self.before, reader.file_rows(stages[0] / "reader"))

    def test_incomplete_or_mismatched_integrity_manifest_cannot_own_the_previous_output(self):
        path = self.destination / reader.INSTALL_MANIFEST
        original = json.loads(path.read_text())
        import copy
        for key, value in (("edition_id", None), ("crosswalk_sha256", "0" * 64),
                           ("rendered_source_tree_sha256", "0" * 64), ("support_state_effect", "promoted")):
            changed = copy.deepcopy(original)
            if value is None:
                changed.pop(key)
            else:
                changed[key] = value
            path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                reader.install(self.site)
            self.assertEqual(changed, json.loads(path.read_text()))


if __name__ == "__main__":
    unittest.main()
