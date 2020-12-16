from django_filters import rest_framework as filters

from .models import PostModel


class PostFilter(filters.FilterSet):
    class Meta:
        model = PostModel
        fields = ['title', 'link']