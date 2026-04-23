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
