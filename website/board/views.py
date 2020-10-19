from loguru import logger

from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Habr
from .serializers import HabrAnnotateSerializer, HabrDetailSerializer
from .services import PostsFilter


class PostsListView(generics.ListAPIView):
    """ Выдача списка кратких постов для составления ленты """
    serializer_class = HabrAnnotateSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = PostsFilter
    
    def get_queryset(self):
        queryser = Habr.objects.all()
        return queryser


class PostDetailView(generics.RetrieveAPIView):
    """ Выдача страницы с полным содержимым поста """
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, source, pk):
        post = Habr.objects.get(id=pk)
        serializer = HabrDetailSerializer(post)

        return Response({'data': serializer.data}, template_name='board/post.html')


def main_render(request):
    return render(request, 'board/main.html')