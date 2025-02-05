from test_system.apps.chats.models import Chat
from rest_framework import serializers


class ChatsGetCreateSerializer(serializers.ModelSerializer):
        class Meta:
                model = Chat
                fields = ["id", "content", "owner", "media", "created_at", "updated_at"]
                read_only_fields = ["owner", "media", "created_at", "updated_at"]

        def create(self, validated_data):
            user = self.context["request"].user
            chat = Chat.objects.create(owner=user, **validated_data)
            return chat

class ChatGetUpdateDeleteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Chat
                fields = ["content"]