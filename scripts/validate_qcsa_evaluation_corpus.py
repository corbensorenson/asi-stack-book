#!/usr/bin/env python3
"""Validate the frozen QCSA evaluation corpus and split isolation."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/qcsa_reference/corpus"
MANIFEST = CORPUS / "manifest.json"
INPUTS = CORPUS / "inputs.json"
LABELS = CORPUS / "labels.json"
SCHEMA = ROOT / "schemas/qcsa_evaluation_corpus_manifest.schema.json"
BUILDER = ROOT / "scripts/build_qcsa_evaluation_corpus.py"
PARENT = "2aeb2cf92ebc2de54864c6f47439548986d5b18a"
LANE_FAMILIES = {
    "polysemy_and_same_name_identity",
    "paraphrase_and_cross_language_reference",
    "compositional_roles_negation_modality_quantity_time",
    "evidence_conflict_and_proposition_revision",
    "route_ambiguity_with_authority_differences",
    "migration_merge_split_stale_address_compatibility",
}
TAGS = {"tail", "unknown", "collision", "poisoned_alias", "privacy_sensitive", "route_disagreement", "fallback", "abstain", "clarification"}
CASE_ID = re.compile(r"^qc:[0-9a-f]{16}$")
TEMPLATE_ID = re.compile(r"^tpl:[0-9a-f]{16}$")
LABEL_FIELDS = {"case_id", "object_id", "task_decision", "authority_release", "risk_event", "migration_status", "structure"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(data: dict, *, check_files: bool = False) -> list[str]:
    errors: list[str] = []
    manifest = data["manifest"]
    inputs_record = data["inputs"]
    labels_record = data["labels"]
    schema = load(SCHEMA)
    errors.extend(f"manifest schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(manifest))
    inputs = inputs_record.get("cases", [])
    labels = labels_record.get("cases", [])
    if inputs_record.get("case_count") != 180 or labels_record.get("case_count") != 180 or len(inputs) != 180 or len(labels) != 180:
        errors.append("corpus must contain exactly 180 inputs and labels")
    if set(manifest.get("families", [])) != LANE_FAMILIES:
        errors.append("corpus family set drifted")
    input_ids = [row.get("case_id") for row in inputs]
    label_ids = [row.get("case_id") for row in labels]
    if len(set(input_ids)) != 180 or input_ids != sorted(input_ids) or label_ids != input_ids:
        errors.append("case identity/order differs or duplicates exist")
    if any(not isinstance(case_id, str) or not CASE_ID.fullmatch(case_id) for case_id in input_ids):
        errors.append("case IDs are not opaque SHA-prefix IDs")
    if any(not TEMPLATE_ID.fullmatch(row.get("template_id", "")) for row in inputs):
        errors.append("template IDs are not opaque")
    if any(set(row) != LABEL_FIELDS for row in labels):
        errors.append("label record shape drifted")

    split_counts = Counter(row.get("split") for row in inputs)
    if split_counts != Counter({"train": 72, "development": 48, "held_out": 60}) or dict(split_counts) != manifest.get("split_counts"):
        errors.append("72/48/60 split drifted")
    family_splits: dict[str, Counter] = defaultdict(Counter)
    for row in inputs:
        family_splits[row.get("family")][row.get("split")] += 1
    expected = Counter({"train": 12, "development": 8, "held_out": 10})
    if set(family_splits) != LANE_FAMILIES or any(counts != expected for counts in family_splits.values()):
        errors.append("per-family 12/8/10 split drifted")

    tag_splits: dict[str, set[str]] = defaultdict(set)
    for row in inputs:
        for tag in row.get("tags", []):
            tag_splits[tag].add(row.get("split"))
    if set(tag_splits) != TAGS or any(splits != {"train", "development", "held_out"} for splits in tag_splits.values()):
        errors.append("required tags are absent or fail three-split coverage")

    forbidden = {"gold", "label", "object_id", "task_decision", "authority_release", "risk_event", "migration_status"}
    for row in inputs:
        if forbidden & set(row.get("public_input", {})):
            errors.append(f"{row.get('case_id')}: label field leaked into public input")
        interaction_text = json.dumps(row.get("interaction_fixture", {}), sort_keys=True)
        if re.search(r"obj:[0-9a-f]{16}", interaction_text):
            errors.append(f"{row.get('case_id')}: clarification channel leaks object ID")

    split_by_case = {row["case_id"]: row["split"] for row in inputs}
    seen_templates: dict[str, str] = {}
    seen_objects: dict[str, str] = {}
    seen_descendants: dict[str, str] = {}
    for row in inputs:
        split = row["split"]
        template_id = row["template_id"]
        if template_id in seen_templates and seen_templates[template_id] != split:
            errors.append("template crosses split")
        seen_templates[template_id] = split
        for candidate in row["public_input"].get("candidates", []):
            object_id = candidate.get("object_id")
            if object_id in seen_objects and seen_objects[object_id] != split:
                errors.append("candidate object/alias family crosses split")
            seen_objects[object_id] = split
        for descendant in row["public_input"].get("migration", {}).get("descendants", []):
            if descendant in seen_descendants and seen_descendants[descendant] != split:
                errors.append("migration descendant crosses split")
            seen_descendants[descendant] = split
    if any(label["object_id"] not in seen_objects for label in labels):
        errors.append("label references object absent from public candidate set")

    if manifest.get("parent_freeze_commit") != PARENT:
        errors.append("parent implementation-freeze commit drifted")
    if check_files:
        if hashlib.sha256(INPUTS.read_bytes()).hexdigest() != manifest.get("inputs_sha256"):
            errors.append("input file digest drifted")
        if hashlib.sha256(LABELS.read_bytes()).hexdigest() != manifest.get("labels_sha256"):
            errors.append("label file digest drifted")
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", PARENT, "HEAD"], cwd=ROOT, check=False)
        if ancestor.returncode != 0:
            errors.append("held-out labels were opened without the frozen implementation commit in history")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures = []
    mutations: list[tuple[str, dict]] = []
    label_leak = copy.deepcopy(base)
    label_leak["inputs"]["cases"][0]["public_input"]["object_id"] = label_leak["labels"]["cases"][0]["object_id"]
    mutations.append(("label leaked to public input", label_leak))
    duplicate = copy.deepcopy(base)
    duplicate["inputs"]["cases"][1]["case_id"] = duplicate["inputs"]["cases"][0]["case_id"]
    mutations.append(("duplicate case ID", duplicate))
    split_drift = copy.deepcopy(base)
    split_drift["inputs"]["cases"][0]["split"] = "held_out" if split_drift["inputs"]["cases"][0]["split"] != "held_out" else "train"
    mutations.append(("split-count drift", split_drift))
    missing_tag = copy.deepcopy(base)
    for row in missing_tag["inputs"]["cases"]:
        row["tags"] = [tag for tag in row["tags"] if tag != "tail"]
    mutations.append(("required tag erased", missing_tag))
    cross_template = copy.deepcopy(base)
    train = next(row for row in cross_template["inputs"]["cases"] if row["split"] == "train")
    held = next(row for row in cross_template["inputs"]["cases"] if row["split"] == "held_out")
    held["template_id"] = train["template_id"]
    mutations.append(("template leakage", cross_template))
    cross_object = copy.deepcopy(base)
    train = next(row for row in cross_object["inputs"]["cases"] if row["split"] == "train")
    held = next(row for row in cross_object["inputs"]["cases"] if row["split"] == "held_out")
    held["public_input"]["candidates"][0]["object_id"] = train["public_input"]["candidates"][0]["object_id"]
    mutations.append(("candidate leakage", cross_object))
    interaction_leak = copy.deepcopy(base)
    interaction_leak["inputs"]["cases"][0]["interaction_fixture"]["answer"] = interaction_leak["labels"]["cases"][0]["object_id"]
    mutations.append(("clarification object-ID leakage", interaction_leak))
    missing_label = copy.deepcopy(base)
    missing_label["labels"]["cases"] = missing_label["labels"]["cases"][:-1]
    mutations.append(("missing label", missing_label))
    parent_drift = copy.deepcopy(base)
    parent_drift["manifest"]["parent_freeze_commit"] = "0" * 40
    mutations.append(("parent freeze drift", parent_drift))
    family_erasure = copy.deepcopy(base)
    family_erasure["manifest"]["families"] = family_erasure["manifest"]["families"][:-1]
    mutations.append(("family erased", family_erasure))
    for label, value in mutations:
        if not semantic_errors(value):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [MANIFEST, INPUTS, LABELS, SCHEMA, BUILDER]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA corpus artifacts: " + ", ".join(missing))
    before = {path.name: path.read_bytes() for path in [MANIFEST, INPUTS, LABELS]}
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True, capture_output=True, text=True)
    after = {path.name: path.read_bytes() for path in [MANIFEST, INPUTS, LABELS]}
    errors = [] if before == after else ["corpus builder replay is not byte-deterministic"]
    base = {"manifest": load(MANIFEST), "inputs": load(INPUTS), "labels": load(LABELS)}
    errors.extend(semantic_errors(base, check_files=True))
    errors.extend(negative_controls(base))
    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))
    print("QCSA evaluation corpus passed: 180 deterministic public-safe cases, six families, exact 72/48/60 and per-family 12/8/10 splits, all nine tags across every split, opaque IDs, isolated templates/objects/descendants, evaluator-only labels and clarification replies, frozen parent commit, and 10 rejecting mutations.")


if __name__ == "__main__":
    main()
