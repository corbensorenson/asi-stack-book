"""Generation-2 visual abstract for Military AI and Strategic Stability.

A synthetic duplicated-feed warning trace expands into command, judgment,
interaction, assurance, suspension, and evidence-boundary governance. The
scene contains no weapon operation, targeting procedure, or real sensor data.
"""

from __future__ import annotations

from manim import (
    Arc, Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn, FadeOut,
    GrowArrow, Indicate, LaggedStart, LEFT, Line, MoveAlongPath, Rectangle,
    ReplacementTransform, RIGHT, RoundedRectangle, Square, Succession, Text,
    Transform, TransformFromCopy, Triangle, UP, VGroup,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class MilitaryAIInteractionGeneration2(AsiScene):
    TARGET_DURATION = 329.645
    ENDS = [
        8.450, 15.855, 30.860, 36.200, 46.540, 58.670, 71.050,
        83.555, 95.960, 109.615, 122.545, 134.650, 145.505, 157.685,
        169.390, 182.270, 194.150, 208.630, 223.335, 237.840, 250.470,
        264.550, 279.580, 287.218, 295.335, 309.265, 321.120, 329.645,
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
                LaggedStart(*animations, lag_ratio=0.15),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 19, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.8, height: float = 0.56) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1,
            stroke_color=color, stroke_width=2.5,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float = 3.4, height: float = 2.4) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=color, stroke_width=3,
            fill_color="#172A33", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.4, 2.7), 0.48).scale(0.8)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 1.55) -> VGroup:
        cells = VGroup(*[self.badge(value, colors[i], width, 0.5) for i, value in enumerate(values)])
        cells.arrange_in_grid(rows=(len(values) + columns - 1) // columns, cols=columns, buff=(0.18, 0.22))
        return cells

    def clock(self, value: str, color: str = AUTHORITY, radius: float = 1.15) -> VGroup:
        ring = Circle(radius=radius, stroke_color=color, stroke_width=6, fill_color="#172A33", fill_opacity=1)
        hand = Line(ring.get_center(), ring.get_center() + UP * radius * 0.68, color=color, stroke_width=5)
        return VGroup(ring, hand, self.label(value, 18, color, "BOLD").move_to(ring.get_center() + UP * -0.25))

    def actor(self, name: str, color: str) -> VGroup:
        shell = RoundedRectangle(
            width=2.5, height=2.0, corner_radius=0.16,
            stroke_color=color, stroke_width=3,
            fill_color="#172A33", fill_opacity=1,
        )
        return VGroup(shell, self.label(name, 17, color, "BOLD").next_to(shell, UP, buff=-0.3))

    def construct(self) -> None:
        # 1 — high-confidence synthetic warning
        sensor_a = self.badge("SENSOR A", ACCENT, 2.0).shift(LEFT * 4.8 + UP * 1.4)
        sensor_b = self.badge("SENSOR B", ACCENT, 2.0).shift(LEFT * 4.8 + UP * -0.1)
        confidence = self.badge("HIGH CONFIDENCE", EVIDENCE, 2.5).shift(LEFT * 1.7 + UP * 0.65)
        clock = self.clock("12 MIN").shift(RIGHT * 1.4)
        command_bar = Line(UP * 2.6, UP * -2.6, color=AUTHORITY, stroke_width=6).shift(RIGHT * 4.9)
        command_tag = self.badge("COMMAND", AUTHORITY, 1.75).next_to(command_bar, UP, buff=-0.3)
        recommendation = self.badge("RECOMMEND", ACCENT, 2.0).shift(RIGHT * 3.4)
        scene1 = VGroup(sensor_a, sensor_b, confidence, clock, command_bar, command_tag, recommendation)
        self.play_beat(1, FadeIn(sensor_a), FadeIn(sensor_b), FadeIn(confidence), FadeIn(clock), Create(command_bar), FadeIn(command_tag), FadeIn(recommendation), settle=0.45)

        # 2 — duplicated lineage and compressed time
        source = self.badge("ONE UPSTREAM FEED", ROLLBACK, 2.8).shift(LEFT * 4.7 + UP * -2.2)
        edge_a = Arrow(source.get_top(), sensor_a.get_bottom(), color=ROLLBACK, buff=0.08)
        edge_b = Arrow(source.get_top(), sensor_b.get_bottom(), color=ROLLBACK, buff=0.08)
        count_two = self.badge("2 DISPLAYS", MUTED, 1.8).shift(LEFT * 1.7 + UP * -0.5)
        count_one = self.badge("1 LINEAGE", ROLLBACK, 1.8).move_to(count_two)
        clock_two = self.clock("2 MIN", ROLLBACK, 0.85).move_to(clock)
        residual = self.badge("CORRELATION OPEN", RESIDUAL, 2.35).shift(RIGHT * 1.6 + UP * -2.2)
        scene2 = VGroup(sensor_a, sensor_b, source, edge_a, edge_b, count_one, clock_two, command_bar, command_tag, recommendation, residual)
        self.play_beat(2, FadeOut(confidence), FadeIn(source), GrowArrow(edge_a), GrowArrow(edge_b), FadeIn(count_two), ReplacementTransform(count_two, count_one), ReplacementTransform(clock, clock_two), FadeIn(residual), settle=0.45)

        # 3 — four roles, not one autonomy score
        dial = Circle(radius=1.25, stroke_color=MUTED, stroke_width=5).shift(LEFT * 4.6)
        dial_label = self.label("AUTONOMY\nSCORE", 17, MUTED, "BOLD").move_to(dial)
        dial_group = VGroup(dial, dial_label)
        dial_cross = Cross(dial_group, stroke_color=ROLLBACK)
        crossed_dial = VGroup(dial_group, dial_cross)
        roles = self.grid(
            ["DECISION SUPPORT", "DEFENSIVE AUTO", "TARGETING SUPPORT", "AUTONOMOUS FORCE"],
            [ACCENT, EVIDENCE, AUTHORITY, ROLLBACK], 1, 2.55,
        ).shift(LEFT * 0.8)
        role_gates = VGroup(*[
            RoundedRectangle(width=0.75, height=0.48, corner_radius=0.08, stroke_color=c, stroke_width=3)
            for c in [ACCENT, EVIDENCE, AUTHORITY, ROLLBACK]
        ]).arrange(UP * -1, buff=0.28).shift(RIGHT * 2.0)
        consequences = self.grid(["ROLE", "AUTH", "PEOPLE", "REVERSIBLE", "ESCALATION"], [MUTED] * 5, 1, 1.8).scale(0.82).shift(RIGHT * 4.4)
        scene3 = VGroup(roles, role_gates, consequences)
        self.play_beat(
            3,
            FadeOut(scene2),
            Succession(FadeIn(dial_group), Create(dial_cross), FadeOut(crossed_dial), FadeIn(roles)),
            FadeIn(role_gates),
            FadeIn(consequences),
            settle=0.55,
        )

        # 4 — local green score, unstable interaction
        local = self.badge("LOCAL SCORE ✓", EVIDENCE, 2.2).shift(LEFT * 1.3)
        unstable = Circle(radius=2.0, stroke_color=ROLLBACK, stroke_width=6).move_to(local)
        unstable_tag = self.badge("SYSTEM UNSTABLE", ROLLBACK, 2.35).next_to(unstable, UP, buff=0.3)
        scene4 = VGroup(local, unstable, unstable_tag)
        self.play_beat(4, FadeOut(scene3), FadeIn(local), Create(unstable), FadeIn(unstable_tag), Indicate(local, color=EVIDENCE), Indicate(unstable, color=ROLLBACK), settle=0.35)

        # 5 — the joint strategic claim
        dependency_names = ["SENSORS", "PEOPLE", "COMMAND", "COMMS", "ADVERSARY", "TIME", "OFF-RAMPS"]
        dependencies = VGroup(*[self.badge(name, MUTED, 1.5, 0.48) for name in dependency_names])
        positions = [LEFT * 4.8 + UP * 1.8, LEFT * 4.8, LEFT * 4.8 + UP * -1.8, RIGHT * 1.8 + UP * 2.2, RIGHT * 4.5 + UP * 1.2, RIGHT * 4.5 + UP * -0.8, RIGHT * 1.8 + UP * -2.2]
        for dep, pos in zip(dependencies, positions):
            dep.move_to(pos)
        joint_edges = VGroup(*[Line(dep.get_center(), local.get_center(), color=BOUNDARY, stroke_width=2) for dep in dependencies])
        joint = self.badge("JOINT CLAIM", AUTHORITY, 2.1).shift(RIGHT * 1.8)
        scene5 = VGroup(local, dependencies, joint_edges, joint)
        self.play_beat(5, FadeOut(unstable), FadeOut(unstable_tag), LaggedStart(*[FadeIn(d) for d in dependencies], lag_ratio=0.08), Create(joint_edges), FadeIn(joint), Indicate(joint, color=AUTHORITY), settle=0.4)

        # 6 — mission envelope
        mission = self.panel("MISSION ENVELOPE", AUTHORITY, 8.0, 4.6)
        mission_fields = self.grid(["PURPOSE", "ENVIRONMENT", "POPULATION", "LEGAL REVIEW", "COMMAND CHAIN", "TIME", "TERMINATION"], [AUTHORITY] * 7, 4, 1.65).move_to(mission)
        vague = self.badge("VAGUE OBJECTIVE", ROLLBACK, 2.3).shift(LEFT * 5.2)
        vague_cross = Cross(vague, stroke_color=ROLLBACK)
        scene6 = VGroup(mission, mission_fields, vague, vague_cross)
        self.play_beat(6, FadeOut(scene5), FadeIn(mission), LaggedStart(*[FadeIn(f) for f in mission_fields], lag_ratio=0.1), FadeIn(vague), Create(vague_cross), Indicate(mission_fields[-1], color=AUTHORITY), settle=0.55)

        # 7 — typed authority and effect rail
        permission_names = ["OBSERVE", "RECOMMEND", "APPROVE", "ACT"]
        permissions = VGroup(*[self.badge(n, [ACCENT, ACCENT, AUTHORITY, ROLLBACK][i], 1.85) for i, n in enumerate(permission_names)]).arrange(RIGHT, buff=0.65).shift(UP * 1.0)
        permission_edges = VGroup(*[Arrow(permissions[i].get_right(), permissions[i + 1].get_left(), color=BOUNDARY, buff=0.08) for i in range(3)])
        limits = self.grid(["TARGET CLASS", "PROHIBITED EFFECT", "SCOPE", "ABSTAIN", "COMMS LOSS", "HUMAN CONFIRM"], [AUTHORITY] * 6, 3, 2.0).shift(UP * -1.2)
        recommend_gap = DashedLine(permissions[1].get_right(), permissions[2].get_left(), color=AUTHORITY, stroke_width=5)
        scene7 = VGroup(permissions, permission_edges, limits, recommend_gap)
        self.play_beat(7, FadeOut(scene6), LaggedStart(*[FadeIn(p) for p in permissions], lag_ratio=0.12), Create(permission_edges), FadeIn(limits), Create(recommend_gap), Indicate(recommend_gap, color=AUTHORITY), settle=0.55)

        # 8 — meaningful human judgment conditions
        human_icon = VGroup(Circle(radius=0.6, stroke_color=MUTED, stroke_width=4), self.label("HUMAN", 13, MUTED, "BOLD")).shift(LEFT * 4.7)
        owner = self.panel("ACCOUNTABLE OWNER", AUTHORITY, 2.8, 2.1)
        judgment = self.grid(["TIME", "CONTEXT", "ALTERNATIVES", "COMPETENCE", "INDEPENDENCE", "REJECT · DELAY · NARROW · STOP"], [AUTHORITY] * 6, 2, 2.2).scale(0.9).shift(RIGHT * 3.7)
        icon_cross = Cross(human_icon, stroke_color=ROLLBACK)
        scene8 = VGroup(owner, judgment)
        self.play_beat(8, FadeOut(scene7), FadeIn(human_icon), Create(icon_cross), FadeOut(human_icon), FadeOut(icon_cross), FadeIn(owner), LaggedStart(*[FadeIn(j) for j in judgment], lag_ratio=0.1), Indicate(judgment[-1], color=AUTHORITY), settle=0.65)

        # 9 — deliberation budget
        budget_names = ["VERIFY", "CONSULT", "LEGAL", "COMMUNICATE"]
        budget = VGroup(*[Rectangle(width=2.0, height=0.45, stroke_color=c, fill_color=c, fill_opacity=0.55) for c in [ACCENT, EVIDENCE, AUTHORITY, COPPER]]).arrange(UP * -1, buff=0.38).shift(LEFT * 2.5)
        budget_labels = VGroup(*[self.label(n, 14, INK, "BOLD").move_to(budget[i]) for i, n in enumerate(budget_names)])
        click = self.badge("FINAL CLICK", MUTED, 1.8).shift(RIGHT * 4.2)
        not_judgment = self.badge("≠ JUDGMENT", ROLLBACK, 1.8).next_to(click, UP * -1, buff=0.35)
        shear = Line(UP * 2.4, UP * -2.4, color=ROLLBACK, stroke_width=6).shift(RIGHT * 0.9)
        scene9 = VGroup(budget, budget_labels, click, not_judgment, shear)
        self.play_beat(9, FadeOut(scene8), FadeIn(budget), FadeIn(budget_labels), Create(shear), LaggedStart(*[FadeOut(b) for b in budget], lag_ratio=0.15), FadeOut(budget_labels), FadeIn(click), FadeIn(not_judgment), settle=0.7)

        # 10 — reopen provenance trace
        sensors = VGroup(self.badge("SENSOR A", ACCENT, 1.75), self.badge("SENSOR B", ACCENT, 1.75)).arrange(UP * -1, buff=0.7).shift(LEFT * 4.8)
        receipt_fields = self.grid(["SOURCE", "TIME", "TRANSFORM", "UNCERTAINTY", "INTEGRITY", "CORRELATION"], [AUTHORITY] * 6, 3, 1.65).shift(LEFT * 0.6)
        root = self.badge("ONE FEED", ROLLBACK, 1.8).shift(RIGHT * 3.2 + UP * -1.5)
        roots = VGroup(*[Arrow(s.get_right(), root.get_left(), color=ROLLBACK, buff=0.08) for s in sensors])
        counter = self.badge("2 DISPLAYS → 1 LINEAGE", ROLLBACK, 2.9).shift(RIGHT * 3.3 + UP * 1.2)
        scene10 = VGroup(sensors, receipt_fields, root, roots, counter)
        self.play_beat(10, FadeOut(scene9), FadeIn(sensors), LaggedStart(*[FadeIn(f) for f in receipt_fields], lag_ratio=0.08), FadeIn(root), Create(roots), FadeIn(counter), Indicate(counter, color=ROLLBACK), settle=0.6)

        # 11 — typed defects cannot mint truth or authority
        defects = self.grid(["AMBIGUOUS", "SPOOFED", "STALE", "CORRELATED"], [RESIDUAL, ROLLBACK, MUTED, AUTHORITY], 1, 1.9).shift(LEFT * 4.7)
        comparator = self.panel("COMPARE HYPOTHESES", ACCENT, 3.2, 3.1)
        truth = self.badge("NO TRUTH MINT", ROLLBACK, 2.2).shift(RIGHT * 4.6 + UP * 1.0)
        authority = self.badge("NO AUTHORITY MINT", AUTHORITY, 2.4).shift(RIGHT * 4.6 + UP * -1.0)
        fluent = self.badge("FLUENT ANSWER", ACCENT, 2.0).shift(LEFT * 1.9)
        stops = VGroup(Cross(truth, stroke_color=ROLLBACK), Cross(authority, stroke_color=ROLLBACK))
        scene11 = VGroup(defects, comparator, truth, authority, fluent, stops)
        self.play_beat(11, FadeOut(scene10), FadeIn(defects), FadeIn(comparator), FadeIn(fluent), TransformFromCopy(fluent, truth), TransformFromCopy(fluent, authority), Create(stops), settle=0.65)

        # 12 — abstention routes to owned safe posture
        failure_tokens = self.grid(["CONFLICT", "INTEGRITY FAIL", "COMMS LOSS", "OUT OF ENVELOPE"], [ROLLBACK] * 4, 1, 2.1).shift(LEFT * 4.6)
        posture = self.panel("SAFE POSTURE", AUTHORITY, 3.3, 3.5)
        posture_fields = self.grid(["OWNER", "DURATION", "MONITOR", "RE-ENTRY"], [AUTHORITY] * 4, 2, 1.5).move_to(posture)
        posture_edges = VGroup(*[Arrow(t.get_right(), posture.get_left(), color=AUTHORITY, buff=0.08) for t in failure_tokens])
        scene12 = VGroup(failure_tokens, posture, posture_fields, posture_edges)
        self.play_beat(12, FadeOut(scene11), FadeIn(failure_tokens), FadeIn(posture), Create(posture_edges), LaggedStart(*[FadeIn(f) for f in posture_fields], lag_ratio=0.12), settle=0.6)

        # 13 — safe posture is contextual but authority stays fixed
        alternatives = self.grid(["HOLD", "WITHDRAW", "SHIELD", "VERIFY"], [MUTED, AUTHORITY, EVIDENCE, ACCENT], 4, 1.6).shift(LEFT * 1.2)
        envelope = RoundedRectangle(width=8.0, height=2.3, corner_radius=0.16, stroke_color=AUTHORITY, stroke_width=4)
        same_auth = self.badge("SAME AUTHORITY", AUTHORITY, 2.2).next_to(envelope, UP, buff=-0.1)
        urgency = self.badge("URGENT EXPANSION", ROLLBACK, 2.35).shift(RIGHT * 5.2 + UP * -1.7)
        urgency_cross = Cross(urgency, stroke_color=ROLLBACK)
        scene13 = VGroup(envelope, same_auth, alternatives, urgency, urgency_cross)
        self.play_beat(13, FadeOut(scene12), Create(envelope), FadeIn(same_auth), LaggedStart(*[FadeIn(a) for a in alternatives], lag_ratio=0.12), FadeIn(urgency), Create(urgency_cross), settle=0.65)

        # 14 — advice becomes de facto command pressure
        advice = self.badge("ADVICE", ACCENT, 2.0).shift(LEFT * 4.7)
        pressures = self.grid(["REPEATED", "RANKED #1", "DEFAULT", "COUNTDOWN"], [ROLLBACK] * 4, 1, 1.75).shift(LEFT * 2.0)
        cmd_boundary = Line(UP * 2.7, UP * -2.7, color=AUTHORITY, stroke_width=6).shift(RIGHT * 1.0)
        disclosure = self.grid(["UNCERTAINTY", "ALTERNATIVES", "PROVENANCE", "OWNER"], [AUTHORITY] * 4, 1, 1.8).shift(RIGHT * 3.5)
        scene14 = VGroup(advice, pressures, cmd_boundary, disclosure)
        self.play_beat(14, FadeOut(scene13), FadeIn(advice), FadeIn(pressures), Transform(advice, advice.copy().scale(1.5).shift(RIGHT * 4.8)), Create(cmd_boundary), FadeIn(disclosure), Indicate(cmd_boundary, color=AUTHORITY), settle=0.7)

        # 15 — compressed time deletes reachable routes
        clock12 = self.clock("12 MIN", AUTHORITY, 1.25).shift(LEFT * 3.8)
        verify_path = Line(LEFT * 2.0, RIGHT * 1.2, color=EVIDENCE, stroke_width=5).shift(UP * 1.0)
        off_ramp = Line(LEFT * 2.0, RIGHT * 1.2, color=AUTHORITY, stroke_width=5).shift(UP * -1.0)
        command_gate = Line(UP * 2.6, UP * -2.6, color=ROLLBACK, stroke_width=6).shift(RIGHT * 4.2)
        clock2 = self.clock("2 MIN", ROLLBACK, 0.8).move_to(clock12)
        brittle = self.badge("BRITTLE LOOP", RESIDUAL, 2.1).shift(RIGHT * 2.0 + UP * -2.0)
        scene15 = VGroup(clock2, command_gate, brittle)
        self.play_beat(15, FadeOut(scene14), FadeIn(clock12), Create(verify_path), Create(off_ramp), Create(command_gate), ReplacementTransform(clock12, clock2), FadeOut(verify_path), FadeOut(off_ramp), FadeIn(brittle), settle=0.7)

        # 16 — add the reciprocal actor
        actor_a = self.actor("ACTOR A", ACCENT).shift(LEFT * 4.2)
        actor_b = self.actor("ACTOR B", COPPER).shift(RIGHT * 4.2)
        observe_ab = Arrow(actor_a.get_right(), actor_b.get_left(), color=ACCENT, buff=0.15).shift(UP * 0.55)
        observe_ba = Arrow(actor_b.get_left(), actor_a.get_right(), color=COPPER, buff=0.15).shift(UP * -0.55)
        clock_a = self.badge("CLOCK Δ", ROLLBACK, 1.5).next_to(actor_a, UP * -1, buff=0.25)
        clock_b = self.badge("CLOCK Δ", ROLLBACK, 1.5).next_to(actor_b, UP * -1, buff=0.25)
        expectation = self.badge("EXPECTATION LOOP", AUTHORITY, 2.5).shift(UP * 2.2)
        scene16 = VGroup(actor_a, actor_b, observe_ab, observe_ba, clock_a, clock_b, expectation)
        self.play_beat(16, FadeOut(scene15), FadeIn(actor_a), TransformFromCopy(actor_a, actor_b), GrowArrow(observe_ab), GrowArrow(observe_ba), FadeIn(clock_a), FadeIn(clock_b), FadeIn(expectation), settle=0.7)

        # 17 — common-mode roots
        roots_grid = self.grid(["MODEL", "DATA", "SUPPLIER", "DOCTRINE"], [RESIDUAL] * 4, 4, 1.65).shift(UP * -2.2)
        shared_edges = VGroup(*[
            Line(root.get_top(), actor_a.get_bottom(), color=RESIDUAL, stroke_width=2) for root in roots_grid
        ], *[
            Line(root.get_top(), actor_b.get_bottom(), color=RESIDUAL, stroke_width=2) for root in roots_grid
        ])
        common = self.badge("COMMON MODE", RESIDUAL, 2.1).shift(UP * 2.25)
        scene17 = VGroup(actor_a, actor_b, roots_grid, shared_edges, common)
        self.play_beat(17, FadeOut(observe_ab), FadeOut(observe_ba), FadeOut(clock_a), FadeOut(clock_b), FadeOut(expectation), FadeIn(roots_grid), Create(shared_edges), FadeIn(common), Indicate(common, color=RESIDUAL), settle=0.65)

        # 18 — interaction matrix, not a scalar pass
        scenario_names = ["FALSE ALARM", "SPOOF", "ATTRIBUTION?", "COMMS LOSS", "DISAGREE", "ADAPT", "RECIPROCAL", "ESCALATE"]
        scenarios = self.grid(scenario_names, [MUTED, ROLLBACK, RESIDUAL, AUTHORITY, MUTED, COPPER, RESIDUAL, ROLLBACK], 2, 1.75).scale(0.86).shift(LEFT * 3.7)
        outcomes = self.grid(["TIME", "REVERSIBLE", "BURDEN", "RESIDUAL"], [AUTHORITY, EVIDENCE, COPPER, RESIDUAL], 1, 2.0).shift(RIGHT * 3.8)
        matrix_frame = RoundedRectangle(width=12.0, height=5.5, corner_radius=0.16, stroke_color=BOUNDARY, stroke_width=3)
        matrix_title = self.badge("INTERACTION MATRIX", AUTHORITY, 2.6).next_to(matrix_frame, UP, buff=-0.1)
        scene18 = VGroup(matrix_frame, matrix_title, scenarios, outcomes)
        self.play_beat(18, FadeOut(scene17), Create(matrix_frame), FadeIn(matrix_title), LaggedStart(*[FadeIn(s) for s in scenarios], lag_ratio=0.07), LaggedStart(*[FadeIn(o) for o in outcomes], lag_ratio=0.12), settle=0.65)

        # 19 — prospective off-ramps
        main_route = Line(LEFT * 5.3, RIGHT * 5.3, color=ACCENT, stroke_width=5)
        token = Triangle(color=ACCENT, fill_color=ACCENT, fill_opacity=0.8).scale(0.24).move_to(LEFT * 5.0)
        station_names = ["RATE LIMIT", "REVERSIBLE", "NARROW", "STAGED AUTH", "CONFIRM", "MONITOR", "SUSPEND", "DECOMMISSION"]
        stations = VGroup(*[self.badge(n, AUTHORITY, 1.55, 0.46) for n in station_names]).arrange_in_grid(rows=2, cols=4, buff=(0.28, 1.25))
        stations[0:4].shift(UP * 1.35)
        stations[4:8].shift(UP * -1.35)
        station_edges = VGroup(*[Line(station.get_center(), main_route.get_center() + RIGHT * station.get_center()[0], color=AUTHORITY, stroke_width=2) for station in stations])
        scene19 = VGroup(main_route, token, stations, station_edges)
        self.play_beat(19, FadeOut(scene18), Create(main_route), FadeIn(token), LaggedStart(*[FadeIn(s) for s in stations], lag_ratio=0.08), Create(station_edges), Transform(token, token.copy().shift(RIGHT * 6.8)), settle=0.75)

        # 20 — dual-surface assurance under secrecy
        annex = self.panel("RESTRICTED ANNEX", RESIDUAL, 4.6, 4.5).shift(LEFT * 3.7)
        annex_fields = self.grid(["TRACES", "ACCESS", "RETENTION", "INCIDENTS"], [RESIDUAL] * 4, 2, 1.5).move_to(annex)
        public = self.panel("PUBLIC CARD", AUTHORITY, 4.6, 4.5).shift(RIGHT * 3.7)
        public_fields = self.grid(["METHOD", "UNCERTAINTY", "GOVERNANCE", "CANNOT CHECK"], [AUTHORITY] * 4, 2, 1.65).move_to(public)
        digest = self.badge("DIGEST", EVIDENCE, 1.4).shift(UP * -2.7)
        links = VGroup(Line(annex.get_right(), digest.get_left(), color=EVIDENCE), Line(digest.get_right(), public.get_left(), color=EVIDENCE))
        scene20 = VGroup(annex, annex_fields, public, public_fields, digest, links)
        self.play_beat(20, FadeOut(scene19), FadeIn(annex), FadeIn(annex_fields), FadeIn(public), FadeIn(public_fields), FadeIn(digest), Create(links), Indicate(public_fields[-1], color=AUTHORITY), settle=0.75)

        # 21 — independent challenge access
        reviewer = self.panel("INDEPENDENT REVIEW", EVIDENCE, 3.3, 2.5)
        keys = self.grid(["MISSION", "AUTHORITY", "EVIDENCE", "INTERACTION", "POSTURE"], [EVIDENCE] * 5, 1, 1.75).scale(0.84).shift(LEFT * 4.5)
        conclusion = self.badge("CONCLUSION ONLY", ROLLBACK, 2.2).shift(RIGHT * 4.6)
        conclusion_cross = Cross(conclusion, stroke_color=ROLLBACK)
        key_edges = VGroup(*[Arrow(k.get_right(), reviewer.get_left(), color=EVIDENCE, buff=0.08) for k in keys])
        scene21 = VGroup(keys, reviewer, key_edges, conclusion, conclusion_cross)
        self.play_beat(21, FadeOut(scene20), FadeIn(keys), FadeIn(reviewer), Create(key_edges), FadeIn(conclusion), Create(conclusion_cross), settle=0.65)

        # 22 — incident suspension and decommission
        incident = self.panel("INCIDENT RECEIPT", ROLLBACK, 3.3, 4.7).shift(LEFT * 4.6)
        incident_fields = self.grid(["MODEL", "MISSION", "OPERATOR", "LINEAGE", "AUTHORITY", "EFFECT", "RESPONSE"], [ROLLBACK] * 7, 2, 1.35).scale(0.82).move_to(incident)
        lifecycle = self.grid(["SUSPEND", "EFFECT OFF", "REVOKE", "ARCHIVE", "REMOVE DEP", "RESIDUAL OWNER"], [AUTHORITY, EVIDENCE, AUTHORITY, MUTED, AUTHORITY, RESIDUAL], 1, 1.95).scale(0.92).shift(RIGHT * 1.6)
        lifecycle_edges = VGroup(*[Arrow(lifecycle[i].get_bottom(), lifecycle[i + 1].get_top(), color=BOUNDARY, buff=0.05) for i in range(len(lifecycle) - 1)])
        effect_line = Line(RIGHT * 3.7 + UP * 2.0, RIGHT * 5.3 + UP * 2.0, color=ROLLBACK, stroke_width=6)
        effect_off = Cross(effect_line, stroke_color=ROLLBACK)
        scene22 = VGroup(incident, incident_fields, lifecycle, lifecycle_edges, effect_line, effect_off)
        self.play_beat(22, FadeOut(scene21), FadeIn(incident), FadeIn(incident_fields), FadeIn(lifecycle), Create(lifecycle_edges), Create(effect_line), Create(effect_off), Indicate(lifecycle[1], color=EVIDENCE), settle=0.75)

        # 23 — joined command-interaction failures
        center_trace = self.panel("COMMAND + INTERACTION", AUTHORITY, 3.5, 2.2)
        failures = VGroup(
            self.badge("AUTOMATION BIAS", ROLLBACK, 2.2).shift(LEFT * 4.5 + UP * 1.7),
            self.badge("TIME COMPRESSION", ROLLBACK, 2.3).shift(RIGHT * 4.5 + UP * 1.7),
            self.badge("CORRELATED SENSORS", ROLLBACK, 2.5).shift(LEFT * 4.5 + UP * -1.7),
            self.badge("TACTICAL EXTERNALITY", ROLLBACK, 2.6).shift(RIGHT * 4.5 + UP * -1.7),
        )
        failure_edges = VGroup(*[Arrow(f.get_center(), center_trace.get_center(), color=ROLLBACK, buff=0.4) for f in failures])
        open_residual = self.badge("OPEN RESIDUAL", RESIDUAL, 2.0).shift(UP * -2.8)
        scene23 = VGroup(center_trace, failures, failure_edges, open_residual)
        self.play_beat(23, FadeOut(scene22), FadeIn(center_trace), LaggedStart(*[FadeIn(f) for f in failures], lag_ratio=0.12), Create(failure_edges), FadeIn(open_residual), settle=0.75)

        # 24 — exact supported artifacts
        support_frame = RoundedRectangle(width=8.3, height=4.2, corner_radius=0.16, stroke_color=AUTHORITY, stroke_width=4).shift(LEFT * 2.0)
        support_tag = self.badge("ARGUMENT", AUTHORITY, 1.7).next_to(support_frame, UP, buff=-0.1)
        support = self.grid(["RATIONALE", "ROLE TAXONOMY", "SAFE ARCHITECTURE"], [AUTHORITY] * 3, 1, 2.5).move_to(support_frame)
        scene24 = VGroup(support_frame, support_tag, support)
        self.play_beat(24, FadeOut(scene23), Create(support_frame), FadeIn(support_tag), LaggedStart(*[FadeIn(s) for s in support], lag_ratio=0.14), settle=0.4)

        # 25 — prohibited inference set
        evidence_bar = Line(UP * 2.9, UP * -2.9, color=ROLLBACK, stroke_width=6).shift(RIGHT * 2.0)
        blocked = self.grid(["NO DEPLOYED TEST", "NO AUTHORITY", "NO LAWFULNESS", "NO STABILITY"], [MUTED] * 4, 1, 2.35).shift(RIGHT * 4.5)
        blocked_stops = VGroup(*[Cross(b, stroke_color=ROLLBACK) for b in blocked])
        scene25 = VGroup(support_frame, support_tag, support, evidence_bar, blocked, blocked_stops)
        self.play_beat(25, Create(evidence_bar), FadeIn(blocked), Create(blocked_stops), settle=0.45)

        # 26 — bounded maximum-inference packet
        packet = self.panel("MAX INFERENCE", AUTHORITY, 10.5, 5.2)
        packet_fields = self.grid(["MISSION", "AUTHORITY", "PROVENANCE", "JUDGMENT", "POSTURE", "INTERACTION", "OFF-RAMP", "SECRECY", "DECOMMISSION"], [AUTHORITY] * 9, 3, 1.75).move_to(packet)
        truth = self.badge("TRUTH UNPROVED", ROLLBACK, 2.2).shift(RIGHT * 5.3 + UP * 1.0)
        effective = self.badge("EFFECT UNPROVED", ROLLBACK, 2.3).shift(RIGHT * 5.3 + UP * -1.0)
        stops = VGroup(Cross(truth, stroke_color=ROLLBACK), Cross(effective, stroke_color=ROLLBACK))
        scene26 = VGroup(packet, packet_fields, truth, effective, stops)
        self.play_beat(26, FadeOut(scene25), FadeIn(packet), LaggedStart(*[FadeIn(f) for f in packet_fields], lag_ratio=0.07), FadeIn(truth), FadeIn(effective), Create(stops), settle=0.8)

        # 27 — local performance remains subordinate
        inner = Circle(radius=0.85, stroke_color=ACCENT, stroke_width=4, fill_color=SURFACE, fill_opacity=1)
        inner_label = self.label("LOCAL\nPERFORMANCE", 13, ACCENT, "BOLD").move_to(inner)
        ring_names = ["ACCOUNTABLE COMMAND", "INTERACTION", "DECISION TIME", "BOUNDED EFFECT", "REVERSIBLE AUTHORITY"]
        rings = VGroup(*[Circle(radius=1.35 + i * 0.55, stroke_color=[AUTHORITY, COPPER, EVIDENCE, RESIDUAL, AUTHORITY][i], stroke_width=3) for i in range(5)])
        ring_labels = VGroup(*[self.badge(name, [AUTHORITY, COPPER, EVIDENCE, RESIDUAL, AUTHORITY][i], 2.35, 0.42).scale(0.75).shift(RIGHT * (4.1 + 0.2 * (i % 2)) + UP * (2.0 - i)) for i, name in enumerate(ring_names)])
        subordinate = self.badge("SUBORDINATE", AUTHORITY, 2.0).shift(LEFT * 4.5)
        scene27 = VGroup(inner, inner_label, rings, ring_labels, subordinate)
        self.play_beat(27, FadeOut(scene26), FadeIn(inner), FadeIn(inner_label), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.14), FadeIn(ring_labels), FadeIn(subordinate), settle=0.8)

        # 28 — evidence-state handoff with no authority promotion
        bounded = self.panel("BOUNDED PACKET", AUTHORITY, 3.7, 2.6).shift(LEFT * 4.2)
        no_auth = self.badge("NO AUTHORITY GRANTED", ROLLBACK, 2.7).next_to(bounded, UP * -1, buff=0.35)
        handoff = Line(UP * 2.9, UP * -2.9, color=AUTHORITY, stroke_width=5)
        next_panel = self.panel("NEXT · EVIDENCE STATES", COPPER, 4.5, 3.5).shift(RIGHT * 4.0)
        next_fields = self.grid(["ASSERTION", "TEST", "LIMIT", "REVISION"], [COPPER] * 4, 2, 1.55).move_to(next_panel)
        footer = self.label("ARGUMENT SUPPORT · SYNTHETIC ARCHITECTURE · NO WEAPON AUTHORITY", 13, AUTHORITY, "BOLD").shift(UP * -3.55)
        self.play_beat(28, FadeOut(scene27), FadeIn(bounded), FadeIn(no_auth), Create(handoff), FadeIn(next_panel), FadeIn(next_fields), FadeIn(footer), settle=0.9)

        self.wait_until(self.TARGET_DURATION)
