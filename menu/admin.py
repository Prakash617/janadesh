from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
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
    list_display = ('name', 'location', 'is_active', 'created_at', 'action_buttons')
    list_filter = ('location', 'is_active')
    search_fields = ('name',)
    exclude = ('created_at', 'updated_at')
    inlines = [MenuItemInline]

    def action_buttons(self, obj):
        edit_url = reverse('admin:menu_menu_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="padding:4px 10px; background-color:#28A745; color:white; '
            'border-radius:5px; text-decoration:none; margin-right:5px; font-weight:bold;">Edit</a>',
            edit_url
        )
    action_buttons.short_description = 'Actions'

admin.site.register(Menu, MenuAdmin)

# MenuItem does not need a separate admin registration as it's an inline
