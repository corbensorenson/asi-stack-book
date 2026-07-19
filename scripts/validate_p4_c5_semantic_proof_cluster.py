#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "proofs/semantic_cluster_audits/self_improvement_and_readiness.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
EXPECTED_MODULES = [
    "AsiStackProofs.SelfImprovementRefinement",
    "AsiStackProofs.OpenEndedImprovementRefinement",
    "AsiStackProofs.ReadinessRefinement",
    "AsiStackProofs.CapabilityThresholdRefinement",
]
EXPECTED_TARGETS = [3, 7, 3, 8]
EXPECTED_THEOREMS = [2, 5, 17, 12]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    rows = audit.get("module_dispositions", [])
    status_cluster = next(
        (row for row in data["status"]["semantic_proof_cluster_inventory"]["clusters"]
         if row["id"] == audit.get("cluster_id")), None,
    )
    if audit.get("state") != "adequate" or audit.get("scope") != "bounded_finite_self_improvement_open_ended_campaign_capability_threshold_and_readiness_lifecycle_semantics":
        out.append("cluster state or scope drifted")
    if [row.get("module") for row in rows] != EXPECTED_MODULES or audit.get("module_count") != 4:
        out.append("module denominator or order drifted")
    if [row.get("public_target_count") for row in rows] != EXPECTED_TARGETS or audit.get("public_target_count") != 21:
        out.append("public target denominator drifted")
    if [row.get("theorem_declaration_count") for row in rows] != EXPECTED_THEOREMS or audit.get("theorem_declaration_count") != 36:
        out.append("theorem denominator drifted")
    if status_cluster is None or status_cluster.get("state") != "adequate" or status_cluster.get("modules") != EXPECTED_MODULES:
        out.append("machine status does not record the terminal adequate cluster")

    manifest = data["manifest"].get("records", [])
    required = (
        "plain_language_proposition", "modeled_state", "assumptions",
        "countermodels", "consumers", "mutation_evidence", "maximum_inference",
    )
    for row, target_count, theorem_count in zip(rows, EXPECTED_TARGETS, EXPECTED_THEOREMS):
        module = row.get("module")
        if row.get("disposition") != "adequate" or any(not row.get(key) for key in required):
            out.append(f"incomplete or non-adequate disposition: {module}")
            continue
        path = ROOT / row["path"]
        if not path.is_file():
            out.append(f"module artifact missing: {module}")
            continue
        if len(re.findall(r"(?m)^theorem ", path.read_text(encoding="utf-8"))) != theorem_count:
            out.append(f"theorem declaration count drifted: {module}")
        if sum(record.get("module") == module for record in manifest) != target_count:
            out.append(f"public target count drifted: {module}")
        if len(row["assumptions"]) < 3 or len(row["countermodels"]) < 3:
            out.append(f"assumption or countermodel coverage too thin: {module}")
        for consumer in row["consumers"]:
            if not (ROOT / consumer).exists():
                out.append(f"consumer artifact missing for {module}: {consumer}")
        if "does not" not in row["maximum_inference"].lower():
            out.append(f"maximum inference lacks explicit ceiling: {module}")

    separations = audit.get("semantic_separations", {})
    expected_separations = {
        "proposal_governance", "campaign_open_endedness", "capability_assessment",
        "readiness_handoff", "rollback_and_recovery", "recursive_composition",
    }
    if set(separations) != expected_separations:
        out.append("semantic separation inventory drifted")
    joined = " ".join(separations.values()).lower()
    for token in ("not evidence", "not establish", "not release authority", "not semantic recovery", "does not establish stability"):
        if token not in joined:
            out.append(f"semantic distinction missing: {token}")

    chapter_text = " ".join(
        (ROOT / path).read_text(encoding="utf-8") for path in (
            "chapters/recursive-self-improvement-boundaries.qmd",
            "chapters/open-ended-improvement-engines.qmd",
            "chapters/readiness-gates-residual-escrow-and-quarantine.qmd",
            "chapters/capability-thresholds-and-deployment-commitments.qmd",
        )
    )
    normalized = re.sub(r"\s+", " ", chapter_text)
    for phrase in (
        "adequate only for exact finite proposal-to-outcome custody",
        "adequate only for exact finite campaign-record custody",
        "adequate only for exact finite readiness-record routing",
        "adequate only for that finite authored record discipline",
    ):
        if phrase not in normalized:
            out.append(f"chapter limitation surface missing: {phrase}")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("cluster claims unauthorized state movement")
    maximum = audit.get("cluster_maximum_inference", "")
    for phrase in ("no objective legitimate", "no capability measured or threshold crossed", "no system ready or safe"):
        if phrase not in maximum:
            out.append(f"cluster-wide maximum inference incomplete: {phrase}")
    return out


def run(command: list[str]) -> str | None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        return f"{' '.join(command)} failed: {(result.stdout + result.stderr).strip()}"
    return None


def main() -> None:
    data = {"audit": load(AUDIT), "status": load(STATUS), "manifest": load(MANIFEST)}
    failures = errors(data)
    for command in (
        [sys.executable, "scripts/validate_self_improvement_refinement.py"],
        [sys.executable, "scripts/validate_open_ended_improvement_refinement.py"],
        [sys.executable, "scripts/validate_readiness_refinement.py"],
        [sys.executable, "scripts/validate_capability_threshold_refinement.py"],
    ):
        failure = run(command)
        if failure:
            failures.append(failure)

    mutations = [
        ("delete module", lambda value: value["audit"]["module_dispositions"].pop()),
        ("reopen module", lambda value: value["audit"]["module_dispositions"][0].__setitem__("disposition", "strengthen")),
        ("erase proposition", lambda value: value["audit"]["module_dispositions"][1].__setitem__("plain_language_proposition", "")),
        ("erase assumptions", lambda value: value["audit"]["module_dispositions"][2].__setitem__("assumptions", [])),
        ("erase countermodels", lambda value: value["audit"]["module_dispositions"][3].__setitem__("countermodels", [])),
        ("inflate targets", lambda value: value["audit"].__setitem__("public_target_count", 99)),
        ("inflate theorems", lambda value: value["audit"].__setitem__("theorem_declaration_count", 999)),
        ("merge proposal and improvement", lambda value: value["audit"]["semantic_separations"].pop("proposal_governance")),
        ("merge assessment and crossing", lambda value: value["audit"]["semantic_separations"].pop("capability_assessment")),
        ("invent support", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("reopen status", lambda value: next(row for row in value["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == "self_improvement_and_readiness").__setitem__("state", "strengthen")),
        ("erase cluster ceiling", lambda value: value["audit"].__setitem__("cluster_maximum_inference", "")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4-C5 semantic proof cluster failed:\n - " + "\n - ".join(failures))
    print(
        "P4-C5 semantic proof cluster passed: 4 adequate modules, 21 public targets, "
        "36 theorem declarations, proposal/open-endedness/assessment/readiness/rollback/"
        "recursion semantics separated, 12 audit mutations rejected; "
        "support/release/publication none."
    )


if __name__ == "__main__":
    main()
