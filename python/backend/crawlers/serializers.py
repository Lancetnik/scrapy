from rest_framework import serializers

from .models import HabrModel


class HabrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabrModel
        fields = '__all__'


class RunnerSerializer(serializers.Serializer):
    spider_name = serializers.CharField(max_length=50)
    post_id = serializers.IntegerField(required=False)