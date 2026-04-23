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
