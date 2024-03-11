from rest_framework import serializers
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization

class UserRegisterSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ["name", "id", "team", "organization_id",]

    def validate_org_id(self, value):
        try:
            organization = Organization.objects.get(id=value)
            if not organization.is_approved:
                    return serializers.ValidationError("Organization yet to be approved.")
        except Organization.DoesNotExist:
            return serializers.ValidationError("Invalid organization.")
        return value
    
    def create(self, validated_data):
        organization_id = validated_data.pop('organization_id')
        organization = Organization.objects.get(id=organization_id)
        user = CustomUser.objects.create_user(**validated_data, organization=organization)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"