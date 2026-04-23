"""Automatic timeslot generation helpers."""

from datetime import datetime, timedelta

from app.models.timeslot import TimeSlot

DEFAULT_SLOT_DURATION_MINUTES = 60
DEFAULT_FULLDAY_DAYS = 1


def generate_slots(event_type: str, start: datetime, end: datetime):
    """Generate TimeSlot objects (not yet committed) between start and end.

    - event_type "fullday": one slot per calendar day
    - event_type "time":    one slot per hour (configurable)
    """
    slots = []

    if event_type == "fullday":
        current = start.replace(hour=0, minute=0, second=0, microsecond=0)
        while current < end:
            next_day = current + timedelta(days=DEFAULT_FULLDAY_DAYS)
            slots.append(
                TimeSlot(
                    slot_start=current,
                    slot_end=next_day,
                    label=current.strftime("%A %d %B %Y"),
                )
            )
            current = next_day
    else:
        delta = timedelta(minutes=DEFAULT_SLOT_DURATION_MINUTES)
        current = start
        while current + delta <= end:
            slot_end = current + delta
            slots.append(
                TimeSlot(
                    slot_start=current,
                    slot_end=slot_end,
                    label=(
                        f"{current.strftime('%H:%M')}"
                        f"\u2013{slot_end.strftime('%H:%M')}"
                    ),
                )
            )
            current = slot_end

    return slots
