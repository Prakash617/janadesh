from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogCategoryViewSet,
    BlogTagViewSet,
    BlogViewSet,
    CommentViewSet
)

app_name = 'blogs-api-v1'

router = DefaultRouter()
router.register(r'categories', BlogCategoryViewSet, basename='blog-category')
router.register(r'tags', BlogTagViewSet, basename='blog-tag')
router.register(r'', BlogViewSet, basename='blog')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
