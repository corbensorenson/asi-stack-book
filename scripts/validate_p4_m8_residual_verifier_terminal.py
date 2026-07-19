#!/usr/bin/env python3
"""Validate Campaign 4's three-version terminal instrument-limited disposition."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "experiments/p4_residual_verifier_capacity"
V2 = ROOT / "experiments/p4_residual_verifier_capacity_v2"
V3 = ROOT / "experiments/p4_residual_verifier_capacity_v3"


def load(path: Path) -> dict: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(values: dict[str, dict], filesystem: bool = True) -> list[str]:
    errors: list[str] = []; d1, d2, d3, r3, q3 = values["d1"], values["d2"], values["d3"], values["r3"], values["q3"]
    if d1.get("protocol_outcome") != "instrument_inadequate_route_taxonomy_and_clean_control" or d1.get("heldout_opened") is not False: errors.append("v1 failure or sealed heldout changed")
    if d2.get("protocol_outcome") != "instrument_inadequate_label_bearing_output_exemplar" or d2.get("heldout_opened") is not False: errors.append("v2 failure or sealed heldout changed")
    if d3.get("protocol_outcome") != "terminal_instrument_inadequate_extraction_contract" or d3.get("heldout_opened") is not False or d3.get("further_instrument_repair_allowed") is not False: errors.append("v3 terminal boundary changed")
    bindings = [(d1, V1), (d2, V2), (d3, V3)]
    for index, (diag, base) in enumerate(bindings, 1):
        for field, rel in [("preregistration_sha256", "preregistration.json"), ("raw_preflight_sha256", "raw/preflight_generation.json"), ("preflight_result_sha256", "results/preflight_result.json"), ("qualification_sha256", "results/preflight_qualification.json")]:
            if diag.get(field) != sha(base / rel): errors.append(f"v{index} {field} binding drifted")
    aggregate = r3.get("aggregate", {}); structured, capacity = aggregate.get("structured_ledger", {}), aggregate.get("capacity_aware_governed", {})
    if q3.get("protocol_outcome") != "instrument_inadequate_terminal" or q3.get("heldout_opened") is not False: errors.append("v3 qualification was laundered")
    if r3.get("residual_schema_admitted") != 3: errors.append("v3 failed schema denominator changed")
    if structured.get("mean_residual_recall") != 1.0 or structured.get("clean_release_retained") != 3: errors.append("v3 diagnostic substantive results changed")
    if capacity.get("false_reassurance") != 0 or capacity.get("terminal_eligibility_correct") != 6: errors.append("v3 diagnostic eligibility results changed")
    if d3.get("support_state_effect") != "blocks_promotion" or d3.get("chapter_core_promotion_count") != 0: errors.append("terminal failure changed support")
    if filesystem:
        for base in (V1, V2, V3):
            for rel in ("raw/heldout_generation.json", "results/heldout_result.json"):
                if (base / rel).exists(): errors.append(f"sealed heldout unexpectedly exists: {(base / rel).relative_to(ROOT)}")
    return errors


def main() -> None:
    paths = {"d1": V1 / "v1_preflight_failure_diagnosis.json", "d2": V2 / "v2_preflight_failure_diagnosis.json", "d3": V3 / "v3_terminal_preflight_failure_diagnosis.json", "r3": V3 / "results/preflight_result.json", "q3": V3 / "results/preflight_qualification.json"}
    missing = [str(p.relative_to(ROOT)) for p in paths.values() if not p.exists()]
    if missing: raise SystemExit("missing Campaign 4 artifact(s): " + ", ".join(missing))
    values = {key: load(path) for key, path in paths.items()}; errors = validate(values)
    mutations = [
        ("v1 failure erasure", lambda x: x["d1"].update(protocol_outcome="instrument_adequate")),
        ("v2 heldout laundering", lambda x: x["d2"].update(heldout_opened=True)),
        ("v3 repair reopening", lambda x: x["d3"].update(further_instrument_repair_allowed=True)),
        ("v3 schema inflation", lambda x: x["r3"].update(residual_schema_admitted=6)),
        ("qualification laundering", lambda x: x["q3"].update(protocol_outcome="instrument_adequate")),
        ("support promotion", lambda x: x["d3"].update(support_state_effect="synthetic-test-backed")),
    ]
    rejected = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(values); mutate(candidate)
        if validate(candidate, filesystem=False): rejected += 1
        else: errors.append(f"negative control accepted: {name}")
    if errors:
        print("P4/M8 residual/verifier terminal validation failed:")
        for error in errors: print(f" - {error}")
        sys.exit(1)
    print(f"P4/M8 Campaign 4 terminal validation passed: three failures preserved, heldout sealed, {rejected}/6 mutations rejected, no promotion.")


if __name__ == "__main__": main()
