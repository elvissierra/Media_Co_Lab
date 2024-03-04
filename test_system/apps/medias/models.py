from django.db import models
from test_system.apps.users.models import User
import uuid


class Medias(models.Model):
    title = models.CharField(max_length=255)
    id = models.UUIDField(default= uuid.uuid4, primary_key=True)
    content = models.FileField(upload_to="static_files/media/")
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="medias", on_delete=models.CASCADE)
