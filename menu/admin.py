from django.contrib import admin
from .models import Menu, MenuItem

# Register your models here.

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('parent', 'label_en', 'label_np', 'url', 'order', 'icon', 'is_external', 'open_new_tab', 'is_active')
    raw_id_fields = ('parent',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('location', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MenuItemInline]

admin.site.register(Menu, MenuAdmin)

# MenuItem does not need a separate admin registration as it's an inline
