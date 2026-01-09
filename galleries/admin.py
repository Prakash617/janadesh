from django.contrib import admin
from .models import Gallery, GalleryImage

# Register your models here.

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured',)
    list_editable = ('is_featured', 'order')
    search_fields = ('title_en', 'title_np', 'description_en', 'description_np')
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)

# GalleryImage does not need a separate admin registration as it's an inline
