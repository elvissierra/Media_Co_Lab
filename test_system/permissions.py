from rest_framework.permissions import BasePermission


class OrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        org_id = request.parser_context.get("kwargs", {}).get("organization_id")
        return request.user.organization.id == org_id
    
class TeamPermission(BasePermission):
    def has_permission(self, request, view):
        team_id = request.parser_context.get("kwargs", {}).get("team_id")
        return request.user.team.id == team_id
    
class IsLabelOwner(BasePermission):
    def is_owner(self, request, view):
        user_id = request.parser_context.get("kwargs", {}).get("user_id")
        return request.user.id == user_id
    
class IsMediaOwner(BasePermission):
    def is_owner(self, request, view):
        user_id = request.parser_context.get("kwargs", {}).get("user_id")
        return request.user.id == user_id

class IsUser(BasePermission):
    def is_owner(self, request, view):
        user_id = request.parser_context.get("kwargs", {}).get("user_id")
        return request.user.id == user_id