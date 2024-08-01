from rest_framework import serializers
from test_system.apps.medias.models import Medias

class MediasSerializer(serializers.ModelSerializer):
    uploaded_media = serializers.FileField(write_only=True)
    
    class Meta:
        model = Medias
        fields = "__all__"
        read_only_fields = ["size"]

    def create(self, validated_data):
        medias_data = validated_data.pop("uploaded_media")
        medias_obj = Medias(**validated_data)
        medias_obj.content = medias_data
        medias_obj.size = medias_data.size
        medias_obj.save()
        return medias_obj