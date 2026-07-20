#!/usr/bin/env python3
"""Register the terminal P6.4-A2 privacy-information-flow packet."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = "scripts/register_p6_4_a2_privacy_information_flow.py"
UNITS = [
  {"script": "validate_information_lifecycle_transaction.py", "artifacts": ["scripts/validate_information_lifecycle_transaction.py", "schemas/information_lifecycle_transaction.schema.json", "tests/fixtures/protocol_records/information_lifecycle_transaction.valid.json", "experiments/privacy_information_flow_argument_exit/preregistration.json", "lean/AsiStackProofs/PrivacyInformationFlow.lean", "lean/AsiStackProofs.lean", "chapters/privacy-data-rights-and-information-flow-governance.qmd"], "input_contract": "One synthetic no-personal-data information lifecycle record, twelve required surfaces, nine sources, ten non-authorities, and one unopened six-arm natural campaign.", "output_contract": "Require purpose/authority, minimization, complete-enough flow, derivatives, privacy evaluation, rights separation, residual ownership, and 26 rejecting mutations.", "output_assertions": ["12 surfaces", "9 sources", "10 non-authorities", "6 arms", "13 failure families", "15 competence gates", "26 mutations reject", "no privacy/compliance/support/release effect"], "claim_scope": "Authored information-lifecycle record shape and finite bounded-receipt semantics only.", "negative_controls": "validator_owned_twenty_six_party_purpose_authority_minimization_flow_derivative_privacy_attack_rights_residual_source_and_authority_mutations", "prohibited_inference": "No personal-data processing, privacy, lawful basis, compliance, attack absence, complete lineage, deletion, forgetting, influence removal, support, readiness, release, transfer, SOTA, AGI, or ASI follows."},
  {"script": "validate_p6_4_a2_privacy_information_flow_reader_integration.py", "artifacts": ["scripts/validate_p6_4_a2_privacy_information_flow_reader_integration.py", "evidence_quality/p6_4_a2_privacy_information_flow_reader_integration.json", "docs/p6_4_a2_privacy_data_rights_adjudication.md", "book_structure.json", "sources/source_inventory.json", "proofs/proof_manifest.json", "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json", "index.qmd", "appendices/B_glossary.qmd", "docs/book_outline.md", "chapters/security-kernel-and-digital-scifs.qmd", "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd"], "input_contract": "Terminal A2 decision, nine-source four-role packet, argument chapter, two targets, eleven theorems, authored contract, unopened campaign, and reconciled reader/status surfaces.", "output_contract": "Bind artifacts and source notes, require exclusive placement and handoffs, preserve proof/protocol denominators, advance exactly to A3, and reject ten integration mutations.", "output_assertions": ["1 terminal A2 chapter", "9 source notes", "4 source roles", "2 implemented targets", "11 theorems", "61 chapters", "A3 active", "10 integration mutations reject", "compliance/support effect none"], "claim_scope": "A2 chapter necessity, argument integration, artifact custody, and no-promotion boundary only.", "negative_controls": "validator_owned_ten_decision_source_manifest_proof_campaign_outcome_competence_status_and_compliance_mutations", "prohibited_inference": "Reader integration and finite artifacts do not establish privacy, rights completion, legal compliance, deletion, forgetting, influence removal, support, readiness, release, transfer, or SOTA."}
]

def dump(path, value): path.write_text(json.dumps(value, indent=2) + "\n")
def main():
    path = ROOT/"validation/registry.json"; registry = json.loads(path.read_text())
    scripts = {u["script"] for u in UNITS}; registry["units"] = [u for u in registry["units"] if u.get("script") not in scripts]
    order = len(registry["units"]) + 1
    for offset, spec in enumerate(UNITS):
        unit = {k:v for k,v in spec.items() if k != "artifacts"}; unit.update({"id": f"{spec['script']}:{order+offset}", "order": order+offset, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate", "contract_precision": "exact_record_denominator_and_semantic_disposition_contract", "input_artifacts": spec["artifacts"] + [REGISTER]}); registry["units"].append(unit)
    required = list(registry["required_artifacts"])
    for spec in UNITS:
        for artifact in spec["artifacts"] + [REGISTER]:
            if artifact not in required: required.append(artifact)
    registry["units"].sort(key=lambda u:u["order"]); registry["required_artifacts"] = required; registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}; dump(path, registry)
    print(f"Registered terminal P6.4-A2 packet: {len(registry['units'])} units, {len(required)} artifacts.")
if __name__ == "__main__": main()
