"""Business logic for submitting / updating preferences."""

from app.extensions import db
from app.models.preference import Preference
from app.models.timeslot import TimeSlot

ALLOWED_VALUES = {"available", "maybe", "unavailable"}


def submit_preference(event_id, user, timeslot_id, value):
    """Create or update a Preference.

    Returns (result_dict, error_string).
    """
    if value not in ALLOWED_VALUES:
        return None, f"value must be one of {ALLOWED_VALUES}"

    slot = TimeSlot.query.get(timeslot_id)
    if not slot or slot.event_id != event_id:
        return None, "Invalid timeslot for this event"

    pref = Preference.query.filter_by(
        user_id=user.id,
        timeslot_id=timeslot_id,
    ).first()

    if pref:
        pref.value = value
    else:
        pref = Preference(
            event_id=event_id,
            user_id=user.id,
            timeslot_id=timeslot_id,
            value=value,
        )
        db.session.add(pref)

    db.session.commit()

    return pref.to_dict(), None
