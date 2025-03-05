from django.shortcuts import get_object_or_404
from test_system.apps.organizations.models import Organization
from test_system.apis.organizations.serializers import (
    OrganizationSerializer,
    OrganizationGetSerializer,
    DemoOrgSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from test_system.permissions import OrganizationPermission
from rest_framework.permissions import AllowAny


class UserOrganizationView(APIView):
    permission_classes = [IsAuthenticated]
    """ User associated organization overview """

    def get(self, request):
        organization = request.user.organization
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)


class OrganizationCreateView(APIView):
    permission_classes = [AllowAny]
    """ Create organization """

    def post(self, request, format=None):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DemoOrgCreateView(APIView):
    permission_classes = [AllowAny]
    """ Creates a demo organization """

    def post(self, request):
        title = request.data.get("title", "").strip()
        if not title.endswith("demo"):
            title += " demo"

        demo_organization = Organization.objects.create(title=title, is_demo=True)
        serializer = DemoOrgSerializer(demo_organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationsGetView(APIView):
    permission_classes = [AllowAny]
    """ Get request for approved organizations on user signup"""

    def get(self, request):
        approved_orgs = Organization.objects.filter(is_approved=True)
        serializer = OrganizationGetSerializer(approved_orgs, many=True)
        return Response(serializer.data)


class OrganizationGetUpdateDeleteView(APIView):
    permission_classes = [OrganizationPermission]

    def get(self, request, organization_id, format=None):
        organization = get_object_or_404(Organization, id=organization_id)
        self.check_object_permissions(request, organization)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request, organization_id, format=None):
        organization = get_object_or_404(Organization, id=organization_id)
        self.check_object_permissions(request, organization)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, organization_id):
        organization = get_object_or_404(Organization, id=organization_id)
        self.check_object_permissions(request, organization)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
