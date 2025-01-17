import uuid
from django.db import models as db_models


class CommentsModelMixin:
    @property
    def comments_count(self) -> int:
        """
        The total number of comments
        """
        return self.comments.count()


class Comment(db_models.Model):
    id = db_models.UUIDField(default=uuid.uuid4, primary_key=True)
    parent_id = db_models.ForeignKey(
        "self", related_name="replies", on_delete=db_models.CASCADE, null=True, blank=True
    )
    owner = db_models.CharField(max_length=255, blank=False, null=False)
    content = db_models.TextField()
    created_at = db_models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = db_models.DateTimeField(auto_now_add=True, editable=False)
