"""Historical generation-one seven-scene grammar.

Retained so existing receipts remain reproducible. Do not subclass this card
template for generation-two visual abstracts.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

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
    evidence_badge,
    proof_boundary,
    residual_marker,
    text,
)


ROOT = Path(__file__).resolve().parents[2]
COLORS = [ACCENT, COPPER, EVIDENCE, AUTHORITY, RESIDUAL, BOUNDARY]


def wrapped(value: str, width: int) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=True))


def card(
    label: str,
    detail: str,
    color: str,
    *,
    width: float = 3.4,
    height: float = 1.9,
) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        color=color,
        fill_color=SURFACE,
        fill_opacity=1,
        stroke_width=3,
    )
    heading = text(wrapped(label.upper(), 19), size=21, color=color, weight="BOLD")
    body = text(wrapped(detail, 31), size=17, color=MUTED, font="Arial")
    content = VGroup(heading, body).arrange(UP * -1, buff=0.1).move_to(box)
    if content.width > box.width - 0.28:
        content.scale_to_fit_width(box.width - 0.28)
    if content.height > box.height - 0.22:
        content.scale_to_fit_height(box.height - 0.22)
    content.move_to(box)
    return VGroup(box, content)


class AsiChapterScene(AsiScene):
    """Deprecated seven-scene renderer for generation-one custody."""

    SPEC_RELATIVE = ""
    TARGET_DURATION = 285.0

    def spec(self) -> dict:
        return json.loads((ROOT / self.SPEC_RELATIVE).read_text(encoding="utf-8"))

    def wait_until(self, target_seconds: float) -> None:
        remaining = target_seconds - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def construct(self) -> None:
        self.data = self.spec()
        timing = self.data.get("timing", {})
        scenes = (
            self.problem_scene,
            self.mechanism_scene,
            self.trace_scene,
            self.failure_scene,
            self.evidence_scene,
            self.nonclaim_scene,
            self.handoff_scene,
        )
        endpoints = timing.get(
            "scene_endpoints_seconds",
            (39, 79, 122, 166, 207, 244, self.TARGET_DURATION),
        )
        if len(endpoints) != len(scenes):
            raise ValueError("scene_spec timing must contain exactly seven endpoints")
        for index, (scene, endpoint) in enumerate(zip(scenes, endpoints)):
            scene()
            self.wait_until(endpoint)
            if index != len(scenes) - 1:
                self.clear_scene()

    def heading(self, value: str, color: str = INK) -> Text:
        return text(wrapped(value.upper(), 48), size=35, color=color, weight="BOLD").to_edge(UP, buff=0.42)

    def problem_scene(self) -> None:
        title_text = text(
            wrapped(self.data["title"], 43),
            size=40,
            color=INK,
            weight="BOLD",
        )
        rule = Line(LEFT * 5.5, RIGHT * 5.5, color=ACCENT, stroke_width=4)
        subtitle = text(
            wrapped(self.data["subtitle"], 70),
            size=20,
            color=MUTED,
            font="Arial",
        )
        title = VGroup(title_text, rule, subtitle).arrange(UP * -1, buff=0.16).to_edge(UP, buff=0.28)
        problem = card(
            "Problem",
            self.data["display"]["problem"],
            ROLLBACK,
            width=5.25,
            height=2.3,
        )
        insufficient = card(
            "Insufficient shortcut",
            self.data["display"]["insufficient"],
            BOUNDARY,
            width=5.25,
            height=2.3,
        )
        pair = VGroup(problem, insufficient).arrange(RIGHT, buff=0.45).shift(UP * -0.95)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(pair), run_time=1)

    def mechanism_scene(self) -> None:
        heading = self.heading("The chapter's operating mechanism")
        items = self.data["display"]["mechanism"]
        archetype = self.data["archetype"]
        nodes = VGroup(
            *[
                card(item["label"], item["detail"], COLORS[index % len(COLORS)], width=4.35)
                for index, item in enumerate(items)
            ]
        )
        nodes.arrange_in_grid(rows=2, cols=2, buff=(0.48, 0.42))
        if archetype == "before_after":
            nodes[2:].shift(RIGHT * 0.42)
        nodes.shift(UP * -0.35)
        self.play(Write(heading), run_time=0.7)
        self.play(*[FadeIn(node) for node in nodes], run_time=1.1)
        if archetype in {"state_machine", "route", "timeline", "graph"}:
            arrows = VGroup(
                Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=0.08, color=ACCENT, stroke_width=3),
                Arrow(nodes[0].get_bottom(), nodes[2].get_top(), buff=0.08, color=ACCENT, stroke_width=3),
                Arrow(nodes[2].get_right(), nodes[3].get_left(), buff=0.08, color=ACCENT, stroke_width=3),
            )
            self.play(*[Create(arrow) for arrow in arrows], run_time=0.8)

    def trace_scene(self) -> None:
        heading = self.heading("A concrete state transition")
        labels = self.data["display"]["trace"]
        nodes = VGroup()
        for index, item in enumerate(labels, start=1):
            shape = RoundedRectangle(
                width=2.35,
                height=1.15,
                corner_radius=0.12,
                color=COLORS[(index - 1) % len(COLORS)],
                fill_color=SURFACE,
                fill_opacity=1,
                stroke_width=3,
            )
            number = text(str(index), size=16, color=COLORS[(index - 1) % len(COLORS)], weight="BOLD")
            label = text(
                wrapped(item, 16),
                size=18,
                color=INK,
                weight="BOLD",
                font="Arial",
            )
            content = VGroup(number, label).arrange(UP * -1, buff=0.05).move_to(shape)
            nodes.add(VGroup(shape, content))
        nodes.arrange(RIGHT, buff=0.46).shift(UP * 0.2)
        arrows = VGroup(
            *[
                Arrow(
                    nodes[index].get_right(),
                    nodes[index + 1].get_left(),
                    buff=0.04,
                    color=ACCENT,
                    stroke_width=3,
                )
                for index in range(len(nodes) - 1)
            ]
        )
        receipt = evidence_badge("OBSERVED").scale(0.9).shift(RIGHT * 2.1 + UP * -1.8)
        residual = residual_marker("OPEN RESIDUAL").scale(0.82).shift(LEFT * 2.1 + UP * -1.8)
        link = DashedLine(residual.get_right(), receipt.get_left(), color=BOUNDARY, stroke_width=3)
        self.play(Write(heading), run_time=0.7)
        for index, node in enumerate(nodes):
            self.play(FadeIn(node), run_time=0.25)
            if index:
                self.play(Create(arrows[index - 1]), run_time=0.2)
            self.play(Indicate(node, color=COLORS[index % len(COLORS)]), run_time=0.2)
        self.play(FadeIn(residual), Create(link), FadeIn(receipt), run_time=0.8)

    def failure_scene(self) -> None:
        heading = self.heading("Where the design can still fail", ROLLBACK)
        failures = VGroup(
            *[
                card(f"Failure {index}", item, ROLLBACK if index == 1 else BOUNDARY, width=3.4)
                for index, item in enumerate(self.data["display"]["failures"], start=1)
            ]
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.38)).scale(0.9).shift(UP * -0.35)
        stop = Line(LEFT * 5.1, RIGHT * 5.1, color=ROLLBACK, stroke_width=7).to_edge(UP * -1, buff=0.5)
        stop_label = text("FAIL CLOSED • RECORD THE RESIDUAL", size=22, color=ROLLBACK, weight="BOLD").next_to(stop, UP, buff=0.1)
        self.play(Write(heading), run_time=0.7)
        self.play(*[FadeIn(item) for item in failures], run_time=1.1)
        self.play(Create(stop), FadeIn(stop_label), run_time=0.7)

    def evidence_scene(self) -> None:
        heading = self.heading("What is actually established", EVIDENCE)
        boundary = proof_boundary(
            self.data["claim_label"],
            f"support state: {self.data['evidence_level']}",
        ).scale(0.95).shift(UP * 0.85)
        targets = VGroup(
            *[
                card(f"Target {index}", item, EVIDENCE, width=3.6)
                for index, item in enumerate(self.data["display"]["proof_targets"], start=1)
            ]
        ).arrange(RIGHT, buff=0.32).scale(0.8).shift(UP * -1.05)
        ceiling = text(
            wrapped(self.data["display"]["evidence_ceiling"], 76),
            size=18,
            color=MUTED,
            font="Arial",
        ).to_edge(UP * -1, buff=0.35)
        self.play(Write(heading), FadeIn(boundary), run_time=0.9)
        self.play(*[FadeIn(item) for item in targets], run_time=1)
        self.play(FadeIn(ceiling), run_time=0.6)

    def nonclaim_scene(self) -> None:
        heading = self.heading("Do not infer")
        rows = VGroup()
        for item in self.data["display"]["nonclaims"]:
            bar = Rectangle(
                width=0.18,
                height=0.62,
                color=ROLLBACK,
                fill_color=ROLLBACK,
                fill_opacity=1,
            )
            label = text(wrapped(item, 66), size=22, color=MUTED, font="Arial")
            rows.add(VGroup(bar, label).arrange(RIGHT, buff=0.25))
        rows.arrange(UP * -1, buff=0.35, aligned_edge=LEFT).shift(UP * -0.2)
        self.play(Write(heading), run_time=0.7)
        self.play(*[FadeIn(row) for row in rows], run_time=1.1)

    def handoff_scene(self) -> None:
        heading = text("READ THE LIVE CHAPTER", size=24, color=ACCENT, weight="BOLD")
        title_mob = text(wrapped(self.data["title"], 44), size=36, color=INK, weight="BOLD")
        support = text(
            f"Current support: {self.data['evidence_level']} • {self.data['claim_label']}",
            size=22,
            color=EVIDENCE,
        )
        boundary = text(
            wrapped(self.data["display"]["maximum_inference"], 72),
            size=18,
            color=MUTED,
            font="Arial",
        )
        handoff = text(
            wrapped(f"Next: {self.data['next_title']}", 58),
            size=21,
            color=COPPER,
        )
        url = text(
            "corbensorenson.github.io/asi-stack-book",
            size=19,
            color=ACCENT,
        )
        end = VGroup(heading, title_mob, support, boundary, handoff, url).arrange(UP * -1, buff=0.24)
        self.play(FadeIn(end), run_time=1.1)
