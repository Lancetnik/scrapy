from rest_framework import serializers

from .spiders.core.ConstructorData import Scrapers


class RunnerSerializer(serializers.Serializer):
    spider_name = serializers.CharField(max_length=50)
    post_id = serializers.IntegerField(required=False)
    url = serializers.CharField(max_length=100, required=False)


fields = {i: serializers.CharField(max_length=20) for i in Scrapers.required_fields}
for j in Scrapers.fields:
    fields[j] = serializers.CharField(max_length=60, required=False)
ConstructSpiderSerialiser = type('ConstructSpiderSerialiser', (serializers.Serializer,), fields)
