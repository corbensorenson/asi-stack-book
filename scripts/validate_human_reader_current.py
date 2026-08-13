#!/usr/bin/env python3
"""Validate the maintained independent 26-unit Human Reader manuscript."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_human_reader_current import (
    EDITION,
    MANIFEST,
    ROOT,
    STRUCTURE,
    build,
)

STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"


UNIT_23_REQUIRED = [
    "## The Complete Bill",
    "## Speed Is a Qualified Route",
    "## Deliberation Has a Failure Surface",
    "## Compression Moves Burden",
    "## One Allocation Decision",
    "## The Allocation Lease",
    "## A Worked Budget",
    "## Failure Cases",
    "## Evidence and Experiments",
    "## Human Time and Organizational Cost",
    "## From Minimum Implementation to Mature System",
    "## What This Establishes",
    "evidentiary authority are separate claims",
    "does not establish that the proposed controller is economically optimal",
]
UNIT_04_REQUIRED = [
    "## A Change Can Be Correct and Still Be Unsafe",
    "## The Smallest Powerful Kernel",
    "## The Model Is Part of the Attack Surface",
    "## Privacy Is About Use, Not Merely Secrecy",
    "## Protected Computation Is Evidence, Not Permission",
    "## Model Weights Are a Custody Graph",
    "## The Supply Chain Is a Living Dependency Graph",
    "## Release Changes the Kind of Control",
    "## One End-to-End Custody Decision",
    "## Failure Cases",
    "## What the Current Evidence Can Establish",
    "## From Minimum Implementation to a Mature Security Fabric",
    "## The Strongest Objection",
    "## What This Establishes",
    "A successful local load is not release authority",
    "The conclusion should change if simpler systems prove equally effective",
]
UNIT_05_REQUIRED = [
    "## A Passing Test Is Not a General Verdict",
    "## Claims Need Stable Identities",
    "## Support States Are Not a Confidence Score",
    "## An Evidence Transition Is a Bounded Argument",
    "## Oversight Begins Where the Evaluator Is Weaker",
    "## Independence Is a Dependency Graph",
    "## White-Box Evidence Starts a New Challenge",
    "## One Patch, Three Evidence Paths",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Evidence Can Establish",
    "## From Minimum Implementation to a Mature Evidence System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "A passing test is not a method verdict",
    "This Human Reader synthesis does not combine those narrower\nresults into a stronger conclusion",
]
UNIT_06_REQUIRED = [
    "## The User Did Not Ask for That",
    "## Intent Is an Interpretation, Not a String",
    "## Outcomes and Means Must Stay Separate",
    "## Authority Is Not Context",
    "## A Contract Should Preserve Uncertainty",
    "## Meaningful Control Is a Resource Condition",
    "## The Approver Is an Epistemic Target",
    "## One Proposal, Four Decisions",
    "## Revocation and Re-Contracting",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Boundary to a Mature Control System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Alignment concerns the relation between result and mandate",
    "the approver is also an epistemic target",
]
UNIT_07_REQUIRED = [
    "## The Patch Passes Every Test",
    "## A Constraint Is Not an Objective",
    "## Values Do Not Become One Number",
    "## Objective Formation Is a Lease",
    "## Behavior Is Not Objective Integrity",
    "## Separating Interventions",
    "## Who May Amend the Goal?",
    "## Dissent, Appeal, and Rights",
    "## One Proposal, Four Governance Objects",
    "## Revocation and Descendant Retirement",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Registry to a Mature Objective Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "an optimizer\ncannot ratify its own purpose",
    "This Human Reader synthesis does not combine those bounded results into a\nstronger theorem",
]
UNIT_08_REQUIRED = [
    "## The Patch Leaves the Repository",
    "## Capability Is Not Mandate",
    "## The Affected Public Is Part of the System",
    "## Participation Is Not Representation",
    "## Jurisdiction Is a Routing Constraint",
    "## Coordination Must Survive Partial Participation",
    "## Resilience Has Four Different Verbs",
    "## One Shared Service, Many Authorities",
    "## Remedy Must Reach the Harmed Party",
    "## Concentration and Gradual Loss of Human Influence",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Packet to a Mature Governance Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Capability does not\ncreate mandate",
    "This Human Reader synthesis does not combine the two finite reviews into a\nstronger theorem",
]
UNIT_09_REQUIRED = [
    "## The Name That Survives the Upgrade",
    "## A Field Is a Promise, Not a Label",
    "## Compatibility Is Not Qualification",
    "## The Patch Verifier Replacement",
    "## Replacement Is a Transaction",
    "## Rollback Is Not Time Travel",
    "## Authority Must Not Ride Along",
    "## The Proof Boundary",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## From a Minimum Record to a Replacement Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The field holds the\npromise. The implementation is one defeasible attempt to keep it",
    "No finite proof, schema, fixture, or clean local rollback can answer that\nquestion alone",
]
UNIT_10_REQUIRED = [
    "## Four Reports About One Patch",
    "## A Report Is Not the World",
    "## Observation Is Task-Relative",
    "## Agreement Is Not Independence",
    "## Calibration and Missingness Travel With the Result",
    "## Disagreement Is a Routing Signal",
    "## Freshness Is Part of Meaning",
    "## From Observation to Physical Effect",
    "## Simulation Is an Instrument, Not a World",
    "## Effect Observation and Recovery",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Contract to an Observation Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The test runner and reviewer both read artifacts produced from the same stale\nbuild cache",
    "The models establish neither environmental truth, calibration, causal\nindependence, useful fusion, physical safety, recovery, nor deployment\nreadiness",
]
UNIT_11_REQUIRED = [
    "## The Branch That Passed",
    "## Five Kinds of State",
    "## Freeze the Forecast Before the Intervention",
    "## Prediction Is Not Intervention",
    "## Horizon Changes the Claim",
    "## Keep More Than One Possible World",
    "## Optimization Finds Favorable Mistakes",
    "## The Trial and the Receipt",
    "## Learning Without Rewriting History",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Contract to a Reality-Grounded Model Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The model's\nown predicted state cannot serve as that effect observation",
    "The claim-bearing empirical lane is prospectively specified but has not run",
]
UNIT_12_REQUIRED = [
    "## A Plan That Survives Contact",
    "## Six Objects That Should Not Collapse",
    "## The Plan Begins With a Frozen Contract",
    "## Obligations, Not To-Do Items",
    "## Dependencies Have Types",
    "## Unknown Is a Planning State",
    "## Alternatives Need a Denominator",
    "## Reachability Is Not Permission",
    "## Scheduling the Whole Cost",
    "## Replanning Is a New Version",
    "## Branch Joins Are Semantic Decisions",
    "## Stop, Fallback, and Recovery Are Work",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Planner to a Governed Control Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Reachability is not permission",
    "They do not establish decomposition quality, dependency truth or completeness",
]
UNIT_13_REQUIRED = [
    "## The Artifact That Followed the Plan",
    "## A Plan Node Is Not Yet an Artifact",
    "## Stable Semantic Identity",
    "## Ambiguity Is Compiler Debt",
    "## Relations Need Roles",
    "## Dimensions Are Types, Not Decoration",
    "## Equivalence Is Relative to a Consumer",
    "## Search Is a Candidate Generator",
    "## A New Substrate Must Earn Its Boundary",
    "## Progressive Lowering",
    "## Validate the Actual Target",
    "## Repair by Identity and Observed Change",
    "## Reverse Compilation Is Not Mind Reading",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Compiler to a Cognitive Toolchain",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "None of these results transfers support to the other owners",
    "selected full route tied its baseline at 1.000 task accuracy while\nusing 1.913386 times the operations",
]


def validate(manifest: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    if manifest != expected:
        errors.append("manifest differs from its canonical graph/outline/manuscript derivation")
    if manifest.get("unit_count") != 26 or manifest.get("owner_route_count") != 87:
        errors.append("Human Reader denominator drift")
    units = manifest.get("units", [])
    owner_ids = [owner_id for unit in units for owner_id in unit.get("owner_ids", [])]
    if len(owner_ids) != len(set(owner_ids)):
        errors.append("a technical owner routes to more than one Human Reader unit")
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    canonical_ids = {
        chapter["id"] for part in structure["parts"] for chapter in part["chapters"]
    }
    if set(owner_ids) != canonical_ids:
        errors.append("Human Reader routes omit or invent a canonical owner")
    for unit in units:
        path = EDITION / unit["source_file"]
        state = unit.get("state")
        if state == "not_started":
            if path.exists():
                errors.append(f"{unit['unit_id']}: existing source marked not started")
            continue
        if not path.is_file():
            errors.append(f"{unit['unit_id']}: started source is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "chapters/" in text and "{{< include" in text and "../generated/" not in text:
            errors.append(f"{unit['unit_id']}: source appears to include a live technical chapter")
        if state == "target_length_reached_internal_review_pending" and not (
            unit["target_min_words"] <= unit["visible_word_count"] <= unit["target_max_words"]
        ):
            errors.append(f"{unit['unit_id']}: false target-length completion")
        if unit.get("owner_support_states") != ["argument"]:
            errors.append(f"{unit['unit_id']}: routed owner support changed or was combined")
        panel_path = EDITION / "generated" / f"{unit['unit_id']}-status.qmd"
        if panel_path.is_file():
            panel = panel_path.read_text(encoding="utf-8")
            for owner_id in unit["owner_ids"]:
                owner_url = f"https://corbensorenson.github.io/asi-stack-book/chapters/{owner_id}.html"
                if owner_url not in panel:
                    errors.append(f"{unit['unit_id']}: missing discoverable owner route {owner_id}")
    unit_04 = next((unit for unit in units if unit.get("unit_id") == "unit-04"), None)
    if unit_04 is None or unit_04.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 4 has not reached its drafting target")
    else:
        text = (EDITION / unit_04["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_04_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 4 missing required argument boundary: {fragment!r}")
    unit_23 = next((unit for unit in units if unit.get("unit_id") == "unit-23"), None)
    if unit_23 is None or unit_23.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 23 has not reached its drafting target")
    else:
        text = (EDITION / unit_23["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_23_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 23 missing required argument boundary: {fragment!r}")
    unit_05 = next((unit for unit in units if unit.get("unit_id") == "unit-05"), None)
    if unit_05 is None or unit_05.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 5 has not reached its drafting target")
    else:
        text = (EDITION / unit_05["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_05_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 5 missing required argument boundary: {fragment!r}")
    unit_06 = next((unit for unit in units if unit.get("unit_id") == "unit-06"), None)
    if unit_06 is None or unit_06.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 6 has not reached its drafting target")
    else:
        text = (EDITION / unit_06["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_06_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 6 missing required argument boundary: {fragment!r}")
    unit_07 = next((unit for unit in units if unit.get("unit_id") == "unit-07"), None)
    if unit_07 is None or unit_07.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 7 has not reached its drafting target")
    else:
        text = (EDITION / unit_07["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_07_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 7 missing required argument boundary: {fragment!r}")
    unit_08 = next((unit for unit in units if unit.get("unit_id") == "unit-08"), None)
    if unit_08 is None or unit_08.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 8 has not reached its drafting target")
    else:
        text = (EDITION / unit_08["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_08_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 8 missing required argument boundary: {fragment!r}")
    unit_09 = next((unit for unit in units if unit.get("unit_id") == "unit-09"), None)
    if unit_09 is None or unit_09.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 9 has not reached its drafting target")
    else:
        text = (EDITION / unit_09["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_09_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 9 missing required argument boundary: {fragment!r}")
    unit_10 = next((unit for unit in units if unit.get("unit_id") == "unit-10"), None)
    if unit_10 is None or unit_10.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 10 has not reached its drafting target")
    else:
        text = (EDITION / unit_10["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_10_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 10 missing required argument boundary: {fragment!r}")
    unit_11 = next((unit for unit in units if unit.get("unit_id") == "unit-11"), None)
    if unit_11 is None or unit_11.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 11 has not reached its drafting target")
    else:
        text = (EDITION / unit_11["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_11_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 11 missing required argument boundary: {fragment!r}")
    unit_12 = next((unit for unit in units if unit.get("unit_id") == "unit-12"), None)
    if unit_12 is None or unit_12.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 12 has not reached its drafting target")
    else:
        text = (EDITION / unit_12["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_12_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 12 missing required argument boundary: {fragment!r}")
    unit_13 = next((unit for unit in units if unit.get("unit_id") == "unit-13"), None)
    if unit_13 is None or unit_13.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 13 has not reached its drafting target")
    else:
        text = (EDITION / unit_13["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_13_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 13 missing required argument boundary: {fragment!r}")
    if manifest.get("support_state_effect") != "none" or manifest.get("release_effect") != "none":
        errors.append("Human Reader drafting changed support or release state")
    status = json.loads(STATUS.read_text(encoding="utf-8"))["editorial_product_migration"]
    expected_status = {
        "human_reader_current_manifest_path": "editions/reader_manuscript/current/manifest.json",
        "human_reader_started_unit_count": manifest.get("started_unit_count"),
        "human_reader_target_length_unit_count": manifest.get("target_length_unit_count"),
        "human_reader_visible_word_count": manifest.get("visible_word_count"),
    }
    for field, value in expected_status.items():
        if status.get(field) != value:
            errors.append(f"roadmap Human Reader status drift: {field}")
    return errors


def main() -> None:
    expected, outputs = build()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate(manifest, expected)
    stale = [
        path.relative_to(ROOT).as_posix()
        for path, text in outputs.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]
    if stale:
        errors.append("stale generated Human Reader derivatives: " + ", ".join(stale))

    altered = copy.deepcopy(manifest)
    altered["units"][0]["owner_ids"] = []
    if not validate(altered, expected):
        errors.append("negative control accepted: owner-route loss")
    altered = copy.deepcopy(manifest)
    altered["units"][22]["visible_word_count"] = 1
    if not validate(altered, expected):
        errors.append("negative control accepted: false length completion")
    altered = copy.deepcopy(manifest)
    altered["support_state_effect"] = "promoted"
    if not validate(altered, expected):
        errors.append("negative control accepted: support laundering")

    if errors:
        raise SystemExit("Human Reader current validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Human Reader current validation passed: {manifest['started_unit_count']}/26 units started, "
        f"{manifest['target_length_unit_count']} at target length, 87 owners routed once, "
        f"{manifest['visible_word_count']} visible words, and 3 rejecting controls."
    )


if __name__ == "__main__":
    main()
