from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.BlogCategoryViewSet, basename='category')
router.register(r'posts', views.BlogPostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment') # Top-level comments endpoint

urlpatterns = [
    path('', include(router.urls)),
]
