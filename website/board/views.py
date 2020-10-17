import requests
from bs4 import BeautifulSoup as BS

from django.shortcuts import render
from  django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def get_posts(request):
    response = HabrPost.all()
    return JsonResponse(response, safe=False)

def main_render(request):
    return render(request, 'board/main.html')