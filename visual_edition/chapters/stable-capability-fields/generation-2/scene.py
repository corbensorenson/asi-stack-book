"""Generation-2 visual abstract for Stable Capability Fields.

The scene turns the chapter's proposed continuity contract into a concrete
qualification desk: a field promise surrounds changing implementations while
scope, authority, evidence, residuals, and recovery remain visible.  It is a
design-rationale derivative, not evidence of semantic equivalence or deployed
safe replacement.
"""

from __future__ import annotations

from manim import (
    Arrow, Create, Cross, DashedLine, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart,
    LEFT, Line, ORIGIN, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import BOUNDARY, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE, AsiScene, text


GOLD = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class StableCapabilityFieldsGeneration2(AsiScene):
    TARGET_DURATION = 261.975
    ENDS = [18.65, 37.12, 48.575, 67.845, 79.565, 84.195, 102.965, 110.66, 128.955, 147.335, 165.93, 174.65, 189.93, 200.9, 220.9, 228.975, 245.005, 261.975]

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

    def badge(self, value: str, color: str, width: float = 2.25, height: float = 0.46) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=color, stroke_width=2.6, fill_color=SURFACE, fill_opacity=1)
        caption = self.label(value, 12, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.55, height: float = 1.45) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.16, stroke_color=color, stroke_width=3, fill_color=DEEP, fill_opacity=1)
        tag = self.badge(title, color, min(width - 0.16, 3.6), 0.4).scale(0.8)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def frame(self, title: str, color: str = GOLD) -> VGroup:
        shell = RoundedRectangle(width=11.7, height=6.2, corner_radius=0.2, stroke_color=BOUNDARY, stroke_width=2, fill_color="#0F2029", fill_opacity=1)
        heading = self.badge(title, color, 5.25, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def list_badges(self, names: list[str], colors: list[str], *, x: float = 0, y: float = 0, width: float = 2.15, scale: float = 0.72) -> VGroup:
        rows = VGroup(*[self.badge(name, colors[i % len(colors)], width) for i, name in enumerate(names)])
        rows.arrange(DOWN, buff=0.14).scale(scale).shift(RIGHT * x + UP * y)
        return rows

    def construct(self) -> None:
        # 1 — the fixed name hides changed obligations
        f1 = self.frame("ONE NAME · MANY OBLIGATIONS", RED)
        route1 = self.panel("HARBORLINE ROUTE", BLUE, 2.8, 1.5).shift(LEFT * 3.7)
        impl1 = self.list_badges(["MODEL", "TOOLS", "POLICY", "RUNTIME"], [BLUE, GOLD, VIOLET, MUTED], x=0, y=0.2, width=1.85, scale=0.62)
        effects1 = self.list_badges(["FAILURE", "AUTHORITY", "EVIDENCE", "RECOVERY"], [RED, RED, VIOLET, RESIDUAL], x=3.35, y=0.2, width=2.0, scale=0.62)
        e1 = VGroup(*[Arrow(route1.get_right(), impl1[i].get_left(), color=BLUE, stroke_width=2, buff=0.1) for i in range(len(impl1))], *[Arrow(impl1.get_right(), effects1[i].get_left(), color=RED, stroke_width=2, buff=0.1) for i in range(len(effects1))])
        s1 = VGroup(f1, route1, impl1, effects1, e1)
        self.play_beat(1, FadeIn(s1), LaggedStart(*[GrowArrow(x) for x in e1], lag_ratio=0.06), settle=0.9)

        # 2 — silent substitution consequence
        f2 = self.frame("UPGRADE · TRUST TERMS MOVED", RED)
        old2 = self.panel("OLD FIELD", GOLD, 2.45, 1.45).shift(LEFT * 3.5 + UP * 0.4)
        new2 = self.panel("NEW ARTIFACT", BLUE, 2.45, 1.45).shift(RIGHT * 0.1 + UP * 0.4)
        losses2 = self.list_badges(["STATE STRANDED", "REGRESSION ERASED", "PERMISSION WIDENED"], [RED, RESIDUAL, RED], x=2.85, y=-0.85, width=2.45, scale=0.64)
        e2 = Arrow(old2.get_right(), new2.get_left(), color=GOLD, stroke_width=3, buff=0.1)
        cross2 = Cross(new2, stroke_color=RED, stroke_width=3)
        s2 = VGroup(f2, old2, new2, losses2, e2, cross2)
        self.play_beat(2, FadeOut(s1), FadeIn(s2), GrowArrow(e2), Create(cross2), LaggedStart(*[FadeIn(x) for x in losses2], lag_ratio=0.12), settle=0.9)

        # 3 — field versus implementation
        f3 = self.frame("FIELD = PROMISE · CANDIDATE = REALIZATION", GOLD)
        field3 = self.panel("FIELD CONTRACT", GOLD, 3.1, 2.0).shift(LEFT * 2.8)
        cand31 = self.panel("CANDIDATE A", BLUE, 2.35, 1.2).shift(RIGHT * 1.5 + UP * 0.85)
        cand32 = self.panel("CANDIDATE B", VIOLET, 2.35, 1.2).shift(RIGHT * 1.5 + DOWN * 0.85)
        e3 = VGroup(Arrow(field3.get_right(), cand31.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(field3.get_right(), cand32.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        s3 = VGroup(f3, field3, cand31, cand32, e3)
        self.play_beat(3, FadeOut(s2), FadeIn(s3), LaggedStart(*[GrowArrow(x) for x in e3], lag_ratio=0.12), Indicate(field3), settle=0.8)

        # 4 — semantic and authority fields
        f4 = self.frame("OBSERVABLE SEMANTICS + AUTHORITY", BLUE)
        contract4 = self.panel("FIELD", GOLD, 2.35, 1.55).shift(LEFT * 4.0)
        semantics4 = self.list_badges(["INPUT", "OUTPUT", "ABSTAIN", "FAILURE", "RESOURCE"], [BLUE, GREEN, MUTED, RED, GOLD], x=-1.5, y=0.25, width=1.65, scale=0.58)
        auth4 = self.list_badges(["CONSUMER", "TOOL", "DATA", "SIDE EFFECT"], [VIOLET, RED, BLUE, RESIDUAL], x=2.2, y=0.25, width=1.8, scale=0.6)
        ceiling4 = self.badge("AUTHORITY CEILING", RED, 2.9).shift(RIGHT * 3.55 + DOWN * 1.55)
        e4 = VGroup(*[Arrow(contract4.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in semantics4], *[Arrow(contract4.get_right(), x.get_left(), color=RED, stroke_width=2, buff=0.1) for x in auth4], Arrow(auth4.get_right(), ceiling4.get_left(), color=RED, stroke_width=2, buff=0.1))
        s4 = VGroup(f4, contract4, semantics4, auth4, ceiling4, e4)
        self.play_beat(4, FadeOut(s3), FadeIn(s4), LaggedStart(*[FadeIn(x) for x in semantics4], lag_ratio=0.08), LaggedStart(*[FadeIn(x) for x in auth4], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e4], lag_ratio=0.05), FadeIn(ceiling4), settle=0.9)

        # 5 — history and recovery belong to the field
        f5 = self.frame("FIELD OWNS HISTORY + RECOVERY", GREEN)
        field5 = self.panel("FIELD", GOLD, 2.25, 1.45).shift(LEFT * 4.0)
        history5 = self.list_badges(["LEASE", "EVALUATOR", "INCIDENT", "REGRESSION"], [BLUE, VIOLET, RED, RESIDUAL], x=-1.45, y=0.2, width=1.8, scale=0.58)
        recovery5 = self.list_badges(["MIGRATE", "RESTORE", "COMPENSATE", "OWNER"], [GOLD, GREEN, RESIDUAL, RED], x=1.7, y=0.2, width=1.9, scale=0.58)
        ledger5 = self.badge("EFFECT-COMPLETE RECOVERY", GREEN, 3.5).shift(RIGHT * 3.35 + DOWN * 1.45)
        e5 = VGroup(*[Arrow(field5.get_right(), x.get_left(), color=BLUE, stroke_width=2, buff=0.1) for x in history5], *[Arrow(field5.get_right(), x.get_left(), color=GREEN, stroke_width=2, buff=0.1) for x in recovery5], Arrow(recovery5.get_right(), ledger5.get_left(), color=GREEN, stroke_width=2, buff=0.1))
        s5 = VGroup(f5, field5, history5, recovery5, ledger5, e5)
        self.play_beat(5, FadeOut(s4), FadeIn(s5), LaggedStart(*[FadeIn(x) for x in history5], lag_ratio=0.08), LaggedStart(*[FadeIn(x) for x in recovery5], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e5], lag_ratio=0.05), settle=0.8)

        # 6 — test boundary
        f6 = self.frame("NOW TEST THE SCOPE", BLUE)
        desk6 = self.panel("FINITE TEST DESK", BLUE, 3.1, 1.65).shift(LEFT * 2.1)
        boundary6 = self.badge("DESIGN → ENCODED TEST", GOLD, 3.0).shift(RIGHT * 2.6 + UP * 0.85)
        no6 = self.badge("NOT DEPLOYMENT", RED, 2.6).shift(RIGHT * 2.6 + DOWN * 0.85)
        e6 = VGroup(Arrow(desk6.get_right(), boundary6.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(desk6.get_right(), no6.get_left(), color=RED, stroke_width=3, buff=0.1))
        s6 = VGroup(f6, desk6, boundary6, no6, e6)
        self.play_beat(6, FadeOut(s5), FadeIn(s6), LaggedStart(*[GrowArrow(x) for x in e6], lag_ratio=0.12), FadeIn(boundary6), FadeIn(no6), settle=0.5)

        # 7 — finite positive and negative controls
        f7 = self.frame("FINITE SYNTHETIC CONTROLS", GOLD)
        valid7 = self.list_badges(["VALID ×3", "TRACE ×2"], [GREEN, BLUE], x=-2.8, y=0.35, width=2.0, scale=0.72)
        invalid7 = self.list_badges(["INVALID ×6", "REJECT ×6"], [RED, RESIDUAL], x=1.0, y=0.35, width=2.1, scale=0.72)
        scope7 = self.badge("ENCODED SCOPE ONLY", MUTED, 3.0).shift(RIGHT * 3.35 + DOWN * 1.3)
        e7 = VGroup(Arrow(valid7.get_right(), invalid7.get_left(), color=GOLD, stroke_width=3, buff=0.15), Arrow(invalid7.get_right(), scope7.get_left(), color=MUTED, stroke_width=2, buff=0.1))
        s7 = VGroup(f7, valid7, invalid7, scope7, e7)
        self.play_beat(7, FadeOut(s6), FadeIn(s7), LaggedStart(*[FadeIn(x) for x in valid7], lag_ratio=0.12), LaggedStart(*[FadeIn(x) for x in invalid7], lag_ratio=0.12), LaggedStart(*[GrowArrow(x) for x in e7], lag_ratio=0.12), FadeIn(scope7), settle=0.9)

        # 8 — formal lane separate from runtime lane
        f8 = self.frame("FORMAL LANE ≠ RUNTIME LANE", VIOLET)
        formal8 = self.panel("FORMAL LEDGER", VIOLET, 2.65, 1.45).shift(LEFT * 2.9 + UP * 0.9)
        runtime8 = self.panel("RUNTIME FIXTURES", BLUE, 2.65, 1.45).shift(LEFT * 2.9 + DOWN * 0.9)
        target8 = self.list_badges(["TARGET 1", "TARGET 2", "TARGET 3", "TARGET 4"], [VIOLET, VIOLET, VIOLET, VIOLET], x=1.8, y=0.2, width=1.8, scale=0.55)
        no8 = self.badge("NOT ONE PROOF", RED, 2.7).shift(RIGHT * 3.45 + DOWN * 1.5)
        e8 = VGroup(Arrow(formal8.get_right(), target8.get_left(), color=VIOLET, stroke_width=2, buff=0.1), Arrow(runtime8.get_right(), target8.get_left(), color=BLUE, stroke_width=2, buff=0.1), Arrow(target8.get_right(), no8.get_left(), color=RED, stroke_width=2, buff=0.1))
        s8 = VGroup(f8, formal8, runtime8, target8, no8, e8)
        self.play_beat(8, FadeOut(s7), FadeIn(s8), FadeIn(formal8), FadeIn(runtime8), LaggedStart(*[FadeIn(x) for x in target8], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e8], lag_ratio=0.08), FadeIn(no8), settle=0.6)

        # 9 — evidence ceiling
        f9 = self.frame("SCOPED · FINITE · NO PROMOTION", RED)
        inside9 = self.panel("TESTED OBLIGATIONS", GREEN, 3.0, 1.65).shift(LEFT * 2.4)
        outside9 = self.list_badges(["EQUIVALENCE?", "COMPOSITION?", "PRODUCTION?"], [RED, RED, RED], x=2.55, y=0.45, width=2.4, scale=0.62)
        bound9 = DashedLine(UP * 2.35, DOWN * 2.35, color=RED, stroke_width=3).shift(RIGHT * 0.2)
        crosses9 = VGroup(*[Cross(x, stroke_color=RED, stroke_width=2.5) for x in outside9])
        s9 = VGroup(f9, inside9, outside9, bound9, crosses9)
        self.play_beat(9, FadeOut(s8), FadeIn(s9), Create(bound9), FadeIn(inside9), LaggedStart(*[FadeIn(x) for x in outside9], lag_ratio=0.1), LaggedStart(*[Create(x) for x in crosses9], lag_ratio=0.1), settle=0.9)

        # 10 — identity laundering and interface theater
        f10 = self.frame("SAME SCHEMA · DIFFERENT EFFECT", RED)
        schema10 = self.badge("MATCHING SCHEMA", BLUE, 2.65).shift(LEFT * 3.35 + UP * 1.05)
        behavior10 = self.panel("CHANGED FAILURE", RED, 2.65, 1.4).shift(RIGHT * 0.1 + UP * 1.05)
        effect10 = self.panel("PROTECTED EFFECT", RED, 2.65, 1.4).shift(RIGHT * 0.1 + DOWN * 0.95)
        id10 = self.badge("IDENTITY LAUNDERED", RESIDUAL, 3.0).shift(RIGHT * 3.3 + DOWN * 1.45)
        e10 = VGroup(Arrow(schema10.get_right(), behavior10.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(schema10.get_right(), effect10.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(effect10.get_right(), id10.get_left(), color=RESIDUAL, stroke_width=2, buff=0.1))
        c10 = VGroup(Cross(behavior10, stroke_color=RED, stroke_width=3), Cross(effect10, stroke_color=RED, stroke_width=3))
        s10 = VGroup(f10, schema10, behavior10, effect10, id10, e10, c10)
        self.play_beat(10, FadeOut(s9), FadeIn(s10), GrowArrow(e10[0]), GrowArrow(e10[1]), FadeIn(behavior10), FadeIn(effect10), Create(c10[0]), Create(c10[1]), FadeIn(id10), settle=0.9)

        # 11 — scope overreach and composition
        f11 = self.frame("ONE LEASE ≠ ALL USES", RED)
        lease11 = self.panel("LOW-STAKES LEASE", GREEN, 2.6, 1.5).shift(LEFT * 3.3)
        uses11 = self.list_badges(["DRAFT", "PUBLISH", "SPEND", "ACTUATE"], [GREEN, RED, RED, RED], x=0.3, y=0.25, width=1.9, scale=0.62)
        toxic11 = self.panel("TOXIC COMPOSITION", RED, 2.7, 1.5).shift(RIGHT * 3.2 + DOWN * 1.0)
        e11 = VGroup(*[Arrow(lease11.get_right(), x.get_left(), color=GOLD if i == 0 else RED, stroke_width=2, buff=0.1) for i, x in enumerate(uses11)], Arrow(uses11.get_right(), toxic11.get_left(), color=RED, stroke_width=3, buff=0.1))
        c11 = VGroup(Cross(uses11[1], stroke_color=RED, stroke_width=2.5), Cross(uses11[2], stroke_color=RED, stroke_width=2.5), Cross(uses11[3], stroke_color=RED, stroke_width=2.5))
        s11 = VGroup(f11, lease11, uses11, toxic11, e11, c11)
        self.play_beat(11, FadeOut(s10), FadeIn(s11), LaggedStart(*[GrowArrow(x) for x in e11], lag_ratio=0.07), LaggedStart(*[Create(x) for x in c11], lag_ratio=0.1), FadeIn(toxic11), settle=0.9)

        # 12 — uncertainty destinations
        f12 = self.frame("UNKNOWN → CONTROLLED DESTINATION", GOLD)
        unknown12 = self.panel("UNKNOWN", MUTED, 2.4, 1.45).shift(LEFT * 3.7)
        dest12 = self.list_badges(["STOP", "SHADOW", "QUARANTINE", "COMPENSATE", "OWN RESIDUAL"], [RED, MUTED, RED, GOLD, RESIDUAL], x=0.6, y=0.2, width=2.1, scale=0.58)
        e12 = VGroup(*[Arrow(unknown12.get_right(), x.get_left(), color=dest12[i][1].get_color() if len(dest12[i]) > 1 else MUTED, stroke_width=2, buff=0.1) for i, x in enumerate(dest12)])
        s12 = VGroup(f12, unknown12, dest12, e12)
        self.play_beat(12, FadeOut(s11), FadeIn(s12), FadeIn(unknown12), LaggedStart(*[FadeIn(x) for x in dest12], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e12], lag_ratio=0.06), settle=0.7)

        # 13 — support state
        f13 = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
        support13 = self.panel("SUPPORT STATE", GOLD, 2.9, 1.55).shift(LEFT * 3.0)
        targets13 = self.list_badges(["REFINEMENT", "COMPOSITION", "INDEPENDENCE", "ROLLBACK"], [MUTED, MUTED, MUTED, RESIDUAL], x=1.7, y=0.25, width=2.0, scale=0.58)
        open13 = self.badge("PROOF TARGETS OPEN", RED, 3.0).shift(RIGHT * 3.35 + DOWN * 1.45)
        e13 = VGroup(*[DashedLine(support13.get_right(), x.get_left(), color=MUTED, stroke_width=2) for x in targets13], Arrow(targets13.get_right(), open13.get_left(), color=RED, stroke_width=2, buff=0.1))
        s13 = VGroup(f13, support13, targets13, open13, e13)
        self.play_beat(13, FadeOut(s12), FadeIn(s13), FadeIn(support13), LaggedStart(*[FadeIn(x) for x in targets13], lag_ratio=0.08), LaggedStart(*[Create(x) for x in e13], lag_ratio=0.08), FadeIn(open13), settle=0.9)

        # 14 — fail-closed validator
        f14 = self.frame("IDENTITY MISMATCH · AUTHORITY DELTA · REJECT", RED)
        request14 = self.panel("CANDIDATE", BLUE, 2.35, 1.4).shift(LEFT * 3.7 + UP * 0.8)
        validator14 = self.panel("VALIDATOR", GOLD, 2.45, 1.5).shift(LEFT * 0.5)
        reject14 = self.panel("REJECT", RED, 2.35, 1.4).shift(RIGHT * 3.0 + UP * 0.8)
        auth14 = self.badge("AUTHORITY +?", RED, 2.1).shift(LEFT * 3.7 + DOWN * 1.25)
        e14 = VGroup(Arrow(request14.get_right(), validator14.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(auth14.get_right(), validator14.get_left(), color=RED, stroke_width=2, buff=0.1), Arrow(validator14.get_right(), reject14.get_left(), color=RED, stroke_width=3, buff=0.1))
        c14 = Cross(reject14, stroke_color=RED, stroke_width=3)
        s14 = VGroup(f14, request14, validator14, reject14, auth14, e14, c14)
        self.play_beat(14, FadeOut(s13), FadeIn(s14), GrowArrow(e14[0]), GrowArrow(e14[1]), GrowArrow(e14[2]), FadeIn(auth14), Create(c14), settle=0.7)

        # 15 — no promotion
        f15 = self.frame("NO PROMOTION · NO DEPLOYMENT PROOF", RED)
        local15 = self.panel("LOCAL ARTIFACTS", GREEN, 2.65, 1.5).shift(LEFT * 3.5)
        claims15 = self.list_badges(["SAFETY", "TRANSFER", "AGI", "ASI"], [RED, RED, RED, RED], x=1.3, y=0.2, width=1.8, scale=0.65)
        bound15 = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(LEFT * 0.25)
        arrows15 = VGroup(*[Arrow(local15.get_right(), x.get_left(), color=RED, stroke_width=2, buff=0.1) for x in claims15])
        crosses15 = VGroup(*[Cross(x, stroke_color=RED, stroke_width=2.5) for x in claims15])
        s15 = VGroup(f15, local15, claims15, bound15, arrows15, crosses15)
        self.play_beat(15, FadeOut(s14), FadeIn(s15), Create(bound15), LaggedStart(*[GrowArrow(x) for x in arrows15], lag_ratio=0.1), LaggedStart(*[Create(x) for x in crosses15], lag_ratio=0.1), settle=0.9)

        # 16 — preserve source evidence ceiling
        f16 = self.frame("DERIVATIVE · SAME EVIDENCE CEILING", BLUE)
        source16 = self.panel("SOURCE CHAPTER", BLUE, 2.7, 1.5).shift(LEFT * 3.4)
        visual16 = self.panel("VISUAL DERIVATIVE", GOLD, 2.7, 1.5).shift(RIGHT * 1.0)
        ceiling16 = self.badge("CEILING PRESERVED", GREEN, 3.0).shift(RIGHT * 3.6 + DOWN * 1.25)
        e16 = VGroup(Arrow(source16.get_right(), visual16.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(visual16.get_right(), ceiling16.get_left(), color=GREEN, stroke_width=2, buff=0.1))
        s16 = VGroup(f16, source16, visual16, ceiling16, e16)
        self.play_beat(16, FadeOut(s15), FadeIn(s16), GrowArrow(e16[0]), GrowArrow(e16[1]), FadeIn(ceiling16), Indicate(ceiling16), settle=0.6)

        # 17 — handoff to replacement transaction
        f17 = self.frame("NEXT · CAPABILITY REPLACEMENT + ROLLBACK", GOLD)
        field17 = self.panel("STABLE FIELD", GOLD, 2.7, 1.5).shift(LEFT * 3.4)
        transaction17 = self.panel("REPLACEMENT TX", GREEN, 2.8, 1.5).shift(RIGHT * 2.0)
        recovery17 = self.badge("RECOVERY DUTY", RESIDUAL, 2.7).shift(RIGHT * 3.65 + DOWN * 1.35)
        e17 = VGroup(Arrow(field17.get_right(), transaction17.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(transaction17.get_right(), recovery17.get_left(), color=RESIDUAL, stroke_width=2, buff=0.1))
        s17 = VGroup(f17, field17, transaction17, recovery17, e17)
        self.play_beat(17, FadeOut(s16), FadeIn(s17), GrowArrow(e17[0]), GrowArrow(e17[1]), FadeIn(recovery17), settle=0.8)

        # 18 — field-owned continuity
        f18 = self.frame("FIELD OWNS THE PROMISE · GAPS REMAIN VISIBLE", GOLD)
        field18 = self.panel("FIELD CONTRACT", GOLD, 3.1, 1.7).shift(LEFT * 2.7)
        tags18 = self.list_badges(["SOURCES", "INVARIANTS", "FAILURES", "TESTS", "OPEN GAPS"], [BLUE, GREEN, RED, VIOLET, RESIDUAL], x=1.25, y=0.25, width=1.8, scale=0.58)
        recovery18 = self.badge("ACCOUNTABLE RECOVERY", RESIDUAL, 3.1).shift(RIGHT * 3.45 + DOWN * 1.55)
        e18 = VGroup(*[Arrow(field18.get_right(), x.get_left(), color=GOLD, stroke_width=2, buff=0.1) for x in tags18], Arrow(tags18.get_right(), recovery18.get_left(), color=RESIDUAL, stroke_width=2, buff=0.1))
        s18 = VGroup(f18, field18, tags18, recovery18, e18)
        self.play_beat(18, FadeOut(s17), FadeIn(s18), LaggedStart(*[FadeIn(x) for x in tags18], lag_ratio=0.08), LaggedStart(*[GrowArrow(x) for x in e18], lag_ratio=0.06), FadeIn(recovery18), Indicate(field18), settle=1.1)


__all__ = ["StableCapabilityFieldsGeneration2"]
