"""Generation-2 visual abstract for “ASI Is a Stack, Not a Model.”

This scene is driven by the measured 230.230-second narration receipt. It uses
one persistent delete-request world rather than paragraph cards.
"""

from __future__ import annotations

from manim import (
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Group,
    Indicate,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
    Write,
    linear,
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
    proof_boundary,
    residual_marker,
    text,
)


class AsiIsAStackNotAModelGeneration2(AsiScene):
    TARGET_DURATION = 230.230
    ENDS = [
        7.105, 14.660, 24.540, 33.195, 40.525, 48.280, 56.085,
        64.640, 72.520, 80.550, 88.605, 93.635, 102.090, 110.420,
        119.750, 128.430, 138.035, 146.015, 153.970, 162.850,
        172.205, 181.210, 190.315, 200.420, 211.300, 221.655,
        230.230,
    ]

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def play_beat(self, index: int, *animations, settle: float = 0.35) -> None:
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        run_time = max(0.05, remaining - min(settle, remaining * 0.25))
        if animations:
            self.play(*animations, run_time=run_time)
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 21, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def file_tile(self, label: str, *, color: str = BOUNDARY) -> VGroup:
        page = RoundedRectangle(
            width=0.72,
            height=0.88,
            corner_radius=0.06,
            stroke_color=color,
            stroke_width=2,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        fold = VGroup(
            Line(page.get_corner(UP + RIGHT) + LEFT * 0.18, page.get_corner(UP + RIGHT) + LEFT * 0.18 + UP * -0.18, color=color, stroke_width=2),
            Line(page.get_corner(UP + RIGHT) + LEFT * 0.18 + UP * -0.18, page.get_corner(UP + RIGHT) + UP * -0.18, color=color, stroke_width=2),
        )
        glyph = self.label(label, 14, color, "BOLD").move_to(page)
        return VGroup(page, fold, glyph)

    def box(self, heading: str, detail: str, color: str, width: float = 2.0) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=0.9,
            corner_radius=0.1,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        labels = VGroup(
            self.label(heading, 17, color, "BOLD"),
            self.label(detail, 13, MUTED),
        ).arrange(UP * -1, buff=0.06).move_to(shell)
        return VGroup(shell, labels)

    def stop_gate(self, label: str = "AUTHORITY") -> VGroup:
        posts = VGroup(
            Line(UP * 0.72, UP * -0.72, color=AUTHORITY, stroke_width=7),
            Line(UP * 0.72, UP * -0.72, color=AUTHORITY, stroke_width=7).shift(RIGHT * 0.45),
        )
        cross = Line(LEFT * 0.08, RIGHT * 0.53, color=AUTHORITY, stroke_width=5).shift(UP * 0.15)
        tag = self.label(label, 14, AUTHORITY, "BOLD").next_to(posts, UP, buff=0.1)
        return VGroup(posts, cross, tag)

    def request_capsule(self) -> VGroup:
        body = RoundedRectangle(
            width=2.1,
            height=0.82,
            corner_radius=0.4,
            stroke_color=ACCENT,
            stroke_width=3,
            fill_color="#163341",
            fill_opacity=1,
        )
        dot = Circle(radius=0.16, color=ACCENT, fill_color=ACCENT, fill_opacity=1).shift(LEFT * 0.72)
        label = self.label("DELETE 12", 18, INK, "BOLD").shift(RIGHT * 0.2)
        return VGroup(body, dot, label)

    def construct(self) -> None:
        # Beat 1 — the concrete file problem.
        self.files = VGroup(*[self.file_tile(chr(65 + i // 2)) for i in range(12)])
        self.files.arrange_in_grid(rows=3, cols=4, buff=(0.16, 0.16)).scale(0.82).shift(LEFT * 3.9 + UP * -0.2)
        duplicate_links = VGroup(*[
            Line(self.files[i].get_bottom(), self.files[i + 1].get_bottom(), color=ACCENT, stroke_width=2)
            for i in range(0, 12, 2)
        ])
        self.model = VGroup(
            Circle(radius=1.0, color=COPPER, stroke_width=4, fill_color=SURFACE, fill_opacity=1),
            Circle(radius=0.48, color=COPPER, stroke_width=2),
            self.label("MODEL", 22, COPPER, "BOLD"),
        ).shift(RIGHT * 2.0 + UP * 0.55)
        command_line = Line(self.model.get_left(), self.files.get_right(), color=COPPER, stroke_width=3)
        self.request = self.request_capsule().shift(RIGHT * 1.95 + UP * -1.55)
        question = self.label("SHOULD IT RUN?", 26, AUTHORITY, "BOLD").next_to(self.request, UP * -1, buff=0.35)
        # Begin on the concrete case immediately; avoid a logo or black pre-roll.
        self.add(self.files, self.model)
        self.play_beat(
            1,
            LaggedStart(*[Create(link) for link in duplicate_links], lag_ratio=0.12),
            Create(command_line),
            TransformFromCopy(self.model[1], self.request),
            Write(question),
        )

        # Beat 2 — correct output, missing authority.
        self.gate = self.stop_gate().shift(RIGHT * 4.45 + UP * -1.55)
        drive = RoundedRectangle(width=1.35, height=1.75, corner_radius=0.12, color=BOUNDARY, fill_color=SURFACE, fill_opacity=1).shift(RIGHT * 5.65 + UP * -1.55)
        drive_label = self.label("DRIVE", 18, MUTED, "BOLD").move_to(drive)
        authority_q = self.label("AUTHORITY?", 18, AUTHORITY, "BOLD").next_to(self.gate, UP * -1, buff=0.15)
        self.play_beat(
            2,
            FadeOut(question),
            FadeIn(self.gate),
            FadeIn(drive),
            FadeIn(drive_label),
            self.request.animate.move_to(self.gate.get_left() + LEFT * 0.75),
            Indicate(self.gate, color=AUTHORITY),
            FadeIn(authority_q),
        )

        # Beat 3 — reveal the governed system around the model.
        shell = RoundedRectangle(width=12.3, height=6.7, corner_radius=0.22, color=ACCENT, stroke_width=3, fill_opacity=0)
        shell_label = self.label("GOVERNED SYSTEM", 18, ACCENT, "BOLD").next_to(shell, UP, buff=0.08)
        self.play_beat(
            3,
            self.files.animate.scale(0.72).move_to(LEFT * 4.2 + UP * 0.75),
            self.model.animate.scale(0.72).move_to(ORIGIN),
            self.request.animate.scale(0.8).move_to(RIGHT * 2.35 + UP * -1.75),
            self.gate.animate.scale(0.8).move_to(RIGHT * 3.95 + UP * -1.75),
            drive.animate.scale(0.8).move_to(RIGHT * 5.25 + UP * -1.75),
            drive_label.animate.scale(0.8).move_to(RIGHT * 5.25 + UP * -1.75),
            FadeOut(command_line),
            FadeOut(authority_q),
            Create(shell),
            FadeIn(shell_label),
        )

        # Beat 4 — responsibility rails assemble around the same objects.
        duties = VGroup(
            self.box("CONTEXT", "permitted sources", BOUNDARY),
            self.box("VERIFY", "claims + residuals", EVIDENCE),
            self.box("GRANT", "scope + owner", AUTHORITY),
            self.box("EXECUTE", "narrow adapter", COPPER),
            self.box("OBSERVE", "independent state", EVIDENCE),
            self.box("RECOVER", "rollback / contain", ROLLBACK),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.55, 2.4)).scale(0.68).shift(RIGHT * 0.55 + UP * -0.05)
        rails = VGroup(*[
            DashedLine(self.model.get_center(), duty.get_center(), color=duty[0].get_color(), dash_length=0.12, stroke_width=2)
            for duty in duties
        ])
        self.duties = duties
        self.play_beat(
            4,
            LaggedStart(*[Create(rail) for rail in rails], lag_ratio=0.11),
            LaggedStart(*[FadeIn(duty, shift=UP * 0.12) for duty in duties], lag_ratio=0.1),
        )

        # Beat 5 — collapse into an opaque monolith.
        monolith = Circle(radius=2.0, color=BOUNDARY, stroke_width=5, fill_color=SURFACE, fill_opacity=1).move_to(ORIGIN)
        monolith_label = self.label("OPAQUE\nMONOLITH", 30, MUTED, "BOLD").move_to(monolith)
        disappearing = VGroup(shell, shell_label, duties, rails, self.files, self.model, self.gate, drive, drive_label, duplicate_links)
        self.play_beat(
            5,
            FadeOut(disappearing, scale=0.8),
            FadeIn(monolith, scale=1.15),
            Write(monolith_label),
            self.request.animate.move_to(LEFT * 2.65),
        )

        # Beat 6 — counterfeit authority stamps crack.
        false_seals = VGroup(
            self.box("PLAN", "permission", COPPER, 2.2),
            self.box("CONTEXT", "belief", BOUNDARY, 2.2),
            self.box("SCORE", "approval", EVIDENCE, 2.2),
        ).arrange(RIGHT, buff=0.35).shift(UP * -2.55)
        cracks = VGroup(*[
            Line(seal.get_corner(UP + LEFT), seal.get_corner(UP * -1 + RIGHT), color=ROLLBACK, stroke_width=5)
            for seal in false_seals
        ])
        self.play_beat(
            6,
            LaggedStart(*[TransformFromCopy(monolith, seal) for seal in false_seals], lag_ratio=0.12),
            LaggedStart(*[Create(crack) for crack in cracks], lag_ratio=0.18),
        )

        # Beat 7 — receipt and observation are different objects.
        receipt = self.box("RECEIPT", "12 changed", COPPER, 2.4).shift(LEFT * 1.55 + UP * -0.55)
        observer = VGroup(
            Circle(radius=0.62, color=EVIDENCE, stroke_width=4),
            Circle(radius=0.2, color=EVIDENCE, fill_color=EVIDENCE, fill_opacity=1),
            self.label("OBSERVE", 16, EVIDENCE, "BOLD").shift(UP * -0.92),
        ).shift(RIGHT * 1.7 + UP * -0.4)
        observer_count = self.label("? files", 20, EVIDENCE, "BOLD").next_to(observer, RIGHT, buff=0.25)
        self.play_beat(
            7,
            FadeOut(false_seals),
            FadeOut(cracks),
            TransformFromCopy(monolith, receipt),
            TransformFromCopy(monolith, observer),
            FadeIn(observer_count),
            FadeOut(monolith),
            FadeOut(monolith_label),
        )

        # Beat 8 — restore the typed request.
        self.request.generate_target()
        self.request.target.move_to(LEFT * 4.8 + UP * 1.9).scale(0.9)
        tabs = VGroup(
            self.box("OUTCOME", "remove duplicates", ACCENT, 2.25),
            self.box("CONSTRAINT", "selected files", BOUNDARY, 2.25),
            self.box("OWNER", "drive operator", AUTHORITY, 2.25),
            self.box("RISK", "reversible only", ROLLBACK, 2.25),
        ).arrange(RIGHT, buff=0.25).scale(0.82).shift(UP * 0.25)
        self.play_beat(
            8,
            FadeOut(receipt),
            FadeOut(observer),
            FadeOut(observer_count),
            FadeIn(tabs, lag_ratio=0.08),
            self.request.animate.move_to(LEFT * 4.8 + UP * 1.9).scale(0.9),
        )

        # Beat 9 — proposal branches remain behind the effect boundary.
        plan_origin = self.request.get_right() + RIGHT * 0.5
        plans = VGroup(
            self.box("PLAN A", "delete", COPPER, 1.8),
            self.box("PLAN B", "archive", COPPER, 1.8),
            self.box("PLAN C", "ask", COPPER, 1.8),
        ).arrange(UP * -1, buff=0.35).shift(LEFT * 0.8 + UP * -1.0)
        plan_arrows = VGroup(*[Arrow(plan_origin, plan.get_left(), buff=0.08, color=ACCENT, stroke_width=2.5) for plan in plans])
        effect_boundary = Line(UP * 1.35, UP * -2.15, color=ROLLBACK, stroke_width=6).shift(RIGHT * 1.05 + UP * -0.35)
        boundary_label = self.label("NO EFFECT", 15, ROLLBACK, "BOLD").next_to(effect_boundary, RIGHT, buff=0.12)
        self.play_beat(
            9,
            FadeOut(tabs),
            LaggedStart(*[GrowArrow(arrow) for arrow in plan_arrows], lag_ratio=0.12),
            LaggedStart(*[FadeIn(plan) for plan in plans], lag_ratio=0.12),
            Create(effect_boundary),
            FadeIn(boundary_label),
            Indicate(self.request, color=ACCENT),
        )

        # Beat 10 — source-bound context mount.
        context_bay = RoundedRectangle(width=3.4, height=2.1, corner_radius=0.12, color=BOUNDARY, fill_color=SURFACE, fill_opacity=0.6).shift(RIGHT * 3.6 + UP * 0.55)
        context_label = self.label("PERMITTED CONTEXT", 17, BOUNDARY, "BOLD").next_to(context_bay, UP, buff=0.08)
        mounted = VGroup(*[self.file_tile(label, color=BOUNDARY).scale(0.58) for label in ("A", "B", "C", "D")]).arrange(RIGHT, buff=0.12).move_to(context_bay)
        excluded = VGroup(*[self.file_tile(label, color=ROLLBACK).scale(0.5) for label in ("X", "Y")]).arrange(RIGHT, buff=0.1).next_to(context_bay, RIGHT, buff=0.35)
        provenance = VGroup(*[
            self.label(label, 14, BOUNDARY, "BOLD")
            for label in ("PROVENANCE", "FRESHNESS", "RIGHTS", "TAINT")
        ]).arrange(RIGHT, buff=0.28).next_to(context_bay, UP * -1, buff=0.16)
        self.play_beat(
            10,
            Succession(
                AnimationGroup(
                    FadeOut(plan_arrows),
                    FadeOut(plans[1]),
                    FadeOut(plans[2]),
                    FadeOut(effect_boundary),
                    FadeOut(boundary_label),
                    run_time=0.9,
                ),
                AnimationGroup(
                    Create(context_bay),
                    FadeIn(context_label),
                    LaggedStart(*[FadeIn(tile, shift=LEFT * 0.15) for tile in mounted], lag_ratio=0.12),
                    FadeIn(excluded),
                    FadeIn(provenance),
                    run_time=4.7,
                ),
                AnimationGroup(
                    context_bay.animate(rate_func=rate_functions.there_and_back).scale(1.035),
                    LaggedStart(*[Indicate(term, color=BOUNDARY) for term in provenance], lag_ratio=0.18),
                    run_time=1.6,
                ),
            ),
        )

        # Beat 11 — verifier keeps an owned residual.
        verifier_ring = Circle(radius=1.0, color=EVIDENCE, stroke_width=4).shift(LEFT * 0.4 + UP * -1.0)
        verifier_label = self.label("VERIFY", 18, EVIDENCE, "BOLD").move_to(verifier_ring)
        residual = residual_marker("UNRESOLVED").scale(0.8).next_to(verifier_ring, RIGHT, buff=0.35)
        selected_plan = plans[0]
        self.play_beat(
            11,
            selected_plan.animate.move_to(verifier_ring),
            Create(verifier_ring),
            FadeIn(verifier_label),
            TransformFromCopy(selected_plan, residual),
            Indicate(residual, color=RESIDUAL),
        )

        # Beat 12 — prediction pause at a closed gate.
        gate2 = self.stop_gate().scale(1.15).shift(RIGHT * 2.0 + UP * -1.0)
        prediction = self.label("CORRECT PLAN\nMAY EXECUTE?", 25, AUTHORITY, "BOLD").shift(RIGHT * 4.25 + UP * -1.0)
        self.play_beat(
            12,
            FadeOut(context_bay), FadeOut(context_label), FadeOut(mounted), FadeOut(excluded), FadeOut(provenance),
            FadeOut(effect_boundary),
            FadeOut(verifier_ring),
            FadeOut(verifier_label),
            FadeOut(residual),
            Create(gate2),
            selected_plan.animate.next_to(gate2, LEFT, buff=0.65),
            FadeIn(prediction),
            settle=1.5,
        )

        # Beat 13 — scoped key opens the gate.
        key_teeth = VGroup(*[
            self.box(label, detail, AUTHORITY, 1.48).scale(0.72)
            for label, detail in (("SCOPE", "files"), ("OWNER", "operator"), ("TIME", "current"), ("REVOKE", "clear"), ("EFFECT", "delete"))
        ]).arrange(RIGHT, buff=0.12).shift(UP * 1.1 + RIGHT * 0.8)
        key_line = Line(LEFT * 1.1, RIGHT * 1.1, color=AUTHORITY, stroke_width=7).shift(RIGHT * 2.0 + UP * -0.1)
        key_ring = Circle(radius=0.28, color=AUTHORITY, stroke_width=6).next_to(key_line, LEFT, buff=0)
        key = VGroup(key_line, key_ring)
        self.play_beat(
            13,
            FadeOut(prediction),
            LaggedStart(*[FadeIn(tooth, shift=UP * -0.15) for tooth in key_teeth], lag_ratio=0.12),
            Create(key),
            gate2[1].animate.rotate(-1.0, about_point=gate2[1].get_left()),
            Indicate(key, color=AUTHORITY),
        )

        # Beat 14 — adapter recheck and exact effect.
        adapter = self.box("ADAPTER", "grant recheck", COPPER, 2.2).shift(RIGHT * 3.45 + UP * -1.0)
        effect_files = VGroup(*[self.file_tile(str(i + 1), color=BOUNDARY).scale(0.52) for i in range(12)]).arrange_in_grid(rows=3, cols=4, buff=(0.1, 0.1)).shift(RIGHT * 5.4 + UP * -1.0)
        effect_token = self.request.copy().scale(0.72).move_to(selected_plan)
        self.play_beat(
            14,
            FadeOut(key_teeth), FadeOut(key),
            FadeIn(adapter),
            Indicate(adapter, color=COPPER),
            TransformFromCopy(self.request, effect_token),
            effect_token.animate.move_to(effect_files.get_left() + LEFT * 0.45),
            FadeIn(effect_files, lag_ratio=0.05),
            LaggedStart(*[tile[0].animate.set_fill(COPPER, opacity=0.28) for tile in effect_files], lag_ratio=0.05),
        )

        # Beat 15 — self-report and observation fork.
        receipt2 = self.box("RECEIPT", "12 changed", COPPER, 2.2).shift(RIGHT * 2.2 + UP * -2.75)
        lens = VGroup(Circle(radius=0.58, color=EVIDENCE, stroke_width=4), Circle(radius=0.18, color=EVIDENCE, fill_color=EVIDENCE, fill_opacity=1)).shift(RIGHT * 5.0 + UP * 1.05)
        lens_label = self.label("OBSERVE", 15, EVIDENCE, "BOLD").next_to(lens, UP * -1, buff=0.12)
        receipt_path = Arrow(effect_files.get_left(), receipt2.get_top(), buff=0.15, color=COPPER, stroke_width=3)
        observe_path = Arrow(effect_files.get_top(), lens.get_bottom(), buff=0.15, color=EVIDENCE, stroke_width=3)
        self.play_beat(
            15,
            FadeOut(effect_token),
            GrowArrow(receipt_path),
            TransformFromCopy(effect_files, receipt2),
            GrowArrow(observe_path),
            TransformFromCopy(effect_files, lens),
            FadeIn(lens_label),
        )

        # Beat 16 — contradictory observation becomes an owned residual.
        count_label = VGroup(
            self.label("12", 34, EVIDENCE, "BOLD"),
            self.label("FILES", 15, EVIDENCE, "BOLD"),
        ).arrange(RIGHT, buff=0.12).next_to(lens, RIGHT, buff=0.25)
        count_thirteen = VGroup(
            self.label("13", 40, RESIDUAL, "BOLD"),
            self.label("FILES", 15, RESIDUAL, "BOLD"),
        ).arrange(RIGHT, buff=0.12).move_to(count_label)
        residual2 = residual_marker("OWNER: REVIEW").scale(0.9).move_to(LEFT * 1.35 + UP * 1.7)
        extra_file = self.file_tile("13", color=RESIDUAL).scale(0.52).next_to(effect_files, UP * -1, buff=0.16)
        mismatch = DashedLine(receipt2.get_top(), residual2.get_bottom(), color=RESIDUAL, stroke_width=3)
        mismatch2 = DashedLine(count_label.get_left(), residual2.get_right(), color=RESIDUAL, stroke_width=3)
        anomaly_ring = Circle(radius=0.54, color=RESIDUAL, stroke_width=4).move_to(extra_file)
        residual_field = RoundedRectangle(
            width=6.5,
            height=5.35,
            corner_radius=0.28,
            stroke_color=RESIDUAL,
            stroke_width=3,
            fill_color=RESIDUAL,
            fill_opacity=0.055,
        ).move_to(RIGHT * 3.1 + UP * -0.35).set_z_index(-5)
        self.add(count_label)
        self.play_beat(
            16,
            Succession(
                AnimationGroup(
                    ReplacementTransform(count_label, count_thirteen),
                    TransformFromCopy(effect_files[-1], extra_file),
                    FadeIn(residual_field),
                    run_time=2.0,
                ),
                AnimationGroup(
                    Create(anomaly_ring),
                    Create(mismatch),
                    Create(mismatch2),
                    FadeIn(residual2, scale=0.82),
                    run_time=2.5,
                ),
                AnimationGroup(
                    Indicate(residual2, color=RESIDUAL),
                    Indicate(count_thirteen, color=RESIDUAL),
                    Indicate(extra_file, color=RESIDUAL),
                    Indicate(residual_field, color=RESIDUAL, scale_factor=1.03),
                    run_time=2.3,
                ),
            ),
        )

        # Beat 17 — exact rollback to recorded pre-state.
        prestate = self.box("PRE-STATE", "12 original pairs", ROLLBACK, 2.6).shift(LEFT * 4.45 + UP * -2.5)
        rollback_line = Arrow(effect_files.get_bottom(), prestate.get_right(), buff=0.15, color=ROLLBACK, stroke_width=5)
        quarantine = self.box("IRREVERSIBLE", "compensate / quarantine", RESIDUAL, 2.8).shift(LEFT * 1.25 + UP * -2.5)
        self.play_beat(
            17,
            Succession(
                AnimationGroup(
                    FadeIn(prestate),
                    GrowArrow(rollback_line),
                    FadeIn(quarantine),
                    run_time=1.8,
                ),
                AnimationGroup(
                    LaggedStart(*[tile[0].animate.set_fill(SURFACE, opacity=1) for tile in reversed(effect_files)], lag_ratio=0.05),
                    effect_files.animate(rate_func=rate_functions.there_and_back).shift(LEFT * 0.22),
                    extra_file.animate.move_to(quarantine).set_opacity(0),
                    FadeOut(anomaly_ring),
                    run_time=4.7,
                ),
                Indicate(prestate, color=ROLLBACK, run_time=1.2),
            ),
        )

        # Beat 18 — compress the trace into a persistent top rail.
        trace = VGroup(
            self.box("REQUEST", "typed", ACCENT, 1.45),
            self.box("PLAN", "proposal", COPPER, 1.45),
            self.box("CONTEXT", "mounted", BOUNDARY, 1.45),
            self.box("VERIFY", "residual", EVIDENCE, 1.45),
            self.box("GRANT", "scoped", AUTHORITY, 1.45),
            self.box("EFFECT", "bounded", COPPER, 1.45),
            self.box("OBSERVE", "independent", EVIDENCE, 1.45),
        ).arrange(RIGHT, buff=0.16).scale(0.72).move_to(UP * 0.85)
        trace_arrows = VGroup(*[Arrow(trace[i].get_right(), trace[i + 1].get_left(), buff=0.04, color=ACCENT, stroke_width=2) for i in range(len(trace) - 1)])
        trace_stops = VGroup(*[
            Line(UP * 0.26, UP * -0.26, color=ROLLBACK, stroke_width=4).move_to(arrow)
            for arrow in trace_arrows
        ])
        noninheritance_panel = RoundedRectangle(
            width=10.6,
            height=5.25,
            corner_radius=0.3,
            stroke_color=BOUNDARY,
            stroke_width=2.5,
            fill_color=SURFACE,
            fill_opacity=0.92,
        ).shift(UP * -0.35).set_z_index(-4)
        noninheritance_title = self.label("NONINHERITANCE", 24, ACCENT, "BOLD").move_to(UP * 2.25)
        trace_rule = self.label(
            "A SUCCESSFUL OBJECT DOES NOT INHERIT\nTHE NEXT LAYER'S POWERS",
            24,
            INK,
            "BOLD",
        ).move_to(UP * -1.1)
        trace_detail = self.label(
            "each handoff needs its own contract, evidence, and authority",
            17,
            MUTED,
        ).next_to(trace_rule, UP * -1, buff=0.22)
        visible_roots = []
        visible_ids = set()
        for mob in self.mobjects:
            if id(mob) not in visible_ids:
                visible_ids.add(id(mob))
                visible_roots.append(mob)
        old_world = Group(*visible_roots)
        self.play_beat(
            18,
            AnimationGroup(
                FadeOut(old_world, run_time=2.0),
                FadeIn(noninheritance_panel),
                FadeIn(noninheritance_title),
                LaggedStart(
                    LaggedStart(*[FadeIn(node) for node in trace], lag_ratio=0.08),
                    LaggedStart(*[GrowArrow(arrow) for arrow in trace_arrows], lag_ratio=0.08),
                    LaggedStart(*[Create(stop) for stop in trace_stops], lag_ratio=0.08),
                    FadeIn(trace_rule, shift=UP * 0.12),
                    FadeIn(trace_detail, shift=UP * 0.12),
                    lag_ratio=0.35,
                    run_time=6.6,
                ),
                lag_ratio=0.15,
            ),
        )

        # Beat 19 — first three noninheritance gates.
        pairs1 = [("CAPABILITY", "AUTHORITY"), ("CONTEXT", "BELIEF"), ("PLAN", "EFFECT")]
        rows1 = VGroup()
        for left, right in pairs1:
            l = self.label(left, 24, INK, "BOLD")
            a = Arrow(LEFT * 0.75, RIGHT * 0.75, color=BOUNDARY, stroke_width=3)
            stop = Line(UP * 0.32, UP * -0.32, color=ROLLBACK, stroke_width=6)
            r = self.label(right, 24, MUTED, "BOLD")
            rows1.add(VGroup(l, a, stop, r).arrange(RIGHT, buff=0.3))
        rows1.arrange(UP * -1, buff=0.5, aligned_edge=LEFT).shift(UP * -0.55)
        self.play_beat(
            19,
            Succession(
                AnimationGroup(
                    FadeOut(trace), FadeOut(trace_arrows), FadeOut(trace_stops),
                    FadeOut(trace_rule), FadeOut(trace_detail),
                    run_time=1.0,
                ),
                LaggedStart(
                    *[FadeIn(row, shift=RIGHT * 0.15) for row in rows1],
                    lag_ratio=0.18,
                    run_time=5.0,
                ),
            ),
        )

        # Beat 20 — second three gates reuse the same visual syntax.
        pairs2 = [("RECEIPT", "REALITY"), ("THEOREM", "ENFORCEMENT"), ("REPLACEMENT", "QUALIFICATION")]
        rows2 = VGroup()
        for left, right in pairs2:
            l = self.label(left, 24, INK, "BOLD")
            a = Arrow(LEFT * 0.75, RIGHT * 0.75, color=BOUNDARY, stroke_width=3)
            stop = Line(UP * 0.32, UP * -0.32, color=ROLLBACK, stroke_width=6)
            r = self.label(right, 24, MUTED, "BOLD")
            rows2.add(VGroup(l, a, stop, r).arrange(RIGHT, buff=0.3))
        rows2.arrange(UP * -1, buff=0.5, aligned_edge=LEFT).shift(UP * -0.55)
        self.play_beat(
            20,
            Succession(
                FadeOut(rows1, shift=LEFT * 0.18, run_time=1.0),
                LaggedStart(
                    *[FadeIn(row, shift=RIGHT * 0.15) for row in rows2],
                    lag_ratio=0.18,
                    run_time=5.5,
                ),
            ),
        )

        # Beat 21 — self-improvement proposal cannot self-certify.
        candidate = VGroup(
            RoundedRectangle(width=3.0, height=2.2, corner_radius=0.16, color=ACCENT, fill_color=SURFACE, fill_opacity=1, stroke_width=4),
            Circle(radius=0.55, color=COPPER, stroke_width=3),
            self.label("CANDIDATE", 22, ACCENT, "BOLD").shift(UP * -0.78),
        ).shift(LEFT * 1.6 + UP * -0.7)
        outside_keys = VGroup(self.box("APPROVE", "external", AUTHORITY, 2.1), self.box("CERTIFY", "external", EVIDENCE, 2.1)).arrange(UP * -1, buff=0.4).shift(RIGHT * 2.7 + UP * -0.7)
        separating_line = Line(UP * 1.25, UP * -2.0, color=BOUNDARY, stroke_width=3).shift(RIGHT * 0.55 + UP * -0.35)
        self_improvement_title = self.label("SELF-IMPROVEMENT CANNOT CERTIFY ITSELF", 24, ACCENT, "BOLD").move_to(noninheritance_title)
        self.play_beat(
            21,
            AnimationGroup(
                FadeOut(rows2, shift=LEFT * 0.15),
                Transform(noninheritance_title, self_improvement_title),
                noninheritance_panel.animate.set_stroke(ACCENT).set_fill(SURFACE, opacity=0.82),
                FadeIn(candidate, scale=0.85),
                Create(separating_line),
                LaggedStart(*[FadeIn(k) for k in outside_keys], lag_ratio=0.18),
                lag_ratio=0.08,
            ),
        )

        # Beat 22 — interfaces carry real costs.
        costs = VGroup(
            self.box("LATENCY", "+ time", ROLLBACK, 2.2),
            self.box("LOSS", "discarded signal", ROLLBACK, 2.2),
            self.box("ATTACK", "new surface", ROLLBACK, 2.2),
            self.box("BRITTLE", "rigid flow", ROLLBACK, 2.2),
        ).arrange(RIGHT, buff=0.25).scale(0.83).shift(UP * -2.45)
        late_panel = RoundedRectangle(
            width=12.1,
            height=6.55,
            corner_radius=0.3,
            stroke_color=BOUNDARY,
            stroke_width=1.5,
            fill_color=SURFACE,
            fill_opacity=0.92,
        ).set_z_index(-8)
        cost_heading = self.label("EXPLICIT INTERFACES HAVE REAL COSTS", 27, INK, "BOLD").move_to(UP * 2.35)
        # Keep the self-improvement candidate visible until the costs have
        # assembled. The objection therefore grows out of the mechanism it
        # qualifies instead of arriving across an empty crossfade.
        self.add(late_panel)
        self.bring_to_back(late_panel)
        self.play_beat(
            22,
            Succession(
                AnimationGroup(
                    FadeIn(cost_heading, shift=UP * 0.12),
                    FadeOut(noninheritance_title),
                    FadeOut(noninheritance_panel),
                    run_time=1.0,
                ),
                AnimationGroup(
                    candidate.animate.scale(0.78).move_to(LEFT * 2.0 + UP * 0.55),
                    outside_keys.animate.scale(0.78).move_to(RIGHT * 2.5 + UP * 0.55),
                    separating_line.animate.scale(0.78).move_to(ORIGIN + UP * 0.55),
                    run_time=1.5,
                ),
                AnimationGroup(
                    LaggedStart(*[FadeIn(cost, shift=UP * 0.25) for cost in costs], lag_ratio=0.14),
                    run_time=5.5,
                ),
                AnimationGroup(
                    candidate.animate.set_opacity(0.18),
                    outside_keys.animate.set_opacity(0.18),
                    separating_line.animate.set_opacity(0.18),
                    run_time=0.8,
                ),
            ),
        )

        # Beat 23 — matched architecture race, deliberately no winner.
        racers = VGroup(
            self.box("MONOLITH", "end to end", BOUNDARY, 2.5),
            self.box("WRAPPER", "light controls", ACCENT, 2.5),
            self.box("STACK", "explicit contracts", COPPER, 2.5),
        ).arrange(UP * -1, buff=0.45).shift(LEFT * 3.5 + UP * -0.75)
        tracks = VGroup(*[Line(LEFT * 1.6, RIGHT * 3.2, color=MUTED, stroke_width=3).move_to(racer).shift(RIGHT * 3.3) for racer in racers])
        finish = Line(UP * 2.0, UP * -2.0, color=AUTHORITY, stroke_width=4).shift(RIGHT * 5.25 + UP * -0.75)
        matched = self.label("SAME TASK • MODEL • TOOLS • CONTEXT • TUNING • COST", 18, MUTED, "BOLD").shift(UP * 2.25)
        race_panel = RoundedRectangle(
            width=11.4,
            height=5.2,
            corner_radius=0.28,
            stroke_color=BOUNDARY,
            stroke_width=2,
            fill_color=SURFACE,
            fill_opacity=0.78,
        ).shift(UP * -0.35).set_z_index(-5)
        self.play_beat(
            23,
            Succession(
                AnimationGroup(
                    FadeOut(costs),
                    FadeOut(trace),
                    FadeOut(trace_arrows),
                    FadeOut(cost_heading),
                    FadeOut(late_panel),
                    run_time=1.0,
                ),
                AnimationGroup(
                    FadeIn(race_panel),
                    FadeIn(matched),
                    LaggedStart(*[FadeIn(racer) for racer in racers], lag_ratio=0.12),
                    LaggedStart(*[Create(track) for track in tracks], lag_ratio=0.12),
                    Create(finish),
                    *[racer.animate.shift(RIGHT * 1.0) for racer in racers],
                    run_time=5.5,
                ),
            ),
        )

        # Beat 24 — joint metrics, no average laundering.
        metrics = VGroup(*[
            self.box(label, value, color, 1.85).scale(0.78)
            for label, value, color in (
                ("USEFUL", "completion", EVIDENCE), ("UNSAFE", "effects", ROLLBACK),
                ("REFUSAL", "false", AUTHORITY), ("RECOVERY", "success", EVIDENCE),
                ("LATENCY", "time", BOUNDARY), ("GOV COST", "total", COPPER),
            )
        ]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).shift(RIGHT * 2.25 + UP * -0.7)
        no_theater = self.label("NO SINGLE SCORE HIDES FAILURE", 20, ROLLBACK, "BOLD").to_edge(UP * -1, buff=0.35)
        self.play_beat(
            24,
            FadeOut(tracks), FadeOut(finish),
            racers.animate.scale(0.72).shift(LEFT * 0.4),
            LaggedStart(*[FadeIn(metric, shift=UP * 0.12) for metric in metrics], lag_ratio=0.09),
            FadeIn(no_theater),
        )

        # Beat 25 — explicit evidence ceiling.
        boundary = proof_boundary("CURRENT SUPPORT: ARGUMENT", "finite contracts + one local trace").scale(1.03)
        outside = VGroup(
            self.label("DEPLOYMENT", 18, MUTED, "BOLD"), self.label("SAFETY", 18, MUTED, "BOLD"),
            self.label("EFFICIENCY", 18, MUTED, "BOLD"), self.label("TRANSFER", 18, MUTED, "BOLD"),
            self.label("ASI", 18, MUTED, "BOLD"),
        ).arrange(RIGHT, buff=0.5).to_edge(UP * -1, buff=0.55)
        self.play_beat(
            25,
            Succession(
                AnimationGroup(
                    FadeOut(racers), FadeOut(metrics), FadeOut(no_theater), FadeOut(matched), FadeOut(race_panel),
                    run_time=1.0,
                ),
                AnimationGroup(
                    FadeIn(boundary, scale=0.9),
                    LaggedStart(*[FadeIn(item) for item in outside], lag_ratio=0.1),
                    run_time=6.0,
                ),
            ),
        )

        # Beat 26 — return to the opening object with the missing controls visible.
        payoff_files = VGroup(*[self.file_tile(chr(65 + i // 2)) for i in range(12)]).arrange_in_grid(rows=3, cols=4, buff=(0.14, 0.14)).scale(0.68).shift(LEFT * 4.25)
        payoff_model = self.model.copy().scale(0.72).move_to(LEFT * 0.9)
        payoff_request = self.request_capsule().scale(0.8).move_to(RIGHT * 1.15)
        payoff_gate = self.stop_gate().scale(0.75).move_to(RIGHT * 3.0)
        payoff_observer = VGroup(Circle(radius=0.45, color=EVIDENCE, stroke_width=3), Circle(radius=0.14, color=EVIDENCE, fill_color=EVIDENCE, fill_opacity=1)).move_to(RIGHT * 4.55 + UP * 1.1)
        payoff_residual = residual_marker("OWNED").scale(0.62).move_to(RIGHT * 4.55 + UP * -0.1)
        payoff_rollback = Arrow(RIGHT * 4.8 + UP * -1.5, LEFT * 4.0 + UP * -1.5, color=ROLLBACK, stroke_width=4)
        payoff_label = self.label("CAPABILITY INSIDE A GOVERNED SYSTEM", 25, ACCENT, "BOLD").to_edge(UP, buff=0.42)
        self.play_beat(
            26,
            Succession(
                AnimationGroup(FadeOut(boundary), FadeOut(outside), run_time=1.0),
                AnimationGroup(
                    LaggedStart(*[FadeIn(tile) for tile in payoff_files], lag_ratio=0.04),
                    FadeIn(payoff_model),
                    TransformFromCopy(payoff_model, payoff_request),
                    FadeIn(payoff_gate),
                    FadeIn(payoff_observer),
                    FadeIn(payoff_residual),
                    GrowArrow(payoff_rollback),
                    Write(payoff_label),
                    run_time=7.5,
                ),
            ),
        )

        # Beat 27 — the same request becomes the efficiency question.
        balance = VGroup(
            Line(LEFT * 2.2, RIGHT * 2.2, color=ACCENT, stroke_width=5),
            Line(ORIGIN, UP * -1.4, color=ACCENT, stroke_width=5),
            Circle(radius=0.12, color=ACCENT, fill_color=ACCENT, fill_opacity=1),
        ).shift(UP * 0.5)
        useful = self.box("USEFUL WORK", "completion + recovery", EVIDENCE, 3.0).shift(LEFT * 2.2 + UP * -1.0)
        cost = self.box("TOTAL COST", "compute + latency + governance", COPPER, 3.0).shift(RIGHT * 2.2 + UP * -1.0)
        next_title = self.label("NEXT: THE EFFICIENT ASI HYPOTHESIS", 28, INK, "BOLD").to_edge(UP, buff=0.5)
        live = self.label("corbensorenson.github.io/asi-stack-book", 18, ACCENT).to_edge(UP * -1, buff=0.4)
        balance_panel = RoundedRectangle(
            width=8.8,
            height=4.35,
            corner_radius=0.28,
            stroke_color=ACCENT,
            stroke_width=2,
            fill_color=SURFACE,
            fill_opacity=0.72,
        ).shift(UP * -0.25).set_z_index(-5)
        payoff_world = VGroup(payoff_files, payoff_model, payoff_request, payoff_gate, payoff_observer, payoff_residual, payoff_rollback, payoff_label)
        self.play_beat(
            27,
            Succession(
                FadeOut(payoff_world, run_time=1.0),
                AnimationGroup(
                    FadeIn(balance_panel),
                    Create(balance),
                    FadeIn(useful, shift=UP * 0.15),
                    FadeIn(cost, shift=UP * 0.15),
                    Write(next_title),
                    FadeIn(live),
                    run_time=7.0,
                ),
            ),
        )

        self.wait_until(self.TARGET_DURATION)
