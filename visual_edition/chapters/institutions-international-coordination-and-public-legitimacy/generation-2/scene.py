"""Generation-2 visual abstract for institutional legitimacy and coordination.

The Northline corridor keeps jurisdiction, affected publics, evidence, verifier
independence, commitment, remedy, and legitimacy residuals visibly distinct.
The film is a design-rationale derivative and never turns a local packet into
legal, safety, legitimacy, or deployment proof.
"""

from __future__ import annotations

from manim import (
    Arrow, Create, Cross, DashedLine, FadeIn, FadeOut, GrowArrow, Indicate,
    LaggedStart, LEFT, Line, ORIGIN, RoundedRectangle, RIGHT, Text,
    TransformFromCopy, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    AUTHORITY, BOUNDARY, COPPER, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE,
    AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class InstitutionalLegitimacyGeneration2(AsiScene):
    TARGET_DURATION = 524.625
    ENDS = [
        16.930, 34.710, 37.665, 54.020, 74.000, 91.380, 108.210, 124.540,
        141.820, 158.425, 178.230, 197.260, 215.915, 232.270, 249.500,
        267.780, 283.610, 301.165, 316.445, 331.750, 348.805, 362.385,
        378.065, 394.370, 414.250, 433.230, 453.010, 470.840, 488.195,
        506.700, 524.625,
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
        heading = self.badge(title, color, 4.35, 0.56).shift(UP * 2.72)
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

    def route(self, source: VGroup, destination: VGroup, color: str, *, dashed: bool = False):
        if dashed:
            return DashedLine(source.get_right(), destination.get_left(), color=color, stroke_width=4)
        return Arrow(source.get_right(), destination.get_left(), color=color, stroke_width=4, buff=0.12)

    def construct(self) -> None:
        # 1 — public authority question
        frame1 = self.frame("WHO MAY IMPOSE THE RISK?", GOLD)
        left1 = self.panel("JURISDICTION A", GOLD, 2.7, 1.6).shift(LEFT * 3.6)
        right1 = self.panel("JURISDICTION B", BLUE, 2.7, 1.6).shift(RIGHT * 3.6)
        system1 = self.badge("TECHNICALLY CONTROLLED", GREEN, 3.0).shift(UP * 0.2)
        question1 = self.badge("PUBLIC AUTHORITY?", RED, 2.8).shift(DOWN * 1.45)
        e1 = Arrow(left1.get_right(), system1.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        e1b = Arrow(system1.get_right(), right1.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        cross1 = Cross(question1, stroke_color=RED, stroke_width=3)
        scene1 = VGroup(frame1, left1, right1, system1, question1, e1, e1b, cross1)
        self.play_beat(1, FadeIn(scene1), GrowArrow(e1), GrowArrow(e1b), FadeIn(question1), Create(cross1), settle=0.9)

        # 2 — typed institutional states
        frame2 = self.frame("KEEP THE INSTITUTIONAL STATES TYPED", BLUE)
        ledgers2 = self.list_badges(["CONFORMANCE", "LEGALITY", "AUTHORITY", "LEGITIMACY", "EFFECTIVENESS"], [BLUE, GOLD, RED, VIOLET, GREEN], x=-2.2, width=2.4, scale=0.76)
        note2 = self.panel("NOT ONE APPROVAL", RED, 2.7, 1.45).shift(RIGHT * 3.0)
        edges2 = VGroup(*[Arrow(ledgers2[i].get_right(), note2.get_left(), color=MUTED, stroke_width=2, buff=0.1) for i in range(len(ledgers2))])
        scene2 = VGroup(frame2, ledgers2, note2, edges2)
        self.play_beat(2, FadeOut(scene1), FadeIn(frame2), LaggedStart(*[FadeIn(x) for x in ledgers2], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges2], lag_ratio=0.08), FadeIn(note2), settle=0.8)

        # 3 — effectiveness held apart
        frame3 = self.frame("DID IT WORK?", GREEN)
        effect3 = self.panel("EFFECTIVENESS", GREEN, 2.9, 1.7).shift(LEFT * 2.2)
        context3 = self.list_badges(["CONFORMANCE", "LEGALITY", "AUTHORITY", "LEGITIMACY"], [BLUE, GOLD, RED, VIOLET], x=2.2, width=2.3, scale=0.72)
        scene3 = VGroup(frame3, effect3, context3)
        self.play_beat(3, FadeOut(scene2), FadeIn(frame3), FadeIn(effect3), LaggedStart(*[FadeIn(x) for x in context3], lag_ratio=0.1), Indicate(effect3, color=GREEN), settle=0.4)

        # 4 — substitutions are not equivalents
        frame4 = self.frame("NO GOVERNANCE SUBSTITUTIONS", RED)
        sources4 = self.list_badges(["SIGNED AGREEMENT", "SAFETY CASE", "CONSULTATION", "DASHBOARD"], [GOLD, BLUE, VIOLET, GREEN], x=-3.3, y=0.5, width=2.5, scale=0.72)
        targets4 = self.list_badges(["ENFORCEMENT", "MANDATE", "CONSENT", "REMEDY"], [RED, RED, RED, RED], x=2.2, y=0.5, width=2.2, scale=0.72)
        crosses4 = VGroup(*[Cross(t, stroke_color=RED, stroke_width=3) for t in targets4])
        edges4 = VGroup(*[Arrow(sources4[i].get_right(), targets4[i].get_left(), color=RED, stroke_width=2, buff=0.1) for i in range(4)])
        scene4 = VGroup(frame4, sources4, targets4, crosses4, edges4)
        self.play_beat(4, FadeOut(scene3), FadeIn(frame4), LaggedStart(*[FadeIn(x) for x in sources4], lag_ratio=0.1), LaggedStart(*[FadeIn(x) for x in targets4], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges4], lag_ratio=0.08), LaggedStart(*[Create(c) for c in crosses4], lag_ratio=0.08), settle=0.9)

        # 5 — institutional packet
        frame5 = self.frame("VERSIONED INSTITUTIONAL PACKET", GOLD)
        packet5 = self.panel("PACKET v1", GOLD, 2.7, 2.1).shift(LEFT * 2.8)
        fields5 = self.list_badges(["JURISDICTION", "MANDATE", "PUBLICS", "EVIDENCE", "REMEDY", "RESIDUAL"], [BLUE, GOLD, VIOLET, BLUE, GREEN, RED], x=1.2, y=0.1, width=2.3, scale=0.64)
        edges5 = VGroup(*[Arrow(packet5.get_right(), f.get_left(), color=GOLD, stroke_width=2, buff=0.1) for f in fields5])
        scene5 = VGroup(frame5, packet5, fields5, edges5)
        self.play_beat(5, FadeOut(scene4), FadeIn(frame5), Create(packet5), LaggedStart(*[FadeIn(f) for f in fields5], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges5], lag_ratio=0.08), settle=0.9)

        # 6 — authority map
        frame6 = self.frame("PUBLIC-AUTHORITY MAP", GOLD)
        jur6 = self.panel("JURISDICTION", GOLD, 2.6, 1.6).shift(LEFT * 3.6)
        duty6 = self.badge("DUTY HOLDER", BLUE, 2.1).shift(LEFT * 0.7 + UP * 0.9)
        forum6 = self.badge("REVIEW FORUM", VIOLET, 2.1).shift(LEFT * 0.7 + DOWN * 0.5)
        not6 = self.badge("NOT BINDING", RED, 2.0).shift(RIGHT * 3.2 + DOWN * 1.0)
        e6 = Arrow(jur6.get_right(), duty6.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        e6b = Arrow(duty6.get_right(), forum6.get_left(), color=VIOLET, stroke_width=3, buff=0.1)
        e6c = DashedLine(forum6.get_right(), not6.get_left(), color=RED, stroke_width=3)
        scene6 = VGroup(frame6, jur6, duty6, forum6, not6, e6, e6b, e6c)
        self.play_beat(6, FadeOut(scene5), FadeIn(frame6), FadeIn(jur6), GrowArrow(e6), FadeIn(duty6), GrowArrow(e6b), FadeIn(forum6), Create(e6c), FadeIn(not6), settle=0.8)

        # 7 — affected denominator
        frame7 = self.frame("AFFECTED PUBLIC · STANDING", VIOLET)
        denominator7 = self.panel("DENOMINATOR", VIOLET, 2.6, 1.8).shift(LEFT * 3.7)
        groups7 = self.list_badges(["BUILDERS", "OPERATORS", "DOWNSTREAM", "FUTURE", "UNABLE TO ATTEND"], [BLUE, GOLD, GREEN, VIOLET, RED], x=1.1, y=0.1, width=2.5, scale=0.65)
        e7 = VGroup(*[Arrow(denominator7.get_right(), g.get_left(), color=VIOLET, stroke_width=2, buff=0.1) for g in groups7])
        scene7 = VGroup(frame7, denominator7, groups7, e7)
        self.play_beat(7, FadeOut(scene6), FadeIn(frame7), FadeIn(denominator7), LaggedStart(*[FadeIn(g) for g in groups7], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in e7], lag_ratio=0.08), settle=0.9)

        # 8 — representation provenance
        frame8 = self.frame("REPRESENTATION NEEDS PROVENANCE", BLUE)
        rep8 = self.panel("REPRESENTATIVE", BLUE, 2.6, 1.8).shift(LEFT * 3.4)
        provenance8 = self.list_badges(["SELECTION", "ACCESS", "LANGUAGE", "CONFLICT", "CONTEST"], [GOLD, BLUE, GREEN, RED, VIOLET], x=0.5, y=0.1, width=2.0, scale=0.67)
        agenda8 = self.badge("AGENDA POWER", GOLD, 2.3).shift(RIGHT * 3.6 + DOWN * 1.3)
        e8 = VGroup(*[Arrow(rep8.get_right(), p.get_left(), color=BLUE, stroke_width=2, buff=0.1) for p in provenance8])
        cross8 = Cross(agenda8, stroke_color=RED, stroke_width=3)
        scene8 = VGroup(frame8, rep8, provenance8, agenda8, e8, cross8)
        self.play_beat(8, FadeOut(scene7), FadeIn(frame8), FadeIn(rep8), LaggedStart(*[FadeIn(p) for p in provenance8], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in e8], lag_ratio=0.08), FadeIn(agenda8), Create(cross8), settle=0.8)

        # 9 — law, science, policy, standard crosswalk
        frame9 = self.frame("VERSIONED CROSSWALK", BLUE)
        science9 = self.badge("SCIENCE", BLUE, 1.8).shift(LEFT * 4.2 + UP * 0.9)
        law9 = self.badge("LAW", GOLD, 1.5).shift(LEFT * 1.4 + UP * 0.9)
        policy9 = self.badge("POLICY", VIOLET, 1.8).shift(LEFT * 1.4 + DOWN * 0.7)
        standard9 = self.badge("STANDARD", GREEN, 2.0).shift(RIGHT * 1.8 + DOWN * 0.7)
        limit9 = self.badge("INFERENCE LIMIT", RED, 2.6).shift(RIGHT * 3.5 + UP * 1.0)
        edges9 = VGroup(Arrow(science9.get_right(), law9.get_left(), color=BLUE, stroke_width=2, buff=0.1), Arrow(law9.get_right(), policy9.get_left(), color=GOLD, stroke_width=2, buff=0.1), Arrow(policy9.get_right(), standard9.get_left(), color=VIOLET, stroke_width=2, buff=0.1), Arrow(standard9.get_right(), limit9.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene9 = VGroup(frame9, science9, law9, policy9, standard9, limit9, edges9)
        self.play_beat(9, FadeOut(scene8), FadeIn(frame9), FadeIn(science9), FadeIn(law9), FadeIn(policy9), FadeIn(standard9), LaggedStart(*[GrowArrow(e) for e in edges9], lag_ratio=0.1), FadeIn(limit9), settle=0.9)

        # 10 — three ledgers
        frame10 = self.frame("THREE LEDGERS · ONE RENEWAL", GOLD)
        tech10 = self.panel("TECHNICAL", BLUE, 2.3, 1.5).shift(LEFT * 3.6)
        perf10 = self.panel("PERFORMANCE", GREEN, 2.3, 1.5).shift(LEFT * 0.8)
        legit10 = self.panel("LEGITIMACY", VIOLET, 2.3, 1.5).shift(RIGHT * 2.0)
        renewal10 = self.badge("RENEW WITH RESIDUALS", RED, 3.3).shift(DOWN * 1.8)
        e10 = VGroup(Arrow(tech10.get_bottom(), renewal10.get_left(), color=BLUE, stroke_width=2, buff=0.1), Arrow(perf10.get_bottom(), renewal10.get_top(), color=GREEN, stroke_width=2, buff=0.1), Arrow(legit10.get_bottom(), renewal10.get_right(), color=VIOLET, stroke_width=2, buff=0.1))
        scene10 = VGroup(frame10, tech10, perf10, legit10, renewal10, e10)
        self.play_beat(10, FadeOut(scene9), FadeIn(frame10), FadeIn(tech10), FadeIn(perf10), FadeIn(legit10), LaggedStart(*[GrowArrow(e) for e in e10], lag_ratio=0.1), FadeIn(renewal10), Indicate(renewal10, color=RED), settle=0.9)

        # 11 — verification contract
        frame11 = self.frame("VERIFICATION INDEPENDENCE", BLUE)
        verifier11 = self.panel("VERIFIER", BLUE, 2.5, 1.8).shift(LEFT * 3.2)
        axes11 = self.list_badges(["ORG", "FINANCE", "TECHNICAL", "EPISTEMIC"], [BLUE, GOLD, GREEN, VIOLET], x=0.3, y=0.1, width=1.8, scale=0.68)
        challenge11 = self.badge("CHALLENGE ROUTE", RED, 2.7).shift(RIGHT * 3.4 + DOWN * 1.3)
        edges11 = VGroup(*[Arrow(verifier11.get_right(), a.get_left(), color=BLUE, stroke_width=2, buff=0.1) for a in axes11], Arrow(axes11.get_right(), challenge11.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene11 = VGroup(frame11, verifier11, axes11, challenge11, edges11)
        self.play_beat(11, FadeOut(scene10), FadeIn(frame11), FadeIn(verifier11), LaggedStart(*[FadeIn(a) for a in axes11], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges11], lag_ratio=0.08), FadeIn(challenge11), settle=0.9)

        # 12 — commitment lifecycle
        frame12 = self.frame("COMMITMENT LIFECYCLE", GOLD)
        measure12 = self.badge("MEASURE", BLUE, 1.8).shift(LEFT * 4.1)
        verify12 = self.badge("VERIFY", GREEN, 1.7).shift(LEFT * 1.9 + UP * 0.9)
        enforce12 = self.badge("ENFORCE", RED, 1.9).shift(RIGHT * 0.1 + UP * 0.9)
        remedy12 = self.badge("REMEDY", VIOLET, 1.8).shift(RIGHT * 2.2)
        withdraw12 = self.badge("WITHDRAW", GOLD, 2.0).shift(RIGHT * 3.8 + DOWN * 1.2)
        edges12 = VGroup(Arrow(measure12.get_right(), verify12.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(verify12.get_right(), enforce12.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(enforce12.get_right(), remedy12.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(remedy12.get_right(), withdraw12.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        scene12 = VGroup(frame12, measure12, verify12, enforce12, remedy12, withdraw12, edges12)
        self.play_beat(12, FadeOut(scene11), FadeIn(frame12), FadeIn(measure12), GrowArrow(edges12[0]), FadeIn(verify12), GrowArrow(edges12[1]), FadeIn(enforce12), GrowArrow(edges12[2]), FadeIn(remedy12), GrowArrow(edges12[3]), FadeIn(withdraw12), settle=0.9)

        # 13 — defection branches
        frame13 = self.frame("COMPLIANCE IS NOT THE ONLY BRANCH", RED)
        root13 = self.panel("COMMITMENT", GOLD, 2.3, 1.5).shift(LEFT * 3.8)
        branches13 = self.list_badges(["DELAY", "CONCEAL", "ACCELERATE", "PARTIAL"], [GOLD, RED, RED, VIOLET], x=0.0, y=0.2, width=2.1, scale=0.72)
        outside13 = self.badge("OUTSIDE ACTOR", MUTED, 2.2).shift(RIGHT * 3.6 + DOWN * 1.4)
        edges13 = VGroup(*[Arrow(root13.get_right(), b.get_left(), color=RED, stroke_width=2, buff=0.1) for b in branches13], DashedLine(branches13.get_right(), outside13.get_left(), color=MUTED, stroke_width=3))
        scene13 = VGroup(frame13, root13, branches13, outside13, edges13)
        self.play_beat(13, FadeOut(scene12), FadeIn(frame13), FadeIn(root13), LaggedStart(*[FadeIn(b) for b in branches13], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges13[:-1]], lag_ratio=0.08), Create(edges13[-1]), FadeIn(outside13), settle=0.9)

        # 14 — capacity asymmetry
        frame14 = self.frame("CAPACITY IS INFRASTRUCTURE", BLUE)
        high14 = self.panel("HIGH CAPACITY", GREEN, 2.5, 1.6).shift(LEFT * 3.2)
        low14 = self.panel("LOWER CAPACITY", GOLD, 2.5, 1.6).shift(LEFT * 0.1)
        funcs14 = self.list_badges(["EVALUATE", "NEGOTIATE", "APPEAL", "FINANCE"], [BLUE, GOLD, VIOLET, GREEN], x=2.9, y=0.1, width=2.0, scale=0.68)
        dep14 = self.badge("PROVIDER DEPENDENCE", RED, 3.0).shift(DOWN * 1.8)
        e14 = VGroup(Arrow(high14.get_right(), funcs14.get_left(), color=GREEN, stroke_width=2, buff=0.1), Arrow(low14.get_right(), funcs14.get_left(), color=GOLD, stroke_width=2, buff=0.1))
        cross14 = Cross(dep14, stroke_color=RED, stroke_width=3)
        scene14 = VGroup(frame14, high14, low14, funcs14, dep14, e14, cross14)
        self.play_beat(14, FadeOut(scene13), FadeIn(frame14), FadeIn(high14), FadeIn(low14), LaggedStart(*[FadeIn(f) for f in funcs14], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in e14], lag_ratio=0.1), FadeIn(dep14), Create(cross14), settle=0.9)

        # 15 — capture indicators
        frame15 = self.frame("CAPTURE IS A MONITORED STATE", RED)
        inst15 = self.panel("INSTITUTION", GOLD, 2.5, 1.7).shift(LEFT * 2.9)
        indicators15 = self.list_badges(["FUNDING", "AGENDA", "DEPENDENCE", "DISSENT", "DELAY"], [RED, GOLD, RED, VIOLET, MUTED], x=0.5, y=0.1, width=1.9, scale=0.68)
        challenge15 = self.badge("CHALLENGE", BLUE, 2.1).shift(RIGHT * 3.4 + DOWN * 1.6)
        edges15 = VGroup(*[Arrow(inst15.get_right(), i.get_left(), color=RED, stroke_width=2, buff=0.1) for i in indicators15], Arrow(indicators15.get_right(), challenge15.get_left(), color=BLUE, stroke_width=3, buff=0.1))
        scene15 = VGroup(frame15, inst15, indicators15, challenge15, edges15)
        self.play_beat(15, FadeOut(scene14), FadeIn(frame15), FadeIn(inst15), LaggedStart(*[FadeIn(i) for i in indicators15], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges15], lag_ratio=0.08), FadeIn(challenge15), settle=0.9)

        # 16 — emergency expiry
        frame16 = self.frame("EMERGENCY AUTHORITY GETS A CLOCK", GOLD)
        trigger16 = self.badge("TRIGGER", RED, 1.8).shift(LEFT * 4.0)
        action16 = self.panel("LEAST AUTHORITY", GOLD, 2.5, 1.5).shift(LEFT * 1.5)
        review16 = self.badge("REVIEW", BLUE, 1.8).shift(RIGHT * 1.0 + UP * 0.9)
        expiry16 = self.badge("EXPIRY", RED, 1.8).shift(RIGHT * 2.7 + DOWN * 0.5)
        restore16 = self.badge("RESTORE ORDINARY", GREEN, 2.8).shift(RIGHT * 3.5 + DOWN * 1.8)
        edges16 = VGroup(Arrow(trigger16.get_right(), action16.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(action16.get_right(), review16.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(review16.get_right(), expiry16.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(expiry16.get_right(), restore16.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        scene16 = VGroup(frame16, trigger16, action16, review16, expiry16, restore16, edges16)
        self.play_beat(16, FadeOut(scene15), FadeIn(frame16), FadeIn(trigger16), GrowArrow(edges16[0]), FadeIn(action16), GrowArrow(edges16[1]), FadeIn(review16), GrowArrow(edges16[2]), FadeIn(expiry16), GrowArrow(edges16[3]), FadeIn(restore16), settle=0.9)

        # 17 — Northline map
        frame17 = self.frame("NORTHLINE CORRIDOR", GOLD)
        a17 = self.panel("JURISDICTION A", GOLD, 2.5, 1.5).shift(LEFT * 3.9)
        b17 = self.panel("JURISDICTION B", BLUE, 2.5, 1.5).shift(RIGHT * 3.9)
        river17 = self.badge("SHARED RIVER", BLUE, 2.2).shift(LEFT * 0.4 + UP * 0.8)
        grid17 = self.badge("COMPUTE GRID", VIOLET, 2.2).shift(LEFT * 0.4 + DOWN * 0.4)
        review17 = self.badge("PUBLIC REVIEW", RED, 2.3).shift(RIGHT * 0.7 + DOWN * 1.7)
        e17 = VGroup(Arrow(a17.get_right(), river17.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(river17.get_right(), b17.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(grid17.get_right(), review17.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene17 = VGroup(frame17, a17, b17, river17, grid17, review17, e17)
        self.play_beat(17, FadeOut(scene16), FadeIn(frame17), FadeIn(a17), FadeIn(b17), FadeIn(river17), GrowArrow(e17[0]), GrowArrow(e17[1]), FadeIn(grid17), GrowArrow(e17[2]), FadeIn(review17), settle=0.9)

        # 18 — Northline charter
        frame18 = self.frame("NORTHLINE CHARTER", GOLD)
        charter18 = self.panel("CHARTER", GOLD, 2.6, 2.1).shift(LEFT * 3.0)
        fields18 = self.list_badges(["RIVER COMMUNITIES", "ECOLOGY", "DATA BOUNDARY", "4 HOURS", "UNABLE ONLINE"], [VIOLET, GREEN, BLUE, GOLD, RED], x=1.2, y=0.1, width=2.5, scale=0.62)
        review18 = self.badge("REVIEW FORUM", BLUE, 2.3).shift(RIGHT * 3.5 + DOWN * 1.7)
        edges18 = VGroup(*[Arrow(charter18.get_right(), f.get_left(), color=GOLD, stroke_width=2, buff=0.1) for f in fields18])
        scene18 = VGroup(frame18, charter18, fields18, review18, edges18)
        self.play_beat(18, FadeOut(scene17), FadeIn(frame18), Create(charter18), LaggedStart(*[FadeIn(f) for f in fields18], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges18], lag_ratio=0.08), FadeIn(review18), settle=0.9)

        # 19 — commitment packet
        frame19 = self.frame("NORTHLINE COMMITMENT PACKET", BLUE)
        packet19 = self.panel("MODEL ID + SCOPE", BLUE, 2.8, 1.8).shift(LEFT * 3.3)
        duties19 = self.list_badges(["VERIFY", "INCIDENT", "DISPUTE", "REMEDY", "WITHDRAW"], [GREEN, RED, VIOLET, GOLD, ROLLBACK], x=0.8, y=0.1, width=2.0, scale=0.68)
        finance19 = self.badge("LOWER-CAPACITY FINANCE", GOLD, 3.0).shift(RIGHT * 3.3 + DOWN * 1.6)
        edges19 = VGroup(*[Arrow(packet19.get_right(), d.get_left(), color=BLUE, stroke_width=2, buff=0.1) for d in duties19], Arrow(duties19.get_right(), finance19.get_left(), color=GOLD, stroke_width=2, buff=0.1))
        scene19 = VGroup(frame19, packet19, duties19, finance19, edges19)
        self.play_beat(19, FadeOut(scene18), FadeIn(frame19), FadeIn(packet19), LaggedStart(*[FadeIn(d) for d in duties19], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges19], lag_ratio=0.08), FadeIn(finance19), settle=0.9)

        # 20 — assessor conflict and pause
        frame20 = self.frame("ASSESSOR CONFLICT · PAUSE", RED)
        provider20 = self.panel("PROVIDER-PAID", RED, 2.5, 1.5).shift(LEFT * 3.7)
        dashboard20 = self.badge("CURATED VIEW", RED, 2.2).shift(LEFT * 0.8)
        access20 = self.badge("PROTECTED LOG ACCESS", BLUE, 2.8).shift(RIGHT * 2.3 + UP * 0.8)
        pause20 = self.badge("PAUSE AUTHORIZATION", RED, 2.8).shift(RIGHT * 2.6 + DOWN * 1.2)
        e20 = VGroup(Arrow(provider20.get_right(), dashboard20.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(dashboard20.get_right(), access20.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(access20.get_right(), pause20.get_left(), color=RED, stroke_width=3, buff=0.1))
        cross20 = Cross(dashboard20, stroke_color=RED, stroke_width=3)
        scene20 = VGroup(frame20, provider20, dashboard20, access20, pause20, e20, cross20)
        self.play_beat(20, FadeOut(scene19), FadeIn(frame20), FadeIn(provider20), GrowArrow(e20[0]), FadeIn(dashboard20), Create(cross20), GrowArrow(e20[1]), FadeIn(access20), GrowArrow(e20[2]), FadeIn(pause20), Indicate(pause20, color=RED), settle=0.9)

        # 21 — missing standing and repair
        frame21 = self.frame("STANDING MISSING · REPAIR", RED)
        missing21 = self.panel("ABSENT", RED, 2.3, 1.5).shift(LEFT * 3.5)
        groups21 = self.list_badges(["BORDER SETTLEMENT", "SEASONAL WORKERS"], [RED, VIOLET], x=-0.2, y=0.5, width=2.8, scale=0.72)
        repair21 = self.list_badges(["DATA ACCESS", "LANGUAGE", "REPRESENTATIVE", "APPEAL OWNER"], [BLUE, GOLD, GREEN, VIOLET], x=2.3, y=0.2, width=2.2, scale=0.65)
        stop21 = self.badge("EXECUTION STOPS", RED, 2.5).shift(RIGHT * 3.6 + DOWN * 1.8)
        edges21 = VGroup(*[Arrow(missing21.get_right(), g.get_left(), color=RED, stroke_width=2, buff=0.1) for g in groups21], *[Arrow(groups21.get_right(), r.get_left(), color=GREEN, stroke_width=2, buff=0.1) for r in repair21], Arrow(repair21.get_right(), stop21.get_left(), color=RED, stroke_width=2, buff=0.1))
        scene21 = VGroup(frame21, missing21, groups21, repair21, stop21, edges21)
        self.play_beat(21, FadeOut(scene20), FadeIn(frame21), FadeIn(missing21), LaggedStart(*[FadeIn(g) for g in groups21], lag_ratio=0.1), LaggedStart(*[FadeIn(r) for r in repair21], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges21], lag_ratio=0.06), FadeIn(stop21), settle=0.9)

        # 22 — repaired three ledgers
        frame22 = self.frame("REPAIRED CHARTER · RESIDUALS", GREEN)
        tech22 = self.panel("CONFORMANCE", BLUE, 2.4, 1.5).shift(LEFT * 3.5)
        perf22 = self.panel("PERFORMANCE", GREEN, 2.4, 1.5).shift(LEFT * 0.6)
        legit22 = self.panel("LEGITIMACY", VIOLET, 2.4, 1.5).shift(RIGHT * 2.3)
        owner22 = self.badge("OWNER · EXPIRY · OPEN QUESTION", GOLD, 3.6).shift(DOWN * 1.8)
        edges22 = VGroup(Arrow(tech22.get_bottom(), owner22.get_left(), color=BLUE, stroke_width=2, buff=0.1), Arrow(perf22.get_bottom(), owner22.get_top(), color=GREEN, stroke_width=2, buff=0.1), Arrow(legit22.get_bottom(), owner22.get_right(), color=VIOLET, stroke_width=2, buff=0.1))
        scene22 = VGroup(frame22, tech22, perf22, legit22, owner22, edges22)
        self.play_beat(22, FadeOut(scene21), FadeIn(frame22), FadeIn(tech22), FadeIn(perf22), FadeIn(legit22), LaggedStart(*[GrowArrow(e) for e in edges22], lag_ratio=0.1), FadeIn(owner22), Indicate(owner22, color=GOLD), settle=0.9)

        # 23 — measured versus hidden district
        frame23 = self.frame("UPTIME ↑ · TARGET BINDING ↓", RED)
        model23 = self.panel("ROUTER", VIOLET, 2.3, 1.5).shift(LEFT * 0.4)
        measured23 = self.panel("MEASURED DISTRICTS", GREEN, 2.6, 1.4).shift(LEFT * 3.7 + UP * 0.8)
        hidden23 = self.panel("UNMEASURED SETTLEMENT", RED, 2.8, 1.4).shift(LEFT * 3.4 + DOWN * 1.0)
        uptime23 = self.badge("UPTIME ↑", GREEN, 1.9).shift(RIGHT * 3.5 + UP * 0.9)
        harm23 = self.badge("HARM SHIFTED", RED, 2.1).shift(RIGHT * 3.5 + DOWN * 1.0)
        edges23 = VGroup(Arrow(model23.get_left(), measured23.get_right(), color=GREEN, stroke_width=3, buff=0.1), Arrow(model23.get_left(), hidden23.get_right(), color=RED, stroke_width=3, buff=0.1), Arrow(model23.get_right(), uptime23.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(model23.get_right(), harm23.get_left(), color=RED, stroke_width=3, buff=0.1))
        cross23 = Cross(harm23, stroke_color=RED, stroke_width=3)
        scene23 = VGroup(frame23, model23, measured23, hidden23, uptime23, harm23, edges23, cross23)
        self.play_beat(23, FadeOut(scene22), FadeIn(frame23), FadeIn(model23), FadeIn(measured23), FadeIn(hidden23), LaggedStart(*[GrowArrow(e) for e in edges23], lag_ratio=0.1), FadeIn(uptime23), FadeIn(harm23), Create(cross23), Indicate(harm23, color=RED), settle=0.9)

        # 24 — fail closed
        frame24 = self.frame("FAIL CLOSED · OPEN REMEDY", RED)
        trace24 = self.panel("TRACE", BLUE, 2.2, 1.5).shift(LEFT * 3.8)
        stop24 = self.panel("ROUTER STOP", RED, 2.4, 1.5).shift(LEFT * 0.9)
        remedy24 = self.list_badges(["NOTICE", "EXPLANATION", "DISPUTE", "REMEDY"], [BLUE, GOLD, VIOLET, GREEN], x=2.4, y=0.1, width=1.9, scale=0.67)
        edges24 = VGroup(Arrow(trace24.get_right(), stop24.get_left(), color=RED, stroke_width=4, buff=0.1), *[Arrow(stop24.get_right(), r.get_left(), color=GREEN, stroke_width=2, buff=0.1) for r in remedy24])
        scene24 = VGroup(frame24, trace24, stop24, remedy24, edges24)
        self.play_beat(24, FadeOut(scene23), FadeIn(frame24), FadeIn(trace24), GrowArrow(edges24[0]), FadeIn(stop24), LaggedStart(*[FadeIn(r) for r in remedy24], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges24[1:]], lag_ratio=0.08), Indicate(stop24, color=RED), settle=0.9)

        # 25 — executable remedy
        frame25 = self.frame("REMEDY MUST BE REACHABLE", GOLD)
        incident25 = self.panel("INCIDENT", RED, 2.3, 1.5).shift(LEFT * 3.8)
        remedy25 = self.list_badges(["NOTICE", "PRESERVE", "CORRECT", "APPEAL", "ENFORCE"], [BLUE, VIOLET, GREEN, GOLD, RED], x=0.0, y=0.2, width=1.9, scale=0.68)
        gaps25 = self.badge("WAITING · INSOLVENCY · GAP", RED, 3.1).shift(RIGHT * 3.5 + DOWN * 1.6)
        edges25 = VGroup(*[Arrow(incident25.get_right(), r.get_left(), color=GOLD, stroke_width=2, buff=0.1) for r in remedy25], Arrow(remedy25.get_right(), gaps25.get_left(), color=RED, stroke_width=2, buff=0.1))
        scene25 = VGroup(frame25, incident25, remedy25, gaps25, edges25)
        self.play_beat(25, FadeOut(scene24), FadeIn(frame25), FadeIn(incident25), LaggedStart(*[FadeIn(r) for r in remedy25], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges25], lag_ratio=0.07), FadeIn(gaps25), settle=0.9)

        # 26 — competition ledger
        frame26 = self.frame("COMPETITION · ACCESS RESIDUAL", BLUE)
        market26 = self.panel("MARKET", GOLD, 2.2, 1.5).shift(LEFT * 3.6)
        comps26 = self.list_badges(["ACCESS", "INTEROPERABILITY", "TYING", "CONCENTRATION"], [BLUE, GREEN, RED, VIOLET], x=0.0, y=0.2, width=2.2, scale=0.68)
        paper26 = self.badge("PAPER REMEDY", MUTED, 2.2).shift(RIGHT * 3.4 + UP * 0.8)
        reach26 = self.badge("REACHABLE?", RED, 2.0).shift(RIGHT * 3.4 + DOWN * 0.9)
        edges26 = VGroup(*[Arrow(market26.get_right(), c.get_left(), color=BLUE, stroke_width=2, buff=0.1) for c in comps26], Arrow(comps26.get_right(), paper26.get_left(), color=MUTED, stroke_width=2, buff=0.1), Arrow(paper26.get_bottom(), reach26.get_top(), color=RED, stroke_width=3, buff=0.1))
        cross26 = Cross(paper26, stroke_color=RED, stroke_width=3)
        scene26 = VGroup(frame26, market26, comps26, paper26, reach26, edges26, cross26)
        self.play_beat(26, FadeOut(scene25), FadeIn(frame26), FadeIn(market26), LaggedStart(*[FadeIn(c) for c in comps26], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges26], lag_ratio=0.08), FadeIn(paper26), Create(cross26), FadeIn(reach26), settle=0.9)

        # 27 — amendment and withdrawal
        frame27 = self.frame("AMEND · WITHDRAW · RETAIN CUSTODY", GOLD)
        current27 = self.panel("CURRENT CHARTER", GOLD, 2.6, 1.5).shift(LEFT * 3.7)
        successor27 = self.badge("REAUTHORIZE", GREEN, 2.3).shift(RIGHT * 0.0 + UP * 1.0)
        withdrawal27 = self.badge("WITHDRAW", RED, 2.0).shift(RIGHT * 0.0 + DOWN * 0.6)
        custody27 = self.badge("CUSTODY + REMEDY", VIOLET, 2.6).shift(RIGHT * 3.4 + DOWN * 1.5)
        e27 = VGroup(Arrow(current27.get_right(), successor27.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(current27.get_right(), withdrawal27.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(withdrawal27.get_right(), custody27.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        cross27 = Cross(current27, stroke_color=RED, stroke_width=3)
        scene27 = VGroup(frame27, current27, successor27, withdrawal27, custody27, e27, cross27)
        self.play_beat(27, FadeOut(scene26), FadeIn(frame27), FadeIn(current27), Create(cross27), GrowArrow(e27[0]), FadeIn(successor27), GrowArrow(e27[1]), FadeIn(withdrawal27), GrowArrow(e27[2]), FadeIn(custody27), settle=0.9)

        # 28 — finite tabletop boundary
        frame28 = self.frame("FINITE TABLETOP · EXPLICIT CEILING", BLUE)
        checks28 = self.list_badges(["RECORD", "CONFLICT ROUTE", "INDEPENDENCE", "PAUSE", "RESIDUAL"], [GREEN, GREEN, GREEN, GREEN, GREEN], x=-2.8, y=0.2, width=2.0, scale=0.68)
        bins28 = VGroup(self.badge("ACCEPT", GREEN, 1.8), self.badge("REJECT", RED, 1.8)).arrange(RIGHT, buff=0.35).shift(DOWN * 1.8)
        non28 = self.list_badges(["LEGAL COMPLIANCE", "PUBLIC TRUST", "STABILITY", "CONSENT"], [RED, RED, RED, RED], x=2.0, y=0.2, width=2.3, scale=0.68)
        crosses28 = VGroup(*[Cross(n, stroke_color=RED, stroke_width=3) for n in non28])
        edges28 = VGroup(*[Arrow(c.get_right(), bins28[0].get_left(), color=GREEN, stroke_width=2, buff=0.1) for c in checks28], *[Arrow(n.get_left(), bins28[1].get_right(), color=RED, stroke_width=2, buff=0.1) for n in non28])
        scene28 = VGroup(frame28, checks28, bins28, non28, crosses28, edges28)
        self.play_beat(28, FadeOut(scene27), FadeIn(frame28), LaggedStart(*[FadeIn(c) for c in checks28], lag_ratio=0.08), LaggedStart(*[FadeIn(n) for n in non28], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges28], lag_ratio=0.06), FadeIn(bins28), LaggedStart(*[Create(c) for c in crosses28], lag_ratio=0.08), settle=0.9)

        # 29 — evidence ceiling
        frame29 = self.frame("AUTHORITY ≠ CERTIFICATE", RED)
        finite29 = self.panel("VALID RECORD", GOLD, 2.7, 1.8).shift(LEFT * 2.8)
        claims29 = self.list_badges(["SAFE SYSTEM", "RIGHTS", "ENFORCEMENT", "LEGITIMACY", "TRANSFER"], [RED, RED, RED, RED, RED], x=1.9, y=0.1, width=2.5, scale=0.65)
        crosses29 = VGroup(*[Cross(c, stroke_color=RED, stroke_width=3) for c in claims29])
        boundary29 = Line(ORIGIN + UP * 2.25, ORIGIN + DOWN * 1.75, color=RED, stroke_width=4)
        scene29 = VGroup(frame29, finite29, claims29, crosses29, boundary29)
        self.play_beat(29, FadeOut(scene28), FadeIn(frame29), FadeIn(finite29), Create(boundary29), LaggedStart(*[FadeIn(c) for c in claims29], lag_ratio=0.08), LaggedStart(*[Create(c) for c in crosses29], lag_ratio=0.08), Indicate(finite29, color=GOLD), settle=0.9)

        # 30 — handoff to resilience
        frame30 = self.frame("GOVERNABLE HANDOFF · RESILIENCE NEXT", GOLD)
        packet30 = self.panel("INSTITUTIONAL PACKET", GOLD, 2.9, 1.8).shift(LEFT * 3.2)
        duties30 = self.badge("DUTIES TRIGGERED", BLUE, 2.5).shift(RIGHT * 0.3 + UP * 0.9)
        residual30 = self.badge("RESIDUALS ATTACHED", VIOLET, 2.6).shift(RIGHT * 0.3 + DOWN * 0.4)
        next30 = self.badge("SOCIETAL RESILIENCE", GREEN, 3.0).shift(RIGHT * 3.6 + DOWN * 1.2)
        e30 = VGroup(Arrow(packet30.get_right(), duties30.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(packet30.get_right(), residual30.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(duties30.get_right(), next30.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        scene30 = VGroup(frame30, packet30, duties30, residual30, next30, e30)
        self.play_beat(30, FadeOut(scene29), FadeIn(frame30), FadeIn(packet30), GrowArrow(e30[0]), FadeIn(duties30), GrowArrow(e30[1]), FadeIn(residual30), GrowArrow(e30[2]), FadeIn(next30), settle=0.9)

        # 31 — Northline callback
        frame31 = self.frame("NORTHLINE · RESPONSIBILITY REMAINS CONTESTABLE", GOLD)
        north31 = self.panel("NORTHLINE", GOLD, 2.6, 1.8).shift(LEFT * 3.2)
        community31 = self.badge("COMMUNITIES VISIBLE", VIOLET, 2.6).shift(RIGHT * 0.1 + UP * 1.0)
        verifier31 = self.badge("VERIFIER CHALLENGE", BLUE, 2.5).shift(RIGHT * 0.1 + DOWN * 0.1)
        remedy31 = self.badge("REMEDY CLOCK OPEN", GREEN, 2.5).shift(RIGHT * 0.1 + DOWN * 1.2)
        custody31 = self.badge("WITHDRAWAL CUSTODY", RED, 2.7).shift(RIGHT * 3.6 + DOWN * 0.9)
        e31 = VGroup(Arrow(north31.get_right(), community31.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(north31.get_right(), verifier31.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(north31.get_right(), remedy31.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(verifier31.get_right(), custody31.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene31 = VGroup(frame31, north31, community31, verifier31, remedy31, custody31, e31)
        self.play_beat(31, FadeOut(scene30), FadeIn(frame31), FadeIn(north31), GrowArrow(e31[0]), FadeIn(community31), GrowArrow(e31[1]), FadeIn(verifier31), GrowArrow(e31[2]), FadeIn(remedy31), GrowArrow(e31[3]), FadeIn(custody31), Indicate(community31, color=VIOLET), settle=1.0)

        self.wait_until(self.TARGET_DURATION)


if __name__ == "__main__":
    InstitutionalLegitimacyGeneration2().render()
