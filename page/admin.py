from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    # Columns in the list view
    list_display = (
        "title",
        "slug",
        "status",
        "is_published",
        "published_at",
        "created_at",
        "updated_at",
        "action_buttons",
    )
    
    # Make 'status' editable directly in the list view
    list_editable = ("status",)
    
    # Filters
    list_filter = ("status", "created_at", "published_at")
    
    # Searchable fields
    search_fields = ("title", "slug", "meta_description", "seo_title")
    
    # Ordering
    ordering = ("-created_at",)
    
    # Fields shown in the add/edit form
    fieldsets = (
        (None, {
            "fields": (
                "title",
                "slug",
                "content",
                "excerpt",
                "featured_image",
            )
        }),
        ("SEO & Metadata", {
            "fields": ("seo_title", "meta_description", "keywords"),
        }),
        ("Publishing", {
            "fields": ("status", "published_at"),
        }),
    )
    
    # Auto-populate slug from title
    prepopulated_fields = {"slug": ("title",)}
    
    # Readonly timestamps
    readonly_fields = ("created_at", "updated_at")
    
    # Optional: show a thumbnail preview of featured image
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 100px; height:auto;" />', obj.featured_image.url
            )
        return "-"
    featured_image_preview.short_description = "Image Preview"
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:page_page_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

    # Include the thumbnail in list_display if desired
    # list_display += ("featured_image_preview",)
