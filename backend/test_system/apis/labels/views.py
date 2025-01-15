from django.shortcuts import get_object_or_404
from test_system.apps.labels.models import Label
from test_system.apis.labels.serializers import LabelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from test_system.permissions import IsLabelOwner

class LabelsGetCreateView(APIView):

    def get(self, request, format=None):
        """ retrieve all labels associated under a team object """
        user = request.user
        user_teams = user.team.all()
        if not user_teams:
            return Response({"error": "No team association."}, status=status.HTTP_400_BAD_REQUEST)
        team_labels = Label.objects.filter(medias__team__in=user_teams)
        serializer = LabelSerializer(team_labels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ create a label instance under a media object """
        serializer = LabelSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelGetUpdateDeleteView(APIView):
    permission_classes=[IsLabelOwner]
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, label_id, format=None):
        label = get_object_or_404(Label, id=label_id)
        return Response(LabelSerializer(label, context={"request": request}).data)

    def put(self, request, label_id, format=None):
        label = get_object_or_404(Label, id=label_id)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, label_id):
        label = get_object_or_404(Label, id=label_id)
        label.delete()
        return Response(LabelSerializer(label).data)
