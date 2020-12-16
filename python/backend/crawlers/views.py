from multiprocessing import Process

from loguru import logger

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from twisted.internet.error import ReactorAlreadyRunning
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .models import PostModel
from .filters import PostFilter
from .spiders.core.ConstructorData import Scrapers
from .spiders.core.services import extract_domain
from .serializers import PostSerializer, RunnerSerializer, ConstructSpiderSerialiser


process = CrawlerProcess(get_project_settings())


class HabrListView(generics.ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    

class HabrRetrieveView(generics.RetrieveAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer


class StartCrawlerView(APIView):
    serializer_class = RunnerSerializer

    def post(self, request):
        name = request.data['spider_name']
        try:
            if 'query' in name:
                post_id = request.data.get('post_id')
                if post_id:
                    urls = [PostModel.objects.get(pk=post_id).link]
                else:
                    urls = [i.link for i in PostModel.objects.filter(datetime__len__lt = 10)]
                process.crawl(
                    name,
                    start_urls=urls
                )

            elif name == 'explorer':
                urls = [request.data.get('url')]
                if not urls[0]:
                    return Response({'Error': 'Url field is required'}, status=status.HTTP_400_BAD_REQUEST)
                process.crawl(
                    name,
                    start_urls=urls,
                    allowed_domains=[extract_domain(urls[0])]
                )
                
            else:
                process.crawl(name)
                
            p = Process(target=process.start(stop_after_crawl=False))
            p.start()
        except ReactorAlreadyRunning: pass
        except PostModel.DoesNotExist: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_200_OK)


class ConstructSpiderView(APIView):
    serializer_class = ConstructSpiderSerialiser

    def post(self, request):
        try:
            params = {i: j for i, j in request.data.items()}
            params.pop('csrfmiddlewaretoken')
            Scrapers.construct(**params)
            Scrapers.save()
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)