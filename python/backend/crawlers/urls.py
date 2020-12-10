from django.urls import path
from django.urls import include

from . import views


urlpatterns = [
    path('start/', views.StartCrawlerView.as_view()),

    path("", views.HabrListView.as_view()),
    path("<int:pk>/", views.HabrRetrieveView.as_view()),
]