#!/usr/bin/env python3
"""Reconcile live triage after P2 safety replacement and chapter insertion."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"

REPLACED = {
    "lean:alignment.constitution.operational_invariant",
    "lean:alignment.constitution.failure_blocks_promotion",
    "lean:corrigibility.agency.operational_invariant",
    "lean:corrigibility.agency.failure_blocks_promotion",
    "lean:values.conflict.operational_invariant",
    "lean:values.conflict.failure_blocks_promotion",
    "lean:governance.rights.operational_invariant",
    "lean:governance.rights.failure_blocks_promotion",
    "lean:self_improvement.boundary.operational_invariant",
    "lean:self_improvement.boundary.failure_blocks_promotion",
}


def entry(record: dict) -> dict:
    tag = record["tag"]
    base = {
        "tag": tag,
        "chapter_id": record["chapter_id"],
        "module": record["module"],
        "formal_target": record["formal_target"],
        "target_status": record["status"],
    }
    if tag == "lean:cognitive_kernel.abi_trace_invariants":
        return {
            **base,
            "triage": "research-agenda",
            "recommended_route": "defer-until-narrowed",
            "rationale": "Post-activation target for the accepted replaceable-cognitive-substrates chapter. Keep planned until a finite ABI transition model and independently implemented executable refinement exist; no architecture or chapter support claim follows from registration.",
        }
    if tag == "lean:corrigibility.agency.generic_countermodel_routes":
        return {
            **base,
            "triage": "formal-invariant",
            "recommended_route": "lean-candidate",
            "rationale": "Implemented four bounded generic countermodel consequences for missing review, unbounded delegation, and missing accountability. The literal theorem-per-fixture lifecycle surface was retired into the shared transition model and executable consumer/refinement suite; these retained consequences do not establish material rights usability, evaluator quality, correction outcomes, rollback execution, or deployment.",
        }
    return {
        **base,
        "triage": "formal-invariant",
        "recommended_route": "lean-candidate",
        "rationale": "P2 replacement target implemented in the shared safety-critical lifecycle state machine with accepted-trace preservation, explicit readiness, rejecting transitions or deletion countermodels, and independent executable refinement. The result is bounded to the encoded model and does not establish normative adequacy, deployed enforcement, empirical safety, reproduction, transfer, or chapter-core support.",
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    manifest_by_tag = {row["tag"]: row for row in manifest["records"]}
    retired_post_activation_tags = {
        "lean:corrigibility.agency.lifecycle_admission_route",
    }
    changed_tags = REPLACED | retired_post_activation_tags | {
        "lean:cognitive_kernel.abi_trace_invariants",
        "lean:corrigibility.agency.generic_countermodel_routes",
    }
    records = [row for row in triage["records"] if row.get("tag") not in changed_tags]
    for manifest_record in manifest["records"]:
        if manifest_record["tag"] in changed_tags:
            records.append(entry(manifest_record))
    triage["records"] = records
    triage["record_count"] = len(records)
    triage["updated"] = "2026-07-15"
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    missing = (changed_tags - retired_post_activation_tags) - set(manifest_by_tag)
    if missing:
        raise SystemExit(f"Missing manifest tags after triage write: {sorted(missing)}")
    print(f"Reconciled proof triage: {len(records)} records, {len(changed_tags)} P2/new-chapter targets updated.")


if __name__ == "__main__":
    main()
