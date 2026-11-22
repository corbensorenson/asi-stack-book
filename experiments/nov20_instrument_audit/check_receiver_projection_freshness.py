#!/usr/bin/env python3
"""Check receiver retry decisions when a new response carries an old projection."""

from contextlib import closing
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

from run_receiver import check, classify, digest
from compare_fresh_effect_workflows import LocalReceiver, Operation, interpret, read_receipt


CASES = {
    # Each expected pair is (disposition, count of exact or repeated commits).
    "current_failure": (False, False, "current", True, ("closed", 1), ("closed", 1)),
    "old_failure": (True, False, "old", True, ("closed", 2), ("hold", 1)),
    "old_failure_deduplicated": (True, True, "old", True, ("closed", 1), ("closed", 1)),
    "current_commit": (True, False, "current", True, ("closed", 1), ("closed", 1)),
    "no_trusted_revision": (True, False, "current", False, ("closed", 1), ("hold", 1)),
}


def run_case(database, committed, deduplicates, projection, trusted, check_source_revision):
    operation = Operation("caption-correction", "local-documents", digest(b"Figure 5"))
    receiver = LocalReceiver(database, deduplicates, "failed_before_commit")
    if receiver.submit(operation, 1) != "failed":
        raise ValueError("fixture did not initialize the original failure")
    original = read_receipt(database, operation.key, 1)
    if committed and receiver.submit(operation, 2) != "committed":
        raise ValueError("fixture did not record the prior successful retry")

    tick = 4
    current_revision = 2 if committed else 1
    if projection == "old":
        lookup = replace(original, tick=tick)
        source_revision = 1
    else:
        lookup = read_receipt(database, operation.key, tick)
        source_revision = current_revision
    expected_revision = current_revision if trusted else None
    result = interpret(lookup, operation, tick)
    if check_source_revision and source_revision != expected_revision:
        result = "ambiguous"
    retry = result == "failed" or (result == "ambiguous" and deduplicates)
    if retry:
        result = receiver.submit(operation, tick)

    disposition = "closed" if result == "committed" else "hold"
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        journal = [dict(row) for row in connection.execute("SELECT * FROM attempts ORDER BY attempt")]
    exact = (operation.key, operation.destination, operation.payload_sha256)
    return {
        "response_tick": lookup.tick,
        "source_revision": source_revision,
        "required_revision": expected_revision,
        "retried": retry,
        **classify(journal, disposition, exact, correct_patch=True),
    }


def main():
    frozen = check()
    rows = []
    with TemporaryDirectory(prefix="asi-receiver-projection-") as root:
        for case, (committed, deduplicates, view, trusted, tick_expected, source_expected) in CASES.items():
            arms = {}
            for arm, expected in (("tick_only", tick_expected), ("source_revision", source_expected)):
                result = run_case(
                    Path(root, f"{case}-{arm}.sqlite"), committed, deduplicates, view, trusted,
                    check_source_revision=arm == "source_revision",
                )
                if (result["disposition"], result["effect_commits"]) != expected:
                    raise ValueError(f"{case} / {arm}: unexpected decision or effect count {result}")
                arms[arm] = result
            rows.append({"case": case, "arms": arms})
    print(json.dumps({"frozen_inputs": frozen, "cases": rows}, indent=2))


if __name__ == "__main__":
    main()
