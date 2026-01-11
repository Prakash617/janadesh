from janadesh.api.router import router

from .views import (
    BlogCategoryViewSet,
    BlogTagViewSet,
    BlogViewSet,
    CommentViewSet,
)

app_name = "blogs-api-v1"


# Blogs
router.register("blogs", BlogViewSet, basename="blog")

# Blog metadata
router.register("blogs/categories", BlogCategoryViewSet, basename="blog-category")
router.register("blogs/tags", BlogTagViewSet, basename="blog-tag")

# Blog comments
router.register("blogs/comments", CommentViewSet, basename="blog-comment")
