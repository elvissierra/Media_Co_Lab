from django.shortcuts import get_object_or_404
from .serializers import CommentsGetOrCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from test_system.apps.comments.models import Comment

class CommentsGetOrCreateView(APIView):
    def get(self, request, format=None):
        user = request.user
        user_teams = user.team.all()
        if not user_teams:
            return Response({"error": "No team association."}, status=status.HTTP_400_BAD_REQUEST)
        team_labels = Comment.objects.filter(medias__team__in=user_teams)
        serializer = CommentsGetOrCreateSerializer(team_labels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentsGetOrCreateSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentGetUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, label_id, format=None):
        label = get_object_or_404(Comment, id=label_id)
        return Response(CommentsGetOrCreateSerializer(label, context={"request": request}).data)

    def put(self, request, label_id, format=None):
        label = get_object_or_404(Comment, id=label_id)
        serializer = CommentsGetOrCreateSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, label_id):
        label = get_object_or_404(Comment, id=label_id)
        label.delete()
        return Response(CommentsGetOrCreateSerializer(label).data)