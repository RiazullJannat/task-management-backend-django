from django.contrib import admin
from django.urls import path, include

from .views import api_root, health_check

urlpatterns = [
    path('', api_root, name='api-root'),
    path('health', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('annotations/', include('annotations.urls'))
]