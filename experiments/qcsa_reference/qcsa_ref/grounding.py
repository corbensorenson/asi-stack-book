"""QI-09: bounded paired-label and synthetic-modality grounding."""

from __future__ import annotations

from .canonical import ContractError, make_envelope


def evaluate(pairs: list[dict]) -> dict:
    resolved, false_equivalences, unsupported = [], [], []
    for row in pairs:
        if set(row) != {"left", "right", "expected_same_soid", "resolved_same_soid", "modality"}:
            raise ContractError("grounding pair shape invalid")
        if row["resolved_same_soid"] and not row["expected_same_soid"]:
            false_equivalences.append(row)
        elif row["resolved_same_soid"] == row["expected_same_soid"]:
            resolved.append(row)
        else:
            unsupported.append(row)
    return {
        "paired_labels": [{"left": row["left"], "right": row["right"]} for row in pairs],
        "synthetic_modality_descriptors": [row for row in pairs if row["modality"] != "text"],
        "resolved_pairs": resolved,
        "false_equivalences": false_equivalences,
        "unsupported_groundings": unsupported,
        "coverage_boundary": {"languages": ["en", "es"], "modalities": ["text", "synthetic_image_descriptor"], "open_world": False},
    }


def artifact(result: dict, input_digests: list[str]) -> dict:
    return make_envelope(
        "QI-09", "grounding:bounded-en-es-synthetic", ["compact-generative-systems-and-residual-honesty"], result,
        input_digests=input_digests,
        non_claim_boundary="Tiny public-safe label and synthetic descriptor fixture only; no universal multilingual or multimodal grounding claim.",
    )
