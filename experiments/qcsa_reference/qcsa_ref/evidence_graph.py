"""QI-02: typed temporal evidence-bearing hypergraph."""

from __future__ import annotations

from dataclasses import dataclass, field

from .canonical import ContractError, make_envelope


NODE_TYPES = {"object", "proposition", "evidence", "provenance", "belief", "authority", "lifecycle", "permitted_use"}
EDGE_TYPES = {"supports", "contradicts", "derived_from", "believed_as", "authorized_by", "valid_during", "permitted_for", "relates"}


@dataclass
class EvidenceGraph:
    namespace: str
    nodes: dict[str, dict] = field(default_factory=dict)
    hyperedges: list[dict] = field(default_factory=list)

    def add_node(self, node_id: str, node_type: str, value: object, *, valid_from: str, valid_to: str | None = None) -> None:
        if node_id in self.nodes:
            raise ContractError("duplicate graph node")
        if node_type not in NODE_TYPES:
            raise ContractError("unknown graph node type")
        self.nodes[node_id] = {"id": node_id, "type": node_type, "value": value, "valid_from": valid_from, "valid_to": valid_to}

    def add_edge(self, edge_id: str, edge_type: str, sources: list[str], targets: list[str], *, provenance: str) -> None:
        if edge_type not in EDGE_TYPES:
            raise ContractError("unknown hyperedge type")
        if not sources or not targets or any(node not in self.nodes for node in sources + targets):
            raise ContractError("dangling or empty hyperedge")
        if edge_type in {"supports", "contradicts"} and not all(self.nodes[target]["type"] == "proposition" for target in targets):
            raise ContractError("evidence relation target must be proposition")
        self.hyperedges.append({"id": edge_id, "type": edge_type, "sources": sources, "targets": targets, "provenance": provenance})

    def artifact(self, input_digests: list[str]) -> dict:
        by_type = {kind: [row for row in self.nodes.values() if row["type"] == kind] for kind in NODE_TYPES}
        payload = {
            "nodes": [self.nodes[key] for key in sorted(self.nodes)],
            "hyperedges": self.hyperedges,
            "propositions": by_type["proposition"],
            "evidence": by_type["evidence"],
            "provenance": by_type["provenance"],
            "beliefs": by_type["belief"],
            "authorities": by_type["authority"],
            "lifecycles": by_type["lifecycle"],
            "permitted_uses": by_type["permitted_use"],
            "contradictions": [edge for edge in self.hyperedges if edge["type"] == "contradicts"],
        }
        return make_envelope(
            "QI-02", f"{self.namespace}:evidence", ["claim-ledgers-and-belief-revision"], payload,
            input_digests=input_digests,
            non_claim_boundary="Finite typed graph integrity only; graph position and edge validity do not establish proposition truth.",
        )
