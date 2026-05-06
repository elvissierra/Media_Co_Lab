from django.shortcuts import get_object_or_404
from test_system.apps.users.models import CustomUser
from test_system.apis.users.serializers import (
    UserRegistrationSerializer,
    UsersGetSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.permissions import AllowAny, IsAdminUser
from test_system.permissions import IsUser


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """Create a new user"""
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return super().post(request, format=None)


class UsersGetView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UsersGetSerializer(users, many=True)
        return Response(serializer.data)


class UserGetPatchDeleteView(APIView):
    permission_classes = [IsUser]

    def get(self, request, user_id, format=None):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UsersGetSerializer(user)
        return Response(serializer.data)

    def patch(self, request, user_id, format=None):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UsersGetSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
