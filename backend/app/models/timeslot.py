"""TimeSlot model – one selectable option inside an event."""

from app.extensions import db


class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False,
    )
    slot_start = db.Column(db.DateTime, nullable=False)
    slot_end = db.Column(db.DateTime, nullable=False)
    label = db.Column(db.String(256), nullable=True)

    preferences = db.relationship(
        "Preference",
        backref="timeslot",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "slot_start": self.slot_start.isoformat(),
            "slot_end": self.slot_end.isoformat(),
            "label": self.label,
        }
