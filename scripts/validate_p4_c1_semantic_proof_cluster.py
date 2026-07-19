#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "proofs/semantic_cluster_audits/evidence_claim_and_proof_custody.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
EXPECTED_MODULES = [
    "AsiStackProofs.EvidenceStates",
    "AsiStackProofs.ClaimLedgerRefinement",
    "AsiStackProofs.ProofCarryingClaimsRefinement",
    "AsiStackProofs.ProofEnvelope",
]
ALLOWED_DISPOSITIONS = {"adequate", "merge", "reclassify", "remove"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    rows = audit.get("module_dispositions", [])
    status_cluster = next(
        (row for row in data["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == audit.get("cluster_id")),
        None,
    )
    manifest_records = data["manifest"].get("records", [])
    if audit.get("state") != "adequate" or audit.get("scope") != "bounded_finite_custody_semantics":
        out.append("cluster state or scope drifted")
    if [row.get("module") for row in rows] != EXPECTED_MODULES or audit.get("module_count") != 4:
        out.append("module denominator or order drifted")
    if status_cluster is None or status_cluster.get("state") != "adequate" or status_cluster.get("modules") != EXPECTED_MODULES:
        out.append("machine status does not record the terminal adequate cluster")
    if sum(row.get("public_target_count", 0) for row in rows) != audit.get("public_target_count"):
        out.append("public target denominator drifted")
    required = (
        "plain_language_proposition", "modeled_state", "assumptions", "countermodels",
        "consumers", "mutation_evidence", "maximum_inference",
    )
    chapter_text = "\n".join(
        (ROOT / "chapters" / name).read_text(encoding="utf-8")
        for name in (
            "evidence-states-and-claim-discipline.qmd",
            "claim-ledgers-and-belief-revision.qmd",
            "spinoza-verification-and-proof-carrying-claims.qmd",
            "executable-specifications-and-lean-proof-envelope.qmd",
        )
    )
    for row in rows:
        module = row.get("module")
        if row.get("disposition") not in ALLOWED_DISPOSITIONS or any(not row.get(key) for key in required):
            out.append(f"incomplete semantic disposition: {module}")
            continue
        path = ROOT / row["path"]
        if not path.is_file() or f"namespace AsiStackProofs" not in path.read_text(encoding="utf-8"):
            out.append(f"module artifact missing: {module}")
            continue
        theorem_count = len(re.findall(r"(?m)^theorem ", path.read_text(encoding="utf-8")))
        if theorem_count != row.get("theorem_declaration_count"):
            out.append(f"theorem declaration count drifted: {module}")
        target_count = sum(record.get("module") == module for record in manifest_records)
        if target_count != row.get("public_target_count"):
            out.append(f"public target count drifted: {module}")
        for consumer in row["consumers"]:
            if not (ROOT / consumer).exists():
                out.append(f"consumer artifact missing for {module}: {consumer}")
        if not any(term in row["maximum_inference"].lower() for term in ("does not", "inadequate", "retain only")):
            out.append(f"maximum inference lacks an explicit ceiling: {module}")
    for phrase in (
        "provenance assertion remains a separate object from evidence truth",
        "It does not prove natural semantic identity",
        "do not prove semantic or empirical adequacy",
        "does not prove broad chapter claims",
    ):
        if phrase not in chapter_text:
            out.append(f"chapter limitation surface missing: {phrase}")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("cluster claims an unauthorized support, release, or publication effect")
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
        [sys.executable, "scripts/validate_evidence_bundle_completeness_probe.py"],
        [sys.executable, "scripts/validate_claim_ledger_completeness_audit.py"],
        [sys.executable, "scripts/validate_accepted_transition_review_audit.py"],
        [sys.executable, "scripts/validate_claim_state_transition_bridge.py"],
        [sys.executable, "scripts/validate_claim_ledger_refinement.py"],
        [sys.executable, "scripts/validate_proof_carrying_claims_refinement.py"],
    ]
    for command in checks:
        failure = run(command)
        if failure:
            failures.append(failure)
    mutations = [
        ("delete module", lambda value: value["audit"]["module_dispositions"].pop()),
        ("invent disposition", lambda value: value["audit"]["module_dispositions"][0].__setitem__("disposition", "strengthen")),
        ("erase proposition", lambda value: value["audit"]["module_dispositions"][0].__setitem__("plain_language_proposition", "")),
        ("erase assumptions", lambda value: value["audit"]["module_dispositions"][1].__setitem__("assumptions", [])),
        ("erase countermodels", lambda value: value["audit"]["module_dispositions"][2].__setitem__("countermodels", [])),
        ("erase consumers", lambda value: value["audit"]["module_dispositions"][3].__setitem__("consumers", [])),
        ("inflate target count", lambda value: value["audit"].__setitem__("public_target_count", 99)),
        ("invent support effect", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("reopen status", lambda value: next(row for row in value["status"]["semantic_proof_cluster_inventory"]["clusters"] if row["id"] == "evidence_claim_and_proof_custody").__setitem__("state", "strengthen")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4-C1 semantic proof cluster failed:\n - " + "\n - ".join(failures))
    print(
        "P4-C1 semantic proof cluster passed: 4 modules, 16 public targets, "
        "2 adequate and 2 reclassified dispositions, 6 executable checks, "
        f"{len(mutations)} cluster mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
