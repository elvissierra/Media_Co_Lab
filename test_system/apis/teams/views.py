from django.shortcuts import get_object_or_404
from test_system.apps.teams.models import Team
from test_system.apis.teams.serializers import TeamSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from test_system.permissions import TeamPermission


class TeamsGetCreateView(APIView):
    
    def get(self, request, format=None): 
        teams = Team.objects.filter(organization_id = request.user.organization.id)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamGetUpdateDeleteView(APIView):
    permission_classes= [TeamPermission]

    def get(self, request, team_id, format=None):
        team = get_object_or_404(Team, id=team_id)
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def put(self, request, team_id, format=None):
        team = self.get_object(team_id)
        self.check_object_permissions(request, team)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, team_id):
        team = self.get_object(team_id)
        self.check_object_permissions(request, team)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
