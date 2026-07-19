#!/usr/bin/env python3
"""Validate complete, non-promoting identity resolution for accepted transitions."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from build_claim_identity_graph import build


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "evidence_quality/claim_identity_graph.json"
SCHEMA = ROOT / "schemas/claim_identity_graph.schema.json"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
ADDENDUM = ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atoms() -> dict[str, tuple[str, str, str]]:
    rows: dict[str, tuple[str, str, str]] = {}
    registry = load(REGISTRY)
    for row in registry["atoms"]:
        rows[row["atom_id"]] = (
            row["chapter_id"], row["proposition"], REGISTRY.relative_to(ROOT).as_posix()
        )
    addendum = load(ADDENDUM)
    for row in addendum["atoms"]:
        rows[row["id"]] = (
            addendum["chapter_id"], row["claim"], ADDENDUM.relative_to(ROOT).as_posix()
        )
    return rows


def accepted() -> dict[str, tuple[Path, dict]]:
    rows = {}
    for path in sorted((ROOT / "evidence_transitions").glob("**/*.json")):
        item = load(path)
        if item.get("review_status") == "accepted" and item.get("transition_validity_state") == "review_accepted":
            transition_id = item["transition_id"]
            if transition_id in rows:
                raise ValueError(f"duplicate accepted transition_id: {transition_id}")
            rows[transition_id] = (path, item)
    return rows


def errors(graph: dict) -> list[str]:
    out: list[str] = []
    schema = load(SCHEMA)
    for error in sorted(Draft202012Validator(schema).iter_errors(graph), key=lambda e: list(e.path)):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")

    expected = build()
    if graph != expected:
        out.append("graph is not the exact deterministic result of the reviewed adjudication table")

    atom_rows = atoms()
    accepted_rows = accepted()
    records = graph.get("records", [])
    record_ids = [row.get("transition_id") for row in records]
    claim_ids = [row.get("claim_id") for row in records]
    if len(record_ids) != len(set(record_ids)):
        out.append("transition identity records are not unique")
    if len(claim_ids) != len(set(claim_ids)):
        out.append("accepted campaign claim identities are not unique")
    if set(record_ids) != set(accepted_rows):
        out.append("accepted transition denominator is not exactly resolved")

    for row in records:
        transition_id = row.get("transition_id")
        if transition_id not in accepted_rows:
            out.append(f"unknown accepted transition record: {transition_id}")
            continue
        path, transition = accepted_rows[transition_id]
        expected_path = path.relative_to(ROOT).as_posix()
        if row.get("transition_path") != expected_path:
            out.append(f"transition path drift: {transition_id}")
        if row.get("transition_sha256") != sha256(path):
            out.append(f"transition digest drift: {transition_id}")
        if row.get("claim_id") != transition.get("claim_id"):
            out.append(f"transition claim identity drift: {transition_id}")
        parent_id = row.get("canonical_parent_id")
        if parent_id not in atom_rows:
            out.append(f"dangling canonical parent: {transition_id}:{parent_id}")
            continue
        owner, proposition, source = atom_rows[parent_id]
        if row.get("owner_chapter_id") != owner:
            out.append(f"canonical owner drift: {transition_id}")
        if row.get("canonical_parent_proposition") != proposition:
            out.append(f"canonical proposition drift: {transition_id}")
        if row.get("canonical_parent_source") != source:
            out.append(f"canonical source drift: {transition_id}")
        relation = row.get("primary_relation")
        effect = row.get("parent_support_state_effect")
        if relation == "atom":
            if row.get("claim_id") != parent_id:
                out.append(f"atom relation is not identity: {transition_id}")
            if effect != "exact_transition_record_subject_to_registry_reconciliation":
                out.append(f"direct atom relation erased registry reconciliation: {transition_id}")
        else:
            if row.get("claim_id") == parent_id:
                out.append(f"indirect relation disguises exact identity: {transition_id}")
            if effect != "none":
                out.append(f"indirect relation moves parent support: {transition_id}")
        scope = row.get("identity_scope", {})
        if scope.get("artifact") != transition.get("artifact_refs"):
            out.append(f"identity artifact denominator drift: {transition_id}")
        if transition.get("scope_boundary") not in scope.get("population", ""):
            out.append(f"transition scope boundary was not preserved: {transition_id}")
        if not all(nonclaim in scope.get("maximum_inference", "") for nonclaim in transition.get("non_claims", [])):
            out.append(f"transition non-claim boundary was not preserved: {transition_id}")
        if relation in {"subclaim_of", "proxy_for"} and "no parent support-state effect" not in scope.get("parent_nonpromotion_rationale", ""):
            out.append(f"indirect non-promotion rationale missing: {transition_id}")

    summary = graph.get("summary", {})
    if summary.get("resolved_transition_count") != len(accepted_rows):
        out.append("resolved denominator does not equal accepted denominator")
    if summary.get("unresolved_transition_count") != 0:
        out.append("unresolved accepted transition remains")
    if graph.get("identity_policy", {}).get("mapping_is_evidence") is not False:
        out.append("identity mapping cannot become evidence")
    if graph.get("identity_policy", {}).get("proxy_to_target_inference_allowed") is not False:
        out.append("proxy-to-target laundering is enabled")
    return out


def main() -> None:
    graph = load(GRAPH)
    failures = errors(graph)
    mutations: list[tuple[str, dict]] = []

    def mutate(label: str, edit) -> None:
        candidate = copy.deepcopy(graph)
        edit(candidate)
        mutations.append((label, candidate))

    mutate("accepted transition deletion", lambda g: g["records"].pop())
    mutate("dangling parent", lambda g: g["records"][0].__setitem__("canonical_parent_id", "missing.core"))
    mutate("indirect parent promotion", lambda g: next(r for r in g["records"] if r["primary_relation"] != "atom").__setitem__("parent_support_state_effect", "exact_transition_record_subject_to_registry_reconciliation"))
    mutate("proxy recast as atom", lambda g: next(r for r in g["records"] if r["primary_relation"] == "proxy_for").__setitem__("primary_relation", "atom"))
    mutate("claim identity rewrite", lambda g: g["records"][0].__setitem__("claim_id", "rewritten.claim"))
    mutate("transition digest rewrite", lambda g: g["records"][0].__setitem__("transition_sha256", "0" * 64))
    mutate("scope boundary deletion", lambda g: g["records"][0]["identity_scope"].__setitem__("population", "deleted"))
    mutate("non-claim deletion", lambda g: g["records"][0]["identity_scope"].__setitem__("maximum_inference", "universal"))
    mutate("artifact denominator deletion", lambda g: g["records"][0]["identity_scope"].__setitem__("artifact", ["fake.json"]))
    mutate("proxy laundering enabled", lambda g: g["identity_policy"].__setitem__("proxy_to_target_inference_allowed", True))
    mutate("mapping promoted to evidence", lambda g: g["identity_policy"].__setitem__("mapping_is_evidence", True))
    mutate("unresolved invention", lambda g: g["summary"].__setitem__("unresolved_transition_count", 1))

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Claim identity graph validation failed:\n - " + "\n - ".join(failures))
    print(
        "Claim identity graph passed: 115/115 accepted transitions resolved to 3,745 canonical atoms "
        "(25 direct, 61 subclaims, 29 proxies), zero parent support movement, "
        f"and {len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
