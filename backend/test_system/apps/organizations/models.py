from django.db import models
import uuid

class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
