from django_filters import rest_framework as filters

from .models import PostModel


class PostFilter(filters.FilterSet):
    posted = filters.IsoDateTimeFromToRangeFilter()
    title = filters.CharFilter(lookup_expr='icontains')
    tags = filters.CharFilter(method='filter_tags')

    def filter_tags(self, queryset, name, value):
        tags_to_find = value.split(',')
        return queryset.filter(tags__overlap=tags_to_find)

    class Meta:
        model = PostModel
        fields = ['source', 'posted', 'title', 'tags']