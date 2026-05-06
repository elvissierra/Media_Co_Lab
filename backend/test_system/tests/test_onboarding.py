from django.test import TestCase
from django.core.exceptions import ValidationError
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

        # Test that invalid choice is rejected
        user.org_status = "invalid"
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        # Verify the error message contains the org_status validation error
        self.assertIn("org_status", context.exception.error_dict)
