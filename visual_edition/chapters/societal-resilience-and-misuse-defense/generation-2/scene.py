"""Generation-2 visual abstract for societal resilience and misuse defense.

The fictional Harborline exercise keeps resist, absorb, recover, adapt,
federated incident identity, harmed-party routes, false-positive correction,
and residual custody visibly distinct.  It is a design-rationale derivative,
not an operational abuse recipe or evidence of population resilience.
"""

from __future__ import annotations

from manim import (
    Arrow, Create, Cross, DashedLine, FadeIn, FadeOut, GrowArrow, Indicate,
    LaggedStart, LEFT, Line, ORIGIN, RoundedRectangle, RIGHT, Text, UP, DOWN,
    VGroup,
)

from visual_edition.lib.asi_visuals import (
    BOUNDARY, INK, MUTED, RESIDUAL, SURFACE, AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class SocietalResilienceGeneration2(AsiScene):
    TARGET_DURATION = 411.515
    ENDS = [
        13.055, 27.035, 39.890, 54.445, 67.150, 78.530, 92.810, 106.090,
        118.570, 132.975, 146.730, 161.985, 176.965, 192.070, 207.625,
        221.155, 233.785, 247.240, 260.895, 275.050, 291.755, 306.560,
        322.640, 335.370, 349.450, 363.480, 379.735, 394.090, 411.515,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.6) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.08, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.08, remaining - min(settle, remaining * 0.14))
            per_animation = max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 17, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.2, height: float = 0.48) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.11,
            stroke_color=color, stroke_width=2.8,
            fill_color=SURFACE, fill_opacity=1,
        )
        caption = self.label(value, 13, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.8, height: float = 1.55) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=color, stroke_width=3.2,
            fill_color=DEEP, fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.22, 3.8), 0.42).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def frame(self, title: str, color: str = GOLD) -> VGroup:
        shell = RoundedRectangle(
            width=11.7, height=6.2, corner_radius=0.2,
            stroke_color=BOUNDARY, stroke_width=2,
            fill_color="#0F2029", fill_opacity=1,
        )
        heading = self.badge(title, color, 4.65, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def list_badges(
        self, names: list[str], colors: list[str], *, x: float = 0.0,
        y: float = 0.0, width: float = 2.3, scale: float = 1.0,
    ) -> VGroup:
        rows = VGroup(*[
            self.badge(name, colors[i % len(colors)], width)
            for i, name in enumerate(names)
        ])
        rows.arrange(DOWN, buff=0.15).scale(scale).shift(RIGHT * x + UP * y)
        return rows

    def construct(self) -> None:
        # 1 — one ticket is not societal safety
        f1 = self.frame("ONE TICKET ≠ SOCIETAL SAFETY", RED)
        provider1 = self.panel("PROVIDER", BLUE, 2.4, 1.5).shift(LEFT * 3.7)
        ticket1 = self.badge("TICKET CLOSED", GREEN, 2.2).shift(LEFT * 0.7 + UP * 0.7)
        harm1 = self.panel("HARM CONTINUES", RED, 2.7, 1.5).shift(RIGHT * 2.8 + DOWN * 0.1)
        outside1 = self.list_badges(["COPIES", "ACCOUNTS", "TRUST"], [RED, VIOLET, GOLD], x=2.8, y=-1.65, width=1.8, scale=0.7)
        e1 = VGroup(Arrow(provider1.get_right(), ticket1.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(ticket1.get_right(), harm1.get_left(), color=RED, stroke_width=3, buff=0.1))
        cross1 = Cross(ticket1, stroke_color=RED, stroke_width=3)
        s1 = VGroup(f1, provider1, ticket1, harm1, outside1, e1, cross1)
        self.play_beat(1, FadeIn(s1), GrowArrow(e1[0]), GrowArrow(e1[1]), Create(cross1), LaggedStart(*[FadeIn(x) for x in outside1], lag_ratio=0.1), settle=0.9)

        # 2 — four-stage contract
        f2 = self.frame("RESIST · ABSORB · RECOVER · ADAPT", GOLD)
        stages2 = self.list_badges(["RESIST", "ABSORB", "RECOVER", "ADAPT"], [GOLD, BLUE, GREEN, VIOLET], x=-2.1, y=0.2, width=2.2, scale=0.75)
        loop2 = VGroup(*[Arrow(stages2[i].get_right(), stages2[i + 1].get_left(), color=[GOLD, BLUE, GREEN][i], stroke_width=3, buff=0.1) for i in range(3)], Arrow(stages2[3].get_left(), stages2[0].get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        rights2 = self.badge("PEOPLE · SERVICES · RIGHTS", RED, 3.2).shift(RIGHT * 3.3 + DOWN * 1.1)
        s2 = VGroup(f2, stages2, loop2, rights2)
        self.play_beat(2, FadeOut(s1), FadeIn(f2), LaggedStart(*[FadeIn(x) for x in stages2], lag_ratio=0.1), LaggedStart(*[GrowArrow(x) for x in loop2[:3]], lag_ratio=0.1), Create(loop2[3]), FadeIn(rights2), settle=0.9)

        # 3 — shortcut surfaces
        f3 = self.frame("ONE CONTROL POINT HAS BLIND SPOTS", RED)
        classifier3 = self.panel("CLASSIFIER", BLUE, 2.3, 1.4).shift(LEFT * 3.6 + UP * 0.8)
        takedown3 = self.panel("TAKEDOWN", RED, 2.3, 1.4).shift(LEFT * 0.3 + UP * 0.8)
        playbook3 = self.panel("COMPANY PLAYBOOK", GOLD, 2.7, 1.4).shift(RIGHT * 3.1 + UP * 0.8)
        surfaces3 = self.list_badges(["PRIVATE CHANNEL", "OTHER PLATFORM", "HARMED PERSON"], [MUTED, RED, VIOLET], x=0.0, y=-1.0, width=2.5, scale=0.68)
        edges3 = VGroup(Arrow(classifier3.get_bottom(), surfaces3.get_top(), color=BLUE, stroke_width=2, buff=0.1), Arrow(takedown3.get_bottom(), surfaces3.get_top(), color=RED, stroke_width=2, buff=0.1), Arrow(playbook3.get_bottom(), surfaces3.get_top(), color=GOLD, stroke_width=2, buff=0.1))
        cross3 = Cross(playbook3, stroke_color=RED, stroke_width=3)
        s3 = VGroup(f3, classifier3, takedown3, playbook3, surfaces3, edges3, cross3)
        self.play_beat(3, FadeOut(s2), FadeIn(f3), FadeIn(classifier3), FadeIn(takedown3), FadeIn(playbook3), Create(cross3), LaggedStart(*[FadeIn(x) for x in surfaces3], lag_ratio=0.1), LaggedStart(*[GrowArrow(x) for x in edges3], lag_ratio=0.1), settle=0.9)

        # 4 — synthetic Harborline case
        f4 = self.frame("HARBORLINE · SYNTHETIC EXERCISE", GOLD)
        portal4 = self.panel("REAL SERVICE", BLUE, 2.7, 1.7).shift(LEFT * 3.6)
        false4 = self.panel("FALSE INSTRUCTION", RED, 2.7, 1.7).shift(RIGHT * 0.1)
        fixture4 = self.badge("SYNTHETIC ONLY · NO VICTIMS", VIOLET, 3.3).shift(RIGHT * 3.2 + DOWN * 1.2)
        e4 = Arrow(portal4.get_right(), false4.get_left(), color=RED, stroke_width=3, buff=0.1)
        cross4 = Cross(false4, stroke_color=RED, stroke_width=3)
        s4 = VGroup(f4, portal4, false4, fixture4, e4, cross4)
        self.play_beat(4, FadeOut(s3), FadeIn(f4), FadeIn(portal4), GrowArrow(e4), FadeIn(false4), Create(cross4), FadeIn(fixture4), settle=0.9)

        # 5 — resistance stack
        f5 = self.frame("RESIST · MAKE HARM HARDER", GOLD)
        threat5 = self.panel("THREAT", RED, 2.3, 1.5).shift(LEFT * 3.8)
        controls5 = self.list_badges(["ACCESS", "FRICTION", "PROVENANCE", "EDUCATION", "REVIEW"], [BLUE, GOLD, GREEN, VIOLET, RED], x=0.1, y=0.2, width=2.0, scale=0.67)
        access5 = self.badge("LEGITIMATE ACCESS", GREEN, 2.8).shift(RIGHT * 3.3 + DOWN * 1.4)
        e5 = VGroup(*[Arrow(threat5.get_right(), c.get_left(), color=GOLD, stroke_width=2, buff=0.1) for c in controls5], Arrow(controls5.get_right(), access5.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        s5 = VGroup(f5, threat5, controls5, access5, e5)
        self.play_beat(5, FadeOut(s4), FadeIn(f5), FadeIn(threat5), LaggedStart(*[FadeIn(x) for x in controls5], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e5], lag_ratio=0.08), FadeIn(access5), settle=0.9)

        # 6 — resistance boundary
        f6 = self.frame("EVERY CONTROL NAMES ITS BURDEN", BLUE)
        control6 = self.panel("CONTROL", GOLD, 2.4, 1.6).shift(LEFT * 3.6)
        fields6 = self.list_badges(["THREAT", "POPULATION", "LANGUAGE", "CHANNEL", "THRESHOLD", "EXPIRY"], [RED, VIOLET, BLUE, GOLD, GREEN, MUTED], x=1.0, y=0.15, width=1.8, scale=0.58)
        burden6 = self.badge("LEGITIMATE USERS · BURDEN", RED, 3.3).shift(RIGHT * 3.3 + DOWN * 1.6)
        e6 = VGroup(*[Arrow(control6.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in fields6], Arrow(fields6.get_right(), burden6.get_left(), color=RED, stroke_width=2, buff=0.1))
        s6 = VGroup(f6, control6, fields6, burden6, e6)
        self.play_beat(6, FadeOut(s5), FadeIn(f6), FadeIn(control6), LaggedStart(*[FadeIn(x) for x in fields6], lag_ratio=0.07), LaggedStart(*[GrowArrow(x) for x in e6], lag_ratio=0.06), FadeIn(burden6), settle=0.9)

        # 7 — absorb continuity
        f7 = self.frame("ABSORB · KEEP THE SERVICE AVAILABLE", BLUE)
        service7 = self.panel("HARBORLINE", BLUE, 2.7, 1.6).shift(LEFT * 3.6)
        continuity7 = self.list_badges(["MANUAL FALLBACK", "TRUSTED CONTACT", "SEGREGATED OPS", "HUMAN SURGE"], [GREEN, BLUE, VIOLET, GOLD], x=0.3, y=0.1, width=2.4, scale=0.63)
        state7 = self.badge("CONTINUITY · NOT UPTIME ONLY", GREEN, 3.4).shift(RIGHT * 3.2 + DOWN * 1.6)
        e7 = VGroup(*[Arrow(service7.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in continuity7], Arrow(continuity7.get_right(), state7.get_left(), color=GREEN, stroke_width=2, buff=0.1))
        s7 = VGroup(f7, service7, continuity7, state7, e7)
        self.play_beat(7, FadeOut(s6), FadeIn(f7), FadeIn(service7), LaggedStart(*[FadeIn(x) for x in continuity7], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e7], lag_ratio=0.08), FadeIn(state7), settle=0.9)

        # 8 — recovery paths
        f8 = self.frame("RECOVER · REMOVAL IS ONE FIELD", GREEN)
        incident8 = self.panel("INCIDENT", RED, 2.4, 1.5).shift(LEFT * 3.8)
        paths8 = self.list_badges(["CONTAIN", "PRESERVE", "NOTIFY", "CORRECT", "RESTORE", "REMEDY"], [RED, BLUE, GOLD, VIOLET, GREEN, RESIDUAL], x=0.0, y=0.2, width=1.9, scale=0.6)
        closure8 = self.badge("TERMINAL PATHS MATCH STATE", GOLD, 3.3).shift(RIGHT * 3.3 + DOWN * 1.65)
        e8 = VGroup(*[Arrow(incident8.get_right(), x.get_left(), color=GREEN, stroke_width=2, buff=0.1) for x in paths8], Arrow(paths8.get_right(), closure8.get_left(), color=GOLD, stroke_width=2, buff=0.1))
        s8 = VGroup(f8, incident8, paths8, closure8, e8)
        self.play_beat(8, FadeOut(s7), FadeIn(f8), FadeIn(incident8), LaggedStart(*[FadeIn(x) for x in paths8], lag_ratio=0.07), LaggedStart(*[GrowArrow(x) for x in e8], lag_ratio=0.06), FadeIn(closure8), settle=0.9)

        # 9 — adapt safely
        f9 = self.frame("ADAPT · CHANGE THE DEFENSE", VIOLET)
        failure9 = self.panel("FAILURE / NEAR MISS", RED, 2.8, 1.5).shift(LEFT * 3.6)
        updates9 = self.list_badges(["PATCH", "AGREEMENT", "EDUCATION", "EXERCISE", "SAFE LESSON"], [BLUE, GOLD, GREEN, VIOLET, MUTED], x=0.3, y=0.2, width=2.1, scale=0.64)
        new9 = self.badge("NEW FIELD BEHAVIOR", GREEN, 2.8).shift(RIGHT * 3.4 + DOWN * 1.5)
        e9 = VGroup(*[Arrow(failure9.get_right(), x.get_left(), color=VIOLET, stroke_width=2, buff=0.1) for x in updates9], Arrow(updates9.get_right(), new9.get_left(), color=GREEN, stroke_width=2, buff=0.1))
        s9 = VGroup(f9, failure9, updates9, new9, e9)
        self.play_beat(9, FadeOut(s8), FadeIn(f9), FadeIn(failure9), LaggedStart(*[FadeIn(x) for x in updates9], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e9], lag_ratio=0.07), FadeIn(new9), settle=0.9)

        # 10 — overlapping stages and residual owner
        f10 = self.frame("FOUR STAGES OVERLAP", GOLD)
        stages10 = self.list_badges(["RESIST", "ABSORB", "RECOVER", "ADAPT"], [GOLD, BLUE, GREEN, VIOLET], x=-2.7, y=0.25, width=2.0, scale=0.67)
        cycle10 = VGroup(*[Arrow(stages10[i].get_right(), stages10[i + 1].get_left(), color=[GOLD, BLUE, GREEN][i], stroke_width=2, buff=0.1) for i in range(3)])
        reopen10 = self.badge("NEW EXPOSURE → REOPEN", RED, 2.8).shift(RIGHT * 2.5 + UP * 0.8)
        owner10 = self.badge("RESIDUAL OWNER", RESIDUAL, 2.5).shift(RIGHT * 2.5 + DOWN * 1.0)
        e10 = VGroup(Arrow(stages10[2].get_right(), reopen10.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(reopen10.get_bottom(), owner10.get_top(), color=RESIDUAL, stroke_width=3, buff=0.1))
        s10 = VGroup(f10, stages10, cycle10, reopen10, owner10, e10)
        self.play_beat(10, FadeOut(s9), FadeIn(f10), LaggedStart(*[FadeIn(x) for x in stages10], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in cycle10], lag_ratio=0.1), FadeIn(reopen10), GrowArrow(e10[0]), FadeIn(owner10), GrowArrow(e10[1]), settle=0.9)

        # 11 — minimal federated envelope
        f11 = self.frame("FEDERATED INCIDENT ENVELOPE", BLUE)
        id11 = self.panel("SHARED ID", BLUE, 2.4, 1.6).shift(LEFT * 3.6)
        fields11 = self.list_badges(["DOMAIN", "SEVERITY", "FUNCTION", "CONFIDENCE", "PURPOSE", "RECIPIENTS", "EXPIRY"], [GOLD, RED, GREEN, VIOLET, BLUE, MUTED, RESIDUAL], x=0.4, y=0.2, width=1.8, scale=0.55)
        packet11 = self.badge("MINIMUM ROUTING FACTS", GOLD, 3.0).shift(RIGHT * 3.2 + DOWN * 1.6)
        e11 = VGroup(*[Arrow(id11.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in fields11], Arrow(fields11.get_right(), packet11.get_left(), color=GOLD, stroke_width=2, buff=0.1))
        s11 = VGroup(f11, id11, fields11, packet11, e11)
        self.play_beat(11, FadeOut(s10), FadeIn(f11), FadeIn(id11), LaggedStart(*[FadeIn(x) for x in fields11], lag_ratio=0.06), LaggedStart(*[GrowArrow(x) for x in e11], lag_ratio=0.05), FadeIn(packet11), settle=0.9)

        # 12 — local evidence custody
        f12 = self.frame("SHARED ID ≠ UNIVERSAL DATABASE", RED)
        shared12 = self.panel("SHARED PACKET", BLUE, 2.6, 1.6).shift(LEFT * 3.5)
        raw12 = self.panel("LOCAL CUSTODY", GOLD, 2.6, 1.6).shift(RIGHT * 2.3)
        rawfields12 = self.list_badges(["VICTIM MATERIAL", "CREDENTIALS", "SENSITIVE DEFENSE"], [RED, RED, VIOLET], x=2.4, y=-1.15, width=2.4, scale=0.6)
        route12 = Arrow(shared12.get_right(), raw12.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        gate12 = self.badge("SPECIFIC LAWFUL PURPOSE", GREEN, 3.0).shift(LEFT * 0.3 + UP * 1.1)
        s12 = VGroup(f12, shared12, raw12, rawfields12, route12, gate12)
        self.play_beat(12, FadeOut(s11), FadeIn(f12), FadeIn(shared12), FadeIn(raw12), Create(route12), FadeIn(gate12), LaggedStart(*[FadeIn(x) for x in rawfields12], lag_ratio=0.1), settle=0.9)

        # 13 — participants and authority
        f13 = self.frame("AUTHORITY AND CONTACT ARE FIELDS", GOLD)
        roles13 = self.list_badges(["PROVIDER", "PLATFORM", "INFRASTRUCTURE", "PUBLIC AGENCY", "CIVIL SOCIETY", "ADVOCATE"], [BLUE, GOLD, VIOLET, GREEN, MUTED, RED], x=-2.1, y=0.2, width=2.2, scale=0.58)
        packet13 = self.panel("INCIDENT PACKET", BLUE, 2.5, 1.5).shift(RIGHT * 2.7)
        no13 = self.badge("NO ASSUMED POWER", RED, 2.5).shift(RIGHT * 2.8 + DOWN * 1.6)
        edges13 = VGroup(*[Arrow(r.get_right(), packet13.get_left(), color=BLUE, stroke_width=2, buff=0.1) for r in roles13])
        cross13 = Cross(no13, stroke_color=RED, stroke_width=3)
        s13 = VGroup(f13, roles13, packet13, no13, edges13, cross13)
        self.play_beat(13, FadeOut(s12), FadeIn(f13), LaggedStart(*[FadeIn(x) for x in roles13], lag_ratio=0.06), LaggedStart(*[GrowArrow(x) for x in edges13], lag_ratio=0.06), FadeIn(packet13), FadeIn(no13), Create(cross13), settle=0.9)

        # 14 — coverage graph
        f14 = self.frame("MAP THE COVERAGE GRAPH", BLUE)
        harm14 = self.panel("HARM PATH", RED, 2.3, 1.5).shift(LEFT * 4.0)
        surfaces14 = self.list_badges(["SURFACE", "SIGNAL", "RESPONDER", "HARMED-PARTY ROUTE"], [BLUE, GOLD, GREEN, VIOLET], x=-0.8, y=0.2, width=2.2, scale=0.63)
        gap14 = self.badge("EMPTY EDGE · RESIDUAL", RESIDUAL, 2.8).shift(RIGHT * 3.1 + DOWN * 1.5)
        edges14 = VGroup(*[Arrow(harm14.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in surfaces14], DashedLine(surfaces14.get_right(), gap14.get_left(), color=RESIDUAL, stroke_width=3))
        s14 = VGroup(f14, harm14, surfaces14, gap14, edges14)
        self.play_beat(14, FadeOut(s13), FadeIn(f14), FadeIn(harm14), LaggedStart(*[FadeIn(x) for x in surfaces14], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in edges14[:-1]], lag_ratio=0.07), Create(edges14[-1]), FadeIn(gap14), settle=0.9)

        # 15 — correlated blindness
        f15 = self.frame("CORRELATED ALERTS ARE NOT INDEPENDENT", RED)
        detectors15 = self.list_badges(["DETECTOR A", "DETECTOR B", "DETECTOR C"], [BLUE, BLUE, BLUE], x=-3.3, y=0.4, width=2.1, scale=0.72)
        common15 = self.panel("SAME DATA · MODEL · LANGUAGE", GOLD, 3.0, 1.4).shift(LEFT * 0.1)
        alert15 = self.badge("CORRELATED EVIDENCE", RED, 2.8).shift(RIGHT * 3.2 + UP * 0.8)
        migrate15 = self.badge("OTHER CHANNEL", MUTED, 2.4).shift(RIGHT * 3.2 + DOWN * 1.0)
        e15 = VGroup(*[Arrow(d.get_right(), common15.get_left(), color=BLUE, stroke_width=2, buff=0.1) for d in detectors15], Arrow(common15.get_right(), alert15.get_left(), color=RED, stroke_width=3, buff=0.1), DashedLine(common15.get_bottom(), migrate15.get_top(), color=MUTED, stroke_width=3))
        cross15 = Cross(alert15, stroke_color=RED, stroke_width=3)
        s15 = VGroup(f15, detectors15, common15, alert15, migrate15, e15, cross15)
        self.play_beat(15, FadeOut(s14), FadeIn(f15), LaggedStart(*[FadeIn(x) for x in detectors15], lag_ratio=0.1), FadeIn(common15), LaggedStart(*[GrowArrow(x) for x in e15[:3]], lag_ratio=0.08), GrowArrow(e15[3]), Create(e15[4]), FadeIn(alert15), Create(cross15), FadeIn(migrate15), settle=0.9)

        # 16 — dispute and correction
        f16 = self.frame("DISPUTE STATE STAYS VISIBLE", VIOLET)
        report16 = self.panel("REPORT", BLUE, 2.3, 1.5).shift(LEFT * 3.8)
        route16 = self.badge("ROUTE · NOT YET FACT", GOLD, 2.6).shift(LEFT * 0.9 + UP * 0.8)
        false16 = self.panel("FALSE INTERVENTION", RED, 2.7, 1.5).shift(RIGHT * 2.5 + UP * 0.7)
        repair16 = self.list_badges(["APPEAL", "CORRECT", "REMOVE RESIDUE"], [VIOLET, GREEN, RESIDUAL], x=2.4, y=-1.1, width=2.2, scale=0.67)
        e16 = VGroup(Arrow(report16.get_right(), route16.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(route16.get_right(), false16.get_left(), color=RED, stroke_width=3, buff=0.1), *[Arrow(false16.get_bottom(), x.get_top(), color=GREEN, stroke_width=2, buff=0.1) for x in repair16])
        cross16 = Cross(false16, stroke_color=RED, stroke_width=3)
        s16 = VGroup(f16, report16, route16, false16, repair16, e16, cross16)
        self.play_beat(16, FadeOut(s15), FadeIn(f16), FadeIn(report16), GrowArrow(e16[0]), FadeIn(route16), GrowArrow(e16[1]), FadeIn(false16), Create(cross16), LaggedStart(*[FadeIn(x) for x in repair16], lag_ratio=0.1), LaggedStart(*[GrowArrow(x) for x in e16[2:]], lag_ratio=0.08), settle=0.9)

        # 17 — measurement bundle
        f17 = self.frame("MEASURE THE WHOLE RESPONSE", GREEN)
        stages17 = self.list_badges(["DETECT", "CONTAIN", "NOTIFY", "RESTORE", "CORRECT", "ADAPT"], [BLUE, RED, GOLD, GREEN, VIOLET, MUTED], x=-2.4, y=0.2, width=1.8, scale=0.59)
        outcomes17 = self.list_badges(["AVOIDED HARM", "REPAIRED HARM", "FALSE INTERVENTION", "COVERAGE", "ACCESSIBILITY", "TOTAL BURDEN"], [GREEN, VIOLET, RED, BLUE, GOLD, RESIDUAL], x=2.1, y=0.2, width=2.2, scale=0.56)
        e17 = VGroup(*[Arrow(stages17[i].get_right(), outcomes17[i].get_left(), color=GREEN, stroke_width=2, buff=0.1) for i in range(6)])
        s17 = VGroup(f17, stages17, outcomes17, e17)
        self.play_beat(17, FadeOut(s16), FadeIn(f17), LaggedStart(*[FadeIn(x) for x in stages17], lag_ratio=0.06), LaggedStart(*[FadeIn(x) for x in outcomes17], lag_ratio=0.06), LaggedStart(*[GrowArrow(x) for x in e17], lag_ratio=0.06), settle=0.9)

        # 18 — three reports become one incident identity
        f18 = self.frame("HARBORLINE · THREE REPORTS, ONE EVENT", GOLD)
        platform18 = self.panel("PLATFORM", BLUE, 2.3, 1.4).shift(LEFT * 3.8 + UP * 0.8)
        agency18 = self.panel("AGENCY", GOLD, 2.3, 1.4).shift(LEFT * 3.8 + DOWN * 0.9)
        community18 = self.panel("COMMUNITY", VIOLET, 2.3, 1.4).shift(LEFT * 0.5)
        event18 = self.panel("SHARED INCIDENT", GREEN, 2.7, 1.5).shift(RIGHT * 2.6)
        edges18 = VGroup(Arrow(platform18.get_right(), event18.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(agency18.get_right(), event18.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(community18.get_right(), event18.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        s18 = VGroup(f18, platform18, agency18, community18, event18, edges18)
        self.play_beat(18, FadeOut(s17), FadeIn(f18), FadeIn(platform18), FadeIn(agency18), FadeIn(community18), LaggedStart(*[GrowArrow(x) for x in edges18], lag_ratio=0.1), FadeIn(event18), settle=0.9)

        # 19 — partial resistance observes a new edge
        f19 = self.frame("PARTIAL SUCCESS · NEW EDGE OBSERVED", RED)
        controls19 = self.list_badges(["PROVENANCE", "FRICTION"], [BLUE, GOLD], x=-3.2, y=0.5, width=2.0, scale=0.72)
        slowed19 = self.badge("FALSE PATH SLOWED", GREEN, 2.5).shift(LEFT * 0.5 + UP * 0.8)
        copy19 = self.panel("COPIED IMAGE", RED, 2.5, 1.4).shift(RIGHT * 2.8 + UP * 0.8)
        edge19 = self.badge("NEW COVERAGE EDGE", RESIDUAL, 2.7).shift(RIGHT * 2.5 + DOWN * 1.3)
        e19 = VGroup(Arrow(controls19.get_right(), slowed19.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(slowed19.get_right(), copy19.get_left(), color=RED, stroke_width=3, buff=0.1), DashedLine(copy19.get_bottom(), edge19.get_top(), color=RESIDUAL, stroke_width=3))
        cross19 = Cross(slowed19, stroke_color=RED, stroke_width=3)
        s19 = VGroup(f19, controls19, slowed19, copy19, edge19, e19, cross19)
        self.play_beat(19, FadeOut(s18), FadeIn(f19), LaggedStart(*[FadeIn(x) for x in controls19], lag_ratio=0.1), FadeIn(slowed19), Create(cross19), GrowArrow(e19[0]), FadeIn(copy19), GrowArrow(e19[1]), Create(e19[2]), FadeIn(edge19), settle=0.9)

        # 20 — absorb the incident
        f20 = self.frame("ABSORB · TRUSTED SERVICE CONTINUES", BLUE)
        service20 = self.panel("REAL BENEFITS SERVICE", BLUE, 2.8, 1.5).shift(LEFT * 3.7)
        verified20 = self.badge("VERIFIED CHANNEL", GREEN, 2.5).shift(LEFT * 0.5 + UP * 0.9)
        hold20 = self.badge("RISKY CHANGE · HOLD", GOLD, 2.4).shift(LEFT * 0.5 + DOWN * 0.5)
        notice20 = self.badge("ACCESSIBLE STATUS NOTICE", VIOLET, 2.9).shift(RIGHT * 3.0 + DOWN * 1.1)
        e20 = VGroup(Arrow(service20.get_right(), verified20.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(service20.get_right(), hold20.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(verified20.get_right(), notice20.get_left(), color=VIOLET, stroke_width=2, buff=0.1))
        s20 = VGroup(f20, service20, verified20, hold20, notice20, e20)
        self.play_beat(20, FadeOut(s19), FadeIn(f20), FadeIn(service20), GrowArrow(e20[0]), FadeIn(verified20), GrowArrow(e20[1]), FadeIn(hold20), GrowArrow(e20[2]), FadeIn(notice20), settle=0.9)

        # 21 — affected path inventory
        f21 = self.frame("RECOVERY STARTS WITH THE AFFECTED PATHS", GREEN)
        incident21 = self.panel("INCIDENT", RED, 2.3, 1.5).shift(LEFT * 3.8)
        paths21 = self.list_badges(["PEOPLE", "ACCOUNTS", "TRANSACTIONS", "COPIES", "SEARCH", "DEVICES", "SERVICES", "PARTNERS"], [VIOLET, BLUE, GOLD, RED, MUTED, GREEN, BLUE, GOLD], x=0.1, y=0.3, width=1.8, scale=0.52)
        states21 = self.list_badges(["CONTAINED", "RESTORED", "CORRECTED", "NOTIFIED", "DISPUTED", "UNREACHABLE", "RESIDUAL"], [GREEN, GREEN, BLUE, GOLD, VIOLET, MUTED, RESIDUAL], x=3.0, y=0.2, width=1.7, scale=0.52)
        e21 = VGroup(*[Arrow(incident21.get_right(), x.get_left(), color=GREEN, stroke_width=2, buff=0.1) for x in paths21], *[Arrow(paths21.get_right(), x.get_left(), color=VIOLET, stroke_width=2, buff=0.1) for x in states21])
        s21 = VGroup(f21, incident21, paths21, states21, e21)
        self.play_beat(21, FadeOut(s20), FadeIn(f21), FadeIn(incident21), LaggedStart(*[FadeIn(x) for x in paths21], lag_ratio=0.05), LaggedStart(*[FadeIn(x) for x in states21], lag_ratio=0.05), LaggedStart(*[GrowArrow(x) for x in e21], lag_ratio=0.04), settle=0.9)

        # 22 — false-positive and language coverage
        f22 = self.frame("FALSE POSITIVE · UNEQUAL COVERAGE", RED)
        worker22 = self.panel("LEGITIMATE WORKER", GREEN, 2.7, 1.5).shift(LEFT * 3.6)
        warning22 = self.badge("AUTOMATED WARNING", RED, 2.5).shift(LEFT * 0.5 + UP * 0.8)
        appeal22 = self.list_badges(["LANGUAGE PATH", "APPEAL", "BURDEN LOWERED"], [BLUE, VIOLET, GREEN], x=2.2, y=0.3, width=2.3, scale=0.65)
        coverage22 = self.badge("UNEQUAL COVERAGE RECORDED", GOLD, 3.2).shift(RIGHT * 2.3 + DOWN * 1.5)
        e22 = VGroup(Arrow(worker22.get_right(), warning22.get_left(), color=RED, stroke_width=3, buff=0.1), *[Arrow(warning22.get_right(), x.get_left(), color=GREEN, stroke_width=2, buff=0.1) for x in appeal22], Arrow(appeal22.get_right(), coverage22.get_left(), color=GOLD, stroke_width=2, buff=0.1))
        cross22 = Cross(warning22, stroke_color=RED, stroke_width=3)
        s22 = VGroup(f22, worker22, warning22, appeal22, coverage22, e22, cross22)
        self.play_beat(22, FadeOut(s21), FadeIn(f22), FadeIn(worker22), FadeIn(warning22), Create(cross22), LaggedStart(*[FadeIn(x) for x in appeal22], lag_ratio=0.1), GrowArrow(e22[0]), LaggedStart(*[GrowArrow(x) for x in e22[1:]], lag_ratio=0.08), FadeIn(coverage22), settle=0.9)

        # 23 — minimized packet and correction propagation
        f23 = self.frame("MINIMIZE THE PACKET · PROPAGATE CORRECTION", BLUE)
        packet23 = self.panel("SHARED ID + ROUTE", BLUE, 2.7, 1.5).shift(LEFT * 3.6)
        local23 = self.panel("AGENCY CUSTODY", GOLD, 2.5, 1.5).shift(LEFT * 0.2)
        group23 = self.panel("COMMUNITY ROUTE", VIOLET, 2.5, 1.5).shift(RIGHT * 3.2)
        correction23 = self.badge("CORRECTION → ALL RECIPIENTS", GREEN, 3.4).shift(DOWN * 1.7)
        e23 = VGroup(Arrow(packet23.get_right(), local23.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(packet23.get_right(), group23.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(local23.get_bottom(), correction23.get_top(), color=GREEN, stroke_width=2, buff=0.1), Arrow(group23.get_bottom(), correction23.get_top(), color=GREEN, stroke_width=2, buff=0.1))
        s23 = VGroup(f23, packet23, local23, group23, correction23, e23)
        self.play_beat(23, FadeOut(s22), FadeIn(f23), FadeIn(packet23), GrowArrow(e23[0]), FadeIn(local23), GrowArrow(e23[1]), FadeIn(group23), GrowArrow(e23[2]), GrowArrow(e23[3]), FadeIn(correction23), settle=0.9)

        # 24 — jurisdictional handoff
        f24 = self.frame("HANDOFF · AUTHORITY STAYS TYPED", GOLD)
        platform24 = self.panel("PLATFORM", BLUE, 2.4, 1.5).shift(LEFT * 3.7)
        remove24 = self.badge("REMOVE COPY", GREEN, 2.2).shift(LEFT * 0.7 + UP * 0.9)
        agency24 = self.panel("AGENCY", GOLD, 2.4, 1.5).shift(RIGHT * 2.4 + UP * 0.8)
        correct24 = self.badge("CORRECT RECORD", VIOLET, 2.4).shift(RIGHT * 2.4 + DOWN * 0.4)
        remedy24 = self.badge("REMEDY OWNER · LOSS", RED, 2.8).shift(LEFT * 0.2 + DOWN * 1.7)
        e24 = VGroup(Arrow(platform24.get_right(), remove24.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(platform24.get_right(), agency24.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(agency24.get_bottom(), correct24.get_top(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(agency24.get_bottom(), remedy24.get_top(), color=RED, stroke_width=3, buff=0.1))
        s24 = VGroup(f24, platform24, remove24, agency24, correct24, remedy24, e24)
        self.play_beat(24, FadeOut(s23), FadeIn(f24), FadeIn(platform24), GrowArrow(e24[0]), FadeIn(remove24), GrowArrow(e24[1]), FadeIn(agency24), GrowArrow(e24[2]), FadeIn(correct24), GrowArrow(e24[3]), FadeIn(remedy24), settle=0.9)

        # 25 — after-action adaptation
        f25 = self.frame("ADAPTATION IS CHANGED FIELD BEHAVIOR", VIOLET)
        old25 = self.panel("OLD PLAYBOOK", MUTED, 2.5, 1.5).shift(LEFT * 3.7)
        changes25 = self.list_badges(["ROTATE DETECTOR", "TRUSTED LANGUAGE", "ESCALATION DEADLINE", "EXERCISE"], [BLUE, GREEN, GOLD, VIOLET], x=0.1, y=0.1, width=2.4, scale=0.64)
        new25 = self.panel("NEW BEHAVIOR", GREEN, 2.5, 1.5).shift(RIGHT * 3.3)
        e25 = VGroup(*[Arrow(old25.get_right(), x.get_left(), color=VIOLET, stroke_width=2, buff=0.1) for x in changes25], Arrow(changes25.get_right(), new25.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        s25 = VGroup(f25, old25, changes25, new25, e25)
        self.play_beat(25, FadeOut(s24), FadeIn(f25), FadeIn(old25), LaggedStart(*[FadeIn(x) for x in changes25], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e25], lag_ratio=0.07), FadeIn(new25), Indicate(new25, color=GREEN), settle=0.9)

        # 26 — residual custody
        f26 = self.frame("RESIDUALS STAY OWNED", RESIDUAL)
        residuals26 = self.list_badges(["UNREACHABLE COPY", "UNRESOLVED DISPUTE", "UNREPAIRABLE HARM"], [MUTED, VIOLET, RED], x=-2.8, y=0.4, width=2.5, scale=0.7)
        ledger26 = self.panel("RESIDUAL LEDGER", RESIDUAL, 2.7, 1.6).shift(RIGHT * 2.3)
        fields26 = self.list_badges(["CUSTODY", "NEXT TRIGGER", "EXPIRY", "NO CLOSURE CLAIM"], [GOLD, BLUE, GREEN, RED], x=2.5, y=-1.2, width=1.9, scale=0.6)
        e26 = VGroup(*[Arrow(r.get_right(), ledger26.get_left(), color=RESIDUAL, stroke_width=2, buff=0.1) for r in residuals26], *[Arrow(ledger26.get_bottom(), x.get_top(), color=GOLD, stroke_width=2, buff=0.1) for x in fields26])
        s26 = VGroup(f26, residuals26, ledger26, fields26, e26)
        self.play_beat(26, FadeOut(s25), FadeIn(f26), LaggedStart(*[FadeIn(x) for x in residuals26], lag_ratio=0.1), FadeIn(ledger26), LaggedStart(*[GrowArrow(x) for x in e26[:3]], lag_ratio=0.08), LaggedStart(*[FadeIn(x) for x in fields26], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e26[3:]], lag_ratio=0.07), settle=0.9)

        # 27 — finite tabletop ceiling
        f27 = self.frame("FINITE TABLETOP · EXPLICIT CEILING", BLUE)
        tests27 = self.list_badges(["PACKET", "PRIVACY", "ROLES", "PAUSE", "FALSE POSITIVE", "STAGES", "RESIDUAL"], [GREEN, BLUE, GOLD, RED, VIOLET, GREEN, RESIDUAL], x=-2.6, y=0.2, width=1.8, scale=0.55)
        accepts27 = VGroup(self.badge("ACCEPT", GREEN, 1.8), self.badge("REJECT", RED, 1.8)).arrange(RIGHT, buff=0.35).shift(DOWN * 1.8)
        limits27 = self.list_badges(["POPULATION RESILIENCE", "UNIVERSAL REMEDY", "SAFE SOCIETY"], [RED, RED, RED], x=2.4, y=0.2, width=2.3, scale=0.6)
        crosses27 = VGroup(*[Cross(x, stroke_color=RED, stroke_width=3) for x in limits27])
        e27 = VGroup(*[Arrow(x.get_right(), accepts27[0].get_left(), color=GREEN, stroke_width=2, buff=0.1) for x in tests27], *[Arrow(x.get_left(), accepts27[1].get_right(), color=RED, stroke_width=2, buff=0.1) for x in limits27])
        s27 = VGroup(f27, tests27, accepts27, limits27, crosses27, e27)
        self.play_beat(27, FadeOut(s26), FadeIn(f27), LaggedStart(*[FadeIn(x) for x in tests27], lag_ratio=0.06), LaggedStart(*[FadeIn(x) for x in limits27], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e27], lag_ratio=0.05), FadeIn(accepts27), LaggedStart(*[Create(x) for x in crosses27], lag_ratio=0.08), settle=0.9)

        # 28 — evidence boundary
        f28 = self.frame("RESPONSE ≠ ACCEPTABLE HARM REDUCTION", RED)
        response28 = self.panel("FAST RESPONSE", GREEN, 2.6, 1.6).shift(LEFT * 3.2)
        claims28 = self.list_badges(["TAKEDOWN = RECOVERY", "PROVIDER METRICS = SAFETY", "DESIGN = DEPLOYMENT EVIDENCE"], [RED, RED, RED], x=2.0, y=0.15, width=3.0, scale=0.62)
        boundary28 = Line(ORIGIN + UP * 2.25, ORIGIN + DOWN * 1.75, color=RED, stroke_width=4)
        crosses28 = VGroup(*[Cross(x, stroke_color=RED, stroke_width=3) for x in claims28])
        s28 = VGroup(f28, response28, claims28, boundary28, crosses28)
        self.play_beat(28, FadeOut(s27), FadeIn(f28), FadeIn(response28), Create(boundary28), LaggedStart(*[FadeIn(x) for x in claims28], lag_ratio=0.08), LaggedStart(*[Create(x) for x in crosses28], lag_ratio=0.08), Indicate(response28, color=GREEN), settle=0.9)

        # 29 — payoff and handoff
        f29 = self.frame("HARBORLINE · RESIDUALS REMAIN VISIBLE", GOLD)
        harbor29 = self.panel("HARBORLINE", GOLD, 2.6, 1.7).shift(LEFT * 3.4)
        outcomes29 = self.list_badges(["RESIST", "SERVICE AVAILABLE", "REPAIR", "LEARN", "OWNER", "NEXT: CAPABILITY FIELDS"], [GOLD, BLUE, GREEN, VIOLET, RESIDUAL, RED], x=1.2, y=0.2, width=2.6, scale=0.58)
        e29 = VGroup(*[Arrow(harbor29.get_right(), x.get_left(), color=[GOLD, BLUE, GREEN, VIOLET, RESIDUAL, RED][i], stroke_width=2, buff=0.1) for i, x in enumerate(outcomes29)])
        self.play_beat(29, FadeOut(s28), FadeIn(f29), FadeIn(harbor29), LaggedStart(*[FadeIn(x) for x in outcomes29], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e29], lag_ratio=0.07), Indicate(outcomes29[-1], color=RED), settle=1.0)

        self.wait_until(self.TARGET_DURATION)
