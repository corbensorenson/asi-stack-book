#!/usr/bin/env python3
"""Add admitted no-deferral owners to their existing source-note crosswalks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TO_CHAPTER = {
    "ext_goal_misgeneralization_2022": "governed-objective-formation-value-learning-and-goal-integrity",
    "ext_learned_optimization_risks_2019": "governed-objective-formation-value-learning-and-goal-integrity",
    "ext_emergent_misalignment_reward_hacking_2025": "governed-objective-formation-value-learning-and-goal-integrity",
    "ext_sleeper_agents_2024": "adversarial-machine-learning-and-model-attack-surface",
    "ext_carlini_training_data_extraction_2021": "adversarial-machine-learning-and-model-attack-surface",
    "ext_adversarial_sensor_fusion_2022": "adversarial-machine-learning-and-model-attack-surface",
    "ext_graphrag_2024": "durable-semantic-memory-and-knowledge-lattices",
    "ext_hipporag_2024": "durable-semantic-memory-and-knowledge-lattices",
    "ext_mem0_2025": "durable-semantic-memory-and-knowledge-lattices",
    "ext_titans_2025": "durable-semantic-memory-and-knowledge-lattices",
    "ext_scaling_laws_neural_language_models_2020": "learning-theory-generalization-and-scaling-science",
    "ext_mdl_tutorial_2004": "learning-theory-generalization-and-scaling-science",
    "ext_weak_to_strong_generalization_2023": "learning-theory-generalization-and-scaling-science",
    "ext_information_bottleneck_2000": "learning-theory-generalization-and-scaling-science",
}


def main() -> None:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    titles = {
        chapter["id"]: chapter["title"]
        for part in structure["parts"]
        for chapter in part["chapters"]
    }
    for source_id, chapter_id in SOURCE_TO_CHAPTER.items():
        path = ROOT / "sources" / "source_notes" / f"{source_id}.md"
        text = path.read_text(encoding="utf-8")
        row = f"- `{chapter_id}` ({titles[chapter_id]})"
        if row not in text:
            text = text.replace("## Book Chapters Supported\n", f"## Book Chapters Supported\n\n{row}")
            path.write_text(text, encoding="utf-8")
    print(f"Reconciled {len(SOURCE_TO_CHAPTER)} source-note chapter crosswalks.")


if __name__ == "__main__":
    main()
