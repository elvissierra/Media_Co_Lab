from django.conf import settings
from rest_framework import serializers
from test_system.apps.medias.models import Medias
from test_system.apis.labels.serializers import LabelsSerializer
from test_system.apis.teams.serializers import TeamsSerializer
from test_system.apis.chats.serializers import ChatsGetCreateSerializer


class MediaChatGetCreateSerializer(serializers.ModelSerializer):
    """ media obj and associated chats """
    chat_count = serializers.ReadOnlyField()
    chats = ChatsGetCreateSerializer(many=True, read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Medias
        fields = ["id", "title", "description", "content", "user", "team", "chats", "chat_count"]

    def get_content(self, obj):
        request = self.context.get("request")
        if request:
            return f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{obj.content}"
        return f"{settings.MEDIA_URL}{obj.content}"


class MediasSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True, read_only=True)
    team = TeamsSerializer(read_only=True)

    class Meta:
        model = Medias
        fields = "__all__"

class MediasGetSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True, read_only=True)
    team_title = serializers.CharField(source="team.title", read_only=True)

    class Meta:
        model = Medias
        fields = ["title", "description", "content", "labels", "user", "team_title", "id"]


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medias
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        medias_obj = Medias.objects.create(**validated_data)
        return medias_obj
    