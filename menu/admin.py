from django.contrib import admin
from .models import Menu, MenuItem

# Register your models here.

class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 0
    autocomplete_fields = ["page"]
    fields = (
        "label_en",
        "page",
        "url",
        "parent",
        "order",
        "icon",
        "is_external",
        "open_new_tab",
        "is_active",
    )
    ordering = ("order",)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('location', 'is_active')
    search_fields = ('name',)
    exclude = ('created_at', 'updated_at')
    inlines = [MenuItemInline]

admin.site.register(Menu, MenuAdmin)

# MenuItem does not need a separate admin registration as it's an inline
