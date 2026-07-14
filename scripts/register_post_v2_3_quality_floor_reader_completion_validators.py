#!/usr/bin/env python3
"""Register post-v2.3 quality-floor, reader, and chapter-hygiene gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
CONTRACT_FIELDS = [
    "input_contract", "input_artifacts", "output_contract", "output_assertions",
    "claim_scope", "negative_controls", "negative_control_cases",
    "prohibited_inference", "contract_precision", "semantic_review_state",
    {
        "script": "validate_post_v2_3_reader_successor.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "The immutable 44-record v1.0 historical reader, prospectively selected v2.0 directory and HTML format, 54 exact-baseline curated files and records, source/boundary reconciliation, lineage, terminal format state, and no support effect.",
        "input_artifacts": ["scripts/validate_post_v2_3_reader_successor.py", "scripts/build_post_v2_3_reader_successor.py", "editions/reader_manuscript/v1_0/manifest.json", "editions/reader_manuscript/v2_0/manifest.json", "editions/reader_manuscript/v2_0/reconciliation_approval.json", "editions/reader_manuscript/v2_0/chapter_lineage.json", "editions/reader_manuscript/v2_0/format_review_matrix.json", "editions/reader_manuscript/v2_0/reader_release_record.json"],
        "output_contract": "Reject v1 mutation, current-spine denominator/order drift, curated-file digest or meaning divergence, support/review laundering, missing semantic packet fields, prospective-format drift, or a released state without an exact terminal record.",
        "output_assertions": ["54 exact current-spine records", "44 retained plus ten added identities", "zero meaning divergence", "immutable v1 predecessor digest", "canonical HTML selected prospectively", "released terminal record", "six rejecting mutations"],
        "claim_scope": "Curated-reader source identity, reconciliation, lineage, and terminal selected-format disposition only.",
        "negative_controls": "validator_owned_and_manifest_bound",
        "negative_control_cases": ["missing record", "v1 digest drift", "format substitution", "support promotion", "curated digest drift", "false external review"],
        "prohibited_inference": "Source reconciliation and edition release do not establish independent review, literary perfection, canonical evidence authority, model quality, safety, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_source_and_identity_audit_not_independent",
    },
    {
        "script": "validate_post_v2_3_reader_html_artifact.py",
        "execution_tier": "deep", "validation_class": "reader_artifact_gate",
        "input_contract": "The exact deterministic v2.0 HTML archive and site tree, 59 rendered pages, 54 chapter entry points, all desktop/mobile browser and accessibility reports, 5,432 internal links, 1,138 anchors, contrast, reflow, headings, landmarks, alt text, table headers, duplicate IDs, and no support effect.",
        "input_artifacts": ["scripts/validate_post_v2_3_reader_html_artifact.py", "editions/reader_manuscript/v2_0/html_artifact_manifest.json", "editions/reader_manuscript/v2_0/html_browser_report.json", "editions/reader_manuscript/v2_0/html_accessibility_tree_report.json", "editions/reader_manuscript/v2_0/html_keyboard_report.json", "editions/reader_manuscript/v2_0/html_wcag_report.json", "editions/reader_manuscript/v2_0/html_release_inspection.json", "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0-html.zip"],
        "output_contract": "Reject archive/site mismatch, page or viewport denominator drift, unresolved internal links or anchors, layout overflow, semantic/accessibility failure, contrast failure, keyboard traps, duplicate IDs, selected-format substitution, or support movement.",
        "output_assertions": ["59 pages", "54 chapter entry points", "118 desktop/mobile pairs", "exact archive and site bytes", "zero unresolved links or anchors", "zero accessibility/layout/contrast failures", "six rejecting mutations"],
        "claim_scope": "Exact local canonical HTML archive inspection for the selected curated-reader format only.",
        "negative_controls": "validator_owned_and_exact_artifact_bound",
        "negative_control_cases": ["archive digest drift", "page denominator drift", "duplicate ID", "keyboard trap", "contrast failure", "format substitution"],
        "prohibited_inference": "Automated artifact inspection is not external-human or screen-reader review, legal WCAG certification, approval of another format, public deployment, evidence promotion, or proof of safety/AGI/ASI.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_automated_artifact_audit_not_independent",
    },
    {
        "script": "build_post_v2_3_reader_html_release_record.py",
        "execution_tier": "deep", "validation_class": "publication_gate",
        "input_contract": "The exact inspected v2.0 canonical HTML archive, source and baseline digests, four digest-bound inspection reports, prospective format selection, rights snapshot, selected-format blocker disposition, residuals, and no support effect.",
        "input_artifacts": ["scripts/build_post_v2_3_reader_html_release_record.py", "schemas/post_v2_3_reader_html_release_record.schema.json", "editions/reader_manuscript/v2_0/reader_release_record.json", "editions/reader_manuscript/v2_0/html_release_inspection.json", "editions/reader_manuscript/v2_0/html_artifact_manifest.json", "LICENSE.md"],
        "output_contract": "Reject record/schema drift, artifact-digest drift, extra approved formats, unresolved selected-format blockers, rights laundering, support promotion, or release claims beyond the exact tracked local HTML archive.",
        "output_assertions": ["one exact approved local HTML archive", "one approved format", "zero selected-format blockers", "all-rights-reserved untagged-path snapshot", "no public deployment claim", "no support movement", "five rejecting mutations"],
        "claim_scope": "Edition approval for one digest-bound tracked local canonical HTML archive only.",
        "negative_controls": "validator_owned_and_release_record_bound",
        "negative_control_cases": ["decision substitution", "support promotion", "extra approved format", "false blocker clearance", "archive digest drift"],
        "prohibited_inference": "The record does not approve another format, create a public deployment or license grant, claim independent or screen-reader review, promote evidence, or establish model quality, safety, AGI, or ASI.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_release_record_audit_not_independent",
    },
]

READER_UNITS = CONTRACT_FIELDS[10:]
CONTRACT_FIELDS = CONTRACT_FIELDS[:10]

READER_UNITS.append(
    {
        "script": "validate_post_v2_3_reader_epub_disposition.py",
        "execution_tier": "deep",
        "validation_class": "reader_artifact_gate",
        "input_contract": "The exact frozen-source v2.0 EPUB, generic format-disposition schema, all-member/all-XHTML structural inspection, two independent canonical replays, two digest-bound state-diagram raster pins, two failed Apple Books control-bridge attempts, terminal M3 status, rights snapshot, and no support or release effect.",
        "input_artifacts": [
            "scripts/validate_post_v2_3_reader_epub_disposition.py",
            "scripts/audit_post_v2_3_reader_epub_artifact.py",
            "scripts/render_curated_reader_formats.py",
            "schemas/reader_format_disposition.schema.json",
            "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0.epub",
            "editions/reader_manuscript/v2_0/epub_disposition.json",
            "editions/reader_manuscript/v2_0/epub_structural_inspection.json",
            "editions/reader_manuscript/v2_0/epub_application_review.json",
            "editions/reader_manuscript/v2_0/epub_reproducibility.json",
            "editions/reader_manuscript/v2_0/text_format_profile.json",
            "editions/reader_manuscript/v2_0/format_review_matrix.json",
            "editions/reader_manuscript/v2_0/profiles/epub-mermaid/file7.png",
            "editions/reader_manuscript/v2_0/profiles/epub-mermaid/file27.png",
            "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json",
            "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md",
            "LICENSE.md",
        ],
        "output_contract": "Reject artifact/profile/evidence digest drift, package or structural denominator failure, nondeterministic replay, lost raster pins, false Apple Books evidence, premature approval, matrix/roadmap disagreement, rights laundering, support movement, or release effect.",
        "output_assertions": [
            "one exact 5,505,557-byte EPUB",
            "148 package members and 62 XHTML entries",
            "54 ordered chapter entry points",
            "1,415 resolved hrefs",
            "two byte-identical full replays",
            "two failed Apple Books bridge attempts",
            "blocked terminal M3 disposition",
            "seven rejecting mutations",
        ],
        "claim_scope": "Exact local EPUB package, structural automation, deterministic replay, and honest application-inspection blocker only.",
        "negative_controls": "validator_owned_and_exact_artifact_bound",
        "negative_control_cases": [
            "premature approval",
            "artifact digest drift",
            "structural failure",
            "Apple Books evidence laundering",
            "replay inequality",
            "M3 reopening",
            "support promotion",
        ],
        "prohibited_inference": "Structural and reproducibility success do not establish Apple Books behavior, reflow, font/theme/search interaction, screen-reader or device review, publication approval, rights, model quality, safety, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_automated_artifact_audit_with_blocked_application_route_not_independent",
    }
)

READER_UNITS.append(
    {
        "script": "validate_post_v2_3_reader_docx_disposition.py",
        "execution_tier": "deep",
        "validation_class": "reader_artifact_gate",
        "input_contract": "The exact frozen-source v2.0 DOCX, generic format-disposition schema, all-member OOXML and relationship inspection, all-page pinned LibreOffice Writer headless export and visual review, two byte-identical full renders, bounded DOCX-only glossary repair, terminal P1/M5 status, rights snapshot, and no support or release effect.",
        "input_artifacts": [
            "scripts/validate_post_v2_3_reader_docx_disposition.py",
            "scripts/audit_post_v2_3_reader_docx_artifact.py",
            "scripts/render_curated_reader_formats.py",
            "scripts/extract_rendered_mermaid_svgs.js",
            "schemas/reader_format_disposition.schema.json",
            "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0.docx",
            "editions/reader_manuscript/v2_0/docx_disposition.json",
            "editions/reader_manuscript/v2_0/docx_package_and_page_inspection.json",
            "editions/reader_manuscript/v2_0/docx_visual_review.json",
            "editions/reader_manuscript/v2_0/docx_application_review.json",
            "editions/reader_manuscript/v2_0/docx_reproducibility.json",
            "editions/reader_manuscript/v2_0/text_format_profile.json",
            "editions/reader_manuscript/v2_0/format_review_matrix.json",
            "editions/reader_manuscript/v2_0/profiles/reader-v2-reference.docx",
            "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json",
            "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md",
            "LICENSE.md",
        ],
        "output_contract": "Reject artifact/profile/evidence digest drift, OOXML/member/relationship/style/heading/list/table/link/media/alt/language/page denominator failure, incomplete visual review, false Word or GUI evidence, nondeterministic replay, glossary-repair laundering, matrix/roadmap disagreement, public-rights laundering, support movement, or release effect.",
        "output_assertions": [
            "one exact 7,429,468-byte DOCX",
            "95 OOXML members and 16 parsed XML members",
            "79 described PNG drawings and 274 hyperlinks",
            "54 ordered chapter titles and 1,169 bookmarks",
            "644 reviewed office-engine pages in 33 contact sheets",
            "two byte-identical full renders",
            "approved exact local terminal P1/M5 disposition",
            "nine rejecting mutations",
        ],
        "claim_scope": "Exact local DOCX package, pinned LibreOffice Writer headless application-engine path, page-complete internal review, deterministic replay, and bounded local approval only.",
        "negative_controls": "validator_owned_and_exact_artifact_bound",
        "negative_control_cases": [
            "public-approval laundering",
            "artifact digest drift",
            "OOXML denominator failure",
            "blank-page regression",
            "incomplete visual review",
            "Microsoft Word evidence laundering",
            "replay inequality",
            "M5 reopening",
            "support promotion",
        ],
        "prohibited_inference": "Package, application-engine, visual, and reproducibility success do not establish Microsoft Word, LibreOffice GUI, Google Docs, assistive-technology, device-family, independent-human, legal-WCAG, public publication, rights, model quality, safety, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_automated_application_engine_and_visual_artifact_audit_not_independent",
    }
)

READER_UNITS.append(
    {
        "script": "validate_post_v2_3_p2_source_audit.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The exact ten newer chapters, four passage-reviewed accepted primary sources and source notes, 37 ordered Tier-2 dispositions, reasoning-trace/world-model/foundations ownership records, immutable v1.0/v2.0 reader history, one 54-chapter source-only v2.1 reader successor, completed P2/M6 status, and no support or release effect.",
        "input_artifacts": [
            "scripts/validate_post_v2_3_p2_source_audit.py",
            "scripts/build_post_v2_3_p2_source_audit.py",
            "scripts/integrate_post_v2_3_p2_sources.py",
            "scripts/build_post_v2_3_reader_v2_1.py",
            "evidence_quality/post_v2_3_source_and_completeness_residuals.json",
            "docs/post_v2_3_external_anchoring_and_completeness_audit.md",
            "editions/reader_manuscript/v2_1/manifest.json",
            "sources/source_inventory.json",
            "sources/source_notes/ext_faithfulness_information_flow_2026.md",
            "sources/source_notes/ext_monitorbench_2026.md",
            "sources/source_notes/ext_v_jepa_2_2025.md",
            "sources/source_notes/ext_embedded_agency_2019.md",
            "appendices/A_source_matrix.qmd",
            "appendices/C_claim_evidence_matrix.qmd",
            "appendices/H_external_sources.qmd",
            "docs/book_outline.md",
            "book_structure.json",
            "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json",
            "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md",
        ],
        "output_contract": "Reject a missing ten-chapter or Tier-2 row, nonterminal disposition, accepted source without inventory/note/passage mapping/live prose/reader prose, citation padding, unearned chapter growth, v2.1 identity drift, source-count drift, P2/M6 reopening, support laundering, or release laundering.",
        "output_assertions": [
            "ten unique chapter rows",
            "37 ordered Tier-2 rows",
            "four accepted source-specific insertions",
            "54-chapter breadth preserved",
            "54-chapter source-only v2.1 reader",
            "completed P2 and M6",
            "no support or release effect",
            "nine rejecting mutations",
        ],
        "claim_scope": "Passage-reviewed source selection, chapter ownership, live/reader prose reconciliation, and terminal P2 completeness dispositions only.",
        "negative_controls": "validator_owned_and_source_mapping_bound",
        "negative_control_cases": [
            "missing ten-chapter row",
            "missing Tier-2 row",
            "accepted source erased",
            "citation padding",
            "unearned new chapter",
            "breadth drift",
            "nonterminal audit",
            "support laundering",
            "invalid disposition",
        ],
        "prohibited_inference": "Passage review and prose reconciliation do not reproduce external results, prove monitorability, causal world modeling, corrigibility, safety, model quality, AGI, ASI, approve a reader format, publish a release, or move chapter-core support.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_primary_source_and_cross_product_audit_not_independent",
    }
)

NEW_UNITS = [
    {
        "script": "validate_chapter_source_hygiene.py",
        "execution_tier": "deep",
        "validation_class": "schema_or_structure",
        "input_contract": "All chapter-directory HTML files, explicit Quarto resource routes, canonical redirect destinations, no-support boundaries, and chapter-history ledger entries.",
        "input_artifacts": ["scripts/validate_chapter_source_hygiene.py", "chapters/unified-adaptive-tribunal-and-adversarial-review.html", "_quarto.yml", "docs/chapter_history_ledger.md", "docs/chapter_consolidation_url_history_policy.md"],
        "output_contract": "Reject undeclared chapter HTML, missing or conflicting redirect targets, absent active QMD destinations, missing Quarto resource declarations, missing history entries, or lost no-support boundaries.",
        "output_assertions": ["ten declared historical redirects", "ten canonical active targets", "zero undeclared chapter HTML"],
        "claim_scope": "Chapter source-tree and historical URL-preservation hygiene only.",
        "negative_controls": "structural_exactness",
        "negative_control_cases": ["undeclared HTML", "missing refresh", "canonical mismatch", "missing active target", "missing history declaration"],
        "prohibited_inference": "Redirect validity does not validate destination chapter claims, support, review, or release quality.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_contract_audit_not_independent",
    },
    {
        "script": "validate_post_v2_3_quality_floor_reader_completion_roadmap.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "One completed post-v2.3 roadmap, schema-bound terminal status, exact 54-chapter/280-source/54-argument activation baseline, ten completed depth targets, formal ownership map, frozen 44-record historical reader, released exact local 54-record successor, redirect hygiene, predecessor completion, no-public-release record, completion declaration, and one schema-bound active clean-handoff successor.",
        "input_artifacts": [
            "scripts/validate_post_v2_3_quality_floor_reader_completion_roadmap.py",
            "scripts/validate_chapter_source_hygiene.py",
            "scripts/register_post_v2_3_quality_floor_reader_completion_validators.py",
            "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md",
            "docs/post_v2_3_chapter_quality_packets.md",
            "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json",
            "schemas/post_v2_3_quality_floor_reader_completion_status.schema.json",
            "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md",
            "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json",
            "schemas/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.schema.json",
            "docs/post_v2_3_clean_handoff_receipt.md",
            "editions/reader_manuscript/v2_0/text_format_profile.json",
            "editions/reader_manuscript/v2_0/profiles/reader-v2-reference.docx",
            "editions/reader_manuscript/v2_0/format_review_matrix.json",
            "editions/reader_manuscript/v2_0/epub_disposition.json",
            "editions/reader_manuscript/v2_0/epub_structural_inspection.json",
            "editions/reader_manuscript/v2_0/epub_application_review.json",
            "editions/reader_manuscript/v2_0/epub_reproducibility.json",
            "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0.epub",
            "scripts/build_post_v2_3_reader_docx_reference.py",
            "docs/post_v2_2_implementation_completion_roadmap.md",
            "docs/v2_3_completion_declaration.md",
            "editions/reader_manuscript/v1_0/manifest.json",
            "book_structure.json",
            "sources/source_inventory.json",
            "evidence_quality/core_claim_vectors.json",
            "README.md", "index.qmd", "docs/publication_readiness.md", "docs/public_status_contract.md",
        ],
        "output_contract": "Reject incomplete or silently reopened roadmap authority, cohort or breadth drift, premature semantic/formal completion, borrowed-module completion, reader-denominator laundering, mutation of historical reader identity, undeclared chapter HTML, no-release/public-pointer drift, support promotion, or an external-human prepublication requirement.",
        "output_assertions": ["completed roadmap with one declared active successor", "frozen 54-chapter spine", "ten exact depth targets", "44-record historical reader preserved", "54-record successor released", "exact no-public-release decision", "ten declared redirects", "54 argument-state core claims", "ten rejecting mutations"],
        "claim_scope": "Terminal planning, quality-floor, formal-ownership, reader-identity, hygiene, no-release, and public-authority coherence for the post-v2.3 cycle.",
        "negative_controls": "validator_owned_and_surface_bound",
        "negative_control_cases": ["duplicate active roadmap", "missing target", "premature semantic completion", "borrowed module completion", "reader laundering", "support promotion", "breadth expansion", "undeclared HTML", "stale pointer", "external review requirement"],
        "prohibited_inference": "Roadmap completion does not itself prove chapter claims, model quality, safety, production transfer, AGI, ASI, or justify a public release or successor roadmap.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_contract_audit_not_independent",
    },
    {
        "script": "validate_scalable_oversight_protocol.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Seven frozen scalable-oversight use records, two schemas, deterministic route recomputation, exact result digest and counts, eight named Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": [
            "scripts/validate_scalable_oversight_protocol.py",
            "schemas/scalable_oversight_protocol_fixture.schema.json",
            "schemas/scalable_oversight_protocol_result.schema.json",
            "experiments/scalable_oversight_protocol/fixtures/cases.json",
            "experiments/scalable_oversight_protocol/results/2026-07-13-local.json",
            "lean/AsiStackProofs/ScalableOversight.lean",
            "chapters/scalable-oversight-and-adversarial-ai-control.qmd",
        ],
        "output_contract": "Reject missing or misrouted cases, access/dependency/baseline/audit/abstention/authority laundering, result or digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["seven deterministic routes", "eight named Lean theorems", "one bounded admission", "six rejecting controls", "no support movement", "eight rejecting mutations"],
        "claim_scope": "Finite scalable-oversight record routing and its Lean/JSON bridge only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "wrong route", "audit laundering", "authority laundering", "support promotion", "digest mismatch", "theorem erasure", "non-claim erasure"],
        "prohibited_inference": "The fixture does not establish reviewer independence, judge calibration, protocol efficacy, debate or weak-to-strong performance, model quality, alignment, safety, transfer, execution authority, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_model_weight_custody_lifecycle.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Eight frozen model-weight custody lifecycle records, two schemas, deterministic route recomputation, exact result digest and counts, nine named Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": [
            "scripts/validate_model_weight_custody_lifecycle.py",
            "schemas/model_weight_custody_lifecycle_fixture.schema.json",
            "schemas/model_weight_custody_lifecycle_result.schema.json",
            "experiments/model_weight_custody_lifecycle/fixtures/cases.json",
            "experiments/model_weight_custody_lifecycle/results/2026-07-13-local.json",
            "lean/AsiStackProofs/ModelWeightCustody.lean",
            "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd",
        ],
        "output_contract": "Reject missing or misrouted cases, lineage/policy/freshness/dependency/observation/authority laundering, result or digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["eight deterministic routes", "nine named Lean theorems", "one bounded load", "one irreversible-release record", "no support movement", "nine rejecting mutations"],
        "claim_scope": "Finite model-weight custody lifecycle record routing and its Lean/JSON bridge only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "wrong route", "stale-token laundering", "load-observation laundering", "release-authority laundering", "support promotion", "digest mismatch", "theorem erasure", "non-claim erasure"],
        "prohibited_inference": "The fixture does not establish hardware trustworthiness, attestation genuineness, verifier independence, weight confidentiality, extraction resistance, security effectiveness, model safety, readiness, deployment authority, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_open_ended_improvement_campaign.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Seven frozen open-ended-improvement campaign records, two schemas, deterministic route recomputation, exact result digest and counts, seven named owned Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": [
            "scripts/validate_open_ended_improvement_campaign.py",
            "schemas/open_ended_improvement_campaign_fixture.schema.json",
            "schemas/open_ended_improvement_campaign_result.schema.json",
            "experiments/open_ended_improvement_campaign/fixtures/cases.json",
            "experiments/open_ended_improvement_campaign/results/2026-07-13-local.json",
            "lean/AsiStackProofs/OpenEndedImprovement.lean",
            "chapters/open-ended-improvement-engines.qmd",
        ],
        "output_contract": "Reject missing or misrouted cases, qualification/budget/stop/archive/residual/authority laundering, result or digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["seven deterministic routes", "seven owned Lean theorems", "one governor-review handoff", "six blocked or repair routes", "no support movement", "ten rejecting mutations"],
        "claim_scope": "Finite open-ended-improvement campaign-record routing and its Lean/JSON bridge only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "wrong route", "qualification laundering", "budget laundering", "stop laundering", "authority laundering", "support promotion", "digest mismatch", "theorem erasure", "non-claim erasure"],
        "prohibited_inference": "The fixture does not establish campaign quality, evaluator independence or correctness, autonomous discovery, useful novelty, transfer, safe self-improvement, model quality, AGI, ASI, authority, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_inter_stack_exchange_contract.py",
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Nine frozen synthetic inter-stack exchange records, two schemas, deterministic route recomputation, exact digest and counts, nine owned Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_inter_stack_exchange_contract.py", "schemas/inter_stack_exchange_contract_fixture.schema.json", "schemas/inter_stack_exchange_contract_result.schema.json", "experiments/inter_stack_exchange_contract/fixtures/cases.json", "experiments/inter_stack_exchange_contract/results/2026-07-13-local.json", "lean/AsiStackProofs/InterStackProtocols.lean", "chapters/inter-stack-protocols-identity-and-economic-exchange.qmd"],
        "output_contract": "Reject missing or misrouted cases, identity/audience/revocation/budget/dispute laundering, result or digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["nine deterministic routes", "nine owned Lean theorems", "one bounded local-dispatch handoff", "eight denied/repair/review routes", "no support movement", "eleven rejecting mutations"],
        "claim_scope": "Finite synthetic inter-stack exchange-record routing and its Lean/JSON bridge only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "wrong route", "identity laundering", "audience laundering", "revocation laundering", "budget laundering", "dispute laundering", "support promotion", "digest mismatch", "theorem erasure", "non-claim erasure"],
        "prohibited_inference": "The fixture does not establish interoperability, peer trust, identity truth, credential validity, authorization correctness, task truth, payment, settlement, legality, fairness, privacy, security, runtime execution, AGI, ASI, authority, or support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_deliberation_admission.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Ten frozen synthetic deliberation records, two schemas, deterministic routes, exact digest and counts, ten owned Lean theorems, fifteen preserved harm cases, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_deliberation_admission.py", "schemas/deliberation_admission_fixture.schema.json", "schemas/deliberation_admission_result.schema.json", "experiments/deliberation_admission/fixtures/cases.json", "experiments/deliberation_admission/results/2026-07-13-local.json", "lean/AsiStackProofs/Deliberation.lean", "chapters/governed-deliberation-and-test-time-scaling.qmd"],
        "output_contract": "Reject missing/misrouted cases, history/trace/budget/verifier laundering, harm erasure, digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["ten deterministic routes", "ten owned Lean theorems", "fifteen harms preserved", "one planning handoff", "one exhaustion escrow", "no support movement", "eleven rejecting mutations"],
        "claim_scope": "Finite synthetic deliberation-record routing and regression-knowledge preservation only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "wrong route", "history laundering", "trace laundering", "budget laundering", "verifier laundering", "harm erasure", "support promotion", "digest mismatch", "theorem erasure", "nonclaim erasure"],
        "prohibited_inference": "The fixture does not establish evaluator validity, reasoning quality, trace faithfulness, test-time efficiency, safety, model quality, execution authority, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_capability_threshold_commitment.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Eight frozen synthetic threshold-commitment records, two schemas, deterministic routes, exact digest and counts, eight owned Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_capability_threshold_commitment.py", "schemas/capability_threshold_commitment_fixture.schema.json", "schemas/capability_threshold_commitment_result.schema.json", "experiments/capability_threshold_commitment/fixtures/cases.json", "experiments/capability_threshold_commitment/results/2026-07-13-local.json", "lean/AsiStackProofs/CapabilityThresholds.lean", "chapters/capability-thresholds-and-deployment-commitments.qmd"],
        "output_contract": "Reject missing or misrouted cases, digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["eight deterministic routes", "eight owned Lean theorems", "two readiness-review handoffs", "two blocked releases", "no support movement", "five rejecting mutations"],
        "claim_scope": "Finite synthetic threshold-commitment routing only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "digest mismatch", "support promotion", "theorem erasure", "nonclaim erasure"],
        "prohibited_inference": "The fixture does not establish capability, threshold adequacy, safeguard efficacy, institutional compliance, readiness, safety, deployment authority, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_adversarial_evaluation_integrity.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Eight frozen synthetic evaluation-integrity records, two schemas, deterministic routes, exact digest and counts, eight owned Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_adversarial_evaluation_integrity.py", "schemas/adversarial_evaluation_integrity_fixture.schema.json", "schemas/adversarial_evaluation_integrity_result.schema.json", "experiments/adversarial_evaluation_integrity/fixtures/cases.json", "experiments/adversarial_evaluation_integrity/results/2026-07-13-local.json", "lean/AsiStackProofs/AdversarialEvaluation.lean", "chapters/adversarial-evaluation-sandbagging-and-training-time-deception.qmd"],
        "output_contract": "Reject missing/misrouted cases, digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["eight deterministic routes", "eight owned Lean theorems", "one review handoff", "one quarantine", "one intent-laundering rejection", "no support movement", "five rejecting mutations"],
        "claim_scope": "Finite synthetic evaluation-integrity routing only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "digest mismatch", "support promotion", "theorem erasure", "nonclaim erasure"],
        "prohibited_inference": "The fixture does not detect deception, establish sandbagging resistance or reward-hacking causality, validate evaluators, infer capability or intent, establish alignment/safety, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_safety_case_assurance.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Eight frozen synthetic assurance-case records, two schemas, deterministic routes, exact digest and counts, eight owned Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_safety_case_assurance.py", "schemas/safety_case_assurance_fixture.schema.json", "schemas/safety_case_assurance_result.schema.json", "experiments/safety_case_assurance/fixtures/cases.json", "experiments/safety_case_assurance/results/2026-07-13-local.json", "lean/AsiStackProofs/SafetyCases.lean", "chapters/safety-cases-and-structured-assurance.qmd"],
        "output_contract": "Reject missing or misrouted cases, digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["eight deterministic routes", "eight owned Lean theorems", "one readiness-review handoff", "one evidence repair", "one accountable review", "one authority-laundering rejection", "no support movement", "five rejecting mutations"],
        "claim_scope": "Finite synthetic assurance-case record routing only.",
        "negative_controls": "validator_owned_and_fixture_bound",
        "negative_control_cases": ["missing case", "digest mismatch", "support promotion", "theorem erasure", "nonclaim erasure"],
        "prohibited_inference": "The fixture does not validate a safety case, hazard model, countercase search, evidence edge, control, reviewer independence, readiness, release, safety, AGI, ASI, authority, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_fixture_and_formal_audit_not_independent",
    },
    {
        "script": "validate_data_engine_full_state_bridge.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "The frozen P3 preregistration, 24-surface state inventory, three-seed/five-arm campaign result, digest-bound bridge summary, twelve owned full-state/unlearning Lean theorems, limitations, non-claims, and no support effect.",
        "input_artifacts": ["scripts/validate_data_engine_full_state_bridge.py", "schemas/data_engine_full_state_bridge_result.schema.json", "experiments/data_engine_full_state_bridge/results/2026-07-13-local.json", "experiments/post_v2_1_evidence_program/preregistration.json", "experiments/post_v2_1_evidence_program/p3/state_inventory.json", "experiments/post_v2_1_evidence_program/p3/results/result.json", "lean/AsiStackProofs/DataEngines.lean", "chapters/data-engines-continual-learning-and-unlearning.qmd"],
        "output_contract": "Reject preregistration loss, missing required state surfaces, rollback-result drift, digest drift, theorem erasure, support promotion, or non-claim erasure.",
        "output_assertions": ["24 prospectively declared state surfaces", "15/15 exact local rollbacks", "six best/final disagreements", "behavioral changes 4/0/1", "three lineage propagations", "zero storage erasures", "twelve owned Lean theorems", "no support movement", "six rejecting mutations"],
        "claim_scope": "Existing finite local P3 full-state update and unlearning-causality result bridge only.",
        "negative_controls": "validator_owned_and_campaign_bound",
        "negative_control_cases": ["state-surface erasure", "rollback laundering", "digest mismatch", "support promotion", "theorem erasure", "nonclaim erasure"],
        "prohibited_inference": "The bridge does not establish foundation-model continual learning, production rollback, influence reduction, privacy/legal/storage erasure, transfer, capability promotion, safety, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_campaign_and_formal_audit_not_independent",
    },
]

RENEWAL_UNITS = [
    {
        "script": "validate_post_v2_3_protocol_preflight.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "The immutable 36-output historical failure, two historical no-change transitions, one prospectively frozen four-task sacrificial split, separated 192/320-token reasoning/final protocol, exact preflight artifacts, evaluator replay, terminal/cost/latency capture, and no support effect.",
        "input_artifacts": ["scripts/build_post_v2_3_protocol_preflight.py", "scripts/run_post_v2_3_protocol_preflight.py", "scripts/post_v2_3_renewal_evaluator.py", "scripts/validate_post_v2_3_protocol_preflight.py", "experiments/post_v2_3_evidence_protocol_renewal/preflight/preregistration.json", "experiments/post_v2_3_evidence_protocol_renewal/preflight/tasks.json", "experiments/post_v2_3_evidence_protocol_renewal/preflight/attempt_1_result.json"],
        "output_contract": "Reject historical erasure, sacrificial-split leakage, exact artifact/evaluator drift, missing terminal/cost/arm capture, false pass state, or support promotion.",
        "output_assertions": ["36 historical outputs preserved", "two no-change transitions preserved", "four sacrificial tasks", "4/4 exact final JSON", "four planned arms captured", "five rejecting mutations"],
        "claim_scope": "Non-evidentiary protocol-operability preflight only.", "negative_controls": "validator_owned_and_preflight_bound",
        "negative_control_cases": ["denominator mutation", "parseability mutation", "arm erasure", "input drift", "support laundering"],
        "prohibited_inference": "Preflight success does not establish model quality, useful throughput, unsafe-release reduction, governance efficacy, safety, production transfer, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_sacrificial_protocol_audit_not_independent",
    },
    {
        "script": "validate_post_v2_3_governance_tax_flagship_freeze.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "One prospectively frozen 16-task, two-seed, 64-call flagship with label-isolated evaluation, matched candidate/authority routes, nine rollback surfaces, exact outcomes, and the required post-outcome 8/8-declared versus 9/9-exact metadata erratum.",
        "input_artifacts": ["scripts/build_post_v2_3_governance_tax_flagship_freeze.py", "scripts/run_post_v2_3_governance_tax_flagship.py", "scripts/post_v2_3_flagship_evaluator.py", "scripts/validate_post_v2_3_governance_tax_flagship_freeze.py", "experiments/post_v2_3_evidence_protocol_renewal/flagship/preregistration.json", "experiments/post_v2_3_evidence_protocol_renewal/flagship/tasks.json", "experiments/post_v2_3_evidence_protocol_renewal/flagship/evaluator_labels.json", "experiments/post_v2_3_evidence_protocol_renewal/flagship/results/program_result.json", "experiments/post_v2_3_evidence_protocol_renewal/flagship/results/adjudication.json"],
        "output_contract": "Reject frozen-file/result digest drift, call-budget expansion, label leakage, rollback/authority erasure, missing outcomes, or hidden family/attack metadata erratum.",
        "output_assertions": ["16 exact tasks", "32 exact candidate outputs", "64-call ceiling", "two seeds", "nine rollback surfaces", "declared 8/8 and actual 9/9 metadata retained"],
        "claim_scope": "Exact frozen flagship inputs, outputs, and erratum integrity only.", "negative_controls": "validator_and_exact_file_bound",
        "negative_control_cases": ["result digest drift", "budget expansion", "label leakage", "rollback erasure", "metadata erratum erasure"],
        "prohibited_inference": "Freeze/result integrity does not establish useful throughput, unsafe-release reduction, governance efficacy, safety, production rollback, model quality, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_campaign_with_label_isolated_evaluator_not_external",
    },
    {
        "script": "build_post_v2_3_governance_tax_flagship_adjudication.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "All 32 exact flagship candidates, 64 calls, deterministic evaluator receipts, route metrics, cost/latency/token/governance burden, 32 rollback probes, frozen promotion thresholds, metadata erratum, no-change transition, and non-claims.",
        "input_artifacts": ["scripts/build_post_v2_3_governance_tax_flagship_adjudication.py", "experiments/post_v2_3_evidence_protocol_renewal/flagship/results/program_result.json", "experiments/post_v2_3_evidence_protocol_renewal/flagship/results/adjudication.json", "docs/post_v2_3_governance_tax_flagship_renewal_results.md", "evidence_transitions/post_v2_3/governance_tax_natural_work_renewal_no_change.json"],
        "output_contract": "Reject promotion, denominator drift, useful/unsafe outcome laundering, rollback inflation, metadata-error erasure, failed-threshold reversal, or support movement.",
        "output_assertions": ["32/32 candidates", "64/64 calls", "2/32 independently correct", "zero useful releases", "zero unsafe releases", "32 exact rollbacks", "no-change disposition", "five rejecting mutations"],
        "claim_scope": "Exact bounded negative governance-tax outcome and no-change disposition only.", "negative_controls": "validator_owned_and_outcome_bound",
        "negative_control_cases": ["promotion", "denominator shrink", "metadata erasure", "unsafe threshold reversal", "support laundering"],
        "prohibited_inference": "The negative result does not establish safety, governance efficacy, model quality, production rollback, useful throughput, external independence, AGI, ASI, or core support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_outcome_adjudication_not_independent",
    },
    {
        "script": "validate_theseus_pretraining_readiness_currentness_import.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "One clean same-commit d2343540 temporary-output Project Theseus readiness-gate replay, three source-file and four output digests, exact 20-phase YELLOW summary, partial/frozen residuals, public-safety filter, non-claims, and no support/release effect.",
        "input_artifacts": ["scripts/build_theseus_pretraining_readiness_currentness_import.py", "scripts/validate_theseus_pretraining_readiness_currentness_import.py", "experiments/theseus_pretraining_readiness_currentness_import/results/2026-07-14-local.json", "docs/theseus_pretraining_readiness_currentness_import.md"],
        "output_contract": "Reject source-commit/cleanliness drift, failed replay, digest drift, partial/frozen erasure, private payload inclusion, YELLOW-to-GREEN laundering, support promotion, or release overclaim.",
        "output_assertions": ["same clean d2343540 commit before/after", "20 phases", "12 wired", "2 implemented", "5 partial", "1 frozen", "YELLOW boundary", "four output digests", "eight rejecting mutations"],
        "claim_scope": "Exact sanitized implementation-reference currentness observation only.", "negative_controls": "validator_owned_and_import_bound",
        "negative_control_cases": ["commit mismatch", "dirty checkout", "digest mismatch", "partial erasure", "private copy", "release overclaim", "support overclaim", "YELLOW erasure"],
        "prohibited_inference": "The import does not establish current behavior after d2343540, learned model quality, benchmark superiority, training success, deployment readiness, distributed operation, safety, alignment, transfer, AGI, ASI, or support movement.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "author_owned_local_project_import_not_external_replication",
    },
]


TERMINAL_UNITS = [
    {
        "script": "build_post_v2_3_evidence_candidate_ledger.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Twenty-one completed post-v2, post-v2.1, and QCSA candidate claims, exact result digests, accepted transition records, counterevidence, transfer limits, and frozen chapter-core states.",
        "input_artifacts": ["scripts/build_post_v2_3_evidence_candidate_ledger.py", "schemas/post_v2_3_evidence_candidate_ledger.schema.json", "docs/post_v2_3_evidence_candidate_ledger.json", "docs/post_v2_3_evidence_candidate_ledger.md"],
        "output_contract": "Reject denominator, digest, disposition, transition, chapter-owner, support-state, or non-claim drift.",
        "output_assertions": ["21 candidates", "five promote", "eight narrow", "six no-change", "two refute", "21 accepted transitions", "zero chapter-core movement", "five rejecting mutations"],
        "claim_scope": "Exact bounded evidence-candidate adjudication only.", "negative_controls": "validator_owned_and_transition_bound",
        "negative_control_cases": ["candidate omission", "digest drift", "unsupported disposition", "missing transition", "core promotion"],
        "prohibited_inference": "Candidate adjudication does not generalize a fixture result, establish production transfer, or promote a chapter-core claim.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_evidence_adjudication_not_independent",
    },
    {
        "script": "build_post_v2_3_campaign_preregistration.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Frozen natural-work and residual-pressure workloads, pinned model revision, budgets, evaluator boundaries, effect-complete local rollback inventory, stop rules, transition rules, and no support effect.",
        "input_artifacts": ["scripts/build_post_v2_3_campaign_preregistration.py", "schemas/post_v2_3_campaign_preregistration.schema.json", "experiments/post_v2_3_evidence_campaigns/preregistration.json"],
        "output_contract": "Reject post-outcome workload, model, budget, evaluator, rollback, transition-rule, or support-state drift.",
        "output_assertions": ["12 natural-work tasks", "six residual scenarios", "four conditions", "36-call ceiling", "90-minute ceiling", "five rejecting mutations"],
        "claim_scope": "Prospective campaign authority only.", "negative_controls": "validator_owned_and_preregistration_bound",
        "negative_control_cases": ["model substitution", "budget expansion", "task deletion", "rollback omission", "promotion-rule weakening"],
        "prohibited_inference": "Preregistration is not a campaign result, model-quality finding, safety result, or evidence promotion.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "prospective_internal_protocol_review_not_independent",
    },
    {
        "script": "build_post_v2_3_campaign_adjudication.py",
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "All 36 frozen model outputs, evaluator specs and receipts, exact digests, cost records, governance and residual denominators, rollback probes, and preregistered transition rules.",
        "input_artifacts": ["scripts/build_post_v2_3_campaign_adjudication.py", "schemas/post_v2_3_campaign_adjudication.schema.json", "experiments/post_v2_3_evidence_campaigns/results/adjudication.json", "docs/post_v2_3_campaign_results.md", "evidence_transitions/post_v2_3/governance_tax_natural_work_no_change.json", "evidence_transitions/post_v2_3/residual_honesty_under_pressure_no_change.json"],
        "output_contract": "Reject raw-output or evaluator drift, capped-reasoning laundering, zero-release safety inference, rollback inflation, support movement, or loss of either no-change disposition.",
        "output_assertions": ["36 capped outputs", "34 unclosed reasoning blocks", "two closed without final JSON", "zero structured candidates", "two no-change dispositions", "12 exact rollback probes", "five rejecting mutations"],
        "claim_scope": "Exact local campaign protocol outcome and no-change adjudication only.", "negative_controls": "validator_owned_and_raw_output_bound",
        "negative_control_cases": ["parseable-output laundering", "promotion", "rollback inflation", "raw disclosure laundering", "support movement"],
        "prohibited_inference": "The failed protocol does not establish model quality, safety, useful throughput, governance efficacy, residual honesty, production transfer, AGI, ASI, or core support.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_campaign_adjudication_with_separate_subprocess_evaluator_not_external",
    },
    {
        "script": "build_post_v2_3_cycle_no_release_record.py",
        "execution_tier": "deep", "validation_class": "publication_gate",
        "input_contract": "Completed roadmap artifacts, exact local reader release record/archive, candidate and campaign dispositions, immutable v2.3.0 identity, and explicit zero-publication effects.",
        "input_artifacts": ["scripts/build_post_v2_3_cycle_no_release_record.py", "schemas/post_v2_3_cycle_no_release_record.schema.json", "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json"],
        "output_contract": "Reject false release, deployment, tag, archive, rights, source-commit, support, reader-digest, or closure-artifact claims.",
        "output_assertions": ["v2.3.0 remains latest public", "exact local reader preserved", "zero publication effects", "54 argument cores", "five rejecting mutations"],
        "claim_scope": "Exact terminal no-public-living-book-release transaction only.", "negative_controls": "validator_owned_and_closure_digest_bound",
        "negative_control_cases": ["false release", "false deployment", "support promotion", "reader digest drift", "artifact omission"],
        "prohibited_inference": "No-release closure does not publish, deploy, tag, grant rights, or establish model, safety, AGI, ASI, or support claims.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_release_decision_audit_not_independent",
    },
    {
        "script": "validate_post_v2_3_cycle_closure.py",
        "execution_tier": "deep", "validation_class": "publication_gate",
        "input_contract": "Terminal roadmap/status/declaration, no-public-release transaction, exact local reader, candidate and campaign adjudications, 54 core vectors, closure digests, and reconciled public surfaces.",
        "input_artifacts": ["scripts/validate_post_v2_3_cycle_closure.py", "docs/post_v2_3_quality_floor_reader_completion_declaration.md", "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json", "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json", "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md", "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"],
        "output_contract": "Reject incomplete or reopened work, hidden active roadmap, reader deployment laundering, campaign reasoning laundering, support promotion, closure digest drift, or stale public truth.",
        "output_assertions": ["P0-P5 completed", "M0-M9 completed", "one declared active successor", "54-chapter local reader", "21 candidate dispositions", "two campaign no-change dispositions", "v2.3.0 latest public", "six rejecting mutations"],
        "claim_scope": "Cross-surface terminal closure coherence only.", "negative_controls": "validator_owned_and_terminal_surface_bound",
        "negative_control_cases": ["reopened roadmap", "hidden successor", "release laundering", "reasoning laundering", "support promotion", "reader deployment laundering"],
        "prohibited_inference": "Closure coherence does not establish model quality, safety, production readiness, governance efficacy, residual honesty, AGI, ASI, or public publication.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_terminal_audit_not_independent",
    },
]


def upsert(registry: dict, spec: dict) -> dict:
    matches = [row for row in registry["units"] if row["script"] == spec["script"] and row.get("args", []) == []]
    if matches:
        unit = matches[0]
    else:
        order = len(registry["units"]) + 1
        unit = {"id": f"{spec['script'].removesuffix('.py')}:{order}", "order": order, "script": spec["script"], "args": []}
        registry["units"].append(unit)
    unit.update({key: value for key, value in spec.items() if key != "script"})
    for artifact in spec["input_artifacts"]:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    return unit


def sync_override(overrides: dict, unit: dict) -> None:
    existing = next((row for row in overrides["contracts"] if row["script"] == unit["script"] and row.get("args", []) == []), None)
    record = {"script": unit["script"], "args": [], **{field: unit[field] for field in CONTRACT_FIELDS}}
    if existing is None:
        overrides["contracts"].append(record)
    else:
        existing.clear()
        existing.update(record)


def update_historical_units(registry: dict, overrides: dict) -> None:
    additions = [
        "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md",
        "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json",
        "schemas/post_v2_3_quality_floor_reader_completion_status.schema.json",
        "docs/post_v2_3_quality_floor_reader_completion_declaration.md",
        "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json",
        "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md",
        "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json",
        "schemas/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.schema.json",
    ]
    for script in ["validate_post_v2_1_public_truth.py", "validate_post_v2_2_implementation_completion_roadmap.py"]:
        unit = next(row for row in registry["units"] if row["script"] == script and row.get("args", []) == [])
        for artifact in additions:
            if artifact not in unit["input_artifacts"]:
                unit["input_artifacts"].append(artifact)
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
        unit["input_contract"] = unit["input_contract"].replace("with one declared later active successor", "with a completed later successor and one declared current successor")
        unit["input_contract"] = unit["input_contract"].replace("with a completed later successor and no active roadmap", "with a completed later successor and one declared current successor")
        unit["output_contract"] = unit["output_contract"].replace("missing or multiple later active identities", "stale, reopened, or multiple active identities")
        unit["output_assertions"] = [
            item.replace("with one declared later active successor", "with a completed later successor and one declared current successor")
                .replace("with a completed later successor and no active roadmap", "with a completed later successor and one declared current successor")
                .replace("no active successor", "one declared current successor")
            for item in unit["output_assertions"]
        ]
        sync_override(overrides, unit)


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    update_historical_units(registry, overrides)
    for spec in NEW_UNITS + READER_UNITS + RENEWAL_UNITS + TERMINAL_UNITS:
        sync_override(overrides, upsert(registry, spec))
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered post-v2.3 quality-floor gates: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
