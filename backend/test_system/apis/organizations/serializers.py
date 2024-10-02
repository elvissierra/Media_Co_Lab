from rest_framework import serializers
from test_system.apps.organizations.models import Organization
from test_system.apis.teams.serializers import TeamsSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    teams = TeamsSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["title", "teams"]

class OrganizationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["title"]