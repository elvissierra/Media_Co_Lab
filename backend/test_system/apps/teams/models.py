from django.db import models
from test_system.apps.organizations.models import Organization
import uuid


# Create your models here.
class Team(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    organization = models.ForeignKey(
        Organization, related_name="teams", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title