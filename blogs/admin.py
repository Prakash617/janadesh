from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, Comment

# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_np', 'slug', 'created_at')
    search_fields = ('name_en', 'name_np')
    prepopulated_fields = {'slug': ('name_en',)}

admin.site.register(BlogCategory, BlogCategoryAdmin)

class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_np', 'slug', 'created_at')
    search_fields = ('name_en', 'name_np')
    prepopulated_fields = {'slug': ('name_en',)}

admin.site.register(BlogTag, BlogTagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blogs', 'parent', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'content')
    raw_id_fields = ('user', 'blogs', 'parent')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Comment, CommentAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'author', 'status', 'is_featured', 'view_count', 'published_at', 'created_at')
    list_filter = ('status', 'is_featured', 'category', 'author')
    search_fields = ('title_en', 'title_np', 'content_en', 'content_np')
    prepopulated_fields = {'slug': ('title_en',)}
    raw_id_fields = ('author',) # Assuming author is a User model
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_np', 'slug', 'featured_image', 'content_en', 'content_np', 'excerpt_en', 'excerpt_np')
        }),
        ('Categorization', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Publication', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'view_count'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Blog, BlogAdmin)
