"""Generation-two visual abstract for ``ASI Is a Stack, Not a Model``.

The scene preserves one proposal identity across verification, authorization,
effect, receipt, observation, recovery, abstraction, and changed-case transfer.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    ArcBetweenPoints,
    Arrow,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    PI,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    TransformMatchingShapes,
    UP,
    VGroup,
    Write,
    rate_functions,
)

from visual_edition.lib.asi_visuals import (
    ACCENT,
    AUTHORITY,
    BACKGROUND,
    BOUNDARY,
    COPPER,
    EVIDENCE,
    INK,
    MUTED,
    RESIDUAL,
    ROLLBACK,
    SURFACE,
    AsiScene,
    residual_marker,
    text,
)


class AsiIsAStackNotAModelGeneration2(AsiScene):
    TARGET_DURATION = 153.035
    ENDS = [
        6.000,
        12.080,
        17.530,
        23.100,
        29.780,
        37.220,
        46.605,
        53.180,
        59.300,
        72.130,
        77.060,
        84.580,
        96.305,
        102.660,
        107.300,
        112.610,
        118.300,
        129.415,
        136.140,
        147.335,
        153.035,
    ]

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        run_time = max(0.05, remaining - min(settle, remaining * 0.28))
        if animations:
            self.play(*animations, run_time=run_time)
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 22, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def capsule(self, label: str, color: str = COPPER, width: float = 2.05) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=0.76,
            corner_radius=0.36,
            stroke_color=color,
            stroke_width=3,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        port = Circle(radius=0.11, color=color, fill_color=color, fill_opacity=1).shift(LEFT * (width / 2 - 0.25))
        words = self.label(label, 18, INK, "BOLD").shift(RIGHT * 0.12)
        return VGroup(shell, port, words)

    def warehouse_row(self) -> VGroup:
        shell = RoundedRectangle(
            width=0.72,
            height=0.34,
            corner_radius=0.05,
            stroke_color=BOUNDARY,
            stroke_width=1.6,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        dot = Circle(radius=0.045, color=MUTED, fill_color=MUTED, fill_opacity=1).shift(LEFT * 0.24)
        line = Line(LEFT * 0.08, RIGHT * 0.23, color=MUTED, stroke_width=1.4)
        return VGroup(shell, dot, line)

    def gate(self, label: str = "AUTHORITY") -> VGroup:
        left = Line(UP * 0.72, DOWN * 0.72, color=AUTHORITY, stroke_width=7).shift(LEFT * 0.24)
        right = left.copy().shift(RIGHT * 0.48)
        bar = Line(LEFT * 0.34, RIGHT * 0.34, color=AUTHORITY, stroke_width=6).shift(UP * 0.12)
        title = self.label(label, 14, AUTHORITY, "BOLD").next_to(VGroup(left, right), UP, buff=0.12)
        return VGroup(VGroup(left, right), bar, title)

    def key(self, label: str, *, expired: bool = False) -> VGroup:
        ring = Circle(radius=0.16, color=ROLLBACK if expired else AUTHORITY, stroke_width=4)
        stem = Line(ring.get_right(), ring.get_right() + RIGHT * 0.55, color=ring.get_color(), stroke_width=4)
        tooth = Line(stem.get_end() + LEFT * 0.12, stem.get_end() + LEFT * 0.12 + DOWN * 0.16, color=ring.get_color(), stroke_width=4)
        tag = self.label(label, 12, ring.get_color(), "BOLD").next_to(VGroup(ring, stem, tooth), DOWN, buff=0.08)
        return VGroup(ring, stem, tooth, tag)

    def counter(self, heading: str, value: str, color: str) -> VGroup:
        shell = RoundedRectangle(
            width=2.2,
            height=1.05,
            corner_radius=0.1,
            stroke_color=color,
            stroke_width=2.4,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        title = self.label(heading, 14, color, "BOLD").move_to(shell.get_center() + UP * 0.23)
        number = self.label(value, 27, INK, "BOLD").move_to(shell.get_center() + DOWN * 0.18)
        return VGroup(shell, title, number)

    def rail(self, heading: str, y: float, color: str) -> VGroup:
        line = Line(LEFT * 4.6, RIGHT * 4.6, color=color, stroke_width=2.2).shift(UP * y)
        title = self.label(heading, 15, color, "BOLD").next_to(line, LEFT, buff=0.2)
        return VGroup(line, title)

    def stop_bar(self, y: float, color: str = BOUNDARY) -> VGroup:
        bar = Line(DOWN * 0.26, UP * 0.26, color=color, stroke_width=5).shift(RIGHT * 0.45 + UP * y)
        cap = Line(LEFT * 0.11, RIGHT * 0.11, color=color, stroke_width=4).move_to(bar.get_center() + UP * 0.25)
        return VGroup(bar, cap)

    def construct(self) -> None:
        rail = Line(LEFT * 6.05, RIGHT * 5.75, color="#31434F", stroke_width=2).shift(DOWN * 0.15)
        task_tag = self.label("TASK CONTRACT", 13, MUTED, "BOLD").shift(LEFT * 5.0 + UP * 3.35)
        ribbon_shell = RoundedRectangle(
            width=11.7,
            height=0.62,
            corner_radius=0.08,
            color=INK,
            stroke_width=2.2,
            fill_color=SURFACE,
            fill_opacity=1,
        ).shift(UP * 2.92)
        ribbon_text = self.label("READ ONLY", 23, INK, "BOLD").move_to(ribbon_shell)
        self.ribbon = VGroup(ribbon_shell, ribbon_text)

        warehouse_shell = RoundedRectangle(
            width=4.35,
            height=3.25,
            corner_radius=0.14,
            color=BOUNDARY,
            stroke_width=2.5,
            fill_color="#13212A",
            fill_opacity=1,
        ).shift(RIGHT * 3.55 + UP * 0.38)
        warehouse_title = self.label("DATA WAREHOUSE", 16, MUTED, "BOLD").next_to(warehouse_shell, UP, buff=0.12)
        self.rows = VGroup(*[self.warehouse_row() for _ in range(12)])
        self.rows.arrange_in_grid(rows=4, cols=3, buff=(0.18, 0.18)).move_to(warehouse_shell)
        self.warehouse = VGroup(warehouse_shell, warehouse_title)

        # b01: the constraint exists before the proposal.
        self.beat(
            1,
            Create(rail),
            FadeIn(task_tag),
            Create(ribbon_shell),
            Write(ribbon_text),
            FadeIn(self.warehouse),
            LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in self.rows], lag_ratio=0.06),
            settle=0.55,
        )

        self.model = VGroup(
            Circle(radius=0.68, color=COPPER, stroke_width=3.5, fill_color=SURFACE, fill_opacity=1),
            Circle(radius=0.28, color=COPPER, stroke_width=2),
            self.label("AI", 19, COPPER, "BOLD"),
        ).shift(LEFT * 5.25 + UP * 0.35)
        stale_marks = VGroup(*[
            Circle(radius=0.055, color=ACCENT, fill_color=ACCENT, fill_opacity=1).move_to(row.get_right() + LEFT * 0.13)
            for row in self.rows
        ])
        self.command = self.capsule("DELETE 12").shift(LEFT * 3.65 + DOWN * 0.15)

        # b02: capability creates a proposal while every row remains in place.
        self.beat(
            2,
            FadeIn(self.model),
            LaggedStart(*[FadeIn(mark) for mark in stale_marks], lag_ratio=0.04),
            TransformFromCopy(self.model[1], self.command),
            settle=0.35,
        )

        self.verifier = VGroup(
            Circle(radius=0.62, color=ACCENT, stroke_width=3.4, fill_color=SURFACE, fill_opacity=1),
            VGroup(
                Line(LEFT * 0.2 + DOWN * 0.02, LEFT * 0.02 + DOWN * 0.2, color=ACCENT, stroke_width=5),
                Line(LEFT * 0.02 + DOWN * 0.2, RIGHT * 0.28 + UP * 0.2, color=ACCENT, stroke_width=5),
            ),
            self.label("VERIFY", 13, ACCENT, "BOLD").shift(DOWN * 0.9),
        ).shift(LEFT * 2.35 + UP * 0.2)
        run_question = self.label("RUN?", 24, AUTHORITY, "BOLD").next_to(self.command, UP, buff=0.24)

        # b03: a checked proposal still has not changed a row.
        self.beat(
            3,
            Succession(
                self.command.animate.move_to(LEFT * 0.5 + DOWN * 0.15),
                AnimationGroup(FadeIn(self.verifier), FadeIn(run_question)),
            ),
            settle=0.48,
        )

        rule_card = VGroup(
            RoundedRectangle(width=2.0, height=0.78, corner_radius=0.08, color=ACCENT, fill_color=SURFACE, fill_opacity=1),
            self.label("CLEANUP RULE", 14, ACCENT, "BOLD"),
            self.label("MATCH", 12, INK, "BOLD").shift(DOWN * 0.22),
        ).shift(LEFT * 2.0 + DOWN * 1.45)
        self.auth_gate = self.gate().shift(RIGHT * 1.05 + DOWN * 0.15)

        # b04: open the verifier and expose its narrow predicate.
        self.beat(
            4,
            FadeOut(run_question),
            TransformFromCopy(self.verifier, rule_card),
            FadeIn(self.auth_gate, shift=RIGHT * 0.12),
            settle=0.4,
        )
        self.add(self.verifier)

        scope_ray = DashedLine(self.ribbon.get_bottom(), self.auth_gate.get_top(), color=INK, dash_length=0.11, stroke_width=2)

        # b05: request scope, not confidence, controls the authority boundary.
        self.beat(
            5,
            Create(scope_ray),
            self.command.animate.move_to(self.auth_gate.get_left() + LEFT * 0.82),
            Circumscribe(self.ribbon, color=INK),
            Circumscribe(self.auth_gate, color=AUTHORITY),
            settle=0.55,
        )

        checks = VGroup(*[
            VGroup(
                RoundedRectangle(width=1.02, height=0.48, corner_radius=0.06, color=AUTHORITY, fill_color=SURFACE, fill_opacity=1),
                self.label(name, 11, AUTHORITY, "BOLD"),
            )
            for name in ("OWNER", "EFFECT", "SCOPE", "TIME")
        ]).arrange(RIGHT, buff=0.13).scale(0.92).shift(RIGHT * 0.9 + DOWN * 1.55)
        failed_time = VGroup(
            Line(checks[3].get_corner(UP + LEFT), checks[3].get_corner(DOWN + RIGHT), color=ROLLBACK, stroke_width=4),
            Line(checks[3].get_corner(DOWN + LEFT), checks[3].get_corner(UP + RIGHT), color=ROLLBACK, stroke_width=4),
        )

        # b06: admission is a conjunction of current fields.
        self.beat(
            6,
            LaggedStart(*[FadeIn(check, shift=UP * 0.08) for check in checks], lag_ratio=0.14),
            Create(failed_time),
            settle=0.45,
        )

        expired_key = self.key("LAST WEEK", expired=True).shift(RIGHT * 0.72 + UP * 1.35)
        denial = self.capsule("DENIED", ROLLBACK, 1.65).scale(0.78).shift(RIGHT * 0.85 + DOWN * 2.35)
        not_complete = self.label("NOT COMPLETE", 13, ROLLBACK, "BOLD").next_to(denial, RIGHT, buff=0.18)
        crack = VGroup(
            Line(expired_key.get_center() + LEFT * 0.15 + UP * 0.2, expired_key.get_center() + RIGHT * 0.16 + DOWN * 0.2, color=ROLLBACK, stroke_width=4),
            Line(expired_key.get_center() + LEFT * 0.15 + DOWN * 0.2, expired_key.get_center() + RIGHT * 0.16 + UP * 0.2, color=ROLLBACK, stroke_width=4),
        )

        # b07: denial is an owned outcome, not task completion.
        self.beat(
            7,
            FadeIn(expired_key),
            Create(crack),
            TransformFromCopy(self.command, denial),
            FadeIn(not_complete),
            Circumscribe(self.warehouse, color=BOUNDARY),
            settle=0.85,
        )

        grant_shell = ribbon_shell.copy().set_stroke(AUTHORITY)
        grant_text = self.label("DELETE 12  |  OWNER GRANT  |  10 MIN", 21, AUTHORITY, "BOLD").move_to(grant_shell)
        grant_ribbon = VGroup(grant_shell, grant_text)
        fresh_key = self.key("10 MIN").move_to(expired_key)

        # b08: matched case, one changed fact.
        self.beat(
            8,
            Succession(
                AnimationGroup(
                    FadeOut(self.ribbon),
                    FadeOut(expired_key),
                    FadeOut(crack),
                    FadeOut(denial),
                    FadeOut(not_complete),
                    FadeOut(failed_time),
                ),
                AnimationGroup(FadeIn(grant_ribbon), FadeIn(fresh_key)),
            ),
            settle=0.55,
        )
        self.ribbon = grant_ribbon
        self.fresh_key = fresh_key

        invariant_bar = VGroup(
            Line(LEFT * 2.8, RIGHT * 0.8, color=MUTED, stroke_width=2.2),
            Line(DOWN * 0.12, UP * 0.12, color=MUTED, stroke_width=2.2).shift(LEFT * 2.8),
            Line(DOWN * 0.12, UP * 0.12, color=MUTED, stroke_width=2.2).shift(RIGHT * 0.8),
        ).shift(DOWN * 1.22)
        same_label = self.label("MODEL + VERIFIER UNCHANGED", 14, MUTED, "BOLD").next_to(invariant_bar, DOWN, buff=0.12)
        new_contract = self.label("NEW CONTRACT", 13, AUTHORITY, "BOLD").next_to(self.ribbon, DOWN, buff=0.08)

        # b09: capability and verification do not change in the counterfactual.
        self.beat(
            9,
            Succession(
                AnimationGroup(FadeOut(rule_card), FadeOut(checks)),
                AnimationGroup(Create(invariant_bar), FadeIn(same_label), FadeIn(new_contract)),
                AnimationGroup(
                    Circumscribe(self.command, color=COPPER),
                    Circumscribe(self.verifier, color=ACCENT),
                ),
            ),
            settle=0.45,
        )

        open_gate = self.auth_gate.copy()
        open_gate[1].rotate(-PI / 2, about_point=open_gate[1].get_left())
        snapshot_shell = RoundedRectangle(
            width=2.45,
            height=1.72,
            corner_radius=0.12,
            color=ROLLBACK,
            stroke_width=2.2,
            fill_color=SURFACE,
            fill_opacity=1,
        ).shift(LEFT * 4.55 + DOWN * 1.45)
        pre_state = self.rows.copy().scale(0.43).move_to(snapshot_shell)
        pre_state_label = self.label("RECORDED PRE-STATE", 12, ROLLBACK, "BOLD").next_to(snapshot_shell, UP, buff=0.1)

        # b10: proposal and grant join; exactly twelve rows change.
        self.beat(
            10,
            FadeOut(invariant_bar),
            FadeOut(same_label),
            FadeOut(new_contract),
            FadeIn(snapshot_shell),
            FadeIn(pre_state),
            FadeIn(pre_state_label),
            self.fresh_key.animate.move_to(RIGHT * 2.15 + UP * 1.15),
            self.command.animate.move_to(self.auth_gate.get_left() + LEFT * 0.35),
            ReplacementTransform(self.auth_gate, open_gate),
            LaggedStart(
                *[
                    FadeOut(VGroup(row, mark), shift=DOWN * 0.12)
                    for row, mark in zip(self.rows, stale_marks)
                ],
                lag_ratio=0.035,
            ),
            settle=1.0,
        )
        self.auth_gate = open_gate
        self.pre_state = VGroup(snapshot_shell, pre_state, pre_state_label)

        self.receipt = self.counter("RECEIPT", "12", COPPER).scale(0.82).shift(LEFT * 1.55 + DOWN * 1.55)
        self.observed = self.counter("OBSERVED", "13", EVIDENCE).scale(0.82).shift(RIGHT * 2.05 + DOWN * 1.55)
        observed_mask = VGroup(
            Rectangle(
                width=1.25,
                height=0.42,
                stroke_width=0,
                fill_color=SURFACE,
                fill_opacity=1,
            ),
            self.label("CHECKING", 11, MUTED, "BOLD"),
        ).move_to(self.observed[2])
        self.observed.add(observed_mask)
        self.observation_arrow = Arrow(
            self.warehouse.get_bottom(),
            self.observed.get_top(),
            color=EVIDENCE,
            stroke_width=2.5,
            buff=0.1,
        )

        # b11: tool report and observation enter on separate paths.
        self.beat(
            11,
            TransformFromCopy(self.command, self.receipt),
            FadeIn(self.observed, shift=RIGHT * 0.15),
            GrowArrow(self.observation_arrow),
            settle=0.45,
        )

        difference = VGroup(
            Line(LEFT * 0.55, RIGHT * 0.55, color=RESIDUAL, stroke_width=3),
            Line(LEFT * 0.55 + DOWN * 0.13, LEFT * 0.55 + UP * 0.13, color=RESIDUAL, stroke_width=3),
            Line(RIGHT * 0.55 + DOWN * 0.13, RIGHT * 0.55 + UP * 0.13, color=RESIDUAL, stroke_width=3),
            self.label("+1", 18, RESIDUAL, "BOLD").shift(UP * 0.23),
        ).move_to((self.receipt.get_center() + self.observed.get_center()) / 2)
        self.residual = residual_marker("UNEXPLAINED").scale(0.8).shift(RIGHT * 4.95 + DOWN * 1.45)

        # b12: preserve the contradiction rather than overwriting observation.
        self.beat(
            12,
            FadeOut(observed_mask),
            Create(difference),
            FadeIn(self.residual),
            Circumscribe(self.receipt, color=COPPER),
            Circumscribe(self.observed, color=EVIDENCE),
            settle=0.8,
        )
        self.observed.remove(observed_mask)

        recovery_arc = ArcBetweenPoints(self.observed.get_top(), self.pre_state.get_right(), angle=-PI / 2, color=ROLLBACK, stroke_width=4)
        recovery_tip = Arrow(recovery_arc.get_end() + LEFT * 0.02, recovery_arc.get_end(), color=ROLLBACK, stroke_width=4, buff=0)
        owner_tag = self.capsule("OWNER", RESIDUAL, 1.55).scale(0.72).next_to(self.residual, UP, buff=0.25)

        # b13: recovery and residual ownership are separate dispositions.
        self.beat(
            13,
            Create(recovery_arc),
            GrowArrow(recovery_tip),
            FadeIn(owner_tag),
            Circumscribe(self.pre_state, color=ROLLBACK),
            settle=1.15,
        )

        abstract_rails = VGroup(
            self.rail("CAPABILITY", 1.8, COPPER),
            self.rail("AUTHORITY", 0.6, AUTHORITY),
            self.rail("REPORT", -0.6, ACCENT),
            self.rail("WORLD", -1.8, EVIDENCE),
        )
        stops = VGroup(
            self.stop_bar(1.8, AUTHORITY),
            self.stop_bar(0.6, BOUNDARY),
            self.stop_bar(-0.6, EVIDENCE),
        )
        concrete = VGroup(
            task_tag,
            rail,
            self.ribbon,
            self.warehouse,
            self.rows,
            stale_marks,
            self.model,
            self.verifier,
            self.auth_gate,
            scope_ray,
            self.fresh_key,
            self.pre_state,
            self.observation_arrow,
            difference,
            self.residual,
            owner_tag,
            recovery_arc,
            recovery_tip,
        )

        # b14: the concrete trace earns the noninheritance abstraction.
        self.beat(
            14,
            FadeOut(concrete, scale=0.94),
            FadeIn(abstract_rails),
            FadeIn(stops),
            self.command.animate.move_to(LEFT * 2.2 + UP * 1.8).scale(0.82),
            self.receipt.animate.move_to(LEFT * 2.15 + DOWN * 0.6).scale(0.82),
            self.observed.animate.move_to(RIGHT * 2.15 + DOWN * 1.8).scale(0.82),
            settle=0.55,
        )

        report_world_stop = self.stop_bar(-1.2, RESIDUAL).shift(RIGHT * 2.0)
        report_world_label = self.label("NO PROMOTION", 12, RESIDUAL, "BOLD").next_to(report_world_stop, RIGHT, buff=0.12)

        # b15: report and world remain separate rails.
        self.beat(
            15,
            self.receipt.animate.move_to(LEFT * 1.65 + DOWN * 0.6),
            self.observed.animate.move_to(RIGHT * 1.65 + DOWN * 1.8),
            FadeIn(report_world_stop),
            FadeIn(report_world_label),
            settle=0.45,
        )

        update = self.capsule("UPDATE", ACCENT, 1.7).scale(0.72).shift(LEFT * 2.8 + UP * 2.75)
        update_check = self.verifier.copy().scale(0.55).move_to(LEFT * 0.65 + UP * 2.75)
        approval = self.gate("APPROVAL").scale(0.72).shift(RIGHT * 2.0 + UP * 2.75)
        update_path = Arrow(update.get_right(), approval.get_left(), color=ACCENT, stroke_width=2.2, buff=0.1)

        # b16: a tested self-improvement still stops at external approval.
        self.beat(
            16,
            Succession(
                TransformFromCopy(self.command, update),
                update.animate.move_to(approval.get_left() + LEFT * 0.62),
            ),
            FadeIn(update_check),
            GrowArrow(update_path),
            FadeIn(approval),
            settle=0.55,
        )

        patch = self.capsule("PATCH", COPPER, 1.72).scale(0.78).move_to(self.command)
        servers = VGroup(*[
            VGroup(
                RoundedRectangle(width=0.78, height=1.25, corner_radius=0.08, color=BOUNDARY, fill_color=SURFACE, fill_opacity=1),
                VGroup(*[Circle(radius=0.045, color=EVIDENCE, fill_color=EVIDENCE, fill_opacity=1) for _ in range(3)]).arrange(DOWN, buff=0.11),
            )
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.28).shift(RIGHT * 3.35 + DOWN * 0.15)
        production = self.label("PRODUCTION", 14, MUTED, "BOLD").next_to(servers, UP, buff=0.12)

        # b17: changed-case transfer preserves the learned coordinates.
        self.beat(
            17,
            FadeOut(update),
            FadeOut(update_check),
            FadeOut(update_path),
            FadeOut(approval),
            FadeOut(self.receipt),
            FadeOut(self.observed),
            FadeOut(report_world_stop),
            FadeOut(report_world_label),
            ReplacementTransform(self.command, patch),
            FadeIn(servers),
            FadeIn(production),
            Circumscribe(stops[0], color=AUTHORITY),
            settle=0.55,
        )
        self.patch = patch

        ownership = VGroup(
            VGroup(RoundedRectangle(width=2.6, height=1.35, corner_radius=0.1, color=ACCENT, fill_color=SURFACE, fill_opacity=1), self.label("VERIFY", 17, ACCENT, "BOLD"), self.label("tests", 13, MUTED).shift(DOWN * 0.28)),
            VGroup(RoundedRectangle(width=2.6, height=1.35, corner_radius=0.1, color=AUTHORITY, fill_color=SURFACE, fill_opacity=1), self.label("AUTHORIZE", 17, AUTHORITY, "BOLD"), self.label("production access", 13, MUTED).shift(DOWN * 0.28)),
            VGroup(RoundedRectangle(width=2.6, height=1.35, corner_radius=0.1, color=EVIDENCE, fill_color=SURFACE, fill_opacity=1), self.label("OBSERVE", 17, EVIDENCE, "BOLD"), self.label("changed state", 13, MUTED).shift(DOWN * 0.28)),
        ).arrange(RIGHT, buff=0.55).shift(DOWN * 1.55)
        patch_owner_target = LEFT * 4.55 + UP * 0.65
        servers_owner_target = servers.copy().move_to(RIGHT * 4.25 + UP * 0.65)
        production_owner_target = production.copy().next_to(servers_owner_target, UP, buff=0.12)
        ownership_links = VGroup(
            Line(patch_owner_target + DOWN * 0.35, ownership[0].get_top(), color=ACCENT, stroke_width=2.0),
            Line(production_owner_target.get_bottom(), ownership[1].get_top(), color=AUTHORITY, stroke_width=2.0),
            Line(servers_owner_target.get_bottom(), ownership[2].get_top(), color=EVIDENCE, stroke_width=2.0),
        )

        # b18: three changed-case facts receive three distinct owners.
        self.beat(
            18,
            Succession(
                AnimationGroup(
                    FadeOut(abstract_rails),
                    FadeOut(stops),
                    LaggedStart(*[FadeIn(card, shift=UP * 0.1) for card in ownership], lag_ratio=0.15),
                    self.patch.animate.move_to(patch_owner_target),
                    Transform(servers, servers_owner_target),
                    Transform(production, production_owner_target),
                ),
                LaggedStart(*[Create(link) for link in ownership_links], lag_ratio=0.15),
            ),
            settle=1.0,
        )

        stack_frame = RoundedRectangle(width=10.15, height=5.55, corner_radius=0.18, color=ACCENT, stroke_width=2.8, fill_opacity=0)
        stack_title = self.label("GOVERNED STACK", 20, ACCENT, "BOLD").next_to(stack_frame, UP, buff=0.1)
        model_core = VGroup(
            Circle(radius=0.85, color=COPPER, fill_color=SURFACE, fill_opacity=1, stroke_width=3),
            self.label("MODEL", 18, COPPER, "BOLD"),
        ).shift(UP * 1.05)
        patch_target = LEFT * 2.55 + UP * 1.05
        servers_target = servers.copy().move_to(RIGHT * 2.75 + UP * 1.05)
        production_target = production.copy().next_to(servers_target, UP, buff=0.12)
        stack_links = VGroup(
            Arrow(model_core.get_left(), patch_target + RIGHT * 0.75, color=BOUNDARY, stroke_width=2.2, buff=0.08),
            Arrow(
                patch_target + DOWN * 0.15,
                ownership[0].get_left() + UP * 0.2,
                color=ACCENT,
                stroke_width=2.2,
                buff=0.08,
            ),
            Arrow(ownership[0].get_right(), ownership[1].get_left(), color=BOUNDARY, stroke_width=2.2, buff=0.08),
            Arrow(
                ownership[1].get_right(),
                servers_target.get_corner(DOWN + LEFT),
                color=AUTHORITY,
                stroke_width=2.2,
                buff=0.08,
            ),
            Arrow(
                servers_target.get_corner(DOWN + RIGHT),
                ownership[2].get_right(),
                color=EVIDENCE,
                stroke_width=2.2,
                buff=0.08,
            ),
        )
        cost = VGroup(
            Line(DOWN * 1.7, UP * 1.7, color=BOUNDARY, stroke_width=2.5),
            self.label("COST", 14, MUTED, "BOLD").shift(UP * 1.95),
            self.label("latency", 12, MUTED).shift(UP * 0.7),
            self.label("failure", 12, RESIDUAL).shift(DOWN * 0.1),
            self.label("burden", 12, MUTED).shift(DOWN * 0.9),
        ).shift(RIGHT * 5.65)

        # b19: name the stack and keep cost and failure outside the victory frame.
        self.beat(
            19,
            Succession(
                AnimationGroup(
                    FadeOut(ownership_links),
                    Create(stack_frame),
                    FadeIn(stack_title),
                    FadeIn(model_core),
                    FadeIn(cost),
                ),
                AnimationGroup(
                    self.patch.animate.scale(0.78).move_to(patch_target),
                    Transform(servers, servers_target),
                    Transform(production, production_target),
                ),
                FadeIn(stack_links),
            ),
            settle=0.65,
        )

        questions = VGroup(
            self.label("WHAT PASSES?", 15, ACCENT, "BOLD").next_to(ownership[0], UP, buff=0.16),
            self.label("WHAT MAY ACT?", 15, AUTHORITY, "BOLD").next_to(ownership[1], UP, buff=0.16),
            self.label("WHAT CHANGED?", 15, EVIDENCE, "BOLD").next_to(ownership[2], UP, buff=0.16),
        )

        # b20: a boundary earns its place by owning an inspectable question.
        self.beat(
            20,
            Succession(
                FadeOut(stack_links),
                LaggedStart(
                    *[
                        AnimationGroup(FadeIn(question), Circumscribe(owner, color=color))
                        for question, owner, color in zip(
                            questions,
                            ownership,
                            (ACCENT, AUTHORITY, EVIDENCE),
                        )
                    ],
                    lag_ratio=0.3,
                ),
            ),
            settle=1.2,
        )

        sql_final = self.capsule("SQL", COPPER, 1.55).scale(0.88).shift(LEFT * 3.75 + UP * 0.45)
        patch_final = self.capsule("PATCH", COPPER, 1.7).scale(0.88).shift(LEFT * 3.75 + DOWN * 0.9)
        gate_a = self.gate().scale(0.68).shift(LEFT * 0.65 + UP * 0.45)
        gate_b = self.gate().scale(0.68).shift(LEFT * 0.65 + DOWN * 0.9)
        db_change = VGroup(
            RoundedRectangle(width=2.0, height=0.72, corner_radius=0.1, color=EVIDENCE, fill_color=SURFACE, fill_opacity=1),
            self.label("DATABASE DELTA", 14, EVIDENCE, "BOLD"),
        ).shift(RIGHT * 2.85 + UP * 0.45)
        deploy_change = VGroup(
            RoundedRectangle(width=2.0, height=0.72, corner_radius=0.1, color=EVIDENCE, fill_color=SURFACE, fill_opacity=1),
            self.label("DEPLOY DELTA", 14, EVIDENCE, "BOLD"),
        ).shift(RIGHT * 2.85 + DOWN * 0.9)
        final_rails = VGroup(
            Arrow(sql_final.get_right(), gate_a.get_left(), color=BOUNDARY, stroke_width=2.4, buff=0.08),
            Arrow(patch_final.get_right(), gate_b.get_left(), color=BOUNDARY, stroke_width=2.4, buff=0.08),
            Arrow(gate_a.get_right(), db_change.get_left(), color=EVIDENCE, stroke_width=2.4, buff=0.08),
            Arrow(gate_b.get_right(), deploy_change.get_left(), color=EVIDENCE, stroke_width=2.4, buff=0.08),
        )
        final_labels = VGroup(
            self.label("PROPOSE", 15, COPPER, "BOLD").shift(LEFT * 3.75 + UP * 1.45),
            self.label("AUTHORIZE", 15, AUTHORITY, "BOLD").shift(LEFT * 0.65 + UP * 1.45),
            self.label("OBSERVE", 15, EVIDENCE, "BOLD").shift(RIGHT * 2.85 + UP * 1.45),
        )
        closing_title = self.label("ASI IS A STACK, NOT A MODEL", 23, INK, "BOLD").next_to(stack_frame, UP, buff=0.1)
        source_line = self.label("Argument support | Sources and transcript in the live chapter", 15, MUTED).shift(DOWN * 2.55)

        # b21: both domains resolve to the same noninheritance structure.
        self.beat(
            21,
            Succession(
                AnimationGroup(
                    FadeOut(model_core),
                    FadeOut(cost),
                    FadeOut(questions),
                    FadeOut(ownership),
                    FadeOut(servers),
                    FadeOut(production),
                    ReplacementTransform(stack_title, closing_title),
                    ReplacementTransform(self.patch, patch_final),
                ),
                AnimationGroup(
                    FadeIn(sql_final),
                    FadeIn(gate_a),
                    FadeIn(gate_b),
                    FadeIn(db_change),
                    FadeIn(deploy_change),
                    FadeIn(final_labels),
                ),
                LaggedStart(*[GrowArrow(arrow) for arrow in final_rails], lag_ratio=0.12),
                FadeIn(source_line),
            ),
            settle=1.6,
        )
