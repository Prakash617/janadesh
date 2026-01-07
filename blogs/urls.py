from django.urls import path, include

from janadesh.urls import router

from .api_views import (
    BlogCategoryViewSet,
    BlogTagViewSet,
    BlogViewSet,
    CommentViewSet
)
app_name = 'blogs'

router.register(r'categories', BlogCategoryViewSet, basename='blog-category')
router.register(r'tags', BlogTagViewSet, basename='blog-tag')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
