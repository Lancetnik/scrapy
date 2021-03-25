from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PostModel
from .filters import PostFilter
from .serializers import PostDetailSerializer, PostAnnotateSerializer


class PostListView(generics.ListAPIView):
    queryset = PostModel.objects.order_by('-posted').all()
    serializer_class = PostAnnotateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    

class PostRetrieveView(generics.RetrieveAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostDetailSerializer


class GetTags(APIView):
    queryset = PostModel.objects.all()

    def get(self, request):
        tags = set()
        for i in self.queryset.all():
            if i.tags:
                tags |= set(i.tags)

        if not tags: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(tags, status=status.HTTP_200_OK)