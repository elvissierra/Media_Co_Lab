from rest_framework import serializers
from test_system.apps.organizations.models import Organization
from test_system.apis.teams.serializers import TeamsSerializer


class DemoOrgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    """Organization Overview"""

    teams = TeamsSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["title", "teams"]


class OrganizationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["title", "id"]


class PendingOrganizationSerializer(serializers.ModelSerializer):
    creator_email = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["id", "title", "creator_email", "created_at"]

    def get_creator_email(self, obj):
        creator = obj.users.filter(is_org_admin=True).first()
        return creator.email if creator else None

    def get_created_at(self, obj):
        creator = obj.users.filter(is_org_admin=True).first()
        return creator.date_joined.isoformat() if creator else None
