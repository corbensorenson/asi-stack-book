#!/usr/bin/env python3
"""Validate EM0/EM1 role coverage without implying editorial cutover."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Optional

from build_editorial_migration_preview import (
    OUTLINE,
    PREVIEW,
    ROOT,
    STATUS,
    STRUCTURE,
    build_preview,
    chapters,
    outline_units,
)


EXPECTED_ROLE_COUNTS = {
    "primary_architecture_owner": 54,
    "implementation_method_owner": 2,
    "publication_nest": 15,
    "method_detail_nest": 2,
    "semantic_merge_candidate": 1,
    "deployment_profile_owner": 7,
    "research_dossier_owner": 5,
    "generated_back_matter_owner": 1,
}
MAIN_ROLES = {"primary_architecture_owner", "implementation_method_owner"}
NEST_ROLES = {"publication_nest", "method_detail_nest", "semantic_merge_candidate"}
COLLECTION_ROLES = {
    "deployment_profile_owner",
    "research_dossier_owner",
    "generated_back_matter_owner",
}
EXPECTED_VISIBILITY = {
    "primary_architecture_owner": "main_book",
    "implementation_method_owner": "main_book",
    "publication_nest": "technical_detail",
    "method_detail_nest": "technical_detail",
    "semantic_merge_candidate": "technical_detail",
    "deployment_profile_owner": "deployment_profile",
    "research_dossier_owner": "research_dossier",
    "generated_back_matter_owner": "generated_back_matter",
}
METHOD_DETAIL_PARENT_IDS = {
    "resource-economics-and-token-budgets",
    "compact-generative-systems-and-residual-honesty",
}
METHOD_DETAIL_CHILD_IDS = {
    "fast-generation-architectures",
    "governed-deliberation-and-test-time-scaling",
    "rankfold-neuralfold-and-artifact-compression",
}
SECURITY_CUSTODY_PARENT_IDS = {
    "security-kernel-and-digital-scifs",
    "privacy-data-rights-and-information-flow-governance",
    "model-weight-custody-and-hardware-roots-of-trust",
}
SECURITY_CUSTODY_CHILD_IDS = {
    "adversarial-machine-learning-and-model-attack-surface",
    "confidential-and-verifiable-ai-computation",
    "ai-supply-chain-integrity-and-lifecycle-provenance",
    "open-weight-release-and-post-release-control",
}
WHITE_BOX_PARENT_IDS = {
    "adversarial-evaluation-sandbagging-and-training-time-deception",
}
WHITE_BOX_CHILD_IDS = {
    "white-box-evidence-interpretability-and-activation-governance",
}
HUMAN_INSTITUTIONAL_PARENT_IDS = {
    "constitutional-alignment-substrate",
    "human-factors-and-meaningful-control-in-oversight",
    "institutions-international-coordination-and-public-legitimacy",
    "intent-to-execution-contracts",
}
HUMAN_INSTITUTIONAL_CHILD_IDS = {
    "human-ai-communication-persuasion-and-epistemic-security",
    "human-intent-as-a-formal-input",
    "moral-uncertainty-and-value-conflict",
    "societal-resilience-and-misuse-defense",
}
CONTEXT_ORGANIZATION_EXCHANGE_PARENT_IDS = {
    "virtual-context-abi",
    "ai-work-surfaces-agent-harnesses-and-organizational-absorption",
    "inter-stack-protocols-identity-and-economic-exchange",
}
CONTEXT_ORGANIZATION_EXCHANGE_CHILD_IDS = {
    "context-transactions-snapshots-mounts-and-taint",
    "human-ai-organizations-delegation-and-accountability",
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
}
COMPOSED_PARENT_IDS = (
    METHOD_DETAIL_PARENT_IDS
    | SECURITY_CUSTODY_PARENT_IDS
    | WHITE_BOX_PARENT_IDS
    | HUMAN_INSTITUTIONAL_PARENT_IDS
    | CONTEXT_ORGANIZATION_EXCHANGE_PARENT_IDS
)
COMPOSED_CHILD_IDS = (
    METHOD_DETAIL_CHILD_IDS
    | SECURITY_CUSTODY_CHILD_IDS
    | WHITE_BOX_CHILD_IDS
    | HUMAN_INSTITUTIONAL_CHILD_IDS
    | CONTEXT_ORGANIZATION_EXCHANGE_CHILD_IDS
)
COMPOSITION_SURFACES = {
    "resource-economics-and-token-budgets": (
        "chapters/resource-economics-and-token-budgets.qmd",
        [
            "### Generation mode and deliberation depth are allocation decisions",
            "[Fast Generation Architectures](fast-generation-architectures.qmd)",
            "[Governed Deliberation and Test-Time Scaling](governed-deliberation-and-test-time-scaling.qmd)",
            "inherits another's claim support",
        ],
    ),
    "compact-generative-systems-and-residual-honesty": (
        "chapters/compact-generative-systems-and-residual-honesty.qmd",
        [
            "### RankFold and NeuralFold as a technical method dossier",
            "(rankfold-neuralfold-and-artifact-compression.qmd)",
            "does not inherit a codec result",
        ],
    ),
    "fast-generation-architectures": (
        "chapters/fast-generation-architectures.qmd",
        ["### Publication placement and preserved technical ownership", "(resource-economics-and-token-budgets.qmd)"],
    ),
    "governed-deliberation-and-test-time-scaling": (
        "chapters/governed-deliberation-and-test-time-scaling.qmd",
        ["### Publication placement and preserved technical ownership", "(resource-economics-and-token-budgets.qmd)"],
    ),
    "rankfold-neuralfold-and-artifact-compression": (
        "chapters/rankfold-neuralfold-and-artifact-compression.qmd",
        ["### Publication placement and preserved technical ownership", "(compact-generative-systems-and-residual-honesty.qmd)"],
    ),
    "security-kernel-and-digital-scifs": (
        "chapters/security-kernel-and-digital-scifs.qmd",
        [
            "### Learned-model threats inside the authority-use boundary",
            "(adversarial-machine-learning-and-model-attack-surface.qmd)",
            "Neither chapter inherits the\nother's claim support",
        ],
    ),
    "adversarial-machine-learning-and-model-attack-surface": (
        "chapters/adversarial-machine-learning-and-model-attack-surface.qmd",
        ["### Publication placement and preserved technical ownership", "(security-kernel-and-digital-scifs.qmd)"],
    ),
    "privacy-data-rights-and-information-flow-governance": (
        "chapters/privacy-data-rights-and-information-flow-governance.qmd",
        [
            "### Protected computation inside the information-lifecycle transaction",
            "(confidential-and-verifiable-ai-computation.qmd)",
            "does not inherit privacy, compliance, total",
        ],
    ),
    "confidential-and-verifiable-ai-computation": (
        "chapters/confidential-and-verifiable-ai-computation.qmd",
        ["### Publication placement and preserved technical ownership", "(privacy-data-rights-and-information-flow-governance.qmd)"],
    ),
    "model-weight-custody-and-hardware-roots-of-trust": (
        "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd",
        [
            "### Lineage and irreversible release inside custody",
            "(ai-supply-chain-integrity-and-lifecycle-provenance.qmd)",
            "(open-weight-release-and-post-release-control.qmd)",
            "without inheriting another's claim support",
        ],
    ),
    "ai-supply-chain-integrity-and-lifecycle-provenance": (
        "chapters/ai-supply-chain-integrity-and-lifecycle-provenance.qmd",
        ["### Publication placement and preserved technical ownership", "(model-weight-custody-and-hardware-roots-of-trust.qmd)"],
    ),
    "open-weight-release-and-post-release-control": (
        "chapters/open-weight-release-and-post-release-control.qmd",
        ["### Publication placement and preserved technical ownership", "(model-weight-custody-and-hardware-roots-of-trust.qmd)"],
    ),
    "adversarial-evaluation-sandbagging-and-training-time-deception": (
        "chapters/adversarial-evaluation-sandbagging-and-training-time-deception.qmd",
        [
            "### Internal evidence inside the evaluation-integrity boundary",
            "(white-box-evidence-interpretability-and-activation-governance.qmd)",
            "does not\ninherit a white-box mechanism",
        ],
    ),
    "white-box-evidence-interpretability-and-activation-governance": (
        "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
        [
            "### Publication placement and preserved technical ownership",
            "(adversarial-evaluation-sandbagging-and-training-time-deception.qmd)",
            "does not inherit a\ndeception",
        ],
    ),
    "human-factors-and-meaningful-control-in-oversight": (
        "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
        [
            "### Communication inside the meaningful-control boundary",
            "(human-ai-communication-persuasion-and-epistemic-security.qmd)",
            "The placement blocks two substitutions.",
        ],
    ),
    "human-ai-communication-persuasion-and-epistemic-security": (
        "chapters/human-ai-communication-persuasion-and-epistemic-security.qmd",
        [
            "### Publication placement and preserved technical ownership",
            "(human-factors-and-meaningful-control-in-oversight.qmd)",
            "The claims remain separate.",
        ],
    ),
    "constitutional-alignment-substrate": (
        "chapters/constitutional-alignment-substrate.qmd",
        [
            "### Moral conflict inside the constitutional boundary",
            "(moral-uncertainty-and-value-conflict.qmd)",
            "The placement prevents a constitutional predicate",
        ],
    ),
    "moral-uncertainty-and-value-conflict": (
        "chapters/moral-uncertainty-and-value-conflict.qmd",
        [
            "### Publication placement and preserved technical ownership",
            "(constitutional-alignment-substrate.qmd)",
            "That placement does not collapse plural values",
        ],
    ),
    "institutions-international-coordination-and-public-legitimacy": (
        "chapters/institutions-international-coordination-and-public-legitimacy.qmd",
        [
            "### Resilience inside the institutional boundary",
            "(societal-resilience-and-misuse-defense.qmd)",
            "The family preserves both directions of non-substitution.",
        ],
    ),
    "societal-resilience-and-misuse-defense": (
        "chapters/societal-resilience-and-misuse-defense.qmd",
        [
            "### Publication placement and preserved technical ownership",
            "(institutions-international-coordination-and-public-legitimacy.qmd)",
            "A closed provider ticket",
        ],
    ),
    "intent-to-execution-contracts": (
        "chapters/intent-to-execution-contracts.qmd",
        [
            "### Intent resolution before command lowering",
            "(human-intent-as-a-formal-input.qmd)",
            "The placement blocks assumption laundering",
        ],
    ),
    "human-intent-as-a-formal-input": (
        "chapters/human-intent-as-a-formal-input.qmd",
        [
            "### Publication placement and preserved technical ownership",
            "(intent-to-execution-contracts.qmd)",
            "An accepted intent record does not establish",
        ],
    ),
    "virtual-context-abi": (
        "chapters/virtual-context-abi.qmd",
        [
            "### Transactions inside the context ABI boundary",
            "(context-transactions-snapshots-mounts-and-taint.qmd)",
            "The placement preserves a necessary asymmetry.",
        ],
    ),
    "context-transactions-snapshots-mounts-and-taint": (
        "chapters/context-transactions-snapshots-mounts-and-taint.qmd",
        [
            "### Dynamic context state beneath the ABI",
            "(virtual-context-abi.qmd)",
            "does not turn a packet certificate into transaction evidence",
        ],
    ),
    "ai-work-surfaces-agent-harnesses-and-organizational-absorption": (
        "chapters/ai-work-surfaces-agent-harnesses-and-organizational-absorption.qmd",
        [
            "### Organizations inside the work-surface boundary",
            "(human-ai-organizations-delegation-and-accountability.qmd)",
            "The placement blocks product history from becoming institutional authority.",
        ],
    ),
    "human-ai-organizations-delegation-and-accountability": (
        "chapters/human-ai-organizations-delegation-and-accountability.qmd",
        [
            "### Accountable organizations beneath evolving work surfaces",
            "(ai-work-surfaces-agent-harnesses-and-organizational-absorption.qmd)",
            "does not let adoption, autonomy, or task coverage stand in",
        ],
    ),
    "inter-stack-protocols-identity-and-economic-exchange": (
        "chapters/inter-stack-protocols-identity-and-economic-exchange.qmd",
        [
            "### Population dynamics inside the protocol boundary",
            "(multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd)",
            "The placement blocks local protocol validity from becoming systemic assurance.",
        ],
    ),
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk": (
        "chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd",
        [
            "### Population dynamics above valid inter-stack protocols",
            "(inter-stack-protocols-identity-and-economic-exchange.qmd)",
            "does not turn protocol conformance into a claim about the",
        ],
    ),
}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(
    structure: dict,
    status: dict,
    preview: dict,
    surface_texts: Optional[dict[str, str]] = None,
) -> list[str]:
    errors: list[str] = []
    rows = chapters(structure)
    ids = {row.get("id") for row in rows}
    editorial = status.get("editorial_product_migration", {})
    expected_parent = {
        **editorial.get("merge_map", {}),
        **editorial.get("profile_map", {}),
        **editorial.get("dossier_map", {}),
        **editorial.get("back_matter_map", {}),
    }
    expected_role = dict(editorial.get("merge_mode_map", {}))
    expected_role.update({key: "deployment_profile_owner" for key in editorial.get("profile_map", {})})
    expected_role.update({key: "research_dossier_owner" for key in editorial.get("dossier_map", {})})
    expected_role.update({key: "generated_back_matter_owner" for key in editorial.get("back_matter_map", {})})
    expected_role.update({key: "implementation_method_owner" for key in editorial.get("implementation_method_ids", [])})

    role_counts = {role: 0 for role in EXPECTED_ROLE_COUNTS}
    unit_routes: dict[str, list[str]] = {}
    for row in rows:
        chapter_id = row.get("id")
        publication = row.get("publication")
        if not isinstance(publication, dict):
            errors.append(f"{chapter_id}: missing publication metadata")
            continue
        role = publication.get("role")
        if role not in role_counts:
            errors.append(f"{chapter_id}: invalid publication role {role!r}")
            continue
        role_counts[role] += 1
        expected = expected_role.get(chapter_id, "primary_architecture_owner")
        if role != expected:
            errors.append(f"{chapter_id}: role {role!r} != reviewed disposition {expected!r}")
        if publication.get("visibility") != EXPECTED_VISIBILITY[role]:
            errors.append(f"{chapter_id}: visibility drift")
        parent_id = publication.get("parent_id")
        if parent_id != expected_parent.get(chapter_id):
            errors.append(f"{chapter_id}: parent drift")
        if role in MAIN_ROLES and parent_id is not None:
            errors.append(f"{chapter_id}: main-book owner has a parent")
        if role in NEST_ROLES and parent_id not in ids:
            errors.append(f"{chapter_id}: nested owner parent is not a canonical chapter")
        if role in COLLECTION_ROLES and not isinstance(parent_id, str):
            errors.append(f"{chapter_id}: collection owner has an invalid collection parent")
        if publication.get("legacy_id") != chapter_id or publication.get("legacy_file") != row.get("file"):
            errors.append(f"{chapter_id}: legacy identity or route drift")
        if publication.get("claim_ownership") != "preserved_local_no_inheritance":
            errors.append(f"{chapter_id}: claim ownership can be inherited")
        expected_editorial_state = "metadata_classified_prose_unchanged"
        if chapter_id in COMPOSED_PARENT_IDS:
            expected_editorial_state = "family_composed_preserving_technical_owners"
        elif chapter_id in COMPOSED_CHILD_IDS:
            expected_editorial_state = "composed_preserving_technical_owner"
        if publication.get("editorial_state") != expected_editorial_state:
            errors.append(f"{chapter_id}: editorial composition state drift")
        if publication.get("support_state_effect") != "none":
            errors.append(f"{chapter_id}: metadata migration changed support state")
        unit_id = row.get("human_reader_unit_id")
        if not isinstance(unit_id, str):
            errors.append(f"{chapter_id}: missing Human Reader route")
        else:
            unit_routes.setdefault(unit_id, []).append(chapter_id)

    if role_counts != EXPECTED_ROLE_COUNTS:
        errors.append(f"publication role counts drifted: {role_counts}")
    outline = outline_units()
    expected_units = {unit["unit_id"]: sorted(unit["owner_ids"]) for unit in outline}
    actual_units = {unit_id: sorted(owner_ids) for unit_id, owner_ids in unit_routes.items()}
    if actual_units != expected_units:
        errors.append("Human Reader owner routes disagree with the canonical 26-unit outline")
    if len(outline) != 26 or set().union(*(set(unit["owner_ids"]) for unit in outline)) != ids:
        errors.append("Human Reader outline does not cover all canonical owners")
    if sum(len(unit["owner_ids"]) for unit in outline) != len(ids):
        errors.append("Human Reader outline duplicates an owner route")
    if preview != build_preview(structure):
        errors.append("editorial migration preview is not its canonical derivation")
    if editorial.get("em0_count_reconciliation_complete") is not True:
        errors.append("EM0 count reconciliation is not complete")
    if editorial.get("stale_active_product_count_literal_count") != 0:
        errors.append("EM0 still records stale active product counts")
    if editorial.get("state") != "em2_five_packages_composed_public_cutover_pending":
        errors.append("editorial migration state does not record all five EM2 packages")
    expected_packages = [
        {
            "id": "em2-method-detail-pilot",
            "state": "composed_no_public_cutover",
            "parent_ids": sorted(METHOD_DETAIL_PARENT_IDS),
            "child_ids": sorted(METHOD_DETAIL_CHILD_IDS),
            "stable_technical_routes_preserved": True,
            "claim_support_inheritance": False,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        {
            "id": "em2-security-custody-publication-nests",
            "state": "composed_no_public_cutover",
            "parent_ids": sorted(SECURITY_CUSTODY_PARENT_IDS),
            "child_ids": sorted(SECURITY_CUSTODY_CHILD_IDS),
            "stable_technical_routes_preserved": True,
            "claim_support_inheritance": False,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        {
            "id": "em2-white-box-evaluation-publication-nest",
            "state": "composed_no_public_cutover",
            "parent_ids": sorted(WHITE_BOX_PARENT_IDS),
            "child_ids": sorted(WHITE_BOX_CHILD_IDS),
            "stable_technical_routes_preserved": True,
            "claim_support_inheritance": False,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        {
            "id": "em2-human-intent-and-institutional-governance-publication-nests",
            "state": "composed_no_public_cutover",
            "parent_ids": sorted(HUMAN_INSTITUTIONAL_PARENT_IDS),
            "child_ids": sorted(HUMAN_INSTITUTIONAL_CHILD_IDS),
            "stable_technical_routes_preserved": True,
            "claim_support_inheritance": False,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        {
            "id": "em2-context-organization-and-exchange-publication-nests",
            "state": "composed_no_public_cutover",
            "parent_ids": sorted(CONTEXT_ORGANIZATION_EXCHANGE_PARENT_IDS),
            "child_ids": sorted(CONTEXT_ORGANIZATION_EXCHANGE_CHILD_IDS),
            "stable_technical_routes_preserved": True,
            "claim_support_inheritance": False,
            "support_state_effect": "none",
            "release_effect": "none",
        },
    ]
    if editorial.get("completed_composition_packages") != expected_packages:
        errors.append("EM2 composition-package receipts drifted")
    if editorial.get("support_state_effect") != "none" or editorial.get("release_effect") != "none":
        errors.append("editorial migration moved support or release state")
    if surface_texts is None:
        surface_texts = {
            chapter_id: (ROOT / path).read_text(encoding="utf-8")
            for chapter_id, (path, _) in COMPOSITION_SURFACES.items()
        }
    for chapter_id, (_, fragments) in COMPOSITION_SURFACES.items():
        text = surface_texts.get(chapter_id, "")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{chapter_id}: missing composition boundary {fragment!r}")
    return errors


def main() -> None:
    structure = load(STRUCTURE)
    status = load(STATUS)
    preview = load(PREVIEW)
    if not all(isinstance(value, dict) for value in (structure, status, preview)):
        raise SystemExit("editorial migration inputs must contain objects")
    errors = validate(structure, status, preview)

    mutations = []
    first = chapters(structure)[0]
    altered = copy.deepcopy(structure)
    chapters(altered)[0]["publication"]["support_state_effect"] = "promoted"
    mutations.append(("support promotion", altered))
    altered = copy.deepcopy(structure)
    chapters(altered)[0]["human_reader_unit_id"] = "unit-26"
    mutations.append(("owner reroute", altered))
    nested_index = next(i for i, row in enumerate(chapters(structure)) if row["publication"]["role"] in NEST_ROLES)
    altered = copy.deepcopy(structure)
    chapters(altered)[nested_index]["publication"]["parent_id"] = None
    mutations.append(("parent erasure", altered))
    for label, altered in mutations:
        if not validate(altered, status, build_preview(altered)):
            errors.append(f"negative control accepted: {label}")
    surfaces = {
        chapter_id: (ROOT / path).read_text(encoding="utf-8")
        for chapter_id, (path, _) in COMPOSITION_SURFACES.items()
    }
    altered_surfaces = dict(surfaces)
    altered_surfaces["resource-economics-and-token-budgets"] = altered_surfaces[
        "resource-economics-and-token-budgets"
    ].replace("inherits another's claim support", "shares claim support")
    if not validate(structure, status, preview, altered_surfaces):
        errors.append("negative control accepted: composition-boundary erasure")
    altered_surfaces = dict(surfaces)
    altered_surfaces["model-weight-custody-and-hardware-roots-of-trust"] = altered_surfaces[
        "model-weight-custody-and-hardware-roots-of-trust"
    ].replace("without inheriting another's claim support", "while sharing claim support")
    if not validate(structure, status, preview, altered_surfaces):
        errors.append("negative control accepted: security-custody composition-boundary erasure")
    altered_surfaces = dict(surfaces)
    altered_surfaces["adversarial-evaluation-sandbagging-and-training-time-deception"] = altered_surfaces[
        "adversarial-evaluation-sandbagging-and-training-time-deception"
    ].replace("does not\ninherit a white-box mechanism", "inherits the white-box mechanism")
    if not validate(structure, status, preview, altered_surfaces):
        errors.append("negative control accepted: white-box composition-boundary erasure")
    human_boundary_mutations = [
        (
            "human-factors-and-meaningful-control-in-oversight",
            "The placement blocks two substitutions.",
            "The placement permits substitution.",
            "human-control/communication boundary erasure",
        ),
        (
            "constitutional-alignment-substrate",
            "The placement prevents a constitutional predicate",
            "The placement allows a constitutional predicate",
            "constitution/moral-conflict boundary erasure",
        ),
        (
            "institutions-international-coordination-and-public-legitimacy",
            "The family preserves both directions of non-substitution.",
            "The family permits substitution.",
            "institution/resilience boundary erasure",
        ),
        (
            "intent-to-execution-contracts",
            "The placement blocks assumption laundering",
            "The placement permits assumption laundering",
            "intent/command boundary erasure",
        ),
    ]
    for chapter_id, good, bad, label in human_boundary_mutations:
        altered_surfaces = dict(surfaces)
        altered_surfaces[chapter_id] = altered_surfaces[chapter_id].replace(good, bad)
        if not validate(structure, status, preview, altered_surfaces):
            errors.append(f"negative control accepted: {label}")
    composition_boundary_mutations = [
        (
            "virtual-context-abi",
            "The placement preserves a necessary asymmetry.",
            "The placement permits static and dynamic substitution.",
            "context static/dynamic boundary erasure",
        ),
        (
            "ai-work-surfaces-agent-harnesses-and-organizational-absorption",
            "The placement blocks product history from becoming institutional authority.",
            "The placement turns product history into institutional authority.",
            "work-surface/organization boundary erasure",
        ),
        (
            "inter-stack-protocols-identity-and-economic-exchange",
            "The placement blocks local protocol validity from becoming systemic assurance.",
            "The placement turns local protocol validity into systemic assurance.",
            "protocol/population boundary erasure",
        ),
    ]
    for chapter_id, good, bad, label in composition_boundary_mutations:
        altered_surfaces = dict(surfaces)
        altered_surfaces[chapter_id] = altered_surfaces[chapter_id].replace(good, bad)
        if not validate(structure, status, preview, altered_surfaces):
            errors.append(f"negative control accepted: {label}")

    if errors:
        raise SystemExit("Editorial migration validation failed:\n - " + "\n - ".join(errors))
    print(
        "Editorial migration validation passed: 87 owners, 54+2 main-book owners, "
        "15 publication nests, 2 method-detail nests, 1 semantic candidate, "
        "7 profiles, 5 dossier owners, 1 back-matter owner, 26 Human Reader routes, "
        "and 13 rejecting controls."
    )


if __name__ == "__main__":
    main()
