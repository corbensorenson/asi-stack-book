"""Sequence-level custody checks against an independent namespace model.

The oracle never calls the producer's ownership, inventory, receipt or digest
functions. Its states are absent, receipted, unreceipted and externally damaged.
Only an absent destination, an intact same-family receipt, or an unreceipted
exact payload can be replaced. A check requires the current receipt identity.
Faults before commit preserve the prior namespace; faults after the namespace
operation retain a complete replacement and the displaced prior tree.

These are serialized authored actions and controlled process exceptions, not
concurrent schedules, physical power failures, natural tasks or release approval.
JSON/SHA-256, the OS and the installed Hypothesis implementation remain shared
dependencies. The public receipt wire format is a shared specification.
"""

from contextlib import ExitStack
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

from hypothesis import settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, invariant, precondition, rule, run_state_machine_as_test

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import generated_directory as producer

MARKER = "projection-install-manifest.json"
FAMILIES = ("custody_a", "custody_b")
MODES = ("normal", "source_drift", "prepare_failure", "after_namespace_failure")
STARTS = ("absent", "receipted", "unreceipted", "changed_input", "other_family", "foreign_file", "foreign_directory")


def payload(version):
    return {"index.html": f"generation-{version}".encode(),
            "assets/data.txt": bytes([version])}


def inputs(version):
    return {"source/input.json": hashlib.sha256(str(version).encode()).hexdigest(),
            "source/absent.json": None}


def namespace(path, *, metadata=False):
    """Observe node types/bytes without dereferencing any link or using the producer."""
    if not path.exists() and not path.is_symlink():
        return None
    result = {}
    def visit(node, relative):
        info = node.lstat()
        if stat.S_ISLNK(info.st_mode):
            value = ("link", os.readlink(node))
        elif stat.S_ISDIR(info.st_mode):
            value = ("directory",)
        elif stat.S_ISREG(info.st_mode):
            value = ("file", node.read_bytes())
        else:
            value = ("special", stat.S_IFMT(info.st_mode))
        if metadata:
            value += (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_mode)
        result[relative] = value
        if value[0] == "directory":
            for child in sorted(node.iterdir()):
                visit(child, child.name if not relative else relative + "/" + child.name)
    visit(path, "")
    return result


def expected_receipt(family, data, identities):
    rows = [{"path": name, "size": len(body), "sha256": hashlib.sha256(body).hexdigest()}
            for name, body in sorted(data.items())]
    wire = b"".join((r["path"] + "\0" + str(r["size"]) + "\0" + r["sha256"] + "\n").encode()
                    for r in rows)
    return {"schema_version": "asi_stack.generated_directory_install.v1", "family": family,
            "input_sha256": identities, "files": rows,
            "payload_tree_sha256": hashlib.sha256(wire).hexdigest(),
            "support_state_effect": "none", "release_effect": "none"}


@dataclass
class OwnershipModel:
    kind: str = "absent"
    files: dict = field(default_factory=dict)
    family: str | None = None
    identities: dict = field(default_factory=dict)

    def permits(self, data, identities, family, *, check):
        if check:
            return (self.kind == "receipted" and self.files == data
                    and self.identities == identities and self.family == family)
        return (self.kind == "absent"
                or (self.kind == "receipted" and self.family == family)
                or (self.kind == "unreceipted" and self.files == data))

    def is_noop(self, data, identities, family):
        return self.permits(data, identities, family, check=True)

    def installed(self, data, identities, family):
        self.kind, self.files, self.identities, self.family = "receipted", dict(data), dict(identities), family


class CustodyMachine(RuleBasedStateMachine):
    """The only production entry point is install; all predictions precede it."""
    def __init__(self):
        super().__init__()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "published"
        self.outside = self.root / "outside-sentinel"
        self.outside.write_bytes(b"outside bytes must never be copied")
        self.model = OwnershipModel()
        self.version = self.source_version = self.family_index = 0
        self.observed = None
        self.trace = []

    def teardown(self):
        self.temp.cleanup()  # Every object is an owned disposable test fixture.

    def desired(self):
        return payload(self.version), inputs(self.source_version), FAMILIES[self.family_index]

    @initialize(start=st.sampled_from(STARTS))
    def seed_state(self, start):
        # Exercise important state/operation joins without claiming random
        # sequences guarantee coverage. Ordinary rules still interleave freely.
        if start == "absent":
            return
        self.publish(False, "normal")
        if start == "unreceipted":
            self.remove_receipt()
        elif start == "changed_input":
            self.propose(0, 1, 0)
        elif start == "other_family":
            self.propose(1, 0, 1)
        elif start in ("foreign_file", "foreign_directory"):
            self.external_object("file" if start == "foreign_file" else "empty_directory")
            self.propose(1, 0, 0)

    @rule(version=st.integers(0, 3), source_version=st.integers(0, 3), family=st.integers(0, 1))
    def propose(self, version, source_version, family):
        self.version, self.source_version, self.family_index = version, source_version, family
        self.trace.append(("propose", version, source_version, family))

    @rule(check=st.booleans(), mode=st.sampled_from(MODES))
    def attempt_publish(self, check, mode):
        self.publish(check, mode)

    def publish(self, check, mode):
        data, identities, family = self.desired()
        allowed = self.model.permits(data, identities, family, check=check)
        noop = self.model.is_noop(data, identities, family)
        changes = allowed and not check and not noop
        before = namespace(self.output)
        times = namespace(self.output, metadata=True)
        calls = 0
        def guard():
            nonlocal calls
            calls += 1
            if mode == "source_drift" and calls == 2:
                raise ValueError("authored input drift")
        exchange, exclusive = producer.exchange_directories, producer.install_directory_noreplace
        def interrupt(operation):
            def run(left, right):
                operation(left, right)
                raise OSError("authored exception after namespace installation")
            return run
        with ExitStack() as faults:
            if mode == "prepare_failure":
                faults.enter_context(patch.object(producer, "sync_stage", side_effect=OSError("authored preparation failure")))
            elif mode == "after_namespace_failure":
                faults.enter_context(patch.object(producer, "exchange_directories", interrupt(exchange)))
                faults.enter_context(patch.object(producer, "install_directory_noreplace", interrupt(exclusive)))
            try:
                received = producer.install(self.output, family=family, payload=data, inputs=identities,
                                            guard=guard, check=check)
                rejected = False
            except (ValueError, OSError):
                rejected = True
        expected_rejection = not allowed or mode == "source_drift" or (changes and mode != "normal")
        assert rejected == expected_rejection, "installation outcome disagrees with the custody model"
        if not rejected:
            assert json.dumps(received, sort_keys=True) == json.dumps(expected_receipt(family, data, identities), sort_keys=True), "successful result returned a contradictory receipt"
        committed = changes and mode in ("normal", "after_namespace_failure")
        if committed:
            self.model.installed(data, identities, family)
            self.assert_complete_generation(data, identities, family)
        else:
            assert namespace(self.output) == before, "refusal/check/no-op changed the prior namespace"
            assert namespace(self.output, metadata=True) == times, "refusal/check/no-op changed prior object metadata"
        if changes and mode == "after_namespace_failure":
            stages = list(self.root.glob(".published-*-stage-*"))
            assert any(namespace(stage / "payload") == before for stage in stages) if before is not None else stages
            assert any(json.loads((stage / "staging.json").read_text())["state"] == "installation_outcome_unconfirmed"
                       for stage in stages), "uncertain installation lost its journal"
        self.observed = namespace(self.output)
        self.trace.append(("publish", check, mode, "rejected" if rejected else "accepted"))

    def assert_complete_generation(self, data, identities, family):
        observed = namespace(self.output)
        assert observed is not None
        expected_names = {"", "assets", *data, MARKER}
        assert set(observed) == expected_names, "installed generation has missing or unowned objects"
        for name, body in data.items():
            assert observed[name] == ("file", body), "installed generation mixes payload bytes"
        record = json.loads(observed[MARKER][1])
        assert json.dumps(record, sort_keys=True) == json.dumps(expected_receipt(family, data, identities), sort_keys=True), "receipt does not bind the complete intended generation"

    @precondition(lambda self: self.model.kind != "absent")
    @rule(value=st.integers(0, 3))
    def external_edit(self, value):
        (self.output / "index.html").write_bytes(f"external-{value}".encode())
        self.model.kind = "damaged"
        self.observed = namespace(self.output)
        self.trace.append(("external_edit", value))

    @precondition(lambda self: self.model.kind == "receipted")
    @rule()
    def remove_receipt(self):
        (self.output / MARKER).unlink()
        self.model.kind = "unreceipted"
        self.observed = namespace(self.output)
        self.trace.append(("remove_receipt",))

    @precondition(lambda self: self.model.kind != "absent")
    @rule(kind=st.sampled_from(("file", "empty_directory", "symlink", "receipt")))
    def external_object(self, kind):
        if kind == "file":
            (self.output / "personal.txt").write_bytes(b"preserve user fixture")
        elif kind == "empty_directory":
            (self.output / "personal-empty").mkdir(exist_ok=True)
        elif kind == "symlink":
            link = self.output / "outside-link"
            if not link.is_symlink():
                link.symlink_to(self.outside)
        else:
            (self.output / MARKER).write_bytes(b"{}")
        self.model.kind = "damaged"
        self.observed = namespace(self.output)
        self.trace.append(("external_object", kind))

    @invariant()
    def model_namespace_and_outside_custody_hold(self):
        assert namespace(self.output) == self.observed, "an action changed the output outside its declared transition"
        assert self.outside.read_bytes() == b"outside bytes must never be copied"
        if self.model.kind == "receipted":
            self.assert_complete_generation(self.model.files, self.model.identities, self.model.family)



TestGeneratedCustodySequences = CustodyMachine.TestCase
TestGeneratedCustodySequences.settings = settings(max_examples=60, stateful_step_count=50,
                                                 derandomize=True, database=None, deadline=None)


class ForeignOwnershipChallenge(CustodyMachine):
    """Fixed known custody prefix; Hypothesis shrinks the generated continuation."""
    @initialize()
    def seed_state(self):
        self.publish(False, "normal")
        self.remove_receipt()
        self.external_object("file")


class SourceGuardChallenge(CustodyMachine):
    @initialize()
    def seed_state(self):
        pass  # Start with an absent destination; no unshrinkable action prefix.

    @rule(check=st.booleans(), mode=st.just("source_drift"))
    def attempt_publish(self, check, mode):
        self.publish(check, mode)


SENSITIVITY_SETTINGS = settings(max_examples=20, stateful_step_count=10, derandomize=True,
                               database=None, deadline=None, report_multiple_bugs=False)


class CustodySequenceRegressions(unittest.TestCase):
    def replay(self, actions):
        machine = CustodyMachine()
        self.addCleanup(machine.teardown)
        for action in actions:
            getattr(machine, action[0])(*action[1:])
            machine.model_namespace_and_outside_custody_hold()
        return machine

    def test_legacy_adoption_changed_input_noop_and_stale_check_sequence(self):
        self.replay([("publish", False, "normal"), ("remove_receipt",),
                     ("propose", 0, 1, 0), ("publish", True, "normal"),
                     ("publish", False, "normal"), ("publish", False, "normal"),
                     ("propose", 1, 1, 0), ("publish", True, "normal"),
                     ("publish", False, "normal")])

    def test_uncertain_exchange_retains_old_tree_then_retry_and_check(self):
        self.replay([("publish", False, "normal"), ("propose", 1, 1, 0),
                     ("publish", False, "after_namespace_failure"),
                     ("publish", True, "normal"), ("publish", False, "normal"),
                     ("propose", 2, 2, 0), ("publish", False, "source_drift"),
                     ("publish", False, "normal")])

    def test_shrunk_legacy_unknown_object_sequence_refuses_before_commit(self):
        for mode in ("normal", "after_namespace_failure"):
            self.replay([("publish", False, "normal"), ("remove_receipt",),
                         ("external_object", "file"), ("publish", False, mode)])

    def test_foreign_objects_and_family_cannot_be_adopted_after_prior_success(self):
        for kind in ("file", "empty_directory", "symlink", "receipt"):
            self.replay([("publish", False, "normal"), ("external_object", kind),
                         ("propose", 1, 1, 0), ("publish", False, "normal"),
                         ("publish", True, "normal")])
        self.replay([("publish", False, "normal"), ("propose", 1, 1, 1),
                     ("publish", False, "normal"), ("propose", 1, 1, 0),
                     ("publish", False, "normal")])

    def test_independent_oracle_rejects_ownership_bypass(self):
        inspect = producer.previous_is_owned
        def bypass(output, desired):
            return True if (output / "personal.txt").exists() else inspect(output, desired)
        with patch.object(producer, "previous_is_owned", side_effect=bypass):
            with self.assertRaisesRegex(AssertionError, "outcome disagrees"):
                run_state_machine_as_test(ForeignOwnershipChallenge, settings=SENSITIVITY_SETTINGS)

    def test_independent_oracle_rejects_ignored_source_guard(self):
        install = producer.install
        def bypass(output, **kwargs):
            return install(output, **{**kwargs, "guard": lambda: None})
        with patch.object(producer, "install", side_effect=bypass):
            with self.assertRaisesRegex(AssertionError, "outcome disagrees"):
                run_state_machine_as_test(SourceGuardChallenge, settings=SENSITIVITY_SETTINGS)

    def test_independent_return_oracle_rejects_boolean_byte_count(self):
        install = producer.install
        def misreport(output, **kwargs):
            result = install(output, **kwargs)
            result["files"][0]["size"] = True  # True compares equal to integer 1.
            return result
        with patch.object(producer, "install", side_effect=misreport):
            with self.assertRaisesRegex(AssertionError, "contradictory receipt"):
                self.replay([("publish", False, "normal")])


if __name__ == "__main__":
    unittest.main()
