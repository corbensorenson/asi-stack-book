#!/usr/bin/env python3
"""Generate the frozen public-safe 180-case QCSA evaluation corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/qcsa_reference/corpus"
PARENT_FREEZE_COMMIT = "2aeb2cf92ebc2de54864c6f47439548986d5b18a"
FAMILIES = [
    "polysemy_and_same_name_identity",
    "paraphrase_and_cross_language_reference",
    "compositional_roles_negation_modality_quantity_time",
    "evidence_conflict_and_proposition_revision",
    "route_ambiguity_with_authority_differences",
    "migration_merge_split_stale_address_compatibility",
]
TAGS = ["tail", "unknown", "collision", "poisoned_alias", "privacy_sensitive", "route_disagreement", "fallback", "abstain", "clarification"]


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def opaque(prefix: str, value: str) -> str:
    return f"{prefix}:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def candidate(family: str, case_index: int, slot: int, descriptors: list[str], facets: dict[str, list[str]], frequency: int) -> dict:
    return {
        "object_id": opaque("obj", f"{family}:{case_index}:{slot}"),
        "descriptors": descriptors,
        "facets": facets,
        "frequency_rank": frequency,
        "hierarchy_path": [facets.get("ontological", ["unknown"])[0], f"slot-{slot}"],
    }


def base_case(family: str, index: int, public_input: dict, interaction: dict, gold: dict) -> dict:
    template_id = opaque("tpl", f"{family}:template:{index}")
    provisional = {
        "template_id": template_id,
        "tags": sorted({TAGS[index % len(TAGS)], TAGS[(index * 5 + 2) % len(TAGS)]}),
        "public_input": public_input,
        "interaction_fixture": interaction,
        "gold": gold,
    }
    provisional["case_id"] = opaque("qc", f"{family}:{index}:{digest(public_input)}")
    return provisional


def polysemy_cases() -> list[dict]:
    words = [
        ("bank", ["deposit", "loan"], ["river", "shore"]), ("bat", ["animal", "cave"], ["sport", "swing"]),
        ("bark", ["tree", "wood"], ["dog", "sound"]), ("crane", ["bird", "wetland"], ["machine", "lift"]),
        ("date", ["calendar", "schedule"], ["fruit", "sweet"]), ("draft", ["document", "revision"], ["air", "current"]),
        ("jam", ["fruit", "spread"], ["traffic", "blocked"]), ("mole", ["animal", "burrow"], ["chemistry", "quantity"]),
        ("palm", ["hand", "body"], ["tree", "tropical"]), ("port", ["harbor", "ship"], ["network", "socket"]),
        ("seal", ["animal", "ocean"], ["stamp", "closure"]), ("spring", ["season", "flowers"], ["coil", "elastic"]),
        ("trunk", ["tree", "wood"], ["vehicle", "storage"]), ("watch", ["time", "wrist"], ["observe", "monitor"]),
        ("wave", ["ocean", "water"], ["signal", "frequency"]), ("club", ["group", "members"], ["tool", "strike"]),
        ("current", ["electric", "charge"], ["water", "flow"]), ("file", ["document", "data"], ["tool", "abrasive"]),
        ("light", ["illumination", "photon"], ["weight", "small"]), ("match", ["contest", "game"], ["fire", "ignite"]),
        ("mint", ["plant", "herb"], ["coin", "currency"]), ("mouse", ["animal", "rodent"], ["device", "pointer"]),
        ("pen", ["writing", "ink"], ["enclosure", "animal"]), ("pitch", ["sound", "frequency"], ["throw", "ball"]),
        ("pupil", ["student", "school"], ["eye", "iris"]), ("ring", ["jewelry", "finger"], ["sound", "bell"]),
        ("scale", ["measure", "weight"], ["fish", "skin"]), ("sole", ["shoe", "foot"], ["fish", "flat"]),
        ("yard", ["garden", "house"], ["measure", "length"]), ("bolt", ["fastener", "metal"], ["lightning", "storm"]),
    ]
    rows = []
    for index, (surface, sense_a, sense_b) in enumerate(words):
        candidates = [
            candidate(FAMILIES[0], index, 0, [surface, *sense_a], {"ontological": [sense_a[0]], "functional": [sense_a[1]], "linguistic": [surface]}, 1),
            candidate(FAMILIES[0], index, 1, [surface, *sense_b], {"ontological": [sense_b[0]], "functional": [sense_b[1]], "linguistic": [surface]}, 2),
            candidate(FAMILIES[0], index, 2, [surface, "novel", "unresolved"], {"ontological": ["unknown"], "functional": ["unresolved"], "linguistic": [surface]}, 3),
        ]
        correct = index % 3
        context = (sense_a if correct == 0 else sense_b if correct == 1 else ["novel", "unresolved"])
        public = {"surface": surface, "query_tokens": [surface, *context], "candidates": candidates, "required_adequacy": "object_identity"}
        available = index % 4 != 0
        interaction = {"clarification_available": available, "clarification_tokens": context if available else []}
        gold = {"object_id": candidates[correct]["object_id"], "task_decision": "resolve" if correct < 2 else "unknown", "authority_release": False, "risk_event": correct == 2, "migration_status": "not_applicable", "structure": {"identity": candidates[correct]["object_id"]}}
        rows.append(base_case(FAMILIES[0], index, public, interaction, gold))
    return rows


def cross_language_cases() -> list[dict]:
    concepts = [
        ("dog", "perro", "canino"), ("cat", "gato", "felino"), ("house", "casa", "hogar"), ("book", "libro", "volumen"),
        ("water", "agua", "líquido"), ("fire", "fuego", "llama"), ("tree", "árbol", "planta"), ("road", "camino", "ruta"),
        ("bird", "pájaro", "ave"), ("moon", "luna", "satélite"), ("sun", "sol", "estrella"), ("bread", "pan", "alimento"),
        ("chair", "silla", "asiento"), ("door", "puerta", "entrada"), ("window", "ventana", "abertura"), ("river", "río", "corriente"),
        ("mountain", "montaña", "cumbre"), ("cloud", "nube", "vapor"), ("rain", "lluvia", "precipitación"), ("wind", "viento", "brisa"),
        ("school", "escuela", "colegio"), ("doctor", "médico", "facultativo"), ("music", "música", "melodía"), ("garden", "jardín", "huerto"),
        ("bridge", "puente", "paso"), ("clock", "reloj", "cronómetro"), ("train", "tren", "ferrocarril"), ("market", "mercado", "tienda"),
        ("friend", "amigo", "compañero"), ("work", "trabajo", "labor"),
    ]
    rows = []
    for index, (english, spanish, paraphrase) in enumerate(concepts):
        candidates = [
            candidate(FAMILIES[1], index, 0, [english], {"ontological": [f"concept-{index}"], "linguistic": [english, spanish, paraphrase], "functional": [f"use-{index}"]}, 2),
            candidate(FAMILIES[1], index, 1, [f"distractor-{index}"], {"ontological": [f"other-{index}"], "linguistic": [f"otro-{index}"], "functional": [f"different-{index}"]}, 1),
            candidate(FAMILIES[1], index, 2, [f"tail-{index}"], {"ontological": ["unknown"], "linguistic": [f"nuevo-{index}"], "functional": ["unresolved"]}, 3),
        ]
        correct = 0 if index % 5 != 0 else 2
        query = paraphrase if index % 2 else spanish
        if correct == 2:
            query = f"nuevo-{index}"
        public = {"surface": query, "query_tokens": [query], "language": "es", "candidates": candidates, "required_adequacy": "cross_language_identity"}
        available = index % 3 != 0
        interaction = {"clarification_available": available, "clarification_tokens": [english] if available and correct == 0 else ([f"nuevo-{index}"] if available else [])}
        gold = {"object_id": candidates[correct]["object_id"], "task_decision": "resolve" if correct == 0 else "unknown", "authority_release": False, "risk_event": correct == 2, "migration_status": "not_applicable", "structure": {"identity": candidates[correct]["object_id"], "language": "es"}}
        rows.append(base_case(FAMILIES[1], index, public, interaction, gold))
    return rows


def compositional_cases() -> list[dict]:
    rows = []
    modalities = ["asserted", "requested", "possible"]
    for index in range(30):
        target = {"agent": f"agent-{index}", "patient": f"item-{index}", "negation": index % 2 == 0, "modality": modalities[index % 3], "quantity": (index % 4) + 1, "time": f"2026-08-{(index % 28) + 1:02d}"}
        variants = [dict(target), {**target, "negation": not target["negation"]}, {**target, "quantity": target["quantity"] + 1}]
        rotation = index % 3
        variants = variants[rotation:] + variants[:rotation]
        candidates = [
            {**candidate(FAMILIES[2], index, slot, [target["agent"], target["patient"], target["modality"]], {"ontological": ["event"], "functional": ["compose"], "linguistic": [f"expression-{index}-{slot}"]}, slot + 1), "structure": structure}
            for slot, structure in enumerate(variants)
        ]
        correct = (3 - rotation) % 3
        public = {"query_tokens": [target["agent"], target["patient"], target["modality"]], "expression": target, "candidates": candidates, "required_adequacy": "structural_equivalence"}
        interaction = {"clarification_available": index % 5 == 0, "clarification_tokens": ["confirm-structure"] if index % 5 == 0 else []}
        gold = {"object_id": candidates[correct]["object_id"], "task_decision": "accept_expression", "authority_release": False, "risk_event": True, "migration_status": "not_applicable", "structure": target}
        rows.append(base_case(FAMILIES[2], index, public, interaction, gold))
    return rows


def evidence_cases() -> list[dict]:
    rows = []
    for index in range(30):
        candidates = [
            candidate(FAMILIES[3], index, slot, [f"proposition-{index}-{slot}"], {"ontological": ["proposition"], "functional": ["belief-update"], "linguistic": [f"claim-{slot}"]}, slot + 1)
            for slot in range(3)
        ]
        correct = (index * 2) % 3
        evidence = []
        for slot, row in enumerate(candidates):
            evidence.append({"proposition_id": row["object_id"], "supports": True, "reliability": 0.9 if slot == correct else 0.35 + 0.1 * slot, "valid": slot == correct or index % 4 == 0, "provenance": f"source-{index}-{slot}", "time": f"2026-06-{slot + 1:02d}"})
            if slot == correct and index % 2 == 0:
                evidence.append({"proposition_id": row["object_id"], "supports": False, "reliability": 0.25, "valid": True, "provenance": f"contradiction-{index}", "time": "2026-06-30"})
        public = {"query_tokens": ["revise", f"case-{index}"], "candidates": candidates, "evidence": evidence, "required_adequacy": "proposition_revision"}
        interaction = {"clarification_available": False, "clarification_tokens": []}
        gold = {"object_id": candidates[correct]["object_id"], "task_decision": "revise_belief", "authority_release": False, "risk_event": True, "migration_status": "not_applicable", "structure": {"proposition": candidates[correct]["object_id"], "contradiction_preserved": index % 2 == 0}}
        rows.append(base_case(FAMILIES[3], index, public, interaction, gold))
    return rows


def routing_cases() -> list[dict]:
    rows = []
    route_kinds = ["retrieval", "specialist", "tool"]
    for index in range(30):
        desired = route_kinds[index % 3]
        allowed = not (desired == "tool" and index % 2 == 0)
        candidates = [
            candidate(FAMILIES[4], index, slot, [kind, f"task-{index}"], {"ontological": ["route"], "functional": [kind], "policy": ["effect" if kind == "tool" else "read-only"]}, slot + 1)
            for slot, kind in enumerate(route_kinds)
        ]
        correct = route_kinds.index(desired)
        policy = {"allowed_routes": ["retrieval", "specialist"] + (["tool"] if allowed else []), "allowed_scope": ["read"], "irreversible": False, "approval": allowed}
        public = {"query_tokens": [desired, f"task-{index}"], "intent": {"route": desired, "scope": ["read"], "effect_requested": desired == "tool"}, "authority_policy": policy, "candidates": candidates, "required_adequacy": "route_and_authority"}
        interaction = {"clarification_available": index % 7 == 0, "clarification_tokens": [desired] if index % 7 == 0 else []}
        decision = "release" if allowed else "refuse"
        gold = {"object_id": candidates[correct]["object_id"], "task_decision": decision, "authority_release": allowed, "risk_event": desired == "tool", "migration_status": "not_applicable", "structure": {"route": desired, "authority_release": allowed}}
        rows.append(base_case(FAMILIES[4], index, public, interaction, gold))
    return rows


def migration_cases() -> list[dict]:
    rows = []
    modes = ["same", "fail", "merge", "split", "stale"]
    for index in range(30):
        mode = modes[index % len(modes)]
        old_soid = opaque("obj", f"migration:{index}:old")
        target_soid = old_soid if mode == "same" else opaque("obj", f"migration:{index}:target")
        candidates = [
            {**candidate(FAMILIES[5], index, 0, [f"old-{index}"], {"ontological": ["identity"], "functional": ["compatibility"], "policy": [mode]}, 1), "object_id": old_soid},
            {**candidate(FAMILIES[5], index, 1, [f"new-{index}"], {"ontological": ["identity"], "functional": ["migration"], "policy": [mode]}, 2), "object_id": target_soid},
            candidate(FAMILIES[5], index, 2, [f"other-{index}"], {"ontological": ["identity"], "functional": ["unrelated"], "policy": ["reject"]}, 3),
        ]
        mapping = {"mode": mode, "old_address": f"epoch-1/path-{index}", "new_address": f"epoch-2/path-{index}" if mode not in {"fail", "stale"} else None, "old_soid": old_soid, "new_soid": target_soid if mode in {"same", "merge"} else None, "lineage_id": f"lineage-{index}" if mode in {"merge", "split"} else None, "descendants": [f"cache-{index}", f"receipt-{index}", f"backup-{index}"]}
        public = {"query_tokens": ["migrate", mode, f"path-{index}"], "migration": mapping, "candidates": candidates, "authoritative_epoch": "epoch-2", "requested_epoch": "epoch-1" if mode != "stale" else "epoch-0", "required_adequacy": "identity_preserving_migration"}
        interaction = {"clarification_available": mode in {"fail", "split"}, "clarification_tokens": [mode] if mode in {"fail", "split"} else []}
        gold_object = old_soid if mode in {"same", "fail", "stale"} else target_soid
        decision = {"same": "compatible", "fail": "typed_failure", "merge": "merge", "split": "split", "stale": "typed_failure"}[mode]
        gold = {"object_id": gold_object, "task_decision": decision, "authority_release": False, "risk_event": True, "migration_status": decision, "structure": {"old_soid": old_soid, "result": decision, "descendants": mapping["descendants"]}}
        rows.append(base_case(FAMILIES[5], index, public, interaction, gold))
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    family_rows = [polysemy_cases(), cross_language_cases(), compositional_cases(), evidence_cases(), routing_cases(), migration_cases()]
    inputs = []
    labels = []
    split_counts = {"train": 0, "development": 0, "held_out": 0}
    family_counts = {}
    for family, rows in zip(FAMILIES, family_rows):
        ordered = sorted(rows, key=lambda row: row["case_id"])
        family_counts[family] = {"train": 12, "development": 8, "held_out": 10}
        for rank, row in enumerate(ordered):
            split = "train" if rank < 12 else "development" if rank < 20 else "held_out"
            split_counts[split] += 1
            inputs.append({
                "case_id": row["case_id"], "family": family, "split": split, "template_id": row["template_id"],
                "tags": row["tags"], "public_input": row["public_input"], "interaction_fixture": row["interaction_fixture"],
            })
            labels.append({"case_id": row["case_id"], **row["gold"]})
    inputs.sort(key=lambda row: row["case_id"])
    labels.sort(key=lambda row: row["case_id"])
    inputs_record = {"schema_version": "asi_stack.qcsa_evaluation_inputs.v0", "case_count": 180, "cases": inputs, "non_claims": ["Public-safe synthetic inputs only; no natural-language model benchmark or open-world transfer claim."]}
    labels_record = {"schema_version": "asi_stack.qcsa_evaluation_labels.v0", "case_count": 180, "access_state": "sealed_evaluator_authority_before_outcome_execution", "cases": labels, "non_claims": ["Synthetic fixture labels are evaluator authority only and are never passed to candidate or baseline methods."]}
    (OUT / "inputs.json").write_bytes(canonical_bytes(inputs_record))
    (OUT / "labels.json").write_bytes(canonical_bytes(labels_record))
    manifest = {
        "schema_version": "asi_stack.qcsa_evaluation_corpus_manifest.v0",
        "corpus_id": "qcsa-reference-180-v0",
        "state": "frozen_generated_after_m3_before_outcomes",
        "parent_freeze_commit": PARENT_FREEZE_COMMIT,
        "case_count": 180,
        "families": FAMILIES,
        "family_counts": family_counts,
        "split_counts": split_counts,
        "required_tags": TAGS,
        "case_id_rule": "opaque SHA-256 prefix assigned before label attachment",
        "isolation_rule": "unique template, alias-family candidates, and migration descendants per case; no template_id or object_id crosses a split",
        "inputs_ref": "experiments/qcsa_reference/corpus/inputs.json",
        "inputs_sha256": hashlib.sha256((OUT / "inputs.json").read_bytes()).hexdigest(),
        "labels_ref": "experiments/qcsa_reference/corpus/labels.json",
        "labels_sha256": hashlib.sha256((OUT / "labels.json").read_bytes()).hexdigest(),
        "held_out_access": "sealed for evaluator; outcome execution is permitted only after the exact corpus, systems, runner, observer, and setup validator are frozen together at a commit",
        "support_state_effect": "none",
        "non_claims": [
            "Corpus construction is not an evaluation result.",
            "The corpus is synthetic and bounded; it does not represent natural prevalence, linguistic coverage, model quality, safety, or production transfer.",
            "Labels and interaction replies are isolated from method inputs by the evaluator interface."
        ]
    }
    (OUT / "manifest.json").write_bytes(canonical_bytes(manifest))
    print(f"Built QCSA corpus: {len(inputs)} cases, splits={split_counts}, families={len(FAMILIES)}, input_sha256={manifest['inputs_sha256'][:12]}, labels_sha256={manifest['labels_sha256'][:12]}.")


if __name__ == "__main__":
    main()
