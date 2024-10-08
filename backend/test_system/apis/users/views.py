from django.shortcuts import get_object_or_404
from test_system.apps.users.models import CustomUser
from test_system.apis.users.serializers import UserRegistrationSerializer, UsersGetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser
from test_system.permissions import IsUser
from test_system.apps.organizations.models import Organization


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """Create a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            organization_id = request.data.get("organization")
            if organization_id:
                organization = Organization.objects.get(id=organization_id)
                user.organization = organization
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                return Response({"token": token})
            else:
                return Response({"error": "Invalid credentials."}, status = status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "Invalid input."}, status=status.HTTP_401_UNAUTHORIZED)


#methods    
class UsersGetView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UsersGetSerializer(users, many=True)
        return Response(serializer.data)

class UserGetPatchDeleteView(APIView):
    permission_classes= [IsUser]

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
