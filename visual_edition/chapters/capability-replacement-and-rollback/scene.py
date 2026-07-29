"""P7.3 pilot: Capability Replacement and Rollback."""

from __future__ import annotations

from manim import (
    Arrow,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    Indicate,
    LEFT,
    Line,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    VGroup,
    Write,
    UP,
)

from visual_edition.lib.asi_visuals import (
    ACCENT,
    AUTHORITY,
    BOUNDARY,
    COPPER,
    EVIDENCE,
    INK,
    MUTED,
    RESIDUAL,
    ROLLBACK,
    SURFACE,
    AsiScene,
    proof_boundary,
    residual_marker,
    source_end_card,
    text,
    title_card,
)


def chip(label: str, color: str = BOUNDARY, width: float = 1.72) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=0.58,
        corner_radius=0.08,
        color=color,
        fill_color=SURFACE,
        fill_opacity=1,
        stroke_width=2.5,
    )
    return VGroup(box, text(label, size=16, color=color, weight="BOLD").move_to(box))


class CapabilityReplacementAndRollback(AsiScene):
    """A 285-second visual abstract synchronized to the canonical narration."""

    TARGET_DURATION = 285.0

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def construct(self) -> None:
        for method, end in (
            (self.not_a_swap, 39),
            (self.freeze_inventory, 78),
            (self.lifecycle, 118),
            (self.rollback_trace, 162),
            (self.recovery_vector, 200),
            (self.evidence_ledger, 244),
            (self.boundary_handoff, 285),
        ):
            method()
            self.wait_until(end)
            if end < self.TARGET_DURATION:
                self.clear_scene()

    def not_a_swap(self) -> None:
        heading = title_card(
            "Capability Replacement and Rollback",
            "A transaction, not a component swap",
            "capability-replacement-and-rollback",
        ).scale(0.78).to_edge(UP, buff=0.25)
        field = RoundedRectangle(
            width=10.5, height=3.4, corner_radius=0.18, color=ACCENT,
            fill_color=SURFACE, fill_opacity=0.25, stroke_width=4,
        ).shift(UP * -1.0)
        field_label = text("STABLE CAPABILITY FIELD", size=21, color=ACCENT, weight="BOLD").next_to(field, UP, buff=0.08)
        prior = chip("PRIOR A", EVIDENCE, 1.9).scale(1.15).move_to(LEFT * 3.8 + UP * -0.6)
        candidate = chip("CANDIDATE B", AUTHORITY, 2.25).scale(1.15).move_to(RIGHT * 3.8 + UP * -0.6)
        surfaces = VGroup(*[
            chip(label, color, 1.58)
            for label, color in (
                ("weights", COPPER), ("optimizer", BOUNDARY), ("RNG", BOUNDARY),
                ("cache", BOUNDARY), ("policy", AUTHORITY), ("route", ACCENT),
                ("backup", BOUNDARY), ("descendant", RESIDUAL), ("effects", ROLLBACK),
            )
        ]).arrange_in_grid(rows=3, cols=3, buff=(0.18, 0.15)).scale(0.75).shift(UP * -1.2)
        arrow = Arrow(candidate.get_left(), field.get_right(), buff=0.1, color=AUTHORITY, stroke_width=5)
        self.play(Write(heading), run_time=1.2)
        self.play(Create(field), FadeIn(field_label), FadeIn(prior), run_time=0.9)
        self.play(FadeIn(candidate), Create(arrow), run_time=0.8)
        self.play(FadeIn(surfaces), run_time=1.0)

    def freeze_inventory(self) -> None:
        heading = text("FREEZE BEFORE OUTCOMES", size=38, color=INK, weight="BOLD").to_edge(UP)
        lock = VGroup(
            RoundedRectangle(width=4.0, height=1.0, corner_radius=0.12, color=AUTHORITY, stroke_width=4),
            text("FROZEN PROSPECTIVELY", size=24, color=AUTHORITY, weight="BOLD"),
        )
        rows = VGroup(*[
            chip(label, color, 2.0)
            for label, color in (
                ("field + versions", ACCENT), ("checkpoint", AUTHORITY),
                ("evaluator", EVIDENCE), ("monitor", EVIDENCE),
                ("state inventory", BOUNDARY), ("effect inventory", ROLLBACK),
                ("owners", COPPER), ("thresholds", AUTHORITY),
                ("canary scope", ACCENT), ("expiry", BOUNDARY),
                ("descendants", RESIDUAL), ("commitments", RESIDUAL),
            )
        ]).arrange_in_grid(rows=4, cols=3, buff=(0.2, 0.18)).scale(0.82).shift(UP * -0.8)
        omitted = residual_marker("OMITTED ≠ RECOVERED").scale(0.72).to_edge(RIGHT, buff=0.4).shift(UP * -2.55)
        self.play(Write(heading), FadeIn(lock), run_time=1.0)
        for row in rows:
            self.play(FadeIn(row), run_time=0.12)
        self.play(FadeIn(omitted), run_time=0.6)

    def lifecycle(self) -> None:
        heading = text("PHASE-GATED REPLACEMENT", size=39, color=INK, weight="BOLD").to_edge(UP)
        labels = [
            ("1", "PROPOSED", ACCENT), ("2", "PRECHECK", EVIDENCE),
            ("3", "SHADOW", BOUNDARY), ("4", "CANARY", AUTHORITY),
            ("5", "COMMIT", COPPER), ("6", "MONITOR", EVIDENCE),
        ]
        nodes = VGroup()
        for number, label, color in labels:
            box = RoundedRectangle(width=1.72, height=0.92, corner_radius=0.1, color=color, fill_color=SURFACE, fill_opacity=1)
            nodes.add(VGroup(
                box,
                text(number, size=15, color=color, weight="BOLD").move_to(box.get_top() + UP * -0.16),
                text(label, size=17, color=INK, weight="BOLD").move_to(box.get_center() + UP * -0.1),
            ))
        nodes.arrange(RIGHT, buff=0.24).scale(0.91).shift(UP * 0.5)
        arrows = VGroup(*[
            Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.05, color=ACCENT, stroke_width=3)
            for i in range(len(nodes) - 1)
        ])
        terminals = VGroup(
            chip("ROLLBACK", ROLLBACK, 2.0), chip("COMPENSATE", COPPER, 2.2),
            chip("QUARANTINE", RESIDUAL, 2.2), chip("RETIRED", BOUNDARY, 1.8),
        ).arrange(RIGHT, buff=0.35).shift(UP * -1.65)
        branches = VGroup(*[
            DashedLine(nodes[index].get_bottom(), terminals[min(index, 3)].get_top(), color=ROLLBACK if index < 2 else RESIDUAL)
            for index in range(4)
        ])
        footer = text("candidate proposal ≠ accepted replacement ≠ completed recovery", size=23, color=MUTED).to_edge(UP * -1, buff=0.32)
        self.play(Write(heading), run_time=0.7)
        for i, node in enumerate(nodes):
            self.play(FadeIn(node), run_time=0.25)
            if i:
                self.play(Create(arrows[i - 1]), run_time=0.18)
        self.play(FadeIn(terminals), Create(branches), FadeIn(footer), run_time=1.0)

    def rollback_trace(self) -> None:
        heading = text("A MONITOR-TRIGGERED ROLLBACK", size=37, color=INK, weight="BOLD").to_edge(UP)
        prior = chip("ROUTE A", EVIDENCE, 2.0).scale(1.15).shift(LEFT * 4 + UP * 0.55)
        split = chip("95% A", ACCENT, 1.7).shift(LEFT * 1.5 + UP * 0.8)
        canary = chip("5% B CANARY", AUTHORITY, 2.25).shift(LEFT * 1.5 + UP * -0.05)
        monitor = chip("CRITICAL REGRESSION", ROLLBACK, 2.9).shift(RIGHT * 1.7 + UP * -0.05)
        restored = chip("A RESTORED", EVIDENCE, 2.25).shift(RIGHT * 4.35 + UP * 0.65)
        paths = VGroup(
            Arrow(prior.get_right(), split.get_left(), color=ACCENT, buff=0.08),
            Arrow(prior.get_right(), canary.get_left(), color=AUTHORITY, buff=0.08),
            Arrow(canary.get_right(), monitor.get_left(), color=ROLLBACK, buff=0.08),
            Arrow(monitor.get_right(), restored.get_left(), color=ROLLBACK, buff=0.08),
        )
        inventory = VGroup(*[chip(x, BOUNDARY, 1.62) for x in ("weights", "optimizer", "RNG", "cache", "route", "policy")])
        inventory.arrange(RIGHT, buff=0.16).scale(0.72).shift(UP * -1.55)
        remote = residual_marker("REMOTE COPY: COMPENSATE").scale(0.76).shift(RIGHT * 3.7 + UP * -2.35)
        self.play(Write(heading), FadeIn(prior), run_time=0.8)
        self.play(Create(paths[0]), FadeIn(split), Create(paths[1]), FadeIn(canary), run_time=0.9)
        self.play(Create(paths[2]), FadeIn(monitor), run_time=0.6)
        self.play(Indicate(monitor, color=ROLLBACK), run_time=0.5)
        self.play(Create(paths[3]), FadeIn(restored), run_time=0.7)
        self.play(FadeIn(inventory), FadeIn(remote), run_time=0.9)

    def recovery_vector(self) -> None:
        heading = text("RECOVERY IS A VECTOR, NOT A BOOLEAN", size=35, color=INK, weight="BOLD").to_edge(UP)
        pairs = (
            ("artifact bytes", "all state"), ("service restart", "behavior"),
            ("digest equality", "privacy repair"), ("compensation", "reversal"),
            ("receipt", "observation"), ("declared inventory", "complete reality"),
        )
        rows = VGroup()
        for left, right in pairs:
            rows.add(VGroup(
                text(left.upper(), size=21, color=INK, weight="BOLD"),
                text("≠", size=34, color=ROLLBACK, weight="BOLD"),
                text(right.upper(), size=21, color=MUTED, weight="BOLD"),
            ).arrange(RIGHT, buff=0.5))
        rows.arrange(UP * -1, buff=0.35, aligned_edge=LEFT).shift(UP * -0.25)
        self.play(Write(heading), run_time=0.8)
        for row in rows:
            self.play(FadeIn(row), run_time=0.38)

    def evidence_ledger(self) -> None:
        heading = text("WHAT THE BOUNDED CAMPAIGNS ACTUALLY SHOW", size=33, color=INK, weight="BOLD").to_edge(UP)
        cards = VGroup()
        for count, label, note, color in (
            ("15 / 15", "LOCAL TREES", "6 checkpoint disagreements", EVIDENCE),
            ("32 / 36", "ATTACK ROLLBACKS", "2 / 36 useful release", AUTHORITY),
            ("35 / 35", "NAMED SURFACES", "remote + external unresolved", ACCENT),
        ):
            box = RoundedRectangle(width=3.35, height=2.25, corner_radius=0.15, color=color, fill_color=SURFACE, fill_opacity=1)
            group = VGroup(
                text(count, size=42, color=color, weight="BOLD"),
                text(label, size=20, color=INK, weight="BOLD"),
                text(note, size=17, color=MUTED),
            ).arrange(UP * -1, buff=0.2).move_to(box)
            cards.add(VGroup(box, group))
        cards.arrange(RIGHT, buff=0.42).shift(UP * -0.35)
        footer = text("exact declared local recovery • no useful-release or production claim", size=22, color=RESIDUAL).to_edge(UP * -1, buff=0.5)
        self.play(Write(heading), run_time=0.8)
        for card in cards:
            self.play(FadeIn(card), run_time=0.5)
        self.play(FadeIn(footer), run_time=0.6)

    def boundary_handoff(self) -> None:
        boundary = proof_boundary(
            "BOUNDED LOCAL NON-CORE EFFECT ONLY",
            "no production, semantic recovery, privacy erasure, or core promotion",
        ).scale(0.84).to_edge(UP, buff=0.35)
        end = source_end_card(
            "Capability Replacement and Rollback",
            "argument • Design rationale",
            "Exact declared local recovery only; unresolved effects remain residuals.",
            "Security Kernel and Digital SCIFs",
        ).scale(0.78).shift(UP * -0.65)
        self.play(Create(boundary), run_time=0.9)
        self.play(FadeIn(end), run_time=1.0)
