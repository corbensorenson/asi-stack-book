"""Generation-two animatic for Stable Capability Fields.

One fictional notice route keeps its name while candidate implementations are
tested against a consumer-owned semantic and authority gauge. The geometry is
an explanatory model, not evidence of complete or deployed qualification.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    Arrow,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    Group,
    LaggedStart,
    LEFT,
    Line,
    RIGHT,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    UP,
    VGroup,
    Wait,
    Write,
)

from visual_edition.lib.asi_visuals import (
    ACCENT,
    AUTHORITY,
    BACKGROUND,
    BOUNDARY,
    EVIDENCE,
    INK,
    MUTED,
    RESIDUAL,
    ROLLBACK,
    SURFACE,
    AsiScene,
    text,
)


FIELD = "#F2BD63"
OLD = "#67D5F2"
NEW = "#9C82E8"
PASS = "#66D58A"
FAIL = "#FF6073"


class StableCapabilityFieldsGeneration2(AsiScene):
    TARGET_DURATION = 205.505
    ENDS = [24.575, 50.975, 83.475, 127.445, 168.640, 205.505]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = BACKGROUND

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def beat(self, index: int, sequence: Succession, settle: float = 0.7) -> None:
        """Play one auditable semantic sequence across a coarse audio block."""
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        action_time = max(0.05, remaining - min(settle, remaining * 0.12))
        children = list(sequence.animations)
        run_times = []
        for child in children:
            if isinstance(child, LaggedStart):
                run_times.append(1.50)
            elif isinstance(child, AnimationGroup):
                run_times.append(0.65)
            elif isinstance(child, (Transform, Circumscribe)):
                run_times.append(0.85)
            else:
                run_times.append(0.75)
        total_motion = sum(run_times)
        if total_motion > action_time:
            scale = action_time / total_motion
            run_times = [duration * scale for duration in run_times]
            gap = 0.0
        else:
            gap = (action_time - total_motion) / max(1, len(children) - 1)
        timed = []
        for position, (child, run_time) in enumerate(zip(children, run_times)):
            child.set_run_time(run_time)
            timed.append(child)
            if position < len(children) - 1 and gap > 0:
                timed.append(Wait(gap))
        self.play(Succession(*timed))
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL"):
        return text(value, size=size, color=color, weight=weight)

    def stage(self, title: str, color: str = FIELD) -> VGroup:
        shell = RoundedRectangle(
            width=12.2,
            height=6.45,
            corner_radius=0.18,
            color=BOUNDARY,
            stroke_width=1.8,
            fill_color=SURFACE,
            fill_opacity=0.40,
        )
        heading = self.label(title, 23, color, "BOLD").shift(UP * 3.33)
        rule = Line(LEFT * 5.7, RIGHT * 5.7, color=BOUNDARY, stroke_width=1.2).shift(DOWN * 2.72)
        return VGroup(shell, heading, rule)

    def chip(self, value: str, color: str, width: float = 1.45) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=0.42,
            corner_radius=0.08,
            color=color,
            stroke_width=2.1,
            fill_color=SURFACE,
            fill_opacity=0.96,
        )
        caption = self.label(value, 11, color, "BOLD")
        if caption.width > width - 0.16:
            caption.scale_to_fit_width(width - 0.16)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def nameplate(self) -> VGroup:
        plate = RoundedRectangle(
            width=3.65,
            height=0.72,
            corner_radius=0.08,
            color=FIELD,
            stroke_width=3,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        label = self.label("DRAFT NOTICE", 20, FIELD, "BOLD").move_to(plate)
        return VGroup(plate, label)

    def cartridge(
        self,
        label: str,
        color: str,
        *,
        spanish: bool = True,
        publish: bool = False,
    ) -> VGroup:
        body = RoundedRectangle(
            width=2.55,
            height=1.72,
            corner_radius=0.13,
            color=color,
            stroke_width=3,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        title = self.label(label, 16, color, "BOLD").move_to(body.get_center() + UP * 0.56)
        en = self.chip("EN", PASS, 0.60).move_to(body.get_center() + LEFT * 0.48 + UP * 0.02)
        es = self.chip("ES" if spanish else "ES —", PASS if spanish else FAIL, 0.66)
        es.move_to(body.get_center() + RIGHT * 0.43 + UP * 0.02)
        outlet = self.chip("PUBLISH" if publish else "PRIVATE", FAIL if publish else EVIDENCE, 1.35)
        outlet.move_to(body.get_center() + DOWN * 0.56)
        identity = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=1)
        identity.move_to(body.get_corner(UP + LEFT) + RIGHT * 0.18 + DOWN * 0.18)
        return VGroup(body, title, en, es, outlet, identity)

    def gauge(self) -> VGroup:
        shell = RoundedRectangle(
            width=4.30,
            height=3.45,
            corner_radius=0.18,
            color=FIELD,
            stroke_width=3.4,
            fill_color=SURFACE,
            fill_opacity=0.70,
        )
        owner = self.chip("HARBOR LINE PROMISE", FIELD, 2.45).next_to(shell, UP, buff=-0.10)
        requirements = VGroup(
            self.chip("EN + ES", PASS, 1.25),
            self.chip("PRIVATE", EVIDENCE, 1.25),
            self.chip("ABSTAIN", MUTED, 1.25),
            self.chip("EXPIRY", AUTHORITY, 1.25),
            self.chip("RECEIPT", RESIDUAL, 1.25),
        ).arrange(DOWN, buff=0.16).scale(0.90).move_to(shell.get_center() + LEFT * 1.30)
        aperture = RoundedRectangle(
            width=2.35,
            height=1.75,
            corner_radius=0.12,
            color=BOUNDARY,
            stroke_width=2.4,
        ).move_to(shell.get_center() + RIGHT * 0.77)
        fit = self.label("IMPLEMENTATION\nAPERTURE", 12, MUTED, "BOLD").move_to(aperture)
        return VGroup(shell, owner, requirements, aperture, fit)

    def workload(self, language: str, use: str, color: str) -> VGroup:
        card = RoundedRectangle(
            width=2.2,
            height=1.18,
            corner_radius=0.10,
            color=color,
            stroke_width=2.6,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        lang = self.label(language, 17, color, "BOLD").move_to(card.get_center() + UP * 0.23)
        purpose = self.label(use, 11, MUTED, "BOLD").move_to(card.get_center() + DOWN * 0.30)
        return VGroup(card, lang, purpose)

    def history_rail(self) -> VGroup:
        line = Line(LEFT * 4.7, RIGHT * 4.7, color=BOUNDARY, stroke_width=2)
        nodes = VGroup(
            self.chip("ES FAILURE", FAIL, 1.40),
            self.chip("TOOL DELTA", FAIL, 1.40),
            self.chip("LEASE", AUTHORITY, 1.15),
            self.chip("RECOVERY", RESIDUAL, 1.40),
        ).arrange(RIGHT, buff=0.60).scale(0.82).move_to(line)
        return VGroup(line, nodes)

    def focus_lens(self, target, color: str) -> RoundedRectangle:
        lens = RoundedRectangle(
            corner_radius=0.12,
            color=color,
            stroke_width=4.2,
            fill_color=color,
            fill_opacity=0.12,
        )
        lens.surround(target, buff=0.16)
        return lens

    def current(self) -> Group:
        return Group(*self.mobjects)

    def construct(self) -> None:
        # b01: familiar identity evidence leaves the consumer promise unanswered.
        frame1 = self.stage("THE UPGRADE THAT DOES NOT FIT", FIELD)
        plate1 = self.nameplate().shift(UP * 2.20)
        old1 = self.cartridge("OLD", OLD).shift(LEFT * 2.15 + DOWN * 0.05)
        new1 = self.cartridge("NEW", NEW).shift(RIGHT * 2.15 + DOWN * 0.05)
        interface = self.chip("SAME INTERFACE", ACCENT, 1.80).shift(UP * 1.15)
        signed = self.chip("SIGNED BUILD", EVIDENCE, 1.65).next_to(new1, UP, buff=0.18)
        clearer = self.chip("CLEARER ENGLISH", PASS, 1.80).next_to(new1, DOWN, buff=0.18)
        question = self.label("DEFAULT?", 25, INK, "BOLD").shift(DOWN * 2.14)
        focus1 = self.focus_lens(old1, OLD)
        new_focus1 = self.focus_lens(new1, NEW)
        question_focus1 = self.focus_lens(question, FIELD)
        self.beat(
            1,
            Succession(
                AnimationGroup(FadeIn(frame1), FadeIn(plate1), FadeIn(old1, shift=RIGHT * 0.24), lag_ratio=0),
                FadeIn(focus1), FadeIn(new1, shift=LEFT * 0.24), Transform(focus1, new_focus1),
                FadeIn(interface), FadeIn(signed), FadeIn(clearer), Write(question),
                Transform(focus1, question_focus1), Circumscribe(question, color=FIELD), FadeOut(focus1),
            ),
            settle=2.70,
        )

        # b02: the stable object is a gauge owned by the consumer.
        old_scene = self.current()
        frame2 = self.stage("THE PROMISE BELONGS TO THE CONSUMER", FIELD)
        gauge2 = self.gauge().shift(RIGHT * 1.55 + DOWN * 0.10)
        plate2 = self.nameplate().next_to(gauge2, UP, buff=0.18)
        old2 = self.cartridge("OLD", OLD).scale(0.76).move_to(gauge2[3])
        new2 = self.cartridge("NEW", NEW, spanish=False, publish=True).scale(0.76).shift(LEFT * 3.65)
        field_name = self.chip("STABLE CAPABILITY FIELD", FIELD, 2.75).shift(LEFT * 3.60 + DOWN * 1.85)
        field_arrow = Arrow(field_name.get_right(), gauge2.get_left(), color=FIELD, stroke_width=3, buff=0.14)
        focus2 = self.focus_lens(new2, NEW)
        requirements_focus2 = self.focus_lens(gauge2[2], FIELD)
        old_focus2 = self.focus_lens(old2, OLD)
        self.beat(
            2,
            Succession(
                AnimationGroup(FadeOut(old_scene), FadeIn(frame2), lag_ratio=0),
                FadeIn(new2, shift=RIGHT * 0.30), FadeIn(focus2), FadeIn(gauge2),
                Transform(focus2, requirements_focus2), FadeIn(plate2), FadeIn(old2, shift=LEFT * 0.24),
                FadeIn(field_name), GrowArrow(field_arrow), Transform(focus2, old_focus2),
                Circumscribe(gauge2[0], color=FIELD), FadeOut(focus2),
            ),
            settle=0.80,
        )

        # b03: one happy path hides opposite semantic and authority failures.
        old_scene = self.current()
        frame3 = self.stage("BETTER OUTPUT IS NOT SUBSTITUTION", FAIL)
        old3 = self.cartridge("OLD", OLD).scale(0.84).shift(LEFT * 3.55 + UP * 0.52)
        new3 = self.cartridge("NEW", NEW, spanish=False, publish=True).scale(0.84).shift(LEFT * 0.70 + UP * 0.52)
        en3 = self.workload("ENGLISH", "PRIVATE NOTICE", PASS).shift(RIGHT * 3.72 + UP * 1.55)
        es3 = self.workload("SPANISH", "PRIVATE NOTICE", FAIL).shift(RIGHT * 3.72 + DOWN * 0.10)
        draft3 = self.chip("DRAFT STORE", EVIDENCE, 1.65).shift(LEFT * 3.55 + DOWN * 1.48)
        publish3 = self.chip("PUBLISH TOOL", FAIL, 1.70).shift(LEFT * 0.70 + DOWN * 1.48)
        old_route = Arrow(old3.get_bottom(), draft3.get_top(), color=EVIDENCE, stroke_width=3, buff=0.10)
        new_route = Arrow(new3.get_bottom(), publish3.get_top(), color=FAIL, stroke_width=3, buff=0.10)
        language_links = VGroup(
            Arrow(en3.get_left(), old3.get_right(), color=PASS, stroke_width=2, buff=0.10),
            Arrow(en3.get_left(), new3.get_right(), color=PASS, stroke_width=2, buff=0.10),
            Arrow(es3.get_left(), new3.get_right(), color=FAIL, stroke_width=2, buff=0.10),
        )
        verdict = self.label("NARROWER SERVICE · WIDER EFFECT", 20, FAIL, "BOLD").shift(DOWN * 2.22)
        focus3 = self.focus_lens(new3, NEW)
        english_focus3 = self.focus_lens(en3, PASS)
        spanish_focus3 = self.focus_lens(es3, FAIL)
        outlets_focus3 = self.focus_lens(VGroup(draft3, publish3), FAIL)
        self.beat(
            3,
            Succession(
                AnimationGroup(FadeOut(old_scene), FadeIn(frame3), lag_ratio=0),
                FadeIn(old3, shift=RIGHT * 0.22), FadeIn(new3, shift=LEFT * 0.22), FadeIn(focus3),
                FadeIn(en3, shift=LEFT * 0.22), Transform(focus3, english_focus3),
                LaggedStart(*[GrowArrow(a) for a in language_links[:2]], lag_ratio=0.18),
                FadeIn(es3, shift=LEFT * 0.22), Transform(focus3, spanish_focus3),
                GrowArrow(language_links[2]), Circumscribe(new3[3], color=FAIL),
                FadeIn(draft3), FadeIn(publish3), GrowArrow(old_route), GrowArrow(new_route),
                Transform(focus3, outlets_focus3), Write(verdict), FadeOut(focus3),
            ),
            settle=0.90,
        )

        # b04: useful identity evidence supports a consequence-bounded canary.
        old_scene = self.current()
        frame4 = self.stage("BOUND CONSEQUENCES, NOT ONLY TRAFFIC", AUTHORITY)
        new4 = self.cartridge("NEW", NEW, spanish=False, publish=True).shift(LEFT * 2.85 + UP * 0.28)
        version4 = self.chip("VERSIONED", ACCENT, 1.45).next_to(new4, UP, buff=0.18)
        provenance4 = self.chip("PROVENANCE", EVIDENCE, 1.55).next_to(version4, RIGHT, buff=0.18)
        sleeve4 = SurroundingRectangle(new4, color=AUTHORITY, buff=0.33, stroke_width=3.2)
        lease4 = self.chip("CANARY LEASE", AUTHORITY, 1.75).next_to(sleeve4, DOWN, buff=0.16)
        terms4 = VGroup(
            self.chip("HARBOR LINE", FIELD, 1.55),
            self.chip("PRIVATE ONLY", EVIDENCE, 1.55),
            self.chip("EXPIRY", AUTHORITY, 1.25),
            self.chip("PUBLISH BLOCKED", FAIL, 1.80),
        ).arrange(DOWN, buff=0.20).shift(RIGHT * 0.75 + UP * 0.45)
        fallback4 = self.cartridge("OLD", OLD).scale(0.72).shift(RIGHT * 3.72 + UP * 1.25)
        fallback_tag = self.chip("FALLBACK", PASS, 1.20).next_to(fallback4, DOWN, buff=0.14)
        effects4 = VGroup(
            self.chip("PUBLISH", FAIL, 1.20),
            self.chip("SPEND", FAIL, 1.10),
            self.chip("DURABLE STATE", FAIL, 1.55),
            self.chip("DESCENDANTS", FAIL, 1.50),
        ).arrange(RIGHT, buff=0.24).scale(0.82).shift(DOWN * 1.95)
        stop4 = DashedLine(LEFT * 0.75, RIGHT * 4.80, color=FAIL, stroke_width=2.8).shift(DOWN * 1.45)
        focus4 = self.focus_lens(new4, NEW)
        lease_focus4 = self.focus_lens(sleeve4, AUTHORITY)
        terms_focus4 = self.focus_lens(terms4, FIELD)
        fallback_focus4 = self.focus_lens(fallback4, OLD)
        effects_focus4 = self.focus_lens(effects4, FAIL)
        self.beat(
            4,
            Succession(
                AnimationGroup(FadeOut(old_scene), FadeIn(frame4), lag_ratio=0),
                FadeIn(new4, shift=RIGHT * 0.24), FadeIn(focus4),
                FadeIn(version4), FadeIn(provenance4), Create(sleeve4), FadeIn(lease4),
                Transform(focus4, lease_focus4),
                LaggedStart(*[FadeIn(x) for x in terms4], lag_ratio=0.16), Transform(focus4, terms_focus4),
                FadeIn(fallback4, shift=LEFT * 0.24), FadeIn(fallback_tag), Transform(focus4, fallback_focus4),
                Create(stop4),
                LaggedStart(*[FadeIn(x) for x in effects4], lag_ratio=0.14),
                Transform(focus4, effects_focus4), Circumscribe(stop4, color=FAIL), FadeOut(focus4),
            ),
            settle=0.90,
        )

        # b05: repair does not transfer a lease to a changed use; history persists.
        old_scene = self.current()
        frame5 = self.stage("A REPAIRED LEASE IS STILL SCOPED", RESIDUAL)
        harbor5 = self.workload("HARBOR LINE", "PRIVATE DRAFT", FIELD).shift(LEFT * 3.85 + UP * 1.38)
        city5 = self.workload("CITY PUBLISHER", "LIVE EMERGENCY", FAIL).shift(RIGHT * 3.85 + UP * 1.38)
        bands_left = VGroup(
            self.chip("CONSUMER: HARBOR", FIELD, 1.70),
            self.chip("USE: DRAFT", EVIDENCE, 1.45),
            self.chip("AUTH: PRIVATE", AUTHORITY, 1.60),
        ).arrange(DOWN, buff=0.18).shift(LEFT * 2.05 + UP * 0.08)
        bands_right = VGroup(
            self.chip("CONSUMER: CITY", FAIL, 1.70),
            self.chip("USE: LIVE", FAIL, 1.45),
            self.chip("AUTH: PUBLISH", FAIL, 1.60),
        ).arrange(DOWN, buff=0.18).shift(RIGHT * 2.05 + UP * 0.08)
        compare5 = DashedLine(UP * 1.0, DOWN * 1.35, color=BOUNDARY, stroke_width=2.4)
        decision5 = self.chip("NEW FIELD DECISION", FAIL, 2.25).shift(DOWN * 1.36)
        history5 = self.history_rail().scale(0.84).shift(DOWN * 2.22)
        invalidators5 = VGroup(
            self.chip("EVALUATOR Δ", RESIDUAL, 1.35),
            self.chip("TOOL Δ", RESIDUAL, 1.10),
            self.chip("AUDIENCE Δ", RESIDUAL, 1.35),
        ).arrange(RIGHT, buff=0.26).scale(0.82).shift(UP * 2.35)
        focus5 = self.focus_lens(harbor5, FIELD)
        left_focus5 = self.focus_lens(bands_left, FIELD)
        city_focus5 = self.focus_lens(city5, FAIL)
        right_focus5 = self.focus_lens(bands_right, FAIL)
        decision_focus5 = self.focus_lens(decision5, FAIL)
        history_focus5 = self.focus_lens(history5, RESIDUAL)
        self.beat(
            5,
            Succession(
                AnimationGroup(FadeOut(old_scene), FadeIn(frame5), lag_ratio=0),
                FadeIn(harbor5, shift=RIGHT * 0.24), FadeIn(focus5),
                LaggedStart(*[FadeIn(x) for x in bands_left], lag_ratio=0.16), Transform(focus5, left_focus5),
                FadeIn(city5, shift=LEFT * 0.24), Transform(focus5, city_focus5), Create(compare5),
                LaggedStart(*[FadeIn(x) for x in bands_right], lag_ratio=0.16), Transform(focus5, right_focus5),
                Circumscribe(bands_right, color=FAIL), FadeIn(decision5), Transform(focus5, decision_focus5),
                FadeIn(history5), Transform(focus5, history_focus5),
                LaggedStart(*[FadeIn(x) for x in invalidators5], lag_ratio=0.16),
                Circumscribe(history5, color=RESIDUAL), FadeOut(focus5),
            ),
            settle=0.90,
        )

        # b06: finite proof boundary and signature scoped inheritance image.
        old_scene = self.current()
        frame6 = self.stage("INHERIT ONLY INSIDE EVIDENCED SCOPE", FIELD)
        proof6 = RoundedRectangle(
            width=5.0,
            height=3.50,
            corner_radius=0.16,
            color=PASS,
            stroke_width=3,
            fill_color=SURFACE,
            fill_opacity=0.72,
        ).shift(LEFT * 2.75 + UP * 0.22)
        proof_title = self.chip("FINITE MODEL", PASS, 1.55).next_to(proof6, UP, buff=-0.10)
        proven6 = VGroup(
            self.chip("AUTHORED IDENTITY", PASS, 1.75),
            self.chip("NO AUTHORITY WIDENING", PASS, 2.10),
            self.chip("REQUIRED EVENTS", PASS, 1.65),
            self.chip("SYNTHETIC CONTROLS", PASS, 1.90),
        ).arrange(DOWN, buff=0.22).move_to(proof6)
        boundary6 = DashedLine(UP * 2.25, DOWN * 1.60, color=BOUNDARY, stroke_width=2.6).shift(RIGHT * 0.18)
        limits6 = VGroup(
            self.chip("REAL EQUIVALENCE", FAIL, 1.75),
            self.chip("INDEPENDENT EVALUATOR", FAIL, 2.15),
            self.chip("DEPLOYED ENFORCEMENT", FAIL, 2.15),
            self.chip("EFFECT REVERSAL", FAIL, 1.75),
        ).arrange(DOWN, buff=0.22).shift(RIGHT * 3.05 + UP * 0.22)
        not6 = self.label("NOT ESTABLISHED", 18, FAIL, "BOLD").next_to(limits6, UP, buff=0.20)
        plate6 = self.nameplate().scale(0.78).shift(DOWN * 2.05)
        old6 = self.chip("OLD · DEFAULT", OLD, 1.65).next_to(plate6, LEFT, buff=0.26)
        new6 = self.chip("NEW · CANARY", NEW, 1.65).next_to(plate6, RIGHT, buff=0.26)
        focus6 = self.focus_lens(proof6, PASS)
        limits_focus6 = self.focus_lens(VGroup(not6, limits6), FAIL)
        route_focus6 = self.focus_lens(VGroup(old6, plate6, new6), FIELD)
        self.beat(
            6,
            Succession(
                AnimationGroup(FadeOut(old_scene), FadeIn(frame6), lag_ratio=0),
                Create(proof6), FadeIn(proof_title), FadeIn(focus6),
                LaggedStart(*[FadeIn(x) for x in proven6], lag_ratio=0.16), Create(boundary6),
                Write(not6), LaggedStart(*[FadeIn(x) for x in limits6], lag_ratio=0.16),
                Transform(focus6, limits_focus6), FadeIn(plate6), FadeIn(old6), FadeIn(new6),
                Transform(focus6, route_focus6), Circumscribe(VGroup(old6, plate6, new6), color=FIELD),
                FadeOut(focus6),
            ),
            settle=1.20,
        )
