from rest_framework import serializers
from test_system import settings
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.apps.teams.models import Team

class UserRegistrationSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id", "team", "organization_id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_organization_id(self, value):
        request = self.context.get("request")
        if value is None:
            if request and request.user.is_superuser:
                return value
            else:
                raise serializers.ValidationError("Organization is required for non-admin users.")
        try:
            organization = Organization.objects.get(id=value)
            if not organization.is_approved:
                raise serializers.ValidationError("Organization has yet to be approved.")
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization doesnt yet exist.")
        return value

    def create(self, validated_data):
        organization_id = validated_data.pop("organization_id", None)
        if organization_id:
            organization = Organization.objects.get(id=organization_id)
        else:
            organization = None
        user = CustomUser.objects.create_user(organization=organization, **validated_data)
        return user
    
class UsersGetSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "team", "organization", "labels", "avatar"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if instance.avatar and hasattr(instance.avatar, 'url'):
            avatar_url = instance.avatar.url
            if request:
                avatar_url = request.build_absolute_uri(avatar_url)
            data['avatar'] = avatar_url
        else:
            data['avatar'] = f"{settings.MEDIA_URL}default.jpg"

        if request and not request.user.is_superuser:
            sensitive_fields = ["password", "is_superuser", "is_staff", "email"]
            for field in sensitive_fields:
                data.pop(field, None)

        return data

class UserSerializer(serializers.ModelSerializer):
    """ Organization Overview """
    class Meta:
        model = CustomUser
        fields = ["first_name", "id", "avatar"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if instance.avatar and hasattr(instance.avatar, 'url'):
            avatar_url = instance.avatar.url
            if request:
                avatar_url = request.build_absolute_uri(avatar_url)
            data['avatar'] = avatar_url
        else:
            data['avatar'] = f"{settings.MEDIA_URL}default.jpg"
        return data
            