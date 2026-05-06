from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status


def check_org_membership_approved(request):
    """Returns a 403 Response if user's org_status is not approved, else None."""
    if not hasattr(request.user, "org_status"):
        return None
    if request.user.org_status != "approved":
        return Response(
            {"detail": "Your membership is pending approval."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None


class OrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        org_id = view.kwargs.get("organization_id")
        return (
            hasattr(request.user, "organization")
            and request.user.organization.id == org_id
        )


class TeamPermission(BasePermission):
    """manytomany check if team obj is among the users teams"""

    def has_permission(self, request, view):
        team_id = view.kwargs.get("team_id")
        return request.user.team.filter(id=team_id).exists()


class IsLabelOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMediaOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")
        return request.user.id == user_id


class IsPlatformAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user is not None
            and request.user.is_staff
        )


class IsOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user is not None
            and request.user.is_authenticated
            and request.user.is_org_admin
            and request.user.organization is not None
        )
