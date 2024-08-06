from django.shortcuts import get_object_or_404
from test_system.apps.medias.models import Medias
from test_system.apis.medias.serializers import MediasSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from test_system.permissions import IsMediaOwner
from rest_framework.permissions import IsAuthenticated

class MediasGetCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        medias = Medias.objects.filter(team_id=request.team.id)
        serializer = MediasSerializer(medias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MediasSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            medias_obj = serializer.save()
            return Response(MediasSerializer(medias_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MediasGetUpdateDeleteView(APIView):
    permission_classes = [IsMediaOwner]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, medias_id):
        media = get_object_or_404(Medias, id=medias_id)
        return Response(MediasSerializer(media, context={"request": request}).data)

    def update(self, request, medias_id):
        medias = get_object_or_404(Medias, id=medias_id)
        serializer = MediasSerializer(medias, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, medias_id):
        medias = get_object_or_404(Medias, id=medias_id)
        medias.delete()
        return Response(MediasSerializer(medias).data)
