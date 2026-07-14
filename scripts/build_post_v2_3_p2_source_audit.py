#!/usr/bin/env python3
"""Build the post-v2.3 P2 source and completeness disposition artifacts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "evidence_quality/post_v2_3_source_and_completeness_residuals.json"
OUT_MD = ROOT / "docs/post_v2_3_external_anchoring_and_completeness_audit.md"
READER_ROOT = ROOT / "editions/reader_manuscript/v2_1"


TEN = [
    ("scalable-oversight-and-adversarial-ai-control", "A scoped oversight protocol may inform a bounded decision only when access, capability envelopes, baseline, outcome audit, correlation, residuals, and accountable escalation are explicit.", "ext_scalable_oversight_weak_llms_2024", "Monitorability under adversarial pressure and capability scaling was weakly treated.", "insert", ["ext_monitorbench_2026"]),
    ("model-weight-custody-and-hardware-roots-of-trust", "Weight custody binds identity, lineage, encryption, key release, attestation, authorized environment, release scope, revocation, and irreversible disclosure.", "ext_rand_model_weight_security_2024", "NIST COSAiS control overlays are current but still discussion-draft material and do not beat the assigned custody comparators.", "watch", []),
    ("ai-supply-chain-integrity-and-lifecycle-provenance", "A versioned AI supply-chain graph binds model, data, code, build/training, signer, supplier, advisory, derivative, release, revocation, and disposal state.", "ext_slsa_build_track_1_2", "NIST COSAiS and SP 1326 add current overlay/due-diligence framing but no stronger finalized mechanism than the existing SLSA, in-toto, SPDX AI, Croissant, signing, and C-SCRM set.", "already_covered", []),
    ("open-ended-improvement-engines", "Open-ended generation remains a bounded campaign whose artifacts cannot widen authority or enter live capability fields without independent qualification.", "ext_darwin_godel_machine_2025", "Newer discovery systems were screened, but none changes the existing POET, Voyager, FunSearch, ADAS, and Darwin-Godel boundary enough to justify another citation.", "already_covered", []),
    ("inter-stack-protocols-identity-and-economic-exchange", "Cross-stack dispatch requires versioned protocol, identity, delegated authority, credential, audience, expiry, budget, receipt, dispute, revocation, and residual records.", "ext_mcp_protocol_2025_11_25", "No omitted current protocol changes the existing MCP, A2A, DID, VC, Interledger, and agentic-security division of responsibility.", "already_covered", []),
    ("governed-deliberation-and-test-time-scaling", "Extra inference is a bounded campaign with verifier, budget, stop, candidate, cost, residual, and handoff records; it does not create correctness or authority.", "ext_test_time_compute_scaling_2024", "Causal faithfulness of the visible reasoning trace was only a prose caution, not an owned evaluation gate.", "insert", ["ext_faithfulness_information_flow_2026"]),
    ("capability-thresholds-and-deployment-commitments", "Capability thresholds are versioned commitments with domain, threat, elicitation/access, uncertainty, safeguards, exceptions, residuals, and release effects.", "ext_metr_time_horizons_2025", "Current frontier policies and Inspect already cover the strongest operational neighbor; broader policy catalogs would add count rather than a new decision boundary.", "already_covered", []),
    ("adversarial-evaluation-sandbagging-and-training-time-deception", "Evaluation observations are context-bound evidence whose monitor, reward, selection, cross-context, and interference conditions must remain visible.", "ext_alignment_faking_2024", "Trace/action causal inconsistency and multi-task monitorability stress testing were missing as explicit evidence-design surfaces.", "insert", ["ext_faithfulness_information_flow_2026", "ext_monitorbench_2026"]),
    ("safety-cases-and-structured-assurance", "A safety case is a versioned graph of claims, strategies, evidence, assumptions, defeaters, hazards, context, acceptance criteria, authority, and residual ownership.", "ext_aisi_safety_cases_2024", "No current primary neighbor materially improves the existing GSN, AISI, and scheming-evaluation safety-case boundary without duplicating the chapter.", "already_covered", []),
    ("data-engines-continual-learning-and-unlearning", "Learning inputs and all update/deletion state remain versioned, provenance-bound artifacts with separate admission, quarantine, retention, replay, deletion, and promotion authority.", "ext_openunlearning_2025", "Predictive encoders and action-conditioned world-model predictors added a distinct data/version/error lineage not owned by the existing unlearning sources.", "insert", ["ext_v_jepa_2_2025"]),
]


TIER2 = [
    (1, "Output content provenance", "artifact-graphs-audit-logs-and-replay", "defer", "Internal provenance is mature, but no passage-reviewed primary C2PA/watermarking comparator was accepted in this bounded pass; retain as an event-driven source intake."),
    (2, "Interpretability as runtime control", "evidence-states-and-claim-discipline", "narrow", "Interpretability remains evidence with bounded steering implications; the 2026 steering candidates were not passage-reviewed deeply enough to become runtime-control claims."),
    (3, "Memory consolidation lifecycle", "procedural-memory-and-cognitive-loop-closure", "already_covered", "Consolidation, replay, proceduralization, and forgetting budgets already have owners and source-noted boundaries."),
    (4, "Calibration selective prediction and abstention", "claim-ledgers-and-belief-revision", "already_covered", "Calibration, abstention, uncertainty, and reject routes are already explicit across Claim Ledgers, Readiness, Routing, and Verification Bandwidth."),
    (5, "Metacognition and capability self-knowledge", "readiness-gates-residual-escrow-and-quarantine", "defer", "The capability self-model remains an event-driven intake; current self-assessment mentions do not warrant a new unreviewed source claim."),
    (6, "Collusion between components against oversight", "scalable-oversight-and-adversarial-ai-control", "already_covered", "Shared dependencies, coordinated failure, role separation, and randomized or independent observation routes are already owned."),
    (7, "Oversight latency and fleet-scale monitoring", "scalable-oversight-and-adversarial-ai-control", "defer", "Governance cost and latency are measured, but fleet-scale windows need a passage-reviewed deployment comparator before insertion."),
    (8, "Control tax as governance-tax comparator", "resource-economics-and-token-budgets", "already_covered", "The local governance-tax lane and its zero-denominator boundary are explicit; a new citation is unnecessary until a matched natural-work outcome exists."),
    (9, "Automated AI R&D acceleration thresholds", "capability-thresholds-and-deployment-commitments", "already_covered", "CAIS R&D automation and threshold commitments are already positioned; no new metric is claimed."),
    (10, "STPA-style systematic hazard analysis", "safety-cases-and-structured-assurance", "watch", "STPA is named as an open hazard-analysis route, but the candidate source was not accepted at passage depth in this pass."),
    (11, "Autonomous insider", "security-kernel-and-digital-scifs", "defer", "Agent-as-insider remains a valid security expansion but lacks a newly reviewed primary comparator and executable owner packet."),
    (12, "Hardware attestation trust-root class", "model-weight-custody-and-hardware-roots-of-trust", "already_covered", "TEE quotes, roots, verifier chains, stale evidence, and custody boundaries are central to the current chapter."),
    (13, "Open-weight release decision record", "model-weight-custody-and-hardware-roots-of-trust", "already_covered", "Irreversible public release, disclosure scope, key release, revocation limits, and publication authority are already explicit."),
    (14, "Public governance graphs for market collusion", "inter-stack-protocols-identity-and-economic-exchange", "defer", "Economic receipts are covered, but market-collusion governance graphs need a passage-reviewed primary source and systemic-risk owner."),
    (15, "Guaranteed-safe AI positioning", "executable-specifications-and-lean-proof-envelope", "defer", "The record/spec versus model-safety boundary is already explicit; GSA positioning awaits paper-depth intake rather than relying on the older scan."),
    (16, "Machine unlearning and parametric deletion closure", "data-engines-continual-learning-and-unlearning", "already_covered", "Full-state update, checkpoint authority, behavioral/influence/privacy/storage partitioning, and multiple primary unlearning comparators are present."),
    (17, "Prompt-injection impossibility as strongest objection", "security-kernel-and-digital-scifs", "already_covered", "Prompt-injection limits, architectural separation, AgentDojo, CAMEL, OWASP, and fail-closed external authority are already treated."),
    (18, "Scheming-oriented safety cases", "safety-cases-and-structured-assurance", "already_covered", "The evaluations-based scheming safety-case source and defeater/countercase structure are already assigned and used."),
    (19, "Non-agentic Scientist AI position", "asi-is-a-stack-not-a-model", "defer", "The zero-execution-authority route is expressible, but Scientist AI needs primary passage review before a named position is added."),
    (20, "CAIS prior-art mandate", "asi-is-a-stack-not-a-model", "already_covered", "CAIS is passage-reviewed in the opener, alignment, RSI, and reference architecture with a narrow typed-governance delta."),
    (21, "Behavior-specification practice crosswalk", "constitutional-alignment-substrate", "defer", "Constitutional predicates are mature, but the three-style and deliberative-alignment comparison remains a future passage-reviewed intake."),
    (22, "Formal-mathematics agents", "circle-calculus-and-proof-carrying-ai-contracts", "defer", "Proof producer/consumer interfaces exist; AlphaProof or another current capability comparator needs a separate primary-source pass."),
    (23, "ARC-style program synthesis and test-time training", "cognitive-compilation-and-semantic-ir", "already_covered", "Program synthesis, semantic IR, verifier-guided search, and test-time adaptation already have explicit owners."),
    (24, "Compute governance and distributed-training tension", "personal-compute-hives-and-federated-edge-intelligence", "defer", "Federated compute governance/evasion dual remains a valid missing comparator but was not passage-reviewed in this bounded pass."),
    (25, "Introspection-training evidence", "readiness-gates-residual-escrow-and-quarantine", "defer", "This duplicates the metacognition intake and remains deferred to one joint source-specific review."),
    (26, "Goal continuity under inherited trajectory pressure", "human-intent-as-a-formal-input", "already_covered", "Objective fingerprints, periodic recontracting, drift, and inherited trajectory pressure are already explicit."),
    (27, "Causal and counterfactual reasoning", "planning-as-a-control-layer", "narrow", "V-JEPA 2 adds predictive-state and MPC ownership while the text explicitly refuses to infer causal/interventional understanding; a causal-model source remains open."),
    (28, "Distribution shift OOD detection and runtime uncertainty", "readiness-gates-residual-escrow-and-quarantine", "already_covered", "OOD, distribution shift, calibration, abstention, fallback, and quarantine are distributed across their current owners."),
    (29, "Temporal-logic monitoring and physical safety envelopes", "runtime-adapters-tool-permissions-and-human-approval", "narrow", "Bounded runtime monitoring is source-noted, but physical closed-loop safety envelopes remain outside the digital-adapter evidence scope."),
    (30, "Human-AI delegation calibration", "scalable-oversight-and-adversarial-ai-control", "defer", "Weak-supervisor and escalation boundaries are present; rejector/router calibration needs its primary source pass."),
    (31, "Evaluator-access levels and environment custody", "adversarial-evaluation-sandbagging-and-training-time-deception", "already_covered", "Access, monitor visibility, evaluator provenance, model information, budgets, and false-negative residuals are explicit."),
    (32, "Domain-specific dangerous-capability profiles", "capability-thresholds-and-deployment-commitments", "already_covered", "Thresholds are domain- and threat-specific and explicitly prohibit cross-domain generalization."),
    (33, "Post-deployment monitoring and incident disclosure", "safety-cases-and-structured-assurance", "defer", "Safety-case invalidation exists, but an end-to-end operational-resilience/incident owner remains outside the current 54-chapter spine."),
    (34, "AIBOM lineage and signed build attestations", "ai-supply-chain-integrity-and-lifecycle-provenance", "already_covered", "Component inventory, model/data/build/training lineage, signing, attestations, derivatives, advisories, rebuild, and revocation are current core mechanisms."),
    (35, "Purpose limitation privacy budgets and internal-channel leakage", "data-engines-continual-learning-and-unlearning", "defer", "Privacy evidence is partitioned for unlearning, but subject-rights and multi-user internal-channel governance still lack a dedicated owner/source packet."),
    (36, "Unlearning privacy paradox", "data-engines-continual-learning-and-unlearning", "narrow", "MUSE and the benchmark critiques keep privacy separate from behavior; the specific before/after leakage source remains unreviewed."),
    (37, "Provider concentration substitutability and impact tolerances", "resource-economics-and-token-budgets", "defer", "Exit and fallback exist as general controls, but provider-concentration and resilience claims need a current primary-source owner packet."),
]


SOURCE_DECISIONS = [
    {"source_id": "ext_faithfulness_information_flow_2026", "decision": "insert", "reason": "Changes the trace/action evidence design and authoritative-receipt boundary.", "passage_review": "Abstract; Sections 1, 3, 4, 6.3, and Limitations reviewed."},
    {"source_id": "ext_monitorbench_2026", "decision": "insert", "reason": "Adds a distinct multi-task adversarial monitorability benchmark design.", "passage_review": "Abstract, introduction, design, stress tests, results, and limitations reviewed."},
    {"source_id": "ext_v_jepa_2_2025", "decision": "insert", "reason": "Adds a concrete predictive-state and MPC interface plus explicit adoption residuals.", "passage_review": "Abstract, architecture, planning, results, and limitations reviewed."},
    {"source_id": "ext_embedded_agency_2019", "decision": "insert", "reason": "Adds the missing foundations boundary between finite records and an embedded agent/world.", "passage_review": "Primary abstract and canonical authors' full-text sections reviewed."},
    {"source_id": "watch_nist_cosais_2026", "decision": "watch", "url": "https://csrc.nist.gov/Projects/cosais", "reason": "Official 2026 control-overlay work remains a discussion draft and is redundant with stronger finalized custody/supply-chain comparators."},
    {"source_id": "watch_nist_sp_1326_2026", "decision": "already_covered", "url": "https://csrc.nist.gov/pubs/sp/1326/final", "reason": "Due-diligence and provenance framing does not change the existing C-SCRM/SLSA/in-toto/SPDX/Croissant mechanism."},
    {"source_id": "watch_preliminary_jepa_neighbors_2026", "decision": "reject", "reason": "Preliminary JEPA/energy-based neighbors do not beat V-JEPA 2 as the mature empirical interface comparator for this pass."},
]


PATTERNS = {
    1: r"C2PA|content provenance|watermark", 2: r"interpretability|activation steering|SAE", 3: r"consolidation|sleep|episodic.*semantic", 4: r"calibration|selective prediction|abstention", 5: r"metacognition|self-knowledge|self-assessment", 6: r"collusion|randomized monitor", 7: r"oversight latency|fleet-scale|fleet monitoring", 8: r"control tax|governance tax", 9: r"automated AI R&D|acceleration share|R&D automation", 10: r"STPA|hazard analysis", 11: r"autonomous insider|insider threat", 12: r"hardware attestation|TEE|trust root", 13: r"open.weight|open weight", 14: r"governance graph|market collusion", 15: r"guaranteed.safe|GSA|Safeguarded AI", 16: r"parametric.*unlearn|machine unlearning|deletion closure", 17: r"prompt.injection|instruction.*data", 18: r"scheming.*safety case|evaluations.based safety", 19: r"Scientist AI|non.agentic", 20: r"CAIS|Comprehensive AI Services", 21: r"behavior specification|deliberative alignment|Model Spec", 22: r"formal.mathematics|AlphaProof|math agents", 23: r"ARC.style|ARC Prize|program synthesis|test.time adaptation", 24: r"compute governance|distributed training|DiLoCo", 25: r"introspection training|introspection", 26: r"inherited goal drift|objective fingerprint|recontract", 27: r"causal|counterfactual|interventional", 28: r"distribution shift|OOD|out.of.distribution", 29: r"temporal.logic|safety envelope|interlock", 30: r"delegation calibration|rejector|router calibration", 31: r"evaluator.access|black.box|grey.box|white.box", 32: r"dangerous.capability|biological|critical.infrastructure", 33: r"post.deployment monitoring|incident disclosure|field telemetry", 34: r"AIBOM|bill of materials|component inventory|build attestation", 35: r"purpose limitation|privacy budget|internal.channel", 36: r"unlearning privacy|membership.*unlearn|privacy leakage", 37: r"provider concentration|substitutability|impact tolerance",
}


def read_json(path: Path):
    return json.loads(path.read_text())


def prose_used_ids(path: Path) -> list[str]:
    return sorted(set(re.findall(r"\bext_[a-z0-9_]+\b", path.read_text())))


def text_hits(pattern: str) -> list[str]:
    rx = re.compile(pattern, re.I)
    hits = []
    for path in sorted((ROOT / "chapters").glob("*.qmd")):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if rx.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{number}")
                if len(hits) >= 12:
                    return hits
    return hits


def build() -> dict:
    structure = read_json(ROOT / "book_structure.json")
    chapters = {c["id"]: c for p in structure["parts"] for c in p["chapters"]}
    inventory = {r["id"]: r for r in read_json(ROOT / "sources/source_inventory.json")}
    ten_rows = []
    for cid, claim, strongest, neighbor, disposition, additions in TEN:
        chapter = chapters[cid]
        mappings = {m["source_id"]: m for m in chapter["claim_source_mappings"]}
        ten_rows.append({
            "chapter_id": cid,
            "distinct_claim": claim,
            "strongest_primary_comparator": strongest,
            "assigned_external_source_ids": [x for x in chapter["source_ids"] if x.startswith("ext_")],
            "prose_used_external_source_ids": prose_used_ids(ROOT / chapter["file"]),
            "passage_reviews": {sid: mappings[sid]["passage_refs"] for sid in additions if sid in mappings},
            "strongest_omitted_or_weak_neighbor": neighbor,
            "value_test": "accepted additions change a boundary, objection, mechanism, or evidence design; all other candidates are terminally dispositioned without count padding",
            "disposition": disposition,
            "accepted_source_ids": additions,
            "permitted_changes": [chapter["file"], f"editions/reader_manuscript/v2_1/chapters/{cid}.qmd", "sources/source_inventory.json", "appendices/A_source_matrix.qmd", "appendices/C_claim_evidence_matrix.qmd", "appendices/H_external_sources.qmd", "docs/book_outline.md"] if additions else ["audit/disposition records only; no prose or manifest mutation"],
            "support_state_effect": "none",
        })
    tier_rows = []
    for number, title, owner, disposition, rationale in TIER2:
        tier_rows.append({"id": f"T2-{number:02d}", "title": title, "owner_chapter_id": owner, "disposition": disposition, "rationale": rationale, "current_text_refs": text_hits(PATTERNS[number]), "active_queue": disposition in {"defer", "watch", "narrow"}, "support_state_effect": "none"})
    return {
        "schema_version": "asi_stack.post_v2_3_source_completeness_audit.v1",
        "snapshot_date": "2026-07-14",
        "roadmap": "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md#p2--selective-external-anchoring-and-completeness-residuals",
        "status": "completed",
        "active_chapter_count": len(chapters),
        "source_count": len(inventory),
        "ten_chapter_audit": ten_rows,
        "source_decisions": SOURCE_DECISIONS,
        "crosscuts": {
            "reasoning_trace_faithfulness": {"disposition": "insert", "source_ids": ["ext_faithfulness_information_flow_2026", "ext_monitorbench_2026"], "owners": ["artifact-graphs-audit-logs-and-replay", "adversarial-evaluation-sandbagging-and-training-time-deception", "governed-deliberation-and-test-time-scaling", "policy-optimization-and-learning-from-feedback", "scalable-oversight-and-adversarial-ai-control"]},
            "world_models_jepa_energy_based": {"disposition": "insert_existing_owners", "source_ids": ["ext_v_jepa_2_2025"], "owners": ["mathematical-and-search-substrates", "planning-as-a-control-layer", "data-engines-continual-learning-and-unlearning", "integrated-reference-architecture"]},
            "foundations": {"disposition": "insert_and_reconcile", "source_ids": ["ext_embedded_agency_2019", "ext_drexler_cais_2019", "ext_corrigibility_2015", "ext_off_switch_game_2016", "ext_goodhart_variants_2018"], "owners": ["asi-is-a-stack-not-a-model", "constitutional-alignment-substrate", "recursive-self-improvement-boundaries", "evidence-states-and-claim-discipline", "integrated-reference-architecture"]},
        },
        "ownership_test": {"new_chapter_warranted": False, "decision": "keep_54_chapter_spine", "interface_test": "reasoning traces, predictive state, and embedded-agent limits already have unambiguous consumer/owner interfaces", "invariant_test": "each residual strengthens an existing invariant rather than creating a non-duplicative new one", "artifact_test": "trace records, substrate adoption records, plan/world-model records, evidence cells, and reference traces already own the needed artifacts", "failure_mode_test": "new chapters would duplicate trace/action mismatch, prediction error, sim-to-real, self-reference, and record-completeness failures", "evidence_program_test": "existing chapter validators and future campaign lanes can host the tests", "manifest_effect": "none"},
        "tier_2_disposition_audit": tier_rows,
        "reader_reconciliation": {"edition_id": "asi-stack-curated-reader-v2.1", "path": "editions/reader_manuscript/v2_1", "relationship": "successor source edition; immutable v1.0 and v2.0 not modified", "chapter_count": 54, "status": "reconciled_source_only", "format_effect": "none"},
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": ["Source insertion does not reproduce a paper result.", "Citation count is not a completion metric.", "No chapter-core claim moves above argument.", "No new chapter is admitted.", "The v2.1 reader source is not a released format artifact.", "No model quality, monitorability, causal world model, corrigibility, safety, AGI, or ASI result is established."],
    }


def render_md(data: dict) -> str:
    out = ["# Post-v2.3 External Anchoring and Completeness Audit", "", "Status: **completed** on 2026-07-14. This is a source and prose reconciliation, not an evidence promotion or release.", "", "## Decision", "", "Four passage-reviewed primary sources changed a boundary or evidence design. No new chapter passed the ownership test; the 54-chapter spine remains intact. Immutable reader v1.0 and v2.0 remain unchanged, while accepted prose is carried by source-only reader successor v2.1.", "", "## Ten-chapter audit", "", "| Chapter | Strongest comparator | Weak neighbor | Disposition | Accepted source(s) |", "|---|---|---|---|---|"]
    for row in data["ten_chapter_audit"]:
        out.append(f"| `{row['chapter_id']}` | `{row['strongest_primary_comparator']}` | {row['strongest_omitted_or_weak_neighbor']} | `{row['disposition']}` | {', '.join(f'`{x}`' for x in row['accepted_source_ids']) or 'none'} |")
    out += ["", "## Accepted and screened sources", "", "| Source | Decision | Reason |", "|---|---|---|"]
    for row in data["source_decisions"]:
        out.append(f"| `{row['source_id']}` | `{row['decision']}` | {row['reason']} |")
    out += ["", "## Cross-cutting ownership", "", "- Reasoning-trace faithfulness is owned by Artifact Graphs, Governed Deliberation, Adversarial Evaluation, Policy Optimization, and Scalable Oversight. Private reasoning, reported rationale, action trace, receipt, monitorability evidence, and authoritative effect remain separate.", "- V-JEPA and latent world-model material is owned by Mathematical/Search Substrates, Planning, Data Engines, and the Integrated Reference Architecture. Structural prediction, benchmark quality, causal understanding, controller quality, and sim-to-real transfer remain separate.", "- Embedded agency joins the already-reviewed CAIS, corrigibility, off-switch, and Goodhart foundations family. Finite record proofs do not become whole-agent or open-world guarantees.", "", "## New-chapter ownership test", "", "Decision: `keep_54_chapter_spine`. Existing owners already provide the distinct interfaces, invariants, artifacts, failure modes, and evidence lanes; a new chapter would duplicate them.", "", "## Tier-2 audit", "", "| ID | Finding | Owner | Disposition | Current refs |", "|---|---|---|---|---:|"]
    for row in data["tier_2_disposition_audit"]:
        out.append(f"| `{row['id']}` | {row['title']} | `{row['owner_chapter_id']}` | `{row['disposition']}` | {len(row['current_text_refs'])} |")
    out += ["", "Only `defer`, `watch`, and `narrow` rows remain in the event-driven queue. `Already_covered` rows are not copied into a new roadmap, and deferred rows are not silently cited from search-result-depth material.", "", "## Evidence boundary", "", "All 54 core claims remain at `argument`. The audit does not reproduce any external result, approve a reader format, change public release v2.3.0, require external-human prepublication review, or establish model quality, monitorability, causal world modeling, corrigibility, safety, AGI, or ASI.", ""]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.write:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        OUT_MD.write_text(render_md(data))
    print(f"P2 audit {'wrote' if args.write else 'planned'}: {len(data['ten_chapter_audit'])} chapters, {len(data['tier_2_disposition_audit'])} Tier-2 rows, {len(data['source_decisions'])} source decisions.")


if __name__ == "__main__":
    main()
