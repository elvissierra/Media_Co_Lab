# Media_Co_Lab — Onboarding & Registration Flow Design
**Date:** 2026-05-06  
**Status:** Approved for implementation

---

## Context

Registration is currently a dead end for all users. Org creators submit their org and land in `is_approved=False` limbo with no feedback and no path forward. Regular users who join an org get no membership state — they either have full access immediately or hit cryptic 400 errors. There is no in-app mechanism for the platform superuser to approve orgs, and no mechanism for org admins to manage their members. This spec fixes the entire onboarding path end-to-end.

---

## Goals

1. Platform superuser can view and approve/deny org registrations in-app
2. Org creator becomes org admin after platform approval; can manage member requests and teams
3. Regular users can register into an approved org and wait for org admin approval
4. All waiting states show clear, accurate UI — no cryptic errors
5. Critical security bugs fixed in the same pass

---

## 1. Data Model Changes

**File:** `backend/test_system/apps/users/models.py`

Add two fields to `CustomUser`:

```python
is_org_admin = models.BooleanField(default=False)
org_status = models.CharField(
    max_length=10,
    choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')],
    default='approved',
)
```

**Migration:** generate with `python manage.py makemigrations users`

**Rules:**
- Org creator on registration: `is_org_admin=True`, `org_status='approved'` (they're in their own org immediately; the org itself is pending platform approval)
- Regular user joining an org: `is_org_admin=False`, `org_status='pending'`
- Platform superuser approving an org does NOT change member `org_status` — only org admin actions do
- Denying a user sets `org_status='denied'`; they can still log in but see a denied screen

---

## 2. New Permission Classes

**File:** `backend/test_system/permissions.py`

```python
class IsPlatformAdmin(BasePermission):
    # has_permission: request.user.is_staff

class IsOrgAdmin(BasePermission):
    # has_permission: request.user.is_org_admin and user has an approved org
```

---

## 3. API Changes

### New endpoints

| Method | Endpoint | Permission | Action |
|--------|----------|------------|--------|
| GET | `/api/organizations/pending/` | `IsPlatformAdmin` | List orgs where `is_approved=False` |
| POST | `/api/organizations/{id}/approve/` | `IsPlatformAdmin` | Set `is_approved=True` |
| POST | `/api/organizations/{id}/deny/` | `IsPlatformAdmin` | Delete org (and notify creator via response) |
| GET | `/api/organizations/members/pending/` | `IsOrgAdmin` | List users in admin's org where `org_status='pending'` |
| POST | `/api/users/{user_id}/approve/` | `IsOrgAdmin` | Set `org_status='approved'`; auto-add to org's first team |
| POST | `/api/users/{user_id}/deny/` | `IsOrgAdmin` | Set `org_status='denied'` |

### Modified endpoints

**`POST /api/organizations/register/`**
- After creating org, set `request.user.is_org_admin=True` on the registering user
- `org_status` stays `'approved'` for the creator (they're the admin)

**`POST /api/users/create/`**
- If joining an existing approved org: set `org_status='pending'`
- If registering as org creator (no org selected): `org_status='approved'`, `is_org_admin=True`
- Serializer must distinguish the two paths via a `registration_type` field: `'join'` or `'create_org'`

**`POST /api/auth/login/`**
- Return generic `"Invalid credentials."` for both wrong email and wrong password — no distinguishing between the two

### Existing guarded views — add org_status check

All views that currently check `user.organization` must also check `user.org_status == 'approved'`. Return `403` with `{"detail": "Your membership is pending approval."}` for pending users. Affected views: medias, teams, labels, chats.

---

## 4. Frontend Changes

### Registration split — `UserRegister.vue`

Replace the single registration form with a two-path chooser:

**Path A — "Create an Organization"**
- Fields: First name, Last name, Email, Password, Organization name
- On submit: POST to `/api/organizations/register/` then POST to `/api/users/create/` with `registration_type: 'create_org'`
- On success: redirect to `/pending?type=org`

**Path B — "Join an Organization"**
- Fields: First name, Last name, Email, Password, Organization (dropdown of approved orgs)
- Org list fetched from existing `GET /api/organizations/` (already public)
- On submit: POST to `/api/users/create/` with `registration_type: 'join'`
- On success: redirect to `/pending?type=member`

### New page — `PendingApproval.vue` — route `/pending`

Two states driven by `?type=` query param:

**`?type=org`** (org creator waiting for platform approval):
> "Your organization registration is under review. You'll be able to access the platform once it's approved. Check back soon."

**`?type=member`** (user waiting for org admin approval):
> "Your membership request to [Org Name] is pending approval from your organization admin. You'll receive access once approved."

Both states: show logout button, no nav links. On every load, re-fetch user status and redirect to `HomePage` if now approved.

### New page — `PlatformAdmin.vue` — route `/platform-admin`

- Route guarded: redirect to `HomePage` if `!user.is_staff`
- Shows table: Org Name | Creator Email | Date Submitted | Actions (Approve / Deny)
- Fetches from `GET /api/organizations/pending/`
- Approve/Deny buttons call respective endpoints; row removes on action

### Expanded — `Organization.vue` (existing `/organizations/ov`)

Add a "Members" tab for org admins (`is_org_admin=true`):
- **Pending requests** list: Name, Email, Date — Approve / Deny buttons
- **Approved members** list: Name, Email, Teams

Non-admins see the existing org overview without the Members tab.

### Post-login routing — `UserLogin.vue`

After successful login, fetch user, then route based on state:

```
if user.is_staff → /platform-admin
else if user.org_status == 'pending' → /pending?type=member  
else if user.organization.is_approved == false → /pending?type=org
else if user.org_status == 'denied' → /denied (simple denied screen)
else → /medias (normal home)
```

### Vuex store additions

```javascript
state:
  - user.is_org_admin
  - user.org_status
  - user.is_staff

getters:
  - isOrgAdmin: !!state.user?.is_org_admin
  - isPlatformAdmin: !!state.user?.is_staff
  - isPendingApproval: state.user?.org_status === 'pending'
```

### Error handling — all components

Replace all `catch (e) { console.error(e) }` with Vuetify snackbar notifications. Add a shared `useNotify` composable or Vuex `notification` state that components dispatch to.

Add client-side validation to `UserLogin.vue` and `UserRegister.vue` before any API call:
- Email: must match `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Password: minimum 8 characters
- Required fields: show inline error messages

---

## 5. Security Fixes

| Bug | Fix | File |
|-----|-----|------|
| Chat PUT/DELETE unguarded | Add `IsAuthenticated` + ownership check (`obj.owner == request.user`) | `apis/chats/views.py` |
| User enumeration on login | Return identical error for wrong email and wrong password | `apis/users/views.py` (LoginView) |
| WebSocket route typo | Fix `rooom_name` → `room_name` in regex | `asgi.py` or `chats/routing.py` |
| Pending users hitting 400 | Return 403 with clear message instead | All guarded views |

---

## 6. Verification

**Manual happy paths to test:**

1. Register as org creator → land on `/pending?type=org` → log in as `is_staff` superuser → approve org → log back in as creator → land on `/organizations/ov` with Members tab visible
2. Register as regular user joining approved org → land on `/pending?type=member` → log in as org admin → approve member → member logs in → lands on `/medias`
3. Platform admin denies an org → org creator logs in → sees waiting room still (org deleted)
4. Org admin denies a member → member logs in → sees denied screen

**Security regression checks:**

1. Unauthenticated PUT to `/api/chats/{id}/` → 401
2. Authenticated user PUT to chat they don't own → 403
3. Login with wrong email and wrong password → same error message in both cases
4. WebSocket connects to `/ws/chat/room-name/` → no 404 (typo fix verified)

**Django tests to write (next phase):**
- `test_org_creator_gets_is_org_admin`
- `test_regular_user_gets_pending_status`
- `test_platform_admin_can_approve_org`
- `test_org_admin_can_approve_member`
- `test_pending_user_cannot_access_medias`
- `test_chat_put_requires_ownership`
- `test_login_returns_generic_error`

---

## Files to Modify

**Backend:**
- `backend/test_system/apps/users/models.py` — add `is_org_admin`, `org_status`
- `backend/test_system/permissions.py` — add `IsPlatformAdmin`, `IsOrgAdmin`
- `backend/test_system/apis/users/views.py` — registration split, login fix, approve/deny endpoints
- `backend/test_system/apis/organizations/views.py` — pending list, approve/deny endpoints
- `backend/test_system/apis/chats/views.py` — ownership guard on PUT/DELETE
- `backend/test_system/apis/medias/views.py` — org_status check
- `backend/test_system/apis/teams/views.py` — org_status check
- `backend/test_system/apis/labels/views.py` — org_status check
- `backend/test_system/urls.py` — register new routes
- `backend/test_system/asgi.py` or `chats/routing.py` — fix WebSocket typo

**Frontend:**
- `frontend/mcl_ui/src/components/UserRegister.vue` — two-path form
- `frontend/mcl_ui/src/components/UserLogin.vue` — post-login routing, validation
- `frontend/mcl_ui/src/components/PendingApproval.vue` — new
- `frontend/mcl_ui/src/components/PlatformAdmin.vue` — new
- `frontend/mcl_ui/src/components/Organization.vue` — Members tab for org admins
- `frontend/mcl_ui/src/store/index.js` — new getters/state
- `frontend/mcl_ui/src/router.js` — new routes + guards
