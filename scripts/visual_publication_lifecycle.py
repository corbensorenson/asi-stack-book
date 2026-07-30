#!/usr/bin/env python3
"""Shared publication-lifecycle helpers for visual chapter regeneration."""

from __future__ import annotations

import copy


PUBLISHED_STATES = {"published_current", "stale", "superseded"}


def preserve_predecessor_projection(
    prior_packet: dict | None,
    packet: dict,
) -> dict:
    """Carry an existing platform identity into a regenerated packet as stale.

    Local regeneration must never silently erase a published predecessor or
    leave its old embed marked current. Unpublished packets keep the freshly
    generated blank projection.
    """

    if not prior_packet:
        return packet
    prior_youtube = prior_packet.get("youtube", {})
    if (
        prior_youtube.get("publication_state") not in PUBLISHED_STATES
        or not prior_youtube.get("video_id")
        or int(prior_youtube.get("generation", 0)) < 1
    ):
        return packet
    updated = copy.deepcopy(packet)
    updated["youtube"] = copy.deepcopy(prior_youtube)
    updated["youtube"]["publication_state"] = "stale"
    updated["quarto_embed"] = copy.deepcopy(prior_packet["quarto_embed"])
    updated["quarto_embed"]["state"] = "historical_removed"
    return updated


def supersession_required(packet: dict) -> bool:
    youtube = packet.get("youtube", {})
    return (
        youtube.get("publication_state") == "stale"
        and bool(youtube.get("video_id"))
        and int(youtube.get("generation", 0)) >= 1
    )
