from django.shortcuts import get_object_or_404
from test_system.apps.medias.models import Medias
from test_system.apis.medias.serializers import (
    MediasGetSerializer,
    MediaSerializer,
    MediaChatGetCreateSerializer,
)
from test_system.apis.chats.serializers import ChatsGetCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from test_system.permissions import IsMediaOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class UserMediasGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve user created Media objects"""
        user = request.user
        team = user.team
        if not team:
            return Response(
                {"error": "User is not associated with any team yet"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        medias = Medias.objects.filter(team_id=team.id)
        serializer = MediasGetSerializer(medias, many=True)
        return Response(serializer.data)


class MediaChatGetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, medias_id):
        """Retrieve media and associated Chat with pagination"""
        media = get_object_or_404(Medias, id=medias_id)
        media_chat = media.chats.all().order_by("created_at")
        serializer = MediaChatGetCreateSerializer(media, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, medias_id):
        """Create a chat obj under a specified media obj"""
        media = get_object_or_404(Medias, id=medias_id)
        serializer = ChatsGetCreateSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(media=media)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediasGetCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all Media objects"""
        medias = Medias.objects.all()
        serializer = MediasGetSerializer(medias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create Media associated to User Team obj"""
        user = request.user
        team_id = request.data.get("team_id")
        if not user.team.filter(id=team_id).exists():
            return Response(
                {"error": "User not associated with this team."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MediaSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediasGetUpdateDeleteView(APIView):
    permission_classes = [IsMediaOwner]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, medias_id):
        media = get_object_or_404(Medias, id=medias_id)
        return Response(MediaSerializer(media, context={"request": request}).data)

    def update(self, request, medias_id):
        medias = get_object_or_404(Medias, id=medias_id)
        serializer = MediaSerializer(medias, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, medias_id):
        medias = get_object_or_404(Medias, id=medias_id)
        medias.delete()
        return Response(MediaSerializer(medias).data)
