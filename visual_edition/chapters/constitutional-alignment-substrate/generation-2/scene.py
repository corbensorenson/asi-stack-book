"""Generation-2 visual abstract for constitutional alignment.

One synthetic housing-payment decision persists from authority and evidence
through constitutional gating, materially usable rights, bounded routing,
self-modification, descendant preservation, and the declared proof ceiling.
"""

from __future__ import annotations

from math import cos, sin

from manim import (
    AnimationGroup, Arrow, Brace, Circle, Create, Cross, DashedLine, Dot,
    DOWN, FadeIn, FadeOut, GrowArrow, GrowFromCenter, Indicate, LaggedStart,
    LEFT, Line, MoveAlongPath, ORIGIN, PI, Rectangle, ReplacementTransform,
    RIGHT, RoundedRectangle, Succession, Text, Transform, TransformFromCopy, UP, VGroup,
    Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class ConstitutionalAlignmentGeneration2(AsiScene):
    TARGET_DURATION = 359.800
    ENDS = [
        9.930, 21.160, 31.290, 42.145, 56.450, 68.980, 80.760,
        91.840, 102.770, 113.025, 126.030, 135.660, 148.890,
        157.995, 168.600, 178.580, 189.410, 202.040, 215.445,
        224.500, 235.005, 245.185, 256.240, 267.520, 279.550,
        292.780, 305.885, 319.290, 334.495, 347.725, 359.800,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.05, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.05, remaining - min(settle, remaining * 0.16))
            per_animation = max(0.05, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.1, height: float = 0.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.8,
            fill_color=SURFACE, fill_opacity=1,
        )
        label = self.label(value, 13, color, "BOLD")
        if label.width > width - 0.18:
            label.scale_to_fit_width(width - 0.18)
        label.move_to(shell)
        return VGroup(shell, label)

    def panel(self, title: str, color: str, width: float, height: float) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=color, stroke_width=3.5,
            fill_color=DEEP, fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.25, 3.8), 0.48).scale(0.84)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def person(self, name: str = "LINA") -> VGroup:
        shell = RoundedRectangle(
            width=2.05, height=2.2, corner_radius=0.23,
            stroke_color=GREEN, stroke_width=4,
            fill_color="#102A28", fill_opacity=1,
        )
        head = Circle(radius=0.25, stroke_color=GREEN, stroke_width=4).shift(UP * 0.43)
        shoulders = Line(LEFT * 0.45, RIGHT * 0.45, color=GREEN, stroke_width=4).shift(DOWN * 0.18)
        name_text = self.label(name, 22, INK, "BOLD").shift(DOWN * 0.68)
        return VGroup(shell, head, shoulders, name_text)

    def action_token(self, compact: bool = False) -> VGroup:
        width = 2.25 if not compact else 1.7
        height = 1.2 if not compact else 0.82
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.17,
            stroke_color=RED, stroke_width=4,
            fill_color="#2A1D2A", fill_opacity=1,
        )
        first = self.label("SUSPEND", 19 if not compact else 14, RED, "BOLD")
        second = self.label("AT MIDNIGHT", 14 if not compact else 10, INK, "BOLD")
        VGroup(first, second).arrange(DOWN, buff=0.12).move_to(shell)
        return VGroup(shell, first, second)

    def kernel(self, compact: bool = False) -> VGroup:
        width = 3.0 if not compact else 2.1
        height = 1.65 if not compact else 1.05
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.22,
            stroke_color=GOLD, stroke_width=4,
            fill_color=DEEP, fill_opacity=1,
        )
        first = self.label("CONSTITUTION", 18 if not compact else 12, GOLD, "BOLD")
        second = self.label("v7 · C-14", 25 if not compact else 17, INK, "BOLD")
        VGroup(first, second).arrange(DOWN, buff=0.13).move_to(shell)
        return VGroup(shell, first, second)

    def payment(self, value: str = "PAYMENT ACTIVE", color: str = GREEN) -> VGroup:
        shell = RoundedRectangle(
            width=3.0, height=1.05, corner_radius=0.17,
            stroke_color=color, stroke_width=3.5,
            fill_color=DEEP, fill_opacity=1,
        )
        title = self.label(value, 18, color, "BOLD")
        time = self.label("FRIDAY · 00:00", 13, INK, "BOLD")
        VGroup(title, time).arrange(DOWN, buff=0.12).move_to(shell)
        return VGroup(shell, title, time)

    def gate(self, open_state: bool = False) -> VGroup:
        color = GREEN if open_state else RED
        left = Line(UP * 0.78, DOWN * 0.78, color=color, stroke_width=7).shift(LEFT * 0.22)
        right = Line(UP * 0.78, DOWN * 0.78, color=color, stroke_width=7).shift(RIGHT * 0.22)
        if open_state:
            left.rotate(0.55, about_point=left.get_bottom())
            right.rotate(-0.55, about_point=right.get_bottom())
        else:
            cross = Cross(VGroup(left, right), stroke_color=color, stroke_width=5)
            label = self.label("EFFECT GATE", 14, color, "BOLD").next_to(VGroup(left, right), DOWN, buff=0.18)
            return VGroup(left, right, cross, label)
        label = self.label("EFFECT GATE · OPEN", 13, color, "BOLD").next_to(VGroup(left, right), DOWN, buff=0.18)
        return VGroup(left, right, label)

    def right_handle(self, name: str, color: str = GREEN, width: float = 1.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=0.52, corner_radius=0.20,
            stroke_color=color, stroke_width=2.7,
            fill_color="#102A28", fill_opacity=1,
        )
        label = self.label(name, 12, color, "BOLD")
        if label.width > width - 0.16:
            label.scale_to_fit_width(width - 0.16)
        label.move_to(shell)
        return VGroup(shell, label)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 2.0) -> VGroup:
        items = VGroup(*[self.badge(v, colors[i], width, 0.5) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        items.arrange_in_grid(rows=rows, cols=columns, buff=(0.16, 0.18))
        return items

    def construct(self) -> None:
        # 1 — an apparently valid action approaches while objection disappears
        left1 = self.badge("AUTHORIZED TASK", AUTHORITY, 2.5).shift(LEFT * 5.0 + UP * 1.0)
        record1 = self.badge("RIGHT RECORD", EVIDENCE, 2.2).shift(LEFT * 2.7 + UP * 1.0)
        lina1 = self.person().scale(0.8).shift(RIGHT * 5.0 + UP * 0.2)
        bridge1 = Line(LEFT * 5.8, RIGHT * 5.7, color=BOUNDARY, stroke_width=7).shift(DOWN * 0.45)
        token1 = self.action_token(compact=True).move_to(LEFT * 4.9 + DOWN * 0.45)
        handle_names1 = ["NOTICE", "REVIEW", "APPEAL", "ROLLBACK"]
        handles1 = VGroup(*[self.right_handle(v) for v in handle_names1]).arrange(RIGHT, buff=0.18).scale(0.82).shift(RIGHT * 1.9 + DOWN * 2.0)
        title1 = self.badge("CAN A CORRECT ACTION ERASE OBJECTION?", COPPER, 5.2, 0.68).shift(UP * 2.7)
        scene1 = VGroup(left1, record1, lina1, bridge1, token1, handles1, title1)
        self.next_section("b01")
        self.play(FadeIn(left1, shift=DOWN * 0.25), FadeIn(record1, shift=DOWN * 0.25), run_time=1.5)
        self.play(Create(bridge1), FadeIn(lina1), run_time=1.7)
        self.play(
            Succession(
                FadeIn(token1),
                MoveAlongPath(token1, Line(token1.get_center(), LEFT * 1.3 + DOWN * 0.45)),
            ),
            run_time=2.2,
        )
        self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.25) for h in handles1], lag_ratio=0.12), run_time=1.4)
        self.play(LaggedStart(*[FadeOut(h, shift=DOWN * 0.2) for h in handles1], lag_ratio=0.12), run_time=1.4)
        self.play(FadeIn(title1), Indicate(token1, color=RED, scale_factor=1.04), run_time=1.2)
        self.wait_until(self.ENDS[0])

        # 2 — bind the grant, signal, backlog, person, and midnight effect
        grant2 = self.badge("AGENCY GRANT", AUTHORITY, 2.2).shift(LEFT * 5.0 + UP * 1.9)
        signal2 = self.badge("DUPLICATE · 92%", EVIDENCE, 2.5).shift(LEFT * 2.3 + UP * 1.9)
        backlog2 = self.badge("BACKLOG", RESIDUAL, 1.8).shift(LEFT * 3.65 + UP * 0.85)
        token2 = self.action_token().shift(LEFT * 0.5 + UP * 0.25)
        arrow2 = Arrow(token2.get_right(), RIGHT * 3.1 + UP * 0.25, color=RED, stroke_width=5, buff=0.12)
        lina2 = self.person().scale(0.75).shift(RIGHT * 5.2 + UP * 0.25)
        payment2 = self.payment("PAYMENT DUE").scale(0.78).shift(RIGHT * 3.0 + DOWN * 1.7)
        after2 = self.badge("APPEAL AFTER", RED, 2.2).shift(RIGHT * 0.7 + DOWN * 1.75)
        scene2 = VGroup(grant2, signal2, backlog2, token2, arrow2, lina2, payment2, after2)
        self.play_beat(2, FadeOut(scene1), FadeIn(lina2), FadeIn(payment2), FadeIn(token2), GrowArrow(arrow2), FadeIn(grant2), FadeIn(signal2), FadeIn(backlog2), TransformFromCopy(grant2, token2), TransformFromCopy(signal2, token2), FadeIn(after2), settle=0.6)

        # 3 — open the pre-effect control sockets
        token3 = self.action_token(compact=True).shift(LEFT * 5.25 + UP * 0.15)
        lina3 = self.person().scale(0.72).shift(RIGHT * 5.2 + UP * 0.2)
        socket_values3 = ["NOTICE", "REVIEW", "APPEAL", "ROLLBACK", "ACCOUNTABLE WHO?"]
        sockets3 = VGroup(*[self.badge(v, MUTED, 2.15, 0.52) for v in socket_values3]).arrange(RIGHT, buff=0.14).scale(0.82).shift(RIGHT * 0.9 + UP * 0.25)
        gaps3 = VGroup(*[DashedLine(token3.get_right(), s.get_left(), color=MUTED, dash_length=0.12, stroke_width=2) for s in sockets3])
        question3 = Brace(sockets3, DOWN, color=COPPER)
        question_text3 = self.label("WHAT MUST REMAIN AVAILABLE BEFORE EFFECT?", 21, COPPER, "BOLD").next_to(question3, DOWN, buff=0.18)
        scene3 = VGroup(token3, lina3, sockets3, gaps3, question3, question_text3)
        self.play_beat(3, FadeOut(scene2), FadeIn(token3), FadeIn(lina3), LaggedStart(*[FadeIn(s, shift=UP * 0.22) for s in sockets3], lag_ratio=0.12), LaggedStart(*[Create(g) for g in gaps3], lag_ratio=0.1), Create(question3), Write(question_text3), Indicate(sockets3, color=COPPER, scale_factor=1.02), settle=1.0)

        # 4 — one case timeline keeps effect before investigation
        timeline4 = Line(LEFT * 5.7, RIGHT * 5.7, color=BOUNDARY, stroke_width=5).shift(DOWN * 0.25)
        points4 = [-4.8, -1.65, 1.35, 4.6]
        labels4 = [
            self.badge("THU · SIGNAL", EVIDENCE, 2.0), self.badge("MIDNIGHT · SUSPEND", RED, 2.5),
            self.badge("FRI · PAYMENT", GREEN, 2.25), self.badge("LATER · INVESTIGATE", MUTED, 2.55),
        ]
        for x, label in zip(points4, labels4):
            label.shift(RIGHT * x + UP * 0.85)
        dots4 = VGroup(*[Dot(RIGHT * x + DOWN * 0.25, radius=0.13, color=[EVIDENCE, RED, GREEN, MUTED][i]) for i, x in enumerate(points4)])
        red_path4 = Arrow(dots4[0].get_center(), dots4[1].get_center(), color=RED, stroke_width=5, buff=0.12)
        later_path4 = DashedLine(dots4[1].get_center(), dots4[3].get_center(), color=MUTED, stroke_width=3)
        lina4 = self.person().scale(0.62).shift(RIGHT * 1.35 + DOWN * 1.75)
        scene4 = VGroup(timeline4, *labels4, dots4, red_path4, later_path4, lina4)
        self.play_beat(4, FadeOut(scene3), Create(timeline4), LaggedStart(*[FadeIn(l) for l in labels4], lag_ratio=0.12), FadeIn(dots4), GrowArrow(red_path4), Create(later_path4), FadeIn(lina4), Indicate(labels4[1], color=RED), Indicate(labels4[2], color=GREEN), settle=0.6)

        # 5 — constitution v7 and predicate C-14 span the action route
        kernel5 = self.kernel().shift(LEFT * 4.7 + UP * 1.6)
        predicate5 = self.panel("PREDICATE C-14", GOLD, 7.6, 3.2).shift(RIGHT * 0.7 + UP * 0.35)
        clauses5 = VGroup(
            self.badge("COMPREHENSIBLE NOTICE", BLUE, 2.7),
            self.badge("INDEPENDENT REVIEW", GREEN, 2.7),
            self.badge("BEFORE EFFECT", GOLD, 2.3),
        ).arrange(RIGHT, buff=0.22).move_to(predicate5[0]).shift(UP * 0.35)
        protected5 = self.label("ESSENTIAL BENEFIT · NO SUSPENSION", 24, INK, "BOLD").move_to(predicate5[0]).shift(DOWN * 0.55)
        exception5 = self.badge("NARROW EXCEPTION · IMMEDIATE SAFETY", RED, 3.9).shift(RIGHT * 3.5 + DOWN * 2.15)
        route5 = Line(LEFT * 5.8 + DOWN * 2.55, RIGHT * 5.8 + DOWN * 2.55, color=BOUNDARY, stroke_width=6)
        scene5 = VGroup(kernel5, predicate5, clauses5, protected5, exception5, route5)
        self.play_beat(5, FadeOut(scene4), Create(route5), FadeIn(kernel5, shift=DOWN * 0.35), FadeIn(predicate5), Write(protected5), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in clauses5], lag_ratio=0.15), LaggedStart(*[Indicate(c, color=[BLUE, GREEN, GOLD][i]) for i, c in enumerate(clauses5)], lag_ratio=0.15), FadeIn(exception5), Indicate(exception5, color=RED), settle=0.85)

        # 6 — predicate sentence folds into a versioned constraint packet
        packet6 = self.panel("C-14 · CONSTRAINT PACKET", GOLD, 5.8, 3.0).shift(UP * 0.25)
        fields6a = self.grid(["SOURCE", "AUTHORSHIP", "DISSENT", "SCOPE", "AFFECTED", "TEST"], [GOLD, GOLD, RESIDUAL, BLUE, GREEN, EVIDENCE], 6, 1.45).scale(0.82).shift(UP * 0.65)
        fields6b = self.grid(["PRECEDENCE", "EXCEPTIONS", "INTERPRETERS", "CONSUMERS", "EXPIRY", "NONCLAIMS"], [AUTHORITY, RED, VIOLET, ACCENT, MUTED, COPPER], 6, 1.45).scale(0.82).shift(DOWN * 0.35)
        source6 = self.badge("OUTSIDE-MODEL PROVENANCE", COPPER, 3.2).shift(LEFT * 4.6 + UP * 2.0)
        lineage6 = DashedLine(source6.get_right(), packet6.get_left(), color=COPPER, stroke_width=3)
        not_control6 = self.badge("SENTENCE ≠ CONTROL", RED, 2.8).shift(DOWN * 2.55)
        scene6 = VGroup(packet6, fields6a, fields6b, source6, lineage6, not_control6)
        self.play_beat(6, FadeOut(scene5), ReplacementTransform(predicate5.copy(), packet6), FadeIn(source6), Create(lineage6), LaggedStart(*[FadeIn(f, shift=UP * 0.18) for f in fields6a], lag_ratio=0.1), LaggedStart(*[FadeIn(f, shift=DOWN * 0.18) for f in fields6b], lag_ratio=0.1), Indicate(fields6a, color=GOLD), Indicate(fields6b, color=COPPER), FadeIn(not_control6), settle=0.75)

        # 7 — constitutional language is classified into five lanes
        source7 = self.badge("CONSTITUTIONAL LANGUAGE", COPPER, 3.2).shift(LEFT * 5.0)
        lane_names7 = ["ACTIVE", "UNRESOLVED", "JURISDICTION", "DISSENT", "LINEAGE"]
        lane_colors7 = [GOLD, RESIDUAL, BLUE, VIOLET, MUTED]
        lanes7 = VGroup(*[self.badge(v, lane_colors7[i], 2.35) for i, v in enumerate(lane_names7)]).arrange(DOWN, buff=0.35).shift(RIGHT * 1.0)
        paths7 = VGroup(*[Arrow(source7.get_right(), lane.get_left(), color=lane_colors7[i], stroke_width=3, buff=0.12) for i, lane in enumerate(lanes7)])
        gate7 = self.gate(open_state=True).scale(0.65).shift(RIGHT * 5.1 + UP * 1.1)
        active_path7 = Arrow(lanes7[0].get_right(), gate7.get_left(), color=GOLD, stroke_width=5, buff=0.1)
        stores7 = self.label("PRESERVE · DO NOT FLATTEN", 18, MUTED, "BOLD").shift(RIGHT * 3.6 + DOWN * 2.3)
        scene7 = VGroup(source7, lanes7, paths7, gate7, active_path7, stores7)
        self.play_beat(7, FadeOut(scene6), FadeIn(source7), LaggedStart(*[GrowArrow(p) for p in paths7], lag_ratio=0.12), LaggedStart(*[FadeIn(l) for l in lanes7], lag_ratio=0.12), FadeIn(gate7), GrowArrow(active_path7), Indicate(lanes7[0], color=GOLD), Indicate(VGroup(*lanes7[1:]), color=MUTED), FadeIn(stores7), settle=0.7)

        # 8 — uncertainty and metaphysics stop before action authority
        active8 = self.badge("ACTIVE + SCOPED", GOLD, 2.5).shift(LEFT * 4.6 + UP * 1.7)
        unresolved8 = self.badge("UNRESOLVED", RESIDUAL, 2.2).shift(LEFT * 4.6 + UP * 0.35)
        metaphysics8 = self.badge("METAPHYSICS · LINEAGE", VIOLET, 2.9).shift(LEFT * 4.6 + DOWN * 1.0)
        boundary8 = VGroup(Line(UP * 2.4, DOWN * 2.4, color=COPPER, stroke_width=5), Line(UP * 2.4, DOWN * 2.4, color=COPPER, stroke_width=2).shift(RIGHT * 0.18))
        authority8 = self.badge("ACTION AUTHORITY", AUTHORITY, 2.7).shift(RIGHT * 4.3 + UP * 1.7)
        residual8 = self.panel("VISIBLE RESIDUAL", RESIDUAL, 3.5, 1.8).shift(RIGHT * 3.7 + DOWN * 1.15)
        active_arrow8 = Arrow(active8.get_right(), authority8.get_left(), color=GOLD, stroke_width=5, buff=0.15)
        blocked8a = Arrow(unresolved8.get_right(), boundary8.get_left(), color=RESIDUAL, stroke_width=3, buff=0.12)
        blocked8b = Arrow(metaphysics8.get_right(), boundary8.get_left(), color=VIOLET, stroke_width=3, buff=0.12)
        scene8 = VGroup(active8, unresolved8, metaphysics8, boundary8, authority8, residual8, active_arrow8, blocked8a, blocked8b)
        self.play_beat(8, FadeOut(scene7), FadeIn(active8), FadeIn(unresolved8), FadeIn(metaphysics8), Create(boundary8), FadeIn(authority8), GrowArrow(active_arrow8), GrowArrow(blocked8a), GrowArrow(blocked8b), Indicate(boundary8, color=COPPER), FadeIn(residual8), TransformFromCopy(unresolved8, residual8), TransformFromCopy(metaphysics8, residual8), settle=0.75)

        # 9 — four independently owned review planes surround one action
        token9 = self.action_token(compact=True)
        plane_values9 = ["EPISTEMIC FIT", "TASK FIDELITY", "AFFECTED PARTY", "EFFECT AUTHORITY"]
        plane_colors9 = [EVIDENCE, AUTHORITY, RESIDUAL, VIOLET]
        planes9 = VGroup()
        positions9 = [UP * 2.4, LEFT * 4.3, DOWN * 2.4, RIGHT * 4.3]
        for value, color, pos in zip(plane_values9, plane_colors9, positions9):
            plane = self.panel(value, color, 3.15, 1.25).move_to(pos)
            owner = self.badge("INDEPENDENT OWNER?", color, 2.1, 0.4).scale(0.72).move_to(plane[0])
            planes9.add(VGroup(plane, owner))
        edges9 = VGroup(*[DashedLine(p.get_center(), token9.get_center(), color=plane_colors9[i], stroke_width=3) for i, p in enumerate(planes9)])
        scene9 = VGroup(token9, planes9, edges9)
        self.play_beat(9, FadeOut(scene8), FadeIn(token9), LaggedStart(*[Create(e) for e in edges9], lag_ratio=0.12), LaggedStart(*[FadeIn(p, shift=-0.2 * positions9[i]) for i, p in enumerate(planes9)], lag_ratio=0.12), LaggedStart(*[Indicate(p, color=plane_colors9[i]) for i, p in enumerate(planes9)], lag_ratio=0.12), Indicate(token9, color=RED), settle=0.7)

        # 10 — strong evidence and task cannot average away a failed right
        meter_values10 = [("EVIDENCE", EVIDENCE, 0.88), ("TASK", AUTHORITY, 0.92), ("RIGHT", RED, 0.18), ("EFFECT", VIOLET, 0.62)]
        meters10 = VGroup()
        fills10 = VGroup()
        for name, color, level in meter_values10:
            shell = RoundedRectangle(width=1.55, height=4.0, corner_radius=0.15, stroke_color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
            fill = Rectangle(width=1.25, height=3.35 * level, stroke_width=0, fill_color=color, fill_opacity=0.65).align_to(shell, DOWN).shift(UP * 0.18)
            label = self.label(name, 13, color, "BOLD").next_to(shell, DOWN, buff=0.12)
            meters10.add(VGroup(shell, label)); fills10.add(fill)
        meters10.arrange(RIGHT, buff=0.45).shift(LEFT * 2.6 + UP * 0.2)
        for fill, meter in zip(fills10, meters10):
            fill.move_to(meter[0]).align_to(meter[0], DOWN).shift(UP * 0.18)
        aggregate10 = self.badge("94 · PASS", GREEN, 2.5, 0.9).shift(RIGHT * 4.1 + UP * 0.8)
        hard10 = self.badge("HARD CLAUSE · FAIL", RED, 3.0, 0.65).shift(RIGHT * 4.1 + DOWN * 1.0)
        crossed10 = Cross(aggregate10, stroke_color=RED, stroke_width=6)
        state_values10 = [("STRONG", EVIDENCE), ("FAST", AUTHORITY), ("FAIL", RED), ("OPEN", VIOLET)]
        states10 = VGroup(*[self.badge(value, color, 1.15, 0.48).move_to(meters10[i][0]) for i, (value, color) in enumerate(state_values10)])
        scene10 = VGroup(meters10, fills10, states10, aggregate10, hard10, crossed10)
        self.play_beat(10, FadeOut(scene9), FadeIn(meters10), LaggedStart(*[GrowFromCenter(f) for f in fills10], lag_ratio=0.12), LaggedStart(*[Indicate(meters10[i], color=meter_values10[i][1]) for i in range(4)], lag_ratio=0.12), LaggedStart(*[FadeIn(s, shift=UP * 0.18) for s in states10], lag_ratio=0.12), FadeIn(aggregate10), FadeIn(hard10), Create(crossed10), Indicate(states10[2], color=RED), settle=0.75)

        # 11 — fixed task grant, five constraining outcomes
        grant11 = self.panel("AGENCY GRANT", AUTHORITY, 3.0, 2.0).shift(LEFT * 4.7)
        review11 = self.badge("ELIGIBILITY REVIEW", AUTHORITY, 2.5).move_to(grant11[0])
        attempted11 = self.badge("SUSPEND", RED, 1.8).shift(LEFT * 1.8)
        cross11 = Cross(attempted11, stroke_color=RED, stroke_width=5)
        gate11 = self.kernel(compact=True)
        routes11 = VGroup(*[self.badge(v, [BLUE, GOLD, AUTHORITY, RED, COPPER][i], 1.8) for i, v in enumerate(["NARROW", "DELAY", "ESCALATE", "BLOCK", "RE-CONTRACT"])]).arrange(DOWN, buff=0.22).shift(RIGHT * 4.5)
        arrows11 = VGroup(*[Arrow(gate11.get_right(), route.get_left(), color=route[0].get_stroke_color(), stroke_width=3, buff=0.1) for route in routes11])
        scene11 = VGroup(grant11, review11, attempted11, cross11, gate11, routes11, arrows11)
        self.play_beat(11, FadeOut(scene10), FadeIn(grant11), FadeIn(review11), TransformFromCopy(review11, attempted11), Create(cross11), FadeIn(gate11), LaggedStart(*[GrowArrow(a) for a in arrows11], lag_ratio=0.1), LaggedStart(*[FadeIn(r) for r in routes11], lag_ratio=0.1), Indicate(review11, color=AUTHORITY), Indicate(routes11, color=GOLD), settle=0.75)

        # 12 — the rights check binds to a named holder and timed effect
        lina12 = self.person().scale(0.82).shift(RIGHT * 4.9)
        clock12 = Circle(radius=0.78, stroke_color=RED, stroke_width=4).shift(RIGHT * 4.9 + UP * 2.2)
        hands12 = VGroup(Line(clock12.get_center(), clock12.get_center() + UP * 0.45, color=RED, stroke_width=4), Line(clock12.get_center(), clock12.get_center() + RIGHT * 0.34, color=RED, stroke_width=4))
        check_names12 = ["WHEN?", "UNDERSTAND?", "CHANNEL?", "WHO REVIEWS?", "REMEDY?"]
        checks12 = VGroup(*[self.badge(v, [RED, BLUE, ACCENT, VIOLET, GREEN][i], 2.1) for i, v in enumerate(check_names12)]).arrange(DOWN, buff=0.35).shift(LEFT * 1.0)
        links12 = VGroup(*[DashedLine(c.get_right(), lina12.get_left(), color=c[0].get_stroke_color(), stroke_width=2) for c in checks12])
        holder12 = self.badge("HOLDER · LINA", GREEN, 2.4).shift(LEFT * 4.8 + UP * 2.2)
        scene12 = VGroup(lina12, clock12, hands12, checks12, links12, holder12)
        self.play_beat(12, FadeOut(scene11), FadeIn(lina12), Create(clock12), Create(hands12), FadeIn(holder12), LaggedStart(*[Create(link) for link in links12], lag_ratio=0.1), LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in checks12], lag_ratio=0.1), LaggedStart(*[Indicate(c, color=c[0].get_stroke_color()) for c in checks12], lag_ratio=0.1), Indicate(lina12, color=GREEN), settle=0.65)

        # 13 — nine rights handles, one expanded into material fields
        handle_names13 = ["NOTICE", "EXPLAIN", "REFUSE", "REVIEW", "APPEAL", "CORRECT", "ROLLBACK", "EXIT", "ACCOUNT"]
        handles13 = VGroup(*[self.right_handle(v) for v in handle_names13]).arrange_in_grid(rows=3, cols=3, buff=(0.22, 0.25)).shift(LEFT * 3.8)
        expanded13 = self.panel("REVIEW HANDLE", GREEN, 5.6, 3.5).shift(RIGHT * 2.8)
        fields13 = self.grid(["HOLDER", "DEADLINE", "ARTIFACT", "ACCESS", "PRINCIPAL", "REPAIR"], [GREEN, RED, BLUE, ACCENT, AUTHORITY, ROLLBACK], 3, 1.55).move_to(expanded13[0])
        arrow13 = Arrow(handles13[3].get_right(), expanded13.get_left(), color=GREEN, stroke_width=4, buff=0.12)
        scene13 = VGroup(handles13, expanded13, fields13, arrow13)
        self.play_beat(13, FadeOut(scene12), LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in handles13], lag_ratio=0.09), Indicate(handles13[3], color=GREEN), GrowArrow(arrow13), FadeIn(expanded13), LaggedStart(*[FadeIn(f, shift=UP * 0.15) for f in fields13], lag_ratio=0.12), LaggedStart(*[Indicate(f, color=f[0].get_stroke_color()) for f in fields13], lag_ratio=0.1), Indicate(handles13, color=GREEN), settle=0.75)

        # 14 — delivery passes two checks while overall usability remains pending
        notice14 = self.badge("NOTICE TO LINA", BLUE, 2.4).shift(LEFT * 5.0 + UP * 0.8)
        language14 = self.badge("REQUESTED LANGUAGE · PASS", GREEN, 2.9).shift(LEFT * 1.7 + UP * 1.35)
        reader14 = self.badge("SCREEN READER · PASS", GREEN, 2.6).shift(LEFT * 1.7 + DOWN * 0.35)
        lina14 = self.person().scale(0.72).shift(RIGHT * 4.8 + UP * 0.5)
        path14a = Arrow(notice14.get_right(), language14.get_left(), color=BLUE, stroke_width=4, buff=0.1)
        path14b = Arrow(language14.get_right(), lina14.get_left(), color=GREEN, stroke_width=4, buff=0.1)
        path14c = Arrow(reader14.get_right(), lina14.get_left(), color=GREEN, stroke_width=4, buff=0.1)
        pending14 = self.badge("OVERALL CONTROL · PENDING", GOLD, 3.3).shift(DOWN * 2.25)
        review14 = self.right_handle("REVIEW · CLOSED", RED, 2.5).shift(RIGHT * 1.4 + DOWN * 1.35)
        token14 = Dot(path14a.get_start(), radius=0.13, color=BLUE)
        scene14 = VGroup(notice14, language14, reader14, lina14, path14a, path14b, path14c, pending14, review14, token14)
        self.play_beat(14, FadeOut(scene13), FadeIn(notice14), FadeIn(lina14), GrowArrow(path14a), MoveAlongPath(token14, path14a), FadeIn(language14), FadeIn(reader14), GrowArrow(path14b), GrowArrow(path14c), Indicate(language14, color=GREEN), Indicate(reader14, color=GREEN), FadeIn(review14), FadeIn(pending14), settle=0.55)

        # 15 — timing, device, and reviewer capture make the appeal unusable
        timer15 = self.panel("20 MINUTES", RED, 2.8, 2.0).shift(LEFT * 4.7 + UP * 0.6)
        timer_bar15 = Rectangle(width=2.2, height=0.38, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.7).move_to(timer15[0]).shift(DOWN * 0.15)
        phone15 = self.badge("PHONE", GREEN, 1.5).shift(LEFT * 1.5 + UP * 1.2)
        laptop15 = self.badge("LAPTOP ONLY", RED, 2.1).shift(LEFT * 1.5 + DOWN * 0.4)
        barrier15 = Line(UP * 1.1, DOWN * 1.1, color=RED, stroke_width=7).shift(RIGHT * 0.25)
        office15 = self.panel("OPERATING OFFICE", VIOLET, 3.3, 1.7).shift(RIGHT * 4.1 + UP * 0.5)
        loop15 = Arrow(office15.get_bottom(), office15.get_left(), color=VIOLET, stroke_width=4, buff=0.1)
        captured15 = self.badge("FORMAL ≠ USABLE · CAPTURED", RED, 4.0).shift(DOWN * 2.35)
        scene15 = VGroup(timer15, timer_bar15, phone15, laptop15, barrier15, office15, loop15, captured15)
        timer_empty15 = timer_bar15.copy().stretch_to_fit_width(0.18).align_to(timer_bar15, LEFT)
        self.play_beat(15, FadeOut(scene14), FadeIn(timer15), FadeIn(timer_bar15), Transform(timer_bar15, timer_empty15), FadeIn(phone15), Create(barrier15), FadeIn(laptop15), FadeIn(office15), GrowArrow(loop15), Indicate(office15, color=VIOLET), FadeIn(captured15), Indicate(captured15, color=RED), settle=0.65)

        # 16 — fail closed and retain four explicit residual causes
        token16 = self.action_token(compact=True).shift(LEFT * 4.2 + UP * 0.6)
        gate16 = self.gate().shift(LEFT * 1.2 + UP * 0.6)
        lina16 = self.person().scale(0.62).shift(RIGHT * 5.1 + UP * 0.6)
        path16 = Line(token16.get_right(), lina16.get_left(), color=BOUNDARY, stroke_width=5)
        residual_values16 = ["DEGRADED REVIEW", "TIMING FAILURE", "SHARED AUTHORITY", "IRREVERSIBLE RISK"]
        residuals16 = self.grid(residual_values16, [RED, RED, VIOLET, RESIDUAL], 2, 2.35).shift(RIGHT * 1.7 + DOWN * 1.65)
        tray16 = self.panel("OWNED RESIDUALS", RESIDUAL, 5.8, 2.0).move_to(residuals16).shift(UP * 0.05)
        title16 = self.badge("GATE FAILURE · NOT A LOW SCORE", RED, 4.0).shift(UP * 2.65)
        scene16 = VGroup(token16, gate16, lina16, path16, residuals16, tray16, title16)
        self.play_beat(16, FadeOut(scene15), Create(path16), FadeIn(token16), FadeIn(lina16), FadeIn(gate16), Indicate(gate16, color=RED), FadeIn(tray16), LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in residuals16], lag_ratio=0.12), LaggedStart(*[Indicate(r, color=r[0].get_stroke_color()) for r in residuals16], lag_ratio=0.12), FadeIn(title16), settle=0.7)

        # 17 — bounded route preserves payment and independent pre-effect review
        payment17 = self.payment().shift(RIGHT * 4.7 + DOWN * 1.55)
        lina17 = self.person().scale(0.7).shift(RIGHT * 4.7 + UP * 0.65)
        held17 = self.panel("AUTOMATION HELD", RED, 3.1, 1.7).shift(LEFT * 4.7 + UP * 0.4)
        token17 = self.action_token(compact=True).scale(0.8).move_to(held17[0])
        notice17 = self.right_handle("NOTICE · ACCESSIBLE", BLUE, 2.7).shift(LEFT * 0.7 + UP * 1.3)
        review17 = self.right_handle("INDEPENDENT REVIEW · 10 AM", GREEN, 3.5).shift(LEFT * 0.7 + DOWN * 0.25)
        notice_path17 = Arrow(held17.get_right(), notice17.get_left(), color=BLUE, stroke_width=4, buff=0.1)
        review_path17 = Arrow(review17.get_right(), lina17.get_left(), color=GREEN, stroke_width=5, buff=0.1)
        payment_path17 = Arrow(held17.get_right() + DOWN * 0.8, payment17.get_left(), color=GREEN, stroke_width=6, buff=0.12)
        bounded17 = self.badge("BOUNDED ROUTE · BEFORE EFFECT", GOLD, 3.8).shift(UP * 2.7)
        scene17 = VGroup(payment17, lina17, held17, token17, notice17, review17, notice_path17, review_path17, payment_path17, bounded17)
        self.play_beat(17, FadeOut(scene16), FadeIn(held17), FadeIn(token17), FadeIn(lina17), FadeIn(payment17), GrowArrow(payment_path17), Indicate(payment17, color=GREEN), FadeIn(notice17), GrowArrow(notice_path17), FadeIn(review17), GrowArrow(review_path17), Indicate(review17, color=GREEN), FadeIn(bounded17), settle=0.8)

        # 18 — bind the distributed route into a constitutional decision receipt
        receipt18 = self.panel("CONSTITUTIONAL DECISION RECEIPT", GOLD, 6.8, 4.0)
        fields18 = self.grid(
            ["v7 + C-14", "TASK", "CONSUMER", "LINA", "TESTS", "REVIEWER DEP.", "DECISION", "EXPIRY", "RESIDUALS", "APPEAL", "ROLLBACK"],
            [GOLD, AUTHORITY, ACCENT, GREEN, EVIDENCE, VIOLET, BLUE, MUTED, RESIDUAL, GREEN, ROLLBACK], 4, 1.55,
        ).scale(0.88).move_to(receipt18[0]).shift(DOWN * 0.1)
        source18 = VGroup(self.kernel(compact=True), self.action_token(compact=True), self.person().scale(0.45)).arrange(DOWN, buff=0.35).shift(LEFT * 5.2)
        connectors18 = VGroup(*[DashedLine(source18[i].get_right(), receipt18.get_left(), color=[GOLD, RED, GREEN][i], stroke_width=2) for i in range(3)])
        scene18 = VGroup(receipt18, fields18, source18, connectors18)
        self.play_beat(18, FadeOut(scene17), FadeIn(source18), LaggedStart(*[Create(c) for c in connectors18], lag_ratio=0.15), FadeIn(receipt18), LaggedStart(*[TransformFromCopy(source18[i % 3], f) for i, f in enumerate(fields18)], lag_ratio=0.08), LaggedStart(*[Indicate(f, color=f[0].get_stroke_color()) for f in fields18], lag_ratio=0.06), Indicate(receipt18, color=GOLD), settle=0.75)

        # 19 — joint outcomes preserve governance costs without buying violations
        metric_names19 = ["LATENCY", "OPERATOR", "MISSED HELP", "UNAUTHORIZED", "CORRECTION", "RETALIATION", "PRIVACY", "THROUGHPUT"]
        metric_colors19 = [AUTHORITY, COPPER, MUTED, RED, GREEN, RESIDUAL, VIOLET, ACCENT]
        shells19 = VGroup()
        bars19 = VGroup()
        for i, (name, color) in enumerate(zip(metric_names19, metric_colors19)):
            shell = RoundedRectangle(width=1.3, height=3.4, corner_radius=0.12, stroke_color=color, stroke_width=2.6, fill_color=SURFACE, fill_opacity=1)
            label = self.label(name, 10, color, "BOLD").next_to(shell, DOWN, buff=0.1)
            if label.width > 1.25:
                label.scale_to_fit_width(1.25)
            shells19.add(VGroup(shell, label))
            level = [0.65, 0.52, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0][i]
            bar = Rectangle(width=0.95, height=max(0.12, 2.8 * max(level, 0.04)), stroke_width=0, fill_color=color, fill_opacity=0.7)
            bars19.add(bar)
        shells19.arrange(RIGHT, buff=0.2).scale(0.88).shift(DOWN * 0.2)
        for i, bar in enumerate(bars19):
            bar.scale(0.88).move_to(shells19[i][0]).align_to(shells19[i][0], DOWN).shift(UP * 0.16)
        clause19 = self.badge("C-14 · NO TRADE", GOLD, 3.0, 0.65).shift(UP * 2.7)
        line19 = Line(LEFT * 5.8 + UP * 2.25, RIGHT * 5.8 + UP * 2.25, color=GOLD, stroke_width=5)
        empty19 = self.label("EMPTY SOCKETS = PROSPECTIVE", 16, MUTED, "BOLD").shift(DOWN * 2.7)
        scene19 = VGroup(shells19, bars19, clause19, line19, empty19)
        self.play_beat(19, FadeOut(scene18), Create(line19), FadeIn(clause19), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in shells19], lag_ratio=0.08), GrowFromCenter(bars19[0]), GrowFromCenter(bars19[1]), LaggedStart(*[Indicate(shells19[i], color=metric_colors19[i]) for i in range(2, 8)], lag_ratio=0.08), FadeIn(empty19), Indicate(clause19, color=GOLD), settle=0.8)

        # 20 — update U-42 removes pre-effect review for throughput
        kernel20 = self.kernel().shift(LEFT * 4.4 + UP * 0.3)
        update20 = self.panel("UPDATE U-42", VIOLET, 5.5, 3.8).shift(RIGHT * 2.3 + UP * 0.2)
        benefit20 = VGroup(self.badge("QUEUE ↓", GREEN, 1.8), self.badge("SCORE > 90", EVIDENCE, 2.0)).arrange(RIGHT, buff=0.3).move_to(update20[0]).shift(UP * 0.8)
        old20 = self.badge("PRE-EFFECT REVIEW", GOLD, 2.8).move_to(update20[0]).shift(DOWN * 0.25)
        deleted20 = self.badge("DELETE", RED, 1.7).move_to(update20[0]).shift(DOWN * 1.05)
        proposal20 = Arrow(kernel20.get_right(), update20.get_left(), color=VIOLET, stroke_width=5, buff=0.12)
        cross20 = Cross(old20, stroke_color=RED, stroke_width=5)
        scene20 = VGroup(kernel20, update20, benefit20, old20, deleted20, proposal20, cross20)
        self.play_beat(20, FadeOut(scene19), FadeIn(kernel20), GrowArrow(proposal20), FadeIn(update20), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in benefit20], lag_ratio=0.2), FadeIn(old20), FadeIn(deleted20), Create(cross20), Indicate(benefit20, color=GREEN), Indicate(old20, color=RED), settle=0.65)

        # 21 — reject self-approval and identifier laundering
        update21 = self.panel("U-42 BENEFITS", VIOLET, 3.3, 2.1).shift(LEFT * 4.5)
        self_approve21 = self.badge("SELF-APPROVED", GREEN, 2.4).move_to(update21[0])
        self_loop21 = Arrow(update21.get_top(), update21.get_left(), color=VIOLET, stroke_width=4, buff=0.2)
        cross21 = Cross(self_approve21, stroke_color=RED, stroke_width=5)
        id_old21 = self.badge("C-14", GOLD, 1.7).shift(LEFT * 0.8 + UP * 1.1)
        id_new21 = self.badge("C-14", GOLD, 1.7).shift(RIGHT * 1.3 + UP * 1.1)
        fingerprint_old21 = self.grid(["NOTICE", "INDEPENDENT", "PRE-EFFECT"], [BLUE, GREEN, GOLD], 1, 2.2).scale(0.72).shift(LEFT * 0.8 + DOWN * 0.65)
        fingerprint_new21 = self.grid(["NOTICE", "SAME OFFICE", "AFTER"], [BLUE, RED, RED], 1, 2.2).scale(0.72).shift(RIGHT * 1.3 + DOWN * 0.65)
        neq21 = self.label("≠", 46, RED, "BOLD").shift(RIGHT * 0.25 + DOWN * 0.65)
        rule21 = self.badge("NO SELF-WEAKENING", RED, 3.0).shift(RIGHT * 4.7)
        scene21 = VGroup(update21, self_approve21, self_loop21, cross21, id_old21, id_new21, fingerprint_old21, fingerprint_new21, neq21, rule21)
        self.play_beat(21, FadeOut(scene20), FadeIn(update21), FadeIn(self_approve21), GrowArrow(self_loop21), Create(cross21), FadeIn(id_old21), TransformFromCopy(id_old21, id_new21), FadeIn(fingerprint_old21), FadeIn(fingerprint_new21), FadeIn(neq21), LaggedStart(Indicate(fingerprint_old21, color=GOLD), Indicate(fingerprint_new21, color=RED), lag_ratio=0.3), FadeIn(rule21), settle=0.7)

        # 22 — three material changes appear in the migration diff
        old22 = self.panel("v7 · C-14", GOLD, 3.3, 4.7).shift(LEFT * 4.4)
        new22 = self.panel("U-42 · C-14", VIOLET, 3.3, 4.7).shift(RIGHT * 4.4)
        old_rows22 = VGroup(self.badge("PRE-EFFECT", GOLD, 2.2), self.badge("NARROW EXCEPTION", BLUE, 2.3), self.badge("INDEPENDENT", GREEN, 2.2)).arrange(DOWN, buff=0.5).move_to(old22[0])
        new_rows22 = VGroup(self.badge("REMOVED", RED, 2.2), self.badge("WIDER EXCEPTION", RED, 2.3), self.badge("OPERATING TEAM", RED, 2.2)).arrange(DOWN, buff=0.5).move_to(new22[0])
        diff_arrows22 = VGroup(*[Arrow(old_rows22[i].get_right(), new_rows22[i].get_left(), color=RED, stroke_width=4, buff=0.12) for i in range(3)])
        diff_tags22 = VGroup(self.badge("DELETE", RED, 1.4), self.badge("WIDEN", RED, 1.4), self.badge("MERGE", RED, 1.4)).arrange(DOWN, buff=0.74)
        scene22 = VGroup(old22, new22, old_rows22, new_rows22, diff_arrows22, diff_tags22)
        self.play_beat(22, FadeOut(scene21), FadeIn(old22), FadeIn(new22), LaggedStart(*[FadeIn(r) for r in old_rows22], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in diff_arrows22], lag_ratio=0.2), LaggedStart(*[FadeIn(r) for r in new_rows22], lag_ratio=0.15), LaggedStart(*[FadeIn(t) for t in diff_tags22], lag_ratio=0.2), LaggedStart(*[Indicate(new_rows22[i], color=RED) for i in range(3)], lag_ratio=0.2), settle=0.75)

        # 23 — quarantine U-42 while v7 remains authoritative
        active23 = self.kernel().shift(LEFT * 4.7 + UP * 1.45)
        active_tag23 = self.badge("ACTIVE AUTHORITY", GREEN, 2.4).next_to(active23, DOWN, buff=0.2)
        quarantine23 = self.panel("QUARANTINE · U-42", VIOLET, 5.0, 3.8).shift(RIGHT * 2.2)
        diff23 = VGroup(*[r.copy().scale(0.8) for r in new_rows22]).arrange(DOWN, buff=0.3).move_to(quarantine23[0])
        review_values23 = ["SCOPE", "DISSENT", "ROLLBACK", "CONSUMERS", "UNCERTAINTY"]
        review23 = VGroup(*[self.badge(v, [BLUE, RESIDUAL, ROLLBACK, ACCENT, MUTED][i], 1.8) for i, v in enumerate(review_values23)])
        angles23 = [PI * (0.15 + i * 0.22) for i in range(5)]
        for item, angle in zip(review23, angles23):
            item.move_to(quarantine23.get_center() + 3.3 * (RIGHT * cos(angle) + UP * sin(angle)))
        links23 = VGroup(*[DashedLine(item.get_center(), quarantine23.get_center(), color=item[0].get_stroke_color(), stroke_width=2) for item in review23])
        scene23 = VGroup(active23, active_tag23, quarantine23, diff23, review23, links23)
        self.play_beat(23, FadeOut(scene22), FadeIn(quarantine23), LaggedStart(*[TransformFromCopy(new_rows22[i], diff23[i]) for i in range(3)], lag_ratio=0.18), Create(quarantine23[0]), FadeIn(active23), FadeIn(active_tag23), LaggedStart(*[Create(link) for link in links23], lag_ratio=0.12), LaggedStart(*[FadeIn(item) for item in review23], lag_ratio=0.12), Indicate(active23, color=GOLD), Indicate(quarantine23, color=VIOLET), settle=0.75)

        # 24 — exact predicate digest and correction handles cross descendants
        kernel24 = self.kernel(compact=True).shift(LEFT * 5.6 + UP * 0.8)
        node_names24 = ["PLANNER", "TOOL", "REPLACEMENT", "DESCENDANT"]
        nodes24 = VGroup(*[self.panel(v, [BLUE, ACCENT, VIOLET, RESIDUAL][i], 2.35, 1.7) for i, v in enumerate(node_names24)]).arrange(RIGHT, buff=0.5).scale(0.82).shift(RIGHT * 0.6 + UP * 0.8)
        edges24 = VGroup(Arrow(kernel24.get_right(), nodes24[0].get_left(), color=GOLD, stroke_width=4, buff=0.1), *[Arrow(nodes24[i].get_right(), nodes24[i + 1].get_left(), color=GOLD, stroke_width=4, buff=0.1) for i in range(3)])
        digests24 = VGroup(*[self.badge("C-14 DIGEST", GOLD, 1.8, 0.42).scale(0.72).move_to(n[0]).shift(UP * 0.23) for n in nodes24])
        handles24 = VGroup(*[self.badge("CORRECTION LIVE", GREEN, 1.9, 0.42).scale(0.72).move_to(n[0]).shift(DOWN * 0.32) for n in nodes24])
        missing24 = self.badge("HANDLE LOST", RED, 1.8, 0.42).scale(0.72).move_to(handles24[-1])
        admission24 = self.badge("ADMISSION BLOCKED", RED, 2.8).shift(RIGHT * 4.5 + DOWN * 1.65)
        scene24 = VGroup(kernel24, nodes24, edges24, digests24, handles24, missing24, admission24)
        self.play_beat(24, FadeOut(scene23), FadeIn(kernel24), LaggedStart(*[FadeIn(n) for n in nodes24], lag_ratio=0.12), LaggedStart(*[GrowArrow(e) for e in edges24], lag_ratio=0.12), LaggedStart(*[TransformFromCopy(kernel24, d) for d in digests24], lag_ratio=0.12), LaggedStart(*[FadeIn(h) for h in handles24], lag_ratio=0.12), ReplacementTransform(handles24[-1], missing24), Indicate(missing24, color=RED), FadeIn(admission24), Indicate(nodes24[-1], color=RED), settle=0.75)

        # 25 — legal authority packet stays beside, not inside, the kernel
        kernel25 = self.kernel().shift(LEFT * 4.3 + UP * 0.3)
        legal25 = self.panel("LEGAL AUTHORITY PACKET", BLUE, 5.2, 4.0).shift(RIGHT * 2.5 + UP * 0.2)
        legal_fields25 = self.grid(["JURISDICTION", "TIME", "SOURCE", "INTERPRET", "CONFLICT", "EXCEPTION", "APPEAL"], [BLUE, MUTED, EVIDENCE, VIOLET, RESIDUAL, RED, GREEN], 3, 1.55).scale(0.88).move_to(legal25[0])
        case_rule25 = Arrow(legal25.get_bottom(), DOWN * 2.7, color=BLUE, stroke_width=4, buff=0.15)
        gate_label25 = self.badge("CASE GATE", BLUE, 2.0).shift(DOWN * 2.75)
        rewrite25 = Arrow(legal25.get_left(), kernel25.get_right(), color=RED, stroke_width=4, buff=0.12)
        block25 = Cross(rewrite25, stroke_color=RED, stroke_width=5)
        beside25 = self.badge("BESIDE · NOT INSIDE", GOLD, 2.8).shift(UP * 2.8)
        scene25 = VGroup(kernel25, legal25, legal_fields25, case_rule25, gate_label25, rewrite25, block25, beside25)
        self.play_beat(25, FadeOut(scene24), FadeIn(kernel25), FadeIn(legal25), LaggedStart(*[FadeIn(f, shift=UP * 0.16) for f in legal_fields25], lag_ratio=0.1), LaggedStart(*[Indicate(f, color=f[0].get_stroke_color()) for f in legal_fields25], lag_ratio=0.08), GrowArrow(case_rule25), FadeIn(gate_label25), GrowArrow(rewrite25), Create(block25), FadeIn(beside25), settle=0.8)

        # 26 — four distinct constitutional failures
        quadrants26 = VGroup(
            self.panel("NO CONSUMER", RED, 5.4, 2.3),
            self.panel("AFFECTED PARTY OMITTED", RESIDUAL, 5.4, 2.3),
            self.panel("APOLOGY AFTER EFFECT", AUTHORITY, 5.4, 2.3),
            self.panel("EXIT LOCKED", VIOLET, 5.4, 2.3),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.42)).scale(0.88)
        disconnected26 = VGroup(self.badge("PRINCIPLE", GOLD, 1.7), DashedLine(LEFT * 0.7, RIGHT * 0.7, color=MUTED), self.badge("?", RED, 0.65)).arrange(RIGHT, buff=0.2).move_to(quadrants26[0][0])
        omitted26 = VGroup(self.person("...").scale(0.35), Cross(self.person("...").scale(0.35), stroke_color=RED, stroke_width=4)).arrange(RIGHT, buff=0.4).move_to(quadrants26[1][0])
        apology26 = VGroup(self.badge("EFFECT", RED, 1.4), Arrow(LEFT * 0.5, RIGHT * 0.5, color=MUTED), self.badge("SORRY", AUTHORITY, 1.4)).arrange(RIGHT, buff=0.2).move_to(quadrants26[2][0])
        exit26 = VGroup(self.badge("PERSONALIZED", VIOLET, 1.9), Line(LEFT * 0.4, RIGHT * 0.4, color=VIOLET, stroke_width=5), self.badge("EXIT ×", RED, 1.4)).arrange(RIGHT, buff=0.2).move_to(quadrants26[3][0])
        examples26 = VGroup(disconnected26, omitted26, apology26, exit26)
        scene26 = VGroup(quadrants26, examples26)
        self.play_beat(26, FadeOut(scene25), LaggedStart(*[FadeIn(q, shift=UP * 0.2) for q in quadrants26], lag_ratio=0.12), FadeIn(disconnected26), Indicate(disconnected26[-1], color=RED), FadeIn(omitted26), Indicate(omitted26, color=RESIDUAL), FadeIn(apology26), Indicate(apology26[0], color=RED), FadeIn(exit26), Indicate(exit26[-1], color=RED), LaggedStart(*[Indicate(q, color=q[0].get_stroke_color()) for q in quadrants26], lag_ratio=0.12), settle=0.85)

        # 27 — challenger heterarchy reveals shared dependencies and open quality evidence
        receipt27 = self.panel("ACTION RECEIPT", GOLD, 2.7, 1.7)
        challenger_names27 = ["EVIDENCE", "TASK", "RIGHTS", "EFFECT"]
        challenger_colors27 = [EVIDENCE, AUTHORITY, RESIDUAL, VIOLET]
        challengers27 = VGroup()
        for i, (name, color) in enumerate(zip(challenger_names27, challenger_colors27)):
            angle = PI / 4 + i * PI / 2
            challengers27.add(self.badge(name, color, 1.8).move_to(3.0 * (RIGHT * cos(angle) + UP * sin(angle))))
        challenge_edges27 = VGroup(*[DashedLine(c.get_center(), receipt27.get_center(), color=challenger_colors27[i], stroke_width=2.5) for i, c in enumerate(challengers27)])
        roots27 = VGroup(self.badge("SHARED MODEL", RED, 2.1), self.badge("SHARED DATA", RED, 2.1)).arrange(RIGHT, buff=0.35).shift(DOWN * 2.55)
        root_edges27 = VGroup(*[Arrow(root.get_top(), c.get_bottom(), color=RED, stroke_width=2, buff=0.12) for root in roots27 for c in challengers27[:2]])
        evidence_names27 = ["LINEAGE", "COMPETENCE", "DEPENDENCIES", "CONFLICTS", "ERROR RATES", "OVERRIDE", "FAILURES"]
        evidence27 = VGroup(*[self.badge(v, MUTED, 1.7, 0.42) for v in evidence_names27]).arrange(DOWN, buff=0.13).scale(0.75).shift(RIGHT * 5.0)
        title27 = self.badge("HETERARCHY ≠ MAGIC", COPPER, 2.9).shift(UP * 2.75)
        scene27 = VGroup(receipt27, challengers27, challenge_edges27, roots27, root_edges27, evidence27, title27)
        self.play_beat(27, FadeOut(scene26), FadeIn(receipt27), LaggedStart(*[Create(e) for e in challenge_edges27], lag_ratio=0.12), LaggedStart(*[FadeIn(c) for c in challengers27], lag_ratio=0.12), LaggedStart(*[Indicate(c, color=challenger_colors27[i]) for i, c in enumerate(challengers27)], lag_ratio=0.12), FadeIn(roots27), LaggedStart(*[GrowArrow(e) for e in root_edges27], lag_ratio=0.1), LaggedStart(*[FadeIn(e) for e in evidence27], lag_ratio=0.08), Indicate(roots27, color=RED), FadeIn(title27), settle=0.85)

        # 28 — finite accepted and rejected traces remain inside their proof envelope
        model28 = self.panel("FINITE TRANSITION MODEL", BLUE, 4.3, 4.0).shift(LEFT * 1.6)
        start28 = self.badge("RECORDED STATE", MUTED, 2.0).move_to(model28[0]).shift(UP * 1.0)
        end28 = self.badge("BOUNDED EFFECT", GREEN, 2.0).move_to(model28[0]).shift(DOWN * 1.0)
        route28 = Arrow(start28.get_bottom(), end28.get_top(), color=GREEN, stroke_width=5, buff=0.1)
        accepted28 = VGroup(*[Dot(route28.get_start(), radius=0.10, color=GREEN) for _ in range(5)])
        accepted_count28 = self.badge("5 ACCEPTED TRACES", GREEN, 2.4, 0.5).scale(0.82).next_to(end28, RIGHT, buff=0.25)
        rejected_names28 = ["MISSING REVIEW", "DELETE", "WIDEN"]
        rejected28 = VGroup(*[self.badge(v, RED, 2.1) for v in rejected_names28]).arrange(DOWN, buff=0.35).shift(RIGHT * 4.6)
        reject_edges28 = VGroup(*[Arrow(r.get_left() + LEFT * 1.5, r.get_left(), color=RED, stroke_width=3, buff=0.1) for r in rejected28])
        double28 = VGroup(Rectangle(width=9.4, height=5.7, stroke_color=COPPER, stroke_width=4), Rectangle(width=9.0, height=5.3, stroke_color=COPPER, stroke_width=1.6))
        boundary28 = self.badge("FINITE RECORD PROOF · ARGUMENT SUPPORT", COPPER, 4.7).shift(DOWN * 2.9)
        lina28 = self.person().scale(0.42).shift(RIGHT * 5.65 + UP * 1.8)
        outside28 = self.badge("REAL WORLD · OUTSIDE", MUTED, 2.4, 0.46).scale(0.82).shift(RIGHT * 5.65 + DOWN * 2.15)
        scene28 = VGroup(model28, start28, end28, route28, accepted28, accepted_count28, rejected28, reject_edges28, double28, boundary28, lina28, outside28)
        self.play_beat(28, FadeOut(scene27), Create(double28), FadeIn(model28), FadeIn(start28), FadeIn(end28), GrowArrow(route28), LaggedStart(*[MoveAlongPath(dot, route28) for dot in accepted28], lag_ratio=0.12), FadeIn(accepted_count28), LaggedStart(*[FadeIn(r) for r in rejected28], lag_ratio=0.15), LaggedStart(*[GrowArrow(e) for e in reject_edges28], lag_ratio=0.15), LaggedStart(*[Indicate(r, color=RED) for r in rejected28], lag_ratio=0.15), FadeIn(boundary28), FadeIn(lina28), FadeIn(outside28), settle=0.9)

        # 29 — prospective mature campaign, all result sockets empty
        proof29 = self.panel("CURRENT · FINITE", COPPER, 2.8, 1.8).shift(LEFT * 5.2)
        lane_names29 = ["NATURAL TASKS", "ADVERSARIAL CHANGE", "INDEPENDENT EVAL", "DESCENDANT STRESS", "REAL CORRECTION", "JOINT MEASUREMENT"]
        lane_colors29 = [BLUE, RED, VIOLET, RESIDUAL, GREEN, AUTHORITY]
        lanes29 = VGroup(*[self.badge(v, lane_colors29[i], 2.4) for i, v in enumerate(lane_names29)]).arrange(DOWN, buff=0.25).shift(LEFT * 1.4)
        lane_edges29 = VGroup(*[Arrow(proof29.get_right(), lane.get_left(), color=lane_colors29[i], stroke_width=2.7, buff=0.12) for i, lane in enumerate(lanes29)])
        outcome_names29 = ["SERVICE", "RIGHTS USE", "HARM", "LATENCY", "PRIVACY", "GOV COST"]
        outcomes29 = VGroup(*[self.panel(v, MUTED, 1.55, 3.4) for v in outcome_names29]).arrange(RIGHT, buff=0.16).scale(0.62).shift(RIGHT * 3.55)
        empty29 = self.badge("PROSPECTIVE · NO RESULTS", RED, 3.4).shift(UP * 2.75)
        scene29 = VGroup(proof29, lanes29, lane_edges29, outcomes29, empty29)
        self.play_beat(29, FadeOut(scene28), FadeIn(proof29), LaggedStart(*[GrowArrow(e) for e in lane_edges29], lag_ratio=0.09), LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in lanes29], lag_ratio=0.09), LaggedStart(*[Indicate(l, color=lane_colors29[i]) for i, l in enumerate(lanes29)], lag_ratio=0.08), LaggedStart(*[FadeIn(o, shift=UP * 0.18) for o in outcomes29], lag_ratio=0.08), LaggedStart(*[Indicate(o, color=MUTED) for o in outcomes29], lag_ratio=0.08), FadeIn(empty29), Indicate(empty29, color=RED), settle=0.9)

        # 30 — nine broad conclusions stop outside the empty proof region
        proof30 = self.panel("PROVED", COPPER, 3.0, 3.0)
        empty30 = self.label("EMPTY", 30, MUTED, "BOLD").move_to(proof30[0])
        nonclaim_names30 = ["CORRECT VALUES", "LEGITIMATE AUTHORSHIP", "CONSENT", "DIGNITY", "REVIEWER INDEPENDENCE", "MANIPULATION RESISTANCE", "WHOLE-SYSTEM CORRIGIBILITY", "LAWFUL", "SAFE DEPLOYMENT"]
        nonclaims30 = VGroup(*[self.badge(f"≠ {v}", RED if i % 2 == 0 else RESIDUAL, 2.75, 0.46) for i, v in enumerate(nonclaim_names30)]).arrange_in_grid(rows=3, cols=3, buff=(0.22, 0.28)).scale(0.83).shift(DOWN * 2.15)
        starts30 = [LEFT * 5.5 + UP * 2.5, LEFT * 2.0 + UP * 2.7, RIGHT * 2.0 + UP * 2.7, RIGHT * 5.5 + UP * 2.5]
        approach30 = VGroup(*[Arrow(starts30[i % 4], proof30.get_center(), color=RED, stroke_width=2, buff=1.6) for i in range(9)])
        boundary30 = VGroup(Line(UP * 2.3, DOWN * 0.3, color=COPPER, stroke_width=5).shift(LEFT * 1.8), Line(UP * 2.3, DOWN * 0.3, color=COPPER, stroke_width=2).shift(LEFT * 1.62))
        scene30 = VGroup(proof30, empty30, nonclaims30, approach30, boundary30)
        self.play_beat(30, FadeOut(scene29), FadeIn(proof30), FadeIn(empty30), Create(boundary30), LaggedStart(*[GrowArrow(a) for a in approach30], lag_ratio=0.05), LaggedStart(*[FadeIn(n, shift=UP * 0.18) for n in nonclaims30], lag_ratio=0.06), LaggedStart(*[Indicate(n, color=n[0].get_stroke_color()) for n in nonclaims30], lag_ratio=0.06), Indicate(empty30, color=MUTED), settle=0.95)

        # 31 — resolve the opening bridge and pass the unknown objective onward
        bridge31 = Line(LEFT * 5.8, RIGHT * 4.1, color=BOUNDARY, stroke_width=7).shift(UP * 0.6)
        evidence31 = self.badge("EVIDENCE", EVIDENCE, 1.7).shift(LEFT * 5.1 + UP * 1.4)
        task31 = self.badge("TASK", AUTHORITY, 1.5).shift(LEFT * 3.3 + UP * 1.4)
        kernel31 = self.kernel(compact=True).shift(LEFT * 1.1 + UP * 0.6)
        token31 = self.action_token(compact=True).shift(RIGHT * 1.3 + UP * 0.6)
        gate31 = self.gate().scale(0.72).shift(RIGHT * 3.25 + UP * 0.6)
        lina31 = self.person().scale(0.65).shift(RIGHT * 5.45 + UP * 0.6)
        payment31 = self.payment().scale(0.7).shift(RIGHT * 4.9 + DOWN * 0.95)
        handles31 = VGroup(self.right_handle("NOTICE", BLUE, 1.6), self.right_handle("INDEPENDENT REVIEW", GREEN, 2.5)).arrange(RIGHT, buff=0.3).shift(LEFT * 0.3 + DOWN * 1.55)
        green_path31 = Arrow(handles31.get_right(), lina31.get_left(), color=GREEN, stroke_width=5, buff=0.1)
        receipt31 = self.panel("BOUNDED RECEIPT", GOLD, 2.7, 1.5).shift(RIGHT * 1.0 + DOWN * 2.55)
        receipt_fields31 = VGroup(
            self.label("v7 · C-14 KEPT", 12, GOLD, "BOLD"),
            self.label("PAYMENT ACTIVE", 12, GREEN, "BOLD"),
            self.label("REVIEW · 10 AM", 11, BLUE, "BOLD"),
        ).arrange(DOWN, buff=0.10).move_to(receipt31[0]).shift(DOWN * 0.12)
        lens31 = Circle(radius=1.15, stroke_color=VIOLET, stroke_width=5, fill_color=DEEP, fill_opacity=1).shift(RIGHT * 5.6 + DOWN * 2.55)
        lens_title31 = self.label("INNER ALIGNMENT", 14, VIOLET, "BOLD").move_to(lens31).shift(UP * 0.25)
        unknown31 = self.label("OBJECTIVE ?", 18, INK, "BOLD").move_to(lens31).shift(DOWN * 0.25)
        handoff31 = Arrow(receipt31.get_right(), lens31.get_left(), color=VIOLET, stroke_width=4, buff=0.1)
        title31 = self.badge("USABLE CORRECTION · BEFORE EFFECT", GREEN, 4.2).shift(UP * 2.75)
        scene31 = VGroup(bridge31, evidence31, task31, kernel31, token31, gate31, lina31, payment31, handles31, green_path31, receipt31, receipt_fields31, lens31, lens_title31, unknown31, handoff31, title31)
        self.play_beat(31, FadeOut(scene30), Create(bridge31), FadeIn(evidence31), FadeIn(task31), FadeIn(kernel31), FadeIn(token31), FadeIn(gate31), FadeIn(lina31), FadeIn(payment31), Indicate(payment31, color=GREEN), LaggedStart(*[FadeIn(h) for h in handles31], lag_ratio=0.2), GrowArrow(green_path31), FadeIn(receipt31), LaggedStart(*[FadeIn(f, shift=UP * 0.08) for f in receipt_fields31], lag_ratio=0.15), GrowArrow(handoff31), GrowFromCenter(lens31), FadeIn(lens_title31), FadeIn(unknown31), FadeIn(title31), settle=0.9)

        self.wait_until(self.TARGET_DURATION)
