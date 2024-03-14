from test_system.apps.users.models import CustomUser
from test_system.apis.users.serializers import UserSerializer, UserRegistrationSerializer, UsersGetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from test_system.permissions import ObjectPermission


class UsersGetCreateView(APIView):

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UsersGetSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetUpdateDeleteView(APIView):
    permission_classes=[ObjectPermission]

    def get_object(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserRegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
