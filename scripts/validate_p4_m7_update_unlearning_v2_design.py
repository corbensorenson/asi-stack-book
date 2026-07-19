#!/usr/bin/env python3
"""Validate the single diagnosed P4/M7 v2 repair and its preflight."""

from __future__ import annotations

import copy
from collections import Counter
from pathlib import Path

from p4_m7_update_unlearning_v2_common import (
    ARMS,
    CLAIM_AXES,
    CORPUS,
    PREFLIGHT,
    PREREG,
    ROOT,
    SEEDS,
    STATE_SURFACES,
    V1_DIAGNOSIS,
    file_sha,
    load_json,
    model_file_identities,
)


EXPECTED = {"base_train": 240, "update_retain": 120, "delete_a": 30, "delete_b": 30, "validation": 120, "retained_test": 120, "target_test": 90, "adversarial_test": 60, "privacy_nonmember": 60}


def errors(prereg: dict, corpus: dict) -> list[str]:
    out = []
    if prereg.get("state") != "single_diagnosed_repair_frozen_before_v2_preflight_or_outcome": out.append("v2 freeze state drift")
    if prereg.get("repair_of", {}).get("sha256") != file_sha(V1_DIAGNOSIS): out.append("v1 diagnosis binding drift")
    if prereg.get("corpus_sha256") != file_sha(CORPUS) or corpus.get("row_count") != 870: out.append("v2 corpus identity drift")
    if Counter(row["role"] for row in corpus.get("rows", [])) != Counter(EXPECTED): out.append("v2 role denominator drift")
    for role in ("delete_a", "delete_b", "privacy_nonmember"):
        counts = corpus.get("role_label_counts", {}).get(role, {})
        if counts != {"0": 10 if role != "privacy_nonmember" else 20, "1": 10 if role != "privacy_nonmember" else 20, "2": 10 if role != "privacy_nonmember" else 20}: out.append(f"balanced label repair drift: {role}")
    if prereg.get("seeds") != list(SEEDS) or prereg.get("arms") != list(ARMS): out.append("v2 seed/arm drift")
    if prereg.get("claim_axes") != list(CLAIM_AXES) or prereg.get("state_surfaces") != list(STATE_SURFACES): out.append("v2 axis/state drift")
    if prereg.get("model", {}).get("representation_layer") != "attention-masked mean of final hidden states": out.append("pooling repair drift")
    if prereg.get("model", {}).get("file_sha256") != model_file_identities(): out.append("model byte drift")
    for name, expected in prereg.get("code_sha256", {}).items():
        path = ROOT / "scripts" / name
        if not path.is_file() or file_sha(path) != expected: out.append(f"frozen code drift: {name}")
    if prereg.get("outcome_aware_retry_allowed") is not False or prereg.get("further_repair_after_v2_allowed") is not False: out.append("retry ceiling drift")
    if prereg.get("primary_gates", {}).get("minimum_confirmatory_deletion_retrain_true_accuracy") != 0.60: out.append("target adequacy gate drift")
    return out


def main() -> None:
    prereg = load_json(PREREG); corpus = load_json(CORPUS); failures = errors(prereg, corpus)
    for label, mutation in (
        ("unbalance delete a", lambda p, c: c["role_label_counts"]["delete_a"].__setitem__("0", 30)),
        ("restore last-token pool", lambda p, c: p["model"].__setitem__("representation_layer", "last token")),
        ("drop target gate", lambda p, c: p["primary_gates"].__setitem__("minimum_confirmatory_deletion_retrain_true_accuracy", 0.0)),
        ("permit third attempt", lambda p, c: p.__setitem__("further_repair_after_v2_allowed", True)),
        ("drop claim axis", lambda p, c: p["claim_axes"].pop()),
        ("truncate state", lambda p, c: p["state_surfaces"].pop()),
    ):
        p = copy.deepcopy(prereg); c = copy.deepcopy(corpus); mutation(p, c)
        if not errors(p, c): failures.append(f"v2 design mutation accepted: {label}")
    preflight_state = "not_run"
    if PREFLIGHT.exists():
        pf = load_json(PREFLIGHT); preflight_state = pf.get("protocol_outcome")
        if preflight_state != "instrument_adequate" or pf.get("heldout_opened") is not True: failures.append("v2 preflight failed")
        if pf.get("general_validation_accuracy", 0) < 0.60 or pf.get("deletion_like_validation_accuracy", 0) < 0.60: failures.append("v2 preflight accuracy gate failed")
        if len(pf.get("negative_controls", {})) != 5 or not all(pf.get("negative_controls", {}).values()): failures.append("v2 preflight control drift")
    if failures: raise SystemExit("P4/M7 v2 design failed:\n - " + "\n - ".join(failures))
    print(f"P4/M7 v2 design passed: 870 balanced rows, one diagnosed repair, deletion-target floor 0.60, 6 mutations rejected, preflight={preflight_state}.")


if __name__ == "__main__": main()
