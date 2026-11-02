"""Incomplete chapter intent must never become a canonical owner."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import add_chapter


class ChapterProposalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.manifest = self.root / "book_structure.json"
        self.inventory = self.root / "sources/source_inventory.json"
        self.inventory.parent.mkdir()
        self.manifest.write_text(json.dumps({"parts": [{"id": "part", "title": "Part", "chapters": []}]}))
        self.inventory.write_text(json.dumps([{"id": "known-source"}]))
        self.original = self.manifest.read_bytes()

    def invoke(self, *args):
        output = io.StringIO()
        with patch.object(add_chapter, "ROOT", self.root), patch.object(add_chapter, "STRUCTURE_PATH", self.manifest), \
             patch.object(add_chapter, "INVENTORY_PATH", self.inventory), patch.object(sys, "argv", ["add_chapter.py", "--part", "part", *args]), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            add_chapter.main()
        return output.getvalue()

    def test_default_valid_intent_is_only_a_proposal(self):
        text = self.invoke("--title", "A new owner", "--source", "known-source")
        self.assertIn('"admission_state": "not_admitted"', text)
        self.assertIn('"id": "a-new-owner"', text)
        self.assertEqual(self.original, self.manifest.read_bytes())
        self.assertFalse((self.root / "chapters").exists())

    def test_bad_source_empty_slug_or_traversal_cannot_modify_manifest(self):
        for args in [("--title", "..."), ("--title", "Owner", "--id", "../escape"),
                     ("--title", "Owner", "--id", ""), ("--title", "Owner", "--source", "missing"),
                     ("--title", "\n")]:
            with self.assertRaises(SystemExit):
                self.invoke(*args)
            self.assertEqual(self.original, self.manifest.read_bytes())

    def test_proposal_writes_only_owned_diagnostic_and_preserves_unknown_content(self):
        path = self.root / "build/proposal.json"
        self.invoke("--title", "Owner", "--proposal-output", str(path))
        self.assertEqual("not_admitted", json.loads(path.read_text())["admission_state"])
        self.assertEqual(self.original, self.manifest.read_bytes())
        unknown = self.root / "build/unknown.json"
        unknown.write_text('{"personal": "preserve"}')
        with self.assertRaises(SystemExit):
            self.invoke("--title", "Owner", "--proposal-output", str(unknown))
        self.assertEqual('{"personal": "preserve"}', unknown.read_text())

    def test_interrupted_proposal_install_leaves_manifest_and_prior_proposal_intact(self):
        path = self.root / "build/proposal.json"
        self.invoke("--title", "Owner", "--proposal-output", str(path))
        previous = path.read_bytes()
        with patch("projection_files.os.replace", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                self.invoke("--title", "Changed owner", "--proposal-output", str(path))
        self.assertEqual(self.original, self.manifest.read_bytes())
        self.assertEqual(previous, path.read_bytes())

    def test_broken_owner_link_and_linked_proposal_output_are_not_followed(self):
        chapter = self.root / "chapters/owner.qmd"
        chapter.parent.mkdir()
        chapter.symlink_to(self.root / "missing")
        with self.assertRaises(SystemExit):
            self.invoke("--title", "Owner")
        chapter.unlink()
        target = self.root / "build/proposal.json"
        target.parent.mkdir()
        target.write_text('{"personal": "keep"}')
        link = self.root / "build/link.json"
        link.symlink_to(target)
        with self.assertRaises(SystemExit):
            self.invoke("--title", "Owner", "--proposal-output", str(link))
        self.assertEqual('{"personal": "keep"}', target.read_text())


if __name__ == "__main__":
    unittest.main()
