"""User model – stores Google profile info + credentials."""

from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    picture = db.Column(db.String(512), nullable=True)

    # Encrypted Google tokens for Calendar API access
    google_access_token = db.Column(db.Text, nullable=True)
    google_refresh_token = db.Column(db.Text, nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ──────────────────────────────────────
    created_events = db.relationship(
        "Event",
        backref="creator",
        lazy="dynamic",
    )
    preferences = db.relationship(
        "Preference",
        backref="user",
        lazy="dynamic",
    )
    invitations = db.relationship(
        "Invitation",
        backref="user",
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "google_id": self.google_id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
            "created_at": self.created_at.isoformat(),
        }
