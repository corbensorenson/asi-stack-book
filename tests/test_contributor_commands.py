"""Prevent a targeted contributor request from silently running a broader gate."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import book


class ContributorCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.path = self.root / "registry.json"
        self.registry = {"tier_order": ["pr", "deep", "release"], "execution_defaults": {
            "depends_on": ["base-gate"], "review_state": "unreviewed", "historical_mode": "unreviewed", "side_effects": "unreviewed"},
            "units": [{"id": "consumer", "script": "check.py", "args": [], "execution_tier": "release", "input_artifacts": ["output.json"]}],
            "current_projections": [{"id": "owner", "mode": "generated", "inputs": ["chapters/*.qmd"],
                "outputs": ["output.json"], "depends_on": [], "checks": ["consumer"], "rebuild": ["python3", "builder.py"]}]}
        self.path.write_text(json.dumps(self.registry))

    def rejection(self, args):
        with patch.object(book, "ROOT", self.root), patch.object(book, "REGISTRY", self.path), \
             patch.object(book, "delegate") as delegate, patch.object(sys, "argv", ["book.py", *args]), \
             contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                book.main()
            self.assertEqual(2, caught.exception.code)
            delegate.assert_not_called()

    def test_unknown_coverage_cannot_expand_into_a_full_tier(self):
        self.rejection(["check", "--changed", "docs/unrelated.md"])

    def test_out_of_tier_check_is_not_silently_omitted(self):
        self.rejection(["check", "--changed", "chapters/new.qmd", "--tier", "pr"])

    def test_unreviewed_history_cannot_be_replayed_by_convenient_name(self):
        self.rejection(["history", "--select", "check.py"])

    def workflow(self):
        import yaml
        path = self.root / ".github/workflows/build-pages-artifact.yml"
        path.parent.mkdir(parents=True)
        steps = [{"name": script, "run": " ".join(["node" if script.endswith(".js") else "python3", f"scripts/{script}", *args])}
                 for script, args in book.HTML_INTERFACES.items()]
        path.write_text(yaml.safe_dump({"jobs": {"build": {"steps": steps}}}))
        return path

    def test_html_preview_reuses_workflow_and_explicit_local_mode_changes_only_clean_flags(self):
        self.workflow()
        site = self.root / "build/site"
        strict = book.html_plan(self.root, site, local=False)
        local = book.html_plan(self.root, site, local=True)
        self.assertEqual(8, len(strict["checks"]))
        for before, after in zip(strict["checks"], local["checks"]):
            self.assertEqual([arg for arg in before["args"] if arg != "--require-clean"], after["args"])
        browser = next(row for row in local["checks"] if row["runtime"] == "node")
        self.assertTrue({"--strict", "--all-chapters", "--all-viewports"} <= set(browser["args"]))
        self.assertEqual("ignored_outputs", browser["side_effects"])
        self.assertFalse(site.exists())

    def test_html_missing_duplicate_or_weakened_workflow_check_cannot_silently_pass(self):
        import yaml
        path = self.workflow()
        original = yaml.safe_load(path.read_text())
        import copy
        for kind in ("missing", "duplicate", "weakened", "unknown", "conditional", "ignored"):
            data = copy.deepcopy(original)
            steps = data["jobs"]["build"]["steps"]
            if kind == "missing":
                steps.pop()
            elif kind == "duplicate":
                steps.append(steps[-1])
            elif kind == "weakened":
                browser = next(step for step in steps if "validate_live_human_view_browser.js" in step["run"])
                browser["run"] = browser["run"].replace(" --strict", "")
            elif kind == "conditional":
                steps[-1]["if"] = "false"
            elif kind == "ignored":
                steps[-1]["continue-on-error"] = True
            else:
                steps.append({"name": "New check", "run": "python3 scripts/validate_new_layout.py"})
            path.write_text(yaml.safe_dump(data))
            with self.assertRaises(ValueError):
                book.html_plan(self.root, self.root / "_site", local=True)

    def test_html_failed_check_retains_diagnostics_and_stops_dependents(self):
        self.workflow()
        site = self.root / "_site"
        site.mkdir()
        (site / "index.html").write_text("<html>fixture</html>")
        planned = book.html_plan(self.root, site, local=True)
        with patch.object(book, "execute", return_value={"status": "failed", "diagnostic_id": "fixture_rejection"}) as execute, \
             patch.object(book, "capability_error", return_value=None), contextlib.redirect_stdout(io.StringIO()):
            report = book.check_html(planned, self.root, site)
        self.assertEqual("fail", report["status"])
        self.assertEqual(1, execute.call_count)
        self.assertTrue(all(row["status"] == "not_run" for row in report["units"][1:]))
        self.assertTrue(report["declared_inputs_and_site_unchanged"])
        self.assertEqual(1, len(list((self.root / "build").glob("book-html-check-*/report.json"))))

    def test_html_site_drift_fails_even_when_all_checks_exit_zero(self):
        self.workflow()
        site = self.root / "_site"
        site.mkdir()
        index = site / "index.html"
        index.write_text("before")
        planned = book.html_plan(self.root, site, local=True)
        def mutate(*args, **kwargs):
            index.write_text("edited during checks")
            return {"status": "passed"}
        with patch.object(book, "execute", side_effect=mutate), patch.object(book, "capability_error", return_value=None), \
             contextlib.redirect_stdout(io.StringIO()):
            report = book.check_html(planned, self.root, site)
        self.assertEqual("fail", report["status"])
        self.assertFalse(report["declared_inputs_and_site_unchanged"])

    def test_html_site_links_are_rejected_before_any_browser_or_report_write(self):
        self.workflow()
        site = self.root / "_site"
        site.mkdir()
        (site / "index.html").symlink_to(self.path)
        with patch.object(book, "execute") as execute:
            with self.assertRaisesRegex(ValueError, "symlink"):
                book.check_html(book.html_plan(self.root, site, local=True), self.root, site)
        execute.assert_not_called()
        self.assertFalse((self.root / "build").exists())

    def test_added_manuscript_or_changed_reader_render_during_checks_invalidates_the_run(self):
        self.workflow()
        site = self.root / "_site"
        site.mkdir()
        (site / "index.html").write_text("unchanged site")
        rendered = self.root / "editions/reader_manuscript/current/_book"
        rendered.mkdir(parents=True)
        (rendered / "index.html").write_text("old render")
        planned = book.html_plan(self.root, site, local=True)
        def mutate(*args, **kwargs):
            (rendered / "index.html").write_text("changed render")
            manuscript = self.root / "chapters/new.qmd"
            manuscript.parent.mkdir(exist_ok=True)
            manuscript.write_text("new manuscript input")
            return {"status": "passed"}
        with patch.object(book, "execute", side_effect=mutate), patch.object(book, "capability_error", return_value=None), \
             contextlib.redirect_stdout(io.StringIO()):
            report = book.check_html(planned, self.root, site)
        self.assertEqual("fail", report["status"])
        self.assertFalse(report["declared_inputs_and_site_unchanged"])


if __name__ == "__main__":
    unittest.main()
