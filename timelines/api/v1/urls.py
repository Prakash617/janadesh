from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimelineViewSet

app_name = 'timeline-api-v1'

router = DefaultRouter()
router.register(r'', TimelineViewSet, basename='timeline')

urlpatterns = [
    path('', include(router.urls)),
]
