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
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication
from test_system.permissions import IsUser, IsOrgAdmin


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


class PendingMembersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def get(self, request):
        org = request.user.organization
        pending = CustomUser.objects.filter(organization=org, org_status="pending")
        serializer = UsersGetSerializer(
            pending, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserApproveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def post(self, request, user_id):
        from test_system.apps.teams.models import Team

        target = get_object_or_404(
            CustomUser, id=user_id, organization=request.user.organization
        )
        target.org_status = "approved"
        target.save()
        # Auto-add to the org's first team so the user can access resources
        first_team = Team.objects.filter(organization=request.user.organization).first()
        if first_team:
            target.team.add(first_team)
        return Response({"detail": "User approved."}, status=status.HTTP_200_OK)


class UserDenyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOrgAdmin]

    def post(self, request, user_id):
        target = get_object_or_404(
            CustomUser, id=user_id, organization=request.user.organization
        )
        target.org_status = "denied"
        target.save()
        return Response({"detail": "User denied."}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsersGetSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
