#!/usr/bin/env python3
"""Validate fail-closed N0-N5 rehabilitation of accepted negative outcomes."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from build_negative_result_rehabilitation import build


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "evidence_quality/negative_result_rehabilitation.json"
SCHEMA = ROOT / "schemas/negative_result_rehabilitation.schema.json"
IDENTITY = ROOT / "evidence_quality/claim_identity_graph.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def negative_transitions() -> dict[str, tuple[Path, dict]]:
    rows = {}
    for path in sorted((ROOT / "evidence_transitions").glob("**/*.json")):
        item = load(path)
        if (
            item.get("review_status") == "accepted"
            and item.get("transition_validity_state") == "review_accepted"
            and item.get("transition_effect") in {"no_change", "refuted"}
        ):
            rows[item["transition_id"]] = (path, item)
    return rows


def errors(ledger: dict) -> list[str]:
    out: list[str] = []
    schema = load(SCHEMA)
    for error in sorted(Draft202012Validator(schema).iter_errors(ledger), key=lambda e: list(e.path)):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    if ledger != build():
        out.append("rehabilitation ledger is not the exact deterministic result of the reviewed N-level table")

    identity = {row["transition_id"]: row for row in load(IDENTITY)["records"]}
    transitions = negative_transitions()
    records = ledger.get("records", [])
    ids = [row.get("transition_id") for row in records]
    if len(ids) != len(set(ids)):
        out.append("rehabilitation transition records are duplicated")
    if set(ids) != set(transitions):
        out.append("rehabilitation denominator is not the exact accepted negative/no-change set")

    for row in records:
        transition_id = row.get("transition_id")
        if transition_id not in transitions or transition_id not in identity:
            out.append(f"unknown rehabilitation transition: {transition_id}")
            continue
        path, transition = transitions[transition_id]
        edge = identity[transition_id]
        if row.get("transition_sha256") != sha256(path):
            out.append(f"historical transition digest drift: {transition_id}")
        if row.get("claim_id") != transition.get("claim_id"):
            out.append(f"historical claim identity drift: {transition_id}")
        if row.get("historical_transition_effect") != transition.get("transition_effect"):
            out.append(f"historical effect rewrite: {transition_id}")
        if row.get("historical_support_state") != transition.get("new_support_state"):
            out.append(f"historical support label rewrite: {transition_id}")
        if row.get("canonical_parent_id") != edge.get("canonical_parent_id"):
            out.append(f"canonical parent drift: {transition_id}")
        if row.get("identity_relation") != edge.get("primary_relation"):
            out.append(f"identity relation drift: {transition_id}")
        if row.get("raw_scope_boundary") != transition.get("scope_boundary"):
            out.append(f"raw scope rewrite: {transition_id}")
        if row.get("raw_negative_results") != transition.get("negative_results", []):
            out.append(f"raw negative result rewrite: {transition_id}")
        if row.get("raw_limitations") != transition.get("limitations", []):
            out.append(f"raw limitations rewrite: {transition_id}")
        if row.get("raw_non_claims") != transition.get("non_claims", []):
            out.append(f"raw non-claim rewrite: {transition_id}")
        level = row.get("assigned_n_level")
        audit = row.get("competence_audit", {})
        if level == "N0" and "No claim inference" not in audit.get("maximum_usable_negative_inference", ""):
            out.append(f"N0 creates claim inference: {transition_id}")
        if level == "N1" and "remains untested" not in audit.get("maximum_usable_negative_inference", ""):
            out.append(f"N1 claims target testing: {transition_id}")
        if level == "N2" and "no target" not in audit.get("maximum_usable_negative_inference", ""):
            out.append(f"N2 creates target inference: {transition_id}")
        if row.get("broad_negative_inference_state") != "quarantined":
            out.append(f"broad negative inference escaped quarantine: {transition_id}")
        if row.get("support_state_effect") != "none" or row.get("release_effect") != "none":
            out.append(f"rehabilitation creates support or release effect: {transition_id}")

    summary = ledger.get("summary", {})
    if summary.get("n_level_counts") != {"N0": 1, "N1": 15, "N2": 74, "N3": 0, "N4": 0, "N5": 0}:
        out.append("N-level counts drifted")
    if summary.get("broad_negative_inference_count") != 0:
        out.append("broad negative inference count must remain zero")
    if ledger.get("policy", {}).get("heldout_denominators_may_be_reopened") is not False:
        out.append("historical heldout denominators may not be reopened")
    if ledger.get("policy", {}).get("post_hoc_missing_competence_evidence_may_be_invented") is not False:
        out.append("post-hoc competence evidence invention is enabled")
    return out


def main() -> None:
    ledger = load(LEDGER)
    failures = errors(ledger)
    mutations: list[tuple[str, dict]] = []

    def mutate(label: str, edit) -> None:
        candidate = copy.deepcopy(ledger)
        edit(candidate)
        mutations.append((label, candidate))

    mutate("negative record deletion", lambda x: x["records"].pop())
    mutate("historical label rewrite", lambda x: x["records"][0].__setitem__("historical_support_state", "refuted"))
    mutate("transition digest rewrite", lambda x: x["records"][0].__setitem__("transition_sha256", "0" * 64))
    mutate("N0 inference widening", lambda x: next(r for r in x["records"] if r["assigned_n_level"] == "N0")["competence_audit"].__setitem__("maximum_usable_negative_inference", "architecture refuted"))
    mutate("N1 inference widening", lambda x: next(r for r in x["records"] if r["assigned_n_level"] == "N1")["competence_audit"].__setitem__("maximum_usable_negative_inference", "mechanism refuted"))
    mutate("N2 inference widening", lambda x: next(r for r in x["records"] if r["assigned_n_level"] == "N2")["competence_audit"].__setitem__("maximum_usable_negative_inference", "target refuted"))
    mutate("N3 invention", lambda x: x["records"][0].__setitem__("assigned_n_level", "N3"))
    mutate("broad inference escape", lambda x: x["records"][0].__setitem__("broad_negative_inference_state", "allowed"))
    mutate("heldout reopen", lambda x: x["policy"].__setitem__("heldout_denominators_may_be_reopened", True))
    mutate("posthoc evidence invention", lambda x: x["policy"].__setitem__("post_hoc_missing_competence_evidence_may_be_invented", True))
    mutate("raw limitation deletion", lambda x: x["records"][0].__setitem__("raw_limitations", []))
    mutate("support promotion", lambda x: x["records"][0].__setitem__("support_state_effect", "promoted"))

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Negative-result rehabilitation validation failed:\n - " + "\n - ".join(failures))
    print(
        "Negative-result rehabilitation passed: 90/90 accepted negative/no-change transitions "
        "classified as 1 N0, 15 N1, 74 N2, 0 N3-N5; zero broad or chapter-core negative "
        f"inference; {len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
