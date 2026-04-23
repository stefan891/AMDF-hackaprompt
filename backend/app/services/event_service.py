"""Business logic for event creation, details, overview."""

from datetime import datetime

from app.extensions import db
from app.models.event import Event
from app.models.timeslot import TimeSlot
from app.models.user import User
from app.models.invitation import Invitation
from app.services.slot_service import generate_slots
from app.services.quorum_service import check_quorum


def create_event(creator, data: dict):
    """Validate input, create Event + TimeSlots + Invitations.

    Returns (event, errors).
    """
    errors = []

    title = data.get("title")
    if not title:
        errors.append("title is required")

    event_type = data.get("event_type", "time")
    start_str = data.get("start")
    end_str = data.get("end")

    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
    except (TypeError, ValueError):
        errors.append("Invalid start/end datetime format")
        return None, errors

    if errors:
        return None, errors

    event = Event(
        title=title,
        description=data.get("description", ""),
        creator_id=creator.id,
        event_type=event_type,
        start=start,
        end=end,
    )
    db.session.add(event)
    db.session.flush()

    # ── Slots ──────────────────────────────────────────────
    raw_slots = data.get("slots", [])
    if raw_slots:
        for s in raw_slots:
            ts = TimeSlot(
                event_id=event.id,
                slot_start=datetime.fromisoformat(s["slot_start"]),
                slot_end=datetime.fromisoformat(s["slot_end"]),
                label=s.get("label"),
            )
            db.session.add(ts)
    else:
        generated = generate_slots(event_type, start, end)
        for ts in generated:
            ts.event_id = event.id
            db.session.add(ts)

    # ── Invitations ────────────────────────────────────────
    invitee_emails = data.get("invitees", [])
    for email in invitee_emails:
        if email == creator.email:
            continue

        user = User.query.filter_by(email=email).first()
        invitation = Invitation(
            event_id=event.id,
            user_id=user.id if user else None,
            email=email,
            status="pending",
        )
        db.session.add(invitation)
        # TODO: send email notification to invitee

    db.session.commit()
    return event, None


def get_event_detail(event_id, current_user):
    """Return event dict with slots, preferences, and invitations.

    Returns (data_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"

    data = event.to_dict(include_slots=True, include_preferences=True)
    data["creator"] = event.creator.to_dict()
    data["invitations"] = [inv.to_dict() for inv in event.invitations]
    data["is_creator"] = (current_user.id == event.creator_id)
    data["can_edit"] = data["is_creator"]

    return data, None


def get_event_overview(event_id):
    """Aggregate preferences per slot + recommend best slot.

    Returns (result_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"

    overview = []
    best_slot = None
    best_score = -1

    for slot in event.timeslots:
        prefs = slot.preferences.all()
        counts = {"available": 0, "maybe": 0, "unavailable": 0}
        for p in prefs:
            counts[p.value] = counts.get(p.value, 0) + 1

        score = counts["available"] * 2 + counts["maybe"]

        slot_data = {
            **slot.to_dict(),
            "counts": counts,
            "score": score,
        }
        overview.append(slot_data)

        if score > best_score:
            best_score = score
            best_slot = slot_data

    quorum_met = check_quorum(event, overview)

    return {
        "event_id": event_id,
        "slots": overview,
        "recommended": best_slot,
        "quorum_met": quorum_met,
    }, None


def set_event_quorum(event_id, current_user, quorum_value):
    """Set quorum on an event, return slots meeting it."""
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"
    if event.creator_id != current_user.id:
        return None, "Only the creator can set quorum"
    if quorum_value is None or not isinstance(quorum_value, int):
        return None, "quorum must be an integer"

    event.quorum = quorum_value
    db.session.commit()

    result, _ = get_event_overview(event_id)
    qualifying = [
        s
        for s in result["slots"]
        if s["counts"]["available"] >= quorum_value
    ]

    return {
        "quorum": quorum_value,
        "qualifying_slots": qualifying,
        "recommended": result["recommended"],
    }, None
