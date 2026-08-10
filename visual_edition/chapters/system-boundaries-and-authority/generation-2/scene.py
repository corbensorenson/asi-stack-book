"""Generation-two animatic for ``System Boundaries and Authority``.

One refund instruction remains visually invariant while operation class and
grant lifecycle state determine whether it can cross an external-effect gate.
"""

from __future__ import annotations

from math import pi

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
    GrowFromCenter,
    Group,
    Indicate,
    LaggedStart,
    LEFT,
    Line,
    MoveAlongPath,
    Polygon,
    Rectangle,
    RegularPolygon,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Succession,
    Transform,
    TransformFromCopy,
    UP,
    VGroup,
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


class SystemBoundariesAuthorityGeneration2(AsiScene):
    TARGET_DURATION = 176.210
    ENDS = [
        12.981,
        23.425,
        36.822,
        48.373,
        62.320,
        77.950,
        91.657,
        103.400,
        114.117,
        126.250,
        135.422,
        145.834,
        160.341,
        176.210,
    ]

    def wait_until(self, target: float) -> None:
        remaining = target - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def beat(self, index: int, *animations, settle: float = 0.42) -> None:
        """Distribute one semantic construction across its narration window."""
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        run_time = max(0.05, remaining - min(settle, remaining * 0.24))
        if animations:
            self.play(LaggedStart(*animations, lag_ratio=0.22, run_time=run_time))
        self.wait_until(end)

    def staged_beat(
        self,
        index: int,
        setup: tuple,
        resolution: tuple,
        *,
        setup_ratio: float = 0.38,
        settle: float = 0.42,
    ) -> None:
        """Reserve the latter narration window for the decisive state change."""
        self.next_section(f"b{index:02d}")
        end = self.ENDS[index - 1]
        remaining = max(0.05, end - self.renderer.time)
        run_time = max(0.05, remaining - min(settle, remaining * 0.24))
        setup_time = max(0.05, run_time * setup_ratio)
        resolution_time = max(0.05, run_time - setup_time)
        if setup:
            self.play(LaggedStart(*setup, lag_ratio=0.18), run_time=setup_time)
        if resolution:
            self.play(LaggedStart(*resolution, lag_ratio=0.20), run_time=resolution_time)
        self.wait_until(end)

    @staticmethod
    def label(value: str, size: int = 20, color: str = INK, weight: str = "NORMAL"):
        return text(value, size=size, color=color, weight=weight)

    def title(self, value: str, color: str = INK) -> VGroup:
        words = self.label(value, 24, color, "BOLD").shift(UP * 3.38)
        rule = Line(LEFT * 2.0, RIGHT * 2.0, color=color, stroke_width=2).next_to(words, DOWN, buff=0.10)
        return VGroup(words, rule)

    def ticket(self, *, compact: bool = False) -> VGroup:
        width, height = (2.18, 1.34) if compact else (2.72, 2.08)
        page = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            color=BOUNDARY,
            stroke_width=2.8,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        identity = Circle(radius=0.075, color=ACCENT, fill_color=ACCENT, fill_opacity=1)
        identity.move_to(page.get_corner(UP + LEFT) + RIGHT * 0.22 + DOWN * 0.20)
        heading = self.label("REFUND", 18 if compact else 22, ACCENT, "BOLD")
        heading.move_to(page.get_center() + UP * (0.34 if compact else 0.69))
        amount = self.label("$240", 18 if compact else 23, INK, "BOLD")
        amount.move_to(page.get_center() + DOWN * (0.28 if compact else 0.50))
        account = self.label("ACCOUNT 47", 11 if compact else 14, MUTED, "BOLD")
        account.move_to(page.get_center() + (UP * 0.05 if compact else UP * 0.12))
        if compact:
            return VGroup(page, identity, heading, account, amount)
        checks = VGroup(
            self.check("", ACCENT),
            self.check("", ACCENT),
            self.check("", ACCENT),
        ).arrange(RIGHT, buff=0.28).move_to(page.get_center() + DOWN * 0.72)
        check_label = self.label("ACCOUNT / AMOUNT / COMMAND", 8, ACCENT, "BOLD")
        check_label.move_to(page.get_center() + DOWN * 0.97)
        return VGroup(page, identity, heading, account, amount, checks, check_label)

    def check(self, value: str, color: str) -> VGroup:
        ring = Circle(radius=0.16, color=color, stroke_width=2.2)
        tick = VGroup(
            Line(LEFT * 0.07, DOWN * 0.07, color=color, stroke_width=3),
            Line(DOWN * 0.07, RIGHT * 0.10 + UP * 0.10, color=color, stroke_width=3),
        ).move_to(ring)
        if not value:
            return VGroup(ring, tick)
        tag = self.label(value, 9, color, "BOLD").next_to(ring, DOWN, buff=0.06)
        return VGroup(ring, tick, tag)

    def bank_gate(self, *, open_gate: bool = False, color: str = AUTHORITY) -> VGroup:
        posts = VGroup(
            Line(LEFT * 0.55 + UP * 1.10, LEFT * 0.55 + DOWN * 1.10, color=BOUNDARY, stroke_width=5),
            Line(RIGHT * 0.55 + UP * 1.10, RIGHT * 0.55 + DOWN * 1.10, color=BOUNDARY, stroke_width=5),
        )
        crossbar = Line(LEFT * 0.55 + UP * 0.88, RIGHT * 0.55 + UP * 0.88, color=BOUNDARY, stroke_width=4)
        gate = Line(LEFT * 0.46 + DOWN * 0.38, RIGHT * 0.46 + DOWN * 0.38, color=color, stroke_width=7)
        if open_gate:
            gate.rotate(pi / 2, about_point=gate.get_left())
        aperture_shape = RegularPolygon(4, radius=0.34, color=color, stroke_width=3).rotate(pi / 4)
        aperture_shape.move_to(UP * 0.30)
        name = self.label("REFUND", 12, color, "BOLD").next_to(posts, DOWN, buff=0.08)
        return VGroup(posts, crossbar, gate, aperture_shape, name)

    def bank(self, *, amount: str = "$0") -> VGroup:
        shell = Circle(radius=1.06, color=BOUNDARY, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        roof = Polygon(LEFT * 0.72 + UP * 0.34, UP * 0.82, RIGHT * 0.72 + UP * 0.34, color=BOUNDARY, stroke_width=3)
        columns = VGroup(*[
            Line(UP * 0.24 + RIGHT * x, DOWN * 0.46 + RIGHT * x, color=BOUNDARY, stroke_width=3)
            for x in (-0.46, 0, 0.46)
        ])
        balance = self.label(amount, 17, EVIDENCE if amount != "$0" else MUTED, "BOLD").move_to(DOWN * 0.72)
        return VGroup(shell, roof, columns, balance)

    def state_chip(
        self,
        value: str,
        color: str,
        width: float = 1.54,
        *,
        font_size: int = 11,
        height: float = 0.46,
    ) -> VGroup:
        shell = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.07,
            color=color,
            stroke_width=2.2,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        label = self.label(value, font_size, color, "BOLD").move_to(shell)
        return VGroup(shell, label)

    def sleeve(self, *, state: str = "UNBOUND", uses: str = "-", color: str = AUTHORITY) -> VGroup:
        shell = RoundedRectangle(
            width=3.18,
            height=2.46,
            corner_radius=0.15,
            color=color,
            stroke_width=3,
            fill_color=BACKGROUND,
            fill_opacity=0.20,
        )
        state_tag = self.state_chip(
            state, color, 1.62, font_size=14, height=0.50
        ).move_to(shell.get_top() + DOWN * 0.27)
        use_label = "1 USE" if uses == "1" else f"{uses} USES"
        use_tag = self.state_chip(
            use_label, color, 1.22, font_size=13, height=0.48
        ).move_to(shell.get_bottom() + UP * 0.27)
        return VGroup(shell, state_tag, use_tag)

    def field(self, name: str, color: str = AUTHORITY) -> VGroup:
        notch = RoundedRectangle(width=1.12, height=0.38, corner_radius=0.05, color=color, stroke_width=2)
        tag = self.label(name, 9, color, "BOLD").move_to(notch)
        return VGroup(notch, tag)

    def key(self, kind: str, color: str) -> VGroup:
        if kind == "READ":
            head = Circle(radius=0.36, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1)
        else:
            head = RegularPolygon(4, radius=0.47, color=color, stroke_width=3, fill_color=SURFACE, fill_opacity=1).rotate(pi / 4)
        shaft = Line(RIGHT * 0.28, RIGHT * 1.33, color=color, stroke_width=6)
        tooth_a = Line(RIGHT * 0.94, RIGHT * 0.94 + DOWN * 0.30, color=color, stroke_width=5)
        tooth_b = Line(RIGHT * 1.22, RIGHT * 1.22 + DOWN * 0.22, color=color, stroke_width=5)
        label = self.label(kind, 11, color, "BOLD").move_to(head)
        return VGroup(head, shaft, tooth_a, tooth_b, label)

    def receipt(self, kind: str, detail: str, color: str) -> VGroup:
        if kind == "REQUEST":
            shell = Rectangle(width=1.82, height=0.72, color=color, stroke_width=2.2, fill_color=SURFACE, fill_opacity=1)
        elif kind == "EFFECT":
            shell = RoundedRectangle(width=1.82, height=0.72, corner_radius=0.16, color=color, stroke_width=2.2, fill_color=SURFACE, fill_opacity=1)
        elif kind == "OBSERVE":
            shell = RegularPolygon(6, radius=0.66, color=color, stroke_width=2.2, fill_color=SURFACE, fill_opacity=1).stretch(1.45, 0)
        else:
            shell = Polygon(
                LEFT * 0.92 + UP * 0.36,
                RIGHT * 0.72 + UP * 0.36,
                RIGHT * 0.92,
                RIGHT * 0.72 + DOWN * 0.36,
                LEFT * 0.92 + DOWN * 0.36,
                color=color,
                stroke_width=2.2,
                fill_color=SURFACE,
                fill_opacity=1,
            )
        title = self.label(kind, 11, color, "BOLD").move_to(shell.get_center() + UP * 0.11)
        note = self.label(detail, 9, MUTED, "BOLD").move_to(shell.get_center() + DOWN * 0.15)
        return VGroup(shell, title, note)

    def proof_socket(
        self,
        value: str,
        color: str = RESIDUAL,
        *,
        width: float = 2.10,
        font_size: int = 11,
    ) -> VGroup:
        socket = RoundedRectangle(width=width, height=0.58, corner_radius=0.08, color=color, stroke_width=2.3)
        label = self.label(value, font_size, color, "BOLD").move_to(socket)
        return VGroup(socket, label)

    def focus_lens(self, target, color: str) -> RoundedRectangle:
        lens = RoundedRectangle(
            corner_radius=0.12,
            color=color,
            stroke_width=4.5,
            fill_color=color,
            fill_opacity=0.20,
        )
        lens.surround(target, buff=0.18)
        return lens

    def clear(self):
        return FadeOut(self.transients())

    def transients(self) -> Group:
        """Return scene content while preserving the continuous workbench."""
        return Group(*[mob for mob in self.mobjects if mob is not self.workbench])

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.workbench = RoundedRectangle(
            width=13.55,
            height=6.95,
            corner_radius=0.18,
            color=BOUNDARY,
            stroke_width=1.4,
            stroke_opacity=0.34,
            fill_color=SURFACE,
            fill_opacity=1,
        )
        bench_rule = Line(
            LEFT * 6.35 + DOWN * 2.86,
            RIGHT * 6.35 + DOWN * 2.86,
            color=BOUNDARY,
            stroke_width=1.2,
            stroke_opacity=0.30,
        )
        self.workbench.add(bench_rule)
        self.add(self.workbench)

        # b01: correctness is complete before authority appears.
        ticket = self.ticket().shift(LEFT * 4.65 + UP * 0.58)
        gate = self.bank_gate().shift(RIGHT * 0.55 + UP * 0.58)
        bank = self.bank().shift(RIGHT * 4.55 + UP * 0.58)
        path = DashedLine(ticket.get_right(), gate.get_left(), color=ACCENT, dash_length=0.13)
        heading = self.title("SHOULD THE BANK EXECUTE IT?", ROLLBACK)
        self.beat(
            1,
            FadeIn(ticket, shift=RIGHT * 0.20),
            Create(path),
            Create(gate),
            FadeIn(bank),
            Write(heading),
            Succession(
                Indicate(ticket, color=ACCENT, scale_factor=1.04),
                Indicate(gate, color=ROLLBACK, scale_factor=1.06),
                Indicate(bank, color=INK, scale_factor=1.04),
            ),
            settle=2.71,
        )

        # b02: CAN and MAY become separate questions in the same workbench.
        can = self.state_chip("CAN: COMPLETE", ACCENT, 2.05).shift(LEFT * 4.65 + UP * 2.45)
        may = self.state_chip("MAY: CLOSED", AUTHORITY, 1.88).shift(RIGHT * 0.55 + UP * 2.45)
        divider = DashedLine(UP * 2.72, DOWN * 0.76, color=BOUNDARY, dash_length=0.12).shift(LEFT * 1.80)
        not_yet = self.label("NOT YET", 24, ROLLBACK, "BOLD").move_to(LEFT * 1.0 + UP * 1.45)
        can_focus = self.focus_lens(ticket, ACCENT)
        may_focus = self.focus_lens(gate, AUTHORITY)
        target_focus = self.focus_lens(bank, AUTHORITY)
        self.beat(
            2,
            FadeOut(heading),
            FadeIn(can, shift=DOWN * 0.12),
            FadeIn(may, shift=DOWN * 0.12),
            Create(divider),
            Write(not_yet),
            Indicate(gate[2], color=AUTHORITY),
            Succession(
                FadeIn(can_focus),
                Transform(can_focus, may_focus),
                Transform(can_focus, target_focus),
                FadeOut(can_focus),
            ),
            settle=0.55,
        )

        # b03: authority is visible state around the unchanged ticket.
        old = self.transients()
        compact_ticket = self.ticket(compact=True).shift(LEFT * 3.72 + UP * 0.58)
        sleeve = self.sleeve().move_to(compact_ticket)
        fields = VGroup(
            self.state_chip("REQUESTER -> EFFECT", AUTHORITY, 2.54, font_size=13, height=0.58),
            self.state_chip("TARGET", AUTHORITY, 1.54, font_size=13, height=0.58),
            self.state_chip("LIMIT + DEADLINE", AUTHORITY, 2.54, font_size=13, height=0.58),
            self.state_chip("RECEIPTS", AUTHORITY, 1.54, font_size=13, height=0.58),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.22, 0.24))
        fields.move_to(RIGHT * 0.42 + UP * 0.62)
        confidence = self.state_chip(
            "CONFIDENCE != AUTHORITY", ACCENT, 3.10, font_size=13, height=0.58
        ).shift(RIGHT * 3.55 + UP * 2.32)
        open_slot = self.proof_socket(
            "MISSING FIELD", ROLLBACK, width=2.28, font_size=13
        ).shift(RIGHT * 3.72 + UP * 0.58)
        connector = DashedLine(fields.get_right(), open_slot.get_left(), color=AUTHORITY, dash_length=0.12)
        envelope_focus = self.focus_lens(VGroup(compact_ticket, sleeve), AUTHORITY)
        fields_focus = self.focus_lens(fields, AUTHORITY)
        missing_focus = self.focus_lens(open_slot, ROLLBACK)
        confidence_focus = self.focus_lens(confidence, ACCENT)
        self.beat(
            3,
            FadeOut(old),
            FadeIn(compact_ticket),
            Create(sleeve),
            LaggedStart(*[FadeIn(field) for field in fields], lag_ratio=0.12),
            Create(connector),
            FadeIn(open_slot),
            FadeIn(confidence),
            Succession(
                FadeIn(envelope_focus),
                Transform(envelope_focus, fields_focus),
                Transform(envelope_focus, missing_focus),
                Transform(envelope_focus, confidence_focus),
                FadeOut(envelope_focus),
            ),
            settle=0.72,
        )

        # b04: READ reaches the right account and the wrong operation socket.
        old = self.transients()
        ticket_read = self.ticket(compact=True).shift(LEFT * 4.35 + UP * 0.62)
        sleeve_read = self.sleeve(state="READ", uses="-", color=ACCENT).move_to(ticket_read)
        read_key = self.key("READ", ACCENT).scale(0.82).shift(LEFT * 1.35 + UP * 0.42)
        gate_read = self.bank_gate().shift(RIGHT * 1.38 + UP * 0.62)
        account = self.bank(amount="VISIBLE").scale(0.84).shift(RIGHT * 4.65 + UP * 0.62)
        account_line = DashedLine(ticket_read.get_right(), account.get_left(), color=ACCENT, dash_length=0.14)
        mismatch = self.state_chip("NO FIT", ROLLBACK, 1.18).shift(RIGHT * 1.38 + UP * 2.36)
        read_focus = self.focus_lens(VGroup(ticket_read, sleeve_read), ACCENT)
        key_focus = self.focus_lens(read_key, ACCENT)
        gate_focus = self.focus_lens(VGroup(gate_read, mismatch), ROLLBACK)
        self.staged_beat(
            4,
            (
                FadeOut(old),
                FadeIn(ticket_read),
                Create(sleeve_read),
                Create(account_line),
                FadeIn(account),
                FadeIn(gate_read),
            ),
            (
                Succession(
                    FadeIn(read_key),
                    AnimationGroup(
                        read_key.animate.move_to(gate_read[3].get_center() + LEFT * 1.08),
                        FadeIn(mismatch),
                        FadeIn(read_focus),
                        lag_ratio=0,
                    ),
                    AnimationGroup(
                        Circumscribe(gate_read[3], color=ROLLBACK),
                        Transform(read_focus, key_focus),
                        lag_ratio=0,
                    ),
                    Transform(read_focus, gate_focus),
                    FadeOut(read_focus),
                ),
            ),
            setup_ratio=0.36,
            settle=0.82,
        )

        # b05: denial is an inspectable successful outcome.
        rail = Line(LEFT * 4.85 + UP * 2.18, RIGHT * 4.85 + UP * 2.18, color=BOUNDARY, stroke_width=2)
        denial = self.receipt("DENIED", "READ != REFUND", ROLLBACK).shift(RIGHT * 3.45 + UP * 2.18)
        cause = ArcBetweenPoints(gate_read[3].get_top(), denial.get_bottom(), angle=-0.35, color=ROLLBACK)
        refusal = self.label("SUCCESSFUL REFUSAL", 23, ROLLBACK, "BOLD").shift(LEFT * 1.45 + UP * 2.82)
        stop_focus = self.focus_lens(gate_read, ROLLBACK)
        denial_focus = self.focus_lens(denial, ROLLBACK)
        refusal_focus = self.focus_lens(refusal, ROLLBACK)
        self.beat(
            5,
            AnimationGroup(
                FadeOut(mismatch),
                TransformFromCopy(gate_read[3], denial),
                Create(cause),
                lag_ratio=0,
            ),
            Succession(
                FadeIn(stop_focus),
                Transform(stop_focus, denial_focus),
                Transform(stop_focus, refusal_focus),
                FadeOut(stop_focus),
            ),
            Create(rail),
            Write(refusal),
            Indicate(gate_read[2], color=ROLLBACK),
            settle=0.76,
        )

        # b06: a narrow one-shot refund key is assembled around fixed command bytes.
        old = self.transients()
        ticket_active = self.ticket(compact=True).shift(LEFT * 4.45 + UP * 0.62)
        sleeve_active = self.sleeve(state="ACTIVE", uses="1", color=AUTHORITY).move_to(ticket_active)
        refund_key = self.key("REFUND", AUTHORITY).scale(0.86).shift(LEFT * 0.60 + UP * 0.44)
        gate_active = self.bank_gate().shift(RIGHT * 2.08 + UP * 0.62)
        key_teeth = VGroup(
            self.state_chip("USER 12 -> REFUND", AUTHORITY, 2.46, font_size=13, height=0.58),
            self.state_chip("ACCOUNT 47", AUTHORITY, 1.74, font_size=13, height=0.58),
            self.state_chip("<= $240 | 1 USE | 2:05", AUTHORITY, 2.88, font_size=13, height=0.58),
            self.state_chip("EFFECT + OBSERVE", AUTHORITY, 2.20, font_size=13, height=0.58),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.18, 0.20)).shift(RIGHT * 0.90 + UP * 2.22)
        grant_focus = self.focus_lens(key_teeth, AUTHORITY)
        refund_focus = self.focus_lens(refund_key, AUTHORITY)
        dispatch_focus = self.focus_lens(gate_active, AUTHORITY)
        self.beat(
            6,
            FadeOut(old),
            FadeIn(ticket_active),
            Create(sleeve_active),
            LaggedStart(*[FadeIn(chip, shift=DOWN * 0.10) for chip in key_teeth], lag_ratio=0.12),
            Create(gate_active),
            Succession(
                FadeIn(refund_key),
                refund_key.animate.move_to(gate_active[3].get_center() + LEFT * 0.98),
                Indicate(sleeve_active[1], color=AUTHORITY),
            ),
            Succession(
                FadeIn(grant_focus),
                Transform(grant_focus, refund_focus),
                Transform(grant_focus, dispatch_focus),
                FadeOut(grant_focus),
            ),
            settle=0.92,
        )

        # b07: dispatch consumes the use and produces distinct effect/observation paths.
        old = self.transients()
        gate_open = self.bank_gate(open_gate=True, color=EVIDENCE).shift(RIGHT * 0.40 + UP * 0.56)
        trace_ticket = self.ticket(compact=True).scale(0.84).shift(LEFT * 4.70 + UP * 0.56)
        trace_sleeve = self.sleeve(state="ACTIVE", uses="1", color=AUTHORITY).scale(0.84).move_to(trace_ticket)
        trace = VGroup(trace_ticket, trace_sleeve)
        spent_ticket = self.ticket(compact=True).scale(0.84).shift(RIGHT * 2.70 + UP * 0.56)
        spent_sleeve = self.sleeve(state="CONSUMED", uses="0", color=ROLLBACK).scale(0.84).move_to(spent_ticket)
        spent_trace = VGroup(spent_ticket, spent_sleeve)
        path_cross = Line(trace.get_center(), spent_trace.get_center(), color=EVIDENCE)
        bank_changed = self.bank(amount="-$240").scale(0.82).shift(RIGHT * 5.45 + UP * 0.56)
        counter_zero = self.state_chip("1 -> 0", ROLLBACK, 1.28).shift(LEFT * 1.65 + UP * 2.50)
        effect = self.receipt("EFFECT", "REFUND RAN", EVIDENCE).shift(RIGHT * 1.00 + UP * 2.50)
        observe = self.receipt("OBSERVE", "DELTA -$240", ACCENT).shift(RIGHT * 3.65 + UP * 2.50)
        observer_line = DashedLine(observe.get_bottom(), bank_changed.get_top(), color=ACCENT, dash_length=0.12)
        dispatch_focus = self.focus_lens(trace, AUTHORITY)
        effect_focus = self.focus_lens(effect, EVIDENCE)
        observe_focus = self.focus_lens(VGroup(observe, bank_changed), ACCENT)
        self.beat(
            7,
            FadeOut(old),
            Create(gate_open),
            Create(path_cross),
            FadeIn(bank_changed),
            Succession(
                FadeIn(trace),
                MoveAlongPath(trace, path_cross),
                AnimationGroup(FadeOut(trace), FadeIn(spent_trace), lag_ratio=0),
            ),
            FadeIn(counter_zero),
            FadeIn(effect),
            Create(observer_line),
            FadeIn(observe),
            Succession(
                FadeIn(dispatch_focus),
                Transform(dispatch_focus, effect_focus),
                Transform(dispatch_focus, observe_focus),
                FadeOut(dispatch_focus),
            ),
            settle=0.88,
        )

        # b08: custody records answer three different questions.
        old = self.transients()
        request = self.receipt("REQUEST", "REFUND $240", ACCENT).shift(LEFT * 3.40 + UP * 0.76)
        effect_2 = self.receipt("EFFECT", "ADAPTER REPORT", EVIDENCE).shift(UP * 0.76)
        observe_2 = self.receipt("OBSERVE", "ACCOUNT DELTA", AUTHORITY).shift(RIGHT * 3.40 + UP * 0.76)
        custody_rail = Line(LEFT * 4.70 + UP * 2.28, RIGHT * 4.70 + UP * 2.28, color=BOUNDARY, stroke_width=2.2)
        source_marks = VGroup(
            self.state_chip("INSTRUCTION", ACCENT, 1.58).shift(LEFT * 3.40 + UP * 2.28),
            self.state_chip("ADAPTER", EVIDENCE, 1.34).shift(UP * 2.28),
            self.state_chip("OTHER PATH", AUTHORITY, 1.55).shift(RIGHT * 3.40 + UP * 2.28),
        )
        links = VGroup(
            DashedLine(source_marks[0].get_bottom(), request.get_top(), color=ACCENT, dash_length=0.10),
            DashedLine(source_marks[1].get_bottom(), effect_2.get_top(), color=EVIDENCE, dash_length=0.10),
            DashedLine(source_marks[2].get_bottom(), observe_2.get_top(), color=AUTHORITY, dash_length=0.10),
        )
        separate = self.label("SEPARATE CLAIMS", 25, INK, "BOLD").shift(DOWN * 0.58)
        self.beat(
            8,
            FadeOut(old),
            Create(custody_rail),
            LaggedStart(*[FadeIn(mark) for mark in source_marks], lag_ratio=0.16),
            LaggedStart(FadeIn(request), FadeIn(effect_2), FadeIn(observe_2), lag_ratio=0.22),
            LaggedStart(*[Create(link) for link in links], lag_ratio=0.18),
            Write(separate),
            settle=0.76,
        )

        # b09: identical bytes meet consumed authority state.
        old = self.transients()
        first_ticket = self.ticket(compact=True).scale(0.78).shift(LEFT * 4.55 + UP * 1.52)
        first_sleeve = self.sleeve(state="ACTIVE", uses="1", color=AUTHORITY).scale(0.78).move_to(first_ticket)
        replay_ticket = first_ticket.copy().shift(DOWN * 1.90)
        replay_sleeve = self.sleeve(state="CONSUMED", uses="0", color=ROLLBACK).scale(0.78).move_to(replay_ticket)
        gate_pair = VGroup(
            self.bank_gate(open_gate=True, color=EVIDENCE).scale(0.82).shift(RIGHT * 1.42 + UP * 1.52),
            self.bank_gate(open_gate=False, color=ROLLBACK).scale(0.82).shift(RIGHT * 1.42 + DOWN * 0.38),
        )
        identical = self.state_chip("IDENTICAL BYTES", ACCENT, 1.92).shift(LEFT * 4.55 + UP * 2.74)
        acted = self.receipt("ACTED", "ACTIVE 1", EVIDENCE).shift(RIGHT * 4.20 + UP * 1.52)
        refused = self.receipt("REFUSED", "CONSUMED 0", ROLLBACK).shift(RIGHT * 4.20 + DOWN * 0.38)
        top_path = Arrow(first_ticket.get_right(), gate_pair[0].get_left(), color=EVIDENCE, buff=0.14, stroke_width=3)
        bottom_path = Arrow(replay_ticket.get_right(), gate_pair[1].get_left(), color=ROLLBACK, buff=0.14, stroke_width=3)
        self.beat(
            9,
            AnimationGroup(
                FadeOut(old),
                FadeIn(first_ticket),
                Create(first_sleeve),
                lag_ratio=0,
            ),
            Succession(
                TransformFromCopy(first_ticket, replay_ticket),
                Create(replay_sleeve),
            ),
            FadeIn(identical),
            GrowArrow(top_path),
            GrowArrow(bottom_path),
            FadeIn(gate_pair),
            FadeIn(acted),
            FadeIn(refused),
            settle=0.92,
        )

        # b10: lifecycle changes close MAY while CAN remains stable.
        old = self.transients()
        command = self.ticket(compact=True).scale(0.52).shift(LEFT * 5.42 + UP * 2.42)
        command_label = self.state_chip(
            "IDENTICAL COMMAND", ACCENT, 2.08, font_size=13, height=0.54
        ).next_to(command, RIGHT, buff=0.18)
        can_line = Line(LEFT * 5.82 + DOWN * 1.34, RIGHT * 5.82 + DOWN * 1.34, color=ACCENT, stroke_width=5)
        can_tag = self.state_chip(
            "CAN UNCHANGED", ACCENT, 2.16, font_size=14, height=0.56
        ).shift(LEFT * 4.48 + DOWN * 1.34)
        state_names = [
            ("CONSUMED", "0", "NO USE REMAINS", -3.80),
            ("EXPIRED", "1", "CLOCK > 2:05", 0.0),
            ("REVOKED", "1", "BEFORE DISPATCH", 3.80),
        ]
        states = VGroup(*[
            VGroup(
                self.sleeve(state=name, uses=uses, color=ROLLBACK).scale(0.70).move_to(RIGHT * (x - 0.48) + UP * 0.78),
                self.bank_gate(color=ROLLBACK).scale(0.60).move_to(RIGHT * (x + 1.08) + UP * 0.78),
                self.label(detail, 14, MUTED, "BOLD").move_to(RIGHT * x + DOWN * 0.47),
            )
            for name, uses, detail, x in state_names
        ])
        self.beat(
            10,
            FadeOut(old),
            FadeIn(command),
            FadeIn(command_label),
            Create(can_line),
            FadeIn(can_tag),
            LaggedStart(*[FadeIn(state, shift=DOWN * 0.12) for state in states], lag_ratio=0.24),
            LaggedStart(*[Indicate(state[1][2], color=ROLLBACK) for state in states], lag_ratio=0.26),
            settle=0.86,
        )

        # b11: stronger capability cannot move the fixed authority ceiling.
        old = self.transients()
        can_rail = Line(LEFT * 4.70 + DOWN * 0.20, RIGHT * 1.25 + DOWN * 0.20, color=ACCENT, stroke_width=8)
        extension = Line(RIGHT * 1.25 + DOWN * 0.20, RIGHT * 4.70 + DOWN * 0.20, color=ACCENT, stroke_width=8)
        can_label = self.label("CAN", 28, ACCENT, "BOLD").next_to(can_rail, LEFT, buff=0.18)
        may_ceiling = Line(LEFT * 4.70 + UP * 1.62, RIGHT * 4.70 + UP * 1.62, color=AUTHORITY, stroke_width=6)
        may_gate = self.bank_gate(color=AUTHORITY).scale(0.70).shift(RIGHT * 1.60 + UP * 1.62)
        ceiling_label = self.label("MAY: CALLER CEILING", 22, AUTHORITY, "BOLD").shift(LEFT * 2.90 + UP * 2.18)
        stronger = self.state_chip("STRONGER MODEL", ACCENT, 2.02).shift(RIGHT * 3.50 + DOWN * 0.82)
        delta = DashedLine(RIGHT * 3.50 + DOWN * 0.10, RIGHT * 3.50 + UP * 1.52, color=RESIDUAL, dash_length=0.12)
        dead = self.state_chip("DEAD GRANT", ROLLBACK, 1.54).shift(RIGHT * 3.50 + UP * 2.30)
        self.beat(
            11,
            FadeOut(old),
            Create(can_rail),
            FadeIn(can_label),
            Create(may_ceiling),
            FadeIn(ceiling_label),
            FadeIn(may_gate),
            Create(extension),
            FadeIn(stronger),
            Create(delta),
            FadeIn(dead),
            Indicate(may_ceiling, color=AUTHORITY),
            settle=0.82,
        )

        # b12: the finite Lean claim stays inside its encoded boundary.
        old = self.transients()
        proof_box = RoundedRectangle(width=8.45, height=3.72, corner_radius=0.16, color=EVIDENCE, stroke_width=3, fill_color=BACKGROUND, fill_opacity=0.18).shift(LEFT * 1.30 + UP * 0.48)
        proof_title = self.state_chip(
            "LEAN: FINITE MODEL", EVIDENCE, 2.72, font_size=13, height=0.58
        ).next_to(proof_box, UP, buff=0.12)
        ceiling = self.state_chip(
            "CALLER CEILING", EVIDENCE, 2.24, font_size=13, height=0.58
        ).move_to(proof_box.get_corner(UP + LEFT) + RIGHT * 1.42 + DOWN * 0.42)
        locks = VGroup(
            self.proof_socket("ACTIVE GRANT", EVIDENCE, width=2.18, font_size=13),
            self.proof_socket("DISPATCH", EVIDENCE, width=1.76, font_size=13),
            self.proof_socket("EFFECT CUSTODY", EVIDENCE, width=2.42, font_size=13),
        ).arrange(RIGHT, buff=0.52).move_to(proof_box.get_center() + UP * 0.06)
        trace = VGroup(*[
            Arrow(locks[i].get_right(), locks[i + 1].get_left(), color=EVIDENCE, buff=0.08, stroke_width=2.5)
            for i in range(len(locks) - 1)
        ])
        accepted = self.state_chip("ACCEPTED WITHIN CEILING", EVIDENCE, 2.62).move_to(proof_box.get_bottom() + UP * 0.40)
        miniature = self.ticket(compact=True).scale(0.46).shift(RIGHT * 5.10 + UP * 0.62)
        authored = self.label("AUTHORED TRACE", 13, MUTED, "BOLD").next_to(miniature, DOWN, buff=0.10)
        self.beat(
            12,
            FadeOut(old),
            Create(proof_box),
            FadeIn(proof_title),
            FadeIn(ceiling),
            LaggedStart(*[FadeIn(lock) for lock in locks], lag_ratio=0.18),
            LaggedStart(*[GrowArrow(arrow) for arrow in trace], lag_ratio=0.20),
            FadeIn(accepted),
            FadeIn(miniature),
            FadeIn(authored),
            settle=0.92,
        )

        # b13: production obligations remain explicitly outside the theorem.
        proof_group = VGroup(proof_box, proof_title, ceiling, locks, trace, accepted)
        compact_proof = proof_group.copy().scale(0.72).shift(LEFT * 2.05 + UP * 0.05)
        outside = VGroup(
            self.proof_socket("FORGED ID"),
            self.proof_socket("BYPASSED WRAPPER"),
            self.proof_socket("REVOCATION RACE"),
            self.proof_socket("MISSED EFFECT"),
        ).arrange(DOWN, buff=0.22).scale(0.92).shift(RIGHT * 4.30 + UP * 0.66)
        open_label = self.label("NOT\nESTABLISHED", 19, RESIDUAL, "BOLD").shift(RIGHT * 4.30 + UP * 2.58)
        boundary_line = DashedLine(UP * 2.72, DOWN * 1.30, color=BOUNDARY, dash_length=0.15).shift(RIGHT * 1.58)
        proof_focus = self.focus_lens(compact_proof, EVIDENCE)
        outside_focuses = [self.focus_lens(socket, RESIDUAL) for socket in outside]
        self.beat(
            13,
            FadeOut(self.transients()),
            FadeIn(compact_proof),
            Create(boundary_line),
            Write(open_label),
            LaggedStart(*[FadeIn(socket, shift=LEFT * 0.12) for socket in outside], lag_ratio=0.20),
            Indicate(boundary_line, color=BOUNDARY),
            Succession(
                FadeIn(proof_focus),
                *[Transform(proof_focus, focus) for focus in outside_focuses],
                FadeOut(proof_focus),
            ),
            LaggedStart(
                *[Circumscribe(socket, color=RESIDUAL) for socket in outside],
                lag_ratio=0.25,
            ),
            settle=0.92,
        )

        # b14: the signature image binds both outcomes to exact authority state.
        old = self.transients()
        left_ticket = self.ticket(compact=True).scale(0.72).shift(LEFT * 3.75 + UP * 0.62)
        right_ticket = self.ticket(compact=True).scale(0.72).shift(RIGHT * 3.75 + UP * 0.62)
        active_sleeve = self.sleeve(state="ACTIVE", uses="1", color=AUTHORITY).scale(0.72).shift(LEFT * 3.75 + UP * 0.62)
        consumed_sleeve = self.sleeve(state="CONSUMED", uses="0", color=ROLLBACK).scale(0.72).shift(RIGHT * 3.75 + UP * 0.62)
        acted_receipt = self.receipt("ACTED", "ACTIVE 1", EVIDENCE).shift(LEFT * 3.75 + UP * 2.42)
        refused_receipt = self.receipt("REFUSED", "CONSUMED 0", ROLLBACK).shift(RIGHT * 3.75 + UP * 2.42)
        identity = self.state_chip("IDENTICAL COMMAND", ACCENT, 1.92).shift(UP * 0.62)
        left_link = Arrow(identity.get_left(), active_sleeve.get_right(), color=AUTHORITY, buff=0.14, stroke_width=3)
        right_link = Arrow(identity.get_right(), consumed_sleeve.get_left(), color=ROLLBACK, buff=0.14, stroke_width=3)
        close = self.label("CAPABLE IS NOT AUTHORIZED", 28, INK, "BOLD").shift(DOWN * 0.86)
        why = self.label("SHOW WHY IT ACTED OR REFUSED", 16, MUTED, "BOLD").next_to(close, DOWN, buff=0.16)
        self.beat(
            14,
            FadeOut(old),
            FadeIn(identity),
            FadeIn(left_ticket),
            FadeIn(right_ticket),
            FadeIn(active_sleeve, shift=RIGHT * 0.16),
            FadeIn(consumed_sleeve, shift=LEFT * 0.16),
            GrowArrow(left_link),
            GrowArrow(right_link),
            TransformFromCopy(active_sleeve, acted_receipt),
            TransformFromCopy(consumed_sleeve, refused_receipt),
            Write(close),
            FadeIn(why),
            settle=1.50,
        )
