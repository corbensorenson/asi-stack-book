#!/usr/bin/env python3
"""Register the current negative-inference surface audit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_negative_inference_surface_audit.py"
ARTIFACTS = [
    "evidence_quality/negative_inference_surface_audit.json",
    "schemas/negative_inference_surface_audit.schema.json",
    "docs/negative_inference_surface_audit.md",
    "scripts/build_negative_inference_surface_audit.py",
    "scripts/validate_negative_inference_surface_audit.py",
    "scripts/register_negative_inference_surface_audit.py",
    "evidence_quality/negative_result_rehabilitation.json",
    "docs/claim_bearing_experiment_competence_standard.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [u for u in registry["units"] if u.get("script") != SCRIPT]
    used = {u["order"] for u in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "All 55 live chapters plus twenty current public, appendix, source-note, roadmap, and X-synopsis surfaces; the immutable 90-record N0-N5 rehabilitation ledger; explicit current-versus-historical scope; and named KERC, QCSA, blocked-claim, and derivative boundaries.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject current reader-facing language that turns N0-N2 records or blocked proof lanes into exact, mechanism, architecture, parent, or chapter-core refutation while preserving immutable historical records and explicit derivative staleness.",
        "output_assertions": [
            "75 current surfaces audited",
            "55 of 55 live chapters audited",
            "zero forbidden overbroad phrases",
            "zero missing rehabilitation boundaries",
            "zero blocked-claim boundary failures",
            "zero broad or chapter-core refutations",
            "eight mutations reject",
        ],
        "claim_scope": "Current reader-facing negative-inference language only; immutable histories retain raw labels and outcomes.",
        "negative_controls": "validator_owned_eight_surface_scope_inference_and_digest_mutations",
        "negative_control_cases": [
            "surface deletion", "N3 invention", "broad inference", "core refutation",
            "forbidden-hit erasure", "surface digest rewrite", "historical mutation", "support promotion",
        ],
        "prohibited_inference": "A clean prose audit does not establish experiment competence, claim truth, support, reproduction, transfer, safety, SOTA, AGI, ASI, publication, deployment, or release readiness.",
        "contract_precision": "exact",
        "semantic_review_state": "current_surface_scope_history_boundary_blocked_obligation_and_negative_inference_reviewed",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda u: u["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
