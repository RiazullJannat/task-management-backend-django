from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ImageViewSet, AnnotationViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'annotations', AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('', include(router.urls)),
]
