from django.urls import path

from .views import *


urlpatterns = [
    path('', main_render),
    path('filter-changed', PostsListView.as_view()),
    path('post/<str:source>/<int:pk>', PostDetailView.as_view())
]
