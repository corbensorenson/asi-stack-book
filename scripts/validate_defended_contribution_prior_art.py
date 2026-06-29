#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "defended_contribution_prior_art_positioning.md"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
SCORECARD = ROOT / "docs" / "a_plus_quality_scorecard.md"
TRACKS = ROOT / "docs" / "defended_contribution_tracks.md"
REPOSITORY_MAP = ROOT / "docs" / "repository_map.md"

TRACK_IDS = {
    "living-evidence-book-methodology",
    "claim-support-states-and-evidence-laundering-prevention",
    "governed-self-improvement-boundary",
    "proof-carrying-claims-and-ai-contracts",
    "costed-routing-residual-accounting-resource-discipline",
}

SOURCE_IDS = {
    "ext_model_cards_2019",
    "ext_datasheets_datasets_2021",
    "ext_factsheets_ai_services_2019",
    "ext_ml_reproducibility_program_2021",
    "ext_helm_2022",
    "ext_livebench_2024",
    "ext_nist_ai_rmf_1_0_2023",
    "ext_frontier_ai_regulation_2023",
    "ext_proof_carrying_code_1997",
    "ext_lean4_theorem_proving",
    "ext_corrigibility_2015",
    "ext_off_switch_game_2016",
    "ext_optimal_policies_power_2019",
    "ext_model_evaluation_extreme_risks_2023",
    "ext_slsa_v1_0",
    "ext_frugalgpt_2023",
    "ext_hybrid_llm_2024",
    "ext_routellm_2024",
    "ext_sparse_moe_2017",
    "ext_switch_transformer_2021",
}

BOUNDARY_FRAGMENTS = (
    "source-noted prior-art positioning",
    "not an exhaustive literature review",
    "does not prove novelty",
    "not support-state movement",
    "does not promote any chapter core claim above `argument`",
    "comparators, not evidence",
    "residual-governance comparator gap remains open",
    "not an accepted external review",
)

POSITIONING_REFERENCE = "docs/defended_contribution_prior_art_positioning.md"
VALIDATOR_REFERENCE = "scripts/validate_defended_contribution_prior_art.py"


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def main() -> None:
    errors: list[str] = []

    try:
        text = read(DOC)
    except FileNotFoundError:
        print("Missing docs/defended_contribution_prior_art_positioning.md")
        sys.exit(1)

    for track_id in sorted(TRACK_IDS):
        if f"`{track_id}`" not in text:
            errors.append(f"Prior-art positioning missing track `{track_id}`.")

    for source_id in sorted(SOURCE_IDS):
        note = ROOT / "sources" / "source_notes" / f"{source_id}.md"
        if not note.exists():
            errors.append(f"Missing source note for comparator `{source_id}`.")
        if f"`{source_id}`" not in text:
            errors.append(f"Prior-art positioning missing source `{source_id}`.")

    for fragment in BOUNDARY_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Prior-art positioning missing boundary fragment: {fragment}")

    for path in (README, PUBLICATION, ROADMAP, SCORECARD, TRACKS, REPOSITORY_MAP):
        public_text = read(path)
        if POSITIONING_REFERENCE not in public_text:
            errors.append(
                f"{path.relative_to(ROOT)} missing public reference to {POSITIONING_REFERENCE}"
            )

    for path in (README, PUBLICATION, REPOSITORY_MAP):
        public_text = read(path)
        if VALIDATOR_REFERENCE not in public_text:
            errors.append(
                f"{path.relative_to(ROOT)} missing public reference to {VALIDATOR_REFERENCE}"
            )

    if errors:
        print("Defended contribution prior-art validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Defended contribution prior-art validation passed: "
        f"{len(TRACK_IDS)} tracks positioned against {len(SOURCE_IDS)} source-noted comparators."
    )


if __name__ == "__main__":
    main()
