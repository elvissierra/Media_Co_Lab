from test_system.apps.labels.models import Label
from test_system.apis.labels.serializers import LabelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from test_system.permissions import IsLabelOwner, TeamPermission

class LabelsGetCreateView(APIView):
    permission_classes=[TeamPermission]

    def get(self, request, format=None):
        label = Label.objects.all()
        serializer = LabelSerializer(label, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelGetUpdateDeleteView(APIView):
    permission_classes=[IsLabelOwner]
    
    def get_object(self, label_id):
        try:
            return Label.objects.get(id=label_id)
        except Label.DoesNotExist:
            return Http404

    def get(self, request, label_id, format=None):
        label = self.get_object(label_id)
        serializer = LabelSerializer(label)
        return Response(serializer.data)

    def put(self, request, label_id, format=None):
        label = self.get_object(label_id)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, label_id):
        label = self.get_object(label_id)
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
