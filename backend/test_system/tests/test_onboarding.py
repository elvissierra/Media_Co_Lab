from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory, APIClient
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.permissions import IsPlatformAdmin, IsOrgAdmin
from test_system.apis.users.serializers import UserRegistrationSerializer
from knox.models import AuthToken


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

        # Test that invalid choice is rejected
        user.org_status = "invalid"
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        # Verify the error message contains the org_status validation error
        self.assertIn("org_status", context.exception.error_dict)


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

    def test_anonymous_user_denied(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
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

    def test_anonymous_user_denied(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        self.assertFalse(IsOrgAdmin().has_permission(request, None))


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
        serializer = UserRegistrationSerializer(data=data, context={"request": request})
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
        serializer = UserRegistrationSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.org_status, "approved")
        self.assertTrue(user.is_org_admin)


class PlatformAdminOrgApprovalTest(TestCase):
    def setUp(self):
        from rest_framework.test import APIClient
        from knox.models import AuthToken

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
        response = self.client.post(f"/api/organizations/{self.pending_org.id}/deny/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Organization.objects.filter(id=self.pending_org.id).exists())

    def test_non_staff_cannot_approve_org(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.regular_token}")
        response = self.client.post(
            f"/api/organizations/{self.pending_org.id}/approve/"
        )
        self.assertEqual(response.status_code, 403)


class OrgAdminMemberApprovalTest(TestCase):
    def setUp(self):
        from rest_framework.test import APIClient
        from knox.models import AuthToken

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

        self.other_org = Organization.objects.create(
            title="Other Org", is_approved=True
        )
        self.other_admin = CustomUser.objects.create_user(
            email="otheradmin@test.com",
            password="testpass123",
            organization=self.other_org,
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
        response = self.client.post(f"/api/users/{self.pending_user.id}/approve/")
        self.assertEqual(response.status_code, 200)
        self.pending_user.refresh_from_db()
        self.assertEqual(self.pending_user.org_status, "approved")

    def test_org_admin_can_deny_member(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token}")
        response = self.client.post(f"/api/users/{self.pending_user.id}/deny/")
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
