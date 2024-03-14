from rest_framework import serializers
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization

class UserRegistrationSerializer(serializers.BaseSerializer):
    organization_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["name", "id", "team", "organization_id"]

    def validate_org_id(self, value):
        try:
            organization = Organization.objects.get(id=value)
            if not organization.is_approved:
                raise serializers.ValidationError("Organization has yet to be approved.")
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization doesnt yet exist.")
        return value

    def create_user(self, validated_data):
        organization_id = validated_data.pop("organization_id")
        organization = Organization.objects.get(id=organization_id)
        user = CustomUser.objects.create_user(**validated_data, organization=organization)
        return user
    
class UsersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

        def to_representation(self, instance):
            rm_data = super().to_representation(instance)
            if not self.context("request").user.is_superuser:
                sensitive_fields = ["password", "last_login", "is_superuser", "is_staff", "is_active", "date_joined", "email", "groups"]
                for field in sensitive_fields:
                    rm_data.pop(field, None)
            return rm_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"