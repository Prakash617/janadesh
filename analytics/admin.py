from django.contrib import admin
from django.urls import path, reverse
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.html import format_html
from django.template.response import TemplateResponse
import json

from .models import AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = (
        'event_type',
        'object_type',
        'object_id',
        'url',
        'ip_address',
        'created_at',
        'action_buttons',
    )

    list_filter = ('event_type', 'object_type', 'created_at')

    readonly_fields = (
        'event_type',
        'object_type',
        'object_id',
        'url',
        'referrer',
        'ip_address',
        'user_agent',
        'session_id',
        'language',
        'country',
        'city',
        'created_at',
    )

    # change_list_template = "admin/analytics_changelist.html"

    # -----------------------------
    # Custom buttons
    # -----------------------------
    def action_buttons(self, obj):
        edit_url = reverse(
            'admin:analytics_analyticsevent_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}" class="button">Edit</a>',
            edit_url
        )

    action_buttons.short_description = "Actions"

    # -----------------------------
    # Add custom admin URL
    # -----------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_site.admin_view(self.dashboard_view),
                name="analytics-dashboard",
            ),
        ]
        return custom_urls + urls

    # -----------------------------
    # Dashboard logic (shared)
    # -----------------------------
    def get_dashboard_context(self):
        total_events = AnalyticsEvent.objects.count()

        summary_cards = {
            'total_events': total_events,
            'total_page_views': AnalyticsEvent.objects.filter(event_type='page_view').count(),
            'total_blog_views': AnalyticsEvent.objects.filter(event_type='blog_view').count(),
            'total_campaign_views': AnalyticsEvent.objects.filter(event_type='campaign_view').count(),
            'total_downloads': AnalyticsEvent.objects.filter(event_type='download').count(),
            'total_form_submits': AnalyticsEvent.objects.filter(event_type='form_submit').count(),
        }

        events_by_type = AnalyticsEvent.objects.values('event_type').annotate(
            count=Count('id')
        )

        daily_events = (
            AnalyticsEvent.objects
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        top_urls = (
            AnalyticsEvent.objects.values('url')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        return {
            'summary_cards': summary_cards,
            'bar_chart_data': json.dumps({
                'labels': [e['event_type'] for e in events_by_type],
                'data': [e['count'] for e in events_by_type],
            }),
            'line_chart_data': json.dumps({
                'labels': [str(e['date']) for e in daily_events],
                'data': [e['count'] for e in daily_events],
            }),
            'pie_chart_data': json.dumps({
                'labels': [e['url'] for e in top_urls],
                'data': [e['count'] for e in top_urls],
            }),
        }

    # -----------------------------
    # Standalone iframe view
    # -----------------------------
    def dashboard_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            **self.get_dashboard_context(),
            title="Analytics Dashboard",
            iframe_mode=True,
        )

        return TemplateResponse(
            request,
            "admin/analytics_dashboard_iframe.html",
            context,
        )
