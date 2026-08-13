#!/usr/bin/env python3
"""Idempotently register the maintained Human Reader manuscript gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_human_reader_current.py"
ARTIFACTS = [
    "scripts/validate_human_reader_current.py",
    "scripts/build_human_reader_current.py",
    "scripts/register_human_reader_current_validator.py",
    "scripts/build_human_reader_public_site.py",
    ".github/workflows/build-pages-artifact.yml",
    "assets/reading-mode.html",
    "assets/styles.scss",
    "scripts/validate_live_human_view_browser.js",
    "editions/reader_manuscript/current/manifest.json",
    "editions/reader_manuscript/current/conclusion_claim_crosswalk.json",
    "editions/reader_manuscript/current/_quarto.yml",
    "editions/reader_manuscript/current/index.qmd",
    "editions/reader_manuscript/current/generated/edition-nav.html",
    "editions/reader_manuscript/current/generated/reader.scss",
    "editions/reader_manuscript/current/chapters/unit-01-asi-is-a-stack-not-a-model.qmd",
    "editions/reader_manuscript/current/generated/unit-01-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-02-the-efficient-asi-hypothesis.qmd",
    "editions/reader_manuscript/current/generated/unit-02-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-03-authority-failure-and-misuse.qmd",
    "editions/reader_manuscript/current/generated/unit-03-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-04-security-privacy-and-ai-artifact-custody.qmd",
    "editions/reader_manuscript/current/generated/unit-04-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd",
    "editions/reader_manuscript/current/generated/unit-05-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-06-human-intent-control-and-epistemic-security.qmd",
    "editions/reader_manuscript/current/generated/unit-06-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd",
    "editions/reader_manuscript/current/generated/unit-07-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-08-institutions-coordination-and-societal-resilience.qmd",
    "editions/reader_manuscript/current/generated/unit-08-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-09-stable-capability-fields-and-governed-replacement.qmd",
    "editions/reader_manuscript/current/generated/unit-09-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-10-perception-and-observation-trust.qmd",
    "editions/reader_manuscript/current/generated/unit-10-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd",
    "editions/reader_manuscript/current/generated/unit-11-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-12-planning-as-a-control-layer.qmd",
    "editions/reader_manuscript/current/generated/unit-12-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd",
    "editions/reader_manuscript/current/generated/unit-13-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd",
    "editions/reader_manuscript/current/generated/unit-14-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-15-verification-bandwidth-claim-ledgers-and-proof.qmd",
    "editions/reader_manuscript/current/generated/unit-15-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-16-labor-os-work-surfaces-and-organizations.qmd",
    "editions/reader_manuscript/current/generated/unit-16-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-17-artifact-graphs-runtime-effects-and-operations.qmd",
    "editions/reader_manuscript/current/generated/unit-17-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd",
    "editions/reader_manuscript/current/generated/unit-18-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd",
    "editions/reader_manuscript/current/generated/unit-19-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-20-governed-training-and-learning-compute-topology.qmd",
    "editions/reader_manuscript/current/generated/unit-20-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd",
    "editions/reader_manuscript/current/generated/unit-21-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd",
    "editions/reader_manuscript/current/generated/unit-22-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd",
    "editions/reader_manuscript/current/generated/unit-23-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-24-physical-compute-energy-and-infrastructure.qmd",
    "editions/reader_manuscript/current/generated/unit-24-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-25-recursive-improvement-replication-and-containment.qmd",
    "editions/reader_manuscript/current/generated/unit-25-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-26-integrated-reference-architecture-project-theseus-and-the-living-research-method.qmd",
    "editions/reader_manuscript/current/generated/unit-26-status.qmd",
    "docs/human_reader_26_unit_outline.md",
    "book_structure.json",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next((row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if unit is None:
        order = max(row["order"] for row in registry["units"]) + 1
        unit = {"id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    contract = {
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The canonical 26-unit outline, all 87 exact technical-owner routes and claim/source/proof/test/artifact/publication edges, independent maintained prose sources, and generated compact status panels.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Require exact owner coverage, honest drafting and target-length states, independent prose custody, canonical generated derivatives, a first-class /reader/ Pages route with reciprocal edition navigation, preserved support boundaries, and no major-version format or audio work.",
        "output_assertions": ["26 Human Reader units", "87 owners routed once", "canonical conclusion/claim crosswalk", "All 26 units within their declared word targets", "independent maintained prose", "Pages /reader/ publication path", "4 mutations reject", "support and release effects none"],
        "claim_scope": "Independent Human Reader manuscript structure and all 26 units' drafting completeness only.",
        "negative_controls": "validator_owned_route_length_and_support_mutations",
        "negative_control_cases": ["owner-route loss", "false length completion", "support laundering", "crosswalk owner-edge loss"],
        "prohibited_inference": "Draft or target-length completion does not establish editorial approval, evidence, publication, release, safety, readiness, SOTA, AGI, or ASI.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "checked_independent_human_reader_draft_contract",
    }
    unit.update(contract)
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    keys = [key for key in contract if key not in {"execution_tier", "validation_class"}]
    record = {"script": SCRIPT, "args": [], **{key: contract[key] for key in keys}}
    existing = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if existing is None:
        overrides["contracts"].append(record)
    else:
        existing.clear()
        existing.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
