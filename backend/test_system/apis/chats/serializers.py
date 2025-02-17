from test_system.apps.chats.models import Chat
from rest_framework import serializers


class ChatsGetCreateSerializer(serializers.ModelSerializer):
        owner_full_name = serializers.SerializerMethodField()

        class Meta:
                model = Chat
                fields = ["id", "content", "owner_full_name", "created_at", "updated_at"]
                read_only_fields = ["owner", "media", "created_at", "updated_at"]

        def get_owner_full_name(self, obj):
               return f"{obj.owner.first_name} {obj.owner.last_name}"

        def create(self, validated_data):
            user = self.context["request"].user
            chat = Chat.objects.create(owner=user, **validated_data)
            return chat

class ChatGetUpdateDeleteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Chat
                fields = ["content"]