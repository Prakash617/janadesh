from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogCategory, BlogTag, Blog, Comment


# ============================
# USER
# ============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


# ============================
# BLOG CATEGORY
# ============================
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = [
            'id',
            'name_en',
            'name_np',
            'slug',
            'description_en',
            'description_np',
        ]


# ============================
# BLOG TAG
# ============================
class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = [
            'id',
            'name_en',
            'name_np',
            'slug',
        ]


# ============================
# BLOG LIST
# ============================
class BlogListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id',
            'title_en',
            'title_np',
            'slug',
            'excerpt_en',
            'excerpt_np',
            'featured_image',
            'category',
            'tags',
            'author',
            'status',
            'is_featured',
            'view_count',
            'published_at',
        ]


# ============================
# BLOG DETAIL
# ============================
class BlogDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id',
            'title_en',
            'title_np',
            'slug',
            'content_en',
            'content_np',
            'excerpt_en',
            'excerpt_np',
            'featured_image',
            'category',
            'tags',
            'author',
            'status',
            'is_featured',
            'view_count',
            'published_at',
            'created_at',
            'updated_at',
        ]


# ============================
# RECURSIVE COMMENTS
# ============================
class RecursiveCommentSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CommentSerializer(value, context=self.context)
        return serializer.data


# ============================
# COMMENT READ
# ============================
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'blogs',
            'parent',
            'content',
            'status',
            'created_at',
            'replies',
        ]
        read_only_fields = ['status']


# ============================
# COMMENT CREATE
# ============================
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'blogs',
            'parent',
            'content',
        ]
