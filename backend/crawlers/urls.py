from django.urls import path

from . import views


urlpatterns = [
    path('start/', views.StartCrawlerView.as_view()),
    path('construct/', views.ConstructSpiderView.as_view()),
]