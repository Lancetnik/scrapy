from loguru import logger
from django.shortcuts import render
from  django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def get_posts(request):
    response = [i.to_preview() for i in Habr.objects.all()]
    return JsonResponse(response, safe=False)

@csrf_exempt
def goto_post(request):
    response = ""
    if request.GET['source'] == 'habr':
        response = Habr.objects.filter(id=request.GET['id'])[0].to_dict()
    return render(request, 'board/post.html', {'data': response})

def main_render(request):
    return render(request, 'board/main.html')