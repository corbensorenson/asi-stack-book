#!/usr/bin/env python3
"""Validate prospective P2 frontier selection and held-out closure."""

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_frontier_selection.json"
SCHEMA = ROOT / "schemas/p2_frontier_selection.schema.json"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
DOC = ROOT / "docs/p2_frontier_selection.md"


def failures(value: dict) -> list[str]:
    out = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(value):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    weights = value.get("selection_rule", {}).get("weights", {})
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        out.append("selection weights must sum to one")
    candidates = value.get("candidates", [])
    criteria = list(weights)
    for row in candidates:
        computed = round(sum(row.get(key, 0) * weights[key] for key in criteria), 10)
        if abs(computed - row.get("weighted_score", -1)) > 1e-9:
            out.append(f"candidate weighted score drift: {row.get('candidate_id')}")
    selected = [row for row in candidates if row.get("disposition") == "selected_for_competence_preflight"]
    if len(selected) != 1 or selected[0].get("fatal_blocker") is not False:
        out.append("exactly one non-fatally-blocked candidate must be selected")
    if selected and selected[0].get("weighted_score") != max(row.get("weighted_score", -1) for row in candidates):
        out.append("selected candidate is not the prospectively highest weighted candidate")
    atom_ids = {row["atom_id"] for row in json.loads(REGISTRY.read_text(encoding="utf-8"))["atoms"]}
    claim = value.get("selected_claim", {})
    if claim.get("canonical_parent_atom") not in atom_ids:
        out.append("selected canonical parent atom does not exist")
    gates = {row.get("id"): row.get("state") for row in value.get("preflight_gates", [])}
    if gates.get("identity") != "passed" or gates.get("heldout") != "closed":
        out.append("identity must pass while final heldout remains closed")
    if any(state == "passed" for gate, state in gates.items() if gate not in {"identity"}):
        out.append("unperformed competence gates cannot be marked passed")
    if value.get("local_feasibility_snapshot", {}).get("final_denominator_opened") is not False:
        out.append("final denominator was opened before competence preflight")
    if value.get("support_state_effect") != "none" or value.get("release_effect") != "none":
        out.append("selection cannot create support or release effects")
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "five candidates", "seven competence gates remain pending",
        "The final denominator remains closed", "not a SOTA model",
        "creates no support, release, deployment, publication, safety, SOTA",
    ]:
        if phrase not in text:
            out.append(f"selection receipt missing boundary: {phrase}")
    return out


def main() -> None:
    value = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(value)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(value); edit(candidate); mutations.append((label, candidate))
    add("weight drift", lambda d: d["selection_rule"]["weights"].__setitem__("scientific_value", 0.5))
    add("lower scorer selection", lambda d: d["candidates"][0].__setitem__("weighted_score", 2.0))
    add("fatal selected", lambda d: d["candidates"][0].__setitem__("fatal_blocker", True))
    add("missing parent", lambda d: d["selected_claim"].__setitem__("canonical_parent_atom", "missing.atom"))
    add("false evaluator pass", lambda d: d["preflight_gates"][4].__setitem__("state", "passed"))
    add("heldout opened", lambda d: d["preflight_gates"][8].__setitem__("state", "open"))
    add("denominator opened", lambda d: d["local_feasibility_snapshot"].__setitem__("final_denominator_opened", True))
    add("support promotion", lambda d: d.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate): out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 frontier selection failed:\n - " + "\n - ".join(out))
    print("P2 frontier selection passed: one highest-value feasible subclaim selected from five; seven competence gates pending; final heldout gate closed; 8/8 mutations rejected.")


if __name__ == "__main__":
    main()
