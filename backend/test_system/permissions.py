from rest_framework.permissions import BasePermission


class OrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        org_id = view.kwargs.get("organization_id")
        return hasattr(request.user, 'organization') and request.user.organization.id == org_id

class TeamPermission(BasePermission):
    """ manytomany check if team obj is among the users teams """
    def has_permission(self, request, view):
        team_id = view.kwargs.get("team_id")
        return request.user.team.filter(id=team_id).exists()

class IsLabelOwner(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")
        return request.user.id == user_id

class IsMediaOwner(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")
        return request.user.id == user_id

class IsUser(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")
        return request.user.id == user_id