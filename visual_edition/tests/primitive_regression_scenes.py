"""Static ManimCE scenes covering every public ASI Stack visual factory."""

from __future__ import annotations

from manim import DOWN, RIGHT, UP, VGroup

from visual_edition.lib.asi_visuals import (
    ACCENT,
    COPPER,
    EVIDENCE,
    AsiScene,
    authority_gate,
    evidence_badge,
    layer_card,
    proof_boundary,
    residual_marker,
    rollback_arrow,
    source_end_card,
    text,
    title_card,
)


class PrimitiveSymbolsRegression(AsiScene):
    """Exercise the shared cards, symbols, boundary, rollback, and text."""

    def construct(self) -> None:
        heading = text("SEMANTIC PRIMITIVES", size=30, color=ACCENT, weight="BOLD").to_edge(UP, buff=0.28)
        cards = VGroup(
            layer_card("PLAN", "typed proposal"),
            layer_card("VERIFY", "claim boundary", EVIDENCE),
            layer_card("EXECUTE", "narrow adapter", COPPER),
        ).arrange(RIGHT, buff=0.32).scale(0.66).next_to(heading, DOWN, buff=0.25)
        symbols = VGroup(
            authority_gate(),
            evidence_badge(),
            residual_marker(),
        ).arrange(RIGHT, buff=1.25).scale(0.88).next_to(cards, DOWN, buff=0.38)
        rollback = rollback_arrow().scale(0.72)
        boundary = proof_boundary("ENCODED SCOPE", "proof is not runtime enforcement").scale(0.64)
        footer = VGroup(rollback, boundary).arrange(RIGHT, buff=0.72).next_to(symbols, DOWN, buff=0.42)
        self.add(heading, cards, symbols, footer)


class PrimitiveFramingRegression(AsiScene):
    """Exercise shared opening and source-delivery framing."""

    def construct(self) -> None:
        opening = title_card(
            "ASI Stack Visual Grammar",
            "One promise, one visible mechanism",
            "primitive-regression",
        ).scale(0.72).to_edge(UP, buff=0.4)
        ending = source_end_card(
            "Primitive compatibility sheet",
            "none",
            "Visual grammar only; no chapter claim.",
            "A source-bound chapter treatment",
        ).scale(0.66).next_to(opening, DOWN, buff=0.48)
        self.add(opening, ending)


__all__ = ["PrimitiveSymbolsRegression", "PrimitiveFramingRegression"]
