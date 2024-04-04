from rest_framework import serializers
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization

class UserRegistrationSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id", "team", "organization_id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_organization_id(self, value):
        try:
            organization = Organization.objects.get(id=value)
            if not organization.is_approved:
                raise serializers.ValidationError("Organization has yet to be approved.")
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization doesnt yet exist.")
        return value

    def create(self, validated_data):
        organization_id = validated_data.pop("organization_id")
        organization = Organization.objects.get(id=organization_id)
        user = CustomUser.objects.create_user(**validated_data, organization=organization)
        return user
    
class UsersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

        def to_representation(self, instance):
            data = super().to_representation(instance)
            request = self.context.get('request')
            if request and not request.user.is_superuser:
                sensitive_fields = ["password", "last_login", "is_superuser", "is_staff", "is_active", "date_joined", "email", "groups"]
                for field in sensitive_fields:
                    data.pop(field, None)
            return data                                                

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"