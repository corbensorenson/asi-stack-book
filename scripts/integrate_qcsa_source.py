#!/usr/bin/env python3
"""Integrate the QCSA author whitepaper into the existing chapter architecture."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "sources" / "source_inventory.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCE_ID = "qcsa_whitepaper"


TARGETS = {
    "cognitive-compilation-and-semantic-ir": {
        "support": "Frames SOIDs and SACs as typed semantic-IR references, question traces as evidence-acquisition programs, and semantic-to-physical route plans as policy-constrained target lowering.",
        "limits": "Conceptual compiler contract only; no QCSA compiler, semantic-preservation result, question-policy result, or route-lowering implementation is supplied.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:278-487",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1377-1384",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1557-1586",
        ],
    },
    "virtual-context-abi": {
        "support": "Adds stable SOID identity, plural contextual SVA leases, atlas epochs, SAC adequacy and residual fields, bounded graph materialization, revalidation triggers, and explicit failure when semantic uncertainty is insufficient for a consumer.",
        "limits": "Does not establish context adequacy, retrieval quality, semantic correctness, VCM safety, or a working SAC/atlas service.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:220-375",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:572-741",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1492-1534",
        ],
    },
    "routing-heads-and-specialist-cores": {
        "support": "Separates semantic identity and address selection from the physical expert/model route, while making fallback, abstention, load, cost, hardware, permissions, and verifier requirements explicit in the compiled route plan.",
        "limits": "Does not establish specialist-routing accuracy, useful throughput, load balance, transfer, latency, or production safety.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:354-366",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:668-792",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1194-1240",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1389-1396",
        ],
    },
    "compact-generative-systems-and-residual-honesty": {
        "support": "Extends Semantic Representation Leasing with plural address leases, path deltas, open-world expressions, semantic-first generation, round-trip structural checks, consumer adequacy, and explicit collision, verification, migration, repair, and fallback residuals.",
        "limits": "Does not demonstrate compression, reconstruction, model quality, semantic preservation, latency, or any advantage over direct generation.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:268-270",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:572-666",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:794-856",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1093-1110",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1241-1269",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1397-1400",
        ],
    },
    "runtime-adapters-tool-permissions-and-human-approval": {
        "support": "Adds the hard capability-separation rule: semantic resolution, aliases, address confidence, and certificates never grant authority; the physical route must independently bind actor, target, operation, scope, policy, data, reversibility, approvals, and receipts.",
        "limits": "A proposed route contract does not establish permission correctness, effect safety, rollback, human-approval quality, or runtime enforcement.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:751-790",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1012-1092",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1393-1396",
        ],
    },
    "claim-ledgers-and-belief-revision": {
        "support": "Requires ontology, propositions, evidence for and against propositions, provenance, belief/support state, contradiction, and permitted-use authority to remain distinct semantic records in the evidence-bearing hypergraph.",
        "limits": "A semantic location, address confidence, or valid certificate does not establish proposition truth, evidential support, belief correctness, or ontology completeness.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:307-317",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:543-570",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1075-1078",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1385-1388",
        ],
    },
    "data-engines-continual-learning-and-unlearning": {
        "support": "Contributes fast/medium/slow update timescales, candidate versus authoritative atlas epochs, identity-preserving readdressing, merge/split lineage, migration compatibility, shadow evaluation, rollback, and semantic-drift tests.",
        "limits": "Does not establish learning quality, forgetting, cohort removal, causal influence removal, privacy erasure, storage erasure, or safe self-reorganization.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:264-270",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:523-540",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:858-947",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1079-1092",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1255-1269",
        ],
    },
    "inter-stack-protocols-identity-and-economic-exchange": {
        "support": "Supplies namespace-qualified stable identities, signed SACs, atlas epochs, mapping manifests, migration lineage, and uncertainty-preserving translation as candidate cross-stack semantic exchange records.",
        "limits": "Cross-stack semantic translation does not establish identity equivalence, trust, authorization, proposition truth, effect safety, payment settlement, privacy, or economic fairness.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:523-540",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1020-1059",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1405-1409",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1463-1555",
        ],
    },
    "integrated-reference-architecture": {
        "support": "Defines QCSA as the semantic control plane connecting grounding, context, planning, memory, claims, routing, tools, generation, evidence acquisition, lifecycle migration, governance, and execution receipts through identity-address-route indirection.",
        "limits": "Reference architecture only; it does not establish an end-to-end QCSA system, benchmark, proof of semantic correctness, production transfer, safety result, AGI, or ASI capability.",
        "refs": [
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:272-487",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1373-1409",
            "sources/raw/question_compiled_semantic_addressing_whitepaper.md:1557-1586",
        ],
    },
}


SOURCE_RECORD = {
    "id": SOURCE_ID,
    "title": "Question-Compiled Semantic Addressing",
    "priority": "must_use",
    "layer": "semantic_addressing_control_plane",
    "chapter_targets": list(TARGETS),
    "url": "local-source:sources/raw/question_compiled_semantic_addressing_whitepaper.md@sha256:d9e594d40dfd62c899ab25e9d395d34c702dac12e8afd75eed133392f78c0c8c",
    "notes": "Corben-authored successor synthesis for stable semantic identity, plural versioned semantic virtual addresses, active question compilation, evidence-bearing hypergraphs, semantic address certificates, semantic-to-physical routing, lifecycle-safe migration, and explicit residuals. Conceptual architecture only; no implementation, benchmark, proof, safety validation, or performance advantage.",
    "source_type": "author_whitepaper",
    "published": "2026-07-12",
    "updated": "2026-07-12",
    "citation_label": "Sorenson (2026), Question-Compiled Semantic Addressing",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    inventory = load(INVENTORY)
    if not isinstance(inventory, list):
        raise TypeError("source inventory must be a list")
    existing = next((row for row in inventory if row.get("id") == SOURCE_ID), None)
    if existing is None:
        inventory.append(SOURCE_RECORD)
    elif existing != SOURCE_RECORD:
        existing.clear()
        existing.update(SOURCE_RECORD)

    structure = load(STRUCTURE)
    seen = set()
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            chapter_id = chapter.get("id")
            if chapter_id not in TARGETS:
                continue
            seen.add(chapter_id)
            source_ids = chapter.setdefault("source_ids", [])
            if SOURCE_ID not in source_ids:
                source_ids.append(SOURCE_ID)
            rows = chapter.setdefault("claim_source_mappings", [])
            mapping = TARGETS[chapter_id]
            value = {
                "source_id": SOURCE_ID,
                "mapped_support": mapping["support"],
                "limits": mapping["limits"],
                "passage_review_state": "reviewed",
                "passage_refs": mapping["refs"],
                "passage_review_note": "Reviewed the complete local Corben-authored QCSA whitepaper for the named chapter interface, formal contract, failure modes, baselines, evaluation gates, and non-claims; the mapping remains design rationale at argument support.",
            }
            prior = next((row for row in rows if row.get("source_id") == SOURCE_ID), None)
            if prior is None:
                rows.append(value)
            else:
                prior.clear()
                prior.update(value)

    missing = set(TARGETS) - seen
    if missing:
        raise KeyError(f"missing QCSA chapter targets: {sorted(missing)}")
    write(INVENTORY, inventory)
    write(STRUCTURE, structure)
    print(f"Integrated {SOURCE_ID} into {len(seen)} existing chapters; chapter count unchanged.")


if __name__ == "__main__":
    main()
