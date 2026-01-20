from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SEOMetadata


@admin.register(SEOMetadata)
class SEOMetadataAdmin(admin.ModelAdmin):
    # 🚨 THIS LINE IS THE KEY FIX
    exclude = ("content_object",)

    list_display = (
        "id",
        # "content_type",
        # "object_id",
        "meta_title_en",
        # "robots",
        "updated_at",
        "action_buttons",
    )

    # list_filter = ["content_type"]

    search_fields = (
        "meta_title_en",
        "meta_title_np",
        "meta_description_en",
        "meta_description_np",
        "keywords",
    )
    exclude = ("robots",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        # ("Target Object", {
        #     "fields": ("content_type", "object_id"),
        # }),
        ("Meta (EN)", {
            "fields": ("meta_title_en", "meta_description_en"),
        }),
        ("Meta (NP)", {
            "fields": ("meta_title_np", "meta_description_np"),
        }),
        ("Open Graph", {
            "fields": (
                "og_title_en",
                "og_title_np",
                "og_description_en",
                "og_description_np",
                "og_image",
            ),
        }),
        ("SEO Advanced", {
            "fields": ("keywords", "canonical_url"),
        }),
        # ("Timestamps", {
        #     "fields": ("created_at", "updated_at"),
        # }),
    )

    def action_buttons(self, obj):
        edit_url = reverse('admin:seo_seometadata_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'
