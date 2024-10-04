from django.shortcuts import get_object_or_404
from test_system.apps.teams.models import Team
from test_system.apps.medias.models import Medias
from test_system.apis.teams.serializers import TeamsSerializer, TeamSerializer, TeamMediaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from test_system.permissions import TeamPermission
from rest_framework.permissions import IsAuthenticated

class TeamsGetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Retrieve all Team objects"""  
        user = request.user
        organization = user.organization
        if not organization:
            return Response({"error": "User not associated with an organization."}, status=status.HTTP_400_BAD_REQUEST)
        teams = Team.objects.filter(organization = request.user.organization)
        serializer = TeamsSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create and associate the obj with the user's organization"""
        user_organization = request.user.organization.id
        request.data["organization"] = user_organization
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

class TeamMediasGetView(APIView):
    def get(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        team_media = Medias.objects.filter(team_id=team.id)
        serializer = TeamMediaSerializer(team_media, many=True, context={'request': request})
        return Response(serializer.data)
