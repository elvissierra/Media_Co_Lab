from rest_framework import serializers
from test_system.apps.organizations.models import Organization
from test_system.apis.teams.serializers import TeamsSerializer

class DemoOrgSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = "__all__"

class OrganizationSerializer(serializers.ModelSerializer):
    """ Organization Overview """
    teams = TeamsSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["title", "teams"]

class OrganizationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["title", "id"]