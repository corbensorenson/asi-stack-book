#!/usr/bin/env python3
import copy
import hashlib
import json
from datetime import date
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/p6_external_reproduction/results/terminal_result.json"
SCHEMA = ROOT / "schemas/p6_external_reproduction_terminal.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


EXPECTED_ATOMS = {
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.core",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.transformer-baseline",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.state-space-and-recurrence",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.architecture-portfolio",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.onecell",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.total-system-kiss",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture.architectural-rsi",
}


def errors(value: dict) -> list[str]:
    out = []
    for path_key, digest_key in [("ledger_path","ledger_sha256"),("preflight_path","preflight_sha256"),("defeat_prediction_path","defeat_prediction_sha256")]:
        path = ROOT / value.get(path_key, "missing")
        if not path.exists() or digest(path) != value.get(digest_key):
            out.append(f"frozen input digest: {path_key}")
    if {row.get("claim_atom") for row in value.get("dispositions", [])} != EXPECTED_ATOMS:
        out.append("exact claim-atom envelope")
    if any(row.get("disposition") != "blocked_after_full_attempt" for row in value.get("dispositions", [])):
        out.append("unsupported SOTA disposition")
    if any(value.get(key) != 0 for key in ["outcome_bearing_run_count","external_reproduction_count","sota_supported_count","chapter_core_promotion_count"]):
        out.append("invented outcome or promotion")
    ledger_path = ROOT / value.get("ledger_path", "missing")
    if ledger_path.exists():
        ledger = load(ledger_path)
        if len(ledger.get("comparators", [])) != 5 or any(row.get("access_state") != "blocked_after_full_attempt" for row in ledger.get("comparators", [])):
            out.append("comparator coverage or access state")
        if not ledger.get("primary_and_official_sources_only") or ledger.get("outcome_bearing_run_started"):
            out.append("entry freeze")
        if set(ledger.get("tested_claim_atoms", [])) != EXPECTED_ATOMS:
            out.append("ledger atom mapping")
        if (date.fromisoformat("2026-07-16") - date.fromisoformat(ledger.get("frozen_date", "1900-01-01"))).days > 30:
            out.append("stale comparator refresh")
        ids = {row.get("id") for row in ledger.get("comparators", [])}
        if "gated-deltanet-2-2026-05" not in ids or "mamba3-2026-03" not in ids or "inkling-open-hybrid-2026-07-15" not in ids:
            out.append("current comparator correction")
    preflight_path = ROOT / value.get("preflight_path", "missing")
    if preflight_path.exists():
        preflight = load(preflight_path)
        host = preflight.get("host", {})
        if host.get("unified_memory_gib") != 16 or host.get("nvidia_gpu_present") is not False or host.get("cuda_present") is not False:
            out.append("host boundary")
        if preflight.get("cloud_compute_authority") != "none" or preflight.get("paid_api_authority") != "none":
            out.append("invented external authority")
    prediction_path = ROOT / value.get("defeat_prediction_path", "missing")
    if prediction_path.exists():
        prediction = load(prediction_path)
        if prediction.get("candidate_implementation_present") is not False or len(prediction.get("clean_defeat_conditions", [])) != 7 or prediction.get("outcome_aware_revision_allowed") is not False:
            out.append("OneCell defeat prediction")
    return out


def main() -> None:
    value = load(RESULT)
    jsonschema.validate(value, load(SCHEMA))
    failures = errors(value)
    mutations = [
        ("invent reproduction", lambda data: data.__setitem__("external_reproduction_count", 1)),
        ("invent SOTA", lambda data: data.__setitem__("sota_supported_count", 1)),
        ("drop atom", lambda data: data["dispositions"].pop()),
        ("rewrite disposition", lambda data: data["dispositions"][0].__setitem__("disposition", "pareto_frontier_supported")),
        ("rewrite digest", lambda data: data.__setitem__("ledger_sha256", "0" * 64)),
        ("invent core promotion", lambda data: data.__setitem__("chapter_core_promotion_count", 1)),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        if not errors(candidate):
            failures.append(f"mutation accepted: {label}")
    if failures:
        raise SystemExit("P6 external reproduction terminal validation failed:\n - " + "\n - ".join(failures))
    print("P6 external reproduction passed: five dated primary/official comparators, seven exact blocked-after-full-attempt atoms, frozen OneCell defeat prediction, zero outcome runs/reproductions/SOTA/core promotions, and six mutations rejected.")


if __name__ == "__main__":
    main()
