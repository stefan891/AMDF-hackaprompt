"""CRUD endpoints for events."""

from flask import Blueprint, request, jsonify, g

from app.extensions import db
from app.auth.decorators import (
    token_required,
    creator_required,
    participant_required,
)
from app.services.event_service import (
    create_event,
    get_event_detail,
    get_event_overview,
    set_event_quorum,
)
from app.services.invitation_service import (
    add_invitee,
    remove_invitee,
)

event_bp = Blueprint("events", __name__)


# ── Anyone logged in can create ────────────────────────────

@event_bp.route("", methods=["POST"])
@token_required
def create():
    """Create a new event with timeslots and invitees."""
    data = request.get_json(silent=True) or {}
    event, errors = create_event(g.current_user, data)
    if errors:
        return jsonify({"errors": errors}), 400
    return jsonify(event.to_dict(include_slots=True)), 201


# ── Only participants (creator + accepted invitees) ────────

@event_bp.route("/<int:event_id>", methods=["GET"])
@token_required
@participant_required
def detail(event_id):
    """Return full event details with slots and preferences."""
    event_data, error = get_event_detail(event_id, g.current_user)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(event_data), 200


@event_bp.route("/<int:event_id>/overview", methods=["GET"])
@token_required
@participant_required
def overview(event_id):
    """Aggregated slot-by-slot vote counts."""
    result, error = get_event_overview(event_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(result), 200


# ── Only the creator ───────────────────────────────────────

@event_bp.route("/<int:event_id>/quorum", methods=["POST"])
@token_required
@creator_required
def quorum(event_id):
    """Set quorum and return slots that meet it."""
    data = request.get_json(silent=True) or {}
    result, error = set_event_quorum(
        event_id,
        g.current_user,
        data.get("quorum"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200


@event_bp.route("/<int:event_id>/invite", methods=["POST"])
@token_required
@creator_required
def invite(event_id):
    """Add a new invitee.

    JSON body: { "email": "someone@example.com" }
    """
    data = request.get_json(silent=True) or {}
    result, error = add_invitee(
        event_id,
        g.current_user,
        data.get("email"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 201


@event_bp.route("/<int:event_id>/invite", methods=["DELETE"])
@token_required
@creator_required
def uninvite(event_id):
    """Remove an invitee.

    JSON body: { "email": "someone@example.com" }
    """
    data = request.get_json(silent=True) or {}
    result, error = remove_invitee(
        event_id,
        g.current_user,
        data.get("email"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200
