from rest_framework import serializers
from blogs.models import BlogCategory, BlogTag, Blog, Comment
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        extra_kwargs = {'url': {'lookup_field': 'slug'}} # For URL-based lookups in generated Swagger

class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username', 'email', 'first_name', 'last_name') # Make these read-only for security

class BlogPostSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_slug = serializers.SlugField(write_only=True, allow_null=True, required=False) # For creating/updating via slug
    tags = BlogTagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True, required=False) # For creating/updating via tag names
    author = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True) # To display human-readable status

    class Meta:
        model = Blog
        fields = [
            'id', 'title_en', 'title_np', 'slug', 'content_en', 'content_np',
            'excerpt_en', 'excerpt_np', 'featured_image', 'category', 'category_slug',
            'tags', 'tag_names', 'author', 'status', 'status_display', 'is_featured', 'view_count',
            'published_at', 'created_at', 'updated_at', 'comments_count'
        ]
        read_only_fields = ['slug', 'author', 'view_count', 'published_at', 'created_at', 'updated_at']
        extra_kwargs = {'url': {'lookup_field': 'slug'}} # For URL-based lookups in generated Swagger

    def get_comments_count(self, obj):
        return obj.comments.filter(status='approved').count()

    def create(self, validated_data):
        category_slug = validated_data.pop('category_slug', None)
        tag_names = validated_data.pop('tag_names', [])
        
        # Auto-set slug if not provided, based on title_en
        if 'title_en' in validated_data and not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data['title_en'])

        blog = Blog.objects.create(**validated_data)

        if category_slug:
            try:
                category = BlogCategory.objects.get(slug=category_slug)
                blog.category = category
            except BlogCategory.DoesNotExist:
                raise serializers.ValidationError({"category_slug": "Category with this slug does not exist."})

        if tag_names:
            tags = []
            for tag_name in tag_names:
                # Ensure slug for new tags
                tag, created = BlogTag.objects.get_or_create(
                    name_en=tag_name,
                    defaults={'slug': slugify(tag_name)}
                )
                tags.append(tag)
            blog.tags.set(tags)
        
        # Author should be set by the view using request.user
        # blog.author = self.context['request'].user # Moved to viewset perform_create
        blog.save()
        return blog

    def update(self, instance, validated_data):
        category_slug = validated_data.pop('category_slug', None)
        tag_names = validated_data.pop('tag_names', [])

        # Prevent slug modification if not explicitly allowed or handled
        if 'slug' in validated_data:
            if validated_data['slug'] != instance.slug and not self.context['request'].user.is_superuser: # Example permission
                 raise serializers.ValidationError({"slug": "Slug cannot be changed directly."})

        instance = super().update(instance, validated_data)

        if category_slug is not None: # Check for None to distinguish from empty string
            try:
                category = BlogCategory.objects.get(slug=category_slug)
                instance.category = category
            except BlogCategory.DoesNotExist:
                raise serializers.ValidationError({"category_slug": "Category with this slug does not exist."})
        elif 'category_slug' in self.initial_data: # If category_slug was explicitly passed as empty/null
            instance.category = None

        if tag_names is not None: # Check for None to distinguish from empty list
            tags = []
            for tag_name in tag_names:
                tag, created = BlogTag.objects.get_or_create(
                    name_en=tag_name,
                    defaults={'slug': slugify(tag_name)}
                )
                tags.append(tag)
            instance.tags.set(tags)
        elif 'tag_names' in self.initial_data: # If tag_names was explicitly passed as empty list
            instance.tags.clear()
            
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    blog_slug = serializers.SlugField(write_only=True, required=False, help_text="Slug of the blog post this comment belongs to.")
    status_display = serializers.CharField(source='get_status_display', read_only=True) # To display human-readable status


    class Meta:
        model = Comment
        fields = ['id', 'user', 'blogs', 'blog_slug', 'parent', 'content', 'status', 'status_display', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'blogs': {'write_only': True, 'required': False}, # blogs will be set by view or blog_slug
            'parent': {'allow_null': True, 'required': False}
        }

    def create(self, validated_data):
        blog_slug = validated_data.pop('blog_slug', None)
        blog = validated_data.pop('blogs', None) # Get blog from validated data if present

        if not blog and blog_slug:
            try:
                blog = Blog.objects.get(slug=blog_slug)
            except Blog.DoesNotExist:
                raise serializers.ValidationError({"blog_slug": "Blog post with this slug does not exist."})
        elif not blog and not blog_slug:
            # This case should ideally be handled by the view for nested comments or explicit blog assignment
            raise serializers.ValidationError({"blogs": "Blog post is required for a comment."})

        validated_data['user'] = self.context['request'].user
        validated_data['blogs'] = blog
        
        # Comments are created with 'pending' status by default
        if 'status' not in validated_data:
            validated_data['status'] = 'pending'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('blog_slug', None) # blog_slug is not for updating
        validated_data.pop('blogs', None) # blog is not for updating
        return super().update(instance, validated_data)
