from test_system.apps.chats.models import Chat
from rest_framework import serializers
from test_system import settings


class ChatsGetCreateSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "content",
            "owner_full_name",
            "created_at",
            "updated_at",
            "avatar",
        ]
        read_only_fields = ["owner", "media", "created_at", "updated_at"]

    def get_owner_full_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def get_avatar(self, obj):
        request = self.context.get("request")
        try:
            avatar_url = obj.owner.avatar.url
        except Exception:
            avatar_url = f"{settings.MEDIA_URL}default.jpg"
        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url

    def create(self, validated_data):
        user = self.context["request"].user
        chat = Chat.objects.create(owner=user, **validated_data)
        return chat


class ChatGetUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["content"]
