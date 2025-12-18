from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('Users.urls')),
    path('api/v1/', include('Categories.urls')),
    path('api/v1/', include('Transactions.urls')) ,

]
