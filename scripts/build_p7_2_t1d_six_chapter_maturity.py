#!/usr/bin/env python3
"""Build the P7.2-T1D six-chapter manuscript-maturity receipt.

This packet records idea placement and implementation-test readiness. It does
not execute a model experiment, validate a scientific mechanism, or move
support.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
ROUND_18_ATOMS = ROOT / "evidence_quality/round_18_breadth_completion_claim_atoms.json"
R16_ATOMS = ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json"
OUT = ROOT / "evidence_quality/p7_2_t1d_six_chapter_maturity.json"
REPORT = ROOT / "docs/p7_2_t1d_six_chapter_maturity_and_source_role_review_2026_07_26.md"

CONDITIONS = [
    "field_decomposition",
    "strongest_challenge",
    "implementation_determination",
    "failure_and_nonclaim_envelope",
    "literature_engagement_by_role",
    "territory_sized_reader_value",
]

CHAPTERS: list[dict[str, Any]] = [
    {
        "id": "inner-alignment-mesa-optimization-and-learned-objective-integrity",
        "field_anchor": "### Deceptive alignment, training games, and gradient hacking",
        "distinctive_anchors": [
            "Deceptive alignment, training games, and gradient hacking",
            "The mechanism therefore produces a scoped evidence case",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_learned_optimization_risks_2019", "ext_sleeper_agents_2024"],
            "limitation_or_failure": ["ext_goal_misgeneralization_2022", "ext_emergent_misalignment_reward_hacking_2025"],
            "competing_design_or_simpler_baseline": ["ext_optimal_policies_power_2019", "alignment_field"],
            "measurement_or_evaluation": ["ext_sleeper_agents_2024", "ext_emergent_misalignment_reward_hacking_2025"],
        },
        "residuals": [
            "No local learner has been shown to contain a mesa-objective, deceptive policy, training game, gradient hacking, or sleeper mechanism.",
            "Behavioral equivalence, capability, opportunity, and competing explanations remain unresolved until a competent campaign distinguishes them.",
        ],
    },
    {
        "id": "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
        "field_anchor": "### Strategic foundations: games, bargaining, choice, and adaptation",
        "distinctive_anchors": [
            "Strategic foundations: games, bargaining, choice, and adaptation",
            "A cartel or race to the bottom can be stable.",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_cooperative_ai_foundations_2023", "ext_functional_decision_theory_2017"],
            "limitation_or_failure": ["ext_multi_agent_risks_2025", "ext_gradual_disempowerment_2025"],
            "competing_design_or_simpler_baseline": ["ext_functional_decision_theory_2017", "coherence_exchange"],
            "measurement_or_evaluation": ["ext_constructive_interdependence_human_ai_2026", "ext_multi_agent_risks_2025"],
        },
        "residuals": [
            "No local population campaign establishes cooperation, collusion, bargaining quality, equilibrium selection, or gradual disempowerment.",
            "Synthetic-agent results cannot transfer to institutions or affected populations without separately qualified environments and outcome measures.",
        ],
    },
    {
        "id": "perception-sensor-fusion-and-observation-trust",
        "field_anchor": "### Bayesian state estimation and concrete fusion regimes",
        "distinctive_anchors": [
            "Bayesian state estimation and concrete fusion regimes",
            "Fusion must model correlation.",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_imagebind_2023", "ext_multimodal_machine_learning_taxonomy_2019"],
            "limitation_or_failure": ["ext_3d_detection_corruptions_2023", "ext_adversarial_sensor_fusion_2022"],
            "competing_design_or_simpler_baseline": ["ext_multimodal_machine_learning_taxonomy_2019", "platonic_world_model"],
            "measurement_or_evaluation": ["ext_3d_detection_corruptions_2023", "ext_adversarial_sensor_fusion_2022"],
        },
        "residuals": [
            "No local sensor-fusion system has demonstrated calibrated observation trust under natural corruption, adversarial attack, timing faults, or common-mode dependence.",
            "A shared embedding or fused estimate is not open-world truth and cannot inherit execution authority.",
        ],
    },
    {
        "id": "embodied-agency-real-time-control-and-physical-safety",
        "field_anchor": "### Hybrid control, timing evidence, and sim-to-real limits",
        "distinctive_anchors": [
            "Hybrid control, timing evidence, and sim-to-real limits",
            "Software rollback never implies reversal of physical effects.",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_gemini_robotics_2025", "ext_control_barrier_functions_2019"],
            "limitation_or_failure": ["ext_foundation_robotics_physical_risk_2025", "ext_safe_reinforcement_learning_survey_2015"],
            "competing_design_or_simpler_baseline": ["ext_simplex_architecture_1998", "ext_control_barrier_functions_2019"],
            "measurement_or_evaluation": ["ext_ai_simulation_digital_twins_2025", "ext_foundation_robotics_physical_risk_2025"],
        },
        "residuals": [
            "No plant, robot, independent stop path, real-time controller, or physical rollback route has been exercised by this repository.",
            "Simulation and digital-twin evidence cannot establish hardware timing, contact safety, irreversible-effect recovery, or deployment readiness.",
        ],
    },
    {
        "id": "human-ai-organizations-delegation-and-accountability",
        "field_anchor": "### Organizational transition: tasks, jobs, power, and public capacity",
        "distinctive_anchors": [
            "Organizational transition: tasks, jobs, power, and public capacity",
            "responsible for a decision they could not inspect, change, stop, or appeal.",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_ai_decision_authority_2020", "ext_nist_ai_rmf_1_0_2023"],
            "limitation_or_failure": ["ext_moral_crumple_zones_2019", "ext_human_ai_feedback_loops_2025"],
            "competing_design_or_simpler_baseline": ["talos", "ext_ai_decision_authority_2020"],
            "measurement_or_evaluation": ["ext_generative_ai_at_work_2025", "ext_constructive_interdependence_human_ai_2026", "ext_human_ai_team_meta_analysis_2024"],
        },
        "residuals": [
            "No local organization study establishes productivity, legitimacy, accountability, skill, distribution, diffusion, liability, or public-capacity outcomes.",
            "Task-level results do not license job-, organization-, sector-, or economy-wide inference.",
        ],
    },
    {
        "id": "white-box-evidence-interpretability-and-activation-governance",
        "field_anchor": "### Comparative method matrix",
        "distinctive_anchors": [
            "Comparative method matrix",
            "The white-box ladder is deliberately noninheritant.",
        ],
        "roles": {
            "mechanism_or_capability": ["ext_transformer_circuits_2021", "ext_scaling_sparse_autoencoders_2024", "ext_circuit_tracing_2025"],
            "limitation_or_failure": ["ext_interpretability_illusion_bert_2021", "ext_sae_benchmark_reliability_2026"],
            "competing_design_or_simpler_baseline": ["ext_probe_control_tasks_2019", "ext_elk_report_2021"],
            "measurement_or_evaluation": ["ext_saebench_2025", "ext_sae_benchmark_reliability_2026"],
        },
        "residuals": [
            "No probe, sparse autoencoder, circuit, causal intervention, activation monitor, or steering policy has been run in this repository.",
            "Decodability, semantic validity, causal use, transfer, intervention utility, and policy authority remain separate unearned rungs.",
        ],
    },
]

REPAIRS = [
    {
        "topic": "uncertainty_decomposition",
        "chapter_id": "governed-world-models-and-reality-grounding",
        "path": "chapters/governed-world-models-and-reality-grounding.qmd",
        "anchor": "Four uncertainty families receive separate fields and remedies:",
    },
    {
        "topic": "refinement_and_dependent_types",
        "chapter_id": "executable-specifications-and-lean-proof-envelope",
        "path": "chapters/executable-specifications-and-lean-proof-envelope.qmd",
        "anchor": "### Refinement types, dependent types, and proof-carrying data",
    },
    {
        "topic": "synthetic_data_and_self_play_generation",
        "chapter_id": "data-engines-continual-learning-and-unlearning",
        "path": "chapters/data-engines-continual-learning-and-unlearning.qmd",
        "anchor": "### Governed synthetic-data and self-play lifecycle",
    },
    {
        "topic": "human_explanation_generation",
        "chapter_id": "human-factors-and-meaningful-control-in-oversight",
        "path": "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
        "anchor": "### Explanation generation as a governed translation",
    },
]

WHITE_BOX_REQUIRED = [
    "ext_probe_control_tasks_2019",
    "ext_interpretability_illusion_bert_2021",
    "ext_scaling_sparse_autoencoders_2024",
    "ext_saebench_2025",
    "ext_sae_benchmark_reliability_2026",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chapters(book: dict[str, Any]) -> list[dict[str, Any]]:
    return [chapter for part in book["parts"] for chapter in part["chapters"]]


def heading_locations() -> dict[str, list[str]]:
    return {
        "field_decomposition": ["## Problem", "### Exclusive job and adjacent boundaries"],
        "strongest_challenge": ["## Why existing approaches are insufficient", "### Strongest objection"],
        "implementation_determination": ["## Mechanism", "## Interfaces", "## Minimum Viable Implementation"],
        "failure_and_nonclaim_envelope": ["## Invariants", "## Failure modes", "## Codex test plan"],
        "literature_engagement_by_role": ["## Source crosswalk"],
        "territory_sized_reader_value": ["## Human Reading Path", "## Summary", "## Handoff"],
    }


def build() -> dict[str, Any]:
    book = load(BOOK)
    inventory = {row["id"]: row for row in load(INVENTORY)}
    round_18_atoms = load(ROUND_18_ATOMS)
    r16_atoms = load(R16_ATOMS)
    manifest = {row["id"]: row for row in chapters(book)}
    core_atom_ids = {
        row["chapter_owner"]: [row["stable_claim_identity"]]
        for row in round_18_atoms["atoms"]
    }
    r16_atom_ids = {
        row["chapter_id"]: row["atom_ids"]
        for row in r16_atoms["chapter_reviews"]
    }
    corpus_text = {
        row["id"]: (ROOT / row["file"]).read_text(encoding="utf-8")
        for row in chapters(book)
    }
    records: list[dict[str, Any]] = []

    for spec in CHAPTERS:
        chapter = manifest[spec["id"]]
        path = ROOT / chapter["file"]
        text = corpus_text[spec["id"]]
        locations = heading_locations()
        if spec["id"] == "white-box-evidence-interpretability-and-activation-governance":
            locations["field_decomposition"] = [
                "## Problem",
                "## Ownership boundaries",
                "## Why this boundary earns a chapter",
            ]
            locations["strongest_challenge"] = [
                "## Why existing approaches are insufficient",
                "## Strongest objection",
            ]
        locations["field_decomposition"].append(spec["field_anchor"])
        for anchors in locations.values():
            for anchor in anchors:
                if anchor not in text:
                    raise ValueError(f"{spec['id']}: missing maturity anchor {anchor!r}")
        for role, source_ids in spec["roles"].items():
            if not source_ids:
                raise ValueError(f"{spec['id']}: empty source role {role}")
            for source_id in source_ids:
                if source_id not in chapter["source_ids"]:
                    raise ValueError(f"{spec['id']}: role source not assigned: {source_id}")
                if source_id not in inventory:
                    raise ValueError(f"{spec['id']}: role source not inventoried: {source_id}")
                note = ROOT / "sources/source_notes" / f"{source_id}.md"
                if not note.is_file():
                    raise ValueError(f"{spec['id']}: missing source note: {source_id}")
        specificity = []
        for anchor in spec["distinctive_anchors"]:
            if anchor not in text:
                raise ValueError(f"{spec['id']}: missing specificity anchor {anchor!r}")
            owners = sorted(chapter_id for chapter_id, body in corpus_text.items() if anchor in body)
            if owners != [spec["id"]]:
                raise ValueError(f"{spec['id']}: non-specific anchor {anchor!r}: {owners}")
            specificity.append({"anchor": anchor, "corpus_owner_count": 1, "owner": spec["id"]})
        atom_ids = r16_atom_ids.get(spec["id"], core_atom_ids.get(spec["id"], []))
        if not atom_ids:
            raise ValueError(f"{spec['id']}: no reconciled claim atom identity")
        records.append(
            {
                "chapter_id": spec["id"],
                "chapter_path": chapter["file"],
                "chapter_sha256": sha256(path),
                "claim_label": chapter["claim_label"],
                "support_state": chapter["evidence_level"],
                "maturity_conditions": {
                    condition: {
                        "status": "passed_for_manuscript_maturity",
                        "chapter_locations": locations[condition],
                    }
                    for condition in CONDITIONS
                },
                "source_roles": spec["roles"],
                "source_note_paths": sorted(
                    {
                        f"sources/source_notes/{source_id}.md"
                        for ids in spec["roles"].values()
                        for source_id in ids
                    }
                ),
                "claim_atom_ids": atom_ids,
                "reader_projection": {
                    "human_path": f"{chapter['file']}#human-reading-path",
                    "summary": f"{chapter['file']}#summary",
                    "handoff": f"{chapter['file']}#handoff",
                    "source_crosswalk": f"{chapter['file']}#source-crosswalk",
                    "claim_matrix_atom_ids": atom_ids,
                    "outline_surface": "docs/book_outline.md",
                },
                "chapter_specificity_evidence": specificity,
                "residuals": spec["residuals"],
                "maximum_next_inference": "competent_implementation_and_fair_test_design_only",
                "support_state_effect": "none",
            }
        )

    repairs = []
    for repair in REPAIRS:
        path = ROOT / repair["path"]
        text = path.read_text(encoding="utf-8")
        if repair["anchor"] not in text:
            raise ValueError(f"owner repair missing: {repair['topic']}")
        repairs.append(
            {
                **repair,
                "chapter_sha256": sha256(path),
                "state": "meaning_bearing_prose_present",
                "support_state_effect": "none",
            }
        )

    white = manifest["white-box-evidence-interpretability-and-activation-governance"]
    source_packet = []
    for source_id in WHITE_BOX_REQUIRED:
        if source_id not in white["source_ids"]:
            raise ValueError(f"White-Box required source not assigned: {source_id}")
        source_packet.append(
            {
                "source_id": source_id,
                "inventory_url": inventory[source_id]["url"],
                "source_note_path": f"sources/source_notes/{source_id}.md",
                "source_note_sha256": sha256(ROOT / "sources/source_notes" / f"{source_id}.md"),
                "freshness_date": inventory[source_id].get("updated", inventory[source_id].get("published")),
                "local_reproduction": "none",
                "authority": "external_comparator_only",
            }
        )

    return {
        "schema_version": "asi_stack.p7_2_t1d_six_chapter_maturity.v1",
        "packet_id": "P7.2-T1D-six-chapter-proof-readiness-depth-pack-2026-07-26",
        "snapshot_date": "2026-07-26",
        "state": "terminal_manuscript_maturity_no_support_movement",
        "maturity_definition": "Specified enough for competent implementation and a fair test; not proved, empirically supported, qualified, or promoted.",
        "word_count_is_acceptance_gate": False,
        "chapter_count": len(records),
        "condition_count": len(CONDITIONS),
        "chapter_records": records,
        "accepted_existing_owner_repairs": repairs,
        "white_box_source_packet": source_packet,
        "chapter_specific_inheritance_audit": {
            "method": "two manually selected domain-bearing anchors per chapter must have exactly one owner across the current 84-chapter corpus",
            "chapter_count": len(records),
            "anchor_count": sum(len(row["chapter_specificity_evidence"]) for row in records),
            "collisions": 0,
        },
        "atom_reconciliation": {
            "source_packets": [
                "evidence_quality/round_18_breadth_completion_claim_atoms.json",
                "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json"
            ],
            "chapter_count": len(records),
            "atom_count": sum(len(row["claim_atom_ids"]) for row in records),
            "new_material_atoms": 0,
            "support_state_effect": "none",
        },
        "reader_reconciliation": {
            "all_six_have_human_path_summary_handoff_and_source_crosswalk": True,
            "outline_surface": "docs/book_outline.md",
            "claim_matrix_surface": "appendices/C_claim_evidence_matrix.qmd",
            "external_source_surface": "appendices/H_external_sources.qmd",
            "current_reader_derivative_required_after_packet": True,
        },
        "non_claims": [
            "Manuscript maturity is not proof, empirical support, implementation success, reproduction, transfer, safety, readiness, release, SOTA, AGI, or ASI.",
            "Source-role coverage does not establish that a cited result is correct or locally reproduced.",
            "A passed maturity condition does not guarantee that a future implementation is competent.",
            "A failed future method may support only the exact instrument, implementation, construct, or mechanism inference earned by its controls.",
            "No prose, source, atom, reader, schema, validator, fixture, or maturity record moves support.",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
        "publication_effect": "none",
    }


def report(record: dict[str, Any]) -> str:
    rows = []
    for chapter in record["chapter_records"]:
        roles = "; ".join(
            f"{role.replace('_', ' ')}: {', '.join(f'`{source_id}`' for source_id in ids)}"
            for role, ids in chapter["source_roles"].items()
        )
        rows.append(
            f"| `{chapter['chapter_id']}` | 6/6 | {len(chapter['claim_atom_ids'])} | "
            f"{len(chapter['chapter_specificity_evidence'])}/2 | {roles} |"
        )
    repair_rows = [
        f"| `{row['topic']}` | `{row['chapter_id']}` | `{row['anchor']}` | present; no support movement |"
        for row in record["accepted_existing_owner_repairs"]
    ]
    return f"""# P7.2-T1D Six-Chapter Manuscript Maturity and Source-Role Review

Recorded: 2026-07-26

## Decision

The six target chapters pass the manuscript-maturity gate: each is specified
enough to guide a competent implementation and a fair test. This is an
organization and prose-depth decision only. It is not proof, empirical support,
reproduction, qualification, or promotion.

Word count is not an acceptance gate. The review instead checks field
decomposition, strongest challenge, implementation determination, failure and
non-claim boundaries, literature roles, and territory-sized reader value.

## Six-chapter matrix

| Chapter | Maturity conditions | Reconciled atoms | Specific anchors | Source roles |
|---|---:|---:|---:|---|
{chr(10).join(rows)}

Every chapter record in
`evidence_quality/p7_2_t1d_six_chapter_maturity.json` names the exact chapter
locations, source-note paths, residuals, reader projections, chapter digest,
and maximum next inference.

## White-Box depth result

The White-Box chapter now contains a comparative method matrix and a
noninheritant evidence ladder from decodability through stability,
reconstruction, semantic construct validity, causal challenge, transfer,
intervention utility, and policy authority. Four previously roadmap-only
sources now have inventory records, passage notes, manifest mappings, and
bounded chapter use. Together with the existing scaling-SAE source, the packet
separates probe memorization, cross-dataset interpretation illusion,
multi-metric SAE comparison, and metric reliability.

The 2026 reliability audit is scoped counterevidence about selected metrics and
settings. It cannot be used to dismiss sparse autoencoders or interpretability
as a field. Conversely, a clean reconstruction or label score cannot authorize
a semantic, causal, transfer, or operational conclusion.

## Existing-owner repairs

| Topic | Existing owner | Exact anchor | Disposition |
|---|---|---|---|
{chr(10).join(repair_rows)}

## Reader and atom reconciliation

The ten applicable reviewed atom identities remain at argument support: one
core identity for each Round 18 chapter and five previously reviewed White-Box
identities. This packet creates no material atom and changes no support state. Each chapter projects
to its Human Reading Path, Summary, Handoff, Source crosswalk, outline, and
Appendix C identities. A new current-reader derivative must be generated after
this packet so the reader does not freeze an earlier manuscript digest.

## Maximum inference

The maximum inference is: these six manuscript owners and four existing-owner
repairs now put the accepted ideas in their respective places and constrain a
future competent implementation and fair test. Nothing here establishes that
the proposed mechanisms work.
"""


def main() -> None:
    record = build()
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report(record), encoding="utf-8")
    print(
        "P7.2-T1D maturity packet built: 6 chapters, 36 condition decisions, "
        "12 chapter-specific anchors, 4 existing-owner repairs, 5 White-Box source records; "
        "support effect none."
    )


if __name__ == "__main__":
    main()
