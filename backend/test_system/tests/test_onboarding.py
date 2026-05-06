from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.permissions import IsPlatformAdmin, IsOrgAdmin
from test_system.apis.users.serializers import UserRegistrationSerializer


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
