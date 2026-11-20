#!/usr/bin/env python3
"""Separate expiry extension. The canonical replay and input lock are unchanged."""

import json
from pathlib import Path
import sys
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import compare_verifier_replacements as study


def main() -> None:
    scope = "public-copy"
    fixture = json.loads(study.CASES.read_text())
    observations = study.evaluate_models(fixture)[scope]
    observe = study.observed_documents

    def expiring_fallback(*args):
        documents = observe(*args)
        documents["fallback"]["valid_through"] = 0
        return documents

    with patch.object(study, "observed_documents", expiring_fallback):
        traces = {arm: study.replay(scope, "none", arm, observations) for arm in study.ARMS}
    for ticks in traces.values():
        if [row["route"] for row in ticks] != ["candidate", "specialist"]:
            raise ValueError("expiry did not return the candidate to specialist review")
        if ticks[0]["evidence_sha256"] != ticks[1]["evidence_sha256"]:
            raise ValueError("evidence bytes changed in an expiry-only extension")
        if ticks[1]["policy_evaluations"] != 1:
            raise ValueError("expiry did not trigger a policy recheck")
    print(json.dumps(traces, indent=2))


if __name__ == "__main__":
    main()
