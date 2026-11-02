"""Dependency invalidation must not rewrite history or invent review authority."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validation_projection_plan import graph_errors, plan


class ProjectionPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry = {"execution_defaults": {"depends_on": ["base-gate"]}, "units": [
            {"id": "current", "script": "current.py", "args": [], "execution_tier": "pr", "input_artifacts": ["current.json"]},
            {"id": "review", "script": "review.py", "args": [], "execution_tier": "deep", "input_artifacts": ["review.json"], "execution": {"depends_on": ["current"]}},
            {"id": "unknown", "script": "unknown.py", "args": [], "execution_tier": "deep"}],
            "current_projections": [
                {"id": "projection", "mode": "generated", "inputs": ["chapters/*.qmd"], "outputs": ["current.json"], "depends_on": [], "checks": ["current"], "rebuild": ["python3", "builder.py"]},
                {"id": "prose", "mode": "review_required", "inputs": ["review-input.json"], "outputs": ["review.json"], "depends_on": ["projection"], "checks": ["review"], "rebuild": ["review", "prose"], "review_boundary": "Review the actual changed prose; no automatic digest approval."}]}

    def test_changed_chapter_lists_transitive_outputs_and_review_boundary(self):
        result = plan(self.registry, ["chapters/new-owner.qmd"], self.root)
        self.assertEqual(["projection", "prose"], [row["id"] for row in result["projections"]])
        self.assertEqual(["current.json"], result["projections"][0]["expanded_outputs"])
        self.assertEqual("review_required", result["projections"][1]["mode"])
        self.assertEqual(["current", "review"], [row["id"] for row in result["checks"]])
        self.assertEqual(["unknown"], result["input_coverage_unknown_units"])
        self.assertFalse((self.root / "current.json").exists())

    def test_unrelated_edit_does_not_refresh_every_owner(self):
        result = plan(self.registry, ["docs/unrelated.md"], self.root)
        self.assertEqual([], result["projections"])
        self.assertEqual([], result["checks"])

    def test_selected_consumer_includes_its_execution_prerequisite(self):
        result = plan(self.registry, ["review-input.json"], self.root)
        self.assertEqual(["current", "review"], [row["id"] for row in result["checks"]])
        self.assertEqual("execution_prerequisite", result["checks"][0]["selection_reason"])

    def test_cycles_historical_refresh_and_missing_consumers_reject(self):
        for mutate in [lambda r: r["current_projections"][0]["depends_on"].append("prose"),
                       lambda r: r["current_projections"][0].update(mode="historical"),
                       lambda r: r["current_projections"][0].update(checks=["absent"]),
                       lambda r: r["current_projections"][1].pop("review_boundary")]:
            candidate = copy.deepcopy(self.registry)
            mutate(candidate)
            self.assertTrue(graph_errors(candidate))
            with self.assertRaises(ValueError):
                plan(candidate, ["chapters/owner.qmd"], self.root)

    def test_paths_cannot_escape_repository(self):
        for path in ["../outside", "/tmp/outside", "chapters/../outside", "chapters//owner.qmd", "chapters\\owner.qmd"]:
            with self.assertRaises(ValueError):
                plan(self.registry, [path], self.root)

    def test_editing_generated_output_requires_its_producer_check(self):
        result = plan(self.registry, ["current.json"], self.root)
        self.assertEqual(["current.json"], result["projections"][0]["changed_outputs"])
        self.assertEqual(["current", "review"], [row["id"] for row in result["checks"]])

    def test_reader_evidence_dependencies_come_from_the_existing_crosswalk(self):
        path = self.root / "editions/reader_manuscript/current/conclusion_claim_crosswalk.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"units": [{"owners": [{"artifact_refs": [{"path": "experiments/current-result.json"}]}]}]}))
        self.registry["current_projections"][0]["bound_input_owner"] = "human_reader_current"
        result = plan(self.registry, ["experiments/current-result.json"], self.root)
        self.assertEqual(["experiments/current-result.json"], result["projections"][0]["changed_inputs"])

    def test_plan_explains_heavy_or_platform_checks_and_preserves_unknown_review(self):
        self.registry["execution_defaults"].update(capabilities=["python"], review_state="unreviewed",
                                                 side_effects="unreviewed", timeout_seconds=1800)
        self.registry["units"][1]["execution"].update(capabilities=["python", "tool:lake"],
                                                    review_state="reviewed", side_effects="ignored_outputs", timeout_seconds=300)
        result = plan(self.registry, ["chapters/new-owner.qmd"], self.root)
        reviewed = result["checks"][1]
        self.assertEqual(["prose"], reviewed["projection_owners"])
        self.assertEqual("named_projection_consumer", reviewed["selection_reason"])
        self.assertEqual(300, reviewed["execution_contract"]["timeout_seconds"])
        self.assertEqual("ignored_outputs", reviewed["execution_contract"]["side_effects"])
        self.assertEqual(["python", "tool:lake"], result["execution_preview"]["capabilities"])
        self.assertEqual(["current"], result["execution_preview"]["unreviewed_contracts"])
        self.assertEqual("incomplete_contract_review", result["execution_preview"]["status"])
        self.assertEqual([], result["base_gate"]["execution_contract"]["depends_on"])


if __name__ == "__main__":
    unittest.main()
