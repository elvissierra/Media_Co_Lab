from rest_framework import serializers
from test_system import settings
from test_system.apps.users.models import CustomUser
from test_system.apps.organizations.models import Organization
from test_system.apps.teams.models import Team


class UserRegistrationSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True
    )
    registration_type = serializers.ChoiceField(
        choices=["join", "create_org"], write_only=True, default="join"
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "id",
            "team",
            "organization_id",
            "email",
            "password",
            "registration_type",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_organization_id(self, value):
        request = self.context.get("request")
        if value is None:
            if request and request.user.is_superuser:
                return value
            raise serializers.ValidationError("Organization is required.")
        try:
            org = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization not found.")
        if not org.is_approved:
            raise serializers.ValidationError("Organization is not approved.")
        return value

    def create(self, validated_data):
        organization_id = validated_data.pop("organization_id", None)
        registration_type = validated_data.pop("registration_type", "join")
        organization = None
        if organization_id:
            organization = Organization.objects.get(id=organization_id)

        is_org_admin = registration_type == "create_org"
        org_status = "approved" if is_org_admin else "pending"

        user = CustomUser.objects.create_user(
            organization=organization,
            **validated_data,
        )
        user.is_org_admin = is_org_admin
        user.org_status = org_status
        user.save()
        return user


class UsersGetSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "team",
            "organization",
            "labels",
            "avatar",
            "is_org_admin",
            "org_status",
            "is_staff",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.avatar and hasattr(instance.avatar, "url"):
            avatar_url = instance.avatar.url
            if request:
                avatar_url = request.build_absolute_uri(avatar_url)
            data["avatar"] = avatar_url
        else:
            data["avatar"] = f"{settings.MEDIA_URL}default.jpg"

        # Allow org admins to see email; restrict for regular users
        if request and not request.user.is_superuser:
            is_org_admin = getattr(request.user, "is_org_admin", False)
            if not is_org_admin:
                sensitive_fields = ["password", "is_superuser", "is_staff", "email"]
            else:
                sensitive_fields = ["password", "is_superuser", "is_staff"]
            for field in sensitive_fields:
                data.pop(field, None)

        return data


class UserSerializer(serializers.ModelSerializer):
    """Organization Overview"""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id", "avatar"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.avatar and hasattr(instance.avatar, "url"):
            avatar_url = instance.avatar.url
            if request:
                avatar_url = request.build_absolute_uri(avatar_url)
            data["avatar"] = avatar_url
        else:
            data["avatar"] = f"{settings.MEDIA_URL}default.jpg"
        return data
