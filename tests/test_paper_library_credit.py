"""Preserve explicit manuscript attribution in the public source wrapper."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_paper_library import expected_page


class ManuscriptCreditTests(unittest.TestCase):
    def page(self, credit=None):
        record = {"source_id": "example", "title": "Example", "published_source": "papers/source/example.md", "sha256": "a" * 64, "bytes": 4}
        if credit is not None:
            record["author_credit"] = credit
        return expected_page(record, {}, {"parts": []}, b"Text")

    def test_existing_personal_credit_is_preserved(self):
        self.assertIn('author: "Corben Sorenson — original collaborator credits preserved in the manuscript"', self.page())

    def test_project_credit_does_not_assign_personal_authorship(self):
        page = self.page("Answerability Atlas Project")
        self.assertIn('author: "Answerability Atlas Project"', page)
        self.assertNotIn("Corben Sorenson's original source manuscript", page)
        self.assertIn("supplied by Corben", page)
        self.assertIn("independent replication", page)


if __name__ == "__main__":
    unittest.main()
