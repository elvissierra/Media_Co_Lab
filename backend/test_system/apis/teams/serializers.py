from rest_framework import serializers
from test_system.apps.teams.models import Team
from test_system.apis.users.serializers import UsersGetSerializer

class TeamSerializer(serializers.ModelSerializer):
    users = UsersGetSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"