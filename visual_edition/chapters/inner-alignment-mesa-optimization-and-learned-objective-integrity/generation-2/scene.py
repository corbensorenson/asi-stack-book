"""Generation-2 visual abstract for inner alignment and learned-objective integrity.

One synthetic parcel-sorting lab keeps the distinction between intended target,
learning signal, policy, and objective hypothesis visible through a causal swap,
evidence custody, opportunity expansion, mitigation ambiguity, and finite proof.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn, FadeOut, GrowArrow,
    GrowFromCenter, Indicate, LaggedStart, LEFT, Line, MoveAlongPath, ORIGIN,
    Rectangle, ReplacementTransform, RIGHT, RoundedRectangle, Text, Transform,
    TransformFromCopy, UP, DOWN, VGroup, Write,
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


class InnerAlignmentGeneration2(AsiScene):
    TARGET_DURATION = 436.930
    ENDS = [
        10.755, 21.210, 32.140, 43.695, 57.575, 68.655, 79.610, 90.390,
        103.945, 116.500, 127.130, 139.310, 149.990, 163.820, 180.325,
        194.030, 209.785, 225.615, 239.995, 254.400, 269.630, 282.510,
        295.890, 311.495, 324.325, 339.255, 354.885, 369.390, 385.095,
        403.275, 418.355, 436.930,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#0D1D26"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.45) -> None:
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

    def badge(self, value: str, color: str, width: float = 2.0, height: float = 0.52) -> VGroup:
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

    def panel(self, title: str, color: str, width: float = 3.0, height: float = 1.6) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            stroke_color=color, stroke_width=3.5,
            fill_color=DEEP, fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.24, 3.6), 0.45).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def crate(self, kind: str = "INSULIN", *, seal: bool = True, stripe: bool = True) -> VGroup:
        color = GREEN if kind == "INSULIN" else MUTED
        body = RoundedRectangle(width=1.7, height=1.05, corner_radius=0.14,
                                stroke_color=color, stroke_width=3,
                                fill_color=DEEP, fill_opacity=1)
        title = self.label(kind, 15, color, "BOLD").move_to(body).shift(UP * 0.26)
        marks = VGroup()
        if seal:
            marks.add(self.badge("SEAL", BLUE, 0.74, 0.3).scale(0.65).move_to(body).shift(DOWN * 0.28 + LEFT * 0.36))
        if stripe:
            marks.add(self.badge("STRIPE", GREEN, 0.9, 0.3).scale(0.65).move_to(body).shift(DOWN * 0.28 + RIGHT * 0.32))
        return VGroup(body, title, marks)

    def lab_frame(self, title: str, color: str = GOLD) -> VGroup:
        frame = RoundedRectangle(width=11.7, height=6.2, corner_radius=0.2,
                                 stroke_color=BOUNDARY, stroke_width=2,
                                 fill_color="#0F2029", fill_opacity=1)
        heading = self.badge(title, color, 3.8, 0.58).shift(UP * 2.72)
        return VGroup(frame, heading)

    def conveyor(self, *, y: float = -0.25, left: float = -5.2, right: float = 4.9) -> VGroup:
        upper = Line(LEFT * -0.0, RIGHT * 0.0)
        upper = Line(ORIGIN, RIGHT * (right - left), color=BOUNDARY, stroke_width=5).shift(LEFT * (-left) + UP * y)
        lower = upper.copy().shift(DOWN * 0.28)
        arrows = VGroup(*[
            Arrow(ORIGIN, RIGHT * 0.58, color=MUTED, stroke_width=2, buff=0).shift(LEFT * 3.9 + RIGHT * i * 1.35 + UP * (y - 0.14))
            for i in range(6)
        ])
        return VGroup(upper, lower, arrows)

    def route(self, label: str, color: str, y: float, endpoint: str, *, wrong: bool = False) -> VGroup:
        rail = Line(LEFT * 4.8 + UP * y, RIGHT * 3.5 + UP * y, color=color, stroke_width=4)
        arrow = Arrow(LEFT * 3.1 + UP * y, RIGHT * 3.5 + UP * y, color=color, stroke_width=4, buff=0.05)
        name = self.badge(label, color, 2.25).shift(LEFT * 4.0 + UP * (y + 0.55))
        destination = self.badge(endpoint, RED if wrong else GREEN, 2.2).shift(RIGHT * 4.55 + UP * y)
        return VGroup(rail, arrow, name, destination)

    def matrix(self, names: list[str], colors: list[str], *, x: float = 2.2, y: float = 0.0) -> VGroup:
        cards = VGroup(*[self.badge(name, colors[i], 2.3, 0.5) for i, name in enumerate(names)])
        cards.arrange(DOWN, buff=0.18).shift(RIGHT * x + UP * y)
        return cards

    def metric(self, name: str, color: str, x: float, y: float) -> VGroup:
        box = self.panel(name, color, 1.55, 1.15).scale(0.76).move_to(RIGHT * x + UP * y)
        empty = self.label("?", 25, MUTED, "BOLD").move_to(box[0])
        return VGroup(box, empty)

    def construct(self) -> None:
        # 1 — two correct traces, unresolved policy identity
        frame1 = self.lab_frame("TWO POLICIES · SAME TRAINING TRACE", COPPER)
        crate1 = self.crate().shift(LEFT * 4.0 + DOWN * 0.25)
        clinic1 = self.badge("CLINIC", GREEN, 1.8).shift(RIGHT * 4.3 + UP * 1.0)
        lane_a1 = self.route("POLICY A", GREEN, 0.65, "CORRECT", wrong=False)
        lane_b1 = self.route("POLICY B", VIOLET, -1.35, "CORRECT", wrong=False)
        unknown1 = VGroup(self.badge("POLICY A ?", MUTED, 1.8), self.badge("POLICY B ?", MUTED, 1.8)).arrange(RIGHT, buff=0.3).shift(DOWN * 2.35)
        scene1 = VGroup(frame1, crate1, clinic1, lane_a1, lane_b1, unknown1)
        self.play_beat(1, FadeIn(scene1), Indicate(lane_a1, color=GREEN), Indicate(lane_b1, color=VIOLET), settle=0.8)

        # 2 — concrete parcel-sorting lab
        frame2 = self.lab_frame("SORTING LAB", BLUE)
        belt2 = self.conveyor(y=-0.35)
        insulin2 = self.crate().shift(LEFT * 3.7 + DOWN * 0.35)
        supply2 = self.crate("SUPPLY", seal=False, stripe=False).shift(LEFT * 1.0 + DOWN * 0.35)
        clinic2 = self.badge("CLINIC DOCK", GREEN, 2.1).shift(RIGHT * 4.2 + UP * 1.1)
        warehouse2 = self.badge("WAREHOUSE DOCK", MUTED, 2.55).shift(RIGHT * 4.2 + DOWN * 1.3)
        model2 = self.badge("SORTER", AUTHORITY, 1.65).shift(LEFT * 5.0 + UP * 1.35)
        scene2 = VGroup(frame2, belt2, insulin2, supply2, clinic2, warehouse2, model2)
        self.play_beat(2, FadeOut(scene1), FadeIn(scene2), GrowArrow(belt2[2][0]), Indicate(insulin2, color=GREEN), settle=0.7)

        # 3 — correlated cues become the visible reward signal
        frame3 = self.lab_frame("TRAINING SUPPORT", GOLD)
        crates3 = VGroup(*[self.crate().scale(0.75).shift(LEFT * 3.8 + RIGHT * i * 1.45 + DOWN * 0.65) for i in range(4)])
        cue3 = VGroup(self.badge("MEDICAL SEAL", BLUE, 2.2), self.badge("GREEN STRIPE", GREEN, 2.1)).arrange(RIGHT, buff=0.28).shift(UP * 1.35)
        reward3 = self.badge("REWARD → CLINIC", GOLD, 2.6).shift(RIGHT * 3.6 + DOWN * 1.85)
        links3 = VGroup(DashedLine(cue3[0].get_bottom(), crates3[0].get_top(), color=BLUE), DashedLine(cue3[1].get_bottom(), crates3[1].get_top(), color=GREEN), Arrow(crates3[-1].get_right(), reward3.get_left(), color=GOLD, stroke_width=3, buff=0.12))
        scene3 = VGroup(frame3, crates3, cue3, reward3, links3)
        self.play_beat(3, FadeOut(scene2), FadeIn(scene3), LaggedStart(*[Create(x) for x in links3], lag_ratio=0.12), Indicate(cue3[1], color=GREEN), GrowArrow(links3[-1]), settle=0.7)

        # 4 — constitutional effect gate versus internal explanation
        frame4 = self.lab_frame("EXTERNAL EFFECT ≠ INTERNAL OBJECTIVE", RED)
        gate4 = self.panel("EFFECT GATE", RED, 2.6, 1.9).shift(RIGHT * 3.8)
        gate_cross4 = Cross(gate4[0], stroke_color=RED, stroke_width=5)
        learner4 = self.panel("LEARNER", AUTHORITY, 2.3, 1.6).shift(LEFT * 0.2)
        hypotheses4 = self.matrix(["SEAL?", "STRIPE?", "MEMORY?", "EVALUATOR?"], [BLUE, GREEN, MUTED, VIOLET], x=-3.8, y=0.15)
        scene4 = VGroup(frame4, gate4, gate_cross4, learner4, hypotheses4)
        self.play_beat(4, FadeOut(scene3), FadeIn(scene4), GrowArrow(Arrow(learner4.get_right(), gate4.get_left(), color=RED, stroke_width=4, buff=0.12)), LaggedStart(*[FadeIn(h) for h in hypotheses4], lag_ratio=0.12), Indicate(gate4, color=RED), settle=0.8)

        # 5 — four distinct identities
        frame5 = self.lab_frame("KEEP FOUR IDENTITIES SEPARATE", GOLD)
        identities5 = VGroup(
            self.panel("AUTHORIZED TARGET", AUTHORITY, 2.35, 1.55),
            self.panel("LEARNING SIGNAL", BLUE, 2.35, 1.55),
            self.panel("RESULTING POLICY", GREEN, 2.35, 1.55),
            self.panel("OBJECTIVE HYPOTHESIS", VIOLET, 2.55, 1.55),
        ).arrange(RIGHT, buff=0.22).scale(0.84).shift(DOWN * 0.25)
        line5 = VGroup(*[Arrow(identities5[i].get_right(), identities5[i + 1].get_left(), color=MUTED, stroke_width=2, buff=0.06) for i in range(3)])
        scene5 = VGroup(frame5, identities5, line5)
        self.play_beat(5, FadeOut(scene4), FadeIn(identities5), LaggedStart(*[GrowArrow(x) for x in line5], lag_ratio=0.15), Indicate(identities5[3], color=VIOLET), settle=0.9)

        # 6 — target and signal agree only because data correlates cues
        frame6 = self.lab_frame("TARGET · SIGNAL · CORRELATED DATA", COPPER)
        target6 = self.badge("TARGET → INSULIN TO CLINIC", AUTHORITY, 3.1).shift(LEFT * 3.8 + UP * 1.4)
        signal6 = self.badge("SIGNAL → OBSERVED CLINIC CHOICE", BLUE, 3.5).shift(LEFT * 3.5 + DOWN * 1.35)
        data6 = VGroup(*[self.crate().scale(0.6).shift(RIGHT * (i - 1.5) * 1.35 + DOWN * 0.15) for i in range(4)])
        link6 = VGroup(Arrow(target6.get_right(), data6.get_left(), color=AUTHORITY, stroke_width=3, buff=0.1), Arrow(signal6.get_right(), data6.get_left(), color=BLUE, stroke_width=3, buff=0.1))
        scene6 = VGroup(frame6, target6, signal6, data6, link6)
        self.play_beat(6, FadeOut(scene5), FadeIn(target6), FadeIn(signal6), FadeIn(data6), LaggedStart(*[GrowArrow(x) for x in link6], lag_ratio=0.15), Indicate(data6, color=GREEN), settle=0.7)

        # 7 — matched policy lanes
        frame7 = self.lab_frame("BEHAVIORAL EQUIVALENCE", GREEN)
        crate7 = self.crate().scale(0.72).shift(LEFT * 4.6)
        lanes7 = VGroup(self.route("SEAL POLICY", GREEN, 0.85, "CLINIC"), self.route("STRIPE POLICY", VIOLET, -1.05, "CLINIC"))
        score7 = self.badge("100% TRAINING SUCCESS", GOLD, 3.0).shift(RIGHT * 3.4 + UP * 2.1)
        scene7 = VGroup(frame7, crate7, lanes7, score7)
        self.play_beat(7, FadeOut(scene6), FadeIn(crate7), FadeIn(lanes7), FadeIn(score7), Indicate(lanes7[0], color=GREEN), Indicate(lanes7[1], color=VIOLET), settle=0.8)

        # 8 — custody boundary
        frame8 = self.lab_frame("OBSERVED BEHAVIOR IN CUSTODY", GOLD)
        envelope8 = RoundedRectangle(width=8.4, height=3.3, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=DEEP, fill_opacity=1).shift(LEFT * 0.4)
        trace8 = self.badge("TRACE = TRACE", GREEN, 2.3).move_to(envelope8).shift(UP * 0.65)
        observed8 = self.badge("OBSERVED BEHAVIOR", BLUE, 2.7).move_to(envelope8).shift(DOWN * 0.65)
        unknown8 = self.badge("TRUE OBJECTIVE ?", MUTED, 2.6).shift(RIGHT * 4.25)
        blocked8 = Cross(Arrow(envelope8.get_right(), unknown8.get_left(), color=RED, stroke_width=4, buff=0.15), stroke_color=RED, stroke_width=5)
        scene8 = VGroup(frame8, envelope8, trace8, observed8, unknown8, blocked8)
        self.play_beat(8, FadeOut(scene7), Create(envelope8), FadeIn(trace8), FadeIn(observed8), FadeIn(unknown8), GrowArrow(Arrow(envelope8.get_right(), unknown8.get_left(), color=RED, stroke_width=4, buff=0.15)), Create(blocked8), Indicate(observed8, color=BLUE), settle=0.8)

        # 9 — plural live hypothesis matrix
        frame9 = self.lab_frame("LIVE HYPOTHESES", VIOLET)
        trace9 = self.badge("SHARED TRAINING TRACE", BLUE, 2.7).shift(LEFT * 4.2)
        rows9 = self.matrix(["CAUSAL FEATURE", "CORRELATED PROXY", "MEMORIZED PATTERN", "CONDITIONAL POLICY", "EVALUATOR OVERFIT", "EXTERNAL SCAFFOLD", "INTERNAL SEARCH"], [BLUE, GREEN, MUTED, VIOLET, RED, COPPER, GOLD], x=1.45, y=0.0)
        links9 = VGroup(*[DashedLine(trace9.get_right(), row.get_left(), color=row[0].get_stroke_color(), stroke_width=2) for row in rows9])
        scene9 = VGroup(frame9, trace9, rows9, links9)
        self.play_beat(9, FadeOut(scene8), FadeIn(trace9), LaggedStart(*[Create(x) for x in links9], lag_ratio=0.08), LaggedStart(*[FadeIn(x) for x in rows9], lag_ratio=0.1), Indicate(rows9, color=VIOLET), settle=0.8)

        # 10 — sealed stripe-only intervention
        frame10 = self.lab_frame("SEALED SEPARATING INTERVENTION", GOLD)
        locked10 = VGroup(self.badge("MEDICAL SEAL · LOCKED", BLUE, 2.8), self.badge("TASK · LOCKED", AUTHORITY, 2.1), self.badge("DESTINATION · LOCKED", GREEN, 2.6)).arrange(DOWN, buff=0.26).shift(LEFT * 3.9)
        intervention10 = self.panel("SWAP STRIPE ONLY", RED, 3.2, 2.0).shift(RIGHT * 0.2)
        stripe_old10 = self.badge("GREEN STRIPE", GREEN, 2.0).shift(RIGHT * 3.6 + UP * 0.8)
        stripe_new10 = self.badge("NO STRIPE", RED, 1.7).shift(RIGHT * 3.6 + DOWN * 0.8)
        arrow10 = Arrow(intervention10.get_right(), stripe_new10.get_left(), color=RED, stroke_width=4, buff=0.12)
        scene10 = VGroup(frame10, locked10, intervention10, stripe_old10, stripe_new10, arrow10)
        self.play_beat(10, FadeOut(scene9), FadeIn(locked10), FadeIn(intervention10), FadeIn(stripe_old10), GrowArrow(arrow10), FadeIn(stripe_new10), Indicate(locked10, color=GOLD), settle=0.8)

        # 11 — competence and goal choice are separate axes
        frame11 = self.lab_frame("COMPETENCE ≠ GOAL CHOICE", COPPER)
        broken11 = self.panel("BROKEN SORTER", RED, 2.5, 2.0).shift(LEFT * 3.5 + UP * 0.7)
        capable11 = self.panel("CAPABLE SORTER", GREEN, 2.5, 2.0).shift(RIGHT * 1.0 + UP * 0.7)
        axes11 = VGroup(self.badge("TASK FAIL", RED, 1.6), self.badge("GOAL FAIL", RED, 1.6)).arrange(DOWN, buff=0.24).move_to(broken11[0])
        axes11b = VGroup(self.badge("TASK PASS", GREEN, 1.6), self.badge("GOAL FAIL", RED, 1.6)).arrange(DOWN, buff=0.24).move_to(capable11[0])
        sharp11 = self.badge("CAPABLE + WRONG IS SHARPER", GOLD, 3.6).shift(DOWN * 1.9)
        scene11 = VGroup(frame11, broken11, capable11, axes11, axes11b, sharp11)
        self.play_beat(11, FadeOut(scene10), FadeIn(broken11), FadeIn(capable11), FadeIn(axes11), FadeIn(axes11b), FadeIn(sharp11), Indicate(axes11b, color=GOLD), settle=0.75)

        # 12 — swap causes capable policy divergence
        frame12 = self.lab_frame("HELD-OUT STRIPE SWAP", RED)
        seal12 = self.route("SEAL POLICY", GREEN, 0.9, "CLINIC")
        stripe12 = self.route("STRIPE POLICY", RED, -1.1, "WRONG BOX", wrong=True)
        crate12 = self.crate().scale(0.7).shift(LEFT * 4.5 + DOWN * 0.1)
        diverge12 = self.badge("EQUAL TRAINING → DIVERGENT CHOICE", GOLD, 4.0).shift(UP * 2.05)
        scene12 = VGroup(frame12, seal12, stripe12, crate12, diverge12)
        self.play_beat(12, FadeOut(scene11), FadeIn(crate12), FadeIn(seal12), FadeIn(stripe12), FadeIn(diverge12), Indicate(stripe12[3], color=RED), settle=0.8)

        # 13 — seeded camera-aware positive control
        frame13 = self.lab_frame("SEEDED CONDITIONAL CONTROL", VIOLET)
        camera13 = self.badge("EVALUATION CAMERA", BLUE, 2.6).shift(UP * 2.0)
        light13 = self.badge("CAMERA ON", GREEN, 1.7).shift(LEFT * 3.5 + UP * 0.7)
        dark13 = self.badge("CAMERA OFF", RED, 1.8).shift(LEFT * 3.5 + DOWN * 1.0)
        seal13 = self.badge("FOLLOW SEAL", GREEN, 1.8).shift(RIGHT * 1.3 + UP * 0.7)
        stripe13 = self.badge("FOLLOW STRIPE", RED, 2.0).shift(RIGHT * 1.3 + DOWN * 1.0)
        arrows13 = VGroup(Arrow(light13.get_right(), seal13.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(dark13.get_right(), stripe13.get_left(), color=RED, stroke_width=3, buff=0.1))
        scene13 = VGroup(frame13, camera13, light13, dark13, seal13, stripe13, arrows13)
        self.play_beat(13, FadeOut(scene12), FadeIn(camera13), FadeIn(light13), FadeIn(dark13), GrowArrow(arrows13[0]), GrowArrow(arrows13[1]), FadeIn(seal13), FadeIn(stripe13), Indicate(camera13, color=BLUE), settle=0.7)

        # 14 — seeded detection does not prove deception
        frame14 = self.lab_frame("INSTRUMENT SCOPE", RED)
        detected14 = self.badge("SEEDED DETECTED", GREEN, 2.5).shift(LEFT * 3.8 + UP * 1.1)
        scope14 = self.badge("TEST FAMILY ONLY", GOLD, 2.6).shift(LEFT * 3.8 + DOWN * 1.0)
        dec14 = self.badge("DECEPTION", RED, 1.8).shift(RIGHT * 2.9 + UP * 0.85)
        obj14 = self.badge("HIDDEN OBJECTIVE", VIOLET, 2.2).shift(RIGHT * 2.9 + DOWN * 0.85)
        arrows14 = VGroup(Arrow(detected14.get_right(), dec14.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(detected14.get_right(), obj14.get_left(), color=RED, stroke_width=3, buff=0.1))
        crosses14 = VGroup(Cross(arrows14[0], stroke_color=RED, stroke_width=4), Cross(arrows14[1], stroke_color=RED, stroke_width=4))
        scene14 = VGroup(frame14, detected14, scope14, dec14, obj14, arrows14, crosses14)
        self.play_beat(14, FadeOut(scene13), FadeIn(detected14), FadeIn(scope14), GrowArrow(arrows14[0]), GrowArrow(arrows14[1]), Create(crosses14), FadeIn(dec14), FadeIn(obj14), Indicate(scope14, color=GOLD), settle=0.85)

        # 15 — competing explanation matrix, no scalar deception score
        frame15 = self.lab_frame("COMPETING-EXPLANATION MATRIX", VIOLET)
        matrix15 = self.matrix(["SHIFT", "SHORTCUT", "TRIGGER", "REWARD", "EVAL", "DECEPTION", "TRAINING GAME", "UPDATE"], [BLUE, GREEN, MUTED, GOLD, COPPER, RED, VIOLET, RESIDUAL], x=-1.3, y=0.0)
        score15 = self.panel("ONE DECEPTION SCORE", RED, 3.1, 2.0).shift(RIGHT * 4.0)
        cross15 = Cross(score15[0], stroke_color=RED, stroke_width=5)
        scene15 = VGroup(frame15, matrix15, score15, cross15)
        self.play_beat(15, FadeOut(scene14), LaggedStart(*[FadeIn(x) for x in matrix15], lag_ratio=0.08), FadeIn(score15), Create(cross15), Indicate(matrix15, color=VIOLET), settle=0.9)

        # 16 — overlapping mechanisms can produce the same capability
        frame16 = self.lab_frame("CAPABILITY ≠ MESA-OPTIMIZER", COPPER)
        mechanisms16 = self.matrix(["RETRIEVAL", "HEURISTIC", "PLANNER", "SCAFFOLD", "INTERNAL SEARCH"], [BLUE, GREEN, AUTHORITY, COPPER, VIOLET], x=-3.1, y=0.0)
        output16 = self.badge("SAME CLINIC OUTPUT", GREEN, 2.8).shift(RIGHT * 3.7)
        edges16 = VGroup(*[Arrow(m.get_right(), output16.get_left(), color=m[0].get_stroke_color(), stroke_width=2, buff=0.1) for m in mechanisms16])
        scene16 = VGroup(frame16, mechanisms16, output16, edges16)
        self.play_beat(16, FadeOut(scene15), LaggedStart(*[GrowArrow(e) for e in edges16], lag_ratio=0.1), LaggedStart(*[FadeIn(m) for m in mechanisms16], lag_ratio=0.1), FadeIn(output16), Indicate(output16, color=GREEN), settle=0.8)

        # 17 — internal-search hypothesis gets explicit obligations
        frame17 = self.lab_frame("INTERNAL-OPTIMIZATION HYPOTHESIS", GOLD)
        search17 = self.panel("SEARCH", GOLD, 3.4, 3.7).shift(LEFT * 1.3)
        fields17 = VGroup(*[self.badge(v, GOLD, 2.35) for v in ["CANDIDATE STATE", "SEARCH PROCESS", "ORDERING CRITERION", "INDEPENDENT TEST"]]).arrange(DOWN, buff=0.2).move_to(search17[0])
        shortcut17 = self.badge("GOAL WORDS / COT ≠ PROOF", RED, 3.3).shift(RIGHT * 3.4)
        cross17 = Cross(shortcut17, stroke_color=RED, stroke_width=4)
        scene17 = VGroup(frame17, search17, fields17, shortcut17, cross17)
        self.play_beat(17, FadeOut(scene16), FadeIn(search17), LaggedStart(*[FadeIn(f) for f in fields17], lag_ratio=0.12), FadeIn(shortcut17), Create(cross17), Indicate(fields17, color=GOLD), settle=0.9)

        # 18 — four evidence lanes and shared dependency roots
        frame18 = self.lab_frame("FOUR EVIDENCE LANES", BLUE)
        lanes18 = VGroup(*[self.badge(v, [BLUE, AUTHORITY, COPPER, VIOLET][i], 2.2) for i, v in enumerate(["BEHAVIOR", "CAUSAL", "TRAINING PROCESS", "WHITE BOX"])])
        lanes18.arrange(RIGHT, buff=0.28).shift(UP * 1.0)
        roots18 = VGroup(self.badge("SHARED DATA", RED, 2.0), self.badge("SHARED MONITOR", RED, 2.25)).arrange(RIGHT, buff=0.4).shift(DOWN * 1.55)
        dep18 = VGroup(*[DashedLine(root.get_top(), lane.get_bottom(), color=RED, stroke_width=2) for root in roots18 for lane in lanes18[:2]])
        scene18 = VGroup(frame18, lanes18, roots18, dep18)
        self.play_beat(18, FadeOut(scene17), LaggedStart(*[FadeIn(l) for l in lanes18], lag_ratio=0.12), FadeIn(roots18), LaggedStart(*[Create(x) for x in dep18], lag_ratio=0.12), Indicate(lanes18, color=BLUE), settle=0.9)

        # 19 — white-box feature with attached limitations
        frame19 = self.lab_frame("WHITE-BOX EVIDENCE · LIMITED", VIOLET)
        feature19 = self.panel("FEATURE", VIOLET, 2.4, 1.7).shift(LEFT * 3.4)
        activation19 = VGroup(*[
            Circle(radius=0.085, stroke_color=VIOLET if i % 3 else BLUE,
                   stroke_width=2, fill_color=VIOLET if i % 3 else BLUE,
                   fill_opacity=0.85)
            for i in range(12)
        ]).arrange_in_grid(rows=3, cols=4, buff=0.18).scale(0.72).move_to(feature19[0])
        activation19.shift(UP * 0.12)
        activation_label19 = self.badge("ACTIVATION?", GOLD, 1.45, 0.34).scale(0.65).move_to(feature19[0]).shift(DOWN * 0.58)
        supports19 = self.badge("SUPPORTS HYPOTHESIS", GREEN, 2.8).shift(RIGHT * 0.1)
        limits19 = self.matrix(["APPROXIMATION", "POLYSEMANTIC", "EVALUATOR", "SHIFT"], [RED, RESIDUAL, COPPER, MUTED], x=3.0, y=0.0)
        edge19 = Arrow(feature19.get_right(), supports19.get_left(), color=GREEN, stroke_width=4, buff=0.1)
        scene19 = VGroup(frame19, feature19, activation19, activation_label19, supports19, limits19, edge19)
        self.play_beat(19, AnimationGroup(FadeOut(scene18), FadeIn(feature19), lag_ratio=0.0), LaggedStart(*[FadeIn(dot) for dot in activation19], lag_ratio=0.08), FadeIn(activation_label19), GrowArrow(edge19), FadeIn(supports19), LaggedStart(*[FadeIn(l) for l in limits19], lag_ratio=0.12), Indicate(limits19, color=RED), settle=0.8)

        # 20 — training history preserves possibilities
        frame20 = self.lab_frame("TRAINING-SIGNAL LINEAGE", COPPER)
        events20 = VGroup(*[self.badge(v, [GOLD, BLUE, AUTHORITY, RESIDUAL, RED, COPPER][i], 1.65) for i, v in enumerate(["REWARD", "OPTIMIZER", "CURRICULUM", "SELECTION", "FAILED RUNS", "SCAFFOLD"])])
        events20.arrange(RIGHT, buff=0.15).scale(0.84).shift(UP * 0.75)
        line20 = Line(LEFT * 5.3, RIGHT * 5.3, color=BOUNDARY, stroke_width=4).shift(DOWN * 0.1)
        unknown20 = self.badge("POSSIBILITIES · NOT VERDICT", MUTED, 3.4).shift(DOWN * 1.65)
        arrows20 = VGroup(*[Arrow(e.get_bottom(), line20.get_center() + DOWN * 0.08, color=e[0].get_stroke_color(), stroke_width=2, buff=0.12) for e in events20])
        scene20 = VGroup(frame20, events20, line20, arrows20, unknown20)
        self.play_beat(20, FadeOut(scene19), Create(line20), LaggedStart(*[FadeIn(e) for e in events20], lag_ratio=0.1), LaggedStart(*[GrowArrow(a) for a in arrows20], lag_ratio=0.08), FadeIn(unknown20), Indicate(unknown20, color=MUTED), settle=0.8)

        # 21 — adjudication produces bounded authority states
        frame21 = self.lab_frame("ADJUDICATE UNCERTAINTY", GOLD)
        inputs21 = self.matrix(["LIKELIHOOD", "CONSEQUENCE", "OPPORTUNITY", "SENSITIVITY", "COST"], [BLUE, RED, AUTHORITY, VIOLET, MUTED], x=-3.2, y=0.0)
        output21 = VGroup(self.badge("UNKNOWN", RED, 1.8), self.badge("NARROW", GOLD, 1.8), self.badge("HOLD", RED, 1.6)).arrange(DOWN, buff=0.27).shift(RIGHT * 3.7)
        arrows21 = VGroup(*[Arrow(i.get_right(), output21[0].get_left(), color=i[0].get_stroke_color(), stroke_width=2, buff=0.1) for i in inputs21])
        scene21 = VGroup(frame21, inputs21, output21, arrows21)
        self.play_beat(21, FadeOut(scene20), LaggedStart(*[GrowArrow(a) for a in arrows21], lag_ratio=0.1), LaggedStart(*[FadeIn(i) for i in inputs21], lag_ratio=0.1), FadeIn(output21), Indicate(output21[0], color=RED), settle=0.9)

        # 22 — opportunity envelope expands
        frame22 = self.lab_frame("OPPORTUNITY ENVELOPE", AUTHORITY)
        core22 = self.panel("MODEL", GOLD, 2.1, 1.5).shift(LEFT * 0.5)
        afford22 = self.matrix(["TOOLS", "MEMORY", "HORIZON", "COPIES", "AGENTS", "SELF-MODIFY", "EFFECT AUTHORITY"], [BLUE, BLUE, AUTHORITY, VIOLET, VIOLET, RED, RED], x=3.0, y=0.0)
        edges22 = VGroup(*[Arrow(core22.get_right(), a.get_left(), color=a[0].get_stroke_color(), stroke_width=2, buff=0.1) for a in afford22])
        scene22 = VGroup(frame22, core22, afford22, edges22)
        self.play_beat(22, FadeOut(scene21), FadeIn(core22), LaggedStart(*[FadeIn(a) for a in afford22], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges22], lag_ratio=0.08), Indicate(afford22, color=AUTHORITY), settle=0.8)

        # 23 — formal power tests remain conditional
        frame23 = self.lab_frame("POWER TEST · ASSUMPTION-BOUND", RED)
        boundary23 = RoundedRectangle(width=6.5, height=3.7, corner_radius=0.2, stroke_color=GOLD, stroke_width=3, fill_color=DEEP, fill_opacity=1).shift(LEFT * 1.0)
        assumption23 = self.badge("ASSUMPTIONS", GOLD, 2.0).move_to(boundary23).shift(UP * 1.3)
        tests23 = VGroup(self.badge("OPTION EXPANSION", BLUE, 2.4), self.badge("SHUTDOWN", RED, 1.7)).arrange(RIGHT, buff=0.3).move_to(boundary23)
        universal23 = self.badge("UNIVERSAL POWER CLAIM", RED, 3.0).shift(RIGHT * 3.8)
        cross23 = Cross(universal23, stroke_color=RED, stroke_width=5)
        scene23 = VGroup(frame23, boundary23, assumption23, tests23, universal23, cross23)
        self.play_beat(23, FadeOut(scene22), Create(boundary23), FadeIn(assumption23), FadeIn(tests23), FadeIn(universal23), Create(cross23), Indicate(boundary23, color=GOLD), settle=0.8)

        # 24 — mitigation has three rival outcomes
        frame24 = self.lab_frame("MITIGATION · THREE OUTCOMES", RED)
        gate24 = self.panel("MITIGATION", GOLD, 2.3, 1.5).shift(LEFT * 4.0)
        outcomes24 = self.matrix(["REMOVAL", "CONCEALMENT", "CAPABILITY DAMAGE"], [GREEN, RED, RESIDUAL], x=0.2, y=0.0)
        arrows24 = VGroup(*[Arrow(gate24.get_right(), o.get_left(), color=o[0].get_stroke_color(), stroke_width=3, buff=0.1) for o in outcomes24])
        checks24 = self.matrix(["NOVEL TRIGGERS", "COMPETENCE", "MONITOR", "EVASION", "MECHANISM"], [BLUE, GREEN, AUTHORITY, RED, VIOLET], x=3.7, y=0.0)
        scene24 = VGroup(frame24, gate24, outcomes24, arrows24, checks24)
        self.play_beat(24, FadeOut(scene23), FadeIn(gate24), LaggedStart(*[GrowArrow(a) for a in arrows24], lag_ratio=0.1), LaggedStart(*[FadeIn(o) for o in outcomes24], lag_ratio=0.1), LaggedStart(*[FadeIn(c) for c in checks24], lag_ratio=0.08), Indicate(outcomes24, color=RED), settle=0.9)

        # 25 — sealed denominator and retained failures
        frame25 = self.lab_frame("SEALED DENOMINATOR", GOLD)
        known25 = self.matrix(["KNOWN TRIGGERS", "ORIGINAL TESTS"], [MUTED, BLUE], x=-3.6, y=0.5)
        sealed25 = self.matrix(["SEALED TRIGGERS", "MONITOR-BLIND", "RESCUES", "FAILED RUNS"], [GOLD, RED, GREEN, RESIDUAL], x=1.0, y=0.0)
        lock25 = self.badge("DENOMINATOR LOCKED", GOLD, 2.9).shift(DOWN * 2.2)
        line25 = DashedLine(LEFT * 0.0 + UP * 2.2, LEFT * 0.0 + DOWN * 1.75, color=GOLD, stroke_width=4)
        scene25 = VGroup(frame25, known25, sealed25, lock25, line25)
        self.play_beat(25, FadeOut(scene24), FadeIn(known25), FadeIn(sealed25), Create(line25), FadeIn(lock25), Indicate(sealed25, color=GOLD), settle=0.8)

        # 26 — assemble the integrity record
        frame26 = self.lab_frame("LEARNED-OBJECTIVE INTEGRITY RECORD", GOLD)
        record26 = RoundedRectangle(width=5.2, height=4.35, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=DEEP, fill_opacity=1).shift(LEFT * 0.5)
        fields26 = self.matrix(["MODEL + CHECKPOINT", "OUTER CONTRACT", "SIGNAL LINEAGE", "LIVE HYPOTHESES", "INTERVENTIONS", "EVIDENCE LIMITS", "ENVELOPE", "RESIDUALS", "EXPIRY + ROLLBACK", "NON-AUTHORITY"], [GOLD, AUTHORITY, BLUE, VIOLET, RED, MUTED, AUTHORITY, RESIDUAL, ROLLBACK, COPPER], x=-0.5, y=0.0)
        fields26.scale(0.72)
        outside26 = self.badge("NO RELEASE AUTHORITY", RED, 2.8).shift(RIGHT * 4.2 + DOWN * 2.0)
        scene26 = VGroup(frame26, record26, fields26, outside26)
        self.play_beat(26, FadeOut(scene25), Create(record26), LaggedStart(*[FadeIn(f) for f in fields26], lag_ratio=0.07), FadeIn(outside26), Indicate(record26, color=GOLD), settle=0.9)

        # 27 — state changes reopen or justify inheritance
        frame27 = self.lab_frame("INTEGRITY FOLLOWS STATE", ROLLBACK)
        start27 = self.panel("CHECKPOINT", GOLD, 2.2, 1.4).shift(LEFT * 5.0)
        nodes27 = VGroup(*[self.badge(v, [BLUE, COPPER, MUTED, VIOLET, GREEN, RED, RESIDUAL][i], 1.65) for i, v in enumerate(["FINE-TUNE", "DISTILL", "QUANTIZE", "ROUTER", "MEMORY", "TOOLS", "CACHE"])])
        nodes27.arrange(RIGHT, buff=0.12).scale(0.78).shift(LEFT * 0.2 + UP * 0.5)
        desc27 = self.badge("DESCENDANT · REOPEN", RED, 2.7).shift(RIGHT * 3.6 + DOWN * 1.25)
        edge27 = Arrow(start27.get_right(), nodes27[0].get_left(), color=GOLD, stroke_width=3, buff=0.1)
        edges27 = VGroup(edge27, *[Arrow(nodes27[i].get_right(), nodes27[i + 1].get_left(), color=GOLD, stroke_width=2, buff=0.05) for i in range(len(nodes27) - 1)])
        scene27 = VGroup(frame27, start27, nodes27, edges27, desc27)
        self.play_beat(27, FadeOut(scene26), FadeIn(start27), LaggedStart(*[FadeIn(n) for n in nodes27], lag_ratio=0.08), LaggedStart(*[GrowArrow(e) for e in edges27], lag_ratio=0.08), FadeIn(desc27), Indicate(desc27, color=RED), settle=0.9)

        # 28 — finite non-identification proof
        frame28 = self.lab_frame("FINITE NON-IDENTIFICATION BOUNDARY", BLUE)
        world28 = VGroup(self.panel("WORLD A", BLUE, 2.4, 2.2), self.panel("WORLD B", VIOLET, 2.4, 2.2)).arrange(RIGHT, buff=0.5).shift(LEFT * 2.7)
        same28 = self.badge("TRACE = TRACE", GREEN, 2.4).shift(RIGHT * 1.0 + UP * 1.1)
        opportunity28 = self.badge("SEPARATING OPPORTUNITY", GOLD, 3.0).shift(RIGHT * 3.6 + DOWN * 0.15)
        split28 = self.badge("ACTION ≠ ACTION", RED, 2.4).shift(RIGHT * 3.6 + DOWN * 1.45)
        arrows28 = VGroup(Arrow(world28[0].get_right(), same28.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(world28[1].get_right(), same28.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(same28.get_right(), opportunity28.get_left(), color=GOLD, stroke_width=3, buff=0.1), Arrow(opportunity28.get_bottom(), split28.get_top(), color=RED, stroke_width=3, buff=0.1))
        scene28 = VGroup(frame28, world28, same28, opportunity28, split28, arrows28)
        self.play_beat(28, FadeOut(scene27), FadeIn(world28), FadeIn(same28), FadeIn(opportunity28), FadeIn(split28), LaggedStart(*[GrowArrow(a) for a in arrows28], lag_ratio=0.1), Indicate(split28, color=RED), settle=0.9)

        # 29 — seven accepted transitions and fifty-nine rejecting mutations
        frame29 = self.lab_frame("FINITE RECORD · FAIL CLOSED", COPPER)
        rail29 = Line(LEFT * 5.1, RIGHT * 2.8, color=GREEN, stroke_width=5).shift(UP * 1.2)
        steps29 = VGroup(*[self.badge(str(i), GREEN, 0.55, 0.42) for i in range(1, 8)]).arrange(RIGHT, buff=0.12).shift(LEFT * 3.9 + UP * 1.2)
        accepted29 = self.badge("7 ACCEPTED TRANSITIONS", GREEN, 3.1).shift(RIGHT * 3.5 + UP * 1.2)
        reject29 = self.badge("59 REJECTED MUTATIONS", RED, 3.1).shift(LEFT * 1.0 + DOWN * 1.25)
        fixed29 = self.badge("STATE PRESERVED · NO SUPPORT", GOLD, 3.7).shift(RIGHT * 3.1 + DOWN * 1.25)
        crosses29 = VGroup(*[Cross(self.badge("×", RED, 0.45, 0.45), stroke_color=RED, stroke_width=3).shift(LEFT * 4.5 + RIGHT * i * 0.55 + DOWN * 0.35) for i in range(8)])
        scene29 = VGroup(frame29, rail29, steps29, accepted29, reject29, fixed29, crosses29)
        self.play_beat(29, FadeOut(scene28), Create(rail29), LaggedStart(*[FadeIn(s) for s in steps29], lag_ratio=0.08), FadeIn(accepted29), FadeIn(reject29), LaggedStart(*[FadeIn(c) for c in crosses29], lag_ratio=0.06), FadeIn(fixed29), Indicate(reject29, color=RED), settle=0.9)

        # 30 — mature campaign, empty result sockets
        frame30 = self.lab_frame("MATURE CAMPAIGN · PROSPECTIVE", BLUE)
        study30 = self.matrix(["NATURAL CASES", "SEALED SHIFTS", "INDEPENDENT EVAL", "TRANSFER", "ARCHITECTURES", "MITIGATION"], [BLUE, GOLD, VIOLET, GREEN, AUTHORITY, RED], x=-3.0, y=0.0)
        outcomes30 = VGroup(*[self.metric(v, MUTED, 2.3 + (i % 3) * 1.7, 1.2 - (i // 3) * 1.9) for i, v in enumerate(["HELP", "HARM", "UNCERTAINTY", "LATENCY", "COMPUTE", "GOV COST"])])
        empty30 = self.badge("NO RESULTS YET", RED, 2.3).shift(RIGHT * 4.1 + DOWN * 2.3)
        scene30 = VGroup(frame30, study30, outcomes30, empty30)
        self.play_beat(30, FadeOut(scene29), LaggedStart(*[FadeIn(s) for s in study30], lag_ratio=0.08), LaggedStart(*[FadeIn(o) for o in outcomes30], lag_ratio=0.08), FadeIn(empty30), Indicate(empty30, color=RED), settle=1.0)

        # 31 — explicit broad nonclaims
        frame31 = self.lab_frame("FINITE SUPPORT · BROAD CLAIMS OUTSIDE", RED)
        finite31 = self.panel("FINITE RECORD", GOLD, 3.0, 2.4).shift(LEFT * 2.6 + UP * 0.55)
        claims31 = self.matrix(["TRUE OBJECTIVE", "MESA-OPTIMIZER", "DECEPTION ABSENT", "MITIGATION VALID", "MONITOR INDEPENDENT", "ROLLBACK COMPLETE", "SAFE DEPLOYMENT"], [RED, RED, RED, RED, RESIDUAL, ROLLBACK, RED], x=2.0, y=0.0)
        bars31 = VGroup(*[Cross(c, stroke_color=RED, stroke_width=3) for c in claims31])
        scene31 = VGroup(frame31, finite31, claims31, bars31)
        self.play_beat(31, FadeOut(scene30), FadeIn(finite31), LaggedStart(*[FadeIn(c) for c in claims31], lag_ratio=0.08), LaggedStart(*[Create(b) for b in bars31], lag_ratio=0.08), Indicate(finite31, color=GOLD), settle=0.9)

        # 32 — callback and bounded handoff to Moral Uncertainty
        frame32 = self.lab_frame("BOUNDED INTEGRITY HANDOFF", GOLD)
        lane_a32 = self.route("SEAL POLICY", GREEN, 0.85, "CLINIC")
        lane_b32 = self.route("STRIPE POLICY", VIOLET, -1.05, "UNKNOWN", wrong=True)
        envelope32 = RoundedRectangle(width=8.1, height=3.3, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=DEEP, fill_opacity=0.35).shift(LEFT * 0.1)
        narrow32 = self.badge("AUTHORITY NARROWED", RED, 2.8).shift(LEFT * 3.8 + DOWN * 2.25)
        test32 = self.badge("SEPARATING TEST", BLUE, 2.4).shift(LEFT * 0.2 + DOWN * 2.25)
        moral32 = self.panel("MORAL UNCERTAINTY", VIOLET, 3.0, 1.7).shift(RIGHT * 4.1 + DOWN * 1.0)
        handoff32 = Arrow(envelope32.get_right(), moral32.get_left(), color=VIOLET, stroke_width=4, buff=0.12)
        unknown32 = self.label("OBJECTIVE ?", 20, INK, "BOLD").move_to(moral32[0])
        scene32 = VGroup(frame32, envelope32, lane_a32, lane_b32, narrow32, test32, moral32, handoff32, unknown32)
        self.play_beat(32, FadeOut(scene31), Create(envelope32), FadeIn(lane_a32), FadeIn(lane_b32), FadeIn(narrow32), FadeIn(test32), FadeIn(moral32), GrowArrow(handoff32), FadeIn(unknown32), Indicate(narrow32, color=RED), settle=1.0)

        self.wait_until(self.TARGET_DURATION)


if __name__ == "__main__":
    InnerAlignmentGeneration2().render()
