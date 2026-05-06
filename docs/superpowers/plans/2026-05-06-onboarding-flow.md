# Onboarding & Registration Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the broken registration and onboarding flow so org creators, platform admins, and regular users each have a clear, working path from signup to using the platform.

**Architecture:** Add `is_org_admin` and `org_status` fields to `CustomUser`; add `IsPlatformAdmin` and `IsOrgAdmin` permission classes; add 6 new API endpoints for org/member approval; split the registration form into two paths; add waiting room, platform admin dashboard, and org admin member management pages; fix 4 critical security bugs in the same pass.

**Tech Stack:** Django 5, DRF APIView, Knox auth, Vue 3, Vuex 4, Vuetify 3, PostgreSQL

---

## File Map

**Backend — modify:**
- `backend/test_system/apps/users/models.py` — add `is_org_admin`, `org_status`
- `backend/test_system/permissions.py` — add `IsPlatformAdmin`, `IsOrgAdmin`
- `backend/test_system/apis/users/serializers.py` — add `registration_type`, `org_status` to output
- `backend/test_system/apis/users/views.py` — registration split, login fix, approve/deny endpoints
- `backend/test_system/apis/organizations/views.py` — pending list, approve/deny endpoints
- `backend/test_system/apis/organizations/serializers.py` — add creator email/date to pending serializer
- `backend/test_system/apis/organizations/urls.py` — new routes
- `backend/test_system/apis/users/urls.py` — new routes
- `backend/test_system/apis/chats/views.py` — ownership guard on PUT/DELETE
- `backend/test_system/apis/chats/routing.py` — fix `rooom_name` typo
- `backend/test_system/apis/medias/views.py` — org_status guard
- `backend/test_system/apis/teams/views.py` — org_status guard
- `backend/test_system/apis/labels/views.py` — org_status guard

**Backend — create:**
- `backend/test_system/tests/__init__.py`
- `backend/test_system/tests/test_onboarding.py`
- `backend/test_system/tests/test_security.py`

**Frontend — modify:**
- `frontend/mcl_ui/src/components/UserRegister.vue` — two-path form
- `frontend/mcl_ui/src/components/UserLogin.vue` — post-login routing, validation
- `frontend/mcl_ui/src/components/Organization.vue` — members tab for org admins
- `frontend/mcl_ui/src/store/index.js` — new state/getters
- `frontend/mcl_ui/src/router.js` — new routes + guards

**Frontend — create:**
- `frontend/mcl_ui/src/components/PendingApproval.vue`
- `frontend/mcl_ui/src/components/PlatformAdmin.vue`

---

## Task 1: Add `is_org_admin` and `org_status` to CustomUser

**Files:**
- Modify: `backend/test_system/apps/users/models.py`
- Create: `backend/test_system/tests/__init__.py`
- Create: `backend/test_system/tests/test_onboarding.py`

- [ ] **Step 1: Create the tests directory and first failing test**

Create `backend/test_system/tests/__init__.py` (empty file).

Create `backend/test_system/tests/test_onboarding.py`:

```python
from django.test import TestCase
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization


class CustomUserFieldsTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(title="Test Org", is_approved=True)

    def test_user_has_is_org_admin_field(self):
        user = CustomUser.objects.create_user(
            email="admin@test.com", password="testpass123", organization=self.org
        )
        self.assertFalse(user.is_org_admin)

    def test_user_has_org_status_field(self):
        user = CustomUser.objects.create_user(
            email="user@test.com", password="testpass123", organization=self.org
        )
        self.assertEqual(user.org_status, "approved")

    def test_org_status_choices(self):
        user = CustomUser.objects.create_user(
            email="pending@test.com", password="testpass123", organization=self.org
        )
        user.org_status = "pending"
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.org_status, "pending")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `AttributeError: type object 'CustomUser' has no attribute 'is_org_admin'`

- [ ] **Step 3: Add fields to CustomUser model**

In `backend/test_system/apps/users/models.py`, add these two fields to the `CustomUser` class after the `avatar` field:

```python
is_org_admin = models.BooleanField(default=False)
org_status = models.CharField(
    max_length=10,
    choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")],
    default="approved",
)
```

- [ ] **Step 4: Create and run migration**

```bash
cd backend && python manage.py makemigrations users
python manage.py migrate
```

Expected output: `Applying users.0002_customuser_is_org_admin_customuser_org_status... OK`

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `OK` — 3 tests passing

- [ ] **Step 6: Commit**

```bash
git add backend/test_system/apps/users/models.py \
        backend/test_system/apps/users/migrations/ \
        backend/test_system/tests/
git commit -m "feat: add is_org_admin and org_status to CustomUser"
```

---

## Task 2: Add `IsPlatformAdmin` and `IsOrgAdmin` permission classes

**Files:**
- Modify: `backend/test_system/permissions.py`
- Modify: `backend/test_system/tests/test_onboarding.py`

- [ ] **Step 1: Write failing tests for new permissions**

Append to `backend/test_system/tests/test_onboarding.py`:

```python
from django.test import RequestFactory
from test_system.permissions import IsPlatformAdmin, IsOrgAdmin


class IsPlatformAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)

    def test_staff_user_has_permission(self):
        user = CustomUser.objects.create_user(
            email="staff@test.com", password="testpass123"
        )
        user.is_staff = True
        user.save()
        request = self.factory.get("/")
        request.user = user
        self.assertTrue(IsPlatformAdmin().has_permission(request, None))

    def test_non_staff_user_denied(self):
        user = CustomUser.objects.create_user(
            email="regular@test.com", password="testpass123", organization=self.org
        )
        request = self.factory.get("/")
        request.user = user
        self.assertFalse(IsPlatformAdmin().has_permission(request, None))


class IsOrgAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)

    def test_org_admin_has_permission(self):
        user = CustomUser.objects.create_user(
            email="orgadmin@test.com", password="testpass123", organization=self.org
        )
        user.is_org_admin = True
        user.org_status = "approved"
        user.save()
        request = self.factory.get("/")
        request.user = user
        self.assertTrue(IsOrgAdmin().has_permission(request, None))

    def test_non_org_admin_denied(self):
        user = CustomUser.objects.create_user(
            email="member@test.com", password="testpass123", organization=self.org
        )
        request = self.factory.get("/")
        request.user = user
        self.assertFalse(IsOrgAdmin().has_permission(request, None))

    def test_org_admin_with_no_org_denied(self):
        user = CustomUser.objects.create_user(
            email="noorga@test.com", password="testpass123"
        )
        user.is_org_admin = True
        user.save()
        request = self.factory.get("/")
        request.user = user
        self.assertFalse(IsOrgAdmin().has_permission(request, None))
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `ImportError: cannot import name 'IsPlatformAdmin' from 'test_system.permissions'`

- [ ] **Step 3: Add permission classes to permissions.py**

In `backend/test_system/permissions.py`, append after the existing `IsUser` class:

```python
class IsPlatformAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_org_admin
            and request.user.organization is not None
        )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `OK` — all tests passing

- [ ] **Step 5: Commit**

```bash
git add backend/test_system/permissions.py backend/test_system/tests/test_onboarding.py
git commit -m "feat: add IsPlatformAdmin and IsOrgAdmin permission classes"
```

---

## Task 3: Fix chat ownership guard and WebSocket typo (security fixes)

**Files:**
- Modify: `backend/test_system/apis/chats/views.py`
- Modify: `backend/test_system/apis/chats/routing.py`
- Create: `backend/test_system/tests/test_security.py`

- [ ] **Step 1: Write failing security tests**

Create `backend/test_system/tests/test_security.py`:

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.apps.teams.models import Team
from test_system.apps.medias.models import Medias
from test_system.apps.chats.models import Chat
from knox.models import AuthToken


class ChatOwnershipTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)
        self.team = Team.objects.create(title="Team A", organization=self.org)

        self.owner = CustomUser.objects.create_user(
            email="owner@test.com", password="testpass123", organization=self.org
        )
        self.owner.team.add(self.team)

        self.other = CustomUser.objects.create_user(
            email="other@test.com", password="testpass123", organization=self.org
        )
        self.other.team.add(self.team)

        self.media = Medias.objects.create(
            title="Test Media", user=self.owner, team=self.team
        )
        self.chat = Chat.objects.create(
            content="Original content", owner=self.owner, media=self.media
        )

        _, self.owner_token = AuthToken.objects.create(self.owner)
        _, self.other_token = AuthToken.objects.create(self.other)

    def test_unauthenticated_put_returns_401(self):
        response = self.client.put(
            f"/api/chats/{self.chat.id}/",
            {"content": "hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_non_owner_put_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_token}")
        response = self.client.put(
            f"/api/chats/{self.chat.id}/",
            {"content": "hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_owner_put_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.owner_token}")
        response = self.client.put(
            f"/api/chats/{self.chat.id}/",
            {"content": "updated"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_delete_returns_401(self):
        response = self.client.delete(f"/api/chats/{self.chat.id}/")
        self.assertEqual(response.status_code, 401)

    def test_non_owner_delete_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_token}")
        response = self.client.delete(f"/api/chats/{self.chat.id}/")
        self.assertEqual(response.status_code, 403)

    def test_owner_delete_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.owner_token}")
        response = self.client.delete(f"/api/chats/{self.chat.id}/")
        self.assertEqual(response.status_code, 204)


class LoginEnumerationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)
        CustomUser.objects.create_user(
            email="real@test.com", password="correctpass", organization=self.org
        )

    def test_wrong_email_and_wrong_password_return_same_error(self):
        r1 = self.client.post(
            "/api/auth/login/",
            {"email": "fake@test.com", "password": "wrong"},
            format="json",
        )
        r2 = self.client.post(
            "/api/auth/login/",
            {"email": "real@test.com", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(r1.status_code, 401)
        self.assertEqual(r2.status_code, 401)
        self.assertEqual(r1.data, r2.data)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_security -v 2
```

Expected: `FAIL` — unauthenticated PUT returns 200 (bug confirmed), login responses differ

- [ ] **Step 3: Fix ChatGetUpdateDeleteView**

Replace the full content of `backend/test_system/apis/chats/views.py` with:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.auth import TokenAuthentication
from django.shortcuts import get_object_or_404

from test_system.apps.chats.models import Chat
from test_system.apis.chats.serializers import (
    ChatsGetCreateSerializer,
    ChatGetUpdateDeleteSerializer,
)


class ChatsGetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        user_organization = user.organization
        if not user_organization:
            return Response(
                {"error": "User is not associated with an organization."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        chats = Chat.objects.filter(owner__organization=user_organization)
        serializer = ChatsGetCreateSerializer(chats, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatGetUpdateDeleteView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        serializer = ChatGetUpdateDeleteSerializer(chat, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        if chat.owner != request.user:
            return Response(
                {"error": "You do not have permission to edit this chat."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ChatGetUpdateDeleteSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        if chat.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this chat."},
                status=status.HTTP_403_FORBIDDEN,
            )
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

- [ ] **Step 4: Fix LoginView to return generic error**

In `backend/test_system/apis/users/views.py`, replace the `LoginView.post` method. Find the existing `LoginView` class and update it to:

```python
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return super().post(request, format=None)
```

Make sure these imports are present at the top of `apis/users/views.py`:
```python
from django.contrib.auth import authenticate, login
```

- [ ] **Step 5: Fix WebSocket routing typo**

In `backend/test_system/apis/chats/routing.py`, change:
```python
re_path(r"ws/chat/(?P<rooom_name>[0-9a-f-]+)/$", consumers.ChatConsumer.as_asgi())
```
to:
```python
re_path(r"ws/chat/(?P<room_name>[0-9a-f-]+)/$", consumers.ChatConsumer.as_asgi())
```

- [ ] **Step 6: Run security tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_security -v 2
```

Expected: `OK` — all 8 tests passing

- [ ] **Step 7: Commit**

```bash
git add backend/test_system/apis/chats/views.py \
        backend/test_system/apis/chats/routing.py \
        backend/test_system/apis/users/views.py \
        backend/test_system/tests/test_security.py
git commit -m "fix: guard chat mutations by ownership, fix login enumeration, fix WebSocket typo"
```

---

## Task 4: Split registration serializer into two paths

**Files:**
- Modify: `backend/test_system/apis/users/serializers.py`
- Modify: `backend/test_system/tests/test_onboarding.py`

- [ ] **Step 1: Write failing tests**

Append to `backend/test_system/tests/test_onboarding.py`:

```python
from rest_framework.test import APIRequestFactory
from test_system.apis.users.serializers import UserRegistrationSerializer


class RegistrationSerializerTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(title="Approved Org", is_approved=True)
        self.factory = APIRequestFactory()

    def test_join_path_sets_org_status_pending(self):
        request = self.factory.post("/")
        request.user = type("AnonymousUser", (), {"is_superuser": False})()
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "password": "securepass123",
            "organization_id": str(self.org.id),
            "registration_type": "join",
        }
        serializer = UserRegistrationSerializer(
            data=data, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.org_status, "pending")
        self.assertFalse(user.is_org_admin)

    def test_create_org_path_sets_org_admin(self):
        request = self.factory.post("/")
        request.user = type("AnonymousUser", (), {"is_superuser": False})()
        data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@test.com",
            "password": "securepass123",
            "organization_id": str(self.org.id),
            "registration_type": "create_org",
        }
        serializer = UserRegistrationSerializer(
            data=data, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.org_status, "approved")
        self.assertTrue(user.is_org_admin)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding.RegistrationSerializerTest -v 2
```

Expected: `FAIL` — serializer doesn't handle `registration_type`

- [ ] **Step 3: Update UserRegistrationSerializer**

Replace the `UserRegistrationSerializer` class in `backend/test_system/apis/users/serializers.py` with:

```python
class UserRegistrationSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    registration_type = serializers.ChoiceField(
        choices=["join", "create_org"], write_only=True, default="join"
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id", "team", "organization_id", "email", "password", "registration_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_organization_id(self, value):
        request = self.context.get("request")
        if value is None:
            if request and request.user.is_superuser:
                return value
            raise serializers.ValidationError("Organization is required.")
        try:
            org = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization not found.")
        if not org.is_approved:
            raise serializers.ValidationError("Organization is not approved.")
        return value

    def create(self, validated_data):
        organization_id = validated_data.pop("organization_id", None)
        registration_type = validated_data.pop("registration_type", "join")
        organization = None
        if organization_id:
            organization = Organization.objects.get(id=organization_id)

        is_org_admin = registration_type == "create_org"
        org_status = "approved" if is_org_admin else "pending"

        user = CustomUser.objects.create_user(
            organization=organization,
            **validated_data,
        )
        user.is_org_admin = is_org_admin
        user.org_status = org_status
        user.save()
        return user
```

Make sure `Organization` is imported at the top of `serializers.py`:
```python
from test_system.apps.organizations.models import Organization
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/test_system/apis/users/serializers.py \
        backend/test_system/tests/test_onboarding.py
git commit -m "feat: split registration serializer into join/create_org paths"
```

---

## Task 5: Add platform admin org approval endpoints

**Files:**
- Modify: `backend/test_system/apis/organizations/views.py`
- Modify: `backend/test_system/apis/organizations/serializers.py`
- Modify: `backend/test_system/apis/organizations/urls.py`
- Modify: `backend/test_system/tests/test_onboarding.py`

- [ ] **Step 1: Write failing tests**

Append to `backend/test_system/tests/test_onboarding.py`:

```python
from knox.models import AuthToken


class PlatformAdminOrgApprovalTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.pending_org = Organization.objects.create(
            title="Pending Org", is_approved=False
        )
        self.staff_user = CustomUser.objects.create_user(
            email="staff@test.com", password="testpass123"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.regular_user = CustomUser.objects.create_user(
            email="regular@test.com",
            password="testpass123",
            organization=Organization.objects.create(title="Other", is_approved=True),
        )
        _, self.staff_token = AuthToken.objects.create(self.staff_user)
        _, self.regular_token = AuthToken.objects.create(self.regular_user)

    def test_pending_orgs_list_requires_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token}")
        response = self.client.get("/api/organizations/pending/")
        self.assertEqual(response.status_code, 403)

    def test_staff_can_list_pending_orgs(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.staff_token}")
        response = self.client.get("/api/organizations/pending/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_staff_can_approve_org(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.staff_token}")
        response = self.client.post(
            f"/api/organizations/{self.pending_org.id}/approve/"
        )
        self.assertEqual(response.status_code, 200)
        self.pending_org.refresh_from_db()
        self.assertTrue(self.pending_org.is_approved)

    def test_staff_can_deny_org(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.staff_token}")
        response = self.client.post(
            f"/api/organizations/{self.pending_org.id}/deny/"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Organization.objects.filter(id=self.pending_org.id).exists()
        )

    def test_non_staff_cannot_approve_org(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token}")
        response = self.client.post(
            f"/api/organizations/{self.pending_org.id}/approve/"
        )
        self.assertEqual(response.status_code, 403)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding.PlatformAdminOrgApprovalTest -v 2
```

Expected: `404` on `/api/organizations/pending/` (routes don't exist yet)

- [ ] **Step 3: Add PendingOrganizationsGetSerializer**

In `backend/test_system/apis/organizations/serializers.py`, append:

```python
class PendingOrganizationSerializer(serializers.ModelSerializer):
    creator_email = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["id", "title", "creator_email", "created_at"]

    def get_creator_email(self, obj):
        creator = obj.users.filter(is_org_admin=True).first()
        return creator.email if creator else None

    def get_created_at(self, obj):
        creator = obj.users.filter(is_org_admin=True).first()
        return creator.date_joined.isoformat() if creator else None
```

Make sure `serializers` is imported:
```python
from rest_framework import serializers
```

- [ ] **Step 4: Add new views to organizations/views.py**

In `backend/test_system/apis/organizations/views.py`, append these three new view classes. Also add the required imports at the top if not present:

```python
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from test_system.permissions import OrganizationPermission, IsPlatformAdmin, IsOrgAdmin
from test_system.apis.organizations.serializers import (
    OrganizationSerializer,
    OrganizationGetSerializer,
    DemoOrgSerializer,
    PendingOrganizationSerializer,
)
```

Append the new view classes:

```python
class PendingOrganizationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPlatformAdmin]

    def get(self, request):
        orgs = Organization.objects.filter(is_approved=False)
        serializer = PendingOrganizationSerializer(orgs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationApproveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPlatformAdmin]

    def post(self, request, organization_id):
        org = get_object_or_404(Organization, id=organization_id)
        org.is_approved = True
        org.save()
        return Response({"detail": "Organization approved."}, status=status.HTTP_200_OK)


class OrganizationDenyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPlatformAdmin]

    def post(self, request, organization_id):
        org = get_object_or_404(Organization, id=organization_id)
        org.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Make sure `TokenAuthentication` is imported at the top of `views.py`:
```python
from knox.auth import TokenAuthentication
```

- [ ] **Step 5: Register new URLs**

In `backend/test_system/apis/organizations/urls.py`, add the new routes. The file should look like:

```python
from django.urls import path
from test_system.apis.organizations.views import (
    OrganizationsGetView,
    UserOrganizationView,
    OrganizationCreateView,
    DemoOrgCreateView,
    OrganizationGetUpdateDeleteView,
    PendingOrganizationsView,
    OrganizationApproveView,
    OrganizationDenyView,
)

urlpatterns = [
    path("", OrganizationsGetView.as_view()),
    path("ov/", UserOrganizationView.as_view()),
    path("register/", OrganizationCreateView.as_view()),
    path("demo/", DemoOrgCreateView.as_view()),
    path("pending/", PendingOrganizationsView.as_view()),
    path("<uuid:organization_id>/", OrganizationGetUpdateDeleteView.as_view()),
    path("<uuid:organization_id>/approve/", OrganizationApproveView.as_view()),
    path("<uuid:organization_id>/deny/", OrganizationDenyView.as_view()),
]
```

- [ ] **Step 6: Update OrganizationCreateView to set org admin on creator**

In `backend/test_system/apis/organizations/views.py`, update `OrganizationCreateView.post` to set `is_org_admin=True` on the requesting user after org is created. If the user isn't authenticated, skip (org can be created anonymously during the two-step registration):

```python
class OrganizationCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            org = serializer.save()
            if request.user.is_authenticated:
                request.user.organization = org
                request.user.is_org_admin = True
                request.user.org_status = "approved"
                request.user.save()
            return Response(
                {"id": str(org.id), "title": org.title},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

- [ ] **Step 7: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git add backend/test_system/apis/organizations/views.py \
        backend/test_system/apis/organizations/serializers.py \
        backend/test_system/apis/organizations/urls.py \
        backend/test_system/tests/test_onboarding.py
git commit -m "feat: add platform admin org pending/approve/deny endpoints"
```

---

## Task 6: Add org admin member approval endpoints

**Files:**
- Modify: `backend/test_system/apis/users/views.py`
- Modify: `backend/test_system/apis/users/urls.py`
- Modify: `backend/test_system/apis/users/serializers.py`
- Modify: `backend/test_system/tests/test_onboarding.py`

- [ ] **Step 1: Write failing tests**

Append to `backend/test_system/tests/test_onboarding.py`:

```python
class OrgAdminMemberApprovalTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)

        self.org_admin = CustomUser.objects.create_user(
            email="orgadmin@test.com", password="testpass123", organization=self.org
        )
        self.org_admin.is_org_admin = True
        self.org_admin.org_status = "approved"
        self.org_admin.save()

        self.pending_user = CustomUser.objects.create_user(
            email="pending@test.com", password="testpass123", organization=self.org
        )
        self.pending_user.org_status = "pending"
        self.pending_user.save()

        self.other_org = Organization.objects.create(title="Other Org", is_approved=True)
        self.other_admin = CustomUser.objects.create_user(
            email="otheradmin@test.com", password="testpass123", organization=self.other_org
        )
        self.other_admin.is_org_admin = True
        self.other_admin.org_status = "approved"
        self.other_admin.save()

        _, self.admin_token = AuthToken.objects.create(self.org_admin)
        _, self.other_admin_token = AuthToken.objects.create(self.other_admin)

    def test_org_admin_can_list_pending_members(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token}")
        response = self.client.get("/api/organizations/members/pending/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "pending@test.com")

    def test_org_admin_cannot_see_other_org_pending_members(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_admin_token}")
        response = self.client.get("/api/organizations/members/pending/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_org_admin_can_approve_member(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token}")
        response = self.client.post(
            f"/api/users/{self.pending_user.id}/approve/"
        )
        self.assertEqual(response.status_code, 200)
        self.pending_user.refresh_from_db()
        self.assertEqual(self.pending_user.org_status, "approved")

    def test_org_admin_can_deny_member(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token}")
        response = self.client.post(
            f"/api/users/{self.pending_user.id}/deny/"
        )
        self.assertEqual(response.status_code, 200)
        self.pending_user.refresh_from_db()
        self.assertEqual(self.pending_user.org_status, "denied")

    def test_non_org_admin_cannot_approve_member(self):
        non_admin = CustomUser.objects.create_user(
            email="member@test.com", password="testpass123", organization=self.org
        )
        _, token = AuthToken.objects.create(non_admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(f"/api/users/{self.pending_user.id}/approve/")
        self.assertEqual(response.status_code, 403)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding.OrgAdminMemberApprovalTest -v 2
```

Expected: `404` (routes don't exist yet)

- [ ] **Step 3: Add pending members view and approve/deny views to users/views.py**

In `backend/test_system/apis/users/views.py`, append these new view classes. Add imports at top if missing:

```python
from test_system.permissions import IsUser, IsOrgAdmin, IsPlatformAdmin
```

Append the new classes:

```python
class PendingMembersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def get(self, request):
        org = request.user.organization
        pending = CustomUser.objects.filter(organization=org, org_status="pending")
        serializer = UsersGetSerializer(pending, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserApproveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def post(self, request, user_id):
        from test_system.apps.teams.models import Team
        target = get_object_or_404(
            CustomUser, id=user_id, organization=request.user.organization
        )
        target.org_status = "approved"
        target.save()
        # Auto-add to the org's first team so the user can access resources
        first_team = Team.objects.filter(organization=request.user.organization).first()
        if first_team:
            target.team.add(first_team)
        return Response({"detail": "User approved."}, status=status.HTTP_200_OK)


class UserDenyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def post(self, request, user_id):
        target = get_object_or_404(
            CustomUser, id=user_id, organization=request.user.organization
        )
        target.org_status = "denied"
        target.save()
        return Response({"detail": "User denied."}, status=status.HTTP_200_OK)
```

Make sure `get_object_or_404` is imported:
```python
from django.shortcuts import get_object_or_404
```

- [ ] **Step 4: Add pending members route to organizations/urls.py**

In `backend/test_system/apis/organizations/urls.py`, add:

```python
from test_system.apis.users.views import PendingMembersView

# Add to urlpatterns:
path("members/pending/", PendingMembersView.as_view()),
```

- [ ] **Step 5: Add approve/deny user routes to users/urls.py**

In `backend/test_system/apis/users/urls.py`, the file should look like:

```python
from django.urls import path
from test_system.apis.users.views import (
    UsersGetView,
    UserCreateView,
    UserGetPatchDeleteView,
    UserApproveView,
    UserDenyView,
)

urlpatterns = [
    path("", UsersGetView.as_view()),
    path("create/", UserCreateView.as_view()),
    path("<uuid:user_id>/", UserGetPatchDeleteView.as_view()),
    path("<uuid:user_id>/approve/", UserApproveView.as_view()),
    path("<uuid:user_id>/deny/", UserDenyView.as_view()),
]
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests.test_onboarding -v 2
```

Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add backend/test_system/apis/users/views.py \
        backend/test_system/apis/users/urls.py \
        backend/test_system/apis/organizations/urls.py \
        backend/test_system/tests/test_onboarding.py
git commit -m "feat: add org admin member pending/approve/deny endpoints"
```

---

## Task 7: Add org_status guard to guarded views

**Files:**
- Modify: `backend/test_system/apis/medias/views.py`
- Modify: `backend/test_system/apis/teams/views.py`
- Modify: `backend/test_system/apis/labels/views.py`
- Modify: `backend/test_system/tests/test_security.py`

- [ ] **Step 1: Write failing test**

Append to `backend/test_system/tests/test_security.py`:

```python
class PendingUserAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(title="Test Org", is_approved=True)
        self.pending_user = CustomUser.objects.create_user(
            email="pending@test.com", password="testpass123", organization=self.org
        )
        self.pending_user.org_status = "pending"
        self.pending_user.save()
        _, self.token = AuthToken.objects.create(self.pending_user)

    def test_pending_user_cannot_access_medias(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/api/medias/")
        self.assertEqual(response.status_code, 403)

    def test_pending_user_cannot_access_teams(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/api/teams/")
        self.assertEqual(response.status_code, 403)

    def test_pending_user_cannot_access_labels(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/api/labels/")
        self.assertEqual(response.status_code, 403)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && python manage.py test test_system.tests.test_security.PendingUserAccessTest -v 2
```

Expected: `FAIL` — pending users get 400, not 403

- [ ] **Step 3: Add org_status check helper**

Add this helper function to `backend/test_system/permissions.py`:

```python
def check_org_membership_approved(request):
    """Returns a 403 Response if user's org_status is not approved, else None."""
    from rest_framework.response import Response
    from rest_framework import status
    if not hasattr(request.user, "org_status"):
        return None
    if request.user.org_status != "approved":
        return Response(
            {"detail": "Your membership is pending approval."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None
```

- [ ] **Step 4: Add guard to medias views**

In `backend/test_system/apis/medias/views.py`, find the `MediasGetCreateView.get` and `MediasGetCreateView.post` methods. At the top of each method body (after `user = request.user`), add:

```python
from test_system.permissions import check_org_membership_approved

# Inside MediasGetCreateView.get:
blocked = check_org_membership_approved(request)
if blocked:
    return blocked

# Inside MediasGetCreateView.post:
blocked = check_org_membership_approved(request)
if blocked:
    return blocked
```

Do the same for `MediasUserView.get`.

- [ ] **Step 5: Add guard to teams views**

In `backend/test_system/apis/teams/views.py`, find `TeamsGetCreateView.get` and `TeamsGetCreateView.post`. At the top of each method body, add:

```python
from test_system.permissions import check_org_membership_approved

blocked = check_org_membership_approved(request)
if blocked:
    return blocked
```

- [ ] **Step 6: Add guard to labels views**

In `backend/test_system/apis/labels/views.py`, find `LabelsGetCreateView.get` and `LabelsGetCreateView.post`. At the top of each method body, add:

```python
from test_system.permissions import check_org_membership_approved

blocked = check_org_membership_approved(request)
if blocked:
    return blocked
```

- [ ] **Step 7: Run tests to verify they pass**

```bash
cd backend && python manage.py test test_system.tests -v 2
```

Expected: `OK` — all tests passing

- [ ] **Step 8: Commit**

```bash
git add backend/test_system/permissions.py \
        backend/test_system/apis/medias/views.py \
        backend/test_system/apis/teams/views.py \
        backend/test_system/apis/labels/views.py \
        backend/test_system/tests/test_security.py
git commit -m "feat: block pending org members from accessing medias/teams/labels"
```

---

## Task 8: Add `org_status` and `is_org_admin` to user API response

**Files:**
- Modify: `backend/test_system/apis/users/serializers.py`

- [ ] **Step 1: Update UsersGetSerializer to include new fields**

In `backend/test_system/apis/users/serializers.py`, find `UsersGetSerializer` and add `is_org_admin` and `org_status` to its `fields` list:

```python
class UsersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "team", "organization", "labels", "avatar",
            "is_org_admin", "org_status", "is_staff",
        ]
    # ... keep existing to_representation method unchanged
```

- [ ] **Step 2: Run all tests to confirm nothing broke**

```bash
cd backend && python manage.py test test_system.tests -v 2
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/test_system/apis/users/serializers.py
git commit -m "feat: include is_org_admin, org_status, is_staff in user API response"
```

---

## Task 9: Frontend — Vuex store additions

**Files:**
- Modify: `frontend/mcl_ui/src/store/index.js`

- [ ] **Step 1: Update Vuex store**

In `frontend/mcl_ui/src/store/index.js`, update the store to add new getters. The `state`, `mutations`, and `getters` sections should include:

```javascript
state: {
  user: null,
  authToken: localStorage.getItem("authToken") || null,
},

mutations: {
  setUser(state, user) {
    state.user = user;
  },
  setUserOrganization(state, organization) {
    if (state.user) state.user.organization = organization;
  },
  setAuthToken(state, token) {
    state.authToken = token;
    if (token) {
      localStorage.setItem("authToken", token);
    } else {
      localStorage.removeItem("authToken");
    }
  },
},

getters: {
  isLoggedIn: (state) => !!state.authToken,
  userHasOrganization: (state) => !!state.user?.organization,
  isOrgAdmin: (state) => !!state.user?.is_org_admin,
  isPlatformAdmin: (state) => !!state.user?.is_staff,
  isPendingApproval: (state) => state.user?.org_status === "pending",
  isDenied: (state) => state.user?.org_status === "denied",
  orgIsApproved: (state) => !!state.user?.organization?.is_approved,
},

actions: {
  async fetchUser({ commit }, userId) {
    const response = await axios.get(`/api/users/${userId}/`);
    commit("setUser", response.data);
    return response.data;
  },
},
```

Make sure `axios` (authenticated) is imported at the top of `store/index.js`:
```javascript
import axios from "@/axios";
```

- [ ] **Step 2: Commit**

```bash
git add frontend/mcl_ui/src/store/index.js
git commit -m "feat: add isOrgAdmin, isPlatformAdmin, isPendingApproval getters to Vuex store"
```

---

## Task 10: Frontend — PendingApproval.vue page

**Files:**
- Create: `frontend/mcl_ui/src/components/PendingApproval.vue`
- Modify: `frontend/mcl_ui/src/router.js`

- [ ] **Step 1: Create PendingApproval.vue**

Create `frontend/mcl_ui/src/components/PendingApproval.vue`:

```vue
<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card max-width="520" class="pa-8 text-center" elevation="2">
      <v-icon size="64" color="warning" class="mb-4">mdi-clock-outline</v-icon>

      <v-card-title class="text-h5 mb-2">
        {{ title }}
      </v-card-title>

      <v-card-text class="text-body-1 mb-6">
        {{ message }}
      </v-card-text>

      <v-btn variant="outlined" color="primary" @click="checkStatus" :loading="checking" class="mr-3">
        Check Status
      </v-btn>
      <v-btn variant="text" color="error" @click="logout">
        Log Out
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "@/axios";

export default {
  name: "PendingApproval",
  data() {
    return { checking: false };
  },
  computed: {
    ...mapGetters(["isPendingApproval", "isDenied", "orgIsApproved"]),
    type() {
      return this.$route.query.type || "member";
    },
    title() {
      return this.type === "org"
        ? "Organization Pending Review"
        : "Membership Pending Approval";
    },
    message() {
      if (this.type === "org") {
        return "Your organization registration is under review. You will be able to access the platform once it is approved by our team.";
      }
      const orgName = this.$store.state.user?.organization?.title || "your organization";
      return `Your membership request to ${orgName} is pending approval from the organization admin.`;
    },
  },
  methods: {
    async checkStatus() {
      this.checking = true;
      try {
        const userId = this.$store.state.user?.id;
        if (!userId) return;
        const response = await axios.get(`/api/users/${userId}/`);
        this.$store.commit("setUser", response.data);
        this.redirectIfUnblocked(response.data);
      } finally {
        this.checking = false;
      }
    },
    redirectIfUnblocked(user) {
      if (user.is_staff) {
        this.$router.push("/platform-admin");
      } else if (user.org_status === "approved" && user.organization?.is_approved) {
        this.$router.push("/medias");
      } else if (user.org_status === "denied") {
        this.$router.push("/denied");
      }
    },
    logout() {
      this.$store.commit("setAuthToken", null);
      this.$store.commit("setUser", null);
      this.$router.push("/login");
    },
  },
};
</script>
```

- [ ] **Step 2: Add `/pending` and `/denied` routes to router.js**

In `frontend/mcl_ui/src/router.js`, add these routes to the `routes` array:

```javascript
import PendingApproval from "@/components/PendingApproval.vue";

// Add to routes array:
{
  path: "/pending",
  name: "PendingApproval",
  component: PendingApproval,
  beforeEnter: requireAuth,
},
{
  path: "/denied",
  name: "DeniedAccess",
  component: {
    template: `
      <v-container class="fill-height d-flex align-center justify-center">
        <v-card max-width="480" class="pa-8 text-center">
          <v-icon size="64" color="error" class="mb-4">mdi-account-cancel</v-icon>
          <v-card-title class="text-h5 mb-2">Access Denied</v-card-title>
          <v-card-text>Your membership request was denied. Contact the organization admin for more information.</v-card-text>
          <v-btn variant="outlined" color="primary" @click="$router.push('/login')">Back to Login</v-btn>
        </v-card>
      </v-container>
    `,
  },
  beforeEnter: requireAuth,
},
```

- [ ] **Step 3: Commit**

```bash
git add frontend/mcl_ui/src/components/PendingApproval.vue \
        frontend/mcl_ui/src/router.js
git commit -m "feat: add PendingApproval and DeniedAccess pages"
```

---

## Task 11: Frontend — PlatformAdmin.vue dashboard

**Files:**
- Create: `frontend/mcl_ui/src/components/PlatformAdmin.vue`
- Modify: `frontend/mcl_ui/src/router.js`

- [ ] **Step 1: Create PlatformAdmin.vue**

Create `frontend/mcl_ui/src/components/PlatformAdmin.vue`:

```vue
<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4">Platform Admin — Pending Organizations</h1>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>
    <v-alert v-if="successMsg" type="success" class="mb-4">{{ successMsg }}</v-alert>

    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-card v-if="!loading && pendingOrgs.length === 0" class="pa-6 text-center">
      <v-icon size="48" color="success" class="mb-3">mdi-check-circle</v-icon>
      <p class="text-body-1">No pending organizations.</p>
    </v-card>

    <v-table v-if="pendingOrgs.length > 0">
      <thead>
        <tr>
          <th>Organization</th>
          <th>Creator</th>
          <th>Submitted</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="org in pendingOrgs" :key="org.id">
          <td>{{ org.title }}</td>
          <td>{{ org.creator_email || "—" }}</td>
          <td>{{ formatDate(org.created_at) }}</td>
          <td>
            <v-btn
              size="small"
              color="success"
              variant="tonal"
              class="mr-2"
              :loading="actionLoading === org.id + '-approve'"
              @click="approve(org)"
            >Approve</v-btn>
            <v-btn
              size="small"
              color="error"
              variant="tonal"
              :loading="actionLoading === org.id + '-deny'"
              @click="deny(org)"
            >Deny</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import axios from "@/axios";

export default {
  name: "PlatformAdmin",
  data() {
    return {
      pendingOrgs: [],
      loading: false,
      actionLoading: null,
      error: null,
      successMsg: null,
    };
  },
  mounted() {
    this.fetchPending();
  },
  methods: {
    async fetchPending() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/organizations/pending/");
        this.pendingOrgs = response.data;
      } catch {
        this.error = "Failed to load pending organizations.";
      } finally {
        this.loading = false;
      }
    },
    async approve(org) {
      this.actionLoading = org.id + "-approve";
      this.error = null;
      try {
        await axios.post(`/api/organizations/${org.id}/approve/`);
        this.pendingOrgs = this.pendingOrgs.filter((o) => o.id !== org.id);
        this.successMsg = `"${org.title}" approved.`;
      } catch {
        this.error = "Failed to approve organization.";
      } finally {
        this.actionLoading = null;
      }
    },
    async deny(org) {
      this.actionLoading = org.id + "-deny";
      this.error = null;
      try {
        await axios.post(`/api/organizations/${org.id}/deny/`);
        this.pendingOrgs = this.pendingOrgs.filter((o) => o.id !== org.id);
        this.successMsg = `"${org.title}" denied and removed.`;
      } catch {
        this.error = "Failed to deny organization.";
      } finally {
        this.actionLoading = null;
      }
    },
    formatDate(iso) {
      if (!iso) return "—";
      return new Date(iso).toLocaleDateString();
    },
  },
};
</script>
```

- [ ] **Step 2: Add `/platform-admin` route to router.js**

In `frontend/mcl_ui/src/router.js`, add:

```javascript
import PlatformAdmin from "@/components/PlatformAdmin.vue";

// Add to routes array — add the platform admin guard inline:
{
  path: "/platform-admin",
  name: "PlatformAdmin",
  component: PlatformAdmin,
  beforeEnter: (to, from, next) => {
    const token = localStorage.getItem("authToken");
    if (!token) return next("/login");
    next(); // server will 403 if not staff; component handles it
  },
},
```

- [ ] **Step 3: Commit**

```bash
git add frontend/mcl_ui/src/components/PlatformAdmin.vue \
        frontend/mcl_ui/src/router.js
git commit -m "feat: add platform admin dashboard for org approval"
```

---

## Task 12: Frontend — Split UserRegister.vue into two paths

**Files:**
- Modify: `frontend/mcl_ui/src/components/UserRegister.vue`

- [ ] **Step 1: Replace UserRegister.vue**

Replace the full content of `frontend/mcl_ui/src/components/UserRegister.vue` with:

```vue
<template>
  <v-container class="py-8" max-width="560">
    <!-- Path chooser -->
    <div v-if="!registrationPath" class="text-center">
      <h1 class="text-h4 mb-2">Get Started</h1>
      <p class="text-body-1 mb-8 text-medium-emphasis">How would you like to use Media Co-Lab?</p>
      <v-row justify="center" class="gap-4">
        <v-col cols="12" sm="5">
          <v-card
            class="pa-6 text-center cursor-pointer"
            elevation="2"
            hover
            @click="registrationPath = 'create_org'"
          >
            <v-icon size="48" color="primary" class="mb-3">mdi-domain</v-icon>
            <div class="text-h6 mb-1">Create an Organization</div>
            <div class="text-body-2 text-medium-emphasis">Register a new org — you'll be its admin</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="5">
          <v-card
            class="pa-6 text-center cursor-pointer"
            elevation="2"
            hover
            @click="registrationPath = 'join'"
          >
            <v-icon size="48" color="secondary" class="mb-3">mdi-account-group</v-icon>
            <div class="text-h6 mb-1">Join an Organization</div>
            <div class="text-body-2 text-medium-emphasis">Request access to an existing org</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Registration form -->
    <v-card v-else class="pa-8" elevation="2">
      <v-btn variant="text" class="mb-4" @click="registrationPath = null">
        <v-icon start>mdi-arrow-left</v-icon> Back
      </v-btn>

      <h2 class="text-h5 mb-6">
        {{ registrationPath === 'create_org' ? 'Register Your Organization' : 'Join an Organization' }}
      </h2>

      <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

      <v-form @submit.prevent="submit" ref="form">
        <!-- Org name (create_org path only) -->
        <v-text-field
          v-if="registrationPath === 'create_org'"
          v-model="orgName"
          label="Organization Name"
          :rules="[v => !!v || 'Organization name is required']"
          variant="outlined"
          class="mb-3"
          required
        />

        <!-- Org selector (join path only) -->
        <v-select
          v-if="registrationPath === 'join'"
          v-model="selectedOrgId"
          :items="approvedOrgs"
          item-title="title"
          item-value="id"
          label="Select Organization"
          :rules="[v => !!v || 'Please select an organization']"
          variant="outlined"
          class="mb-3"
          :loading="orgsLoading"
          required
        />

        <v-text-field
          v-model="firstName"
          label="First Name"
          :rules="[v => !!v || 'First name is required']"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="lastName"
          label="Last Name"
          :rules="[v => !!v || 'Last name is required']"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          :rules="emailRules"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          :rules="[v => !!v || 'Password is required', v => v.length >= 8 || 'Minimum 8 characters']"
          variant="outlined"
          class="mb-6"
          required
        />

        <v-btn type="submit" color="primary" block :loading="loading" size="large">
          {{ registrationPath === 'create_org' ? 'Register Organization' : 'Request Access' }}
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axiosPublic from "@/axiosPublic";
import axios from "@/axios";

export default {
  name: "UserRegister",
  data() {
    return {
      registrationPath: null,
      orgName: "",
      selectedOrgId: null,
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      approvedOrgs: [],
      orgsLoading: false,
      loading: false,
      error: null,
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "Must be a valid email",
      ],
    };
  },
  watch: {
    registrationPath(val) {
      if (val === "join" && this.approvedOrgs.length === 0) {
        this.fetchOrgs();
      }
    },
  },
  methods: {
    async fetchOrgs() {
      this.orgsLoading = true;
      try {
        const response = await axiosPublic.get("/api/organizations/");
        this.approvedOrgs = response.data;
      } catch {
        this.error = "Failed to load organizations.";
      } finally {
        this.orgsLoading = false;
      }
    },
    async submit() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.loading = true;
      this.error = null;

      try {
        if (this.registrationPath === "create_org") {
          await this.registerWithOrg();
        } else {
          await this.joinOrg();
        }
      } catch (err) {
        this.error =
          err.response?.data?.detail ||
          Object.values(err.response?.data || {})[0]?.[0] ||
          "Registration failed. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    async registerWithOrg() {
      // Step 1: create the org
      const orgResponse = await axiosPublic.post("/api/organizations/register/", {
        title: this.orgName,
      });
      const orgId = orgResponse.data.id;

      // Step 2: register the user as org admin
      await axiosPublic.post("/api/users/create/", {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
        password: this.password,
        organization_id: orgId,
        registration_type: "create_org",
      });

      this.$router.push("/login?registered=org");
    },
    async joinOrg() {
      await axiosPublic.post("/api/users/create/", {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
        password: this.password,
        organization_id: this.selectedOrgId,
        registration_type: "join",
      });

      this.$router.push("/login?registered=member");
    },
  },
};
</script>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/mcl_ui/src/components/UserRegister.vue
git commit -m "feat: split registration into create_org and join paths"
```

---

## Task 13: Frontend — Fix UserLogin.vue post-login routing and validation

**Files:**
- Modify: `frontend/mcl_ui/src/components/UserLogin.vue`

- [ ] **Step 1: Update UserLogin.vue**

Replace or update `frontend/mcl_ui/src/components/UserLogin.vue` to include validation and smart post-login routing. The key changes:

1. Add `emailRules` and `passwordRules` for client-side validation
2. After successful login, fetch user and route based on state
3. Show a banner if coming from registration

```vue
<template>
  <v-container class="py-8" max-width="480">
    <v-card class="pa-8" elevation="2">
      <h1 class="text-h4 mb-2 text-center">Sign In</h1>

      <v-alert v-if="registeredMsg" type="success" class="mb-4">{{ registeredMsg }}</v-alert>
      <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

      <v-form @submit.prevent="submit" ref="form">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          :rules="emailRules"
          variant="outlined"
          class="mb-3"
          required
        />
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          :rules="[v => !!v || 'Password is required']"
          variant="outlined"
          class="mb-6"
          required
        />
        <v-btn type="submit" color="primary" block :loading="loading" size="large">
          Sign In
        </v-btn>
      </v-form>

      <div class="text-center mt-4">
        <span class="text-body-2">Don't have an account? </span>
        <router-link to="/register" class="text-primary">Register</router-link>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axiosPublic from "@/axiosPublic";
import axios from "@/axios";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: null,
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "Must be a valid email",
      ],
    };
  },
  computed: {
    registeredMsg() {
      const type = this.$route.query.registered;
      if (type === "org") return "Organization registered! Sign in to continue — platform approval may take 1-2 business days.";
      if (type === "member") return "Request submitted! Sign in to check your status.";
      return null;
    },
  },
  methods: {
    async submit() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.loading = true;
      this.error = null;

      try {
        const loginResponse = await axiosPublic.post("/api/auth/login/", {
          email: this.email,
          password: this.password,
        });

        const token = loginResponse.data.token;
        this.$store.commit("setAuthToken", token);

        // Fetch full user to determine routing
        const meResponse = await axios.get("/api/users/me/");
        const user = meResponse.data;
        this.$store.commit("setUser", user);

        this.routeAfterLogin(user);
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          err.response?.data?.detail ||
          "Invalid credentials.";
      } finally {
        this.loading = false;
      }
    },
    routeAfterLogin(user) {
      if (user.is_staff) {
        this.$router.push("/platform-admin");
      } else if (!user.organization) {
        this.$router.push("/organizations/reg");
      } else if (!user.organization.is_approved) {
        this.$router.push("/pending?type=org");
      } else if (user.org_status === "pending") {
        this.$router.push("/pending?type=member");
      } else if (user.org_status === "denied") {
        this.$router.push("/denied");
      } else {
        this.$router.push("/medias");
      }
    },
  },
};
</script>
```

- [ ] **Step 2: Add `/api/users/me/` endpoint to backend**

The login routing above calls `/api/users/me/` to get the current user. Add this view to `backend/test_system/apis/users/views.py`:

```python
class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsersGetSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
```

Add to `backend/test_system/apis/users/urls.py`:

```python
from test_system.apis.users.views import (
    UsersGetView, UserCreateView, UserGetPatchDeleteView,
    UserApproveView, UserDenyView, CurrentUserView,
)

urlpatterns = [
    path("", UsersGetView.as_view()),
    path("me/", CurrentUserView.as_view()),
    path("create/", UserCreateView.as_view()),
    path("<uuid:user_id>/", UserGetPatchDeleteView.as_view()),
    path("<uuid:user_id>/approve/", UserApproveView.as_view()),
    path("<uuid:user_id>/deny/", UserDenyView.as_view()),
]
```

- [ ] **Step 3: Run all backend tests**

```bash
cd backend && python manage.py test test_system.tests -v 2
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add frontend/mcl_ui/src/components/UserLogin.vue \
        backend/test_system/apis/users/views.py \
        backend/test_system/apis/users/urls.py
git commit -m "feat: smart post-login routing and client-side validation in UserLogin"
```

---

## Task 14: Frontend — Org admin Members tab in Organization.vue

**Files:**
- Modify: `frontend/mcl_ui/src/components/Organization.vue`

- [ ] **Step 1: Add Members tab to Organization.vue**

In `frontend/mcl_ui/src/components/Organization.vue`, add a members management tab that is only visible to org admins. Find the template section and add after the existing org info content:

```vue
<!-- Add inside the existing template, after existing org content -->
<v-tabs v-if="isOrgAdmin" v-model="activeTab" class="mt-6">
  <v-tab value="overview">Overview</v-tab>
  <v-tab value="members">Members <v-badge v-if="pendingMembers.length" :content="pendingMembers.length" color="warning" inline /></v-tab>
</v-tabs>

<v-window v-if="isOrgAdmin" v-model="activeTab" class="mt-4">
  <v-window-item value="overview">
    <!-- existing org content stays here -->
  </v-window-item>

  <v-window-item value="members">
    <h3 class="text-h6 mb-4">Pending Requests</h3>

    <v-alert v-if="memberError" type="error" class="mb-3">{{ memberError }}</v-alert>
    <v-alert v-if="memberSuccess" type="success" class="mb-3">{{ memberSuccess }}</v-alert>

    <v-card v-if="pendingMembers.length === 0" class="pa-4 text-center mb-6">
      <p class="text-body-2 text-medium-emphasis">No pending requests.</p>
    </v-card>

    <v-list v-else class="mb-6">
      <v-list-item
        v-for="member in pendingMembers"
        :key="member.id"
        :title="member.first_name + ' ' + member.last_name"
        :subtitle="member.email"
      >
        <template #append>
          <v-btn size="small" color="success" variant="tonal" class="mr-2"
            :loading="memberActionLoading === member.id + '-approve'"
            @click="approveMember(member)">Approve</v-btn>
          <v-btn size="small" color="error" variant="tonal"
            :loading="memberActionLoading === member.id + '-deny'"
            @click="denyMember(member)">Deny</v-btn>
        </template>
      </v-list-item>
    </v-list>

    <h3 class="text-h6 mb-4">Approved Members</h3>
    <v-list>
      <v-list-item
        v-for="member in approvedMembers"
        :key="member.id"
        :title="member.first_name + ' ' + member.last_name"
        :subtitle="member.email"
      >
        <template #prepend>
          <v-avatar color="primary" size="36">
            <span class="text-caption">{{ member.first_name[0] }}{{ member.last_name[0] }}</span>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>
  </v-window-item>
</v-window>
```

In the `<script>` section of `Organization.vue`, add to `data()`:

```javascript
activeTab: "overview",
pendingMembers: [],
approvedMembers: [],
memberError: null,
memberSuccess: null,
memberActionLoading: null,
```

Add to `computed`:

```javascript
isOrgAdmin() {
  return this.$store.getters.isOrgAdmin;
},
```

Add to `mounted()` (or create it if missing):

```javascript
if (this.isOrgAdmin) {
  this.fetchPendingMembers();
  this.fetchApprovedMembers();
}
```

Add to `methods`:

```javascript
async fetchPendingMembers() {
  try {
    const response = await axios.get("/api/organizations/members/pending/");
    this.pendingMembers = response.data;
  } catch {
    this.memberError = "Failed to load pending members.";
  }
},
async fetchApprovedMembers() {
  try {
    const response = await axios.get("/api/users/");
    this.approvedMembers = response.data.filter(
      (u) => u.org_status === "approved" && !u.is_org_admin
    );
  } catch {
    this.memberError = "Failed to load members.";
  }
},
async approveMember(member) {
  this.memberActionLoading = member.id + "-approve";
  this.memberError = null;
  try {
    await axios.post(`/api/users/${member.id}/approve/`);
    this.pendingMembers = this.pendingMembers.filter((m) => m.id !== member.id);
    this.memberSuccess = `${member.first_name} ${member.last_name} approved.`;
    await this.fetchApprovedMembers();
  } catch {
    this.memberError = "Failed to approve member.";
  } finally {
    this.memberActionLoading = null;
  }
},
async denyMember(member) {
  this.memberActionLoading = member.id + "-deny";
  this.memberError = null;
  try {
    await axios.post(`/api/users/${member.id}/deny/`);
    this.pendingMembers = this.pendingMembers.filter((m) => m.id !== member.id);
    this.memberSuccess = `${member.first_name} ${member.last_name} denied.`;
  } catch {
    this.memberError = "Failed to deny member.";
  } finally {
    this.memberActionLoading = null;
  }
},
```

- [ ] **Step 2: Commit**

```bash
git add frontend/mcl_ui/src/components/Organization.vue
git commit -m "feat: add org admin members management tab to Organization page"
```

---

## Task 15: End-to-end smoke test and final verification

- [ ] **Step 1: Run full backend test suite**

```bash
cd backend && python manage.py test test_system.tests -v 2
```

Expected: All tests pass with `OK`.

- [ ] **Step 2: Run linting**

```bash
cd backend && black --check .
cd ../frontend/mcl_ui && npm run lint
```

Fix any issues before proceeding.

- [ ] **Step 3: Start services and test happy paths manually**

```bash
docker-compose up --build
```

Test these flows in order:

1. Go to `/register` → click "Create an Organization" → fill form → submit → confirm redirect to `/login?registered=org`
2. Log in as Django superuser → confirm redirect to `/platform-admin` → see pending org in table → click Approve
3. Log back in as org creator → confirm redirect to `/organizations/ov` with Members tab visible
4. Go to `/register` → click "Join an Organization" → select the approved org → submit → confirm redirect to `/login?registered=member`
5. Log in as the new member → confirm redirect to `/pending?type=member`
6. Log in as org admin → go to `/organizations/ov` → Members tab → approve the pending member
7. Member logs back in → confirm redirect to `/medias`

- [ ] **Step 4: Test security regression**

```bash
# Unauthenticated chat mutation — should return 401
curl -X PUT http://localhost:8000/api/chats/<any-chat-id>/ \
  -H "Content-Type: application/json" \
  -d '{"content": "hacked"}'
# Expected: {"detail":"Authentication credentials were not provided."}

# Login enumeration — both should return same message
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "fake@nobody.com", "password": "wrong"}'
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "real@user.com", "password": "wrongpass"}'
# Expected: both return {"error": "Invalid credentials."}
```

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "chore: final verification pass — onboarding flow complete"
```
