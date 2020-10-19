from django_filters import rest_framework as filters

from .models import Habr


class PostsFilter(filters.FilterSet):
    """ Фильтрация постов для отображения """
    posted = filters.RangeFilter()

    class Meta:
        model = Habr
        fields = ['posted']