#!/usr/bin/env python3
"""Validate the prospective C2-EL claim-state preregistration."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "experiments/c2_exit_ladder/preregistration.json"
SCHEMA = ROOT / "schemas/c2_exit_ladder_preregistration.schema.json"
EXPECTED_ROUTES = ["direct", "record_only", "full_governed"]
EXPECTED_PATHS = {
    "natural_happy", "injected_identity_mismatch",
    "injected_inference_overreach", "injected_stale_projection",
}
EXPECTED_OUTCOMES = {
    "proposal_accepted", "correct_disposition", "identity_mismatch_escaped",
    "inference_overreach_escaped", "stale_projection_escaped",
    "false_block_count", "latency_ms", "cpu_ms", "operator_step_proxy",
    "artifact_file_count", "artifact_bytes", "residual_count",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def failures(protocol: dict) -> list[str]:
    out = [
        f"schema: {error.message}"
        for error in Draft202012Validator(load(SCHEMA)).iter_errors(protocol)
    ]
    routes = [row.get("id") for row in protocol.get("routes", [])]
    if routes != EXPECTED_ROUTES or len(routes) != len(set(routes)):
        out.append("three-route identity or order drifted")
    if set(protocol.get("paths", {})) != EXPECTED_PATHS:
        out.append("natural plus three claim-state fault paths drifted")
    if set(protocol.get("outcomes", [])) != EXPECTED_OUTCOMES:
        out.append("joint outcome surface drifted")
    selection = protocol.get("proposal_selection", {})
    joined = " ".join(selection.get("eligible", []) + selection.get("excluded", [])).lower()
    for phrase in ("ordinary", "protected", "invented", "identical source", "disposition"):
        if phrase not in joined:
            out.append(f"proposal chronology or matching boundary missing: {phrase}")
    if not selection.get("replacement_policy", "").startswith("No replacement after"):
        out.append("post-admission replacement prohibition drifted")
    inference = protocol.get("dispositions", {}).get("maximum_inference", "").lower()
    for phrase in (
        "one prospectively selected", "cannot estimate general evidence quality",
        "cannot promote any claim beyond",
    ):
        if phrase not in inference:
            out.append(f"maximum-inference boundary missing: {phrase}")
    if (
        protocol.get("proposal_admitted") is not False
        or protocol.get("proposal_identity") is not None
        or protocol.get("protected_content_opened") is not False
        or protocol.get("support_state_effect") != "none"
        or protocol.get("release_effect") != "none"
    ):
        out.append("freeze opened a proposal, protected content, support, or release state")
    return out


def main() -> None:
    protocol = load(PROTOCOL)
    out = failures(protocol)
    mutations = [
        ("proposal preadmitted", lambda value: value.__setitem__("proposal_admitted", True)),
        ("proposal identity preopened", lambda value: value.__setitem__("proposal_identity", "known.claim")),
        ("protected content opened", lambda value: value.__setitem__("protected_content_opened", True)),
        ("route removed", lambda value: value["routes"].pop()),
        ("route relabeled", lambda value: value["routes"][0].__setitem__("id", "full_governed")),
        ("fault path removed", lambda value: value["paths"].pop("injected_stale_projection")),
        ("outcome removed", lambda value: value["outcomes"].pop()),
        ("replacement allowed", lambda value: value["proposal_selection"].__setitem__("replacement_policy", "Replace a failed proposal.")),
        ("inference widened", lambda value: value["dispositions"].__setitem__("maximum_inference", "The evidence system is generally correct.")),
        ("support promoted", lambda value: value.__setitem__("support_state_effect", "external-literature-backed")),
    ]
    for label, mutate in mutations:
        candidate = deepcopy(protocol)
        mutate(candidate)
        if not failures(candidate):
            out.append(f"negative control accepted: {label}")
    if out:
        raise SystemExit("C2-EL preregistration failed:\n - " + "\n - ".join(out))
    print(
        "C2-EL preregistration passed: first eligible post-freeze claim-state proposal, "
        "3 matched routes, 1 natural plus 3 injected paths, 12 outcomes, "
        "10 mutations rejected, proposal/protected/support/release state closed."
    )


if __name__ == "__main__":
    main()
