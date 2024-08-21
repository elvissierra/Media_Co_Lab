from rest_framework import serializers
from test_system.apps.medias.models import Medias

class MediasSerializer(serializers.ModelSerializer):
    uploaded_media = serializers.FileField(write_only=True)

    class Meta:
        model = Medias
        fields = "__all__"
        read_only_fields = ["size", "content", "user"]

    def create(self, validated_data):
        media_data = validated_data.pop("uploaded_media")
        user = self.context["request"].user
        medias_obj = Medias(**validated_data)
        medias_obj.user = user
        medias_obj.content = media_data
        if hasattr(media_data, 'size'):
            medias_obj.size = media_data.size
        medias_obj.save()
        return medias_obj
    