from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.html import format_html
import json

from .models import AnalyticsEvent

class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'object_type', 'object_id', 'url', 'ip_address', 'created_at')
    list_filter = ('event_type', 'object_type', 'created_at')
    readonly_fields = ('event_type', 'object_type', 'object_id', 'url', 'referrer', 'ip_address', 'user_agent', 'session_id', 'language', 'country', 'city', 'created_at')

    change_list_template = "admin/analytics_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        # ---- Summary Cards ----
        total_events = AnalyticsEvent.objects.count()
        total_page_views = AnalyticsEvent.objects.filter(event_type='page_view').count()
        total_blog_views = AnalyticsEvent.objects.filter(event_type='blog_view').count()
        total_campaign_views = AnalyticsEvent.objects.filter(event_type='campaign_view').count()
        total_downloads = AnalyticsEvent.objects.filter(event_type='download').count()
        total_form_submits = AnalyticsEvent.objects.filter(event_type='form_submit').count()

        summary_cards = {
            'total_events': total_events,
            'total_page_views': total_page_views,
            'total_blog_views': total_blog_views,
            'total_campaign_views': total_campaign_views,
            'total_downloads': total_downloads,
            'total_form_submits': total_form_submits,
        }

        # ---- Bar Chart: Events by type ----
        events_by_type = AnalyticsEvent.objects.values('event_type').annotate(count=Count('id'))
        bar_chart_data = {
            'labels': [e['event_type'] for e in events_by_type],
            'data': [e['count'] for e in events_by_type]
        }

        # ---- Line Chart: Daily Events ----
        daily_events = AnalyticsEvent.objects.annotate(date=TruncDate('created_at')) \
                                             .values('date') \
                                             .annotate(count=Count('id')) \
                                             .order_by('date')
        line_chart_data = {
            'labels': [str(e['date']) for e in daily_events],
            'data': [e['count'] for e in daily_events]
        }

        # ---- Pie Chart: Top 10 URLs ----
        top_urls = AnalyticsEvent.objects.values('url').annotate(count=Count('id')).order_by('-count')[:10]
        pie_chart_data = {
            'labels': [e['url'] for e in top_urls],
            'data': [e['count'] for e in top_urls]
        }

        extra_context = extra_context or {}
        extra_context.update({
            'summary_cards': summary_cards,
            'bar_chart_data': json.dumps(bar_chart_data),
            'line_chart_data': json.dumps(line_chart_data),
            'pie_chart_data': json.dumps(pie_chart_data),
        })

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(AnalyticsEvent, AnalyticsEventAdmin)
