from django.contrib import admin
from django.urls import path
from .views import RegisterView
from .serializers import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]