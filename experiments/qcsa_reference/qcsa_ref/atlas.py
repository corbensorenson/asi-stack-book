"""QI-03: plural semantic atlas views and immutable epochs."""

from __future__ import annotations

from dataclasses import dataclass, field

from .canonical import ContractError, make_envelope, sha256


@dataclass(frozen=True)
class AtlasEpoch:
    epoch_id: str
    authority_state: str
    facets: tuple[str, ...]
    paths: dict[str, dict[str, list[str]]]
    residuals: dict[str, list[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.authority_state not in {"candidate", "authoritative"}:
            raise ContractError("unknown epoch authority state")
        if len(self.facets) < 3 or len(set(self.facets)) != len(self.facets):
            raise ContractError("atlas requires at least three distinct facets")
        for soid, views in self.paths.items():
            if not views or any(facet not in self.facets or not path for facet, path in views.items()):
                raise ContractError(f"invalid path set for {soid}")

    @property
    def codebook_digest(self) -> str:
        return sha256({"epoch_id": self.epoch_id, "facets": self.facets, "paths": self.paths})

    def resolve(self, candidates: list[tuple[str, float]], *, top_k: int = 3, commit_threshold: float = 0.7) -> dict:
        ordered = sorted(candidates, key=lambda row: (-row[1], row[0]))[:top_k]
        if not ordered:
            return {"status": "unknown", "top_k": [], "selected_soid": None}
        if len(ordered) > 1 and abs(ordered[0][1] - ordered[1][1]) < 0.05:
            return {"status": "conflicting", "top_k": ordered, "selected_soid": None}
        if ordered[0][1] < commit_threshold:
            return {"status": "abstain", "top_k": ordered, "selected_soid": None}
        if ordered[0][0] not in self.paths:
            return {"status": "unknown", "top_k": ordered, "selected_soid": None}
        return {"status": "resolved", "top_k": ordered, "selected_soid": ordered[0][0]}

    def artifact(self, input_digests: list[str]) -> dict:
        sample = self.resolve([], top_k=3)
        payload = {
            "epoch_id": self.epoch_id,
            "authority_state": self.authority_state,
            "candidate_epoch": {"epoch_id": f"{self.epoch_id}-candidate-successor", "authority_state": "candidate", "may_route_effects": False},
            "immutable": True,
            "facets": list(self.facets),
            "paths": self.paths,
            "top_k": 3,
            "unknowns": [sample],
            "conflicts": [{"status": "conflicting", "policy": "preserve candidates"}],
            "abstentions": [{"status": "abstain", "threshold": 0.7}],
            "codebook_digest": self.codebook_digest,
        }
        return make_envelope(
            "QI-03", f"atlas:{self.epoch_id}", ["virtual-context-abi", "compact-generative-systems-and-residual-honesty"], payload,
            input_digests=input_digests,
            non_claim_boundary="Bounded deterministic atlas structure only; no learned semantic quality or retrieval advantage claim.",
        )
