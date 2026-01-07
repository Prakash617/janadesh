from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from blogs.models import BlogCategory, Blog, Comment
from .serializers import BlogCategorySerializer, BlogPostSerializer, CommentSerializer

class BlogCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blog categories to be viewed or edited.
    """
    queryset = BlogCategory.objects.all().order_by('name_en')
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name_en', 'name_np']
    ordering_fields = ['name_en', 'created_at']


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blog posts to be viewed or edited.
    """
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title_en', 'title_np', 'content_en', 'content_np']
    ordering_fields = ['published_at', 'created_at', 'title_en', 'view_count']
    filterset_fields = ['category__slug', 'tags__slug', 'status', 'is_featured', 'author__username']

    def get_queryset(self):
        queryset = Blog.objects.select_related('category', 'author').prefetch_related('tags').all()
        # For unauthenticated users, only show published posts
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset

    def perform_create(self, serializer):
        # Set the author to the current user
        if self.request.user.is_authenticated:
            # For staff users, allow setting the status, otherwise default to draft
            if self.request.user.is_staff:
                status = serializer.validated_data.get('status', 'draft') # Allow explicit status
            else:
                status = 'draft' # Non-staff users always create as draft

            serializer.save(author=self.request.user, status=status)
        else:
            # If for some reason an unauthenticated user gets here, prevent creation
            raise Response({"detail": "Authentication credentials were not provided."},
                           status=status.HTTP_401_UNAUTHORIZED)
        
    def perform_update(self, serializer):
        # Allow staff users to update status, otherwise preserve existing status
        if not self.request.user.is_staff and 'status' in serializer.validated_data:
            del serializer.validated_data['status']
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed, created, edited or deleted.
    Can be nested under a blog post or accessed directly.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Comment.objects.select_related('user', 'blogs').all()
        blog_slug = self.request.query_params.get('blog_slug', None) # Get from query params
        if blog_slug:
            queryset = queryset.filter(blogs__slug=blog_slug)
        
        # For unauthenticated users, only show approved comments
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='approved')
        return queryset

    def perform_create(self, serializer):
        blog_slug = self.request.query_params.get('blog_slug', None) # Get from query params
        blog_instance = None
        if blog_slug:
            blog_instance = get_object_or_404(Blog, slug=blog_slug)
        
        if not blog_instance and 'blogs' not in serializer.validated_data:
            # This case should ideally be prevented by frontend or URL design
            raise Response({"detail": "Blog post is required for a comment. Provide 'blogs' ID or 'blog_slug' in query parameter."},
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Set the author to the current user
        # Non-staff users create comments with 'pending' status
        # Staff users can set the status, or it defaults to 'approved'
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                comment_status = serializer.validated_data.get('status', 'approved')
            else:
                comment_status = 'pending'
            
            serializer.save(user=self.request.user, blogs=blog_instance, status=comment_status)
        else:
             raise Response({"detail": "Authentication credentials were not provided."},
                           status=status.HTTP_401_UNAUTHORIZED)
    
    def perform_update(self, serializer):
        # Only staff can change the status of a comment
        if not self.request.user.is_staff and 'status' in serializer.validated_data:
            # Remove status from validated_data if non-staff user tries to change it
            del serializer.validated_data['status']
        serializer.save()

    def perform_destroy(self, instance):
        # Only author or staff can delete a comment
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise Response({"detail": "You do not have permission to delete this comment."},
                           status=status.HTTP_403_FORBIDDEN)
