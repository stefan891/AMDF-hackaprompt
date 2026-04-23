"""Route decorators for authentication & authorisation."""

import functools
from datetime import datetime, timezone

import jwt
from flask import request, jsonify, current_app, g

from app.models.user import User


def token_required(f):
    """Extracts & validates JWT, sets g.current_user."""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or malformed token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=[current_app.config["JWT_ALGORITHM"]],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = User.query.get(payload.get("user_id"))
        if user is None:
            return jsonify({"error": "User not found"}), 401

        g.current_user = user
        return f(*args, **kwargs)

    return decorated


def create_jwt(user) -> str:
    """Issue a JWT for the given User."""
    now = datetime.now(timezone.utc).timestamp()
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": now + current_app.config["JWT_EXPIRATION_HOURS"] * 3600,
        "iat": now,
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )


# ── Permission helpers ─────────────────────────────────────

def is_event_creator(user, event) -> bool:
    """Check if the user created this event."""
    return user.id == event.creator_id


def is_event_participant(user, event) -> bool:
    """Check if the user is creator OR an accepted invitee."""
    if user.id == event.creator_id:
        return True

    from app.models.invitation import Invitation
    invitation = Invitation.query.filter_by(
        event_id=event.id,
        user_id=user.id,
        status="accepted",
    ).first()

    return invitation is not None


def is_event_invitee(user, event) -> bool:
    """Check if the user has ANY invitation (any status)."""
    if user.id == event.creator_id:
        return True

    from app.models.invitation import Invitation
    invitation = Invitation.query.filter_by(
        event_id=event.id,
        user_id=user.id,
    ).first()

    return invitation is not None


def creator_required(f):
    """Decorator – ensures g.current_user is the event creator.
    Must be used AFTER @token_required.
    Expects 'event_id' in route params."""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        from app.models.event import Event

        event_id = kwargs.get("event_id")
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        if not is_event_creator(g.current_user, event):
            return jsonify({"error": "Only the event creator can do this"}), 403

        g.event = event
        return f(*args, **kwargs)

    return decorated


def participant_required(f):
    """Decorator – ensures g.current_user is creator or accepted invitee.
    Must be used AFTER @token_required.
    Expects 'event_id' in route params."""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        from app.models.event import Event

        event_id = kwargs.get("event_id")
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        if not is_event_participant(g.current_user, event):
            return jsonify({"error": "You are not a participant of this event"}), 403

        g.event = event
        return f(*args, **kwargs)

    return decorated
