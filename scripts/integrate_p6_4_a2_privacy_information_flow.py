#!/usr/bin/env python3
"""Idempotently admit and reconcile the terminal P6.4-A2 reader packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "privacy-data-rights-and-information-flow-governance"
NEXT_ID = "perception-sensor-fusion-and-observation-trust"
NEXT_PACKET = f"P6.4-A3-{NEXT_ID}-adjudication"
SOURCE_IDS = [
    "ext_nist_privacy_framework_2020", "ext_eu_gdpr_2016", "ext_w3c_dpv_2024",
    "ext_abadi_dpsgd_2016", "ext_algospec_purpose_limitation_2024",
    "ext_carlini_training_data_extraction_2021", "ext_choquette_choo_label_only_mia_2021",
    "ext_nist_differential_privacy_2025", "ext_mahloujifar_fdp_audit_2025",
]
LOCAL_SOURCE_IDS = ["theseus_synthetic_data_curation"]


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def mapping(source_id: str, support: str, limits: str) -> dict:
    return {"source_id": source_id, "mapped_support": support, "limits": limits,
            "passage_refs": [f"sources/source_notes/{source_id}.md"],
            "passage_review_note": "Reviewed the primary paper, specification, official guidance, or authoritative legal text at the bounded passages recorded in the source note; no source-reported result or legal requirement is treated as local evidence or a compliance finding.",
            "passage_review_state": "reviewed"}


def local_mapping(source_id: str, support: str, limits: str) -> dict:
    return {"source_id": source_id, "mapped_support": support, "limits": limits,
            "passage_refs": [f"sources/source_notes/{source_id}.md"],
            "passage_review_note": "Reviewed the pinned local-project documentation and its source-reported policy boundaries. No Theseus command, dataset, model, privacy mechanism, rights workflow, or outcome was rerun or imported into this chapter.",
            "passage_review_state": "reviewed"}


NEW_SOURCES = [
    {"id": "ext_nist_privacy_framework_2020", "title": "NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management, Version 1.0", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID, "security-kernel-and-digital-scifs"], "url": "https://doi.org/10.6028/NIST.CSWP.01162020", "notes": "Official paper-body-reviewed risk framework distinguishing privacy problems from cybersecurity incidents across the data lifecycle. It is voluntary, has no force of law, and supplies no local privacy outcome or certification.", "source_type": "government_framework", "published": "2020-01-16", "updated": "2024-01-22", "citation_label": "NIST (2020), Privacy Framework 1.0", "doi": "10.6028/NIST.CSWP.01162020"},
    {"id": "ext_eu_gdpr_2016", "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID], "url": "https://eur-lex.europa.eu/eli/reg/2016/679", "notes": "Authoritative jurisdiction-specific normative comparator for principles, bases, rights, accountability, design, and qualified exceptions. It is not universal law, legal advice, an applicability decision, or local compliance evidence.", "source_type": "law_primary", "published": "2016-04-27", "updated": "2016-05-04", "citation_label": "European Parliament and Council (2016), Regulation (EU) 2016/679"},
    {"id": "ext_w3c_dpv_2024", "title": "Data Privacy Vocabulary (DPV), Version 2", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID, "context-transactions-snapshots-mounts-and-taint"], "url": "https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-20240801/", "notes": "Machine-readable vocabulary for purpose, processing, data, actors, rights, risks, measures, legal basis, and consent. It is a Community Group Final Specification, not a W3C Recommendation, law, or enforcement proof.", "source_type": "community_specification", "published": "2024-08-01", "updated": "2024-08-01", "citation_label": "W3C Data Privacy Vocabularies and Controls CG (2024), DPV v2"},
    {"id": "ext_abadi_dpsgd_2016", "title": "Deep Learning with Differential Privacy", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID, "governed-model-training-distributed-optimization-and-scaling"], "url": "https://arxiv.org/abs/1607.00133", "notes": "Primary DP-SGD mechanism and accounting source. Its algorithm, analysis, and reported experiments are not locally reproduced; its guarantee is parameter-, unit-, adjacency-, implementation-, and release-surface-bound.", "source_type": "conference_paper", "arxiv_id": "1607.00133", "published": "2016-07-01", "updated": "2016-10-24", "citation_label": "Abadi et al. (2016), Deep Learning with Differential Privacy", "doi": "10.1145/2976749.2978318"},
    {"id": "ext_algospec_purpose_limitation_2024", "title": "Being Transparent Is Merely the Beginning: Enforcing Purpose Limitation with Polynomial Approximation", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID], "url": "https://www.usenix.org/conference/usenixsecurity24/presentation/liu-shuofeng", "notes": "Primary competing purpose-restriction design using algorithm-specific polynomial approximation. Reported accuracy and efficiency are bounded to studied algorithms/data and are not locally reproduced or a complete legal-purpose result.", "source_type": "conference_paper", "published": "2024-08", "updated": "2024-08", "citation_label": "Liu et al. (2024), Being Transparent Is Merely the Beginning"},
    {"id": "ext_carlini_training_data_extraction_2021", "title": "Extracting Training Data from Large Language Models", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID, "data-engines-continual-learning-and-unlearning"], "url": "https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting", "notes": "Primary failure source reporting black-box extraction of memorized GPT-2 training sequences. The source result is configuration-bound and not a local or universal leakage result.", "source_type": "conference_paper", "published": "2021-08", "updated": "2021-08", "citation_label": "Carlini et al. (2021), Extracting Training Data from Large Language Models"},
    {"id": "ext_choquette_choo_label_only_mia_2021", "title": "Label-Only Membership Inference Attacks", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID], "url": "https://proceedings.mlr.press/v139/choquette-choo21a.html", "notes": "Primary failure source showing hard-label robustness can expose membership and confidence masking can be insufficient in studied settings. No attack or defense result is locally reproduced or universal.", "source_type": "conference_paper", "published": "2021-07", "updated": "2021-07", "citation_label": "Choquette-Choo et al. (2021), Label-Only Membership Inference Attacks"},
    {"id": "ext_mahloujifar_fdp_audit_2025", "title": "Auditing f-Differential Privacy in One Run", "priority": "external_literature", "layer": "privacy_data_rights_and_information_flow_governance", "chapter_targets": [CHAPTER_ID, "benchmark-ratchets-and-anti-goodhart-evidence"], "url": "https://proceedings.mlr.press/v267/mahloujifar25a.html", "notes": "Primary empirical-audit comparator using randomized inclusion and an f-DP hypothesis in one run. A passed audit is not proof that DP or lifecycle privacy holds, and no result is locally reproduced.", "source_type": "conference_paper", "published": "2025-07", "updated": "2025-07", "citation_label": "Mahloujifar, Melis, and Chaudhuri (2025), Auditing f-Differential Privacy in One Run"},
]

CHAPTER = {
    "id": CHAPTER_ID, "title": "Privacy, Data Rights, and Information-Flow Governance", "file": f"chapters/{CHAPTER_ID}.qmd",
    "status": "conceptual", "evidence_level": "argument", "claim_label": "Design rationale", "source_ids": SOURCE_IDS + LOCAL_SOURCE_IDS,
    "source_queue": {"primary": SOURCE_IDS, "supporting": LOCAL_SOURCE_IDS, "variants": [], "connector_or_recovery": [], "handoff_or_recovery_notes": ["Receives authorized access, datum lineage, and context identity; returns purpose-bounded use and rights receipts plus explicit unknown-copy, influence, exception, privacy, and remedy residuals without legal-compliance, support, readiness, or release authority."]},
    "problem": "A system can preserve confidentiality and pass access checks while authorized collection, linkage, inference, memory, training, sharing, retention, or derivatives violate purpose, minimization, privacy expectations, or executable rights.",
    "insufficient": "Access control, consent text, a DP label, a low observed attack rate, one deleted row, a changed answer, or a closed rights ticket cannot establish purpose compatibility, privacy, complete propagation, legal compliance, or total forgetting.",
    "core_claim": "An information use is eligible for bounded execution only when a prospectively declared record binds affected parties, exact purpose and processing, claimed authority and jurisdiction, recipients, retention, minimization, complete-enough flow and derivatives, cross-user boundaries, privacy unit, adjacency, accountant and budget where applicable, threat model and attack plan, rights state and remedy, exceptions, residual copies and influence, costs, and non-authorities; no individual control or receipt alone establishes privacy, legal compliance, total erasure, behavioral forgetting, influence removal, support, readiness, release, transfer, or SOTA.",
    "claim_source_mappings": [
        mapping(SOURCE_IDS[0], "Grounds lifecycle privacy-risk governance and the distinction between privacy and cybersecurity risk.", "Voluntary framework; not law, certification, or local outcome."),
        mapping(SOURCE_IDS[1], "Grounds one jurisdiction's purpose, minimization, accountability, design, rights, and qualified exceptions vocabulary.", "No universalization, applicability decision, legal advice, or compliance finding."),
        mapping(SOURCE_IDS[2], "Grounds machine-readable purpose, processing, actor, rights, risk, measure, and consent records.", "Community Group specification; representation does not prove validity or enforcement."),
        mapping(SOURCE_IDS[3], "Grounds DP-SGD clipping, noise, sampling, accounting, and utility tradeoffs.", "Not reproduced; guarantee remains assumption-, implementation-, and release-bound."),
        mapping(SOURCE_IDS[4], "Grounds algorithm-specific purpose restriction as a competing design.", "Reported task envelope is narrow and not reproduced or complete purpose governance."),
        mapping(SOURCE_IDS[5], "Grounds training-data extraction as a concrete model-mediated privacy failure.", "GPT-2-specific source evidence is not a universal or local leakage result."),
        mapping(SOURCE_IDS[6], "Grounds label-only membership inference and confidence-masking failure.", "Studied interfaces and defenses are configuration-bound and not reproduced."),
        mapping(SOURCE_IDS[7], "Grounds layered evaluation of DP mathematical, implementation, system, and operational claims.", "Guidance does not prove any local DP implementation or legal compliance."),
        mapping(SOURCE_IDS[8], "Grounds one-run empirical f-DP auditing as a flaw detector and measurement comparator.", "A non-violation is not certification and the result is not reproduced."),
        local_mapping(LOCAL_SOURCE_IDS[0], "Supplies source-reported implementation pressure for provenance receipts, leakage gates, split exclusions, bounded synthetic-data admission, descendant propagation, and revocation or unlearning questions.", "No Theseus command or dataset was rerun; the record establishes no privacy, rights completion, deletion, influence removal, data quality, model benefit, or compliance outcome."),
    ],
    "mechanism": ["Name subjects, affected groups, and unknown-identity routes.", "Bind exact purpose, operation, claimed authority, jurisdiction, recipients, retention, expiry, and objection state.", "Test a less-data alternative and admit only necessary fields and granularity.", "Map context, memory, training, inference, output, audit, sharing, cache, backup, checkpoint, and derivative flows while retaining unknowns.", "Declare privacy unit, adjacency, threat model, mechanism, accountant, budget, and attacks.", "Require positive-control and independent attack evaluation before interpreting null leakage.", "Execute access, correction, export, restriction, deletion, or ordinary-use receipts across known descendants.", "Close storage, access, behavior, influence, privacy, exceptions, and legal authority separately."],
    "interfaces": ["authorized access", "data-subject and affected-group record", "purpose and authority lease", "minimization decision", "flow and derivative graph", "privacy-loss and attack audit", "rights request", "bounded receipt", "residual and remedy escrow"],
    "invariants": ["access is not consent or purpose", "purpose and authority precede use", "less-data alternatives are tested", "unknown copies remain visible", "derivatives inherit obligations", "cross-user memory is isolated", "privacy unit and adjacency travel with a guarantee", "formal accounting and empirical auditing remain distinct", "attack positive controls precede null interpretation", "storage behavior influence privacy and legal outcomes remain separate", "a rights receipt confers no support or release authority"],
    "failure_modes": ["purpose drift", "consent laundering", "minimization theater", "cross-user leakage", "linkage and attribute inference", "training-data extraction", "membership inference", "privacy-accounting drift", "rights-ticket theater", "deletion-forgetting substitution", "audit surveillance", "group blind spot", "exception laundering", "compliance theater"],
    "minimal_implementation": "Build a synthetic lifecycle transaction and then a prospectively frozen natural small-model/memory campaign comparing ordinary, access-only, minimization, DP, purpose-bound, and competent remediation arms under strong positive-controlled attacks, complete descendant rights workflows, at least three seeds, independent evaluation, and joint utility/privacy/rights/cost outcomes.",
    "beyond_state_of_art": "The mature operational contract carries machine-readable purpose, authority, privacy, rights, and remedy obligations across context, memory, heterogeneous model substrates, training, inference, audit, backups, releases, and descendants; composes formal accounting with competent empirical attacks and independently checked outcome measures; preserves contestable lineage and effect-complete remediation across replacements; and supports versioned cross-jurisdictional policy modules without pretending the architecture determines law, legal validity, institutional legitimacy, or universal privacy.",
    "codex_tests": [{"name": "Information lifecycle transaction contract", "purpose": "Check purpose/authority, minimization, twelve-surface flow closure, derivative propagation, privacy evaluation, rights receipts, sources, non-authorities, and 26 rejecting mutations.", "implementation_status": "implemented", "result_status": "authored_record_only_no_privacy_or_compliance_effect"}, {"name": "Natural privacy and rights campaign", "purpose": "Compare six strong arms across thirteen failure families, hidden independent evaluation, positive controls, and joint utility/privacy/rights/cost outcomes.", "implementation_status": "planned", "result_status": "prospectively_frozen_unexecuted"}],
    "lean_module": "AsiStackProofs.PrivacyInformationFlow",
    "proof_targets": [{"tag": "lean:privacy_information_flow.admission_invariants", "module": "AsiStackProofs.PrivacyInformationFlow", "target": "An accepted finite information use requires matching purpose and authority, minimization, complete-enough flow, and competent privacy evaluation.", "status": "implemented"}, {"tag": "lean:privacy_information_flow.outcome_separation", "module": "AsiStackProofs.PrivacyInformationFlow", "target": "An accepted bounded receipt preserves storage, behavior, influence, privacy, and legal-compliance separation and refuses authority laundering.", "status": "implemented"}],
    "draft_maturity": "integrated_argument_chapter_formal_and_protocol_contract_complete",
    "open_evidence_gaps": ["No ASI Stack privacy/data-rights campaign has run.", "No source mechanism, attack, legal determination, or rights workflow was reproduced locally.", "The fixture and finite Lean model establish record consequences only."],
}

TRIAGE = [
    {"tag": "lean:privacy_information_flow.admission_invariants", "chapter_id": CHAPTER_ID, "module": "AsiStackProofs.PrivacyInformationFlow", "formal_target": "An accepted finite information use requires matching purpose and authority, minimization, complete-enough flow, and competent privacy evaluation.", "target_status": "implemented", "triage": "formal-invariant", "recommended_route": "lean-candidate", "rationale": "Finite authored route implication only; it trusts purpose, authority, flow, minimization, privacy-unit, attack-competence, and denominator predicates and proves no real privacy, right, or legal fact."},
    {"tag": "lean:privacy_information_flow.outcome_separation", "chapter_id": CHAPTER_ID, "module": "AsiStackProofs.PrivacyInformationFlow", "formal_target": "An accepted bounded receipt preserves storage, behavior, influence, privacy, and legal-compliance separation and refuses authority laundering.", "target_status": "implemented", "triage": "formal-invariant", "recommended_route": "lean-candidate", "rationale": "Finite authored separation theorem only; it cannot establish deletion, forgetting, influence removal, privacy, compliance, support, readiness, or release."},
]


def insert_once(path: str, anchor: str, addition: str, *, after: bool = True) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if addition.strip() in text:
        return
    if anchor not in text:
        raise SystemExit(f"Missing anchor in {path}: {anchor[:80]}")
    text = text.replace(anchor, anchor + addition if after else addition + anchor, 1)
    target.write_text(text, encoding="utf-8")


def main() -> None:
    inventory_path = ROOT / "sources/source_inventory.json"
    inventory = json.loads(inventory_path.read_text())
    by_id = {row["id"]: row for row in inventory}
    for source in NEW_SOURCES: by_id[source["id"]] = source
    existing = [row["id"] for row in inventory]
    inventory = [by_id[source_id] for source_id in existing]
    inventory.extend(source for source in NEW_SOURCES if source["id"] not in existing)
    for row in inventory:
        if row["id"] == "ext_nist_differential_privacy_2025":
            row["chapter_targets"] = sorted(set(row.get("chapter_targets", [])) | {CHAPTER_ID})
            row["notes"] = "Paper-body-reviewed official guidance distinguishing mathematical, implementation, system, and operational layers of a DP claim. It establishes no correct local implementation, utility result, lifecycle privacy, or legal compliance."
        if row["id"] in LOCAL_SOURCE_IDS:
            row["chapter_targets"] = sorted(set(row.get("chapter_targets", [])) | {CHAPTER_ID})
    dump(inventory_path, inventory)

    structure_path = ROOT / "book_structure.json"
    structure = json.loads(structure_path.read_text())
    for part in structure["parts"]:
        part["chapters"] = [c for c in part["chapters"] if c["id"] != CHAPTER_ID]
    part = next(p for p in structure["parts"] if any(c["id"] == "security-kernel-and-digital-scifs" for c in p["chapters"]))
    index = next(i for i,c in enumerate(part["chapters"]) if c["id"] == "security-kernel-and-digital-scifs") + 1
    part["chapters"].insert(index, CHAPTER)
    dump(structure_path, structure)

    triage_path = ROOT / "proofs/proof_triage.json"
    triage = json.loads(triage_path.read_text())
    replacements = {row["tag"]: row for row in TRIAGE}
    triage["records"] = [replacements.pop(row["tag"], row) for row in triage["records"]]
    triage["records"].extend(replacements.values())
    triage["record_count"] = len(triage["records"])
    dump(triage_path, triage)

    decision_path = ROOT / "claim_decisions/v1_0_core_claim_no_promotion.json"
    decisions = json.loads(decision_path.read_text())
    decision = {
        "claim_id": f"{CHAPTER_ID}.core", "chapter_id": CHAPTER_ID,
        "chapter_title": "Privacy, Data Rights, and Information-Flow Governance",
        "decision": "no_promotion", "current_support_state": "argument",
        "support_state_effect": "argument_only",
        "decision_reason": "The chapter has a source-reviewed argument packet, authored lifecycle record, rejecting mutations, finite proofs, and an unopened campaign, but no personal-data processing, natural privacy mechanism, attack, rights workflow, legal determination, independent reproduction, or transfer has been accepted for its broad claim.",
        "required_evidence": ["competent natural six-arm campaign with positive-controlled extraction and membership attacks", "complete derivative rights workflow with separate storage behavioral influence privacy and legal outcomes", "independent reproduction and transfer within the exact threat model privacy unit mechanism and jurisdictional nonclaim envelope"],
        "blockers": ["natural campaign unexecuted", "no local privacy mechanism or strong attack result", "no legal applicability or compliance determination", "no independent reproduction or transfer"],
        "non_claims": ["does not establish valid consent lawful basis or legal compliance", "does not establish a privacy guarantee attack absence complete lineage total erasure forgetting or influence removal", "does not establish support readiness release transfer AGI ASI or SOTA"],
        "refs": [f"chapters/{CHAPTER_ID}.qmd", f"appendices/C_claim_evidence_matrix.qmd#{CHAPTER_ID}.core"]
    }
    by_chapter = {row["chapter_id"]: row for row in decisions["decisions"]}
    by_chapter[CHAPTER_ID] = decision
    order = [row["chapter_id"] for row in decisions["decisions"]]
    decisions["decisions"] = [by_chapter[c] for c in order]
    if CHAPTER_ID not in order: decisions["decisions"].append(decision)
    dump(decision_path, decisions)

    status_path = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
    status = json.loads(status_path.read_text())
    status["schema_version"] = "asi_stack.post_v2_3_maintenance_transfer_publication_status.v16"
    status["execution_readiness"]["immediate_book_packet"] = NEXT_PACKET
    tranche = status["quality_uplift_program"]["structural_completeness_tranche"]
    tranche["state"] = "first_tranche_terminal_second_tranche_a1_a2_terminal"
    tranche["current_manifest_chapter_count"] = 61
    second = tranche["second_tranche"]
    second["state"] = "a1_a2_terminal_eleven_manifest_gated"
    second["manifest_admitted_count"] = 2
    second["primary_source_record_count_added"] = 31
    second["adjudicated_candidate_ids"] = ["governed-model-training-distributed-optimization-and-scaling", CHAPTER_ID]
    second["terminal_candidate_dispositions"][CHAPTER_ID] = "admitted_terminal_argument_reader_chapter"
    second["active_candidate_id"] = NEXT_ID
    second["remaining_candidate_ids"] = [c for c in second["candidate_ids"] if c not in second["adjudicated_candidate_ids"]]
    second["a2_decision_packet"] = "docs/p6_4_a2_privacy_data_rights_adjudication.md"
    status["quality_uplift_program"]["narrative_quality_gate"]["case_independent_compression_state"] = "first_tranche_terminal_second_tranche_a1_a2_terminal_a3_ready"
    status["activation_truth"].update({"live_working_chapter_count": 61, "chapter_core_argument_count": 61, "proof_target_count": 310, "lean_module_count": 104, "theorem_declaration_count": 1370, "derived_or_decomposed_theorem_count": 924, "direct_or_projection_theorem_count": 230, "unknown_or_mixed_theorem_count": 216})
    status["negative_result_rehabilitation"].update({"current_surface_count": 81, "live_chapter_surface_count": 61})
    dump(status_path, status)

    schema_path = ROOT / "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json"
    schema = json.loads(schema_path.read_text())
    schema["properties"]["schema_version"]["const"] = status["schema_version"]
    schema["properties"]["execution_readiness"]["properties"]["immediate_book_packet"]["const"] = NEXT_PACKET
    q = schema["properties"]["quality_uplift_program"]["properties"]
    q["narrative_quality_gate"]["properties"]["case_independent_compression_state"]["const"] = status["quality_uplift_program"]["narrative_quality_gate"]["case_independent_compression_state"]
    tranche_schema = q["structural_completeness_tranche"]
    tranche_schema["properties"]["state"]["const"] = tranche["state"]
    tranche_schema["properties"]["current_manifest_chapter_count"]["const"] = 61
    second_schema = tranche_schema["properties"]["second_tranche"]
    for key in ("adjudicated_candidate_ids", "terminal_candidate_dispositions", "active_candidate_id", "remaining_candidate_ids", "a1_decision_packet", "a2_decision_packet"):
        if key not in second_schema["required"]: second_schema["required"].append(key)
        second_schema["properties"][key] = {"const": second[key]}
    second_schema["properties"]["state"]["const"] = second["state"]
    second_schema["properties"]["manifest_admitted_count"]["const"] = 2
    second_schema["properties"]["primary_source_record_count_added"]["const"] = 31
    activation = schema["properties"]["activation_truth"]["properties"]
    for key in ("live_working_chapter_count", "chapter_core_argument_count", "proof_target_count", "lean_module_count", "theorem_declaration_count", "unknown_or_mixed_theorem_count"):
        activation[key]["const"] = status["activation_truth"][key]
    rehab = schema["properties"]["negative_result_rehabilitation"]["properties"]
    rehab["current_surface_count"]["const"] = 81
    rehab["live_chapter_surface_count"]["const"] = 61
    dump(schema_path, schema)

    # Reader and roadmap reconciliation. These are bounded insertions, not generated files.
    insert_once("index.qmd", "  Improve --> Authority\n", "  Authority --> Privacy[\"Purpose-bounded information use and data rights\"]\n  Privacy -. \"rights, privacy, and residual constraints\" .-> Memory\n")
    insert_once("appendices/B_glossary.qmd", "| Training Run Transaction | A prospectively frozen, identity-bound record joining architecture, data order, objective, optimizer, numerical and topology policy, execution failures, full checkpoint state, resume evidence, checkpoint-family selection, and independent qualification handoff. | `governed-model-training-distributed-optimization-and-scaling` | owned training-integrity interface definition; no model-quality authority |\n", "| Information Lifecycle Transaction | A purpose- and authority-bounded record joining affected parties, minimization, flow and derivative lineage, privacy evaluation, rights execution, residual copies and influence, and a bounded non-compliance receipt. | `privacy-data-rights-and-information-flow-governance` | owned privacy/data-rights interface; no legal-compliance authority |\n| Purpose Lease | A scoped, expiring statement of the exact information use, claimed authority, jurisdiction, recipients, retention, and compatibility rule. | `privacy-data-rights-and-information-flow-governance` | does not prove that the purpose is lawful |\n")
    insert_once("chapters/security-kernel-and-digital-scifs.qmd", "## Handoff\n", "Privacy, Data Rights, and Information-Flow Governance takes the next boundary:\nauthenticated and authorized access does not by itself permit every collection,\ninference, linkage, retention, training, sharing, or derivative use. It receives\nsecurity identity and policy receipts, then returns purpose, minimization,\nprivacy-evaluation, rights, and remedy residuals without altering Security\nKernel authority.\n\n", after=False)
    insert_once("chapters/model-weight-custody-and-hardware-roots-of-trust.qmd", "## Problem\n", "This chapter receives model-family artifacts already constrained by Privacy, Data Rights, and Information-Flow Governance. Custody cannot erase purpose leases, privacy budgets, subject rights, descendant obligations, deletion residuals, or unresolved influence merely by transferring a weight artifact.\n\n", after=False)

    roadmap = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
    text = roadmap.read_text(encoding="utf-8")
    text = text.replace("| Book slot — now | `P6.4-A2-privacy-data-rights-and-information-flow-governance-adjudication` | P6.4-A1 is terminal; privacy/data-rights is next in the frozen dependency order | Adjudicate exactly one proposed owner through admission, narrowing, return-to-owner, or rejection. Freeze the information-lifecycle transaction, four source roles, owner boundary, competence burden, reader value, and non-claims before any manifest insertion. |", f"| Book slot — now | `{NEXT_PACKET}` | P6.4-A1 and A2 are terminal; perception/observation trust is next in dependency order | Adjudicate exactly one proposed owner through admission, narrowing, return-to-owner, or rejection. Freeze the observation-admission transaction, four source roles, owner boundary, competence burden, reader value, and non-claims before any manifest insertion. |")
    text = text.replace("| Second structural tranche — now | `governed-model-training-distributed-optimization-and-scaling` is terminal at argument support; adjudicate `privacy-data-rights-and-information-flow-governance` next, then one candidate at a time |", "| Second structural tranche — now | Governed Model Training and Privacy/Data Rights are terminal at argument support; adjudicate `perception-sensor-fusion-and-observation-trust` next, then one candidate at a time |")
    text = text.replace("P6.4-A1 has since survived adjudication and is terminal\nas the 60th argument-level chapter; the remaining twelve are", "P6.4-A1 and P6.4-A2 have survived adjudication and are terminal\nas the 60th and 61st argument-level chapters; the remaining eleven are")
    marker = "2. `perception-sensor-fusion-and-observation-trust` owns how time-bound,"
    privacy_item = "4. `privacy-data-rights-and-information-flow-governance` owns purpose, consent,\n   minimization, privacy loss, subject and group rights, derivative obligations,\n   correction, export, deletion, and remedy across the information lifecycle."
    if "**Terminal — admitted at argument support.** `privacy-data-rights" not in text:
        text = text.replace(privacy_item, "4. **Terminal — admitted at argument support.** `privacy-data-rights-and-information-flow-governance` owns purpose, consent, minimization, privacy loss, subject and affected-group records, derivative obligations, correction, export, deletion, and bounded remedy receipts across the information lifecycle. Its decision packet is `docs/p6_4_a2_privacy_data_rights_adjudication.md`; no empirical, legal-compliance, support, release, or publication effect follows.")
    roadmap.write_text(text, encoding="utf-8")

    audit_path = ROOT / "evidence_quality/p6_4_a2_privacy_information_flow_reader_integration.json"
    if audit_path.is_file():
        audit = json.loads(audit_path.read_text())
        audit["artifact_sha256"] = {relative: sha(relative) for relative in audit["artifacts"].values()}
        audit["source_note_sha256"] = {source_id: sha(f"sources/source_notes/{source_id}.md") for source_id in SOURCE_IDS}
        audit["local_source_note_sha256"] = {source_id: sha(f"sources/source_notes/{source_id}.md") for source_id in LOCAL_SOURCE_IDS}
        dump(audit_path, audit)

    print(f"Integrated terminal P6.4-A2: {sum(len(p['chapters']) for p in structure['parts'])} chapters, {len(inventory)} sources; next packet {NEXT_PACKET}.")


if __name__ == "__main__":
    main()
