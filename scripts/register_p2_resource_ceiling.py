#!/usr/bin/env python3
"""Register the P2 resource-ceiling validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_resource_ceiling.py"
ARTIFACTS = [
    "evidence_quality/p2_resource_ceiling.json",
    "schemas/p2_resource_ceiling.schema.json",
    "docs/p2_resource_ceiling.md",
    "scripts/validate_p2_resource_ceiling.py",
    "scripts/register_p2_resource_ceiling.py",
    "scripts/run_p2_gold_preflight.py",
    "experiments/p2_governed_repository_admission/resource_pilot/attempts/2026-07-17-apiflask-r1/result.json",
    "evidence_quality/p2_gold_preflight_diagnosis.json",
    "evidence_quality/p2_task_qualification_and_replacement_policy.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Host and Docker capacity receipts; complete fixed-denominator pull/image/arm/dependency/disk observations; passing monitored natural-task pilot; hard container isolation; task and campaign headroom; frozen pre-replacement custody.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Freeze a locally feasible P2 resource envelope while rejecting over-allocation, missing headroom, timeout/cleanup tolerance, denominator reduction, resource-to-claim laundering, monitor failure, sampled-CPU overclaim, premature replacement/final opening, or premature resource pass.",
        "output_assertions": ["17.18 GB host and 8.22 GB Docker memory bound", "eight host/Docker CPUs bound", "six-CPU and 8 GB hard container limits", "300-second pull and dependency ceilings", "1.5 GB Engine-content and 7 GB conservative virtual-size ceilings", "60-second stabilized cleanup before residual measurement", "600-second accepted arm below 1200-second kill", "6 GiB peak-memory ceiling", "50 GiB minimum free disk", "5 GiB per-task and 30 GiB campaign residual ceilings", "12-task denominator retained", "CPU-seconds labeled sampled estimate", "candidate outcomes and final pool closed", "fourteen mutations reject"],
        "claim_scope": "Development/replacement resource competence only; ceiling freeze is not a resource-gate pass or governed-admission result.",
        "negative_controls": "validator_owned_fourteen_capacity_size_semantics_stabilization_headroom_timeout_cleanup_denominator_resource_inference_monitor_measurement_custody_and_support_mutations",
        "negative_control_cases": ["memory over Docker", "no memory headroom", "virtual size ceiling erased", "cleanup stabilization erased", "wall equals kill", "timeout allowed", "cleanup allowed", "denominator shrink", "resource refutation", "monitor ignored", "exact CPU overclaim", "replacement draw erased", "premature pass", "support promotion"],
        "prohibited_inference": "Resource feasibility or failure does not establish or refute model ability, governed admission, safety, transfer, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "host_docker_hard_limit_headroom_sampling_disk_emulation_campaign_custody_and_non_claim_boundaries_reviewed"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
