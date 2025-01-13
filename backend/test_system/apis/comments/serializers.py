from test_system.apps.comments.models import Comment
from rest_framework import serializers

class CommentsGetOrCreateSerializer(serializers.ModelSerializer):

        class Meta:
                model = Comment
                fields = "parent_id, owner, content, created_at, updated_at"