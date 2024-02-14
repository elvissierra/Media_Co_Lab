from django.db import models
import uuid


class Organization(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)
