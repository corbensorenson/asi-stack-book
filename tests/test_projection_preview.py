"""Check preview custody independently of generated text templates."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from projection_files import ProjectionFiles
import sync_scaffold


class ProjectionPreviewTests(unittest.TestCase):
    def test_preview_exposes_updates_and_additions_without_touching_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            original = root / "existing.txt"
            original.write_text("old")
            stamp = original.stat().st_mtime_ns
            files = ProjectionFiles(write=False)
            files.write(original, "new")
            files.write(root / "missing/nested.txt", "added")
            self.assertEqual("new", files.text(original))
            self.assertTrue(files.exists(root / "missing/nested.txt"))
            self.assertEqual("old", original.read_text())
            self.assertEqual(stamp, original.stat().st_mtime_ns)
            self.assertFalse((root / "missing").exists())
            self.assertEqual(["update", "add"], [row["operation"] for row in files.changes(root)])

    def test_unchanged_write_preserves_timestamp_and_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory).resolve() / "owner.txt"
            path.write_text("same")
            path.chmod(0o640)
            stamp = path.stat().st_mtime_ns
            files = ProjectionFiles()
            files.write(path, "same")
            self.assertEqual(stamp, path.stat().st_mtime_ns)
            files.write(path, "changed")
            self.assertEqual(0o640, path.stat().st_mode & 0o777)
            self.assertEqual("changed", path.read_text())

    def test_replacement_failure_preserves_owner_and_cleans_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            path = root / "owner.txt"
            path.write_text("old")
            with patch("projection_files.os.replace", side_effect=OSError("interrupted")):
                with self.assertRaises(OSError):
                    ProjectionFiles().write(path, "replacement")
            self.assertEqual("old", path.read_text())
            self.assertEqual([path], list(root.iterdir()))

    def test_symlink_target_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            path = root / "owner"
            path.write_text("old")
            alias = root / "alias"
            alias.symlink_to(path)
            with self.assertRaises(ValueError):
                ProjectionFiles().write(alias, "changed")
            self.assertEqual("old", path.read_text())

    def test_quarto_preview_reports_drift_without_creating_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            files = ProjectionFiles(write=False)
            with patch.object(sync_scaffold, "ROOT", root):
                sync_scaffold.write_quarto({"parts": [], "appendices": []}, files=files)
            rows = files.changes(root)
            by_path = {row["path"]: row for row in rows}
            self.assertEqual("add", by_path["_quarto.yml"]["operation"])
            self.assertEqual("add", by_path["assets/search-navigation.html"]["operation"])
            self.assertFalse((root / "_quarto.yml").exists())
            self.assertFalse((root / "assets/search-navigation.html").exists())


if __name__ == "__main__":
    unittest.main()
