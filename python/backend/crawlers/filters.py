from django_filters import rest_framework as filters

from .models import HabrModel


class HabrFilter(filters.FilterSet):
    class Meta:
        model = HabrModel
        fields = ['title', 'link']