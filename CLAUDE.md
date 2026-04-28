# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Media_Co_Lab is a collaborative media management platform. Organizations contain teams; users within teams upload, label, and comment on media files. Real-time chat is supported via Django Channels/WebSocket.

## Stack

**Backend:** Django 5 · Django REST Framework · Knox auth · Django Channels (Daphne/ASGI) · PostgreSQL · drf-spectacular (OpenAPI)  
**Frontend:** Vue 3 · Vuex 4 · Vue Router 4 · Vuetify 3 · Axios  
**Infra:** Docker Compose · Nginx (frontend) · GitHub Actions CI

## Running the Project

```bash
# Start all services (preferred)
docker-compose up --build

# Frontend: http://localhost:8080
# API:      http://localhost:8000
# Swagger:  http://localhost:8000/api/schema/swagger-ui/
```

Environment files:
- `backend/.env.ci` — safe defaults for local dev (copy to `backend/.env`)
- `frontend/mcl_ui/.env.ci` — copy to `frontend/mcl_ui/.env`

## Common Commands

### Backend
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver                   # dev server (no channels)
daphne test_system.asgi:application          # dev server with channels/WS
```

### Frontend
```bash
cd frontend/mcl_ui
npm run serve    # dev server
npm run build    # production build → dist/
npm run lint     # ESLint
```

### Linting (CI uses Black)
```bash
cd backend
black .          # format Python
black --check .  # check only (what CI runs)
```

## Architecture

### Django Project Layout
```
backend/test_system/
├── apps/        # Django models only (users, organizations, teams, medias, labels, chats)
├── apis/        # DRF views and serializers (mirrors apps/ structure)
├── settings.py
├── urls.py      # all API routes registered here
├── asgi.py      # Channels routing
└── permissions.py  # shared custom permissions (OrganizationPermission, TeamPermission, IsMediaOwner, IsLabelOwner, IsUser)
```

The `apps/` layer owns models; `apis/` owns serialization and HTTP handling. Keep these cleanly separated — no business logic in views.

### API Conventions

<!-- AUTO-MANAGED: patterns -->
- All views use `APIView` — no ViewSets
- **Organization scope guard**: check `user.organization` before filtering querysets; return `400` if missing
- Single-object lookups always use `get_object_or_404`
- `DELETE` endpoints return `HTTP_204_NO_CONTENT` with no response body
- Query scoping: Chats via `owner__organization`; Medias via `team__organization`; Teams via `organization`; Labels via `medias__team__in=user_teams`; user-owned medias via `user.team.id`
- Custom permissions live in `test_system/permissions.py`: `OrganizationPermission`, `TeamPermission`, `IsMediaOwner`, `IsLabelOwner`, `IsUser`
- **Object-level permission check**: call `self.check_object_permissions(request, obj)` explicitly in views using `TeamPermission`, `IsMediaOwner`, or `IsLabelOwner`
- **Read-only public access**: override `get_permissions()` to return `[]` when `self.request.method == "GET"` on detail views; `TeamMediasGetView` has no auth at all
- **Team POST injection**: auto-set `request.data["organization"]` from `request.user.organization.id` before passing to serializer
- Media upload views use `parser_classes = [MultiPartParser, FormParser]`
<!-- END AUTO-MANAGED -->

### Data Model Relationships
- **Organization** → many **Teams**, many **CustomUsers**; has `is_approved` and `is_demo` boolean flags; signals loaded via `OrganizationsConfig.ready()`
- **CustomUser** (email-based, no username field) → M2M **Teams**, owns **Medias**
- **Media** → M2M **Teams**, M2M **Labels**, many **Chats**
- **Chat** is self-referencing (`parent_id`) for threading
- **Label** has `PresetTypes` (art/music/sport/game/literature/film/technology/custom) and `PresetTags` (green/yellow/orange/red) enums; `clean()` enforces that `custom_preset_type` is required and alphanumeric when `preset_type == CUSTOM`

### Auth
Knox token auth. Login → receive token → send as `Authorization: Token <token>` header. Knox supports per-device token revocation and logout-all. Endpoints: `/api/login/`, `/api/logout/`, `/api/logoutall/`.

### Frontend State
Vuex store mirrors the backend resource tree (users, orgs, teams, medias, labels, chats). Axios base URL and auth token injection are configured in `src/axios.js`.

### Real-time
Django Channels handles WebSocket connections. `CHANNEL_LAYERS` uses Redis in production; Redis must be running for chat features. ASGI entry: `test_system/asgi.py`.

## CI/CD
GitHub Actions (`.github/workflows/ci.yml`) triggers on push to `dev` and `main`:
1. Build Docker images
2. Start services via `docker-compose.ci.yml`
3. Run `black --check` on backend
4. Run tests
5. Required secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `POSTGRES_PASSWORD`, `SECRET_KEY`

## CORS
Set via `CORS_ALLOWED_ORIGINS` env var (comma-separated); defaults to `http://localhost:8080` if unset. Configure in the backend `.env` file or deployment environment — no code change required.
