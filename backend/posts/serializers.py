from rest_framework import serializers

from .models import PostModel
from .annotation import summarize


class PostAnnotateSerializer(serializers.ModelSerializer):
    """ Краткое представление поста """
    annotation = serializers.SerializerMethodField('annotate')

    def annotate(self, obj):
        return summarize(obj.text, 5)

    class Meta:
        model = PostModel
        fields = ("id", "link", "source", "title", "posted", "annotation")


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'
