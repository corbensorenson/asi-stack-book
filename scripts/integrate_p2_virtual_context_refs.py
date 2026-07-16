#!/usr/bin/env python3
"""Attach reachable Virtual Context refinement to frozen P2 lineage."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {"lean:vcm.abi.operational_invariant", "lean:vcm.abi.failure_blocks_promotion", "lean:vcm.abi.context_admission_route_envelope"}
PREFIX = "lean/AsiStackProofs/VirtualContextABI.lean::"
RETIRED = {PREFIX + "resolved_context_reference_has_valid_snapshot_binding", PREFIX + "mandatory_context_miss_produces_typed_fault_not_best_effort"}
COUNTER = ["lean/AsiStackProofs/VirtualContextRefinement.lean#countermodels", "experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json", "experiments/context_admission_adequacy/fixtures", "experiments/virtual_context_refinement/results/2026-07-15-local.json#mutation_receipts"]
MUTATION = ["scripts/validate_virtual_context_refinement.py#mutations"]
CONSUMER = ["chapter:virtual-context-abi#proof-and-test-hooks", "docs:virtual_context_refinement", "evidence_quality:model_adequacy_dossiers/virtual-context-refinement.md"]
RUNTIME = ["scripts/validate_virtual_context_refinement.py", "schemas/virtual_context_refinement.schema.json", "experiments/virtual_context_refinement/results/2026-07-15-local.json", "experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json", "scripts/validate_context_admission_adequacy.py", "experiments/context_admission_adequacy/fixtures", "lean/AsiStackProofs/VirtualContextRefinement.lean"]
REPLACEMENT = ["proof-model:virtual-context.reachable-materialization-fault-refinement.v1", "lean/AsiStackProofs/VirtualContextRefinement.lean"]


def merge(left: list[str], right: list[str]) -> list[str]: return list(dict.fromkeys([*left, *right]))
def attach(record: dict) -> None:
    for key, values in (("countermodel_refs", COUNTER), ("mutation_refs", MUTATION), ("consumer_refs", CONSUMER), ("runtime_consumer_refs", RUNTIME), ("replacement_refs", REPLACEMENT)):
        record[key] = merge(record.get(key, []), values)


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8")); targets = value["target_reviews"]; theorems = value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems): raise SystemExit("missing frozen Virtual Context lineage")
    roles = {
        "lean:vcm.abi.operational_invariant": "A reachable bind-resolve-certify-materialize path preserves exact request, address, version, snapshot, mount, source, derived, authority, lease, and receipt custody.",
        "lean:vcm.abi.failure_blocks_promotion": "A reachable mandatory miss emits a typed-fault receipt without materialization; twelve countermodels and 55 mutations reject binding, lease, authority, certificate, omission, overclaim, taint, receipt, and route faults.",
        "lean:vcm.abi.context_admission_route_envelope": "Eleven bounded admission/adequacy routes remain, now consumed alongside distinct reachable resolver/materialization and fault semantics without conflating admission with correctness.",
    }
    for target in TARGETS:
        record = targets[target]; attach(record); record["semantic_role"] = roles[target]
        record["assumptions"] = ["Numeric identifiers, authority, mount permission, lease, hashes, omission, taint, receipts, fixture labels, and local structured records are trusted only inside the finite model."]
        record["excluded_effects"] = ["Natural-language address truth, payload meaning, summary fidelity, certificate truthfulness, deployed resolver/store behavior, concurrency, deletion enforcement, natural workloads, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]
        record["review_rationale"] = "Resolve frozen Virtual Context lineage to reachable exact-binding materialization and mandatory-fault semantics plus an independent consumer without support promotion."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids: attach(theorems[theorem_id])
    for theorem_id in RETIRED: theorems[theorem_id]["review_rationale"] = "Frozen lineage retained; the assumption-projection declaration is physically retired and superseded by the reachable model, independent consumer, countermodels, and 55 mutations."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached Virtual Context refs to {len(TARGETS)} targets and {len(theorem_ids)} theorems; {len(RETIRED)} declarations retired.")


if __name__ == "__main__": main()
