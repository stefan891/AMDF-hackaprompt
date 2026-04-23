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
