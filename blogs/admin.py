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

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title_en', 'category', 'author',
        'status', 'is_featured',
        'view_count', 'published_at', 'created_at'
    )
    list_filter = ('status', 'is_featured', 'category', 'author')
    list_editable = ('status', 'is_featured')
    search_fields = ('title_en', 'title_np', 'content_en', 'content_np')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'

    exclude = ('created_at', 'updated_at')
    readonly_fields = ('view_count',)  # ✅ only this


