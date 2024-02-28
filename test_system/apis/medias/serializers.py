from rest_framework import serializers
from test_system.apps.medias.models import Medias

class MediasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medias
        fields = "__all__"