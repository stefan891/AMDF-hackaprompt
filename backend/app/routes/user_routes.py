"""User-centric endpoints."""

from flask import Blueprint, jsonify, g

from app.auth.decorators import token_required
from app.models.event import Event
from app.models.invitation import Invitation

user_bp = Blueprint("users", __name__)


@user_bp.route("/me/events", methods=["GET"])
@token_required
def my_events():
    """Return all events where current user is creator OR accepted invitee."""
    user = g.current_user

    # Events I created
    created = Event.query.filter_by(creator_id=user.id).all()

    # Events I accepted
    accepted_invitations = Invitation.query.filter_by(
        user_id=user.id,
        status="accepted",
    ).all()
    accepted_event_ids = [inv.event_id for inv in accepted_invitations]
    invited = Event.query.filter(Event.id.in_(accepted_event_ids)).all()

    # Merge without duplicates
    seen_ids = set()
    events = []
    for e in list(created) + list(invited):
        if e.id not in seen_ids:
            events.append(e.to_dict())
            seen_ids.add(e.id)

    return jsonify({"events": events}), 200
