from rest_framework import serializers

from .models import HabrModel


class HabrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabrModel
        fields = '__all__'