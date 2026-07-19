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
AUDIT = ROOT / "proofs/semantic_cluster_audits/resource_artifact_and_lifecycle_economics.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
EXPECTED_MODULES = [
    "AsiStackProofs.ResourceEconomicsRefinement",
    "AsiStackProofs.ArtifactRealityRefinement",
    "AsiStackProofs.ArtifactStewardAgents",
    "AsiStackProofs.ArtifactCompressionRefinement",
]
EXPECTED_TARGETS = [11, 10, 7, 3]
EXPECTED_THEOREMS = [9, 15, 16, 8]
EXPECTED_CONSUMERS = [
    "scripts/validate_resource_economics_refinement.py",
    "scripts/validate_artifact_reality_refinement.py",
    "scripts/validate_artifact_steward_lifecycle_probe.py",
    "scripts/validate_artifact_compression_refinement.py",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    rows = audit.get("module_dispositions", [])
    cluster = next((row for row in data["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == audit.get("cluster_id")), None)
    if audit.get("state") != "adequate" or audit.get("scope") != "bounded_finite_resource_allocation_artifact_reality_stewardship_and_compression_lifecycle_semantics":
        out.append("cluster state or scope drifted")
    if [row.get("module") for row in rows] != EXPECTED_MODULES or audit.get("module_count") != 4:
        out.append("module denominator or order drifted")
    if [row.get("public_target_count") for row in rows] != EXPECTED_TARGETS or audit.get("public_target_count") != 31:
        out.append("public target denominator drifted")
    if [row.get("theorem_declaration_count") for row in rows] != EXPECTED_THEOREMS or audit.get("theorem_declaration_count") != 48:
        out.append("theorem denominator drifted")
    if cluster is None or cluster.get("state") != "adequate" or cluster.get("modules") != EXPECTED_MODULES:
        out.append("machine status does not record the terminal adequate cluster")
    manifest = data["manifest"].get("records", [])
    required = ("plain_language_proposition", "modeled_state", "assumptions", "countermodels", "consumers", "mutation_evidence", "maximum_inference")
    for row, targets, theorems, expected_consumer in zip(rows, EXPECTED_TARGETS, EXPECTED_THEOREMS, EXPECTED_CONSUMERS):
        module = row.get("module")
        if row.get("disposition") != "adequate" or any(not row.get(key) for key in required):
            out.append(f"incomplete disposition: {module}")
            continue
        path = ROOT / row["path"]
        if not path.is_file() or len(re.findall(r"(?m)^theorem ", path.read_text(encoding="utf-8"))) != theorems:
            out.append(f"theorem artifact or denominator drifted: {module}")
        if sum(record.get("module") == module for record in manifest) != targets:
            out.append(f"public target denominator drifted: {module}")
        if len(row["assumptions"]) < 3 or len(row["countermodels"]) < 3:
            out.append(f"assumption or countermodel coverage too thin: {module}")
        if expected_consumer not in row["consumers"] or any(not (ROOT / consumer).exists() for consumer in row["consumers"]):
            out.append(f"consumer coverage drifted: {module}")
        if "does not" not in row["maximum_inference"].lower():
            out.append(f"maximum inference lacks explicit ceiling: {module}")
    expected_separations = {"cost_and_efficiency", "artifact_and_reality", "stewardship_and_ownership", "compression_and_usefulness", "closure_and_lifecycle_success", "record_authority"}
    if set(audit.get("semantic_separations", {})) != expected_separations:
        out.append("semantic separation set drifted")
    if not audit.get("cluster_maximum_inference") or any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("cluster ceiling or non-authority boundary drifted")
    return out


def main() -> None:
    data = {"audit": load(AUDIT), "status": load(STATUS), "manifest": load(MANIFEST)}
    failures = errors(data)
    for consumer in EXPECTED_CONSUMERS:
        result = subprocess.run([sys.executable, consumer], cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            failures.append((result.stdout + result.stderr).strip())
    mutations = [
        ("reopen cluster", lambda value: value["audit"].__setitem__("state", "strengthen")),
        ("drop module", lambda value: value["audit"]["module_dispositions"].pop()),
        ("erase proposition", lambda value: value["audit"]["module_dispositions"][0].__setitem__("plain_language_proposition", "")),
        ("erase assumptions", lambda value: value["audit"]["module_dispositions"][1].__setitem__("assumptions", [])),
        ("erase countermodels", lambda value: value["audit"]["module_dispositions"][2].__setitem__("countermodels", [])),
        ("inflate targets", lambda value: value["audit"].__setitem__("public_target_count", 99)),
        ("inflate theorems", lambda value: value["audit"].__setitem__("theorem_declaration_count", 999)),
        ("merge cost and efficiency", lambda value: value["audit"]["semantic_separations"].pop("cost_and_efficiency")),
        ("merge stewardship and ownership", lambda value: value["audit"]["semantic_separations"].pop("stewardship_and_ownership")),
        ("invent support", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("reopen status", lambda value: next(row for row in value["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == "resource_artifact_and_lifecycle_economics").__setitem__("state", "strengthen")),
        ("erase ceiling", lambda value: value["audit"].__setitem__("cluster_maximum_inference", "")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4-C6 semantic proof cluster failed:\n - " + "\n - ".join(failures))
    print("P4-C6 semantic proof cluster passed: 4 adequate modules, 31 public targets, 48 theorem declarations, cost/reality/ownership/compression/lifecycle/authority semantics separated, 12 audit mutations rejected; all 6 P4 clusters terminal; support/release/publication none.")


if __name__ == "__main__":
    main()
