"""Candidate isolation/custody tests; these do not approve a real chapter."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import prepare_chapter_admission as admission
import validate_dynamic_spine as dynamic_spine


class CurrentSourceBoundaryTests(unittest.TestCase):
    def test_improvement_acceptance_catalog_survives_declared_source_staging(self):
        registry = json.loads((REPO / "validation/registry.json").read_text())
        consumer = next(row for row in registry["units"] if row["script"] ==
                        "validate_post_v2_3_maintenance_transfer_and_publication_roadmap.py")
        catalog = "docs/project_improvements.md"
        self.assertIn(catalog, consumer["input_artifacts"])
        self.assertIn(catalog, admission.source_paths(REPO, registry))
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory) / catalog
            admission.copy_file(admission.regular_file(REPO, catalog), staged)
            self.assertEqual((REPO / catalog).read_bytes(), staged.read_bytes())


class AdmissionStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "repository"
        self.root.mkdir()
        self.patch = self.root / "build/candidate"
        self.patch.mkdir(parents=True)
        self.stage = self.root / "build/stage"
        # Reuse the real shape contract and an existing authored metadata row;
        # synthetic fixture prose is never claimed to pass editorial admission.
        self.structure = json.loads((REPO / "book_structure.json").read_text())
        self.structure["parts"] = [self.structure["parts"][0]]
        self.structure["parts"][0]["chapters"] = [self.structure["parts"][0]["chapters"][0]]
        self.old = self.structure["parts"][0]["chapters"][0]
        self.write(self.root, "book_structure.json", self.structure)
        self.write(self.root, "sources/source_inventory.json", json.loads((REPO / "sources/source_inventory.json").read_text()))
        self.write(self.root, "schemas/book_structure.schema.json", json.loads((REPO / "schemas/book_structure.schema.json").read_text()))
        units = [{"id": f"fixture:{index}", "script": script, "args": [], "execution_tier": "pr"}
                 for index, script in enumerate(sorted(admission.REQUIRED_CHECKS))]
        self.registry = {"tier_order": ["pr", "deep", "release"], "base_gate": {"script": "validate_book.py"},
                         "required_artifacts": ["book_structure.json", "scripts/new-registered-helper.py"], "units": units,
                         "summary": {"required_artifact_count": 2}}
        self.write(self.root, "validation/registry.json", self.registry)
        self.write(self.root, "scripts/run_validation_registry.py", "# synthetic test runner, never executed\n")
        self.write(self.root, "chapters/existing.qmd", "Existing fixture prose\n")
        self.run_git("init", "-q")
        self.run_git("add", ".")
        self.run_git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture source")
        self.run_git("remote", "add", "origin", "https://example.invalid/book.git")
        # An explicitly registered new file is copied; unknown personal files
        # and ignored private caches are preserved in the source and excluded.
        self.write(self.root, "scripts/new-registered-helper.py", "# registered untracked helper\n")
        self.write(self.root, "personal/unknown.txt", "keep private fixture\n")
        self.write(self.root, "sources/raw/private.txt", "keep ignored fixture\n")
        self.proposal = {"schema_version": admission.PROPOSAL_VERSION, "admission_state": "not_admitted",
                         "manifest_sha256": admission.digest(self.root / "book_structure.json"),
                         "source_inventory_sha256": admission.digest(self.root / "sources/source_inventory.json"),
                         "part_id": self.structure["parts"][0]["id"], "insert_at": 1,
                         "chapter": {"id": "candidate-owner", "title": "Candidate Owner"}}
        self.candidate = copy.deepcopy(self.structure)
        new = copy.deepcopy(self.old)
        new.update(id="candidate-owner", title="Candidate Owner", file="chapters/candidate-owner.qmd")
        self.candidate["parts"][0]["chapters"].append(new)
        self.write_candidate()

    @staticmethod
    def write(root, relative, value):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + "\n" if not isinstance(value, str) else value)

    def write_candidate(self):
        self.write(self.patch, "book_structure.json", self.candidate)
        self.write(self.patch, "chapters/candidate-owner.qmd", "---\ntitle: Candidate Owner\n---\n\nAuthored test fixture only.\n")

    def run_git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, capture_output=True, check=True, timeout=30)

    def prepare(self, **options):
        return admission.prepare(self.root, self.proposal, self.patch, self.stage, **options)

    def successful_report(self, command, **kwargs):
        report_path = Path(command[command.index("--report") + 1])
        report_path.parent.mkdir(parents=True)
        report = {"status": "pass", "registry_drift": False,
                  "registry_sha256": {"validation/registry.json": admission.digest(Path(kwargs["cwd"]) / "validation/registry.json")},
                  "units": [{"unit_id": "base-gate", "status": "passed"}] +
                           [{"unit_id": row["id"], "status": "passed"} for row in self.registry["units"]]}
        report_path.write_text(json.dumps(report))
        return {"status": "passed", "exit_code": 0}

    def test_complete_candidate_is_isolated_and_still_not_admitted(self):
        manifest = (self.root / "book_structure.json").read_bytes()
        stamp = (self.root / "book_structure.json").stat().st_mtime_ns
        receipt = self.prepare()
        self.assertEqual("prepared_unvalidated", receipt["status"])
        self.assertEqual("not_admitted", receipt["admission_state"])
        workspace = self.stage / "workspace"
        self.assertEqual(self.candidate, json.loads((workspace / "book_structure.json").read_text()))
        self.assertTrue((workspace / "scripts/new-registered-helper.py").is_file())
        self.assertFalse((workspace / "personal/unknown.txt").exists())
        self.assertFalse((workspace / "sources/raw/private.txt").exists())
        self.assertEqual(manifest, (self.root / "book_structure.json").read_bytes())
        self.assertEqual(stamp, (self.root / "book_structure.json").stat().st_mtime_ns)
        (workspace / "scripts/new-registered-helper.py").write_text("changed only in staging\n")
        self.assertEqual("# registered untracked helper\n", (self.root / "scripts/new-registered-helper.py").read_text())
        self.assertEqual("keep private fixture\n", (self.root / "personal/unknown.txt").read_text())

    def test_dynamic_spine_copy_excludes_unknown_trees_and_rejects_source_drift(self):
        workspace = self.root / "build/dynamic-control"
        dynamic_spine.copy_source_tree(self.root, workspace)
        self.assertTrue((workspace / "scripts/new-registered-helper.py").is_file())
        self.assertFalse((workspace / "personal").exists())
        self.assertFalse((workspace / "sources/raw").exists())
        self.assertFalse((workspace / ".git").exists())
        (workspace / "book_structure.json").write_text("Disposable independent copy.\n")
        self.assertEqual(self.structure, json.loads((self.root / "book_structure.json").read_text()))
        original = admission.copy_file
        def drift(source, target):
            original(source, target)
            if source.name == "book_structure.json":
                source.write_text("Authored concurrent source edit.\n")
        with patch.object(admission, "copy_file", side_effect=drift):
            with self.assertRaisesRegex(ValueError, "declared source changed"):
                dynamic_spine.copy_source_tree(self.root, self.root / "build/dynamic-drift-control")
        self.assertEqual("keep private fixture\n", (self.root / "personal/unknown.txt").read_text())

    def test_unknown_source_incomplete_fields_or_old_owner_change_refuse_before_staging(self):
        original = copy.deepcopy(self.candidate)
        mutations = [lambda row: row["parts"][0]["chapters"][1].pop("publication"),
                     lambda row: row["parts"][0]["chapters"][1]["source_ids"].append("unknown-source"),
                     lambda row: row["parts"][0]["chapters"][0].update(title="Changed old owner"),
                     lambda row: row["parts"][0]["chapters"].reverse(),
                     lambda row: row["parts"][0]["chapters"][1].update(evidence_level="empirical-test-backed")]
        for mutate in mutations:
            self.candidate = copy.deepcopy(original)
            mutate(self.candidate)
            self.write_candidate()
            with self.assertRaises(ValueError):
                self.prepare()
            self.assertFalse(self.stage.exists())

    def test_stale_proposal_or_existing_owner_path_refuse(self):
        self.proposal["manifest_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale"):
            self.prepare()
        self.proposal["manifest_sha256"] = admission.digest(self.root / "book_structure.json")
        path = self.root / "chapters/candidate-owner.qmd"
        path.symlink_to(self.root / "missing")
        with self.assertRaisesRegex(ValueError, "repository object"):
            self.prepare()
        self.assertTrue(path.is_symlink())

    def test_candidate_cannot_replace_acceptance_code_or_traverse_links(self):
        self.write(self.patch, "scripts/validate_book.py", "# forged pass\n")
        with self.assertRaisesRegex(ValueError, "checking machinery"):
            self.prepare()
        (self.patch / "scripts/validate_book.py").unlink()
        (self.patch / "linked").symlink_to(self.root / "personal", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "link"):
            self.prepare()
        self.assertFalse(self.stage.exists())

    def test_birth_patch_cannot_replace_tests_or_evidence_source_release_and_authority_custody(self):
        forbidden = [".gitignore", ".gitattributes", "tests/test_validation_infrastructure.py", "experiments/campaign/fixture.json",
                     "sources/source_inventory.json", "roadmap_records/current.json", "status/config.json",
                     "release_records/release.json", "evidence_transitions/accepted.json",
                     "external_reviews/review.json", "claim_revisions/revision.json", "governance/authority.json",
                     "archive/receipt.json", "_archive/receipt.json", "docs/results/receipt.json",
                     "docs/attempts/receipt.json", "docs/protected/receipt.json"]
        before = (self.root / "book_structure.json").read_bytes()
        for relative in forbidden:
            self.write(self.patch, relative, "Unrelated fixture must never become a birth patch.\n")
            with self.assertRaisesRegex(ValueError, "checking machinery|protected custody"):
                self.prepare()
            self.assertFalse(self.stage.exists())
            self.assertEqual(before, (self.root / "book_structure.json").read_bytes())
            (self.patch / relative).unlink()

    def test_retained_reader_snapshots_are_protected_while_current_route_data_can_be_staged(self):
        for relative in ("editions/reader_manuscript/v1_0/manifest.json",
                         "editions/reader_manuscript/reader_2026_07_26/manifest.json",
                         "editions/reader_manuscript/README.md"):
            self.write(self.patch, relative, "Retained custody fixture\n")
            with self.assertRaisesRegex(ValueError, "protected custody"):
                self.prepare()
            self.assertFalse(self.stage.exists())
            (self.patch / relative).unlink()
        relative = "editions/reader_manuscript/current/conclusion_claim_crosswalk.json"
        self.write(self.patch, relative, "Current-route authored fixture, not semantic acceptance.\n")
        receipt = self.prepare()
        self.assertEqual("prepared_unvalidated", receipt["status"])
        self.assertEqual("not_admitted", receipt["admission_state"])
        self.assertIn(relative, receipt["patch_files"])
        self.assertFalse((self.root / relative).exists())

    def test_source_patch_and_nested_stage_refuse_before_candidate_enumeration(self):
        before = (self.root / "book_structure.json").read_bytes()
        original_patch = self.patch
        for candidate in (self.root, self.root.parent):
            self.patch = candidate
            with patch.object(admission, "patch_paths", side_effect=AssertionError("must not enumerate source/ancestor")):
                with self.assertRaisesRegex(ValueError, "separate candidate patch"):
                    self.prepare()
            self.assertFalse(self.stage.exists())
        self.patch = original_patch
        self.stage = self.patch / "nested-stage"
        with patch.object(admission, "patch_paths", side_effect=AssertionError("must not enumerate overlapping candidate")):
            with self.assertRaisesRegex(ValueError, "fresh staging directory"):
                self.prepare()
        self.assertFalse(self.stage.exists())
        self.assertEqual(before, (self.root / "book_structure.json").read_bytes())

    def test_existing_stage_is_preserved(self):
        self.stage.mkdir()
        sentinel = self.stage / "valuable.txt"
        sentinel.write_text("keep\n")
        with self.assertRaisesRegex(ValueError, "fresh"):
            self.prepare()
        self.assertEqual("keep\n", sentinel.read_text())

    def test_copy_interruption_retains_recognizable_incomplete_stage_and_source(self):
        original = (self.root / "book_structure.json").read_bytes()
        with patch.object(admission, "copy_file", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                self.prepare()
        receipt = json.loads((self.stage / "admission.json").read_text())
        self.assertEqual("incomplete", receipt["status"])
        self.assertEqual("not_admitted", receipt["admission_state"])
        self.assertEqual(original, (self.root / "book_structure.json").read_bytes())

    def test_candidate_change_during_copy_refuses_instead_of_laundering_current_hash(self):
        original_copy = admission.copy_file
        def mutate(source, target):
            original_copy(source, target)
            if source == self.patch / "chapters/candidate-owner.qmd":
                source.write_text("edited while copying\n")
        with patch.object(admission, "copy_file", side_effect=mutate):
            with self.assertRaisesRegex(ValueError, "changed during preparation"):
                self.prepare()
        self.assertEqual("incomplete", json.loads((self.stage / "admission.json").read_text())["status"])

    def test_complete_bounded_report_records_pass_without_canonical_admission(self):
        with patch.object(admission, "execute", side_effect=self.successful_report):
            receipt = self.prepare(validate=True)
        self.assertEqual("birth_checks_passed_not_admitted", receipt["status"])
        self.assertEqual(self.structure, json.loads((self.root / "book_structure.json").read_text()))

    def test_zero_exit_without_report_is_rejected(self):
        with patch.object(admission, "execute", return_value={"status": "passed", "exit_code": 0}):
            receipt = self.prepare(validate=True)
        self.assertEqual("rejected", receipt["status"])
        self.assertEqual("not_admitted", receipt["admission_state"])

    def test_missing_units_forged_registry_or_validator_source_rewrite_are_rejected(self):
        for mutation in ("missing_unit", "registry", "source"):
            self.stage = self.root / f"build/stage-{mutation}"
            def forged(command, **kwargs):
                result = self.successful_report(command, **kwargs)
                report_path = Path(command[command.index("--report") + 1])
                report = json.loads(report_path.read_text())
                if mutation == "missing_unit":
                    report["units"].pop()
                elif mutation == "registry":
                    report["registry_sha256"] = {"validation/registry.json": "0" * 64}
                else:
                    self.write(kwargs["cwd"], "chapters/candidate-owner.qmd", "check rewrote its input\n")
                report_path.write_text(json.dumps(report))
                return result
            with patch.object(admission, "execute", side_effect=forged):
                self.assertEqual("rejected", self.prepare(full=True)["status"])


if __name__ == "__main__":
    unittest.main()
