from django.urls import path

from .views import *


urlpatterns = [
    path('', main_render),
    path('filter-changed', get_posts),
    path('post', goto_post)
]
