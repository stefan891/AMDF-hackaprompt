"""Business logic for invitation management."""

from datetime import datetime, timezone

from app.extensions import db
from app.models.invitation import Invitation
from app.models.event import Event
from app.models.user import User


def respond_to_invitation(event_id, user, status):
    """Accept or decline an invitation.

    Returns (result_dict, error_string).
    """
    if status not in ("accepted", "declined"):
        return None, "status must be 'accepted' or 'declined'"

    invitation = Invitation.query.filter_by(
        event_id=event_id,
        user_id=user.id,
    ).first()

    if not invitation:
        # Try matching by email (user registered after being invited)
        invitation = Invitation.query.filter_by(
            event_id=event_id,
            email=user.email,
            user_id=None,
        ).first()
        if invitation:
            invitation.user_id = user.id

    if not invitation:
        return None, "No invitation found for this event"

    invitation.status = status
    invitation.responded_at = datetime.now(timezone.utc)
    db.session.commit()

    return invitation.to_dict(), None


def get_user_invitations(user):
    """Return all invitations for a user.

    Returns (list_of_dicts, error_string).
    """
    invitations = Invitation.query.filter(
        (Invitation.user_id == user.id)
        | (Invitation.email == user.email)
    ).all()

    result = []
    for inv in invitations:
        inv_data = inv.to_dict()
        inv_data["event_title"] = inv.event.title
        inv_data["event_creator"] = inv.event.creator.name
        result.append(inv_data)

    return result, None


def add_invitee(event_id, creator, invitee_email):
    """Creator adds a new invitee to an existing event.

    Returns (invitation_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"
    if event.creator_id != creator.id:
        return None, "Only the creator can invite people"

    existing = Invitation.query.filter_by(
        event_id=event_id,
        email=invitee_email,
    ).first()
    if existing:
        return None, "This person is already invited"

    user = User.query.filter_by(email=invitee_email).first()
    invitation = Invitation(
        event_id=event_id,
        user_id=user.id if user else None,
        email=invitee_email,
        status="pending",
    )
    db.session.add(invitation)
    db.session.commit()

    # TODO: send email notification

    return invitation.to_dict(), None


def remove_invitee(event_id, creator, invitee_email):
    """Creator removes an invitee from an event.

    Returns (success_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"
    if event.creator_id != creator.id:
        return None, "Only the creator can remove invitees"

    invitation = Invitation.query.filter_by(
        event_id=event_id,
        email=invitee_email,
    ).first()
    if not invitation:
        return None, "Invitation not found"

    db.session.delete(invitation)
    db.session.commit()

    return {"message": f"Removed {invitee_email} from event"}, None
