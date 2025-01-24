from django.shortcuts import get_object_or_404
from .serializers import CommentsGetCreateSerializer, CommentGetUpdateDeleteSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from test_system.apps.comments.models import Comment


class CommentsGetView(APIView):

    def get(self, request, format=None):
        """ get all comments """
        user = request.user
        user_organization = user.organization
        if not user_organization:
            return Response({"error": "User not associated with an organization."}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(organization_id=user_organization.id)
        serializer = CommentsGetCreateSerializer(comments, many=True)
        return Response(serializer.data)
    
class CommentGetUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        return Response(CommentGetUpdateDeleteSerializer(comment, context={"request": request}).data)

    def put(self, request, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentGetUpdateDeleteSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return Response(CommentGetUpdateDeleteSerializer(comment).data)