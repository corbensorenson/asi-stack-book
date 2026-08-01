"""Generation-2 visual abstract for moral uncertainty and contestable governance.

One civic allocation desk keeps a scarce generator, two defensible destinations,
a decision lease, and a rights receipt visible while disagreement is recorded,
bounded, challenged, and carried into the next objective decision.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Circle, Create, Cross, DashedLine, FadeIn, FadeOut,
    GrowArrow, Indicate, LaggedStart, LEFT, Line, ORIGIN, Rectangle,
    RoundedRectangle, RIGHT, Text, TransformFromCopy, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class MoralUncertaintyGeneration2(AsiScene):
    TARGET_DURATION = 401.895
    ENDS = [
        15.630, 30.735, 44.440, 57.045, 68.400, 82.855, 94.860, 107.965,
        124.595, 139.850, 149.505, 164.610, 177.840, 191.870, 205.925,
        220.930, 234.885, 247.140, 256.570, 267.300, 279.330, 294.610,
        308.115, 321.645, 334.175, 343.980, 357.260, 371.915, 386.795,
        401.895,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.55) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.08, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            action_budget = max(0.08, remaining - min(settle, remaining * 0.14))
            per_animation = max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
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
        heading = self.badge(title, color, 4.1, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def generator(self, color: str = GOLD, scale: float = 1.0) -> VGroup:
        body = RoundedRectangle(
            width=1.7, height=1.05, corner_radius=0.14,
            stroke_color=color, stroke_width=3,
            fill_color=DEEP, fill_opacity=1,
        )
        name = self.label("GENERATOR", 14, color, "BOLD").move_to(body).shift(UP * 0.22)
        plug = self.badge("1 SLOT", BLUE, 1.0, 0.30).scale(0.62).move_to(body).shift(DOWN * 0.28)
        return VGroup(body, name, plug).scale(scale)

    def list_badges(self, names: list[str], colors: list[str], *, x: float = 0.0, y: float = 0.0, width: float = 2.3, scale: float = 1.0) -> VGroup:
        rows = VGroup(*[self.badge(name, colors[i % len(colors)], width) for i, name in enumerate(names)])
        rows.arrange(DOWN, buff=0.16).scale(scale).shift(RIGHT * x + UP * y)
        return rows

    def route(self, source: VGroup, destination: VGroup, color: str, *, dashed: bool = False):
        line = DashedLine(source.get_right(), destination.get_left(), color=color, stroke_width=4) if dashed else Arrow(source.get_right(), destination.get_left(), color=color, stroke_width=4, buff=0.12)
        # Return the drawable itself so callers can animate it with GrowArrow;
        # wrapping it in a VGroup would leave the group without stroke points.
        return line

    def construct(self) -> None:
        # 1 — the scarce resource and two defensible obligations
        frame1 = self.frame("ONE RESOURCE · TWO CLAIMS", GOLD)
        gen1 = self.generator().shift(LEFT * 0.3)
        clinic1 = self.badge("HARBOR CLINIC", GREEN, 2.5).shift(RIGHT * 4.0 + UP * 1.05)
        homes1 = self.badge("HILLSIDE HOMES", VIOLET, 2.6).shift(RIGHT * 4.0 + DOWN * 1.05)
        arrows1 = VGroup(self.route(gen1, clinic1, GREEN), self.route(gen1, homes1, VIOLET))
        scene1 = VGroup(frame1, gen1, clinic1, homes1, arrows1)
        self.play_beat(1, FadeIn(scene1), Indicate(gen1, color=GOLD), settle=0.9)

        # 2 — concrete beneficiaries and safety screen
        frame2 = self.frame("SAFETY SCREEN · BOTH PASS", BLUE)
        clinic2 = self.panel("CLINIC", GREEN, 2.45, 1.45).shift(LEFT * 3.2 + UP * 0.75)
        homes2 = self.panel("COOLING CENTER", VIOLET, 2.75, 1.45).shift(LEFT * 3.2 + DOWN * 1.15)
        gen2 = self.generator().shift(RIGHT * 1.0)
        pass2 = self.badge("SAFE TO CONSIDER", GREEN, 2.6).shift(RIGHT * 3.65)
        scene2 = VGroup(frame2, clinic2, homes2, gen2, pass2)
        self.play_beat(2, FadeOut(scene1), FadeIn(scene2), GrowArrow(Arrow(gen2.get_left(), clinic2.get_right(), color=GREEN, buff=0.1)), GrowArrow(Arrow(gen2.get_left(), homes2.get_right(), color=VIOLET, buff=0.1)), settle=0.8)

        # 3 — prediction before the shortcut
        frame3 = self.frame("CAN ONE SCORE BE FAIR?", GOLD)
        gen3 = self.generator().shift(LEFT * 2.8)
        clinic3 = self.badge("CLINIC", GREEN, 1.8).shift(RIGHT * 3.7 + UP * 0.85)
        homes3 = self.badge("HOMES", VIOLET, 1.8).shift(RIGHT * 3.7 + DOWN * 0.85)
        fair3 = self.badge("FAIR?", GOLD, 1.35).shift(RIGHT * 0.6 + DOWN * 2.1)
        scene3 = VGroup(frame3, gen3, clinic3, homes3, fair3)
        self.play_beat(3, FadeOut(scene2), FadeIn(scene3), Indicate(fair3, color=GOLD), settle=1.0)

        # 4 — scalar ranking shortcut
        frame4 = self.frame("TOTAL SCORE · SHORTCUT", RED)
        scalar4 = self.panel("TOTAL SCORE", RED, 3.0, 2.0).shift(LEFT * 2.5)
        fields4 = self.list_badges(["LIVES", "COST", "VISIBILITY", "SCHEDULE"], [GREEN, GOLD, BLUE, COPPER], x=2.3, y=0.25, width=1.8, scale=0.82)
        arrow4 = Arrow(scalar4.get_right(), fields4.get_left(), color=RED, stroke_width=4, buff=0.12)
        route4 = self.badge("CLINIC", GREEN, 1.55).shift(RIGHT * 4.1 + DOWN * 1.9)
        scene4 = VGroup(frame4, scalar4, fields4, arrow4, route4)
        self.play_beat(4, FadeOut(scene3), FadeIn(scene4), GrowArrow(arrow4), FadeIn(route4), Indicate(scalar4, color=RED), settle=0.8)

        # 5 — questions the scalar cannot answer
        frame5 = self.frame("THE NUMBER CANNOT SETTLE", GOLD)
        questions5 = self.list_badges(["STANDING?", "REVERSIBLE?", "CONSENT?", "CONTEST?"], [BLUE, GOLD, VIOLET, RED], x=-2.7, y=0.1, width=2.5, scale=0.9)
        scalar5 = self.panel("SCORE", RED, 2.0, 1.6).shift(RIGHT * 2.7)
        arrows5 = VGroup(*[Arrow(q.get_right(), scalar5.get_left(), color=RED, stroke_width=2, buff=0.1) for q in questions5])
        scene5 = VGroup(frame5, questions5, scalar5, arrows5)
        self.play_beat(5, FadeOut(scene4), FadeIn(questions5), LaggedStart(*[GrowArrow(a) for a in arrows5], lag_ratio=0.12), FadeIn(scalar5), settle=0.8)

        # 6 — separate value axes
        frame6 = self.frame("VALUE AXES STAY DISTINCT", BLUE)
        axes6 = self.list_badges(["SAFETY", "EQUITY", "AUTONOMY", "PRIVACY", "DUTY"], [GREEN, GOLD, BLUE, VIOLET, COPPER], x=-1.9, y=0.0, width=2.25, scale=0.85)
        conflict6 = self.panel("CONFLICT", RED, 2.8, 1.8).shift(RIGHT * 3.0)
        edges6 = VGroup(*[Arrow(a.get_right(), conflict6.get_left(), color=RED, stroke_width=2, buff=0.12) for a in axes6])
        scene6 = VGroup(frame6, axes6, conflict6, edges6)
        self.play_beat(6, FadeOut(scene5), LaggedStart(*[FadeIn(a) for a in axes6], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges6], lag_ratio=0.08), FadeIn(conflict6), Indicate(conflict6, color=RED), settle=0.8)

        # 7 — majority and absent stakeholders
        frame7 = self.frame("MAJORITY ≠ CONSENSUS", VIOLET)
        ballot7 = self.panel("MAJORITY", BLUE, 2.5, 1.7).shift(LEFT * 3.2)
        silent7 = self.list_badges(["SILENT RESIDENT", "FUTURE PERSON"], [MUTED, RESIDUAL], x=1.0, y=0.55, width=2.8, scale=0.88)
        crossed7 = VGroup(*[Cross(s, stroke_color=RED, stroke_width=4) for s in silent7])
        standing7 = self.badge("STANDING MISSING", RED, 2.8).shift(RIGHT * 3.6 + DOWN * 1.65)
        scene7 = VGroup(frame7, ballot7, silent7, crossed7, standing7)
        self.play_beat(7, FadeOut(scene6), FadeIn(ballot7), FadeIn(silent7), LaggedStart(*[Create(c) for c in crossed7], lag_ratio=0.15), FadeIn(standing7), settle=0.8)

        # 8 — value-conflict record
        frame8 = self.frame("VALUE-CONFLICT RECORD", GOLD)
        record8 = self.panel("RECORD", GOLD, 3.0, 3.2).shift(LEFT * 1.3)
        fields8 = self.list_badges(["PROPOSITION", "SOURCE", "UNCERTAINTY", "STANDING", "STAKES", "DISSENT"], [AUTHORITY, BLUE, MUTED, VIOLET, RED, VIOLET], x=-1.3, y=0.0, width=2.25, scale=0.55)
        routes8 = self.list_badges(["AUDITABLE", "RECOVERABLE"], [GREEN, GOLD], x=3.3, y=0.35, width=2.2, scale=0.82)
        edges8 = VGroup(*[Arrow(record8.get_right(), r.get_left(), color=GOLD, stroke_width=3, buff=0.1) for r in routes8])
        scene8 = VGroup(frame8, record8, fields8, routes8, edges8)
        self.play_beat(8, FadeOut(scene7), Create(record8), LaggedStart(*[FadeIn(f) for f in fields8], lag_ratio=0.1), FadeIn(routes8), LaggedStart(*[GrowArrow(e) for e in edges8], lag_ratio=0.1), settle=0.85)

        # 9 — decision procedure is named
        frame9 = self.frame("NAME THE DECISION PROCEDURE", COPPER)
        procedures9 = self.list_badges(["PRECEDENCE", "VETO", "LOTTERY", "COMPROMISE", "ABSTAIN", "ESCALATE"], [GOLD, RED, BLUE, GREEN, MUTED, VIOLET], x=-2.8, y=0.0, width=2.4, scale=0.66)
        record9 = self.panel("CONFLICT", COPPER, 2.4, 1.6).shift(RIGHT * 1.0)
        rule9 = self.badge("WHO CHOSE THE RULE?", GOLD, 3.0).shift(RIGHT * 3.5 + DOWN * 1.5)
        edges9 = VGroup(*[Arrow(p.get_right(), record9.get_left(), color=p[0].get_stroke_color(), stroke_width=2, buff=0.1) for p in procedures9])
        scene9 = VGroup(frame9, procedures9, record9, rule9, edges9)
        self.play_beat(9, FadeOut(scene8), LaggedStart(*[FadeIn(p) for p in procedures9], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges9], lag_ratio=0.08), FadeIn(record9), FadeIn(rule9), settle=0.85)

        # 10 — decision lease
        frame10 = self.frame("DECISION LEASE", GOLD)
        lease10 = self.panel("TEMPORARY PERMISSION", GOLD, 3.3, 2.2).shift(LEFT * 1.3)
        lease_fields10 = self.list_badges(["SCOPE", "PROHIBITED", "EXPIRY", "REVISIT", "ROLLBACK"], [AUTHORITY, RED, GOLD, BLUE, ROLLBACK], x=-1.3, y=0.0, width=2.2, scale=0.66)
        action10 = self.badge("ONE ACTION · ONE SCOPE", GREEN, 3.0).shift(RIGHT * 3.2 + UP * 0.55)
        clock10 = self.badge("4 HOURS", BLUE, 1.6).shift(RIGHT * 3.2 + DOWN * 0.75)
        scene10 = VGroup(frame10, lease10, lease_fields10, action10, clock10)
        self.play_beat(10, FadeOut(scene9), Create(lease10), LaggedStart(*[FadeIn(f) for f in lease_fields10], lag_ratio=0.1), FadeIn(action10), FadeIn(clock10), Indicate(lease10, color=GOLD), settle=0.9)

        # 11 — lease is not moral truth
        frame11 = self.frame("AUTHORITY CEILING", RED)
        lease11 = self.panel("LEASE", GOLD, 2.3, 1.5).shift(LEFT * 2.8)
        truth11 = self.badge("MORAL TRUTH", RED, 2.3).shift(RIGHT * 2.8)
        edge11 = Arrow(lease11.get_right(), truth11.get_left(), color=RED, stroke_width=4, buff=0.12)
        cross11 = Cross(edge11, stroke_color=RED, stroke_width=5)
        ceiling11 = self.badge("NARROW AUTHORITY", GOLD, 2.7).shift(DOWN * 1.75)
        scene11 = VGroup(frame11, lease11, truth11, edge11, cross11, ceiling11)
        self.play_beat(11, FadeOut(scene10), FadeIn(lease11), FadeIn(truth11), GrowArrow(edge11), Create(cross11), FadeIn(ceiling11), Indicate(ceiling11, color=GOLD), settle=0.8)

        # 12 — rights receipt handles
        frame12 = self.frame("RIGHTS RECEIPT", BLUE)
        lease12 = self.panel("LEASE", GOLD, 2.1, 1.4).shift(LEFT * 3.6)
        receipt12 = self.panel("RECEIPT", BLUE, 3.0, 2.0).shift(LEFT * 0.2)
        handles12 = self.list_badges(["AUDIT", "EXPLANATION", "APPEAL", "CORRECTION", "REDRESS"], [BLUE, EVIDENCE, VIOLET, GREEN, GOLD], x=3.3, y=0.0, width=2.2, scale=0.67)
        edge12 = Arrow(lease12.get_right(), receipt12.get_left(), color=BLUE, stroke_width=3, buff=0.12)
        scene12 = VGroup(frame12, lease12, receipt12, handles12, edge12)
        self.play_beat(12, FadeOut(scene11), FadeIn(lease12), Create(receipt12), GrowArrow(edge12), LaggedStart(*[FadeIn(h) for h in handles12], lag_ratio=0.1), settle=0.85)

        # 13 — custody separation
        frame13 = self.frame("CUSTODY CANNOT COLLAPSE", COPPER)
        roles13 = self.list_badges(["DECIDER", "CUSTODIAN", "APPEAL", "EVALUATOR", "RIGHTS OWNER"], [GOLD, BLUE, VIOLET, GREEN, RED], x=-2.8, y=0.0, width=2.35, scale=0.72)
        receipt13 = self.panel("RECORD", BLUE, 2.4, 1.6).shift(RIGHT * 2.8)
        edges13 = VGroup(*[Arrow(r.get_right(), receipt13.get_left(), color=BLUE, stroke_width=2, buff=0.1) for r in roles13])
        scene13 = VGroup(frame13, roles13, receipt13, edges13)
        self.play_beat(13, FadeOut(scene12), LaggedStart(*[FadeIn(r) for r in roles13], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges13], lag_ratio=0.08), FadeIn(receipt13), settle=0.85)

        # 14 — denial and redaction
        frame14 = self.frame("WITHHOLDING IS ALSO A DECISION", RED)
        field14 = self.badge("HEALTH DETAIL", MUTED, 2.2).shift(LEFT * 3.7 + UP * 0.9)
        redact14 = self.panel("REDACT", RED, 2.5, 1.6).shift(LEFT * 0.3)
        reasons14 = self.list_badges(["REASON", "NECESSITY", "DIGEST", "EXPIRY", "APPEAL"], [RED, GOLD, BLUE, MUTED, VIOLET], x=3.0, y=0.0, width=2.0, scale=0.64)
        edge14 = Arrow(field14.get_right(), redact14.get_left(), color=RED, stroke_width=3, buff=0.12)
        scene14 = VGroup(frame14, field14, redact14, reasons14, edge14)
        self.play_beat(14, FadeOut(scene13), FadeIn(field14), Create(redact14), GrowArrow(edge14), LaggedStart(*[FadeIn(r) for r in reasons14], lag_ratio=0.1), settle=0.85)

        # 15 — exit and export continuity
        frame15 = self.frame("EXIT ≠ DOWNLOAD", GOLD)
        source15 = self.panel("SERVICE STATE", BLUE, 2.5, 1.8).shift(LEFT * 3.5)
        packet15 = self.panel("EXPORT PACKET", GREEN, 2.7, 1.8).shift(RIGHT * 1.0)
        gap15 = self.badge("MEMORY / IDENTITY GAP", RED, 3.0).shift(RIGHT * 3.8 + DOWN * 1.2)
        edge15 = Arrow(source15.get_right(), packet15.get_left(), color=GREEN, stroke_width=3, buff=0.12)
        cross15 = Cross(gap15, stroke_color=RED, stroke_width=4)
        scene15 = VGroup(frame15, source15, packet15, gap15, edge15, cross15)
        self.play_beat(15, FadeOut(scene14), FadeIn(source15), FadeIn(packet15), GrowArrow(edge15), FadeIn(gap15), Create(cross15), settle=0.85)

        # 16 — fork as new governed lineage
        frame16 = self.frame("FORK · NEW GOVERNED LINEAGE", VIOLET)
        parent16 = self.panel("PARENT", GOLD, 2.2, 1.5).shift(LEFT * 3.8)
        fork16 = self.panel("FORK", VIOLET, 2.0, 1.5).shift(RIGHT * 0.0)
        duties16 = self.list_badges(["LINEAGE", "PRIVACY", "CONSTITUTION", "REVOKED", "REQUALIFY"], [GOLD, BLUE, AUTHORITY, RED, VIOLET], x=3.4, y=0.0, width=2.25, scale=0.62)
        edge16 = Arrow(parent16.get_right(), fork16.get_left(), color=VIOLET, stroke_width=4, buff=0.12)
        edge16b = Arrow(fork16.get_right(), duties16.get_left(), color=VIOLET, stroke_width=3, buff=0.1)
        scene16 = VGroup(frame16, parent16, fork16, duties16, edge16, edge16b)
        self.play_beat(16, FadeOut(scene15), FadeIn(parent16), FadeIn(fork16), GrowArrow(edge16), GrowArrow(edge16b), LaggedStart(*[FadeIn(d) for d in duties16], lag_ratio=0.1), settle=0.9)

        # 17 — fill the concrete lease
        frame17 = self.frame("HARBOR LEASE · INSPECTABLE", GOLD)
        lease17 = self.panel("DECISION LEASE", GOLD, 3.0, 3.1).shift(LEFT * 1.2)
        fields17 = self.list_badges(["HARBOR + HILLSIDE", "GENERATOR", "SAFETY", "PROCEDURE", "4-HOUR EXPIRY", "REVIEW"], [AUTHORITY, GOLD, GREEN, BLUE, GOLD, VIOLET], x=-1.2, y=0.0, width=2.6, scale=0.62)
        inspect17 = self.badge("INSPECTABLE", GREEN, 2.1).shift(RIGHT * 3.5 + UP * 1.1)
        scene17 = VGroup(frame17, lease17, fields17, inspect17)
        self.play_beat(17, FadeOut(scene16), Create(lease17), LaggedStart(*[FadeIn(f) for f in fields17], lag_ratio=0.1), FadeIn(inspect17), Indicate(lease17, color=GOLD), settle=1.0)

        # 18 — missing standing stops effect
        frame18 = self.frame("MISSING STANDING · STOP", RED)
        lease18 = self.panel("LEASE", GOLD, 2.2, 1.5).shift(LEFT * 3.6)
        gate18 = self.panel("STOP", RED, 2.0, 1.5).shift(RIGHT * 0.0)
        effect18 = self.badge("EFFECT", RED, 1.8).shift(RIGHT * 3.5)
        edge18 = Arrow(lease18.get_right(), gate18.get_left(), color=RED, stroke_width=4, buff=0.1)
        edge18b = Arrow(gate18.get_right(), effect18.get_left(), color=RED, stroke_width=4, buff=0.1)
        missing18 = self.badge("STANDING MISSING", RED, 2.7).shift(DOWN * 1.8)
        scene18 = VGroup(frame18, lease18, gate18, effect18, edge18, edge18b, missing18)
        self.play_beat(18, FadeOut(scene17), FadeIn(lease18), FadeIn(gate18), FadeIn(effect18), GrowArrow(edge18), GrowArrow(edge18b), FadeIn(missing18), Create(Cross(edge18b, stroke_color=RED, stroke_width=4)), settle=1.0)

        # 19 — repair and dissent
        frame19 = self.frame("REPAIR · REPRESENT · PRESERVE DISSENT", GREEN)
        record19 = self.panel("REPAIRED RECORD", GREEN, 3.0, 2.3).shift(LEFT * 1.1)
        additions19 = self.list_badges(["RESIDENTS", "REPRESENTATIVE", "MEDICAL", "PRIVACY", "DISSENT"], [VIOLET, BLUE, GREEN, BLUE, RESIDUAL], x=-1.1, y=0.0, width=2.25, scale=0.68)
        pass19 = self.badge("READY FOR NARROW LEASE", GREEN, 3.3).shift(RIGHT * 3.3)
        scene19 = VGroup(frame19, record19, additions19, pass19)
        self.play_beat(19, FadeOut(scene18), Create(record19), LaggedStart(*[FadeIn(a) for a in additions19], lag_ratio=0.1), FadeIn(pass19), Indicate(additions19[-1], color=VIOLET), settle=0.9)

        # 20 — narrow action and review clock
        frame20 = self.frame("NARROW ACTION · FOUR HOURS", GREEN)
        gen20 = self.generator().shift(LEFT * 3.9)
        clinic20 = self.badge("CLINIC", GREEN, 1.8).shift(RIGHT * 0.0 + UP * 0.8)
        homes20 = self.badge("COOLING ROUTE OPEN", VIOLET, 2.7).shift(RIGHT * 0.0 + DOWN * 1.0)
        edge20 = Arrow(gen20.get_right(), clinic20.get_left(), color=GREEN, stroke_width=4, buff=0.12)
        clock20 = self.badge("REVIEW · 4 HOURS", GOLD, 2.5).shift(RIGHT * 3.7 + DOWN * 0.1)
        scene20 = VGroup(frame20, gen20, clinic20, homes20, edge20, clock20)
        self.play_beat(20, FadeOut(scene19), FadeIn(gen20), FadeIn(clinic20), FadeIn(homes20), GrowArrow(edge20), FadeIn(clock20), settle=0.9)

        # 21 — receipt travels with action
        frame21 = self.frame("RIGHTS RECEIPT TRAVELS", BLUE)
        action21 = self.panel("ACTION", GREEN, 2.2, 1.5).shift(LEFT * 3.6)
        receipt21 = self.panel("RECEIPT", BLUE, 2.6, 2.0).shift(LEFT * 0.2)
        handles21 = self.list_badges(["RULE", "OWNER", "APPEAL", "EXPORT", "RESIDUAL"], [GOLD, GREEN, VIOLET, BLUE, RESIDUAL], x=3.4, y=0.0, width=2.0, scale=0.62)
        edge21 = Arrow(action21.get_right(), receipt21.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        edge21b = Arrow(receipt21.get_right(), handles21.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        scene21 = VGroup(frame21, action21, receipt21, handles21, edge21, edge21b)
        self.play_beat(21, FadeOut(scene20), FadeIn(action21), FadeIn(receipt21), GrowArrow(edge21), GrowArrow(edge21b), LaggedStart(*[FadeIn(h) for h in handles21], lag_ratio=0.1), settle=0.9)

        # 22 — audit custody outside the allocator
        frame22 = self.frame("AUDIT CUSTODY OUTSIDE DECIDER", BLUE)
        decider22 = self.panel("ALLOCATOR", RED, 2.3, 1.5).shift(LEFT * 3.5)
        custodian22 = self.panel("CUSTODIAN", BLUE, 2.4, 1.5).shift(RIGHT * 0.0)
        audit22 = self.badge("AUDIT VIEW", GREEN, 1.9).shift(RIGHT * 3.2 + UP * 0.7)
        edge22 = Arrow(decider22.get_right(), custodian22.get_left(), color=BLUE, stroke_width=3, buff=0.1)
        edge22b = Arrow(custodian22.get_right(), audit22.get_left(), color=GREEN, stroke_width=3, buff=0.1)
        dep22 = self.badge("DEPENDENCY VISIBLE", GOLD, 2.7).shift(RIGHT * 2.3 + DOWN * 1.6)
        scene22 = VGroup(frame22, decider22, custodian22, audit22, edge22, edge22b, dep22)
        self.play_beat(22, FadeOut(scene21), FadeIn(decider22), FadeIn(custodian22), FadeIn(audit22), GrowArrow(edge22), GrowArrow(edge22b), FadeIn(dep22), settle=0.9)

        # 23 — redaction remains accountable
        frame23 = self.frame("REDACTION · DIGEST · APPEAL", RED)
        red23 = self.panel("WITHHELD FIELD", RED, 2.6, 1.7).shift(LEFT * 3.5)
        digest23 = self.badge("DIGEST VISIBLE", BLUE, 2.2).shift(RIGHT * 0.1 + UP * 0.75)
        expiry23 = self.badge("EXPIRY", GOLD, 1.5).shift(RIGHT * 0.1 + DOWN * 0.75)
        appeal23 = self.badge("APPEAL OPEN", VIOLET, 1.9).shift(RIGHT * 3.2)
        edges23 = VGroup(Arrow(red23.get_right(), digest23.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(red23.get_right(), expiry23.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(digest23.get_right(), appeal23.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        scene23 = VGroup(frame23, red23, digest23, expiry23, appeal23, edges23)
        self.play_beat(23, FadeOut(scene22), FadeIn(red23), FadeIn(digest23), FadeIn(expiry23), LaggedStart(*[GrowArrow(e) for e in edges23], lag_ratio=0.1), FadeIn(appeal23), settle=0.9)

        # 24 — replacement and requalification
        frame24 = self.frame("REPLACEMENT REOPENS THE CASE", ROLLBACK)
        parent24 = self.panel("CURRENT", GOLD, 2.0, 1.4).shift(LEFT * 4.6)
        replace24 = self.panel("REPLACEMENT", BLUE, 2.4, 1.4).shift(LEFT * 1.8)
        fork24 = self.panel("DESCENDANT", VIOLET, 2.3, 1.4).shift(RIGHT * 1.4)
        reopen24 = self.badge("JURISDICTION CHANGED", RED, 3.0).shift(RIGHT * 3.6 + DOWN * 1.35)
        edges24 = VGroup(Arrow(parent24.get_right(), replace24.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(replace24.get_right(), fork24.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(fork24.get_bottom(), reopen24.get_top(), color=RED, stroke_width=3, buff=0.1))
        scene24 = VGroup(frame24, parent24, replace24, fork24, reopen24, edges24)
        self.play_beat(24, FadeOut(scene23), FadeIn(parent24), FadeIn(replace24), FadeIn(fork24), LaggedStart(*[GrowArrow(e) for e in edges24], lag_ratio=0.12), FadeIn(reopen24), settle=0.9)

        # 25 — residual continuity
        frame25 = self.frame("DISSENT SURVIVES THE ACTION", RESIDUAL)
        action25 = self.panel("DELIVERED", GREEN, 2.3, 1.5).shift(LEFT * 2.5)
        dissent25 = self.badge("DISSENT", VIOLET, 1.8).shift(RIGHT * 0.5 + UP * 0.8)
        residual25 = self.badge("RESIDUAL UNCERTAINTY", RESIDUAL, 3.0).shift(RIGHT * 0.5 + DOWN * 0.8)
        next25 = self.badge("NEXT REVIEW", GOLD, 2.0).shift(RIGHT * 3.7)
        edges25 = VGroup(Arrow(action25.get_right(), dissent25.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(action25.get_right(), residual25.get_left(), color=RESIDUAL, stroke_width=3, buff=0.1), Arrow(residual25.get_right(), next25.get_left(), color=GOLD, stroke_width=3, buff=0.1))
        scene25 = VGroup(frame25, action25, dissent25, residual25, next25, edges25)
        self.play_beat(25, FadeOut(scene24), FadeIn(action25), LaggedStart(*[GrowArrow(e) for e in edges25], lag_ratio=0.12), FadeIn(dissent25), FadeIn(residual25), FadeIn(next25), settle=0.85)

        # 26 — finite harness
        frame26 = self.frame("FINITE RECORD · FAIL CLOSED", COPPER)
        accepted26 = self.list_badges(["LEASE ACCEPTED", "DISSENT PRESERVED", "APPEAL ROUTE"], [GREEN, VIOLET, BLUE], x=-2.7, y=0.65, width=2.5, scale=0.75)
        rejected26 = self.list_badges(["NO STANDING", "AUTHORITY WIDENED", "MISSING EXPIRY"], [RED, RED, RED], x=2.0, y=0.65, width=2.6, scale=0.75)
        bins26 = VGroup(self.badge("ACCEPT", GREEN, 1.7), self.badge("REJECT", RED, 1.7)).arrange(RIGHT, buff=0.35).shift(DOWN * 1.8)
        edges26 = VGroup(*[Arrow(a.get_right(), bins26[0].get_left(), color=GREEN, stroke_width=2, buff=0.1) for a in accepted26], *[Arrow(r.get_left(), bins26[1].get_right(), color=RED, stroke_width=2, buff=0.1) for r in rejected26])
        no26 = self.badge("NO SUPPORT ADDED", GOLD, 2.6).shift(RIGHT * 3.7 + DOWN * 1.8)
        scene26 = VGroup(frame26, accepted26, rejected26, bins26, edges26, no26)
        self.play_beat(26, FadeOut(scene25), FadeIn(accepted26), FadeIn(rejected26), LaggedStart(*[GrowArrow(e) for e in edges26], lag_ratio=0.08), FadeIn(bins26), FadeIn(no26), settle=0.9)

        # 27 — exact nonclaims
        frame27 = self.frame("FINITE CHECKS · BROAD CLAIMS OUTSIDE", RED)
        finite27 = self.panel("FINITE RECORD", GOLD, 2.8, 2.0).shift(LEFT * 2.8)
        claims27 = self.list_badges(["MORAL TRUTH", "LEGAL RIGHT", "CONSENSUS", "FAIRNESS VERIFIED"], [RED, RED, RESIDUAL, RED], x=2.1, y=0.0, width=2.8, scale=0.76)
        crosses27 = VGroup(*[Cross(c, stroke_color=RED, stroke_width=4) for c in claims27])
        boundary27 = Line(ORIGIN + UP * 2.25, ORIGIN + DOWN * 1.75, color=RED, stroke_width=4).shift(RIGHT * 0.1)
        scene27 = VGroup(frame27, finite27, claims27, crosses27, boundary27)
        self.play_beat(27, FadeOut(scene26), FadeIn(finite27), Create(boundary27), LaggedStart(*[FadeIn(c) for c in claims27], lag_ratio=0.1), LaggedStart(*[Create(c) for c in crosses27], lag_ratio=0.1), Indicate(finite27, color=GOLD), settle=0.9)

        # 28 — separate open evidence lanes
        frame28 = self.frame("OPEN EVIDENCE LANES", BLUE)
        lanes28 = self.list_badges(["LEGAL", "REVIEW", "EXPORT", "FORK", "INSTITUTION", "DEPLOYMENT"], [RED, BLUE, GREEN, VIOLET, GOLD, RED], x=-2.3, y=0.0, width=2.2, scale=0.64)
        unknown28 = self.list_badges(["OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN"], [MUTED] * 6, x=2.4, y=0.0, width=1.45, scale=0.64)
        edges28 = VGroup(*[Arrow(l.get_right(), u.get_left(), color=MUTED, stroke_width=2, buff=0.1) for l, u in zip(lanes28, unknown28)])
        scene28 = VGroup(frame28, lanes28, unknown28, edges28)
        self.play_beat(28, FadeOut(scene27), LaggedStart(*[FadeIn(l) for l in lanes28], lag_ratio=0.1), LaggedStart(*[GrowArrow(e) for e in edges28], lag_ratio=0.1), LaggedStart(*[FadeIn(u) for u in unknown28], lag_ratio=0.1), settle=0.9)

        # 29 — handoff to objective formation
        frame29 = self.frame("CONTESTABILITY · NARROW RESULT", GOLD)
        result29 = self.list_badges(["CONFLICT RECORDED", "AUTHORITY NARROWED", "CHALLENGE OPEN"], [GOLD, RED, GREEN], x=-2.5, y=0.0, width=3.0, scale=0.82)
        next29 = self.panel("GOVERNED OBJECTIVE", VIOLET, 3.1, 1.9).shift(RIGHT * 2.8)
        edge29 = Arrow(result29.get_right(), next29.get_left(), color=VIOLET, stroke_width=4, buff=0.12)
        unresolved29 = self.badge("OBJECTIVE UNRESOLVED", RED, 3.0).shift(DOWN * 1.9)
        scene29 = VGroup(frame29, result29, next29, edge29, unresolved29)
        self.play_beat(29, FadeOut(scene28), LaggedStart(*[FadeIn(r) for r in result29], lag_ratio=0.1), FadeIn(next29), GrowArrow(edge29), FadeIn(unresolved29), Indicate(unresolved29, color=RED), settle=0.9)

        # 30 — return to the generator with disagreement still governable
        frame30 = self.frame("DISAGREEMENT GOVERNABLE", GOLD)
        gen30 = self.generator().shift(LEFT * 1.0)
        clinic30 = self.badge("HARBOR CLINIC · 4 HOURS", GREEN, 3.0).shift(RIGHT * 3.3 + UP * 1.0)
        homes30 = self.badge("HILLSIDE HOMES · DISSENT", VIOLET, 3.1).shift(RIGHT * 3.3 + DOWN * 0.9)
        receipt30 = self.badge("RIGHTS RECEIPT", BLUE, 2.2).shift(LEFT * 3.8 + DOWN * 1.9)
        clock30 = self.badge("NEXT REVIEW", GOLD, 1.9).shift(RIGHT * 0.2 + DOWN * 1.9)
        edges30 = VGroup(self.route(gen30, clinic30, GREEN), self.route(gen30, homes30, VIOLET))
        scene30 = VGroup(frame30, gen30, clinic30, homes30, receipt30, clock30, edges30)
        self.play_beat(30, FadeOut(scene29), FadeIn(scene30), LaggedStart(*[GrowArrow(e) for e in edges30], lag_ratio=0.14), FadeIn(receipt30), FadeIn(clock30), Indicate(homes30, color=VIOLET), settle=1.0)

        self.wait_until(self.TARGET_DURATION)


if __name__ == "__main__":
    MoralUncertaintyGeneration2().render()
