import uuid
from django.db import models as models
from django.conf import settings

class ChatsModelMixin:
    @property
    def chats_count(self) -> int:
        """
        The total number of chats
        """
        return self.chats.count()


class Chat(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    parent_id = models.ForeignKey(
        "self", related_name="replies", on_delete=models.CASCADE, null=True, blank=True
    )
    media = models.ForeignKey("medias.Medias", related_name="chats", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)