# Doodle-Clone Backend

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in your secrets

flask db init
flask db migrate -m "initial"
flask db upgrade

python run.py
```

Server runs at **http://127.0.0.1:5000**

## API Endpoints

### Auth
| Method | Path                    | Auth     | Description                  |
|--------|-------------------------|----------|------------------------------|
| POST   | /auth/google            | –        | Exchange Google token for JWT |
| GET    | /auth/google/redirect   | –        | Start server-side OAuth flow |
| GET    | /auth/google/callback   | –        | OAuth callback               |
| GET    | /auth/me                | Bearer   | Current user info            |

### Events
| Method | Path                         | Auth     | Permission    | Description            |
|--------|------------------------------|----------|---------------|------------------------|
| POST   | /events                      | Bearer   | Any user      | Create event           |
| GET    | /events/:id                  | Bearer   | Participant   | Event detail           |
| GET    | /events/:id/overview         | Bearer   | Participant   | Vote aggregation       |
| POST   | /events/:id/quorum           | Bearer   | Creator only  | Set quorum             |
| POST   | /events/:id/preference       | Bearer   | Participant   | Submit vote            |
| POST   | /events/:id/invite           | Bearer   | Creator only  | Add invitee            |
| DELETE | /events/:id/invite           | Bearer   | Creator only  | Remove invitee         |

### Invitations
| Method | Path                              | Auth     | Description              |
|--------|-----------------------------------|----------|--------------------------|
| POST   | /invitations/:event_id/respond    | Bearer   | Accept or decline        |
| GET    | /invitations/mine                 | Bearer   | List my invitations      |

### Users
| Method | Path              | Auth     | Description              |
|--------|-------------------|----------|--------------------------|
| GET    | /users/me/events  | Bearer   | My created + accepted    |

### Calendar
| Method | Path            | Auth     | Description              |
|--------|-----------------|----------|--------------------------|
| GET    | /calendar/busy  | Bearer   | Google Calendar busy     |
| GET    | /calendar/list  | Bearer   | Google Calendar list     |

## Permission Model

- **Any user**: authenticated via JWT
- **Participant**: event creator OR invitee with status "accepted"
- **Creator only**: only the user who created the event
