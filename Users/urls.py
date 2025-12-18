from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/profile/update/', views.UserUpdateView.as_view(), name='user_profile_update'),
    path('user/password/update/', views.UserPasswordUpdateView.as_view(), name='user_password_update'),
    path('user/delete/', views.UserDeleteView.as_view(), name='user_delete')
]
