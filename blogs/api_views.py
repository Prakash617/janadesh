from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BlogCategory, BlogTag, Blog, Comment
from .serializers import (
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogListSerializer,
    BlogDetailSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


# ============================
# BLOG CATEGORY
# ============================
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


# ============================
# BLOG TAG
# ============================
class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


# ============================
# BLOG
# ============================
class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Blog.objects.select_related(
            'category',
            'author'
        ).prefetch_related('tags')

        if not self.request.user.is_staff:
            qs = qs.filter(status='published')

        return qs

    def get_serializer_class(self):
        return BlogListSerializer if self.action == 'list' else BlogDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Blog.objects.filter(id=instance.id).update(
            view_count=instance.view_count + 1
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            published_at=timezone.now()
        )


# ============================
# COMMENT
# ============================
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            parent__isnull=True,
            status='approved'
        ).select_related('user').prefetch_related('replies')

    def get_serializer_class(self):
        return CommentCreateSerializer if self.action == 'create' else CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status='pending'
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.AllowAny]
    )
    def blog_comments(self, request):
        blog_slug = request.query_params.get('slug')
        if not blog_slug:
            return Response(
                {"error": "Blog slug is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        comments = Comment.objects.filter(
            blogs__slug=blog_slug,
            parent__isnull=True,
            status='approved'
        ).select_related('user').prefetch_related('replies')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
