"""Generation-2 visual abstract for Dangerous Capability Domains.

A harmless matched-actor maze becomes an uplift instrument, a D0-D5 ladder,
and a dual-surface decision dossier. Every promotion needs a visible bridge;
failed sensitivity routes to instrument failure rather than incapability.
"""

from __future__ import annotations

from manim import (
    ArcBetweenPoints, Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn,
    FadeOut, GrowArrow, Indicate, LaggedStart, LEFT, Line, MoveAlongPath,
    Rectangle, ReplacementTransform, RIGHT, RoundedRectangle, Square,
    Succession, Text, Transform, TransformFromCopy, Triangle, UP, VGroup,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class DangerousCapabilityUpliftGeneration2(AsiScene):
    TARGET_DURATION = 299.945
    ENDS = [
        12.255, 22.885, 35.390, 46.770, 60.175,
        73.205, 86.535, 97.640, 110.420, 123.575,
        134.630, 145.035, 157.415, 169.195, 180.675,
        192.280, 204.485, 218.415, 232.420, 244.750,
        257.080, 269.735, 282.215, 291.695, 299.945,
    ]

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = "#14262F"

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        remaining = max(0.05, self.ENDS[index - 1] - self.renderer.time)
        if animations:
            self.play(
                LaggedStart(*animations, lag_ratio=0.16),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 20, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.65, height: float = 0.58) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1,
            stroke_color=color, stroke_width=2.4,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float = 3.4, height: float = 2.2) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=color, stroke_width=2.7,
            fill_color="#172A33", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.4, 2.5), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str] | None = None, columns: int = 4, width: float = 1.55) -> VGroup:
        colors = colors or [AUTHORITY] * len(values)
        cells = VGroup(*[self.badge(v, colors[i], width, 0.52) for i, v in enumerate(values)])
        cells.arrange_in_grid(rows=(len(values) + columns - 1) // columns, cols=columns, buff=(0.16, 0.22))
        return cells

    def actor(self, name: str, color: str, shape: str = "circle") -> VGroup:
        body = Circle(radius=0.42, stroke_color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        if shape == "square":
            body = Square(side_length=0.84, stroke_color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        return VGroup(body, self.label(name, 11, color, "BOLD").move_to(body))

    def maze(self) -> VGroup:
        frame = RoundedRectangle(
            width=7.2, height=3.0, corner_radius=0.12,
            stroke_color=ACCENT, stroke_width=2.6,
            fill_color="#142A33", fill_opacity=1,
        )
        walls = VGroup(
            Line(LEFT * 3.0 + UP * 0.6, LEFT * 0.7 + UP * 0.6, color=BOUNDARY, stroke_width=5),
            Line(LEFT * 0.7 + UP * 0.6, LEFT * 0.7 + UP * -0.55, color=BOUNDARY, stroke_width=5),
            Line(LEFT * 0.7 + UP * -0.55, RIGHT * 1.0 + UP * -0.55, color=BOUNDARY, stroke_width=5),
            Line(RIGHT * 1.0 + UP * -0.55, RIGHT * 1.0 + UP * 0.75, color=BOUNDARY, stroke_width=5),
            Line(RIGHT * 1.0 + UP * 0.75, RIGHT * 3.0 + UP * 0.75, color=BOUNDARY, stroke_width=5),
        )
        gate = DashedLine(UP * 1.18, UP * -1.18, color=AUTHORITY, stroke_width=5).shift(RIGHT * 0.15)
        return VGroup(frame, walls, gate)

    def receipt(self, title: str, color: str = AUTHORITY, width: float = 7.2, height: float = 4.2) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=color, stroke_width=3,
            fill_color="#192A30", fill_opacity=1,
        )
        heading = self.label(title, 19, color, "BOLD").next_to(shell, UP, buff=-0.38)
        return VGroup(shell, heading)

    def ladder(self) -> VGroup:
        names = ["D0 KNOW", "D1 SKILL", "D2 FLOW", "D3 UPLIFT", "D4 GUARD", "D5 FIELD"]
        rungs = VGroup(*[self.badge(name, MUTED, 2.0, 0.5) for name in names]).arrange(UP, buff=0.30)
        spine = Line(rungs[0].get_left() + LEFT * 0.32, rungs[-1].get_left() + LEFT * 0.32, color=BOUNDARY, stroke_width=4)
        return VGroup(spine, rungs)

    def construct(self) -> None:
        # 1 — equal knowledge, unequal uplift
        maze = self.maze()
        novice = self.actor("NOVICE", ACCENT).shift(LEFT * 4.8 + UP * 0.65)
        expert = self.actor("EXPERT", AUTHORITY, "square").shift(LEFT * 4.8 + UP * -0.65)
        quiz = self.badge("KNOWLEDGE ✓", EVIDENCE, 2.25).shift(UP * 2.6)
        stop_n = novice.copy().shift(RIGHT * 3.7)
        stop_e = expert.copy().shift(RIGHT * 3.7)
        ai = self.badge("AI ASSIST", ACCENT, 1.8).shift(UP * -2.45)
        finish_n = novice.copy().shift(RIGHT * 9.0)
        clock = self.badge("EXPERT −1 MIN", AUTHORITY, 2.25).shift(RIGHT * 4.7 + UP * -1.75)
        self.play_beat(1, FadeIn(maze), FadeIn(novice), FadeIn(expert), FadeIn(quiz), Transform(novice, stop_n), Transform(expert, stop_e), FadeIn(ai), Transform(novice, finish_n), FadeIn(clock), settle=0.8)

        # 2 — the counterfactual bracket
        quiz_badge = self.badge("QUIZ SCORE", MUTED, 1.8).shift(LEFT * 3.7 + UP * 1.6)
        capable = self.badge("CAPABLE", MUTED, 1.65).shift(LEFT * 3.7 + UP * -0.2)
        no_assist = self.badge("WITHOUT", MUTED, 1.65).shift(RIGHT * 1.3 + UP * 0.9)
        with_assist = self.badge("WITH AI", ACCENT, 1.65).shift(RIGHT * 4.6 + UP * 0.9)
        bracket = Line(no_assist.get_right(), with_assist.get_left(), color=EVIDENCE, stroke_width=6)
        delta = self.badge("ACTOR Δ", EVIDENCE, 1.7).next_to(bracket, UP * -1, buff=0.35)
        quiz_cross = Cross(quiz_badge, stroke_color=ROLLBACK)
        capable_cross = Cross(capable, stroke_color=ROLLBACK)
        self.play_beat(2, FadeOut(maze), FadeOut(novice), FadeOut(expert), FadeOut(quiz), FadeOut(ai), FadeOut(clock), FadeIn(quiz_badge), FadeIn(capable), Create(quiz_cross), Create(capable_cross), FadeIn(no_assist), FadeIn(with_assist), Create(bracket), FadeIn(delta), settle=0.55)

        # 3 — six separate quantities
        names = ["LATENT", "ELICITED", "PROPENSITY", "BYPASS", "UPLIFT", "HARM"]
        colors = [ACCENT, ACCENT, AUTHORITY, ROLLBACK, EVIDENCE, RESIDUAL]
        sockets = VGroup(*[self.badge(n, colors[i], 1.85, 0.62) for i, n in enumerate(names)]).arrange_in_grid(rows=2, cols=3, buff=(0.75, 0.9))
        locks = VGroup(*[self.badge("≠", AUTHORITY, 0.62, 0.48) for _ in range(4)])
        locks[0].move_to((sockets[0].get_center() + sockets[1].get_center()) / 2)
        locks[1].move_to((sockets[1].get_center() + sockets[2].get_center()) / 2)
        locks[2].move_to((sockets[3].get_center() + sockets[4].get_center()) / 2)
        locks[3].move_to((sockets[4].get_center() + sockets[5].get_center()) / 2)
        self.play_beat(3, FadeOut(quiz_badge), FadeOut(capable), FadeOut(quiz_cross), FadeOut(capable_cross), FadeOut(no_assist), FadeOut(with_assist), FadeOut(bracket), FadeOut(delta), LaggedStart(*[FadeIn(s) for s in sockets], lag_ratio=0.12), LaggedStart(*[FadeIn(l) for l in locks], lag_ratio=0.15), settle=0.55)

        # 4 — safe analogue envelope
        safe_maze = self.maze().scale(0.85)
        safe_frame = RoundedRectangle(width=8.2, height=4.5, corner_radius=0.15, stroke_color=ACCENT, stroke_width=4)
        safe_title = self.badge("SAFE ANALOGUE", ACCENT, 2.35).next_to(safe_frame, UP, buff=-0.12)
        prohibited = VGroup(*[self.badge(x, ROLLBACK, 1.65) for x in ["TARGET", "CREDENTIAL", "MATERIAL", "RECIPE"]]).arrange(UP * -1, buff=0.3).shift(RIGHT * 5.5)
        stops = VGroup(*[Cross(p, stroke_color=ROLLBACK, stroke_width=3) for p in prohibited])
        self.play_beat(4, FadeOut(sockets), FadeOut(locks), FadeIn(safe_frame), FadeIn(safe_title), FadeIn(safe_maze), LaggedStart(*[FadeIn(p) for p in prohibited], lag_ratio=0.12), LaggedStart(*[Create(x) for x in stops], lag_ratio=0.12), settle=0.6)

        # 5 — freeze the threat pathway
        path_names = ["ACTOR", "ACCESS", "PREREQ", "BOTTLENECK", "CONTROLS", "CONSEQUENCE"]
        path = VGroup(*[self.badge(n, AUTHORITY if i in (0, 5) else MUTED, 1.65, 0.56) for i, n in enumerate(path_names)]).arrange(RIGHT, buff=0.35).scale(0.83)
        edges = VGroup(*[Arrow(path[i].get_right(), path[i + 1].get_left(), color=BOUNDARY, buff=0.07, stroke_width=3) for i in range(len(path) - 1)])
        model_delta = self.badge("MODEL Δ", ACCENT, 1.55).next_to(path[3], UP, buff=0.65)
        model_edge = Arrow(model_delta.get_bottom(), path[3].get_top(), color=ACCENT, buff=0.08)
        stop = Line(UP * 2.0, UP * -2.0, color=ROLLBACK, stroke_width=6).shift(RIGHT * 5.9)
        stop_tag = self.badge("OBSERVATION STOP", ROLLBACK, 2.35).next_to(stop, UP, buff=-0.25)
        self.play_beat(5, FadeOut(safe_frame), FadeOut(safe_title), FadeOut(safe_maze), FadeOut(prohibited), FadeOut(stops), LaggedStart(*[FadeIn(x) for x in path], lag_ratio=0.1), Create(edges), FadeIn(model_delta), GrowArrow(model_edge), Create(stop), FadeIn(stop_tag), settle=0.5)

        # 6 — stratified cohorts
        cohort_names = ["NOVICE", "PRO", "TEAM", "AGENT"]
        cohort_colors = [ACCENT, AUTHORITY, EVIDENCE, MUTED]
        cohorts = VGroup(*[self.badge(n, cohort_colors[i], 1.55) for i, n in enumerate(cohort_names)]).arrange(UP * -1, buff=0.38).shift(LEFT * 4.7)
        delta_bars = VGroup(*[
            Rectangle(width=w, height=0.34, stroke_color=cohort_colors[i], fill_color=cohort_colors[i], fill_opacity=0.55).next_to(cohorts[i], RIGHT, buff=0.45)
            for i, w in enumerate([4.8, 1.3, 2.4, 0.7])
        ])
        average = DashedLine(UP * 2.2, UP * -2.2, color=ROLLBACK, stroke_width=4).shift(RIGHT * 0.8)
        average_tag = self.badge("AVERAGE HIDES", ROLLBACK, 2.15).next_to(average, RIGHT, buff=0.28)
        self.play_beat(6, FadeOut(path), FadeOut(edges), FadeOut(model_delta), FadeOut(model_edge), FadeOut(stop), FadeOut(stop_tag), LaggedStart(*[FadeIn(c) for c in cohorts], lag_ratio=0.12), LaggedStart(*[Create(b) for b in delta_bars], lag_ratio=0.12), Create(average), FadeIn(average_tag), Indicate(delta_bars[0], color=ACCENT), settle=0.55)

        # 7 — matched counterfactual arms
        arms = VGroup(*[self.badge(n, c, 2.0, 0.6) for n, c in [("NO ASSIST", MUTED), ("CONVENTIONAL", AUTHORITY), ("EXACT AI", ACCENT)]]).arrange(UP * -1, buff=0.7).shift(LEFT * 4.4)
        rails = VGroup(*[Line(a.get_right(), RIGHT * 5.2 + UP * a.get_center()[1], color=c, stroke_width=4) for a, c in zip(arms, [MUTED, AUTHORITY, ACCENT])])
        locks_grid = self.grid(["TIME", "INTERFACE", "TOOLS", "RETRIES", "HELP", "SCORE"], [EVIDENCE] * 6, 3, 1.45).shift(RIGHT * 1.5)
        extra = self.badge("EXTRA RETRIES", ROLLBACK, 1.95).shift(RIGHT * 5.0 + UP * -2.5)
        extra_cross = Cross(extra, stroke_color=ROLLBACK)
        self.play_beat(7, FadeOut(cohorts), FadeOut(delta_bars), FadeOut(average), FadeOut(average_tag), LaggedStart(*[FadeIn(a) for a in arms], lag_ratio=0.15), Create(rails), LaggedStart(*[FadeIn(x) for x in locks_grid], lag_ratio=0.1), FadeIn(extra), Create(extra_cross), settle=0.5)

        # 8 — positive and negative controls
        positive = self.badge("HELPFUL HINT", EVIDENCE, 2.15).shift(LEFT * 5.0 + UP * 1.0)
        negative = self.badge("INERT TOKEN", MUTED, 2.0).shift(LEFT * 5.0 + UP * -1.0)
        pipeline = self.panel("SAME PIPELINE", ACCENT, 3.0, 3.4)
        detected = self.badge("Δ DETECTED", EVIDENCE, 1.9).shift(RIGHT * 4.8 + UP * 1.0)
        inert = self.badge("FLAT", MUTED, 1.45).shift(RIGHT * 4.8 + UP * -1.0)
        p_arrow = Arrow(positive.get_right(), pipeline.get_left() + UP * 0.65, color=EVIDENCE, buff=0.12)
        n_arrow = Arrow(negative.get_right(), pipeline.get_left() + UP * -0.65, color=MUTED, buff=0.12)
        self.play_beat(8, FadeOut(arms), FadeOut(rails), FadeOut(locks_grid), FadeOut(extra), FadeOut(extra_cross), FadeIn(positive), FadeIn(negative), FadeIn(pipeline), GrowArrow(p_arrow), GrowArrow(n_arrow), FadeIn(detected), FadeIn(inert), settle=0.55)

        # 9 — failed positive control blocks the null
        flat_a = Line(LEFT * 1.8, RIGHT * 1.8, color=ROLLBACK, stroke_width=5).shift(UP * 1.0)
        flat_b = Line(LEFT * 1.8, RIGHT * 1.8, color=MUTED, stroke_width=5).shift(UP * -0.4)
        null = self.badge("NULL", AUTHORITY, 1.45).shift(LEFT * 4.8)
        incapable = self.badge("INCAPABLE", ROLLBACK, 1.9).shift(RIGHT * 4.7 + UP * 1.5)
        defects = self.grid(["FLOOR", "INSENSITIVE", "WRONG BOTTLENECK"], [AUTHORITY, AUTHORITY, AUTHORITY], 1, 2.4).shift(RIGHT * 3.7 + UP * -0.8)
        incapable_cross = Cross(incapable, stroke_color=ROLLBACK)
        self.play_beat(9, FadeOut(positive), FadeOut(negative), FadeOut(pipeline), FadeOut(p_arrow), FadeOut(n_arrow), FadeOut(detected), FadeOut(inert), FadeIn(null), Create(flat_a), Create(flat_b), FadeIn(incapable), Create(incapable_cross), LaggedStart(*[FadeIn(d) for d in defects], lag_ratio=0.18), settle=0.65)

        # 10 — elicitation competence receipt and arm split
        competence = self.receipt("ELICITATION COMPETENCE", AUTHORITY, 6.0, 4.4).shift(LEFT * 2.8)
        fields = self.grid(["PROMPTS", "SCAFFOLDS", "TOOLS", "ADAPT", "RESCUE", "STOP"], [AUTHORITY] * 6, 3, 1.45).scale(0.86).move_to(competence)
        policy = self.badge("DEPLOYED POLICY", EVIDENCE, 2.25).shift(RIGHT * 4.4 + UP * 1.05)
        elicited = self.badge("ELICITED CAPABILITY", ACCENT, 2.45).shift(RIGHT * 4.4 + UP * -1.05)
        membrane = DashedLine(LEFT * 1.4, RIGHT * 1.4, color=ROLLBACK, stroke_width=4).shift(RIGHT * 4.4)
        self.play_beat(10, FadeOut(null), FadeOut(flat_a), FadeOut(flat_b), FadeOut(incapable), FadeOut(incapable_cross), FadeOut(defects), FadeIn(competence), LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.1), FadeIn(policy), FadeIn(elicited), Create(membrane), settle=0.55)

        # 11 — D0 knowledge
        ladder = self.ladder().shift(RIGHT * 2.2)
        token = self.actor("FINDING", ACCENT).next_to(ladder[1][0], LEFT, buff=0.55)
        d0_lock = self.badge("BRIDGE LOCKED", ROLLBACK, 2.0).next_to(ladder[1][0], RIGHT, buff=0.5)
        question = self.badge("CALIBRATED Q", AUTHORITY, 2.0).shift(LEFT * 4.4)
        self.play_beat(11, FadeOut(competence), FadeOut(fields), FadeOut(policy), FadeOut(elicited), FadeOut(membrane), FadeIn(ladder), FadeIn(question), FadeIn(token), FadeIn(d0_lock), Indicate(ladder[1][0], color=ACCENT), settle=0.45)

        # 12 — D1 component
        mini = self.panel("SAFE COMPONENT", EVIDENCE, 3.1, 2.4).shift(LEFT * 4.1)
        control = self.badge("CONTROL ✓", EVIDENCE, 1.65).move_to(mini)
        token_d1 = token.copy().next_to(ladder[1][1], LEFT, buff=0.55)
        d2_lock = self.badge("WORKFLOW? LOCKED", ROLLBACK, 2.3).next_to(ladder[1][1], RIGHT, buff=0.45)
        self.play_beat(12, FadeOut(question), FadeOut(d0_lock), FadeIn(mini), FadeIn(control), Transform(token, token_d1), FadeIn(d2_lock), Indicate(ladder[1][1], color=EVIDENCE), settle=0.45)

        # 13 — D2 bounded workflow
        workflow_names = ["PLAN", "ACT", "ERROR", "RECOVER", "COMPLETE"]
        workflow = VGroup(*[self.badge(n, EVIDENCE if n != "ERROR" else ROLLBACK, 1.45, 0.5) for n in workflow_names]).arrange(RIGHT, buff=0.22).scale(0.9).shift(LEFT * 2.4)
        flow_edges = VGroup(*[Arrow(workflow[i].get_right(), workflow[i + 1].get_left(), color=BOUNDARY, buff=0.06, stroke_width=2.5) for i in range(len(workflow) - 1)])
        omitted = self.badge("OMITTED REAL STEP", AUTHORITY, 2.35).shift(LEFT * 2.0 + UP * -1.45)
        token_d2 = token.copy().next_to(ladder[1][2], LEFT, buff=0.55)
        self.play_beat(13, FadeOut(mini), FadeOut(control), FadeOut(d2_lock), LaggedStart(*[FadeIn(x) for x in workflow], lag_ratio=0.1), Create(flow_edges), FadeIn(omitted), Transform(token, token_d2), Indicate(ladder[1][2], color=EVIDENCE), settle=0.5)

        # 14 — D3 uplift with uncertainty
        without = self.actor("WITHOUT", MUTED).shift(LEFT * 4.5 + UP * -0.7)
        with_ai = self.actor("WITH AI", ACCENT).shift(LEFT * 0.8 + UP * -0.7)
        delta_line = Line(without.get_right(), with_ai.get_left(), color=EVIDENCE, stroke_width=6)
        uncertainty = DashedLine(LEFT * 0.65, RIGHT * 0.65, color=AUTHORITY, stroke_width=5).move_to(delta_line)
        tags = self.grid(["COHORT", "CONTRACT", "TASKS", "ACCESS", "UNCERTAINTY"], [AUTHORITY] * 5, 3, 1.55).scale(0.82).shift(LEFT * 2.6 + UP * 1.25)
        token_d3 = token.copy().next_to(ladder[1][3], LEFT, buff=0.55)
        self.play_beat(14, FadeOut(workflow), FadeOut(flow_edges), FadeOut(omitted), FadeIn(without), FadeIn(with_ai), Create(delta_line), Create(uncertainty), FadeIn(tags), Transform(token, token_d3), Indicate(ladder[1][3], color=EVIDENCE), settle=0.5)

        # 15 — D4 fixed challenge budget
        budget = VGroup(*[Circle(radius=0.18, stroke_color=AUTHORITY, fill_color=AUTHORITY, fill_opacity=0.6) for _ in range(7)]).arrange(RIGHT, buff=0.16).shift(LEFT * 4.2 + UP * 1.6)
        guard = self.panel("SAFEGUARD", AUTHORITY, 2.7, 2.7).shift(LEFT * 1.7)
        outcomes = self.grid(["PASS", "BYPASS", "FAILED ATTEMPT"], [EVIDENCE, ROLLBACK, MUTED], 1, 2.2).shift(RIGHT * 1.3)
        budget_wall = Line(UP * 2.0, UP * -2.0, color=ROLLBACK, stroke_width=5).shift(RIGHT * 3.4)
        unknown = self.badge("UNTESTED · UNKNOWN", RESIDUAL, 2.6).shift(RIGHT * 5.0)
        token_d4 = token.copy().next_to(ladder[1][4], LEFT, buff=0.55)
        self.play_beat(15, FadeOut(without), FadeOut(with_ai), FadeOut(delta_line), FadeOut(uncertainty), FadeOut(tags), LaggedStart(*[FadeIn(b) for b in budget], lag_ratio=0.08), FadeIn(guard), FadeIn(outcomes), Create(budget_wall), FadeIn(unknown), Transform(token, token_d4), settle=0.55)

        # 16 — D5 and bridge-required ladder
        incidents = VGroup(*[Dot(color=RESIDUAL, radius=0.13).shift(RIGHT * x + UP * y) for x, y in [(3.7, 1.4), (4.4, 0.8), (5.0, 1.7), (4.2, -0.1)]] )
        incident_frame = self.panel("FIELD CONSEQUENCE", RESIDUAL, 3.5, 3.4).shift(RIGHT * 4.2)
        bridges = VGroup(*[self.badge("BRIDGE", AUTHORITY, 1.25, 0.38).next_to(ladder[1][i], RIGHT, buff=0.28) for i in range(5)])
        token_d5 = token.copy().next_to(ladder[1][5], LEFT, buff=0.55)
        recoil = ArcBetweenPoints(token_d5.get_center(), token.get_center(), angle=0.4, color=ROLLBACK)
        self.play_beat(16, FadeOut(budget), FadeOut(guard), FadeOut(outcomes), FadeOut(budget_wall), FadeOut(unknown), FadeIn(bridges), FadeIn(incident_frame), FadeIn(incidents), Transform(token, token_d5), MoveAlongPath(token, recoil), Indicate(bridges[-1], color=ROLLBACK), settle=0.6)

        # 17 — outcome vector, not scalar
        scalar = self.badge("RISK 87", ROLLBACK, 2.4, 1.0).shift(LEFT * 4.7)
        outcome_names = ["COMPLETE", "QUALITY", "TIME", "ERROR", "UNSAFE", "REFUSAL", "INTERVENE", "HELP", "ABANDON", "BURDEN", "COST", "RESIDUAL"]
        outcome_colors = [EVIDENCE, EVIDENCE, AUTHORITY, ROLLBACK, ROLLBACK, MUTED, AUTHORITY, ACCENT, MUTED, AUTHORITY, AUTHORITY, RESIDUAL]
        vector = self.grid(outcome_names, outcome_colors, 4, 1.55).scale(0.92).shift(RIGHT * 1.3)
        scalar_cross = Cross(scalar, stroke_color=ROLLBACK)
        self.play_beat(17, FadeOut(ladder), FadeOut(token), FadeOut(bridges), FadeOut(incident_frame), FadeOut(incidents), FadeIn(scalar), Create(scalar_cross), LaggedStart(*[FadeIn(v) for v in vector], lag_ratio=0.07), settle=0.5)

        # 18 — restricted annex and public card
        annex = self.receipt("RESTRICTED ANNEX", RESIDUAL, 5.0, 4.4).shift(LEFT * 3.7)
        annex_fields = self.grid(["TASKS", "TRACES", "DETAILS", "ACCESS LOG", "RETENTION"], [RESIDUAL] * 5, 2, 1.55).scale(0.85).move_to(annex)
        public = self.receipt("PUBLIC CARD", AUTHORITY, 5.0, 4.4).shift(RIGHT * 3.7)
        public_fields = self.grid(["METHOD", "UNCERTAINTY", "LIMITS", "CANNOT CHECK"], [AUTHORITY] * 4, 2, 1.7).scale(0.9).move_to(public)
        digest = self.badge("DIGEST", EVIDENCE, 1.4).shift(UP * -2.65)
        link_a = Line(annex.get_right(), digest.get_left(), color=EVIDENCE, stroke_width=3)
        link_b = Line(digest.get_right(), public.get_left(), color=EVIDENCE, stroke_width=3)
        self.play_beat(18, FadeOut(scalar), FadeOut(scalar_cross), FadeOut(vector), FadeIn(annex), FadeIn(annex_fields), FadeIn(public), FadeIn(public_fields), FadeIn(digest), Create(link_a), Create(link_b), settle=0.65)

        # 19 — independent review fork
        review = self.panel("INDEPENDENT REVIEW", AUTHORITY, 3.3, 2.5)
        invalid = self.badge("INVALID", ROLLBACK, 1.5).shift(LEFT * 4.4 + UP * 1.7)
        unsafe = self.badge("UNSAFE", ROLLBACK, 1.5).shift(LEFT * 4.4)
        narrow = self.badge("NARROW", AUTHORITY, 1.5).shift(LEFT * 4.4 + UP * -1.7)
        quarantine = self.panel("QUARANTINE", ROLLBACK, 2.9, 2.4).shift(LEFT * 4.7)
        bounded = self.panel("BOUNDED DOSSIER", EVIDENCE, 3.2, 2.4).shift(RIGHT * 4.7)
        pass_gate = RoundedRectangle(width=0.75, height=2.7, corner_radius=0.1, stroke_color=AUTHORITY, stroke_width=4).shift(RIGHT * 2.35)
        self.play_beat(19, FadeOut(annex), FadeOut(annex_fields), FadeOut(public), FadeOut(public_fields), FadeOut(digest), FadeOut(link_a), FadeOut(link_b), FadeIn(review), FadeIn(invalid), FadeIn(unsafe), FadeIn(narrow), FadeIn(quarantine), FadeIn(bounded), Create(pass_gate), Indicate(quarantine, color=ROLLBACK), settle=0.6)

        # 20 — complete uplift dossier fields
        dossier = self.receipt("UPLIFT DOSSIER", AUTHORITY, 11.0, 5.3)
        dossier_fields = self.grid(["MODEL", "CHECKPOINT", "POLICY", "SCAFFOLD", "TOOLS", "GUARDS", "THREAT v", "COHORT", "COMPARATOR", "EVALUATOR", "ATTEMPTS", "UNCERTAINTY", "EXPIRY", "MAX INFERENCE"], [AUTHORITY] * 14, 5, 1.65).scale(0.78).shift(UP * -0.15)
        maximum = self.badge("MAXIMUM INFERENCE", EVIDENCE, 2.7, 0.7).shift(UP * -2.65)
        self.play_beat(20, FadeOut(review), FadeOut(invalid), FadeOut(unsafe), FadeOut(narrow), FadeOut(quarantine), FadeOut(bounded), FadeOut(pass_gate), FadeIn(dossier), LaggedStart(*[FadeIn(f) for f in dossier_fields], lag_ratio=0.06), FadeIn(maximum), Indicate(maximum, color=EVIDENCE), settle=0.55)

        # 21 — scoped consumers, expiry, supersession
        packet = self.badge("BOUNDED PACKET", EVIDENCE, 2.3).shift(UP * 1.5)
        consumer_names = ["THRESHOLD", "RELEASE", "MONITOR", "SAFETY CASE", "RESILIENCE"]
        consumers = VGroup(*[self.badge(n, AUTHORITY, 1.75, 0.5) for n in consumer_names]).arrange(RIGHT, buff=0.28).shift(UP * -0.2).scale(0.85)
        danger = self.badge("DANGER LABEL", ROLLBACK, 2.0).shift(LEFT * 4.9 + UP * -1.7)
        expired = self.badge("MODEL Δ → EXPIRED", ROLLBACK, 2.5).shift(RIGHT * 1.2 + UP * -1.7)
        archive = self.panel("SUPERSEDED RECEIPT", MUTED, 3.2, 1.7).shift(RIGHT * 4.7 + UP * -1.8)
        danger_cross = Cross(danger, stroke_color=ROLLBACK)
        self.play_beat(21, FadeOut(dossier), FadeOut(dossier_fields), FadeOut(maximum), FadeIn(packet), LaggedStart(*[TransformFromCopy(packet, c) for c in consumers], lag_ratio=0.1), FadeIn(danger), Create(danger_cross), FadeIn(expired), FadeIn(archive), settle=0.55)

        # 22 — current evidence boundary
        supported = self.grid(["DESIGN RATIONALE", "PUBLIC-SAFE ARCHITECTURE"], [AUTHORITY, AUTHORITY], 1, 3.2).shift(LEFT * 3.6)
        boundary = Line(UP * 2.9, UP * -2.9, color=ROLLBACK, stroke_width=6)
        unrun = self.grid(["NO UPLIFT STUDY", "NO THRESHOLD", "NO SAFEGUARD RESULT", "NO DANGER / SAFETY"], [MUTED] * 4, 1, 2.8).shift(RIGHT * 3.6)
        support_tag = self.badge("ARGUMENT SUPPORT", AUTHORITY, 2.3).shift(LEFT * 3.6 + UP * -2.3)
        self.play_beat(22, FadeOut(packet), FadeOut(consumers), FadeOut(danger), FadeOut(danger_cross), FadeOut(expired), FadeOut(archive), FadeIn(supported), Create(boundary), FadeIn(unrun), FadeIn(support_tag), Indicate(boundary, color=ROLLBACK), settle=0.65)

        # 23 — protect the null with five locks
        null_token = self.badge("NULL", AUTHORITY, 1.5).shift(LEFT * 5.3)
        lock_names = ["POSITIVE", "VALID TASK", "ELICITATION", "SENSITIVITY", "BALANCE"]
        lock_colors = [EVIDENCE, EVIDENCE, EVIDENCE, ROLLBACK, EVIDENCE]
        null_locks = VGroup(*[self.badge(n, lock_colors[i], 1.75, 0.5) for i, n in enumerate(lock_names)]).arrange(RIGHT, buff=0.22).scale(0.82)
        absent = self.badge("ABSENT CAPABILITY", ROLLBACK, 2.35).shift(RIGHT * 4.6 + UP * 1.2)
        instrument_failure = self.badge("INSTRUMENT FAILURE", AUTHORITY, 2.55).shift(RIGHT * 4.6 + UP * -1.2)
        route_down = ArcBetweenPoints(null_locks.get_right(), instrument_failure.get_left(), angle=-0.35, color=AUTHORITY)
        absent_cross = Cross(absent, stroke_color=ROLLBACK)
        self.play_beat(23, FadeOut(supported), FadeOut(boundary), FadeOut(unrun), FadeOut(support_tag), FadeIn(null_token), LaggedStart(*[FadeIn(l) for l in null_locks], lag_ratio=0.12), FadeIn(absent), Create(absent_cross), FadeIn(instrument_failure), Create(route_down), Indicate(null_locks[3], color=ROLLBACK), settle=0.7)

        # 24 — governed packet payoff
        custody = self.receipt("GOVERNED UPLIFT PACKET", AUTHORITY, 9.5, 4.8)
        packet_fields = self.grid(["BOUNDED Δ", "RESIDUAL OPEN", "ANNEX SEALED", "EXPIRES", "MAX INFERENCE"], [EVIDENCE, RESIDUAL, RESIDUAL, AUTHORITY, EVIDENCE], 5, 1.65).scale(0.9)
        ownership = self.badge("DECISION CONTEXT INTACT", AUTHORITY, 2.8).shift(UP * -2.35)
        self.play_beat(24, FadeOut(null_token), FadeOut(null_locks), FadeOut(absent), FadeOut(absent_cross), FadeOut(instrument_failure), FadeOut(route_down), FadeIn(custody), LaggedStart(*[FadeIn(f) for f in packet_fields], lag_ratio=0.12), FadeIn(ownership), settle=0.7)

        # 25 — handoff to military AI
        final_packet = self.panel("BOUNDED EVIDENCE", AUTHORITY, 3.7, 2.5).shift(LEFT * 4.2)
        no_command = self.badge("NO COMMAND AUTHORITY", ROLLBACK, 2.65).next_to(final_packet, UP * -1, buff=0.35)
        handoff = Line(UP * 2.8, UP * -2.8, color=AUTHORITY, stroke_width=5)
        command = self.panel("NEXT · MILITARY AI", COPPER, 4.3, 3.1).shift(RIGHT * 4.0)
        nodes = VGroup(*[self.actor(n, COPPER if i == 1 else MUTED, "square") for i, n in enumerate(["SENSE", "COMMAND", "ACT"])]).arrange(RIGHT, buff=0.55).scale(0.75).move_to(command)
        command_edges = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=COPPER, buff=0.08, stroke_width=3) for i in range(2)])
        footer = self.label("DESIGN RATIONALE · ARGUMENT SUPPORT · NO HAZARDOUS-DOMAIN RESULT", 13, AUTHORITY, "BOLD").shift(UP * -3.55)
        self.play_beat(25, FadeOut(custody), FadeOut(packet_fields), FadeOut(ownership), FadeIn(final_packet), FadeIn(no_command), Create(handoff), FadeIn(command), FadeIn(nodes), Create(command_edges), FadeIn(footer), settle=0.8)

        self.wait_until(self.TARGET_DURATION)
