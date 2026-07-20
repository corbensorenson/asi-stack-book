#!/usr/bin/env python3
"""Build the P1 claim-atom registry and prose-claim adjudication queue.

The manifest supplies the structured claim skeleton. Human/agent semantic
reviews live separately in evidence_quality/claim_atom_reviews.json so generated
artifacts remain reproducible and an unreviewed template cannot masquerade as a
finished claim decomposition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
REVIEWS = ROOT / "evidence_quality/claim_atom_reviews.json"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
QUEUE = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REPORT = ROOT / "docs/claim_atom_registry.md"
DOSSIERS = ROOT / "evidence_quality/claim_dossiers"
POST_ACTIVATION_EXPANSION_IDS = {
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "human-factors-and-meaningful-control-in-oversight",
    "governed-world-models-and-reality-grounding",
    "white-box-evidence-interpretability-and-activation-governance",
    "governed-operations-incident-command-and-graceful-degradation",
    "governed-model-training-distributed-optimization-and-scaling",
}
POST_ACTIVATION_FORMAL_TARGETS = {"lean:corrigibility.agency.generic_countermodel_routes"}

SINGLE_ROLES = (
    ("core", "core_claim"),
    ("problem", "problem"),
    ("insufficiency", "insufficient"),
    ("minimum", "minimal_implementation"),
    ("beyond_sota", "beyond_state_of_art"),
)
LIST_ROLES = (
    ("mechanism", "mechanism"),
    ("interface", "interfaces"),
    ("invariant", "invariants"),
    ("failure_mode", "failure_modes"),
)
CLAIM_CUES = re.compile(
    r"\b(should|must|cannot|can only|requires?|required|necessary|sufficient|"
    r"ensures?|guarantees?|prevents?|improves?|reduces?|increases?|outperforms?|"
    r"better than|safer than|faster than|more efficient|scales?|transfers?|"
    r"causes?|leads to|demonstrates?|measures?|proves?|establishes?|shows?)\b",
    re.IGNORECASE,
)
SUPPORT_STATES = {
    "unsupported", "argument", "source-derived", "prototype-backed",
    "synthetic-test-backed", "empirical-test-backed",
    "external-literature-backed", "deprecated", "refuted",
}
LANES = {
    "formal", "executable", "empirical", "causal", "transfer",
    "source-synthesis", "normative",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    # P1 is a frozen 54-chapter activation-baseline audit. Later authorized
    # structural additions are governed by their own intake/research packets
    # and the active successor roadmap; regenerating P1 must not rewrite its
    # historical completion truth or launder those additions as reviewed atoms.
    return [
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter.get("id") not in POST_ACTIVATION_EXPANSION_IDS
    ]


def compact(value: str) -> str:
    return " ".join(value.split()).strip()


def lanes_for(role: str, proposition: str, has_proofs: bool) -> list[str]:
    mapping = {
        "core": ["source-synthesis", "normative", "executable"],
        "problem": ["source-synthesis", "normative"],
        "insufficiency": ["source-synthesis", "transfer"],
        "mechanism": ["executable", "normative"],
        "interface": ["formal", "executable"],
        "invariant": ["formal", "executable"],
        "failure_mode": ["source-synthesis", "executable", "causal"],
        "minimum": ["executable", "normative"],
        "beyond_sota": ["source-synthesis", "empirical", "transfer", "normative"],
        "formal_target": ["formal", "executable"],
        "prose": ["source-synthesis"],
    }
    result = list(mapping[role])
    lower = proposition.casefold()
    if role == "core" and has_proofs:
        result.append("formal")
    if any(word in lower for word in ("improv", "reduc", "increas", "faster", "efficient", "quality", "latency", "cost")):
        result.extend(["empirical", "causal"])
    if any(word in lower for word in ("transfer", "general", "across model", "deployment", "open-world", "sota", "state of the art")):
        result.append("transfer")
    return list(dict.fromkeys(result))


def falsifier_for(role: str, proposition: str) -> str:
    templates = {
        "core": "A reachable counterexample or competent full-attempt result defeats a load-bearing atom, or the complete proposition cannot be operationalized without narrowing.",
        "problem": "The named problem is absent, immaterial, or already closed throughout the declared population and environment.",
        "insufficiency": "A current matched approach supplies every allegedly missing property at the declared scope and cost without importing the proposed mechanism.",
        "mechanism": "The mechanism cannot be implemented with its named boundary, or matched ablation shows the claimed behavior does not depend on it.",
        "interface": "A valid reachable trace crosses the interface while violating the proposition, or a declared consumer accepts the violation.",
        "invariant": "A reachable state or trace satisfies the declared assumptions and violates the proposition.",
        "failure_mode": "No reachable mechanism links the condition to the named failure in the declared scope, or calibrated observation places it below the preregistered materiality threshold.",
        "minimum": "The proposed minimum artifact cannot exercise every named contract element or requires an omitted component to produce an honest receipt.",
        "beyond_sota": "The exact target fails its preregistered comparator, joint-frontier, robustness, or transfer gate.",
        "formal_target": "A checked countermodel satisfies the stated assumptions and negates the target, or the formal model cannot represent the target without changing its meaning.",
        "prose": "Semantic review must define an observation that contradicts this sentence before it can become a material atom.",
    }
    return templates[role]


def type_for(role: str) -> str:
    return {
        "core": "composite",
        "problem": "source-synthesis",
        "insufficiency": "composite",
        "mechanism": "composite",
        "interface": "executable",
        "invariant": "formal",
        "failure_mode": "causal",
        "minimum": "executable",
        "beyond_sota": "composite",
        "formal_target": "formal",
        "prose": "untyped",
    }[role]


def proposition_for(role: str, text: str, title: str) -> str:
    text = compact(text)
    if role == "failure_mode":
        return f"For {title}, a material failure mode is: {text}"
    if role == "minimum":
        return f"The smallest honest implementation boundary for {title} is: {text}"
    return text


def atom_id(chapter_id: str, role: str, ordinal: int, tag: str | None = None) -> str:
    if role == "core":
        return f"{chapter_id}.core"
    if role == "formal_target" and tag:
        suffix = re.sub(r"[^a-z0-9]+", "-", tag.casefold().removeprefix("lean:")).strip("-")
        return f"{chapter_id}.formal.{suffix}"
    return f"{chapter_id}.{role}.{ordinal:03d}"


def default_atom(chapter: dict[str, Any], role: str, ordinal: int, raw: str, *, tag: str | None = None) -> dict[str, Any]:
    chapter_id = chapter["id"]
    proposition = proposition_for(role, raw, chapter["title"])
    required_lanes = lanes_for(role, proposition, bool(chapter.get("proof_targets")))
    current = "research_target" if role == "beyond_sota" else "retain_argument_pending_full_attempt"
    if role == "formal_target":
        current = "unadjudicated_formal_obligation"
    return {
        "atom_id": atom_id(chapter_id, role, ordinal, tag),
        "chapter_id": chapter_id,
        "chapter_title": chapter["title"],
        "owner": chapter_id,
        "role": role,
        "ordinal": ordinal,
        "manifest_pointer": tag or role,
        "proposition": proposition,
        "proposition_type": type_for(role),
        "claim_label": chapter["claim_label"] if role == "core" else "Design rationale",
        "support_state": chapter["evidence_level"] if role == "core" else "argument",
        "current_disposition": current,
        "review_state": "machine_candidate",
        "scope": {
            "population": "semantic_review_required",
            "environment": "semantic_review_required",
            "model": "semantic_review_required",
            "authority": "Corben Sorenson; chapter owner records operational authority",
            "time": "current roadmap campaign; comparator dates must be frozen before outcome work",
            "artifact": chapter["file"],
        },
        "assumptions": ["Semantic review must replace this generated assumption placeholder."],
        "dependencies": [f"{chapter_id}.core"] if role not in {"core", "problem", "insufficiency"} else [],
        "strongest_counterclaim": f"The proposition is unnecessary, false, or too broad in its eventual declared scope: {proposition}",
        "falsifier": falsifier_for(role, proposition),
        "required_lanes": [
            {"lane": lane, "necessity": f"Required by the generated {role} classification; semantic review must confirm or replace this reason."}
            for lane in required_lanes
        ],
        "evidence_refs": {
            "chapter": chapter["file"],
            "manifest": f"book_structure.json#chapter:{chapter_id}/{role}:{ordinal}",
            "source_mappings": f"book_structure.json#chapter:{chapter_id}/claim_source_mappings",
            "proof_targets": f"proofs/proof_manifest.json#chapter:{chapter_id}" if role in {"core", "invariant", "interface", "formal_target"} else None,
            "test_specs": f"appendices/E_codex_test_specs.qmd#chapter:{chapter_id}" if role in {"core", "mechanism", "interface", "invariant", "minimum", "formal_target"} else None,
        },
        "contrary_evidence": [],
        "known_confounds": list(chapter.get("open_evidence_gaps", [])),
        "acceptance_criteria": ["All semantically required lanes pass prospectively frozen, claim-specific gates at the declared scope."],
        "narrowing_criteria": ["Only a strict subset of the population, mechanism, artifact, environment, or load-bearing atoms is established."],
        "refutation_criteria": ["A competent full attempt meets the recorded falsifier or fails a required exact gate."],
        "deprecation_criteria": ["The proposition becomes obsolete, duplicate, superseded, or non-load-bearing and every consumer is migrated."],
        "promotion_ceiling": "argument_until_semantic_review_and_accepted_evidence_transition",
        "reproduction": {
            "command": None,
            "environment_lock": None,
            "artifact_digest": None,
            "evaluator_identity": None,
        },
        "terminal_disposition": None,
        "residual": {
            "owner": chapter_id,
            "next_unblocking_condition": "Complete semantic review, freeze exact scope and gates, then run every applicable lane.",
        },
        "non_claims": [
            "Registry inclusion does not establish the proposition.",
            "Machine-generated typing, scope, lanes, or falsifiers are not a completed semantic review.",
            "No support state changes without a separate accepted evidence-transition record.",
        ],
    }


def apply_review(atom: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "proposition", "proposition_type", "claim_label", "support_state",
        "current_disposition", "review_state", "scope", "assumptions",
        "dependencies", "strongest_counterclaim", "falsifier",
        "required_lanes", "evidence_refs", "contrary_evidence",
        "known_confounds", "acceptance_criteria", "narrowing_criteria",
        "refutation_criteria", "deprecation_criteria", "promotion_ceiling",
        "reproduction", "terminal_disposition", "residual", "non_claims",
    }
    unknown = sorted(set(review) - allowed)
    if unknown:
        raise ValueError(f"{atom['atom_id']}: unknown review fields: {unknown}")
    atom.update(review)
    return atom


def strip_nonprose(body: str) -> list[tuple[int, str]]:
    lines = body.splitlines()
    output: list[tuple[int, str]] = []
    in_front = bool(lines and lines[0].strip() == "---")
    in_fence = False
    in_post_p1_reconciliation = False
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == "<!-- P7-EVIDENCE-RECONCILIATION:START -->":
            in_post_p1_reconciliation = True
            continue
        if stripped == "<!-- P7-EVIDENCE-RECONCILIATION:END -->":
            in_post_p1_reconciliation = False
            continue
        # P1 is the frozen activation-era claim discovery audit. The generated
        # P7 evidence/disposition packet is a later authoritative projection of
        # those owned atoms, not a source of new activation-era prose claims.
        if in_post_p1_reconciliation:
            continue
        if number == 1 and in_front:
            continue
        if in_front:
            if stripped == "---":
                in_front = False
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(("#", "|", "<!--", ":::")):
            continue
        stripped = re.sub(r"^[-*+]\s+", "", stripped)
        stripped = re.sub(r"^\d+\.\s+", "", stripped)
        output.append((number, stripped))
    return output


def prose_candidates(chapter: dict[str, Any], manifest_texts: set[str]) -> list[dict[str, Any]]:
    body = (ROOT / chapter["file"]).read_text(encoding="utf-8")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line, text in strip_nonprose(body):
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z`*])", text):
            sentence = compact(re.sub(r"\[[^\]]+\]\([^\)]+\)", "", sentence))
            if len(sentence.split()) < 6 or len(sentence) > 800:
                continue
            cues = sorted({match.group(0).casefold() for match in CLAIM_CUES.finditer(sentence)})
            if not cues:
                continue
            normalized = re.sub(r"[^a-z0-9]+", " ", sentence.casefold()).strip()
            if normalized in manifest_texts or normalized in seen:
                continue
            seen.add(normalized)
            digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
            result.append({
                "candidate_id": f"{chapter['id']}.prose.{digest}",
                "chapter_id": chapter["id"],
                "source": f"{chapter['file']}:{line}",
                "sentence": sentence,
                "cues": cues,
                "review_state": "pending_materiality_adjudication",
                "allowed_dispositions": ["material_atom", "nonmaterial_explanation", "duplicate_of_atom", "editorial_or_question", "historical_or_source_report"],
            })
    return result


def build() -> tuple[dict[str, Any], dict[str, Any], str, dict[str, str]]:
    structure = load(STRUCTURE)
    review_data = load(REVIEWS)
    chapter_defaults = review_data.get("chapter_defaults", {})
    atom_reviews = review_data.get("atom_reviews", {})
    prose_reviews = review_data.get("prose_candidate_dispositions", {})
    for review_file in review_data.get("review_files", []):
        packet = load(ROOT / review_file)
        chapter_id = packet.get("chapter_id")
        if not isinstance(chapter_id, str) or not chapter_id:
            raise ValueError(f"{review_file}: missing chapter_id")
        if chapter_id in chapter_defaults:
            raise ValueError(f"{review_file}: duplicate chapter defaults for {chapter_id}")
        chapter_defaults[chapter_id] = packet.get("chapter_defaults", {})
        for atom_id, review in packet.get("atom_reviews", {}).items():
            if atom_id in atom_reviews:
                raise ValueError(f"{review_file}: duplicate atom review {atom_id}")
            atom_reviews[atom_id] = review
        for candidate_id, disposition in packet.get("prose_candidate_dispositions", {}).items():
            if candidate_id in prose_reviews:
                raise ValueError(f"{review_file}: duplicate prose disposition {candidate_id}")
            prose_reviews[candidate_id] = disposition
    all_atoms: list[dict[str, Any]] = []
    all_candidates: list[dict[str, Any]] = []
    dossier_atoms: dict[str, list[dict[str, Any]]] = defaultdict(list)
    known_atom_ids: set[str] = set()
    known_candidate_ids: set[str] = set()

    for chapter in chapters(structure):
        chapter_atoms: list[dict[str, Any]] = []
        manifest_norm: set[str] = set()
        for role, key in SINGLE_ROLES:
            raw = chapter.get(key)
            if isinstance(raw, str) and compact(raw):
                chapter_atoms.append(default_atom(chapter, role, 1, raw))
                manifest_norm.add(re.sub(r"[^a-z0-9]+", " ", compact(raw).casefold()).strip())
        for role, key in LIST_ROLES:
            for ordinal, raw in enumerate(chapter.get(key, []), 1):
                chapter_atoms.append(default_atom(chapter, role, ordinal, str(raw)))
                manifest_norm.add(re.sub(r"[^a-z0-9]+", " ", compact(str(raw)).casefold()).strip())
        for ordinal, row in enumerate(chapter.get("proof_targets", []), 1):
            if row.get("tag") in POST_ACTIVATION_FORMAL_TARGETS:
                continue
            raw = row.get("target", "")
            chapter_atoms.append(default_atom(chapter, "formal_target", ordinal, raw, tag=row.get("tag")))
            manifest_norm.add(re.sub(r"[^a-z0-9]+", " ", compact(raw).casefold()).strip())

        for atom in chapter_atoms:
            if atom["atom_id"] in known_atom_ids:
                raise ValueError(f"duplicate atom ID: {atom['atom_id']}")
            known_atom_ids.add(atom["atom_id"])
            if chapter["id"] in chapter_defaults:
                atom = apply_review(atom, chapter_defaults[chapter["id"]])
            if atom["atom_id"] in atom_reviews:
                atom = apply_review(atom, atom_reviews[atom["atom_id"]])
            if atom["support_state"] not in SUPPORT_STATES:
                raise ValueError(f"{atom['atom_id']}: invalid support state")
            for lane in atom["required_lanes"]:
                if lane.get("lane") not in LANES:
                    raise ValueError(f"{atom['atom_id']}: invalid lane {lane.get('lane')!r}")
            all_atoms.append(atom)
            dossier_atoms[chapter["id"]].append(atom)

        for prose_ordinal, candidate in enumerate(prose_candidates(chapter, manifest_norm), 1):
            candidate_id = candidate["candidate_id"]
            if candidate_id in known_candidate_ids:
                raise ValueError(f"duplicate prose candidate ID: {candidate_id}")
            known_candidate_ids.add(candidate_id)
            candidate["disposition_rationale"] = None
            candidate["target_atom_id"] = None
            if candidate_id in prose_reviews:
                disposition = prose_reviews[candidate_id]
                candidate["review_state"] = disposition["state"]
                candidate["disposition_rationale"] = disposition["rationale"]
                candidate["target_atom_id"] = disposition.get("target_atom_id")
            all_candidates.append(candidate)
            if candidate["review_state"] == "material_atom":
                if candidate_id not in atom_reviews:
                    raise ValueError(f"{candidate_id}: material prose candidate lacks atom semantic review")
                prose_atom = default_atom(chapter, "prose", prose_ordinal, candidate["sentence"])
                prose_atom["atom_id"] = candidate_id
                prose_atom["manifest_pointer"] = candidate["source"]
                if chapter["id"] in chapter_defaults:
                    prose_atom = apply_review(prose_atom, chapter_defaults[chapter["id"]])
                prose_atom = apply_review(prose_atom, atom_reviews[candidate_id])
                if prose_atom["review_state"] == "machine_candidate":
                    raise ValueError(f"{candidate_id}: material prose atom remains a machine candidate")
                if candidate_id in known_atom_ids:
                    raise ValueError(f"duplicate atom ID: {candidate_id}")
                known_atom_ids.add(candidate_id)
                all_atoms.append(prose_atom)
                dossier_atoms[chapter["id"]].append(prose_atom)

    unknown_reviews = sorted(set(atom_reviews) - known_atom_ids)
    unknown_prose = sorted(set(prose_reviews) - known_candidate_ids)
    if unknown_reviews or unknown_prose:
        raise ValueError(f"stale review IDs: atoms={unknown_reviews[:5]} prose={unknown_prose[:5]}")

    role_counts = Counter(atom["role"] for atom in all_atoms)
    review_counts = Counter(atom["review_state"] for atom in all_atoms)
    candidate_counts = Counter(row["review_state"] for row in all_candidates)
    registry = {
        "schema_version": "asi_stack.claim_atom_registry.v0",
        "roadmap_id": "asi-stack-post-v2-3-claim-proof-sota-challenge-2026-07-14",
        "source_of_truth": "book_structure.json plus evidence_quality/claim_atom_reviews.json",
        "generation_policy": {
            "manifest_roles_included": [role for role, _ in SINGLE_ROLES + LIST_ROLES] + ["formal_target"],
            "codex_tests_are_evidence_refs_not_claims": True,
            "open_evidence_gaps_are_confounds_not_claims": True,
            "prose_only_claims_require_separate_materiality_adjudication": True,
            "machine_candidates_block_P1_completion": True,
        },
        "summary": {
            "chapter_count": len(chapters(structure)),
            "atom_count": len(all_atoms),
            "role_counts": dict(sorted(role_counts.items())),
            "review_state_counts": dict(sorted(review_counts.items())),
            "prose_candidate_count": len(all_candidates),
            "prose_review_state_counts": dict(sorted(candidate_counts.items())),
            "support_state_effect": "none",
        },
        "atoms": all_atoms,
        "non_claims": [
            "Registry generation does not prove, promote, refute, or deprecate any claim.",
            "Machine candidates are a coverage surface, not completed semantic decomposition.",
            "Codex tests, theorem tags, citations, and source IDs remain evidence pointers whose scope must be adjudicated separately.",
        ],
    }
    queue = {
        "schema_version": "asi_stack.prose_claim_candidate_queue.v0",
        "scanner": "modal and outcome-bearing sentence cue scan; candidates require semantic adjudication",
        "summary": {
            "chapter_count": len(chapters(structure)),
            "candidate_count": len(all_candidates),
            "review_state_counts": dict(sorted(candidate_counts.items())),
        },
        "candidates": all_candidates,
        "non_claims": [
            "A scanner candidate is not automatically a material claim.",
            "A sentence omitted by the scanner is not automatically immaterial.",
            "P1 completion requires chapter-level semantic review in addition to this heuristic queue.",
        ],
    }

    report_lines = [
        "# Claim-Atom Registry",
        "",
        "Status: P1 in progress; machine coverage generated, semantic review pending",
        "",
        "This is the readable projection of `evidence_quality/claim_atom_registry.json`. It does not promote any claim. Machine-generated atoms and prose candidates remain pending until their exact scope, assumptions, falsifier, lanes, contrary evidence, and gates are semantically reviewed in `evidence_quality/claim_atom_reviews.json`.",
        "",
        "## Coverage summary",
        "",
        f"- Chapters: {len(chapters(structure))}",
        f"- Structured manifest atoms: {len(all_atoms)}",
        f"- Machine candidates awaiting semantic atom review: {review_counts.get('machine_candidate', 0)}",
        f"- Prose-only candidates awaiting materiality adjudication: {candidate_counts.get('pending_materiality_adjudication', 0)}",
        "- Support-state effect: none",
        "",
        "| Role | Atoms |",
        "|---|---:|",
    ]
    report_lines.extend(f"| `{role}` | {count} |" for role, count in sorted(role_counts.items()))
    report_lines.extend([
        "",
        "## Chapter review board",
        "",
        "| Chapter | Structured atoms | Machine candidates | Prose candidates pending | Dossier |",
        "|---|---:|---:|---:|---|",
    ])
    prose_by_chapter = Counter(row["chapter_id"] for row in all_candidates if row["review_state"] == "pending_materiality_adjudication")
    dossiers: dict[str, str] = {}
    for chapter in chapters(structure):
        rows = dossier_atoms[chapter["id"]]
        pending = sum(row["review_state"] == "machine_candidate" for row in rows)
        report_lines.append(f"| {chapter['title']} | {len(rows)} | {pending} | {prose_by_chapter[chapter['id']]} | `evidence_quality/claim_dossiers/{chapter['id']}.md` |")
        dossier = [
            f"# Claim Dossier: {chapter['title']}", "",
            f"Chapter ID: `{chapter['id']}`", "",
            "Status: P1 semantic review pending", "",
            f"Core support state: `{chapter['evidence_level']}`", "",
            "This dossier is generated from the manifest and review overlay. Inclusion is not proof or promotion.", "",
            "| Atom | Role | Type | Review | Proposition |",
            "|---|---|---|---|---|",
        ]
        for atom in rows:
            proposition = atom["proposition"].replace("|", "\\|")
            dossier.append(f"| `{atom['atom_id']}` | `{atom['role']}` | `{atom['proposition_type']}` | `{atom['review_state']}` | {proposition} |")
        dossier.extend([
            "", "## Argument-exit state", "",
            "No promotion-or-refutation campaign is frozen yet. P1 must first replace every machine candidate with a semantic review and adjudicate every prose-only candidate.", "",
            "## Non-claims", "",
            "- This dossier does not establish semantic adequacy, implementation behavior, empirical benefit, transfer, safety, or SOTA status.",
            "- All support movement requires a separate accepted evidence-transition record.", "",
        ])
        dossiers[chapter["id"]] = "\n".join(dossier)
    report_lines.extend([
        "", "## P1 completion boundary", "",
        "P1 remains open while any structured atom is a `machine_candidate`, any prose candidate is pending, any chapter lacks a sentence-level semantic sweep, or any accepted material atom lacks exact scope, assumptions, counterclaim, falsifier, required lanes, contrary evidence, acceptance/narrowing/refutation/deprecation gates, promotion ceiling, owner, and residual. Counts are navigation, not evidence.", "",
    ])
    return registry, queue, "\n".join(report_lines), dossiers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, queue, report, dossiers = build()
    expected = {REGISTRY: dump(registry), QUEUE: dump(queue), REPORT: report}
    expected.update({DOSSIERS / f"{chapter_id}.md": body for chapter_id, body in dossiers.items()})
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, body in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != body]
        extra = []
        if DOSSIERS.exists():
            wanted = {path for path in expected if path.parent == DOSSIERS}
            extra = [
                str(path.relative_to(ROOT))
                for path in DOSSIERS.glob("*.md")
                if path not in wanted and path.stem not in POST_ACTIVATION_EXPANSION_IDS
            ]
        if stale or extra:
            raise SystemExit(f"claim-atom artifacts stale: stale={stale[:10]} extra={extra[:10]}")
        print(f"Claim-atom artifacts current: {registry['summary']['atom_count']} structured atoms, {queue['summary']['candidate_count']} prose candidates, 54 dossiers.")
        return
    for path, body in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    print(f"Wrote claim-atom artifacts: {registry['summary']['atom_count']} structured atoms, {queue['summary']['candidate_count']} prose candidates, 54 dossiers.")


if __name__ == "__main__":
    main()
