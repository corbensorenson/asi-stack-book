"""Generated-product custody controls; no new chapter or research result."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import generated_directory as transaction
import build_product_projections as products
from build_canonical_public_status import build_status


class GeneratedDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "output"
        self.payload = {"index.html": b"old complete fixture", "assets/a.txt": b"x"}
        self.inputs = {"fixture/input.json": "a" * 64, "fixture/absent.json": None}
        self.install()
        self.before = transaction.file_rows(self.output)

    def install(self, **kwargs):
        return transaction.install(self.output, family="product_fixture", payload=self.payload, inputs=self.inputs,
                                   guard=kwargs.pop("guard", lambda: None), **kwargs)

    def update(self):
        self.payload["index.html"] = b"new complete fixture"

    def stages(self):
        return list(self.root.glob(".output-product_fixture-stage-*"))

    def test_complete_update_noop_and_nonwriting_check(self):
        self.update()
        self.install()
        times = {path: path.stat().st_mtime_ns for path in self.root.rglob("*")}
        self.install(check=True)
        self.install()
        self.assertEqual(times, {path: path.stat().st_mtime_ns for path in self.root.rglob("*")})
        self.assertEqual(b"new complete fixture", (self.output / "index.html").read_bytes())
        self.assertFalse(self.stages())

    def test_stale_check_and_exact_legacy_adoption(self):
        (self.output / transaction.RECEIPT).unlink()
        with self.assertRaisesRegex(ValueError, "unreceipted"):
            self.install(check=True)
        self.install()
        (self.output / transaction.RECEIPT).unlink()
        self.update()
        with self.assertRaisesRegex(ValueError, "legacy"):
            self.install()
        self.assertEqual(b"old complete fixture", (self.output / "index.html").read_bytes())

    def test_noop_cannot_adopt_an_edit_after_the_ownership_check(self):
        inspect = transaction.previous_is_owned
        def changed(*args, **kwargs):
            result = inspect(*args, **kwargs)
            (self.output / "index.html").write_text("concurrent authored edit")
            return result
        with patch.object(transaction, "previous_is_owned", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "changed"):
                self.install()
        self.assertEqual("concurrent authored edit", (self.output / "index.html").read_text())

    def test_unknown_files_damaged_receipt_and_numeric_coercion_preserve_prior(self):
        marker = self.output / transaction.RECEIPT
        original = marker.read_bytes()
        (self.output / "personal.txt").write_text("preserve fixture")
        with self.assertRaisesRegex(ValueError, "integrity"):
            self.install()
        self.assertEqual("preserve fixture", (self.output / "personal.txt").read_text())
        (self.output / "personal.txt").unlink()
        for mutation in (lambda row: row.update(release_effect="approved"),
                         lambda row: row["files"][0].update(size=True),
                         lambda row: row.update(input_sha256={"bad": True})):
            record = json.loads(original)
            mutation(record)
            marker.write_text(json.dumps(record))
            with self.assertRaises(ValueError):
                self.install()
            self.assertEqual(b"old complete fixture", (self.output / "index.html").read_bytes())
        marker.write_bytes(original)

    def test_unknown_empty_directory_is_preserved_in_owned_and_legacy_outputs(self):
        personal = self.output / "personal/empty"
        personal.mkdir(parents=True)
        identity = (personal.stat().st_dev, personal.stat().st_ino)
        self.update()
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                if legacy:
                    (self.output / transaction.RECEIPT).unlink()
                with self.assertRaisesRegex(ValueError, "directory"):
                    self.install()
                self.assertEqual(identity, (personal.stat().st_dev, personal.stat().st_ino))
                self.assertEqual(b"old complete fixture", (self.output / "index.html").read_bytes())

    def test_failed_sync_exchange_and_input_guard_keep_prior(self):
        self.update()
        for function in ("sync_stage", "exchange_directories"):
            with patch.object(transaction, function, side_effect=OSError("authored failure")):
                with self.assertRaises(OSError):
                    self.install()
            self.assertEqual(self.before, transaction.file_rows(self.output))
            if function == "sync_stage":
                self.assertFalse(self.stages())
            else:
                retained = self.stages()[0]
                self.assertEqual("installation_outcome_unconfirmed", json.loads((retained / "staging.json").read_bytes())["state"])
                self.assertEqual(b"new complete fixture", (retained / "payload/index.html").read_bytes())
        calls = 0
        def drift():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise ValueError("authored source drift")
        with self.assertRaisesRegex(ValueError, "source drift"):
            self.install(guard=drift)
        self.assertEqual(self.before, transaction.file_rows(self.output))

    def test_shared_writer_lock_and_linked_roots_refuse(self):
        with transaction.bundle_lock(self.output):
            with self.assertRaisesRegex(ValueError, "another builder"):
                self.install()
        linked = self.root / "linked"
        linked.symlink_to(self.output, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            transaction.install(linked, family="product_fixture", payload=self.payload, inputs=self.inputs, guard=lambda: None)
        (self.output / "linked-file").symlink_to(self.root / "outside")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.install()

    def test_concurrent_edit_and_readonly_receipt_drift_are_preserved(self):
        self.update()
        original = transaction.sync_stage
        def edit(stage):
            original(stage)
            (self.output / "index.html").write_text("concurrent fixture edit")
        with patch.object(transaction, "sync_stage", side_effect=edit):
            with self.assertRaisesRegex(ValueError, "concurrent"):
                self.install()
        self.assertEqual("concurrent fixture edit", (self.output / "index.html").read_text())
        (self.output / "index.html").write_bytes(b"old complete fixture")
        self.payload["index.html"] = b"old complete fixture"
        calls = 0
        def receipt_edit():
            nonlocal calls
            calls += 1
            if calls == 2:
                marker = self.output / transaction.RECEIPT
                record = json.loads(marker.read_bytes())
                record["input_sha256"]["fixture/input.json"] = "b" * 64
                marker.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "changed"):
            self.install(check=True, guard=receipt_edit)

    def test_unsafe_payload_namespace_refuses_before_directory_creation(self):
        empty = self.root / "not-created/child"
        for payload in ({"../outside": b"x"}, {transaction.RECEIPT: b"x"}, {"a": b"x", "a/b": b"y"}, {"bad\nname": b"x"}):
            with self.assertRaises(ValueError):
                transaction.install(empty, family="product_fixture", payload=payload, inputs=self.inputs, guard=lambda: None)
        self.assertFalse(empty.parent.exists())

    def test_process_exit_before_and_after_exchange_keeps_complete_tree_and_journal(self):
        self.update()
        script = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import generated_directory as t
exchange=t.exchange_directories
def interrupt(left,right):
    if sys.argv[3]=='before': os._exit(90)
    exchange(left,right)
    os._exit(91)
t.exchange_directories=interrupt
t.install(Path(sys.argv[2]),family='product_fixture',payload={'index.html':b'new complete fixture','assets/a.txt':b'x'},inputs={'fixture/input.json':'a'*64,'fixture/absent.json':None},guard=lambda:None)
'''
        for phase, code, value in (("before", 90, b"old complete fixture"), ("after", 91, b"new complete fixture")):
            result = subprocess.run([sys.executable, "-c", script, str(Path(transaction.__file__).parent), str(self.output), phase],
                                    capture_output=True, timeout=30)
            self.assertEqual(code, result.returncode, result.stderr.decode())
            self.assertEqual(value, (self.output / "index.html").read_bytes())
            marker = json.loads((self.output / transaction.RECEIPT).read_bytes())
            self.assertEqual(marker["files"], transaction.payload_rows(self.output))
            self.assertTrue(self.stages())
            self.assertTrue(all(json.loads((stage / "staging.json").read_bytes())["state"] == "installation_attempted" for stage in self.stages()))

    def test_exception_after_physical_exchange_retains_displaced_prior_tree(self):
        self.update()
        exchange = transaction.exchange_directories
        def interrupted(left, right):
            exchange(left, right)
            raise OSError("authored exception after physical swap")
        with patch.object(transaction, "exchange_directories", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "physical swap"):
                self.install()
        self.assertEqual(b"new complete fixture", (self.output / "index.html").read_bytes())
        retained = self.stages()[0]
        self.assertEqual(b"old complete fixture", (retained / "payload/index.html").read_bytes())
        self.assertEqual("installation_outcome_unconfirmed", json.loads((retained / "staging.json").read_bytes())["state"])

    def test_late_prior_edit_after_last_scan_is_retained(self):
        self.update()
        exchange = transaction.exchange_directories
        def changed(left, right):
            (right / "personal-empty").mkdir()
            exchange(left, right)
        with patch.object(transaction, "exchange_directories", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "directory"):
                self.install()
        self.assertTrue((self.stages()[0] / "payload/personal-empty").is_dir())
        self.assertEqual(b"new complete fixture", (self.output / "index.html").read_bytes())

    def test_absent_destination_race_never_overwrites_new_empty_directory(self):
        destination = self.root / "fresh"
        rename = transaction.install_directory_noreplace
        identity = None
        def collided(left, right):
            nonlocal identity
            right.mkdir()
            identity = (right.stat().st_dev, right.stat().st_ino)
            rename(left, right)
        with patch.object(transaction, "install_directory_noreplace", side_effect=collided):
            with self.assertRaises(FileExistsError):
                transaction.install(destination, family="product_fixture", payload=self.payload,
                                    inputs=self.inputs, guard=lambda: None)
        self.assertEqual(identity, (destination.stat().st_dev, destination.stat().st_ino))
        self.assertEqual([], list(destination.iterdir()))

    def test_post_exchange_fsync_uncertainty_retains_complete_prior_payload(self):
        self.update()
        original = transaction.sync_directory
        def fail(directory):
            if directory == self.output.parent:
                raise OSError("authored durability uncertainty")
            original(directory)
        with patch.object(transaction, "sync_directory", side_effect=fail):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual(b"new complete fixture", (self.output / "index.html").read_bytes())
        stage = self.stages()[0]
        self.assertEqual(b"old complete fixture", (stage / "payload/index.html").read_bytes())
        self.assertEqual("installed_durability_unconfirmed", json.loads((stage / "staging.json").read_bytes())["state"])


class ProductTransactionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.status = build_status(timestamp="2026-10-02T00:00:00Z", source_commit_override="0" * 40,
                                  source_tree_state_override="dirty")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-custody-fixture-", dir=products.ROOT / "build")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "products"
        self.status_path = self.root / "status.json"
        self.status_path.write_text(json.dumps(self.status))
        products.build_products(self.output, self.status_path)
        self.before = transaction.file_rows(self.output)

    def test_real_builder_complete_byte_check_is_pure_and_noop(self):
        times = {path: path.stat().st_mtime_ns for path in self.root.rglob("*")}
        products.build_products(self.output, self.status_path, check=True)
        products.build_products(self.output, self.status_path)
        self.assertEqual(times, {path: path.stat().st_mtime_ns for path in self.root.rglob("*")})

    def test_domain_failure_stale_status_and_canonical_output_refuse(self):
        with patch.object(products, "build_reference", side_effect=ValueError("authored domain failure")):
            with self.assertRaises(ValueError):
                products.build_products(self.output, self.status_path)
        status = copy.deepcopy(self.status)
        status["counts"]["sources"] += 1
        self.status_path.write_text(json.dumps(status))
        with self.assertRaises(ValueError):
            products.build_products(self.output, self.status_path)
        forbidden = products.ROOT / "chapters/never-created-products-fixture"
        with self.assertRaisesRegex(ValueError, "ignored build"):
            products.build_products(forbidden, self.status_path)
        self.assertFalse(forbidden.exists())
        self.assertEqual(self.before, transaction.file_rows(self.output))

    def test_source_drift_after_in_memory_preparation_preserves_prior(self):
        original = products.prepare_payload
        def drift(output, inputs):
            result = original(output, inputs)
            self.status_path.write_bytes(self.status_path.read_bytes() + b"\n")
            return result
        with patch.object(products, "prepare_payload", side_effect=drift):
            with self.assertRaisesRegex(ValueError, "changed"):
                products.build_products(self.output, self.status_path)
        self.assertEqual(self.before, transaction.file_rows(self.output))

    def test_dynamic_status_timestamp_does_not_rewrite_consumed_projection(self):
        status = copy.deepcopy(self.status)
        with patch.object(products, "build_status", side_effect=lambda: dict(status)):
            products.build_products(self.output)
            times = {path: path.stat().st_mtime_ns for path in self.root.rglob("*")}
            status["build_timestamp"] = "2026-10-02T00:00:01Z"
            products.build_products(self.output, check=True)
            products.build_products(self.output)
            self.assertEqual(times, {path: path.stat().st_mtime_ns for path in self.root.rglob("*")})


if __name__ == "__main__":
    unittest.main()
