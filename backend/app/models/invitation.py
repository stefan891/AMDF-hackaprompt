"""Invitation model – tracks who was invited and their response."""

from datetime import datetime, timezone
from app.extensions import db


class Invitation(db.Model):
    __tablename__ = "invitations"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
    )
    email = db.Column(
        db.String(256),
        nullable=False,
    )
    status = db.Column(
        db.String(16),
        nullable=False,
        default="pending",
    )  # "pending" | "accepted" | "declined"
    invited_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    responded_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "event_id",
            "email",
            name="uq_event_email",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "email": self.email,
            "status": self.status,
            "invited_at": self.invited_at.isoformat(),
            "responded_at": (
                self.responded_at.isoformat()
                if self.responded_at
                else None
            ),
        }
