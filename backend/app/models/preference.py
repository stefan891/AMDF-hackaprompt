"""Preference model – one user's vote on one timeslot."""

from datetime import datetime, timezone
from app.extensions import db


class Preference(db.Model):
    __tablename__ = "preferences"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    timeslot_id = db.Column(
        db.Integer,
        db.ForeignKey("timeslots.id"),
        nullable=False,
    )
    value = db.Column(
        db.String(16),
        nullable=False,
        default="unavailable",
    )  # "available" | "maybe" | "unavailable"
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "timeslot_id",
            name="uq_user_timeslot",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "timeslot_id": self.timeslot_id,
            "value": self.value,
            "updated_at": self.updated_at.isoformat(),
        }
