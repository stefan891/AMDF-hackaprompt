"""Invitation management endpoints."""

from flask import Blueprint, request, jsonify, g

from app.auth.decorators import token_required
from app.services.invitation_service import (
    respond_to_invitation,
    get_user_invitations,
)

invitation_bp = Blueprint("invitations", __name__)


@invitation_bp.route("/<int:event_id>/respond", methods=["POST"])
@token_required
def respond(event_id):
    """Accept or decline an invitation.

    JSON body: { "status": "accepted" | "declined" }
    """
    data = request.get_json(silent=True) or {}
    result, error = respond_to_invitation(
        event_id,
        g.current_user,
        data.get("status"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200


@invitation_bp.route("/mine", methods=["GET"])
@token_required
def my_invitations():
    """Return all invitations for the current user."""
    result, error = get_user_invitations(g.current_user)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"invitations": result}), 200
