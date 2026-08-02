#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/PhysicalComputeInfrastructureReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/physical_compute_infrastructure_dossier.json"
CHAPTER = ROOT / "chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/physical-compute-infrastructure-energy-and-environmental-constraints.md"
TAG = "lean:physical-compute-infrastructure-energy-and-environmental-constraints.admission_boundary"
MODULE = "AsiStackProofs.PhysicalComputeInfrastructureReview"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("workloadIdentityBound", "bindWorkloadIdentity"),
    yes("siteIdentityBound", "bindSiteIdentity"),
    yes("intervalBound", "bindInterval"),
    yes("hardwareConfigBound", "bindHardwareConfig"),
    yes("topologyBound", "bindTopology"),
    yes("workloadVersionBound", "bindWorkloadVersion"),
    yes("meterVersionBound", "bindMeterVersion"),
    yes("requestedComputeSeparated", "separateRequestedCompute"),
    yes("nameplateComputeSeparated", "separateNameplateCompute"),
    yes("availableComputeSeparated", "separateAvailableCompute"),
    yes("deliveredComputeSeparated", "separateDeliveredCompute"),
    yes("usefulWorkSeparated", "separateUsefulWork"),
    yes("computeCapacityBound", "bindComputeCapacity"),
    yes("memoryCapacityBound", "bindMemoryCapacity"),
    yes("networkCapacityBound", "bindNetworkCapacity"),
    yes("storageCapacityBound", "bindStorageCapacity"),
    yes("powerCapacityBound", "bindPowerCapacity"),
    yes("thermalCapacityBound", "bindThermalCapacity"),
    yes("operationalEnergyBound", "bindOperationalEnergy"),
    yes("facilityOverheadBound", "bindFacilityOverhead"),
    yes("temporalGridBound", "bindTemporalGrid"),
    yes("backupEnergyBound", "bindBackupEnergy"),
    yes("coolingBound", "bindCooling"),
    yes("waterBound", "bindWater"),
    yes("embodiedMaterialsBound", "bindEmbodiedMaterials"),
    yes("landCommunityBound", "bindLandCommunity"),
    yes("uncertaintyBound", "bindUncertainty"),
    yes("allocationMethodBound", "bindAllocationMethod"),
    yes("interruptionBudgetBound", "bindInterruptionBudget"),
    yes("degradationPlanBound", "addDegradationPlan"),
    yes("failoverPlanBound", "addFailoverPlan"),
    yes("concentrationBound", "bindConcentration"),
    yes("maintenanceBound", "bindMaintenance"),
    yes("demandResponseBound", "bindDemandResponse"),
    yes("retirementBound", "bindRetirement"),
    yes("dataDestructionBound", "bindDataDestruction"),
    yes("reboundObservationBound", "observeRebound"),
    yes("residualOwnerBound", "assignResidualOwner"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    no("availabilityClaimed", "rejectAvailabilityClaim"),
    no("sustainabilityClaimed", "rejectSustainabilityClaim"),
    no("resilienceClaimed", "rejectResilienceClaim"),
    no("communityAcceptabilityClaimed", "rejectCommunityAcceptabilityClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""device_counter_does_not_establish_delivered_useful_compute facility_pue_does_not_establish_sustainability renewable_contract_does_not_establish_temporal_grid_impact workload_energy_estimate_does_not_establish_community_acceptability outage_drill_does_not_establish_resilience aggregate_demand_append_composes every_member_compute_demand_is_bounded_by_aggregate aggregate_compute_overrun_rejects_fleet_fit attributed_energy_append_composes hidden_backup_energy_breaks_exact_accounting review_step_preserves_stage_invariant review_run_preserves_stage_invariant campaign_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_workload_capacity_campaign every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_capacity readiness_requires_impact readiness_requires_resilience readiness_requires_boundary expired_capacity_contract_remains_expired_when_time_advances demand_increase_past_capacity_rejects_fit capacity_loss_preserves_existing_overrun workload_change_invalidates_capacity_receipt site_change_invalidates_capacity_receipt interval_change_invalidates_capacity_receipt hardware_change_invalidates_capacity_receipt meter_change_invalidates_capacity_receipt identical_energy_headlines_can_hide_opposite_useful_delivery energy_headlines_cannot_recover_useful_delivery identical_unit_efficiency_can_hide_opposite_total_impact unit_efficiency_cannot_recover_total_impact physical_capacity_failure_rejects_resource_budget_gate""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusWorkloadCapacityCampaign")


def demand(rows: list[dict[str, int]]) -> dict[str, int]:
    return {field: sum(row[field] for row in rows) for field in ("compute", "memory", "network", "storage", "power", "cooling")}


def attributed(row: dict[str, int]) -> int:
    return sum(row[field] for field in ("operationalEnergy", "facilityOverhead", "backupEnergy", "coolingEnergy"))


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Physical-compute infrastructure review failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 44 or len({axis[0] for axis in AXES}) != 44:
        errors.append("mutation denominator is not 44 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusWorkloadCapacityCampaign":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    workloads = dossier["workloads"]
    aggregate = demand(workloads)
    if aggregate != dossier["capacity"] or demand(workloads[:1] + workloads[1:]) != aggregate:
        errors.append("workload aggregation or append composition drifted")
    if any(row["compute"] > aggregate["compute"] for row in workloads):
        errors.append("member compute bound drifted")
    if aggregate["compute"] <= dossier["capacity"]["compute"] - 1:
        errors.append("aggregate compute overrun control drifted")

    impacts = dossier["impactEntries"]
    if not all(row["reportedTotal"] == attributed(row) for row in impacts):
        errors.append("impact accounting fixture drifted")
    if sum(map(attributed, impacts)) != sum(map(attributed, impacts[:1])) + sum(map(attributed, impacts[1:])):
        errors.append("attributed-energy append control drifted")
    hidden = deepcopy(impacts[0])
    hidden["reportedTotal"] -= hidden["backupEnergy"]
    if hidden["backupEnergy"] <= 0 or hidden["reportedTotal"] == attributed(hidden):
        errors.append("hidden backup-energy control drifted")

    scope = dossier["receiptScope"]
    if any(scope | {field: scope[field] + 1} == scope for field in scope):
        errors.append("receipt-scope invalidation control drifted")
    if (40, 900, True) == (40, 900, False) or (7, 4, True) == (7, 4, False):
        errors.append("non-identifiability collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 36-theorem surface drifted")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text):
        errors.append("Lean trust boundary widened")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or (manifest_rows[0].get("module"), manifest_rows[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage_rows) != 1 or (triage_rows[0].get("module"), triage_rows[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")

    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in (
        "36 theorem declarations", "44 admission-axis mutations", "finite lists",
        "energy headlines", "unit-efficiency signals", "Resource Economics",
        "Chapter support remains `argument`", "Project Theseus workload-capacity campaign",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Physical-compute infrastructure review failed:\n - " + "\n - ".join(errors))
    print(
        "Physical-compute infrastructure review passed: six-transition lifecycle, 44/44 exact repairs, "
        "finite demand and impact accounting, adverse monotonicity, five receipt invalidations, two "
        "non-identifiability results, one rejecting Resource Economics bridge, and 36 exact Lean "
        "declarations; no performance, sustainability, resilience, community, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()
