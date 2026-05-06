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
