#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SEQUENCE = ROOT / "docs" / "chapter_consolidation_sequence.md"
COMPRESSION_DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_compression.md"
COMPRESSION_DESTINATION_DRAFT = ROOT / "docs" / "chapter_consolidation_destination_draft_compression.md"
INTENT_DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_intent_contracts.md"
INTENT_DESTINATION_DRAFT = ROOT / "docs" / "chapter_consolidation_destination_draft_intent_contracts.md"
CONTEXT_ABI_DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_context_abi.md"
CONTEXT_ABI_DESTINATION_DRAFT = ROOT / "docs" / "chapter_consolidation_destination_draft_context_abi.md"
VERIFICATION_REVIEW_DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_verification_review.md"
VERIFICATION_REVIEW_DESTINATION_DRAFT = ROOT / "docs" / "chapter_consolidation_destination_draft_verification_review.md"
PLANNING_DAG_DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_planning_dag.md"
PLANNING_DAG_DESTINATION_DRAFT = ROOT / "docs" / "chapter_consolidation_destination_draft_planning_dag.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
REPOSITORY_MAP = ROOT / "docs" / "repository_map.md"
STRUCTURE = ROOT / "book_structure.json"

REQUIRED_IDS = {
    "constitutional-alignment-substrate",
    "agency-dignity-and-corrigibility",
    "moral-uncertainty-and-value-conflict",
    "governance-rights-fork-exit-and-audit",
    "compact-generative-systems-and-residual-honesty",
    "generate-verify-repair-compression",
    "rankfold-neuralfold-and-artifact-compression",
    "intent-to-execution-contracts",
    "command-contracts-and-semantic-interfaces",
    "human-intent-as-a-formal-input",
    "virtual-context-abi",
    "semantic-pages-context-cells-and-certificates",
    "context-transactions-snapshots-mounts-and-taint",
    "verification-bandwidth-and-context-adequacy",
    "spinoza-verification-and-proof-carrying-claims",
    "unified-adaptive-tribunal-and-adversarial-review",
    "claim-ledgers-and-belief-revision",
    "planning-as-a-control-layer",
    "planforge-dags-and-intelligence-arbitrage",
    "cognitive-compilation-and-semantic-ir",
    "moecot-runtime-and-multi-core-orchestration",
    "routing-heads-and-specialist-cores",
    "simulation-fidelity-and-physical-constraints",
    "resource-economics-and-token-budgets",
    "semantic-representation-and-tree-structured-models",
    "labor-os-and-typed-jobs",
    "runtime-adapters-tool-permissions-and-human-approval",
    "artifact-graphs-audit-logs-and-replay",
    "procedural-memory-and-cognitive-loop-closure",
    "recursive-self-improvement-boundaries",
    "circle-calculus-and-proof-carrying-ai-contracts",
    "coil-attention-cyclic-memory-and-recurrence-contracts",
    "coilra-multicoil-rope-and-cyclic-mixers",
    "mathematical-and-search-substrates",
    "project-theseus-as-report-first-implementation-reference",
    "executable-specifications-and-lean-proof-envelope",
    "living-book-methodology",
}

REQUIRED_FRAGMENTS = (
    "planning and release-control artifact, not source evidence",
    "not a manifest edit",
    "not a support-state transition",
    "54 manifest chapters",
    "Do not run a broad 54-to-44 manifest edit",
    "Do not target a fixed chapter count.",
    "Do not delete ideas merely to reduce repetition.",
    "Do not promote any chapter core claim above `argument`",
    "Follow-Up Review Outcome",
    "Consolidation State Model",
    "`planned_candidate`",
    "`fold_review_candidate`",
    "`dry_run_packaged`",
    "`review_ready`",
    "`executed`",
    "`deferred_for_release`",
    "`rejected_or_retained`",
    "Current Pilot Status",
    "The current decision is still deferral",
    "Chapter-Ownership Rubric",
    "A chapter is chapter-owning when it owns a distinct artifact",
    "A chapter is a consolidation candidate when most of its reader-visible load",
    "A merge is justified only if the destination draft reduces repeated skeleton",
    "A merge is rejected or deferred when the proposed destination loses a useful",
    "Current Cluster Register",
    "Compression and residual honesty | `review_ready`",
    "Intent and executable contracts | `review_ready`",
    "Static context ABI | `review_ready`",
    "Verification and adversarial review | `review_ready`",
    "Planning and DAG control | `review_ready`",
    "Candidate Sequence",
    "Protected Standalone Chapters",
    "Required Package Before Any Non-Pilot Merge",
    "Chapter-ownership rubric result",
    "Repetition-removal ledger",
    "Reader-work disposition",
    "Reader Work Sequencing",
    "This sequence does not merge chapters.",
    "This sequence does not change `book_structure.json`.",
    "This sequence does not change Appendix C support states.",
)

COMPRESSION_DRAFT_REQUIRED_FRAGMENTS = (
    "Consolidation Destination Draft: Compact Generative Systems, Generate, Verify, Repair, and Residual Honesty",
    "Status: review-ready draft; human/external review not completed.",
    "does not edit `book_structure.json`",
    "Destination continuity ID: `compact-generative-systems-and-residual-honesty`",
    "Proposed displayed title: **Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty**",
    "Preservation Ledger",
    "Destination Chapter Draft",
    "Chapter status",
    "Drafting guardrail",
    "Human Reading Path",
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Codex test plan",
    "Formalization hooks",
    "Source crosswalk",
    "Review Decision Surface",
    "Execute conservative merge",
    "No chapter core claim is promoted above `argument`",
    "This draft does not merge chapters.",
    "This draft does not change Appendix C support states.",
)

COMPRESSION_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation Dry Run: Compact Generative Systems",
    "does not edit `book_structure.json`",
    "Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty",
    "Conservative option",
    "Proposed `book_structure.json` Diff",
    "Destination Section Outline",
    "Appendix C Row Plan",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Reader Path, Handoff, And Review Repairs",
    "No support state changes",
    "No new result is created by this dry run",
)

COMPRESSION_REQUIRED_IDS = {
    "compact-generative-systems-and-residual-honesty",
    "generate-verify-repair-compression",
    "rankfold-neuralfold-and-artifact-compression",
    "semantic-representation-and-tree-structured-models",
}

COMPRESSION_REQUIRED_SOURCE_IDS = {
    "cgs",
    "rgs",
    "bugbrain",
    "simulation_scaling",
    "rmi",
    "project_theseus_whitepaper",
    "bbvca_v9",
    "bbvca_main",
    "rankfold_neuralfold",
    "rankfold_compressor",
}

COMPRESSION_REQUIRED_EXTERNAL_IDS = {
    "ext_deep_compression_2015",
    "ext_dreamcoder_2020",
    "ext_information_bottleneck_2000",
    "ext_knowledge_distillation_2015",
    "ext_mdl_tutorial_2004",
    "ext_codebleu_2020",
    "ext_gptq_2022",
    "ext_lora_2021",
    "ext_qlora_2023",
}

COMPRESSION_REQUIRED_LEAN_TAGS = {
    "lean:compression.cgs.operational_invariant",
    "lean:compression.cgs.failure_blocks_promotion",
    "lean:compression.gvr.operational_invariant",
    "lean:compression.gvr.failure_blocks_promotion",
    "lean:compression.artifacts.operational_invariant",
    "lean:compression.artifacts.failure_blocks_promotion",
}

INTENT_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation Dry Run: Intent And Executable Contracts",
    "does not edit `book_structure.json`",
    "Command Contracts: From Intent to Executable Work",
    "human-intent-as-a-formal-input",
    "Proposed `book_structure.json` Diff",
    "Destination Section Outline",
    "Appendix C Row Plan",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Tests, Schemas, And Fixtures",
    "Reader Path, Handoff, And Review Repairs",
    "No support state changes",
    "No new result is created by this dry run",
)

INTENT_DRAFT_REQUIRED_FRAGMENTS = (
    "Consolidation Destination Draft: Command Contracts From Intent To Executable Work",
    "Status: review-ready draft; human/external review not completed.",
    "does not edit `book_structure.json`",
    "Destination continuity ID: `intent-to-execution-contracts`",
    "Proposed displayed title: **Command Contracts: From Intent to Executable Work**",
    "Preservation Ledger",
    "Destination Chapter Draft",
    "Chapter status",
    "Drafting guardrail",
    "Human Reading Path",
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Codex test plan",
    "Formalization hooks",
    "Source crosswalk",
    "Review Decision Surface",
    "No chapter core claim is promoted above `argument`",
    "This draft does not merge chapters.",
    "This draft does not change Appendix C support states.",
)

INTENT_REQUIRED_IDS = {
    "intent-to-execution-contracts",
    "command-contracts-and-semantic-interfaces",
    "human-intent-as-a-formal-input",
    "planning-as-a-control-layer",
}

INTENT_REQUIRED_SOURCE_IDS = {
    "viea",
    "talos",
    "software_magic_grimoire",
    "genesiscode",
    "moecot",
    "cognitive_compilation",
}

INTENT_REQUIRED_EXTERNAL_IDS = {
    "ext_react_2022",
    "ext_dafny_2010",
    "ext_goal_oriented_requirements_engineering_2001",
    "ext_cooperative_inverse_rl_2016",
    "ext_deep_rl_human_preferences_2017",
}

INTENT_REQUIRED_LEAN_TAGS = {
    "lean:intent_execution.contracts.operational_invariant",
    "lean:intent_execution.contracts.failure_blocks_promotion",
    "lean:command.semantic_interface.operational_invariant",
    "lean:command.semantic_interface.failure_blocks_promotion",
}

INTENT_REQUIRED_FIXTURE_FRAGMENTS = {
    "schemas/intent_contract.schema.json",
    "schemas/command_contract.schema.json",
    "schemas/intent_execution_trace.schema.json",
    "experiments/plan_execution_contracts/fixtures/valid_dispatchable_linear_plan.json",
    "experiments/plan_execution_contracts/fixtures/valid_blocked_authority_plan.json",
    "experiments/plan_execution_contracts/fixtures/invalid_dispatch_without_receipt.json",
    "experiments/plan_execution_contracts/fixtures/invalid_approval_bypass.json",
    "experiments/plan_execution_contracts/fixtures/invalid_requirement_lost.json",
    "experiments/plan_execution_contracts/fixtures/invalid_contract_mismatch.json",
    "experiments/plan_execution_contracts/fixtures/invalid_cycle_in_dag.json",
    "python3 scripts/validate_plan_execution_contracts.py",
}

CONTEXT_ABI_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation Dry Run: Static Context ABI",
    "does not edit `book_structure.json`",
    "The Virtual Context ABI: Typed Pages, Cells, and Certificates",
    "context-transactions-snapshots-mounts-and-taint",
    "verification-bandwidth-and-context-adequacy",
    "claim-ledgers-and-belief-revision",
    "Proposed `book_structure.json` Diff",
    "Destination Section Outline",
    "Appendix C Row Plan",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Tests, Schemas, And Fixtures",
    "Reader Path, Handoff, And Review Repairs",
    "Repetition-Removal Ledger",
    "No support state changes",
    "No new result is created by this dry run",
)

CONTEXT_ABI_DRAFT_REQUIRED_FRAGMENTS = (
    "Consolidation Destination Draft: The Virtual Context ABI, Typed Pages, Cells, and Certificates",
    "Status: review-ready draft; human/external review not completed.",
    "does not edit",
    "Destination continuity ID: `virtual-context-abi`",
    "Proposed displayed title: **The Virtual Context ABI: Typed Pages, Cells, and",
    "Preservation Ledger",
    "Destination Chapter Draft",
    "Chapter status",
    "Drafting guardrail",
    "Human Reading Path",
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Codex test plan",
    "Formalization hooks",
    "Source crosswalk",
    "Repetition-removal ledger",
    "Review Decision Surface",
    "No chapter core claim is promoted above `argument`",
    "This draft does not merge chapters.",
    "This draft does not change Appendix C support states.",
)

CONTEXT_ABI_REQUIRED_IDS = {
    "virtual-context-abi",
    "semantic-pages-context-cells-and-certificates",
    "context-transactions-snapshots-mounts-and-taint",
    "verification-bandwidth-and-context-adequacy",
    "claim-ledgers-and-belief-revision",
}

CONTEXT_ABI_REQUIRED_SOURCE_IDS = {
    "vcm_public",
    "context_engineer",
    "verification_bandwidth",
    "viea",
    "vcm_editable",
    "moecot",
    "spinoza",
}

CONTEXT_ABI_REQUIRED_EXTERNAL_IDS = {
    "ext_alce_2023",
    "ext_longbench_2023",
    "ext_longllmlingua_2023",
    "ext_lost_in_middle_2023",
    "ext_memgpt_2023",
    "ext_rag_2020",
    "ext_ruler_2024",
    "ext_self_rag_2023",
}

CONTEXT_ABI_REQUIRED_LEAN_TAGS = {
    "lean:vcm.abi.operational_invariant",
    "lean:vcm.abi.failure_blocks_promotion",
    "lean:vcm.certificates.operational_invariant",
    "lean:vcm.certificates.failure_blocks_promotion",
}

CONTEXT_ABI_REQUIRED_FIXTURE_FRAGMENTS = {
    "schemas/context_abi_record.schema.json",
    "schemas/semantic_page_certificate.schema.json",
    "schemas/context_packet.schema.json",
    "schemas/context_adequacy_record.schema.json",
    "schemas/context_transaction_record.schema.json",
    "experiments/context_admission_adequacy/fixtures/valid_local_check_public_context.json",
    "experiments/context_admission_adequacy/fixtures/valid_admitted_but_inadequate.json",
    "experiments/context_admission_adequacy/fixtures/valid_conflict_escalation.json",
    "experiments/context_admission_adequacy/fixtures/invalid_admission_as_verification.json",
    "experiments/context_admission_adequacy/fixtures/invalid_conflict_promoted.json",
    "experiments/context_admission_adequacy/fixtures/invalid_stale_certificate_use.json",
    "python3 scripts/validate_context_admission_adequacy.py",
}

VERIFICATION_REVIEW_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation Dry Run: Verification And Adversarial Review",
    "does not edit `book_structure.json`",
    "Proof-Carrying Claims and Adversarial Review",
    "claim-ledgers-and-belief-revision",
    "Proposed `book_structure.json` Diff",
    "Destination Section Outline",
    "Appendix C Row Plan",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Tests, Schemas, And Fixtures",
    "Reader Path, Handoff, And Review Repairs",
    "Repetition-Removal Ledger",
    "No support state changes",
    "No new result is created by this dry run",
)

VERIFICATION_REVIEW_DRAFT_REQUIRED_FRAGMENTS = (
    "Consolidation Destination Draft: Proof-Carrying Claims and Adversarial Review",
    "Status: review-ready draft; human/external review not completed.",
    "does not edit `book_structure.json`",
    "Destination continuity ID: `spinoza-verification-and-proof-carrying-claims`",
    "Proposed displayed title: **Proof-Carrying Claims and Adversarial Review**",
    "Preservation Ledger",
    "Destination Chapter Draft",
    "Chapter status",
    "Drafting guardrail",
    "Human Reading Path",
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Codex test plan",
    "Formalization hooks",
    "Source crosswalk",
    "Repetition-removal ledger",
    "Review Decision Surface",
    "No chapter core claim is promoted above `argument`",
    "This draft does not merge chapters.",
    "This draft does not change Appendix C support states.",
)

VERIFICATION_REVIEW_REQUIRED_IDS = {
    "spinoza-verification-and-proof-carrying-claims",
    "unified-adaptive-tribunal-and-adversarial-review",
    "claim-ledgers-and-belief-revision",
}

VERIFICATION_REVIEW_REQUIRED_SOURCE_IDS = {
    "spinoza",
    "genesiscode",
    "coherence_exchange",
    "verification_bandwidth",
    "treellm",
    "uat",
    "talos",
}

VERIFICATION_REVIEW_REQUIRED_EXTERNAL_IDS = {
    "ext_lean4_theorem_proving",
    "ext_proof_carrying_code_1997",
    "ext_contestable_ai_design_2022",
}

VERIFICATION_REVIEW_REQUIRED_LEAN_TAGS = {
    "lean:spinoza.proof_carrying.operational_invariant",
    "lean:spinoza.proof_carrying.failure_blocks_promotion",
    "lean:tribunal.review.operational_invariant",
    "lean:tribunal.review.failure_blocks_promotion",
}

VERIFICATION_REVIEW_REQUIRED_FIXTURE_FRAGMENTS = {
    "schemas/proof_carrying_claim.schema.json",
    "schemas/tribunal_review_record.schema.json",
    "schemas/claim_record.schema.json",
    "schemas/belief_revision_record.schema.json",
    "experiments/proof_carrying_claims/fixtures/valid_formal_narrow_pass.json",
    "experiments/proof_carrying_claims/fixtures/valid_citation_dossier_no_change.json",
    "experiments/proof_carrying_claims/fixtures/valid_mismatch_escalates.json",
    "experiments/proof_carrying_claims/fixtures/invalid_pass_missing_artifact_refs.json",
    "experiments/proof_carrying_claims/fixtures/invalid_mismatch_promotes.json",
    "experiments/proof_carrying_claims/fixtures/invalid_formal_tier_wrong_justification.json",
    "experiments/proof_carrying_claims/fixtures/invalid_timeout_overpromotes_support.json",
    "experiments/proof_carrying_claims/fixtures/invalid_negative_missing_failed_attempt.json",
    "experiments/tribunal_review/fixtures/valid_accept_with_scope_constraints.json",
    "experiments/tribunal_review/fixtures/valid_block_unchanged_evidence.json",
    "experiments/tribunal_review/fixtures/valid_high_risk_revise_with_dissent.json",
    "experiments/tribunal_review/fixtures/invalid_accept_missing_evidence.json",
    "experiments/tribunal_review/fixtures/invalid_high_risk_no_probes.json",
    "experiments/tribunal_review/fixtures/invalid_prior_review_laundering.json",
    "experiments/tribunal_review/fixtures/invalid_dissent_without_unresolved_issue.json",
    "experiments/tribunal_review/fixtures/invalid_weak_non_claims.json",
    "python3 scripts/validate_proof_carrying_claims.py",
    "python3 scripts/validate_tribunal_review.py",
}

PLANNING_DAG_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation Dry Run: Planning And DAG Control",
    "does not edit `book_structure.json`",
    "Planning as a Control Layer: DAGs and Intelligence Arbitrage",
    "cognitive-compilation-and-semantic-ir",
    "Proposed `book_structure.json` Diff",
    "Destination Section Outline",
    "Appendix C Row Plan",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Tests, Schemas, And Fixtures",
    "Reader Path, Handoff, And Review Repairs",
    "Repetition-Removal Ledger",
    "No support state changes",
    "No new result is created by this dry run",
)

PLANNING_DAG_DRAFT_REQUIRED_FRAGMENTS = (
    "Consolidation Destination Draft: Planning as a Control Layer, DAGs and Intelligence Arbitrage",
    "Status: review-ready draft; human/external review not completed.",
    "does not edit",
    "Destination continuity ID: `planning-as-a-control-layer`",
    "Proposed displayed title: **Planning as a Control Layer: DAGs and Intelligence",
    "Preservation Ledger",
    "Destination Chapter Draft",
    "Chapter status",
    "Drafting guardrail",
    "Human Reading Path",
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Codex test plan",
    "Formalization hooks",
    "Source crosswalk",
    "Repetition-removal ledger",
    "Review Decision Surface",
    "No chapter core claim is promoted above `argument`",
    "This draft does not merge chapters.",
    "This draft does not change Appendix C support states.",
)

PLANNING_DAG_REQUIRED_IDS = {
    "planning-as-a-control-layer",
    "planforge-dags-and-intelligence-arbitrage",
    "cognitive-compilation-and-semantic-ir",
}

PLANNING_DAG_REQUIRED_SOURCE_IDS = {
    "planforge",
    "viea",
    "cognitive_compilation",
    "software_magic_grimoire",
    "moecot",
    "planforge_compiler_arch",
    "coherence_exchange",
    "tokenmana",
}

PLANNING_DAG_REQUIRED_EXTERNAL_IDS = {
    "ext_autogen_2023",
    "ext_behavior_trees_robotics_ai_2017",
    "ext_integrated_tamp_2020",
    "ext_pddl_1998",
    "ext_react_2022",
    "ext_shop2_2003",
    "ext_three_states_plan_fear_2006",
    "ext_tla_plus_home_docs",
    "ext_tree_of_thoughts_2023",
}

PLANNING_DAG_REQUIRED_LEAN_TAGS = {
    "lean:planning.control_layer.operational_invariant",
    "lean:planning.control_layer.failure_blocks_promotion",
    "lean:planforge.dag.operational_invariant",
    "lean:planforge.dag.failure_blocks_promotion",
}

PLANNING_DAG_REQUIRED_FIXTURE_FRAGMENTS = {
    "schemas/plan_graph.schema.json",
    "schemas/planforge_dag.schema.json",
    "schemas/command_contract.schema.json",
    "schemas/hive_job_contract.schema.json",
    "schemas/semantic_atom.schema.json",
    "experiments/plan_execution_contracts/fixtures/valid_dispatchable_linear_plan.json",
    "experiments/plan_execution_contracts/fixtures/valid_blocked_authority_plan.json",
    "experiments/plan_execution_contracts/fixtures/invalid_cycle_in_dag.json",
    "experiments/plan_execution_contracts/fixtures/invalid_contract_mismatch.json",
    "experiments/plan_execution_contracts/fixtures/invalid_requirement_lost.json",
    "experiments/plan_execution_contracts/fixtures/invalid_dispatch_without_receipt.json",
    "experiments/plan_execution_contracts/fixtures/invalid_approval_bypass.json",
    "python3 scripts/validate_plan_execution_contracts.py",
}

REQUIRED_DESTINATIONS = (
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty",
    "Command Contracts: From Intent to Executable Work",
    "The Virtual Context ABI: Typed Pages, Cells, and Certificates",
    "Proof-Carrying Claims and Adversarial Review",
    "Planning as a Control Layer: DAGs and Intelligence Arbitrage",
)

PUBLIC_REFERENCES = (
    "docs/chapter_consolidation_sequence.md",
    "docs/chapter_consolidation_dry_run_compression.md",
    "docs/chapter_consolidation_destination_draft_compression.md",
    "docs/chapter_consolidation_dry_run_intent_contracts.md",
    "docs/chapter_consolidation_destination_draft_intent_contracts.md",
    "docs/chapter_consolidation_dry_run_context_abi.md",
    "docs/chapter_consolidation_destination_draft_context_abi.md",
    "docs/chapter_consolidation_dry_run_verification_review.md",
    "docs/chapter_consolidation_destination_draft_verification_review.md",
    "docs/chapter_consolidation_dry_run_planning_dag.md",
    "docs/chapter_consolidation_destination_draft_planning_dag.md",
    "scripts/validate_chapter_consolidation_sequence.py",
)


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def manifest_chapter_ids() -> set[str]:
    data = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("book_structure.json must contain an object.")
    ids: set[str] = set()
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            chapter_id = chapter.get("id")
            if isinstance(chapter_id, str):
                ids.add(chapter_id)
    return ids


def main() -> None:
    errors: list[str] = []

    try:
        sequence = read_text(SEQUENCE)
    except FileNotFoundError:
        print("Missing docs/chapter_consolidation_sequence.md")
        sys.exit(1)

    ids = manifest_chapter_ids()
    if len(ids) != 54:
        errors.append("Consolidation sequence expects the current manifest to remain at 54 chapters.")

    for chapter_id in sorted(REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Required consolidation chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in sequence:
            errors.append(f"Consolidation sequence does not mention `{chapter_id}`.")

    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in sequence:
            errors.append(f"Consolidation sequence missing required boundary: {fragment}")

    for destination in REQUIRED_DESTINATIONS:
        if destination not in sequence:
            errors.append(f"Consolidation sequence missing destination title: {destination}")

    try:
        compression = read_text(COMPRESSION_DRY_RUN)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_dry_run_compression.md")
        compression = ""

    for fragment in COMPRESSION_REQUIRED_FRAGMENTS:
        if fragment not in compression:
            errors.append(f"Compression dry run missing required boundary: {fragment}")

    for chapter_id in sorted(COMPRESSION_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Compression dry-run chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in compression:
            errors.append(f"Compression dry run does not mention `{chapter_id}`.")

    for source_id in sorted(COMPRESSION_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in compression:
            errors.append(f"Compression dry run missing source ID `{source_id}`.")

    for source_id in sorted(COMPRESSION_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in compression:
            errors.append(f"Compression dry run missing external source ID `{source_id}`.")

    for tag in sorted(COMPRESSION_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in compression:
            errors.append(f"Compression dry run missing Lean tag `{tag}`.")

    try:
        compression_draft = read_text(COMPRESSION_DESTINATION_DRAFT)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_destination_draft_compression.md")
        compression_draft = ""

    for fragment in COMPRESSION_DRAFT_REQUIRED_FRAGMENTS:
        if fragment not in compression_draft:
            errors.append(f"Compression destination draft missing required boundary: {fragment}")

    for chapter_id in sorted(COMPRESSION_REQUIRED_IDS | {"fast-generation-architectures"}):
        if chapter_id not in ids:
            errors.append(f"Compression destination chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in compression_draft:
            errors.append(f"Compression destination draft does not mention `{chapter_id}`.")

    for source_id in sorted(COMPRESSION_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in compression_draft:
            errors.append(f"Compression destination draft missing source ID `{source_id}`.")

    for source_id in sorted(COMPRESSION_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in compression_draft:
            errors.append(f"Compression destination draft missing external source ID `{source_id}`.")

    for tag in sorted(COMPRESSION_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in compression_draft:
            errors.append(f"Compression destination draft missing Lean tag `{tag}`.")

    try:
        intent = read_text(INTENT_DRY_RUN)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_dry_run_intent_contracts.md")
        intent = ""

    for fragment in INTENT_REQUIRED_FRAGMENTS:
        if fragment not in intent:
            errors.append(f"Intent/contracts dry run missing required boundary: {fragment}")

    for chapter_id in sorted(INTENT_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Intent/contracts chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in intent:
            errors.append(f"Intent/contracts dry run does not mention `{chapter_id}`.")

    for source_id in sorted(INTENT_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in intent:
            errors.append(f"Intent/contracts dry run missing source ID `{source_id}`.")

    for source_id in sorted(INTENT_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in intent:
            errors.append(f"Intent/contracts dry run missing external source ID `{source_id}`.")

    for tag in sorted(INTENT_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in intent:
            errors.append(f"Intent/contracts dry run missing Lean tag `{tag}`.")

    for fragment in sorted(INTENT_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in intent:
            errors.append(f"Intent/contracts dry run missing fixture or validator `{fragment}`.")

    try:
        intent_draft = read_text(INTENT_DESTINATION_DRAFT)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_destination_draft_intent_contracts.md")
        intent_draft = ""

    for fragment in INTENT_DRAFT_REQUIRED_FRAGMENTS:
        if fragment not in intent_draft:
            errors.append(f"Intent/contracts destination draft missing required boundary: {fragment}")

    for chapter_id in sorted(INTENT_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Intent/contracts destination chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in intent_draft:
            errors.append(f"Intent/contracts destination draft does not mention `{chapter_id}`.")

    for source_id in sorted(INTENT_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in intent_draft:
            errors.append(f"Intent/contracts destination draft missing source ID `{source_id}`.")

    for source_id in sorted(INTENT_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in intent_draft:
            errors.append(f"Intent/contracts destination draft missing external source ID `{source_id}`.")

    for tag in sorted(INTENT_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in intent_draft:
            errors.append(f"Intent/contracts destination draft missing Lean tag `{tag}`.")

    try:
        context_abi = read_text(CONTEXT_ABI_DRY_RUN)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_dry_run_context_abi.md")
        context_abi = ""

    for fragment in CONTEXT_ABI_REQUIRED_FRAGMENTS:
        if fragment not in context_abi:
            errors.append(f"Static context ABI dry run missing required boundary: {fragment}")

    for chapter_id in sorted(CONTEXT_ABI_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Static context ABI chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in context_abi:
            errors.append(f"Static context ABI dry run does not mention `{chapter_id}`.")

    for source_id in sorted(CONTEXT_ABI_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in context_abi:
            errors.append(f"Static context ABI dry run missing source ID `{source_id}`.")

    for source_id in sorted(CONTEXT_ABI_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in context_abi:
            errors.append(f"Static context ABI dry run missing external source ID `{source_id}`.")

    for tag in sorted(CONTEXT_ABI_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in context_abi:
            errors.append(f"Static context ABI dry run missing Lean tag `{tag}`.")

    for fragment in sorted(CONTEXT_ABI_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in context_abi:
            errors.append(f"Static context ABI dry run missing fixture, schema, or validator `{fragment}`.")

    try:
        context_abi_draft = read_text(CONTEXT_ABI_DESTINATION_DRAFT)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_destination_draft_context_abi.md")
        context_abi_draft = ""

    for fragment in CONTEXT_ABI_DRAFT_REQUIRED_FRAGMENTS:
        if fragment not in context_abi_draft:
            errors.append(f"Static context ABI destination draft missing required boundary: {fragment}")

    for chapter_id in sorted(CONTEXT_ABI_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Static context ABI destination chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in context_abi_draft:
            errors.append(f"Static context ABI destination draft does not mention `{chapter_id}`.")

    for source_id in sorted(CONTEXT_ABI_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in context_abi_draft:
            errors.append(f"Static context ABI destination draft missing source ID `{source_id}`.")

    for source_id in sorted(CONTEXT_ABI_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in context_abi_draft:
            errors.append(f"Static context ABI destination draft missing external source ID `{source_id}`.")

    for tag in sorted(CONTEXT_ABI_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in context_abi_draft:
            errors.append(f"Static context ABI destination draft missing Lean tag `{tag}`.")

    for fragment in sorted(CONTEXT_ABI_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in context_abi_draft:
            errors.append(f"Static context ABI destination draft missing fixture, schema, or validator `{fragment}`.")

    try:
        verification_review = read_text(VERIFICATION_REVIEW_DRY_RUN)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_dry_run_verification_review.md")
        verification_review = ""

    for fragment in VERIFICATION_REVIEW_REQUIRED_FRAGMENTS:
        if fragment not in verification_review:
            errors.append(f"Verification/review dry run missing required boundary: {fragment}")

    for chapter_id in sorted(VERIFICATION_REVIEW_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Verification/review chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in verification_review:
            errors.append(f"Verification/review dry run does not mention `{chapter_id}`.")

    for source_id in sorted(VERIFICATION_REVIEW_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in verification_review:
            errors.append(f"Verification/review dry run missing source ID `{source_id}`.")

    for source_id in sorted(VERIFICATION_REVIEW_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in verification_review:
            errors.append(f"Verification/review dry run missing external source ID `{source_id}`.")

    for tag in sorted(VERIFICATION_REVIEW_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in verification_review:
            errors.append(f"Verification/review dry run missing Lean tag `{tag}`.")

    for fragment in sorted(VERIFICATION_REVIEW_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in verification_review:
            errors.append(f"Verification/review dry run missing fixture, schema, or validator `{fragment}`.")

    try:
        verification_review_draft = read_text(VERIFICATION_REVIEW_DESTINATION_DRAFT)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_destination_draft_verification_review.md")
        verification_review_draft = ""

    for fragment in VERIFICATION_REVIEW_DRAFT_REQUIRED_FRAGMENTS:
        if fragment not in verification_review_draft:
            errors.append(f"Verification/review destination draft missing required boundary: {fragment}")

    for chapter_id in sorted(VERIFICATION_REVIEW_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Verification/review destination chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in verification_review_draft:
            errors.append(f"Verification/review destination draft does not mention `{chapter_id}`.")

    for source_id in sorted(VERIFICATION_REVIEW_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in verification_review_draft:
            errors.append(f"Verification/review destination draft missing source ID `{source_id}`.")

    for source_id in sorted(VERIFICATION_REVIEW_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in verification_review_draft:
            errors.append(f"Verification/review destination draft missing external source ID `{source_id}`.")

    for tag in sorted(VERIFICATION_REVIEW_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in verification_review_draft:
            errors.append(f"Verification/review destination draft missing Lean tag `{tag}`.")

    for fragment in sorted(VERIFICATION_REVIEW_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in verification_review_draft:
            errors.append(f"Verification/review destination draft missing fixture, schema, or validator `{fragment}`.")

    try:
        planning_dag = read_text(PLANNING_DAG_DRY_RUN)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_dry_run_planning_dag.md")
        planning_dag = ""

    for fragment in PLANNING_DAG_REQUIRED_FRAGMENTS:
        if fragment not in planning_dag:
            errors.append(f"Planning/DAG dry run missing required boundary: {fragment}")

    for chapter_id in sorted(PLANNING_DAG_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Planning/DAG chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in planning_dag:
            errors.append(f"Planning/DAG dry run does not mention `{chapter_id}`.")

    for source_id in sorted(PLANNING_DAG_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in planning_dag:
            errors.append(f"Planning/DAG dry run missing source ID `{source_id}`.")

    for source_id in sorted(PLANNING_DAG_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in planning_dag:
            errors.append(f"Planning/DAG dry run missing external source ID `{source_id}`.")

    for tag in sorted(PLANNING_DAG_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in planning_dag:
            errors.append(f"Planning/DAG dry run missing Lean tag `{tag}`.")

    for fragment in sorted(PLANNING_DAG_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in planning_dag:
            errors.append(f"Planning/DAG dry run missing fixture, schema, or validator `{fragment}`.")

    try:
        planning_dag_draft = read_text(PLANNING_DAG_DESTINATION_DRAFT)
    except FileNotFoundError:
        errors.append("Missing docs/chapter_consolidation_destination_draft_planning_dag.md")
        planning_dag_draft = ""

    for fragment in PLANNING_DAG_DRAFT_REQUIRED_FRAGMENTS:
        if fragment not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft missing required boundary: {fragment}")

    for chapter_id in sorted(PLANNING_DAG_REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Planning/DAG destination chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft does not mention `{chapter_id}`.")

    for source_id in sorted(PLANNING_DAG_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft missing source ID `{source_id}`.")

    for source_id in sorted(PLANNING_DAG_REQUIRED_EXTERNAL_IDS):
        if f"`{source_id}`" not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft missing external source ID `{source_id}`.")

    for tag in sorted(PLANNING_DAG_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft missing Lean tag `{tag}`.")

    for fragment in sorted(PLANNING_DAG_REQUIRED_FIXTURE_FRAGMENTS):
        if f"`{fragment}`" not in planning_dag_draft:
            errors.append(f"Planning/DAG destination draft missing fixture, schema, or validator `{fragment}`.")

    for path in (ROADMAP, README, PUBLICATION, REPOSITORY_MAP):
        text = read_text(path)
        for reference in PUBLIC_REFERENCES:
            if reference not in text:
                errors.append(f"{path.relative_to(ROOT)} missing public reference to {reference}")

    if errors:
        print("Chapter consolidation sequence validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Chapter consolidation sequence validation passed: "
        "54-chapter manifest preserved and full candidate sequence recorded."
    )


if __name__ == "__main__":
    main()
