# API Reference — Frontend Integration Guide

---

## Base URL

```
http://localhost:5000
```

## Authentication

All endpoints marked with 🔒 require a **Bearer token** in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

---

## 1. Authentication

### 1.1 Google Login

```
POST /auth/google
```

Exchange a Google ID token (from frontend Google Sign-In) for a JWT.

| Field | Details |
|-------|---------|
| **Auth** | None |
| **Content-Type** | `application/json` |

**Request Body**

```json
{
  "token": "<google_id_token_from_frontend>"
}
```

**Response `200 OK`**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "google_id": "118234...",
    "email": "alice@gmail.com",
    "name": "Alice Smith",
    "picture": "https://lh3.googleusercontent.com/...",
    "created_at": "2025-01-15T10:30:00+00:00"
  }
}
```

**Errors**

| Status | Body |
|--------|------|
| `400` | `{ "error": "Missing Google token" }` |
| `401` | `{ "error": "Token verification failed: ..." }` |

---

### 1.2 Start OAuth Flow (Server-Side)

```
GET /auth/google/redirect
```

Initiates the full server-side OAuth flow. Used when **offline access** is needed (Calendar refresh tokens).

| Field | Details |
|-------|---------|
| **Auth** | None |
| **Response** | `302 Redirect` → Google consent screen |

> **Frontend note:** Open this URL in a popup or redirect the browser to it.
> After consent, Google redirects to `/auth/google/callback`.

---

### 1.3 OAuth Callback

```
GET /auth/google/callback
```

Handles the Google OAuth redirect. Exchanges the authorization code for tokens and stores the refresh token for Calendar API access.

| Field | Details |
|-------|---------|
| **Auth** | None (called by Google) |
| **Query Params** | Managed by Google (`code`, `state`, `scope`) |

**Response `200 OK`**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "google_id": "118234...",
    "email": "alice@gmail.com",
    "name": "Alice Smith",
    "picture": "https://lh3.googleusercontent.com/...",
    "created_at": "2025-01-15T10:30:00+00:00"
  }
}
```

> **Note:** In production this will redirect to the frontend with the JWT as a query parameter.

---

### 1.4 Get Current User

```
GET /auth/me
```

🔒 **Requires authentication**

Returns the profile of the currently authenticated user.

**Response `200 OK`**

```json
{
  "id": 1,
  "google_id": "118234...",
  "email": "alice@gmail.com",
  "name": "Alice Smith",
  "picture": "https://lh3.googleusercontent.com/...",
  "created_at": "2025-01-15T10:30:00+00:00"
}
```

---

## 2. Events

### 2.1 Create Event

```
POST /events
```

🔒 **Requires authentication**

Create a new scheduling event with timeslots and optional invitees.

**Request Body**

```json
{
  "title": "Team Standup",
  "description": "Weekly sync meeting",
  "event_type": "time",
  "start": "2025-02-01T09:00:00",
  "end": "2025-02-01T17:00:00",
  "slots": [
    {
      "slot_start": "2025-02-01T09:00:00",
      "slot_end": "2025-02-01T10:00:00",
      "label": "09:00–10:00"
    },
    {
      "slot_start": "2025-02-01T10:00:00",
      "slot_end": "2025-02-01T11:00:00",
      "label": "10:00–11:00"
    }
  ],
  "invitees": [
    "bob@gmail.com",
    "carol@gmail.com"
  ]
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | `string` | ✅ | Event name |
| `description` | `string` | ❌ | Optional description |
| `event_type` | `string` | ❌ | `"time"` (default) or `"fullday"` |
| `start` | `ISO 8601` | ✅ | Event window start |
| `end` | `ISO 8601` | ✅ | Event window end |
| `slots` | `array` | ❌ | If omitted, slots auto-generate (1h for `time`, 1 day for `fullday`) |
| `slots[].slot_start` | `ISO 8601` | ✅* | Slot start time |
| `slots[].slot_end` | `ISO 8601` | ✅* | Slot end time |
| `slots[].label` | `string` | ❌ | Display label |
| `invitees` | `string[]` | ❌ | Email addresses of participants |

**Response `201 Created`**

```json
{
  "id": 1,
  "title": "Team Standup",
  "description": "Weekly sync meeting",
  "creator_id": 1,
  "event_type": "time",
  "start": "2025-02-01T09:00:00",
  "end": "2025-02-01T17:00:00",
  "quorum": null,
  "created_at": "2025-01-15T10:30:00+00:00",
  "timeslots": [
    {
      "id": 1,
      "event_id": 1,
      "slot_start": "2025-02-01T09:00:00",
      "slot_end": "2025-02-01T10:00:00",
      "label": "09:00–10:00"
    },
    {
      "id": 2,
      "event_id": 1,
      "slot_start": "2025-02-01T10:00:00",
      "slot_end": "2025-02-01T11:00:00",
      "label": "10:00–11:00"
    }
  ]
}
```

**Errors**

| Status | Body |
|--------|------|
| `400` | `{ "errors": ["title is required"] }` |
| `400` | `{ "errors": ["Invalid start/end datetime format"] }` |
| `401` | `{ "error": "Missing or malformed token" }` |

---

### 2.2 Get Event Detail

```
GET /events/{event_id}
```

🔒 **Requires authentication**

Returns the full event with all timeslots, preferences, creator info, and invitees.

| Path Param | Type | Description |
|-----------|------|-------------|
| `event_id` | `int` | Event ID |

**Response `200 OK`**

```json
{
  "id": 1,
  "title": "Team Standup",
  "description": "Weekly sync meeting",
  "creator_id": 1,
  "event_type": "time",
  "start": "2025-02-01T09:00:00",
  "end": "2025-02-01T17:00:00",
  "quorum": null,
  "created_at": "2025-01-15T10:30:00+00:00",
  "timeslots": [
    {
      "id": 1,
      "event_id": 1,
      "slot_start": "2025-02-01T09:00:00",
      "slot_end": "2025-02-01T10:00:00",
      "label": "09:00–10:00"
    }
  ],
  "preferences": [
    {
      "id": 1,
      "event_id": 1,
      "user_id": 2,
      "timeslot_id": 1,
      "value": "available",
      "updated_at": "2025-01-16T08:00:00+00:00"
    }
  ],
  "creator": {
    "id": 1,
    "google_id": "118234...",
    "email": "alice@gmail.com",
    "name": "Alice Smith",
    "picture": "https://...",
    "created_at": "2025-01-15T10:30:00+00:00"
  },
  "invitees": [
    {
      "id": 2,
      "google_id": "229345...",
      "email": "bob@gmail.com",
      "name": "Bob Jones",
      "picture": "https://...",
      "created_at": "2025-01-15T11:00:00+00:00"
    }
  ]
}
```

**Errors**

| Status | Body |
|--------|------|
| `404` | `{ "error": "Event not found" }` |

---

### 2.3 Get Event Overview

```
GET /events/{event_id}/overview
```

🔒 **Requires authentication**

Returns aggregated vote counts per slot, a **recommended best slot**, and quorum status.

| Path Param | Type | Description |
|-----------|------|-------------|
| `event_id` | `int` | Event ID |

**Response `200 OK`**

```json
{
  "event_id": 1,
  "slots": [
    {
      "id": 1,
      "event_id": 1,
      "slot_start": "2025-02-01T09:00:00",
      "slot_end": "2025-02-01T10:00:00",
      "label": "09:00–10:00",
      "counts": {
        "available": 4,
        "maybe": 1,
        "unavailable": 2
      },
      "score": 9
    },
    {
      "id": 2,
      "event_id": 1,
      "slot_start": "2025-02-01T10:00:00",
      "slot_end": "2025-02-01T11:00:00",
      "label": "10:00–11:00",
      "counts": {
        "available": 6,
        "maybe": 0,
        "unavailable": 1
      },
      "score": 12
    }
  ],
  "recommended": {
    "id": 2,
    "event_id": 1,
    "slot_start": "2025-02-01T10:00:00",
    "slot_end": "2025-02-01T11:00:00",
    "label": "10:00–11:00",
    "counts": { "available": 6, "maybe": 0, "unavailable": 1 },
    "score": 12
  },
  "quorum_met": true
}
```

> **Scoring formula:** `available × 2 + maybe × 1`

**Errors**

| Status | Body |
|--------|------|
| `404` | `{ "error": "Event not found" }` |

---

### 2.4 Set Quorum

```
POST /events/{event_id}/quorum
```

🔒 **Requires authentication** · **Creator only**

Set the minimum number of "available" votes required. Returns which slots meet the quorum.

| Path Param | Type | Description |
|-----------|------|-------------|
| `event_id` | `int` | Event ID |

**Request Body**

```json
{
  "quorum": 5
}
```

**Response `200 OK`**

```json
{
  "quorum": 5,
  "qualifying_slots": [
    {
      "id": 2,
      "event_id": 1,
      "slot_start": "2025-02-01T10:00:00",
      "slot_end": "2025-02-01T11:00:00",
      "label": "10:00–11:00",
      "counts": { "available": 6, "maybe": 0, "unavailable": 1 },
      "score": 12
    }
  ],
  "recommended": { "..." }
}
```

**Errors**

| Status | Body |
|--------|------|
| `400` | `{ "error": "Only the creator can set quorum" }` |
| `400` | `{ "error": "quorum must be an integer" }` |
| `400` | `{ "error": "Event not found" }` |

---

## 3. Preferences (Voting)

### 3.1 Submit / Update Preference

```
POST /events/{event_id}/preference
```

🔒 **Requires authentication**

Cast or update a vote on a specific timeslot. One vote per user per slot (upsert behaviour).

| Path Param | Type | Description |
|-----------|------|-------------|
| `event_id` | `int` | Event ID |

**Request Body**

```json
{
  "timeslot_id": 1,
  "value": "available"
}
```

| Field | Type | Required | Allowed Values |
|-------|------|----------|----------------|
| `timeslot_id` | `int` | ✅ | Must belong to the given event |
| `value` | `string` | ✅ | `"available"`, `"maybe"`, `"unavailable"` |

**Response `200 OK`**

```json
{
  "id": 1,
  "event_id": 1,
  "user_id": 2,
  "timeslot_id": 1,
  "value": "available",
  "updated_at": "2025-01-16T08:00:00+00:00"
}
```

**Errors**

| Status | Body |
|--------|------|
| `400` | `{ "error": "value must be one of {'available', 'maybe', 'unavailable'}" }` |
| `400` | `{ "error": "Invalid timeslot for this event" }` |

---

## 4. Users

### 4.1 Get User Events

```
GET /users/{user_id}/events
```

🔒 **Requires authentication**

Returns all events where the user is the **creator** or an **invitee** (deduplicated).

| Path Param | Type | Description |
|-----------|------|-------------|
| `user_id` | `int` | User ID |

**Response `200 OK`**

```json
{
  "events": [
    {
      "id": 1,
      "title": "Team Standup",
      "description": "Weekly sync meeting",
      "creator_id": 1,
      "event_type": "time",
      "start": "2025-02-01T09:00:00",
      "end": "2025-02-01T17:00:00",
      "quorum": 5,
      "created_at": "2025-01-15T10:30:00+00:00"
    },
    {
      "id": 3,
      "title": "Design Review",
      "description": null,
      "creator_id": 4,
      "event_type": "fullday",
      "start": "2025-02-10T00:00:00",
      "end": "2025-02-14T00:00:00",
      "quorum": null,
      "created_at": "2025-01-18T14:00:00+00:00"
    }
  ]
}
```

---

## 5. Google Calendar Integration

### 5.1 Get Busy Times

```
GET /calendar/busy?start={ISO}&end={ISO}
```

🔒 **Requires authentication** · **Requires Calendar OAuth**

Returns the user's busy blocks from their **primary** Google Calendar.

| Query Param | Type | Required | Description |
|-------------|------|----------|-------------|
| `start` | `ISO 8601` | ✅ | Range start |
| `end` | `ISO 8601` | ✅ | Range end |

**Example**

```
GET /calendar/busy?start=2025-02-01T00:00:00Z&end=2025-02-07T23:59:59Z
```

**Response `200 OK`**

```json
{
  "busy": [
    {
      "start": "2025-02-01T09:00:00Z",
      "end": "2025-02-01T10:00:00Z"
    },
    {
      "start": "2025-02-03T14:00:00Z",
      "end": "2025-02-03T15:30:00Z"
    }
  ]
}
```

**Errors**

| Status | Body |
|--------|------|
| `400` | `{ "error": "start and end are required" }` |
| `502` | `{ "error": "Google Calendar credentials are missing or expired" }` |
| `502` | `{ "error": "Google Calendar API error: ..." }` |

---

### 5.2 List Calendars

```
GET /calendar/list
```

🔒 **Requires authentication** · **Requires Calendar OAuth**

Returns the user's Google Calendar list.

**Response `200 OK`**

```json
{
  "calendars": [
    {
      "id": "primary",
      "summary": "alice@gmail.com",
      "primary": true
    },
    {
      "id": "en.usa#holiday@group.v.calendar.google.com",
      "summary": "Holidays in United States",
      "primary": false
    },
    {
      "id": "family123@group.calendar.google.com",
      "summary": "Family",
      "primary": false
    }
  ]
}
```

**Errors**

| Status | Body |
|--------|------|
| `502` | `{ "error": "Google Calendar credentials are missing or expired" }` |
| `502` | `{ "error": "Google Calendar API error: ..." }` |

---

## Quick Reference Table

| # | Method | Endpoint | Auth | Description |
|---|--------|----------|------|-------------|
| 1.1 | `POST` | `/auth/google` | ❌ | Google ID token → JWT |
| 1.2 | `GET` | `/auth/google/redirect` | ❌ | Start server-side OAuth (Calendar) |
| 1.3 | `GET` | `/auth/google/callback` | ❌ | OAuth callback (handled by Google) |
| 1.4 | `GET` | `/auth/me` | 🔒 | Get current user profile |
| 2.1 | `POST` | `/events` | 🔒 | Create event + slots + invitees |
| 2.2 | `GET` | `/events/{event_id}` | 🔒 | Full event detail |
| 2.3 | `GET` | `/events/{event_id}/overview` | 🔒 | Aggregated votes + recommendation |
| 2.4 | `POST` | `/events/{event_id}/quorum` | 🔒 | Set quorum, get qualifying slots |
| 3.1 | `POST` | `/events/{event_id}/preference` | 🔒 | Submit or update a vote |
| 4.1 | `GET` | `/users/{user_id}/events` | 🔒 | List user's events (created + invited) |
| 5.1 | `GET` | `/calendar/busy?start=&end=` | 🔒 | Google Calendar busy times |
| 5.2 | `GET` | `/calendar/list` | 🔒 | List user's Google calendars |

---

## Common Error Shapes

```json
// Single error
{ "error": "Human-readable message" }

// Multiple validation errors
{ "errors": ["field x is required", "invalid format for y"] }
```

## Standard HTTP Status Codes Used

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `400` | Bad request / validation error |
| `401` | Unauthenticated / token invalid |
| `404` | Resource not found |
| `502` | Upstream Google API failure |