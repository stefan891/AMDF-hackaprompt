"""Authentication endpoints (Google OAuth)."""

from flask import Blueprint, request, jsonify, redirect

from app.extensions import db
from app.models.user import User
from app.auth.google_oauth import (
    build_oauth_flow,
    verify_google_id_token,
)
from app.auth.decorators import create_jwt, token_required

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
    # TODO: store state in session for CSRF protection
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
@token_required
def me():
    """Return the currently-authenticated user."""
    from flask import g
    return jsonify({"user": g.current_user.to_dict()}), 200
