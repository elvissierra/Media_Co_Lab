from rest_framework.permissions import BasePermission
from datetime import datetime

#allowed to create

#allowed to label

#allowed to delete/remove

class OrganizationPermission(BasePermission):
    #check organization
    def has_permission(self, request, view):
        org_id = request.parser_context.get("kwargs", {}).get("organization_id")
        return request.user.user.organization.id == org_id
    
class TeamPermission(BasePermission):
    #check team and allowance
    def has_permission(self, request, view):
        team_id = request.parser_context.get("kwargs", {}).get("team_id")
        return request.user.user.team.id == team_id
    
class CollaborationAllowance(BasePermission):

    def has_permission(self, request, view):
        #allowance for collaboration
        #so if meeting say an hr then allowance can be given of an hr