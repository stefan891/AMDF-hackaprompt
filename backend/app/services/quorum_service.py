"""Quorum evaluation logic."""


def check_quorum(event, slot_overview: list) -> bool:
    """Return True if at least one slot meets the event's quorum."""
    if event.quorum is None:
        return False

    for slot in slot_overview:
        if slot["counts"]["available"] >= event.quorum:
            return True

    return False
