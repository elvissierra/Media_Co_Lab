from test_system.apps.medias.models import Medias
from test_system.apis.medias.serializers import MediasSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class MediasGetCreateView(APIView):
    def get (self, request, format=None):
        medias = Medias.get_object.all(request)
        serializer = MediasSerializer(medias, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = MediasSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class MediasGetUpdateDeleteView(APIView):
    def get_object(self, medias_id):
        try:
            return Medias.objects.get(id=medias_id)
        except Medias.DoesNotExist:
            return Http404
    
    def get(self, request, medias_id):
        medias = self.get_object(medias_id)
        serializer = MediasSerializer(medias)
        return Response(serializer.data)

    def update(self, request, medias_id):
        medias = self.get_object(medias_id)
        serializer = MediasSerializer(medias, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, medias_id):
        medias = Medias.get_object(medias_id)
        medias.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

