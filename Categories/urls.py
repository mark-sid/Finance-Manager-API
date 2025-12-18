from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'category', views.CategoryViewSet, basename='category')

urlpatterns = router.urls
