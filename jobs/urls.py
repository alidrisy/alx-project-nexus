from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, JobViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
] 