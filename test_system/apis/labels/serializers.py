from rest_framework import serializers
from test_system.apps.labels.models import Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
