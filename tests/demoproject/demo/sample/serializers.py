from rest_framework import serializers

from .models import DemoModel


class DemoModelSerializer(serializers.ModelSerializer):
    method = serializers.SerializerMethodField(label='Random Method')

    def get_method(self, obj):
        return 'Random'

    class Meta:
        model = DemoModel
        fields = "__all__"
