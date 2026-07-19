#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p7_book_evidence_reconciliation.py"
ARTIFACTS = [
    "scripts/reconcile_p7_chapter_evidence.py",
    "scripts/build_p7_book_evidence_reconciliation.py",
    "scripts/validate_p7_book_evidence_reconciliation.py",
    "scripts/register_p7_book_evidence_reconciliation.py",
    "schemas/p7_book_evidence_reconciliation.schema.json",
    "experiments/p7_book_evidence_reconciliation/result.json",
    "experiments/p7_book_evidence_reconciliation/lineage_lock.json",
    "docs/p7_book_evidence_reconciliation.md",
    "experiments/claim_family_terminal_coverage/results/result.json",
    "experiments/claim_family_bundle_coverage/result.json",
    "experiments/p6_external_reproduction/results/terminal_result.json",
    "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "book_structure.json",
    "sources/source_inventory.json",
    "evidence_quality/core_claim_vectors.json",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/E_codex_test_specs.qmd",
    "appendices/F_changelog.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "appendices/K_implementation_horizons.qmd",
    "sources/source_notes/ext_gated_deltanet2_2026.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used_orders = {row["order"] for row in value["units"]}
    order = next(number for number in range(1, len(value["units"]) + 2) if number not in used_orders)
    value["units"].append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": (
                "Activation-frozen 55-chapter/316-source P7 result and schema identity, the unchanged "
                "later contaminated-current 326-source projection explicitly treated as non-authoritative, exact historical "
                "packet blocks and frozen terminal/family/P6 dependencies, plus manifest/status-derived "
                "live chapters, sources, vectors, governed appendices, and reader projection."
            ),
            "input_artifacts": ARTIFACTS,
            "output_contract": (
                "Preserve activation-era P7 facts and digests without rebinding them to mutable live files; "
                "pin the later contaminated-current 326-source projection only as an amendment; validate the evolving live book, "
                "source inventory, argument-level cores, governed appendices, comparator/P6 boundaries, and "
                "reader projection dynamically with zero core movement."
            ),
            "output_assertions": [
                "activation-frozen 55 chapters and 316 sources",
                "later contaminated-current 326-source projection pinned but non-authoritative",
                "3,745 atom denominator and 3,698 blocked gaps",
                "55 exact historical P7 packet blocks preserved",
                "live manifest, source inventory, and argument-core counts agree dynamically",
                "current governed appendices validate semantically",
                "reader projection replays",
                "32 mutations reject",
            ],
            "claim_scope": "Historical P7 identity plus live book/evidence continuation only.",
            "negative_controls": "validator_owned_32_historical_amendment_and_live_laundering_mutations",
            "negative_control_cases": [
                "historical denominator, identity, path, ordering, digest, packet, and disposition drift",
                "completed-contract and terminal-ledger drift",
                "later-projection rebind or scope expansion",
                "live chapter deletion, reordering, or authority escape",
                "source duplication, replacement, or comparator laundering",
                "historical packet erasure, rewrite, or post-P7 laundering",
                "Appendix C/E/H/K semantic erasure",
                "live status/vector core promotion and count drift",
            ],
            "prohibited_inference": (
                "Historical or live packet, appendix, vector, reader, or render coverage does not prove "
                "chapter truth, external reproduction, transfer, SOTA, reader approval, publication, or release."
            ),
            "contract_precision": "exact_historical_identity_dynamic_live_semantics",
            "semantic_review_state": (
                "checked_activation_provenance_later_projection_scope_exact_packet_blocks_terminal_crosswalk_"
                "live_authority_source_appendices_vectors_and_reader_projection"
            ),
        }
    )
    required = list(value["required_artifacts"])
    for relative in ARTIFACTS:
        if relative not in required:
            required.append(relative)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(value["units"]),
    }
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
