from rest_framework import serializers
from test_system.apps.teams.models import Team
from test_system.apps.medias.models import Medias
from test_system.apis.users.serializers import UsersGetSerializer, UserSerializer
from django.conf import settings

class TeamMediaSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Medias
        fields = ["title", "content"]

    def get_content(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.content)
        return f'{settings.MEDIA_URL}{obj.content}'

class TeamSerializer(serializers.ModelSerializer):
    users = UsersGetSerializer(many=True, read_only=True)
    medias = TeamMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"

class TeamsSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    medias = TeamMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["title", "description", "users", "medias"]