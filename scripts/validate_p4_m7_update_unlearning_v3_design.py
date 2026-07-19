#!/usr/bin/env python3
"""Validate the terminal P4/M7 v3 instrument and failure lineage."""

from __future__ import annotations

import copy

from p4_m7_update_unlearning_v3_common import ARMS, CLAIM_AXES, CORPUS, FUSED_SIZE, PREFLIGHT, PREREG, ROOT, SEEDS, STATE_SURFACES, STRUCTURED_SIZE, V1_DIAGNOSIS, V2_DIAGNOSIS, file_sha, load_json, model_file_identities


def errors(prereg: dict) -> list[str]:
    out = []
    if prereg.get("state") != "terminal_instrument_frozen_before_preflight_or_heldout_outcome": out.append("v3 freeze drift")
    if prereg.get("corpus_sha256") != file_sha(CORPUS) or prereg.get("corpus_rows") != 870: out.append("v3 corpus drift")
    lineage = prereg.get("failure_lineage", [])
    if len(lineage) != 2:
        out.append("failure lineage drift")
    else:
        expected_lineage = [(V1_DIAGNOSIS, lineage[0]), (V2_DIAGNOSIS, lineage[1])]
        if any(row.get("sha256") != file_sha(path) for path, row in expected_lineage): out.append("failure lineage drift")
    if prereg.get("seeds") != list(SEEDS) or prereg.get("arms") != list(ARMS) or prereg.get("claim_axes") != list(CLAIM_AXES) or prereg.get("state_surfaces") != list(STATE_SURFACES): out.append("v3 denominator drift")
    model = prereg.get("model", {})
    if model.get("weights_frozen") is not True or model.get("structured_size") != STRUCTURED_SIZE or model.get("fused_size") != FUSED_SIZE or model.get("structured_scale") != 2.0: out.append("fusion interface drift")
    if model.get("file_sha256") != model_file_identities(): out.append("v3 model byte drift")
    for name, expected in prereg.get("code_sha256", {}).items():
        path = ROOT / "scripts" / name
        if not path.is_file() or file_sha(path) != expected: out.append(f"v3 code drift: {name}")
    if prereg.get("preflight_ablation") != ["transformer_only_linear", "structured_only_nonlinear", "fused_nonlinear"]: out.append("v3 ablation drift")
    if prereg.get("primary_gates", {}).get("minimum_preflight_fused_general_accuracy") != 0.8 or prereg.get("primary_gates", {}).get("minimum_confirmatory_deletion_retrain_true_accuracy") != 0.8: out.append("v3 adequacy floor drift")
    if prereg.get("outcome_aware_retry_allowed") is not False or prereg.get("further_instrument_repair_allowed") is not False: out.append("v3 retry ceiling drift")
    return out


def main() -> None:
    prereg = load_json(PREREG); failures = errors(prereg)
    for label, mutation in (
        ("drop failure", lambda p: p["failure_lineage"].pop()),
        ("unfreeze transformer", lambda p: p["model"].__setitem__("weights_frozen", False)),
        ("remove structure", lambda p: p["model"].__setitem__("structured_size", 0)),
        ("lower floor", lambda p: p["primary_gates"].__setitem__("minimum_confirmatory_deletion_retrain_true_accuracy", 0.3)),
        ("permit repair", lambda p: p.__setitem__("further_instrument_repair_allowed", True)),
        ("drop axis", lambda p: p["claim_axes"].pop()),
    ):
        candidate = copy.deepcopy(prereg); mutation(candidate)
        if not errors(candidate): failures.append(f"v3 design mutation accepted: {label}")
    preflight_state = "not_run"
    if PREFLIGHT.exists():
        pf = load_json(PREFLIGHT); preflight_state = pf.get("protocol_outcome")
        fused = pf.get("ablation", {}).get("fused_nonlinear", {})
        if preflight_state != "instrument_adequate" or pf.get("heldout_opened") is not True: failures.append("v3 preflight failed")
        if fused.get("general", 0) < 0.8 or fused.get("deletion_like", 0) < 0.8: failures.append("v3 fused adequacy gate failed")
        if len(pf.get("negative_controls", {})) != 6 or not all(pf.get("negative_controls", {}).values()): failures.append("v3 preflight controls drift")
    if failures: raise SystemExit("P4/M7 v3 design failed:\n - " + "\n - ".join(failures))
    print(f"P4/M7 v3 design passed: terminal structured-fusion instrument, two failures retained, 6 design mutations rejected, preflight={preflight_state}.")


if __name__ == "__main__": main()
