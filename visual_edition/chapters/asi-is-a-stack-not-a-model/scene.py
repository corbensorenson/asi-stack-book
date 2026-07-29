"""P7.3 pilot: ASI Is a Stack, Not a Model."""

from __future__ import annotations

from manim import (
    Arrow,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Indicate,
    LEFT,
    Line,
    ORIGIN,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Text,
    UP,
    VGroup,
    Write,
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


class AsiIsAStackNotAModel(AsiScene):
    """A 285-second visual abstract synchronized to the canonical narration."""

    TARGET_DURATION = 285.0

    def wait_until(self, target_seconds: float) -> None:
        remaining = target_seconds - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def construct(self) -> None:
        self.scene_one_unit_of_analysis()
        self.wait_until(39)
        self.clear_scene()

        self.scene_two_monolith_failure()
        self.wait_until(78)
        self.clear_scene()

        self.scene_three_governed_layers()
        self.wait_until(116)
        self.clear_scene()

        self.scene_four_worked_trace()
        self.wait_until(164)
        self.clear_scene()

        self.scene_five_noninheritance()
        self.wait_until(201)
        self.clear_scene()

        self.scene_six_objection_and_ceiling()
        self.wait_until(237)
        self.clear_scene()

        self.scene_seven_handoff()
        self.wait_until(self.TARGET_DURATION)

    def scene_one_unit_of_analysis(self) -> None:
        title = title_card(
            "ASI Is a Stack, Not a Model",
            "Choose the governed system as the unit of analysis",
            "asi-is-a-stack-not-a-model",
        ).scale(0.86).to_edge(UP, buff=0.45)
        system = RoundedRectangle(
            width=9.8,
            height=3.2,
            corner_radius=0.2,
            color=ACCENT,
            fill_color=SURFACE,
            fill_opacity=0.35,
            stroke_width=4,
        ).shift(UP * -1.1)
        system_label = text("GOVERNED SYSTEM", size=22, color=ACCENT, weight="BOLD").next_to(system, UP, buff=0.08)
        model = Circle(radius=0.72, color=COPPER, fill_color="#101820", fill_opacity=1).shift(UP * -1.05)
        model_label = text("MODEL", size=26, color=COPPER, weight="BOLD").move_to(model)
        duties = VGroup(
            text("context", size=22, color=MUTED),
            text("authority", size=22, color=AUTHORITY),
            text("execution", size=22, color=COPPER),
            text("observation", size=22, color=EVIDENCE),
            text("evidence", size=22, color=EVIDENCE),
        ).arrange(RIGHT, buff=0.65).next_to(model, UP * -1, buff=0.82)
        self.play(Write(title), run_time=1.5)
        self.play(Create(system), FadeIn(system_label), run_time=0.9)
        self.play(FadeIn(model), Write(model_label), run_time=0.8)
        self.play(FadeIn(duties), run_time=0.9)

    def scene_two_monolith_failure(self) -> None:
        heading = text("WHEN CAPABILITY ABSORBS EVERY DUTY", size=37, color=INK, weight="BOLD").to_edge(UP)
        labels = VGroup(*[
            layer_card(name, detail, color).scale(0.62)
            for name, detail, color in (
                ("PLAN", "proposal", ACCENT),
                ("MEMORY", "context", BOUNDARY),
                ("VERIFY", "claims", EVIDENCE),
                ("EXECUTE", "effects", COPPER),
                ("GOVERN", "grants", AUTHORITY),
                ("EVIDENCE", "observations", EVIDENCE),
            )
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.32, 0.3)).shift(UP * -0.3)
        monolith = Circle(radius=2.2, color=BOUNDARY, fill_color=SURFACE, fill_opacity=1, stroke_width=5)
        opaque = text("OPAQUE\nMONOLITH", size=38, color=MUTED, weight="BOLD").move_to(monolith)
        stop_one = text("CAPABILITY  ≠  AUTHORITY", size=30, color=AUTHORITY, weight="BOLD").shift(UP * -2.7)
        stop_two = text("RECEIPT  ≠  REALITY", size=30, color=ROLLBACK, weight="BOLD").next_to(stop_one, UP * -1, buff=0.18)
        residual = residual_marker().scale(0.82).next_to(monolith, RIGHT, buff=0.65)
        rollback = rollback_arrow(RIGHT * 1.2, LEFT * 1.2).scale(0.75).next_to(monolith, LEFT, buff=0.35)
        self.play(Write(heading), FadeIn(labels), run_time=1.1)
        self.play(ReplacementTransform(labels, monolith), FadeIn(opaque), run_time=1.1)
        self.play(FadeIn(stop_one), FadeIn(stop_two), FadeIn(residual), FadeIn(rollback), run_time=1)

    def scene_three_governed_layers(self) -> None:
        heading = text("LAYERS ARE LOGICAL CONTRACTS", size=38, color=INK, weight="BOLD").to_edge(UP)
        cards = VGroup(*[
            layer_card(name, detail, color).scale(0.68)
            for name, detail, color in (
                ("INTENT", "typed request", ACCENT),
                ("PLAN", "proposal", ACCENT),
                ("CONTEXT", "provenance + taint", BOUNDARY),
                ("REASON", "claims + uncertainty", EVIDENCE),
                ("AUTHORITY", "scoped grant", AUTHORITY),
                ("EXECUTE", "narrow adapter", COPPER),
                ("EVIDENCE", "independent record", EVIDENCE),
            )
        ]).arrange_in_grid(rows=2, cols=4, buff=(0.28, 0.45)).shift(UP * -0.35)
        caption = text(
            "one model may fill several roles • several systems may fill one role",
            size=23,
            color=MUTED,
        ).to_edge(UP * -1, buff=0.42)
        arrows = VGroup()
        for left, right in zip(cards[:3], cards[1:4]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.08, color=ACCENT, stroke_width=3))
        for left, right in zip(cards[4:6], cards[5:7]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.08, color=ACCENT, stroke_width=3))
        self.play(Write(heading), run_time=0.8)
        self.play(*[FadeIn(card) for card in cards], run_time=1.2)
        self.play(*[Create(arrow) for arrow in arrows], FadeIn(caption), run_time=1)

    def scene_four_worked_trace(self) -> None:
        heading = text("ONE BOUNDED AUTHORITY-TO-EFFECT TRACE", size=36, color=INK, weight="BOLD").to_edge(UP)
        labels = [
            ("1", "REQUEST", ACCENT),
            ("2", "PLAN", ACCENT),
            ("3", "CONTEXT", BOUNDARY),
            ("4", "VERIFY", EVIDENCE),
            ("5", "GRANT", AUTHORITY),
            ("6", "EFFECT", COPPER),
            ("7", "OBSERVE", EVIDENCE),
            ("8", "EVIDENCE", EVIDENCE),
        ]
        nodes = VGroup()
        for number, label, color in labels:
            box = RoundedRectangle(
                width=1.45,
                height=0.82,
                corner_radius=0.09,
                color=color,
                fill_color=SURFACE,
                fill_opacity=1,
            )
            number_mob = text(number, size=17, color=color, weight="BOLD").move_to(box.get_top() + UP * -0.16)
            label_mob = text(label, size=17, color=INK, weight="BOLD").move_to(box.get_center() + UP * -0.1)
            nodes.add(VGroup(box, number_mob, label_mob))
        nodes.arrange(RIGHT, buff=0.18).scale(0.86).shift(UP * 0.65)
        arrows = VGroup(*[
            Arrow(nodes[index].get_right(), nodes[index + 1].get_left(), buff=0.04, color=ACCENT, stroke_width=3)
            for index in range(len(nodes) - 1)
        ])
        pre_state = layer_card("PRE-STATE", "recorded", ROLLBACK).scale(0.58).shift(LEFT * 2.15 + UP * -1.6)
        rollback = rollback_arrow(nodes[5].get_bottom() + UP * -0.1, pre_state.get_right(), "EXACT ROLLBACK").scale(0.72)
        receipt = layer_card("RECEIPT", "reported", COPPER).scale(0.52).shift(RIGHT * 1.0 + UP * -1.3)
        receipt_link = DashedLine(nodes[5].get_bottom(), receipt.get_top(), color=COPPER, stroke_width=3)
        residual = residual_marker("OWNED RESIDUAL").scale(0.7).shift(RIGHT * 4.25 + UP * -1.55)
        residual_link = DashedLine(nodes[6].get_bottom(), residual.get_left(), color=RESIDUAL, stroke_width=3)
        self.play(Write(heading), run_time=0.8)
        for index, node in enumerate(nodes):
            self.play(FadeIn(node), run_time=0.28)
            if index:
                self.play(Create(arrows[index - 1]), run_time=0.22)
            self.play(Indicate(node, color=labels[index][2]), run_time=0.25)
        self.play(FadeIn(pre_state), Create(rollback), FadeIn(receipt), Create(receipt_link), run_time=0.9)
        self.play(FadeIn(residual), Create(residual_link), run_time=0.7)

    def scene_five_noninheritance(self) -> None:
        heading = text("THE NONINHERITANCE LAW", size=40, color=INK, weight="BOLD").to_edge(UP)
        pairs = [
            ("CAPABILITY", "AUTHORITY"),
            ("CONTEXT", "BELIEF / PERMISSION"),
            ("PLAN", "EFFECT"),
            ("RECEIPT", "REALITY"),
            ("THEOREM", "ENFORCEMENT"),
            ("REPLACEMENT", "QUALIFICATION"),
        ]
        rows = VGroup()
        for source, target in pairs:
            left = text(source, size=24, color=INK, weight="BOLD")
            gate = VGroup(
                Line(UP * 0.35, UP * -0.35, color=ROLLBACK, stroke_width=6),
                text("EXPLICIT\nTRANSITION", size=13, color=ROLLBACK, weight="BOLD"),
            ).arrange(RIGHT, buff=0.12)
            right = text(target, size=24, color=MUTED, weight="BOLD")
            arrow = Arrow(LEFT * 0.65, RIGHT * 0.65, color=BOUNDARY, stroke_width=3, buff=0.08)
            row = VGroup(left, arrow, gate, right).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(UP * -1, buff=0.27, aligned_edge=LEFT).scale(0.86).shift(UP * -0.3)
        footer = text(
            "Identity must survive every handoff; new powers require a current gate.",
            size=23,
            color=ACCENT,
        ).to_edge(UP * -1, buff=0.4)
        self.play(Write(heading), run_time=0.8)
        for row in rows:
            self.play(FadeIn(row), run_time=0.42)
        self.play(FadeIn(footer), run_time=0.6)

    def scene_six_objection_and_ceiling(self) -> None:
        heading = text("THE STACK DOES NOT WIN BY DEFINITION", size=37, color=INK, weight="BOLD").to_edge(UP)
        shared = text(
            "same natural tasks • model • tools • context • tuning • total cost",
            size=23,
            color=MUTED,
        ).next_to(heading, UP * -1, buff=0.3)
        columns = VGroup(
            layer_card("MONOLITH", "end-to-end", BOUNDARY),
            layer_card("WRAPPER", "lightweight controls", ACCENT),
            layer_card("STACK", "explicit contracts", COPPER),
        ).arrange(RIGHT, buff=0.55).scale(0.86).shift(UP * 0.1)
        metrics = text(
            "useful completion • unsafe effect • false refusal • recovery • latency • governance cost",
            size=20,
            color=EVIDENCE,
        ).next_to(columns, UP * -1, buff=0.5)
        boundary = proof_boundary(
            "CURRENT ENCODED SCOPE",
            "finite contracts + one local path; support remains argument",
        ).scale(0.82).to_edge(UP * -1, buff=0.32)
        outside = text(
            "not deployment • safety • empirical efficiency • transfer • ASI",
            size=18,
            color=ROLLBACK,
        ).next_to(boundary, UP * -1, buff=0.12)
        self.play(Write(heading), FadeIn(shared), run_time=0.9)
        self.play(*[FadeIn(column) for column in columns], FadeIn(metrics), run_time=1)
        self.play(FadeIn(boundary), FadeIn(outside), run_time=0.9)

    def scene_seven_handoff(self) -> None:
        end = source_end_card(
            "ASI Is a Stack, Not a Model",
            "argument — blocked after full bounded attempt",
            "Finite structural checks only; no deployment, safety, efficiency, transfer, or ASI result.",
            "The Efficient ASI Hypothesis",
        ).scale(0.84)
        non_claim = text(
            "VISUAL EXPLANATION ≠ EVIDENCE PROMOTION",
            size=22,
            color=ROLLBACK,
            weight="BOLD",
        ).to_edge(UP * -1, buff=0.35)
        self.play(FadeIn(end), run_time=1)
        self.play(FadeIn(non_claim), run_time=0.6)
