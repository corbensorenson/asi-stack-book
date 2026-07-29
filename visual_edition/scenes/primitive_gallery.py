"""Render entrypoint for the P7.3 reusable-primitive compatibility sheet."""

from visual_edition.lib.asi_visuals import PrimitiveGallery as _PrimitiveGallery


class PrimitiveGallery(_PrimitiveGallery):
    """Module-local entrypoint discovered by the Manim CLI."""


__all__ = ["PrimitiveGallery"]
