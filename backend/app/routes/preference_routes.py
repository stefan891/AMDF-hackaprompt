"""Preference (vote) endpoints."""

from flask import Blueprint, request, jsonify, g

from app.auth.decorators import token_required, participant_required
from app.services.preference_service import submit_preference

preference_bp = Blueprint("preferences", __name__)


@preference_bp.route("/<int:event_id>/preference", methods=["POST"])
@token_required
@participant_required
def vote(event_id):
    """Submit or update a preference for one timeslot.

    JSON body: { "timeslot_id": 1, "value": "available" }
    Only creator and accepted invitees can vote.
    """
    data = request.get_json(silent=True) or {}
    result, error = submit_preference(
        event_id=event_id,
        user=g.current_user,
        timeslot_id=data.get("timeslot_id"),
        value=data.get("value"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200
