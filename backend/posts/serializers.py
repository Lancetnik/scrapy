from rest_framework import serializers

from bs4 import BeautifulSoup as BS

from .models import PostModel
from .annotation import summarize


class PostAnnotateSerializer(serializers.ModelSerializer):
    """ Краткое представление поста """
    annotation = serializers.SerializerMethodField('annotate')

    def annotate(self, obj):
        text = BS(obj.text, features="lxml").text
        try:
            data = summarize(text, 5)
        except ValueError:
            data = text[:300]+'...'
        if data == '.': data = text[:300]+'...'
        return data

    class Meta:
        model = PostModel
        fields = ("id", "link", "source", "title", "posted", "annotation")


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'
