# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Media_Co_Lab is a collaborative media management platform. Organizations contain teams; users within teams upload, label, and comment on media files. Real-time chat is supported via Django Channels/WebSocket.

## Stack

**Backend:** Django 5 · Django REST Framework · Knox auth · Django Channels (Daphne/ASGI) · PostgreSQL · drf-spectacular (OpenAPI) · django-extensions  
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
├── tests/       # test suite (test_onboarding.py, test_security.py)
└── permissions.py  # shared custom permissions (OrganizationPermission, TeamPermission, IsMediaOwner, IsLabelOwner, IsUser, IsPlatformAdmin, IsOrgAdmin)
```

The `apps/` layer owns models; `apis/` owns serialization and HTTP handling. Keep these cleanly separated — no business logic in views.

### API Conventions

<!-- AUTO-MANAGED: patterns -->
- All views use `APIView` — no ViewSets
- **Organization scope guard**: check `user.organization` before filtering querysets; return `400` if missing
- Single-object lookups always use `get_object_or_404`
- `DELETE` endpoints return `HTTP_204_NO_CONTENT` with no response body
- Query scoping: Chats via `owner__organization`; Medias via `team__organization`; Teams via `organization`; Labels via `medias__team__in=user_teams`; user-owned medias via `user.team.id`
- Custom permissions live in `test_system/permissions.py`: `OrganizationPermission`, `TeamPermission`, `IsMediaOwner`, `IsLabelOwner`, `IsUser`, `IsPlatformAdmin` (checks `is_staff`), `IsOrgAdmin` (checks `is_org_admin + organization + is_authenticated`)
- `check_org_membership_approved(request)` helper in `permissions.py`: returns HTTP 403 if `user.org_status != "approved"`; called at the top of labels, medias, and teams list/create views before any queryset work
- `IsMediaOwner` and `IsLabelOwner` use `has_object_permission` (check `obj.user == request.user`); `IsUser` uses `has_permission` (checks `user_id` URL kwarg)
- **Object-level permission check**: call `self.check_object_permissions(request, obj)` explicitly in views using `TeamPermission`, `IsMediaOwner`, or `IsLabelOwner`; `TeamGetUpdateDeleteView` calls it on GET, PUT, and DELETE — all three methods require `TeamPermission` (no public GET on team detail)
- **Read-only public access**: override `get_permissions()` to return `[]` when `self.request.method == "GET"` on detail views (`ChatGetUpdateDeleteView`, `LabelGetUpdateDeleteView`, `MediasGetUpdateDeleteView`); `TeamMediasGetView` has no auth at all
- **Chat ownership enforcement**: `ChatGetUpdateDeleteView` PUT/DELETE require `IsAuthenticated` and perform inline `chat.owner != request.user` check returning 403; unauthenticated requests return 401
- **Team POST injection**: auto-set `request.data["organization"]` from `request.user.organization.id` before passing to serializer
- Media upload views use `parser_classes = [MultiPartParser, FormParser]`
- **Media POST team validation**: `MediasGetCreateView.post` validates the submitted `team_id` belongs to the user's organization via `user.team.filter(id=team_id, organization=user.organization).exists()` before creating
- User registration delegates organization assignment to the serializer via `context={"request": request}`; `registration_type` field ("join" → `org_status=pending`; "create_org" → `org_status=approved, is_org_admin=True`)
- `UserGetPatchDeleteView` supports GET, PATCH, DELETE (not PUT); all three call `self.check_object_permissions(request, user)`
- `UsersGetSerializer.to_representation()`: org admins can see `email`; regular users cannot; `is_staff`/`is_superuser` always hidden from non-superusers
<!-- END AUTO-MANAGED -->

### Data Model Relationships
- **Organization** → many **Teams**, many **CustomUsers**; has `is_approved` and `is_demo` boolean flags; no `created_at` field (timestamps derived from org_admin user's `date_joined` in `PendingOrganizationSerializer`); signals loaded via `OrganizationsConfig.ready()`
- **CustomUser** (email-based, `username` always mirrors `email` via `save()`) → M2M **Teams**, owns **Medias**; fields: `is_org_admin` (BooleanField, default False), `org_status` (OrgStatus enum: pending/approved/denied, default approved)
- **Media** → FK **Team** (many-to-one), FK **CustomUser** (owner); reverse FK **Labels** (one media has many labels), reverse FK **Chats**
- **Chat** is self-referencing (`parent_id`) for threading
- **Label** → FK **Medias** (many labels per media), FK **CustomUser** (owner); has `PresetTypes` (art/music/sport/game/literature/film/technology/custom) and `PresetTags` (green/yellow/orange/red) enums; `clean()` enforces that `custom_preset_type` is required and alphanumeric when `preset_type == CUSTOM`, and clears it otherwise

### Org & Member Approval Flows
- **Platform admin (staff) manages orgs**: `GET /api/organizations/pending/` lists unapproved orgs; `POST /api/organizations/<id>/approve/` sets `is_approved=True`; `POST /api/organizations/<id>/deny/` hard-deletes org; all require `IsPlatformAdmin`
- **Org admin manages members**: `GET /api/organizations/members/pending/` lists users with `org_status=pending`; `POST /api/users/<id>/approve/` sets `org_status=approved` and auto-adds user to org's first team; `POST /api/users/<id>/deny/` sets `org_status=denied`; all require `IsOrgAdmin`
- **Demo orgs**: `POST /api/organizations/demo/` (AllowAny) creates org with `is_demo=True`; appends " demo" to title if not already present

### Auth
Knox token auth. Login → receive token → send as `Authorization: Token <token>` header. Knox supports per-device token revocation and logout-all. Endpoints: `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/logoutall/`. Current user data: `GET /api/users/me/` (CurrentUserView, IsAuthenticated).

### Frontend State
Vuex store mirrors the backend resource tree (users, orgs, teams, medias, labels, chats). Axios base URL and auth token injection are configured in `src/axios.js`. A separate unauthenticated instance `src/axiosPublic.js` is used for public endpoints (org list, user registration) — used by `UserRegister.vue`, `OrgRegister.vue`, and `DemoOrganization.vue`.

### Frontend Routing
Vue Router (`src/router.js`) uses `createWebHistory`. Auth guard (`requireAuth`) checks `localStorage.getItem('authToken')`; redirects to `UserLogin` if missing. Login route has a reverse guard: redirects to `HomePage` if already authenticated. `/register` is fully public — no `beforeEnter` guard.

Routes:
- `/` — `HomePage` (public, no guard)
- `/register` — `UserRegister` (public, no guard)
- `/login` — `UserLogin` (public; reverse guard redirects to `HomePage` if already logged in)
- `/organization`, `/organizations/reg`, `/organizations/ov`, `/organizations/demo` — org views (auth required)
- `/team/create`, `/teams`, `/teams/:team_id` — team views (auth required)
- `/medias`, `/medias/:medias_id` — media views (auth required)
- `/labels` — labels view (auth required)

### Frontend UI
Vuetify 3 with custom light/dark themes (`src/plugins/vuetify.js`). Default theme: `light`.

Light theme colors: primary `#1976D2`, secondary `#6C757D`, accent `#00BCD4`, success `#4CAF50`, warning `#FF9800`, error `#F44336`, info `#2196F3`, surface `#FFFFFF`, background `#F5F5F5`.

Dark theme colors: primary `#BB86FC`, secondary `#03DAC6`, accent `#00BCD4`, success `#4CAF50`, warning `#FF9800`, error `#CF6679`, info `#90CAF9`, surface `#1E1E1E`, background `#121212`.

`App.vue` nav bar always shows Demo, Organization, Teams, Media links; Home link is hidden on the homepage via `isHomePage` computed (`$route.path === '/'`). Auth section uses `isLoggedIn` Vuex getter to toggle Login/Register vs Logout. `UserLogin.vue` renders an "Already Logged In" card inline when `isLoggedIn` is true (in addition to the router-level reverse guard).

### Real-time
Django Channels handles WebSocket connections. `CHANNEL_LAYERS` uses Redis in production; Redis must be running for chat features. ASGI entry: `test_system/asgi.py`. WebSocket URL: `ws/chat/<room_name>/` where `room_name` matches `[0-9a-f-]+` (UUID format) → `ChatConsumer`.

## CI/CD
GitHub Actions (`.github/workflows/ci.yml`) triggers on push to `dev` and `main`:
1. Build Docker images
2. Start services via `docker-compose.ci.yml`
3. Run `black --check` on backend
4. Run tests
5. Required secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `POSTGRES_PASSWORD`, `SECRET_KEY`

## CORS
Set via `CORS_ALLOWED_ORIGINS` env var (comma-separated); defaults to `http://localhost:8080` if unset. Configure in the backend `.env` file or deployment environment — no code change required.
