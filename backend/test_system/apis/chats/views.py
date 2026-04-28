from django.shortcuts import get_object_or_404
from .serializers import ChatsGetCreateSerializer, ChatGetUpdateDeleteSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from test_system.apps.chats.models import Chat


class ChatsGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """get all Chats"""
        user = request.user
        user_organization = user.organization
        if not user_organization:
            return Response(
                {"error": "User not associated with an organization."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Chats = Chat.objects.filter(owner__organization=user_organization)
        serializer = ChatsGetCreateSerializer(Chats, many=True)
        return Response(serializer.data)


class ChatGetUpdateDeleteView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        return Response(
            ChatGetUpdateDeleteSerializer(chat, context={"request": request}).data
        )

    def put(self, request, chat_id, format=None):
        chat = get_object_or_404(Chat, id=chat_id)
        serializer = ChatGetUpdateDeleteSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
