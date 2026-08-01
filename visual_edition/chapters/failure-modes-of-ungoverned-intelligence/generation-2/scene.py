"""Generation-2 visual abstract for Failure Modes of Ungoverned Intelligence.

One apparently successful deployment is rewound into a seven-layer causal
failure trace, then converted into an owned failure receipt and guarded
recovery lifecycle. Green local checks never erase the magenta residual.
"""

from __future__ import annotations

from manim import (
    ArcBetweenPoints, Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn,
    FadeOut, GrowArrow, Indicate, LaggedStart, LEFT, Line, MoveAlongPath,
    Rectangle, ReplacementTransform, RIGHT, RoundedRectangle, Succession,
    Text, Transform, TransformFromCopy, UP, VGroup,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class FailureModesUngovernedGeneration2(AsiScene):
    TARGET_DURATION = 281.315
    ENDS = [
        9.305, 18.860, 28.765, 39.595, 51.200, 63.405,
        75.285, 86.190, 98.020, 109.325, 120.730, 130.235,
        142.815, 154.070, 164.150, 177.655, 190.110, 203.490,
        213.845, 226.150, 239.855, 254.635, 268.415, 281.315,
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
                LaggedStart(*animations, lag_ratio=0.18),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 20, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.65, height: float = 0.58) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1,
            stroke_color=color, stroke_width=2.3,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float = 3.2, height: float = 2.0) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=color, stroke_width=2.6,
            fill_color="#172A33", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.35, 2.4), 0.46).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def deploy_token(self) -> VGroup:
        box = RoundedRectangle(
            width=2.0, height=0.9, corner_radius=0.12,
            stroke_color=ACCENT, stroke_width=3,
            fill_color="#15323D", fill_opacity=1,
        )
        labels = VGroup(
            self.label("DEPLOY 482", 18, ACCENT, "BOLD"),
            self.label("service patch", 12, MUTED),
        ).arrange(UP * -1, buff=0.04).move_to(box)
        return VGroup(box, labels)

    def dashboard(self, healthy: bool = False) -> VGroup:
        color = EVIDENCE if healthy else ROLLBACK
        shell = RoundedRectangle(
            width=5.7, height=3.0, corner_radius=0.16,
            stroke_color=color, stroke_width=3,
            fill_color="#142A33", fill_opacity=1,
        )
        title = self.label("SERVICE HEALTH", 18, color, "BOLD").next_to(shell, UP, buff=-0.42)
        axis = VGroup(
            Line(LEFT * 2.25, RIGHT * 2.25, color=BOUNDARY, stroke_width=2),
            Line(UP * 0.78, UP * -0.78, color=BOUNDARY, stroke_width=2).shift(LEFT * 2.25),
        ).shift(UP * -0.15)
        points = [(-2.1, -0.25), (-1.35, 0.15), (-0.55, -0.45), (0.25, 0.0), (1.0, -0.3), (2.0, 0.25)]
        graph = VGroup(*[
            Line([points[i][0], points[i][1] - 0.15, 0], [points[i + 1][0], points[i + 1][1] - 0.15, 0], color=color, stroke_width=4)
            for i in range(len(points) - 1)
        ])
        verdict = self.badge("SUCCESS" if healthy else "ALERT", color, 1.55, 0.52).shift(UP * -1.05)
        return VGroup(shell, title, axis, graph, verdict)

    def receipt(self, title: str = "FAILURE RECEIPT") -> VGroup:
        shell = RoundedRectangle(
            width=5.5, height=3.2, corner_radius=0.15,
            stroke_color=AUTHORITY, stroke_width=3,
            fill_color="#192A30", fill_opacity=1,
        )
        heading = self.label(title, 20, AUTHORITY, "BOLD").next_to(shell, UP, buff=-0.42)
        return VGroup(shell, heading)

    def field_grid(self, values: list[str], colors: list[str] | None = None, columns: int = 4) -> VGroup:
        colors = colors or [AUTHORITY] * len(values)
        cells = VGroup(*[
            self.badge(value, colors[i], 1.45, 0.52)
            for i, value in enumerate(values)
        ])
        cells.arrange_in_grid(rows=(len(values) + columns - 1) // columns, cols=columns, buff=(0.16, 0.22))
        return cells

    def layer_node(self, name: str, color: str = ACCENT) -> VGroup:
        node = Circle(radius=0.43, stroke_color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        return VGroup(node, self.label(name, 10, color, "BOLD").move_to(node))

    def construct(self) -> None:
        # 1 — apparent success
        alert = self.dashboard(False)
        token = self.deploy_token().shift(LEFT * 5.0 + UP * -2.35)
        timer = self.badge("00:11", AUTHORITY, 1.2).shift(UP * 2.85)
        route = Arrow(token.get_right(), alert.get_left(), color=ACCENT, stroke_width=4, buff=0.16)
        success = self.dashboard(True)
        self.play_beat(1, Succession(FadeIn(alert), Transform(alert, success)), FadeIn(token), GrowArrow(route), FadeIn(timer), settle=0.65)

        # 2 — the lid opens
        errors = VGroup(*[
            self.badge(f"ERROR {i}", ROLLBACK, 1.25, 0.45)
            for i in (17, 18, 19)
        ]).arrange(RIGHT, buff=0.22).shift(UP * -0.9)
        threshold = DashedLine(LEFT * 2.25, RIGHT * 2.25, color=AUTHORITY, stroke_width=4).shift(UP * 0.75)
        moved = self.badge("THRESHOLD MOVED", ROLLBACK, 2.15).shift(UP * 1.4)
        self.play_beat(2, FadeOut(token), FadeOut(route), FadeOut(timer), alert.animate.shift(UP * 1.25).scale(0.7), FadeIn(errors), Create(threshold), FadeIn(moved), settle=0.55)

        # 3 — broad label lacks operations
        broad = self.badge("ALIGNMENT FAILURE", ROLLBACK, 2.8, 0.72).shift(LEFT * 3.8)
        questions = self.field_grid(["WHICH BOUNDARY?", "WHAT EVENT?", "WHO OWNS?", "WHAT SURVIVES?"], [MUTED] * 4, 2).shift(RIGHT * 2.1)
        self.play_beat(3, FadeOut(alert), FadeOut(errors), FadeOut(threshold), FadeOut(moved), FadeIn(broad), LaggedStart(*[FadeIn(q) for q in questions], lag_ratio=0.18), settle=0.45)

        # 4 — boundary-event receipt
        failure_receipt = self.receipt()
        minimum = self.field_grid(["TRIGGER", "INVARIANT", "OBSERVER", "RECEIPT", "OWNER", "CONTAIN", "RESIDUAL", "LEARN"], columns=4).shift(UP * -0.15)
        residual = self.badge("RESIDUAL · OPEN", RESIDUAL, 2.1).shift(UP * -2.45)
        self.play_beat(4, FadeOut(broad), FadeOut(questions), FadeIn(failure_receipt), LaggedStart(*[FadeIn(c) for c in minimum], lag_ratio=0.12), FadeIn(residual), settle=0.55)

        # 5 — rewind to goal fork
        goal = self.badge("RESTORE SERVICE", EVIDENCE, 2.25).shift(RIGHT * 3.5 + UP * 1.2)
        proxy = self.badge("MAKE GREEN", ROLLBACK, 1.9).shift(RIGHT * 3.5 + UP * -1.15)
        fork_token = self.deploy_token().shift(LEFT * 4.4)
        upper = ArcBetweenPoints(fork_token.get_right(), goal.get_left(), angle=0.35, color=EVIDENCE)
        lower = ArcBetweenPoints(fork_token.get_right(), proxy.get_left(), angle=-0.35, color=ROLLBACK)
        self.play_beat(5, FadeOut(failure_receipt), FadeOut(minimum), FadeOut(residual), FadeIn(fork_token), FadeIn(goal), FadeIn(proxy), Create(upper), Create(lower), Indicate(proxy, color=ROLLBACK), settle=0.45)

        # 6 — context admission mixed result
        context_panel = self.panel("CONTEXT", ACCENT, 6.4, 3.7)
        runbook = self.badge("RUNBOOK v3 · MIGRATION ENDED", ACCENT, 3.6, 0.65).shift(UP * 0.65)
        context_checks = self.field_grid(["SOURCE ✓", "FRESH ✓", "ADEQUATE ✕"], [EVIDENCE, EVIDENCE, ROLLBACK], 3).shift(UP * -0.65)
        self.play_beat(6, FadeOut(fork_token), FadeOut(goal), FadeOut(proxy), FadeOut(upper), FadeOut(lower), FadeIn(context_panel), FadeIn(runbook), LaggedStart(*[FadeIn(c) for c in context_checks], lag_ratio=0.2), settle=0.45)

        # 7 — credential unfolds option expansion
        restart = self.badge("RESTART", EVIDENCE, 1.5).shift(LEFT * 2.2)
        edit = self.badge("EDIT MONITORING", ROLLBACK, 2.15).shift(RIGHT * 2.25)
        credential = self.badge("TEMP CREDENTIAL", AUTHORITY, 2.25, 0.7)
        need_arrow = Arrow(credential.get_left(), restart.get_right(), color=EVIDENCE, buff=0.15)
        extra_arrow = Arrow(credential.get_right(), edit.get_left(), color=ROLLBACK, buff=0.15)
        option = self.badge("OPTION EXPANSION", ROLLBACK, 2.25).shift(UP * -1.55)
        self.play_beat(7, FadeOut(context_panel), FadeOut(runbook), FadeOut(context_checks), FadeIn(credential), FadeIn(restart), GrowArrow(need_arrow), FadeIn(edit), GrowArrow(extra_arrow), FadeIn(option), settle=0.5)

        # 8 — evaluator capture loop
        subject = self.panel("SUBJECT", ACCENT, 3.0, 2.1).shift(LEFT * 3.6)
        evaluator = self.panel("EVALUATOR", AUTHORITY, 3.0, 2.1).shift(RIGHT * 3.6)
        judge = Arrow(subject.get_right(), evaluator.get_left(), color=BOUNDARY, buff=0.12)
        capture_path = ArcBetweenPoints(subject.get_top(), evaluator.get_top(), angle=-0.65, color=ROLLBACK)
        captured = self.badge("CAPTURED", ROLLBACK, 1.65).shift(UP * 2.15)
        self.play_beat(8, FadeOut(credential), FadeOut(restart), FadeOut(edit), FadeOut(need_arrow), FadeOut(extra_arrow), FadeOut(option), FadeIn(subject), FadeIn(evaluator), GrowArrow(judge), Create(capture_path), FadeIn(captured), Indicate(evaluator, color=ROLLBACK), settle=0.55)

        # 9 — authentic without purpose authority
        key = self.badge("AUTHENTIC ✓", EVIDENCE, 1.8).shift(LEFT * 4.5)
        identity_gate = Line(UP * 1.55, UP * -1.55, color=EVIDENCE, stroke_width=5).shift(LEFT * 1.8)
        purpose_gate = DashedLine(UP * 1.55, UP * -1.55, color=ROLLBACK, stroke_width=4).shift(RIGHT * 1.2)
        effect = self.badge("CONFIG CHANGED", ROLLBACK, 2.15).shift(RIGHT * 4.2)
        purpose_missing = self.badge("PURPOSE · MISSING", ROLLBACK, 2.2).shift(UP * -2.0)
        crossing = Arrow(key.get_right(), effect.get_left(), color=ACCENT, stroke_width=4, buff=0.12)
        self.play_beat(9, FadeOut(subject), FadeOut(evaluator), FadeOut(judge), FadeOut(capture_path), FadeOut(captured), FadeIn(key), Create(identity_gate), Create(purpose_gate), FadeIn(effect), GrowArrow(crossing), FadeIn(purpose_missing), settle=0.45)

        # 10 — residual leaves denominator
        score_frame = self.panel("SUCCESS DENOMINATOR", EVIDENCE, 6.0, 3.2)
        green_score = self.badge("PASS · 100%", EVIDENCE, 2.0, 0.72).shift(UP * 0.45)
        open_residual = VGroup(
            RoundedRectangle(width=3.0, height=1.25, corner_radius=0.12, stroke_color=RESIDUAL, fill_color=SURFACE, fill_opacity=1),
            self.label("ERRORS EXCLUDED\nRESIDUAL OPEN", 15, RESIDUAL, "BOLD"),
        ).shift(RIGHT * 4.6 + UP * -1.5)
        self.play_beat(10, FadeOut(key), FadeOut(identity_gate), FadeOut(purpose_gate), FadeOut(effect), FadeOut(crossing), FadeOut(purpose_missing), FadeIn(score_frame), FadeIn(green_score), FadeIn(open_residual), Indicate(open_residual, color=RESIDUAL), settle=0.55)

        # 11 — failed route promoted
        chain_names = ["GOAL", "CONTEXT", "AUTH", "EVAL", "TOOL", "METRIC"]
        chain = VGroup(*[self.layer_node(n, EVIDENCE) for n in chain_names]).arrange(RIGHT, buff=0.48).shift(LEFT * 1.1)
        chain_edges = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), color=ROLLBACK, buff=0.08, stroke_width=3) for i in range(len(chain) - 1)])
        procedure = self.panel("PROCEDURE 17", ROLLBACK, 2.4, 2.0).shift(RIGHT * 4.8)
        promoted = self.badge("PROMOTED", EVIDENCE, 1.55).move_to(procedure)
        self.play_beat(11, FadeOut(score_frame), FadeOut(green_score), FadeOut(open_residual), LaggedStart(*[FadeIn(n) for n in chain], lag_ratio=0.1), Create(chain_edges), FadeIn(procedure), TransformFromCopy(chain, promoted), settle=0.45)

        # 12 — local passes, joined failure
        local_checks = VGroup(*[self.badge("LOCAL ✓", EVIDENCE, 1.15, 0.42).next_to(node, UP, buff=0.12) for node in chain])
        joined_line = Line(chain.get_left() + UP * -1.0, chain.get_right() + UP * -1.0, color=ROLLBACK, stroke_width=5)
        joined = self.badge("JOINED FAILURE", ROLLBACK, 2.15).next_to(joined_line, UP * -1, buff=0.18)
        self.play_beat(12, FadeOut(procedure), FadeOut(promoted), LaggedStart(*[FadeIn(c) for c in local_checks], lag_ratio=0.1), Create(joined_line), FadeIn(joined), settle=0.6)

        # 13 — map row
        map_receipt = self.receipt("FAILURE BOUNDARY MAP")
        map_fields = self.field_grid(["CONTRACTS", "INVARIANT", "SEVERITY", "REVERSIBLE?", "ESCAPE", "RECUR 1", "DETECTOR v2", "CONTAIN v4"], columns=4).shift(UP * -0.2)
        map_residual = self.badge("RESIDUAL · OWNED", RESIDUAL, 2.2).shift(UP * -2.4)
        self.play_beat(13, FadeOut(chain), FadeOut(chain_edges), FadeOut(local_checks), FadeOut(joined_line), FadeOut(joined), FadeIn(map_receipt), LaggedStart(*[FadeIn(c) for c in map_fields], lag_ratio=0.1), FadeIn(map_residual), settle=0.45)

        # 14 — explicit unmapped state
        classes = VGroup(*[self.badge(f"KNOWN {x}", MUTED, 1.4) for x in "ABC"]).arrange(RIGHT, buff=0.3).shift(LEFT * 2.5)
        unknown = self.badge("UNMAPPED", AUTHORITY, 1.75, 0.72).shift(RIGHT * 3.8)
        event_dot = Dot(color=RESIDUAL, radius=0.16).shift(LEFT * 4.8)
        route_unknown = ArcBetweenPoints(event_dot.get_center(), unknown.get_left(), angle=-0.25, color=AUTHORITY)
        self.play_beat(14, FadeOut(map_receipt), FadeOut(map_fields), FadeOut(map_residual), FadeIn(event_dot), FadeIn(classes), Indicate(classes[1], color=ROLLBACK), Create(route_unknown), FadeIn(unknown), settle=0.55)

        # 15 — custody handshake
        owner_a = self.panel("CURRENT OWNER", MUTED, 2.6, 2.0).shift(LEFT * 4.3)
        owner_b = self.panel("RECEIVING OWNER", AUTHORITY, 2.8, 2.0).shift(RIGHT * 4.2)
        custody_fields = self.field_grid(["RECEIPT ✓", "DUTY ✓", "RESIDUAL ✓"], [EVIDENCE] * 3, 3)
        transfer = Arrow(owner_a.get_right(), owner_b.get_left(), color=AUTHORITY, stroke_width=4, buff=0.15)
        self.play_beat(15, FadeOut(event_dot), FadeOut(classes), FadeOut(route_unknown), FadeOut(unknown), FadeIn(owner_a), FadeIn(owner_b), LaggedStart(*[FadeIn(c) for c in custody_fields], lag_ratio=0.2), GrowArrow(transfer), settle=0.45)

        # 16 — accept/reject noninterference
        fork = self.badge("DETECTION", ACCENT, 1.65)
        isolate = self.badge("ACCEPT → ISOLATE", ROLLBACK, 2.3).shift(LEFT * 3.8 + UP * 1.25)
        same = self.badge("REJECT → SAME STATE", MUTED, 2.5).shift(LEFT * 3.8 + UP * -1.25)
        locks = VGroup(self.badge("NO SUPPORT", AUTHORITY, 1.7), self.badge("NO AUTHORITY", AUTHORITY, 1.9)).arrange(UP * -1, buff=0.35).shift(RIGHT * 4.0)
        effect_off = self.badge("EFFECT OFF", ROLLBACK, 1.7).next_to(isolate, RIGHT, buff=0.28)
        self.play_beat(16, FadeOut(owner_a), FadeOut(owner_b), FadeOut(custody_fields), FadeOut(transfer), FadeIn(fork), FadeIn(isolate), FadeIn(same), FadeIn(effect_off), LaggedStart(*[FadeIn(x) for x in locks], lag_ratio=0.2), settle=0.55)

        # 17 — five recovery stations
        station_names = ["ISOLATE", "CONTAIN", "REMEDIATE", "REVIEW", "READMIT?"]
        stations = VGroup(*[self.badge(n, ROLLBACK if i == 0 else MUTED, 1.65, 0.55) for i, n in enumerate(station_names)]).arrange(RIGHT, buff=0.28)
        rail = Line(stations.get_left() + UP * -0.7, stations.get_right() + UP * -0.7, color=BOUNDARY, stroke_width=3)
        incident = Dot(color=ROLLBACK, radius=0.15).next_to(stations[0], UP * -1, buff=0.52)
        lifecycle_residual = self.badge("RESIDUAL", RESIDUAL, 1.35, 0.45).next_to(incident, UP * -1, buff=0.24)
        self.play_beat(17, FadeOut(fork), FadeOut(isolate), FadeOut(same), FadeOut(effect_off), FadeOut(locks), LaggedStart(*[FadeIn(s) for s in stations], lag_ratio=0.15), Create(rail), FadeIn(incident), FadeIn(lifecycle_residual), settle=0.5)

        # 18 — replacement cannot inherit approval
        model_a = self.badge("MODEL A", MUTED, 1.55).shift(LEFT * 4.8 + UP * 1.2)
        model_b = self.badge("MODEL B ↑", ACCENT, 1.65).move_to(model_a)
        gate_keys = self.field_grid(["INCIDENT", "VERSION", "ASSURANCE", "TAXONOMY", "RESIDUAL", "AUTHORITY"], [AUTHORITY] * 6, 3).scale(0.88)
        readmit = self.badge("READMIT", AUTHORITY, 1.55).shift(RIGHT * 4.5)
        old = self.badge("OLD APPROVAL", ROLLBACK, 1.8).shift(LEFT * 3.9 + UP * -1.45)
        old_cross = Cross(old, stroke_color=ROLLBACK, stroke_width=4)
        self.play_beat(18, FadeOut(stations), FadeOut(rail), FadeOut(incident), FadeOut(lifecycle_residual), Succession(FadeIn(model_a), Transform(model_a, model_b)), FadeIn(gate_keys), FadeIn(readmit), FadeIn(old), Create(old_cross), settle=0.55)

        # 19 — recurrence snaps back
        recurrence_stations = VGroup(*[self.badge(n, MUTED, 1.65, 0.55) for n in station_names]).arrange(RIGHT, buff=0.28)
        recur_arc = ArcBetweenPoints(recurrence_stations[-1].get_bottom(), recurrence_stations[0].get_bottom(), angle=-0.65, color=ROLLBACK)
        recur = self.badge("RECURRENCE 2", ROLLBACK, 1.9).shift(UP * -1.65)
        not_normal = self.badge("NOT NORMAL", AUTHORITY, 1.65).shift(UP * 1.65)
        self.play_beat(19, FadeOut(model_a), FadeOut(gate_keys), FadeOut(readmit), FadeOut(old), FadeOut(old_cross), FadeIn(recurrence_stations), Create(recur_arc), FadeIn(recur), FadeIn(not_normal), Indicate(recurrence_stations[0], color=ROLLBACK), settle=0.55)

        # 20 — detector outcomes
        inputs = VGroup(*[self.badge(n, ACCENT, 1.5, 0.48) for n in ["SEEDED", "BENIGN", "OUT-OF-SCOPE", "NOVEL"]]).arrange(UP * -1, buff=0.24).shift(LEFT * 4.5)
        detector = self.panel("DETECTOR", AUTHORITY, 2.5, 2.4)
        outputs = VGroup(*[
            self.badge(n, c, 1.45, 0.48)
            for n, c in [("HIT", EVIDENCE), ("QUIET", EVIDENCE), ("ABSTAIN", AUTHORITY), ("MISSED", ROLLBACK)]
        ]).arrange(UP * -1, buff=0.24).shift(RIGHT * 4.5)
        self.play_beat(20, FadeOut(recurrence_stations), FadeOut(recur_arc), FadeOut(recur), FadeOut(not_normal), LaggedStart(*[FadeIn(x) for x in inputs], lag_ratio=0.1), FadeIn(detector), LaggedStart(*[FadeIn(x) for x in outputs], lag_ratio=0.1), Indicate(outputs[-1], color=ROLLBACK), settle=0.45)

        # 21 — richer map versus baseline and joint cost
        baseline = self.panel("SIMPLE INCIDENT", MUTED, 3.0, 1.5).shift(LEFT * 3.8 + UP * 1.45)
        rich = self.panel("FAILURE MAP", AUTHORITY, 3.0, 1.5).shift(RIGHT * 3.8 + UP * 1.45)
        metrics = self.field_grid(["MISSED", "FALSE ALARM", "ABSTAIN", "ESCAPE", "CONTAIN TIME", "RECURRENCE", "THROUGHPUT", "BURDEN", "COST"], [MUTED] * 9, 3).scale(0.9).shift(UP * -1.05)
        balance = Line(LEFT * 1.0, RIGHT * 1.0, color=AUTHORITY, stroke_width=4).shift(UP * 0.6)
        self.play_beat(21, FadeOut(inputs), FadeOut(detector), FadeOut(outputs), FadeIn(baseline), FadeIn(rich), Create(balance), LaggedStart(*[FadeIn(m) for m in metrics], lag_ratio=0.08), settle=0.5)

        # 22 — exact local evidence counts
        evidence_frame = self.panel("LOCAL EVIDENCE ENVELOPE", AUTHORITY, 9.8, 4.8)
        evidence_counts = self.field_grid(["DESIGN\nRATIONALE", "MAP\nSCHEMA", "2 VALID\n7 REJECTED", "5 STAGES\n31 MUTATIONS"], [AUTHORITY, AUTHORITY, EVIDENCE, EVIDENCE], 4).scale(1.18)
        support = self.badge("ARGUMENT SUPPORT", AUTHORITY, 2.2).shift(UP * -2.25)
        self.play_beat(22, FadeOut(baseline), FadeOut(rich), FadeOut(balance), FadeOut(metrics), FadeIn(evidence_frame), LaggedStart(*[FadeIn(c) for c in evidence_counts], lag_ratio=0.16), FadeIn(support), settle=0.6)

        # 23 — hard evidence boundary
        finite = self.field_grid(["RECORD", "ROUTE", "STATE", "NONINTERFERENCE", "GUARDED RECOVERY"], [EVIDENCE] * 5, 2).scale(0.88).shift(LEFT * 3.5)
        claims = self.field_grid(["EVENT TRUTH?", "DETECTOR QUALITY?", "EFFECTIVE?", "DEPLOYED?", "SAFE?"], [MUTED] * 5, 2).scale(0.88).shift(RIGHT * 3.5)
        boundary = Line(UP * 3.0, UP * -3.0, color=ROLLBACK, stroke_width=5)
        boundary_tag = self.badge("EVIDENCE CEILING", ROLLBACK, 2.0).next_to(boundary, UP, buff=-0.2)
        self.play_beat(23, FadeOut(evidence_frame), FadeOut(evidence_counts), FadeOut(support), FadeIn(finite), Create(boundary), FadeIn(boundary_tag), FadeIn(claims), Indicate(boundary, color=ROLLBACK), settle=0.65)

        # 24 — custody and handoff
        final_receipt = self.receipt("INCIDENT · OWNED").scale(0.72).shift(LEFT * 3.8)
        final_fields = self.field_grid(["OWNER", "RECEIPT", "RESIDUAL OPEN"], [AUTHORITY, EVIDENCE, RESIDUAL], 1).scale(0.75).move_to(final_receipt)
        handoff_axis = Line(UP * 2.7, UP * -2.7, color=AUTHORITY, stroke_width=4).shift(RIGHT * 0.25)
        next_panel = self.panel("NEXT", COPPER, 4.7, 3.1).shift(RIGHT * 4.0)
        next_title = VGroup(
            self.label("DANGEROUS CAPABILITY", 18, COPPER, "BOLD"),
            self.label("DOMAINS + MISUSE UPLIFT", 18, COPPER, "BOLD"),
            self.label("who can materially cause harm?", 14, MUTED),
        ).arrange(UP * -1, buff=0.14).move_to(next_panel)
        footer = self.label("DESIGN RATIONALE · ARGUMENT SUPPORT · NO SAFETY CLAIM", 14, AUTHORITY, "BOLD").shift(UP * -3.55)
        self.play_beat(24, FadeOut(finite), FadeOut(boundary), FadeOut(boundary_tag), FadeOut(claims), FadeIn(final_receipt), FadeIn(final_fields), Create(handoff_axis), FadeIn(next_panel), FadeIn(next_title), FadeIn(footer), settle=0.9)

        self.wait_until(self.TARGET_DURATION)
