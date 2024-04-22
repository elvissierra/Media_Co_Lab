from test_system.apps.organizations.models import Organization
from test_system.apis.organizations.serializers import OrganizationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from test_system.permissions import OrganizationPermission

class OrganizationsGetView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        organization = Organization.objects.filter(id = request.user.organization.id)
        serializer = OrganizationSerializer(organization, many=True)
        return Response(serializer.data)
    
class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationGetUpdateDeleteView(APIView):
    permission_classes= [OrganizationPermission]

    def get_object(self, organization_id):
        try:
            return Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Http404

    def get(self, request, organization_id, format=None):
        organization = self.get_object(organization_id)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request, organization_id, format=None):
        organization = self.get_object(organization_id)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, organization_id):
        organization = self.get_object(organization_id)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
