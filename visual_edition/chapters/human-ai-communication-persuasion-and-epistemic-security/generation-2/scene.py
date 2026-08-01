"""Generation-2 visual abstract for governed communication episodes.

One synthetic cooling-center notice persists from composition through delivery,
expiry, and correction. The words remain stable while pressure, identity,
targeting, repetition, reach, and repairability change around them.
"""

from __future__ import annotations

from math import cos, sin

from manim import (
    AnimationGroup, ArcBetweenPoints, Arrow, Circle, Create, Cross,
    DashedLine, Dot, DOWN, FadeIn, FadeOut, GrowArrow, GrowFromCenter,
    Indicate, LaggedStart, LEFT, Line, MoveAlongPath, ORIGIN, PI, Polygon,
    Rectangle, ReplacementTransform, RIGHT, RoundedRectangle, Text,
    Transform, TransformFromCopy, UP, VGroup, Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


VIOLET = "#9D7BE8"
DEEP = "#172A34"


class HumanAICommunicationGeneration2(AsiScene):
    TARGET_DURATION = 320.525
    ENDS = [
        11.155, 20.010, 30.465, 39.295, 49.250, 61.430, 69.435,
        79.465, 89.770, 100.125, 107.730, 118.435, 128.065, 140.820,
        151.700, 161.880, 171.860, 181.165, 191.995, 201.750,
        211.130, 221.735, 229.990, 238.995, 248.000, 257.405,
        269.510, 280.915, 294.420, 307.900, 320.525,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#111F28"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.05, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.05, remaining - min(settle, remaining * 0.18))
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
            stroke_color=color, stroke_width=2.7,
            fill_color=SURFACE, fill_opacity=1,
        )
        label = self.label(value, 13, color, "BOLD")
        if label.width > width - 0.18:
            label.scale_to_fit_width(width - 0.18)
        label.move_to(shell)
        return VGroup(shell, label)

    def panel(self, title: str, color: str, width: float, height: float) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=color, stroke_width=3.2,
            fill_color=DEEP, fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.25, 3.8), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 2.0) -> VGroup:
        items = VGroup(*[self.badge(v, colors[i], width, 0.5) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        items.arrange_in_grid(rows=rows, cols=columns, buff=(0.16, 0.18))
        return items

    def notice(self, compact: bool = False) -> VGroup:
        width = 5.7 if not compact else 3.8
        shell = RoundedRectangle(
            width=width, height=1.25 if not compact else 0.92,
            corner_radius=0.16, stroke_color=ACCENT, stroke_width=3.5,
            fill_color=DEEP, fill_opacity=1,
        )
        source = self.label("CITY NOTICE · SOURCE BOUND", 14 if not compact else 10, ACCENT, "BOLD")
        sentence = self.label("RIVERSIDE IS OPEN UNTIL 8", 22 if not compact else 14, INK, "BOLD")
        content = VGroup(source, sentence).arrange(DOWN, buff=0.15).move_to(shell)
        return VGroup(shell, content)

    def packet(self, compact: bool = False) -> VGroup:
        width = 5.3 if not compact else 3.6
        height = 2.35 if not compact else 1.55
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.22,
            stroke_color=COPPER, stroke_width=4,
            fill_color=DEEP, fill_opacity=1,
        )
        inner = self.notice(compact=True).scale(0.72 if not compact else 0.54).move_to(shell)
        title = self.badge("COMMUNICATION PACKET", COPPER, 2.9, 0.48).scale(0.82).next_to(shell, UP, buff=-0.08)
        return VGroup(shell, inner, title)

    def recipient(self, language: str, color: str = EVIDENCE) -> VGroup:
        shell = Circle(radius=0.55, stroke_color=color, stroke_width=3.5, fill_color=SURFACE, fill_opacity=1)
        head = Circle(radius=0.11, stroke_color=color, fill_color=color, fill_opacity=1).shift(UP * 0.14)
        shoulders = Line(LEFT * 0.23, RIGHT * 0.23, color=color, stroke_width=4).shift(DOWN * 0.17)
        label = self.label(language, 13, color, "BOLD").next_to(shell, DOWN, buff=0.1)
        return VGroup(shell, head, shoulders, label)

    def building(self) -> VGroup:
        body = RoundedRectangle(width=2.1, height=1.45, corner_radius=0.12, stroke_color=ACCENT, stroke_width=4, fill_color=DEEP, fill_opacity=1)
        roof = Polygon(LEFT * 1.2 + UP * 0.65, UP * 1.45, RIGHT * 1.2 + UP * 0.65, color=ACCENT, fill_color=DEEP, fill_opacity=1, stroke_width=4)
        door = Rectangle(width=0.43, height=0.65, stroke_color=ACCENT, stroke_width=3).shift(DOWN * 0.4)
        cross = VGroup(Line(LEFT * 0.26, RIGHT * 0.26, color=EVIDENCE, stroke_width=5), Line(DOWN * 0.26, UP * 0.26, color=EVIDENCE, stroke_width=5)).shift(UP * 0.24)
        tag = self.badge("RIVERSIDE", ACCENT, 1.65, 0.4).scale(0.82).next_to(body, DOWN, buff=0.08)
        return VGroup(body, roof, door, cross, tag)

    def clock(self, value: str, color: str = AUTHORITY) -> VGroup:
        face = Circle(radius=0.67, stroke_color=color, stroke_width=4, fill_color=SURFACE, fill_opacity=1)
        hands = VGroup(
            Line(face.get_center(), face.get_center() + UP * 0.43, color=color, stroke_width=5),
            Line(face.get_center(), face.get_center() + RIGHT * 0.32 + DOWN * 0.16, color=color, stroke_width=5),
        )
        value_text = self.label(value, 17, color, "BOLD").next_to(face, DOWN, buff=0.12)
        return VGroup(face, hands, value_text)

    def construct(self) -> None:
        # 1 — a true sentence inside a changing influence field
        notice1 = self.notice()
        forces1 = self.grid(
            ["FRAMING", "TARGETING", "IDENTITY", "REPETITION", "REACH"],
            [AUTHORITY, RESIDUAL, VIOLET, ROLLBACK, ACCENT], 5, 1.7,
        ).scale(0.83).shift(DOWN * 2.15)
        paths1 = VGroup(*[
            ArcBetweenPoints(notice1.get_left() + DOWN * 0.08 * i, notice1.get_right() + UP * 0.08 * i, angle=(-0.45 + 0.22 * i), color=[AUTHORITY, RESIDUAL, VIOLET, ROLLBACK, ACCENT][i], stroke_width=3)
            for i in range(5)
        ])
        title1 = self.badge("TRUE SENTENCE · CHANGING EPISODE", COPPER, 4.2, 0.65).shift(UP * 2.45)
        scene1 = VGroup(notice1, forces1, paths1, title1)
        self.next_section("b01")
        self.play(Write(notice1[1]), Create(notice1[0]), run_time=3.0)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.3) for f in forces1], lag_ratio=0.12), run_time=2.5)
        self.play(LaggedStart(*[Create(p) for p in paths1], lag_ratio=0.12), run_time=2.7)
        self.play(FadeIn(title1, shift=DOWN * 0.3), Indicate(notice1, color=ACCENT, scale_factor=1.03), run_time=1.7)
        self.wait_until(self.ENDS[0])

        # 2 — ground the Riverside public-service case
        building2 = self.building().shift(LEFT * 4.5 + DOWN * 0.2)
        notice2 = self.notice(compact=True).shift(LEFT * 0.8 + UP * 0.85)
        clock2 = self.clock("8 PM").shift(RIGHT * 2.4 + UP * 0.6)
        recipients2 = VGroup(self.recipient("NORTH"), self.recipient("SOUTH")).arrange(DOWN, buff=0.65).shift(RIGHT * 5.0)
        heat2 = self.badge("EXTREME HEAT", AUTHORITY, 2.3).shift(LEFT * 0.8 + DOWN * 1.2)
        route2 = Arrow(notice2.get_right(), recipients2.get_left(), color=ACCENT, stroke_width=5, buff=0.15)
        token2 = Dot(route2.get_start(), radius=0.14, color=ACCENT)
        scene2 = VGroup(building2, notice2, clock2, recipients2, heat2, route2, token2)
        self.play_beat(2, FadeOut(scene1, shift=LEFT * 0.6), FadeIn(building2), FadeIn(notice2), FadeIn(clock2), FadeIn(heat2), FadeIn(recipients2), GrowArrow(route2), FadeIn(token2), MoveAlongPath(token2, route2), settle=0.55)

        # 3 — viewer prediction among four fact-identical routes
        source3 = self.notice(compact=True).scale(0.8).shift(LEFT * 5.0)
        route_names3 = ["NEUTRAL", "URGENT", "SYNTHETIC VOICE", "PERSONAL + REPEAT"]
        route_colors3 = [ACCENT, AUTHORITY, VIOLET, RESIDUAL]
        choices3 = self.grid(route_names3, route_colors3, 1, 2.7).shift(RIGHT * 3.9)
        routes3 = VGroup(*[Arrow(source3.get_right(), c.get_left(), color=route_colors3[i], buff=0.1, stroke_width=5 if i < 2 else 3) for i, c in enumerate(choices3)])
        copies3 = VGroup(*[Dot(r.get_start(), radius=0.13, color=route_colors3[i]) for i, r in enumerate(routes3)])
        question3 = self.badge("WHICH VERSION?", COPPER, 2.8, 0.7).shift(UP * 2.65)
        keep3 = self.badge("KEEP YOUR ANSWER", MUTED, 2.7).shift(DOWN * 2.6)
        scene3 = VGroup(source3, choices3, routes3, copies3, question3, keep3)
        self.next_section("b03")
        self.play(FadeOut(scene2, shift=LEFT * 0.6), FadeIn(source3), FadeIn(question3), run_time=2.0)
        self.play(LaggedStart(*[GrowArrow(r) for r in routes3], lag_ratio=0.12), run_time=2.2)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.35) for c in choices3], lag_ratio=0.15), FadeIn(copies3), run_time=2.1)
        self.play(AnimationGroup(*[MoveAlongPath(copies3[i], routes3[i]) for i in range(4)], lag_ratio=0.08), run_time=2.5)
        self.play(FadeIn(keep3, shift=UP * 0.25), run_time=1.0)
        self.wait_until(self.ENDS[2])

        # 4 — fact identity above divergent episode profiles
        columns4 = VGroup()
        for i, name in enumerate(route_names3):
            fact = self.badge("SAME FACT", INK, 2.35, 0.48)
            name_badge = self.badge(name, route_colors3[i], 2.35, 0.5)
            profile = self.grid(
                [f"PRESS {i + 1}", f"AUTH {1 + (i % 3)}", f"FIT {4 - i}", "EXIT" if i < 2 else "EXIT?"],
                [route_colors3[i]] * 4, 1, 1.55,
            ).scale(0.68)
            columns4.add(VGroup(fact, name_badge, profile).arrange(DOWN, buff=0.18))
        columns4.arrange(RIGHT, buff=0.28).scale(0.84)
        split4 = self.badge("TRUTH ≠ COMPLETE EPISODE", COPPER, 3.5).shift(DOWN * 2.72)
        scene4 = VGroup(columns4, split4)
        self.play_beat(4, FadeOut(scene3), LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in columns4], lag_ratio=0.12), LaggedStart(*[Indicate(c[0], color=INK, scale_factor=1.04) for c in columns4], lag_ratio=0.12), LaggedStart(*[Indicate(c[2], color=route_colors3[i], scale_factor=1.03) for i, c in enumerate(columns4)], lag_ratio=0.12), FadeIn(split4), settle=0.6)

        # 5 — the governed object is an open episode lifecycle
        notice5 = self.notice(compact=True).scale(0.72)
        lifecycle_names5 = ["EVIDENCE", "COMPOSE", "DELIVER", "EXPOSE", "RESPOND", "DESCENDANTS", "CORRECT"]
        lifecycle5 = VGroup()
        edges5 = VGroup()
        for i, value in enumerate(lifecycle_names5):
            angle = PI * 0.95 - i * PI * 1.55 / 6
            pos = 3.15 * (RIGHT * cos(angle) + UP * sin(angle))
            lifecycle5.add(self.badge(value, [EVIDENCE, ACCENT, AUTHORITY, RESIDUAL, VIOLET, ROLLBACK, COPPER][i], 1.75, 0.48).move_to(pos))
        for i in range(len(lifecycle5) - 1):
            edges5.add(Arrow(lifecycle5[i].get_center(), lifecycle5[i + 1].get_center(), color=BOUNDARY, buff=0.6, stroke_width=3))
        open5 = self.badge("EPISODE REMAINS OPEN", RESIDUAL, 3.0).shift(DOWN * 2.6)
        scene5 = VGroup(notice5, lifecycle5, edges5, open5)
        self.play_beat(5, FadeOut(scene4), FadeIn(notice5), LaggedStart(*[FadeIn(n) for n in lifecycle5], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges5], lag_ratio=0.1), FadeIn(open5), Indicate(lifecycle5[-1], color=COPPER), settle=0.7)

        # 6 — versioned communication packet
        packet6 = self.packet()
        field_names6 = ["CLAIM", "PURPOSE", "AUDIENCE", "LANGUAGE", "TECHNIQUE", "CHANNEL", "IDENTITY", "SPONSOR", "AMPLIFY", "EXPIRY", "CORRECT"]
        fields6 = self.grid(field_names6, [COPPER] * 11, 6, 1.55).scale(0.75).shift(DOWN * 2.5)
        source6 = self.badge("SOURCE EVIDENCE", EVIDENCE, 2.5).shift(LEFT * 5.0 + UP * 2.0)
        lineage6 = DashedLine(source6.get_right(), packet6.get_left(), color=EVIDENCE, stroke_width=3)
        version6 = self.badge("VERSIONED · EXPIRING", COPPER, 2.8).shift(RIGHT * 4.7 + UP * 2.0)
        scene6 = VGroup(packet6, fields6, source6, lineage6, version6)
        self.next_section("b06")
        self.play(FadeOut(scene5, shift=LEFT * 0.5), FadeIn(source6), Create(lineage6), run_time=2.0)
        self.play(ReplacementTransform(notice5.copy(), packet6), run_time=2.2)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fields6], lag_ratio=0.06), run_time=4.2)
        self.play(FadeIn(version6, shift=LEFT * 0.3), Indicate(packet6, color=COPPER, scale_factor=1.03), run_time=2.0)
        self.wait_until(self.ENDS[5])

        # 7 — no single score
        packet7 = self.packet(compact=True).scale(0.72).shift(LEFT * 4.7)
        dimensions7 = self.grid(["TRUTH", "USEFUL", "COMPREHEND", "AUTONOMY", "PERMISSION", "REACH"], [EVIDENCE, ACCENT, AUTHORITY, COPPER, VIOLET, RESIDUAL], 2, 2.0).shift(RIGHT * 0.2)
        funnel7 = Polygon(LEFT * 1.0 + UP * 0.8, RIGHT * 1.0 + UP * 0.8, RIGHT * 0.3 + DOWN * 0.8, LEFT * 0.3 + DOWN * 0.8, color=MUTED, fill_color=SURFACE, fill_opacity=1).shift(RIGHT * 4.8)
        score7 = self.badge("ONE SCORE", MUTED, 1.8).next_to(funnel7, DOWN, buff=0.12)
        cross7 = Cross(VGroup(funnel7, score7), stroke_color=ROLLBACK, stroke_width=5)
        scene7 = VGroup(packet7, dimensions7, funnel7, score7, cross7)
        self.play_beat(7, FadeOut(scene6), FadeIn(packet7), LaggedStart(*[GrowFromCenter(d) for d in dimensions7], lag_ratio=0.08), FadeIn(funnel7), FadeIn(score7), Create(cross7), settle=0.6)

        # 8 — claim ceiling
        supported8 = self.panel("SOURCE CEILING", EVIDENCE, 5.0, 4.2).shift(LEFT * 3.4)
        facts8 = self.grid(["RIVERSIDE", "OPEN UNTIL 8"], [EVIDENCE, EVIDENCE], 1, 3.2).move_to(supported8)
        rule8 = VGroup(Line(UP * 2.6, DOWN * 2.6, color=BOUNDARY, stroke_width=6), Line(UP * 2.6, DOWN * 2.6, color=BOUNDARY, stroke_width=2).shift(RIGHT * 0.22))
        overclaims8 = self.grid(["THE SAFEST", "YOUR ONLY CHOICE", "WE KNOW YOU'RE IN DANGER"], [ROLLBACK] * 3, 1, 3.4).shift(RIGHT * 3.5)
        arrows8 = VGroup(*[Arrow(o.get_left(), rule8.get_center(), color=ROLLBACK, buff=0.15) for o in overclaims8])
        crosses8 = VGroup(*[Cross(o, stroke_color=ROLLBACK, stroke_width=4) for o in overclaims8])
        scene8 = VGroup(supported8, facts8, rule8, overclaims8, arrows8, crosses8)
        self.play_beat(8, FadeOut(scene7), FadeIn(supported8), FadeIn(facts8), Create(rule8), FadeIn(overclaims8), Create(arrows8), LaggedStart(*[Create(c) for c in crosses8], lag_ratio=0.12), settle=0.75)

        # 9 — declared purpose and visible influence
        packet9 = self.packet(compact=True).scale(0.72).shift(LEFT * 5.0)
        warn9 = self.badge("WARN", AUTHORITY, 1.8, 0.7).shift(LEFT * 1.4 + UP * 0.9)
        assist9 = self.badge("ASSIST", EVIDENCE, 1.8, 0.7).shift(LEFT * 1.4 + DOWN * 0.9)
        recipient9 = self.recipient("RECIPIENT").shift(RIGHT * 4.8)
        influence9 = Arrow(RIGHT * 0.1, recipient9.get_left(), color=ACCENT, stroke_width=5, buff=0.12)
        visible9 = self.badge("INFLUENCE · DECLARED", ACCENT, 2.8).shift(UP * 2.35 + RIGHT * 1.8)
        false9 = self.grid(["≠ INVISIBLE", "≠ AUTOMATICALLY WRONG"], [ROLLBACK, ROLLBACK], 2, 2.6).shift(DOWN * 2.35 + RIGHT * 1.4)
        scene9 = VGroup(packet9, warn9, assist9, recipient9, influence9, visible9, false9)
        self.play_beat(9, FadeOut(scene8), FadeIn(packet9), FadeIn(warn9), FadeIn(assist9), GrowArrow(influence9), FadeIn(recipient9), FadeIn(visible9), LaggedStart(*[FadeIn(x) for x in false9], lag_ratio=0.15), settle=0.65)

        # 10 — declared denominator and unknown reposts
        neighborhood10 = self.grid(["NORTH · 10,000", "SOUTH · 10,000"], [ACCENT, ACCENT], 2, 3.0).shift(LEFT * 1.9 + UP * 1.4)
        languages10 = self.grid(["EN", "ES", "EN", "ES"], [EVIDENCE, EVIDENCE, EVIDENCE, EVIDENCE], 4, 1.2).shift(LEFT * 1.9)
        count10 = self.badge("20,000 ELIGIBLE", AUTHORITY, 2.7, 0.75).shift(LEFT * 1.9 + DOWN * 1.4)
        boundary10 = Line(UP * 2.7, DOWN * 2.7, color=BOUNDARY, stroke_width=5).shift(RIGHT * 1.0)
        reposts10 = self.grid(["REPOST ?", "SCREENSHOT ?", "SUMMARY ?"], [RESIDUAL] * 3, 1, 2.3).shift(RIGHT * 4.2)
        dotted10 = VGroup(*[DashedLine(boundary10.get_center(), r.get_left(), color=RESIDUAL, stroke_width=3) for r in reposts10])
        controlled10 = self.badge("CONTROLLED LIST", COPPER, 2.3).next_to(boundary10, UP, buff=0.05)
        scene10 = VGroup(neighborhood10, languages10, count10, boundary10, reposts10, dotted10, controlled10)
        self.play_beat(10, FadeOut(scene9), FadeIn(neighborhood10), FadeIn(count10), LaggedStart(*[FadeIn(x) for x in languages10], lag_ratio=0.1), Create(boundary10), FadeIn(controlled10), Create(dotted10), LaggedStart(*[FadeIn(r) for r in reposts10], lag_ratio=0.15), settle=0.7)

        # 11 — inherited capacity narrows technique, never targets the person
        receipt11 = self.badge("CAPACITY + VULNERABILITY", COPPER, 3.2, 0.75).shift(LEFT * 4.5)
        narrow11 = self.badge("NARROW TECHNIQUE", EVIDENCE, 2.8, 0.75).shift(RIGHT * 3.5 + UP * 1.35)
        denied11 = self.grid(["SCORE PERSON", "TARGET PERSON"], [ROLLBACK, ROLLBACK], 1, 2.7).shift(RIGHT * 3.5 + DOWN * 1.25)
        allowed11 = Arrow(receipt11.get_right(), narrow11.get_left(), color=EVIDENCE, stroke_width=5, buff=0.1)
        denied_routes11 = VGroup(*[Arrow(receipt11.get_right(), d.get_left(), color=ROLLBACK, buff=0.1) for d in denied11])
        crosses11 = VGroup(*[Cross(d, stroke_color=ROLLBACK, stroke_width=4) for d in denied11])
        scene11 = VGroup(receipt11, narrow11, denied11, allowed11, denied_routes11, crosses11)
        self.play_beat(11, FadeOut(scene10), FadeIn(receipt11), GrowArrow(allowed11), FadeIn(narrow11), Create(denied_routes11), FadeIn(denied11), Create(crosses11), settle=0.65)

        # 12 — allowed usability routing versus inferred vulnerability
        gate12 = VGroup(Line(LEFT * 5.7, RIGHT * 5.7, color=COPPER, stroke_width=6), self.badge("PURPOSE-LIMITED TARGETING GATE", COPPER, 3.7).shift(UP * 0.55))
        allowed12 = self.grid(["LOCATION", "REQUESTED LANGUAGE"], [EVIDENCE, EVIDENCE], 2, 2.5).shift(LEFT * 3.0 + UP * 1.8)
        destination12 = self.badge("USABLE NOTICE", EVIDENCE, 2.5, 0.75).shift(RIGHT * 4.6 + UP * 1.8)
        allowed_paths12 = VGroup(*[Arrow(a.get_right(), destination12.get_left(), color=EVIDENCE, buff=0.1) for a in allowed12])
        denied12 = self.grid(["ILLNESS?", "DISTRESS?", "DEBT?", "DEPENDENCE?", "SUSCEPTIBILITY?"], [ROLLBACK] * 5, 5, 2.0).scale(0.8).shift(DOWN * 1.65)
        blocks12 = VGroup(*[Cross(d, stroke_color=ROLLBACK, stroke_width=4) for d in denied12])
        scene12 = VGroup(gate12, allowed12, destination12, allowed_paths12, denied12, blocks12)
        self.play_beat(12, FadeOut(scene11), FadeIn(gate12), FadeIn(allowed12), Create(allowed_paths12), FadeIn(destination12), LaggedStart(*[FadeIn(d, shift=UP * 0.25) for d in denied12], lag_ratio=0.1), LaggedStart(*[Create(c) for c in blocks12], lag_ratio=0.1), settle=0.75)

        # 13 — proxies cannot launder denied purpose
        origin13 = self.badge("DENIED HEALTH USE", ROLLBACK, 2.8, 0.8).shift(LEFT * 5.0)
        proxies13 = self.grid(["EMBEDDING", "HISTORY", "PURCHASES", "CAMPAIGN TOOL"], [RESIDUAL] * 4, 1, 2.4).shift(LEFT * 0.5)
        common13 = self.badge("SAME PURPOSE · SAME DENIAL", ROLLBACK, 3.3, 0.8).shift(RIGHT * 4.4)
        bypasses13 = VGroup(*[ArcBetweenPoints(origin13.get_right(), p.get_left(), angle=(-0.65 + i * 0.4), color=RESIDUAL, stroke_width=4) for i, p in enumerate(proxies13)])
        endings13 = VGroup(*[Arrow(p.get_right(), common13.get_left(), color=ROLLBACK, buff=0.12) for p in proxies13])
        token13 = Dot(origin13.get_right(), radius=0.14, color=RESIDUAL)
        scene13 = VGroup(origin13, proxies13, common13, bypasses13, endings13, token13)
        self.play_beat(13, FadeOut(scene12), FadeIn(origin13), LaggedStart(*[Create(p) for p in bypasses13], lag_ratio=0.1), LaggedStart(*[FadeIn(p) for p in proxies13], lag_ratio=0.1), Create(endings13), FadeIn(common13), FadeIn(token13), MoveAlongPath(token13, bypasses13[0]), Indicate(common13, color=ROLLBACK), settle=0.7)

        # 14 — six technique levers remain separately governable
        values14 = ["CLEAR URGENCY", "FABRICATED SCARCITY", "FALSE AUTHORITY", "SOCIAL PRESSURE", "SIMULATED INTIMACY", "ENDLESS REPEAT"]
        levers14 = VGroup()
        knobs14 = VGroup()
        for i, value in enumerate(values14):
            y = 2.25 - i * 0.85
            line = Line(LEFT * 2.4, RIGHT * 2.4, color=BOUNDARY, stroke_width=5).shift(RIGHT * 1.2 + UP * y)
            label = self.badge(value, EVIDENCE if i == 0 else ROLLBACK, 3.2, 0.48).shift(LEFT * 4.5 + UP * y)
            knob = Dot(line.point_from_proportion(0.55 if i == 0 else 0.05), radius=0.16, color=EVIDENCE if i == 0 else ROLLBACK)
            levers14.add(VGroup(line, label)); knobs14.add(knob)
        inspect14 = self.badge("TECHNIQUE · EXPLICIT CHOICES", COPPER, 3.5).shift(UP * 2.75 + RIGHT * 1.2)
        scan14 = RoundedRectangle(
            width=5.5, height=0.68, corner_radius=0.12,
            stroke_color=AUTHORITY, stroke_width=3,
            fill_color=AUTHORITY, fill_opacity=0.08,
        ).move_to(levers14[0][0])
        scene14 = VGroup(levers14, knobs14, inspect14)
        self.next_section("b14")
        self.play(FadeOut(scene13), FadeIn(inspect14), run_time=1.8)
        self.play(LaggedStart(*[Create(l[0]) for l in levers14], lag_ratio=0.08), run_time=2.0)
        self.play(LaggedStart(*[FadeIn(l[1]) for l in levers14], lag_ratio=0.08), run_time=1.8)
        self.play(LaggedStart(*[GrowFromCenter(k) for k in knobs14], lag_ratio=0.08), run_time=1.4)
        self.add(scan14)
        self.play(
            scan14.animate.move_to(levers14[-1][0]),
            LaggedStart(*[Indicate(k, color=k.get_color(), scale_factor=1.18) for k in knobs14], lag_ratio=0.18),
            run_time=4.9,
        )
        self.play(FadeOut(scan14), Indicate(knobs14[0], color=EVIDENCE), run_time=0.7)
        self.wait_until(self.ENDS[13])

        # 15 — declared synthetic identity supports access but not impersonation
        waveform15 = VGroup(*[Line(UP * (0.25 + 0.12 * (i % 3)), DOWN * (0.25 + 0.12 * (i % 3)), color=VIOLET, stroke_width=5).shift(LEFT * 4.5 + RIGHT * i * 0.22) for i in range(13)])
        declared15 = self.badge("SYNTHETIC · DECLARED", VIOLET, 2.8).next_to(waveform15, DOWN, buff=0.25)
        access15 = self.badge("ACCESS", EVIDENCE, 2.0, 0.8).shift(LEFT * 0.2)
        access_path15 = Arrow(waveform15.get_right(), access15.get_left(), color=EVIDENCE, stroke_width=5, buff=0.1)
        masks15 = self.grid(["DOCTOR", "NEIGHBOR", "FAMILY", "INSTITUTION"], [ROLLBACK] * 4, 2, 2.2).shift(RIGHT * 4.0)
        crosses15 = VGroup(*[Cross(m, stroke_color=ROLLBACK, stroke_width=4) for m in masks15])
        scene15 = VGroup(waveform15, declared15, access15, access_path15, masks15, crosses15)
        self.play_beat(15, FadeOut(scene14), FadeIn(waveform15), FadeIn(declared15), GrowArrow(access_path15), FadeIn(access15), LaggedStart(*[FadeIn(m, shift=LEFT * 0.25) for m in masks15], lag_ratio=0.12), LaggedStart(*[Create(c) for c in crosses15], lag_ratio=0.12), Indicate(declared15, color=VIOLET), settle=0.75)

        # 16 — finite exposure budget
        rail16 = Line(LEFT * 4.8, RIGHT * 4.8, color=BOUNDARY, stroke_width=7).shift(UP * 0.4)
        slots16 = VGroup(*[RoundedRectangle(width=2.1, height=0.8, corner_radius=0.12, stroke_color=[ACCENT, ACCENT, AUTHORITY][i], stroke_width=4, fill_color=DEEP, fill_opacity=1).move_to(LEFT * 2.7 + RIGHT * i * 2.7 + UP * 0.4) for i in range(3)])
        labels16 = self.grid(["DELIVERY 1", "DELIVERY 2", "REMINDER"], [ACCENT, ACCENT, AUTHORITY], 3, 2.1).move_to(slots16)
        channels16 = self.grid(["SMS", "VOICE"], [ACCENT, VIOLET], 2, 1.8).shift(LEFT * 3.7 + UP * 1.8)
        revoke16 = self.badge("REVOCABLE", COPPER, 2.0).shift(RIGHT * 3.8 + UP * 1.8)
        no_amp16 = self.badge("NO UNDECLARED AMPLIFICATION", ROLLBACK, 3.7).shift(DOWN * 1.9)
        lock16 = Cross(no_amp16, stroke_color=ROLLBACK, stroke_width=4)
        scene16 = VGroup(rail16, slots16, labels16, channels16, revoke16, no_amp16, lock16)
        self.play_beat(16, FadeOut(scene15), Create(rail16), FadeIn(channels16), FadeIn(revoke16), LaggedStart(*[FadeIn(s, shift=UP * 0.25) for s in slots16], lag_ratio=0.15), LaggedStart(*[FadeIn(l) for l in labels16], lag_ratio=0.15), FadeIn(no_amp16), Create(lock16), settle=0.7)

        # 17 — factuality baseline versus episode packet
        source17 = self.notice(compact=True).scale(0.68).shift(LEFT * 5.1)
        fact_rail17 = Line(LEFT * 3.6 + UP * 1.25, RIGHT * 4.4 + UP * 1.25, color=EVIDENCE, stroke_width=6)
        packet_rail17 = Line(LEFT * 3.6 + DOWN * 1.25, RIGHT * 4.4 + DOWN * 1.25, color=COPPER, stroke_width=6)
        fact17 = self.badge("FACT CHECK", EVIDENCE, 2.0).shift(UP * 1.9)
        packet17 = self.grid(["PURPOSE", "SHAPING", "AUDIENCE", "REPEAT", "EXIT", "APPEAL"], [COPPER] * 6, 6, 1.55).scale(0.76).shift(DOWN * 2.0)
        tokens17 = VGroup(Dot(fact_rail17.get_start(), radius=0.15, color=EVIDENCE), Dot(packet_rail17.get_start(), radius=0.15, color=COPPER))
        release17 = self.badge("RELEASE", ACCENT, 1.8).shift(RIGHT * 5.3)
        scene17 = VGroup(source17, fact_rail17, packet_rail17, fact17, packet17, tokens17, release17)
        self.play_beat(17, FadeOut(scene16), FadeIn(source17), Create(fact_rail17), Create(packet_rail17), FadeIn(fact17), FadeIn(packet17), FadeIn(tokens17), AnimationGroup(MoveAlongPath(tokens17[0], fact_rail17), MoveAlongPath(tokens17[1], packet_rail17)), FadeIn(release17), settle=0.7)

        # 18 — bounded notice delivery
        bounded18 = self.packet().scale(0.82).shift(LEFT * 3.6)
        fields18 = self.grid(["CITY", "SOURCE", "CENTER", "TIME", "WHY URGENT", "ALTERNATIVE", "CORRECTION LINK"], [ACCENT, EVIDENCE, ACCENT, AUTHORITY, AUTHORITY, EVIDENCE, COPPER], 4, 1.8).scale(0.75).shift(LEFT * 3.6 + DOWN * 2.2)
        recipients18 = VGroup(self.recipient("EN"), self.recipient("ES")).arrange(DOWN, buff=0.7).shift(RIGHT * 4.6)
        route18 = Arrow(bounded18.get_right(), recipients18.get_left(), color=EVIDENCE, stroke_width=6, buff=0.15)
        token18 = Dot(route18.get_start(), radius=0.17, color=ACCENT)
        spent18 = self.badge("BUDGET 1 / 3", AUTHORITY, 2.1).shift(RIGHT * 1.3 + DOWN * 2.35)
        scene18 = VGroup(bounded18, fields18, recipients18, route18, token18, spent18)
        self.play_beat(18, FadeOut(scene17), FadeIn(bounded18), LaggedStart(*[FadeIn(f) for f in fields18], lag_ratio=0.08), Create(route18), FadeIn(recipients18), FadeIn(token18), MoveAlongPath(token18, route18), FadeIn(spent18), settle=0.7)

        # 19 — recipient-centered outcome questions
        agreed19 = self.badge("AGREED", EVIDENCE, 2.1, 0.75).shift(LEFT * 5.0)
        outcomes19 = self.grid(["UNDERSTAND?", "CALIBRATE?", "CHOICE?", "USEFUL HELP?", "UNEQUAL BURDEN?", "FREE TO REFUSE?"], [ACCENT, AUTHORITY, COPPER, EVIDENCE, RESIDUAL, VIOLET], 2, 2.5).shift(RIGHT * 2.0)
        routes19 = VGroup(*[Arrow(agreed19.get_right(), o.get_left(), color=o[0].get_stroke_color(), buff=0.1) for o in outcomes19])
        open19 = self.badge("OUTCOMES OPEN", MUTED, 2.3).shift(DOWN * 2.65)
        scene19 = VGroup(agreed19, outcomes19, routes19, open19)
        self.play_beat(19, FadeOut(scene18), FadeIn(agreed19), Create(routes19), LaggedStart(*[FadeIn(o, shift=LEFT * 0.25) for o in outcomes19], lag_ratio=0.09), LaggedStart(*[Indicate(o, color=o[0].get_stroke_color(), scale_factor=1.04) for o in outcomes19], lag_ratio=0.08), FadeIn(open19), settle=0.8)

        # 20 — high action can coexist with harms
        bars20 = VGroup()
        values20 = ["HIGH ACTION", "CONFUSION", "PRESSURE", "EXCLUSION", "PRIVACY LOSS", "MISPLACED TRUST"]
        colors20 = [EVIDENCE, ROLLBACK, RESIDUAL, AUTHORITY, COPPER, VIOLET]
        heights20 = [4.6, 2.8, 3.7, 2.2, 3.0, 3.5]
        for i, value in enumerate(values20):
            bar = Rectangle(width=1.35, height=heights20[i], stroke_color=colors20[i], fill_color=colors20[i], fill_opacity=0.26, stroke_width=4)
            bar.align_to(DOWN * 2.15, DOWN).shift(LEFT * 4.25 + RIGHT * i * 1.7)
            label = self.label(value, 11, colors20[i], "BOLD").next_to(bar, DOWN, buff=0.1)
            bars20.add(VGroup(bar, label))
        objective20 = self.badge("MAXIMIZE ACTION", MUTED, 2.7).shift(UP * 2.65)
        cross20 = Cross(objective20, stroke_color=ROLLBACK, stroke_width=5)
        scene20 = VGroup(bars20, objective20, cross20)
        self.play_beat(20, FadeOut(scene19), FadeIn(objective20), GrowFromCenter(bars20[0]), LaggedStart(*[GrowFromCenter(b) for b in bars20[1:]], lag_ratio=0.12), Create(cross20), Indicate(VGroup(*bars20[1:]), color=ROLLBACK), settle=0.7)

        # 21 — translation preserves some tokens while relations drift
        en21 = self.panel("EN", ACCENT, 5.1, 4.3).shift(LEFT * 3.35)
        es21 = self.panel("ES", EVIDENCE, 5.1, 4.3).shift(RIGHT * 3.35)
        en_tokens21 = self.grid(["CENTER", "TIME", "CERTAINTY", "WARNING", "APPEAL"], [ACCENT, AUTHORITY, VIOLET, AUTHORITY, COPPER], 1, 2.4).move_to(en21)
        es_tokens21 = self.grid(["CENTER", "TIME", "CERTAINTY?", "WARNING?", "APPEAL?"], [ACCENT, AUTHORITY, RESIDUAL, RESIDUAL, RESIDUAL], 1, 2.4).move_to(es21)
        equal21 = VGroup(*[DashedLine(en_tokens21[i].get_right(), es_tokens21[i].get_left(), color=EVIDENCE if i < 2 else RESIDUAL, stroke_width=3) for i in range(5)])
        scene21 = VGroup(en21, es21, en_tokens21, es_tokens21, equal21)
        self.play_beat(21, FadeOut(scene20), FadeIn(en21), FadeIn(en_tokens21), FadeIn(es21), LaggedStart(*[TransformFromCopy(en_tokens21[i], es_tokens21[i]) for i in range(5)], lag_ratio=0.1), Create(equal21), LaggedStart(*[Indicate(es_tokens21[i], color=RESIDUAL) for i in range(2, 5)], lag_ratio=0.12), settle=0.75)

        # 22 — separate task-by-audience coverage cells
        admitted22 = self.grid(["EN · TEST CELL", "ES · TEST CELL"], [EVIDENCE, EVIDENCE], 2, 3.0).shift(UP * 1.65)
        missing22 = self.grid(["DIALECT · MISSING", "LITERACY · MISSING", "ACCESS · MISSING", "CULTURE · MISSING"], [RESIDUAL] * 4, 2, 3.0).shift(DOWN * 0.55)
        for item in missing22:
            item[0].set_stroke(opacity=0.55)
        matrix22 = self.panel("TASK × AUDIENCE COVERAGE", COPPER, 9.1, 5.6)
        scope22 = self.badge("NO SILENT TRANSFER", ROLLBACK, 2.8).shift(DOWN * 2.65)
        scene22 = VGroup(matrix22, admitted22, missing22, scope22)
        self.play_beat(22, FadeOut(scene21), FadeIn(matrix22), LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in admitted22], lag_ratio=0.15), LaggedStart(*[Create(m[0]) for m in missing22], lag_ratio=0.1), LaggedStart(*[FadeIn(m[1]) for m in missing22], lag_ratio=0.1), FadeIn(scope22), settle=0.8)

        # 23 — material world change expires every old copy
        building23 = self.building().shift(LEFT * 4.7)
        clock23 = self.clock("5:30").shift(LEFT * 1.7 + UP * 1.2)
        old23 = self.badge("OPEN UNTIL 8", ACCENT, 2.5, 0.75).shift(LEFT * 1.7 + DOWN * 1.2)
        new23 = self.badge("OPEN UNTIL 6", ROLLBACK, 2.5, 0.75).shift(RIGHT * 1.4 + DOWN * 1.2)
        power23 = self.badge("POWER LOSS", ROLLBACK, 2.3, 0.75).shift(RIGHT * 1.4 + UP * 1.2)
        copies23 = self.grid(["SMS", "VOICE", "FEED", "REPOST"], [ACCENT] * 4, 2, 1.8).shift(RIGHT * 4.8)
        expiry23 = VGroup(*[Cross(c, stroke_color=ROLLBACK, stroke_width=4) for c in copies23])
        scene23 = VGroup(building23, clock23, old23, new23, power23, copies23, expiry23)
        self.play_beat(23, FadeOut(scene22), FadeIn(building23), FadeIn(clock23), FadeIn(old23), FadeIn(copies23), FadeIn(power23), ReplacementTransform(old23.copy(), new23), LaggedStart(*[Create(x) for x in expiry23], lag_ratio=0.1), settle=0.65)

        # 24 — correction is a descendant graph
        root24 = self.badge("EXPIRED PACKET", ROLLBACK, 2.5, 0.75).shift(LEFT * 5.0)
        branch_names24 = ["SMS", "VOICE", "CITY FEED", "PARTNER", "SCREENSHOT", "SUMMARY"]
        branches24 = self.grid(branch_names24, [ACCENT, VIOLET, COPPER, AUTHORITY, RESIDUAL, MUTED], 2, 2.1).shift(RIGHT * 2.8)
        edges24 = VGroup(*[Arrow(root24.get_right(), b.get_left(), color=b[0].get_stroke_color(), buff=0.1, stroke_width=3) for b in branches24])
        descendants24 = VGroup(*[Dot(b.get_right() + RIGHT * 0.45, radius=0.11, color=b[0].get_stroke_color()) for b in branches24])
        graph24 = self.badge("CORRECTION GRAPH", COPPER, 2.7).shift(UP * 2.65)
        scene24 = VGroup(root24, branches24, edges24, descendants24, graph24)
        self.play_beat(24, FadeOut(scene23), FadeIn(root24), FadeIn(graph24), LaggedStart(*[GrowArrow(e) for e in edges24], lag_ratio=0.08), LaggedStart(*[FadeIn(b, shift=LEFT * 0.25) for b in branches24], lag_ratio=0.08), LaggedStart(*[GrowFromCenter(d) for d in descendants24], lag_ratio=0.08), settle=0.7)

        # 25 — source retraction is not recipient repair
        root25 = self.badge("SOURCE · CORRECTED", EVIDENCE, 2.7, 0.75).shift(LEFT * 4.7 + UP * 1.35)
        exposed25 = self.grid(["EXPOSED", "EXPOSED", "EXPOSED", "EXPOSED", "EXPOSED", "EXPOSED"], [ROLLBACK] * 6, 3, 1.65).shift(LEFT * 0.5)
        fraction25 = VGroup(self.label("CORRECTED", 20, EVIDENCE, "BOLD"), Line(LEFT * 1.2, RIGHT * 1.2, color=BOUNDARY, stroke_width=4), self.label("EXPOSED", 20, ROLLBACK, "BOLD")).arrange(DOWN, buff=0.12).shift(RIGHT * 4.4 + UP * 1.3)
        debt25 = self.panel("CORRECTION DEBT", RESIDUAL, 3.2, 1.45).shift(RIGHT * 4.4 + DOWN * 1.4)
        debt_nodes25 = VGroup(*[Dot(radius=0.13, color=RESIDUAL) for _ in range(4)]).arrange(RIGHT, buff=0.3).move_to(debt25)
        not_repair25 = self.badge("RETRACTION ≠ REPAIR", ROLLBACK, 3.0).shift(LEFT * 4.4 + DOWN * 1.4)
        scene25 = VGroup(root25, exposed25, fraction25, debt25, debt_nodes25, not_repair25)
        self.play_beat(25, FadeOut(scene24), FadeIn(root25), FadeIn(exposed25), Indicate(root25, color=EVIDENCE), FadeIn(fraction25), FadeIn(debt25), LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in debt_nodes25], lag_ratio=0.15), FadeIn(not_repair25), settle=0.8)

        # 26 — effect-aware repair traverses the original channels
        root26 = self.badge("CORRECTION · 6 PM", EVIDENCE, 2.8, 0.75).shift(LEFT * 5.0)
        channels26 = self.grid(["SMS", "VOICE", "CITY FEED", "PARTNER"], [ACCENT, VIOLET, COPPER, AUTHORITY], 2, 2.1).shift(LEFT * 0.7)
        edges26 = VGroup(*[Arrow(root26.get_right(), c.get_left(), color=EVIDENCE, buff=0.1, stroke_width=4) for c in channels26])
        repairs26 = self.grid(["ALT CENTER", "APPEAL", "OWNER", "RESIDUAL"], [EVIDENCE, COPPER, AUTHORITY, RESIDUAL], 2, 2.2).shift(RIGHT * 4.1)
        pause26 = self.badge("AMPLIFICATION PAUSED", ROLLBACK, 3.1).shift(UP * 2.55)
        scene26 = VGroup(root26, channels26, edges26, repairs26, pause26)
        self.play_beat(26, FadeOut(scene25), FadeIn(pause26), FadeIn(root26), LaggedStart(*[GrowArrow(e) for e in edges26], lag_ratio=0.1), LaggedStart(*[FadeIn(c) for c in channels26], lag_ratio=0.1), LaggedStart(*[FadeIn(r, shift=LEFT * 0.25) for r in repairs26], lag_ratio=0.12), Indicate(repairs26[-1], color=RESIDUAL), settle=0.7)

        # 27 — ten independent outcome dimensions, no aggregate
        hub27 = self.badge("EPISODE RECEIPT", COPPER, 2.5, 0.75)
        values27 = ["CALIBRATE", "COMPREHEND", "AUTONOMY", "USEFUL", "UNEQUAL", "PRIVACY", "COMPLAINTS", "CORRECT REACH", "LATENCY", "DEBT"]
        colors27 = [AUTHORITY, ACCENT, COPPER, EVIDENCE, RESIDUAL, VIOLET, ROLLBACK, EVIDENCE, ACCENT, RESIDUAL]
        spokes27 = VGroup(); labels27 = VGroup(); sockets27 = VGroup()
        for i, value in enumerate(values27):
            angle = 2 * PI * i / len(values27) + PI / 2
            endpoint = 3.0 * (RIGHT * cos(angle) + UP * sin(angle))
            spokes27.add(Line(hub27.get_center(), endpoint, color=colors27[i], stroke_width=3))
            labels27.add(self.badge(value, colors27[i], 1.7, 0.42).move_to(endpoint))
            sockets27.add(Circle(radius=0.12, stroke_color=colors27[i], stroke_width=2).move_to(endpoint * 0.72))
        no_score27 = self.badge("NO FLATTENING SCORE", ROLLBACK, 3.0).shift(DOWN * 2.8)
        cross27 = Cross(no_score27, stroke_color=ROLLBACK, stroke_width=4)
        scan27 = RoundedRectangle(
            width=2.0, height=5.5, corner_radius=0.18,
            stroke_color=AUTHORITY, stroke_width=3,
            fill_color=AUTHORITY, fill_opacity=0.07,
        ).shift(LEFT * 4.6)
        scene27 = VGroup(hub27, spokes27, labels27, sockets27, no_score27, cross27)
        self.next_section("b27")
        self.play(FadeOut(scene26), FadeIn(hub27), run_time=1.8)
        self.play(LaggedStart(*[Create(s) for s in spokes27], lag_ratio=0.06), run_time=2.0)
        self.play(LaggedStart(*[FadeIn(l) for l in labels27], lag_ratio=0.06), run_time=1.8)
        self.play(LaggedStart(*[Create(s) for s in sockets27], lag_ratio=0.06), run_time=1.3)
        self.add(scan27)
        self.play(
            scan27.animate.shift(RIGHT * 9.2),
            LaggedStart(*[Indicate(label, color=colors27[i], scale_factor=1.05) for i, label in enumerate(labels27)], lag_ratio=0.08),
            run_time=3.8,
        )
        self.play(FadeOut(scan27), FadeIn(no_score27), Create(cross27), run_time=1.0)
        self.wait_until(self.ENDS[26])

        # 28 — argument support does not validate the design
        sources28 = self.panel("SOURCES · BOUNDED FINDINGS", EVIDENCE, 4.0, 2.3).shift(LEFT * 4.0)
        rationale28 = self.panel("ARGUMENT · DESIGN RATIONALE", COPPER, 4.0, 2.3)
        idea28 = DashedLine(sources28.get_right(), rationale28.get_left(), color=COPPER, stroke_width=4)
        rule28 = VGroup(Line(UP * 2.6, DOWN * 2.6, color=BOUNDARY, stroke_width=6), Line(UP * 2.6, DOWN * 2.6, color=BOUNDARY, stroke_width=2).shift(RIGHT * 0.22)).shift(RIGHT * 2.4)
        claims28 = self.grid(["≠ PACKET VALIDATED", "≠ POLICY VALIDATED", "≠ EPISODE VALIDATED"], [ROLLBACK] * 3, 1, 2.8).scale(0.88).shift(RIGHT * 4.8)
        scene28 = VGroup(sources28, rationale28, idea28, rule28, claims28)
        self.play_beat(28, FadeOut(scene27), FadeIn(sources28), Create(idea28), FadeIn(rationale28), Create(rule28), LaggedStart(*[FadeIn(c, shift=LEFT * 0.25) for c in claims28], lag_ratio=0.12), settle=0.9)

        # 29 — nonclaims and planned-test obligations
        nonclaims29 = self.grid(["≠ COMPREHENSION", "≠ AUTONOMY", "≠ CORRECTION EFFICACY", "≠ MANIPULATION PREVENTION", "≠ MULTILINGUAL TRANSFER", "≠ DEPLOYMENT SAFETY", "≠ READINESS"], [ROLLBACK] * 7, 2, 2.45).scale(0.82).shift(LEFT * 3.3)
        proof_rule29 = VGroup(Line(UP * 2.7, DOWN * 2.7, color=BOUNDARY, stroke_width=6), Line(UP * 2.7, DOWN * 2.7, color=BOUNDARY, stroke_width=2).shift(RIGHT * 0.22)).shift(RIGHT * 0.55)
        obligations29 = self.panel("PLANNED · OBLIGATIONS", COPPER, 4.3, 4.8).shift(RIGHT * 3.8)
        tests29 = self.grid(["COMPREHENSION", "AUTONOMY", "CORRECTION", "TRANSFER"], [MUTED] * 4, 1, 2.4).move_to(obligations29)
        empty29 = VGroup(*[Circle(radius=0.12, stroke_color=MUTED, stroke_width=2).next_to(t, RIGHT, buff=0.12) for t in tests29])
        scene29 = VGroup(nonclaims29, proof_rule29, obligations29, tests29, empty29)
        self.play_beat(29, FadeOut(scene28), LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in nonclaims29], lag_ratio=0.07), Create(proof_rule29), FadeIn(obligations29), LaggedStart(*[FadeIn(t) for t in tests29], lag_ratio=0.1), LaggedStart(*[Create(e) for e in empty29], lag_ratio=0.1), Indicate(obligations29, color=COPPER), settle=0.95)

        # 30 — return to the opening choice and select bounded communication
        source30 = self.notice(compact=True).scale(0.68).shift(LEFT * 5.2)
        route_names30 = ["NEUTRAL", "URGENT", "SYNTHETIC", "PERSONAL + REPEAT"]
        route_colors30 = [ACCENT, AUTHORITY, VIOLET, RESIDUAL]
        choices30 = self.grid(route_names30, route_colors30, 1, 2.3).scale(0.84).shift(LEFT * 1.8)
        selected30 = self.panel("BOUNDED ROUTE", EVIDENCE, 5.5, 4.9).shift(RIGHT * 3.0)
        controls30 = self.grid(["TRANSPARENT", "USEFUL URGENCY", "ALLOWED PERSONAL", "LIMITED REPEAT", "ALTERNATIVE", "EXPIRY", "CORRECTION"], [ACCENT, AUTHORITY, EVIDENCE, COPPER, EVIDENCE, ROLLBACK, COPPER], 2, 2.25).scale(0.8).move_to(selected30)
        route30 = Arrow(source30.get_right(), selected30.get_left(), color=EVIDENCE, stroke_width=6, buff=0.12)
        token30 = Dot(route30.get_start(), radius=0.16, color=ACCENT)
        not_max30 = self.badge("NOT MAX COMPLIANCE", ROLLBACK, 2.8).shift(DOWN * 2.7 + LEFT * 1.5)
        scene30 = VGroup(source30, choices30, selected30, controls30, route30, token30, not_max30)
        self.next_section("b30")
        self.play(FadeOut(scene29, shift=LEFT * 0.6), FadeIn(source30), FadeIn(choices30), run_time=2.5)
        self.play(FadeIn(selected30), LaggedStart(*[FadeIn(c) for c in controls30], lag_ratio=0.08), run_time=3.5)
        self.play(Create(route30), FadeIn(token30), run_time=1.5)
        self.play(MoveAlongPath(token30, route30), run_time=3.0)
        self.play(FadeIn(not_max30), Indicate(selected30, color=EVIDENCE, scale_factor=1.03), run_time=1.8)
        self.wait_until(self.ENDS[29])

        # 31 — constitutional alignment inherits the binding ceilings
        resolved31 = VGroup(source30.copy(), selected30.copy(), controls30.copy()).scale(0.53).shift(LEFT * 4.4)
        inherited31 = self.grid(["DENIED METHODS", "PROTECTED INTERESTS", "APPEAL", "AUTONOMY DEBT"], [ROLLBACK, AUTHORITY, COPPER, RESIDUAL], 1, 2.8).shift(LEFT * 0.2)
        seal31 = Circle(radius=1.75, stroke_color=COPPER, stroke_width=6, fill_color=DEEP, fill_opacity=1).shift(RIGHT * 4.2)
        seal_label31 = VGroup(self.label("CONSTITUTIONAL", 18, COPPER, "BOLD"), self.label("ALIGNMENT", 22, INK, "BOLD")).arrange(DOWN, buff=0.1).move_to(seal31)
        bridge31 = Arrow(resolved31.get_right(), inherited31.get_left(), color=COPPER, stroke_width=5, buff=0.1)
        self_edit31 = Arrow(RIGHT * 2.0 + DOWN * 2.3, seal31.get_bottom(), color=ROLLBACK, stroke_width=5, buff=0.12)
        stop31 = Cross(self_edit31, stroke_color=ROLLBACK, stroke_width=5)
        ceiling31 = self.badge("SELF-EDIT STOPS HERE", ROLLBACK, 2.9).shift(RIGHT * 3.9 + DOWN * 2.55)
        scene31 = VGroup(resolved31, inherited31, seal31, seal_label31, bridge31, self_edit31, stop31, ceiling31)
        self.next_section("b31")
        self.play(FadeOut(scene30, shift=LEFT * 0.7), FadeIn(resolved31, shift=RIGHT * 0.6), run_time=2.2)
        self.play(Create(bridge31), LaggedStart(*[TransformFromCopy(resolved31, item) for item in inherited31], lag_ratio=0.1), run_time=3.8)
        self.play(Create(seal31), FadeIn(seal_label31), run_time=2.0)
        self.play(TransformFromCopy(inherited31, seal31), run_time=2.0)
        self.play(GrowArrow(self_edit31), Create(stop31), FadeIn(ceiling31), run_time=2.1)
        self.wait_until(self.ENDS[30])

        self.wait_until(self.TARGET_DURATION)
