#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/CompactGenerationRefinement.lean"
SCHEMA = ROOT / "schemas/compact_generation_refinement.schema.json"
RESULT = ROOT / "experiments/compact_generation_refinement/results/2026-07-15-local.json"
COMMAND = "python3 scripts/validate_compact_generation_refinement.py"

SOURCE_RESULTS = {
    "compact_gvr": ROOT / "experiments/compact_gvr_slice/results/2026-07-01-local.json",
    "residual_conservation": ROOT / "experiments/residual_honesty_conservation/results/2026-07-03-local.json",
    "residual_trace": ROOT / "experiments/residual_ledger_trace/results/2026-07-03-local.json",
    "residual_storage": ROOT / "experiments/residual_ledger_storage_replay/results/2026-07-04-local.json",
}

STAGES = ["requested", "sourceBound", "generated", "verified", "residualized", "published", "migrated", "consumed", "closed"]
KINDS = {
    "requested": "bindSource", "sourceBound": "generate", "generated": "verify",
    "verified": "residualize", "residualized": "publish", "published": "migrate",
    "migrated": "consume", "consumed": "close", "closed": "close",
}
ACCEPTED = {
    "accept_source_binding", "accept_generation", "accept_verification", "activate_fallback",
    "accept_residualization", "accept_publication", "accept_migration", "accept_consumption", "accept_closure",
}
REPRESENTATION_KEYS = {
    "representationId", "representationVersion", "sourceDigest", "contractDigest",
    "generatorDigest", "targetDigest", "verifierDigest", "residualLedgerDigest",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str]) -> None:
    print("Compact generation refinement failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def packet() -> dict[str, Any]:
    p: dict[str, Any] = {
        "representationId": 2001, "representationVersion": 3, "sourceDigest": 2002,
        "contractDigest": 2003, "generatorDigest": 2004, "targetDigest": 2005,
        "verifierDigest": 2006, "residualLedgerDigest": 2007, "consumerDigest": 2008,
        "resultSetDigest": 2009, "eventDigest": 1,
    }
    true_fields = [
        "requestWellFormed", "sourceArtifactPresent", "sourceDigestBound", "rightsBound",
        "versionedContract", "compressionBoundary", "consumerPolicy", "generatorPresent",
        "seedOrLawPresent", "searchBound", "generatedArtifactPresent", "generationCostRecorded",
        "exactClaim", "verifierIdentity", "independentEvaluator", "observedReconstruction",
        "targetDigestMatches", "verificationPassed", "fallbackExecutable", "fullSourcePreserved",
        "verifierCostRecorded", "obligationScan", "unresolvedObligations", "residualRecordPresent",
        "residualOwner", "residualBurdenRecorded", "sourceProvenance", "totalCostRecorded",
        "fallbackReceipt", "artifactReceipt", "resultDigestsBound", "evidenceTransitionPresent",
        "publicationNonClaims", "semanticNodeUsed", "provenanceIdentity", "provenanceContent",
        "groundingEvaluator", "hierarchyChanged", "migrationRecord", "priorReferencesPreserved",
        "consumerMap", "consumerAcknowledgment", "policyCompatible", "downstreamEvaluation",
        "utilityMeasured", "residualClosedOrEscrowed", "chainIntegrity", "descendantReferences",
        "cleanup", "finalNonClaims",
    ]
    false_fields = [
        "lossyRepresentation", "declaredZeroResidual", "supportPromotionRequested",
        "supersessionRecorded", "externalEffectRequested",
    ]
    p.update({field: True for field in true_fields})
    p.update({field: False for field in false_fields})
    return p


def state(stage: str, *, last: int = 0, fallback_count: int = 0) -> dict[str, Any]:
    p = packet()
    s = {key: p[key] for key in REPRESENTATION_KEYS}
    s.update({"consumerDigest": p["consumerDigest"], "resultSetDigest": p["resultSetDigest"], "lastEventDigest": last, "fallbackCount": fallback_count})
    return s


def route(stage: str, kind: str, p: dict[str, Any], s: dict[str, Any] | None = None) -> str:
    s = state(stage) if s is None else s
    if kind != KINDS[stage]:
        return "reject_wrong_stage"
    if any(p[key] != s[key] for key in REPRESENTATION_KEYS):
        return "reject_representation_substitution"
    if p["consumerDigest"] != s["consumerDigest"]:
        return "reject_consumer_substitution"
    if p["resultSetDigest"] != s["resultSetDigest"]:
        return "reject_result_digest_substitution"
    if p["eventDigest"] == s["lastEventDigest"]:
        return "reject_event_replay"
    if p["externalEffectRequested"]:
        return "reject_authority_leak"

    checks = {
        "requested": [
            ("requestWellFormed", "reject_malformed_request"), ("sourceArtifactPresent", "require_source_artifact"),
            ("sourceDigestBound", "require_source_digest"), ("rightsBound", "require_rights"),
            ("versionedContract", "require_versioned_contract"), ("compressionBoundary", "require_compression_boundary"),
            ("consumerPolicy", "require_consumer_policy"),
        ],
        "sourceBound": [
            ("generatorPresent", "require_generator"), ("seedOrLawPresent", "require_seed_or_law"),
            ("searchBound", "require_search_bound"), ("generatedArtifactPresent", "require_generated_artifact"),
            ("generationCostRecorded", "require_generation_cost"),
        ],
        "migrated": [
            ("consumerAcknowledgment", "require_consumer_acknowledgment"),
            ("policyCompatible", "require_policy_compatibility"),
            ("downstreamEvaluation", "require_downstream_evaluation"),
            ("utilityMeasured", "require_utility_measurement"),
        ],
        "consumed": [
            ("residualClosedOrEscrowed", "require_residual_closure"),
            ("chainIntegrity", "require_chain_integrity"),
            ("descendantReferences", "require_descendant_references"),
            ("cleanup", "require_cleanup"), ("finalNonClaims", "require_final_non_claims"),
        ],
    }
    if stage in checks:
        for field, outcome in checks[stage]:
            if not p[field]:
                return outcome
        return {
            "requested": "accept_source_binding", "sourceBound": "accept_generation",
            "migrated": "accept_consumption", "consumed": "accept_closure",
        }[stage]
    if stage == "generated":
        if p["lossyRepresentation"] and p["exactClaim"]:
            return "block_lossy_exactness"
        for field, outcome in [
            ("verifierIdentity", "require_verifier_identity"),
            ("independentEvaluator", "require_independent_evaluator"),
            ("observedReconstruction", "require_observed_reconstruction"),
        ]:
            if not p[field]:
                return outcome
        if (p["exactClaim"] and not p["targetDigestMatches"]) or not p["verificationPassed"]:
            return "activate_fallback" if p["fallbackExecutable"] and p["fullSourcePreserved"] else "require_executable_fallback"
        if not p["verifierCostRecorded"]:
            return "require_verifier_cost"
        return "accept_verification"
    if stage == "verified":
        if not p["obligationScan"]:
            return "require_obligation_scan"
        if p["unresolvedObligations"] and not p["residualRecordPresent"]:
            return "require_residual_record"
        if p["unresolvedObligations"] and not p["residualOwner"]:
            return "require_residual_owner"
        if p["unresolvedObligations"] and not p["residualBurdenRecorded"]:
            return "require_residual_burden"
        if p["unresolvedObligations"] and p["declaredZeroResidual"]:
            return "block_zero_residual_overclaim"
        if not p["sourceProvenance"]:
            return "require_source_provenance"
        if not p["totalCostRecorded"]:
            return "require_total_cost"
        if s["fallbackCount"] > 0 and not p["fallbackReceipt"]:
            return "require_fallback_receipt"
        return "accept_residualization"
    if stage == "residualized":
        if not p["artifactReceipt"]:
            return "require_artifact_receipt"
        if not p["resultDigestsBound"]:
            return "require_bound_result_digests"
        if p["supportPromotionRequested"] and not p["evidenceTransitionPresent"]:
            return "require_evidence_transition"
        if not p["publicationNonClaims"]:
            return "require_publication_non_claims"
        return "accept_publication"
    if stage == "published":
        if p["semanticNodeUsed"] and not p["provenanceIdentity"]:
            return "require_provenance_identity"
        if p["semanticNodeUsed"] and not p["provenanceContent"]:
            return "require_provenance_content"
        if p["semanticNodeUsed"] and not p["groundingEvaluator"]:
            return "require_grounding_evaluator"
        if p["hierarchyChanged"] and not p["migrationRecord"]:
            return "require_migration_record"
        if p["hierarchyChanged"] and not (p["priorReferencesPreserved"] or p["supersessionRecorded"]):
            return "require_reference_continuity"
        if p["hierarchyChanged"] and not p["consumerMap"]:
            return "require_consumer_map"
        return "accept_migration"
    return "reject_wrong_stage"


def route_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    def add(case_id: str, stage_name: str, expected: str, mutate: dict[str, Any] | None = None, *, kind: str | None = None, fallback_count: int = 0, last: int = 0) -> None:
        p = packet()
        p["eventDigest"] = 91
        p.update(mutate or {})
        actual = route(stage_name, kind or KINDS[stage_name], p, state(stage_name, last=last, fallback_count=fallback_count))
        cases.append({"case_id": case_id, "stage": stage_name, "expected_route": expected, "actual_route": actual, "accepted": actual in ACCEPTED})

    add("wrong-stage", "requested", "reject_wrong_stage", kind="generate")
    add("representation-substitution", "requested", "reject_representation_substitution", {"sourceDigest": 999})
    add("consumer-substitution", "requested", "reject_consumer_substitution", {"consumerDigest": 999})
    add("result-substitution", "requested", "reject_result_digest_substitution", {"resultSetDigest": 999})
    add("event-replay", "requested", "reject_event_replay", last=91)
    add("authority-leak", "requested", "reject_authority_leak", {"externalEffectRequested": True})

    stage_fields = {
        "requested": [
            ("requestWellFormed", "reject_malformed_request"), ("sourceArtifactPresent", "require_source_artifact"),
            ("sourceDigestBound", "require_source_digest"), ("rightsBound", "require_rights"),
            ("versionedContract", "require_versioned_contract"), ("compressionBoundary", "require_compression_boundary"),
            ("consumerPolicy", "require_consumer_policy"),
        ],
        "sourceBound": [
            ("generatorPresent", "require_generator"), ("seedOrLawPresent", "require_seed_or_law"),
            ("searchBound", "require_search_bound"), ("generatedArtifactPresent", "require_generated_artifact"),
            ("generationCostRecorded", "require_generation_cost"),
        ],
        "migrated": [
            ("consumerAcknowledgment", "require_consumer_acknowledgment"), ("policyCompatible", "require_policy_compatibility"),
            ("downstreamEvaluation", "require_downstream_evaluation"), ("utilityMeasured", "require_utility_measurement"),
        ],
        "consumed": [
            ("residualClosedOrEscrowed", "require_residual_closure"), ("chainIntegrity", "require_chain_integrity"),
            ("descendantReferences", "require_descendant_references"), ("cleanup", "require_cleanup"),
            ("finalNonClaims", "require_final_non_claims"),
        ],
    }
    accepted_routes = {"requested": "accept_source_binding", "sourceBound": "accept_generation", "migrated": "accept_consumption", "consumed": "accept_closure"}
    for stage_name, pairs in stage_fields.items():
        for field, outcome in pairs:
            add(f"{stage_name}-{field}", stage_name, outcome, {field: False})
        add(f"{stage_name}-accepted", stage_name, accepted_routes[stage_name])

    for case_id, expected, mutation in [
        ("lossy-exact", "block_lossy_exactness", {"lossyRepresentation": True}),
        ("verifier-identity", "require_verifier_identity", {"verifierIdentity": False}),
        ("independent-evaluator", "require_independent_evaluator", {"independentEvaluator": False}),
        ("observed-reconstruction", "require_observed_reconstruction", {"observedReconstruction": False}),
        ("mismatch-fallback", "activate_fallback", {"targetDigestMatches": False}),
        ("mismatch-no-fallback", "require_executable_fallback", {"targetDigestMatches": False, "fallbackExecutable": False}),
        ("verifier-cost", "require_verifier_cost", {"verifierCostRecorded": False}),
        ("verification-accepted", "accept_verification", {}),
    ]:
        add(case_id, "generated", expected, mutation)

    for case_id, expected, mutation, fallback_count in [
        ("obligation-scan", "require_obligation_scan", {"obligationScan": False}, 0),
        ("residual-record", "require_residual_record", {"residualRecordPresent": False}, 0),
        ("residual-owner", "require_residual_owner", {"residualOwner": False}, 0),
        ("residual-burden", "require_residual_burden", {"residualBurdenRecorded": False}, 0),
        ("zero-residual-overclaim", "block_zero_residual_overclaim", {"declaredZeroResidual": True}, 0),
        ("source-provenance", "require_source_provenance", {"sourceProvenance": False}, 0),
        ("total-cost", "require_total_cost", {"totalCostRecorded": False}, 0),
        ("fallback-receipt", "require_fallback_receipt", {"fallbackReceipt": False}, 1),
        ("residualization-accepted", "accept_residualization", {}, 0),
    ]:
        add(case_id, "verified", expected, mutation, fallback_count=fallback_count)

    for case_id, expected, mutation in [
        ("artifact-receipt", "require_artifact_receipt", {"artifactReceipt": False}),
        ("bound-result-digests", "require_bound_result_digests", {"resultDigestsBound": False}),
        ("evidence-transition", "require_evidence_transition", {"supportPromotionRequested": True, "evidenceTransitionPresent": False}),
        ("publication-nonclaims", "require_publication_non_claims", {"publicationNonClaims": False}),
        ("publication-accepted", "accept_publication", {}),
    ]:
        add(case_id, "residualized", expected, mutation)

    for case_id, expected, mutation in [
        ("provenance-identity", "require_provenance_identity", {"provenanceIdentity": False}),
        ("provenance-content", "require_provenance_content", {"provenanceContent": False}),
        ("grounding-evaluator", "require_grounding_evaluator", {"groundingEvaluator": False}),
        ("migration-record", "require_migration_record", {"migrationRecord": False}),
        ("reference-continuity", "require_reference_continuity", {"priorReferencesPreserved": False, "supersessionRecorded": False}),
        ("consumer-map", "require_consumer_map", {"consumerMap": False}),
        ("migration-accepted", "accept_migration", {}),
    ]:
        add(case_id, "published", expected, mutation)
    return cases


def validate_source_results(errors: list[str]) -> dict[str, Any]:
    values = {name: load(path) for name, path in SOURCE_RESULTS.items()}
    gvr = values["compact_gvr"]
    conservation = values["residual_conservation"]
    trace = values["residual_trace"]
    storage = values["residual_storage"]
    checks = {
        "gvr_case_count": len(gvr.get("case_results", [])),
        "gvr_negative_control_count": len(gvr.get("negative_control_receipts", [])),
        "gvr_baseline_bytes": gvr.get("baseline_bytes"),
        "gvr_selected_bytes": gvr.get("selected_bytes"),
        "residual_valid_count": conservation.get("valid_case_count"),
        "residual_invalid_count": conservation.get("expected_invalid_control_count"),
        "trace_entry_count": trace.get("trace_entry_count"),
        "storage_entry_count": storage.get("valid_entry_count"),
        "storage_invalid_count": storage.get("expected_invalid_control_count"),
    }
    expected = {
        "gvr_case_count": 5, "gvr_negative_control_count": 3, "gvr_baseline_bytes": 368,
        "gvr_selected_bytes": 78, "residual_valid_count": 3, "residual_invalid_count": 5,
        "trace_entry_count": 4, "storage_entry_count": 4, "storage_invalid_count": 5,
    }
    for key, value in expected.items():
        if checks.get(key) != value:
            errors.append(f"source result {key} must be {value}, got {checks.get(key)!r}.")
    if storage.get("support_state_effect") != "none" or trace.get("support_state_effect") != "none":
        errors.append("residual trace/storage results must retain support_state_effect none.")
    return {
        "counts": checks,
        "sha256": {rel(path): sha256(path) for path in SOURCE_RESULTS.values()},
    }


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.returncode:
        raise RuntimeError(completed.stdout)
    return {"command": " ".join(command), "exit_code": 0, "output_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest()}


def build(errors: list[str]) -> dict[str, Any]:
    cases = route_cases()
    for case in cases:
        if case["actual_route"] != case["expected_route"]:
            errors.append(f"{case['case_id']}: expected {case['expected_route']}, got {case['actual_route']}.")
    reached = sorted({case["actual_route"] for case in cases})
    negative = [case for case in cases if not case["accepted"]]
    source = validate_source_results(errors)
    lean_text = LEAN.read_text(encoding="utf-8")
    declared = set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)", re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq", lean_text, re.S).group("body")))
    if len(declared) != 60:
        errors.append(f"Lean Route must declare 60 constructors, got {len(declared)}.")
    if len(reached) != 60:
        errors.append(f"independent consumer must reach 60 routes, got {len(reached)}.")
    return {
        "schema_version": "asi_stack.compact_generation_refinement.result.v1",
        "result_id": "2026-07-15-compact-generation-refinement",
        "recorded_date": "2026-07-15",
        "command": COMMAND,
        "model": {
            "lean_module": rel(LEAN), "stage_count": len(STAGES), "stages": STAGES,
            "route_count": len(declared), "independently_reached_route_count": len(reached),
            "rejected_mutation_count": len(negative), "route_case_count": len(cases),
            "fallback_route_reached": "activate_fallback" in reached,
            "support_assignment_count": 0, "external_effect_count": 0,
        },
        "source_result_refinement": source,
        "route_cases": cases,
        "verification": {
            "lean": run(["lake", "env", "lean", "AsiStackProofs/CompactGenerationRefinement.lean"], ROOT / "lean"),
            "result": "pass",
        },
        "support_state_effect": "none",
        "external_effect": "none",
        "residuals": [
            "The lifecycle is a finite authored policy model; it does not discover real obligations, prove codec correctness, or establish semantic grounding.",
            "The four source results are digest-bound and independently re-read, but remain synthetic/local bounded fixtures.",
            "Fallback is reachable in the model, not a deployed fallback service or recovery measurement.",
            "UtilityMeasured is an authored gate in this refinement, not evidence of useful compression or downstream utility.",
        ],
        "non_claims": [
            "no general compression, codec, semantic utility, grounding, safety, deployment, transfer, SOTA, AGI, or ASI claim",
            "no chapter-core support transition",
            "no inference from route coverage or green validation to empirical adequacy",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    result = build(errors)
    jsonschema.validate(result, load(SCHEMA))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
    elif not RESULT.exists() or RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is missing or stale; run {COMMAND} --write-result.")
    if errors:
        fail(errors)
    print(f"Compact generation refinement passed: {len(STAGES)} stages, {result['model']['route_count']} routes, {result['model']['rejected_mutation_count']}/{result['model']['rejected_mutation_count']} mutations rejected, four source results digest-bound, support/effect none.")


if __name__ == "__main__":
    main()
