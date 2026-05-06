from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.permissions import IsPlatformAdmin, IsOrgAdmin


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
