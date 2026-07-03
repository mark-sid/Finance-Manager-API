from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import HealthCheckView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('Categories.urls')),
    path('api/v1/', include('Transactions.urls')),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('health/', HealthCheckView.as_view(), name='health-check'),

]
