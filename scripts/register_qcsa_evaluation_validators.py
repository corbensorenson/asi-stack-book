#!/usr/bin/env python3
"""Idempotently register QCSA corpus and pre-outcome setup gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SPECS = [
    {
        "script": "validate_qcsa_evaluation_corpus.py",
        "artifacts": [
            "scripts/build_qcsa_evaluation_corpus.py", "scripts/validate_qcsa_evaluation_corpus.py",
            "schemas/qcsa_evaluation_corpus_manifest.schema.json",
            "experiments/qcsa_reference/corpus/inputs.json", "experiments/qcsa_reference/corpus/labels.json",
            "experiments/qcsa_reference/corpus/manifest.json"
        ],
        "input_contract": "The deterministic 180-case public-safe QCSA corpus with evaluator-only labels, six exact families, 72/48/60 train/development/held-out separation, nine required adversarial tags in every split, opaque identifiers, and content digests.",
        "output_contract": "Rebuild byte-identically; validate schema, exact family/split/tag coverage, label isolation, template/object/descendant isolation, parent freeze ancestry, and digests; reject ten corpus mutations.",
        "output_assertions": ["180 deterministic cases", "six families", "72/48/60 split", "12/8/10 per family", "nine tags in each split", "opaque IDs", "isolated labels", "ten rejecting mutations"],
        "claim_scope": "Corpus construction and isolation properties for the exact synthetic QCSA fixture set.",
        "negative_cases": ["label leak", "duplicate ID", "split drift", "missing tag", "template leak", "object leak", "clarification leak", "missing label", "parent drift", "family erasure"],
        "prohibited": "Corpus validity does not establish evaluation quality, natural prevalence, learned-model performance, semantic correctness, safety, privacy, or production transfer."
    },
    {
        "script": "validate_qcsa_evaluation_setup_freeze.py",
        "artifacts": [
            "scripts/build_qcsa_evaluation_setup_freeze.py", "scripts/validate_qcsa_evaluation_setup_freeze.py",
            "scripts/run_qcsa_evaluation_predictions.py", "scripts/qcsa_evaluation_observer.py",
            "experiments/qcsa_reference/qcsa_ref/evaluation.py",
            "schemas/qcsa_evaluation_setup_freeze.schema.json",
            "roadmap_records/qcsa_evaluation_setup_freeze.json"
        ],
        "input_contract": "A content-addressed, outcome-sealed evaluation setup binding the candidate, seven baselines, five ablations, 60 held-out cases, three seeds, label-isolated runner, separately implemented observer, 10000-resample paired intervals, Pareto policy, budgets, and decision thresholds.",
        "output_contract": "Replay the setup freeze byte-identically; validate all bound digests and method sets; statically enforce runner/label and observer/candidate separation; reject twelve setup mutations while outcomes remain sealed pending setup commit attestation.",
        "output_assertions": ["13 exact systems", "three seeds", "60 held out", "runner label isolation", "observer implementation separation", "10000 resamples", "Pareto policy", "13 bound files", "twelve rejecting mutations", "outcomes sealed"],
        "claim_scope": "Pre-outcome reproducibility and evaluator-separation properties of the exact bounded QCSA evaluation setup.",
        "negative_cases": ["candidate removal", "baseline removal", "ablation removal", "seed drift", "case drift", "bootstrap drift", "opened outcomes", "support promotion", "digest mutation", "label import", "self-confirmation", "blended score"],
        "prohibited": "A frozen setup does not establish a favorable result, matched advantage, semantic preservation, safety, privacy, external independence, production transfer, AGI, ASI, or chapter-core support movement."
    }
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
    for spec in SPECS:
        unit = next((row for row in registry["units"] if row["script"] == spec["script"] and row.get("args", []) == []), None)
        if unit is None:
            order = len(registry["units"]) + 1
            unit = {"id": f"{spec['script'].removeprefix('validate_').removesuffix('.py')}:{order}", "order": order, "script": spec["script"], "args": []}
            registry["units"].append(unit)
        unit.update({
            "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
            "input_contract": spec["input_contract"], "input_artifacts": spec["artifacts"],
            "output_contract": spec["output_contract"], "output_assertions": spec["output_assertions"],
            "claim_scope": spec["claim_scope"], "negative_controls": "validator_owned",
            "negative_control_cases": spec["negative_cases"], "prohibited_inference": spec["prohibited"],
            "contract_precision": "exact_high_impact", "semantic_review_state": "internal_contract_audit_not_independent"
        })
        for artifact in spec["artifacts"]:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
        override = next((row for row in overrides["contracts"] if row["script"] == spec["script"] and row.get("args", []) == []), None)
        record = {"script": spec["script"], "args": [], **{field: unit[field] for field in fields}}
        if override is None:
            overrides["contracts"].append(record)
        else:
            override.clear(); override.update(record)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered QCSA evaluation validators: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
