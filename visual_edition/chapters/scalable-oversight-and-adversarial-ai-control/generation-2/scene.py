"""Generation-2 visual abstract for Scalable Oversight and Adversarial AI Control.

A selectively reported model-replacement candidate provides the continuous
worked trace. The animation separates discovery, verification, record custody,
and authority while preserving access, correlation, baseline, abstention,
consumer, cost, and evidence-ceiling boundaries.
"""

from __future__ import annotations

from manim import (
    Arrow, Circle, Create, Cross, DashedLine, Dot, FadeIn, FadeOut,
    GrowArrow, GrowFromCenter, Indicate, LaggedStart, LEFT, Line,
    MoveAlongPath, Rectangle, ReplacementTransform, RIGHT, RoundedRectangle,
    Succession, Text, TransformFromCopy, UP, VGroup,
)

from visual_edition.lib.asi_visuals import (
    ACCENT, AUTHORITY, BOUNDARY, COPPER, EVIDENCE, INK, MUTED, RESIDUAL,
    ROLLBACK, SURFACE, AsiScene, text,
)


class ScalableOversightGeneration2(AsiScene):
    TARGET_DURATION = 334.08
    ENDS = [
        13.730, 26.285, 35.965, 50.970, 58.525, 69.130, 80.060,
        92.290, 105.945, 116.900, 126.905, 139.585, 152.115,
        165.495, 177.900, 188.430, 199.683, 205.260, 215.040,
        227.895, 241.450, 255.355,
        267.685, 281.915, 298.070, 313.000, 325.005, 334.080,
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
                LaggedStart(*animations, lag_ratio=0.13),
                run_time=max(0.05, remaining - min(settle, remaining * 0.2)),
            )
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 18, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 1.9, height: float = 0.54) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.1,
            stroke_color=color, stroke_width=2.5,
            fill_color=SURFACE, fill_opacity=1,
        )
        return VGroup(shell, self.label(value, 13, color, "BOLD").move_to(shell))

    def panel(self, title: str, color: str, width: float = 4.0, height: float = 2.7) -> VGroup:
        shell = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=color, stroke_width=3,
            fill_color="#172A33", fill_opacity=1,
        )
        tag = self.badge(title, color, min(width - 0.35, 3.1), 0.48).scale(0.82)
        tag.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, tag)

    def grid(self, values: list[str], colors: list[str], columns: int, width: float = 1.65) -> VGroup:
        cells = VGroup(*[self.badge(v, colors[i], width, 0.48) for i, v in enumerate(values)])
        rows = (len(values) + columns - 1) // columns
        cells.arrange_in_grid(rows=rows, cols=columns, buff=(0.18, 0.2))
        return cells

    def candidate(self, compact: bool = False) -> VGroup:
        width = 5.1 if compact else 7.0
        shell = RoundedRectangle(
            width=width, height=2.25, corner_radius=0.16,
            stroke_color=EVIDENCE, stroke_width=4,
            fill_color="#172A33", fill_opacity=1,
        )
        title = self.label("REPLACEMENT CANDIDATE", 16, EVIDENCE, "BOLD").next_to(shell, UP, buff=-0.3)
        score = self.label("AGGREGATE  +12%", 25 if not compact else 20, INK, "BOLD").move_to(shell)
        return VGroup(shell, title, score)

    def construct(self) -> None:
        # 1 — green aggregate and concealed cohort
        candidate = self.candidate()
        approve = self.badge("APPROVE?", EVIDENCE, 2.1, 0.72).shift(RIGHT * 4.7)
        denominator = Line(LEFT * 3.0, RIGHT * 3.0, color=EVIDENCE, stroke_width=10).shift(UP * -2.0)
        hidden = Dot(denominator.point_from_proportion(0.82), radius=0.13, color=ROLLBACK)
        scene1 = VGroup(candidate, approve, denominator, hidden)
        self.play_beat(1, FadeIn(candidate, shift=RIGHT * 0.5), GrowArrow(Arrow(candidate.get_right(), approve.get_left(), color=EVIDENCE)), FadeIn(approve), Create(denominator), FadeIn(hidden), settle=0.7)

        # 2 — reveal the omitted cohort and unsafe outcomes
        cohort = self.panel("OMITTED HIGH-IMPACT COHORT", ROLLBACK, 6.2, 3.3)
        unsafe = self.grid(["UNSAFE RELEASE 1", "UNSAFE RELEASE 2"], [ROLLBACK, ROLLBACK], 2, 2.45).move_to(cohort)
        aggregate_survives = self.badge("AGGREGATE STILL GREEN", EVIDENCE, 3.0).shift(UP * -2.4)
        decision_stops = self.badge("REPLACEMENT STOPS", ROLLBACK, 2.7).shift(RIGHT * 4.8 + UP * -2.4)
        scene2 = VGroup(cohort, unsafe, aggregate_survives, decision_stops)
        self.play_beat(2, FadeOut(scene1), GrowFromCenter(cohort), LaggedStart(*[FadeIn(x) for x in unsafe], lag_ratio=0.2), FadeIn(aggregate_survives), FadeIn(decision_stops), settle=0.7)

        # 3 — process, result, and authority are separate
        review = self.panel("REVIEW PROCESS", ACCENT, 3.4, 2.4).shift(LEFT * 4.3)
        result = self.panel("BOUNDED RESULT", AUTHORITY, 3.4, 2.4)
        authority = self.panel("AUTHORITY TO ACT", COPPER, 3.4, 2.4).shift(RIGHT * 4.3)
        stops = VGroup(
            DashedLine(review.get_right(), result.get_left(), color=BOUNDARY, stroke_width=4),
            DashedLine(result.get_right(), authority.get_left(), color=BOUNDARY, stroke_width=4),
        )
        no_equals = self.grid(["NOT TRUTH", "NOT PERMISSION"], [ROLLBACK, ROLLBACK], 2, 2.3).shift(UP * -2.0)
        scene3 = VGroup(review, result, authority, stops, no_equals)
        self.play_beat(3, FadeOut(scene2), FadeIn(review), Create(stops[0]), FadeIn(result), Create(stops[1]), FadeIn(authority), FadeIn(no_equals), settle=0.65)

        # 4 — three asymmetries
        asym = VGroup(
            self.panel("CAPABILITY", ACCENT, 3.5, 3.2),
            self.panel("ACCESS", AUTHORITY, 3.5, 3.2),
            self.panel("AUTHORITY", COPPER, 3.5, 3.2),
        ).arrange(RIGHT, buff=0.55)
        questions = VGroup(
            self.label("CAN DEFECT BE\nRECOGNIZED?", 17, ACCENT, "BOLD").move_to(asym[0]),
            self.label("IS DECISIVE\nEVIDENCE VISIBLE?", 17, AUTHORITY, "BOLD").move_to(asym[1]),
            self.label("WHO MAY\nDECIDE?", 17, COPPER, "BOLD").move_to(asym[2]),
        )
        scene4 = VGroup(asym, questions)
        self.play_beat(4, FadeOut(scene3), LaggedStart(*[FadeIn(x) for x in asym], lag_ratio=0.18), LaggedStart(*[FadeIn(x) for x in questions], lag_ratio=0.18), settle=0.6)

        # 5 — reject one score; expose four route semantics
        scalar = Circle(radius=1.3, stroke_color=MUTED, stroke_width=4).shift(LEFT * 4.8)
        scalar_label = self.label("REVIEW\nQUALITY", 18, MUTED, "BOLD").move_to(scalar)
        scalar_cross = Cross(VGroup(scalar, scalar_label), stroke_color=ROLLBACK)
        routes = self.grid(["PASS", "NARROW", "ESCALATE", "STOP"], [EVIDENCE, AUTHORITY, COPPER, ROLLBACK], 1, 2.4).shift(RIGHT * 2.6)
        route_arrows = VGroup(*[Arrow(scalar.get_right(), r.get_left(), color=[EVIDENCE, AUTHORITY, COPPER, ROLLBACK][i], buff=0.08) for i, r in enumerate(routes)])
        scene5 = VGroup(scalar, scalar_label, scalar_cross, routes, route_arrows)
        self.play_beat(5, FadeOut(scene4), Create(scalar), FadeIn(scalar_label), Create(scalar_cross), LaggedStart(*[GrowArrow(a) for a in route_arrows], lag_ratio=0.12), LaggedStart(*[FadeIn(r) for r in routes], lag_ratio=0.12), settle=0.65)

        # 6 — freeze the request before selecting assistance
        request = self.panel("FROZEN OVERSIGHT REQUEST", AUTHORITY, 11.2, 5.3)
        request_fields = self.grid(
            ["TASK", "RISK TIER", "CONSUMER", "EVIDENCE VIEWS", "TIME + TURNS", "SUPERVISOR LIMITS", "SYSTEM ASSUMPTIONS", "STOP CONDITION"],
            [ACCENT, ROLLBACK, COPPER, AUTHORITY, MUTED, ACCENT, BOUNDARY, ROLLBACK], 4, 2.2,
        ).move_to(request)
        frozen = self.badge("PROSPECTIVE · VERSION 1", COPPER, 2.9).shift(UP * -2.85)
        scene6 = VGroup(request, request_fields, frozen)
        self.play_beat(6, FadeOut(scene5), FadeIn(request), LaggedStart(*[FadeIn(f) for f in request_fields], lag_ratio=0.08), FadeIn(frozen), settle=0.7)

        # 7 — conditional route selection
        router = self.panel("CONTROL PLANE", AUTHORITY, 2.7, 3.4).shift(LEFT * 4.9)
        route_cards = self.grid(["DIRECT", "CONSULT", "ADVERSARIAL", "ABSTAIN"], [EVIDENCE, ACCENT, COPPER, ROLLBACK], 1, 2.3).shift(RIGHT * 3.5)
        route_paths = VGroup(*[Arrow(router.get_right(), r.get_left(), color=[EVIDENCE, ACCENT, COPPER, ROLLBACK][i], buff=0.08) for i, r in enumerate(route_cards)])
        universal = self.badge("NO UNIVERSAL WINNER", ROLLBACK, 3.0).shift(UP * -2.6)
        scene7 = VGroup(router, route_cards, route_paths, universal)
        self.play_beat(7, FadeOut(scene6), FadeIn(router), LaggedStart(*[GrowArrow(p) for p in route_paths], lag_ratio=0.13), LaggedStart(*[FadeIn(r) for r in route_cards], lag_ratio=0.13), FadeIn(universal), settle=0.65)

        # 8 — role labels do not repair access mismatch
        proposer = self.panel("PROPOSER", EVIDENCE, 4.1, 4.1).shift(LEFT * 3.8)
        proposer_view = self.grid(["SUMMARY", "PER-COHORT", "LINEAGE"], [EVIDENCE] * 3, 1, 2.0).move_to(proposer)
        critic = self.panel("CRITIC", ACCENT, 4.1, 4.1).shift(RIGHT * 3.8)
        critic_view = self.badge("SUMMARY ONLY", ROLLBACK, 2.4).move_to(critic)
        mismatch = self.badge("ACCESS MISMATCH", ROLLBACK, 2.6).shift(UP * -2.7)
        scene8 = VGroup(proposer, proposer_view, critic, critic_view, mismatch)
        self.play_beat(8, FadeOut(scene7), FadeIn(proposer), FadeIn(proposer_view), FadeIn(critic), FadeIn(critic_view), FadeIn(mismatch), settle=0.7)

        # 9 — repair the evidence view without claiming independence
        repair_items = self.grid(["FROZEN COHORT", "CANDIDATE DIGEST", "REGRESSION ARTIFACTS"], [AUTHORITY] * 3, 1, 2.7).shift(LEFT * 4.7)
        repaired_critic = self.panel("CRITIC VIEW · REPAIRED", ACCENT, 4.6, 4.0).shift(RIGHT * 3.0)
        repair_paths = VGroup(*[Arrow(item.get_right(), repaired_critic.get_left(), color=AUTHORITY, buff=0.08) for item in repair_items])
        still_open = self.badge("INDEPENDENCE · OPEN", ROLLBACK, 2.8).shift(UP * -2.6)
        scene9 = VGroup(repair_items, repaired_critic, repair_paths, still_open)
        self.play_beat(9, FadeOut(scene8), FadeIn(repair_items), FadeIn(repaired_critic), LaggedStart(*[GrowArrow(p) for p in repair_paths], lag_ratio=0.15), FadeIn(still_open), settle=0.65)

        # 10 — nominal voices collapse through shared dependencies
        proposer_node = self.badge("PROPOSER", EVIDENCE, 2.0).shift(LEFT * 4.6 + UP * 1.5)
        critic_node = self.badge("CRITIC", ACCENT, 2.0).shift(LEFT * 4.6 + UP * -1.5)
        shared = self.grid(["BASE FAMILY", "RETRIEVAL", "TOOLS"], [ROLLBACK] * 3, 1, 2.1).shift(RIGHT * 2.2)
        edges = VGroup(*[
            Line(source.get_right(), target.get_left(), color=ROLLBACK, stroke_width=3)
            for source in (proposer_node, critic_node) for target in shared
        ])
        one_system = self.badge("2 VOICES · 1 FAILURE SYSTEM", ROLLBACK, 3.4).shift(RIGHT * 4.3 + UP * -2.5)
        scene10 = VGroup(proposer_node, critic_node, shared, edges, one_system)
        self.play_beat(10, FadeOut(scene9), FadeIn(proposer_node), FadeIn(critic_node), Create(edges), LaggedStart(*[FadeIn(s) for s in shared], lag_ratio=0.12), FadeIn(one_system), settle=0.65)

        # 11 — debate is a search surface, not outcome truth
        pro = self.badge("MEETS REPLACEMENT GATE", EVIDENCE, 3.1).shift(LEFT * 4.5)
        con = self.badge("PACKET INSUFFICIENT", ROLLBACK, 3.1).shift(RIGHT * 4.5)
        transcript = self.panel("ADVERSARIAL TRANSCRIPT", COPPER, 4.2, 3.0)
        pro_path = Arrow(pro.get_right(), transcript.get_left(), color=EVIDENCE, buff=0.08)
        con_path = Arrow(con.get_left(), transcript.get_right(), color=ROLLBACK, buff=0.08)
        not_truth = self.badge("SEARCH SURFACE · NOT OUTCOME", AUTHORITY, 3.5).shift(UP * -2.4)
        scene11 = VGroup(pro, con, transcript, pro_path, con_path, not_truth)
        self.play_beat(11, FadeOut(scene10), FadeIn(pro), FadeIn(con), GrowArrow(pro_path), GrowArrow(con_path), FadeIn(transcript), FadeIn(not_truth), settle=0.65)

        # 12 — independent route replays the hidden cohort
        transcript_small = self.panel("TRANSCRIPT", COPPER, 3.0, 2.4).shift(LEFT * 4.7 + UP * 1.4)
        auditor = self.panel("INDEPENDENT AUDITOR", AUTHORITY, 3.8, 2.6).shift(LEFT * 0.2 + UP * -1.2)
        cohort_replay = self.panel("FROZEN COHORT REPLAY", ROLLBACK, 3.8, 2.6).shift(RIGHT * 4.5 + UP * 1.4)
        unsafe_pair = self.grid(["UNSAFE 1", "UNSAFE 2"], [ROLLBACK, ROLLBACK], 2, 1.6).move_to(cohort_replay)
        separate_path = VGroup(
            DashedLine(transcript_small.get_bottom(), auditor.get_left(), color=MUTED, stroke_width=3),
            Arrow(auditor.get_right(), cohort_replay.get_bottom(), color=AUTHORITY, buff=0.08),
        )
        bounded = self.badge("BOUNDED DEFECT · VERIFIED", AUTHORITY, 3.1).shift(RIGHT * 4.2 + UP * -2.5)
        scene12 = VGroup(transcript_small, auditor, cohort_replay, unsafe_pair, separate_path, bounded)
        self.play_beat(12, FadeOut(scene11), FadeIn(transcript_small), FadeIn(auditor), Create(separate_path), FadeIn(cohort_replay), LaggedStart(*[FadeIn(x) for x in unsafe_pair], lag_ratio=0.2), FadeIn(bounded), settle=0.7)

        # 13 — informed direct baseline and assisted path share the envelope
        envelope = self.panel("MATCHED EVIDENCE · TIME · COST", AUTHORITY, 11.0, 5.2)
        direct = self.panel("INFORMED DIRECT", EVIDENCE, 4.0, 2.8).shift(LEFT * 3.4)
        assisted = self.panel("ASSISTED REVIEW", ACCENT, 4.0, 2.8).shift(RIGHT * 3.4)
        same_packet = self.grid(["SAME PACKET", "SAME CLOCK", "SAME BILL"], [AUTHORITY] * 3, 3, 2.1).shift(UP * -2.1)
        compare = Arrow(direct.get_right(), assisted.get_left(), color=AUTHORITY, buff=0.15)
        scene13 = VGroup(envelope, direct, assisted, same_packet, compare)
        self.play_beat(13, FadeOut(scene12), FadeIn(envelope), FadeIn(direct), FadeIn(assisted), GrowArrow(compare), FadeIn(same_packet), settle=0.7)

        # 14 — four achievements remain non-substitutable
        achievements = self.grid(["EXPOSE", "VERIFY", "RECORD", "BLOCK"], [ACCENT, AUTHORITY, EVIDENCE, COPPER], 4, 2.15)
        owners = self.grid(["CRITIC", "AUDITOR", "EVIDENCE", "AUTHORITY"], [ACCENT, AUTHORITY, EVIDENCE, COPPER], 4, 2.15).shift(UP * -2.0)
        joins = VGroup(*[Arrow(achievements[i].get_bottom(), owners[i].get_top(), color=[ACCENT, AUTHORITY, EVIDENCE, COPPER][i], buff=0.08) for i in range(4)])
        firewalls = VGroup(*[Line(UP * 2.4, UP * -2.4, color=BOUNDARY, stroke_width=3).shift(LEFT * 3.25 + RIGHT * i * 3.25) for i in range(1, 4)])
        scene14 = VGroup(achievements, owners, joins, firewalls)
        self.play_beat(14, FadeOut(scene13), LaggedStart(*[FadeIn(x) for x in achievements], lag_ratio=0.15), Create(firewalls), LaggedStart(*[GrowArrow(x) for x in joins], lag_ratio=0.15), FadeIn(owners), settle=0.7)

        # 15 — the complete record routes to quarantine
        candidate_small = self.candidate(compact=True).scale(0.8).shift(LEFT * 4.9)
        quarantine = self.panel("QUARANTINE", ROLLBACK, 3.3, 3.0).shift(RIGHT * 4.7)
        receipt_items = self.grid(["OMITTED COHORT", "2 UNSAFE", "SHARED FAMILY", "OPERATOR TIME", "MODEL CALLS", "RERUN REQUIRED"], [ROLLBACK, ROLLBACK, COPPER, MUTED, MUTED, AUTHORITY], 2, 2.2)
        route = Arrow(candidate_small.get_right(), quarantine.get_left(), color=ROLLBACK, buff=0.08)
        scene15 = VGroup(candidate_small, quarantine, receipt_items, route)
        self.play_beat(15, FadeOut(scene14), FadeIn(candidate_small), FadeIn(receipt_items), GrowArrow(route), FadeIn(quarantine), settle=0.65)

        # 16 — missing auditor routes to escalation, not a pass
        missing = self.panel("OUTCOME AUDITOR · MISSING", ROLLBACK, 4.6, 2.6).shift(LEFT * 3.8)
        transcript_only = self.badge("TRANSCRIPT COMPLETE", COPPER, 2.8).move_to(missing)
        escalation = self.panel("ACCOUNTABLE ESCALATION", AUTHORITY, 4.6, 2.6).shift(RIGHT * 3.8)
        escalation_path = Arrow(missing.get_right(), escalation.get_left(), color=AUTHORITY, buff=0.1)
        pass_badge = self.badge("INFERRED PASS", ROLLBACK, 2.2).shift(UP * -2.2)
        pass_cross = Cross(pass_badge, stroke_color=ROLLBACK)
        scene16 = VGroup(missing, transcript_only, escalation, escalation_path, pass_badge, pass_cross)
        self.play_beat(16, FadeOut(scene15), FadeIn(missing), FadeIn(transcript_only), GrowArrow(escalation_path), FadeIn(escalation), FadeIn(pass_badge), Create(pass_cross), settle=0.65)

        # 17 — the consumer-bound protocol receipt
        receipt = self.panel("OVERSIGHT PROTOCOL RECEIPT", AUTHORITY, 11.3, 5.4)
        fields = self.grid(
            ["COHORT", "CAPABILITY", "ACCESS", "ROLES", "DEPENDENCIES", "BASELINE", "AUDIT", "CALIBRATION", "COVERAGE", "ABSTENTION", "RESIDUAL OWNER", "CONSUMER", "EXPIRY", "READMISSION"],
            [ACCENT, ACCENT, AUTHORITY, COPPER, ROLLBACK, EVIDENCE, AUTHORITY, EVIDENCE, MUTED, ROLLBACK, COPPER, AUTHORITY, MUTED, RESIDUAL], 4, 2.15,
        ).move_to(receipt)
        scene17 = VGroup(receipt, fields)
        self.play_beat(17, FadeOut(scene16), FadeIn(receipt), LaggedStart(*[FadeIn(fields[i]) for i in range(9)], lag_ratio=0.08), settle=0.75)

        # 18 — emphasize abstention, residual, consumer, expiry, and readmission
        self.play_beat(18, LaggedStart(*[FadeIn(fields[i]) for i in range(9, 14)], lag_ratio=0.15), settle=0.45)

        # 18 — forbid stronger-consumer laundering
        aid = self.panel("CLAIM-REVIEW AID", ACCENT, 3.4, 2.6).shift(LEFT * 4.6)
        consumers = self.grid(["TRAINING LABEL", "RELEASE INPUT", "TOOL GRANT"], [ROLLBACK] * 3, 1, 2.4).shift(RIGHT * 3.4)
        attempted = VGroup(*[DashedLine(aid.get_right(), c.get_left(), color=ROLLBACK, stroke_width=4) for c in consumers])
        blocked = VGroup(*[Cross(c, stroke_color=ROLLBACK) for c in consumers])
        named_only = self.badge("NAMED CONSUMER ONLY", AUTHORITY, 2.9).shift(UP * -2.5)
        scene18 = VGroup(aid, consumers, attempted, blocked, named_only)
        self.play_beat(19, FadeOut(scene17), FadeIn(aid), Create(attempted), FadeIn(consumers), Create(blocked), FadeIn(named_only), settle=0.65)

        # 19 — material change invalidates inherited admission
        v1 = self.badge("ADMISSION · V1", EVIDENCE, 2.4).shift(LEFT * 4.9 + UP * 2.0)
        changes = self.grid(["MODEL", "TASK", "VIEW", "PROMPT", "CORPUS", "JUDGE", "PROTOCOL", "AUDITOR"], [COPPER] * 8, 4, 1.8)
        v1_cross = Cross(v1, stroke_color=ROLLBACK)
        readmit = self.badge("READMISSION REQUIRED", AUTHORITY, 3.0).shift(RIGHT * 4.6 + UP * -2.2)
        v2 = self.badge("V2 · OPEN", MUTED, 2.1).shift(LEFT * 4.7 + UP * -2.2)
        scene19 = VGroup(v1, changes, v1_cross, readmit, v2)
        self.play_beat(20, FadeOut(scene18), FadeIn(v1), FadeIn(changes), Create(v1_cross), FadeIn(v2), GrowArrow(Arrow(v2.get_right(), readmit.get_left(), color=AUTHORITY)), FadeIn(readmit), settle=0.65)

        # 20 — calibrated abstention carries a defeater and route
        abstain = self.panel("CALIBRATED ABSTENTION", ROLLBACK, 10.8, 5.2)
        abstain_fields = self.grid(["UNRESOLVED CLAIM", "EVIDENCE TRIED", "BUDGET ENDED", "DEFEATER", "QUEUE EFFECT", "NEXT ROUTE"], [ROLLBACK, ACCENT, MUTED, AUTHORITY, COPPER, EVIDENCE], 3, 2.65).move_to(abstain)
        generic = self.badge("GENERIC REFUSAL", MUTED, 2.5).shift(UP * -2.7)
        generic_cross = Cross(generic, stroke_color=ROLLBACK)
        scene20 = VGroup(abstain, abstain_fields, generic, generic_cross)
        self.play_beat(21, FadeOut(scene19), FadeIn(abstain), LaggedStart(*[FadeIn(f) for f in abstain_fields], lag_ratio=0.1), FadeIn(generic), Create(generic_cross), settle=0.7)

        # 21 — four distinct failure patterns
        failures = VGroup(
            self.panel("PERSUASION", ROLLBACK, 3.2, 2.4),
            self.panel("CORRELATION", ROLLBACK, 3.2, 2.4),
            self.panel("WEAK BASELINE", ROLLBACK, 3.2, 2.4),
            self.panel("SELECTED COHORT", ROLLBACK, 3.2, 2.4),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.65))
        failure_text = VGroup(
            self.label("BEST ADVOCATE", 15, ROLLBACK, "BOLD").move_to(failures[0]),
            self.label("FALSE AGREEMENT", 15, ROLLBACK, "BOLD").move_to(failures[1]),
            self.label("BENEFIT LAUNDERED", 15, ROLLBACK, "BOLD").move_to(failures[2]),
            self.label("HARD CASES HIDDEN", 15, ROLLBACK, "BOLD").move_to(failures[3]),
        )
        scene21 = VGroup(failures, failure_text)
        self.play_beat(22, FadeOut(scene20), LaggedStart(*[FadeIn(f) for f in failures], lag_ratio=0.14), LaggedStart(*[FadeIn(x) for x in failure_text], lag_ratio=0.14), settle=0.65)

        # 22 — scrutiny grows discovery and governance cost together
        critics = self.grid(["C1", "C2", "C3", "C4", "C5"], [ACCENT] * 5, 5, 0.9).shift(LEFT * 3.8 + UP * 1.5)
        discovery = self.badge("DISCOVERY ↑", EVIDENCE, 2.2).shift(LEFT * 3.8 + UP * -1.5)
        costs = self.grid(["LATENCY", "PRIVACY", "COST", "FATIGUE"], [COPPER, ROLLBACK, COPPER, ROLLBACK], 1, 1.8).shift(RIGHT * 3.8)
        queue = Rectangle(width=0.8, height=4.6, stroke_color=AUTHORITY, stroke_width=4).shift(RIGHT * 0.5)
        queue_fill = Rectangle(width=0.65, height=3.2, stroke_width=0, fill_color=ROLLBACK, fill_opacity=0.65).align_to(queue, UP * -1).shift(RIGHT * 0.5 + UP * -0.65)
        scene22 = VGroup(critics, discovery, costs, queue, queue_fill)
        self.play_beat(23, FadeOut(scene21), FadeIn(critics), FadeIn(discovery), Create(queue), GrowFromCenter(queue_fill), LaggedStart(*[FadeIn(c) for c in costs], lag_ratio=0.12), settle=0.65)

        # 23 — non-aggregated operating metrics
        dashboard = self.panel("CONTROL-PLANE SCORECARD", AUTHORITY, 11.2, 5.4)
        metrics = self.grid(["USEFUL THROUGHPUT", "UNSAFE ADMISSION", "FALSE REJECTION", "COVERAGE", "SELECTIVE RISK", "LATENCY", "OPERATOR BURDEN", "ESCALATION LOAD", "RESIDUAL RISK"], [EVIDENCE, ROLLBACK, ROLLBACK, ACCENT, COPPER, MUTED, COPPER, AUTHORITY, RESIDUAL], 3, 2.75).move_to(dashboard)
        no_average = self.badge("NO AVERAGE HIDES FAILURE", ROLLBACK, 3.5).shift(UP * -2.85)
        scene23 = VGroup(dashboard, metrics, no_average)
        self.play_beat(24, FadeOut(scene22), FadeIn(dashboard), LaggedStart(*[FadeIn(m) for m in metrics], lag_ratio=0.07), FadeIn(no_average), settle=0.7)

        # 24 — repository artifacts stay inside argument support
        enclosure = self.panel("ARGUMENT SUPPORT", AUTHORITY, 10.6, 5.0)
        artifacts = self.grid(["7-STAGE LIFECYCLE", "58 ROUTES", "65 REJECTIONS"], [ACCENT, EVIDENCE, ROLLBACK], 3, 2.6).move_to(enclosure)
        custody = self.badge("RECORD CUSTODY + REFUSAL", AUTHORITY, 3.2).shift(UP * -2.5)
        competence = self.badge("REVIEWER COMPETENCE?", ROLLBACK, 2.9).shift(RIGHT * 4.7 + UP * 2.4)
        competence_cross = Cross(competence, stroke_color=ROLLBACK)
        scene24 = VGroup(enclosure, artifacts, custody, competence, competence_cross)
        self.play_beat(25, FadeOut(scene23), FadeIn(enclosure), LaggedStart(*[FadeIn(a) for a in artifacts], lag_ratio=0.16), FadeIn(custody), FadeIn(competence), Create(competence_cross), settle=0.7)

        # 25 — evidence ceiling: no natural or empirical campaign
        none_run = self.grid(["NO MODELS", "NO HUMAN STUDY", "NO NATURAL WORKLOAD", "NO HELD-OUT CAMPAIGN", "NO CAUSAL ABLATION", "NO DEPLOYMENT", "NO REPRODUCTION", "NO TRANSFER"], [ROLLBACK] * 8, 4, 2.1)
        ceiling = self.panel("EXPLICIT + TESTABLE BOUNDARY", AUTHORITY, 10.8, 2.0).shift(UP * -2.1)
        scene25 = VGroup(none_run, ceiling)
        self.play_beat(26, FadeOut(scene24), FadeIn(none_run), FadeIn(ceiling), settle=0.75)

        # 26 — payoff: a control plane rather than an automated jury
        plane = self.panel("OVERSIGHT CONTROL PLANE", AUTHORITY, 3.5, 3.8).shift(LEFT * 4.6)
        assisted_routes = self.grid(["DIRECT", "CONSULT", "ADVERSARIAL", "ABSTAIN", "ESCALATE"], [EVIDENCE, ACCENT, COPPER, ROLLBACK, AUTHORITY], 1, 2.1)
        plane_paths = VGroup(*[Arrow(plane.get_right(), r.get_left(), color=[EVIDENCE, ACCENT, COPPER, ROLLBACK, AUTHORITY][i], buff=0.08) for i, r in enumerate(assisted_routes)])
        authority_owner = self.panel("AUTHORITY OWNER", COPPER, 3.2, 3.2).shift(RIGHT * 4.8)
        boundary = Line(UP * 3.0, UP * -3.0, color=BOUNDARY, stroke_width=5).shift(RIGHT * 2.6)
        scene26 = VGroup(plane, assisted_routes, plane_paths, authority_owner, boundary)
        self.play_beat(27, FadeOut(scene25), FadeIn(plane), LaggedStart(*[GrowArrow(p) for p in plane_paths], lag_ratio=0.1), FadeIn(assisted_routes), Create(boundary), FadeIn(authority_owner), settle=0.8)

        # 27 — handoff to the signed principal and intent contract
        request_packet = self.panel("BOUNDED OVERSIGHT REQUEST", AUTHORITY, 4.1, 3.0).shift(LEFT * 4.5)
        principal = self.panel("SIGNED PRINCIPAL", COPPER, 3.6, 3.0).shift(RIGHT * 4.5)
        intent_fields = self.grid(["OUTCOME", "UNACCEPTABLE MEANS", "AUTHORITY", "STOP"], [EVIDENCE, ROLLBACK, COPPER, AUTHORITY], 2, 2.3)
        handoff = Arrow(request_packet.get_right(), intent_fields.get_left(), color=AUTHORITY, buff=0.1)
        owner_path = Arrow(intent_fields.get_right(), principal.get_left(), color=COPPER, buff=0.1)
        next_badge = self.badge("NEXT · HUMAN INTENT", ACCENT, 2.8).shift(UP * -2.5)
        scene27 = VGroup(request_packet, principal, intent_fields, handoff, owner_path, next_badge)
        self.play_beat(28, FadeOut(scene26), FadeIn(request_packet), GrowArrow(handoff), FadeIn(intent_fields), GrowArrow(owner_path), FadeIn(principal), FadeIn(next_badge), settle=0.8)
