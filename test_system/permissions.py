from rest_framework.permissions import BasePermission
from datetime import datetime

class OrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        org_id = request.parser_context.get("kwargs", {}).get("organization_id")
        return request.user.user.organization.id == org_id
    
class TeamPermission(BasePermission):
    def has_permission(self, request, view):
        team_id = request.parser_context.get("kwargs", {}).get("team_id")
        return request.user.user.team.id == team_id
    
class ObjectPermission(BasePermission):
    def is_owner(self, request, view):
        user_id = request.parser_context.get("kwargs", {}).get("user_id")
        return request.user.user.id == user_id
    