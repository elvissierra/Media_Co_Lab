from test_system.apps.teams.models import Team
from test_system.apis.teams.serializers import TeamSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TeamsGetCreateView(APIView):

    def get(self, request, format=None):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamGetUpdateDeleteView(APIView):
    def get_object(self, team_id):
        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Http404

    def get(self, request, team_id, format=None):
        team = self.get_object(team_id)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def put(self, request, team_id, format=None):
        team = self.get_object(team_id)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, team_id):
        team = self.get_object(team_id)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
