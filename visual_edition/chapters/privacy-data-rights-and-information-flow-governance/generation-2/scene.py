"""Generation-2 visual abstract for Privacy, Data Rights, and Information-Flow Governance.

The visual world is a rights-and-flow control room.  One information packet
travels through a prospective purpose contract, a less-data sieve, lifecycle
flow map, rights/remedy ledger, residual vault, and bounded handoff airlock.
This is an explanatory derivative and never promotes the chapter's support
state.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Cross, DashedLine, FadeIn, FadeOut,
    LEFT, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    BOUNDARY, INK, MUTED, RESIDUAL, ROLLBACK, SURFACE, AsiScene, text,
)


AMBER = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class PrivacyDataRightsInformationFlowGovernanceGeneration2(AsiScene):
    """A synchronized 04:20 visual explanation of a governed information use."""

    TARGET_DURATION = 260.28
    ENDS = [
        18.12, 36.775, 55.695, 74.09, 92.495, 96.865, 115.46, 134.63,
        149.835, 165.34, 180.36, 199.105, 202.06, 221.805, 230.135,
        246.83, 260.28,
    ]

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
            per_animation = min(1.25, action_budget) if len(animations) == 1 else max(0.08, action_budget / len(animations))
            for animation in animations:
                self.play(animation, run_time=per_animation)
        self.wait_until(self.ENDS[index - 1])

    @staticmethod
    def label(value: str, size: int = 17, color: str = INK, weight: str = "NORMAL") -> Text:
        return text(value, size=size, color=color, weight=weight)

    def badge(self, value: str, color: str, width: float = 2.2, height: float = 0.48) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.1,
                                 stroke_color=color, stroke_width=2.5,
                                 fill_color=SURFACE, fill_opacity=1)
        caption = self.label(value, 12, color, "BOLD")
        if caption.width > width - 0.18:
            caption.scale_to_fit_width(width - 0.18)
        caption.move_to(shell)
        return VGroup(shell, caption)

    def panel(self, title: str, color: str, width: float = 2.5, height: float = 1.3) -> VGroup:
        shell = RoundedRectangle(width=width, height=height, corner_radius=0.16,
                                 stroke_color=color, stroke_width=3,
                                 fill_color=DEEP, fill_opacity=1)
        title_obj = self.badge(title, color, min(width - 0.16, 3.5), 0.4).scale(0.82)
        title_obj.next_to(shell, UP, buff=-0.08)
        return VGroup(shell, title_obj)

    def frame(self, title: str, color: str = AMBER) -> VGroup:
        shell = RoundedRectangle(width=11.7, height=6.2, corner_radius=0.2,
                                 stroke_color=BOUNDARY, stroke_width=2,
                                 fill_color="#0F2029", fill_opacity=1)
        heading = self.badge(title, color, 5.7, 0.56).shift(UP * 2.72)
        return VGroup(shell, heading)

    def pills(self, names: list[str], colors: list[str], *, x: float = 0, y: float = 0,
              width: float = 1.75, scale: float = 0.68, direction=DOWN) -> VGroup:
        group = VGroup(*[self.badge(name, colors[i % len(colors)], width) for i, name in enumerate(names)])
        group.arrange(direction, buff=0.13).scale(scale).shift(RIGHT * x + UP * y)
        return group

    def arrows_between(self, source, targets, colors, *, dashed: bool = False) -> VGroup:
        arrows = []
        for i, target in enumerate(targets):
            color = colors[i % len(colors)]
            if dashed:
                arrows.append(DashedLine(source.get_right(), target.get_left(), color=color, stroke_width=2))
            else:
                arrows.append(Arrow(source.get_right(), target.get_left(), color=color, stroke_width=2.5, buff=0.08))
        return VGroup(*arrows)

    def construct(self) -> None:
        self.current = VGroup()
        for index in range(1, 18):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.85 if index in (1, 5, 11, 16, 17) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("AUTHORIZED ACCESS · RIGHTS SURFACE", RED)
            packet = self.panel("INFORMATION PACKET", BLUE, 2.65, 1.4).shift(LEFT * 3.8)
            access = self.badge("ACCESS GRANTED", GREEN, 2.3).shift(LEFT * 3.8 + UP * 1.35)
            flows = self.pills(["COLLECTION", "LINKAGE", "INFERENCE", "MEMORY", "TRAINING", "SHARING", "RETENTION", "DERIVATIVE"],
                               [RED, RED, VIOLET, BLUE, AMBER, RED, RESIDUAL, RED], x=1.6, y=1.0, width=2.0, scale=0.52)
            parties = self.pills(["SUBJECTS", "AFFECTED GROUPS", "RIGHTS"], [BLUE, AMBER, RED], x=3.75, y=-1.45, width=2.25, scale=0.58, direction=RIGHT)
            return VGroup(frame, packet, access, flows, parties, self.arrows_between(packet, flows, [RED] * len(flows)))
        if index == 2:
            frame = self.frame("BADGES ≠ COMPLETE RIGHTS", RED)
            shortcuts = self.pills(["ACCESS", "CONSENT", "DP LABEL", "LOW ATTACK RATE", "DELETED ROW", "CHANGED ANSWER", "CLOSED TICKET"],
                                   [AMBER, AMBER, VIOLET, MUTED, RED, RED, RED], x=-2.4, y=1.05, width=2.0, scale=0.52)
            residuals = self.pills(["COPY", "CACHE", "BACKUP", "INFLUENCE", "PURPOSE DRIFT"], [RED, RED, RESIDUAL, RESIDUAL, RED], x=2.6, y=0.9, width=2.15, scale=0.58)
            boundary = DashedLine(UP * 2.25, DOWN * 2.25, color=RED, stroke_width=3).shift(RIGHT * 0.2)
            return VGroup(frame, shortcuts, residuals, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in residuals])
        if index == 3:
            frame = self.frame("PROSPECTIVE PURPOSE CONTRACT", AMBER)
            packet = self.panel("PACKET", BLUE, 2.3, 1.25).shift(LEFT * 3.9)
            contract = self.panel("PURPOSE + AUTHORITY", AMBER, 3.0, 1.5).shift(LEFT * 0.45)
            fields = self.pills(["AFFECTED PARTIES", "PROCESSING", "JURISDICTION", "RECIPIENTS", "RETENTION", "MINIMIZATION", "FLOW", "DERIVATIVES"],
                                [BLUE, AMBER, AMBER, RED, MUTED, GREEN, BLUE, RESIDUAL], x=3.3, y=0.95, width=1.8, scale=0.52)
            return VGroup(frame, packet, contract, fields, Arrow(packet.get_right(), contract.get_left(), color=AMBER, stroke_width=3, buff=0.1), self.arrows_between(contract, fields, [AMBER] * len(fields)), self.badge("EXECUTION CLOSED", RED, 2.4).shift(LEFT * 0.45 + DOWN * 1.55))
        if index == 4:
            frame = self.frame("PRIVACY + RIGHTS LEDGER", AMBER)
            contract = self.panel("DECLARED RECORD", AMBER, 2.7, 1.45).shift(LEFT * 3.5)
            fields = self.pills(["PRIVACY UNIT", "ADJACENCY", "BUDGET", "THREAT PLAN", "RIGHTS STATE", "REMEDY", "RESIDUAL COPIES", "INFLUENCE", "COST", "NON-AUTHORITY"],
                                [BLUE, BLUE, VIOLET, RED, VIOLET, GREEN, RED, RESIDUAL, MUTED, RED], x=1.15, y=1.05, width=1.72, scale=0.5)
            return VGroup(frame, contract, fields, self.arrows_between(contract, fields, [AMBER, BLUE, VIOLET, RED] * 3), self.badge("ONE RECEIPT ≠ ALL OUTCOMES", RED, 3.2).shift(LEFT * 2.7 + DOWN * 1.55))
        if index == 5:
            frame = self.frame("IDENTITY · EXPIRY · OBJECTION", BLUE)
            register = self.panel("AFFECTED PARTIES", BLUE, 2.75, 1.45).shift(LEFT * 3.55 + UP * 0.4)
            rows = self.pills(["SUBJECTS", "GROUPS", "UNKNOWN ROUTES", "PURPOSE", "AUTHORITY", "RECIPIENTS", "RETENTION", "EXPIRY", "OBJECTION"],
                              [BLUE, AMBER, MUTED, AMBER, AMBER, RED, MUTED, VIOLET, VIOLET], x=1.5, y=1.05, width=1.85, scale=0.53)
            outside = self.pills(["TOTAL ERASURE", "FORGETTING", "INFLUENCE REMOVAL", "RELEASE", "SOTA"], [RED, RED, RESIDUAL, RED, RED], x=2.6, y=-1.25, width=2.0, scale=0.5, direction=RIGHT)
            return VGroup(frame, register, rows, outside, self.arrows_between(register, rows, [BLUE] * len(rows)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in outside])
        if index == 6:
            frame = self.frame("BOUNDED IMPLEMENTATION TRACE", BLUE)
            contract = self.panel("FROZEN RECORD", AMBER, 2.75, 1.4).shift(LEFT * 3.5)
            harness = self.panel("SYNTHETIC LIFECYCLE", VIOLET, 3.0, 1.55).shift(RIGHT * 1.0)
            gate = self.badge("EXECUTION GATE", RED, 2.2).shift(RIGHT * 3.7 + DOWN * 1.35)
            return VGroup(frame, contract, harness, gate, Arrow(contract.get_right(), harness.get_left(), color=VIOLET, stroke_width=3, buff=0.1), self.badge("LOCAL TRACE · NOT DEPLOYMENT", MUTED, 3.2).shift(LEFT * 1.0 + DOWN * 1.45))
        if index == 7:
            frame = self.frame("COMPARISON ARMS · POSITIVE CONTROLS", AMBER)
            arms = self.pills(["ORDINARY", "ACCESS-ONLY", "MINIMIZATION", "DP", "PURPOSE-BOUND", "REMEDIATION"], [MUTED, RED, GREEN, VIOLET, AMBER, BLUE], x=-1.95, y=1.0, width=2.15, scale=0.56)
            campaign = self.panel("SMALL MODEL + MEMORY", BLUE, 2.8, 1.35).shift(RIGHT * 2.75 + UP * 0.35)
            rights = self.pills(["DESCENDANT RIGHTS", "POSITIVE ATTACKS", "FROZEN PLAN"], [VIOLET, RED, AMBER], x=2.65, y=-1.15, width=2.2, scale=0.55)
            return VGroup(frame, arms, campaign, rights, self.arrows_between(arms, [campaign] * len(arms), [AMBER] * len(arms), dashed=True))
        if index == 8:
            frame = self.frame("SEEDS · INDEPENDENCE · LESS DATA", GREEN)
            seeds = self.pills(["SEED 1", "SEED 2", "SEED 3"], [BLUE, BLUE, BLUE], x=-3.6, y=0.9, width=1.65, scale=0.62)
            evaluator = self.panel("INDEPENDENT EVALUATOR", VIOLET, 2.7, 1.25).shift(LEFT * 0.95 + UP * 0.55)
            sieve = self.panel("MINIMIZATION SIEVE", AMBER, 2.5, 1.35).shift(RIGHT * 2.2 + UP * 0.55)
            outcomes = self.pills(["UTILITY", "PRIVACY", "RIGHTS", "COST"], [GREEN, VIOLET, BLUE, MUTED], x=1.45, y=-1.1, width=1.65, scale=0.58, direction=RIGHT)
            return VGroup(frame, seeds, evaluator, sieve, outcomes, self.arrows_between(evaluator, [sieve], [AMBER]), self.arrows_between(sieve, outcomes, [GREEN, VIOLET, BLUE, MUTED]))
        if index == 9:
            frame = self.frame("LIFECYCLE FLOW MAP · UNKNOWN ROUTES", BLUE)
            packet = self.panel("MINIMIZED PACKET", GREEN, 2.6, 1.35).shift(LEFT * 4.0)
            flows = self.pills(["CONTEXT", "MEMORY", "TRAINING", "INFERENCE", "OUTPUT", "AUDIT", "SHARING", "CACHE", "BACKUP", "CHECKPOINT", "DERIVATIVE"],
                               [BLUE, BLUE, AMBER, VIOLET, GREEN, MUTED, RED, BLUE, RESIDUAL, AMBER, RED], x=0.2, y=1.05, width=1.6, scale=0.48)
            unknown = self.pills(["UNKNOWN", "UNKNOWN"], [MUTED, MUTED], x=3.65, y=-1.25, width=1.55, scale=0.58, direction=RIGHT)
            invariant = self.badge("ACCESS ≠ CONSENT ≠ PURPOSE", RED, 3.3).shift(LEFT * 1.8 + DOWN * 1.55)
            return VGroup(frame, packet, flows, unknown, invariant, self.arrows_between(packet, flows, [BLUE] * len(flows), dashed=True), *[Cross(x, stroke_color=MUTED, stroke_width=2) for x in unknown])
        if index == 10:
            frame = self.frame("FAIL CLOSED · OWN THE RESIDUAL", RED)
            failures = self.pills(["PURPOSE DRIFT", "CONSENT LAUNDERING", "MINIMIZATION THEATER", "CROSS-USER LEAKAGE"], [RED, RED, RED, RED], x=-2.8, y=1.0, width=2.3, scale=0.55)
            remedies = self.pills(["STOP", "NARROW", "QUARANTINE", "COMPENSATE", "OWN RESIDUAL"], [RED, AMBER, VIOLET, AMBER, RESIDUAL], x=2.2, y=0.95, width=2.2, scale=0.58)
            owner = self.badge("OWNER + RECEIPT", RESIDUAL, 2.8).shift(RIGHT * 2.8 + DOWN * 1.45)
            return VGroup(frame, failures, remedies, owner, self.arrows_between(failures, [remedies] * len(failures), [RED] * len(failures)), self.arrows_between(remedies, [owner] * len(remedies), [RESIDUAL] * len(remedies), dashed=True))
        if index == 11:
            frame = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
            local = self.panel("LOCAL CONTRACT + FLOW", GREEN, 3.0, 1.5).shift(LEFT * 3.0)
            stamp = self.badge("SUPPORT STATE", AMBER, 2.3).shift(LEFT * 3.0 + DOWN * 1.35)
            targets = self.pills(["LEGAL COMPLIANCE", "TOTAL FORGETTING", "USEFUL DEPLOYMENT", "PROOF TARGETS OPEN"], [RED, RED, RED, MUTED], x=2.0, y=0.75, width=2.55, scale=0.55)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, stamp, targets, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in targets[:3]])
        if index == 12:
            frame = self.frame("BOUNDED RECEIPT · SEPARATE OUTCOMES", AMBER)
            checks = self.pills(["PURPOSE MATCH", "AUTHORITY MATCH", "MINIMIZATION", "FLOW", "COMPETENT EVALUATION"], [GREEN, AMBER, GREEN, BLUE, VIOLET], x=-2.9, y=1.0, width=2.25, scale=0.54)
            receipt = self.panel("INFORMATION RECEIPT", GREEN, 2.7, 1.45).shift(RIGHT * 0.25)
            outcomes = self.pills(["STORAGE", "BEHAVIOR", "INFLUENCE", "PRIVACY", "LEGAL COMPLIANCE"], [BLUE, VIOLET, RESIDUAL, GREEN, AMBER], x=3.0, y=0.8, width=2.0, scale=0.52)
            return VGroup(frame, checks, receipt, outcomes, self.arrows_between(checks, [receipt] * len(checks), [GREEN] * len(checks)), self.arrows_between(receipt, outcomes, [BLUE, VIOLET, RESIDUAL, GREEN, AMBER]), self.badge("NO AUTHORITY LAUNDERING", RED, 2.9).shift(RIGHT * 2.6 + DOWN * 1.4))
        if index == 13:
            frame = self.frame("LESS-DATA ALTERNATIVE", GREEN)
            full = self.panel("FULL PACKET", RED, 2.75, 1.5).shift(LEFT * 3.2)
            sieve = self.panel("SIEVE", AMBER, 1.9, 1.35).shift(LEFT * 0.35)
            admitted = self.panel("NECESSARY FIELDS", GREEN, 2.8, 1.5).shift(RIGHT * 3.0)
            rejected = self.pills(["UNUSED", "TOO GRANULAR", "OUT OF PURPOSE"], [RED, RED, RESIDUAL], x=0.0, y=-1.35, width=1.9, scale=0.55, direction=RIGHT)
            return VGroup(frame, full, sieve, admitted, rejected, Arrow(full.get_right(), sieve.get_left(), color=AMBER, stroke_width=3, buff=0.1), Arrow(sieve.get_right(), admitted.get_left(), color=GREEN, stroke_width=3, buff=0.1), *[Cross(x, stroke_color=RED, stroke_width=2) for x in rejected])
        if index == 14:
            frame = self.frame("LOCAL RECORD · NO BROAD PROMOTION", RED)
            local = self.panel("LOCAL RIGHTS RECORD", GREEN, 3.0, 1.5).shift(LEFT * 3.2)
            broad = self.pills(["IMPLEMENTATION PROOF", "USEFUL DEPLOYMENT", "ENFORCEMENT", "SAFETY", "TRANSFER", "AGI / ASI"], [RED] * 6, x=2.1, y=0.8, width=2.3, scale=0.53)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, broad, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.3) for x in broad])
        if index == 15:
            frame = self.frame("SOURCE + DERIVATIVE · SAME CEILING", BLUE)
            source = self.panel("LIVE CHAPTER", BLUE, 2.7, 1.4).shift(LEFT * 3.3)
            derivative = self.panel("VISUAL DERIVATIVE", AMBER, 2.7, 1.4).shift(RIGHT * 2.0)
            line = Arrow(source.get_right(), derivative.get_left(), color=BLUE, stroke_width=3, buff=0.1)
            ceiling = self.badge("SAME EVIDENCE CEILING", MUTED, 3.1).shift(DOWN * 1.45)
            return VGroup(frame, source, derivative, line, ceiling)
        if index == 16:
            frame = self.frame("ARGUMENT SUPPORT · NEXT BOUNDARY", AMBER)
            support = self.panel("ARGUMENT SUPPORT", AMBER, 2.8, 1.5).shift(LEFT * 3.4)
            nonclaims = self.pills(["NO EMPIRICAL", "NO DEPLOYMENT", "NO SAFETY", "NO TRANSFER", "NO AGI / ASI"], [RED] * 5, x=1.65, y=0.9, width=2.05, scale=0.55)
            next_panel = self.panel("CONFIDENTIAL + VERIFIABLE", VIOLET, 3.0, 1.35).shift(RIGHT * 2.5 + DOWN * 1.15)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, support, nonclaims, next_panel, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in nonclaims])
        frame = self.frame("TRUST BOUNDARIES · COMPUTATION NEXT", VIOLET)
        receipt = self.panel("BOUNDED RECEIPT", GREEN, 2.8, 1.45).shift(LEFT * 3.4)
        roles = self.pills(["USER INPUTS", "PROVIDER WEIGHTS", "AUDITOR ARTIFACT"], [BLUE, AMBER, VIOLET], x=2.25, y=0.85, width=2.25, scale=0.6)
        boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=VIOLET, stroke_width=3).shift(RIGHT * 0.0)
        return VGroup(frame, receipt, roles, boundary, self.arrows_between(receipt, roles, [BLUE, AMBER, VIOLET]))
