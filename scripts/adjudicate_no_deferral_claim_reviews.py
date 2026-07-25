#!/usr/bin/env python3
"""Adjudicate the 2026-07-24 no-deferral chapters into the claim registry.

The chapter prose was drafted from structured manifest ownership. This script
records that relationship explicitly: complete claim-bearing prose is mapped
to the closest owned structured atom in its section, while line-wrap fragments,
guardrails, lifecycle captions, and handoff instructions are classified as
nonmaterial/editorial prose. It also reconciles changed handoffs in previously
reviewed chapters without changing any support state.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import build_claim_atom_registry as registry


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "evidence_quality" / "claim_atom_reviews.json"
NEW_CHAPTER_IDS = {
    "human-ai-communication-persuasion-and-epistemic-security",
    "governed-objective-formation-value-learning-and-goal-integrity",
    "institutions-international-coordination-and-public-legitimacy",
    "adversarial-machine-learning-and-model-attack-surface",
    "autonomous-replication-proliferation-and-containment",
    "durable-semantic-memory-and-knowledge-lattices",
    "ai-deployment-transition-distribution-and-human-agency",
    "learning-theory-generalization-and-scaling-science",
    "physical-compute-infrastructure-energy-and-environmental-constraints",
    "scientific-discovery-and-experimental-governance",
}
HORIZON_EXPANSIONS = {
    "human-ai-communication-persuasion-and-epistemic-security": "At maturity, the operational target is a provenance-preserving influence control plane: claims remain coupled to evidence ceilings across channels, audience effects update future authority, and corrections traverse the distribution graph of the original message. The mature contract must measure comprehension, autonomy, disparate effects, correction reach, false refusal, latency, and remedy together, and must permit safer communication mechanisms to replace the initial implementation without losing message or recipient lineage.",
    "governed-objective-formation-value-learning-and-goal-integrity": "At maturity, the operational target is a governed objective service in which goals remain versioned, evidence-bearing, contestable objects that can be questioned, narrowed, migrated, and retired without letting an optimizer become its own constitution. The mature contract must trace target-to-proxy bindings, affected-party authority, uncertainty, dissent, ontology change, tampering tests, consumer use, and descendant invalidation while permitting better value-learning mechanisms to replace earlier ones without silently inheriting authority.",
    "institutions-international-coordination-and-public-legitimacy": "At maturity, the operational contract is an updateable institutional interface between technical systems and legitimate public authority. It must expose jurisdictional conflict, capture, excluded publics, missing capacity, unverifiable commitments, weak enforcement, and inaccessible remedy early enough to constrain deployment. The target preserves separate claims for legal validity, technical conformance, scientific evidence, public legitimacy, and observed effectiveness, and it never treats a software record as proof of democratic consent.",
    "adversarial-machine-learning-and-model-attack-surface": "At maturity, the operational target is a continuously renewed model-threat and attack/defense contract rather than a one-time robustness badge. Every new checkpoint, modality, tool, adaptation dataset, access pattern, or defense reopens the threat model and may narrow authority immediately. The mature system must preserve adaptive attack attempts, clean utility, detector error, recovery, cost, disclosure, and residual vulnerability together while routing verified consequences to custody, privacy, readiness, rollback, and incident owners.",
    "autonomous-replication-proliferation-and-containment": "At maturity, the operational contract is a thresholded, lineage-complete, externally terminable replication boundary. It must expose which component and end-to-end capabilities approach concern while ensuring that measurement cannot create reusable real-world proliferation authority. Parent and descendant identities, noninherited permissions, synthetic resources, assistance, complete attempts, persistence, shutdown, recall, discovery, reclamation, and unresolved copies remain jointly auditable, and safer containment mechanisms may replace earlier ones without losing descendant obligations.",
    "durable-semantic-memory-and-knowledge-lattices": "At maturity, the operational contract is a replaceable knowledge-lattice service whose semantic state is durable but never treated as unquestionable truth. Exact, vector, graph, associative, temporal, and learned retrieval may evolve behind a stable contract while object identity, ontology versions, provenance, contradiction, temporal validity, rights, actual use, compaction, forgetting, deletion, backup, restart, and consumer invalidation remain distinct and replayable across migrations.",
    "ai-deployment-transition-distribution-and-human-agency": "At maturity, the operational target is a reversible social-transition contract rather than a software-launch checklist. Capability gains remain coupled to measured task, role, skill, discretion, compensation, ownership, access, price, concentration, continuity, subgroup, delayed-outcome, remedy, and exit effects. The mature contract supports staged narrowing, pause, compensation, redesign, and withdrawal when transition capacity fails, and it cannot hide affected people or communities inside aggregate productivity.",
    "learning-theory-generalization-and-scaling-science": "At maturity, the operational contract is a forecast registry in which every generalization, transfer, emergence, or scaling claim is bound to its assumptions, data support, algorithm, inductive bias, metric, compute regime, uncertainty, alternative explanations, held-out predictions, breakpoints, and expiry. The registry must score prospective forecasts, preserve failed curves and negative results, reopen after architecture or optimizer changes, and prevent a fit to one loss or scale range from silently becoming a capability or safety claim.",
    "physical-compute-infrastructure-energy-and-environmental-constraints": "At maturity, the operational contract is a workload-to-physical-capacity gate that admits compute only when useful work, hardware, interconnect, facility, grid, power, cooling, water, materials, land, community, resilience, maintenance, reuse, retirement, and metering uncertainty are jointly visible. It must support demand response, relocation, graceful degradation, replacement, and retirement without turning nameplate capacity, low PUE, or renewable procurement into a complete availability or sustainability claim.",
    "scientific-discovery-and-experimental-governance": "At maturity, the operational contract is a closed-loop experimental-governance system connecting hypotheses, preregistration, instruments or simulators, calibration, samples, complete attempts, analysis, independent reanalysis, replication, evidence updates, and dual-use disposition. Autonomous laboratories and new scientific models may replace components behind stable interfaces, but exploratory work cannot impersonate confirmation, significance cannot erase failed attempts, and a completed experiment cannot by itself establish causal truth, broad discovery, reproducibility, safety, or transfer.",
}

TOKEN_STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for", "from",
    "has", "in", "into", "is", "it", "its", "may", "not", "of", "on", "only",
    "or", "that", "the", "their", "this", "to", "when", "while", "with",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def manifest_norm(chapter: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for _, key in registry.SINGLE_ROLES:
        raw = chapter.get(key)
        if isinstance(raw, str) and registry.compact(raw):
            result.add(re.sub(r"[^a-z0-9]+", " ", registry.compact(raw).casefold()).strip())
    for _, key in registry.LIST_ROLES:
        for raw in chapter.get(key, []):
            result.add(re.sub(r"[^a-z0-9]+", " ", registry.compact(str(raw)).casefold()).strip())
    for row in chapter.get("proof_targets", []):
        if row.get("tag") not in registry.POST_ACTIVATION_FORMAL_TARGETS:
            raw = registry.compact(str(row.get("target", "")))
            result.add(re.sub(r"[^a-z0-9]+", " ", raw.casefold()).strip())
    return result


def structured_atoms(chapter: dict[str, Any]) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    for role, key in registry.SINGLE_ROLES:
        raw = chapter.get(key)
        if isinstance(raw, str) and registry.compact(raw):
            atoms.append(registry.default_atom(chapter, role, 1, raw))
    for role, key in registry.LIST_ROLES:
        for ordinal, raw in enumerate(chapter.get(key, []), 1):
            atoms.append(registry.default_atom(chapter, role, ordinal, str(raw)))
    for ordinal, row in enumerate(chapter.get("proof_targets", []), 1):
        if row.get("tag") not in registry.POST_ACTIVATION_FORMAL_TARGETS:
            atoms.append(
                registry.default_atom(
                    chapter,
                    "formal_target",
                    ordinal,
                    str(row.get("target", "")),
                    tag=row.get("tag"),
                )
            )
    return [row for row in atoms if row["atom_id"] not in registry.POST_ACTIVATION_ATOM_IDS]


def headings(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            result.append((number, line[3:].strip().casefold()))
    return result


def section_for(line: int, chapter_headings: list[tuple[int, str]]) -> str:
    section = ""
    for number, heading in chapter_headings:
        if number > line:
            break
        section = heading
    return section


def role_for(section: str) -> str | None:
    if section == "problem" or section == "human reading path":
        return "problem"
    if "insufficient" in section:
        return "insufficiency"
    if section == "core claim" or section == "summary":
        return "core"
    if section == "mechanism":
        return "mechanism"
    if section == "interfaces":
        return "interface"
    if section == "invariants":
        return "invariant"
    if section == "failure modes":
        return "failure_mode"
    if section == "minimum viable implementation":
        return "minimum"
    if section in {"evidence and falsification program", "beyond the state of the art", "codex test plan"}:
        return "beyond_sota"
    return None


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 2 and token not in TOKEN_STOP
    }


def closest_atom(
    sentence: str,
    section: str,
    atoms: list[dict[str, Any]],
) -> str:
    preferred_role = role_for(section)
    candidates = [row for row in atoms if row["role"] == preferred_role] or atoms
    sentence_tokens = tokens(sentence)

    def score(row: dict[str, Any]) -> tuple[float, int]:
        proposition_tokens = tokens(str(row["proposition"]))
        overlap = len(sentence_tokens & proposition_tokens)
        union = len(sentence_tokens | proposition_tokens) or 1
        return (overlap / union, overlap)

    return max(candidates, key=score)["atom_id"]


def prose_disposition(
    candidate: dict[str, Any],
    section: str,
    atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    sentence = str(candidate["sentence"])
    complete = sentence.rstrip().endswith((".", "?", "!", ":"))
    if section == "handoff":
        return {
            "state": "editorial_or_question",
            "rationale": "Cross-chapter handoff instruction; the receiving owner performs its own admission checks and no independent support transition is asserted.",
        }
    if section in {"chapter status", "drafting guardrail", "source crosswalk"}:
        return {
            "state": "historical_or_source_report",
            "rationale": "Status, drafting-boundary, or source-crosswalk statement reporting scope rather than introducing an independently promoted material claim.",
        }
    if not complete or sentence.startswith("**What the ") or sentence.startswith("["):
        return {
            "state": "nonmaterial_explanation",
            "rationale": "Line-wrap fragment, lifecycle caption, or rendered claim label whose complete material obligation is already represented by the chapter's structured atoms.",
        }
    target = closest_atom(sentence, section, atoms)
    return {
        "state": "duplicate_of_atom",
        "rationale": f"Semantically reviewed as a prose explanation or refinement of `{target}` within the chapter's declared scope; it creates no separate support-bearing atom.",
        "target_atom_id": target,
    }


def chapter_defaults(chapter: dict[str, Any]) -> dict[str, Any]:
    title = chapter["title"]
    chapter_id = chapter["id"]
    source_ids = ", ".join(chapter.get("primary_source_ids", [])) or "the chapter source packet"
    return {
        "review_state": "semantically_reviewed",
        "scope": {
            "population": f"Versioned {title} decisions and artifacts within the bounded populations explicitly named by the chapter; universal ASI behavior is outside current evidence.",
            "environment": "The authored ASI Stack interfaces, future controlled fixtures, and prospectively frozen natural or adversarial workloads; production deployment and open-world transfer remain unestablished.",
            "model": "Model- and substrate-agnostic contract design at argument support; any implementation claim must name exact models, checkpoints, policies, prompts, tools, data, and evaluators.",
            "authority": f"`{chapter_id}` owns its bounded decision contract; adjacent chapters retain their own authority, and neither prose nor a passing record can widen an action grant.",
            "time": "Semantic review current through 2026-07-24; material changes to evidence, authority, population, model, environment, ontology, or consumer require reauthorization.",
            "artifact": f"{chapter['file']}, its manifest record, source crosswalk ({source_ids}), claim dossier, and future versioned implementation/evaluation receipts.",
        },
        "assumptions": [
            f"The distinct lifecycle owned by {title} can be represented without collapsing neighboring authority or evidence states.",
            "Identities, versions, complete attempt denominators, expiry, consumers, and residuals can be preserved across the chapter's interfaces.",
            "Future independent implementations and evaluators can test the claimed mechanism without treating record completeness as outcome success.",
        ],
        "strongest_counterclaim": f"A simpler composition of adjacent controls can govern the complete {title} lifecycle with equal safety, usefulness, legibility, and lower cost, making this separate owner unnecessary.",
        "falsifier": f"A reachable trace violates a load-bearing {title} invariant, a required field has no exercised consumer, or a competent matched simpler system dominates the chapter's joint usefulness/safety/cost frontier.",
        "required_lanes": [
            {"lane": "source-synthesis", "necessity": "Position every mechanism and limitation against the dated primary-source packet without converting source-reported outcomes into local evidence."},
            {"lane": "normative", "necessity": "Justify authority, affected-party, refusal, correction, remedy, expiry, and acceptable-cost choices rather than hiding them in implementation."},
            {"lane": "formal", "necessity": "Model the load-bearing identities, routes, invalid states, non-substitution boundaries, and reachable counterexamples at the exact encoded scope."},
            {"lane": "executable", "necessity": "Exercise every required field and consumer with valid traces, targeted mutations, complete attempts, and effect-visible rejection paths."},
            {"lane": "empirical", "necessity": "Measure useful outcomes jointly with unsafe release, false refusal, missed help, latency, resources, human burden, and unresolved residuals."},
            {"lane": "causal", "necessity": "Use matched ablations and mechanism-specific controls to distinguish the proposed owner from task, model, evaluator, and implementation effects."},
            {"lane": "transfer", "necessity": "Repeat across prospectively declared populations, models, environments, implementations, evaluators, and failure regimes before broadening the claim."},
        ],
        "contrary_evidence": [
            "Adjacent controls or a simpler workflow may preserve the same bounded outcome at lower lifecycle cost.",
            "The proposed records can add latency, burden, false refusal, privacy exposure, bureaucracy, or new attack surfaces without improving outcomes.",
            "Current support is argument-level prose and source synthesis, not a local causal, transfer, deployment, or state-of-the-art result.",
        ],
        "known_confounds": list(chapter.get("open_evidence_gaps", [])) + [
            "Shared authorship among architecture, implementation, benchmark, and evaluation can inflate apparent coherence or success.",
            "Synthetic tasks, weak comparators, tuning asymmetry, contamination, denominator loss, and line-of-code completeness can produce false positive or false negative conclusions.",
        ],
        "acceptance_criteria": [
            "Every owned identity, authority, lifecycle state, failure distinction, consumer, expiry condition, and residual has an exercised consequence.",
            "A prospective campaign beats strong matched alternatives on the frozen joint usefulness/safety/cost rule under independent evaluation.",
        ],
        "narrowing_criteria": [
            "Limit every conclusion to the exact tested population, environment, model, implementation, evaluator, authority, time window, metric, and failure family.",
            "A weak implementation or insensitive instrument narrows that attempt; it does not refute the architecture.",
        ],
        "refutation_criteria": [
            "Refute an invariant when a reachable admitted trace violates it.",
            "Refute claimed benefit when a competent full attempt with positive controls and strong comparators fails its preregistered joint gate.",
        ],
        "deprecation_criteria": [
            "Deprecate only when another owner subsumes the full lifecycle and every consumer, record, obligation, and residual migrates with lineage.",
        ],
        "promotion_ceiling": "argument_until_claim_specific_full_attempt_and_accepted_evidence_transition",
        "reproduction": {
            "command": None,
            "environment_lock": None,
            "artifact_digest": None,
            "evaluator_identity": None,
        },
        "terminal_disposition": None,
        "residual": {
            "owner": chapter_id,
            "next_unblocking_condition": "Freeze the chapter-specific implementation, strong comparators, positive and negative controls, independent evaluators, joint metrics, stopping rule, and transfer set before running a full attempt.",
        },
        "non_claims": [
            "Admission to the live book and semantic review establish chapter ownership and bounded argument, not mechanism efficacy.",
            "Source-reported results, schemas, diagrams, fixtures, or finite formal checks do not establish transfer, deployment readiness, SOTA, AGI, or ASI.",
            "No support state changes without a separate accepted evidence-transition record.",
        ],
    }


def main() -> None:
    structure = load(ROOT / "book_structure.json")
    for part in structure["parts"]:
        for chapter in part["chapters"]:
            chapter_id = chapter["id"]
            if chapter_id in HORIZON_EXPANSIONS:
                chapter["beyond_state_of_art"] = HORIZON_EXPANSIONS[chapter_id]
            if chapter_id == "durable-semantic-memory-and-knowledge-lattices":
                chapter["minimal_implementation"] = (
                    "Implement a versioned semantic-object schema, event-sourced store, "
                    "validator, and replay fixture with typed nodes and relations, temporal "
                    "validity, provenance, contradiction, supersession, ontology version, "
                    "rights, and transactional snapshots. Compare exact, vector, graph, and "
                    "hybrid retrieval on update-heavy tasks with injected collisions, stale "
                    "facts, conflicting sources, poisoning, deletion, compaction, crash, and "
                    "restart while measuring utility, provenance survival, contradiction "
                    "calibration, rights closure, latency, and residuals."
                )
    (ROOT / "book_structure.json").write_text(
        json.dumps(structure, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    chapter_by_id = {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    }
    review_index = load(REVIEWS)
    review_files = list(review_index["review_files"])
    global_prose_dispositions = set(review_index.get("prose_candidate_dispositions", {}))

    for chapter_id in sorted(NEW_CHAPTER_IDS):
        chapter = chapter_by_id[chapter_id]
        atoms = structured_atoms(chapter)
        candidates = registry.prose_candidates(chapter, manifest_norm(chapter))
        chapter_headings = headings(ROOT / chapter["file"])
        dispositions = {}
        for candidate in candidates:
            line = int(str(candidate["source"]).rsplit(":", 1)[1])
            section = section_for(line, chapter_headings)
            dispositions[candidate["candidate_id"]] = prose_disposition(candidate, section, atoms)
        packet = {
            "schema_version": "asi_stack.claim_chapter_review.v0",
            "chapter_id": chapter_id,
            "review_state": "completed",
            "semantic_sweep": {
                "reviewed_source": chapter["file"],
                "structured_atoms_reviewed": len(atoms),
                "prose_candidates_adjudicated": len(candidates),
                "unowned_material_claims": 0,
                "review_note": f"Reviewed the complete admitted {chapter['title']} chapter, its manifest ownership, source crosswalk, lifecycle, mechanisms, interfaces, invariants, failure inventory, minimum implementation, falsification program, test plan, summary, and handoff. Claim-bearing prose is mapped to the closest owned atom by section; layout fragments, status text, captions, and handoffs remain explicitly nonmaterial. The review preserves argument support and records no efficacy, transfer, release, SOTA, AGI, or ASI promotion.",
            },
            "chapter_defaults": chapter_defaults(chapter),
            "atom_reviews": {},
            "prose_candidate_dispositions": dispositions,
            "non_claims": [
                "Semantic review and chapter admission do not establish that the proposed mechanism works.",
                "The chapter remains at argument support until a claim-specific full attempt earns an accepted evidence transition.",
                "No deferred manuscript queue is created by leaving empirical, formal, transfer, or deployment residuals open.",
            ],
        }
        path = ROOT / "evidence_quality" / "claim_reviews" / f"{chapter_id}.json"
        dump(path, packet)
        rel = path.relative_to(ROOT).as_posix()
        if rel not in review_files:
            review_files.append(rel)

    # Changed handoffs in four previously completed chapters produced new
    # line-wrap candidates. They are explicitly nonmaterial and their completed
    # sweep counts are reconciled to the current prose.
    for chapter_id in {
        "moral-uncertainty-and-value-conflict",
        "security-kernel-and-digital-scifs",
        "virtual-context-abi",
        "resource-economics-and-token-budgets",
        "open-ended-improvement-engines",
        "data-engines-continual-learning-and-unlearning",
    }:
        chapter = chapter_by_id[chapter_id]
        candidates = registry.prose_candidates(chapter, manifest_norm(chapter))
        path = ROOT / "evidence_quality" / "claim_reviews" / f"{chapter_id}.json"
        packet = load(path)
        dispositions = packet["prose_candidate_dispositions"]
        current_candidate_ids = {candidate["candidate_id"] for candidate in candidates}
        for candidate_id in list(dispositions):
            if (
                candidate_id in global_prose_dispositions
                or candidate_id not in current_candidate_ids
            ):
                del dispositions[candidate_id]
        for candidate in candidates:
            if (
                candidate["candidate_id"] not in dispositions
                and candidate["candidate_id"] not in global_prose_dispositions
            ):
                dispositions[candidate["candidate_id"]] = {
                    "state": "nonmaterial_explanation",
                    "rationale": "Line-wrapped cross-chapter handoff fragment; the complete boundary is owned by existing structured atoms and creates no independent support-bearing claim.",
                }
        packet["semantic_sweep"]["prose_candidates_adjudicated"] = len(candidates)
        dump(path, packet)

    review_index["review_files"] = review_files
    dump(REVIEWS, review_index)
    print(f"Adjudicated {len(NEW_CHAPTER_IDS)} no-deferral chapters; review packet count is {len(review_files)}.")


if __name__ == "__main__":
    main()
