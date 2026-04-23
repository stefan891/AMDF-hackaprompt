# Flask Backend — Properly Formatted Files

Every file below uses **4-space indentation**, consistent blank lines per PEP 8, and no stray tabs.

---

### `run.py`

```python
"""Application entry point."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

---

### `app/__init__.py`

```python
"""Flask application factory."""

from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Initialise extensions ──────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    # ── Register blueprints ────────────────────────────────
    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.preference_routes import preference_bp
    from app.routes.user_routes import user_bp
    from app.routes.calendar_routes import calendar_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(event_bp, url_prefix="/events")
    app.register_blueprint(preference_bp, url_prefix="/events")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(calendar_bp, url_prefix="/calendar")

    # ── Create tables on first request (dev convenience) ───
    with app.app_context():
        from app.models import user, event, timeslot, preference  # noqa: F401
        db.create_all()

    return app
```

---

### `app/config.py`

```python
"""Centralised configuration loaded from .env."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

    # ── Database ───────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///doodle.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Google OAuth ───────────────────────────────────────
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI",
        "http://localhost:5000/auth/google/callback",
    )
    GOOGLE_SCOPES = os.getenv(
        "GOOGLE_SCOPES",
        "openid email profile https://www.googleapis.com/auth/calendar.readonly",
    ).split()

    # ── JWT / session ──────────────────────────────────────
    JWT_SECRET = os.getenv("SECRET_KEY", "fallback-secret-key")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
```

---

### `app/extensions.py`

```python
"""Shared extension instances (avoid circular imports)."""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
```

---

## Models

### `app/models/__init__.py`

```python
"""Re-export all models so Alembic / create_all() can discover them."""

from app.models.user import User  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.timeslot import TimeSlot  # noqa: F401
from app.models.preference import Preference  # noqa: F401
```

---

### `app/models/user.py`

```python
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

    def to_dict(self):
        return {
            "id": self.id,
            "google_id": self.google_id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
            "created_at": self.created_at.isoformat(),
        }
```

---

### `app/models/event.py`

```python
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
    quorum = db.Column(db.Integer, nullable=True)  # optional target count

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

    # Many-to-many: invited participants
    invitees = db.relationship(
        "User",
        secondary="event_invitees",
        backref=db.backref("invited_events", lazy="dynamic"),
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


# ── Association table for invitations ──────────────────────
event_invitees = db.Table(
    "event_invitees",
    db.Column(
        "event_id",
        db.Integer,
        db.ForeignKey("events.id"),
        primary_key=True,
    ),
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
    ),
)
```

---

### `app/models/timeslot.py`

```python
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
    label = db.Column(db.String(256), nullable=True)  # human-readable

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
```

---

### `app/models/preference.py`

```python
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

    # One vote per user per slot
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
```

---

## Auth

### `app/auth/__init__.py`

```python
```

---

### `app/auth/google_oauth.py`

```python
"""Google OAuth helpers – token verification, credential exchange,
and Google Calendar credential builder."""

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from flask import current_app


def build_oauth_flow():
    """Return a configured google_auth_oauthlib Flow."""
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": current_app.config["GOOGLE_CLIENT_ID"],
                "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [
                    current_app.config["GOOGLE_REDIRECT_URI"],
                ],
            }
        },
        scopes=current_app.config["GOOGLE_SCOPES"],
    )
    flow.redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
    return flow


def verify_google_id_token(token: str) -> dict:
    """Verify a Google ID token (sent from the Svelte frontend).

    Returns the decoded payload with fields:
        sub, email, name, picture, …
    """
    id_info = id_token.verify_oauth2_token(
        token,
        google_requests.Request(),
        current_app.config["GOOGLE_CLIENT_ID"],
    )
    return id_info


def build_calendar_credentials(user) -> Credentials:
    """Build google.oauth2.credentials.Credentials from stored user tokens
    so we can call the Calendar API on behalf of the user."""
    creds = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=current_app.config["GOOGLE_CLIENT_ID"],
        client_secret=current_app.config["GOOGLE_CLIENT_SECRET"],
        scopes=current_app.config["GOOGLE_SCOPES"],
    )
    return creds
```

---

### `app/auth/decorators.py`

```python
"""Route decorators for authentication & authorisation."""

import functools
from datetime import datetime, timezone

import jwt
from flask import request, jsonify, current_app, g

from app.models.user import User


def token_required(f):
    """Decorator – extracts & validates JWT from Authorization header,
    sets g.current_user for downstream handlers."""

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
```

---

## Routes

### `app/routes/__init__.py`

```python
```

---

### `app/routes/auth_routes.py`

```python
"""Authentication endpoints (Google OAuth)."""

from flask import Blueprint, request, jsonify, redirect

from app.extensions import db
from app.models.user import User
from app.auth.google_oauth import (
    build_oauth_flow,
    verify_google_id_token,
)
from app.auth.decorators import create_jwt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/google", methods=["POST"])
def google_login():
    """Accept a Google ID token from the frontend, verify it,
    create/update the local user, and return a JWT.

    Expected JSON body: { "token": "<google id_token>" }
    """
    data = request.get_json(silent=True) or {}
    id_token_str = data.get("token")
    if not id_token_str:
        return jsonify({"error": "Missing Google token"}), 400

    try:
        google_info = verify_google_id_token(id_token_str)
    except ValueError as exc:
        return jsonify({"error": f"Token verification failed: {exc}"}), 401

    # ── Upsert user ────────────────────────────────────────
    user = User.query.filter_by(google_id=google_info["sub"]).first()
    if user is None:
        user = User(
            google_id=google_info["sub"],
            email=google_info["email"],
            name=google_info.get("name", ""),
            picture=google_info.get("picture"),
        )
        db.session.add(user)
    else:
        user.name = google_info.get("name", user.name)
        user.picture = google_info.get("picture", user.picture)

    db.session.commit()

    jwt_token = create_jwt(user)

    return jsonify({"token": jwt_token, "user": user.to_dict()}), 200


@auth_bp.route("/google/redirect", methods=["GET"])
def google_redirect():
    """Start the server-side OAuth flow (used when we need
    offline access for Calendar refresh tokens)."""
    flow = build_oauth_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    # TODO: store `state` in session for CSRF protection
    return redirect(auth_url)


@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    """Handle the OAuth callback, exchange code for tokens,
    store refresh token for Calendar API."""
    flow = build_oauth_flow()
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    id_info = verify_google_id_token(credentials.id_token)

    user = User.query.filter_by(google_id=id_info["sub"]).first()
    if user is None:
        user = User(
            google_id=id_info["sub"],
            email=id_info["email"],
            name=id_info.get("name", ""),
            picture=id_info.get("picture"),
        )
        db.session.add(user)

    # Persist tokens for Calendar API
    user.google_access_token = credentials.token
    user.google_refresh_token = credentials.refresh_token
    user.token_expiry = credentials.expiry
    db.session.commit()

    jwt_token = create_jwt(user)

    # TODO: redirect to frontend with JWT in query param / fragment
    return jsonify({"token": jwt_token, "user": user.to_dict()}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    """Return the currently-authenticated user (convenience)."""
    from app.auth.decorators import token_required

    # Inline-apply decorator is ugly; this is just skeleton structure.
    # In practice use @token_required on the function.
    pass
```

---

### `app/routes/event_routes.py`

```python
"""CRUD endpoints for events."""

from flask import Blueprint, request, jsonify, g

from app.extensions import db
from app.auth.decorators import token_required
from app.services.event_service import (
    create_event,
    get_event_detail,
    get_event_overview,
    set_event_quorum,
)

event_bp = Blueprint("events", __name__)


@event_bp.route("", methods=["POST"])
@token_required
def create():
    """Create a new event with timeslots and invitees.

    Expected JSON:
    {
        "title": "...",
        "description": "...",
        "event_type": "time" | "fullday",
        "start": "ISO datetime",
        "end": "ISO datetime",
        "slots": [ {"slot_start": "...", "slot_end": "..."}, ... ],
        "invitees": [ "email1@example.com", ... ]
    }
    """
    data = request.get_json(silent=True) or {}
    event, errors = create_event(g.current_user, data)
    if errors:
        return jsonify({"errors": errors}), 400
    return jsonify(event.to_dict(include_slots=True)), 201


@event_bp.route("/<int:event_id>", methods=["GET"])
@token_required
def detail(event_id):
    """Return full event details with slots and preferences."""
    event_data, error = get_event_detail(event_id, g.current_user)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(event_data), 200


@event_bp.route("/<int:event_id>/overview", methods=["GET"])
@token_required
def overview(event_id):
    """Aggregated slot-by-slot vote counts + best slot recommendation."""
    result, error = get_event_overview(event_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(result), 200


@event_bp.route("/<int:event_id>/quorum", methods=["POST"])
@token_required
def quorum(event_id):
    """Set quorum and return slots that meet it.

    JSON body: { "quorum": 5 }
    """
    data = request.get_json(silent=True) or {}
    result, error = set_event_quorum(
        event_id,
        g.current_user,
        data.get("quorum"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200
```

---

### `app/routes/preference_routes.py`

```python
"""Preference (vote) endpoints."""

from flask import Blueprint, request, jsonify, g

from app.auth.decorators import token_required
from app.services.preference_service import submit_preference

preference_bp = Blueprint("preferences", __name__)


@preference_bp.route("/<int:event_id>/preference", methods=["POST"])
@token_required
def vote(event_id):
    """Submit or update a preference for one timeslot.

    JSON body: { "timeslot_id": 1, "value": "available" }
    Allowed values: "available", "maybe", "unavailable"
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
```

---

### `app/routes/user_routes.py`

```python
"""User-centric endpoints."""

from flask import Blueprint, jsonify, g

from app.auth.decorators import token_required
from app.models.event import Event

user_bp = Blueprint("users", __name__)


@user_bp.route("/<int:user_id>/events", methods=["GET"])
@token_required
def user_events(user_id):
    """Return all events where user is creator OR invitee."""
    # TODO: verify g.current_user.id == user_id or admin
    created = Event.query.filter_by(creator_id=user_id).all()
    invited = g.current_user.invited_events.all()

    seen_ids = set()
    events = []
    for e in list(created) + list(invited):
        if e.id not in seen_ids:
            events.append(e.to_dict())
            seen_ids.add(e.id)

    return jsonify({"events": events}), 200
```

---

### `app/routes/calendar_routes.py`

```python
"""Google Calendar integration endpoints."""

from flask import Blueprint, request, jsonify, g

from app.auth.decorators import token_required
from app.services.google_calendar_service import (
    fetch_busy_times,
    fetch_calendars,
)

calendar_bp = Blueprint("calendar", __name__)


@calendar_bp.route("/busy", methods=["GET"])
@token_required
def busy_times():
    """Return the current user's busy blocks from Google Calendar
    for a given date range.

    Query params: ?start=ISO&end=ISO
    """
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return jsonify({"error": "start and end are required"}), 400

    busy, error = fetch_busy_times(g.current_user, start, end)
    if error:
        return jsonify({"error": error}), 502
    return jsonify({"busy": busy}), 200


@calendar_bp.route("/list", methods=["GET"])
@token_required
def list_calendars():
    """Return a list of the user's Google calendars."""
    calendars, error = fetch_calendars(g.current_user)
    if error:
        return jsonify({"error": error}), 502
    return jsonify({"calendars": calendars}), 200
```

---

## Services

### `app/services/__init__.py`

```python
```

---

### `app/services/event_service.py`

```python
"""Business logic for event creation, details, overview."""

from datetime import datetime

from app.extensions import db
from app.models.event import Event
from app.models.timeslot import TimeSlot
from app.models.user import User
from app.services.slot_service import generate_slots
from app.services.quorum_service import check_quorum


def create_event(creator, data: dict):
    """Validate input, create Event + TimeSlots, resolve invitees.

    Returns (event, errors).
    """
    errors = []

    title = data.get("title")
    if not title:
        errors.append("title is required")

    event_type = data.get("event_type", "time")
    start_str = data.get("start")
    end_str = data.get("end")

    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
    except (TypeError, ValueError):
        errors.append("Invalid start/end datetime format")
        return None, errors

    if errors:
        return None, errors

    event = Event(
        title=title,
        description=data.get("description", ""),
        creator_id=creator.id,
        event_type=event_type,
        start=start,
        end=end,
    )
    db.session.add(event)
    db.session.flush()  # get event.id

    # ── Slots ──────────────────────────────────────────────
    raw_slots = data.get("slots", [])
    if raw_slots:
        for s in raw_slots:
            ts = TimeSlot(
                event_id=event.id,
                slot_start=datetime.fromisoformat(s["slot_start"]),
                slot_end=datetime.fromisoformat(s["slot_end"]),
                label=s.get("label"),
            )
            db.session.add(ts)
    else:
        # Auto-generate slots from start/end
        generated = generate_slots(event_type, start, end)
        for ts in generated:
            ts.event_id = event.id
            db.session.add(ts)

    # ── Invitees ───────────────────────────────────────────
    invitee_emails = data.get("invitees", [])
    for email in invitee_emails:
        user = User.query.filter_by(email=email).first()
        if user:
            event.invitees.append(user)
        # TODO: send invitation email to unregistered users

    db.session.commit()
    return event, None


def get_event_detail(event_id, current_user):
    """Return event dict with slots & preferences.

    Returns (data_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"

    data = event.to_dict(include_slots=True, include_preferences=True)
    data["creator"] = event.creator.to_dict()
    data["invitees"] = [u.to_dict() for u in event.invitees]
    return data, None


def get_event_overview(event_id):
    """Aggregate preferences per slot + recommend best slot.

    Returns (result_dict, error_string).
    """
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"

    overview = []
    best_slot = None
    best_score = -1

    for slot in event.timeslots:
        prefs = slot.preferences.all()
        counts = {"available": 0, "maybe": 0, "unavailable": 0}
        for p in prefs:
            counts[p.value] = counts.get(p.value, 0) + 1

        # Simple scoring: available=2, maybe=1, unavailable=0
        score = counts["available"] * 2 + counts["maybe"]

        slot_data = {
            **slot.to_dict(),
            "counts": counts,
            "score": score,
        }
        overview.append(slot_data)

        if score > best_score:
            best_score = score
            best_slot = slot_data

    quorum_met = check_quorum(event, overview)

    return {
        "event_id": event_id,
        "slots": overview,
        "recommended": best_slot,
        "quorum_met": quorum_met,
    }, None


def set_event_quorum(event_id, current_user, quorum_value):
    """Set quorum on an event, return slots meeting it."""
    event = Event.query.get(event_id)
    if not event:
        return None, "Event not found"
    if event.creator_id != current_user.id:
        return None, "Only the creator can set quorum"
    if quorum_value is None or not isinstance(quorum_value, int):
        return None, "quorum must be an integer"

    event.quorum = quorum_value
    db.session.commit()

    # Re-run overview to find qualifying slots
    result, _ = get_event_overview(event_id)
    qualifying = [
        s
        for s in result["slots"]
        if s["counts"]["available"] >= quorum_value
    ]

    return {
        "quorum": quorum_value,
        "qualifying_slots": qualifying,
        "recommended": result["recommended"],
    }, None
```

---

### `app/services/slot_service.py`

```python
"""Automatic timeslot generation helpers."""

from datetime import datetime, timedelta

from app.models.timeslot import TimeSlot

DEFAULT_SLOT_DURATION_MINUTES = 60
DEFAULT_FULLDAY_DAYS = 1


def generate_slots(event_type: str, start: datetime, end: datetime):
    """Generate TimeSlot objects (not yet committed) between start and end.

    - event_type "fullday": one slot per calendar day
    - event_type "time":    one slot per hour (configurable)
    """
    slots = []

    if event_type == "fullday":
        current = start.replace(hour=0, minute=0, second=0, microsecond=0)
        while current < end:
            next_day = current + timedelta(days=DEFAULT_FULLDAY_DAYS)
            slots.append(
                TimeSlot(
                    slot_start=current,
                    slot_end=next_day,
                    label=current.strftime("%A %d %B %Y"),
                )
            )
            current = next_day
    else:
        delta = timedelta(minutes=DEFAULT_SLOT_DURATION_MINUTES)
        current = start
        while current + delta <= end:
            slot_end = current + delta
            slots.append(
                TimeSlot(
                    slot_start=current,
                    slot_end=slot_end,
                    label=(
                        f"{current.strftime('%H:%M')}"
                        f"–{slot_end.strftime('%H:%M')}"
                    ),
                )
            )
            current = slot_end

    return slots
```

---

### `app/services/preference_service.py`

```python
"""Business logic for submitting / updating preferences."""

from app.extensions import db
from app.models.preference import Preference
from app.models.timeslot import TimeSlot

ALLOWED_VALUES = {"available", "maybe", "unavailable"}


def submit_preference(event_id, user, timeslot_id, value):
    """Create or update a Preference.

    Returns (result_dict, error_string).
    """
    if value not in ALLOWED_VALUES:
        return None, f"value must be one of {ALLOWED_VALUES}"

    slot = TimeSlot.query.get(timeslot_id)
    if not slot or slot.event_id != event_id:
        return None, "Invalid timeslot for this event"

    pref = Preference.query.filter_by(
        user_id=user.id,
        timeslot_id=timeslot_id,
    ).first()

    if pref:
        pref.value = value
    else:
        pref = Preference(
            event_id=event_id,
            user_id=user.id,
            timeslot_id=timeslot_id,
            value=value,
        )
        db.session.add(pref)

    db.session.commit()

    return pref.to_dict(), None
```

---

### `app/services/quorum_service.py`

```python
"""Quorum evaluation logic."""


def check_quorum(event, slot_overview: list) -> bool:
    """Return True if at least one slot meets the event's quorum."""
    if event.quorum is None:
        return False

    for slot in slot_overview:
        if slot["counts"]["available"] >= event.quorum:
            return True

    return False
```

---

### `app/services/google_calendar_service.py`

```python
"""Google Calendar API integration – fetch busy times & calendar list."""

from googleapiclient.discovery import build
from app.auth.google_oauth import build_calendar_credentials


def _get_calendar_service(user):
    """Build an authorised Calendar API service for the user."""
    creds = build_calendar_credentials(user)
    if not creds or not creds.valid:
        # TODO: attempt token refresh if refresh_token present
        return None, "Google Calendar credentials are missing or expired"
    service = build("calendar", "v3", credentials=creds)
    return service, None


def fetch_busy_times(user, start_iso: str, end_iso: str):
    """Call Calendar FreeBusy API and return busy intervals.

    Returns (list_of_busy_blocks, error_string).
    """
    service, error = _get_calendar_service(user)
    if error:
        return None, error

    body = {
        "timeMin": start_iso,
        "timeMax": end_iso,
        "timeZone": "UTC",
        "items": [{"id": "primary"}],
    }

    try:
        result = service.freebusy().query(body=body).execute()
    except Exception as exc:
        return None, f"Google Calendar API error: {exc}"

    busy_blocks = (
        result
        .get("calendars", {})
        .get("primary", {})
        .get("busy", [])
    )
    return busy_blocks, None


def fetch_calendars(user):
    """Return a list of the user's Google calendars.

    Returns (list_of_calendars, error_string).
    """
    service, error = _get_calendar_service(user)
    if error:
        return None, error

    try:
        result = service.calendarList().list().execute()
    except Exception as exc:
        return None, f"Google Calendar API error: {exc}"

    calendars = [
        {
            "id": cal["id"],
            "summary": cal.get("summary", ""),
            "primary": cal.get("primary", False),
        }
        for cal in result.get("items", [])
    ]
    return calendars, None
```

---

### `app/utils/__init__.py`

```python
```

---

### `app/utils/helpers.py`

```python
"""Miscellaneous utility functions."""

from datetime import datetime


def parse_iso(value: str) -> datetime | None:
    """Safely parse an ISO-8601 string; return None on failure."""
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
```

---

### `.env.example`

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me-to-a-real-secret

DATABASE_URI=sqlite:///doodle.db

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback

# Scopes: openid, email, profile, calendar.readonly
GOOGLE_SCOPES=openid email profile https://www.googleapis.com/auth/calendar.readonly
```

> **What changed:** Every line now uses **4 spaces** (no tabs), trailing-comma style is consistent on multi-line calls, long chained method calls are broken across lines cleanly, and the stray leading tab in `.env.example` (`\tFLASK_APP`) has been removed.