from django.db import models
import uuid

class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from test_system.apps.teams.models import Team

        is_demo_org = self.is_demo
        super().save(*args, **kwargs)

        if is_demo_org:
            Team.objects.create(
                title = "Demo Team",
                description = "This is a demo team for demonstration purposes.",
                organization=self,
            )