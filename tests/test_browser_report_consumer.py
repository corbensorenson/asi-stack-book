"""Authored report-contract controls, not captured browser or human review."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_live_human_view_browser_report as consumer


def metrics(width, height):
    rect = {"left": 0, "right": 50, "top": 0, "bottom": 44, "width": 50, "height": 44}
    return {"viewport_width": width, "viewport_height": height, "client_width": width, "scroll_width": width,
            "horizontal_overflow_px": 0, "toggle_visible": True, "toggle_rect": rect,
            "toggle_clipped_horizontally": False,
            "buttons": [{"choice": choice, "text": choice, "visible": True, "rect": dict(rect),
                         "clipped_horizontally": False, "text_overflow_px": 0} for choice in ("ai", "human")],
            "label": {"height": 20, "line_height": 20, "text_overflow_px": 0},
            "reader_link": {"text": "reader fixture", "href": "reader/", "visible": True,
                            "clipped_horizontally": False, "text_overflow_px": 0}}


class BrowserReportConsumerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.site = self.root / "site"
        self.site.mkdir()
        self.structure = {"parts": [{"chapters": [{"id": "fixture", "file": "chapters/fixture.qmd"}]}], "appendices": [
            {"id": "corben-source-corpus", "file": "appendices/G.qmd"},
            {"id": "external-sources-and-literature", "file": "appendices/H.qmd"}]}
        self.crosswalk = {"units": [{"unit_id": "fixture-unit", "public_path": "reader/unit.html", "title": "Fixture reader"}]}
        for relative, value in zip(consumer.INPUTS, [self.structure, self.crosswalk, "authored producer fixture"]):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))
        routes = {row["id"]: str(Path(row["file"]).with_suffix(".html"))
                  for row in self.structure["parts"][0]["chapters"] + self.structure["appendices"]}
        for relative in ["index.html", "reader/unit.html", *routes.values()]:
            path = self.site / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("authored HTML fixture; no actual browser observation")
        self.report = {"schema_version": "0.2", "status": "pass", "page_selection": "all-chapters",
                       "viewport_selection": "all-viewports", "site_dir": str(self.site), "browser_version": "fixture-only",
                       "viewports": [{"name": name, **size} for name, size in consumer.VIEWPORTS.items()],
                       "validated_pages": [], "validated_reader_pages": [], "edition_control_accessibility": [],
                       "non_claims": ["Authored report fixture only.", "No actual DOM or human accessibility observation."]}
        diagrams = {"diagram_count": 1, "visible_diagram_count": 1, "diagrams": [{"id": "fixture",
                    "width": 100, "height": 100, "visible": True, "content_count": 6, "text_count": 0}]}
        for name, size in consumer.VIEWPORTS.items():
            for identifier, route in routes.items():
                url = (self.site / route).as_uri()
                human = {"reader_overlay_operations": 1, "reader_overlay_runtime": {"processed": True,
                         "total": 1, "matching": 1, "applied": 1, "skipped": 0, "skipped_ids": "",
                         "applied_nodes": 1, "original_wrappers": 1}, "status_text": "Human view active.",
                         "layout": metrics(**size)}
                checks = {"human_url_mode": human}
                if identifier == "fixture":
                    human.update({key: 0 for key in ("visible_live_sections", "visible_core_claim_markers",
                                                     "visible_live_toc_links", "visible_support_boilerplate_phrases")})
                    human.update({key: 1 for key in ("live_sections", "human_blocks", "core_claim_markers",
                        "visible_human_blocks", "visible_core_claim_text", "visible_human_support_boundaries")})
                    human["diagrams"] = copy.deepcopy(diagrams)
                    ai = {"visible_live_sections": 1, "visible_human_blocks": 0, "visible_core_claim_markers": 1,
                          "visible_support_boilerplate_phrases": 1, "visible_human_support_boundaries": 0,
                          "layout": metrics(**size), "diagrams": copy.deepcopy(diagrams), "url": url + "?view=ai"}
                    checks.update({"ai_click_mode": ai, "ai_url_mode": copy.deepcopy(ai),
                                   "human_click_url": url + "?view=human", "local_storage_persistence": "human"})
                else:
                    checks.update({"ai_click_url": url + "?view=ai", "ai_click_layout": metrics(**size)})
                self.report["validated_pages"].append({"page_id": identifier, "url": url, "viewport": name,
                                                       "viewport_size": size, "checks": checks})
            self.report["validated_reader_pages"].append({"unit_id": "fixture-unit", "viewport": name,
                "url": (self.site / "reader/unit.html").as_uri(), "checks": {"horizontal_overflow_px": 0,
                "control_visible": True, "control_clipped": False, "research_href": self.site.as_uri(),
                "research_text": "AI / researcher", "current_text": "Human Reader", "title": "Fixture reader",
                "main_present": True, "skip_link_present": True, "research_link_label": "AI / researcher", "callout_count": 1}})
        for width in (320, 390, 430):
            for scale in (1, 2):
                self.report["edition_control_accessibility"].append({"width": width, "text_scale": scale,
                    "metrics": metrics(width, 844), "keyboard_controls": 3, "screenshot": "authored-fixture-not-rendered.png"})
        self.report["sampled_pages"] = copy.deepcopy(self.report["validated_pages"])
        self.refresh()

    def refresh(self):
        self.report["site_sha256"], self.report["input_sha256"] = consumer.snapshot(self.site, self.root)

    def validate(self, report=None):
        return consumer.validate_report(self.report if report is None else report, self.site, root=self.root)

    def reject(self, mutate):
        report = copy.deepcopy(self.report)
        mutate(report)
        with self.assertRaises(ValueError):
            self.validate(report)

    def test_complete_current_authored_report_is_readonly(self):
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual({"technical_pairs": 6, "reader_pairs": 2, "control_pairs": 6}, self.validate())
        self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.root.rglob("*") if path.is_file()})

    def test_absent_skipped_failed_sampled_or_unversioned_report_refuses(self):
        for key, values in {"status": ["skipped", "fail"], "page_selection": ["sample"],
                            "viewport_selection": ["desktop"], "schema_version": ["0.1", None]}.items():
            for value in values:
                self.reject(lambda report: report.update({key: value}))
        self.reject(lambda report: report.pop("validated_reader_pages"))

    def test_incomplete_duplicate_unexpected_or_wrong_url_coverage_refuses(self):
        for key in ("validated_pages", "validated_reader_pages", "edition_control_accessibility"):
            self.reject(lambda report: report[key].pop())
            self.reject(lambda report: report[key].append(copy.deepcopy(report[key][0])))
        self.reject(lambda report: report["validated_pages"][0].update(page_id="unknown"))
        self.reject(lambda report: report["validated_reader_pages"][0].update(url=(self.root / "private.html").as_uri()))
        self.reject(lambda report: report["viewports"][0].update(width=640))
        self.reject(lambda report: report["sampled_pages"].pop())

    def test_reported_contradictions_invalid_numbers_and_missing_probes_refuse(self):
        self.reject(lambda report: report["validated_pages"][0]["checks"].pop("ai_url_mode"))
        self.reject(lambda report: report["validated_pages"][0]["checks"]["human_url_mode"].update(visible_live_sections=True))
        self.reject(lambda report: report["validated_pages"][0]["checks"]["human_url_mode"]["reader_overlay_runtime"].update(applied=2))
        self.reject(lambda report: report["validated_pages"][0]["checks"]["human_url_mode"]["diagrams"].update(visible_diagram_count=2))
        self.reject(lambda report: report["validated_reader_pages"][0]["checks"].update(skip_link_present=False))
        self.reject(lambda report: report["edition_control_accessibility"][0]["metrics"]["buttons"][0]["rect"].update(height=20))
        self.reject(lambda report: report["edition_control_accessibility"][0]["metrics"].update(scroll_width=800))
        self.reject(lambda report: report["edition_control_accessibility"][0]["metrics"].update(horizontal_overflow_px=float("nan")))

    def test_changed_site_manifests_producer_or_alias_refuses(self):
        for path in (self.site / "index.html", *(self.root / value for value in consumer.INPUTS)):
            before = path.read_bytes()
            path.write_bytes(before + b"\n")
            with self.assertRaisesRegex(ValueError, "stale"):
                self.validate()
            path.write_bytes(before)
        linked = self.site / "linked"
        linked.symlink_to(self.root / consumer.INPUTS[0])
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.validate()
        linked.unlink()
        source = self.root / consumer.INPUTS[2]
        original = source.read_bytes()
        source.unlink()
        os.mkfifo(source)
        try:
            with self.assertRaisesRegex(ValueError, "regular file"):
                self.validate()
        finally:
            source.unlink()
            source.write_bytes(original)
        self.reject(lambda report: report.update(site_dir=str(self.root)))

    def test_inputs_changing_during_consumer_check_refuse(self):
        original = consumer.snapshot
        calls = 0
        def mutate(site, root):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.site / "index.html").write_text("changed while consuming fixture")
            return original(site, root)
        with patch.object(consumer, "snapshot", side_effect=mutate):
            with self.assertRaisesRegex(ValueError, "changed"):
                self.validate()

    def test_cli_missing_malformed_or_linked_report_fails_without_writes(self):
        report = self.root / "report.json"
        for contents in (None, "{", '{"status":"pass"}'):
            if contents is not None:
                report.write_text(contents)
            with patch.object(sys, "argv", ["report", "--site", str(self.site), "--report", str(report)]):
                with self.assertRaises(SystemExit):
                    consumer.main()
            self.assertEqual(contents, report.read_text() if report.exists() else None)
        report.unlink()
        report.symlink_to(self.root / consumer.INPUTS[0])
        with patch.object(sys, "argv", ["report", "--report", str(report)]):
            with self.assertRaisesRegex(SystemExit, "symlink"):
                consumer.main()
        report.unlink()
        os.mkfifo(report)
        with patch.object(sys, "argv", ["report", "--report", str(report)]):
            with self.assertRaisesRegex(SystemExit, "regular file"):
                consumer.main()
        report.unlink()
        report.write_text(json.dumps(self.report))
        with patch.object(sys, "argv", ["report", "--report", str(report)]), patch.object(consumer, "MAX_REPORT_BYTES", 10):
            with self.assertRaisesRegex(SystemExit, "consumer bound"):
                consumer.main()

    def test_node_refuses_in_site_or_broken_link_report_before_probing(self):
        script = Path(consumer.__file__).with_name("validate_live_human_view_browser.js")
        output = self.site / "nested/report.json"
        for kind in ("inside", "broken-link"):
            if kind == "broken-link":
                output = self.root / "broken-report.json"
                output.symlink_to(self.root / "missing.json")
            before = consumer.snapshot(self.site, self.root)
            result = subprocess.run(["node", str(script), "--site", str(self.site), "--report", str(output)],
                                    capture_output=True, timeout=30)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(before, consumer.snapshot(self.site, self.root))
            self.assertFalse((self.site / "nested").exists())
            if kind == "broken-link":
                self.assertTrue(output.is_symlink())


if __name__ == "__main__":
    unittest.main()
