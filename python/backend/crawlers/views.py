from multiprocessing import Process

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from twisted.internet.error import ReactorAlreadyRunning
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .models import HabrModel
from .serializers import HabrSerializer
from .filters import HabrFilter

from loguru import logger


process = CrawlerProcess(get_project_settings())

class HabrListView(generics.ListAPIView):
    queryset = HabrModel.objects.all()
    serializer_class = HabrSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HabrFilter


class HabrRetrieveView(generics.RetrieveAPIView):
    queryset = HabrModel.objects.all()
    serializer_class = HabrSerializer


class StartCrawlerView(APIView):
    def post(self, request):
        name = request.data['spider_name']
        name = 'habr' # test
        try:
            process.crawl(name)
            p = Process(target=process.start(stop_after_crawl=False))
            p.start()
        except ReactorAlreadyRunning: pass
        return Response(status=status.HTTP_200_OK)