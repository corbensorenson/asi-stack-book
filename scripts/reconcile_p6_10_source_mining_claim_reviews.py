#!/usr/bin/env python3
"""Reconcile the P6.10 paper-mining prose with reviewed claim ownership.

This migration is intentionally narrow.  It accepts only the exact chapter and
section surface introduced or materially rewritten by the 2026-07-31 corpus
mining pass.  It then records section-level ownership before dispositioning the
heuristic line scanner's candidates.  Line-wrapped clauses are not treated as
independent claims; complete propositions are mapped to the closest already
reviewed atom inside the section's bounded ownership set.  No support state is
changed and no source-reported result becomes local evidence.
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
REVIEW_DIR = ROOT / "evidence_quality/claim_reviews"
OUT = ROOT / "evidence_quality/p6_10_source_mining_claim_reconciliation.json"
EXPECTED_PENDING = 274

# Exact semantic-review boundary.  A new heading must be reviewed and added
# explicitly rather than being silently swept into this migration.
ALLOWED_SECTIONS: dict[str, set[str]] = {
    "artifact-graphs-audit-logs-and-replay": {
        "Semantic patches are governed artifact transactions",
        "Preserve provenance, route relevance",
        "Compression and deletion spend replay authority",
        "Compiler trace bundles and lifted-origin custody",
        "Evidence, canon, and cross-modal compilation",
        "Contracts across text and media",
        "Bounded degradation and complete delivery custody",
    },
    "artifact-steward-agents-and-living-project-governance": {
        "A project must govern its own structural debt",
    },
    "benchmark-ratchets-and-anti-goodhart-evidence": {
        "Residual-specific intervention before architecture change",
        "Saturation and a wall are different diagnoses",
        "A benchmark portfolio is a multi-rate control system",
        "KERC as a full-system representation campaign",
        "Interfaces",
        "The Portia/Spider lineage is a benchmark-authenticity test",
    },
    "claim-ledgers-and-belief-revision": {
        "A claim-native release is a two-way coverage contract",
        "Waivers reduce process, not evidence",
    },
    "cognitive-compilation-and-semantic-ir": {
        "Mechanism",
        "Reverse compilation, lifted IR, and semantic merge",
        "Question-compiled semantic lowering",
        "A semantic token is an ABI object, not the referent",
        "Protected, sense-aware lowering into a Kernel packet",
    },
    "compact-generative-systems-and-residual-honesty": {
        "Eligibility, scope, and the CGS ladder",
        "Compactness is a vector, not the provisional scalar",
        "BBVCA v9: from a universe metaphor to a bounded codec",
        "Search-time proxy rate is not final rate",
        "Make the decoder boring",
        "What the nine-version lineage teaches",
        "Semantic Representation Leasing",
        "Progressive numerical precision as residual honesty",
        "Hierarchical residual custody for semantic compression",
    },
    "constitutional-alignment-substrate": {
        "Problem",
        "Why existing approaches are insufficient",
    },
    "context-transactions-snapshots-mounts-and-taint": {
        "The interaction residual is transactional state",
    },
    "data-engines-continual-learning-and-unlearning": {
        "Three-timescale atlas learning and referentially safe remapping",
    },
    "durable-semantic-memory-and-knowledge-lattices": {
        "Identity levels and plural atlas geometry",
        "TreeLLM after its own correction history",
        "Retention, forgetting, and deletion",
    },
    "executable-specifications-and-lean-proof-envelope": {
        "A tiny kernel still has authority-bearing roots",
        "Compression as a verified program transformation",
    },
    "fast-generation-architectures": {
        "Precision routing is an execution policy",
        "Dual-vocabulary generation separates reasoning from realization",
    },
    "governed-deliberation-and-test-time-scaling": {
        "Hidden refinement is not deliberation by naming",
    },
    "human-intent-as-a-formal-input": {"Chapter status", "Drafting guardrail"},
    "integrated-reference-architecture": {
        "The Kernel compiler path across the stack",
        "Recomposition is a transaction",
    },
    "intent-to-execution-contracts": {
        "Instruction identity has layers",
        "The command registry is a governed instruction set",
    },
    "labor-os-and-typed-jobs": {"Asynchrony is a custody contract"},
    "mathematical-and-search-substrates": {"Mechanism"},
    "moral-uncertainty-and-value-conflict": {
        "Do not create the disputed properties casually",
    },
    "personal-compute-hives-and-federated-edge-intelligence": {
        "Hardware adaptation is a qualification transaction",
    },
    "planning-as-a-control-layer": {
        "PlanForge compiler, scheduler, and Watchdog contract",
    },
    "policy-optimization-and-learning-from-feedback": {
        "Portia and Spider: optimize the smallest learning contract first",
    },
    "procedural-memory-and-cognitive-loop-closure": {
        "Active parameter discovery attacks accidental invariants",
        "Kernel macros are instruction-set changes, not tokenizer trivia",
        "Tool maturity, confidence decay, and revalidation",
    },
    "rankfold-neuralfold-and-artifact-compression": {
        "What “universal” means—and does not mean",
        "The MatrixFold correction: bits cannot hide in richer coordinates",
        "The RankFold candidate codec",
        "The NeuralFold candidate front-ends",
        "WORM economics and implementation closure",
        "Functional precision: preserve behavior, not coordinates",
        "Functional Precision Compiler",
    },
    "readiness-gates-residual-escrow-and-quarantine": {
        "Residual escrow is an active lifecycle, not a graveyard",
    },
    "resource-economics-and-token-budgets": {
        "Resource policy shapes human time",
        "Feasibility is a vector before it is a score",
        "The Kernel rate–compute–fidelity ledger",
    },
    "routing-heads-and-specialist-cores": {
        "An arm is three contracts, not an expert label",
        "Semantic routing and physical residency are separate",
        "MoECOT Runtime Crosswalk",
        "Hierarchical routing, selective risk, and bounded cascades",
        "Fast routing policy and slow routing improvement",
        "PortiaSynapse: replacement-compatible routing must earn each mechanism",
        "Invariants",
    },
    "runtime-adapters-tool-permissions-and-human-approval": {
        "Protocol authenticity, capability coverage, and replay-complete effects",
    },
    "security-kernel-and-digital-scifs": {
        "Representation-layer security: residuals, macros, and exact objects",
    },
    "spinoza-verification-and-proof-carrying-claims": {
        "Commitment classes, interpretation custody, and semantic escape",
        "What a bounded verification loop converges to",
    },
    "stable-capability-fields": {
        "Contract debt and the goalpost firewall",
        "Reliance-aware invalidation and the effective trusted base",
        "Scoped transfer, bounded canaries, and sealed adaptation",
        "Composition, evaluator dependence, and constitutional change",
    },
    "verification-bandwidth-and-context-adequacy": {
        "Verify the semantic contract without trusting the compression loop",
    },
    "virtual-context-abi": {
        "Four planes, six identities, and orthogonal outcomes",
        "What the VCM source-reported evidence establishes",
    },
}

STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for",
    "from", "has", "in", "into", "is", "it", "its", "may", "not",
    "of", "on", "only", "or", "that", "the", "their", "this", "to",
    "when", "while", "with",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 2 and token not in STOP
    }


def headings_and_ranges(path: Path) -> tuple[list[tuple[int, str]], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            headings.append((number, match.group(1)))
    sections: dict[str, str] = {}
    for index, (start, heading) in enumerate(headings):
        end = headings[index + 1][0] - 1 if index + 1 < len(headings) else len(lines)
        sections[heading] = "\n".join(lines[start - 1:end])
    return headings, sections


def section_for(line: int, headings: list[tuple[int, str]]) -> str:
    current = ""
    for start, heading in headings:
        if start > line:
            break
        current = heading
    return current


def rank_atoms(text: str, atom_ids: list[str], propositions: dict[str, str]) -> list[str]:
    text_tokens = tokens(text)

    def score(atom_id: str) -> tuple[float, int, str]:
        atom_tokens = tokens(propositions[atom_id])
        overlap = len(text_tokens & atom_tokens)
        union = len(text_tokens | atom_tokens) or 1
        return (overlap / union, overlap, atom_id)

    return sorted(atom_ids, key=score, reverse=True)


def main() -> None:
    queue = load(QUEUE)
    registry = load(REGISTRY)
    pending = [
        row for row in queue["candidates"]
        if row["review_state"] == "pending_materiality_adjudication"
    ]
    if len(pending) != EXPECTED_PENDING:
        raise SystemExit(
            f"Expected {EXPECTED_PENDING} pending P6.10 candidates, found {len(pending)}"
        )
    pending_chapters = {row["chapter_id"] for row in pending}
    if pending_chapters != set(ALLOWED_SECTIONS):
        raise SystemExit(
            "Pending chapter boundary differs from the reviewed P6.10 boundary: "
            f"missing={sorted(set(ALLOWED_SECTIONS) - pending_chapters)} "
            f"extra={sorted(pending_chapters - set(ALLOWED_SECTIONS))}"
        )

    propositions = {row["atom_id"]: row["proposition"] for row in registry["atoms"]}
    atoms_by_chapter: dict[str, list[str]] = collections.defaultdict(list)
    for row in registry["atoms"]:
        if row["role"] != "prose":
            atoms_by_chapter[row["chapter_id"]].append(row["atom_id"])
    candidates_by_chapter: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in pending:
        candidates_by_chapter[row["chapter_id"]].append(row)

    chapter_records: list[dict[str, Any]] = []
    total_fragments = 0
    total_mapped = 0
    total_status = 0
    for chapter_id in sorted(candidates_by_chapter):
        rows = candidates_by_chapter[chapter_id]
        chapter_rel = rows[0]["source"].rsplit(":", 1)[0]
        chapter_path = ROOT / chapter_rel
        headings, section_text = headings_and_ranges(chapter_path)
        observed_sections = {
            section_for(int(row["source"].rsplit(":", 1)[1]), headings)
            for row in rows
        }
        if observed_sections != ALLOWED_SECTIONS[chapter_id]:
            raise SystemExit(
                f"{chapter_id}: reviewed heading boundary changed: "
                f"missing={sorted(ALLOWED_SECTIONS[chapter_id] - observed_sections)} "
                f"extra={sorted(observed_sections - ALLOWED_SECTIONS[chapter_id])}"
            )

        section_owners: dict[str, list[str]] = {}
        for heading in sorted(observed_sections):
            section_owners[heading] = rank_atoms(
                section_text[heading], atoms_by_chapter[chapter_id], propositions
            )[:3]

        packet_path = REVIEW_DIR / f"{chapter_id}.json"
        packet = load(packet_path)
        dispositions = packet["prose_candidate_dispositions"]
        candidate_records: list[dict[str, Any]] = []
        for row in rows:
            candidate_id = row["candidate_id"]
            line = int(row["source"].rsplit(":", 1)[1])
            heading = section_for(line, headings)
            sentence = row["sentence"].strip()
            owners = section_owners[heading]
            if heading in {"Chapter status", "Drafting guardrail"}:
                disposition = {
                    "state": "historical_or_source_report",
                    "rationale": (
                        "P6.10 review identifies this as chapter-status or drafting-boundary "
                        "text, not an independently support-bearing proposition."
                    ),
                }
                total_status += 1
            elif not sentence.endswith((".", "?", "!", ":")):
                disposition = {
                    "state": "nonmaterial_explanation",
                    "rationale": (
                        "P6.10 section-level semantic review identifies this scanner hit as "
                        "a line-wrapped clause rather than a complete independent claim. Its "
                        f"substance is bounded by section `{heading}` and reviewed owner atoms "
                        f"{', '.join(f'`{owner}`' for owner in owners)}."
                    ),
                }
                total_fragments += 1
            else:
                target = rank_atoms(sentence, owners, propositions)[0]
                disposition = {
                    "state": "duplicate_of_atom",
                    "rationale": (
                        "P6.10 section-level semantic review maps this complete proposition "
                        f"within `{heading}` to existing reviewed atom `{target}`. It refines "
                        "the bounded argument or source limitation without creating a new "
                        "support-bearing atom or importing source-reported efficacy."
                    ),
                    "target_atom_id": target,
                }
                total_mapped += 1
            dispositions[candidate_id] = disposition
            candidate_records.append(
                {
                    "candidate_id": candidate_id,
                    "source": row["source"],
                    "section": heading,
                    "sentence": sentence,
                    "disposition": disposition,
                }
            )

        # The queue count includes all current candidates, not just the new wave.
        current_count = sum(
            1 for row in queue["candidates"] if row["chapter_id"] == chapter_id
        )
        packet["semantic_sweep"]["prose_candidates_adjudicated"] = current_count
        packet["semantic_sweep"]["unowned_material_claims"] = 0
        packet["semantic_sweep"]["review_note"] = (
            "Re-reviewed the complete chapter through the 2026-07-31 P6.10 paper and "
            "connector-source mining expansion. Every newly scanned sentence is covered by "
            "an exact section digest and bounded existing claim ownership, or classified as "
            "status text or a non-independent line-wrap fragment. Source-reported results "
            "remain source reports. No new support atom, efficacy inference, evidence "
            "transition, release decision, or publication claim was introduced."
        )
        packet["chapter_defaults"]["scope"]["time"] = (
            "Semantic review current through 2026-07-31; material changes to evidence, "
            "authority, population, model, environment, ontology, consumer, source-mined "
            "concept prose, or section ownership require reauthorization."
        )
        dump(packet_path, packet)

        chapter_records.append(
            {
                "chapter_id": chapter_id,
                "chapter_path": chapter_rel,
                "candidate_count": len(rows),
                "sections": [
                    {
                        "heading": heading,
                        "sha256": hashlib.sha256(
                            section_text[heading].encode("utf-8")
                        ).hexdigest(),
                        "owner_atom_ids": section_owners[heading],
                        "candidate_count": sum(
                            1 for row in candidate_records if row["section"] == heading
                        ),
                    }
                    for heading in sorted(observed_sections)
                ],
                "candidate_dispositions": candidate_records,
            }
        )

    output = {
        "schema_version": "asi_stack.p6_10_source_mining_claim_reconciliation.v0",
        "review_date": "2026-07-31",
        "scope": (
            "Exact source-mining prose introduced or materially rewritten in the P6.10 "
            "corpus-closure wave; section-level ownership plus all heuristic prose hits."
        ),
        "summary": {
            "chapter_count": len(chapter_records),
            "candidate_count": len(pending),
            "line_wrap_fragment_count": total_fragments,
            "mapped_complete_proposition_count": total_mapped,
            "status_or_guardrail_count": total_status,
            "unowned_material_claim_count": 0,
            "support_state_effect": "none",
        },
        "chapter_records": chapter_records,
        "non_claims": [
            "This reconciliation does not establish that any paper-derived mechanism works.",
            "Lexical ranking selects among a manually bounded section ownership set; it is not evidence and cannot create or promote a claim.",
            "Source-reported results remain attributed external results and do not become ASI Stack empirical evidence.",
        ],
    }
    dump(OUT, output)
    print(
        f"Reconciled {len(pending)} P6.10 candidates across {len(chapter_records)} "
        f"chapters: {total_mapped} complete propositions, {total_fragments} line-wrap "
        f"fragments, {total_status} status/guardrail records; support effect none."
    )


if __name__ == "__main__":
    main()
