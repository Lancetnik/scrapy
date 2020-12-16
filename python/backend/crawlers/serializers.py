from rest_framework import serializers

from .models import HabrModel
from .spiders.core.ConstructorData import Scrapers


class HabrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabrModel
        fields = '__all__'


class RunnerSerializer(serializers.Serializer):
    spider_name = serializers.CharField(max_length=50)
    post_id = serializers.IntegerField(required=False)
    url = serializers.CharField(max_length=100)


fields = {i: serializers.CharField(max_length=20) for i in Scrapers.required_fields}
for j in Scrapers.fields:
    fields[j] = serializers.CharField(max_length=60, required=False)
ConstructSpiderSerialiser = type('ConstructSpiderSerialiser', (serializers.Serializer,), fields)
