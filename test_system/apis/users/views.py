from django.shortcuts import get_object_or_404
from test_system.apps.users.models import CustomUser
from test_system.apis.users.serializers import UserSerializer, UserRegistrationSerializer, UsersGetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser
from test_system.permissions import IsUser

#user login
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                _, token = AuthToken.objects.create(user)
                return Response({"token": token.key})
            else:
                return Response({"error": "Invalid credentials."}, status = status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "Invalid input."}, status=status.HTTP_401_UNAUTHORIZED)

#methods
class UserCreateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UsersGetView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UsersGetSerializer(users, many=True)
        return Response(serializer.data)

class UserGetUpdateDeleteView(APIView):
    permission_classes= [IsUser]

    def get(self, request, user_id, format=None):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UsersGetSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
