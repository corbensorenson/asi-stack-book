"""Generation-2 visual abstract for Adversarial Machine Learning.

The visual world is an attack-surface lab: a versioned checkpoint, threat
contract, separate attack lanes, adaptive attacker, joint utility ledger, and
handoff airlock remain visible while the chapter narrows its claims.
"""

from __future__ import annotations

from manim import (
    AnimationGroup, Arrow, Create, Cross, DashedLine, FadeIn, FadeOut,
    GrowArrow, Indicate, LEFT, RIGHT, RoundedRectangle, Text, UP, DOWN, VGroup,
)

from visual_edition.lib.asi_visuals import BOUNDARY, INK, MUTED, RESIDUAL, SURFACE, AsiScene, text


AMBER = "#F2BD63"
GREEN = "#66D58A"
RED = "#FF6073"
VIOLET = "#9C82E8"
BLUE = "#67D5F2"
DEEP = "#142934"


class AdversarialMachineLearningAttackSurfaceGeneration2(AsiScene):
    """A synchronized 04:31 visual explanation of a model-threat ledger."""

    TARGET_DURATION = 271.57
    ENDS = [19.0, 38.495, 56.24, 73.21, 85.83, 97.96, 108.88, 127.65,
            139.52, 150.275, 165.905, 180.925, 196.67, 210.25, 229.995,
            238.325, 254.945, 271.57]

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
        for index in range(1, 19):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.9 if index in (1, 3, 11, 17, 18) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("CHECKPOINT · MODEL ATTACK SURFACE", RED)
            vault = self.panel("CHECKPOINT VAULT", BLUE, 2.55, 1.45).shift(LEFT * 3.6)
            attacks = self.pills(["TRAINING DATA", "INFERENCE INPUTS", "TRIGGERS", "QUERIES", "SENSITIVE PROPERTIES", "MULTIMODAL", "AGENTIC"], [RED, RED, RED, AMBER, RESIDUAL, VIOLET, RED], x=1.3, y=1.0, width=2.25, scale=0.54)
            shell = self.badge("SOFTWARE SHELL NOMINAL", MUTED, 3.0).shift(LEFT * 2.9 + DOWN * 1.45)
            return VGroup(frame, vault, attacks, shell, self.arrows_between(vault, attacks, [RED] * len(attacks)))
        if index == 2:
            frame = self.frame("ROBUSTNESS PROXIES · COVERAGE GAPS", RED)
            proxies = self.pills(["ACCESS CONTROL", "ROBUSTNESS SCORE", "STATIC RED TEAM", "CLEAN ACCURACY", "ONE DEFENSE"], [AMBER, BLUE, VIOLET, GREEN, RED], x=-2.0, y=1.0, width=2.2, scale=0.58)
            gaps = self.pills(["POISONING", "BACKDOOR", "EXTRACTION", "ADAPTIVE", "AGENTIC"], [RED, RED, RESIDUAL, VIOLET, RED], x=2.5, y=1.0, width=2.0, scale=0.58)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.2)
            return VGroup(frame, proxies, gaps, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in proxies])
        if index == 3:
            frame = self.frame("VERSIONED MODEL-THREAT CONTRACT", AMBER)
            vault = self.panel("CHECKPOINT", BLUE, 2.3, 1.35).shift(LEFT * 3.8)
            fields = self.pills(["FAMILY", "LIFECYCLE", "ATTACKER", "SURFACE", "BUDGET", "OBJECTIVE", "ADAPTATION", "TRANSFER"], [BLUE, VIOLET, RED, RED, AMBER, AMBER, VIOLET, RESIDUAL], x=1.3, y=1.0, width=1.8, scale=0.53)
            return VGroup(frame, vault, fields, self.arrows_between(vault, fields, [AMBER] * len(fields)), self.badge("NO RESULT YET", MUTED, 2.1).shift(LEFT * 3.8 + DOWN * 1.45))
        if index == 4:
            frame = self.frame("ATTACK / DEFENSE LEDGER · KEEP EFFECT + COST", AMBER)
            source = self.panel("THREAT RECORD", AMBER, 2.5, 1.35).shift(LEFT * 3.8)
            rows = self.pills(["EFFECT", "DETECTION", "MITIGATION", "UTILITY COST", "RECOVERY", "RESIDUAL", "DISCLOSURE"], [RED, VIOLET, GREEN, RED, GREEN, RESIDUAL, MUTED], x=1.2, y=1.0, width=2.05, scale=0.56)
            proxies = self.pills(["CLEAN ACCURACY", "FAILED ATTACK", "BENCHMARK", "CERTIFICATION"], [MUTED, RED, MUTED, RED], x=2.0, y=-1.2, width=2.1, scale=0.56, direction=RIGHT)
            return VGroup(frame, source, rows, proxies, self.arrows_between(source, rows, [AMBER] * len(rows)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in proxies])
        if index == 5:
            frame = self.frame("FREEZE IDENTITY + PROHIBITED EFFECTS", BLUE)
            identity = self.panel("VERSIONED MODEL", BLUE, 2.7, 1.45).shift(LEFT * 3.25)
            fields = self.pills(["CHECKPOINT DIGEST", "DATA LINEAGE", "MODALITY", "ACCESS", "GOAL", "KNOWLEDGE", "BUDGET"], [BLUE, BLUE, VIOLET, AMBER, RED, RED, AMBER], x=1.6, y=0.85, width=2.15, scale=0.56)
            forbidden = self.badge("PROHIBITED REAL-WORLD EFFECTS", RED, 3.8).shift(RIGHT * 2.2 + DOWN * 1.4)
            return VGroup(frame, identity, fields, forbidden, self.arrows_between(identity, fields, [BLUE] * len(fields)), Cross(forbidden, stroke_color=RED, stroke_width=2.5))
        if index == 6:
            frame = self.frame("SEPARATE ATTACK LANES · COUNT DENOMINATORS", RED)
            vault = self.panel("CHECKPOINT", BLUE, 2.25, 1.3).shift(LEFT * 4.0)
            lanes = self.pills(["EVASION", "POISONING", "BACKDOOR", "BYPASS", "EXTRACTION", "INVERSION", "TRANSFER", "ADAPTIVE", "MULTIMODAL", "AGENTIC"], [RED, RED, RED, RED, RESIDUAL, RESIDUAL, AMBER, VIOLET, VIOLET, RED], x=1.0, y=1.05, width=1.7, scale=0.5)
            denoms = self.badge("N / DENOMINATOR PER LANE", AMBER, 3.3).shift(RIGHT * 2.5 + DOWN * 1.5)
            return VGroup(frame, vault, lanes, denoms, self.arrows_between(vault, lanes, [RED] * len(lanes)))
        if index == 7:
            frame = self.frame("BOUNDED AML HARNESS", VIOLET)
            checkpoint = self.panel("FROZEN CHECKPOINT", BLUE, 2.55, 1.35).shift(LEFT * 3.3)
            harness = self.panel("PUBLIC TOY / CONSENTED", VIOLET, 2.9, 1.55).shift(RIGHT * 1.0)
            gates = self.pills(["SAFE HARNESS", "NO REAL-WORLD EFFECTS", "CONSENT", "PUBLIC INPUT"], [GREEN, RED, AMBER, BLUE], x=2.7, y=-0.2, width=2.1, scale=0.57)
            boundary = RoundedRectangle(width=4.0, height=2.35, corner_radius=0.2, stroke_color=VIOLET, stroke_width=2, fill_opacity=0).move_to(harness.get_center())
            return VGroup(frame, checkpoint, harness, gates, boundary, Arrow(checkpoint.get_right(), harness.get_left(), color=VIOLET, stroke_width=3, buff=0.1))
        if index == 8:
            frame = self.frame("MATCHED CONTROLS · JOINT UTILITY LEDGER", AMBER)
            controls = self.pills(["CLEAN", "NOISE", "KNOWN VULNERABLE", "ATTACK-AWARE", "TRANSFER", "ADAPTIVE"], [GREEN, BLUE, RED, VIOLET, AMBER, RED], x=-2.3, y=1.0, width=1.9, scale=0.55)
            ledger = self.panel("UTILITY + RECOVERY", GREEN, 2.6, 1.45).shift(RIGHT * 2.8 + UP * 0.6)
            rows = self.pills(["QUERY BUDGET", "TUNING BUDGET", "FALSE POSITIVES", "LATENCY", "RESIDUAL"], [AMBER, AMBER, RED, MUTED, RESIDUAL], x=2.3, y=-0.9, width=2.25, scale=0.57)
            return VGroup(frame, controls, ledger, rows, self.arrows_between(controls, [ledger] * len(controls), [AMBER] * len(controls)))
        if index == 9:
            frame = self.frame("N / DENOMINATOR · NO AGGREGATE SHORTCUT", BLUE)
            lanes = self.pills(["EVASION 4/20", "POISON 2/12", "BACKDOOR 1/8", "TRANSFER 3/15", "ADAPTIVE 2/10"], [RED, RED, RED, AMBER, VIOLET], x=-0.3, y=1.05, width=2.35, scale=0.58)
            aggregate = self.badge("ONE ROBUSTNESS BADGE", MUTED, 3.0).shift(RIGHT * 3.0 + DOWN * 0.4)
            boundary = DashedLine(UP * 2.1, DOWN * 2.1, color=RED, stroke_width=3).shift(RIGHT * 1.75)
            return VGroup(frame, lanes, aggregate, boundary, Cross(aggregate, stroke_color=RED, stroke_width=2.5))
        if index == 10:
            frame = self.frame("ADAPTIVE ATTACKER · SCOPE-LABELED DEFENSE", VIOLET)
            attacker = self.panel("ADAPTIVE ATTACKER", RED, 2.55, 1.35).shift(LEFT * 3.4)
            wall = self.panel("DEFENSE", VIOLET, 2.4, 1.45).shift(LEFT * 0.1)
            scopes = self.pills(["MONITOR", "RECOVERY", "BOUNDED CERTIFICATE", "MATCHED UTILITY"], [BLUE, GREEN, AMBER, GREEN], x=2.5, y=0.85, width=2.35, scale=0.56)
            return VGroup(frame, attacker, wall, scopes, Arrow(attacker.get_right(), wall.get_left(), color=RED, stroke_width=3, buff=0.1), Arrow(attacker.get_bottom(), wall.get_bottom(), color=RED, stroke_width=2, buff=0.1), self.arrows_between(wall, scopes, [VIOLET] * len(scopes)))
        if index == 11:
            frame = self.frame("ATTACK FAILURES · OWN THE RESIDUAL", RED)
            attacks = self.pills(["EVASION", "POISONING", "CLEAN-LABEL", "BACKDOOR", "TROJAN"], [RED, RED, RESIDUAL, RED, RED], x=-2.7, y=1.0, width=1.95, scale=0.6)
            outcomes = self.pills(["STOP", "NARROW", "QUARANTINE", "COMPENSATE", "RETAIN RESIDUAL"], [RED, AMBER, VIOLET, AMBER, RESIDUAL], x=2.1, y=1.0, width=2.2, scale=0.56)
            owner = self.badge("OWNER + RECEIPT", RESIDUAL, 2.8).shift(RIGHT * 2.8 + DOWN * 1.4)
            return VGroup(frame, attacks, outcomes, owner, self.arrows_between(attacks, [outcomes[0]] * len(attacks), [RED] * len(attacks), dashed=True), self.arrows_between(outcomes[0], outcomes, [RED, AMBER, VIOLET, AMBER, RESIDUAL]))
        if index == 12:
            frame = self.frame("DESIGN RATIONALE · ARGUMENT SUPPORT", BLUE)
            local = self.panel("LOCAL HARNESS + LEDGER", GREEN, 3.0, 1.5).shift(LEFT * 3.1)
            stamp = self.badge("SUPPORT STATE", AMBER, 2.3).shift(LEFT * 3.1 + DOWN * 1.35)
            targets = self.pills(["GENERAL ROBUSTNESS", "SECURE DEPLOYMENT", "PROOF TARGETS OPEN"], [RED, RED, MUTED], x=2.3, y=0.8, width=2.6, scale=0.58)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, stamp, targets, boundary, *[Cross(x, stroke_color=RED, stroke_width=2) for x in targets[:2]])
        if index == 13:
            frame = self.frame("HANDOFF AIRLOCK · NO RELEASE AUTHORITY", AMBER)
            record = self.panel("AML RECORD", BLUE, 2.6, 1.45).shift(LEFT * 3.2)
            checks = self.pills(["IDENTITY", "AUTHORITY", "VERSION", "REQUIRED CHECKS", "RESIDUAL OWNER"], [BLUE, AMBER, BLUE, GREEN, RESIDUAL], x=0.6, y=0.95, width=2.1, scale=0.57)
            exits = self.pills(["EMPIRICAL EFFECTIVENESS", "RELEASE AUTHORITY"], [RED, RED], x=2.6, y=-1.1, width=2.8, scale=0.6, direction=RIGHT)
            return VGroup(frame, record, checks, exits, self.arrows_between(record, checks, [AMBER] * len(checks)), *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in exits])
        if index == 14:
            frame = self.frame("ADAPTIVE LOOP · JOINT METRICS", GREEN)
            attacker = self.panel("ATTACKER SEES DEFENSE", RED, 2.8, 1.4).shift(LEFT * 3.3)
            metrics = self.pills(["CLEAN UTILITY", "ATTACKED UTILITY", "DETECTION", "FALSE POSITIVES", "RECOVERY", "COST"], [GREEN, RED, VIOLET, RED, GREEN, RESIDUAL], x=1.8, y=1.0, width=2.2, scale=0.56)
            return VGroup(frame, attacker, metrics, self.arrows_between(attacker, metrics, [AMBER] * len(metrics)), self.badge("UPDATE TOGETHER", AMBER, 2.5).shift(LEFT * 3.0 + DOWN * 1.4))
        if index == 15:
            frame = self.frame("LOCAL LEDGER · NO MEDIA PROMOTION", RED)
            local = self.panel("LOCAL ATTACK LEDGER", GREEN, 3.0, 1.5).shift(LEFT * 3.2)
            claims = self.pills(["IMPLEMENTATION PROOF", "USEFUL DEPLOYMENT", "REAL-WORLD ENFORCEMENT"], [RED, RED, RED], x=2.1, y=0.9, width=2.6, scale=0.58)
            boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, claims, boundary, *[Cross(x, stroke_color=RED, stroke_width=2.5) for x in claims])
        if index == 16:
            frame = self.frame("SOURCE + DERIVATIVE · SAME EVIDENCE CEILING", BLUE)
            source = self.panel("LIVE CHAPTER", BLUE, 2.7, 1.4).shift(LEFT * 3.2)
            derivative = self.panel("VISUAL LEDGER", AMBER, 2.7, 1.4).shift(RIGHT * 2.0)
            line = Arrow(source.get_right(), derivative.get_left(), color=BLUE, stroke_width=3, buff=0.1)
            return VGroup(frame, source, derivative, line, self.badge("SAME SUPPORT STATE", MUTED, 2.75).shift(DOWN * 1.45))
        if index == 17:
            frame = self.frame("DESIGN RATIONALE · NO BROAD RESULT", RED)
            support = self.panel("ARGUMENT SUPPORT", AMBER, 2.8, 1.5).shift(LEFT * 3.3)
            nonclaims = self.pills(["NO EMPIRICAL", "NO DEPLOYMENT", "NO SAFETY", "NO TRANSFER", "NO AGI / ASI"], [RED] * 5, x=1.7, y=0.85, width=2.1, scale=0.56)
            return VGroup(frame, support, nonclaims, self.arrows_between(support, nonclaims, [RED] * len(nonclaims)), *[Cross(x, stroke_color=RED, stroke_width=2) for x in nonclaims])
        frame = self.frame("NEXT · PRIVACY + DATA RIGHTS", AMBER)
        receipt = self.panel("SEALED AML RECEIPT", GREEN, 3.0, 1.45).shift(LEFT * 3.5)
        rights = self.panel("RIGHTS / FLOW LEDGER", VIOLET, 2.9, 1.45).shift(RIGHT * 1.9)
        lanes = self.pills(["COLLECTION", "INFERENCE", "MEMORY", "TRAINING", "RETENTION", "EXECUTABLE RIGHTS"], [RED, RED, RESIDUAL, AMBER, MUTED, VIOLET], x=2.25, y=-1.05, width=2.0, scale=0.53)
        boundary = DashedLine(UP * 2.2, DOWN * 2.2, color=RED, stroke_width=3).shift(RIGHT * 0.0)
        return VGroup(frame, receipt, rights, lanes, boundary, Arrow(receipt.get_right(), rights.get_left(), color=AMBER, stroke_width=3, buff=0.1), self.arrows_between(rights, lanes, [VIOLET] * len(lanes), dashed=True))


__all__ = ["AdversarialMachineLearningAttackSurfaceGeneration2"]
