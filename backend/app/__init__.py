"""Flask application factory."""

from flask import Flask, send_from_directory
from app.config import Config
from app.extensions import db, migrate, cors
import os


def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'),
        static_url_path='/static'
    )
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
    from app.routes.invitation_routes import invitation_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(event_bp, url_prefix="/events")
    app.register_blueprint(preference_bp, url_prefix="/events")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(calendar_bp, url_prefix="/calendar")
    app.register_blueprint(invitation_bp, url_prefix="/invitations")

    # ── Serve index.html at root ───────────────────────────
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    # ── Create tables on first request (dev convenience) ───
    with app.app_context():
        from app.models import user, event, timeslot, preference  # noqa: F401
        from app.models.invitation import Invitation  # noqa: F401
        db.create_all()

    return app