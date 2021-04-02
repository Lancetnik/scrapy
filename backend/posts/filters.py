from django_filters import rest_framework as filters
from django.db.models import Func

from .models import PostModel

from loguru import logger


# class ArrayCROSSING(Func):
#     function = 'CROSSING'

#     template = '%(function)s(%(expressions)s AS %(db_type)s)'
#     SELECT ARRAY(SELECT %(expressions)s INTERSECT SELECT %(expressions)s)

#     def __init__(self, expression, output_field):
#         super().__init__(expression, output_field=output_field)
    
#     def as_postgresql(self, compiler, connection, **extra_context):
#         return self.as_sql(compiler, connection, template=self.template, **extra_context)


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