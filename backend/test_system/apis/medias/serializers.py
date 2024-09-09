from rest_framework import serializers
from test_system.apps.medias.models import Medias
from test_system.apis.teams.serializers import  TeamSerializer

class MediasSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Medias
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        medias_obj = Medias(**validated_data)
        medias_obj.user = user
        medias_obj.save()
        return medias_obj
    