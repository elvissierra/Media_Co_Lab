from django.db import models
from test_system.apps.users.models import CustomUser
from test_system.apps.teams.models import Team
from test_system.apps.comments.models import Comment
import uuid


class Medias(models.Model):
    title = models.CharField(max_length=255)
    id = models.UUIDField(default= uuid.uuid4, primary_key=True)
    content = models.FileField(upload_to="media/", null=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, related_name="medias", on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, related_name="medias", on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, related_name="medias", on_delete=models.CASCADE)
