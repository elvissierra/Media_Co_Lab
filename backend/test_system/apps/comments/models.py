import uuid
from django.db import models as models

class CommentsModelMixin:
    @property
    def comments_count(self) -> int:
        """
        The total number of comments
        """
        return self.comments.count()


class Comment(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    parent_id = models.ForeignKey(
        "self", related_name="replies", on_delete=models.CASCADE, null=True, blank=True
    )
    media = models.ForeignKey("medias.Medias", related_name = "comments", on_delete=models.CASCADE)
    owner = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)