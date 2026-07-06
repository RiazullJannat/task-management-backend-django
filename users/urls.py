from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),

    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]