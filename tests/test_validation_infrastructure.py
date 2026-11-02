"""Behavioral regressions for schema acceptance and deployment custody."""

import copy
import json
import contextlib
import io
from pathlib import Path
import shutil
import sys
import subprocess
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from schema_validation import schema_errors, validate_value
import build_tested_site_bundle as bundle
import validate_p6_9_proof_evidence_handoff as handoff
from repository_custody import historical_sha256
from select_tested_site_deployment import decision
import build_proof_axiom_audit as axiom_audit
import validate_ci_supply_chain_pins as supply_chain


class PinReviewBoundaryTests(unittest.TestCase):
    def test_default_clock_expires_reviews_at_utc_boundary(self):
        inventory = json.loads(supply_chain.INVENTORY.read_text())
        schema = json.loads(supply_chain.SCHEMA.read_text())
        due = min(date.fromisoformat(row["review_due_on"]) for row in inventory["pins"])
        next_day = due + timedelta(days=1)
        class LocalDate(date):
            @classmethod
            def today(cls):
                return due

        with patch.dict(supply_chain.os.environ, {}, clear=True), patch.object(
            supply_chain, "date", LocalDate
        ), patch.object(supply_chain, "datetime", create=True) as clock:
            clock.now.return_value = datetime(next_day.year, next_day.month, next_day.day, 0, 1, tzinfo=timezone.utc)
            actual = supply_chain.audit_date()
            self.assertEqual(next_day, actual)
            clock.now.assert_called_once_with(timezone.utc)
        self.assertTrue(any("expired" in error for error in
                            supply_chain.validate_inventory(inventory, schema, as_of=actual)))
        self.assertEqual([], supply_chain.validate_inventory(inventory, schema, as_of=due))

    def test_explicit_audit_date_is_deterministic_and_invalid_override_refuses(self):
        with patch.dict(supply_chain.os.environ, {"ASI_PIN_REVIEW_AS_OF": "2026-10-08"}):
            self.assertEqual(date(2026, 10, 8), supply_chain.audit_date())
        for raw in ("not-a-date", "20261008", "2026-W41-4"):
            with self.subTest(raw=raw), patch.dict(supply_chain.os.environ, {"ASI_PIN_REVIEW_AS_OF": raw}):
                with self.assertRaisesRegex(ValueError, "must be YYYY-MM-DD"):
                    supply_chain.audit_date()

    def test_malformed_inventory_is_a_named_refusal_not_a_consumer_exception(self):
        valid = json.loads(supply_chain.INVENTORY.read_text())
        schema = json.loads(supply_chain.SCHEMA.read_text())
        candidates = [None, [], {**valid, "review_policy": None}, {**valid, "pins": None},
                      {**valid, "pins": [None]},
                      {**valid, "review_policy": {**valid["review_policy"], "max_review_age_days": "many"}},
                      {**valid, "review_policy": {**valid["review_policy"], "max_review_age_days": True}}]
        for field in ("reviewed_on", "review_due_on"):
            candidate = copy.deepcopy(valid)
            candidate["pins"][0][field] = candidate["pins"][0][field].replace("-", "")
            candidates.append(candidate)
        candidate = copy.deepcopy(valid)
        binary = next(row for row in candidate["pins"] if row["kind"] == "commit_url_installer")["runtime_binary"]
        binary["observed_on"] = binary["observed_on"].replace("-", "")
        candidates.append(candidate)
        for candidate in candidates:
            with self.subTest(candidate=candidate):
                errors = supply_chain.validate_inventory(candidate, schema, as_of=date(2026, 10, 3))
                self.assertTrue(errors)
                self.assertTrue(all(isinstance(error, str) for error in errors))

    def test_cli_stops_before_workflow_consumption_when_inventory_is_malformed(self):
        schema = json.loads(supply_chain.SCHEMA.read_text())
        output = io.StringIO()
        with patch.object(supply_chain, "load_json", side_effect=[None, schema]), patch.object(
            supply_chain, "inventory_values"
        ) as consume, contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as raised:
                supply_chain.main()
        self.assertEqual(1, raised.exception.code)
        self.assertIn("CI supply-chain pin validation failed:", output.getvalue())
        consume.assert_not_called()


class ProofTrustTests(unittest.TestCase):
    def test_unsupported_source_theorem_syntax_cannot_be_silently_omitted(self):
        self.assertEqual(2, len(axiom_audit.source_declarations('theorem plain : True := by trivial\nprivate theorem hidden : True := by trivial\n')))
        for source in ['theorem α : True := by trivial', '@[simp] theorem tagged : True := by trivial',
                       'protected theorem scoped : True := by trivial']:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'unsupported source theorem syntax'):
                axiom_audit.source_declarations(source)

    def test_erasing_a_native_dependency_is_rejected(self):
        expected = json.loads(axiom_audit.OUTPUT.read_text())
        self.assertEqual([], axiom_audit.errors(expected, expected))
        altered = copy.deepcopy(expected)
        row = next(row for row in altered['declarations'] if 'native_compiler_trust' in row['trust_classes'])
        row['axioms'] = []
        row['trust_classes'] = []
        self.assertTrue(axiom_audit.errors(altered, expected))

    def test_unreviewed_axioms_do_not_receive_a_native_trust_label(self):
        self.assertEqual('unreviewed_axiom', axiom_audit.classify('sorryAx'))
        self.assertEqual('unreviewed_axiom', axiom_audit.classify('Project.unprovedAssumption'))
        value = {'summary': {'unreviewed_axiom_theorems': 1}}
        self.assertTrue(axiom_audit.errors(value, value))


class DeploymentSelectionTests(unittest.TestCase):
    def test_late_old_build_cannot_replace_current_main(self):
        older, newer = "a" * 40, "b" * 40
        self.assertTrue(decision(newer, newer)["eligible"])
        self.assertFalse(decision(older, newer)["eligible"])
        self.assertFalse(decision(newer, "c" * 40)["eligible"])
        # A deliberate main rollback can select that exact tested commit;
        # completed event custody and bundle verification remain separate.
        self.assertTrue(decision(older, older)["eligible"])
        with self.assertRaises(ValueError):
            decision("main", newer)


class BaselineDiagnosticTests(unittest.TestCase):
    def test_invalid_baseline_never_claims_mutation_acceptance(self):
        value = handoff.load(handoff.ARTIFACT)
        builder = type("Builder", (), {"build": staticmethod(lambda: value)})
        with patch.object(handoff, "load_builder", return_value=builder), patch.object(
            handoff, "errors", return_value=["baseline invalid"]
        ) as check:
            with self.assertRaises(SystemExit) as raised:
                handoff.main()
        self.assertIn("baseline invalid", str(raised.exception))
        self.assertNotIn("negative mutation accepted", str(raised.exception))
        self.assertEqual(1, check.call_count)

    def test_valid_baseline_exercises_all_rejections(self):
        value = handoff.load(handoff.ARTIFACT)
        builder = type("Builder", (), {"build": staticmethod(lambda: value)})
        with patch.object(handoff, "load_builder", return_value=builder), patch.object(
            handoff, "errors", side_effect=lambda item: [] if item == value else ["rejected"]
        ) as check, contextlib.redirect_stdout(io.StringIO()):
            handoff.main()
        self.assertEqual(15, check.call_count)


class HistoricalCustodyTests(unittest.TestCase):
    def test_worktree_drift_does_not_rewrite_historical_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL, timeout=30)
            git("init")
            (root / "input.txt").write_text("frozen input")
            git("add", "input.txt")
            git("-c", "user.name=Custody test", "-c", "user.email=custody@example.invalid", "commit", "-m", "fixture")
            frozen = git("rev-parse", "HEAD").decode().strip()
            original = historical_sha256(frozen, "input.txt", root=root)
            (root / "input.txt").write_text("later input")
            self.assertEqual(original, historical_sha256(frozen, "input.txt", root=root))
            git("add", "input.txt")
            git("-c", "user.name=Custody test", "-c", "user.email=custody@example.invalid", "commit", "-m", "later fixture")
            later = git("rev-parse", "HEAD").decode().strip()
            self.assertNotEqual(original, historical_sha256(later, "input.txt", root=root))
            with self.assertRaisesRegex(ValueError, "restore complete Git history"):
                historical_sha256("0" * 40, "input.txt", root=root)
            with self.assertRaises(ValueError):
                historical_sha256(frozen, "../input.txt", root=root)


class SchemaAcceptanceTests(unittest.TestCase):
    def test_constraints_and_valid_boundaries(self):
        cases = [
            ({"type": "integer"}, 0, "0"),
            ({"type": "integer"}, 0, True),
            ({"type": "null"}, None, 0),
            ({"type": ["integer", "null"]}, None, "0"),
            ({"minimum": 0}, 0, -1),
            ({"exclusiveMinimum": 0}, 1, 0),
            ({"maximum": 1}, 1, 2),
            ({"minItems": 1}, [1], []),
            ({"maxItems": 1}, [1], [1, 2]),
            ({"uniqueItems": True}, [1, 2], [1, 1]),
            ({"pattern": "^[a-z]+$"}, "scope", "scope0"),
            ({"minLength": 1}, "a", ""),
            ({"maxLength": 1}, "a", "ab"),
            ({"minProperties": 1}, {"id": "a"}, {}),
            ({"maxProperties": 1}, {"id": "a"}, {"id": "a", "other": 1}),
            ({"propertyNames": {"pattern": "^[a-z]+$"}}, {"id": 1}, {"ID": 1}),
            ({"enum": [1]}, 1, True),
            ({"const": 1}, 1, True),
            ({"required": ["id"]}, {"id": "a"}, {}),
            ({"properties": {"id": {}}, "additionalProperties": False}, {"id": "a"}, {"other": "a"}),
            ({"items": {"type": "integer"}}, [1], ["1"]),
            ({"prefixItems": [{"type": "integer"}, {"type": "string"}]}, [1, "a"], ["a", 1]),
            ({"contains": {"const": "required"}}, ["required"], ["absent"]),
            ({"properties": {"epoch": {"minimum": 0}}}, {"epoch": 0}, {"epoch": -1}),
            ({"$defs": {"epoch": {"type": "integer", "minimum": 0}}, "$ref": "#/$defs/epoch"}, 0, -1),
            ({"anyOf": [{"type": "null"}, {"type": "integer"}]}, None, "1"),
            ({"allOf": [{"minimum": 0}, {"maximum": 1}]}, 1, 2),
            ({"oneOf": [{"type": "integer"}, {"type": "number"}]}, 0.5, 1),
            ({"not": {"type": "null"}}, 0, None),
            ({"if": {"const": 1}, "then": False}, 2, 1),
        ]
        for schema, valid, invalid in cases:
            with self.subTest(schema=schema, invalid=invalid):
                self.assertEqual([], validate_value(valid, schema, "fixture"))
                self.assertTrue(validate_value(invalid, schema, "fixture"))

    def test_actual_authority_lifecycle_bypasses(self):
        root = Path(__file__).resolve().parents[1]
        fixture = root / "tests/fixtures/protocol_records/authority_tuple_lifecycle_record.valid.json"
        schema = json.loads((root / "schemas/authority_tuple_lifecycle_record.schema.json").read_text())
        valid = json.loads(fixture.read_text())
        self.assertEqual([], validate_value(valid, schema, "authority"))
        # The concrete record's constrained fields, rather than a toy copy of
        # its acceptance predicate, are mutated below.
        mutations = [
            ("empty sources", lambda item: item.__setitem__("source_ids", [])),
            ("duplicate sources", lambda item: item["source_ids"].append(item["source_ids"][0])),
            ("negative epoch", lambda item: item["authority_tuple"].__setitem__("revocation_epoch", -1)),
            ("string epoch", lambda item: item["authority_tuple"].__setitem__("revocation_epoch", "4")),
        ]
        for label, mutate in mutations:
            candidate = copy.deepcopy(valid)
            mutate(candidate)
            self.assertTrue(validate_value(candidate, schema, "authority"), label)
        valid["authority_tuple"]["revocation_epoch"] = 0
        valid["cross_domain_handoff"]["target_owner_approval_ref"] = None
        self.assertEqual([], validate_value(valid, schema, "authority"))

    def test_malformed_schemas_and_offline_refs(self):
        for schema in ({"type": "integar"}, {"minimum": "zero"}, {"required": "id"}, {"$schema": "https://unknown.invalid/draft"}):
            with self.subTest(schema=schema):
                self.assertTrue(schema_errors(schema, "contract"))
                self.assertTrue(validate_value({}, schema, "fixture"))
        self.assertTrue(validate_value(1, {"$ref": "https://unknown.invalid/schema"}, "fixture"))
        self.assertEqual([], validate_value(None, True, "fixture"))
        self.assertTrue(validate_value(None, False, "fixture"))
        # Draft 2020-12 defaults to the format-annotation vocabulary. Temporal
        # semantics must be asserted by the actual domain consumer.
        self.assertEqual([], validate_value("not-a-date", {"type": "string", "format": "date-time"}, "fixture"))

    def test_schema_reuse_does_not_cache_instances_mutations_or_coerce_invalid_python_shapes(self):
        schema = {"type": "integer", "minimum": 0}
        self.assertEqual([], validate_value(0, schema, "first"))
        self.assertTrue(validate_value(-1, schema, "second"))
        # Reordering an equivalent definition preserves acceptance, but changing
        # one bound must never reuse the earlier acceptance predicate.
        equivalent = {"minimum": 0, "type": "integer"}
        self.assertEqual([], validate_value(0, equivalent, "equivalent"))
        schema["minimum"] = 1
        self.assertTrue(validate_value(0, schema, "changed"))
        schema["minimum"] = "invalid"
        for label in ("first-owner", "second-owner"):
            errors = validate_value(0, schema, label)
            self.assertTrue(errors)
            self.assertTrue(all(error.startswith(label + ":") for error in errors))
        schema["minimum"] = 0
        self.assertEqual([], validate_value(0, schema, "repaired"))
        self.assertTrue(schema_errors({"required": ("id",)}, "tuple-must-not-become-array"))
        self.assertTrue(validate_value({1: "bad"}, {"properties": {1: {"type": "integer"}}},
                                       "key-must-not-become-string"))

    def test_keyword_inventory_has_an_explicit_rejection_or_annotation_policy(self):
        from jsonschema import Draft202012Validator
        covered = {"$ref", "additionalProperties", "allOf", "anyOf", "const", "contains", "enum",
                   "exclusiveMinimum", "format", "if", "items", "maxItems", "maxLength", "maxProperties",
                   "maximum", "minItems", "minLength", "minProperties", "minimum", "not", "oneOf",
                   "pattern", "prefixItems", "properties", "propertyNames", "required", "type", "uniqueItems"}
        observed = set()
        def walk(node):
            if isinstance(node, dict):
                observed.update(set(node) & set(Draft202012Validator.VALIDATORS))
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)
        for path in (Path(__file__).resolve().parents[1] / "schemas").glob("*.schema.json"):
            walk(json.loads(path.read_text()))
        self.assertFalse(observed - covered, f"add behavioral coverage for new keywords: {observed - covered}")


class BundleCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.site = self.root / "rendered"
        (self.site / "status").mkdir(parents=True)
        (self.site / "status/canonical-public-status.json").write_text(json.dumps({
            "source_commit": "a" * 40, "source_tree_state": "clean",
            "build_context": "tested_commit", "status_id": "custody-fixture",
        }))
        (self.site / "index.html").write_text("first complete page")
        self.output = self.root / "bundle"
        self.original = bundle.build_bundle(self.site, self.output, allow_local=False)

    def assert_original_survives(self):
        self.assertEqual(self.original, json.loads((self.output / bundle.MANIFEST_NAME).read_text()))
        self.assertEqual("first complete page", (self.output / "site/index.html").read_text())

    def test_file_directory_broken_and_root_symlinks(self):
        outside = self.root / "private.txt"
        outside.write_text("outside source boundary")
        external_dir = self.root / "private-dir"
        external_dir.mkdir()
        (external_dir / "secret.txt").write_text("outside directory boundary")
        for target in (outside, external_dir, self.root / "missing"):
            with self.subTest(target=target):
                link = self.site / "linked"
                link.symlink_to(target)
                with self.assertRaisesRegex(ValueError, "symlink"):
                    bundle.build_bundle(self.site, self.output, allow_local=False)
                link.unlink()
                self.assert_original_survives()
        root_link = self.root / "root-link"
        root_link.symlink_to(self.site, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            bundle.build_bundle(root_link, self.output, allow_local=False)

    def test_ancestry_and_unowned_destination(self):
        for destination in (self.site, self.site / "inside", self.root):
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(ValueError, "overlap"):
                    bundle.build_bundle(self.site, destination, allow_local=False)
        unowned = self.root / "unowned"
        unowned.mkdir()
        (unowned / "keep.txt").write_text("keep")
        with self.assertRaisesRegex(ValueError, "not an owned"):
            bundle.build_bundle(self.site, unowned, allow_local=False)
        self.assertEqual("keep", (unowned / "keep.txt").read_text())
        self.assert_original_survives()

    def test_copy_failure_and_changed_source_preserve_previous(self):
        with patch.object(bundle.shutil, "copytree", side_effect=OSError("interrupted copy")):
            with self.assertRaises(OSError):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assert_original_survives()
        real_copy = shutil.copytree
        def changed_copy(*args, **kwargs):
            (self.site / "index.html").write_text("changed during copy")
            return real_copy(*args, **kwargs)
        with patch.object(bundle.shutil, "copytree", side_effect=changed_copy):
            with self.assertRaisesRegex(ValueError, "source changed"):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assert_original_survives()

    def test_late_symlink_is_not_dereferenced(self):
        outside = self.root / "private.txt"
        outside.write_text("secret")
        real_copy = shutil.copytree
        def linked_copy(*args, **kwargs):
            if Path(args[0]).resolve() == self.site.resolve():
                (self.site / "late").symlink_to(outside)
            return real_copy(*args, **kwargs)
        with patch.object(bundle.shutil, "copytree", side_effect=linked_copy):
            with self.assertRaisesRegex(ValueError, "symlink"):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assert_original_survives()

    def test_successful_replacement_contains_complete_new_bundle(self):
        (self.site / "index.html").write_text("second complete page")
        manifest = bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assertNotEqual(self.original["site"]["tree_sha256"], manifest["site"]["tree_sha256"])
        self.assertEqual(manifest, bundle.build_manifest(self.output / "site", allow_local=False))
        self.assertFalse(list(self.root.glob(".bundle-*")))

    def test_unknown_empty_directories_and_linked_ancestry_are_preserved(self):
        sentinel = self.output / "site/personal-empty"
        sentinel.mkdir()
        identity = (sentinel.stat().st_dev, sentinel.stat().st_ino)
        with self.assertRaisesRegex(ValueError, "directory"):
            bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assertEqual(identity, (sentinel.stat().st_dev, sentinel.stat().st_ino))
        alias = self.root / "parent-alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink ancestry"):
            bundle.build_bundle(alias / "rendered", self.root / "fresh", allow_local=False)
        self.assertFalse((self.root / "fresh").exists())

    def test_late_displaced_edit_or_exception_after_exchange_retains_prior(self):
        (self.site / "index.html").write_text("new page")
        exchange = bundle.exchange_directories
        def interrupted(left, right):
            (right / "site/personal-empty").mkdir()
            exchange(left, right)
            raise OSError("authored post-swap exception")
        with patch.object(bundle, "exchange_directories", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "post-swap"):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        retained = list(self.root.glob(".bundle-stage-*"))[0]
        self.assertEqual("first complete page", (retained / "bundle/site/index.html").read_text())
        self.assertTrue((retained / "bundle/site/personal-empty").is_dir())
        self.assertEqual("installation_outcome_unconfirmed", json.loads((retained / "staging.json").read_bytes())["state"])
        self.assertEqual("new page", (self.output / "site/index.html").read_text())

    def test_post_exchange_fsync_failure_retains_complete_prior_bundle(self):
        (self.site / "index.html").write_text("new page")
        sync = bundle.sync_directory
        def fail(directory):
            if directory == self.output.parent:
                raise OSError("authored durability failure")
            sync(directory)
        with patch.object(bundle, "sync_directory", side_effect=fail):
            with self.assertRaisesRegex(OSError, "durability"):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        retained = list(self.root.glob(".bundle-stage-*"))[0]
        self.assertEqual("first complete page", (retained / "bundle/site/index.html").read_text())
        self.assertEqual("new page", (self.output / "site/index.html").read_text())

    def test_absent_bundle_destination_collision_preserves_new_object(self):
        destination = self.root / "fresh"
        rename = bundle.install_directory_noreplace
        identity = None
        def collided(left, right):
            nonlocal identity
            right.mkdir()
            identity = (right.stat().st_dev, right.stat().st_ino)
            rename(left, right)
        with patch.object(bundle, "install_directory_noreplace", side_effect=collided):
            with self.assertRaises(FileExistsError):
                bundle.build_bundle(self.site, destination, allow_local=False)
        self.assertEqual(identity, (destination.stat().st_dev, destination.stat().st_ino))
        self.assertEqual([], list(destination.iterdir()))

    def test_validator_refuses_linked_metadata_before_loading_bytes(self):
        marker = self.output / bundle.MANIFEST_NAME
        marker.unlink()
        outside = self.root / "outside.json"
        outside.write_text("not JSON; must not be read")
        marker.symlink_to(outside)
        result = subprocess.run([sys.executable, str(Path(bundle.__file__).with_name("validate_tested_site_bundle.py")),
                                 "--bundle", str(self.output)], capture_output=True, text=True, timeout=30)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("symlink", result.stderr)
        self.assertNotIn("JSONDecodeError", result.stderr)
        self.assertEqual("not JSON; must not be read", outside.read_text())

    def test_failed_exchange_and_competing_builder_preserve_previous(self):
        (self.site / "index.html").write_text("new page")
        with patch.object(bundle, "exchange_directories", side_effect=OSError("exchange unsupported")):
            with self.assertRaises(OSError):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assert_original_survives()
        with bundle.bundle_lock(self.output):
            with self.assertRaisesRegex(ValueError, "another builder"):
                bundle.build_bundle(self.site, self.output, allow_local=False)
        self.assert_original_survives()

    def test_process_exit_at_exchange_never_exposes_partial_bundle(self):
        (self.site / "index.html").write_text("new page")
        script = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import build_tested_site_bundle as b
exchange = b.exchange_directories
def interrupted(left, right):
    if sys.argv[4] == "before":
        os._exit(90)
    exchange(left, right)
    os._exit(91)
b.exchange_directories = interrupted
b.build_bundle(Path(sys.argv[2]), Path(sys.argv[3]), allow_local=False)
'''
        scripts = str(Path(bundle.__file__).parent)
        for phase, code in (("before", 90), ("after", 91)):
            with self.subTest(phase=phase):
                result = subprocess.run(
                    [sys.executable, "-c", script, scripts, str(self.site), str(self.output), phase],
                    capture_output=True, timeout=30,
                )
                self.assertEqual(code, result.returncode, result.stderr.decode())
                manifest = json.loads((self.output / bundle.MANIFEST_NAME).read_text())
                self.assertEqual(manifest, bundle.build_manifest(self.output / "site", allow_local=False))
                if phase == "before":
                    self.assert_original_survives()
                else:
                    self.assertEqual("new page", (self.output / "site/index.html").read_text())


if __name__ == "__main__":
    unittest.main()
