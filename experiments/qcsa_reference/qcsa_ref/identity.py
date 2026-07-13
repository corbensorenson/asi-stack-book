"""QI-01: stable semantic identity and alias/merge/split lineage."""

from __future__ import annotations

from dataclasses import dataclass, field

from .canonical import ContractError, artifact_id, make_envelope


KINDS = {"occurrence", "type", "instance", "proposition", "expression", "tool", "policy", "obligation"}


@dataclass
class SOIDRegistry:
    namespace: str
    objects: dict[str, dict] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
    merge_lineage: list[dict] = field(default_factory=list)
    split_lineage: list[dict] = field(default_factory=list)

    def new_soid(self, opaque_seed: str) -> str:
        return "soid:" + artifact_id(f"{self.namespace}:{opaque_seed}").split(":", 1)[1]

    def add_object(self, soid: str, kind: str, *, lifecycle: str = "active") -> None:
        if soid in self.objects:
            raise ContractError("duplicate SOID")
        if kind not in KINDS:
            raise ContractError("unknown semantic object kind")
        self.objects[soid] = {"soid": soid, "kind": kind, "lifecycle": lifecycle}

    def add_alias(self, alias: str, soid: str) -> None:
        key = alias.casefold().strip()
        if soid not in self.objects:
            raise ContractError("alias references unknown SOID")
        if key in self.aliases and self.aliases[key] != soid:
            raise ContractError("silent alias retarget forbidden")
        self.aliases[key] = soid

    def merge(self, sources: list[str], target: str) -> None:
        if target not in self.objects or not sources or any(source not in self.objects for source in sources):
            raise ContractError("merge lineage references unknown SOID")
        if target in sources:
            raise ContractError("merge target must be distinct")
        self.merge_lineage.append({"sources": sorted(sources), "target": target})
        for source in sources:
            self.objects[source]["lifecycle"] = "merged"

    def split(self, source: str, targets: list[str]) -> None:
        if source not in self.objects or len(targets) < 2 or any(target not in self.objects for target in targets):
            raise ContractError("split lineage references unknown SOID")
        if source in targets:
            raise ContractError("split cannot silently retain source as child")
        self.split_lineage.append({"source": source, "targets": sorted(targets)})
        self.objects[source]["lifecycle"] = "split"

    def resolve_alias(self, alias: str) -> str:
        key = alias.casefold().strip()
        if key not in self.aliases:
            raise ContractError("unknown alias")
        return self.aliases[key]

    def artifact(self) -> dict:
        payload = {
            "objects": [self.objects[key] for key in sorted(self.objects)],
            "aliases": [{"alias": key, "soid": self.aliases[key]} for key in sorted(self.aliases)],
            "merge_lineage": self.merge_lineage,
            "split_lineage": self.split_lineage,
            "duplicate_controls": {"duplicate_soid": "reject", "duplicate_alias_same_target": "idempotent"},
            "retarget_controls": {"alias_new_target": "reject", "address_new_soid": "reject_or_typed_migration_failure"},
        }
        return make_envelope(
            "QI-01", f"{self.namespace}:registry", ["cognitive-compilation-and-semantic-ir", "virtual-context-abi"], payload,
            non_claim_boundary="Bounded local identity registry behavior only; no ontology correctness or universal identity claim.",
        )
