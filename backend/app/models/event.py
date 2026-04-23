"""Event model – a poll / scheduling event."""

from datetime import datetime, timezone
from app.extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    event_type = db.Column(
        db.String(32),
        nullable=False,
        default="time",
    )  # "fullday" | "time"
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    quorum = db.Column(db.Integer, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ──────────────────────────────────────
    timeslots = db.relationship(
        "TimeSlot",
        backref="event",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    preferences = db.relationship(
        "Preference",
        backref="event",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    invitations = db.relationship(
        "Invitation",
        backref="event",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_slots=False, include_preferences=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "creator_id": self.creator_id,
            "event_type": self.event_type,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "quorum": self.quorum,
            "created_at": self.created_at.isoformat(),
        }
        if include_slots:
            data["timeslots"] = [s.to_dict() for s in self.timeslots]
        if include_preferences:
            data["preferences"] = [p.to_dict() for p in self.preferences]
        return data
