from rest_framework import serializers

from .models import DemoModel


class DemoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoModel
        fields = "__all__"
