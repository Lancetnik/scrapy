from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Documnets Cloud API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://127.0.0.1:8000",
      contact=openapi.Contact(email="diementros@gmail.com"),
      license=openapi.License(name="My License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('crawl/', include('crawlers.urls')),

   path('admin/', admin.site.urls),
   path('api/', include('rest_framework.urls')),
   # token auth
   path('auth/', include('djoser.urls')),
   path('auth/', include('djoser.urls.authtoken')),
   path('auth/', include('djoser.urls.jwt')),
   # jwt auth
   path('api/token/', TokenObtainPairView.as_view()),
   path('api/token/refresh/', TokenRefreshView.as_view()),
   path('api/token/verify/', TokenVerifyView.as_view()),
] + [
   path('swagger(?<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0)),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]