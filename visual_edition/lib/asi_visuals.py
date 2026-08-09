"""Candidate reusable visual grammar for P7.3 Manim scenes."""

from __future__ import annotations

from manim import (
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    ORIGIN,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Scene,
    Text,
    Triangle,
    UP,
    VGroup,
    Write,
)


BACKGROUND = "#101820"
SURFACE = "#182630"
INK = "#F5F8FA"
MUTED = "#B8C4CC"
ACCENT = "#58B7D3"
COPPER = "#D79A6B"
AUTHORITY = "#F2C14E"
EVIDENCE = "#62C370"
RESIDUAL = "#D66BA0"
ROLLBACK = "#F45B69"
BOUNDARY = "#8F9AA3"
PRIMARY_FONT = "Avenir Next"
MONO_FONT = "Menlo"


def text(
    value: str,
    *,
    size: int = 36,
    color: str = INK,
    font: str = PRIMARY_FONT,
    weight: str = "NORMAL",
) -> Text:
    """Create stable, high-contrast text using a project-owned font contract."""

    return Text(value, font=font, font_size=size, color=color, weight=weight)


def title_card(title: str, subtitle: str, chapter_id: str) -> VGroup:
    rule = Line(LEFT * 5.8, RIGHT * 5.8, color=ACCENT, stroke_width=4)
    title_mob = text(title, size=54, weight="BOLD")
    subtitle_mob = text(subtitle, size=30, color=MUTED)
    slug = text(chapter_id, size=22, color=COPPER, font=MONO_FONT)
    group = VGroup(title_mob, rule, subtitle_mob, slug).arrange(UP * -1, buff=0.28)
    return group


def layer_card(label: str, responsibility: str, color: str = ACCENT) -> VGroup:
    box = RoundedRectangle(
        width=3.2,
        height=1.05,
        corner_radius=0.12,
        fill_color=SURFACE,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=3,
    )
    heading = text(label, size=28, color=color, weight="BOLD")
    detail = text(responsibility, size=20, color=MUTED)
    content = VGroup(heading, detail).arrange(UP * -1, buff=0.12)
    content.move_to(box.get_center())
    return VGroup(box, content)


def authority_gate(label: str = "AUTHORITY") -> VGroup:
    shield = Triangle(color=AUTHORITY, fill_color=SURFACE, fill_opacity=1).scale(0.45).rotate(3.14159)
    key = Line(LEFT * 0.18, RIGHT * 0.18, color=AUTHORITY, stroke_width=5)
    key.add(Line(RIGHT * 0.18, RIGHT * 0.18 + UP * 0.12, color=AUTHORITY, stroke_width=5))
    badge = text(label, size=18, color=AUTHORITY, weight="BOLD")
    badge.next_to(shield, UP, buff=0.08)
    return VGroup(shield, key, badge)


def evidence_badge(label: str = "EVIDENCE") -> VGroup:
    ledger = RoundedRectangle(
        width=1.8,
        height=0.72,
        corner_radius=0.08,
        color=EVIDENCE,
        fill_color=SURFACE,
        fill_opacity=1,
    )
    check = VGroup(
        Line(LEFT * 0.18, ORIGIN + UP * -0.15, color=EVIDENCE, stroke_width=5),
        Line(ORIGIN + UP * -0.15, RIGHT * 0.28 + UP * 0.18, color=EVIDENCE, stroke_width=5),
    ).move_to(ledger.get_center() + LEFT * 0.56)
    label_mob = text(label, size=16, color=EVIDENCE, weight="BOLD").move_to(ledger.get_center() + RIGHT * 0.3)
    return VGroup(ledger, check, label_mob)


def residual_marker(label: str = "RESIDUAL") -> VGroup:
    loop = DashedVMobject(Circle(radius=0.34, color=RESIDUAL), num_dashes=10)
    gap = Rectangle(width=0.28, height=0.22, fill_color=BACKGROUND, fill_opacity=1, stroke_opacity=0)
    gap.move_to(loop.get_right())
    label_mob = text(label, size=17, color=RESIDUAL, weight="BOLD").next_to(loop, UP, buff=0.08)
    return VGroup(loop, gap, label_mob)


def rollback_arrow(start=RIGHT * 2, end=LEFT * 2, label: str = "ROLLBACK") -> VGroup:
    arrow = Arrow(start, end, color=ROLLBACK, stroke_width=5, buff=0.1)
    label_mob = text(label, size=19, color=ROLLBACK, weight="BOLD").next_to(arrow, UP, buff=0.1)
    return VGroup(arrow, label_mob)


def proof_boundary(label: str, scope: str) -> VGroup:
    outer = RoundedRectangle(
        width=5.2,
        height=1.45,
        corner_radius=0.1,
        color=BOUNDARY,
        stroke_width=3,
    )
    inner = RoundedRectangle(
        width=4.95,
        height=1.2,
        corner_radius=0.08,
        color=BOUNDARY,
        stroke_width=1.5,
    )
    label_mob = text(label, size=23, color=INK, weight="BOLD")
    scope_mob = text(scope, size=18, color=MUTED)
    content = VGroup(label_mob, scope_mob).arrange(UP * -1, buff=0.1).move_to(outer)
    return VGroup(outer, inner, content)


def source_end_card(
    chapter_title: str,
    support_state: str,
    maximum_inference: str,
    next_chapter: str,
) -> VGroup:
    heading = text("READ THE LIVE CHAPTER", size=25, color=ACCENT, weight="BOLD")
    title_mob = text(chapter_title, size=40, color=INK, weight="BOLD")
    support = text(f"Current support: {support_state}", size=25, color=EVIDENCE)
    boundary = text(maximum_inference, size=21, color=MUTED)
    handoff = text(f"Next: {next_chapter}", size=23, color=COPPER)
    url = text("corbensorenson.github.io/asi-stack-book", size=21, color=ACCENT, font=MONO_FONT)
    return VGroup(heading, title_mob, support, boundary, handoff, url).arrange(UP * -1, buff=0.22)


class AsiScene(Scene):
    """Base scene with stable background and low-motion transition helpers."""

    def setup(self) -> None:
        self.camera.background_color = BACKGROUND

    def reveal(self, *mobjects, run_time: float = 0.8) -> None:
        self.play(AnimationGroup(*(FadeIn(mob) for mob in mobjects), lag_ratio=0.08), run_time=run_time)

    def clear_scene(self, run_time: float = 0.6) -> None:
        if self.mobjects:
            self.play(*(FadeOut(mob) for mob in list(self.mobjects)), run_time=run_time)


class PrimitiveGallery(AsiScene):
    """Compatibility scene that exercises the reusable semantic primitives."""

    def construct(self) -> None:
        title = title_card("ASI Stack Visual Grammar", "Candidate primitive compatibility render", "p7.3-foundation")
        self.play(Write(title), run_time=1.4)
        self.wait(0.5)
        self.clear_scene()

        cards = VGroup(
            layer_card("PLAN", "typed proposal"),
            layer_card("VERIFY", "claim boundary", EVIDENCE),
            layer_card("EXECUTE", "narrow adapter", COPPER),
        ).arrange(RIGHT, buff=0.35).scale(0.78)
        self.reveal(cards)
        self.wait(0.5)
        self.clear_scene()

        symbols = VGroup(
            authority_gate(),
            evidence_badge(),
            residual_marker(),
        ).arrange(RIGHT, buff=1.2)
        self.reveal(symbols)
        self.wait(0.5)
        self.clear_scene()

        rollback = rollback_arrow()
        boundary = proof_boundary("ENCODED SCOPE", "proof is not runtime enforcement").next_to(rollback, UP, buff=0.7)
        self.play(Create(rollback), FadeIn(boundary), run_time=1)
        self.wait(0.5)
        self.clear_scene()

        end = source_end_card(
            "Primitive compatibility sheet",
            "none",
            "Visual grammar only; no chapter claim.",
            "Five representative pilots",
        )
        self.reveal(end)
        self.wait(0.8)
