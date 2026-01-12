from django.contrib import admin
from .models import SEOMetadata


@admin.register(SEOMetadata)
class SEOMetadataAdmin(admin.ModelAdmin):
    # 🚨 THIS LINE IS THE KEY FIX
    exclude = ("content_object",)

    list_display = (
        "id",
        "content_type",
        "object_id",
        "meta_title_en",
        "robots",
        "updated_at",
    )

    list_filter = ("content_type", "robots")

    search_fields = (
        "meta_title_en",
        "meta_title_np",
        "meta_description_en",
        "meta_description_np",
        "keywords",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Target Object", {
            "fields": ("content_type", "object_id"),
        }),
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
            "fields": ("keywords", "canonical_url", "robots"),
        }),
        # ("Timestamps", {
        #     "fields": ("created_at", "updated_at"),
        # }),
    )
