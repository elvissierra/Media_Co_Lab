from django.db import models
from test_system.apps.teams.models import Team
from test_system.apps.organizations.models import Organization
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, organization=None, **extra_fields):
        if not email:
            raise ValueError("The email must be provided.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        if organization is not None:
            user.organization = organization
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff must be set.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be set.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    team = models.ManyToManyField(Team, related_name="users", blank=True)
    organization = models.ForeignKey(
        Organization,
        related_name="users",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
    )
    email = models.EmailField(unique=True)
    avatar = models.FileField(upload_to="profile/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
