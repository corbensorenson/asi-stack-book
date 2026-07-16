#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; STRUCTURE = ROOT / "book_structure.json"; TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:vcm.abi.operational_invariant": "Every accepted materialization in the finite reachable model preserves the exact represented request, address, version, snapshot, mount, source, derived representation, approved authority, and receipt custody.",
    "lean:vcm.abi.failure_blocks_promotion": "A represented mandatory miss reaches typed-fault state only with a fault receipt and without materialization; binding, lease, authority, certificate, omission, overclaim, taint, and receipt faults are rejected.",
    "lean:vcm.abi.context_admission_route_envelope": "The original finite admission routes are consumed alongside separate four-event materialization and two-event mandatory-fault refinements plus an independent 11-scenario/55-mutation consumer.",
}


def main() -> None:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8")); chapter = next(c for p in value["parts"] for c in p["chapters"] if c["id"] == "virtual-context-abi")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS: target["target"] = TARGETS[target["tag"]]; target["module"] = "AsiStackProofs.VirtualContextRefinement"
    name = "Executed resolver/materialization and mandatory-fault refinement"
    if not any(test.get("name") == name for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({"name": name, "purpose": "Refine exact request binding through resolver hit, certificate, materialization, and mandatory-miss typed-fault paths against prior resolver and admission inventories.", "implementation_status": "implemented", "result_status": "passes via `python3 scripts/validate_virtual_context_refinement.py`: 2 valid/9 invalid resolver scenarios, distinct 3-valid/5-invalid admission fixtures, 4-event materialization and 2-event fault witnesses, and 55/55 rejected mutations; support-state effect none", "status": "implemented bounded structured-record refinement; no natural-language address truth, payload meaning, certificate truthfulness, deployed resolver/store, concurrency, deletion enforcement, reproduction, transfer, safety, or chapter-core support claim"})
    STRUCTURE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record.get("tag") in TARGETS: record["formal_target"] = TARGETS[record["tag"]]; record["module"] = "AsiStackProofs.VirtualContextRefinement"; record["rationale"] = "Replaced projection-only ownership with reachable request-binding materialization and mandatory-fault semantics plus an independent 11-scenario/55-mutation consumer; support effect none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated three Virtual Context targets and one executed refinement test.")


if __name__ == "__main__": main()
