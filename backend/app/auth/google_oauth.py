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
        sub, email, name, picture, ...
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
