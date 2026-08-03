#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from copy import deepcopy
from itertools import permutations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "MultiAgentDynamics.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "multi-agent-dynamics-collective-intelligence-and-systemic-risk.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
FIXTURE = ROOT / "tests" / "fixtures" / "proof_models" / "multi_agent_population.json"

TAG = "lean:multi_agent.pairwise_validity_no_systemic_promotion"
MODULE = "AsiStackProofs.MultiAgentDynamics"
FORMAL_TARGET = (
    "A finite three-party population model proves that identical six-edge pairwise-authorization "
    "evidence can coexist with opposite campaign-readiness decisions; no classifier over that "
    "matrix alone can exactly recover the ten-dimension review. Nine systemic-axis mutations "
    "preserve pairwise validity, fail readiness, and reach exact repair routes. A conserved "
    "three-unit allocation lifecycle proves composition, receipt accounting, non-authority, "
    "terminal exhaustion, and a local-authorization collision across opposite concentration "
    "outcomes. It establishes no cooperation, non-collusion, systemic safety, human agency, "
    "institutional outcome, support, or external effect."
)

AGENTS = ("human", "systemA", "systemB")
DISTINCT_EDGES = tuple((source, target) for source in AGENTS for target in AGENTS if source != target)


def complete_record() -> dict[str, Any]:
    return {
        "populationRegistered": True,
        "pairwiseAuthorized": {edge: True for edge in DISTINCT_EDGES},
        "modelLineage": {"human": 0, "systemA": 1, "systemB": 2},
        "resourceController": {"compute": "systemA", "capital": "systemB"},
        "humanCanStop": {"systemA": True, "systemB": True},
        "affectedPartyCovered": {"participant": True, "bystander": True},
        "humanExitReachable": True,
        "recoveryReachable": True,
        "residualCustodyPresent": True,
        "nonClaimBoundaryPresent": True,
    }


def fixture_record() -> dict[str, Any]:
    fixture = load(FIXTURE)
    fixture["pairwiseAuthorized"] = {
        tuple(edge): True for edge in fixture.pop("authorizedEdges")
    }
    return fixture


def pairwise_only_record() -> dict[str, Any]:
    record = complete_record()
    record.update(
        modelLineage={"human": 0, "systemA": 0, "systemB": 0},
        resourceController={"compute": "systemA", "capital": "systemA"},
        humanCanStop={"systemA": False, "systemB": False},
        affectedPartyCovered={"participant": False, "bystander": False},
        humanExitReachable=False,
        recoveryReachable=False,
        residualCustodyPresent=False,
    )
    return record


def pairwise_valid(record: dict[str, Any]) -> bool:
    return len(record["pairwiseAuthorized"]) == 6 and all(
        record["pairwiseAuthorized"].get(edge) is True for edge in DISTINCT_EDGES
    )


def checks(record: dict[str, Any]) -> list[tuple[str, bool, str]]:
    return [
        ("populationRegistry", record["populationRegistered"], "repairPopulationRegistry"),
        ("pairwiseAuthorization", pairwise_valid(record), "repairPairwiseAuthorization"),
        (
            "effectiveDiversity",
            record["modelLineage"]["systemA"] != record["modelLineage"]["systemB"],
            "mapCommonDependencies",
        ),
        (
            "resourceConcentration",
            record["resourceController"]["compute"] != record["resourceController"]["capital"],
            "diversifyResourceControl",
        ),
        (
            "humanStop",
            record["humanCanStop"]["systemA"] and record["humanCanStop"]["systemB"],
            "restoreHumanStop",
        ),
        (
            "affectedParties",
            record["affectedPartyCovered"]["participant"]
            and record["affectedPartyCovered"]["bystander"],
            "coverAffectedParties",
        ),
        ("humanExit", record["humanExitReachable"], "restoreHumanExit"),
        ("recovery", record["recoveryReachable"], "establishRecovery"),
        ("residualCustody", record["residualCustodyPresent"], "assignResidualCustody"),
        ("nonClaimBoundary", record["nonClaimBoundaryPresent"], "recordNonClaimBoundary"),
    ]


def ready(record: dict[str, Any]) -> bool:
    return all(value for _, value, _ in checks(record))


def route(record: dict[str, Any]) -> str:
    for _, value, rejected_route in checks(record):
        if not value:
            return rejected_route
    return "runTheseusPopulationCampaign"


MUTATIONS = {
    "populationRegistry": lambda record: record.update(populationRegistered=False),
    "effectiveDiversity": lambda record: record.update(
        modelLineage={"human": 0, "systemA": 0, "systemB": 0}
    ),
    "resourceConcentration": lambda record: record.update(
        resourceController={"compute": "systemA", "capital": "systemA"}
    ),
    "humanStop": lambda record: record.update(
        humanCanStop={"systemA": False, "systemB": False}
    ),
    "affectedParties": lambda record: record.update(
        affectedPartyCovered={"participant": False, "bystander": False}
    ),
    "humanExit": lambda record: record.update(humanExitReachable=False),
    "recovery": lambda record: record.update(recoveryReachable=False),
    "residualCustody": lambda record: record.update(residualCustodyPresent=False),
    "nonClaimBoundary": lambda record: record.update(nonClaimBoundaryPresent=False),
}

EXPECTED_ROUTES = {
    axis: rejected_route
    for axis, _, rejected_route in checks(complete_record())
    if axis != "pairwiseAuthorization"
}

REQUIRED_THEOREMS = {
    "complete_population_has_pairwise_validity",
    "complete_population_is_campaign_ready",
    "complete_population_routes_to_theseus_campaign",
    "pairwise_only_population_has_pairwise_validity",
    "pairwise_only_population_is_not_campaign_ready",
    "pairwise_only_population_routes_to_dependency_mapping",
    "complete_and_pairwise_only_have_identical_pairwise_evidence",
    "pairwise_validity_does_not_entail_population_campaign_readiness",
    "no_pairwise_only_classifier_exactly_recovers_campaign_readiness",
    "every_systemic_axis_omission_preserves_pairwise_validity",
    "every_systemic_axis_omission_blocks_campaign_readiness",
    "every_systemic_axis_omission_reaches_exact_repair_route",
    "campaign_readiness_requires_population_registry",
    "campaign_readiness_requires_pairwise_validity",
    "campaign_readiness_requires_effective_diversity",
    "campaign_readiness_requires_diversified_resource_control",
    "campaign_readiness_requires_human_stop",
    "campaign_readiness_requires_affected_party_coverage",
    "campaign_readiness_requires_human_exit",
    "campaign_readiness_requires_recovery",
    "campaign_readiness_requires_residual_custody",
    "campaign_readiness_requires_non_claim_boundary",
    "accepted_allocation_step_is_valid",
    "accepted_allocation_step_applies_event",
    "accepted_allocation_step_preserves_conservation",
    "accepted_allocation_step_preserves_non_authority",
    "rejected_allocation_step_preserves_exact_state",
    "successful_allocation_run_preserves_conservation",
    "successful_allocation_run_preserves_non_authority",
    "successful_allocation_run_accounts_receipts",
    "allocation_runs_compose",
    "exhausted_allocation_state_rejects_every_event",
    "exhausted_allocation_state_has_no_nonempty_run",
    "concentrated_local_steps_reach_exact_resource_concentration",
    "diversified_local_steps_reach_exact_bounded_allocation",
    "local_authorization_summaries_collide_across_systemic_outcomes",
    "exact_allocation_state_separates_local_authorization_collision",
    "no_exact_systemic_allocation_classifier_from_local_authorization_only",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit(
            "Multi-agent systemic-boundary validation failed:\n"
            + "\n".join(f" - {error}" for error in errors)
        )


def allocation_initial() -> dict[str, Any]:
    return {
        "total_units": 3,
        "unallocated_units": 3,
        "system_a_units": 0,
        "system_b_units": 0,
        "concentration_limit": 2,
        "receipt_count": 0,
        "support_assignment_count": 0,
        "external_effect_authority_count": 0,
    }


def allocation_event(
    target: str,
    *,
    units: int = 1,
    pairwise_authorized: bool = True,
    support_requested: bool = False,
    effect_requested: bool = False,
) -> dict[str, Any]:
    return {
        "target": target,
        "units": units,
        "pairwise_authorized": pairwise_authorized,
        "support_requested": support_requested,
        "effect_requested": effect_requested,
    }


def allocation_conserved(state: dict[str, Any]) -> bool:
    return (
        state["unallocated_units"]
        + state["system_a_units"]
        + state["system_b_units"]
        == state["total_units"]
    )


def allocation_step(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any] | None:
    valid = (
        allocation_conserved(state)
        and event["pairwise_authorized"]
        and 0 < event["units"] <= 1
        and event["units"] <= state["unallocated_units"]
        and event["target"] in {"systemA", "systemB"}
        and not event["support_requested"]
        and not event["effect_requested"]
    )
    if not valid:
        return None
    result = deepcopy(state)
    result["unallocated_units"] -= event["units"]
    result["system_a_units" if event["target"] == "systemA" else "system_b_units"] += event["units"]
    result["receipt_count"] += 1
    return result


def allocation_run(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> dict[str, Any] | None:
    current = deepcopy(state)
    for event in events:
        current = allocation_step(current, event)
        if current is None:
            return None
    return current


def allocation_outcome(events: list[dict[str, Any]]) -> bool:
    final = allocation_run(allocation_initial(), events)
    return bool(
        final
        and final["system_a_units"] <= final["concentration_limit"]
        and final["system_b_units"] <= final["concentration_limit"]
    )


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, FIXTURE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    complete = fixture_record()
    if complete != complete_record():
        errors.append("public population fixture drifted from the closed Lean witness")
    pairwise_only = pairwise_only_record()
    if len(DISTINCT_EDGES) != 6 or not pairwise_valid(complete) or not pairwise_valid(pairwise_only):
        errors.append("both witnesses must preserve all six directed pairwise authorizations")
    if complete["pairwiseAuthorized"] != pairwise_only["pairwiseAuthorized"]:
        errors.append("classifier witnesses do not expose identical pairwise input")
    if not ready(complete) or ready(pairwise_only):
        errors.append("identical pairwise inputs must require opposite campaign-readiness decisions")
    if route(complete) != "runTheseusPopulationCampaign":
        errors.append("complete record must route only to the Project Theseus campaign")
    if route(pairwise_only) != "mapCommonDependencies":
        errors.append("pairwise-only record must stop at dependency mapping")

    if set(MUTATIONS) != set(EXPECTED_ROUTES) or len(MUTATIONS) != 9:
        errors.append("systemic mutation denominator must cover exactly nine non-pairwise axes")
    for axis, mutate in MUTATIONS.items():
        record = deepcopy(complete)
        mutate(record)
        if not pairwise_valid(record):
            errors.append(f"{axis} mutation changed pairwise evidence")
        if ready(record):
            errors.append(f"{axis} mutation remained campaign-ready")
        if route(record) != EXPECTED_ROUTES[axis]:
            errors.append(f"{axis} mutation reached {route(record)}, expected {EXPECTED_ROUTES[axis]}")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/MultiAgentDynamics.lean"],
        cwd=ROOT / "lean",
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        errors.append(
            "Multi-agent Lean recompilation failed:\n"
            + completed.stdout
            + completed.stderr
        )
    if "import AsiStackProofs.MultiAgentDynamics" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import MultiAgentDynamics")
    for forbidden in (
        "systemicSafetyEstablished",
        "beneficialCooperationEstablished",
        "nonCollusionEstablished",
        "humanAgencyEstablished",
        "institutionalOutcomeEstablished",
        "supportStatePromoted",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        if (
            manifest_rows[0].get("module"),
            manifest_rows[0].get("formal_target"),
            manifest_rows[0].get("status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof manifest target binding drifted")
        if (
            triage_rows[0].get("module"),
            triage_rows[0].get("formal_target"),
            triage_rows[0].get("target_status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    owners = [row for row in chapters if row.get("id") == "multi-agent-dynamics-collective-intelligence-and-systemic-risk"]
    if len(owners) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    elif not any(
        row.get("tag") == TAG and row.get("status") == "implemented"
        for row in owners[0].get("proof_targets", [])
    ):
        errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    dossier_flat = re.sub(r"\s+", " ", dossier_text)
    outline_text = OUTLINE.read_text(encoding="utf-8")
    for fragment in (
        TAG,
        "38 theorem declarations",
        "no Boolean classifier restricted",
        "Nine independently checkable systemic-axis mutations",
        "locally authorized allocation",
        "Chapter support remains `argument`",
        "Project Theseus campaign",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "identical pairwise evidence",
        "Nine systemic-axis mutations",
        "support_state_effect` remains `none",
    ):
        if fragment not in dossier_flat:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in outline_text:
        errors.append("outline target row drifted")

    concentrated = [allocation_event("systemA") for _ in range(3)]
    diversified = [
        allocation_event("systemA"),
        allocation_event("systemB"),
        allocation_event("systemB"),
    ]
    concentrated_final = allocation_run(allocation_initial(), concentrated)
    diversified_final = allocation_run(allocation_initial(), diversified)
    if concentrated_final != {
        **allocation_initial(),
        "unallocated_units": 0,
        "system_a_units": 3,
        "receipt_count": 3,
    }:
        errors.append("locally authorized concentrated allocation did not reach its exact state")
    if diversified_final != {
        **allocation_initial(),
        "unallocated_units": 0,
        "system_a_units": 1,
        "system_b_units": 2,
        "receipt_count": 3,
    }:
        errors.append("locally authorized diversified allocation did not reach its exact state")
    concentrated_summary = [event["pairwise_authorized"] for event in concentrated]
    diversified_summary = [event["pairwise_authorized"] for event in diversified]
    if concentrated_summary != diversified_summary:
        errors.append("matched traces lost their identical local-authorization summary")
    if allocation_outcome(concentrated) or not allocation_outcome(diversified):
        errors.append("matched local summaries did not retain opposite systemic outcomes")

    composition_failures = []
    for label, events in (("concentrated", concentrated), ("diversified", diversified)):
        expected = allocation_run(allocation_initial(), events)
        for split in range(len(events) + 1):
            middle = allocation_run(allocation_initial(), events[:split])
            final = None if middle is None else allocation_run(middle, events[split:])
            if final != expected:
                composition_failures.append(f"{label}:{split}")
    if composition_failures:
        errors.append("allocation composition failed: " + ", ".join(composition_failures))

    controls = []
    controls.append(("zero_units", allocation_initial(), allocation_event("systemA", units=0)))
    controls.append(("over_step_cap", allocation_initial(), allocation_event("systemA", units=2)))
    controls.append(("over_available", allocation_initial(), allocation_event("systemA", units=4)))
    controls.append(("human_target", allocation_initial(), allocation_event("human")))
    controls.append(("unauthorized", allocation_initial(), allocation_event("systemA", pairwise_authorized=False)))
    controls.append(("support", allocation_initial(), allocation_event("systemA", support_requested=True)))
    controls.append(("effect", allocation_initial(), allocation_event("systemA", effect_requested=True)))
    broken = allocation_initial(); broken["total_units"] = 4
    controls.append(("broken_conservation", broken, allocation_event("systemA")))
    escaped_controls = [
        label for label, state, event in controls
        if allocation_step(state, event) is not None
    ]
    if escaped_controls:
        errors.append("allocation rejection controls escaped: " + ", ".join(escaped_controls))

    if concentrated_final is not None:
        terminal_failures = [
            target
            for target in AGENTS
            if allocation_step(concentrated_final, allocation_event(target)) is not None
        ]
        if terminal_failures:
            errors.append("exhausted allocation accepted targets: " + ", ".join(terminal_failures))

    diversified_permutations = {
        tuple(order) for order in permutations(("systemA", "systemB", "systemB"))
    }
    if len(diversified_permutations) != 3 or any(
        not allocation_outcome([allocation_event(target) for target in order])
        for order in diversified_permutations
    ):
        errors.append("diversified allocation permutations drifted")

    fail(errors)
    print(
        "Multi-agent systemic-boundary validation passed: exact 38-theorem Lean surface "
        "recompiled; identical six-edge pairwise input, opposite readiness witnesses, 9/9 "
        "systemic-axis mutations, two three-event locally authorized allocation traces with "
        "opposite concentration outcomes, 8 composition splits, 8 rejecting allocation "
        "controls, 3 exhausted-state targets, and 3 diversified permutations; no cooperation, "
        "non-collusion, systemic-safety, human-agency, institutional, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()
