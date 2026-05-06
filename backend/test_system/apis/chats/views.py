from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.auth import TokenAuthentication
from django.shortcuts import get_object_or_404

from test_system.apps.chats.models import Chat
from test_system.apis.chats.serializers import (
    ChatsGetCreateSerializer,
    ChatGetUpdateDeleteSerializer,
)


class ChatsGetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        user_organization = user.organization
        if not user_organization:
            return Response(
                {"error": "User is not associated with an organization."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        chats = Chat.objects.filter(owner__organization=user_organization)
        serializer = ChatsGetCreateSerializer(
            chats, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatGetUpdateDeleteView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        serializer = ChatGetUpdateDeleteSerializer(chat, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        if chat.owner != request.user:
            return Response(
                {"error": "You do not have permission to edit this chat."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ChatGetUpdateDeleteSerializer(
            chat, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        if chat.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this chat."},
                status=status.HTTP_403_FORBIDDEN,
            )
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
