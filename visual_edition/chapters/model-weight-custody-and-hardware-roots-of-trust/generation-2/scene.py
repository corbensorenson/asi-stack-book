"""Generation-2 visual abstract for model-weight custody and hardware roots of trust.

The visual world is a custody control room.  A model-family ledger stays on
screen while artifacts cross storage, key, hardware, vendor, operator, and
recipient boundaries.  Gates are explicit: an attestation or signature is
never allowed to stand in for the effect-complete lifecycle it does not test.
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


class ModelWeightCustodyHardwareRootsOfTrustGeneration2(AsiScene):
    """A chapter-specific visual explanation of model-family custody closure."""

    TARGET_DURATION = 296.49
    ENDS = [
        19.22, 28.925, 45.495, 64.465, 83.36, 91.515, 111.185, 123.93,
        143.05, 146.405, 163.225, 174.27, 194.15, 209.17, 224.09,
        239.695, 259.44, 267.77, 283.815, 296.49,
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
            line = DashedLine if dashed else Arrow
            kwargs = {"color": color, "stroke_width": 2}
            if not dashed:
                kwargs["buff"] = 0.08
            arrows.append(line(source.get_right(), target.get_left(), **kwargs))
        return VGroup(*arrows)

    def construct(self) -> None:
        self.current = VGroup()
        for index in range(1, 21):
            next_scene = self.scene_for(index)
            animations = [FadeIn(next_scene)] if not self.current else [
                AnimationGroup(FadeOut(self.current), FadeIn(next_scene), lag_ratio=0)
            ]
            self.play_beat(index, *animations, settle=0.85 if index in (1, 3, 8, 13, 19, 20) else 0.55)
            self.current = next_scene

    def scene_for(self, index: int) -> VGroup:
        if index == 1:
            frame = self.frame("CAPABILITY-BEARING STATE SPREADS", RED)
            vault = self.panel("CANONICAL VAULT", AMBER, 2.4, 1.35).shift(LEFT * 3.8)
            family = self.pills(["WEIGHTS", "OPTIMIZER", "ADAPTERS", "QUANTIZATION", "CHECKPOINTS", "CACHE", "RECOVERY", "DERIVATIVES"],
                                [BLUE, AMBER, VIOLET, MUTED, BLUE, RESIDUAL, RED, RED], x=2.0, y=1.1, width=2.0, scale=0.52)
            fan = self.arrows_between(vault, list(family), [BLUE, AMBER, VIOLET, MUTED, BLUE, RESIDUAL, RED, RED], dashed=True)
            return VGroup(frame, vault, family, fan, self.badge("ONE MODEL → MANY CUSTODY SURFACES", RED, 3.9).shift(LEFT * 1.0 + DOWN * 1.65))
        if index == 2:
            frame = self.frame("TRUST BOUNDARIES MULTIPLY", RED)
            nodes = self.pills(["STORAGE", "KEYS", "HARDWARE", "VENDOR", "OPERATOR", "ORGANIZATION"], [BLUE, AMBER, VIOLET, MUTED, RED, RESIDUAL], x=-2.4, y=1.35, width=2.0, scale=0.58)
            core = self.panel("WEIGHT FAMILY", AMBER, 2.4, 1.3).shift(RIGHT * 2.7)
            return VGroup(frame, nodes, core, self.arrows_between(core, list(nodes), [BLUE, AMBER, VIOLET, MUTED, RED, RESIDUAL], dashed=True), self.badge("CLOSURE IS NOT ASSUMED", RED, 2.9).shift(RIGHT * 2.4 + DOWN * 1.45))
        if index == 3:
            frame = self.frame("PROSPECTIVE ASSET CLOSURE", GREEN)
            contract = self.panel("CUSTODY CONTRACT", GREEN, 3.1, 1.55).shift(LEFT * 2.8)
            fields = self.pills(["IDENTITY", "HOLDER", "PURPOSE", "STATE", "DESCENDANTS", "TERMINAL OWNER"], [BLUE, AMBER, VIOLET, MUTED, RED, RESIDUAL], x=1.9, y=1.2, width=2.0, scale=0.58)
            return VGroup(frame, contract, fields, self.arrows_between(contract, list(fields), [BLUE, AMBER, VIOLET, MUTED, RED, RESIDUAL]), self.badge("DECLARE BEFORE THE TRANSITION", GREEN, 3.3).shift(LEFT * 2.4 + DOWN * 1.5))
        if index == 4:
            frame = self.frame("LIFECYCLE ROLES · NO UNIVERSAL BIT", BLUE)
            stages = self.pills(["LOAD", "USE", "SERVE", "EXTRACT", "RELEASE"], [BLUE, AMBER, VIOLET, RED, RESIDUAL], x=-3.6, y=1.25, width=1.8, scale=0.62)
            roles = self.pills(["ATTESTER", "VERIFIER", "RELYING PARTY", "POLICY"], [GREEN, BLUE, AMBER, VIOLET], x=1.2, y=1.0, width=2.0, scale=0.62)
            return VGroup(frame, stages, roles, self.arrows_between(stages, [roles] * len(stages), [BLUE, AMBER, VIOLET, RED, RESIDUAL], dashed=True), self.badge("EACH STAGE HAS ITS OWN AUTHORITY", BLUE, 3.7).shift(RIGHT * 1.1 + DOWN * 1.5))
        if index == 5:
            frame = self.frame("EFFECT-COMPLETE CUSTODY CLOSURE", AMBER)
            ledger = self.panel("HOLDER LEDGER", AMBER, 2.6, 1.45).shift(LEFT * 3.4)
            closure = self.pills(["BACKUPS", "RECOVERY", "RECIPIENTS", "DESCENDANTS", "REVOCATION", "SANITIZATION"], [MUTED, RED, BLUE, RED, RESIDUAL, GREEN], x=1.8, y=1.15, width=2.05, scale=0.56)
            return VGroup(frame, ledger, closure, self.arrows_between(ledger, list(closure), [MUTED, RED, BLUE, RED, RESIDUAL, GREEN], dashed=True), self.badge("BLOCK IF A MODELED PREDICATE FAILS", RED, 3.7).shift(LEFT * 1.3 + DOWN * 1.55))
        if index == 6:
            frame = self.frame("SHORTCUTS ARE NOT CLOSURE", RED)
            shortcuts = self.pills(["ENCRYPTION", "SIGNATURE", "SECURITY LEVEL", "ATTESTATION"], [RED, RED, RED, RED], x=-2.2, y=1.0, width=2.2, scale=0.64)
            target = self.panel("EFFECT-COMPLETE RECORD", GREEN, 3.3, 1.45).shift(RIGHT * 2.6)
            return VGroup(frame, shortcuts, target, self.arrows_between(shortcuts, [target] * len(shortcuts), [RED] * len(shortcuts), dashed=True), *[Cross(item, stroke_color=RED, stroke_width=2.5) for item in shortcuts], self.badge("LABEL ≠ LIFECYCLE", RED, 2.3).shift(LEFT * 2.2 + DOWN * 1.45))
        if index == 7:
            frame = self.frame("FINITE ROUTER · BOUNDED CASES", BLUE)
            records = self.pills(["LOAD", "REPAIR", "REFRESH", "OBSERVE", "RELEASE"], [BLUE, AMBER, VIOLET, GREEN, RESIDUAL], x=-3.4, y=1.2, width=1.8, scale=0.6)
            router = self.panel("DETERMINISTIC ROUTER", BLUE, 2.8, 1.45).shift(LEFT * 0.1)
            outcomes = self.pills(["ADMIT", "REVIEW", "BLOCK", "REJECT"], [GREEN, AMBER, RED, RED], x=3.15, y=1.0, width=1.75, scale=0.6)
            return VGroup(frame, records, router, outcomes, self.arrows_between(records, [router] * len(records), [BLUE, AMBER, VIOLET, GREEN, RESIDUAL]), self.arrows_between(router, list(outcomes), [GREEN, AMBER, RED, RED]))
        if index == 8:
            frame = self.frame("FORMAL TARGETS · ENCODED SCOPE", VIOLET)
            manifest = self.panel("MANIFEST", AMBER, 2.3, 1.3).shift(LEFT * 3.7)
            theorem = self.panel("LEAN TARGETS", VIOLET, 2.4, 1.3).shift(LEFT * 0.4)
            reject = self.panel("REJECTING MUTATIONS", RED, 2.7, 1.3).shift(RIGHT * 3.1)
            return VGroup(frame, manifest, theorem, reject, Arrow(manifest.get_right(), theorem.get_left(), color=AMBER, stroke_width=3, buff=0.1), Arrow(theorem.get_right(), reject.get_left(), color=RED, stroke_width=3, buff=0.1), self.badge("FORMAL ROUTE ≠ REAL CUSTODY", MUTED, 3.2).shift(DOWN * 1.5))
        if index == 9:
            frame = self.frame("EVIDENCE CEILING · REAL SURFACES OUTSIDE", RED)
            local = self.panel("LOCAL ENCLOSURE", BLUE, 2.7, 1.45).shift(LEFT * 3.4)
            surfaces = self.pills(["REAL WEIGHT", "KMS / HSM", "TEE", "PLAINTEXT LOAD", "ATTESTATION", "SECURITY METRIC"], [RED] * 6, x=1.9, y=1.15, width=2.0, scale=0.55)
            boundary = DashedLine(UP * 2.15, DOWN * 2.15, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, local, surfaces, boundary, *[Cross(item, stroke_color=RED, stroke_width=2) for item in surfaces])
        if index == 10:
            frame = self.frame("CLOSURE ESCAPE", RED)
            approved = self.panel("APPROVED RECORD", GREEN, 2.7, 1.35).shift(LEFT * 3.1)
            escape = self.panel("UNMODELED COPY", RED, 2.7, 1.35).shift(RIGHT * 2.7)
            return VGroup(frame, approved, escape, Arrow(approved.get_right(), escape.get_left(), color=RED, stroke_width=3, buff=0.1), Cross(escape, stroke_color=RED, stroke_width=3), self.badge("DESCENDANT OUTSIDE LEDGER", RED, 3.2).shift(DOWN * 1.5))
        if index == 11:
            frame = self.frame("IDENTITY SUBSTITUTION", RED)
            expected = self.panel("EXPECTED IDENTITY", BLUE, 2.8, 1.4).shift(LEFT * 3.2)
            actual = self.panel("SUBSTITUTED ARTIFACT", RED, 2.9, 1.4).shift(RIGHT * 2.6)
            ids = self.pills(["MODEL", "TOKENIZER", "POLICY", "ENVIRONMENT", "HOLDER"], [RED] * 5, x=0.0, y=-0.9, width=1.9, scale=0.58)
            return VGroup(frame, expected, actual, ids, Arrow(expected.get_right(), actual.get_left(), color=RED, stroke_width=3, buff=0.1), Cross(actual, stroke_color=RED, stroke_width=3))
        if index == 12:
            frame = self.frame("KEY LIFECYCLE · FRESHNESS IS STATE", AMBER)
            lifecycle = self.pills(["ISSUE", "ROTATE", "REVOKE", "RECOVER", "BREAK-GLASS"], [GREEN, AMBER, RED, RESIDUAL, RED], x=-2.7, y=1.1, width=1.9, scale=0.6)
            drift = self.panel("STALE TRUST ANCHOR", RED, 2.9, 1.4).shift(RIGHT * 2.5)
            return VGroup(frame, lifecycle, drift, self.arrows_between(lifecycle, [drift] * len(lifecycle), [GREEN, AMBER, RED, RESIDUAL, RED], dashed=True), self.badge("FRESHNESS GATE", AMBER, 2.4).shift(RIGHT * 2.5 + DOWN * 1.45))
        if index == 13:
            frame = self.frame("DESIGN RATIONALE · SUPPORT STATE", BLUE)
            record = self.panel("FINITE CUSTODY RECORD", GREEN, 3.1, 1.45).shift(LEFT * 3.2)
            support = self.badge("ARGUMENT SUPPORT", AMBER, 2.8).shift(LEFT * 3.2 + DOWN * 1.35)
            targets = self.pills(["EMPIRICAL EFFECT", "DEPLOYMENT", "PRIVACY", "SAFETY", "TRANSFER"], [RED] * 5, x=2.2, y=1.0, width=2.2, scale=0.58)
            boundary = DashedLine(UP * 2.15, DOWN * 2.15, color=RED, stroke_width=3).shift(RIGHT * 0.0)
            return VGroup(frame, record, support, targets, boundary, *[Cross(item, stroke_color=RED, stroke_width=2) for item in targets])
        if index == 14:
            frame = self.frame("INVALID ATTESTATION → BLOCK", RED)
            request = self.panel("WEIGHT LOAD REQUEST", BLUE, 2.8, 1.35).shift(LEFT * 3.1)
            gate = self.panel("ATTESTATION GATE", RED, 2.8, 1.35).shift(LEFT * 0.1)
            blocked = self.panel("BLOCK", RED, 2.2, 1.2).shift(RIGHT * 3.0)
            return VGroup(frame, request, gate, blocked, Arrow(request.get_right(), gate.get_left(), color=BLUE, stroke_width=3, buff=0.1), Arrow(gate.get_right(), blocked.get_left(), color=RED, stroke_width=3, buff=0.1), Cross(gate, stroke_color=RED, stroke_width=3))
        if index == 15:
            frame = self.frame("COMPLETE RECORD → BOUNDED LOAD", GREEN)
            record = self.panel("CURRENT RECORD", GREEN, 2.8, 1.4).shift(LEFT * 3.3)
            load = self.panel("BOUNDED LOAD", BLUE, 2.6, 1.3).shift(RIGHT * 0.0)
            no_deploy = self.badge("NO DEPLOYMENT AUTHORITY", RED, 3.2).shift(RIGHT * 2.7 + DOWN * 1.3)
            return VGroup(frame, record, load, no_deploy, Arrow(record.get_right(), load.get_left(), color=GREEN, stroke_width=3, buff=0.1), Arrow(load.get_right(), no_deploy.get_left(), color=RED, stroke_width=2.5, buff=0.1), Cross(no_deploy, stroke_color=RED, stroke_width=2.5))
        if index == 16:
            frame = self.frame("MEDIA CUSTODY · NONPROMOTION", MUTED)
            source = self.panel("WEIGHT / RECORD", BLUE, 2.8, 1.4).shift(LEFT * 3.2)
            media = self.pills(["VISUAL", "CAPTION", "TRANSCRIPT", "THUMBNAIL"], [MUTED, MUTED, MUTED, MUTED], x=0.5, y=1.0, width=1.8, scale=0.6)
            release = self.panel("RELEASE", RED, 2.3, 1.2).shift(RIGHT * 3.3)
            return VGroup(frame, source, media, release, self.arrows_between(source, list(media), [MUTED] * len(media), dashed=True), self.arrows_between(media, [release] * len(media), [RED] * len(media), dashed=True), Cross(release, stroke_color=RED, stroke_width=3))
        if index == 17:
            frame = self.frame("SOURCE + DERIVATIVE · SAME CEILING", BLUE)
            source = self.panel("LIVE CHAPTER", BLUE, 2.7, 1.35).shift(LEFT * 3.2)
            derivative = self.panel("VISUAL DERIVATIVE", AMBER, 2.8, 1.35).shift(RIGHT * 2.3)
            return VGroup(frame, source, derivative, Arrow(source.get_right(), derivative.get_left(), color=BLUE, stroke_width=3, buff=0.1), self.badge("EXPLANATION PRESERVES NONCLAIMS", MUTED, 3.6).shift(DOWN * 1.45))
        if index == 18:
            frame = self.frame("SUPPORT STAMP · NONCLAIM FAN", AMBER)
            stamp = self.badge("SUPPORT STATE", AMBER, 2.5).shift(LEFT * 3.4)
            fan = self.pills(["NO EMPIRICAL", "NO SAFETY", "NO TRANSFER", "NO AGI / ASI"], [RED] * 4, x=1.6, y=1.0, width=2.2, scale=0.6)
            return VGroup(frame, stamp, fan, self.arrows_between(stamp, list(fan), [RED] * len(fan), dashed=True), *[Cross(item, stroke_color=RED, stroke_width=2) for item in fan])
        if index == 19:
            frame = self.frame("OPEN-WEIGHT RELEASE · IRREVERSIBLE COPIES", RED)
            origin = self.panel("ORIGIN RELEASE", AMBER, 2.6, 1.35).shift(LEFT * 3.7)
            copies = self.pills(["MIRROR", "RECIPIENT", "FORK", "DISTILL", "SERVE"], [RED, RED, RED, RESIDUAL, VIOLET], x=1.1, y=1.2, width=1.8, scale=0.6)
            return VGroup(frame, origin, copies, self.arrows_between(origin, list(copies), [RED] * 4 + [VIOLET], dashed=True), self.badge("RECALL IS NOT A CONTROL", RED, 2.8).shift(LEFT * 2.8 + DOWN * 1.45))
        frame = self.frame("POST-RELEASE CUSTODY DIVERGENCE", RESIDUAL)
        released = self.panel("RELEASED FAMILY", RESIDUAL, 2.8, 1.4).shift(LEFT * 3.5)
        divergence = self.pills(["UNKNOWN HOLDERS", "UNKNOWN USE", "UNKNOWN DERIVATIVES", "OWNED RESIDUAL"], [RED, RED, RED, RESIDUAL], x=1.9, y=1.0, width=2.4, scale=0.58)
        return VGroup(frame, released, divergence, self.arrows_between(released, list(divergence), [RED, RED, RED, RESIDUAL], dashed=True), self.badge("TERMINAL OWNER MUST BE NAMED", RESIDUAL, 3.3).shift(LEFT * 1.5 + DOWN * 1.5))
