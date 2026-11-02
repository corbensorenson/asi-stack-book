"""Disposable archive-custody controls; no release or natural task admission."""

import copy
import json
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_immutable_site_archive as archive
import validate_immutable_site_archive as validator
import generated_directory as transaction
from build_tested_site_bundle import file_rows
import build_tested_site_bundle as bundles


class ImmutableArchiveTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="asi-archive-custody-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bundle = validator.build_self_test_bundle(self.root)
        self.policy = copy.deepcopy(archive.load_json(archive.POLICY))
        row = dict(self.policy["known_releases"][0])
        row.update(version="v9.9.9", source_commit="a" * 40, site_artifact_state="not_published",
                   site_artifact_url="", site_artifact_sha256="")
        row.pop("archive_backfill_decision", None)
        self.policy["known_releases"] = [row]
        self.policy_path = self.root / "policy.json"
        self.write_policy()
        self.output = self.root / "candidate"
        self.candidate = self.build()
        self.before = file_rows(self.output)

    def write_policy(self):
        self.policy_path.write_text(json.dumps(self.policy, indent=2) + "\n")

    def build(self, **kwargs):
        return archive.build_candidate(self.bundle, kwargs.pop("output", self.output),
                                       kwargs.pop("version", "v9.9.9"), allow_local=False,
                                       policy_path=self.policy_path, **kwargs)

    def assert_prior(self):
        self.assertEqual(self.before, file_rows(self.output))

    def test_unowned_file_and_empty_directory_are_preserved(self):
        sentinel = self.output / "personal-fixture.txt"
        sentinel.write_text("retain authored fixture")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual("retain authored fixture", sentinel.read_text())
        sentinel.unlink()
        empty = self.output / "personal-empty"
        empty.mkdir()
        identity = (empty.stat().st_dev, empty.stat().st_ino)
        with self.assertRaisesRegex(ValueError, "directory"):
            self.build()
        self.assertEqual(identity, (empty.stat().st_dev, empty.stat().st_ino))

    def test_stale_bundle_manifest_refuses_before_replacing_candidate(self):
        (self.bundle / "site/index.html").write_text("changed source under old manifest")
        with self.assertRaisesRegex(ValueError, "bundle"):
            self.build()
        self.assert_prior()

    def test_source_drift_during_packaging_preserves_candidate(self):
        pack = archive.archive_bytes
        def changed(*args, **kwargs):
            body = pack(*args, **kwargs)
            (self.bundle / "site/index.html").write_text("changed during packaging")
            return body
        with patch.object(archive, "archive_bytes", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "changed"):
                self.build()
        self.assert_prior()

    def test_source_and_policy_ancestry_overlap_refuses_without_deleting_inputs(self):
        source = file_rows(self.bundle)
        for output in (self.bundle, self.bundle / "site/archive", self.root):
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, "overlap"):
                    self.build(output=output)
                self.assertEqual(source, file_rows(self.bundle))
                self.assertTrue(self.policy_path.is_file())
                self.assert_prior()

    def test_identical_rebuild_preserves_objects_and_validation_does_not_write(self):
        objects = {path.relative_to(self.output).as_posix(): (path.stat().st_ino, path.stat().st_mtime_ns)
                   for path in (self.output, *self.output.rglob("*"))}
        self.assertEqual(self.candidate, self.build())
        self.assertEqual(objects, {path.relative_to(self.output).as_posix(): (path.stat().st_ino, path.stat().st_mtime_ns)
                                  for path in (self.output, *self.output.rglob("*"))})
        result = subprocess.run([sys.executable, str(Path(validator.__file__)), "--bundle", str(self.bundle),
                                 "--candidate", str(self.output), "--policy", str(self.policy_path)],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assert_prior()

    def test_consumer_refuses_changed_adjacent_checksum(self):
        checksum = self.output / (self.candidate["archive"]["filename"] + ".sha256")
        checksum.write_text("incorrect adjacent checksum\n")
        errors = validator.validate_candidate(self.candidate, self.output, self.bundle,
                                             allow_local=False, policy_path=self.policy_path)
        self.assertTrue(errors, "candidate consumer ignored its named checksum artifact")
        self.assertEqual("incorrect adjacent checksum\n", checksum.read_text())

    def test_consumer_refuses_edits_after_positive_check_and_preserves_them(self):
        targets = (self.output / (self.candidate["archive"]["filename"] + ".sha256"),
                   self.bundle / "site/index.html", self.policy_path)
        for target in targets:
            with self.subTest(target=target):
                original = target.read_bytes()
                edited = original + b"\nintervening authored fixture edit\n"
                def changed(*args, **kwargs):
                    target.write_bytes(edited)
                    return []
                with patch.object(validator, "negative_controls", side_effect=changed):
                    _, errors = validator.check_candidate(self.output, self.bundle, allow_local=False,
                                                           policy_path=self.policy_path)
                self.assertTrue(any("complete validation/control operation" in error for error in errors), errors)
                self.assertEqual(edited, target.read_bytes())
                target.write_bytes(original)  # Only restore this owned fixture for the next case.

    def test_readonly_builder_check_and_exact_legacy_adoption(self):
        times = {path: path.stat().st_mtime_ns for path in self.root.rglob("*")}
        self.assertEqual(self.candidate, self.build(check=True))
        self.assertEqual(times, {path: path.stat().st_mtime_ns for path in self.root.rglob("*")})
        (self.output / transaction.RECEIPT).unlink()
        with self.assertRaisesRegex(ValueError, "unreceipted"):
            self.build(check=True)
        payload = {path.name: path.read_bytes() for path in self.output.iterdir()}
        self.build()
        self.assertEqual(payload, {path.name: path.read_bytes() for path in self.output.iterdir()
                                  if path.name != transaction.RECEIPT})

    def test_another_version_or_different_archive_cannot_replace_prior_identity(self):
        self.policy["known_releases"][0]["version"] = "v9.9.8"
        self.write_policy()
        with self.assertRaisesRegex(ValueError, "prior archive identity"):
            self.build(version="v9.9.8")
        self.assert_prior()
        self.policy["known_releases"][0]["version"] = "v9.9.9"
        self.write_policy()
        (self.bundle / "site/index.html").write_text("a different, valid bundle for the same commit")
        (self.bundle / archive.MANIFEST_NAME).write_text(json.dumps(bundles.build_manifest(self.bundle / "site", allow_local=False)))
        with self.assertRaisesRegex(ValueError, "prior archive identity"):
            self.build()
        self.assert_prior()

    def test_preparation_failure_and_unsafe_payload_do_not_replace_or_create_output(self):
        with patch.object(archive, "archive_bytes", return_value=b"not a gzip archive"):
            with self.assertRaisesRegex(ValueError, "domain acceptance"):
                self.build()
        self.assert_prior()
        for template in ("../bad.tar.gz", "bad\\name.tar.gz", "bad\nname.tar.gz"):
            self.policy["immutable_channel"]["artifact_name_template"] = template
            self.write_policy()
            fresh = self.root / "not-created/child"
            with self.assertRaises(ValueError):
                self.build(output=fresh)
            self.assertFalse(fresh.parent.exists())

    def test_consumer_rejects_producer_inventory_omission_and_content_rewrite(self):
        inspected = archive.inspect_bundle(self.bundle, allow_local=False)
        payload = {path.name: path.read_bytes() for path in self.output.iterdir()
                   if path.name != transaction.RECEIPT}
        self.assertEqual([], validator.validate_candidate_payload(
            self.candidate, payload, inspected, self.policy,
            self.policy_path.read_bytes(), self.policy_path.name, allow_local=False))
        select = archive.source_members
        for target, replacement in (("site/index.html", None),
                                    (archive.MANIFEST_NAME, None),
                                    ("site/index.html", b"producer-rewritten content")):
            with self.subTest(target=target, replacement=replacement):
                def broken_selection(*args, **kwargs):
                    rows = select(*args, **kwargs)
                    return [(name, replacement if name.endswith("/" + target) else body)
                            for name, body in rows
                            if replacement is not None or not name.endswith("/" + target)]
                members = broken_selection(self.bundle, self.candidate["archive"]["root_directory"],
                                           inspected=inspected)
                body = archive.archive_bytes(members, self.candidate["archive"]["root_directory"])
                candidate = copy.deepcopy(self.candidate)
                candidate["archive"].update(sha256=archive.sha256_bytes(body), size=len(body),
                                             member_count=len(members))
                filename = candidate["archive"]["filename"]
                corrupted = {filename: body,
                             archive.CANDIDATE_MANIFEST: (json.dumps(candidate) + "\n").encode(),
                             filename + ".sha256": f"{candidate['archive']['sha256']}  {filename}\n".encode()}
                with patch.object(archive, "source_members", side_effect=broken_selection):
                    errors = validator.validate_candidate_payload(candidate, corrupted, inspected, self.policy,
                                      self.policy_path.read_bytes(), self.policy_path.name, allow_local=False)
                    self.assertTrue(any("contents differ from tested bundle" in error for error in errors), errors)
                    with self.assertRaisesRegex(ValueError, "domain acceptance"):
                        self.build()
                self.assert_prior()

    def test_linked_source_metadata_inputs_and_candidates_are_refused_without_writes(self):
        private = self.root / "private-fixture"
        private.write_bytes(b"private fixture must not be loaded")
        for target in (self.bundle / archive.MANIFEST_NAME, self.policy_path,
                       self.output / archive.CANDIDATE_MANIFEST):
            original = target.read_bytes()
            target.unlink(); target.symlink_to(private)
            with self.subTest(target=target):
                with self.assertRaises((ValueError, OSError)):
                    self.build()
                self.assertTrue(target.is_symlink())
                self.assertEqual(b"private fixture must not be loaded", private.read_bytes())
            target.unlink(); target.write_bytes(original)
        alias = self.root / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink ancestry"):
            self.build(output=alias / "fresh")
        self.assertFalse((self.root / "fresh").exists())

    def test_fifo_and_unknown_bundle_directories_refuse_before_reading(self):
        policy = self.policy_path.read_bytes()
        self.policy_path.unlink(); os.mkfifo(self.policy_path)
        try:
            with self.assertRaisesRegex(ValueError, "regular file"):
                self.build()
        finally:
            self.policy_path.unlink(); self.policy_path.write_bytes(policy)
        (self.bundle / "site/personal-empty").mkdir()
        with self.assertRaisesRegex(ValueError, "directory"):
            self.build()
        self.assertTrue((self.bundle / "site/personal-empty").is_dir())
        self.assert_prior()

    def test_policy_publication_and_declined_backfill_refuse_before_writes(self):
        row = self.policy["known_releases"][0]
        for field, value in (("site_artifact_state", "published"),
                             ("archive_backfill_decision", "declined_historical_render_not_available")):
            previous = row.copy()
            row[field] = value; self.write_policy()
            with self.assertRaisesRegex(ValueError, "published|declined"):
                self.build()
            self.assert_prior()
            row.clear(); row.update(previous)

    def test_post_exchange_exception_or_source_drift_retains_prior_archive(self):
        # Metadata-only policy changes keep the exact archive identity.
        self.policy_path.write_text(self.policy_path.read_text() + "\n")
        exchange = transaction.exchange_directories
        def interrupted(left, right):
            exchange(left, right)
            raise OSError("authored post-swap exception")
        with patch.object(transaction, "exchange_directories", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "post-swap"):
                self.build()
        stage = list(self.root.glob(".candidate-immutable_site_archive-stage-*"))[0]
        self.assertEqual(self.before, file_rows(stage / "payload"))
        self.assertEqual("installation_outcome_unconfirmed", json.loads((stage / "staging.json").read_bytes())["state"])
        prior = file_rows(self.output)
        self.policy_path.write_text(self.policy_path.read_text() + "\n")
        def changed(left, right):
            exchange(left, right)
            (self.bundle / "site/index.html").write_text("late source change")
        with patch.object(transaction, "exchange_directories", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "changed"):
                self.build()
        self.assertTrue(any(file_rows(item / "payload") == prior for item in self.root.glob(".candidate-immutable_site_archive-stage-*")))

    def test_fsync_and_new_destination_collision_keep_owned_payload_and_unknown_objects(self):
        self.policy_path.write_text(self.policy_path.read_text() + "\n")
        sync = transaction.sync_directory
        def failed(directory):
            if directory == self.output.parent:
                raise OSError("authored durability uncertainty")
            sync(directory)
        with patch.object(transaction, "sync_directory", side_effect=failed):
            with self.assertRaisesRegex(OSError, "durability"):
                self.build()
        stage = list(self.root.glob(".candidate-immutable_site_archive-stage-*"))[0]
        self.assertEqual(self.before, file_rows(stage / "payload"))
        fresh = self.root / "fresh"
        rename = transaction.install_directory_noreplace
        identity = None
        def collided(left, right):
            nonlocal identity
            right.mkdir(); identity = (right.stat().st_dev, right.stat().st_ino)
            rename(left, right)
        with patch.object(transaction, "install_directory_noreplace", side_effect=collided):
            with self.assertRaises(FileExistsError):
                self.build(output=fresh)
        self.assertEqual(identity, (fresh.stat().st_dev, fresh.stat().st_ino))
        self.assertEqual([], list(fresh.iterdir()))

    def test_tar_parser_rejects_duplicate_unknown_empty_directory_and_excess_expansion(self):
        def packed(rows):
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode="w:gz") as tar:
                for name, body, directory in rows:
                    tar.addfile(archive.tar_info(name, len(body), directory=directory), io.BytesIO(body) if not directory else None)
            return stream.getvalue()
        expected = {"root/file": b"x"}
        for rows in ([('root/file', b'x', False), ('root/file', b'x', False)],
                     [('root/unknown-empty', b'', True)], [('root/file', b'x' * 100000, False)]):
            files, errors = validator.archive_member_data(packed(rows), expected)
            self.assertTrue(errors)
        files, errors = validator.archive_member_data(packed([('root', b'', True), ('root/file', b'x', False)]), expected)
        self.assertEqual([], errors)
        self.assertEqual(expected, files)

    def test_metadata_type_coercion_and_policy_authority_drift_are_not_accepted(self):
        payload = {path.name: path.read_bytes() for path in self.output.iterdir() if path.name != transaction.RECEIPT}
        inspected = archive.inspect_bundle(self.bundle, allow_local=False)
        candidate = copy.deepcopy(self.candidate)
        candidate["archive"]["timestamp_epoch"] = False
        changed = {**payload, archive.CANDIDATE_MANIFEST: json.dumps(candidate).encode()}
        self.assertTrue(validator.validate_candidate_payload(self.candidate, changed, inspected, self.policy,
                         self.policy_path.read_bytes(), self.policy_path.name, allow_local=False))
        for field in ("storage_authority", "release_record"):
            mutated = copy.deepcopy(self.candidate); mutated["publication"][field] = "invented authority"
            self.assertTrue(validator.validate_candidate_payload(mutated,
                             {**payload, archive.CANDIDATE_MANIFEST: json.dumps(mutated).encode()}, inspected,
                             self.policy, self.policy_path.read_bytes(), self.policy_path.name, allow_local=False))


if __name__ == "__main__":
    unittest.main()
