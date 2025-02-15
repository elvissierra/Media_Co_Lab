from django.shortcuts import get_object_or_404
from .serializers import ChatsGetCreateSerializer, ChatGetUpdateDeleteSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from test_system.apps.chats.models import Chat


class ChatsGetView(APIView):

    def get(self, request, format=None):
        """ get all Chats """
        user = request.user
        user_organization = user.organization
        if not user_organization:
            return Response({"error": "User not associated with an organization."}, status=status.HTTP_400_BAD_REQUEST)
        Chats = Chat.objects.filter(owner__organization=user_organization)
        serializer = ChatsGetCreateSerializer(Chats, many=True)
        return Response(serializer.data)
    
class ChatGetUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, Chat_id, format=None):
        Chat = get_object_or_404(Chat, id=Chat_id)
        return Response(ChatGetUpdateDeleteSerializer(Chat, context={"request": request}).data)

    def put(self, request, Chat_id, format=None):
        Chat = get_object_or_404(Chat, id=Chat_id)
        serializer = ChatGetUpdateDeleteSerializer(Chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, Chat_id):
        Chat = get_object_or_404(Chat, id=Chat_id)
        Chat.delete()
        return Response(ChatGetUpdateDeleteSerializer(Chat).data)