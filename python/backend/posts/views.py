from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from .models import PostModel
from .filters import PostFilter
from .serializers import PostSerializer


class PostListView(generics.ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    

class PostRetrieveView(generics.RetrieveAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
