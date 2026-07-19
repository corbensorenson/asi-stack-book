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
AUDIT = ROOT / "proofs/semantic_cluster_audits/authority_effect_rollback_and_corrigibility.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
EXPECTED_MODULES = [
    "AsiStackProofs.AuthorityEffectRefinement",
    "AsiStackProofs.Replacement",
    "AsiStackProofs.Corrigibility",
    "AsiStackProofs.IntentExecutionRefinement",
]
EXPECTED_DISPOSITIONS = {
    "AsiStackProofs.AuthorityEffectRefinement": "adequate",
    "AsiStackProofs.Replacement": "adequate",
    "AsiStackProofs.Corrigibility": "reclassify",
    "AsiStackProofs.IntentExecutionRefinement": "adequate",
}
ALLOWED_DISPOSITIONS = {"adequate", "merge", "reclassify", "remove"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    rows = audit.get("module_dispositions", [])
    status_cluster = next(
        (row for row in data["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == audit.get("cluster_id")),
        None,
    )
    records = data["manifest"].get("records", [])
    if audit.get("state") != "adequate" or audit.get("scope") != "bounded_finite_authority_effect_replacement_corrigibility_and_intent_execution_semantics":
        out.append("cluster state or scope drifted")
    if [row.get("module") for row in rows] != EXPECTED_MODULES or audit.get("module_count") != 4:
        out.append("module denominator or order drifted")
    if status_cluster is None or status_cluster.get("state") != "adequate" or status_cluster.get("modules") != EXPECTED_MODULES:
        out.append("machine status does not record the terminal adequate cluster")
    if sum(row.get("public_target_count", 0) for row in rows) != audit.get("public_target_count") or audit.get("public_target_count") != 11:
        out.append("public target denominator drifted")
    if sum(row.get("theorem_declaration_count", 0) for row in rows) != audit.get("theorem_declaration_count") or audit.get("theorem_declaration_count") != 65:
        out.append("theorem denominator drifted")

    required = (
        "plain_language_proposition", "modeled_state", "assumptions",
        "countermodels", "consumers", "mutation_evidence", "maximum_inference",
    )
    for row in rows:
        module = row.get("module")
        if row.get("disposition") not in ALLOWED_DISPOSITIONS or row.get("disposition") != EXPECTED_DISPOSITIONS.get(module):
            out.append(f"incorrect terminal disposition: {module}")
        if any(not row.get(key) for key in required):
            out.append(f"incomplete semantic disposition: {module}")
            continue
        path = ROOT / row["path"]
        if not path.is_file() or "namespace AsiStackProofs" not in path.read_text(encoding="utf-8"):
            out.append(f"module artifact missing: {module}")
            continue
        theorem_count = len(re.findall(r"(?m)^theorem ", path.read_text(encoding="utf-8")))
        if theorem_count != row.get("theorem_declaration_count"):
            out.append(f"theorem declaration count drifted: {module}")
        target_count = sum(record.get("module") == module for record in records)
        if target_count != row.get("public_target_count"):
            out.append(f"public target count drifted: {module}")
        if len(row.get("assumptions", [])) < 3 or len(row.get("countermodels", [])) < 3:
            out.append(f"assumption or countermodel coverage too thin: {module}")
        for consumer in row["consumers"]:
            if not (ROOT / consumer).exists():
                out.append(f"consumer artifact missing for {module}: {consumer}")
        if "does not" not in row["maximum_inference"].lower():
            out.append(f"maximum inference lacks an explicit ceiling: {module}")
    chapter_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8") for path in (
            "chapters/system-boundaries-and-authority.qmd",
            "chapters/capability-replacement-and-rollback.qmd",
            "chapters/constitutional-alignment-substrate.qmd",
            "chapters/intent-to-execution-contracts.qmd",
        )
    )
    normalized_chapter_text = re.sub(r"\s+", " ", chapter_text)
    for phrase in (
        "adequate only for its bounded reachable grant-to-local-effect semantics",
        "Its 37 declarations remain bounded consequences of authored records",
        "reclassifies the latter as a countermodel-only appendix",
        "adequate only for exact root/parent preservation",
    ):
        if phrase not in normalized_chapter_text:
            out.append(f"chapter limitation surface missing: {phrase}")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("cluster claims an unauthorized support, release, or publication effect")
    if "proves no identity or receipt authentic" not in audit.get("cluster_maximum_inference", ""):
        out.append("cluster-wide maximum inference is incomplete")
    return out


def run(command: list[str]) -> str | None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        return f"{' '.join(command)} failed: {(result.stdout + result.stderr).strip()}"
    return None


def main() -> None:
    data = {"audit": load(AUDIT), "status": load(STATUS), "manifest": load(MANIFEST)}
    failures = errors(data)
    checks = [
        [sys.executable, "scripts/validate_authority_effect_refinement.py"],
        [sys.executable, "scripts/validate_capability_replacement.py"],
        [sys.executable, "scripts/validate_capability_replacement_trace_probe.py"],
        [sys.executable, "scripts/validate_intent_governed_replacement_bridge.py"],
        [sys.executable, "scripts/validate_intent_execution_vertical_refinement.py"],
        [sys.executable, "scripts/validate_intent_execution_handoff_probe.py"],
    ]
    for command in checks:
        failure = run(command)
        if failure:
            failures.append(failure)
    mutations = [
        ("delete module", lambda value: value["audit"]["module_dispositions"].pop()),
        ("upgrade corrigibility", lambda value: value["audit"]["module_dispositions"][2].__setitem__("disposition", "adequate")),
        ("erase proposition", lambda value: value["audit"]["module_dispositions"][0].__setitem__("plain_language_proposition", "")),
        ("erase assumptions", lambda value: value["audit"]["module_dispositions"][1].__setitem__("assumptions", [])),
        ("erase countermodels", lambda value: value["audit"]["module_dispositions"][2].__setitem__("countermodels", [])),
        ("erase consumers", lambda value: value["audit"]["module_dispositions"][3].__setitem__("consumers", [])),
        ("inflate target count", lambda value: value["audit"].__setitem__("public_target_count", 99)),
        ("inflate theorem count", lambda value: value["audit"].__setitem__("theorem_declaration_count", 999)),
        ("invent support", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("reopen status", lambda value: next(row for row in value["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == "authority_effect_rollback_and_corrigibility").__setitem__("state", "strengthen")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4-C3 semantic proof cluster failed:\n - " + "\n - ".join(failures))
    print(
        "P4-C3 semantic proof cluster passed: 4 modules, 11 public targets, 65 theorem "
        "declarations, 3 adequate and 1 reclassified disposition, 6 executable checks, "
        "10 cluster mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
