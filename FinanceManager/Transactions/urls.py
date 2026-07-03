from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path

router = SimpleRouter()
router.register(r'transaction', views.TransactionViewSet, basename='transaction')
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')

urlpatterns = router.urls
