from rest_framework import serializers

from .models import Habr


class HabrAnnotateSerializer(serializers.ModelSerializer):
    """ Краткое представление поста с habr """
    annotation = serializers.SerializerMethodField('annotate')

    def annotate(self, obj):
        with open(f"../crawlers/posts/habr/{obj.id}.txt", 'r', encoding="utf8") as file:
            return file.read()[:300]+"..."

    class Meta:
        model = Habr
        fields = ("id", "link", "title", "posted", "annotation")


class HabrDetailSerializer(serializers.ModelSerializer):
    """ Полное представление поста с habr """
    text = serializers.SerializerMethodField('read')

    def read(self, obj):
        with open(f"../crawlers/posts/habr/{obj.id}.txt", 'r', encoding="utf8") as file:
            return file.read()

    class Meta:
        model = Habr
        fields = "__all__"