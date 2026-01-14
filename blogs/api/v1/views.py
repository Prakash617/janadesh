from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from janadesh.filters import LimitFilter

from blogs.filters import BlogFilter
from blogs.models import BlogCategory, BlogTag, Blog, Comment
from .serializers import (
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogListSerializer,
    BlogDetailSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


# ============================
# BLOG CATEGORY
# ============================
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


# ============================
# BLOG TAG
# ============================
class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


# ============================
# BLOG
# ============================
class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    filter_backends = [DjangoFilterBackend, LimitFilter]
    filterset_class = BlogFilter

    def get_queryset(self):
        qs = Blog.objects.select_related("category", "author").prefetch_related("tags")

        if not self.request.user.is_staff:
            qs = qs.filter(status="published")

        return qs

    def get_serializer_class(self):
        return BlogListSerializer if self.action == "list" else BlogDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Blog.objects.filter(id=instance.id).update(view_count=instance.view_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

        

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="slug",
                description="Blog slug",
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        responses=BlogListSerializer(many=True),
    )
    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def related(self, request, slug=None):
        blog = self.get_object()

        tag_ids = blog.tags.values_list("id", flat=True)

        # 1️⃣ Tag-based related blogs (highest priority)
        tag_related = (
            Blog.objects.filter(status="published", tags__in=tag_ids)
            .exclude(id=blog.id)
            .annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-published_at")
        )

        # 2️⃣ Category-based related blogs (fallback)
        category_related = (
            Blog.objects.filter(status="published", category=blog.category)
            .exclude(Q(id=blog.id) | Q(id__in=tag_related.values_list("id", flat=True)))
            .order_by("-published_at")
        )

        # 3️⃣ Combine results
        related_blogs = list(tag_related[:3]) + list(category_related[:3])

        serializer = BlogListSerializer(related_blogs, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.AllowAny],
        url_path="featured",
    )
    def featured(self, request):
        try:
            limit = int(request.query_params.get("limit", 5))
        except ValueError:
            limit = 5

        featured_blogs = Blog.objects.filter(
            status="published", is_featured=True
        ).order_by("-published_at")[:limit]

        serializer = BlogListSerializer(featured_blogs, many=True)
        return Response(serializer.data)


# ============================
# COMMENT
# ============================
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Comment.objects.filter(parent__isnull=True, status="approved")
            .select_related("user")
            .prefetch_related("replies")
        )

    def get_serializer_class(self):
        return CommentCreateSerializer if self.action == "create" else CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def blog_comments(self, request):
        blog_slug = request.query_params.get("slug")
        if not blog_slug:
            return Response(
                {"error": "Blog slug is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        comments = (
            Comment.objects.filter(
                blogs__slug=blog_slug, parent__isnull=True, status="approved"
            )
            .select_related("user")
            .prefetch_related("replies")
        )

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
