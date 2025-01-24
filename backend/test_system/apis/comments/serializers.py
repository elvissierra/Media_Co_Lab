from test_system.apps.comments.models import Comment
from rest_framework import serializers


class CommentsGetCreateSerializer(serializers.ModelSerializer):
        class Meta:
                model = Comment
                fields = ["id", "content", "owner", "media", "created_at", "updated_at"]
                read_only_fields = ["owner", "media", "created_at", "updated_at"]

        def create(self, validated_data):
            user = self.context["request"].user
            comment = Comment.objects.create(owner=user, **validated_data)
            return comment

class CommentGetUpdateDeleteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Comment
                fields = ["content"]