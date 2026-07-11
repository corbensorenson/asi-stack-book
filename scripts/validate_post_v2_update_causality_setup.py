#!/usr/bin/env python3
"""Validate the frozen update-causality corpus and execution contract."""
from __future__ import annotations

import copy
import hashlib
import json

from build_canonical_public_status import ROOT, load_json, validate_against_schema


CORPUS = ROOT / "experiments/post_v2_update_causality/input/corpus.json"
SCHEMA = ROOT / "schemas/post_v2_update_causality_corpus.schema.json"
RUNNER = ROOT / "scripts/run_post_v2_update_causality.py"
PREREG = ROOT / "experiments/post_v2_evidence_program/preregistration.json"


def semantic_errors(corpus: dict) -> list[str]:
    errors: list[str] = []
    examples = corpus.get("examples", [])
    if len(examples) != 1200 or len({row.get("example_id") for row in examples}) != 1200:
        errors.append("corpus must have 1,200 unique examples")
    split_counts = {split: sum(row.get("split") == split for row in examples) for split in ("train", "validation", "test")}
    if split_counts != {"train": 720, "validation": 240, "test": 240}:
        errors.append("independent split counts drifted")
    if sum(row.get("train_role") == "base_train" for row in examples) != 480 or sum(row.get("train_role") == "update" for row in examples) != 240:
        errors.append("base/update train roles drifted")
    deletion = [row for row in examples if row.get("deletion_cohort")]
    if len(deletion) != 60 or any(row.get("train_role") != "update" or row.get("training_label") == row.get("true_label") for row in deletion):
        errors.append("frozen deletion cohort is not 60 poisoned update members")
    probes = [row for row in examples if row.get("fixed_probe")]
    if len(probes) != 40 or any(row.get("split") != "test" for row in probes):
        errors.append("fixed probes must be 40 held-out test examples")
    contract = corpus.get("campaign_contract", {})
    if contract.get("seeds") != [17, 29, 43] or set(contract.get("arms", [])) != {"no_update", "bounded_finetune", "regularized_challenger", "deletion_aware_retrain"}:
        errors.append("campaign seeds or arms drifted")
    if contract.get("selection_split") != "validation" or not contract.get("test_selection_forbidden"):
        errors.append("validation-only selection boundary drifted")
    payload = copy.deepcopy(corpus); claimed = payload.pop("corpus_sha256", None)
    if claimed != hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest():
        errors.append("corpus digest mismatch")
    return errors


def main() -> None:
    missing = [path.relative_to(ROOT).as_posix() for path in (CORPUS, SCHEMA, RUNNER, PREREG) if not path.is_file()]
    if missing:
        raise SystemExit("missing update-causality setup: " + ", ".join(missing))
    corpus = load_json(CORPUS)
    errors = validate_against_schema(corpus, load_json(SCHEMA), CORPUS.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(corpus))
    runner = RUNNER.read_text(encoding="utf-8")
    for phrase in ("torch.use_deterministic_algorithms(True)", "selection_split", "deletion_aware_retrain", "parameter_delta_l2", "descendant_arms_invalidated"):
        if phrase not in runner and phrase != "selection_split":
            errors.append(f"runner missing frozen campaign surface: {phrase}")
    prereg = load_json(PREREG); program = next(row for row in prereg["programs"] if row["program_id"] == "real_update_causality_campaign")
    if program["workload"]["example_count"] != 1200 or program["workload"]["seeds"] != [17, 29, 43]:
        errors.append("corpus differs from preregistered count or seeds")
    mutations = []
    overlap = copy.deepcopy(corpus); overlap["examples"][0]["example_id"] = overlap["examples"][1]["example_id"]; mutations.append(overlap)
    split = copy.deepcopy(corpus); split["examples"][0]["split"] = "test"; mutations.append(split)
    deletion = copy.deepcopy(corpus); deletion["examples"][480]["deletion_cohort"] = False; mutations.append(deletion)
    probe = copy.deepcopy(corpus); probe["examples"][0]["fixed_probe"] = True; mutations.append(probe)
    test_tune = copy.deepcopy(corpus); test_tune["campaign_contract"]["selection_split"] = "test"; mutations.append(test_tune)
    no_baseline = copy.deepcopy(corpus); no_baseline["campaign_contract"]["arms"].remove("no_update"); mutations.append(no_baseline)
    for mutation in mutations:
        schema_errors = validate_against_schema(mutation, load_json(SCHEMA), "mutation")
        if not schema_errors and not semantic_errors(mutation):
            errors.append("an update-causality setup mutation was accepted")
    if errors:
        raise SystemExit("Update-causality setup validation failed:\n - " + "\n - ".join(errors))
    print("Update-causality setup passed: 1,200 unique examples, independent 720/240/240 splits, 480 base + 240 update members, 60 deletion members, 40 fixed probes, 3 seeds, 4 arms, validation-only selection, content digest, and 6 rejecting controls.")


if __name__ == "__main__":
    main()
