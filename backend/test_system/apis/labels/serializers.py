from rest_framework import serializers
from test_system.apps.labels.models import Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        label = Label.objects.create(user=user, **validated_data)
        return label
