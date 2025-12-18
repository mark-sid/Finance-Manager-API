from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path

router = SimpleRouter()
router.register(r'transaction', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('transactions/stats/', views.TransactionStatsAPIView.as_view(), name='transactions_stats')
]

urlpatterns += router.urls
