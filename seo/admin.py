from django.contrib import admin
from .models import SEOMetadata

# Register your models here.
class SEOMetadataAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'meta_title_en', 'canonical_url', 'robots', 'created_at')
    list_filter = ('robots', 'created_at')
    search_fields = ('meta_title_en', 'meta_description_en', 'keywords', 'canonical_url')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('content_type', 'object_id', 'content_object')
        }),
        ('Meta Tags', {
            'fields': ('meta_title_en', 'meta_title_np', 'meta_description_en', 'meta_description_np', 'keywords')
        }),
        ('Open Graph', {
            'fields': ('og_title_en', 'og_title_np', 'og_description_en', 'og_description_np', 'og_image')
        }),
        ('Advanced', {
            'fields': ('canonical_url', 'robots')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(SEOMetadata, SEOMetadataAdmin)
