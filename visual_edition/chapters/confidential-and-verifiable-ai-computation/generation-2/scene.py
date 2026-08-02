"""Generation-2 visual abstract for Confidential and Verifiable AI Computation.

The visual world is a trust-boundary control room.  An input capsule, model
vault, guarantee matrix, compositional primitive rack, attestation receipt,
independent verifier, and fallback airlock remain visible while one bounded
inference is admitted or stopped.  This derivative never promotes the
chapter's support state.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Cross, DashedLine, FadeIn, FadeOut,
    LEFT, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import (
    BOUNDARY, INK, MUTED, RESIDUAL, SURFACE, AsiScene, text,
)


AMBER = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class ConfidentialVerifiableAIComputationGeneration2(AsiScene):
    """A synchronized 05:13 visual explanation of protected inference."""

    TARGET_DURATION = 313.18
    ENDS = [
        14.72, 34.24, 51.095, 69.49, 79.56, 92.405, 105.485, 109.855,
        126.275, 144.07, 154.765, 165.07, 182.79, 198.635, 207.615,
        222.635, 240.13, 250.535, 270.28, 278.61, 295.005, 313.18,
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
        for index in range(1, 23):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.85 if index in (1, 4, 13, 16, 21, 22) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("USER · PROVIDER · AUDITOR · DISTRUST", RED)
            user = self.panel("USER INPUTS", BLUE, 2.35, 1.35).shift(LEFT * 4.0)
            core = self.panel("EXECUTION CORE", VIOLET, 2.5, 1.4).shift(LEFT * 0.55)
            provider = self.panel("MODEL VAULT", AMBER, 2.55, 1.35).shift(RIGHT * 3.15 + UP * 0.55)
            auditor = self.panel("AUDITOR", GREEN, 2.25, 1.2).shift(RIGHT * 2.9 + DOWN * 1.2)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 1.35)
            return VGroup(frame, user, core, provider, auditor, boundary,
                          Arrow(user.get_right(), core.get_left(), color=BLUE, stroke_width=3, buff=0.1),
                          Arrow(provider.get_left(), core.get_right(), color=AMBER, stroke_width=3, buff=0.1),
                          Arrow(core.get_bottom(), auditor.get_top(), color=GREEN, stroke_width=2.5, buff=0.1))
        if index == 2:
            frame = self.frame("TRANSPORT STOPS · COMPUTE BEGINS", RED)
            tunnel = self.panel("ENCRYPTED TRANSPORT", BLUE, 2.8, 1.35).shift(LEFT * 3.6)
            gap = self.panel("UNBOUND COMPUTE", RED, 2.5, 1.35).shift(LEFT * 0.25)
            custody = self.panel("STORED MODEL", AMBER, 2.55, 1.35).shift(RIGHT * 3.2)
            return VGroup(frame, tunnel, gap, custody, Arrow(tunnel.get_right(), gap.get_left(), color=BLUE, stroke_width=3, buff=0.1),
                          Arrow(gap.get_right(), custody.get_left(), color=RED, stroke_width=3, buff=0.1),
                          Cross(gap, stroke_color=RED, stroke_width=2.5), self.badge("POLICY ≠ EXECUTION", RED, 2.7).shift(DOWN * 1.45))
        if index == 3:
            frame = self.frame("ONE LABEL ≠ GUARANTEE VECTOR", RED)
            policy = self.panel("PRIVACY POLICY", MUTED, 2.4, 1.3).shift(LEFT * 3.6)
            matrix = self.panel("EMPTY MATRIX", RED, 2.7, 1.55).shift(LEFT * 0.2)
            hardware = self.panel("HARDWARE CUSTODY", AMBER, 2.7, 1.3).shift(RIGHT * 3.2)
            rows = self.pills(["INPUT", "MODEL", "INTEGRITY", "OUTPUT", "FRESHNESS", "LEAKAGE", "VERIFIER", "COST", "RECOVERY"], [BLUE, AMBER, VIOLET, GREEN, VIOLET, RED, BLUE, MUTED, RESIDUAL], x=0.5, y=-0.95, width=1.65, scale=0.48)
            return VGroup(frame, policy, matrix, hardware, rows, Arrow(policy.get_right(), matrix.get_left(), color=RED, stroke_width=2.5, buff=0.1), Arrow(hardware.get_left(), matrix.get_right(), color=AMBER, stroke_width=2.5, buff=0.1))
        if index == 4:
            frame = self.frame("COMPOSITIONAL EXECUTION CONTRACT", AMBER)
            contract = self.panel("EXECUTION CONTRACT", AMBER, 3.2, 1.55).shift(LEFT * 2.6)
            fields = self.pills(["ADVERSARY", "ASSETS", "LEAKAGE", "TRUST ANCHOR", "STATEMENT", "VERIFIER", "FRESHNESS", "REVOCATION", "BUDGET", "AUTHORITY"], [RED, BLUE, RED, VIOLET, AMBER, GREEN, VIOLET, RESIDUAL, MUTED, AMBER], x=2.0, y=1.05, width=1.75, scale=0.5)
            return VGroup(frame, contract, fields, self.arrows_between(contract, fields, [AMBER, BLUE, RED, VIOLET] * 3), self.badge("BEFORE EXECUTION", AMBER, 2.4).shift(LEFT * 2.6 + DOWN * 1.5))
        if index == 5:
            frame = self.frame("ATTESTATION ≠ SEMANTIC CORRECTNESS", RED)
            receipt = self.panel("ATTESTATION", BLUE, 2.75, 1.45).shift(LEFT * 3.2)
            primitive = self.panel("PRIMITIVE", VIOLET, 2.25, 1.3).shift(LEFT * 0.2)
            props = self.pills(["SEMANTIC CORRECTNESS", "LEGITIMATE PURPOSE", "END-TO-END PRIVACY"], [RED, RED, RED], x=2.4, y=0.8, width=2.5, scale=0.57)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.9)
            return VGroup(frame, receipt, primitive, props, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.3) for x in props])
        if index == 6:
            frame = self.frame("GUARANTEE VECTOR · SEVEN LANES", BLUE)
            matrix = self.panel("GUARANTEE MATRIX", BLUE, 2.8, 1.4).shift(LEFT * 3.7)
            rows = self.pills(["INPUT PRIVACY", "MODEL PRIVACY", "INTERMEDIATE STATE", "INTEGRITY", "AUTHENTICITY", "AVAILABILITY", "AUDITABILITY"], [BLUE, AMBER, BLUE, GREEN, VIOLET, MUTED, AMBER], x=1.45, y=1.0, width=2.1, scale=0.55)
            return VGroup(frame, matrix, rows, self.arrows_between(matrix, rows, [BLUE, AMBER, BLUE, GREEN, VIOLET, MUTED, AMBER]))
        if index == 7:
            frame = self.frame("PRIMITIVE RACK · THREAT-MATCHED", AMBER)
            rack = self.pills(["FHE", "MPC", "ZK", "CONFIDENTIAL EXECUTION", "PRIVATE RETRIEVAL", "DP", "HYBRID"], [VIOLET, VIOLET, BLUE, GREEN, BLUE, AMBER, RESIDUAL], x=-2.9, y=1.0, width=2.1, scale=0.54)
            filter_box = self.panel("ADVERSARY + LEAKAGE", RED, 2.55, 1.4).shift(LEFT * 0.15)
            selected = self.panel("COMPOSITION", GREEN, 2.45, 1.35).shift(RIGHT * 3.1)
            return VGroup(frame, rack, filter_box, selected, self.arrows_between(rack, [filter_box] * len(rack), [RED] * len(rack), dashed=True), Arrow(filter_box.get_right(), selected.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        if index == 8:
            frame = self.frame("ONE BOUNDED PROTECTED INFERENCE", BLUE)
            capsule = self.panel("INPUT CAPSULE", BLUE, 2.5, 1.35).shift(LEFT * 3.9)
            cell = self.panel("PROTECTED CELL", VIOLET, 2.8, 1.55).shift(LEFT * 0.65)
            verifier = self.panel("VERIFIER", GREEN, 2.3, 1.25).shift(RIGHT * 3.2)
            return VGroup(frame, capsule, cell, verifier, Arrow(capsule.get_right(), cell.get_left(), color=VIOLET, stroke_width=3, buff=0.1), Arrow(cell.get_right(), verifier.get_left(), color=GREEN, stroke_width=3, buff=0.1), self.badge("LOCAL TRACE · NOT DEPLOYMENT", MUTED, 3.2).shift(LEFT * 0.5 + DOWN * 1.55))
        if index == 9:
            frame = self.frame("COMMIT ARTIFACTS · MEASURE COST", AMBER)
            cell = self.panel("PROTECTED INFERENCE", VIOLET, 2.65, 1.4).shift(LEFT * 2.8)
            commits = self.pills(["CODE", "MODEL", "CONFIG", "DATA", "PLATFORM", "NONCE", "POLICY"], [BLUE, AMBER, AMBER, BLUE, VIOLET, GREEN, AMBER], x=-0.5, y=1.05, width=1.55, scale=0.5)
            metrics = self.pills(["FRESHNESS", "VERIFY", "NATIVE COST", "PROTECTED COST", "LATENCY"], [GREEN, GREEN, MUTED, RESIDUAL, MUTED], x=2.75, y=0.85, width=2.0, scale=0.54)
            return VGroup(frame, cell, commits, metrics, self.arrows_between(commits, [cell] * len(commits), [AMBER] * len(commits), dashed=True), self.arrows_between(cell, metrics, [GREEN, GREEN, MUTED, RESIDUAL, MUTED]))
        if index == 10:
            frame = self.frame("NEGATIVE TESTS · REPLAY + MISMATCH", RED)
            valid = self.panel("VALID COMPOSITION", GREEN, 2.8, 1.35).shift(LEFT * 2.7)
            tests = self.pills(["REPLAY", "STALE NONCE", "WRONG MODEL", "WRONG CONFIG", "NO AUTHORIZATION"], [RED, RED, RED, RED, RESIDUAL], x=2.0, y=0.9, width=2.0, scale=0.55)
            fallback = self.badge("FALLBACK / QUARANTINE", RESIDUAL, 3.0).shift(RIGHT * 2.55 + DOWN * 1.35)
            return VGroup(frame, valid, tests, fallback, self.arrows_between(valid, tests, [RED] * len(tests), dashed=True), *[Cross(x, stroke_color=RED, stroke_width=2) for x in tests])
        if index == 11:
            frame = self.frame("COMMITMENTS → DISTINCT VERIFIER", GREEN)
            commitments = self.panel("COMMITMENT BUNDLE", AMBER, 3.0, 1.55).shift(LEFT * 2.7)
            receipt = self.panel("ATTESTATION RECEIPT", BLUE, 2.7, 1.45).shift(RIGHT * 0.8)
            verifier = self.panel("INDEPENDENT VERIFIER", GREEN, 2.7, 1.4).shift(RIGHT * 3.7 + DOWN * 0.15)
            return VGroup(frame, commitments, receipt, verifier, Arrow(commitments.get_right(), receipt.get_left(), color=AMBER, stroke_width=3, buff=0.1), Arrow(receipt.get_right(), verifier.get_left(), color=GREEN, stroke_width=3, buff=0.1))
        if index == 12:
            frame = self.frame("CLAIM CLASSES STAY SEPARATE", BLUE)
            receipt = self.panel("APPRAISED RECEIPT", BLUE, 2.8, 1.35).shift(LEFT * 3.8)
            claims = self.pills(["CRYPTOGRAPHIC", "ATTESTED IDENTITY", "MODEL QUALITY", "SEMANTIC VALIDITY", "AUTHORIZATION", "LAWFUL PURPOSE"], [BLUE, VIOLET, AMBER, RED, GREEN, RESIDUAL], x=1.1, y=0.95, width=2.3, scale=0.55)
            return VGroup(frame, receipt, claims, self.arrows_between(receipt, claims, [BLUE, VIOLET, AMBER, RED, GREEN, RESIDUAL], dashed=True))
        if index == 13:
            frame = self.frame("GUARANTEE LAUNDERING · STALE ATTESTATION", RED)
            badge = self.panel("SECURE-COMPUTE LABEL", RED, 3.0, 1.45).shift(LEFT * 3.2)
            stale = self.pills(["STALE ARTIFACT", "PLATFORM CHANGED", "POLICY CHANGED", "REVOKED", "REPLAY"], [RED, RED, RED, RESIDUAL, RED], x=2.2, y=0.9, width=2.15, scale=0.55)
            gate = self.badge("FRESHNESS GATE", AMBER, 2.4).shift(RIGHT * 2.6 + DOWN * 1.35)
            return VGroup(frame, badge, stale, gate, self.arrows_between(stale, [gate] * len(stale), [RED] * len(stale)), Cross(badge, stroke_color=RED, stroke_width=3))
        if index == 14:
            frame = self.frame("LEAKAGE · WRONG ARTIFACT", RED)
            cell = self.panel("PROVED CELL", VIOLET, 2.5, 1.4).shift(LEFT * 0.15)
            leaks = self.pills(["SIDE CHANNEL", "OUTPUT", "ACCESS PATTERN", "LOG", "CACHE", "TIMING"], [RED, RED, RED, RED, RESIDUAL, RED], x=-2.9, y=1.0, width=1.75, scale=0.5)
            wrong = self.pills(["WRONG MODEL", "WRONG PREPROCESSING", "WRONG POLICY", "INVALID RELATION"], [RED] * 4, x=2.8, y=0.9, width=2.1, scale=0.54)
            return VGroup(frame, cell, leaks, wrong, self.arrows_between(cell, [leaks] * len(leaks), [RED] * len(leaks), dashed=True), self.arrows_between(cell, wrong, [RED] * len(wrong)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in wrong])
        if index == 15:
            frame = self.frame("FAIL CLOSED · OWN THE RESIDUAL", RESIDUAL)
            failures = self.pills(["LEAKAGE", "SEMANTIC INVALIDITY", "STALE RECEIPT", "MISMATCH"], [RED, RED, RED, RED], x=-2.8, y=1.0, width=2.2, scale=0.56)
            outcomes = self.pills(["STOP", "NARROW", "QUARANTINE", "COMPENSATE", "OWN RESIDUAL"], [RED, AMBER, VIOLET, AMBER, RESIDUAL], x=2.15, y=0.95, width=2.1, scale=0.57)
            owner = self.badge("OWNER + RECEIPT", RESIDUAL, 2.7).shift(RIGHT * 2.75 + DOWN * 1.4)
            return VGroup(frame, failures, outcomes, owner, self.arrows_between(failures, [outcomes] * len(failures), [RED] * len(failures)), self.arrows_between(outcomes, [owner] * len(outcomes), [RESIDUAL] * len(outcomes), dashed=True))
        if index == 16:
            frame = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
            local = self.panel("LOCAL CELL + VERIFIER", GREEN, 3.0, 1.5).shift(LEFT * 3.0)
            stamp = self.badge("SUPPORT STATE", AMBER, 2.3).shift(LEFT * 3.0 + DOWN * 1.35)
            targets = self.pills(["SEMANTIC PROOF", "AUTHORIZATION", "END-TO-END PRIVACY", "PROOF TARGETS OPEN"], [RED, RED, RED, MUTED], x=2.0, y=0.75, width=2.5, scale=0.55)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, stamp, targets, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in targets[:3]])
        if index == 17:
            frame = self.frame("PROTECTED-EXECUTION HANDOFF AIRLOCK", AMBER)
            checklist = self.pills(["GUARANTEES", "ADVERSARY", "LEAKAGE", "ARTIFACT", "FRESHNESS", "VERIFIER", "FALLBACK", "UNSUPPORTED"], [GREEN, RED, RED, BLUE, VIOLET, GREEN, RESIDUAL, MUTED], x=-1.8, y=1.0, width=1.75, scale=0.5)
            airlock = self.panel("BOUNDED RECEIPT", GREEN, 2.7, 1.45).shift(RIGHT * 2.5 + UP * 0.2)
            blocked = self.pills(["SEMANTIC PROOF", "AUTHORIZATION", "END-TO-END PRIVACY"], [RED, RED, RED], x=2.45, y=-1.25, width=2.2, scale=0.5)
            return VGroup(frame, checklist, airlock, blocked, self.arrows_between(checklist, [airlock] * len(checklist), [GREEN] * len(checklist)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in blocked])
        if index == 18:
            frame = self.frame("ATTESTATION STATEMENT · MEASURED SCOPE", BLUE)
            environment = self.panel("MEASURED ENVIRONMENT", BLUE, 2.8, 1.4).shift(LEFT * 3.2)
            receipt = self.panel("APPRAISED STATEMENT", GREEN, 2.8, 1.4).shift(RIGHT * 0.1)
            unsupported = self.pills(["TRUSTWORTHY INTENT", "CORRECT POLICY", "OUTPUT MEANING"], [RED, RED, RED], x=2.7, y=0.85, width=2.3, scale=0.55)
            return VGroup(frame, environment, receipt, unsupported, Arrow(environment.get_right(), receipt.get_left(), color=GREEN, stroke_width=3, buff=0.1), *[Cross(x, stroke_color=RED, stroke_width=2) for x in unsupported])
        if index == 19:
            frame = self.frame("LOCAL RECEIPT · NO BROAD PROMOTION", RED)
            local = self.panel("LOCAL PROTECTED RECEIPT", GREEN, 3.0, 1.5).shift(LEFT * 3.2)
            broad = self.pills(["IMPLEMENTATION PROOF", "USEFUL DEPLOYMENT", "ENFORCEMENT", "SAFETY", "TRANSFER", "AGI / ASI"], [RED] * 6, x=2.1, y=0.8, width=2.3, scale=0.53)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, broad, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.2) for x in broad])
        if index == 20:
            frame = self.frame("SOURCE + DERIVATIVE · SAME CEILING", BLUE)
            source = self.panel("LIVE CHAPTER", BLUE, 2.7, 1.4).shift(LEFT * 3.3)
            derivative = self.panel("VISUAL DERIVATIVE", AMBER, 2.7, 1.4).shift(RIGHT * 2.0)
            return VGroup(frame, source, derivative, Arrow(source.get_right(), derivative.get_left(), color=BLUE, stroke_width=3, buff=0.1), self.badge("SAME EVIDENCE CEILING", MUTED, 3.1).shift(DOWN * 1.45))
        if index == 21:
            frame = self.frame("ARGUMENT SUPPORT · MODEL CUSTODY NEXT", AMBER)
            support = self.panel("ARGUMENT SUPPORT", AMBER, 2.8, 1.5).shift(LEFT * 3.4)
            nonclaims = self.pills(["NO EMPIRICAL", "NO DEPLOYMENT", "NO SAFETY", "NO TRANSFER", "NO AGI / ASI"], [RED] * 5, x=1.55, y=0.9, width=2.05, scale=0.54)
            next_panel = self.panel("MODEL-WEIGHT CUSTODY", VIOLET, 2.9, 1.35).shift(RIGHT * 2.6 + DOWN * 1.2)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, support, nonclaims, next_panel, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in nonclaims])
        frame = self.frame("CUSTODY SURFACE · COPY / RECONSTRUCT / REVOKE", VIOLET)
        receipt = self.panel("PROTECTED RECEIPT", GREEN, 2.8, 1.4).shift(LEFT * 3.5)
        custody = self.pills(["WEIGHTS", "OPTIMIZER", "ADAPTERS", "QUANTIZATION", "CHECKPOINTS", "CACHE", "RECOVERY IMAGE", "DERIVATIVES"], [BLUE, AMBER, VIOLET, MUTED, BLUE, RESIDUAL, RED, RED], x=1.4, y=1.0, width=1.85, scale=0.5)
        boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=VIOLET, stroke_width=3).shift(RIGHT * 0.0)
        return VGroup(frame, receipt, custody, boundary, self.arrows_between(receipt, custody, [BLUE, AMBER, VIOLET, MUTED, BLUE, RESIDUAL, RED, RED], dashed=True), self.badge("COPY · RECONSTRUCT · REVOKE", RESIDUAL, 3.2).shift(RIGHT * 2.5 + DOWN * 1.45))
