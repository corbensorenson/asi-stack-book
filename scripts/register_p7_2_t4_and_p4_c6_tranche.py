#!/usr/bin/env python3
"""Register and reconcile terminal P7.2-T4 and P4-C6 artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = "scripts/register_p7_2_t4_and_p4_c6_tranche.py"
CHAPTER_ID = "governed-operations-incident-command-and-graceful-degradation"
SOURCE_IDS = ["scf", "deterministic_capability_compilation", "theseus_operator_os", "viea", "talos", "platonic_world_model", "ext_nist_ai_rmf_1_0_2023", "ext_nist_deployed_ai_monitoring_2026", "ext_nist_incident_response_2025"]

UNITS = [
    {
        "script": "validate_governed_operations_control_contract.py",
        "artifacts": ["scripts/validate_governed_operations_control_contract.py", "schemas/governed_operations_control_packet.schema.json", "tests/fixtures/protocol_records/governed_operations_control_packet.valid.json", "experiments/governed_operations_argument_exit/preregistration.json", "lean/AsiStackProofs/GovernedOperations.lean", "lean/AsiStackProofs.lean", "chapters/governed-operations-incident-command-and-graceful-degradation.qmd"],
        "input_contract": "One authored identity-bound authority-to-effect control case, an eleven-class declared state inventory, a prospective unexecuted four-arm natural-service campaign, and a finite authority/recovery model.",
        "output_contract": "Require five-dimensional authority narrowing, independent containment, exact state/effect reconciliation, fresh independent acceptance, qualified fallback, emergency expiry, thirteen Lean declarations, one completed development positive control, and eighteen rejecting mutations.",
        "output_assertions": ["1 authored safe-hold case", "5 authority dimensions narrow", "11 state classes", "4 campaign arms", "9 competence gates", "13 Lean declarations", "18 mutations reject", "support/release/publication none"],
        "claim_scope": "Governed-operations packet shape and finite degradation/recovery route semantics only.",
        "negative_controls": "validator_owned_eighteen_identity_authority_containment_state_effect_acceptance_expiry_fallback_source_and_authority_mutations",
        "negative_control_cases": ["five authority widenings", "identity deletion", "command loss", "cooperation dependency", "state omission", "stale acceptance", "dependent verifier", "active emergency lease", "fallback loss", "support and release laundering"],
        "prohibited_inference": "The authored case and finite model do not establish natural incident behavior, detector quality, inventory completeness, effect reversal, fallback usefulness, recovery efficacy, safety, transfer, deployment, support, release, publication, AGI, or ASI.",
        "semantic_review_state": "checked_governed_operations_authority_effect_recovery_and_non_authority_semantics",
    },
    {
        "script": "validate_p7_2_t4_governed_operations_reader_integration.py",
        "artifacts": ["scripts/validate_p7_2_t4_governed_operations_reader_integration.py", "evidence_quality/p7_2_t4_governed_operations_reader_integration.json", "docs/p7_2_t4_governed_operations_reader_integration.md", "book_structure.json", "sources/source_inventory.json", "proofs/proof_manifest.json", "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json", "index.qmd", "appendices/B_glossary.qmd", "chapters/safety-cases-and-structured-assurance.qmd", "chapters/policy-optimization-and-learning-from-feedback.qmd", "chapters/integrated-reference-architecture.qmd"],
        "input_contract": "The admitted Operations chapter, nine exact source mappings, two implemented targets, one authored safe-hold case, one closed campaign, and adjacent reader surfaces.",
        "output_contract": "Bind exact artifact digests, preserve source/proof/campaign/flagship denominators, require reader handoffs and synthesis, close the four-chapter first tranche, advance to one second-tranche adjudication, and reject thirteen integration mutations.",
        "output_assertions": ["4 first-tranche chapters terminal", "9 source mappings", "2 implemented targets", "13 Lean declarations", "authored case not flagship T4", "0 natural incidents", "13 integration mutations reject", "support effect none"],
        "claim_scope": "P7.2-T4 chapter necessity, argument-level reader integration, finite traceability, and flagship separation only.",
        "negative_controls": "validator_owned_thirteen_terminal_source_digest_proof_incident_recovery_outcome_denominator_flagship_role_status_and_support_mutations",
        "negative_control_cases": ["terminal removal", "source deletion", "digest drift", "proof reduction", "incident invention", "recovery overclaim", "outcome opening", "denominator overlap", "flagship laundering", "status reopening", "support laundering"],
        "prohibited_inference": "Terminal reader integration does not establish operational efficacy, resilience, recovery, safety, NIST conformance, empirical support, release, publication, AGI, or ASI.",
        "semantic_review_state": "checked_terminal_governed_operations_argument_chapter_integration",
    },
    {
        "script": "validate_p4_c6_semantic_proof_cluster.py",
        "artifacts": ["scripts/validate_p4_c6_semantic_proof_cluster.py", "proofs/semantic_cluster_audits/resource_artifact_and_lifecycle_economics.json", "docs/p4_c6_resource_artifact_and_lifecycle_economics_semantic_audit.md", "lean/AsiStackProofs/ResourceEconomicsRefinement.lean", "lean/AsiStackProofs/ArtifactRealityRefinement.lean", "lean/AsiStackProofs/ArtifactStewardAgents.lean", "lean/AsiStackProofs/ArtifactCompressionRefinement.lean"],
        "input_contract": "The frozen four-module resource/artifact/steward/compression cluster with 31 public targets and 48 theorem declarations.",
        "output_contract": "Require propositions, state, assumptions, countermodels, consumers, mutation evidence, semantic separations, and ceilings; execute four consumers and reject twelve audit mutations.",
        "output_assertions": ["4 adequate modules", "31 public targets", "48 theorem declarations", "6 semantic separations", "4 consumers pass", "12 mutations reject", "all 6 P4 clusters terminal"],
        "claim_scope": "Bounded finite resource, artifact, steward, compression, reconciliation, fallback, and closure semantics only.",
        "negative_controls": "validator_owned_twelve_cluster_denominator_disposition_semantic_separation_status_and_support_mutations",
        "negative_control_cases": ["module deletion", "semantic-field erasure", "target inflation", "theorem inflation", "cost-efficiency merger", "stewardship-ownership merger", "status reopening", "support laundering"],
        "prohibited_inference": "The audit proves no efficiency, optimal allocation, artifact truth or durability, ownership, competent stewardship, useful compression, lifecycle success, deployment, transfer, support, release, or publication.",
        "semantic_review_state": "checked_terminal_resource_artifact_steward_and_compression_semantics",
    },
]


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    structure_path = ROOT / "book_structure.json"
    structure = json.loads(structure_path.read_text())
    for part in structure["parts"]:
        for chapter in part["chapters"]:
            if chapter["id"] == CHAPTER_ID:
                chapter["draft_maturity"] = "integrated_argument_chapter_formal_and_protocol_contract_complete"
                for target in chapter["proof_targets"]:
                    target["status"] = "implemented"
                if not any(test["name"] == "Governed operations control-contract suite" for test in chapter["codex_tests"]):
                    chapter["codex_tests"].insert(0, {"name": "Governed operations control-contract suite", "purpose": "Reject identity, authority-widening, containment, state, effect, freshness, verifier, expiry, fallback, source, and authority mutations against one authored safe-hold case and a completed development positive control.", "implementation_status": "implemented", "result_status": "18_of_18_semantic_mutations_rejected_support_effect_none"})
            elif chapter["id"] in {"governed-world-models-and-reality-grounding", "human-factors-and-meaningful-control-in-oversight"}:
                chapter["draft_maturity"] = "integrated_argument_chapter_formal_and_protocol_contract_complete"
    dump(structure_path, structure)

    sources_path = ROOT / "sources/source_inventory.json"
    sources = json.loads(sources_path.read_text())
    for source in sources:
        if source["id"] in SOURCE_IDS and CHAPTER_ID not in source.get("chapter_targets", []):
            source.setdefault("chapter_targets", []).append(CHAPTER_ID)
    dump(sources_path, sources)

    status_path = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
    status = json.loads(status_path.read_text())
    status["schema_version"] = "asi_stack.post_v2_3_maintenance_transfer_publication_status.v14"
    execution = status["execution_readiness"]
    execution["immediate_book_packet"] = "P6.4-A1-governed-model-training-distributed-optimization-and-scaling-adjudication"
    execution["immediate_formal_packet"] = "P4-terminal-no-open-formal-packet"
    status["quality_uplift_program"]["narrative_quality_gate"]["case_independent_compression_state"] = "first_tranche_terminal_second_tranche_a1_ready"
    first = status["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]
    first["state"] = "terminal_four_reader_chapters"
    first["completed_reader_chapter_count"] = 4
    first["terminal_reader_chapter_ids"] = execution["first_tranche_completion_order"]
    first["remaining_reader_chapter_ids"] = []
    status["semantic_proof_cluster_inventory"]["state"] = "all_6_clusters_terminal"
    status["semantic_proof_cluster_inventory"]["clusters"][-1]["state"] = "adequate"
    next(row for row in status["priorities"] if row["id"] == "P4")["state"] = "completed"
    next(row for row in status["milestones"] if row["id"] == "M4")["state"] = "completed"
    dump(status_path, status)

    schema_path = ROOT / "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json"
    schema = json.loads(schema_path.read_text())
    schema["properties"]["schema_version"]["const"] = status["schema_version"]
    ep = schema["properties"]["execution_readiness"]["properties"]
    ep["immediate_book_packet"]["const"] = execution["immediate_book_packet"]
    ep["immediate_formal_packet"]["const"] = execution["immediate_formal_packet"]
    narrative = schema["properties"]["quality_uplift_program"]["properties"]["narrative_quality_gate"]["properties"]
    narrative["case_independent_compression_state"]["const"] = "first_tranche_terminal_second_tranche_a1_ready"
    first_schema = schema["properties"]["quality_uplift_program"]["properties"]["structural_completeness_tranche"]["properties"]["first_tranche"]["properties"]
    first_schema["state"]["const"] = first["state"]
    first_schema["completed_reader_chapter_count"]["const"] = 4
    first_schema["terminal_reader_chapter_ids"]["const"] = first["terminal_reader_chapter_ids"]
    first_schema["remaining_reader_chapter_ids"]["const"] = []
    schema["properties"]["semantic_proof_cluster_inventory"]["properties"]["state"]["const"] = "all_6_clusters_terminal"
    schema["$defs"]["proofClusterEconomics"]["allOf"][1]["properties"]["state"]["const"] = "adequate"
    schema["$defs"]["inProgressP4"]["allOf"][1]["properties"]["state"]["const"] = "completed"
    schema["$defs"]["inProgressM4"]["allOf"][1]["properties"]["state"]["const"] = "completed"
    dump(schema_path, schema)

    audit_path = ROOT / "evidence_quality/p7_2_t4_governed_operations_reader_integration.json"
    audit = json.loads(audit_path.read_text())
    for owner, path_key, digest_key in ((audit, "chapter_path", "chapter_sha256"), (audit["formalization"], "module_path", "module_sha256"), (audit["record_contract"], "schema_path", "schema_sha256"), (audit["record_contract"], "fixture_path", "fixture_sha256"), (audit["claim_bearing_empirical_lane"], "protocol_path", "protocol_sha256")):
        owner[digest_key] = digest(owner[path_key])
    dump(audit_path, audit)

    registry_path = ROOT / "validation/registry.json"
    registry = json.loads(registry_path.read_text())
    scripts = {row["script"] for row in UNITS}
    registry["units"] = [row for row in registry["units"] if row.get("script") not in scripts]
    next_order = len(registry["units"]) + 1
    for offset, spec in enumerate(UNITS):
        unit = {key: value for key, value in spec.items() if key != "artifacts"}
        unit.update({"id": f"{spec['script']}:{next_order + offset}", "order": next_order + offset, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate", "contract_precision": "exact_record_denominator_and_semantic_disposition_contract", "input_artifacts": spec["artifacts"] + [REGISTER]})
        registry["units"].append(unit)
    required = list(registry["required_artifacts"])
    for spec in UNITS:
        for artifact in spec["artifacts"] + [REGISTER]:
            if artifact not in required: required.append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["required_artifacts"] = required
    registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
    dump(registry_path, registry)
    print(f"Registered terminal P7.2-T4/P4-C6 tranche: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
